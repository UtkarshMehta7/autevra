"""Typed design commands and their resolution into absolute parameter values.

Operation semantics:
- ``set``: value (in ``unit``, or the parameter's own unit) becomes the new value.
- ``increase`` / ``decrease``: add or subtract the value. A ``%`` unit on a
  parameter that is not itself a ratio means a relative change
  ("increase the wheelbase by 5 %" -> x 1.05). On a ratio parameter such as
  the tyre aspect ratio, ``%`` means percentage points (50 % + 5 % = 55 %).
- ``scale``: multiply by a unitless factor (1.05 = +5 %).
"""

from collections.abc import Mapping
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from autevra.domain.parameters import REGISTRY
from autevra.domain.units import Dimension, Unit, UnitError, convert, dimension_of


class Operation(StrEnum):
    SET = "set"
    INCREASE = "increase"
    DECREASE = "decrease"
    SCALE = "scale"


class Source(StrEnum):
    UI = "ui"
    API = "api"
    RULES = "rules"
    LLM = "llm"


class Change(BaseModel):
    model_config = ConfigDict(frozen=True)

    parameter: str
    operation: Operation
    value: float
    unit: Unit | None = None


class SetParameters(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: Literal["set_parameters"] = "set_parameters"
    changes: tuple[Change, ...] = Field(min_length=1)
    source: Source = Source.API
    instruction: str | None = None


class CommandError(ValueError):
    """A change that cannot be resolved (unknown parameter, unit mismatch, ...)."""


def _to_parameter_unit(change: Change, target: Unit) -> float:
    unit = change.unit or target
    try:
        return convert(change.value, unit, target)
    except UnitError as exc:
        raise CommandError(f"{change.parameter}: {exc}") from None


def resolve_change(change: Change, current: float) -> float:
    spec = REGISTRY.get(change.parameter)
    if spec is None:
        raise CommandError(f"unknown parameter '{change.parameter}'")
    relative_percent = (
        change.unit is Unit.PERCENT and dimension_of(spec.unit) is not Dimension.RATIO
    )
    match change.operation:
        case Operation.SET:
            if relative_percent:
                raise CommandError(f"{spec.label} cannot be set to a percentage")
            return _to_parameter_unit(change, spec.unit)
        case Operation.SCALE:
            if change.unit is not None:
                raise CommandError("scale takes a unitless factor (e.g. 1.05)")
            if change.value <= 0:
                raise CommandError("scale factor must be positive")
            return current * change.value
        case Operation.INCREASE | Operation.DECREASE:
            sign = 1.0 if change.operation is Operation.INCREASE else -1.0
            if relative_percent:
                return current * (1.0 + sign * change.value / 100.0)
            return current + sign * _to_parameter_unit(change, spec.unit)
    raise CommandError(f"unsupported operation '{change.operation}'")  # pragma: no cover


def resolve(command: SetParameters, values: Mapping[str, float]) -> dict[str, float]:
    """New absolute values for every parameter the command touches.

    Changes apply in order, so two changes to one parameter compound.
    """
    working = dict(values)
    touched: dict[str, float] = {}
    for change in command.changes:
        new = round(resolve_change(change, working.get(change.parameter, 0.0)), 6)
        working[change.parameter] = new
        touched[change.parameter] = new
    return touched
