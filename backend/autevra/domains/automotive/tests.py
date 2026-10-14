"""Automotive component tests: quarter-car ride, ride modes and longitudinal performance.

Registered by the automotive domain module. Each definition names its solver, the
parameters it reads, its scenarios and criteria (limits from the design, never invented),
and hooks that explain its limits to the diagnosis and propose optimisation variables.
"""

from collections.abc import Mapping

from autevra.core.parameters import REGISTRY
from autevra.domains.automotive import derived as d
from autevra.domains.automotive.sim import half_car as hc
from autevra.domains.automotive.sim import longitudinal as lg
from autevra.domains.automotive.sim import quarter_car as qc
from autevra.engineering.testing import (
    Credibility,
    Criterion,
    CriterionResult,
    Scenario,
    TestDefinition,
)

Values = Mapping[str, float]


def explain_travel_limit(criterion: CriterionResult, values: Values, target: str):  # type: ignore[no-untyped-def]
    """How the usable wheel travel is set: which packaging limit governs."""
    if criterion.id not in ("bump_travel", "rebound_travel"):
        return None
    limits = d.travel_limits(values, target)
    keys = d.BUMP_LIMITS if criterion.id == "bump_travel" else d.REBOUND_LIMITS
    governing = min(keys, key=lambda k: limits[k][0])
    parts = ", ".join(f"{k.replace('_', ' ')} {limits[k][0]:.1f} mm" for k in keys)
    return (f"usable travel is the smallest of: {parts}; the "
            f"{governing.replace('_', ' ')} governs", limits[governing][1])  # fmt: skip


def corner_variables(target: str, values: Values, spread: float = 0.3):  # type: ignore[no-untyped-def]
    """Spring rate and damping of the corner, ±``spread`` around the design, within bounds."""
    out = []
    for suffix in ("spring_rate", "damping_bump", "damping_rebound"):
        pid = f"{target}_{suffix}"
        spec = REGISTRY[pid]
        v = values[pid]
        out.append((pid, max(spec.min, v * (1 - spread)), min(spec.max, v * (1 + spread))))
    return out


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


def road(scenario: Scenario) -> qc.Road:
    """Scenario (engineering units) to the solver's road input (SI)."""
    return qc.Road(scenario.road, scenario.height_mm / 1000, scenario.length_m,
                   scenario.speed_kmh / 3.6)  # fmt: skip


def _run_quarter_car(values: Values, axle: str, scenario: Scenario, quick: bool = False):  # type: ignore[no-untyped-def]
    params = quarter_car_params(values, axle)
    config = qc.Config(duration=scenario.duration_s, check_convergence=not quick,
                       trace_points=2 if quick else 600)  # fmt: skip
    result = qc.simulate(params, road(scenario), config)
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
    solver_version=qc.SOLVER_VERSION,
    explain_limit=explain_travel_limit,
    default_variables=corner_variables,
    proxies={"tyre_contact": "lift_off_time"},  # tyre load saturates at 0 when off the road
)


# --- Half-car ride test (bounce and pitch) -----------------------------------------------


def half_car_inputs(target: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(
        (*quarter_car_inputs("front"), *quarter_car_inputs("rear"), "wheelbase",
         "pitch_dynamic_index")
    ))  # fmt: skip


def half_car_params(values: Values) -> hc.Params:
    """Whole-vehicle solver inputs (SI). The sprung-mass centre sits where the axle sprung
    loads balance; the pitch inertia comes from the dynamic index."""
    front, rear = (
        2 * d.sprung_corner_mass(values, "front"),
        2 * d.sprung_corner_mass(values, "rear"),
    )
    mass = front + rear
    wheelbase = values["wheelbase"] / 1000.0
    b = wheelbase * front / mass  # rear axle to the CG
    a = wheelbase - b
    return hc.Params(
        sprung_mass=mass, front_to_cg=a, rear_to_cg=b,
        pitch_inertia=hc.pitch_inertia(mass, a, b, values["pitch_dynamic_index"]),
        front_unsprung_mass=values["front_unsprung_mass"],
        rear_unsprung_mass=values["rear_unsprung_mass"],
        front_spring_rate=values["front_spring_rate"] * 1000.0,
        rear_spring_rate=values["rear_spring_rate"] * 1000.0,
        front_damping_bump=values["front_damping_bump"],
        front_damping_rebound=values["front_damping_rebound"],
        rear_damping_bump=values["rear_damping_bump"],
        rear_damping_rebound=values["rear_damping_rebound"],
        tyre_stiffness=values["tyre_vertical_stiffness"] * 1000.0,
    )  # fmt: skip


