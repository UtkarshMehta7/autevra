"""Deterministic intent parser: instruction text -> command, query or clarification.

Pipeline (see docs/ARCHITECTURE.md §5): normalise, detect undo/redo/query,
split compound requests, match the longest alias, detect the operation,
extract and convert the quantity, and either emit a typed ``SetParameters``
command or ask a clarifying question. Nothing here touches geometry.
"""

import difflib
import re
from dataclasses import dataclass, field
from enum import StrEnum

from autevra.ai import lexicon as lx
from autevra.ai.lexicon import Target, TargetKind
from autevra.domain.commands import Change, Operation, SetParameters, Source
from autevra.domain.derived import DERIVED
from autevra.domain.parameters import REGISTRY
from autevra.domain.units import Unit, parse_unit


class Kind(StrEnum):
    COMMAND = "command"
    UNDO = "undo"
    REDO = "redo"
    QUERY = "query"
    CLARIFICATION = "clarification"
    PROPOSAL = "proposal"  # LLM-derived command: must be confirmed before it is applied
    OUT_OF_SCOPE = "out_of_scope"


class Reason(StrEnum):
    """Why a clarification was asked; only ``NO_TARGET`` may be escalated to the LLM."""

    EMPTY = "empty"
    NO_TARGET = "no_target"
    DERIVED = "derived"
    MISSING_AMOUNT = "missing_amount"
    INVALID = "invalid"
    UNMODELLED = "unmodelled"
    AMBIGUOUS = "ambiguous"  # names a modelled system but not which quantity


@dataclass
class Interpretation:
    kind: Kind
    command: SetParameters | None = None
    query: tuple[str, ...] = ()  # parameter or derived IDs
    question: str | None = None
    suggestions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    reason: Reason | None = None
    interpreted_by: str = "rules"


_NUMBER = r"(-?\d+(?:\.\d+)?)"
_UNIT = (
    r"(mm|millimet(?:er|re)s?|cm|centimet(?:er|re)s?|m|met(?:er|re)s?|inch(?:es)?|in|\"|"
    r"deg(?:rees?)?|°|%|percent|pct)"
)
QUANTITY = re.compile(_NUMBER + r"\s*" + _UNIT + r"?(?![a-z0-9])")
_SPLIT = re.compile(r"\s*(?:,|;|\band then\b|\bthen\b|\band also\b|\balso\b|\band\b)\s*")
_QUESTION_START = re.compile(r"^(what|what's|whats|how|show|tell|give me|list|which)\b")


def normalise(text: str) -> str:
    t = text.strip().lower()
    t = t.replace("tire", "tyre").replace("”", '"').replace("“", '"').replace("’", "'")
    t = re.sub(r"(\d)\s*(?:''|inch)\b", r"\1 in", t)
    t = re.sub(r"(\d+)s\b", r"\1", t)  # "18s" -> "18" (rim sizes)
    t = re.sub(r"(\d) in (wheels?|alloys?)\b", r"\1 in rims", t)  # "18 inch wheels" = rim size
    t = re.sub(
        r"\bfront and rear (track|overhangs?)\b",
        lambda m: "track" if m.group(1) == "track" else "overhangs",
        t,
    )
    t = re.sub(r"\bthe (car|vehicle)\b", "it", t)
    t = re.sub(r"[!.]+$", "", t)
    return re.sub(r"\s+", " ", t).strip()


def _find_target(clause: str) -> Target | None:
    for alias in lx.ALIASES_BY_LENGTH:
        if re.search(rf"(?<![a-z]){re.escape(alias)}(?![a-z])", clause):
            return lx.ALIASES[alias]
    return None


def _words(clause: str) -> list[str]:
    return re.findall(r"[a-z']+", clause)


def _detect_operation(clause: str, words: list[str]) -> Operation | None:
    if re.search(r"\bto\s+-?\d", clause) or "=" in clause:
        return Operation.SET
    if "factor" in words or "scale" in words or "times" in words:
        return Operation.SCALE
    if any(w in lx.INCREASE_VERBS for w in words):
        return Operation.INCREASE
    if any(w in lx.DECREASE_VERBS for w in words):
        return Operation.DECREASE
    if any(w in lx.SET_VERBS for w in words):
        return Operation.SET
    return None


