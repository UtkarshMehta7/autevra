import pytest

from autevra.core.units import Unit, UnitError, convert, parse_unit


@pytest.mark.parametrize(
    ("value", "src", "dst", "expected"),
    [
        (100, Unit.MM, Unit.MM, 100),
        (10, Unit.CM, Unit.MM, 100),
        (2.7, Unit.M, Unit.MM, 2700),
        (1, Unit.IN, Unit.MM, 25.4),
        (431.8, Unit.MM, Unit.IN, 17),
        (35, Unit.DEG, Unit.DEG, 35),
        (50, Unit.PERCENT, Unit.PERCENT, 50),
        (2.2046226218, Unit.LB, Unit.KG, 1),
        (26_000, Unit.N_PER_M, Unit.N_PER_MM, 26),
        (26, Unit.KN_PER_M, Unit.N_PER_MM, 26),
        (100, Unit.LBF_PER_IN, Unit.N_PER_MM, 17.5126835),
        (1.5, Unit.KNS_PER_M, Unit.NS_PER_M, 1500),
        (1.5, Unit.NS_PER_MM, Unit.NS_PER_M, 1500),
    ],
)
def test_convert(value: float, src: Unit, dst: Unit, expected: float) -> None:
    assert convert(value, src, dst) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("src", "dst"),
    [(Unit.MM, Unit.DEG), (Unit.N_PER_MM, Unit.NS_PER_M), (Unit.KG, Unit.N_PER_MM),
     (Unit.MM, Unit.N_PER_MM)],
)  # fmt: skip
def test_cross_dimension_conversion_is_rejected(src: Unit, dst: Unit) -> None:
    with pytest.raises(UnitError):
        convert(10, src, dst)


@pytest.mark.parametrize(
    ("text", "unit"),
    [
        ("mm", Unit.MM),
        ("Millimetres", Unit.MM),
        ("cm", Unit.CM),
        ("metres", Unit.M),
        ("inch", Unit.IN),
        ('"', Unit.IN),
        ("degrees", Unit.DEG),
        ("°", Unit.DEG),
        ("%", Unit.PERCENT),
        ("percent", Unit.PERCENT),
        ("kg", Unit.KG),
        ("lbs", Unit.LB),
        ("N/mm", Unit.N_PER_MM),
        ("kN/m", Unit.KN_PER_M),
        ("Ns/m", Unit.NS_PER_M),
        ("N·s/m", Unit.NS_PER_M),
        ("kN·s/m", Unit.KNS_PER_M),
    ],
)
def test_parse_unit(text: str, unit: Unit) -> None:
    assert parse_unit(text) is unit


def test_parse_unknown_unit() -> None:
    with pytest.raises(UnitError):
        parse_unit("furlong")
