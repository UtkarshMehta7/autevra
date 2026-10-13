"""Units and conversions.

Every quantity belongs to a dimension (length, angle, ratio). Values convert
through the dimension's base unit: mm for length, deg for angle, % for ratio.
"""

from enum import StrEnum


class Dimension(StrEnum):
    LENGTH = "length"
    ANGLE = "angle"
    RATIO = "ratio"


class Unit(StrEnum):
    MM = "mm"
    CM = "cm"
    M = "m"
    IN = "in"
    DEG = "deg"
    PERCENT = "%"


# unit -> (dimension, factor to the dimension's base unit)
_UNITS: dict[Unit, tuple[Dimension, float]] = {
    Unit.MM: (Dimension.LENGTH, 1.0),
    Unit.CM: (Dimension.LENGTH, 10.0),
    Unit.M: (Dimension.LENGTH, 1000.0),
    Unit.IN: (Dimension.LENGTH, 25.4),
    Unit.DEG: (Dimension.ANGLE, 1.0),
    Unit.PERCENT: (Dimension.RATIO, 1.0),
}

# Spellings accepted from people and the parser, mapped to canonical units.
UNIT_ALIASES: dict[str, Unit] = {
    "mm": Unit.MM,
    "millimetre": Unit.MM,
    "millimetres": Unit.MM,
    "millimeter": Unit.MM,
    "millimeters": Unit.MM,
    "cm": Unit.CM,
    "centimetre": Unit.CM,
    "centimetres": Unit.CM,
    "centimeter": Unit.CM,
    "centimeters": Unit.CM,
    "m": Unit.M,
    "metre": Unit.M,
    "metres": Unit.M,
    "meter": Unit.M,
    "meters": Unit.M,
    "in": Unit.IN,
    "inch": Unit.IN,
    "inches": Unit.IN,
    '"': Unit.IN,
    "deg": Unit.DEG,
    "degree": Unit.DEG,
    "degrees": Unit.DEG,
    "°": Unit.DEG,
    "%": Unit.PERCENT,
    "percent": Unit.PERCENT,
    "pct": Unit.PERCENT,
}


class UnitError(ValueError):
    """Raised for unknown units or conversions between dimensions."""


def parse_unit(text: str) -> Unit:
    try:
        return UNIT_ALIASES[text.strip().lower()]
    except KeyError:
        raise UnitError(f"unknown unit '{text}'") from None


def dimension_of(unit: Unit) -> Dimension:
    return _UNITS[unit][0]


def convert(value: float, from_unit: Unit, to_unit: Unit) -> float:
    from_dim, from_factor = _UNITS[from_unit]
    to_dim, to_factor = _UNITS[to_unit]
    if from_dim is not to_dim:
        raise UnitError(f"cannot convert {from_unit} ({from_dim}) to {to_unit} ({to_dim})")
    return value * from_factor / to_factor
