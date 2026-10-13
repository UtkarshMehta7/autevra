"""Derived values: read-only quantities computed from parameters.

The core holds the registry; engineering domains register their derived values
(see ``autevra.domains``). Requests to edit a derived value are answered with
a clarification naming the parameters in ``controlled_by``.
"""

from collections.abc import Callable, Mapping

from pydantic import BaseModel, ConfigDict

Values = Mapping[str, float]


class DerivedDef(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    unit: str
    controlled_by: tuple[str, ...]
    aliases: tuple[str, ...]


# Registries (filled by domain modules and plugins through ``autevra.extensions``).
_DERIVED: dict[str, tuple[DerivedDef, Callable[[Values], float]]] = {}
DERIVED: dict[str, DerivedDef] = {}


def compute(derived_id: str, p: Values) -> float:
    return _DERIVED[derived_id][1](p)


def compute_all(p: Values) -> dict[str, float]:
    return {k: fn(p) for k, (_, fn) in _DERIVED.items()}
