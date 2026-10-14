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

from autevra.ai import language
from autevra.ai import lexicon as lx
from autevra.ai.lexicon import Target, TargetKind
from autevra.core.commands import Change, Operation, SetParameters, Source
from autevra.core.derived import DERIVED
from autevra.core.parameters import REGISTRY
from autevra.core.units import Unit, parse_unit


class Kind(StrEnum):
    COMMAND = "command"
    UNDO = "undo"
    REDO = "redo"
    QUERY = "query"
    CLARIFICATION = "clarification"
    PROPOSAL = "proposal"  # LLM-derived command: must be confirmed before it is applied
    OUT_OF_SCOPE = "out_of_scope"
    TEST = "test"  # run component tests (no design change)
    DIAGNOSE = "diagnose"  # explain the latest failed test
    OPTIMIZE = "optimize"  # bounded optimisation of a solver metric under the test criteria
    LOOP = "loop"  # engineering loop: diagnose and fix until the tests pass
    PREVIEW = "preview"  # impact of a command, without applying it
    REQUIREMENT = "requirement"  # create a requirement
    VERIFY = "verify"  # verify every requirement (runs missing tests)
    SPEC = "spec"  # specification statement ("I want an electric SUV with 150 kW")


class Reason(StrEnum):
    """Why a clarification was asked; only ``NO_TARGET`` may be escalated to the LLM."""

    EMPTY = "empty"
    NO_TARGET = "no_target"
    DERIVED = "derived"
    MISSING_AMOUNT = "missing_amount"
    INVALID = "invalid"
    UNMODELLED = "unmodelled"
    AMBIGUOUS = "ambiguous"  # names a modelled system but not which quantity


@dataclass(frozen=True)
class TestRequest:
    """Which tests to run. ``target`` None: both axles (or those a change affects)."""

    test_id: str = ""  # "" = the language's default test
    target: str | None = None
    scenario_id: str | None = None  # None: every scenario
    focus: str | None = None  # diagnosis: "travel" or "contact" failures first
    objective: str | None = None  # optimisation metric
    sense: str = "minimize"
    unmodelled: tuple[str, ...] = ()  # constraints named by the user that no model checks


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
    tests: TestRequest | None = None  # run after the command, or on its own for Kind.TEST
    requirement: dict | None = None  # fields of a requirement to create (Kind.REQUIREMENT)


_NUMBER = r"(-?\d+(?:\.\d+)?)"
_UNIT = (
    r"(mm|millimet(?:er|re)s?|cm|centimet(?:er|re)s?|"
    r"kn[·.]?s/m|kns/m|n[·.]?s/mm|ns/mm|n[·.]?s/m|ns/m|n s/m|kn/m|n/mm|n/m|lbf/in|lb/in|"
    r"kgs?|kilograms?|lbs?|pounds?|"
    r"m(?!/s)|met(?:er|re)s?|inch(?:es)?|in|\"|deg(?:rees?)?|°|%|percent|pct)"
)
QUANTITY = re.compile(_NUMBER + r"\s*" + _UNIT + r"?(?![a-z0-9])")
_SPLIT = re.compile(r"\s*(?:,|;|\band then\b|\bthen\b|\band also\b|\balso\b|\band\b)\s*")
_QUESTION_START = re.compile(r"^(what|what's|whats|how|show|tell|give me|list|which)\b")


_TEST_VERB = r"(?:re-?test|test|simulate|run|do|perform)"
_TEST_TAIL = re.compile(
    r"(?:\s*,\s*|\s+)(?:and\s+)?(?:then\s+)?(?:re-?test|test|simulate)\b(?P<rest>[^,;]*)$"
)


def _test_words() -> re.Pattern[str]:
    extra = language.alternation("test_words")
    return re.compile(
        r"\b(test|tests|simulate|simulation" + (f"|{extra}" if extra else "") + r")\b"
    )


def _optimize_words() -> re.Pattern[str]:
    extra = language.alternation("optimise_words")
    return re.compile(r"\b(optimi[sz]e|optimi[sz]ation|improve|maximi[sz]e|minimi[sz]e"
                      + (f"|{extra}" if extra else "") + r")\b")  # fmt: skip


def _loop_words() -> re.Pattern[str]:
    extra = language.alternation("loop_words")
    return re.compile(r"^(?:please )?(?:fix|repair|sort out)\b.*\b(tests?|failures?"
                      + (f"|{extra}" if extra else "")
                      + r")\b|^(?:please )?(?:make|get)\b.*\bpass(?:ing)?\b")  # fmt: skip


def _diagnose_words() -> re.Pattern[str]:
    extra = language.alternation("diagnose_words")
    return re.compile(r"^(?:please )?(?:diagnose|explain|why)\b.*\b(fail|failed|fails|failure|"
                      r"exceed|exceeded|exceeds|limit|test|diagnos" + (f"|{extra}" if extra else "")
                      + r")|^diagnose\b")  # fmt: skip


