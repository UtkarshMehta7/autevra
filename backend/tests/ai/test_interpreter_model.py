"""AI-originated commands name the model that proposed them (architecture, section 19)."""

from autevra.ai.interpreter import Kind, from_llm_output
from autevra.core.commands import Source
from autevra.core.parameters import default_values
from autevra.domains import load_builtin

load_builtin()


def test_llm_commands_record_their_model_and_prompt() -> None:
    raw = {
        "action": "set_parameters",
        "changes": [
            {"parameter": "wheelbase", "operation": "increase", "value": 100, "unit": "mm"}
        ],
    }
    out = from_llm_output(raw, "make the wheelbase 100 mm longer", default_values(), "qwen3:1.7b")
    assert out.kind is Kind.PROPOSAL  # never applied without the user confirming
    assert out.command.source is Source.LLM and out.command.model == "qwen3:1.7b"
    assert out.command.instruction == "make the wheelbase 100 mm longer"
