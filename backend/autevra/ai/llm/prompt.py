"""Prompt built from the parameter registry and the current design values."""

import json
from collections.abc import Mapping

from autevra.core import derived
from autevra.core.parameters import REGISTRY

_RULES = """You convert automotive design instructions into JSON for the Autevra CAD system.
Output only JSON matching the schema. Never invent parameter ids; use only the ids listed.
Coordinate system: ISO 8855, millimetres. Vehicle length is derived (front_overhang +
wheelbase + rear_overhang), so ask which one to change instead of guessing.
Actions:
- set_parameters: one change per parameter. operation is set, increase, decrease or scale.
  value is the number the user gave; unit is the unit the user gave, or null if none.
  "by 10%" on a length means unit "%". scale takes a unitless factor (unit null).
- query: the user asks for current values; list ids in "query".
- undo / redo: the user wants to revert or repeat the last change.
- clarify: the request is about the vehicle but ambiguous or not supported by the
  listed parameters; put one short question in "question".
- out_of_scope: the request is not about automotive design, engineering or testing.
Leave unused fields empty ([] or "")."""

_EXAMPLES: list[tuple[str, dict]] = [
    ("stretch the distance between the axles by 4 inches",
     {"action": "set_parameters", "changes": [
         {"parameter": "wheelbase", "operation": "increase", "value": 4, "unit": "in"}],
      "query": [], "question": ""}),
    ("give it a bit more room under the floor, say 15 mm",
     {"action": "set_parameters", "changes": [
         {"parameter": "ground_clearance", "operation": "increase", "value": 15, "unit": "mm"}],
      "query": [], "question": ""}),
    ("how big are the wheels at the moment",
     {"action": "query", "changes": [], "query": ["rim_diameter", "tyre_diameter"],
      "question": ""}),
    ("make the car look more aggressive",
     {"action": "clarify", "changes": [], "query": [],
      "question": "Which dimension should change: for example lower ride height, wider "
                  "track or larger rims?"}),
    ("write me a poem about the sea",
     {"action": "out_of_scope", "changes": [], "query": [], "question": ""}),
]  # fmt: skip


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
    system = "\n\n".join([_RULES, _parameter_table(values), _derived_table(values)])
    out = [{"role": "system", "content": system}]
    for example, answer in _EXAMPLES:
        out.append({"role": "user", "content": example})
        out.append({"role": "assistant", "content": json.dumps(answer)})
    out.append({"role": "user", "content": text})
    return out