def _run_half_car(values: Values, target: str, scenario: Scenario, quick: bool = False):  # type: ignore[no-untyped-def]
    params = half_car_params(values)
    config = hc.Config(duration=max(scenario.duration_s, 3.5), check_convergence=not quick,
                       trace_points=2 if quick else 600)  # fmt: skip
    result = hc.simulate(params, road(scenario), config)
    bounce, pitch = hc.body_frequencies(params)
    solver_inputs = {k: round(v, 6) for k, v in params.__dict__.items()} | {
        "body_frequencies_Hz": [round(bounce, 4), round(pitch, 4)]
    }
    config_out = {"dt": config.dt, "duration": config.duration, "solver_inputs": solver_inputs}
    return (result.metrics, result.numerics, result.solver, result.warnings,
            {"trace": result.trace, "config": config_out})  # fmt: skip


def explain_half_car_limit(criterion: CriterionResult, values: Values, target: str):  # type: ignore[no-untyped-def]
    axle, _, rest = criterion.id.partition("_")
    if axle not in ("front", "rear") or rest not in ("bump_travel", "rebound_travel"):
        return None
    inner = criterion.model_copy(update={"id": rest})
    return explain_travel_limit(inner, values, axle)


def vehicle_variables(target: str, values: Values, spread: float = 0.3):  # type: ignore[no-untyped-def]
    """Springs and dampers of both axles, ±``spread`` around the design."""
    return [v for axle in ("front", "rear") for v in corner_variables(axle, values, spread)]


def _axle_criteria(axle: str) -> tuple[Criterion, ...]:
    return (
        Criterion(f"{axle}_bump_travel", f"{axle.title()} bump travel within the usable travel",
                  f"{axle}_max_bump_travel", "<=", "mm",
                  limit_from=f"{axle}_available_bump_travel", source="design"),
        Criterion(f"{axle}_rebound_travel",
                  f"{axle.title()} rebound travel within the usable travel",
                  f"{axle}_max_rebound_travel", "<=", "mm",
                  limit_from=f"{axle}_available_rebound_travel", source="design"),
        Criterion(f"{axle}_tyre_contact", f"{axle.title()} tyres stay on the road",
                  f"{axle}_min_tyre_load_ratio", ">", "", limit=0.0),
    )  # fmt: skip


HALF_CAR = TestDefinition(
    id="half_car",
    name="Half-car ride test (bounce and pitch)",
    description="The whole vehicle over a road event, front axle first and the rear a "
    "wheelbase later: body heave and pitch, travel on both axles, tyre contact.",
    solver=hc.SOLVER_ID,
    credibility=Credibility.NUMERICAL_SIMULATION,
    targets=("vehicle",),
    components={
        "vehicle": (
            "body",
            "damper_fl",
            "damper_fr",
            "damper_rl",
            "damper_rr",
            "wheel_fl",
            "wheel_fr",
            "wheel_rl",
            "wheel_rr",
            "front_axle",
            "rear_axle",
        ),
    },  # fmt: skip
    inputs=half_car_inputs,
    scenarios=QUARTER_CAR.scenarios,
    criteria=(*_axle_criteria("front"), *_axle_criteria("rear")),
    metrics=hc.METRICS,
    assumptions=hc.ASSUMPTIONS,
    run=_run_half_car,
    solver_version=hc.SOLVER_VERSION,
    explain_limit=explain_half_car_limit,
    default_variables=vehicle_variables,
    proxies={"front_tyre_contact": "lift_off_time", "rear_tyre_contact": "lift_off_time"},
)


# --- Ride modes (analytical) ------------------------------------------------------------


def _run_ride_modes(values: Values, axle: str, scenario: Scenario, quick: bool = False):  # type: ignore[no-untyped-def]
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
    default_variables=corner_variables,
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
    solver_version=lg.SOLVER_VERSION,
)

DEFINITIONS: tuple[TestDefinition, ...] = (QUARTER_CAR, HALF_CAR, RIDE_MODES, LONGITUDINAL)
