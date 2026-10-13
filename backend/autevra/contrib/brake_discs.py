"""Example plugin: ventilated brake discs with caliper envelopes, and a disc temperature test.

Enable with ``AUTEVRA_PLUGINS=autevra.contrib.brake_discs``. It shows every extension point:
parameters (with aliases), derived values, a packaging rule, a CAD builder, four components
mated to the existing axle hubs, exact clearance checks against the wheels, and an
analytical test. See docs/EXTENDING.md.
"""

import math
from collections.abc import Mapping

from autevra.assembly import transforms as tf
from autevra.assembly.vehicle import ComponentDef, Mate
from autevra.cad import kernel as k
from autevra.cad.components import RIM_BARREL
from autevra.domain import derived as d
from autevra.domain.derived import DerivedDef
from autevra.domain.parameters import ParameterDef
from autevra.domain.rules import Rule
from autevra.domain.units import Unit
from autevra.engineering.integration import Clearance
from autevra.engineering.testing import Credibility, Scenario, TestDefinition
from autevra.extensions import Plugin

Values = Mapping[str, float]
CALIPER_RADIAL = 35.0  # mm the caliper reaches beyond the disc edge
CALIPER_GAP = 8.0  # mm minimum gap from the caliper to the rim barrel
IRON_DENSITY = 7200.0  # kg/m³, grey cast iron
IRON_HEAT = 460.0  # J/(kg K)
VENT_FILL = 0.7  # solid share of a ventilated disc's swept volume
INNER_RATIO = 0.5  # friction ring inner radius / outer radius


def _param(axle: str, what: str, default: float, lo: float, hi: float) -> ParameterDef:
    a = axle.capitalize()
    label = {"disc_diameter": "brake disc diameter", "disc_thickness": "brake disc thickness"}[what]
    return ParameterDef(
        id=f"{axle}_{what}",
        label=f"{a} {label}",
        group="brakes",
        unit=Unit.MM,
        default=default,
        min=lo,
        max=hi,
        step=1,
        description=f"{a} {label} (ventilated cast-iron disc).",
        aliases=(f"{axle} {label}", f"{axle} {label.replace('brake ', '')}"),
    )


PARAMETERS = (
    _param("front", "disc_diameter", 300, 200, 450),
    _param("front", "disc_thickness", 26, 10, 40),
    _param("rear", "disc_diameter", 280, 200, 450),
    _param("rear", "disc_thickness", 20, 10, 40),
)


def disc_mass(p: Values, axle: str) -> float:
    r = p[f"{axle}_disc_diameter"] / 2000.0
    t = p[f"{axle}_disc_thickness"] / 1000.0
    return IRON_DENSITY * VENT_FILL * math.pi * (r * r - (INNER_RATIO * r) ** 2) * t


DERIVED = tuple(
    (
        DerivedDef(
            id=f"{axle}_disc_mass",
            label=f"{axle.capitalize()} brake disc mass",
            unit="kg",
            controlled_by=(f"{axle}_disc_diameter", f"{axle}_disc_thickness"),
            aliases=(f"{axle} disc mass", f"{axle} brake disc mass"),
        ),
        lambda p, axle=axle: disc_mass(p, axle),
    )
    for axle in d.AXLES
)


def _fits(axle: str):  # type: ignore[no-untyped-def]
    def rule(p: Values) -> str | None:
        room = d.rim_diameter_mm(p) / 2.0 - RIM_BARREL - CALIPER_GAP
        need = p[f"{axle}_disc_diameter"] / 2.0 + CALIPER_RADIAL
        if need > room:
            return (
                f"{axle} brake disc and caliper need {need:.1f} mm of radius inside the rim, "
                f"only {room:.1f} mm is available: fit bigger wheels or a smaller disc"
            )
        return None

    return rule


RULES = tuple(
    (
        Rule(
            id=f"{axle}_disc_fits_rim",
            description=f"{axle.capitalize()} brake disc and caliper must fit inside the rim.",
            parameters=(f"{axle}_disc_diameter", "rim_diameter"),
        ),
        _fits(axle),
    )
    for axle in d.AXLES
)


def build_brake_disc(p: Mapping[str, float]) -> k.Shape:
    """Disc (friction ring and hat) on the hub, with a caliper envelope at the rear.
    Local frame as the wheel's: origin at the hub, axis along Y, outboard towards +Y."""
    r, t = p["diameter"] / 2.0, p["thickness"]
    ring = k.ring_y(r, INNER_RATIO * r, (2.0, 2.0 + t))
    hat = k.ring_y(INNER_RATIO * r + 2.0, 40.0, (2.0 + t, 2.0 + t + 30.0))
    caliper = k.box((-(r + CALIPER_RADIAL), -(r - 45.0)), (-12.0, t + 16.0), (-55.0, 55.0))
    return k.fuse(ring, hat, caliper)


