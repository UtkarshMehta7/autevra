"""Bounded, reproducible design optimisation on the real simulation service.

Method: seeded Latin-hypercube sampling of the design variables, then a compass (pattern)
search around the best feasible point, within a fixed evaluation budget. Derivative-free,
because each evaluation is a simulation; small budgets suit a handful of variables.

- Candidates that break a design rule are rejected before any simulation.
- Feasible means every criterion of the test (and every approved requirement) passes in
  every chosen scenario.
- Objectives are solver metrics, aggregated as the worst case over the scenarios. With two
  objectives the result is a Pareto set: no single "best" is claimed.
- Scores come only from computed results. The chosen design is re-run with full numerics
  (half-step convergence check) before it is offered, and it is applied only on approval.
"""

import random
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from autevra.core.commands import Change, Operation, SetParameters, Source
from autevra.core.parameters import REGISTRY
from autevra.core.rules import validate
from autevra.engineering import testing as tst

Values = Mapping[str, float]


class Variable(BaseModel):
    parameter: str
    lower: float
    upper: float


class Objective(BaseModel):
    metric: str
    sense: str = "minimize"  # minimize | maximize


class Study(BaseModel):
    """What to optimise. Everything the search may touch is listed here."""

    test_id: str = "quarter_car"
    target: str
    scenarios: list[str]
    objectives: list[Objective] = Field(min_length=1, max_length=2)
    variables: list[Variable] = Field(min_length=1, max_length=6)
    budget: int = Field(default=60, ge=5, le=400)
    seed: int = 0


class Candidate(BaseModel):
    index: int
    phase: str  # baseline | sample | refine
    values: dict[str, float]
    rule_violations: list[str] = []
    simulated: bool = False
    feasible: bool = False
    objectives: dict[str, float] = {}
    failed: list[str] = []  # "scenario: criterion"


