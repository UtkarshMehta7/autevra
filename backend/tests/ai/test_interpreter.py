import pytest

from autevra.ai.interpreter import interpret
from autevra.ai.llm.clients import LLMResponseError, LLMUnavailableError
from autevra.ai.rule_parser import Kind, Reason
from autevra.domain.commands import Operation, Source
from autevra.domain.parameters import default_values
from autevra.domain.units import Unit
from tests.ai.fakes import FakeLLM, proposal

V = default_values()


def test_parser_handles_known_phrasing_without_calling_the_llm() -> None:
    llm = FakeLLM()
    result = interpret("increase the wheelbase by 100 mm", V, llm)
    assert result.kind is Kind.COMMAND and result.interpreted_by == "rules"
    assert llm.calls == []


@pytest.mark.parametrize("text", ["make it longer", "lower the car", "increase the wheelbase"])
def test_parser_clarifications_are_final(text: str) -> None:
    llm = FakeLLM()
    result = interpret(text, V, llm)
    assert result.kind is Kind.CLARIFICATION
    assert result.reason in (Reason.DERIVED, Reason.MISSING_AMOUNT)
    assert llm.calls == []


def test_softer_suspension_asks_which_quantity() -> None:
    llm = FakeLLM()
    result = interpret("make the suspension softer", V, llm)
    assert result.kind is Kind.CLARIFICATION and result.reason is Reason.AMBIGUOUS
    assert result.question is not None
    for word in ("spring rate", "compression", "rebound damping"):
        assert word in result.question
    assert result.suggestions == [
        "reduce the spring rate by 10%",
        "reduce the bump damping by 10%",
        "reduce the rebound damping by 10%",
    ]
    for suggestion in result.suggestions:  # every suggestion is itself a valid command
        assert interpret(suggestion, V, llm).kind is Kind.COMMAND
    assert llm.calls == []


@pytest.mark.parametrize(
    "text",
    ["change the gear ratio", "fit bigger brakes", "paint it red"],
)
def test_unmodelled_concepts_are_reported_not_guessed(text: str) -> None:
    result = interpret(text, V, FakeLLM())
    assert result.kind is Kind.CLARIFICATION and result.reason is Reason.UNMODELLED
    assert "not" in (result.question or "")


@pytest.mark.parametrize(
    "text", ["write me a poem about the sea", "what's the capital of France", "tell me a joke"]
)
def test_off_topic_is_declined_without_the_llm(text: str) -> None:
    llm = FakeLLM()
    assert interpret(text, V, llm).kind is Kind.OUT_OF_SCOPE
    assert llm.calls == []


def test_unresolved_text_becomes_a_proposal_not_a_command() -> None:
    llm = FakeLLM(proposal(("wheelbase", "increase", 4, "in")))
    result = interpret("stretch the gap between the hubs by four inches", V, llm)
    assert result.kind is Kind.PROPOSAL and result.interpreted_by == "llm"
    assert result.command is not None
    assert result.command.source is Source.LLM
    change = result.command.changes[0]
    assert (change.parameter, change.operation, change.value, change.unit) == (
        "wheelbase",
        Operation.INCREASE,
        4,
        Unit.IN,
    )
    assert len(llm.calls) == 1
    assert "confirm" in result.assumptions[0]


@pytest.mark.parametrize(
    ("answer", "fragment"),
    [
        (proposal(("wheelbase", "set", 10, "deg")), "not valid"),
        (proposal(("colour", "set", 1, None)), "does not exist"),
        (proposal(("wheelbase", "scale", -1, None)), "not valid"),
        ({"action": "set_parameters", "changes": [], "query": [], "question": ""}, "Which"),
        ({"action": "explode", "changes": []}, "could not interpret"),
        ({"action": "query", "changes": [], "query": ["nonsense"], "question": ""}, "Which"),
    ],
)
def test_invalid_llm_output_is_never_proposed(answer: dict, fragment: str) -> None:
    result = interpret("do the thing to the hubs", V, FakeLLM(answer))
    assert result.kind is Kind.CLARIFICATION
    assert fragment in (result.question or "")


def test_llm_query_and_clarify_and_out_of_scope() -> None:
    q = interpret(
        "how far apart are the hubs",
        V,
        FakeLLM({"action": "query", "changes": [], "query": ["wheelbase"], "question": ""}),
    )
    assert q.kind is Kind.QUERY and q.query == ("wheelbase",)
    c = interpret(
        "make the hubs nicer",
        V,
        FakeLLM({"action": "clarify", "changes": [], "query": [], "question": "Nicer how?"}),
    )
    assert c.kind is Kind.CLARIFICATION and c.question == "Nicer how?"
    o = interpret(
        "hubs of the internet",
        V,
        FakeLLM({"action": "out_of_scope", "changes": [], "query": [], "question": ""}),
    )
    assert o.kind is Kind.OUT_OF_SCOPE


