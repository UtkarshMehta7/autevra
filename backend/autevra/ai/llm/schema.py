"""JSON schema for model output, generated from the parameter registry.

Constrained decoding (Ollama ``format``, llama-server ``response_format``)
guarantees the model emits JSON of this shape with parameter IDs from the
registry only. Semantic validity is checked afterwards by the interpreter.
"""

from typing import Any

from autevra.core.commands import Operation
from autevra.core.derived import DERIVED
from autevra.core.parameters import REGISTRY
from autevra.core.units import Unit

ACTIONS = ("set_parameters", "query", "undo", "redo", "clarify", "out_of_scope")


def proposal_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": list(ACTIONS)},
            "changes": {
                "type": "array",
                "maxItems": 6,
                "items": {
                    "type": "object",
                    "properties": {
                        "parameter": {"type": "string", "enum": list(REGISTRY)},
                        "operation": {"type": "string", "enum": [o.value for o in Operation]},
                        "value": {"type": "number"},
                        "unit": {
                            "type": ["string", "null"],
                            "enum": [*(u.value for u in Unit), None],
                        },
                    },
                    "required": ["parameter", "operation", "value", "unit"],
                },
            },
            "query": {
                "type": "array",
                "maxItems": 6,
                "items": {"type": "string", "enum": [*REGISTRY, *DERIVED]},
            },
            "question": {"type": "string"},
        },
        "required": ["action", "changes", "query", "question"],
    }
