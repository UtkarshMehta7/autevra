"""Prompt built from the parameter registry and the current design values."""

import json
from collections.abc import Mapping

from autevra.ai import language
from autevra.core import derived
from autevra.core.parameters import REGISTRY

_ACTIONS = (
    "Output only JSON matching the schema. Never invent parameter ids; use only the ids listed.\n"
    """{notes}Actions:
- set_parameters: one change per parameter. operation is set, increase, decrease or scale.
  value is the number the user gave; unit is the unit the user gave, or null if none.
  "by 10%" on a length means unit "%". scale takes a unitless factor (unit null).
- query: the user asks for current values; list ids in "query".
- undo / redo: the user wants to revert or repeat the last change.
- clarify: the request is about the {subject} but ambiguous or not supported by the
  listed parameters; put one short question in "question".
- out_of_scope: the request is not about {scope}.
Leave unused fields empty ([] or "")."""
)


def _rules() -> str:
    intro = (
        language.first("prompt_intro") or "You convert design instructions into JSON for Autevra."
    )
    notes = language.first("prompt_notes") or ""
    actions = _ACTIONS.format(
        notes=notes + "\n" if notes else "",
        subject=language.first("prompt_subject") or "design",
        scope=language.first("prompt_scope") or "the engineering domain of this design",
    )
    return "\n".join((intro, actions))


def _examples() -> list[tuple[str, dict]]:
    return list(language.joined("prompt_examples"))


def _parameter_table(values: Mapping[str, float]) -> str:
    lines = ["id | unit | current | range | meaning | also called"]
    for spec in REGISTRY.values():
        aliases = ", ".join(spec.aliases)
        lines.append(
            f"{spec.id} | {spec.unit} | {values[spec.id]:g} | "
            f"{spec.min:g}-{spec.max:g} | {spec.description} | {aliases}"
        )
    return "\n".join(lines)


def _derived_table(values: Mapping[str, float]) -> str:
    lines = ["Read-only derived values (query only): id | label | current"]
    for spec in derived.DERIVED.values():
        value = derived.compute(spec.id, values)
        shown = f"{value:.1f}" if abs(value) >= 10 else f"{value:.3f}"
        lines.append(f"{spec.id} | {spec.label} | {shown} {spec.unit}".rstrip())
    return "\n".join(lines)


def messages(text: str, values: Mapping[str, float]) -> list[dict[str, str]]:
    system = "\n\n".join([_rules(), _parameter_table(values), _derived_table(values)])
    out = [{"role": "system", "content": system}]
    for example, answer in _examples():
        out.append({"role": "user", "content": example})
        out.append({"role": "assistant", "content": json.dumps(answer)})
    out.append({"role": "user", "content": text})
    return out
