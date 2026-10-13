"""The engineering loop: objective -> test -> diagnose -> change -> retest, bounded.

Each iteration runs the full tests (with convergence checks) on a candidate design, and if a
criterion fails, applies the diagnosis's smallest single-parameter fix that keeps every rule
and every other criterion satisfied. Candidate designs live only in the loop record; the
project design changes only when the user accepts the final proposal (one undoable command).

Stops when every criterion passes, when no admissible fix exists (a decision for the user),
or after ``max_iterations``. Optionally finishes with a bounded optimisation of an objective.
"""

from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from autevra.core.commands import Change, Operation, SetParameters, Source
from autevra.core.parameters import REGISTRY
from autevra.engineering import diagnosis as dg
from autevra.engineering import optimize as opt
from autevra.engineering import testing as tst

Values = Mapping[str, float]


class Goal(BaseModel):
    test_id: str = "quarter_car"
    target: str
    scenarios: list[str] | None = None  # None: every scenario of the test
    editable: list[str] | None = None  # parameters the loop may change; None: test inputs
    objective: opt.Objective | None = None  # optional final optimisation
    max_iterations: int = Field(default=4, ge=1, le=10)


class Iteration(BaseModel):
    index: int
    changes: dict[str, dict]  # parameter -> {from, to, unit} relative to the start
    runs: list[dict]  # per scenario: status, failed criteria, converged
    diagnosis: str | None = None
    decision: str


class LoopResult(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    goal: Goal
    iterations: list[Iteration]
    outcome: str  # all_pass | needs_decision | iteration_limit | already_passing
    optimization: opt.StudyResult | None = None
    command: SetParameters | None = None
    status: str = "proposed"  # proposed | accepted | rejected | nothing_to_apply
    notes: list[str] = []


def _changes(start: Values, values: Values) -> dict[str, dict]:
    return {
        p: {"from": start[p], "to": values[p], "unit": str(REGISTRY[p].unit)}
        for p in REGISTRY
        if values[p] != start[p]
    }


def run_loop(goal: Goal, start: Values, requirements: Iterable[tst.Requirement] = ()
             ) -> LoopResult:  # fmt: skip
    requirements = list(requirements)
    definition = tst.DEFINITIONS[goal.test_id]
    scenarios = goal.scenarios or [s.id for s in definition.scenarios]
    editable = set(goal.editable or definition.inputs(goal.target))
    values = dict(start)
    iterations: list[Iteration] = []
    outcome = "iteration_limit"

    for i in range(goal.max_iterations):
        runs = [tst.run_test(goal.test_id, goal.target, sc, values, requirements=requirements)
                for sc in scenarios]  # fmt: skip
        summary = [{
            "scenario": r.scenario["id"], "status": r.status.value,
            "converged": bool(r.numerics.get("converged")),
            "failed": [c.label for c in r.criteria if c.passed is False],
        } for r in runs]  # fmt: skip
        failed = [r for r in runs if r.status is tst.RunStatus.FAILED]
        invalid = [r for r in runs if r.status is tst.RunStatus.INVALID]
        if invalid:
            iterations.append(Iteration(index=i, changes=_changes(start, values), runs=summary,
                                        decision="stop: numerics not acceptable"))  # fmt: skip
            outcome = "needs_decision"
            break
        if not failed:
            outcome = "already_passing" if i == 0 else "all_pass"
            iterations.append(Iteration(index=i, changes=_changes(start, values), runs=summary,
                                        decision="stop: every criterion passes"))  # fmt: skip
            break
        run = failed[0]
        found = dg.diagnose(run, values, current=True, requirements=requirements)
        finding = found.findings[0]
        fixes = [f for f in finding.fixes
                 if f.parameter in editable and not f.rule_violations and not f.breaks]  # fmt: skip
        # A fix must not break the other scenarios either: check before taking it.
        chosen = None
        for f in fixes:
            trial = values | {f.parameter: f.to_value}
            others = [tst.quick_evaluate(goal.test_id, goal.target, sc, trial, requirements)[1]
                      for sc in scenarios if sc != run.scenario["id"]]  # fmt: skip
            newly = [c for res in others for c in res if c.passed is False]
            before = [r for r in runs if r.scenario["id"] != run.scenario["id"]
                      and r.status is tst.RunStatus.FAILED]  # fmt: skip
            if len(newly) <= sum(len([c for c in r.criteria if c.passed is False]) for r in before):
                chosen = f
                break
        if chosen is None:
            iterations.append(Iteration(
                index=i, changes=_changes(start, values), runs=summary,
                diagnosis=finding.explanation,
                decision="stop: no single-parameter fix within ±30 % keeps every rule and "
                "criterion; needs an engineering decision",
            ))  # fmt: skip
            outcome = "needs_decision"
            break
        iterations.append(Iteration(
            index=i, changes=_changes(start, values), runs=summary, diagnosis=finding.explanation,
            decision=f"change {chosen.label.lower()} {chosen.from_value:g} → {chosen.to_value:g} "
            f"{chosen.unit} and retest",
        ))  # fmt: skip
        values = values | {chosen.parameter: chosen.to_value}

    result = LoopResult(goal=goal, iterations=iterations, outcome=outcome)
    if goal.objective is not None and outcome in ("all_pass", "already_passing"):
        variables = [v for v in opt.default_variables(goal.test_id, goal.target, values)
                     if v.parameter in editable]  # fmt: skip
        if variables:
            study = opt.Study(
                test_id=goal.test_id, target=goal.target, scenarios=scenarios,
                objectives=[goal.objective], variables=variables, budget=40,
            )  # fmt: skip
            result.optimization = opt.run_study(study, values, requirements)
            if result.optimization.best is not None and result.optimization.command is not None:
                values = values | result.optimization.best.values
    changes = _changes(start, values)
    if changes:
        result.command = SetParameters(
            changes=tuple(Change(parameter=p, operation=Operation.SET, value=c["to"])
                          for p, c in changes.items()),
            source=Source.OPTIMIZER, instruction=f"engineering loop {result.id}",
        )  # fmt: skip
    else:
        result.status = "nothing_to_apply"
    result.notes = [
        f"{len(iterations)} iteration(s), each with full test runs on the candidate design",
        "candidate designs are not part of the project history until accepted",
    ]
    return result
