"""Domain language for the deterministic parser, the concept check and the LLM prompt.

The parser engine (``rule_parser``) is domain-agnostic: it knows English verbs,
quantities, units, comparators and instruction shapes ("what if ...", "require ...",
"test ...", "optimise ..."). Everything a domain's engineers say that is specific to that
domain (vocabulary normalisation, comparative words, how to read a test request, which
phrases name a test metric, concepts that are not modelled, the prompt's framing) is
contributed by the domain module as a ``Language`` and merged here.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

Replacement = str | Callable[[Any], str]


@dataclass(frozen=True)
class Language:
    name: str
    # (regex, replacement) applied in order after lower-casing.
    normalisers: Sequence[tuple[str, Replacement]] = ()
    # Comparative word -> (parameter or derived id, is increase): "longer" -> overall_length.
    comparatives: Mapping[str, tuple[str, bool]] = field(default_factory=dict)
    # Adjective used with an absolute value: "make it 1.9 m wide" -> body_width.
    adjectives: Mapping[str, str] = field(default_factory=dict)
    # Question word -> quantity: "how long is it?" -> overall_length.
    query_words: Mapping[str, str] = field(default_factory=dict)
    # Example instructions for derived values: derived id -> suggestions.
    derived_examples: Mapping[str, Sequence[str]] = field(default_factory=dict)
    # Target refinement: (clause words, target ids) -> replacement ids or None.
    target_hint: Callable[[list[str], tuple[str, ...]], tuple[str, ...] | None] | None = None
    # Extra words (regex alternation) that make an instruction a test request.
    test_words: str = ""
    # Text -> TestRequest; reads which test, target and scenario are meant.
    test_request: Callable[[str], Any] | None = None
    default_test: str = ""
    # (text, limit value) -> requirement fields, a clarification Interpretation, or None.
    requirement_metric: Callable[[str, float], Any] | None = None
    # (pattern, metric, sense) objectives for optimisation requests.
    objectives: Sequence[tuple[str, str, str]] = ()
    optimise_words: str = ""  # extra regex alternation that signals optimisation
    loop_words: str = ""  # nouns for "fix the ...": e.g. suspension|corner
    diagnose_words: str = ""  # extra words for "why did it ...": e.g. lift|lifted
    unmodelled_limits: Mapping[str, str] = field(default_factory=dict)
    spec_trigger: str = ""  # regex: a specification statement ("I want an electric SUV")
    concepts: Sequence[Any] = ()  # ai.concepts.Concept
    scope_words: frozenset[str] = frozenset()
    out_of_scope: str = ""
    prompt_intro: str = ""
    prompt_notes: str = ""  # placed before the action list
    prompt_subject: str = ""  # what a clarify request is about, e.g. "vehicle"
    prompt_scope: str = ""  # what is in scope, for out_of_scope
    prompt_examples: Sequence[tuple[str, dict]] = ()


LANGUAGES: list[Language] = []


def register(language: Language) -> None:
    if all(lang.name != language.name for lang in LANGUAGES):
        LANGUAGES.append(language)


def unregister(name: str) -> None:
    LANGUAGES[:] = [lang for lang in LANGUAGES if lang.name != name]


def normalisers() -> list[tuple[str, Replacement]]:
    return [n for lang in LANGUAGES for n in lang.normalisers]


def merged(attr: str) -> dict:
    out: dict = {}
    for lang in LANGUAGES:
        out.update(getattr(lang, attr))
    return out


def joined(attr: str) -> list:
    return [x for lang in LANGUAGES for x in getattr(lang, attr)]


def alternation(attr: str) -> str:
    return "|".join(getattr(lang, attr) for lang in LANGUAGES if getattr(lang, attr))


def first(attr: str):  # type: ignore[no-untyped-def]
    return next((getattr(lang, attr) for lang in LANGUAGES if getattr(lang, attr)), None)


def scope_words() -> frozenset[str]:
    return frozenset().union(*(lang.scope_words for lang in LANGUAGES))
