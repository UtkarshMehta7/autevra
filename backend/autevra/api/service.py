"""Workspace service: the one place where commands, persistence and CAD meet.

All mutations and CAD builds run under one lock: the kernel is used from a
single thread at a time and jobs stay sequential (8 GB memory budget).
"""

import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from autevra.ai import interpreter
from autevra.ai.llm.clients import DisabledClient, LLMClient
from autevra.ai.rule_parser import Kind, TestRequest
from autevra.api import model_service, schemas
from autevra.assembly import graph
from autevra.cad.cache import GeometryCache
from autevra.domain import derived, parameters
from autevra.domain.commands import CommandError, SetParameters, Source
from autevra.domain.design import ApplyResult, CommandRejectedError, DesignState
from autevra.domain.rules import validate
from autevra.engineering import diagnosis as dgn
from autevra.engineering import integration
from autevra.engineering import loop as eloop
from autevra.engineering import optimize as opt
from autevra.engineering import testing as tst
from autevra.storage.database import Database
from autevra.storage.repository import ProjectInfo, ProjectRepository
from autevra.storage.runs import RunRepository, StudyRepository


def _derived(values: dict[str, float]) -> list[schemas.DerivedValue]:
    computed = derived.compute_all(values)
    return [
        schemas.DerivedValue(
            id=d.id,
            label=d.label,
            unit=d.unit,
            value=round(computed[d.id], 3),
            controlled_by=d.controlled_by,
        )
        for d in derived.DERIVED.values()
    ]


def _state(info: ProjectInfo, state: DesignState) -> schemas.ProjectState:
    return schemas.ProjectState(
        id=info.id,
        name=info.name,
        created_at=info.created_at,
        updated_at=info.updated_at,
        values=state.values,
        derived=_derived(state.values),
        can_undo=state.can_undo,
        can_redo=state.can_redo,
        history_length=len(state.history),
        cursor=state.cursor,
    )


def _result(state: DesignState, applied: ApplyResult) -> schemas.CommandResult:
    return _command_result(state, applied.changed, applied.entry)


def _command_result(state: DesignState, changed: Iterable[str], entry) -> schemas.CommandResult:  # type: ignore[no-untyped-def]
    changed = list(changed)
    impact = graph.impact(changed)
    retest = [f"{t}:{target}" for t, target in tst.tests_affected(changed)]
    return schemas.CommandResult(
        changed=changed,
        values=state.values,
        impact=schemas.ImpactOut(
            rebuild=sorted(impact.rebuild), move=sorted(impact.move), retest=retest
        ),
        entry=entry,
        can_undo=state.can_undo,
        can_redo=state.can_redo,
    )


def _entry_id(state: DesignState, cursor: int) -> str | None:
    return state.history[cursor - 1].id if cursor > 0 else None


def _run_message(run: tst.RunRecord, comparison: tst.Comparison | None) -> str:
    head = f"{run.target.capitalize()} {run.test_name.lower()}, {run.scenario['label']}: "
    verdict = run.status.value.replace("_", " ")
    failed = [
        f"{c.label.lower()} ({c.measured:.3g} vs {c.comparator} {c.limit:.3g} {c.unit}".rstrip()
        + ")"
        for c in run.criteria
        if c.passed is False and c.measured is not None
    ]
    text = head + verdict + (": " + "; ".join(failed) if failed else "")
    if comparison is not None:
        moved = [m for m in comparison.metrics if m.verdict in ("better", "worse")][:3]
        if moved:
            text += ". Compared with before: " + ", ".join(
                f"{m.label.lower()} {m.before:.3g} → {m.after:.3g} {m.unit} ({m.verdict})"
                for m in moved
            )
    return text + "."


def _study_message(result: opt.StudyResult, label: str) -> str:
    target = result.study.target.capitalize()
    n = result.evaluations
    if result.status == "no_feasible_design" or result.best is None:
        why = f" Blocking: {result.blocking}." if result.blocking else ""
        return f"{target}: no design met every criterion within the bounds ({n} evaluations).{why}"
    metric = result.study.objectives[0].metric
    change = result.improvement.get(metric)
    base = result.baseline.objectives.get(metric)
    best = result.best.objectives[metric]
    pct = f" ({change / base * 100:+.1f} %)" if change is not None and base else ""
    moves = ", ".join(
        f"{c.parameter} {c.value:g}" for c in (result.command.changes if result.command else ())
    )
    return (
        f"{target}: worst-case {label} {base:.3g} → {best:.3g}{pct} with "
        f"{moves or 'no change'}; verified with full runs ({n} evaluations)."
    )