def _disc(cid: str, name: str, axle: str, side: str) -> ComponentDef:
    geometry = (f"{axle}_disc_diameter", f"{axle}_disc_thickness")
    return ComponentDef(
        id=cid,
        name=name,
        category="brakes",
        builder="brake_disc",
        geometry=geometry,
        inputs=lambda p: {"diameter": p[geometry[0]], "thickness": p[geometry[1]]},
        frames={"hub": ()},
        interfaces=lambda p: {"hub": tf.identity()},
        mate=Mate(f"{axle}_axle", f"hub_{side}", "hub"),
        color=(0.55, 0.12, 0.12),
    )


CORNERS = (
    ("fl", "front", "left"),
    ("fr", "front", "right"),
    ("rl", "rear", "left"),
    ("rr", "rear", "right"),
)
COMPONENTS = tuple(_disc(f"disc_{c}", f"Brake disc {a} {s}", a, s) for c, a, s in CORNERS)
CLEARANCES = tuple(
    Clearance(
        f"disc_{c}",
        f"wheel_{c}",
        3.0,
        "brake caliper clearance to the rim",
        (f"{a}_disc_diameter", "rim_diameter"),
    )
    for c, a, _ in CORNERS
)


# --- Analytical test: disc temperature rise in one stop ----------------------------------


def _inputs(axle: str) -> tuple[str, ...]:
    return (
        "vehicle_mass",
        "front_mass_distribution",
        "cg_height",
        "wheelbase",
        f"{axle}_disc_diameter",
        f"{axle}_disc_thickness",
    )


def _run(values: Values, axle: str, scenario: Scenario):  # type: ignore[no-untyped-def]
    mass = values["vehicle_mass"] + 75.0
    v = scenario.speed_kmh / 3.6
    mu = scenario.friction
    f = values["front_mass_distribution"] / 100.0
    transfer = mu * values["cg_height"] / values["wheelbase"]
    front_share = min(1.0, f + transfer)  # ideal brake distribution at deceleration mu*g
    share = front_share if axle == "front" else 1.0 - front_share
    energy = 0.5 * mass * v * v * share / 2.0  # per disc
    m_disc = disc_mass(values, axle)
    metrics = {
        "energy_per_disc": energy / 1000.0,
        "disc_temperature_rise": energy / (m_disc * IRON_HEAT),
        "axle_brake_share": share * 100.0,
    }
    solver = {
        "id": "autevra.contrib.brake_heat",
        "version": "1.0.0",
        "method": "energy balance, single stop",
    }
    return metrics, {"converged": True, "finite": True}, solver, [], {"trace": {}, "config": {}}


BRAKE_HEAT = TestDefinition(
    id="brake_heat",
    name="Brake disc heating (analytical)",
    description="Temperature rise of each disc in one full stop: kinetic energy split by the "
    "ideal brake distribution, all heat into the disc, no cooling (conservative).",
    solver="autevra.contrib.brake_heat",
    credibility=Credibility.ANALYTICAL_ESTIMATE,
    targets=("front", "rear"),
    components={"front": ("disc_fl", "disc_fr"), "rear": ("disc_rl", "disc_rr")},
    inputs=_inputs,
    scenarios=(
        Scenario(
            "stop_100",
            "Stop from 100 km/h",
            "brake",
            0,
            0,
            100,
            0,
            friction=1.0,
            note="Deceleration at friction 1.0 (about 1 g).",
        ),
        Scenario(
            "stop_200",
            "Stop from 200 km/h",
            "brake",
            0,
            0,
            200,
            0,
            friction=1.0,
            note="High-speed stop at friction 1.0.",
        ),
    ),
    criteria=(),
    metrics={
        "energy_per_disc": ("Energy per disc", "kJ", True),
        "disc_temperature_rise": ("Disc temperature rise", "K", True),
        "axle_brake_share": ("Axle share of braking", "%", False),
    },
    assumptions=(
        "All braking energy enters the disc; no pad heat share, no cooling.",
        f"Ventilated cast-iron disc: {IRON_DENSITY:g} kg/m³, {IRON_HEAT:g} J/(kg K), "
        f"{VENT_FILL:.0%} solid.",
    ),
    run=_run,
)

PLUGIN = Plugin(
    name="brake_discs",
    version="1.0.0",
    description="Ventilated brake discs, caliper envelopes, rim fit rule and disc heating test.",
    parameters=PARAMETERS,
    group_aliases={
        "brake discs": ("front_disc_diameter", "rear_disc_diameter"),
        "discs": ("front_disc_diameter", "rear_disc_diameter"),
    },
    derived=DERIVED,
    rules=RULES,
    builders={"brake_disc": build_brake_disc},
    components=COMPONENTS,
    clearances=CLEARANCES,
    tests=(BRAKE_HEAT,),
)
