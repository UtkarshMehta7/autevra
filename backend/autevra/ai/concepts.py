"""Concepts behind vague or out-of-model requests, and the scope check.

Domain languages contribute concepts (see ``autevra.ai.language``). A concept turns a
vague request into an honest, specific question instead of a guess: a modelled system
named without a quantity gets a "which quantity?" question; a system that is not modelled
yet is reported as such. The scope check keeps the assistant on the loaded domains.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass, field

from autevra.ai import language
from autevra.ai import lexicon as lx


@dataclass(frozen=True)
class Concept:
    id: str
    words: tuple[str, ...]
    meanings: tuple[str, ...]  # the engineering quantities the words can refer to
    phase: str  # roadmap phase where it becomes editable
    modelled: bool = False  # True: editable parameters exist, the request is just ambiguous
    # Optional domain-specific question: text -> (question, suggestions) or None.
    clarify: Callable[[str], tuple[str, list[str]] | None] | None = field(
        default=None, compare=False
    )


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", text.lower()))


def find(text: str) -> Concept | None:
    t = text.lower()
    for concept in language.joined("concepts"):
        for w in concept.words:
            if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", t):
                return concept
    return None


def clarification(concept: Concept, text: str) -> tuple[str, list[str]]:
    specific = concept.clarify(text) if concept.clarify else None
    if specific is not None:
        return specific
    meanings = ", ".join(concept.meanings)
    if concept.modelled:
        return (
            f"Which {concept.id.replace('_', ' ')} quantity should change: {meanings}? "
            "Say front, rear or both, and the amount.",
            [],
        )
    question = (
        f"That refers to {concept.id.replace('_', ' ')} ({meanings}), which is not an "
        f"editable parameter yet; it is planned for {concept.phase}."
    )
    return question, []


def in_scope(text: str) -> bool:
    """True if the text plausibly concerns a loaded domain (conservative: errs inward)."""
    words = _words(text)
    if words & language.scope_words():
        return True
    if find(text) is not None:
        return True
    if any(alias in text.lower() for alias in lx.ALIASES):
        return True
    verbs = lx.INCREASE_VERBS | lx.DECREASE_VERBS | lx.SET_VERBS | set(lx.COMPARATIVES)
    return bool(words & verbs) or bool(re.search(r"\d", text))
