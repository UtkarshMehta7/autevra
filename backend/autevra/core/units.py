"""Units and conversions.

Every quantity belongs to a dimension. Values convert through the dimension's
base unit: mm for length, deg for angle, % for ratio, kg for mass, N/mm for
stiffness, N·s/m for damping, kW for power and kWh for energy; coefficients are
dimensionless.
Converting between dimensions is an error, so millimetres can never be silently
mixed with newtons or kilograms.
"""

from enum import StrEnum


class Dimension(StrEnum):
    LENGTH = "length"
    ANGLE = "angle"
    RATIO = "ratio"
    MASS = "mass"
    STIFFNESS = "stiffness"  # force per length
    DAMPING = "damping"  # force per velocity
    POWER = "power"
    ENERGY = "energy"
    NONE = "none"  # dimensionless coefficients (drag, rolling resistance)


class Unit(StrEnum):
    MM = "mm"
    CM = "cm"
    M = "m"
    IN = "in"
    DEG = "deg"
    PERCENT = "%"
    KG = "kg"
    LB = "lb"
    N_PER_MM = "N/mm"
    N_PER_M = "N/m"
    KN_PER_M = "kN/m"
    LBF_PER_IN = "lbf/in"
    NS_PER_M = "N·s/m"
    NS_PER_MM = "N·s/mm"
    KNS_PER_M = "kN·s/m"
    KW = "kW"
    HP = "hp"
    PS = "PS"
    KWH = "kWh"
    WH = "Wh"
    NONE = ""


# unit -> (dimension, factor to the dimension's base unit)
_UNITS: dict[Unit, tuple[Dimension, float]] = {
    Unit.MM: (Dimension.LENGTH, 1.0),
    Unit.CM: (Dimension.LENGTH, 10.0),
    Unit.M: (Dimension.LENGTH, 1000.0),
    Unit.IN: (Dimension.LENGTH, 25.4),
    Unit.DEG: (Dimension.ANGLE, 1.0),
    Unit.PERCENT: (Dimension.RATIO, 1.0),
    Unit.KG: (Dimension.MASS, 1.0),
    Unit.LB: (Dimension.MASS, 0.45359237),
    Unit.N_PER_MM: (Dimension.STIFFNESS, 1.0),
    Unit.N_PER_M: (Dimension.STIFFNESS, 1e-3),
    Unit.KN_PER_M: (Dimension.STIFFNESS, 1.0),
    Unit.LBF_PER_IN: (Dimension.STIFFNESS, 4.4482216152605 / 25.4),
    Unit.NS_PER_M: (Dimension.DAMPING, 1.0),
    Unit.NS_PER_MM: (Dimension.DAMPING, 1000.0),
    Unit.KNS_PER_M: (Dimension.DAMPING, 1000.0),
    Unit.KW: (Dimension.POWER, 1.0),
    Unit.HP: (Dimension.POWER, 0.745699872),  # mechanical horsepower
    Unit.PS: (Dimension.POWER, 0.73549875),  # metric horsepower
    Unit.KWH: (Dimension.ENERGY, 1.0),
    Unit.WH: (Dimension.ENERGY, 1e-3),
    Unit.NONE: (Dimension.NONE, 1.0),
}

# Spellings accepted from people and the parser, mapped to canonical units.
UNIT_ALIASES: dict[str, Unit] = {
    "kwh": Unit.KWH,
    "kw h": Unit.KWH,
    "kw·h": Unit.KWH,
    "kilowatt hour": Unit.KWH,
    "kilowatt hours": Unit.KWH,
    "kilowatt-hours": Unit.KWH,
    "wh": Unit.WH,
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
    "kg": Unit.KG,
    "kgs": Unit.KG,
    "kilogram": Unit.KG,
    "kilograms": Unit.KG,
    "lb": Unit.LB,
    "lbs": Unit.LB,
    "pound": Unit.LB,
    "pounds": Unit.LB,
    "n/mm": Unit.N_PER_MM,
    "n/m": Unit.N_PER_M,
    "kn/m": Unit.KN_PER_M,
    "lbf/in": Unit.LBF_PER_IN,
    "lb/in": Unit.LBF_PER_IN,
    "n·s/m": Unit.NS_PER_M,
    "ns/m": Unit.NS_PER_M,
    "n.s/m": Unit.NS_PER_M,
    "n s/m": Unit.NS_PER_M,
    "n·s/mm": Unit.NS_PER_MM,
    "ns/mm": Unit.NS_PER_MM,
    "n.s/mm": Unit.NS_PER_MM,
    "kn·s/m": Unit.KNS_PER_M,
    "kns/m": Unit.KNS_PER_M,
    "kn.s/m": Unit.KNS_PER_M,
    "kw": Unit.KW,
    "kilowatt": Unit.KW,
    "kilowatts": Unit.KW,
    "hp": Unit.HP,
    "bhp": Unit.HP,
    "horsepower": Unit.HP,
    "ps": Unit.PS,
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
