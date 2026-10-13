"""Instruction interpreter: deterministic parser first, local LLM only as a fallback.

Escalation policy (docs/ARCHITECTURE.md D3/D4):
1. The rule parser handles everything it can. Its answers, including its
   clarifying questions about derived values or missing amounts, are final.
2. Text naming an automotive concept that is not modelled yet ("make the
   suspension softer") gets a specific, deterministic question.
3. Text that is clearly not about vehicle design is declined.
4. Only text the parser cannot attach to any parameter goes to the LLM. The
   LLM's JSON is re-validated here; a command becomes a *proposal* that the
   user must confirm. The LLM never applies anything, never runs code and
   never touches geometry.
"""

import re
from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel, ValidationError

from autevra.ai import concepts, rule_parser
from autevra.ai import lexicon as lx
from autevra.ai.llm import prompt, schema
from autevra.ai.llm.clients import LLMClient, LLMResponseError, LLMUnavailableError
from autevra.ai.rule_parser import Interpretation, Kind, Reason
from autevra.domain.commands import (
    Change,
    CommandError,
    Operation,
    SetParameters,
    Source,
    resolve,
)
from autevra.domain.derived import DERIVED
from autevra.domain.parameters import REGISTRY
from autevra.domain.units import parse_unit

OUT_OF_SCOPE_MESSAGE = (
    "Autevra handles automotive design, engineering and testing. I can change the vehicle's "
    "dimensions, wheels, cabin, chassis, suspension and mass, run suspension tests, or answer "
    "questions about them."
)


class _LLMChange(BaseModel):
    parameter: str
    operation: Literal["set", "increase", "decrease", "scale"]
    value: float
    unit: str | None = None


class _LLMOutput(BaseModel):
    action: Literal["set_parameters", "query", "undo", "redo", "clarify", "out_of_scope"]
    changes: list[_LLMChange] = []
    query: list[str] = []
    question: str = ""


_NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "twenty": 20,
    "fifty": 50,
    "hundred": 100,
}


def _numbers(text: str) -> set[float]:
    found = {float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)}
    found |= {float(v) for w, v in _NUMBER_WORDS.items() if re.search(rf"\b{w}\b", text)}
    return found


_RELATIVE_WORDS = frozenset({
    "forward", "forwards", "back", "backward", "backwards", "rearward", "up", "down", "out",
    "outward", "outwards", "inward", "apart", "closer", "further", "farther", "more", "less",
    "extra", "bigger", "smaller",
})  # fmt: skip


class _GroundingError(ValueError):
    pass


def ground(change: Change, text: str) -> Change:
    """Check a model-proposed change against the user's own words.

    The value must be a number the user wrote (the model may not invent amounts), and the
    operation must agree with the phrasing: "to 40" is an absolute value, "by 40" a relative
    one. Small models confuse the two, which silently produces plausible but wrong values.
    """
    t = text.lower()
    numbers = _numbers(t)
    if change.operation is Operation.SCALE:
        # "10 %" allows 1.1 or 0.9, never a factor of 10.
        percents = {float(n) for n in re.findall(r"(\d+(?:\.\d+)?)\s*(?:%|percent\b)", t)}
        factors = numbers - percents
        factors |= {round(1 + n / 100, 6) for n in percents}
        factors |= {round(1 - n / 100, 6) for n in percents}
        if re.search(r"\b(double|twice)\b", t):
            factors.add(2.0)
        if re.search(r"\b(halve|half)\b", t):
            factors.add(0.5)
        if round(change.value, 6) not in factors:
            raise _GroundingError(
                f"it used a scale factor of {change.value:g}, "
                "which does not follow from what you wrote"
            )
        return change
    if change.value not in numbers:
        raise _GroundingError(f"it used the value {change.value:g}, which you did not give")
    # The unit the user wrote next to that number wins over the model's unit.
    for match in rule_parser.QUANTITY.finditer(rule_parser.normalise(text)):
        if float(match.group(1)) == change.value and match.group(2):
            change = change.model_copy(update={"unit": parse_unit(match.group(2))})
            break
    value = re.escape(f"{change.value:g}")
    says_to = re.search(rf"\b(to|=|at)\s*{value}\b", t) is not None
    says_by = re.search(rf"\bby\s*{value}\b", t) is not None
    op = change.operation
    words = set(re.findall(r"[a-z]+", t))
    relative = bool(words & (lx.INCREASE_VERBS | lx.DECREASE_VERBS | _RELATIVE_WORDS))
    if op in (Operation.INCREASE, Operation.DECREASE) and (says_to or not (says_by or relative)):
        op = Operation.SET  # "to 40", or a bare amount such as "18 inch alloys"
    elif says_by and op is Operation.SET:
        if words & lx.INCREASE_VERBS and not words & lx.DECREASE_VERBS:
            op = Operation.INCREASE
        elif words & lx.DECREASE_VERBS and not words & lx.INCREASE_VERBS:
            op = Operation.DECREASE
        else:
            raise _GroundingError("it is unclear whether the amount is added or subtracted")
    return change.model_copy(update={"operation": op})


