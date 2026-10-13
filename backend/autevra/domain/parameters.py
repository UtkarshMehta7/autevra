"""Parameter registry: every editable design parameter, its unit and bounds.

The registry is the single list of parameter IDs. The command system, the
intent parser, the API and (later) the LLM schema are all derived from it.
"""

from collections.abc import Mapping
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from autevra.domain.units import Unit


class Group(StrEnum):
    DIMENSIONS = "dimensions"
    CABIN = "cabin"
    WHEELS = "wheels"
    STEERING = "steering"
    FRAME = "frame"


class ParameterDef(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    group: Group
    unit: Unit
    default: float
    min: float
    max: float
    step: float = 1.0
    description: str = ""
    aliases: tuple[str, ...] = Field(default=())
    increase_words: tuple[str, ...] = Field(default=())
    decrease_words: tuple[str, ...] = Field(default=())


def _p(**kwargs: object) -> ParameterDef:
    return ParameterDef.model_validate(kwargs)


_DEFINITIONS: tuple[ParameterDef, ...] = (
    # --- Dimensions ---
    _p(
        id="wheelbase",
        label="Wheelbase",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=2700,
        min=2000,
        max=3600,
        step=10,
        description="Distance between front and rear axle centres.",
        aliases=("wheelbase", "wheel base", "axle distance", "axle spacing"),
    ),
    _p(
        id="front_overhang",
        label="Front overhang",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=900,
        min=500,
        max=1400,
        step=10,
        description="Distance from the front axle to the front of the body.",
        aliases=("front overhang", "nose length", "front overhang length"),
    ),
    _p(
        id="rear_overhang",
        label="Rear overhang",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=1000,
        min=500,
        max=1500,
        step=10,
        description="Distance from the rear axle to the rear of the body.",
        aliases=("rear overhang", "tail length", "rear overhang length"),
    ),
    _p(
        id="body_width",
        label="Body width",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=1820,
        min=1500,
        max=2200,
        step=10,
        description="Overall width of the body, excluding mirrors.",
        aliases=("body width", "width", "overall width", "car width", "vehicle width"),
        increase_words=("wider", "widen", "broaden"),
        decrease_words=("narrower", "narrow"),
    ),
    _p(
        id="overall_height",
        label="Overall height",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=1450,
        min=1100,
        max=2100,
        step=10,
        description="Height of the roof above the ground.",
        aliases=("overall height", "height", "roof height", "car height", "vehicle height"),
        increase_words=("taller",),
        decrease_words=("shorter in height",),
    ),
    _p(
        id="beltline_height",
        label="Beltline height",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=960,
        min=700,
        max=1400,
        step=10,
        description="Height of the top of the lower body (bottom of the windows).",
        aliases=("beltline height", "beltline", "belt line", "waistline", "shoulder line"),
    ),
    _p(
        id="ground_clearance",
        label="Ground clearance",
        group=Group.DIMENSIONS,
        unit=Unit.MM,
        default=160,
        min=90,
        max=350,
        step=5,
        description="Distance from the ground to the lowest point of the chassis.",
        aliases=("ground clearance", "ride height", "clearance"),
        increase_words=("raise", "lift"),
        decrease_words=("lower", "drop"),
    ),
    # --- Cabin ---
    _p(
        id="cabin_length",
        label="Cabin length",
        group=Group.CABIN,
        unit=Unit.MM,
        default=2500,
        min=1200,
        max=4200,
        step=10,
        description="Length of the greenhouse measured at the beltline.",
        aliases=("cabin length", "cabin", "greenhouse length", "greenhouse"),
    ),
    _p(
        id="roof_length",
        label="Roof length",
        group=Group.CABIN,
        unit=Unit.MM,
        default=1500,
        min=600,
        max=3800,
        step=10,
        description="Length of the flat roof panel.",
        aliases=("roof length", "roof"),
    ),
    _p(
        id="cabin_offset",
        label="Cabin fore/aft offset",
        group=Group.CABIN,
        unit=Unit.MM,
        default=-150,
        min=-900,
        max=900,
        step=10,
        description="Shift of the cabin centre from the body centre (positive = forward).",
        aliases=("cabin offset", "cabin position", "greenhouse offset"),
    ),
    # --- Wheels and tyres ---
    _p(
        id="track_front",
        label="Front track",
        group=Group.WHEELS,
        unit=Unit.MM,
        default=1560,
        min=1200,
        max=1900,
        step=5,
        description="Distance between the front tyre centre planes.",
        aliases=("front track", "front track width", "front wheel track"),
    ),
    _p(
        id="track_rear",
        label="Rear track",
        group=Group.WHEELS,
        unit=Unit.MM,
        default=1560,
        min=1200,
        max=1900,
        step=5,
        description="Distance between the rear tyre centre planes.",
        aliases=("rear track", "rear track width", "rear wheel track"),
    ),
    _p(
        id="rim_diameter",
        label="Rim diameter",
        group=Group.WHEELS,
        unit=Unit.IN,
        default=17,
        min=13,
        max=22,
        step=1,
        description="Nominal rim (wheel) diameter.",
        aliases=(
            "rim diameter",
            "rim size",
            "rims",
            "rim",
            "wheel size",
            "wheel diameter",
            "alloys",
        ),
    ),
    _p(
        id="tyre_width",
        label="Tyre width",
        group=Group.WHEELS,
        unit=Unit.MM,
        default=225,
        min=145,
        max=335,
        step=5,
        description="Nominal section width of the tyre.",
        aliases=("tyre width", "tire width", "tyre section width", "tire section width"),
    ),
    _p(
        id="tyre_aspect_ratio",
        label="Tyre aspect ratio",
        group=Group.WHEELS,
        unit=Unit.PERCENT,
        default=50,
        min=25,
        max=80,
        step=5,
        description="Sidewall height as a percentage of section width.",
        aliases=(
            "tyre aspect ratio",
            "tire aspect ratio",
            "aspect ratio",
            "tyre profile",
            "tire profile",
            "profile",
            "sidewall",
        ),
    ),
    _p(
        id="arch_clearance",
        label="Wheel arch clearance",
        group=Group.WHEELS,
        unit=Unit.MM,
        default=35,
        min=15,
        max=120,
        step=5,
        description="Radial gap between the tyre and the wheel arch.",
        aliases=("wheel arch clearance", "arch clearance", "arch gap", "wheel arch gap"),
    ),
    # --- Steering ---
    _p(
        id="max_steer_angle",
        label="Max steer angle",
        group=Group.STEERING,
        unit=Unit.DEG,
        default=35,
        min=20,
        max=45,
        step=1,
        description="Maximum road-wheel steer angle at full lock.",
        aliases=("max steer angle", "steer angle", "steering angle", "steering lock", "lock"),
    ),
    # --- Chassis frame ---
    _p(
        id="rail_spacing",
        label="Rail spacing",
        group=Group.FRAME,
        unit=Unit.MM,
        default=900,
        min=600,
        max=1300,
        step=10,
        description="Centre-to-centre distance between the ladder frame rails.",
        aliases=("rail spacing", "frame width", "rail distance", "frame rail spacing"),
    ),
    _p(
        id="rail_width",
        label="Rail section width",
        group=Group.FRAME,
        unit=Unit.MM,
        default=70,
        min=40,
        max=150,
        step=5,
        description="Outer width of the rectangular rail section.",
        aliases=("rail width", "rail section width", "frame rail width"),
    ),
    _p(
        id="rail_height",
        label="Rail section height",
        group=Group.FRAME,
        unit=Unit.MM,
        default=110,
        min=60,
        max=250,
        step=5,
        description="Outer height of the rectangular rail section.",
        aliases=("rail height", "rail section height", "frame rail height", "rail depth"),
    ),
    _p(
        id="rail_wall",
        label="Rail wall thickness",
        group=Group.FRAME,
        unit=Unit.MM,
        default=4,
        min=2,
        max=10,
        step=0.5,
        description="Wall thickness of the hollow rail section.",
        aliases=(
            "rail wall thickness",
            "rail wall",
            "wall thickness",
            "rail thickness",
            "frame thickness",
        ),
    ),
)

REGISTRY: Mapping[str, ParameterDef] = {d.id: d for d in _DEFINITIONS}

# Group aliases: one word that addresses several parameters at once.
GROUP_ALIASES: Mapping[str, tuple[str, ...]] = {
    "track": ("track_front", "track_rear"),
    "track width": ("track_front", "track_rear"),
    "wheel track": ("track_front", "track_rear"),
    "overhangs": ("front_overhang", "rear_overhang"),
}


def get(parameter_id: str) -> ParameterDef:
    try:
        return REGISTRY[parameter_id]
    except KeyError:
        raise KeyError(f"unknown parameter '{parameter_id}'") from None


def default_values() -> dict[str, float]:
    return {d.id: d.default for d in _DEFINITIONS}
