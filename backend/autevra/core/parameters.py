"""Parameter registry: every editable design parameter, its unit and bounds.

The registry is the single list of parameter IDs. The command system, the
intent parser, the API and (later) the LLM schema are all derived from it.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from autevra.core.units import Unit


class Group(StrEnum):
    DIMENSIONS = "dimensions"
    CABIN = "cabin"
    WHEELS = "wheels"
    STEERING = "steering"
    FRAME = "frame"
    SUSPENSION = "suspension"
    MASS = "mass"
    POWERTRAIN = "powertrain"


class ParameterDef(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    label: str
    group: Group | str  # plugins may add groups
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


# --- Suspension (per axle) ---
# Starting values of the template, not measurements: with the tyre in series the rates
# give ride frequencies of about 1.2 Hz (front) and 1.3 Hz (rear); damping is about 25 %
# (bump) and 50 % (rebound) of critical. Rates and damping are at the wheel: the dampers
# stand vertically over a beam axle, so the motion ratio is 1 in heave.
def _axle_suspension(axle: str, rate: float, bump: float, rebound: float, unsprung: float):
    a, A = axle, axle.capitalize()  # noqa: N806
    return (
        _p(
            id=f"{a}_spring_rate", label=f"{A} spring rate", group=Group.SUSPENSION,
            unit=Unit.N_PER_MM, default=rate, min=5, max=150, step=0.5,
            description=f"{A} wheel rate of the coil spring (force per wheel travel).",
            aliases=(f"{a} spring rate", f"{a} springs", f"{a} spring", f"{a} spring stiffness",
                     f"{a} wheel rate"),
        ),
        _p(
            id=f"{a}_damping_bump", label=f"{A} bump damping", group=Group.SUSPENSION,
            unit=Unit.NS_PER_M, default=bump, min=200, max=10000, step=50,
            description=f"{A} damper coefficient in compression (bump), at the wheel.",
            aliases=(f"{a} bump damping", f"{a} compression damping", f"{a} bump",
                     f"{a} compression"),
        ),
        _p(
            id=f"{a}_damping_rebound", label=f"{A} rebound damping", group=Group.SUSPENSION,
            unit=Unit.NS_PER_M, default=rebound, min=200, max=15000, step=50,
            description=f"{A} damper coefficient in extension (rebound), at the wheel.",
            aliases=(f"{a} rebound damping", f"{a} rebound", f"{a} extension damping"),
        ),
        _p(
            id=f"{a}_unsprung_mass", label=f"{A} unsprung mass", group=Group.SUSPENSION,
            unit=Unit.KG, default=unsprung, min=15, max=150, step=1,
            description=f"Unsprung mass per {a} corner: wheel, tyre, brake and half the axle.",
            aliases=(f"{a} unsprung mass", f"{a} unsprung weight"),
        ),
        _p(
            id=f"{a}_bump_travel", label=f"{A} bump travel", group=Group.SUSPENSION,
            unit=Unit.MM, default=60, min=20, max=200, step=5,
            description=f"{A} wheel travel in compression from ride height to the bump stop.",
            aliases=(f"{a} bump travel", f"{a} compression travel", f"{a} jounce travel"),
        ),
        _p(
            id=f"{a}_rebound_travel", label=f"{A} rebound travel", group=Group.SUSPENSION,
            unit=Unit.MM, default=70, min=20, max=200, step=5,
            description=f"{A} wheel travel in extension from ride height to full droop.",
            aliases=(f"{a} rebound travel", f"{a} droop travel", f"{a} droop"),
        ),
        _p(
            id=f"{a}_damper_stroke", label=f"{A} damper stroke", group=Group.SUSPENSION,
            unit=Unit.MM, default=140, min=60, max=300, step=5,
            description=f"Total stroke of the {a} dampers (fully compressed to fully extended).",
            aliases=(f"{a} damper stroke", f"{a} shock stroke", f"{a} shock absorber stroke"),
        ),
        _p(
            id=f"{a}_shock_mount_height", label=f"{A} upper shock mount height",
            group=Group.SUSPENSION, unit=Unit.MM, default=670, min=400, max=1100, step=5,
            description=f"Height above the ground of the {a} upper damper mounts on the body.",
            aliases=(f"{a} shock mount height", f"{a} upper mount height",
                     f"{a} shock tower height", f"{a} damper mount height"),
        ),
    )  # fmt: skip


_DEFINITIONS += (
    *_axle_suspension("front", rate=26, bump=1500, rebound=3000, unsprung=45),
    *_axle_suspension("rear", rate=24, bump=1300, rebound=2600, unsprung=55),
    _p(
        id="tyre_vertical_stiffness", label="Tyre vertical stiffness", group=Group.SUSPENSION,
        unit=Unit.N_PER_MM, default=200, min=80, max=600, step=5,
        description="Radial (vertical) stiffness of one tyre.",
        aliases=("tyre vertical stiffness", "tyre stiffness", "vertical tyre stiffness",
                 "tyre spring rate", "tyre rate"),
    ),
    _p(
        id="damper_body_diameter", label="Damper body diameter", group=Group.SUSPENSION,
        unit=Unit.MM, default=50, min=30, max=90, step=1,
        description="Outer diameter of the damper body tube.",
        aliases=("damper body diameter", "damper diameter", "shock diameter",
                 "shock body diameter"),
    ),
    _p(
        id="spring_coil_diameter", label="Spring mean coil diameter", group=Group.SUSPENSION,
        unit=Unit.MM, default=100, min=60, max=200, step=1,
        description="Mean diameter of the coil springs (the wire diameter follows from the rate).",
        aliases=("spring coil diameter", "coil diameter", "spring diameter",
                 "mean coil diameter"),
    ),
    # --- Mass ---
    _p(
        id="vehicle_mass", label="Vehicle mass", group=Group.MASS,
        unit=Unit.KG, default=1600, min=600, max=4000, step=10,
        description="Total vehicle mass in the test condition (kerb mass plus load).",
        aliases=("vehicle mass", "kerb mass", "curb mass", "kerb weight", "curb weight",
                 "vehicle weight", "car weight", "mass", "weight"),
        increase_words=("heavier",), decrease_words=("lighter",),
    ),
    _p(
        id="front_mass_distribution", label="Front mass distribution", group=Group.MASS,
        unit=Unit.PERCENT, default=55, min=30, max=70, step=1,
        description="Share of the vehicle mass carried by the front axle.",
        aliases=("front mass distribution", "front weight distribution", "weight distribution",
                 "mass distribution", "weight balance", "front weight"),
    ),
)  # fmt: skip

# --- Powertrain and road loads (used by the longitudinal test) ---
_DEFINITIONS += (
    _p(
        id="peak_power", label="Peak power", group=Group.POWERTRAIN,
        unit=Unit.KW, default=150, min=20, max=1000, step=5,
        description="Peak power of the engine or motors.",
        aliases=("peak power", "power", "engine power", "motor power", "power output",
                 "horsepower"),
        increase_words=("faster", "quicker", "more powerful"),
        decrease_words=("slower", "less powerful"),
    ),
    _p(
        id="front_drive_share", label="Front drive torque share", group=Group.POWERTRAIN,
        unit=Unit.PERCENT, default=0, min=0, max=100, step=5,
        description="Share of drive torque at the front axle: 0 = rear-wheel drive, "
        "100 = front-wheel drive, in between = all-wheel drive.",
        aliases=("front drive share", "front drive torque share", "torque split",
                 "drive split", "front torque share"),
    ),
    _p(
        id="drivetrain_efficiency", label="Drivetrain efficiency", group=Group.POWERTRAIN,
        unit=Unit.PERCENT, default=90, min=50, max=99, step=1,
        description="Power reaching the wheels as a share of peak power.",
        aliases=("drivetrain efficiency", "transmission efficiency", "driveline efficiency"),
    ),
    _p(
        id="drag_coefficient", label="Drag coefficient", group=Group.POWERTRAIN,
        unit=Unit.NONE, default=0.32, min=0.15, max=0.8, step=0.01,
        description="Aerodynamic drag coefficient Cd (with the frontal area gives the drag area).",
        aliases=("drag coefficient", "cd", "cx", "aero drag coefficient"),
    ),
    _p(
        id="rolling_resistance", label="Rolling resistance coefficient",
        group=Group.POWERTRAIN, unit=Unit.NONE, default=0.012, min=0.005, max=0.03,
        step=0.001, description="Tyre rolling resistance force per unit weight (Crr).",
        aliases=("rolling resistance", "rolling resistance coefficient", "crr"),
    ),
    _p(
        id="cg_height", label="Centre of gravity height", group=Group.MASS,
        unit=Unit.MM, default=550, min=300, max=1200, step=10,
        description="Height of the centre of gravity above the ground (load transfer).",
        aliases=("centre of gravity height", "center of gravity height", "cg height",
                 "cog height", "centre of gravity", "center of gravity"),
    ),
)  # fmt: skip

REGISTRY: dict[str, ParameterDef] = {d.id: d for d in _DEFINITIONS}  # extensible

# Group aliases: one word that addresses several parameters at once.
GROUP_ALIASES: dict[str, tuple[str, ...]] = {
    "track": ("track_front", "track_rear"),
    "track width": ("track_front", "track_rear"),
    "wheel track": ("track_front", "track_rear"),
    "overhangs": ("front_overhang", "rear_overhang"),
    "spring rate": ("front_spring_rate", "rear_spring_rate"),
    "spring rates": ("front_spring_rate", "rear_spring_rate"),
    "springs": ("front_spring_rate", "rear_spring_rate"),
    "spring stiffness": ("front_spring_rate", "rear_spring_rate"),
    "wheel rate": ("front_spring_rate", "rear_spring_rate"),
    "bump damping": ("front_damping_bump", "rear_damping_bump"),
    "compression damping": ("front_damping_bump", "rear_damping_bump"),
    "rebound damping": ("front_damping_rebound", "rear_damping_rebound"),
    "unsprung mass": ("front_unsprung_mass", "rear_unsprung_mass"),
    "bump travel": ("front_bump_travel", "rear_bump_travel"),
    "rebound travel": ("front_rebound_travel", "rear_rebound_travel"),
    "damper stroke": ("front_damper_stroke", "rear_damper_stroke"),
    **{
        alias: ("front_damping_bump", "front_damping_rebound", "rear_damping_bump",
                "rear_damping_rebound")
        for alias in ("damping", "dampers", "damper damping", "shock absorbers",
                      "shock absorber damping", "shock damping", "shocks", "damper")
    },
    **{
        f"{axle} {alias}": (f"{axle}_damping_bump", f"{axle}_damping_rebound")
        for axle in ("front", "rear")
        for alias in ("damping", "dampers", "damper", "damper damping", "shocks",
                      "shock absorbers", "shock absorber", "shock absorber damping",
                      "shock damping")
    },
}  # fmt: skip


def get(parameter_id: str) -> ParameterDef:
    try:
        return REGISTRY[parameter_id]
    except KeyError:
        raise KeyError(f"unknown parameter '{parameter_id}'") from None


def default_values() -> dict[str, float]:
    return {d.id: d.default for d in REGISTRY.values()}
