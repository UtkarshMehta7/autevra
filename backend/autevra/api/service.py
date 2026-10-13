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
from autevra.engineering import integration
from autevra.engineering import testing as tst
from autevra.storage.database import Database
from autevra.storage.repository import ProjectInfo, ProjectRepository
from autevra.storage.runs import RunRepository


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
