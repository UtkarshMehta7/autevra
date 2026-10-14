"""Vehicle specification: adaptive interview, conflict detection and design generation.

The specification captures what the user wants (class, use, powertrain, power, mass, seats,
targets). Every value records its source: ``user`` or ``default`` (a class-typical value,
labelled as such). Checks come in two severities:

- ``conflict``: impossible within a stated model. Example: the 0–100 km/h target is faster
  than a lower-bound estimate that ignores drag, rolling resistance and shift time.
- ``warning``: implausible against a stated basis (e.g. the battery would be over 40 % of the
  vehicle mass at an assumed pack energy density). The user may proceed.

Generation turns the specification into a full parameter set (class templates for the
dimensions; springs from target ride frequencies; dampers from damping ratios) and checks
it with the design rules, so packaging conflicts (seven seats in a city car) surface as
rule violations. The result is a proposal plus provisional requirements; nothing is applied
here.
"""

import math
import re
from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel, Field

from autevra.core.parameters import REGISTRY, default_values
from autevra.core.rules import Violation, validate
from autevra.core.templates import Template
from autevra.domains.automotive import derived as d

G = d.G
HP_KW = 0.745699872  # mechanical horsepower
PS_KW = 0.73549875  # metric horsepower

VehicleClass = Literal[
    "city_car",
    "hatchback",
    "sedan",
    "suv",
    "pickup",
    "sports_car",
    "van",
    "box_truck",
    "estate",
    "crossover",
    "mpv",
    "roadster",
    "supercar",
]
CLASS_LABELS = {
    "city_car": "city car",
    "hatchback": "hatchback",
    "sedan": "sedan",
    "suv": "SUV",
    "pickup": "pickup",
    "sports_car": "sports car",
    "van": "van",
    "box_truck": "box truck",
    "estate": "estate",
    "crossover": "crossover",
    "mpv": "MPV",
    "roadster": "roadster",
    "supercar": "supercar",
}


class Answer(BaseModel):
    value: str | float
    source: Literal["user", "default"] = "user"
    note: str = ""


class VehicleSpec(BaseModel):
    answers: dict[str, Answer] = {}

    def get(self, key: str) -> str | float | None:
        a = self.answers.get(key)
        return None if a is None else a.value

    def set(self, key: str, value: str | float, source: str = "user", note: str = "") -> None:
        self.answers[key] = Answer(value=value, source=source, note=note)  # type: ignore[arg-type]


# --- Questions --------------------------------------------------------------------------


class Question(BaseModel):
    id: str
    prompt: str
    kind: Literal["choice", "number"]
    options: list[str] = []  # choice ids
    option_labels: list[str] = []
    unit: str = ""
    minimum: float | None = None
    maximum: float | None = None
    optional: bool = False  # skipping uses the class-typical default
    help: str = ""


def _choice(qid: str, prompt: str, options: Mapping[str, str], **kw: object) -> Question:
    return Question(
        id=qid,
        prompt=prompt,
        kind="choice",
        options=list(options),
        option_labels=list(options.values()),
        **kw,
    )  # type: ignore[arg-type]


QUESTIONS: tuple[Question, ...] = (
    _choice("vehicle_class", "What kind of vehicle is it?", CLASS_LABELS),
    _choice(
        "use",
        "What is it mainly for?",
        {
            "commuting": "commuting",
            "family": "family",
            "touring": "long-distance touring",
            "off_road": "off-road",
            "track": "track days",
            "delivery": "delivery / cargo",
        },
    ),
    _choice(
        "powertrain",
        "Which powertrain?",
        {
            "petrol": "petrol",
            "diesel": "diesel",
            "hybrid": "hybrid",
            "electric": "battery electric",
        },
    ),
    _choice(
        "drivetrain",
        "Which wheels are driven?",
        {
            "fwd": "front-wheel drive",
            "rwd": "rear-wheel drive",
            "awd": "all-wheel drive",
        },
    ),
    Question(
        id="peak_power",
        prompt="Peak power?",
        kind="number",
        unit="kW",
        minimum=20,
        maximum=1500,
        help="hp and PS are converted.",
    ),
    Question(
        id="battery_capacity",
        prompt="Usable battery capacity?",
        kind="number",
        unit="kWh",
        minimum=10,
        maximum=250,
    ),
    Question(
        id="target_mass",
        prompt="Target kerb mass?",
        kind="number",
        unit="kg",
        minimum=600,
        maximum=4000,
        optional=True,
        help="Skip to use a class-typical value (labelled as a default).",
    ),
    _choice("seats", "How many seats?", {"2": "2", "4": "4", "5": "5", "7": "7"}),
    Question(
        id="accel_0_100",
        prompt="Target 0–100 km/h time?",
        kind="number",
        unit="s",
        minimum=2,
        maximum=30,
        optional=True,
        help="Skip if there is no target.",
    ),
    _choice(
        "ride",
        "Ride character?",
        {
            "comfort": "comfort",
            "balanced": "balanced",
            "sporty": "sporty",
        },
        optional=True,
    ),
    Question(
        id="rim_diameter",
        prompt="Wheel (rim) size?",
        kind="number",
        unit="in",
        minimum=13,
        maximum=22,
        optional=True,
    ),
)
BY_ID = {q.id: q for q in QUESTIONS}


def applicable(q: Question, spec: VehicleSpec) -> bool:
    """Conditions of the question graph."""
    if q.id == "battery_capacity":
        return spec.get("powertrain") == "electric"
    if q.id == "drivetrain":
        return spec.get("vehicle_class") is not None
    return True


def next_question(spec: VehicleSpec) -> Question | None:
    for q in QUESTIONS:
        if applicable(q, spec) and q.id not in spec.answers:
            return q
    return None