def _loop_message(result: eloop.LoopResult) -> str:
    target = result.goal.target.capitalize()
    steps = "; ".join(it.decision for it in result.iterations)
    outcome = result.outcome.replace("_", " ")
    return f"{target}: {outcome} after {len(result.iterations)} iteration(s): {steps}."


def _format(pid: str, values: dict[str, float]) -> str:
    if pid in parameters.REGISTRY:
        spec = parameters.REGISTRY[pid]
        return f"{spec.label}: {values[pid]:g} {spec.unit}"
    spec = derived.DERIVED[pid]
    return f"{spec.label}: {derived.compute(pid, values):.1f} {spec.unit}"


PROPOSAL_TTL_S = 15 * 60


@dataclass(frozen=True)
class _Proposal:
    project_id: str
    command: SetParameters
    created: float


class ProposalNotFoundError(LookupError):
    pass


class Workspace:
    def __init__(self, db: Database, data_dir: Path, llm: LLMClient | None = None) -> None:
        self.db = db
        self.data_dir = data_dir
        self.llm: LLMClient = llm or DisabledClient()
        self.cache = GeometryCache()
        self._clearances = integration.ClearanceCache()
        self._lock = threading.RLock()
        # LLM proposals awaiting confirmation; in memory, they expire and do not survive restarts.
        self._proposals: dict[str, _Proposal] = {}

    # --- projects ---
    def create_project(self, name: str) -> schemas.ProjectState:
        with self.db.session() as s:
            repo = ProjectRepository(s)
            info = repo.create(name)
            return _state(info, repo.load(info.id))

    def list_projects(self) -> list[schemas.ProjectSummary]:
        with self.db.session() as s:
            return [schemas.ProjectSummary(**vars(i)) for i in ProjectRepository(s).list()]

    def project(self, project_id: str) -> schemas.ProjectState:
        with self.db.session() as s:
            repo = ProjectRepository(s)
            return _state(repo.info(project_id), repo.load(project_id))

    def rename(self, project_id: str, name: str) -> schemas.ProjectState:
        with self.db.session() as s:
            repo = ProjectRepository(s)
            info = repo.rename(project_id, name)
            return _state(info, repo.load(project_id))

    def delete(self, project_id: str) -> None:
        with self.db.session() as s:
            ProjectRepository(s).delete(project_id)

    def history(self, project_id: str) -> schemas.HistoryOut:
        with self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            return schemas.HistoryOut(entries=state.history, cursor=state.cursor)

    # --- commands ---
    def apply(self, project_id: str, command: SetParameters) -> schemas.CommandResult:
        """Validate and apply; raises CommandRejectedError (state untouched) or CommandError."""
        with self._lock, self.db.session() as s:
            repo = ProjectRepository(s)
            state = repo.load(project_id)
            applied = state.apply(command)
            repo.save(project_id, state)
            return _result(state, applied)

    def undo(self, project_id: str) -> schemas.CommandResult:
        return self._step(project_id, redo=False)

    def redo(self, project_id: str) -> schemas.CommandResult:
        return self._step(project_id, redo=True)

    def _step(self, project_id: str, redo: bool) -> schemas.CommandResult:
        with self._lock, self.db.session() as s:
            repo = ProjectRepository(s)
            state = repo.load(project_id)
            entry = state.redo() if redo else state.undo()
            repo.save(project_id, state)
            changed = [c.parameter for c in entry.changes] if entry else []
            return _command_result(state, changed, entry)

    def instruct(self, project_id: str, text: str) -> schemas.InstructionResult:
        values = self.project(project_id).values
        interpretation = interpreter.interpret(text, values, self.llm)
        by = interpretation.interpreted_by
        match interpretation.kind:
            case Kind.UNDO | Kind.REDO:
                redo = interpretation.kind is Kind.REDO
                result = self._step(project_id, redo=redo)
                word = "Redid" if redo else "Undid"
                message = (
                    f"{word} the change to {', '.join(result.changed)}."
                    if result.changed
                    else f"Nothing to {'redo' if redo else 'undo'}."
                )
                return schemas.InstructionResult(
                    kind=interpretation.kind.value, message=message, result=result
                )
            case Kind.QUERY:
                values = self.project(project_id).values
                answer = {
                    pid: (values[pid] if pid in values else derived.compute(pid, values))
                    for pid in interpretation.query
                }
                message = "; ".join(_format(pid, values) for pid in interpretation.query)
                return schemas.InstructionResult(
                    kind="query", message=message, answer=answer, interpreted_by=by
                )
            case Kind.CLARIFICATION:
                return schemas.InstructionResult(
                    kind="clarification",
                    message=interpretation.question or "",
                    suggestions=interpretation.suggestions,
                    interpreted_by=by,
                )
            case Kind.OUT_OF_SCOPE:
                return schemas.InstructionResult(
                    kind="out_of_scope", message=interpretation.question or "", interpreted_by=by
                )
            case Kind.TEST:
                assert interpretation.tests is not None
                return self._instruct_tests(project_id, interpretation.tests)
            case Kind.OPTIMIZE:
                assert interpretation.tests is not None
                return self._instruct_optimize(project_id, interpretation.tests)
            case Kind.LOOP:
                request = interpretation.tests or TestRequest()
                targets = [request.target] if request.target else ["front", "rear"]
                loops = [
                    self.engineering_loop(
                        project_id,
                        eloop.Goal(
                            test_id=request.test_id,
                            target=t,
                            scenarios=[request.scenario_id] if request.scenario_id else None,
                        ),
                    )  # fmt: skip
                    for t in targets
                ]
                return schemas.InstructionResult(
                    kind="loop", message=" ".join(_loop_message(r) for r in loops), loops=loops
                )
            case Kind.DIAGNOSE:
                request = interpretation.tests or TestRequest()
                target = request.target
                run = self.latest_failed_run(project_id, target, request.focus)
                if run is None:
                    return schemas.InstructionResult(
                        kind="clarification",
                        message="No current test has failed"
                        + (f" on the {target} corner" if target else "")
                        + ". Run a test first, for example 'test the rear over the hump'.",
                        suggestions=["test the rear over the hump", "run a quarter-car test"],
                    )
                found = self.diagnose(project_id, run.id)
                summary = schemas.RunSummary.of(run, True)
                return schemas.InstructionResult(
                    kind="diagnosis",
                    message=" ".join(f.explanation for f in found.findings),
                    runs=[summary],
                    diagnosis=found,
                )
            case Kind.PROPOSAL:
                # LLM-derived: never applied here, only stored until the user confirms it.
                assert interpretation.command is not None
                return self._propose(project_id, interpretation.command, interpretation.assumptions)
        # Only commands from the deterministic parser reach this point.
        command = interpretation.command
        assert command is not None
        if interpretation.kind is not Kind.COMMAND or command.source is Source.LLM:
            raise RuntimeError("LLM-derived commands must go through confirmation")
        try:
            result = self.apply(project_id, command)
        except CommandRejectedError as exc:
            return schemas.InstructionResult(
                kind="rejected",
                message=f"I can't apply that: {exc}",
                command=command,
                violations=exc.violations,
                assumptions=interpretation.assumptions,
            )
        if result.changed:
            values = result.values
            message = "Set " + "; ".join(_format(p, values) for p in result.changed) + "."
        else:
            message = "No change: the design already has those values."
        runs: list[schemas.RunSummary] = []
        comparisons: list[tst.Comparison] = []
        if interpretation.tests is not None:
            request = interpretation.tests
            targets = [request.target] if request.target else sorted({
                target for t, target in tst.tests_affected(result.changed) if t == request.test_id
            }) or list(tst.DEFINITIONS[request.test_id].targets)  # fmt: skip
            out = self.run_tests(project_id, request.test_id, targets, request.scenario_id)
            runs = [schemas.RunSummary.of(r, True) for r in out.runs]
            comparisons = out.comparisons
            by_run = {c.candidate: c for c in comparisons}
            message += " " + " ".join(_run_message(r, by_run.get(r.id)) for r in out.runs)
        return schemas.InstructionResult(
            kind="command",
            message=message,
            command=command,
            result=result,
            assumptions=interpretation.assumptions,
            runs=runs,
            comparisons=comparisons,
        )

    def _instruct_optimize(
        self, project_id: str, request: TestRequest
    ) -> schemas.InstructionResult:
        assert request.objective is not None
        definition = tst.DEFINITIONS[request.test_id]
        targets = [request.target] if request.target else list(definition.targets)
        scenarios = (
            [request.scenario_id] if request.scenario_id else [s.id for s in definition.scenarios]
        )
        values = self.project(project_id).values
        studies = []
        for target in targets:
            study = opt.Study(
                test_id=request.test_id, target=target, scenarios=scenarios,
                objectives=[opt.Objective(metric=request.objective, sense=request.sense)],
                variables=opt.default_variables(request.test_id, target, values),
            )  # fmt: skip
            result = self.optimize(project_id, study)
            if request.unmodelled:
                result.notes.append(
                    f"not checked: {', '.join(request.unmodelled)} (no model for it yet)"
                )
            studies.append(result)
        label = definition.metrics[request.objective][0].lower()
        parts = [_study_message(r, label) for r in studies]
        if request.unmodelled:
            parts.append(
                f"I did not constrain {', '.join(request.unmodelled)}: the quarter-car model has "
                "no roll or pitch, so that limit is not checked. A half-car or full-vehicle model "
                "is needed for it."
            )
        parts.append(
            "Constraints: every test criterion and approved requirement in each scenario. "
            "Accept a proposal to apply it (undoable)."
        )
        return schemas.InstructionResult(
            kind="optimization", message=" ".join(parts), studies=studies
        )

    def _instruct_tests(self, project_id: str, request: TestRequest) -> schemas.InstructionResult:
        definition = tst.DEFINITIONS[request.test_id]
        targets = [request.target] if request.target else list(definition.targets)
        out = self.run_tests(project_id, request.test_id, targets, request.scenario_id)
        by_run = {c.candidate: c for c in out.comparisons}
        return schemas.InstructionResult(
            kind="test",
            message=" ".join(_run_message(r, by_run.get(r.id)) for r in out.runs),
            runs=[schemas.RunSummary.of(r, True) for r in out.runs],
            comparisons=out.comparisons,
        )

    # --- component tests ---
    def run_tests(
        self,
        project_id: str,
        test_id: str,
        targets: list[str],
        scenario_id: str | None = None,
    ) -> schemas.TestRunResponse:
        """Run tests on the current design, store every run, and compare each with the same
        test on the previous design revision (run now if it was never run)."""
        definition = tst.DEFINITIONS[test_id]
        scenarios = [scenario_id] if scenario_id else [sc.id for sc in definition.scenarios]
        with self._lock, self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            runs_repo = RunRepository(s)
            reqs = runs_repo.requirements(project_id)
            previous = self._previous_values(state)
            runs, comparisons = [], []
            for target in targets:
                for sc in scenarios:
                    run = tst.run_test(
                        test_id, target, sc, state.values, history_cursor=state.cursor,
                        entry_id=_entry_id(state, state.cursor), requirements=reqs,
                    )  # fmt: skip
                    runs_repo.add(project_id, run)
                    runs.append(run)
                    if previous is None:
                        continue
                    base = self._baseline(
                        runs_repo, project_id, state, previous, run, test_id, target, sc, reqs
                    )
                    if base is not None:
                        comparisons.append(tst.compare(base, run))
            return schemas.TestRunResponse(runs=runs, comparisons=comparisons)

    @staticmethod
    def _previous_values(state: DesignState) -> dict[str, float] | None:
        if state.cursor == 0:
            return None
        entry = state.history[state.cursor - 1]
        return state.values | {c.parameter: c.old for c in entry.changes}

    @staticmethod
    def _baseline(
        repo: RunRepository, project_id: str, state: DesignState, previous: dict[str, float],
        run: tst.RunRecord, test_id: str, target: str, scenario_id: str,
        reqs: list[tst.Requirement],
    ) -> tst.RunRecord | None:  # fmt: skip
        """Same test on the previous revision: reuse a stored run with identical inputs
        (results are deterministic), otherwise run and store it."""
        definition = tst.DEFINITIONS[test_id]
        scenario = definition.scenario(scenario_id)
        key = tst.inputs_hash(definition, target, scenario, previous, reqs)
        if key == run.revision.inputs_hash:
            return None  # the last change did not touch this test's inputs
        base = repo.latest_by_inputs(project_id, key)
        if base is None:
            cursor = state.cursor - 1
            base = tst.run_test(
                test_id, target, scenario_id, previous, history_cursor=cursor,
                entry_id=_entry_id(state, cursor), requirements=reqs,
            )  # fmt: skip
            repo.add(project_id, base)
        return base

    def list_runs(
        self, project_id: str, test_id: str | None, target: str | None, scenario_id: str | None
    ) -> list[schemas.RunSummary]:
        with self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            repo = RunRepository(s)
            reqs = repo.requirements(project_id)
            out = []
            for run in repo.find(project_id, test_id, target, scenario_id):
                definition = tst.DEFINITIONS[run.test_id]
                scenario = definition.scenario(run.scenario["id"])
                key = tst.inputs_hash(definition, run.target, scenario, state.values, reqs)
                out.append(schemas.RunSummary.of(run, key == run.revision.inputs_hash))
            return out

    def get_run(self, project_id: str, run_id: str) -> tst.RunRecord:
        with self.db.session() as s:
            ProjectRepository(s).info(project_id)
            return RunRepository(s).get(project_id, run_id)

    def diagnose(self, project_id: str, run_id: str) -> dgn.Diagnosis:
        with self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            repo = RunRepository(s)
            run = repo.get(project_id, run_id)
            reqs = repo.requirements(project_id)
        # The run's own inputs over the current design: only its inputs affect the test.
        values = state.values | {p: v["value"] for p, v in run.inputs.items()}
        definition = tst.DEFINITIONS[run.test_id]
        scenario = definition.scenario(run.scenario["id"])
        current = tst.inputs_hash(definition, run.target, scenario, state.values, reqs) == (
            run.revision.inputs_hash
        )
        return dgn.diagnose(run, values, current=current, requirements=reqs)

    def latest_failed_run(
        self, project_id: str, target: str | None, focus: str | None = None
    ) -> tst.RunRecord | None:
        """Most recent failed run on the current design; ``focus`` prefers travel or tyre
        contact failures."""
        wanted = {"travel": ("bump_travel", "rebound_travel"), "contact": ("tyre_contact",)}
        fallback = None
        for summary in self.list_runs(project_id, None, target, None):
            if not summary.current or summary.status != tst.RunStatus.FAILED:
                continue
            run = self.get_run(project_id, summary.id)
            if focus is None or any(
                c.id in wanted[focus] and c.passed is False for c in run.criteria
            ):
                return run
            fallback = fallback or run
        return fallback

    # --- optimisation ---
    def optimize(self, project_id: str, study: opt.Study) -> opt.StudyResult:
        with self._lock, self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            reqs = RunRepository(s).requirements(project_id)
            result = opt.run_study(study, state.values, reqs)
            result.notes.append(f"run on design revision {state.cursor}")
            StudyRepository(s).save(
                project_id, "optimization", result.id, result.status, result.model_dump_json()
            )
            return result

    def engineering_loop(self, project_id: str, goal: eloop.Goal) -> eloop.LoopResult:
        with self._lock, self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            reqs = RunRepository(s).requirements(project_id)
            result = eloop.run_loop(goal, state.values, reqs)
            result.notes.append(f"started from design revision {state.cursor}")
            StudyRepository(s).save(
                project_id, "loop", result.id, result.status, result.model_dump_json()
            )
            return result

    def choose_candidate(self, project_id: str, study_id: str, index: int) -> opt.StudyResult:
        """Pick a design from a study (e.g. a Pareto point); it is re-verified before proposing."""
        with self._lock, self.db.session() as s:
            kind, raw = StudyRepository(s).get(project_id, study_id)
            if kind != "optimization":
                raise CommandError("only optimisation studies have candidates")
            result = opt.StudyResult.model_validate_json(raw)
            if result.status not in ("proposed", "no_feasible_design"):
                raise CommandError(f"study is {result.status}")
            candidate = next((c for c in result.candidates if c.index == index), None)
            if candidate is None or not candidate.feasible:
                raise CommandError("choose a feasible candidate")
            state = ProjectRepository(s).load(project_id)
            result.status = "proposed"
            opt.propose(result, candidate, state.values, RunRepository(s).requirements(project_id))
            StudyRepository(s).save(
                project_id, kind, result.id, result.status, result.model_dump_json()
            )
            return result

    def loops(self, project_id: str) -> list[eloop.LoopResult]:
        with self.db.session() as s:
            ProjectRepository(s).info(project_id)
            return [
                eloop.LoopResult.model_validate_json(r)
                for r in StudyRepository(s).find(project_id, "loop")
            ]

    def studies(self, project_id: str) -> list[opt.StudyResult]:
        with self.db.session() as s:
            ProjectRepository(s).info(project_id)
            return [
                opt.StudyResult.model_validate_json(r)
                for r in StudyRepository(s).find(project_id, "optimization")
            ]

    def decide_study(
        self, project_id: str, study_id: str, accept: bool
    ) -> schemas.CommandResult | None:
        """Accept applies the proposed command (undoable); reject records the decision."""
        with self.db.session() as s:
            kind, raw = StudyRepository(s).get(project_id, study_id)
        model = opt.StudyResult if kind == "optimization" else eloop.LoopResult
        result = model.model_validate_json(raw)
        if result.status != "proposed":
            raise CommandError(f"study is {result.status}, not awaiting a decision")
        applied = None
        if accept:
            if result.command is None:
                raise CommandError("the study has no change to apply")
            applied = self.apply(project_id, result.command)
        result.status = "accepted" if accept else "rejected"
        with self.db.session() as s:
            StudyRepository(s).save(
                project_id, kind, result.id, result.status, result.model_dump_json()
            )
        return applied

    def compare_runs(self, project_id: str, baseline: str, candidate: str) -> tst.Comparison:
        with self.db.session() as s:
            repo = RunRepository(s)
            return tst.compare(repo.get(project_id, baseline), repo.get(project_id, candidate))

    def component_status(self, project_id: str) -> list[schemas.ComponentTestStatus]:
        order = [st.value for st in (
            tst.ComponentStatus.FAILED, tst.ComponentStatus.INVALID, tst.ComponentStatus.STALE,
            tst.ComponentStatus.NOT_TESTED, tst.ComponentStatus.PASSED_WITHIN_MODEL,
            tst.ComponentStatus.NO_CRITERIA,
        )]  # fmt: skip
        with self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            repo = RunRepository(s)
            reqs = repo.requirements(project_id)
            per_component: dict[str, list[dict]] = {}
            for definition in tst.DEFINITIONS.values():
                for target in definition.targets:
                    for sc in definition.scenarios:
                        key = tst.inputs_hash(definition, target, sc, state.values, reqs)
                        run = repo.latest_by_inputs(project_id, key)
                        if run is not None:
                            status, run_id = run.status.value, run.id
                        else:
                            older = repo.find(project_id, definition.id, target, sc.id, limit=1)
                            status = "stale" if older else "not_tested"
                            run_id = older[0].id if older else None
                        for cid in definition.components[target]:
                            per_component.setdefault(cid, []).append({
                                "test_id": definition.id, "test_name": definition.name,
                                "target": target, "scenario_id": sc.id,
                                "scenario_label": sc.label, "status": status, "run_id": run_id,
                            })  # fmt: skip
            out = []
            for cid, tests in per_component.items():
                statuses = {t["status"] for t in tests}
                verdict = statuses - {"no_criteria"} or statuses
                status = next(st for st in order if st in verdict)
                out.append(schemas.ComponentTestStatus(component=cid, status=status, tests=tests))
            return out

    def requirements(self, project_id: str) -> list[schemas.RequirementOut]:
        with self.db.session() as s:
            ProjectRepository(s).info(project_id)
            return [
                schemas.RequirementOut(**vars(r)) for r in RunRepository(s).requirements(project_id)
            ]

    def add_requirement(
        self, project_id: str, body: schemas.RequirementIn
    ) -> schemas.RequirementOut:
        definition = tst.DEFINITIONS.get(body.test_id)
        if definition is None or body.metric not in definition.metrics:
            raise CommandError(f"unknown test or metric: {body.test_id} / {body.metric}")
        with self.db.session() as s:
            ProjectRepository(s).info(project_id)
            req = RunRepository(s).add_requirement(
                project_id, tst.Requirement(id="", approved=True, **body.model_dump())
            )
            return schemas.RequirementOut(**vars(req))

    def delete_requirement(self, project_id: str, requirement_id: str) -> None:
        with self.db.session() as s:
            RunRepository(s).delete_requirement(project_id, requirement_id)

    def integration(self, project_id: str) -> schemas.IntegrationOut:
        values = self.project(project_id).values
        with self._lock:
            model = model_service.build_model(values, self.cache)
            checks = (
                integration.structural_checks(values)
                + integration.travel_checks(values)
                + integration.clearance_checks(model, self._clearances)
            )
        counts: dict[str, int] = {}
        for c in checks:
            counts[c.status.value] = counts.get(c.status.value, 0) + 1
        return schemas.IntegrationOut(
            checks=[
                schemas.CheckOut(
                    id=c.id,
                    kind=c.kind,
                    status=c.status.value,
                    message=c.message,
                    components=list(c.components),
                    parameters=list(c.parameters),
                    measured=c.measured,
                    limit=c.limit,
                    unit=c.unit,
                )  # fmt: skip
                for c in checks
            ],
            counts=counts,
            not_checked=list(integration.NOT_CHECKED),
        )

    # --- LLM proposals ---
    def _propose(
        self, project_id: str, command: SetParameters, assumptions: list[str]
    ) -> schemas.InstructionResult:
        state = DesignState.model_validate(
            {"values": self.project(project_id).values}
        )  # current values only
        proposed = state.preview(command)
        violations = validate(proposed)
        if violations:
            return schemas.InstructionResult(
                kind="rejected",
                interpreted_by="llm",
                command=command,
                violations=violations,
                assumptions=assumptions,
                message="The local model suggested a change that breaks a design rule: "
                + "; ".join(v.message for v in violations),
            )
        changed = [c.parameter for c in command.changes]
        preview = {pid: proposed[pid] for pid in dict.fromkeys(changed)}
        self._expire_proposals()
        proposal_id = uuid4().hex
        self._proposals[proposal_id] = _Proposal(project_id, command, time.monotonic())
        summary = "; ".join(_format(pid, proposed) for pid in preview)
        return schemas.InstructionResult(
            kind="proposal",
            interpreted_by="llm",
            command=command,
            proposal_id=proposal_id,
            preview=preview,
            assumptions=assumptions,
            message=f"Suggested by the local model: {summary}. Confirm to apply it.",
        )

    def _expire_proposals(self) -> None:
        now = time.monotonic()
        for pid in [k for k, p in self._proposals.items() if now - p.created > PROPOSAL_TTL_S]:
            del self._proposals[pid]

    def _take_proposal(self, project_id: str, proposal_id: str) -> _Proposal:
        self._expire_proposals()
        proposal = self._proposals.get(proposal_id)
        if proposal is None or proposal.project_id != project_id:
            raise ProposalNotFoundError(proposal_id)
        del self._proposals[proposal_id]
        return proposal

    def confirm(self, project_id: str, proposal_id: str) -> schemas.CommandResult:
        """Apply a confirmed LLM proposal through the normal validated command path."""
        return self.apply(project_id, self._take_proposal(project_id, proposal_id).command)

    def reject(self, project_id: str, proposal_id: str) -> None:
        self._take_proposal(project_id, proposal_id)

    def llm_status(self) -> schemas.LLMStatusOut:
        status = self.llm.status()
        return schemas.LLMStatusOut(
            provider=status.provider,
            model=status.model,
            url=status.url,
            available=status.available,
            detail=status.detail,
            models=status.models,
        )

    # --- geometry ---
    def model(self, project_id: str, known: set[str]) -> dict:
        values = self.project(project_id).values
        with self._lock:
            model = model_service.build_model(values, self.cache)
            return model_service.mesh_payload(model, self.cache, skip=known)

    def export_step(self, project_id: str) -> Path:
        values = self.project(project_id).values
        with self._lock:
            model = model_service.build_model(values, self.cache)
            return model_service.export_step(
                model, self.data_dir / "exports" / f"{project_id}.step"
            )
