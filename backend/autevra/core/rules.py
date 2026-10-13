"""Rules: cross-parameter consistency checks, and validation of complete designs.

The core holds the mechanism; engineering domains and plugins register their rules
through ``autevra.extensions``. Bounds on single parameters come from the registry.
"""

from collections.abc import Callable

from pydantic import BaseModel, ConfigDict

from autevra.core.derived import Values
from autevra.core.parameters import REGISTRY


class Violation(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule: str
    message: str
    parameters: tuple[str, ...]


class Rule(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    description: str
    parameters: tuple[str, ...]


_RuleFn = Callable[[Values], str | None]
# Registries (filled by domain modules and plugins).
_RULES: list[tuple[Rule, _RuleFn]] = []
RULES: list[Rule] = []


def check_bounds(p: Values) -> list[Violation]:
    out = []
    for pid, value in p.items():
        spec = REGISTRY[pid]
        if not spec.min <= value <= spec.max:
            out.append(
                Violation(
                    rule="bounds",
                    message=(
                        f"{spec.label} {value:g} {spec.unit} is outside "
                        f"{spec.min:g}–{spec.max:g} {spec.unit}"
                    ),
                    parameters=(pid,),
                )
            )
    return out


def check_rules(p: Values) -> list[Violation]:
    out = []
    for rule, fn in _RULES:
        message = fn(p)
        if message is not None:
            out.append(Violation(rule=rule.id, message=message, parameters=rule.parameters))
    return out


def validate(p: Values) -> list[Violation]:
    """All violations for a complete parameter set: bounds first, then rules."""
    missing = set(REGISTRY) - set(p)
    if missing:
        raise KeyError(f"missing parameters: {sorted(missing)}")
    return check_bounds(p) + check_rules(p)
