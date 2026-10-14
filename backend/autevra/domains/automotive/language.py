"""The automotive language: how engineers talk about road vehicles.

Registered into ``autevra.ai.language`` by the automotive domain module. The parser
engine stays domain-agnostic; this module supplies vocabulary normalisation, comparative
words, test-request reading, requirement metric phrases, optimisation objectives,
unmodelled concepts, the scope vocabulary and the LLM prompt's framing.
"""

import re

from autevra.ai.concepts import Concept
from autevra.ai.language import Language
from autevra.ai.rule_parser import Interpretation, Kind, Reason, TestRequest, find_target, words_of

NORMALISERS = (
    (r"tire", "tyre"),
    (r"(\d+)s\b", r"\1"),  # "18s" -> "18" (rim sizes)
    (r"(\d) in (wheels?|alloys?)\b", r"\1 in rims"),  # "18 inch wheels" = rim size
    (
        r"\bfront and rear (track|overhangs?)\b",
        lambda m: "track" if m.group(1) == "track" else "overhangs",
    ),
    (r"\bthe (car|vehicle)\b", "it"),
)

COMPARATIVES: dict[str, tuple[str, bool]] = {
    "longer": ("overall_length", True),
    "lengthen": ("overall_length", True),
    "shorter": ("overall_length", False),
    "shorten": ("overall_length", False),
    "higher": ("ground_clearance", True),
}
ADJECTIVES: dict[str, str] = {
    "wide": "body_width",
    "tall": "overall_height",
    "high": "overall_height",
    "long": "overall_length",
}

QUERY_WORDS = {
    "long": "overall_length",
    "wide": "body_width",
    "tall": "overall_height",
    "high": "overall_height",
}
DERIVED_EXAMPLES = {
    "overall_length": [
        "increase the wheelbase by 100 mm",
        "increase the front overhang by 50 mm",
        "increase the rear overhang by 50 mm",
    ],
}


def target_hint(words: list[str], ids: tuple[str, ...]) -> tuple[str, ...] | None:
    """'lower the roof' means the overall height, not the roof panel length."""
    if ids == ("roof_length",) and any(w in ("lower", "raise") for w in words):
        return ("overall_height",)
    return None


TEST_WORDS = (
    r"quarter[- ]car|half[- ]car|pitch(?:ing)?|pothole|hump|speed bump|ride modes?|"
    r"acceleration|braking|stopping|0-100|natural frequenc(?:y|ies)|modal"
)

_ACCEL = re.compile(r"\baccelerat|\b0\s*(?:-|to)\s*100\b|\bsprint\b")
_BRAKE = re.compile(r"\bbrak(?:e|es|ing)\b|\bstopping\b|\bstop from\b")


def test_request(text: str) -> TestRequest:
    if _ACCEL.search(text):
        return TestRequest("longitudinal", "vehicle", "accel_0_100")
    if _BRAKE.search(text):
        wet = re.search(r"\bwet|rain", text) is not None
        dry = re.search(r"\bdry\b", text) is not None
        scenario = "brake_100_0_wet" if wet else "brake_100_0_dry" if dry else None
        return TestRequest("longitudinal", "vehicle", scenario)
    words = set(words_of(text))
    test_id = "ride_modes" if re.search(r"ride modes?|natural frequenc|modal", text) else None
    if re.search(r"half[- ]car|\bpitch(?:ing)?\b|both axles|whole (?:car|vehicle)", text):
        test_id = "half_car"
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
    if test_id == "half_car":
        return TestRequest("half_car", "vehicle", scenario, focus)
    return TestRequest(test_id or "quarter_car", target, None if test_id else scenario, focus)