def _quantity(clause: str) -> tuple[float, Unit | None] | None:
    matches = list(QUANTITY.finditer(clause))
    if not matches:
        return None
    chosen = matches[-1]
    to_match = re.search(r"\bto\s+" + _NUMBER, clause)
    if to_match:
        chosen = next(m for m in matches if m.start() == to_match.start(1))
    unit = parse_unit(chosen.group(2)) if chosen.group(2) else None
    return float(chosen.group(1)), unit


def _suggest(clause: str) -> list[str]:
    words = _words(clause)
    candidates = set()
    for w in words:
        candidates.update(difflib.get_close_matches(w, lx.ALIASES.keys(), n=3, cutoff=0.75))
    return sorted(candidates)[:5]


@dataclass
class _Clause:
    changes: list[Change]
    assumptions: list[str]


class _UnresolvedError(Exception):
    def __init__(
        self, question: str, suggestions: list[str] | None = None, reason: Reason = Reason.INVALID
    ) -> None:
        self.question = question
        self.suggestions = suggestions or []
        self.reason = reason


def _derived_clarification(derived_id: str) -> _UnresolvedError:
    spec = DERIVED[derived_id]
    controls = ", ".join(REGISTRY[p].label.lower() for p in spec.controlled_by)
    examples = {
        "overall_length": [
            "increase the wheelbase by 100 mm",
            "increase the front overhang by 50 mm",
            "increase the rear overhang by 50 mm",
        ],
    }.get(derived_id, [f"increase the {REGISTRY[spec.controlled_by[0]].label.lower()} by 10 mm"])
    return _UnresolvedError(
        f"{spec.label} is derived from the {controls}. Which of these should change?",
        examples,
        Reason.DERIVED,
    )


# Words that carry no meaning of their own in an instruction.
_FILLER = frozenset({
    "the", "a", "an", "it", "its", "to", "by", "of", "at", "is", "be", "on", "for", "please",
    "me", "from", "with", "set", "make", "so", "that", "now", "value", "size",
    "mm", "cm", "m", "in", "inch", "inches", "deg", "degree", "degrees", "percent", "pct",
    "millimetre", "millimetres", "millimeter", "millimeters", "metre", "metres", "meter",
    "meters", "centimetre", "centimetres", "centimeter", "centimeters", "factor", "times",
})  # fmt: skip
_KNOWN = (
    _FILLER
    | lx.INCREASE_VERBS
    | lx.DECREASE_VERBS
    | lx.SET_VERBS
    | set(lx.COMPARATIVES)
    | set(lx.ADJECTIVES)
)


def _unexplained(clause: str, alias: str | None) -> list[str]:
    """Words the parser cannot account for. Used before any guess: if a clause has words
    we do not understand, guessing could change the wrong parameter."""
    text = clause if alias is None else re.sub(re.escape(alias), " ", clause)
    return [w for w in _words(text) if w not in _KNOWN]