_PREVIEW = re.compile(
    r"^(?:what if|what happens if|what would happen if|preview|show the impact of|"
    r"impact of)\s+(?:i|we|you)?\s*(?P<rest>.+?)\??$"
)
_VERIFY = re.compile(r"^(?:please )?(?:verify|check|re-?check)\b.*\brequirements?\b")
_REQUIRE = re.compile(
    r"^(?:please )?(?:add (?:a )?requirement:?|requirement:|require|"
    r"we require|it must|the requirement is)\b\s*(?P<rest>.+)$"
)
# Specification style: "the peak pitch angle over the hump shall be below 1.5 deg".
_SHALL = re.compile(r"^(?P<rest>.+\bshall\b.+)$")
_AT_LEAST = (
    r"(?:at least|no less than|not less than|a minimum of|minimum|above|over|more than|"
    r"greater than|>=|>)"
)
_AT_MOST = (
    r"(?:at most|no more than|not more than|a maximum of|maximum|below|under|less than|within|<=|<)"
)


def _parse_requirement(text: str) -> Interpretation:
    numbers = list(QUANTITY.finditer(text))
    number = numbers[-1] if numbers else None  # the limit is the last amount
    before = text[: number.start()] if number else text
    least = [m.end() for m in re.finditer(_AT_LEAST, before)]
    most = [m.end() for m in re.finditer(_AT_MOST, before)]
    if least and (not most or max(least) > max(most)):
        comparator = ">="
    elif most:
        comparator = "<="
    else:
        return Interpretation(
            Kind.CLARIFICATION,
            reason=Reason.INVALID,
            question="Should that be at least or at most a value? For example: require the "
            "ground clearance to be at least 150 mm.",
            suggestions=["require the ground clearance to be at least 150 mm"],
        )
    quantity = _quantity(text)
    if quantity is None:
        return Interpretation(
            Kind.CLARIFICATION,
            reason=Reason.MISSING_AMOUNT,
            question="What limit should the requirement have?",
        )
    value, unit = quantity
    hook = language.first("requirement_metric")
    found = hook(text, value) if hook else None
    if isinstance(found, Interpretation):
        return found
    if found is not None:
        fields = dict(found) | {"comparator": comparator, "limit": value, "unit": ""}
        return Interpretation(Kind.REQUIREMENT, requirement=fields)
    request = _test_request(text)
    target = _find_target(text)
    if target is None:
        question = f"Which quantity is the requirement about in '{text}'?"
        return Interpretation(Kind.CLARIFICATION, reason=Reason.NO_TARGET, question=question)
    if len(target.ids) > 1:
        ids = target.ids
        if request.target:
            ids = tuple(i for i in ids if i.startswith(request.target)) or ids
        if len(ids) > 1:
            names = ", ".join(REGISTRY[i].label.lower() for i in ids)
            return Interpretation(
                Kind.CLARIFICATION,
                reason=Reason.INVALID,
                question=f"'{target.alias}' covers several parameters ({names}); name one.",
            )
        target = Target(target.kind, ids, target.alias)
    return Interpretation(
        Kind.REQUIREMENT,
        requirement={
            "kind": "design",
            "quantity": target.ids[0],
            "comparator": comparator,
            "limit": value,
            "unit": str(unit) if unit else "",
        },
    )


def _objective(text: str) -> tuple[str, str] | None:
    for pattern, metric, sense in language.joined("objectives"):
        if re.search(pattern, text):
            return metric, sense
    return None


def _test_request(text: str) -> TestRequest:
    reader = language.first("test_request")
    if reader is not None:
        return reader(text)
    return TestRequest(language.first("default_test") or "")


def default_test_request() -> TestRequest:
    return TestRequest(language.first("default_test") or "")


def _split_test_tail(t: str) -> tuple[str, TestRequest | None]:
    """'increase the rear damping by 10% and test its response' -> (command text, request)."""
    match = _TEST_TAIL.search(t)
    if match is None or match.start() == 0:
        return t, None
    request = _test_request(match.group("rest"))
    return t[: match.start()].strip(), request


def normalise(text: str) -> str:
    t = text.strip().lower()
    t = t.replace("”", '"').replace("“", '"').replace("’", "'")
    t = re.sub(r"(\d)\s*(?:''|inch)\b", r"\1 in", t)
    t = re.sub(r"/\s*(s|sec)\s*(?:\^\s*2|2)\b", "/s²", t)  # m/s2, deg/s^2 -> /s²
    for pattern, replacement in language.normalisers():  # domain vocabulary
        t = re.sub(pattern, replacement, t)
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
    examples = list(language.merged("derived_examples").get(
        derived_id, [f"increase the {REGISTRY[spec.controlled_by[0]].label.lower()} by 10 mm"]
    ))  # fmt: skip
    return _UnresolvedError(
        f"{spec.label} is derived from the {controls}. Which of these should change?",
        examples,
        Reason.DERIVED,
    )


