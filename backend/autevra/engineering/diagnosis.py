"""Explainable failure diagnosis from deterministic checks and measured sensitivities.

For every failed (or tightest) criterion of a run, the diagnosis reports:
- the violated criterion, measured value, limit and scenario, with the run's identifiers;
- where the limit comes from (for wheel travel: which packaging limit governs);
- the measured effect of each input parameter: the same scenario re-simulated with the
  parameter moved by one step each way, giving the change in margin and the side effects;
- corrective changes that make the criterion pass *in the model*, smallest step first, each
  checked against the design rules, with the trade-offs measured in the same runs.

Evidence levels: ``confirmed_in_model`` (measured by re-simulation), ``deterministic`` (a
rule or derived value), ``possible`` (small measured effect). Nothing here is a physical
root cause; a fix is only resolved once a full test run on the changed design passes.
"""

from collections.abc import Iterable, Mapping

from pydantic import BaseModel

from autevra.domain import derived as d
from autevra.domain.commands import Change, Operation, SetParameters, Source
from autevra.domain.parameters import REGISTRY
from autevra.domain.rules import validate
from autevra.engineering import testing as tst

Values = Mapping[str, float]
STEPS = (0.1, 0.2, 0.3)  # relative steps tried for corrective changes
# A criterion whose margin saturates (tyre load is 0 whenever the tyre is off the road) is
# probed through a metric that keeps responding: less time off the road is better.
PROXIES = {"tyre_contact": "lift_off_time"}


class Effect(BaseModel):
    parameter: str
    label: str
    unit: str
    value: float
    margin_up: float | None  # margin change when the parameter rises one step
    margin_down: float | None
    better_direction: str | None  # increase | decrease | None (no measured effect)
    evidence: str  # confirmed_in_model | possible | none
    side_effects: list[str] = []  # other criteria or key metrics made worse by that step


class Fix(BaseModel):
    parameter: str
    label: str
    operation: str
    from_value: float
    to_value: float
    unit: str
    step_percent: float
    margin_after: float
    breaks: list[str]  # other criteria that fail after the change (measured)
    rule_violations: list[str]
    command: SetParameters


class Finding(BaseModel):
    criterion: str
    label: str
    status: str  # failed | tightest_margin
    measured: float | None
    limit: float
    unit: str
    margin: float | None
    limit_source: str  # how the limit is set
    governing_parameter: str | None
    effects: list[Effect]
    fixes: list[Fix]
    explanation: str


class Diagnosis(BaseModel):
    run_id: str
    test_id: str
    target: str
    scenario_id: str
    scenario_label: str
    design_revision: int
    current: bool
    status: str
    findings: list[Finding]
    evidence: dict
    recommendation: str
    caveats: list[str]


def _limit_source(criterion: tst.CriterionResult, values: Values, target: str):  # type: ignore[no-untyped-def]
    if criterion.id in ("bump_travel", "rebound_travel"):
        limits = d.travel_limits(values, target)
        keys = d.BUMP_LIMITS if criterion.id == "bump_travel" else d.REBOUND_LIMITS
        governing = min(keys, key=lambda k: limits[k][0])
        parts = ", ".join(f"{k.replace('_', ' ')} {limits[k][0]:.1f} mm" for k in keys)
        return (f"usable travel is the smallest of: {parts}; the "
                f"{governing.replace('_', ' ')} governs", limits[governing][1])  # fmt: skip
    if criterion.source == "user":
        return "user requirement", None
    return "test definition", None


def _margin(criteria: list[tst.CriterionResult], cid: str) -> float | None:
    for c in criteria:
        if c.id == cid:
            return c.margin
    return None


def _stepped(values: Values, pid: str, step: float) -> dict[str, float] | None:
    spec = REGISTRY[pid]
    new = values[pid] * (1.0 + step)
    if new == values[pid]:
        new = values[pid] + step * (spec.max - spec.min)
    new = min(max(new, spec.min), spec.max)
    if abs(new - values[pid]) < 1e-9:
        return None  # at the bound
    return dict(values) | {pid: round(new, 6)}


