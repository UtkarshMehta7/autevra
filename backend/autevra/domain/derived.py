"""Derived values: read-only quantities computed from parameters (all mm).

Requests to edit a derived value are answered with a clarification naming
the parameters in ``CONTROLLED_BY``.
"""

from collections.abc import Callable, Mapping

from pydantic import BaseModel, ConfigDict

INCH_MM = 25.4

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
}

DERIVED: Mapping[str, DerivedDef] = {k: v[0] for k, v in _DERIVED.items()}


def compute(derived_id: str, p: Values) -> float:
    return _DERIVED[derived_id][1](p)


def compute_all(p: Values) -> dict[str, float]:
    return {k: fn(p) for k, (_, fn) in _DERIVED.items()}