def answer(spec: VehicleSpec, qid: str, raw: str | float | None) -> str | None:
    """Record an answer (``None`` skips an optional question). Returns an error message."""
    q = BY_ID.get(qid)
    if q is None:
        return f"unknown question '{qid}'"
    if raw is None or raw == "":
        if not q.optional:
            return f"'{q.prompt}' needs an answer"
        spec.answers.pop(qid, None)
        spec.set(qid, "skip", source="default", note="skipped: class-typical value used")
        return None
    if q.kind == "choice":
        value = str(raw)
        if value not in q.options:
            return f"choose one of: {', '.join(q.option_labels)}"
        spec.set(qid, value)
        return None
    try:
        number = float(raw)
    except (TypeError, ValueError):
        return f"'{raw}' is not a number"
    if q.minimum is not None and number < q.minimum or q.maximum is not None and number > q.maximum:
        return f"{q.prompt} must be between {q.minimum:g} and {q.maximum:g} {q.unit}"
    spec.set(qid, number)
    return None


# --- Slot filling from text --------------------------------------------------------------

_CLASS_WORDS = (
    (r"city ?car|microcar", "city_car"),
    (r"hatch(?:back)?", "hatchback"),
    (r"estate|station wagon|\bwagon\b|shooting brake", "estate"),
    (r"sedan|saloon", "sedan"),
    (r"crossover|\bcuv\b", "crossover"),
    (r"suv|4x4", "suv"),
    (r"box ?truck|light truck|delivery truck|lorry|luton", "box_truck"),
    (r"pick-?up|ute|truck", "pickup"),
    (r"supercar|hypercar|mid-?engine", "supercar"),
    (r"roadster|convertible|cabriolet|spyder|spider", "roadster"),
    (r"sports? ?car|coupe", "sports_car"),
    (r"\bmpv\b|minivan|people carrier", "mpv"),
    (r"\bvan\b", "van"),
)
_USE_WORDS = (
    (r"off-?road|trail|overland", "off_road"),
    (r"track|racing|circuit", "track"),
    (r"deliver|cargo|courier", "delivery"),
    (r"family|school run", "family"),
    (r"commut|city driving|urban", "commuting"),
    (r"touring|long[- ]distance|motorway", "touring"),
)
_POWERTRAIN_WORDS = (
    (r"plug-?in hybrid|phev|hybrid|hev", "hybrid"),
    (r"electric|\bev\b|\bbev\b|battery[- ]electric", "electric"),
    (r"diesel", "diesel"),
    (r"petrol|gasoline|\bgas\b", "petrol"),
)
_DRIVE_WORDS = (
    (r"\bawd\b|\b4wd\b|all[- ]wheel|four[- ]wheel", "awd"),
    (r"\brwd\b|rear[- ]wheel drive|rear[- ]drive", "rwd"),
    (r"\bfwd\b|front[- ]wheel drive|front[- ]drive", "fwd"),
)
_RIDE_WORDS = (
    (r"comfort|soft|plush|smooth", "comfort"),
    (r"sport|firm|stiff|agile", "sporty"),
    (r"balanced", "balanced"),
)
NUM = r"(\d+(?:\.\d+)?)"


def extract(text: str) -> dict[str, str | float]:
    """Specification answers stated in free text. Deterministic; amounts need their unit."""
    t = text.lower().replace("–", "-")
    found: dict[str, str | float] = {}
    for words, key in (
        (_CLASS_WORDS, "vehicle_class"),
        (_USE_WORDS, "use"),
        (_POWERTRAIN_WORDS, "powertrain"),
        (_DRIVE_WORDS, "drivetrain"),
        (_RIDE_WORDS, "ride"),
    ):
        for pattern, value in words:
            if re.search(pattern, t):
                found[key] = value
                break
    if m := re.search(NUM + r"\s*kwh\b", t):
        found["battery_capacity"] = float(m.group(1))
    if m := re.search(NUM + r"\s*kw\b", t):
        found["peak_power"] = float(m.group(1))
    elif m := re.search(NUM + r"\s*(?:b?hp|horsepower)\b", t):
        found["peak_power"] = round(float(m.group(1)) * HP_KW, 1)
    elif m := re.search(NUM + r"\s*ps\b", t):
        found["peak_power"] = round(float(m.group(1)) * PS_KW, 1)
    if m := re.search(NUM + r"\s*(?:kg|kilograms?)\b", t):
        found["target_mass"] = float(m.group(1))
    elif m := re.search(NUM + r"\s*(?:t|tonnes?|tons?)\b", t):
        found["target_mass"] = float(m.group(1)) * 1000
    if m := re.search(
        r"0\s*(?:-|to)\s*100(?:\s*km/?h)?\s*(?:in\s*)?" + NUM + r"\s*(?:s|sec|seconds?)\b", t
    ):
        found["accel_0_100"] = float(m.group(1))
    if m := re.search(r"\b(\d)\s*(?:-\s*)?(?:seats?|seater)\b", t):
        found["seats"] = m.group(1)
    if m := re.search(NUM + r"\s*(?:\"|in|inch|inches)\s*(?:wheels?|rims?|alloys?)\b", t):
        found["rim_diameter"] = float(m.group(1))
    return found


# --- Checks ------------------------------------------------------------------------------


class Check(BaseModel):
    id: str
    severity: Literal["conflict", "warning", "info"]
    message: str
    basis: str  # the model or reference value the check rests on
    answers: list[str] = []  # answers involved
    parameters: list[str] = []  # generated parameters involved
    estimate: dict[str, float] = {}


