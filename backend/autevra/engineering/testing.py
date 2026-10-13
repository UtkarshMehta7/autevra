"""Component test framework: definitions, criteria, runs and comparisons.

A test definition says which simulator it runs, which design parameters it reads (so the
dependency graph knows when a result goes stale), which scenarios it covers and which
criteria decide pass or fail. Results are labelled by credibility; nothing here marks a
result as experimentally validated.

A run passes only when every criterion holds *and* the numerics are valid:
- ``passed_within_model``: all criteria met by the model's computed results;
- ``failed``: at least one criterion not met;
- ``no_criteria``: results computed, but no criterion was defined, so no verdict;
- ``invalid``: inputs or numerics not acceptable (e.g. not converged), no verdict.
"""

import hashlib
import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field

from autevra.domain import derived as d
from autevra.domain.parameters import REGISTRY
from autevra.sim import longitudinal as lg
from autevra.sim import quarter_car as qc

Values = Mapping[str, float]


class Credibility(StrEnum):
    ANALYTICAL_ESTIMATE = "analytical_estimate"
    NUMERICAL_SIMULATION = "numerical_simulation"
    EXPERIMENTALLY_VALIDATED = "experimentally_validated"  # needs test data; never automatic


class RunStatus(StrEnum):
    PASSED_WITHIN_MODEL = "passed_within_model"
    FAILED = "failed"
    NO_CRITERIA = "no_criteria"
    INVALID = "invalid"


class ComponentStatus(StrEnum):
    NOT_TESTED = "not_tested"
    STALE = "stale"  # results exist, but the inputs changed since
    FAILED = "failed"
    PASSED_WITHIN_MODEL = "passed_within_model"
    NO_CRITERIA = "no_criteria"
    INVALID = "invalid"
    EXPERIMENTALLY_VALIDATED = "experimentally_validated"


COMPARATORS: dict[str, Callable[[float, float], bool]] = {
    "<=": lambda m, lim: m <= lim,
    "<": lambda m, lim: m < lim,
    ">=": lambda m, lim: m >= lim,
    ">": lambda m, lim: m > lim,
}


@dataclass(frozen=True)
class Scenario:
    id: str
    label: str
    road: str  # step | bump | pothole
    height_mm: float
    length_m: float
    speed_kmh: float
    duration_s: float = 3.0
    note: str = ""
    friction: float = 1.0  # tyre-road friction for vehicle-level manoeuvres

    def road_si(self) -> qc.Road:
        return qc.Road(self.road, self.height_mm / 1000, self.length_m, self.speed_kmh / 3.6)


@dataclass(frozen=True)
class Criterion:
    """``limit`` is a number, or ``limit_from`` names a derived value ({axle} is filled in)."""

    id: str
    label: str
    metric: str
    comparator: str
    unit: str
    limit: float | None = None
    limit_from: str | None = None
    source: str = "test_definition"  # test_definition | design | user

    def resolve_limit(self, values: Values, target: str) -> tuple[float, tuple[str, ...]]:
        if self.limit_from is None:
            assert self.limit is not None
            return self.limit, ()
        did = self.limit_from.format(axle=target)
        return d.compute(did, values), d.DERIVED[did].controlled_by


class CriterionResult(BaseModel):
    id: str
    label: str
    metric: str
    comparator: str
    limit: float
    unit: str
    measured: float | None
    passed: bool | None  # None: the metric was not available
    source: str
    limit_parameters: list[str] = []
    margin: float | None = None  # limit - measured for <=, measured - limit for >=


class Revision(BaseModel):
    """The exact design the run used."""

    values_hash: str
    inputs_hash: str  # hash of only the parameters this test reads
    history_cursor: int
    entry_id: str | None  # history entry at the cursor (None: the initial design)