_LONGITUDINAL_METRICS = {  # requirement phrase -> longitudinal metric
    "0-100 time": "accel_time",
    "0 to 100 time": "accel_time",
    "0-100": "accel_time",
    "acceleration time": "accel_time",
    "stopping distance": "stopping_distance",
    "braking distance": "stopping_distance",
}
_HALF_CAR_METRICS = {  # requirement phrase -> half-car metric
    "peak pitch angle": "peak_pitch_angle",
    "pitch angle": "peak_pitch_angle",
    "pitch": "peak_pitch_angle",
    "rms pitch acceleration": "rms_pitch_acceleration",
    "pitch acceleration": "peak_pitch_acceleration",
    "rms heave acceleration": "rms_heave_acceleration",
    "heave acceleration": "peak_heave_acceleration",
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


def requirement_metric(text: str, value: float):  # type: ignore[no-untyped-def]
    """Requirement fields for a test metric named in the text, a clarification, or None."""
    long_phrase = next(
        (ph for ph in sorted(_LONGITUDINAL_METRICS, key=len, reverse=True) if ph in text), None
    )
    if long_phrase is not None:
        metric = _LONGITUDINAL_METRICS[long_phrase]
        stand_in = " stopping " if metric == "stopping_distance" else " 0-100 "
        request = test_request(text.replace(long_phrase, stand_in))
        return {
            "kind": "performance",
            "test_id": "longitudinal",
            "metric": metric,
            "target": "vehicle",
            "scenario_id": request.scenario_id or "*",
        }
    half = next(
        (ph for ph in sorted(_HALF_CAR_METRICS, key=len, reverse=True)
         if re.search(rf"\b{re.escape(ph)}\b", text)),
        None,
    )  # fmt: skip
    if half is not None:
        request = test_request(text.replace(half, " "))
        return {
            "kind": "performance",
            "test_id": "half_car",
            "metric": _HALF_CAR_METRICS[half],
            "target": "vehicle",
            "scenario_id": request.scenario_id or "*",
        }
    phrase = next((ph for ph in sorted(_METRICS, key=len, reverse=True) if ph in text), None)
    metric = _METRICS[phrase] if phrase else None
    # The metric's own words ("bump travel") must not pick a scenario ("bump" -> hump).
    request = test_request(text.replace(phrase, " ") if phrase else text)
    if metric is not None and (_TEST_CONTEXT.search(text) or find_target(text) is None):
        return {
            "kind": "performance",
            "test_id": "quarter_car",
            "metric": metric,
            "target": request.target or "*",
            "scenario_id": request.scenario_id or "*",
        }
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
    return None


_COMFORT = r"\bcomfort|comfortable|comfier|plusher|smoother|ride quality|better ride"
_GRIP = r"\bgrip|road holding|roadholding|tyre contact|keep the tyres? on"
_OBJECTIVES = (  # phrase -> (metric, sense)
    (_COMFORT, "rms_body_acceleration", "minimize"),
    (r"\bsettl", "settling_time", "minimize"),
    (_GRIP, "min_tyre_load_ratio", "maximize"),
    (r"\bharsh|peak acceleration|jolt", "peak_body_acceleration", "minimize"),
)
_UNMODELLED_LIMITS = {
    "roll": "body roll",
    "pitch": "pitch",
    "dive": "brake dive",
    "squat": "squat",
    "noise": "noise",
}
SPEC_TRIGGER = (
    r"^(?:i want|i'd like|i would like|i need|we need|we want|design|build|create|make me|"
    r"give me)\s+(?:a|an|me a|me an)\s+.*\b(car|city ?car|hatch(?:back)?|sedan|saloon|suv|"
    r"crossover|pick-?up|truck|sports ?car|coupe|roadster|van|minivan|mpv|vehicle|ev)\b"
)


SOFTER = frozenset(
    {
        "softer",
        "soft",
        "stiffer",
        "stiff",
        "firmer",
        "firm",
        "harder",
        "comfier",
        "sportier",
        "plusher",
    }
)


def _suspension_clarify(text: str) -> tuple[str, list[str]] | None:
    """'Softer' or 'stiffer' suspension: which quantity, front or rear, and how much."""
    words = set(re.findall(r"[a-z]+", text.lower()))
    if not words & SOFTER:
        return None
    softer = bool(words & {"softer", "soft", "comfier", "plusher"})
    verb = "reduce" if softer else "increase"
    question = (
        f"'{'Softer' if softer else 'Stiffer'}' could mean the spring rate, the bump "
        "(compression) damping or the rebound damping, front, rear or both. Which one do "
        "you mean, and by how much?"
    )
    return question, [
        f"{verb} the spring rate by 10%",
        f"{verb} the bump damping by 10%",
        f"{verb} the rebound damping by 10%",
    ]


CONCEPTS: tuple[Concept, ...] = (
    Concept(
        "suspension",
        (
            "suspension",
            "ride",
            "spring",
            "springs",
            "damper",
            "dampers",
            "damping",
            "shock",
            "shocks",
            "shock absorber",
            "coilover",
            "coilovers",
        ),
        (
            "spring rate (N/mm)",
            "bump (compression) damping (N·s/m)",
            "rebound damping (N·s/m)",
            "ride height (ground clearance)",
        ),
        "now",
        modelled=True,
        clarify=_suspension_clarify,
    ),
    Concept(
        "brakes",
        ("brake", "brakes", "braking", "disc", "discs", "rotor", "rotors", "caliper", "calipers"),
        ("brake disc diameter", "disc thickness", "caliper piston area"),
        "Phase 5 (brakes)",
    ),
    Concept(
        "engine",
        (
            "engine",
            "motor",
            "horsepower",
            "power",
            "torque",
            "displacement",
            "turbo",
            "cylinder",
            "cylinders",
            "piston",
            "pistons",
            "crankshaft",
        ),
        ("power and torque targets", "displacement", "engine envelope dimensions"),
        "Phase 3 (specification) and Phase 5 (powertrain geometry)",
    ),
    Concept(
        "transmission",
        (
            "gearbox",
            "transmission",
            "gear",
            "gears",
            "gear ratio",
            "final drive",
            "differential",
            "clutch",
        ),
        ("gear ratios", "final drive ratio", "gearbox envelope"),
        "Phase 5 (gearbox) and Phase 6 (powertrain simulation)",
    ),
    Concept(
        "steering_system",
        ("steering ratio", "steering rack", "rack", "tie rod", "tie rods", "ackermann"),
        ("steering ratio", "rack travel", "Ackermann geometry"),
        "Phase 5 (steering); max steer angle is editable now",
    ),
    Concept(
        "roof_and_aero_options",
        ("sunroof", "panoramic roof", "moonroof", "roof rack", "roof bars", "spoiler", "wing"),
        ("roof opening size", "roof load", "downforce"),
        "later (body options)",
    ),
)

SCOPE_WORDS = frozenset(
    {
        "car",
        "hub",
        "hubs",
        "road",
        "tarmac",
        "vehicle",
        "it",
        "chassis",
        "frame",
        "body",
        "axle",
        "axles",
        "wheel",
        "wheels",
        "tyre",
        "tyres",
        "tire",
        "tires",
        "cabin",
        "roof",
        "bonnet",
        "hood",
        "boot",
        "trunk",
        "door",
        "doors",
        "bumper",
        "fender",
        "arch",
        "arches",
        "design",
        "model",
        "suv",
        "sedan",
        "hatchback",
        "pickup",
        "truck",
        "coupe",
        "drivetrain",
        "awd",
        "fwd",
        "rwd",
        "simulation",
        "simulate",
        "test",
        "acceleration",
        "cornering",
        "stopping",
        "pothole",
        "potholes",
        "speed",
        "drag",
        "aero",
        "aerodynamic",
        "step",
        "export",
        "cad",
    }
)


OUT_OF_SCOPE = (
    "Autevra handles automotive design, engineering and testing. I can change the vehicle's "
    "dimensions, wheels, cabin, chassis, suspension and mass, run suspension tests, or answer "
    "questions about them."
)
PROMPT_INTRO = "You convert automotive design instructions into JSON for the Autevra CAD system."
PROMPT_NOTES = (
    "Coordinate system: ISO 8855, millimetres. Vehicle length is derived (front_overhang +\n"
    "wheelbase + rear_overhang), so ask which one to change instead of guessing."
)

PROMPT_EXAMPLES: list[tuple[str, dict]] = [
    (
        "stretch the distance between the axles by 4 inches",
        {
            "action": "set_parameters",
            "changes": [
                {"parameter": "wheelbase", "operation": "increase", "value": 4, "unit": "in"}
            ],
            "query": [],
            "question": "",
        },
    ),
    (
        "give it a bit more room under the floor, say 15 mm",
        {
            "action": "set_parameters",
            "changes": [
                {
                    "parameter": "ground_clearance",
                    "operation": "increase",
                    "value": 15,
                    "unit": "mm",
                }
            ],
            "query": [],
            "question": "",
        },
    ),
    (
        "how big are the wheels at the moment",
        {
            "action": "query",
            "changes": [],
            "query": ["rim_diameter", "tyre_diameter"],
            "question": "",
        },
    ),
    (
        "make the car look more aggressive",
        {
            "action": "clarify",
            "changes": [],
            "query": [],
            "question": "Which dimension should change: for example lower ride height, wider "
            "track or larger rims?",
        },
    ),
    (
        "write me a poem about the sea",
        {"action": "out_of_scope", "changes": [], "query": [], "question": ""},
    ),
]


LANGUAGE = Language(
    name="automotive",
    normalisers=NORMALISERS,
    comparatives=COMPARATIVES,
    adjectives=ADJECTIVES,
    query_words=QUERY_WORDS,
    derived_examples=DERIVED_EXAMPLES,
    target_hint=target_hint,
    test_words=TEST_WORDS,
    test_request=test_request,
    default_test="quarter_car",
    requirement_metric=requirement_metric,
    objectives=_OBJECTIVES,
    optimise_words="more comfortable|comfier|plusher|smoother",
    loop_words="suspension|corner",
    diagnose_words="lift|lifted",
    unmodelled_limits=_UNMODELLED_LIMITS,
    spec_trigger=SPEC_TRIGGER,
    option_aliases={
        "interior_trim": {
            "Standard": ("basic", "base", "entry"),
            "Comfort": ("mid", "comfort pack"),
            "Premium": ("luxury", "luxurious", "high end", "high-end", "top", "executive"),
        },
        "interior_colour": {
            "Charcoal": ("black interior", "dark interior"),
            "Stone Grey": ("grey interior", "gray interior"),
            "Cream": ("cream", "ivory", "white interior"),
            "Tan": ("tan", "camel", "beige interior"),
            "Cognac": ("cognac", "brown interior", "saddle"),
            "Oxblood": ("oxblood", "red interior", "burgundy"),
        },
        "driving_side": {
            "Left-hand drive": ("lhd", "left hand drive", "left-hand-drive"),
            "Right-hand drive": ("rhd", "right hand drive", "right-hand-drive"),
        },
        "paint_colour": {
            "Arctic White": ("white", "pearl white", "snow white"),
            "Lunar Silver": ("silver",),
            "Graphite Grey": ("grey", "gray", "gunmetal", "dark grey", "dark gray"),
            "Obsidian Black": ("black",),
            "Racing Red": ("red",),
            "Deep Ocean Blue": ("navy", "dark blue", "navy blue"),
            "Electric Blue": ("blue", "bright blue"),
            "Forest Green": ("green", "racing green", "british racing green"),
            "Sunset Orange": ("orange",),
            "Solar Yellow": ("yellow",),
            "Champagne": ("gold", "beige"),
            "Satin Bronze": ("bronze", "brown"),
        },
        "paint_finish": {
            "Gloss": ("glossy", "solid", "shiny"),
            "Metallic": ("metal flake",),
            "Matte": ("matt", "satin", "flat"),
            "Pearl": ("pearlescent", "pearl effect"),
        },
        "body_style": {
            "Sedan": ("saloon", "three-box", "three box", "notchback"),
            "Hatchback": ("hatch", "two-box", "two box", "estate", "wagon", "station wagon"),
            "SUV": ("crossover", "4x4", "sport utility vehicle", "off-roader"),
            "Coupe": ("coupé", "fastback", "sports car", "gt"),
            "Pickup": ("pick-up", "pick up", "pickup truck", "ute"),
            "Van": ("minivan", "mpv", "people carrier", "one-box", "one box", "panel van"),
            "Box truck": ("truck", "lorry", "light truck", "delivery truck", "luton", "box van"),
        },
    },
    concepts=CONCEPTS,
    scope_words=SCOPE_WORDS,
    out_of_scope=OUT_OF_SCOPE,
    prompt_intro=PROMPT_INTRO,
    prompt_notes=PROMPT_NOTES,
    prompt_subject="vehicle",
    prompt_scope="automotive design, engineering or testing",
    prompt_examples=tuple(PROMPT_EXAMPLES),
)