# Class templates. Values are starting points chosen inside the registry bounds and checked
# by the design rules in tests; they are not data for any real vehicle.
TEMPLATES: dict[str, dict[str, float]] = {
    "city_car": {
        "roof_type": 0,
        "roof_rails": 0,
        "rear_spoiler": 0,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 4,
        "rim_finish": 5,
        "head_lamp_style": 2,
        "tail_lamp_style": 2,
        "front_suspension": 1,
        "rear_suspension": 1,
        "chassis_type": 1,
        "seat_rows": 2,
        "interior_trim": 0,
        "interior_colour": 1,
        "paint_colour": 0,
        "paint_finish": 0,
        "drag_coefficient": 0.33,
        "rolling_resistance": 0.01,
        "cg_height": 520,
        "body_style": 1,
        "wheelbase": 2450,
        "front_overhang": 700,
        "rear_overhang": 600,
        "body_width": 1660,
        "overall_height": 1500,
        "beltline_height": 920,
        "ground_clearance": 140,
        "track_front": 1430,
        "track_rear": 1420,
        "rim_diameter": 15,
        "tyre_width": 185,
        "tyre_aspect_ratio": 65,
        "cabin_length": 2300,
        "roof_length": 1300,
        "cabin_offset": -100,
        "vehicle_mass": 1050,
        "front_mass_distribution": 61,
        "haunch": 25,
        "nose_taper": 80,
        "tail_taper": 88,
        "sill_tuck": 50,
        "body_roundness": 60,
        "tumblehome": 100,
    },
    "hatchback": {
        "roof_type": 2,
        "roof_rails": 0,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 1,
        "rim_finish": 1,
        "head_lamp_style": 0,
        "tail_lamp_style": 1,
        "front_suspension": 1,
        "rear_suspension": 1,
        "chassis_type": 1,
        "seat_rows": 2,
        "interior_trim": 1,
        "interior_colour": 0,
        "paint_colour": 6,
        "paint_finish": 1,
        "drag_coefficient": 0.31,
        "rolling_resistance": 0.01,
        "cg_height": 540,
        "body_style": 1,
        "wheelbase": 2620,
        "front_overhang": 850,
        "rear_overhang": 750,
        "body_width": 1790,
        "overall_height": 1460,
        "beltline_height": 940,
        "ground_clearance": 140,
        "track_front": 1540,
        "track_rear": 1520,
        "rim_diameter": 16,
        "tyre_width": 205,
        "tyre_aspect_ratio": 55,
        "cabin_length": 2450,
        "roof_length": 1450,
        "cabin_offset": -150,
        "vehicle_mass": 1300,
        "front_mass_distribution": 60,
        "haunch": 30,
        "nose_taper": 74,
        "tail_taper": 84,
        "sill_tuck": 60,
        "body_roundness": 50,
        "tumblehome": 110,
    },
    "sedan": {
        "roof_type": 2,
        "roof_rails": 0,
        "rear_spoiler": 0,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 2,
        "rim_finish": 3,
        "head_lamp_style": 1,
        "tail_lamp_style": 0,
        "front_suspension": 1,
        "rear_suspension": 2,
        "chassis_type": 1,
        "seat_rows": 2,
        "interior_trim": 2,
        "interior_colour": 3,
        "paint_colour": 3,
        "paint_finish": 1,
        "drag_coefficient": 0.28,
        "rolling_resistance": 0.01,
        "cg_height": 530,
        "body_style": 0,
        "wheelbase": 2800,
        "front_overhang": 900,
        "rear_overhang": 1050,
        "body_width": 1830,
        "overall_height": 1450,
        "beltline_height": 960,
        "ground_clearance": 140,
        "track_front": 1570,
        "track_rear": 1570,
        "rim_diameter": 17,
        "tyre_width": 225,
        "tyre_aspect_ratio": 50,
        "cabin_length": 2600,
        "roof_length": 1500,
        "cabin_offset": -150,
        "vehicle_mass": 1550,
        "front_mass_distribution": 57,
        "haunch": 30,
        "nose_taper": 72,
        "tail_taper": 82,
        "sill_tuck": 60,
        "body_roundness": 45,
        "tumblehome": 110,
    },
    "suv": {
        "roof_type": 1,
        "roof_rails": 1,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 1,
        "wheel_design": 0,
        "rim_finish": 0,
        "head_lamp_style": 3,
        "tail_lamp_style": 1,
        "front_suspension": 1,
        "rear_suspension": 2,
        "chassis_type": 1,
        "seat_rows": 2,
        "interior_trim": 1,
        "interior_colour": 0,
        "paint_colour": 2,
        "paint_finish": 1,
        "drag_coefficient": 0.36,
        "rolling_resistance": 0.011,
        "cg_height": 680,
        "body_style": 2,
        "wheelbase": 2850,
        "front_overhang": 920,
        "rear_overhang": 1000,
        "body_width": 1900,
        "overall_height": 1700,
        "beltline_height": 1100,
        "ground_clearance": 200,
        "track_front": 1620,
        "track_rear": 1620,
        "rim_diameter": 18,
        "tyre_width": 235,
        "tyre_aspect_ratio": 60,
        "cabin_length": 2900,
        "roof_length": 2100,
        "cabin_offset": -200,
        "vehicle_mass": 1950,
        "front_mass_distribution": 55,
        "haunch": 35,
        "nose_taper": 80,
        "tail_taper": 88,
        "sill_tuck": 50,
        "body_roundness": 40,
        "tumblehome": 100,
    },
    "pickup": {
        "roof_type": 0,
        "roof_rails": 0,
        "rear_spoiler": 0,
        "mirror_type": 0,
        "tow_bar": 1,
        "wheel_design": 0,
        "rim_finish": 2,
        "head_lamp_style": 1,
        "tail_lamp_style": 2,
        "front_suspension": 2,
        "rear_suspension": 0,
        "chassis_type": 0,
        "seat_rows": 2,
        "interior_trim": 1,
        "interior_colour": 0,
        "paint_colour": 5,
        "paint_finish": 1,
        "drag_coefficient": 0.45,
        "rolling_resistance": 0.011,
        "cg_height": 750,
        "body_style": 4,
        "wheelbase": 3200,
        "front_overhang": 950,
        "rear_overhang": 1200,
        "body_width": 1900,
        "overall_height": 1800,
        "beltline_height": 1150,
        "ground_clearance": 220,
        "track_front": 1620,
        "track_rear": 1620,
        "rim_diameter": 18,
        "tyre_width": 255,
        "tyre_aspect_ratio": 65,
        "cabin_length": 2600,
        "roof_length": 1600,
        "cabin_offset": 600,
        "vehicle_mass": 2100,
        "front_mass_distribution": 57,
        "haunch": 15,
        "nose_taper": 86,
        "tail_taper": 96,
        "sill_tuck": 30,
        "body_roundness": 30,
        "tumblehome": 80,
    },
    "sports_car": {
        "roof_type": 0,
        "roof_rails": 0,
        "rear_spoiler": 2,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 3,
        "rim_finish": 4,
        "head_lamp_style": 1,
        "tail_lamp_style": 0,
        "front_suspension": 2,
        "rear_suspension": 3,
        "chassis_type": 1,
        "seat_rows": 1,
        "interior_trim": 2,
        "interior_colour": 5,
        "paint_colour": 4,
        "paint_finish": 3,
        "drag_coefficient": 0.32,
        "rolling_resistance": 0.011,
        "cg_height": 450,
        "body_style": 3,
        "wheelbase": 2450,
        "front_overhang": 950,
        "rear_overhang": 850,
        "body_width": 1900,
        "overall_height": 1250,
        "beltline_height": 850,
        "ground_clearance": 110,
        "track_front": 1620,
        "track_rear": 1600,
        "rim_diameter": 19,
        "tyre_width": 255,
        "tyre_aspect_ratio": 35,
        "cabin_length": 1900,
        "roof_length": 1000,
        "cabin_offset": -100,
        "vehicle_mass": 1450,
        "front_mass_distribution": 50,
        "haunch": 55,
        "nose_taper": 62,
        "tail_taper": 78,
        "sill_tuck": 70,
        "body_roundness": 60,
        "tumblehome": 150,
    },
    "van": {
        "roof_type": 0,
        "roof_rails": 2,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 1,
        "wheel_design": 5,
        "rim_finish": 0,
        "head_lamp_style": 0,
        "tail_lamp_style": 2,
        "front_suspension": 1,
        "rear_suspension": 0,
        "chassis_type": 1,
        "seat_rows": 3,
        "interior_trim": 0,
        "interior_colour": 1,
        "paint_colour": 0,
        "paint_finish": 0,
        "drag_coefficient": 0.35,
        "rolling_resistance": 0.01,
        "cg_height": 700,
        "body_style": 5,
        "wheelbase": 3000,
        "front_overhang": 900,
        "rear_overhang": 1000,
        "body_width": 1950,
        "overall_height": 2000,
        "beltline_height": 1100,
        "ground_clearance": 160,
        "track_front": 1650,
        "track_rear": 1650,
        "rim_diameter": 16,
        "tyre_width": 215,
        "tyre_aspect_ratio": 65,
        "cabin_length": 3600,
        "roof_length": 3300,
        "cabin_offset": -150,
        "vehicle_mass": 2000,
        "front_mass_distribution": 55,
        "haunch": 5,
        "nose_taper": 90,
        "tail_taper": 96,
        "sill_tuck": 20,
        "body_roundness": 30,
        "tumblehome": 60,
    },
    "box_truck": {
        "roof_type": 0,
        "roof_rails": 0,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 5,
        "rim_finish": 5,
        "head_lamp_style": 3,
        "tail_lamp_style": 1,
        "front_suspension": 0,
        "rear_suspension": 0,
        "chassis_type": 0,
        "seat_rows": 1,
        "interior_trim": 0,
        "interior_colour": 0,
        "paint_colour": 0,
        "paint_finish": 0,
        "drag_coefficient": 0.6,
        "rolling_resistance": 0.009,
        "cg_height": 950,
        "body_style": 6,
        "wheelbase": 3500,
        "front_overhang": 800,
        "rear_overhang": 1400,
        "body_width": 2050,
        "overall_height": 2100,
        "beltline_height": 1200,
        "ground_clearance": 200,
        "track_front": 1700,
        "track_rear": 1700,
        "rim_diameter": 16,
        "tyre_width": 215,
        "tyre_aspect_ratio": 75,
        "cabin_length": 2600,
        "roof_length": 1800,
        "cabin_offset": 0,
        "vehicle_mass": 3200,
        "front_mass_distribution": 45,
        "haunch": 0,
        "nose_taper": 94,
        "tail_taper": 98,
        "sill_tuck": 20,
        "body_roundness": 15,
        "tumblehome": 60,
    },
    "estate": {
        "roof_type": 2,
        "roof_rails": 1,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 2,
        "rim_finish": 3,
        "head_lamp_style": 1,
        "tail_lamp_style": 2,
        "front_suspension": 1,
        "rear_suspension": 2,
        "chassis_type": 1,
        "seat_rows": 2,
        "interior_trim": 2,
        "interior_colour": 3,
        "paint_colour": 3,
        "paint_finish": 1,
        "drag_coefficient": 0.29,
        "rolling_resistance": 0.01,
        "cg_height": 530,
        "body_style": 7,
        "wheelbase": 2800,
        "front_overhang": 900,
        "rear_overhang": 1080,
        "body_width": 1830,
        "overall_height": 1450,
        "beltline_height": 960,
        "ground_clearance": 140,
        "track_front": 1570,
        "track_rear": 1570,
        "rim_diameter": 17,
        "tyre_width": 225,
        "tyre_aspect_ratio": 50,
        "cabin_length": 2600,
        "roof_length": 1500,
        "cabin_offset": -150,
        "vehicle_mass": 1600,
        "front_mass_distribution": 57,
        "haunch": 30,
        "nose_taper": 72,
        "tail_taper": 88,
        "sill_tuck": 60,
        "body_roundness": 45,
        "tumblehome": 100,
    },
    "crossover": {
        "roof_type": 1,
        "roof_rails": 0,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 1,
        "wheel_design": 2,
        "rim_finish": 0,
        "head_lamp_style": 0,
        "tail_lamp_style": 0,
        "front_suspension": 1,
        "rear_suspension": 2,
        "chassis_type": 1,
        "seat_rows": 2,
        "interior_trim": 1,
        "interior_colour": 0,
        "paint_colour": 2,
        "paint_finish": 1,
        "drag_coefficient": 0.31,
        "rolling_resistance": 0.011,
        "cg_height": 680,
        "body_style": 8,
        "wheelbase": 2850,
        "front_overhang": 920,
        "rear_overhang": 1000,
        "body_width": 1900,
        "overall_height": 1600,
        "beltline_height": 1100,
        "ground_clearance": 190,
        "track_front": 1620,
        "track_rear": 1620,
        "rim_diameter": 18,
        "tyre_width": 235,
        "tyre_aspect_ratio": 60,
        "cabin_length": 2900,
        "roof_length": 1300,
        "cabin_offset": -200,
        "vehicle_mass": 1700,
        "front_mass_distribution": 55,
        "haunch": 40,
        "nose_taper": 74,
        "tail_taper": 84,
        "sill_tuck": 50,
        "body_roundness": 55,
        "tumblehome": 130,
    },
    "mpv": {
        "roof_type": 0,
        "roof_rails": 1,
        "rear_spoiler": 1,
        "mirror_type": 0,
        "tow_bar": 1,
        "wheel_design": 1,
        "rim_finish": 0,
        "head_lamp_style": 0,
        "tail_lamp_style": 2,
        "front_suspension": 1,
        "rear_suspension": 0,
        "chassis_type": 1,
        "seat_rows": 3,
        "interior_trim": 0,
        "interior_colour": 1,
        "paint_colour": 0,
        "paint_finish": 0,
        "drag_coefficient": 0.31,
        "rolling_resistance": 0.01,
        "cg_height": 700,
        "body_style": 9,
        "wheelbase": 3000,
        "front_overhang": 900,
        "rear_overhang": 1000,
        "body_width": 1950,
        "overall_height": 1750,
        "beltline_height": 1000,
        "ground_clearance": 160,
        "track_front": 1650,
        "track_rear": 1650,
        "rim_diameter": 16,
        "tyre_width": 215,
        "tyre_aspect_ratio": 65,
        "cabin_length": 3600,
        "roof_length": 3300,
        "cabin_offset": -150,
        "vehicle_mass": 2000,
        "front_mass_distribution": 55,
        "haunch": 15,
        "nose_taper": 78,
        "tail_taper": 92,
        "sill_tuck": 20,
        "body_roundness": 55,
        "tumblehome": 90,
    },
    "roadster": {
        "roof_type": 0,
        "roof_rails": 0,
        "rear_spoiler": 2,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 3,
        "rim_finish": 4,
        "head_lamp_style": 1,
        "tail_lamp_style": 0,
        "front_suspension": 2,
        "rear_suspension": 3,
        "chassis_type": 1,
        "seat_rows": 1,
        "interior_trim": 2,
        "interior_colour": 5,
        "paint_colour": 4,
        "paint_finish": 3,
        "drag_coefficient": 0.35,
        "rolling_resistance": 0.011,
        "cg_height": 450,
        "body_style": 10,
        "wheelbase": 2400,
        "front_overhang": 950,
        "rear_overhang": 850,
        "body_width": 1900,
        "overall_height": 1200,
        "beltline_height": 850,
        "ground_clearance": 110,
        "track_front": 1620,
        "track_rear": 1600,
        "rim_diameter": 19,
        "tyre_width": 255,
        "tyre_aspect_ratio": 35,
        "cabin_length": 1700,
        "roof_length": 1000,
        "cabin_offset": -100,
        "vehicle_mass": 1300,
        "front_mass_distribution": 50,
        "haunch": 50,
        "nose_taper": 62,
        "tail_taper": 76,
        "sill_tuck": 70,
        "body_roundness": 65,
        "tumblehome": 150,
    },
    "supercar": {
        "roof_type": 0,
        "roof_rails": 0,
        "rear_spoiler": 3,
        "mirror_type": 0,
        "tow_bar": 0,
        "wheel_design": 3,
        "rim_finish": 4,
        "head_lamp_style": 1,
        "tail_lamp_style": 0,
        "front_suspension": 2,
        "rear_suspension": 3,
        "chassis_type": 1,
        "seat_rows": 1,
        "interior_trim": 2,
        "interior_colour": 5,
        "paint_colour": 8,
        "paint_finish": 1,
        "drag_coefficient": 0.33,
        "rolling_resistance": 0.011,
        "cg_height": 450,
        "body_style": 11,
        "wheelbase": 2650,
        "front_overhang": 1050,
        "rear_overhang": 1000,
        "body_width": 2000,
        "overall_height": 1150,
        "beltline_height": 820,
        "ground_clearance": 110,
        "track_front": 1680,
        "track_rear": 1660,
        "rim_diameter": 20,
        "tyre_width": 275,
        "tyre_aspect_ratio": 30,
        "cabin_length": 1900,
        "roof_length": 1000,
        "cabin_offset": 250,
        "vehicle_mass": 1500,
        "front_mass_distribution": 42,
        "haunch": 70,
        "nose_taper": 56,
        "tail_taper": 80,
        "sill_tuck": 70,
        "body_roundness": 70,
        "tumblehome": 170,
    },
}
# Template values that are typical figures for the class, not data for any vehicle.
TYPICAL_ROAD_LOADS = ("drag_coefficient", "rolling_resistance", "cg_height")
APPEARANCE = ("paint_colour", "paint_finish", "interior_colour")  # template choices
STYLING = (
    "wheel_design", "rim_finish", "head_lamp_style", "tail_lamp_style", "roof_type",
    "roof_rails", "rear_spoiler", "mirror_type", "tow_bar",
)  # fmt: skip
# Wheel travel to the bump stop and tyre-to-arch gap per class, mm (template values; the arch
# gap is kept at least as large as the bump travel so the tyre clears the arch at full bump).
TRAVEL = {
    "city_car": (60, 60),
    "hatchback": (65, 65),
    "sedan": (70, 70),
    "suv": (90, 95),
    "pickup": (100, 105),
    "sports_car": (50, 50),
    "van": (80, 85),
    "box_truck": (100, 105),
    "estate": (70, 70),
    "crossover": (80, 85),
    "mpv": (75, 80),
    "roadster": (50, 50),
    "supercar": (45, 45),
}
# Unsprung mass per corner (front, rear), kg: light cars have light wheels, brakes and beams;
# pickups carry a live rear axle (template values).
UNSPRUNG = {
    "city_car": (32, 30),
    "hatchback": (36, 34),
    "sedan": (42, 42),
    "suv": (50, 52),
    "pickup": (55, 75),
    "sports_car": (38, 40),
    "van": (45, 55),
    "box_truck": (55, 90),
    "estate": (42, 44),
    "crossover": (46, 46),
    "mpv": (44, 48),
    "roadster": (36, 38),
    "supercar": (40, 44),
}
SEAT_ROWS = {
    "2": 1,
    "4": 2,
    "5": 2,
    "7": 3,
}  # two seats per row; the middle rear seat is a bench place
SEAT_CABIN = {"2": 1900, "4": 2300, "5": 2500, "7": 3000}  # cabin length at the beltline, mm
# Target body-bounce (ride) frequencies for the front axle, Hz; the rear is set 10 % higher
# (flat-ride guidance after Olley). Typical published ranges: passenger cars 1.0–1.5 Hz,
# performance cars 1.5–2.0 Hz.
RIDE_FRONT_HZ = {"comfort": 1.1, "balanced": 1.3, "sporty": 1.6}
DAMPING = {"comfort": (0.2, 0.4), "balanced": (0.25, 0.5), "sporty": (0.3, 0.6)}  # bump, rebound
MU = 1.0  # tyre-road friction for the acceleration estimate (dry asphalt)
ETA = 0.9  # drivetrain efficiency for the acceleration estimate
DRIVER_KG = 75.0
PACK_WH_PER_KG = 160.0  # assumed pack-level energy density
BATTERY_SHARE_WARNING = 0.40
CABIN_SHARE_WARNING = 0.72  # all templates with their typical seat counts stay below this


