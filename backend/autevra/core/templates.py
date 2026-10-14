"""Design templates: complete starting designs a project can be created from.

The core holds the registry; domain modules and plugins register templates through
``autevra.extensions`` (the automotive module adds one per vehicle class).
"""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    id: str
    label: str
    description: str
    values: Callable[[], dict[str, float]]  # a complete, rule-checked set of design values


TEMPLATES: dict[str, Template] = {}


def get(template_id: str) -> Template:
    try:
        return TEMPLATES[template_id]
    except KeyError:
        raise KeyError(f"unknown template '{template_id}'") from None