class StudyResult(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    study: Study
    method: str
    baseline: Candidate
    candidates: list[Candidate]
    best: Candidate | None  # single objective: best feasible
    pareto: list[int]  # candidate indices of the feasible non-dominated set
    verified: list[dict] = []  # full runs of the proposed design, one per scenario
    improvement: dict[str, float] = {}  # objective change vs baseline (same sign as metric)
    command: SetParameters | None = None
    evaluations: int
    status: str = "proposed"  # proposed | accepted | rejected | no_feasible_design
    blocking: str | None = None  # the criterion that most often made candidates infeasible
    notes: list[str] = []


def default_variables(test_id: str, target: str, values: Values, spread: float = 0.3
                      ) -> list[Variable]:  # fmt: skip
    """Spring rate and damping of the corner, ±``spread`` around the design, within bounds."""
    out = []
    for suffix in ("spring_rate", "damping_bump", "damping_rebound"):
        pid = f"{target}_{suffix}"
        spec = REGISTRY[pid]
        v = values[pid]
        out.append(Variable(parameter=pid, lower=max(spec.min, v * (1 - spread)),
                            upper=min(spec.max, v * (1 + spread))))  # fmt: skip
    return out


def _check(study: Study) -> None:
    definition = tst.DEFINITIONS[study.test_id]
    if study.target not in definition.targets:
        raise ValueError(f"unknown target '{study.target}'")
    for sc in study.scenarios:
        definition.scenario(sc)
    for o in study.objectives:
        if o.metric not in definition.metrics:
            raise ValueError(f"unknown metric '{o.metric}'")
        if o.sense not in ("minimize", "maximize"):
            raise ValueError("objective sense must be minimize or maximize")
    inputs = set(definition.inputs(study.target))
    for var in study.variables:
        spec = REGISTRY.get(var.parameter)
        if spec is None or var.parameter not in inputs:
            raise ValueError(f"'{var.parameter}' is not an input of this test")
        if not spec.min <= var.lower < var.upper <= spec.max:
            raise ValueError(
                f"bounds for {var.parameter} must lie within {spec.min:g}–{spec.max:g}"
            )


def _score(study: Study, metrics: list[dict]) -> dict[str, float]:
    out = {}
    for o in study.objectives:
        values = [m[o.metric] for m in metrics if m.get(o.metric) is not None]
        worst = max(values) if o.sense == "minimize" else min(values)
        out[o.metric] = worst
    return out


def _key(study: Study, c: Candidate) -> tuple[float, ...]:
    """Lower is better for every entry."""
    return tuple(
        c.objectives[o.metric] if o.sense == "minimize" else -c.objectives[o.metric]
        for o in study.objectives
    )


def _dominates(a: tuple[float, ...], b: tuple[float, ...]) -> bool:
    return all(x <= y for x, y in zip(a, b, strict=True)) and any(
        x < y for x, y in zip(a, b, strict=True)
    )


def run_study(study: Study, values: Values, requirements: Iterable[tst.Requirement] = ()
              ) -> StudyResult:  # fmt: skip
    _check(study)
    requirements = list(requirements)
    rng = random.Random(study.seed)
    names = [v.parameter for v in study.variables]
    candidates: list[Candidate] = []
    seen: dict[tuple, Candidate] = {}

    def evaluate(point: dict[str, float], phase: str) -> Candidate:
        point = {k: round(v, 3) for k, v in point.items()}
        key = tuple(point[n] for n in names)
        if key in seen:
            return seen[key]
        design = dict(values) | point
        c = Candidate(index=len(candidates), phase=phase, values=point)
        c.rule_violations = [v.message for v in validate(design)]
        if not c.rule_violations:  # never simulate an invalid design
            metrics, failed = [], []
            for sc in study.scenarios:
                m, criteria = tst.quick_evaluate(study.test_id, study.target, sc, design,
                                                 requirements)  # fmt: skip
                metrics.append(m)
                failed += [f"{sc}: {x.label}" for x in criteria if x.passed is not True]
            c.simulated, c.failed = True, failed
            c.feasible = not failed
            c.objectives = _score(study, metrics)
        candidates.append(c)
        seen[key] = c
        return c

    baseline = evaluate({n: values[n] for n in names}, "baseline")
    budget = study.budget - 1

    # Latin hypercube: one sample per stratum of every variable, strata shuffled per variable.
    n_samples = max(1, budget * 2 // 3)
    strata = {n: rng.sample(range(n_samples), n_samples) for n in names}
    for i in range(n_samples):
        point = {}
        for var in study.variables:
            u = (strata[var.parameter][i] + rng.random()) / n_samples
            point[var.parameter] = var.lower + u * (var.upper - var.lower)
        evaluate(point, "sample")

    # Compass search around the incumbent (single objective) or the first front point.
    def incumbent() -> Candidate | None:
        feasible = [c for c in candidates if c.feasible]
        return min(feasible, key=lambda c: _key(study, c)) if feasible else None

    step = 0.25
    while len(candidates) < study.budget and step > 0.02:
        best = incumbent()
        if best is None:
            break
        improved = False
        for var in study.variables:
            for sign in (1, -1):
                if len(candidates) >= study.budget:
                    break
                span = var.upper - var.lower
                x = min(max(best.values[var.parameter] + sign * step * span, var.lower), var.upper)
                c = evaluate(best.values | {var.parameter: x}, "refine")
                if c.feasible and _key(study, c) < _key(study, best):
                    improved = True
        if not improved:
            step /= 2

    feasible = [c for c in candidates if c.feasible]
    keys = {c.index: _key(study, c) for c in feasible}
    pareto = [c.index for c in feasible
              if not any(_dominates(keys[o.index], keys[c.index]) for o in feasible)]  # fmt: skip
    best = incumbent() if len(study.objectives) == 1 else None
    notes = [
        f"objective: worst case over {', '.join(study.scenarios)}",
        "feasible: every test criterion and approved requirement passes in every scenario",
        f"{sum(1 for c in candidates if c.rule_violations)} candidates rejected by design rules "
        "before simulation",
    ]
    result = StudyResult(
        study=study, method="latin-hypercube + compass search (seeded)", baseline=baseline,
        candidates=candidates, best=best, pareto=sorted(pareto, key=lambda i: keys[i]),
        evaluations=sum(1 for c in candidates if c.simulated), notes=notes,
    )  # fmt: skip
    chosen = best
    if chosen is None and len(study.objectives) == 2 and pareto:
        notes.append("two objectives: pick a design from the Pareto set; none is proposed alone")
    if not feasible:
        counts: dict[str, int] = {}
        for c in candidates:
            for f in set(c.failed):
                counts[f] = counts.get(f, 0) + 1
        simulated = sum(1 for c in candidates if c.simulated)
        if counts:
            blocker, n = max(counts.items(), key=lambda kv: kv[1])
            result.blocking = f"{blocker} (fails in {n} of {simulated} simulated candidates)"
        result.status = "no_feasible_design"
        notes.append("no candidate met every criterion; widen the bounds or the budget, or "
                     "diagnose the failing criterion")  # fmt: skip
    if chosen is not None:
        propose(result, chosen, values, requirements)
        at_bound = [
            v.parameter for v in study.variables
            if chosen.values[v.parameter] in (round(v.lower, 3), round(v.upper, 3))
        ]  # fmt: skip
        if at_bound:
            notes.append(f"at a bound: {', '.join(at_bound)}; wider bounds may improve further")
    if any(v.parameter.endswith("spring_rate") for v in study.variables):
        notes.append("spring rate changes assume the ride height is kept (spring preload or "
                     "free length adjusted); static sag is not modelled")  # fmt: skip
    return result


def propose(result: StudyResult, chosen: Candidate, values: Values,
            requirements: Iterable[tst.Requirement] = ()) -> None:  # fmt: skip
    """Re-run the chosen design with full numerics and attach the command to apply it."""
    study = result.study
    design = dict(values) | chosen.values
    verified = []
    for sc in study.scenarios:
        run = tst.run_test(study.test_id, study.target, sc, design, requirements=requirements)
        verified.append({
            "scenario": sc, "status": run.status.value,
            "converged": bool(run.numerics.get("converged")),
            "metrics": {o.metric: run.metrics[o.metric]["value"] for o in study.objectives},
        })  # fmt: skip
    result.verified = verified
    if not all(v["status"] == "passed_within_model" and v["converged"] for v in verified):
        result.status = "no_feasible_design"
        result.notes.append("the chosen design did not pass the full verification run")
        return
    result.best = chosen
    result.improvement = {
        k: round(chosen.objectives[k] - result.baseline.objectives[k], 6)
        for k in chosen.objectives
        if result.baseline.simulated
    }
    changes = tuple(
        Change(parameter=p, operation=Operation.SET, value=v)
        for p, v in chosen.values.items()
        if v != round(values[p], 3)
    )
    if changes:
        goal = ", ".join(o.metric for o in study.objectives)
        result.command = SetParameters(
            changes=changes,
            source=Source.OPTIMIZER,
            instruction=f"optimisation {result.id}: {goal}",
        )
    else:
        result.notes.append("the current design is already the best candidate found")