def acceleration_lower_bound(
    power_kw: float, mass_kg: float, driven_share: float
) -> dict[str, float]:
    """0–100 km/h time with no drag, rolling resistance or shifting: traction-limited at
    mu*g*share until the power limit, then constant power. A lower bound, s."""
    v = 100 / 3.6
    m = mass_kg + DRIVER_KG
    a_max = MU * G * driven_share
    p = power_kw * 1000 * ETA
    v_star = p / (m * a_max)
    if v_star >= v:
        return {"time": v / a_max, "traction_limited_until_kmh": 100.0}
    t = v_star / a_max + m * (v * v - v_star * v_star) / (2 * p)
    return {"time": t, "traction_limited_until_kmh": v_star * 3.6}


def _value(spec: VehicleSpec, key: str) -> str | float | None:
    v = spec.get(key)
    return None if v == "skip" else v


def resolved_mass(spec: VehicleSpec) -> float:
    m = _value(spec, "target_mass")
    if isinstance(m, float | int):
        return float(m)
    cls = spec.get("vehicle_class") or "sedan"
    mass = TEMPLATES[str(cls)]["vehicle_mass"]
    if spec.get("powertrain") == "electric":
        mass += 250  # typical extra mass of a battery-electric version (default, labelled)
    return mass


def driven_share(spec: VehicleSpec, front_share: float) -> float:
    drive = spec.get("drivetrain") or "fwd"
    return {"fwd": front_share, "rwd": 1 - front_share, "awd": 1.0}[str(drive)]


