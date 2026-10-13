"""Automotive lexicon: aliases for parameters, groups and derived values, plus verbs."""

from dataclasses import dataclass
from enum import StrEnum

from autevra.domain.derived import DERIVED
from autevra.domain.parameters import GROUP_ALIASES, REGISTRY


class TargetKind(StrEnum):
    PARAMETER = "parameter"
    DERIVED = "derived"


@dataclass(frozen=True)
class Target:
    kind: TargetKind
    ids: tuple[str, ...]
    alias: str


def _build_aliases() -> dict[str, Target]:
    table: dict[str, Target] = {}

    def add(alias: str, target: Target) -> None:
        if alias in table and table[alias] != target:
            raise ValueError(f"alias '{alias}' is ambiguous")
        table[alias] = target

    for spec in REGISTRY.values():
        for alias in (*spec.aliases, spec.label.lower(), spec.id.replace("_", " ")):
            add(alias, Target(TargetKind.PARAMETER, (spec.id,), alias))
    for alias, ids in GROUP_ALIASES.items():
        add(alias, Target(TargetKind.PARAMETER, ids, alias))
    for spec in DERIVED.values():
        for alias in (*spec.aliases, spec.label.lower()):
            add(alias, Target(TargetKind.DERIVED, (spec.id,), alias))
    return table


ALIASES: dict[str, Target] = _build_aliases()
# Longest alias first, so "front track" wins over "track" and "ride height" over "height".
ALIASES_BY_LENGTH: list[str] = sorted(ALIASES, key=len, reverse=True)

INCREASE_VERBS = frozenset({
    "increase", "increased", "raise", "extend", "lengthen", "widen", "grow", "enlarge",
    "stretch", "lift", "boost", "add", "bigger", "larger", "longer", "wider", "taller",
    "higher", "more", "up", "upsize",
})  # fmt: skip
DECREASE_VERBS = frozenset({
    "decrease", "decreased", "reduce", "lower", "shorten", "narrow", "shrink", "cut",
    "drop", "trim", "smaller", "shorter", "narrower", "less", "down", "lessen",
    "downsize",
})  # fmt: skip
SET_VERBS = frozenset({"set", "change", "make", "use", "fit", "put", "give", "adjust"})

# Comparative words with no explicit parameter ("make it wider").
COMPARATIVES: dict[str, tuple[str, bool]] = {}  # word -> (target id, is_increase)
for _spec in REGISTRY.values():
    for _w in _spec.increase_words:
        COMPARATIVES[_w] = (_spec.id, True)
    for _w in _spec.decrease_words:
        COMPARATIVES[_w] = (_spec.id, False)
COMPARATIVES |= {
    "longer": ("overall_length", True),
    "lengthen": ("overall_length", True),
    "shorter": ("overall_length", False),
    "shorten": ("overall_length", False),
    "higher": ("ground_clearance", True),
}

# Plain adjectives used with an absolute value ("make it 1.9 m wide").
ADJECTIVES: dict[str, str] = {
    "wide": "body_width",
    "tall": "overall_height",
    "high": "overall_height",
    "long": "overall_length",
}

UNDO_PHRASES = frozenset(
    {
        "undo",
        "undo that",
        "undo it",
        "undo the last change",
        "go back",
        "revert",
        "revert that",
        "take that back",
        "undo last",
    }
)
REDO_PHRASES = frozenset({"redo", "redo that", "redo it", "redo the last change", "do it again"})
