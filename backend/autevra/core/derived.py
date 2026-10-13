"""Derived values: read-only quantities computed from parameters.

Requests to edit a derived value are answered with a clarification naming
the parameters in ``CONTROLLED_BY``.

Suspension values follow textbook relations (each function names its
assumptions). They are analytical estimates for the template, not
measurements of a real vehicle.
"""

import math
from collections.abc import Callable, Mapping

from pydantic import BaseModel, ConfigDict

INCH_MM = 25.4
G = 9.80665  # standard gravity, m/s²

AXLE_RADIUS = 35.0  # mm, beam axle tube radius (shared with the CAD builder)
# Damper length that is not stroke: two mounting eyes, piston and seal head (template value).
DAMPER_DEAD_LENGTH = 100.0  # mm
# Helical spring assumptions: spring steel shear modulus and active coils (template values).
SPRING_SHEAR_MODULUS = 79_300.0  # N/mm² (79.3 GPa)
SPRING_ACTIVE_COILS = 6.0
SPRING_SEAT_OFFSET = 40.0  # mm, damper eye centre to spring seat face, at each end
AXLES = ("front", "rear")

Values = Mapping[str, float]


class DerivedDef(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    unit: str
    controlled_by: tuple[str, ...]
    aliases: tuple[str, ...]


def overall_length(p: Values) -> float:
    return p["front_overhang"] + p["wheelbase"] + p["rear_overhang"]


def tyre_sidewall(p: Values) -> float:
    return p["tyre_width"] * p["tyre_aspect_ratio"] / 100.0


def rim_diameter_mm(p: Values) -> float:
    return p["rim_diameter"] * INCH_MM


def tyre_diameter(p: Values) -> float:
    return rim_diameter_mm(p) + 2.0 * tyre_sidewall(p)


def tyre_radius(p: Values) -> float:
    """Unloaded tyre radius; also the wheel-centre height above the ground."""
    return tyre_diameter(p) / 2.0


def arch_radius(p: Values) -> float:
    return tyre_radius(p) + p["arch_clearance"]


def arch_top_height(p: Values) -> float:
    return tyre_radius(p) + arch_radius(p)


def overall_width_at_tyres(p: Values) -> float:
    return max(p["track_front"], p["track_rear"]) + p["tyre_width"]


def body_floor_height(p: Values) -> float:
    """The ladder frame sits on the ground-clearance line; the body sits on the frame."""
    return p["ground_clearance"] + p["rail_height"]


def body_x_range(p: Values) -> tuple[float, float]:
    """(rear, front) x of the body in ISO 8855 coordinates (front axle at x = 0)."""
    return (-(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"])


def cabin_x_range(p: Values) -> tuple[float, float]:
    rear, front = body_x_range(p)
    centre = (rear + front) / 2.0 + p["cabin_offset"]
    half = p["cabin_length"] / 2.0
    return (centre - half, centre + half)


# --- Suspension (per axle; ``a`` is "front" or "rear") ---
def axle_load(p: Values, a: str) -> float:
    """Static load on one axle, kg."""
    share = p["front_mass_distribution"] / 100.0
    return p["vehicle_mass"] * (share if a == "front" else 1.0 - share)


def sprung_corner_mass(p: Values, a: str) -> float:
    """Sprung mass carried by one corner, kg (half the axle load minus the unsprung mass)."""
    return axle_load(p, a) / 2.0 - p[f"{a}_unsprung_mass"]


def ride_rate(p: Values, a: str) -> float:
    """Spring and tyre in series, N/mm."""
    k, kt = p[f"{a}_spring_rate"], p["tyre_vertical_stiffness"]
    return k * kt / (k + kt)


def ride_frequency(p: Values, a: str) -> float:
    """Undamped body bounce frequency of one corner, Hz."""
    m = sprung_corner_mass(p, a)
    return math.sqrt(ride_rate(p, a) * 1000.0 / m) / (2.0 * math.pi) if m > 0 else 0.0


def damping_ratio(p: Values, a: str, direction: str) -> float:
    """Damping as a fraction of critical damping of the sprung mass on the spring."""
    m = sprung_corner_mass(p, a)
    if m <= 0:
        return 0.0
    critical = 2.0 * math.sqrt(p[f"{a}_spring_rate"] * 1000.0 * m)
    return p[f"{a}_damping_{direction}"] / critical


def spring_wire_diameter(p: Values, a: str) -> float:
    """Wire diameter that gives the spring rate: k = G d⁴ / (8 D³ n), solved for d, mm."""
    k, d_coil = p[f"{a}_spring_rate"], p["spring_coil_diameter"]
    return (8.0 * k * d_coil**3 * SPRING_ACTIVE_COILS / SPRING_SHEAR_MODULUS) ** 0.25


def spring_outer_diameter(p: Values, a: str) -> float:
    return p["spring_coil_diameter"] + spring_wire_diameter(p, a)


def spring_installed_length(p: Values, a: str) -> float:
    """Spring length between its seats at ride height, mm."""
    return damper_installed_length(p, a) - 2.0 * SPRING_SEAT_OFFSET


def spring_solid_length(p: Values, a: str) -> float:
    """Length with every coil touching: active coils plus one closed end coil each side."""
    return (SPRING_ACTIVE_COILS + 2.0) * spring_wire_diameter(p, a)


def lower_shock_mount_height(p: Values) -> float:
    """Lower damper eye height: on top of the beam axle at the wheel-centre height."""
    return tyre_radius(p) + AXLE_RADIUS


def damper_installed_length(p: Values, a: str) -> float:
    """Eye-to-eye damper length at ride height, set by the two mounts, mm."""
    return p[f"{a}_shock_mount_height"] - lower_shock_mount_height(p)


def damper_min_length(p: Values, a: str) -> float:
    return p[f"{a}_damper_stroke"] + DAMPER_DEAD_LENGTH


def damper_max_length(p: Values, a: str) -> float:
    return 2.0 * p[f"{a}_damper_stroke"] + DAMPER_DEAD_LENGTH


def travel_limits(p: Values, a: str) -> dict[str, tuple[float, str]]:
    """Each candidate wheel-travel limit at ride height, mm, with the parameter governing it.

    Bump: the bump stop, the tyre reaching the wheel arch, or the damper bottoming out.
    Rebound: the droop limit or the damper topping out.
    """
    length = damper_installed_length(p, a)
    return {
        "bump_stop": (p[f"{a}_bump_travel"], f"{a}_bump_travel"),
        "arch": (p["arch_clearance"], "arch_clearance"),
        "damper_compression": (length - damper_min_length(p, a), f"{a}_shock_mount_height"),
        "droop": (p[f"{a}_rebound_travel"], f"{a}_rebound_travel"),
        "damper_extension": (damper_max_length(p, a) - length, f"{a}_damper_stroke"),
    }


BUMP_LIMITS = ("bump_stop", "arch", "damper_compression")
REBOUND_LIMITS = ("droop", "damper_extension")


def available_bump_travel(p: Values, a: str) -> float:
    limits = travel_limits(p, a)
    return min(limits[k][0] for k in BUMP_LIMITS)


def available_rebound_travel(p: Values, a: str) -> float:
    limits = travel_limits(p, a)
    return min(limits[k][0] for k in REBOUND_LIMITS)


_MASS = ("vehicle_mass", "front_mass_distribution")
FRONTAL_FILL = 0.85  # frontal area / (width x height above the ground), typical for cars


def frontal_area(p: Values) -> float:
    """Approximate frontal area, m²: body width x height above the ground x fill factor."""
    return FRONTAL_FILL * p["body_width"] * (p["overall_height"] - p["ground_clearance"]) / 1e6


def power_to_weight(p: Values) -> float:
    """Peak power per tonne of vehicle mass, kW/t."""
    return p["peak_power"] / (p["vehicle_mass"] / 1000.0)


_SUSPENSION_DERIVED: dict[str, tuple[DerivedDef, Callable[[Values], float]]] = {}
for _a in AXLES:
    _A = _a.capitalize()
    _TYRE = ("rim_diameter", "tyre_width", "tyre_aspect_ratio")
    _mount = (f"{_a}_shock_mount_height", *_TYRE)
    _entries = {
        f"{_a}_sprung_corner_mass": (
            f"{_A} sprung corner mass", "kg", (*_MASS, f"{_a}_unsprung_mass"),
            (f"{_a} sprung mass", f"{_a} sprung corner mass", f"{_a} corner mass"),
            lambda p, a=_a: sprung_corner_mass(p, a),
        ),
        f"{_a}_ride_frequency": (
            f"{_A} ride frequency", "Hz",
            (f"{_a}_spring_rate", "tyre_vertical_stiffness", *_MASS, f"{_a}_unsprung_mass"),
            (f"{_a} ride frequency", f"{_a} natural frequency", f"{_a} bounce frequency"),
            lambda p, a=_a: ride_frequency(p, a),
        ),
        f"{_a}_damping_ratio_bump": (
            f"{_A} bump damping ratio", "",
            (f"{_a}_damping_bump", f"{_a}_spring_rate", *_MASS, f"{_a}_unsprung_mass"),
            (f"{_a} bump damping ratio", f"{_a} compression damping ratio"),
            lambda p, a=_a: damping_ratio(p, a, "bump"),
        ),
        f"{_a}_damping_ratio_rebound": (
            f"{_A} rebound damping ratio", "",
            (f"{_a}_damping_rebound", f"{_a}_spring_rate", *_MASS, f"{_a}_unsprung_mass"),
            (f"{_a} rebound damping ratio",),
            lambda p, a=_a: damping_ratio(p, a, "rebound"),
        ),
        f"{_a}_spring_wire_diameter": (
            f"{_A} spring wire diameter", "mm", (f"{_a}_spring_rate", "spring_coil_diameter"),
            (f"{_a} spring wire diameter", f"{_a} wire diameter"),
            lambda p, a=_a: spring_wire_diameter(p, a),
        ),
        f"{_a}_damper_length": (
            f"{_A} damper installed length", "mm", _mount,
            (f"{_a} damper length", f"{_a} shock length", f"{_a} damper installed length"),
            lambda p, a=_a: damper_installed_length(p, a),
        ),
        f"{_a}_available_bump_travel": (
            f"{_A} available bump travel", "mm",
            (f"{_a}_bump_travel", "arch_clearance", f"{_a}_damper_stroke", *_mount),
            (f"{_a} available bump travel", f"{_a} usable bump travel"),
            lambda p, a=_a: available_bump_travel(p, a),
        ),
        f"{_a}_available_rebound_travel": (
            f"{_A} available rebound travel", "mm",
            (f"{_a}_rebound_travel", f"{_a}_damper_stroke", *_mount),
            (f"{_a} available rebound travel", f"{_a} usable rebound travel"),
            lambda p, a=_a: available_rebound_travel(p, a),
        ),
    }  # fmt: skip
    for _id, (_label, _unit, _controls, _aliases, _fn) in _entries.items():
        _SUSPENSION_DERIVED[_id] = (
            DerivedDef(id=_id, label=_label, unit=_unit, controlled_by=_controls,
                       aliases=_aliases),
            _fn,
        )  # fmt: skip


_DERIVED: dict[str, tuple[DerivedDef, Callable[[Values], float]]] = {
    "overall_length": (
        DerivedDef(
            id="overall_length",
            label="Overall length",
            unit="mm",
            controlled_by=("front_overhang", "wheelbase", "rear_overhang"),
            aliases=("overall length", "length", "car length", "vehicle length", "body length"),
        ),
        overall_length,
    ),
    "tyre_diameter": (
        DerivedDef(
            id="tyre_diameter",
            label="Tyre outer diameter",
            unit="mm",
            controlled_by=("rim_diameter", "tyre_width", "tyre_aspect_ratio"),
            aliases=("tyre diameter", "tire diameter", "wheel outer diameter", "rolling diameter"),
        ),
        tyre_diameter,
    ),
    "tyre_sidewall": (
        DerivedDef(
            id="tyre_sidewall",
            label="Tyre sidewall height",
            unit="mm",
            controlled_by=("tyre_width", "tyre_aspect_ratio"),
            aliases=("sidewall height", "tyre sidewall height", "tire sidewall height"),
        ),
        tyre_sidewall,
    ),
    "overall_width_at_tyres": (
        DerivedDef(
            id="overall_width_at_tyres",
            label="Width over tyres",
            unit="mm",
            controlled_by=("track_front", "track_rear", "tyre_width"),
            aliases=("width over tyres", "width over tires"),
        ),
        overall_width_at_tyres,
    ),
    "arch_top_height": (
        DerivedDef(
            id="arch_top_height",
            label="Wheel arch top height",
            unit="mm",
            controlled_by=("rim_diameter", "tyre_width", "tyre_aspect_ratio", "arch_clearance"),
            aliases=("arch height", "wheel arch height"),
        ),
        arch_top_height,
    ),
    **_SUSPENSION_DERIVED,
    "frontal_area": (
        DerivedDef(
            id="frontal_area", label="Frontal area", unit="m²",
            controlled_by=("body_width", "overall_height", "ground_clearance"),
            aliases=("frontal area", "frontal area of the car"),
        ),
        frontal_area,
    ),
    "power_to_weight": (
        DerivedDef(
            id="power_to_weight", label="Power-to-weight", unit="kW/t",
            controlled_by=("peak_power", "vehicle_mass"),
            aliases=("power to weight", "power-to-weight", "power to weight ratio"),
        ),
        power_to_weight,
    ),
}  # fmt: skip

DERIVED: dict[str, DerivedDef] = {k: v[0] for k, v in _DERIVED.items()}  # extensible


def compute(derived_id: str, p: Values) -> float:
    return _DERIVED[derived_id][1](p)


def compute_all(p: Values) -> dict[str, float]:
    return {k: fn(p) for k, (_, fn) in _DERIVED.items()}