def diagnose(
    run: tst.RunRecord,
    values: Values,
    *,
    current: bool,
    requirements: Iterable[tst.Requirement] = (),
) -> Diagnosis:
    """``values``: the design the run used (its inputs over the current design)."""
    requirements = list(requirements)
    definition = tst.DEFINITIONS[run.test_id]
    scenario = run.scenario["id"]
    failed = [c for c in run.criteria if c.passed is False]
    targets = (
        failed
        or sorted(
            (c for c in run.criteria if c.margin is not None),
            key=lambda c: c.margin,  # type: ignore[arg-type, return-value]
        )[:1]
    )
    params = [p for p in definition.inputs(run.target) if p in REGISTRY]

    def evaluate(v: Values) -> list[tst.CriterionResult]:
        metrics, criteria = tst.quick_evaluate(run.test_id, run.target, scenario, v, requirements)
        for cid, metric in PROXIES.items():  # stash the proxy metric alongside the criteria
            if metrics.get(metric) is not None:
                criteria.append(tst.CriterionResult(
                    id=f"proxy:{cid}", label=metric, metric=metric, comparator="<=", limit=0,
                    unit="s", measured=metrics[metric], passed=None, source="proxy",
                    margin=-float(metrics[metric] or 0.0),
                ))  # fmt: skip
        return criteria

    base = evaluate(values)
    base_pass = {c.id: c.passed for c in base}
    # One perturbation run per parameter and direction, shared by all findings.
    perturbed: dict[tuple[str, float], list[tst.CriterionResult] | None] = {}
    for pid in params:
        for step in (STEPS[0], -STEPS[0]):
            v = _stepped(values, pid, step)
            perturbed[(pid, step)] = None if v is None else evaluate(v)

    findings = []
    for crit in targets:
        source, governing = _limit_source(crit, values, run.target)
        probe = crit.id
        if crit.id in PROXIES and crit.measured == 0:
            probe = f"proxy:{crit.id}"  # tyre off the road: rank by time off the road
            source += f"; effects measured on {PROXIES[crit.id].replace('_', ' ')}"
        base_margin = _margin(base, probe)
        effects = []
        for pid in params:
            spec = REGISTRY[pid]
            deltas = {}
            side: list[str] = []
            for step in (STEPS[0], -STEPS[0]):
                res = perturbed[(pid, step)]
                if res is None or base_margin is None:
                    deltas[step] = None
                    continue
                m = _margin(res, probe)
                deltas[step] = None if m is None else round(m - base_margin, 6)
            up, down = deltas[STEPS[0]], deltas[-STEPS[0]]
            probe_base = next((c for c in base if c.id == probe), crit)
            scale = max(abs(probe_base.limit), abs(probe_base.measured or 0), 1e-9)
            best = max(
                (x for x in ((up, "increase"), (down, "decrease")) if x[0] is not None),
                key=lambda x: x[0], default=(None, None),
            )  # fmt: skip
            direction = best[1] if best[0] is not None and best[0] > 1e-6 * scale else None
            if direction:
                res = perturbed[(pid, STEPS[0] if direction == "increase" else -STEPS[0])]
                side = [
                    c.label for c in res or []
                    if c.id != crit.id and base_pass.get(c.id) and c.passed is False
                    and c.source != "proxy"
                ]  # fmt: skip
            strength = abs(best[0]) / scale if best[0] is not None else 0.0
            evidence = (
                "confirmed_in_model" if strength >= 0.01 else "possible" if direction else "none"
            )
            effects.append(Effect(
                parameter=pid, label=spec.label, unit=str(spec.unit), value=values[pid],
                margin_up=up, margin_down=down, better_direction=direction, evidence=evidence,
                side_effects=side,
            ))  # fmt: skip
        effects.sort(key=lambda e: -max(e.margin_up or 0, e.margin_down or 0))

        fixes = []
        candidates = [e for e in effects if e.evidence == "confirmed_in_model"][:6]
        for e in candidates if crit.passed is False else []:
            sign = 1.0 if e.better_direction == "increase" else -1.0
            for step in STEPS:
                v = _stepped(values, e.parameter, sign * step)
                if v is None:
                    break
                res = evaluate(v)
                m = _margin(res, crit.id)
                if m is None or m <= 0 and crit.comparator in ("<", ">") or m < 0:
                    continue
                violations = [x.message for x in validate(v)]
                op = Operation.INCREASE if sign > 0 else Operation.DECREASE
                command = SetParameters(
                    changes=(Change(parameter=e.parameter, operation=Operation.SET,
                                    value=v[e.parameter]),),
                    source=Source.API,
                    instruction=f"diagnosis fix for {crit.label.lower()} ({run.id})",
                )  # fmt: skip
                fixes.append(Fix(
                    parameter=e.parameter, label=e.label, operation=op.value,
                    from_value=values[e.parameter], to_value=v[e.parameter], unit=e.unit,
                    step_percent=step * 100, margin_after=round(m, 6),
                    breaks=[c.label for c in res if c.id != crit.id and base_pass.get(c.id)
                            and c.passed is False and c.source != "proxy"],
                    rule_violations=violations, command=command,
                ))  # fmt: skip
                break
        fixes.sort(key=lambda f: (bool(f.rule_violations), bool(f.breaks), f.step_percent))

        top = [e for e in effects if e.evidence == "confirmed_in_model"][:3]
        verb = "fails" if crit.passed is False else "has the smallest margin"
        explanation = (
            f"{crit.label} {verb}: measured {crit.measured:.3g} {crit.unit} against "
            f"{crit.comparator} {crit.limit:.3g} {crit.unit} in the {run.scenario['label']} "
            f"scenario. Limit: {source}."
        )
        if top:
            unit = "s less off the road" if probe != crit.id else crit.unit
            explanation += (
                " Largest measured effects (one 10 % step): "
                + "; ".join(
                    f"{e.label} ({e.better_direction} helps by "
                    f"{max(e.margin_up or 0, e.margin_down or 0):.3g} {unit})".replace(" )", ")")
                    for e in top
                )
                + "."
            )
        clean = [f for f in fixes if not f.rule_violations and not f.breaks]
        if crit.passed is not False:
            pass
        elif clean:
            f = clean[0]
            explanation += (
                f" Smallest tested fix in the model: {f.operation} the {f.label.lower()} from "
                f"{f.from_value:g} to {f.to_value:g} {f.unit} ({f.step_percent:g} %)."
            )
        elif fixes:
            explanation += " Tested single-parameter fixes break other criteria or rules."
        else:
            explanation += " No single parameter within ±30 % fixes it in the model."
        findings.append(Finding(
            criterion=crit.id, label=crit.label,
            status="failed" if crit.passed is False else "tightest_margin",
            measured=crit.measured, limit=crit.limit, unit=crit.unit, margin=crit.margin,
            limit_source=source, governing_parameter=governing, effects=effects, fixes=fixes,
            explanation=explanation,
        ))  # fmt: skip

    if failed:
        recommendation = (
            "Apply a fix that keeps the other criteria and rules satisfied, then rerun "
            f"'{run.test_name}' ({run.scenario['label']}) to confirm it with a full run."
        )
    else:
        recommendation = "No criterion failed; the finding shows the tightest margin."
    return Diagnosis(
        run_id=run.id,
        test_id=run.test_id,
        target=run.target,
        scenario_id=scenario,
        scenario_label=run.scenario["label"],
        design_revision=run.revision.history_cursor,
        current=current,
        status=run.status.value,
        findings=findings,
        evidence={
            "run": run.id,
            "solver": run.solver,
            "values_hash": run.revision.values_hash,
            "perturbation_runs": sum(1 for x in perturbed.values() if x is not None),
            "step": f"±{STEPS[0] * 100:g} % per parameter (clamped to its bounds)",
            "warnings": run.warnings,
        },
        recommendation=recommendation,
        caveats=[
            "Effects are measured in the model by re-simulating the same scenario; they are "
            "not physical root causes.",
            "Perturbation runs skip the half-step convergence check; a fix counts only after "
            "a full test run on the changed design.",
            *run.assumptions,
        ],
    )