class RunRecord(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    test_id: str
    test_name: str
    target: str
    scenario: dict
    revision: Revision
    inputs: dict[str, dict]  # parameter -> {value, unit, label}
    solver: dict[str, str]
    config: dict
    numerics: dict
    metrics: dict[str, dict]  # id -> {value, unit, label, lower_is_better}
    criteria: list[CriterionResult]
    status: RunStatus
    credibility: Credibility
    assumptions: list[str]
    warnings: list[str]
    trace: dict[str, list[float]] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class Requirement:
    """A user-defined criterion. Only approved requirements take part in verdicts."""

    id: str
    test_id: str
    target: str  # front | rear | *
    scenario_id: str  # scenario id | *
    metric: str
    comparator: str
    limit: float
    unit: str
    approved: bool = True
    note: str = ""

    def applies(self, test_id: str, target: str, scenario_id: str) -> bool:
        return (
            self.approved
            and self.test_id == test_id
            and self.target in ("*", target)
            and self.scenario_id in ("*", scenario_id)
        )

    def criterion(self) -> Criterion:
        label = f"{self.metric} {self.comparator} {self.limit:g} {self.unit}".strip()
        return Criterion(f"user:{self.id}", label, self.metric, self.comparator, self.unit,
                         limit=self.limit, source="user")  # fmt: skip


@dataclass(frozen=True)
class TestDefinition:
    id: str
    name: str
    description: str
    solver: str
    credibility: Credibility
    targets: tuple[str, ...]
    components: Mapping[str, tuple[str, ...]]  # target -> component ids under test
    inputs: Callable[[str], tuple[str, ...]]  # target -> parameter ids read
    scenarios: tuple[Scenario, ...]
    criteria: tuple[Criterion, ...]
    metrics: Mapping[str, tuple[str, str, bool]]  # id -> (label, unit, lower is better)
    assumptions: tuple[str, ...]
    run: Callable[[Values, str, Scenario], tuple[dict, dict, dict, list[str], dict]] = field(
        repr=False, default=lambda v, t, s: ({}, {}, {}, [], {})
    )

    def scenario(self, scenario_id: str) -> Scenario:
        for s in self.scenarios:
            if s.id == scenario_id:
                return s
        raise KeyError(f"unknown scenario '{scenario_id}' for test '{self.id}'")


# --- Quarter-car ride test -------------------------------------------------------------

_CORNERS = {"front": ("fl", "fr"), "rear": ("rl", "rr")}


def quarter_car_inputs(axle: str) -> tuple[str, ...]:
    """Parameters the quarter-car test reads: the dynamic model and the travel limits."""
    return (
        "vehicle_mass", "front_mass_distribution", f"{axle}_unsprung_mass",
        f"{axle}_spring_rate", f"{axle}_damping_bump", f"{axle}_damping_rebound",
        "tyre_vertical_stiffness", f"{axle}_bump_travel", f"{axle}_rebound_travel",
        "arch_clearance", f"{axle}_damper_stroke", f"{axle}_shock_mount_height",
        "rim_diameter", "tyre_width", "tyre_aspect_ratio",
    )  # fmt: skip


def quarter_car_params(values: Values, axle: str) -> qc.Params:
    """Design parameters (engineering units) to solver inputs (SI)."""
    return qc.Params(
        sprung_mass=d.sprung_corner_mass(values, axle),
        unsprung_mass=values[f"{axle}_unsprung_mass"],
        spring_rate=values[f"{axle}_spring_rate"] * 1000.0,  # N/mm -> N/m
        damping_bump=values[f"{axle}_damping_bump"],
        damping_rebound=values[f"{axle}_damping_rebound"],
        tyre_stiffness=values["tyre_vertical_stiffness"] * 1000.0,
    )


def _run_quarter_car(values: Values, axle: str, scenario: Scenario):  # type: ignore[no-untyped-def]
    params = quarter_car_params(values, axle)
    config = qc.Config(duration=scenario.duration_s)
    result = qc.simulate(params, scenario.road_si(), config)
    solver_inputs = {
        "sprung_mass_kg": params.sprung_mass, "unsprung_mass_kg": params.unsprung_mass,
        "spring_rate_N_per_m": params.spring_rate, "damping_bump_Ns_per_m": params.damping_bump,
        "damping_rebound_Ns_per_m": params.damping_rebound,
        "tyre_stiffness_N_per_m": params.tyre_stiffness,
    }  # fmt: skip
    config_out = {"dt": config.dt, "duration": config.duration, "solver_inputs": solver_inputs}
    return (
        result.metrics,
        result.numerics,
        result.solver,
        result.warnings,
        {
            "trace": result.trace,
            "config": config_out,
        },
    )


QUARTER_CAR = TestDefinition(
    id="quarter_car",
    name="Quarter-car ride test",
    description="One corner over a road event: body acceleration, wheel travel against the "
    "usable travel, tyre contact and settling.",
    solver=qc.SOLVER_ID,
    credibility=Credibility.NUMERICAL_SIMULATION,
    targets=("front", "rear"),
    components={
        axle: (f"damper_{c[0]}", f"damper_{c[1]}", f"wheel_{c[0]}", f"wheel_{c[1]}", f"{axle}_axle")
        for axle, c in _CORNERS.items()
    },  # fmt: skip
    inputs=quarter_car_inputs,
    scenarios=(
        Scenario(
            "step_25",
            "25 mm step",
            "step",
            25,
            0.25,
            30,
            note="Kerb-like step, half-cosine ramp over 0.25 m at 30 km/h.",
        ),
        Scenario(
            "hump_75",
            "75 mm road hump",
            "bump",
            75,
            3.7,
            25,
            note="Cosine approximation of a 75 mm x 3.7 m round-top hump at 25 km/h.",
        ),
        Scenario(
            "pothole_50",
            "50 mm pothole",
            "pothole",
            50,
            0.6,
            40,
            note="Cosine dip 50 mm deep, 0.6 m long, at 40 km/h.",
        ),
    ),  # fmt: skip
    criteria=(
        Criterion(
            "bump_travel",
            "Bump travel within the usable travel",
            "max_bump_travel",
            "<=",
            "mm",
            limit_from="{axle}_available_bump_travel",
            source="design",
        ),
        Criterion(
            "rebound_travel",
            "Rebound travel within the usable travel",
            "max_rebound_travel",
            "<=",
            "mm",
            limit_from="{axle}_available_rebound_travel",
            source="design",
        ),
        Criterion(
            "tyre_contact", "Tyre stays on the road", "min_tyre_load_ratio", ">", "", limit=0.0
        ),
    ),  # fmt: skip
    metrics=qc.METRICS,
    assumptions=qc.ASSUMPTIONS,
    run=_run_quarter_car,
)


# --- Ride modes (analytical) ------------------------------------------------------------


def _run_ride_modes(values: Values, axle: str, scenario: Scenario):  # type: ignore[no-untyped-def]
    params = quarter_car_params(values, axle)
    body, hop = qc.natural_frequencies(params)
    metrics = {
        "body_bounce_frequency": body,
        "wheel_hop_frequency": hop,
        "damping_ratio_bump": d.damping_ratio(values, axle, "bump"),
        "damping_ratio_rebound": d.damping_ratio(values, axle, "rebound"),
    }
    solver = {"id": "autevra.ride_modes", "version": "1.0.0", "method": "closed-form 2-DOF"}
    return metrics, {"converged": True, "finite": True}, solver, [], {"trace": {}, "config": {}}


RIDE_MODES = TestDefinition(
    id="ride_modes",
    name="Ride modes (analytical)",
    description="Undamped body-bounce and wheel-hop frequencies from the 2-DOF characteristic "
    "equation, and damping ratios. No default criteria: add your own requirements.",
    solver="autevra.ride_modes",
    credibility=Credibility.ANALYTICAL_ESTIMATE,
    targets=("front", "rear"),
    components=QUARTER_CAR.components,
    inputs=lambda a: quarter_car_inputs(a)[:7],
    scenarios=(
        Scenario(
            "modal",
            "Modal estimate",
            "flat",
            0,
            1,
            1,
            0,
            note="No road input: eigenvalues of the linear model.",
        ),
    ),  # fmt: skip
    criteria=(),
    metrics={
        "body_bounce_frequency": ("Body bounce frequency", "Hz", False),
        "wheel_hop_frequency": ("Wheel hop frequency", "Hz", False),
        "damping_ratio_bump": ("Bump damping ratio", "", False),
        "damping_ratio_rebound": ("Rebound damping ratio", "", False),
    },
    assumptions=("Linear, undamped 2-DOF model of one corner; tyre and spring in series.",),
    run=_run_ride_modes,
)

# --- Longitudinal performance -----------------------------------------------------------

DRIVER_KG = 75.0  # test mass = vehicle mass + driver


def longitudinal_inputs(target: str) -> tuple[str, ...]:
    return (
        "vehicle_mass", "front_mass_distribution", "peak_power", "drivetrain_efficiency",
        "front_drive_share", "cg_height", "wheelbase", "drag_coefficient", "body_width",
        "overall_height", "ground_clearance", "rolling_resistance",
    )  # fmt: skip


def longitudinal_params(values: Values) -> lg.Params:
    return lg.Params(
        mass=values["vehicle_mass"] + DRIVER_KG,
        power=values["peak_power"] * 1000.0,
        efficiency=values["drivetrain_efficiency"] / 100.0,
        front_drive_share=values["front_drive_share"] / 100.0,
        front_static_share=values["front_mass_distribution"] / 100.0,
        cg_height=values["cg_height"] / 1000.0,
        wheelbase=values["wheelbase"] / 1000.0,
        drag_area=values["drag_coefficient"] * d.frontal_area(values),
        rolling_resistance=values["rolling_resistance"],
    )


def _manoeuvre(scenario: Scenario) -> lg.Manoeuvre:
    kind = "accelerate" if scenario.road == "accelerate" else "brake"
    return lg.Manoeuvre(kind=kind, friction=scenario.friction, v_end=scenario.speed_kmh / 3.6)


def _run_longitudinal(values: Values, target: str, scenario: Scenario, quick: bool = False):  # type: ignore[no-untyped-def]
    params = longitudinal_params(values)
    config = lg.Config(check_convergence=not quick, trace_points=2 if quick else 400)
    result = lg.simulate(params, _manoeuvre(scenario), config)
    solver_inputs = {k: getattr(params, k) for k in params.__dataclass_fields__}
    config_out = {"dt": config.dt, "solver_inputs": solver_inputs}
    return (
        result.metrics,
        result.numerics,
        result.solver,
        result.warnings,
        {
            "trace": result.trace,
            "config": config_out,
        },
    )


LONGITUDINAL = TestDefinition(
    id="longitudinal",
    name="Longitudinal performance",
    description="Straight-line 0–100 km/h acceleration and 100–0 km/h braking with traction "
    "limits, load transfer, drag and rolling resistance. No default criteria: add "
    "requirements such as a 0–100 km/h time or a stopping distance.",
    solver=lg.SOLVER_ID,
    credibility=Credibility.NUMERICAL_SIMULATION,
    targets=("vehicle",),
    components={
        "vehicle": ("wheel_fl", "wheel_fr", "wheel_rl", "wheel_rr", "front_axle", "rear_axle")
    },  # fmt: skip
    inputs=longitudinal_inputs,
    scenarios=(
        Scenario(
            "accel_0_100",
            "0–100 km/h, dry",
            "accelerate",
            0,
            0,
            100,
            60,
            note="Full power from rest on dry asphalt (friction 1.0).",
            friction=1.0,
        ),
        Scenario(
            "brake_100_0_dry",
            "100–0 km/h, dry",
            "brake",
            0,
            0,
            100,
            60,
            note="Full braking from 100 km/h, dry asphalt (friction 1.0), 0.15 s build-up.",
            friction=1.0,
        ),
        Scenario(
            "brake_100_0_wet",
            "100–0 km/h, wet",
            "brake",
            0,
            0,
            100,
            60,
            note="Full braking from 100 km/h, wet asphalt (friction 0.6), 0.15 s build-up.",
            friction=0.6,
        ),
    ),  # fmt: skip
    criteria=(),
    metrics=lg.METRICS,
    assumptions=(
        *lg.ASSUMPTIONS,
        f"Test mass is the vehicle mass plus a {DRIVER_KG:g} kg driver.",
        f"Frontal area estimated as {d.FRONTAL_FILL} x width x height above ground.",
    ),  # fmt: skip
    run=_run_longitudinal,
)

DEFINITIONS: dict[str, TestDefinition] = {t.id: t for t in (QUARTER_CAR, RIDE_MODES, LONGITUDINAL)}


def register_test(definition: TestDefinition) -> TestDefinition:
    """Add a test definition (extension point; see docs/EXTENDING.md)."""
    if definition.id in DEFINITIONS:
        raise ValueError(f"test '{definition.id}' is already registered")
    DEFINITIONS[definition.id] = definition
    return definition


# --- Running ------------------------------------------------------------------------


def _hash(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def values_hash(values: Values) -> str:
    return _hash({k: round(float(v), 9) for k, v in values.items()})


def inputs_hash(definition: TestDefinition, target: str, scenario: Scenario, values: Values,
                requirements: Iterable[Requirement] = ()) -> str:  # fmt: skip
    """Changes when anything that can change this run's result changes."""
    return _hash({
        "test": definition.id, "target": target, "scenario": scenario.__dict__,
        "solver": definition.solver, "version": qc.SOLVER_VERSION,
        "inputs": {p: round(float(values[p]), 9) for p in definition.inputs(target)},
        "requirements": sorted(r.id for r in requirements
                               if r.applies(definition.id, target, scenario.id)),
    })  # fmt: skip


def evaluate(definition: TestDefinition, target: str, scenario: Scenario, values: Values,
             metrics: Mapping[str, float | None], requirements: Iterable[Requirement] = ()
             ) -> list[CriterionResult]:  # fmt: skip
    criteria = [*definition.criteria] + [
        r.criterion() for r in requirements if r.applies(definition.id, target, scenario.id)
    ]
    out = []
    for c in criteria:
        limit, limit_params = c.resolve_limit(values, target)
        measured = metrics.get(c.metric)
        passed = None if measured is None else COMPARATORS[c.comparator](measured, limit)
        margin = None
        if measured is not None:
            margin = limit - measured if c.comparator in ("<=", "<") else measured - limit
        out.append(CriterionResult(
            id=c.id, label=c.label, metric=c.metric, comparator=c.comparator,
            limit=round(limit, 6), unit=c.unit,
            measured=None if measured is None else round(measured, 6), passed=passed,
            source=c.source, limit_parameters=list(limit_params),
            margin=None if margin is None else round(margin, 6),
        ))  # fmt: skip
    return out


def run_test(
    test_id: str,
    target: str,
    scenario_id: str,
    values: Values,
    *,
    history_cursor: int = 0,
    entry_id: str | None = None,
    requirements: Iterable[Requirement] = (),
) -> RunRecord:
    definition = DEFINITIONS[test_id]
    if target not in definition.targets:
        raise KeyError(f"test '{test_id}' has no target '{target}'")
    scenario = definition.scenario(scenario_id)
    requirements = list(requirements)
    metrics, numerics, solver, warnings, extra = definition.run(values, target, scenario)
    criteria = evaluate(definition, target, scenario, values, metrics, requirements)
    if not numerics.get("converged") or not numerics.get("finite", True):
        status = RunStatus.INVALID
    elif not criteria:
        status = RunStatus.NO_CRITERIA
    elif any(c.passed is not True for c in criteria):
        status = RunStatus.FAILED
    else:
        status = RunStatus.PASSED_WITHIN_MODEL
    return RunRecord(
        test_id=test_id,
        test_name=definition.name,
        target=target,
        scenario=scenario.__dict__,
        revision=Revision(
            values_hash=values_hash(values),
            inputs_hash=inputs_hash(definition, target, scenario, values, requirements),
            history_cursor=history_cursor,
            entry_id=entry_id,
        ),
        inputs={
            p: {"value": values[p], "unit": str(REGISTRY[p].unit), "label": REGISTRY[p].label}
            for p in definition.inputs(target)
        },
        solver=solver,
        config=extra["config"],
        numerics=numerics,
        metrics={
            k: {
                "value": None if v is None else round(v, 6),
                "label": definition.metrics[k][0],
                "unit": definition.metrics[k][1],
                "lower_is_better": definition.metrics[k][2],
            }
            for k, v in metrics.items()
        },  # fmt: skip
        criteria=criteria,
        status=status,
        credibility=definition.credibility,
        assumptions=list(definition.assumptions),
        warnings=warnings,
        trace=extra["trace"],
    )


def quick_evaluate(
    test_id: str,
    target: str,
    scenario_id: str,
    values: Values,
    requirements: Iterable[Requirement] = (),
) -> tuple[dict[str, float | None], list[CriterionResult]]:
    """Metrics and criteria without a stored record or the half-step convergence rerun.

    For perturbation studies (diagnosis, optimisation) around designs whose numerics a full
    run has checked; anything presented as a result is re-run with ``run_test``.
    """
    definition = DEFINITIONS[test_id]
    scenario = definition.scenario(scenario_id)
    if test_id == "longitudinal":
        metrics = _run_longitudinal(values, target, scenario, quick=True)[0]
    elif test_id == "quarter_car":
        config = qc.Config(duration=scenario.duration_s, check_convergence=False, trace_points=2)
        metrics = qc.simulate(
            quarter_car_params(values, target), scenario.road_si(), config
        ).metrics
    else:
        metrics = definition.run(values, target, scenario)[0]
    return metrics, evaluate(definition, target, scenario, values, metrics, requirements)


def tests_affected(changed: Iterable[str]) -> list[tuple[str, str]]:
    """(test, target) pairs whose results a change to these parameters makes stale."""
    changed = set(changed)
    return [
        (t.id, target)
        for t in DEFINITIONS.values()
        for target in t.targets
        if changed & set(t.inputs(target))
    ]


class MetricDelta(BaseModel):
    metric: str
    label: str
    unit: str
    before: float | None
    after: float | None
    change: float | None
    percent: float | None
    verdict: str  # better | worse | unchanged | n/a


class Comparison(BaseModel):
    baseline: str
    candidate: str
    same_test: bool
    changed_inputs: dict[str, dict]
    metrics: list[MetricDelta]
    criteria: list[dict]
    summary: str


def compare(baseline: RunRecord, candidate: RunRecord) -> Comparison:
    same = (baseline.test_id, baseline.target, baseline.scenario.get("id")) == (
        candidate.test_id, candidate.target, candidate.scenario.get("id"),
    )  # fmt: skip
    changed = {
        p: {"before": baseline.inputs[p]["value"], "after": v["value"], "unit": v["unit"]}
        for p, v in candidate.inputs.items()
        if p in baseline.inputs and baseline.inputs[p]["value"] != v["value"]
    }
    deltas = []
    for key, m in candidate.metrics.items():
        before = baseline.metrics.get(key, {}).get("value")
        after = m["value"]
        if before is None or after is None:
            deltas.append(MetricDelta(
                metric=key, label=m["label"], unit=m["unit"], before=before, after=after,
                change=None, percent=None, verdict="n/a",
            ))  # fmt: skip
            continue
        change = after - before
        tol = 1e-6 + 1e-4 * abs(before)
        if abs(change) <= tol:
            verdict = "unchanged"
        else:
            verdict = "better" if (change < 0) == m["lower_is_better"] else "worse"
        percent = None if before == 0 else round(change / abs(before) * 100, 3)
        deltas.append(MetricDelta(metric=key, label=m["label"], unit=m["unit"], before=before,
                                  after=after, change=round(change, 6), percent=percent,
                                  verdict=verdict))  # fmt: skip
    before_c = {c.id: c for c in baseline.criteria}
    criteria = []
    for c in candidate.criteria:
        prior = before_c.get(c.id)
        criteria.append({
            "id": c.id, "label": c.label, "before": prior.passed if prior else None,
            "after": c.passed, "measured_before": prior.measured if prior else None,
            "measured_after": c.measured, "limit": c.limit, "unit": c.unit,
        })  # fmt: skip
    better = [x.label for x in deltas if x.verdict == "better"]
    worse = [x.label for x in deltas if x.verdict == "worse"]
    summary = (
        f"{baseline.status.value} → {candidate.status.value}. "
        f"Better: {', '.join(better) or 'none'}. Worse: {', '.join(worse) or 'none'}."
    )
    return Comparison(
        baseline=baseline.id, candidate=candidate.id, same_test=same, changed_inputs=changed,
        metrics=deltas, criteria=criteria, summary=summary,
    )  # fmt: skip
