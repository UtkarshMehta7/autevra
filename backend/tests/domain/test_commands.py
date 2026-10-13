import pytest

from autevra.core.commands import Change, CommandError, Operation, SetParameters, resolve
from autevra.core.parameters import default_values
from autevra.core.units import Unit


def _resolve(*changes: Change) -> dict[str, float]:
    return resolve(SetParameters(changes=changes), default_values())


def test_increase_in_mm() -> None:
    assert _resolve(
        Change(parameter="wheelbase", operation=Operation.INCREASE, value=100, unit=Unit.MM)
    ) == {"wheelbase": 2800}


def test_increase_with_unit_conversion() -> None:
    assert _resolve(
        Change(parameter="wheelbase", operation=Operation.INCREASE, value=10, unit=Unit.CM)
    ) == {"wheelbase": 2800}


def test_set_rim_from_mm_converts_to_inches() -> None:
    assert _resolve(
        Change(parameter="rim_diameter", operation=Operation.SET, value=457.2, unit=Unit.MM)
    ) == {"rim_diameter": 18}


def test_decrease_defaults_to_parameter_unit() -> None:
    assert _resolve(
        Change(parameter="ground_clearance", operation=Operation.DECREASE, value=20)
    ) == {"ground_clearance": 140}


def test_relative_percent_on_length() -> None:
    assert _resolve(
        Change(parameter="wheelbase", operation=Operation.INCREASE, value=10, unit=Unit.PERCENT)
    ) == {"wheelbase": 2970}


def test_percent_points_on_ratio_parameter() -> None:
    assert _resolve(
        Change(
            parameter="tyre_aspect_ratio", operation=Operation.INCREASE, value=5, unit=Unit.PERCENT
        )
    ) == {"tyre_aspect_ratio": 55}


def test_scale() -> None:
    assert _resolve(Change(parameter="body_width", operation=Operation.SCALE, value=1.05)) == {
        "body_width": 1911
    }


def test_compound_changes_on_same_parameter() -> None:
    assert _resolve(
        Change(parameter="wheelbase", operation=Operation.INCREASE, value=100),
        Change(parameter="wheelbase", operation=Operation.DECREASE, value=50),
    ) == {"wheelbase": 2750}


@pytest.mark.parametrize(
    "change",
    [
        Change(parameter="nonexistent", operation=Operation.SET, value=1),
        Change(parameter="wheelbase", operation=Operation.SET, value=10, unit=Unit.DEG),
        Change(parameter="wheelbase", operation=Operation.SET, value=10, unit=Unit.PERCENT),
        Change(parameter="wheelbase", operation=Operation.SCALE, value=1.1, unit=Unit.MM),
        Change(parameter="wheelbase", operation=Operation.SCALE, value=0),
    ],
)
def test_invalid_changes(change: Change) -> None:
    with pytest.raises(CommandError):
        _resolve(change)


def test_command_requires_changes() -> None:
    with pytest.raises(ValueError):
        SetParameters(changes=())