def _parse_clause(clause: str, previous_op: Operation | None) -> _Clause:
    words = _words(clause)
    target = _find_target(clause)
    op = _detect_operation(clause, words)

    # Guards against confident misreadings ("slide the cabin forward" is not "set cabin
    # length"; "drop the window line" is not "lower the car"): when the parser would have to
    # guess the operation or the target, every other word must be understood.
    guessing_op = target is not None and op is None and previous_op is None
    if guessing_op and _unexplained(clause, target.alias):
        raise _UnresolvedError(
            f"I am not sure what '{clause}' should do to the {target.alias}.", [], Reason.NO_TARGET
        )
    if target is None and _unexplained(clause, None):
        raise _UnresolvedError(
            f"I could not find a design parameter in '{clause}'."
            + (f" Did you mean: {', '.join(_suggest(clause))}?" if _suggest(clause) else ""),
            _suggest(clause),
            Reason.NO_TARGET,
        )

    if target is None:
        comparative = next((lx.COMPARATIVES[w] for w in words if w in lx.COMPARATIVES), None)
        adjective = next((lx.ADJECTIVES[w] for w in words if w in lx.ADJECTIVES), None)
        if comparative is None and adjective is not None and op in (None, Operation.SET):
            comparative = (adjective, True)
            op = Operation.SET
        if comparative is None:
            suggestions = _suggest(clause)
            hint = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            raise _UnresolvedError(
                f"I could not find a design parameter in '{clause}'.{hint}",
                suggestions,
                Reason.NO_TARGET,
            )
        target_id, is_increase = comparative
        kind = TargetKind.DERIVED if target_id in DERIVED else TargetKind.PARAMETER
        target = Target(kind, (target_id,), target_id)
        if op is None or (
            op in (Operation.INCREASE, Operation.DECREASE)
            and target_id not in lx.ADJECTIVES.values()
        ):
            op = Operation.INCREASE if is_increase else Operation.DECREASE
    elif target.ids == ("roof_length",) and any(w in ("lower", "raise") for w in words):
        target = Target(TargetKind.PARAMETER, ("overall_height",), "roof")

    if target.kind is TargetKind.DERIVED:
        raise _derived_clarification(target.ids[0])

    if op is None:
        op = previous_op
    quantity = _quantity(clause)
    label = ", ".join(REGISTRY[i].label.lower() for i in target.ids)

    if quantity is None:
        if op is Operation.SCALE and "double" in words:
            quantity = (2.0, None)
        else:
            what = {Operation.INCREASE: "increase", Operation.DECREASE: "decrease"}.get(op, "set")
            unit = REGISTRY[target.ids[0]].unit
            raise _UnresolvedError(
                f"By how much should I {what} the {label}?"
                if op in (Operation.INCREASE, Operation.DECREASE)
                else f"What value should the {label} have?",
                [
                    f"{what} the {label} by 20 {unit}"
                    if what != "set"
                    else f"set the {label} to {REGISTRY[target.ids[0]].default:g} {unit}"
                ],
                Reason.MISSING_AMOUNT,
            )
    if op is None:
        op = Operation.SET
    value, unit = quantity
    assumptions = []
    if unit is None and op is not Operation.SCALE:
        assumed = REGISTRY[target.ids[0]].unit
        assumptions.append(f"assumed {value:g} {assumed} for the {label}")
    if op is not Operation.SCALE and value < 0:
        value = -value
        op = {Operation.INCREASE: Operation.DECREASE, Operation.DECREASE: Operation.INCREASE}.get(
            op, op
        )
    if op is Operation.SET and value < 0:
        raise _UnresolvedError(f"The {label} cannot be negative.")
    changes = [Change(parameter=pid, operation=op, value=value, unit=unit) for pid in target.ids]
    return _Clause(changes=changes, assumptions=assumptions)


def _parse_query(text: str) -> Interpretation:
    target = _find_target(text)
    if target is None:
        words = _words(text)
        comparative = {
            "long": "overall_length",
            "wide": "body_width",
            "tall": "overall_height",
            "high": "overall_height",
        }
        hit = next((comparative[w] for w in words if w in comparative), None)
        if hit is not None:
            return Interpretation(Kind.QUERY, query=(hit,))
        if set(words) & {"everything", "all", "parameters", "specs", "specification", "dimensions"}:
            return Interpretation(Kind.QUERY, query=tuple(REGISTRY))  # "show me everything"
        return Interpretation(
            Kind.CLARIFICATION,
            question=f"I could not find a design parameter in '{text}'.",
            reason=Reason.NO_TARGET,
        )
    return Interpretation(Kind.QUERY, query=target.ids)


def parse(text: str) -> Interpretation:
    t = normalise(text)
    if not t:
        return Interpretation(
            Kind.CLARIFICATION, question="What would you like to change?", reason=Reason.EMPTY
        )
    if t in lx.UNDO_PHRASES:
        return Interpretation(Kind.UNDO)
    if t in lx.REDO_PHRASES:
        return Interpretation(Kind.REDO)
    if t.endswith("?") or _QUESTION_START.match(t):
        return _parse_query(t.rstrip("?"))

    clauses = [c for c in _SPLIT.split(t) if c]
    changes: list[Change] = []
    assumptions: list[str] = []
    previous: Operation | None = None
    for clause in clauses:
        try:
            parsed = _parse_clause(clause, previous)
        except _UnresolvedError as exc:
            return Interpretation(
                Kind.CLARIFICATION,
                question=exc.question,
                suggestions=exc.suggestions,
                reason=exc.reason,
            )
        changes.extend(parsed.changes)
        assumptions.extend(parsed.assumptions)
        previous = parsed.changes[-1].operation
    command = SetParameters(changes=tuple(changes), source=Source.RULES, instruction=text)
    return Interpretation(Kind.COMMAND, command=command, assumptions=assumptions)
