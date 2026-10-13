from autevra.ai.interpreter import _LLMOutput
from autevra.ai.llm import prompt, schema
from autevra.core.derived import DERIVED
from autevra.core.parameters import REGISTRY, default_values


def test_schema_enumerates_registry_ids_only() -> None:
    s = schema.proposal_schema()
    change = s["properties"]["changes"]["items"]["properties"]
    assert change["parameter"]["enum"] == list(REGISTRY)
    assert set(s["properties"]["query"]["items"]["enum"]) == set(REGISTRY) | set(DERIVED)
    assert s["required"] == ["action", "changes", "query", "question"]


def test_prompt_lists_every_parameter_with_current_value() -> None:
    values = default_values() | {"wheelbase": 2800}
    messages = prompt.messages("stretch it between the axles", values)
    system = messages[0]["content"]
    for pid in REGISTRY:
        assert f"\n{pid} |" in system
    assert "wheelbase | mm | 2800 | 2000-3600 | Distance between front and rear axle" in system
    assert "overall_length | Overall length | 4700.0 mm" in system
    assert messages[-1] == {"role": "user", "content": "stretch it between the axles"}


def test_few_shot_examples_match_the_schema() -> None:
    for example, answer in prompt._EXAMPLES:
        out = _LLMOutput.model_validate(answer)
        assert all(c.parameter in REGISTRY for c in out.changes), example
        assert all(q in REGISTRY or q in DERIVED for q in out.query), example
