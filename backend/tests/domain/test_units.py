import pytest

from autevra.domain.units import Unit, UnitError, convert, parse_unit


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
    ],
)
def test_convert(value: float, src: Unit, dst: Unit, expected: float) -> None:
    assert convert(value, src, dst) == pytest.approx(expected)


def test_cross_dimension_conversion_is_rejected() -> None:
    with pytest.raises(UnitError):
        convert(10, Unit.MM, Unit.DEG)


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
    ],
)
def test_parse_unit(text: str, unit: Unit) -> None:
    assert parse_unit(text) is unit


def test_parse_unknown_unit() -> None:
    with pytest.raises(UnitError):
        parse_unit("furlong")