def checks(spec: VehicleSpec, generated: Mapping[str, float] | None = None) -> list[Check]:
    out: list[Check] = []
    mass = resolved_mass(spec)
    power = _value(spec, "peak_power")
    target = _value(spec, "accel_0_100")
    front = (generated or {}).get("front_mass_distribution", 55.0) / 100
    if isinstance(power, float | int):
        est = acceleration_lower_bound(float(power), mass, driven_share(spec, front))
        basis = (
            f"traction (mu {MU}, driven-axle static load) then constant power at {ETA:.0%} "
            f"efficiency; {mass:.0f} kg + {DRIVER_KG:.0f} kg driver; no drag, rolling "
            "resistance or shift time, so real times are longer"
        )
        if isinstance(target, float | int):
            if target < est["time"]:
                out.append(
                    Check(
                        id="accel_target",
                        severity="conflict",
                        message=f"0–100 km/h in {target:g} s is not reachable with {power:g} kW "
                        f"and {mass:.0f} kg: even the lower-bound estimate is {est['time']:.1f} s "
                        f"(traction-limited up to {est['traction_limited_until_kmh']:.0f} km/h). "
                        "Raise the power, cut mass, change the drivetrain or relax the target.",
                        basis=basis,
                        answers=["accel_0_100", "peak_power", "target_mass", "drivetrain"],
                        estimate={k: round(v, 3) for k, v in est.items()},
                    )
                )
            else:
                out.append(
                    Check(
                        id="accel_target",
                        severity="info",
                        message=f"0–100 km/h in {target:g} s is not ruled out: the lower bound is "
                        f"{est['time']:.1f} s. It is not claimed as met until the longitudinal "
                        "performance test verifies it (proposed as a requirement).",
                        basis=basis,
                        answers=["accel_0_100", "peak_power"],
                        estimate={k: round(v, 3) for k, v in est.items()},
                    )
                )
        else:
            out.append(
                Check(
                    id="accel_estimate",
                    severity="info",
                    message=f"0–100 km/h lower bound: {est['time']:.1f} s.",
                    basis=basis,
                    answers=["peak_power"],
                    estimate={k: round(v, 3) for k, v in est.items()},
                )
            )
    capacity = _value(spec, "battery_capacity")
    if spec.get("powertrain") == "electric" and isinstance(capacity, float | int):
        pack = capacity * 1000 / PACK_WH_PER_KG
        share = pack / mass
        if pack >= mass:
            sev = "conflict"
        elif share > BATTERY_SHARE_WARNING:
            sev = "warning"
        else:
            sev = "info"
        out.append(
            Check(
                id="battery_mass",
                severity=sev,
                message=f"A {capacity:g} kWh pack is about {pack:.0f} kg, {share:.0%} of the "
                f"{mass:.0f} kg vehicle"
                + (
                    " — more than the whole vehicle."
                    if sev == "conflict"
                    else f" — above the {BATTERY_SHARE_WARNING:.0%} plausibility threshold."
                    if sev == "warning"
                    else "."
                ),
                basis=f"assumed pack-level energy density {PACK_WH_PER_KG:g} Wh/kg",
                answers=["battery_capacity", "target_mass"],
                estimate={"pack_mass": round(pack, 1)},
            )
        )
    if generated is not None:
        share = generated["cabin_length"] / d.overall_length(generated)
        if share > CABIN_SHARE_WARNING:
            out.append(
                Check(
                    id="cabin_share",
                    severity="warning",
                    message=f"The cabin takes {share:.0%} of the body length, leaving little room "
                    "for the powertrain, crash structure and luggage. Choose a longer class or "
                    "fewer seats.",
                    basis=f"cabin above {CABIN_SHARE_WARNING:.0%} of the overall length",
                    answers=["seats", "vehicle_class"],
                    parameters=["cabin_length", "wheelbase"],
                    estimate={"cabin_share": round(share, 3)},
                )
            )
    if spec.get("use") == "off_road" and spec.get("vehicle_class") in (
        "city_car",
        "sports_car",
        "roadster",
        "supercar",
    ):
        out.append(
            Check(
                id="off_road_class",
                severity="warning",
                message="Off-road use with a low-clearance class: the template's "
                "ground clearance is raised to 200 mm, check the packaging.",
                basis="class templates",
                answers=["use", "vehicle_class"],
            )
        )
    return out


