"""The evaluation set is well-formed, and the parser passes its whole 'rules' tier."""

from autevra.ai import evaluate
from autevra.domain.derived import DERIVED
from autevra.domain.parameters import REGISTRY


def test_dataset_is_well_formed() -> None:
    cases = evaluate.load()
    assert len(cases) >= 40
    assert {c.tier for c in cases} == {"rules", "llm"}
    for case in cases:
        expect = case.expect
        assert len(expect) == 1, case.text
        if "set" in expect:
            assert set(expect["set"]) <= set(REGISTRY), case.text
            for pid, value in expect["set"].items():
                assert REGISTRY[pid].min <= value <= REGISTRY[pid].max, case.text
        elif "query" in expect:
            assert set(expect["query"]) <= set(REGISTRY) | set(DERIVED), case.text
        else:
            assert expect["action"] in {"clarify", "out_of_scope", "undo", "redo"}, case.text


def test_parser_passes_the_rules_tier() -> None:
    cases = [c for c in evaluate.load() if c.tier == "rules"]
    failures = [o for o in evaluate.run(cases) if not o.passed]
    assert failures == [], "\n".join(f"{o.text} -> {o.got}" for o in failures)


def test_parser_never_misapplies_an_llm_tier_phrase() -> None:
    # Without a model, paraphrases must end in a question or a decline, never a wrong change.
    cases = [c for c in evaluate.load() if c.tier == "llm"]
    for outcome in evaluate.run(cases):
        if not outcome.passed:
            assert outcome.got.split()[0] in {"clarify", "out_of_scope"}, outcome
