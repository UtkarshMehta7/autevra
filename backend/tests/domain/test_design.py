import pytest

from autevra.core.commands import Change, Operation, SetParameters
from autevra.core.design import CommandRejectedError, DesignState


def _cmd(parameter: str, op: Operation, value: float) -> SetParameters:
    return SetParameters(changes=(Change(parameter=parameter, operation=op, value=value),))


def test_apply_undo_redo_wheelbase() -> None:
    design = DesignState()
    result = design.apply(_cmd("wheelbase", Operation.INCREASE, 100))
    assert design.values["wheelbase"] == 2800
    assert result.changed == ("wheelbase",)
    assert result.entry is not None
    assert result.entry.changes[0].old == 2700

    design.undo()
    assert design.values["wheelbase"] == 2700
    design.redo()
    assert design.values["wheelbase"] == 2800


def test_rejected_command_leaves_state_untouched() -> None:
    design = DesignState()
    with pytest.raises(CommandRejectedError) as exc:
        design.apply(_cmd("body_width", Operation.SET, 1700))
    assert exc.value.violations[0].rule == "tyres_within_body"
    assert design.values["body_width"] == 1820
    assert design.history == []


def test_out_of_bounds_rejected() -> None:
    design = DesignState()
    with pytest.raises(CommandRejectedError) as exc:
        design.apply(_cmd("wheelbase", Operation.INCREASE, 2000))
    assert exc.value.violations[0].rule == "bounds"


def test_new_command_discards_redo_branch() -> None:
    design = DesignState()
    design.apply(_cmd("wheelbase", Operation.INCREASE, 100))
    design.apply(_cmd("wheelbase", Operation.INCREASE, 100))
    design.undo()
    design.apply(_cmd("body_width", Operation.SET, 1900))
    assert len(design.history) == 2
    assert not design.can_redo
    assert design.values["wheelbase"] == 2800


def test_undo_redo_at_ends_are_noops() -> None:
    design = DesignState()
    assert design.undo() is None
    assert design.redo() is None


def test_noop_command_records_nothing() -> None:
    design = DesignState()
    result = design.apply(_cmd("wheelbase", Operation.SET, 2700))
    assert result.entry is None
    assert design.history == []


def test_undo_is_exact_for_relative_changes() -> None:
    design = DesignState()
    for _ in range(7):
        design.apply(_cmd("body_width", Operation.SCALE, 1.013))
    for _ in range(7):
        design.undo()
    assert design.values["body_width"] == 1820


def test_replay_matches_values_and_state_round_trips() -> None:
    design = DesignState()
    design.apply(_cmd("wheelbase", Operation.INCREASE, 100))
    design.apply(_cmd("ground_clearance", Operation.DECREASE, 20))
    design.undo()
    assert design.replay() == design.values
    restored = DesignState.model_validate_json(design.model_dump_json())
    assert restored.values == design.values
    assert restored.cursor == 1
    restored.redo()
    assert restored.values["ground_clearance"] == 140