# --- Generation --------------------------------------------------------------------------


class Generated(BaseModel):
    values: dict[str, float]
    sources: dict[str, str]  # parameter -> how it was chosen
    violations: list[Violation]
    checks: list[Check]
    requirements: list[dict] = Field(default_factory=list)  # provisional requirement bodies
    missing: list[str] = []  # required questions still unanswered


def _spring_and_damping(values: dict[str, float], ride: str) -> dict[str, tuple[float, str]]:
    out = {}
    f_front = RIDE_FRONT_HZ[ride]
    zb, zr = DAMPING[ride]
    kt = values["tyre_vertical_stiffness"] * 1000
    for axle, f in (("front", f_front), ("rear", f_front * 1.1)):
        m = d.sprung_corner_mass(values, axle)
        k_ride = (2 * math.pi * f) ** 2 * m
        k = k_ride * kt / (kt - k_ride)  # spring in series with the tyre
        crit = 2 * math.sqrt(k * m)
        spec_k = REGISTRY[f"{axle}_spring_rate"]
        k_mm = min(max(round(k / 1000 * 2) / 2, spec_k.min), spec_k.max)
        out[f"{axle}_spring_rate"] = (k_mm, f"{f:.2f} Hz {ride} ride frequency")
        for key, z in (("damping_bump", zb), ("damping_rebound", zr)):
            ps = REGISTRY[f"{axle}_{key}"]
            c = min(max(round(z * crit / 50) * 50, ps.min), ps.max)
            out[f"{axle}_{key}"] = (c, f"{z:.0%} of critical ({ride})")
    return out


