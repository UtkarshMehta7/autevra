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

    test_id: str = "quarter_car"
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
_TEST_WORDS = re.compile(
    r"\b(test|tests|simulate|simulation|quarter[- ]car|pothole|hump|speed bump|ride modes?|"
    r"acceleration|braking|stopping|0-100|"
    r"natural frequenc(?:y|ies)|modal)\b"
)


_COMFORT = r"\bcomfort|comfortable|comfier|plusher|smoother|ride quality|better ride"
_GRIP = r"\bgrip|road holding|roadholding|tyre contact|keep the tyres? on"
_OBJECTIVES = (  # phrase -> (metric, sense)
    (_COMFORT, "rms_body_acceleration", "minimize"),
    (r"\bsettl", "settling_time", "minimize"),
    (_GRIP, "min_tyre_load_ratio", "maximize"),
    (r"\bharsh|peak acceleration|jolt", "peak_body_acceleration", "minimize"),
)
_OPTIMIZE = re.compile(
    r"\b(optimi[sz]e|optimi[sz]ation|improve|maximi[sz]e|minimi[sz]e|"
    r"more comfortable|comfier|plusher|smoother)\b"
)
_LOOP = re.compile(
    r"^(?:please )?(?:fix|repair|sort out)\b.*\b(suspension|tests?|corner|"
    r"failures?)\b|^(?:please )?(?:make|get)\b.*\bpass(?:ing)?\b"
)
_UNMODELLED_LIMITS = {
    "roll": "body roll",
    "pitch": "pitch",
    "dive": "brake dive",
    "squat": "squat",
    "noise": "noise",
}
_DIAGNOSE = re.compile(
    r"^(?:please )?(?:diagnose|explain|why)\b.*\b(fail|failed|fails|failure|exceed|exceeded|"
    r"exceeds|limit|test|lift|lifted|diagnos)|^diagnose\b"
)