def _with_note(result: Interpretation, note: str) -> Interpretation:
    result.question = f"{result.question} {note}".strip()
    return result


def from_llm_output(
    raw: dict, text: str, values: Mapping[str, float], model: str
) -> Interpretation:
    """Validate raw model JSON and turn it into an interpretation (never applied here)."""
    by = "llm"
    try:
        out = _LLMOutput.model_validate(raw)
    except ValidationError:
        return Interpretation(
            Kind.CLARIFICATION,
            reason=Reason.INVALID,
            interpreted_by=by,
            question="I could not interpret that reliably. Could you "
            "rephrase it with the parameter and the amount?",
        )
    match out.action:
        case "out_of_scope":
            return Interpretation(
                Kind.OUT_OF_SCOPE, question=OUT_OF_SCOPE_MESSAGE, interpreted_by=by
            )
        case "clarify":
            question = out.question.strip() or "Could you say which dimension should change?"
            return Interpretation(
                Kind.CLARIFICATION, question=question, reason=Reason.NO_TARGET, interpreted_by=by
            )
        case "undo" | "redo":
            return Interpretation(
                Kind.CLARIFICATION,
                reason=Reason.INVALID,
                interpreted_by=by,
                question=f"Did you mean to {out.action} the last change?",
                suggestions=[out.action],
            )
        case "query":
            ids = tuple(dict.fromkeys(i for i in out.query if i in REGISTRY or i in DERIVED))
            if not ids:
                return Interpretation(
                    Kind.CLARIFICATION,
                    reason=Reason.INVALID,
                    interpreted_by=by,
                    question="Which value do you mean?",
                )
            return Interpretation(Kind.QUERY, query=ids, interpreted_by=by)

    if not out.changes:
        return Interpretation(
            Kind.CLARIFICATION,
            reason=Reason.INVALID,
            interpreted_by=by,
            question="Which parameter should change, and by how much?",
        )
    try:
        changes = tuple(
            Change.model_validate(c.model_dump()) for c in out.changes if c.parameter in REGISTRY
        )
        if len(changes) != len(out.changes):
            raise CommandError("the model referred to a parameter that does not exist")
        changes = tuple(ground(c, text) for c in changes)
        command = SetParameters(changes=changes, source=Source.LLM, instruction=text)
        resolve(command, values)  # unit compatibility, positive scale factors, ...
    except (CommandError, ValidationError, _GroundingError) as exc:
        message = exc.errors()[0]["msg"] if isinstance(exc, ValidationError) else str(exc)
        return Interpretation(
            Kind.CLARIFICATION,
            reason=Reason.INVALID,
            interpreted_by=by,
            question=f"The suggested change is not valid ({message}). Could you rephrase it?",
        )
    return Interpretation(
        Kind.PROPOSAL,
        command=command,
        interpreted_by=by,
        assumptions=[f"interpreted by the local model {model}; confirm before it is applied"],
    )


def interpret(
    text: str, values: Mapping[str, float], llm: LLMClient | None = None
) -> Interpretation:
    result = rule_parser.parse(text)
    if result.kind is not Kind.CLARIFICATION or result.reason is not Reason.NO_TARGET:
        return result

    concept = concepts.find(text)
    if concept is not None:
        question, suggestions = concepts.clarification(concept, text)
        reason = Reason.AMBIGUOUS if concept.modelled else Reason.UNMODELLED
        return Interpretation(
            Kind.CLARIFICATION, question=question, suggestions=suggestions, reason=reason
        )
    if not concepts.is_automotive(text):
        return Interpretation(Kind.OUT_OF_SCOPE, question=OUT_OF_SCOPE_MESSAGE)
    if llm is None or llm.provider == "off":
        return result
    try:
        raw = llm.complete_json(prompt.messages(text, values), schema.proposal_schema())
    except LLMUnavailableError:
        return _with_note(
            result,
            "(The local language model is not running, so only the built-in parser was used.)",
        )
    except LLMResponseError:
        return _with_note(result, "(The local language model gave no usable answer.)")
    return from_llm_output(raw, text, values, llm.model)