def _place_dampers(
    values: dict[str, float], sources: dict[str, str], axle: str, bump: float
) -> None:
    """Choose the stroke and the upper mount height so the damper has room for the bump
    and rebound travel at ride height (with 5 mm to spare at each end)."""
    rebound = bump + 10.0
    stroke = bump + rebound + 10.0
    lower = d.tyre_radius(values) + d.AXLE_RADIUS
    length = stroke + d.DAMPER_DEAD_LENGTH + bump + 5.0  # compression room = bump + 5
    values[f"{axle}_bump_travel"] = bump
    values[f"{axle}_rebound_travel"] = rebound
    values[f"{axle}_damper_stroke"] = stroke
    values[f"{axle}_shock_mount_height"] = round(lower + length, 0)
    why = f"damper centred for {bump:g} mm bump and {rebound:g} mm rebound travel"
    for key in ("bump_travel", "rebound_travel", "damper_stroke", "shock_mount_height"):
        sources[f"{axle}_{key}"] = why


def generate(spec: VehicleSpec) -> Generated:
    missing = [
        q.id
        for q in QUESTIONS
        if applicable(q, spec) and not q.optional and q.id not in spec.answers
    ]
    cls = str(spec.get("vehicle_class") or "sedan")
    values = default_values()
    sources = {}
    for k, v in TEMPLATES[cls].items():
        values[k] = v
        sources[k] = (
            f"typical for a {CLASS_LABELS[cls]} (not measured)"
            if k in TYPICAL_ROAD_LOADS
            else f"{CLASS_LABELS[cls]} template colour"
            if k in APPEARANCE
            else f"{CLASS_LABELS[cls]} template styling"
            if k in STYLING
            else f"{CLASS_LABELS[cls]} template"
        )
    if (seats := spec.get("seats")) is not None and seats != "skip":
        values["cabin_length"] = SEAT_CABIN[str(seats)]
        values["seat_rows"] = SEAT_ROWS[str(seats)]
        sources["seat_rows"] = f"{seats} seats"
        values["roof_length"] = min(values["roof_length"], values["cabin_length"] - 400)
        sources["cabin_length"] = f"{seats} seats"
    if spec.get("use") == "off_road":
        values["ground_clearance"] = max(values["ground_clearance"], 200)
        sources["ground_clearance"] = "off-road use"
    if (rim := _value(spec, "rim_diameter")) is not None:
        values["rim_diameter"] = float(rim)
        sources["rim_diameter"] = "specification"
    values["vehicle_mass"] = resolved_mass(spec)
    sources["vehicle_mass"] = (
        "specification"
        if isinstance(_value(spec, "target_mass"), float)
        else f"{CLASS_LABELS[cls]} typical (default)"
    )
    pt_answer = str(spec.get("powertrain") or "petrol")
    if pt_answer in ("electric", "hybrid"):
        values["powertrain_type"] = 2.0 if pt_answer == "electric" else 1.0
        sources["powertrain_type"] = "specification"
        if pt_answer == "electric" and values.get("chassis_type", 0) != 0:
            values["chassis_type"] = 2.0  # skateboard: the battery in the floor
            sources["chassis_type"] = "battery electric: skateboard platform (default)"
        values["battery_capacity"] = 75.0 if pt_answer == "electric" else 14.0
        sources["battery_capacity"] = "typical for the powertrain (default)"
    layout = {("electric", "fwd"): 54, ("electric", "rwd"): 48, ("electric", "awd"): 50}
    pt, drive = str(spec.get("powertrain") or "petrol"), str(spec.get("drivetrain") or "fwd")
    if (pt, drive) in layout:
        values["front_mass_distribution"] = layout[(pt, drive)]
        sources["front_mass_distribution"] = "battery in the floor (default)"
    elif drive == "rwd":
        values["front_mass_distribution"] = min(values["front_mass_distribution"], 52)
        sources["front_mass_distribution"] = "rear-wheel drive layout (default)"
    if isinstance(power := _value(spec, "peak_power"), float | int):
        values["peak_power"] = float(power)
        sources["peak_power"] = "specification"
    values["front_drive_share"] = {"fwd": 100.0, "rwd": 0.0, "awd": 40.0}[drive]
    sources["front_drive_share"] = f"{drive.upper()}" + (
        " (40/60 split suits rearward load transfer)" if drive == "awd" else ""
    )
    for axle, mass in zip(d.AXLES, UNSPRUNG[cls], strict=True):
        values[f"{axle}_unsprung_mass"] = float(mass)
        sources[f"{axle}_unsprung_mass"] = f"{CLASS_LABELS[cls]} template"
    bump, arch = TRAVEL[cls]
    values["arch_clearance"] = float(arch)
    sources["arch_clearance"] = f"{CLASS_LABELS[cls]} template (covers {bump} mm bump travel)"
    for axle in d.AXLES:
        _place_dampers(values, sources, axle, float(bump))
    ride = str(_value(spec, "ride") or ("sporty" if spec.get("use") == "track" else "balanced"))
    for k, (v, why) in _spring_and_damping(values, ride).items():
        values[k] = v
        sources[k] = why
    requirements = [
        {
            "kind": "design",
            "quantity": "front_ride_frequency",
            "comparator": "<=",
            "limit": round(RIDE_FRONT_HZ[ride] * 1.15, 2),
            "approved": False,
            "rationale": f"provisional, from the {ride} ride character",
        }
    ]
    if spec.get("use") == "off_road":
        requirements.append(
            {
                "kind": "design",
                "quantity": "ground_clearance",
                "comparator": ">=",
                "limit": 200,
                "unit": "mm",
                "approved": False,
                "rationale": "provisional, from off-road use",
            }
        )
    if isinstance(target := _value(spec, "accel_0_100"), float | int):
        requirements.append(
            {
                "kind": "performance",
                "test_id": "longitudinal",
                "target": "vehicle",
                "scenario_id": "accel_0_100",
                "metric": "accel_time",
                "comparator": "<=",
                "limit": float(target),
                "approved": False,
                "rationale": "from the specification",
            }
        )
    return Generated(
        values=values,
        sources=sources,
        violations=validate(values),
        checks=checks(spec, values),
        requirements=requirements,
        missing=missing,
    )