_PREVIEW = re.compile(
    r"^(?:what if|what happens if|what would happen if|preview|show the impact of|"
    r"impact of)\s+(?:i|we|you)?\s*(?P<rest>.+?)\??$"
)
_SPEC = re.compile(
    r"^(?:i want|i'd like|i would like|i need|we need|we want|design|build|create|make me|"
    r"give me)\s+(?:a|an|me a|me an)\s+.*\b(car|city ?car|hatch(?:back)?|sedan|saloon|suv|"
    r"crossover|pick-?up|truck|sports ?car|coupe|roadster|van|minivan|mpv|vehicle|ev)\b"
)
_VERIFY = re.compile(r"^(?:please )?(?:verify|check|re-?check)\b.*\brequirements?\b")
_REQUIRE = re.compile(
    r"^(?:please )?(?:add (?:a )?requirement:?|requirement:|require|"
    r"we require|it must|the requirement is)\b\s*(?P<rest>.+)$"
)
_AT_LEAST = (
    r"(?:at least|no less than|not less than|a minimum of|minimum|above|over|more than|"
    r"greater than|>=|>)"
)
_AT_MOST = (
    r"(?:at most|no more than|not more than|a maximum of|maximum|below|under|less than|within|<=|<)"
)
_LONGITUDINAL_METRICS = {  # requirement phrase -> longitudinal metric
    "0-100 time": "accel_time",
    "0 to 100 time": "accel_time",
    "0-100": "accel_time",
    "acceleration time": "accel_time",
    "stopping distance": "stopping_distance",
    "braking distance": "stopping_distance",
}
_METRICS = {  # requirement phrase -> quarter-car metric
    "peak body acceleration": "peak_body_acceleration",
    "rms body acceleration": "rms_body_acceleration",
    "body settling time": "settling_time",
    "settling time": "settling_time",
    "bump travel": "max_bump_travel",
    "compression travel": "max_bump_travel",
    "rebound travel": "max_rebound_travel",
    "body displacement": "peak_body_displacement",
    "overshoot": "step_overshoot",
    "time off the road": "lift_off_time",
    "lift-off time": "lift_off_time",
    "lift off time": "lift_off_time",
    "minimum tyre load": "min_tyre_load_ratio",
    "tyre load": "min_tyre_load_ratio",
}
_TEST_CONTEXT = re.compile(
    r"\b(test|tests|scenario|hump|pothole|step|bump test|quarter[- ]car|over the)\b"
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
    long_phrase = next(
        (ph for ph in sorted(_LONGITUDINAL_METRICS, key=len, reverse=True) if ph in text), None
    )
    if long_phrase is not None:
        metric = _LONGITUDINAL_METRICS[long_phrase]
        stand_in = " stopping " if metric == "stopping_distance" else " 0-100 "
        request = _test_request(text.replace(long_phrase, stand_in))
        return Interpretation(
            Kind.REQUIREMENT,
            requirement={
                "kind": "performance",
                "test_id": "longitudinal",
                "metric": metric,
                "target": "vehicle",
                "scenario_id": request.scenario_id or "*",
                "comparator": comparator,
                "limit": value,
                "unit": "",
            },
        )
    phrase = next((ph for ph in sorted(_METRICS, key=len, reverse=True) if ph in text), None)
    metric = _METRICS[phrase] if phrase else None
    # The metric's own words ("bump travel") must not pick a scenario ("bump" -> hump).
    request = _test_request(text.replace(phrase, " ") if phrase else text)
    if metric is not None and (_TEST_CONTEXT.search(text) or _find_target(text) is None):
        return Interpretation(
            Kind.REQUIREMENT,
            requirement={
                "kind": "performance",
                "test_id": "quarter_car",
                "metric": metric,
                "target": request.target or "*",
                "scenario_id": request.scenario_id or "*",
                "comparator": comparator,
                "limit": value,
                "unit": "",
            },
        )
    if re.search(r"\bbody acceleration\b", text):
        return Interpretation(
            Kind.CLARIFICATION,
            reason=Reason.INVALID,
            question="Peak or RMS body acceleration?",
            suggestions=[
                f"require the peak body acceleration to be at most {value:g} m/s²",
                f"require the rms body acceleration to be at most {value:g} m/s²",
            ],
        )
    target = _find_target(text)
    if target is None:
        question = f"Which quantity is the requirement about in '{text}'?"
        return Interpretation(Kind.CLARIFICATION, reason=Reason.NO_TARGET, question=question)
    if len(target.ids) > 1:
        ids = target.ids
        if request.target:
            ids = tuple(i for i in ids if i.startswith(request.target)) or ids
        if len(ids) > 1:
            return Interpretation(
                Kind.CLARIFICATION,
                reason=Reason.INVALID,
                question=f"'{target.alias}' covers several parameters; say front or rear.",
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
    for pattern, metric, sense in _OBJECTIVES:
        if re.search(pattern, text):
            return metric, sense
    return None


_ACCEL = re.compile(r"\baccelerat|\b0\s*(?:-|to)\s*100\b|\bsprint\b")
_BRAKE = re.compile(r"\bbrak(?:e|es|ing)\b|\bstopping\b|\bstop from\b")


def _test_request(text: str) -> TestRequest:
    if _ACCEL.search(text):
        return TestRequest("longitudinal", "vehicle", "accel_0_100")
    if _BRAKE.search(text):
        wet = re.search(r"\bwet|rain", text) is not None
        dry = re.search(r"\bdry\b", text) is not None
        scenario = "brake_100_0_wet" if wet else "brake_100_0_dry" if dry else None
        return TestRequest("longitudinal", "vehicle", scenario)
    words = set(_words(text))
    test_id = "ride_modes" if re.search(r"ride modes?|natural frequenc|modal", text) else None
    scenario = None
    if re.search(r"\bpotholes?\b", text):
        scenario = "pothole_50"
    elif re.search(r"\b(hump|speed bump|bump)\b", text):
        scenario = "hump_75"
    elif re.search(r"\b(step|kerb|curb)\b", text):
        scenario = "step_25"
    front, rear = "front" in words, "rear" in words or "back" in words
    target = "front" if front and not rear else "rear" if rear and not front else None
    focus = (
        "travel"
        if "travel" in words
        else "contact"
        if words & {"contact", "lift", "lifted", "grip"}
        else None
    )
    return TestRequest(test_id or "quarter_car", target, None if test_id else scenario, focus)


def _split_test_tail(t: str) -> tuple[str, TestRequest | None]:
    """'increase the rear damping by 10% and test its response' -> (command text, request)."""
    match = _TEST_TAIL.search(t)
    if match is None or match.start() == 0:
        return t, None
    request = _test_request(match.group("rest"))
    return t[: match.start()].strip(), request


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
    if _VERIFY.search(t):
        return Interpretation(Kind.VERIFY)
    if _SPEC.match(t) or t.startswith("spec:") or t.startswith("specification:"):
        return Interpretation(Kind.SPEC)
    if (req := _REQUIRE.match(t)) is not None:
        return _parse_requirement(req.group("rest"))
    if (what_if := _PREVIEW.match(t)) is not None:
        inner = parse(what_if.group("rest"))
        if inner.kind is Kind.COMMAND and inner.command is not None:
            return Interpretation(
                Kind.PREVIEW, command=inner.command, assumptions=inner.assumptions
            )
        return inner
    if _DIAGNOSE.search(t):
        return Interpretation(Kind.DIAGNOSE, tests=_test_request(t))
    if _OPTIMIZE.search(t) and (objective := _objective(t)) is not None:
        request = _test_request(t)
        words = set(_words(t))
        unmodelled = tuple(v for k, v in _UNMODELLED_LIMITS.items() if k in words)
        return Interpretation(
            Kind.OPTIMIZE,
            tests=TestRequest(
                request.test_id, request.target, request.scenario_id, None, *objective, unmodelled
            ),
        )
    if _LOOP.search(t) and not _find_target(t.replace("suspension", "")):
        return Interpretation(Kind.LOOP, tests=_test_request(t))
    if t.endswith("?") or _QUESTION_START.match(t):
        return _parse_query(t.rstrip("?"))
    if re.match(rf"^(?:please )?{_TEST_VERB}\b", t) and _TEST_WORDS.search(t):
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