def test_llm_undo_is_turned_into_a_suggestion() -> None:
    result = interpret(
        "take the hubs back to how they were",
        V,
        FakeLLM({"action": "undo", "changes": [], "query": [], "question": ""}),
    )
    assert result.kind is Kind.CLARIFICATION and result.suggestions == ["undo"]


@pytest.mark.parametrize("error", [LLMUnavailableError("down"), LLMResponseError("garbage")])
def test_llm_failure_falls_back_to_the_parser_answer(error: Exception) -> None:
    result = interpret("stretch the hubs apart", V, FakeLLM(error))
    assert result.kind is Kind.CLARIFICATION and result.reason is Reason.NO_TARGET
    assert "language model" in (result.question or "")


def test_without_llm_behaviour_is_unchanged() -> None:
    result = interpret("stretch the hubs apart", V, None)
    assert result.kind is Kind.CLARIFICATION and result.reason is Reason.NO_TARGET


@pytest.mark.parametrize(
    ("text", "answer", "expected"),
    [
        # "to N" is absolute even if the model says increase.
        (
            "let the front wheels turn up to 40 degrees",
            proposal(("max_steer_angle", "increase", 40, "deg")),
            ("set", 40),
        ),
        # "by N" with an increase verb is relative even if the model says set.
        (
            "stretch the hubs apart by 100 mm",
            proposal(("wheelbase", "set", 100, "mm")),
            ("increase", 100),
        ),
        ("trim the nose by 50 mm", proposal(("front_overhang", "set", 50, "mm")), ("decrease", 50)),
        # Number words count as numbers the user gave.
        (
            "stretch the gap between the hubs by four inches",
            proposal(("wheelbase", "increase", 4, "in")),
            ("increase", 4),
        ),
    ],
)
def test_grounding_fixes_the_operation(text: str, answer: dict, expected: tuple) -> None:
    result = interpret(text, V, FakeLLM(answer))
    assert result.kind is Kind.PROPOSAL and result.command is not None
    change = result.command.changes[0]
    assert (change.operation.value, change.value) == expected


@pytest.mark.parametrize(
    ("text", "answer"),
    [
        ("put fatter rubber on it, 255 mm wide", proposal(("tyre_width", "increase", 5, "mm"))),
        ("slide the cabin forward a bit", proposal(("cabin_offset", "increase", 100, "mm"))),
        ("move the hubs by 30 mm", proposal(("wheelbase", "set", 30, "mm"))),  # no direction
    ],
)
def test_ungrounded_proposals_become_questions(text: str, answer: dict) -> None:
    result = interpret(text, V, FakeLLM(answer))
    assert result.kind is Kind.CLARIFICATION
    assert "not valid" in (result.question or "")


@pytest.mark.parametrize(
    ("text", "answer", "expected"),
    [
        (
            "I want 18 inch alloys on it",
            proposal(("rim_diameter", "increase", 18, "in")),
            ("set", 18),
        ),
        (
            "leave a 50 mm gap between tyre and arch",
            proposal(("arch_clearance", "increase", 50, "mm")),
            ("set", 50),
        ),
        # Direction words keep it relative.
        (
            "slide the hubs 100 mm forward",
            proposal(("wheelbase", "increase", 100, "mm")),
            ("increase", 100),
        ),
    ],
)
def test_bare_amounts_are_absolute(text: str, answer: dict, expected: tuple) -> None:
    result = interpret(text, V, FakeLLM(answer))
    assert result.command is not None
    change = result.command.changes[0]
    assert (change.operation.value, change.value) == expected


@pytest.mark.parametrize(
    ("text", "factor", "ok"),
    [
        ("grow the hubs spacing by 10%", 1.1, True),
        ("shrink the hubs spacing by 10 percent", 0.9, True),
        ("double the hubs gap", 2.0, True),
        ("slide the cabin 100 mm forward", 0.1, False),  # invented factor
        ("grow the hubs spacing by 10 percent", 10, False),  # "10 percent" is not "x 10"
        ("scale the hubs spacing by 1.5", 1.5, True),
    ],
)
def test_scale_factors_must_follow_from_the_text(text: str, factor: float, ok: bool) -> None:
    result = interpret(text, V, FakeLLM(proposal(("wheelbase", "scale", factor, None))))
    assert (result.kind is Kind.PROPOSAL) is ok


def test_the_users_unit_overrides_the_models() -> None:
    result = interpret(
        "slam it 2 cm closer to the ground",
        V,
        FakeLLM(proposal(("ground_clearance", "decrease", 2, "mm"))),
    )
    assert result.command is not None
    assert result.command.changes[0].unit is Unit.CM


def test_engine_power_is_now_a_parameter() -> None:
    result = interpret("increase the engine power by 20 kW", V, FakeLLM())
    assert result.kind is Kind.COMMAND and result.command is not None
    assert result.command.changes[0].parameter == "peak_power"