# --- Project templates ----------------------------------------------------------------

CLASS_DESCRIPTIONS = {
    "city_car": "Short two-box hatch for town: small wheels, light, front-heavy.",
    "hatchback": "Compact family two-box with a tailgate.",
    "sedan": "Three-box saloon with a separate boot.",
    "suv": "Tall, upright two-box with more ground clearance and wheel travel.",
    "pickup": "Cab and open cargo bed on a long wheelbase, live rear axle masses.",
    "sports_car": "Low fastback coupe, wide and stiff.",
    "van": "One-box people or panel van with a short nose.",
    "box_truck": "Light truck: cab and a separate cargo box, long wheelbase, heavy rear.",
    "estate": "Long-roof two-box with an upright tailgate and roof rails.",
    "crossover": "Raised two-box with a sloping roof and a glass roof.",
    "mpv": "One-box people carrier with three seat rows and a long, raked screen.",
    "roadster": "Open two-seater: long bonnet, short cockpit, boot lip.",
    "supercar": "Mid-engine wedge: low nose, cab-forward canopy, wide haunches, wing.",
}


def template_values(cls: str) -> dict[str, float]:
    """The design the specification interview generates for a class with defaults only."""
    spec = VehicleSpec()
    spec.set("vehicle_class", cls, source="default")
    return generate(spec).values


def project_templates() -> list[Template]:
    return [
        Template(
            id=cls,
            label=label[0].upper() + label[1:],
            description=CLASS_DESCRIPTIONS[cls],
            values=lambda cls=cls: template_values(cls),
        )
        for cls, label in CLASS_LABELS.items()
    ]
