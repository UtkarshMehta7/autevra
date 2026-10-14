"""Parameter registry: every editable design parameter, its unit and bounds.

The registry is the single list of parameter IDs; the command system, the intent parser,
the API and the LLM schema are derived from it. The core holds the mechanism; engineering
domains and plugins register their parameters through ``autevra.extensions``.
"""

from pydantic import BaseModel, ConfigDict, Field

from autevra.core.units import Unit


class ParameterDef(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    group: str  # defined by the domain (e.g. dimensions, suspension)
    unit: Unit
    default: float
    min: float
    max: float
    step: float = 1.0
    description: str = ""
    aliases: tuple[str, ...] = Field(default=())
    increase_words: tuple[str, ...] = Field(default=())
    decrease_words: tuple[str, ...] = Field(default=())
    # A choice instead of a quantity: the value is the index of one of these labels
    # (min 0, max len - 1, step 1). Empty for ordinary numeric parameters.
    options: tuple[str, ...] = Field(default=())

    def option(self, value: float) -> str:
        """Label of the option a value selects (for choice parameters)."""
        return self.options[min(max(int(round(value)), 0), len(self.options) - 1)]


# Registries (filled by domain modules and plugins).
REGISTRY: dict[str, ParameterDef] = {}
# Group aliases: one word that addresses several parameters at once.
GROUP_ALIASES: dict[str, tuple[str, ...]] = {}


def get(parameter_id: str) -> ParameterDef:
    try:
        return REGISTRY[parameter_id]
    except KeyError:
        raise KeyError(f"unknown parameter '{parameter_id}'") from None


def default_values() -> dict[str, float]:
    return {d.id: d.default for d in REGISTRY.values()}
