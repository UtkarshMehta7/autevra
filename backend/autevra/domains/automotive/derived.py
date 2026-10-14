"""Automotive derived values: vehicle geometry, suspension and mass relations.

Suspension values follow textbook relations (each function names its
assumptions). They are analytical estimates for the template, not
measurements of a real vehicle. ``DEFINITIONS`` is registered into the core
derived-value registry by the automotive domain module.
"""

import math
from collections.abc import Callable

from autevra.core.derived import DERIVED, DerivedDef, Values, compute, compute_all

__all__ = ["DEFINITIONS", "DERIVED", "compute", "compute_all"]

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


# Pack-level battery figures (typical of current lithium-ion packs; assumptions, not data
# for any product): energy per volume and per mass.
PACK_KWH_PER_L = 0.25
PACK_KWH_PER_KG = 0.16
UNIBODY_FLOOR = 50.0  # floor structure above the ground-clearance line, mm
PACK_CLEARANCE = 20.0  # gap above the ground-clearance line and below the floor, mm

# Parameters the floor height (and so every body-mounted part) depends on.
CHASSIS_INPUTS = (
    "chassis_type", "powertrain_type", "battery_capacity", "rail_height", "ground_clearance",
    "wheelbase", "body_width", "rail_spacing", "rail_width",
)  # fmt: skip


def chassis(p: Values) -> str:
    return ("ladder", "unibody", "skateboard")[min(max(int(round(p["chassis_type"])), 0), 2)]


def powertrain(p: Values) -> str:
    return ("combustion", "hybrid", "electric")[min(max(int(round(p["powertrain_type"])), 0), 2)]


def pack_footprint(p: Values) -> tuple[tuple[float, float], tuple[float, float]]:
    """(x, y) extents of the traction battery between the axles, mm: between the rails on a
    ladder frame, nearly body-wide on a unibody or skateboard."""
    x = (-p["wheelbase"] + 450.0, -400.0)
    if chassis(p) == "ladder":
        half = p["rail_spacing"] / 2.0 - p["rail_width"] / 2.0 - 20.0
    else:
        half = p["body_width"] / 2.0 - 180.0
    return x, (-half, half)


def floor_pack_height(p: Values) -> float:
    """Height of a flat floor pack of this energy over the pack footprint, mm."""
    (x0, x1), (y0, y1) = pack_footprint(p)
    volume = p["battery_capacity"] / PACK_KWH_PER_L * 1e6  # mm³
    return min(max(volume / ((x1 - x0) * (y1 - y0)), 90.0), 320.0)


HYBRID_PACK_LENGTH = 650.0  # compact pack under the rear seat, mm


def pack_height(p: Values) -> float:
    """Traction battery height, mm: a flat floor pack (battery electric) or a compact pack
    under the rear seat (hybrid); 0 for combustion."""
    kind = powertrain(p)
    if kind == "combustion":
        return 0.0
    if kind == "electric":
        return floor_pack_height(p)
    _, (y0, y1) = pack_footprint(p)
    volume = p["battery_capacity"] / PACK_KWH_PER_L * 1e6
    return min(max(volume / (HYBRID_PACK_LENGTH * 0.6 * (y1 - y0)), 90.0), 320.0)


def body_floor_height(p: Values) -> float:
    """Floor of the body: on top of the rails (ladder frame), on a low integrated floor
    structure (unibody) or on top of the battery (skateboard)."""
    kind = chassis(p)
    if kind == "ladder":
        return p["ground_clearance"] + p["rail_height"]
    if kind == "unibody":
        return p["ground_clearance"] + UNIBODY_FLOOR
    # The platform is sized for a floor pack even when a smaller pack is fitted.
    return p["ground_clearance"] + 2 * PACK_CLEARANCE + max(floor_pack_height(p), 110.0)


def battery_mass(p: Values) -> float:
    """Traction battery mass at the assumed pack energy density, kg (0 for combustion)."""
    return 0.0 if powertrain(p) == "combustion" else p["battery_capacity"] / PACK_KWH_PER_KG


def electric_range(p: Values) -> float:
    """Rough steady 100 km/h range on battery energy, km: aerodynamic drag plus rolling
    resistance at constant speed, 90 % usable energy, 85 % drive efficiency. An estimate
    with stated assumptions, not a test-cycle figure; 0 for combustion."""
    if powertrain(p) == "combustion":
        return 0.0
    v = 100 / 3.6
    drag = 0.5 * 1.204 * p["drag_coefficient"] * frontal_area(p) * v**3
    rolling = p["rolling_resistance"] * p["vehicle_mass"] * 9.80665 * v
    power_w = (drag + rolling) / 0.85
    hours = p["battery_capacity"] * 0.9 * 1000 / power_w
    return hours * 100.0


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


def front_headroom(p: Values) -> float:
    """Roof liner above a large adult's head in the front row, mm (allowance-based)."""
    from autevra.domains.automotive import interior  # (interior imports the builders)

    return interior.front_headroom(p | {"body_floor": body_floor_height(p)})


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


DEFINITIONS: dict[str, tuple[DerivedDef, Callable[[Values], float]]] = {
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
    "battery_mass": (
        DerivedDef(
            id="battery_mass", label="Traction battery mass", unit="kg",
            controlled_by=("battery_capacity", "powertrain_type"),
            aliases=("battery mass", "battery weight", "pack mass", "pack weight"),
        ),
        battery_mass,
    ),
    "electric_range": (
        DerivedDef(
            id="electric_range", label="Estimated range at 100 km/h", unit="km",
            controlled_by=("battery_capacity", "drag_coefficient", "vehicle_mass",
                           "rolling_resistance", "body_width", "overall_height"),
            aliases=("range", "electric range", "driving range", "ev range"),
        ),
        electric_range,
    ),
    "front_headroom": (
        DerivedDef(
            id="front_headroom", label="Front headroom", unit="mm",
            controlled_by=("overall_height", "ground_clearance", "rail_height", "body_style"),
            aliases=("headroom", "front headroom", "head room"),
        ),
        front_headroom,
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