# Words that carry no meaning of their own in an instruction.
_FILLER = frozenset(
    {
        "the",
        "a",
        "an",
        "it",
        "its",
        "to",
        "by",
        "of",
        "at",
        "is",
        "be",
        "on",
        "for",
        "please",
        "me",
        "from",
        "with",
        "set",
        "make",
        "so",
        "that",
        "now",
        "value",
        "size",
        "mm",
        "cm",
        "m",
        "in",
        "inch",
        "inches",
        "deg",
        "degree",
        "degrees",
        "percent",
        "pct",
        "millimetre",
        "millimetres",
        "millimeter",
        "millimeters",
        "metre",
        "metres",
        "meter",
        "meters",
        "centimetre",
        "centimetres",
        "centimeter",
        "centimeters",
        "factor",
        "times",
        "n",
        "kn",
        "kg",
        "kgs",
        "lb",
        "lbs",
        "lbf",
        "kilogram",
        "kilograms",
        "pound",
        "pounds",
    }
)


def _known() -> set[str]:
    return (
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
    known = _known()
    return [w for w in _words(text) if w not in known]


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
    else:
        hint = language.first("target_hint")
        ids = hint(words, target.ids) if hint else None
        if ids:
            target = Target(TargetKind.PARAMETER, ids, target.alias)

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
        comparative = language.merged("query_words")
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


_CHOICE_VERB = (
    r"(?:make it|make this|make the (?:car|vehicle|body|design)|turn it into|turn this into|"
    r"convert it (?:in)?to|convert to|change it (?:in)?to|switch (?:it )?to|"
    r"paint it|paint the (?:car|vehicle|body)|respray it(?: in)?|colou?r it|"
    r"(?:change|set|switch) (?:the )?(?:{alias}) to|(?:{alias}))"
)


def _option_words(spec_id: str) -> list[tuple[str, int]]:
    """(phrase, option index) for a choice parameter, longest phrase first."""
    spec = REGISTRY[spec_id]
    extra: dict[str, list[str]] = {}
    for lang in language.LANGUAGES:
        for label, words in lang.option_aliases.get(spec_id, {}).items():
            extra.setdefault(label, []).extend(words)
    out = []
    for i, label in enumerate(spec.options):
        for phrase in (label, *extra.get(label, ())):
            out.append((phrase.lower(), i))
    return sorted(out, key=lambda x: -len(x[0]))


def _parse_choice(t: str) -> Interpretation | None:
    """ "make it a pickup", "change the body style to SUV": set a choice parameter."""
    for spec in REGISTRY.values():
        if not spec.options:
            continue
        aliases = "|".join(re.escape(a) for a in (*spec.aliases, spec.label.lower()))
        options = "|".join(re.escape(w) for w, _ in _option_words(spec.id))
        verb = _CHOICE_VERB.format(alias=aliases)
        m = re.match(
            rf"^(?:please )?{verb}(?: (?:an?|the))? (?P<option>{options})"
            rf"(?: (?:body|style|shape|form|version))?[.!]?$",
            t,
        )
        if m is None:
            continue
        index = dict(_option_words(spec.id))[m.group("option")]
        change = Change(parameter=spec.id, operation=Operation.SET, value=float(index))
        command = SetParameters(changes=(change,), source=Source.RULES, instruction=t)
        return Interpretation(
            Kind.COMMAND, command=command, assumptions=[f"{spec.label}: {spec.options[index]}"]
        )
    return None


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
    if _VERIFY.search(t):
        return Interpretation(Kind.VERIFY)
    spec_trigger = language.first("spec_trigger")
    if (spec_trigger and re.match(spec_trigger, t)) or t.startswith(("spec:", "specification:")):
        return Interpretation(Kind.SPEC)
    if (req := _REQUIRE.match(t) or _SHALL.match(t)) is not None:
        return _parse_requirement(req.group("rest"))
    if (what_if := _PREVIEW.match(t)) is not None:
        inner = parse(what_if.group("rest"))
        if inner.kind is Kind.COMMAND and inner.command is not None:
            return Interpretation(
                Kind.PREVIEW, command=inner.command, assumptions=inner.assumptions
            )
        return inner
    if (choice := _parse_choice(t)) is not None:
        return choice
    if _diagnose_words().search(t):
        return Interpretation(Kind.DIAGNOSE, tests=_test_request(t))
    if _optimize_words().search(t) and (objective := _objective(t)) is not None:
        request = _test_request(t)
        words = set(_words(t))
        limits = language.merged("unmodelled_limits")
        unmodelled = tuple(v for k, v in limits.items() if k in words)
        return Interpretation(
            Kind.OPTIMIZE,
            tests=TestRequest(
                request.test_id, request.target, request.scenario_id, None, *objective, unmodelled
            ),
        )
    if _loop_words().search(t) and not _find_target(t):
        return Interpretation(Kind.LOOP, tests=_test_request(t))
    if t.endswith("?") or _QUESTION_START.match(t):
        return _parse_query(t.rstrip("?"))
    if re.match(rf"^(?:please )?{_TEST_VERB}\b", t) and _test_words().search(t):
        return Interpretation(Kind.TEST, tests=_test_request(t))
    t, tests = _split_test_tail(t)

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
    return Interpretation(Kind.COMMAND, command=command, assumptions=assumptions, tests=tests)


# Public helpers for domain languages.
find_target = _find_target
words_of = _words
