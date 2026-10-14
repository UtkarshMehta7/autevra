"""The automotive vehicle assembly: components, interfaces, mates and coincidences.

Each component declares the parameters its geometry depends on (``geometry``)
and, per interface, the parameters that interface frame depends on (``frames``). Input and
interface functions receive a view of the design that contains **only** the
declared parameters, so an undeclared dependency fails loudly instead of
silently breaking selective rebuilds.
"""

from collections.abc import Callable, Mapping

from autevra.assembly import transforms as tf
from autevra.assembly.model import Coincidence, ComponentDef, Mate
from autevra.assembly.transforms import Matrix
from autevra.domains.automotive import derived as d

Values = Mapping[str, float]

TYRE = ("rim_diameter", "tyre_width", "tyre_aspect_ratio")


BODY_GEOMETRY = (
    "body_style", "wheelbase", "front_overhang", "rear_overhang", "body_width", "overall_height",
    "beltline_height", "ground_clearance", "rail_height", "cabin_length", "roof_length",
    "cabin_offset", "track_front", "track_rear", "arch_clearance", *TYRE, *d.CHASSIS_INPUTS,
    "head_lamp_style", "tail_lamp_style",  # the body is recessed for the lamps
)  # fmt: skip


# The glazing follows the greenhouse only: not the wheels, arches or track.
GLASS_GEOMETRY = (
    "body_style", "wheelbase", "front_overhang", "rear_overhang", "body_width",
    "overall_height", "beltline_height", "ground_clearance", "rail_height", "cabin_length",
    "roof_length", "cabin_offset", *d.CHASSIS_INPUTS,
)  # fmt: skip


def _glass_inputs(p: Values) -> dict[str, float]:
    return {k: p[k] for k in dict.fromkeys(GLASS_GEOMETRY)} | {"body_floor": d.body_floor_height(p)}


# Interior parts follow the cabin (greenhouse) plus their own choices.
INTERIOR_GEOMETRY = (*GLASS_GEOMETRY, "seat_rows", "interior_trim", "driving_side")


def _interior_inputs(p: Values) -> dict[str, float]:
    return {k: p[k] for k in INTERIOR_GEOMETRY} | {"body_floor": d.body_floor_height(p)}


# Powertrain and electrical equipment follow the chassis, the drive layout and the tyres.
POWERTRAIN_GEOMETRY = (
    *d.CHASSIS_INPUTS, "front_overhang", "rear_overhang", "beltline_height", "front_drive_share",
    "engine_cylinders", *TYRE,
)  # fmt: skip


def _powertrain_inputs(p: Values) -> dict[str, float]:
    keys = dict.fromkeys(k for k in POWERTRAIN_GEOMETRY if k not in TYRE)
    return {k: p[k] for k in keys} | {
        "tyre_radius": d.tyre_radius(p), "body_floor": d.body_floor_height(p),
    }  # fmt: skip


def _equipment(cid: str, name: str, category: str, color: tuple[float, float, float],
               finish: str) -> ComponentDef:  # fmt: skip
    return ComponentDef(
        id=cid, name=name, category=category, builder=cid,
        geometry=POWERTRAIN_GEOMETRY, inputs=_powertrain_inputs,
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=color, finish=finish,
    )  # fmt: skip


EQUIPMENT = (
    ("engine", "Engine", "powertrain", (0.24, 0.25, 0.27), "metal"),
    ("gearbox", "Gearbox", "powertrain", (0.32, 0.33, 0.35), "metal"),
    ("fuel_tank", "Fuel tank", "powertrain", (0.06, 0.06, 0.07), "trim"),
    ("exhaust", "Exhaust", "powertrain", (0.42, 0.39, 0.36), "metal"),
    ("radiator", "Cooling module", "powertrain", (0.14, 0.15, 0.17), "metal"),
    ("traction_battery", "Traction battery", "electrical", (0.08, 0.13, 0.24), "metal"),
    ("front_motor", "Front e-motor", "powertrain", (0.55, 0.56, 0.58), "metal"),
    ("rear_motor", "Rear e-motor", "powertrain", (0.55, 0.56, 0.58), "metal"),
    ("inverters", "Inverters", "electrical", (0.34, 0.35, 0.37), "metal"),
    ("charger", "On-board charger and DC-DC", "electrical", (0.29, 0.30, 0.32), "metal"),
    ("charge_port", "Charge port", "electrical", (0.04, 0.04, 0.045), "trim"),
    ("hv_cables", "High-voltage cables", "electrical", (0.95, 0.33, 0.02), "rubber"),
    ("battery_12v", "12 V battery", "electrical", (0.05, 0.05, 0.06), "trim"),
    ("ecus", "Control units", "electrical", (0.10, 0.12, 0.14), "metal"),
    ("harness", "Wiring harness", "electrical", (0.03, 0.03, 0.03), "rubber"),
)


# Interior colour palette, in the order of the ``interior_colour`` options.
UPHOLSTERY = (
    (0.035, 0.036, 0.04), (0.28, 0.28, 0.27), (0.62, 0.56, 0.44), (0.42, 0.24, 0.11),
    (0.30, 0.11, 0.04), (0.22, 0.02, 0.03),
)  # fmt: skip
_TRIM_FINISH = ("fabric", "leather", "leather")


def _upholstery(p: Values) -> tuple[tuple[float, float, float], str]:
    colour = UPHOLSTERY[min(max(int(round(p["interior_colour"])), 0), len(UPHOLSTERY) - 1)]
    return colour, _TRIM_FINISH[min(max(int(round(p["interior_trim"])), 0), 2)]


def _interior(cid: str, name: str, builder: str, color: tuple[float, float, float],
              finish: str, **extra: object) -> ComponentDef:  # fmt: skip
    return ComponentDef(
        id=cid, name=name, category="interior", builder=builder,
        geometry=INTERIOR_GEOMETRY, inputs=_interior_inputs,
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=color, finish=finish, **extra,  # type: ignore[arg-type]
    )  # fmt: skip


def _body_inputs(p: Values) -> dict[str, float]:
    keys = list(dict.fromkeys(k for k in BODY_GEOMETRY if k not in TYRE))
    return {k: p[k] for k in keys} | {
        "body_floor": d.body_floor_height(p),
        "tyre_width": p["tyre_width"],
        "tyre_radius": d.tyre_radius(p),
        "arch_radius": d.arch_radius(p),
    }


FRAME_GEOMETRY = (
    "wheelbase", "front_overhang", "rear_overhang", "rail_spacing", "rail_width",
    "rail_height", "rail_wall", "ground_clearance", *d.CHASSIS_INPUTS,
)  # fmt: skip


def _wheel_inputs(p: Values) -> dict[str, float]:
    return {
        "tyre_radius": d.tyre_radius(p),
        "rim_radius": d.rim_diameter_mm(p) / 2.0,
        "tyre_width": p["tyre_width"],
    }


def _vehicle_interfaces(p: Values) -> dict[str, Matrix]:
    z = d.tyre_radius(p)  # wheel centre height (unloaded tyre)
    return {
        "origin": tf.identity(),
        "front_axle_mount": tf.translation(0.0, 0.0, z),
        "rear_axle_mount": tf.translation(-p["wheelbase"], 0.0, z),
    }


def _axle_interfaces(track_param: str) -> Callable[[Values], dict[str, Matrix]]:
    def interfaces(p: Values) -> dict[str, Matrix]:
        half = p[track_param] / 2.0
        shock_y = p["rail_spacing"] / 2.0  # dampers stand over the frame rail lines
        return {
            "centre": tf.identity(),
            "hub_left": tf.translation(0.0, half, 0.0),
            # Right hub faces outward along -Y: the wheel is turned 180 degrees about Z.
            "hub_right": tf.compose(tf.translation(0.0, -half, 0.0), tf.rotation_z(180.0)),
            "shock_left": tf.translation(0.0, shock_y, d.AXLE_RADIUS),
            "shock_right": tf.translation(0.0, -shock_y, d.AXLE_RADIUS),
        }

    return interfaces


SHOCK_TOWERS = {  # body interface -> (axle, side)
    "shock_tower_fl": ("front", 1.0),
    "shock_tower_fr": ("front", -1.0),
    "shock_tower_rl": ("rear", 1.0),
    "shock_tower_rr": ("rear", -1.0),
}


def _body_interfaces(p: Values) -> dict[str, Matrix]:
    """Origin plus the upper damper mounts (shock towers) built into the body."""
    out = {"origin": tf.identity()}
    for name, (axle, side) in SHOCK_TOWERS.items():
        x = 0.0 if axle == "front" else -p["wheelbase"]
        out[name] = tf.translation(
            x, side * p["rail_spacing"] / 2.0, p[f"{axle}_shock_mount_height"]
        )
    return out


def _damper_geometry(axle: str) -> tuple[str, ...]:
    return (
        f"{axle}_shock_mount_height", *TYRE, f"{axle}_damper_stroke", "damper_body_diameter",
        "spring_coil_diameter", f"{axle}_spring_rate",
    )  # fmt: skip


def _damper_inputs(axle: str) -> Callable[[Values], dict[str, float]]:
    def inputs(p: Values) -> dict[str, float]:
        return {
            "length": d.damper_installed_length(p, axle),
            "stroke": p[f"{axle}_damper_stroke"],
            "body_diameter": p["damper_body_diameter"],
            "coil_diameter": p["spring_coil_diameter"],
            "wire_diameter": round(d.spring_wire_diameter(p, axle), 3),
        }

    return inputs


def _damper_interfaces(axle: str) -> Callable[[Values], dict[str, Matrix]]:
    def interfaces(p: Values) -> dict[str, Matrix]:
        return {
            "lower_eye": tf.identity(),
            "upper_eye": tf.translation(0.0, 0.0, d.damper_installed_length(p, axle)),
        }

    return interfaces


def _hub(p: Values) -> dict[str, Matrix]:
    return {"hub": tf.identity()}


_BODY_COLOR = (0.62, 0.70, 0.80)
# Paint palette, in the order of the ``paint_colour`` options (linear RGB for the viewer).
PAINT = (
    (0.86, 0.87, 0.88), (0.55, 0.57, 0.60), (0.16, 0.17, 0.19), (0.02, 0.022, 0.025),
    (0.55, 0.02, 0.025), (0.02, 0.06, 0.22), (0.02, 0.22, 0.70), (0.02, 0.10, 0.05),
    (0.80, 0.18, 0.02), (0.88, 0.58, 0.02), (0.60, 0.48, 0.32), (0.22, 0.12, 0.06),
)  # fmt: skip
PAINT_FINISHES = ("gloss", "metallic", "matte", "pearl")


def _paint(p: Values) -> tuple[tuple[float, float, float], str]:
    colour = PAINT[min(max(int(round(p["paint_colour"])), 0), len(PAINT) - 1)]
    finish = PAINT_FINISHES[min(max(int(round(p["paint_finish"])), 0), len(PAINT_FINISHES) - 1)]
    return colour, f"paint_{finish}"


_FRAME_COLOR = (0.30, 0.32, 0.36)
_GLASS_COLOR = (0.08, 0.11, 0.15)
_HEAD_LAMP_COLOR = (0.93, 0.92, 0.82)
_TAIL_LAMP_COLOR = (0.72, 0.08, 0.08)
_AXLE_COLOR = (0.45, 0.45, 0.48)
_WHEEL_COLOR = (0.12, 0.12, 0.13)
_DAMPER_COLOR = (0.85, 0.55, 0.12)


def _wheel(cid: str, name: str, axle: str, side: str) -> ComponentDef:
    return ComponentDef(
        id=cid, name=name, category="wheel", builder="wheel",
        geometry=TYRE, inputs=_wheel_inputs,
        frames={"hub": ()}, interfaces=_hub,
        mate=Mate(axle, f"hub_{side}", "hub"), color=_WHEEL_COLOR, finish="rubber",
    )  # fmt: skip


RIM_GEOMETRY = (*TYRE, "wheel_design")
RIM_FINISHES = (
    ((0.72, 0.73, 0.75), "metal"), ((0.26, 0.27, 0.29), "metal"),
    ((0.025, 0.025, 0.03), "paint_gloss"), ((0.86, 0.87, 0.88), "polished"),
    ((0.42, 0.30, 0.16), "paint_metallic"), ((0.88, 0.88, 0.87), "paint_gloss"),
)  # fmt: skip


def _rim_finish(p: Values) -> tuple[tuple[float, float, float], str]:
    return RIM_FINISHES[min(max(int(round(p["rim_finish"])), 0), len(RIM_FINISHES) - 1)]


def _rim_inputs(p: Values) -> dict[str, float]:
    return _wheel_inputs(p) | {"wheel_design": p["wheel_design"]}


def _rim(cid: str, name: str, axle: str, side: str) -> ComponentDef:
    return ComponentDef(
        id=cid, name=name, category="wheel", builder="rim",
        geometry=RIM_GEOMETRY, inputs=_rim_inputs,
        frames={"hub": ()}, interfaces=_hub,
        mate=Mate(axle, f"hub_{side}", "hub"), color=RIM_FINISHES[0][0], finish="metal",
        appearance=_rim_finish, appearance_inputs=("rim_finish",),
    )  # fmt: skip


def _damper(cid: str, name: str, axle: str, side: str) -> ComponentDef:
    upper = (f"{axle}_shock_mount_height", *TYRE)
    return ComponentDef(
        id=cid, name=name, category="suspension", builder="damper",
        geometry=_damper_geometry(axle), inputs=_damper_inputs(axle),
        frames={"lower_eye": (), "upper_eye": upper}, interfaces=_damper_interfaces(axle),
        mate=Mate(f"{axle}_axle", f"shock_{side}", "lower_eye"), color=_DAMPER_COLOR,
        finish="metal",
    )  # fmt: skip


def _axle(cid: str, name: str, track: str, mount: str) -> ComponentDef:
    axle = 0.0 if cid.startswith("front") else 1.0
    kind = "front_suspension" if axle == 0.0 else "rear_suspension"
    return ComponentDef(
        id=cid, name=name, category="axle", builder="axle",
        geometry=(track, kind, "rail_spacing"),
        inputs=lambda p: {"track": p[track], "suspension": p[kind], "axle": axle,
                          "rail_spacing": p["rail_spacing"]},  # fmt: skip
        frames={"centre": (), "hub_left": (track,), "hub_right": (track,),
                "shock_left": ("rail_spacing",), "shock_right": ("rail_spacing",)},
        interfaces=_axle_interfaces(track),
        mate=Mate("vehicle", mount, "centre"), color=_AXLE_COLOR, finish="metal",
    )  # fmt: skip


COMPONENTS: tuple[ComponentDef, ...] = (
    ComponentDef(
        id="vehicle", name="Vehicle", category="assembly", builder=None,
        frames={"origin": (), "front_axle_mount": TYRE,
                "rear_axle_mount": ("wheelbase", *TYRE)},
        interfaces=_vehicle_interfaces,
    ),
    ComponentDef(
        id="body", name="Body", category="body", builder="body",
        geometry=BODY_GEOMETRY, inputs=_body_inputs,
        frames={"origin": (),
                **{name: ("wheelbase", "rail_spacing", f"{axle}_shock_mount_height")
                   for name, (axle, _) in SHOCK_TOWERS.items()}},
        interfaces=_body_interfaces,
        mate=Mate("vehicle", "origin", "origin"), color=_BODY_COLOR,
        appearance=_paint, appearance_inputs=("paint_colour", "paint_finish"),
    ),
    ComponentDef(
        id="glass", name="Glazing", category="body", builder="glass",
        geometry=GLASS_GEOMETRY, inputs=_glass_inputs,
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=_GLASS_COLOR, finish="glass",
    ),
    ComponentDef(
        id="head_lamps", name="Head lamps", category="body", builder="head_lamps",
        geometry=BODY_GEOMETRY, inputs=_body_inputs,  # on the body faces
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=_HEAD_LAMP_COLOR,
        finish="lamp",
    ),
    ComponentDef(
        id="tail_lamps", name="Tail lamps", category="body", builder="tail_lamps",
        geometry=BODY_GEOMETRY, inputs=_body_inputs,  # on the body faces
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=_TAIL_LAMP_COLOR,
        finish="lamp",
    ),
    _interior("seats", "Seats", "seats", UPHOLSTERY[0], "leather", appearance=_upholstery,
              appearance_inputs=("interior_colour", "interior_trim")),
    _interior("dashboard", "Dashboard", "dashboard", (0.05, 0.052, 0.058), "trim"),
    _interior("display", "Display", "display", (0.02, 0.03, 0.05), "screen"),
    _interior("steering_wheel", "Steering wheel", "steering_wheel", (0.03, 0.03, 0.035), "leather"),
    _interior("console", "Centre console", "console", (0.05, 0.052, 0.058), "trim"),
    *(_equipment(*e) for e in EQUIPMENT),
    ComponentDef(
        id="frame", name="Chassis frame", category="chassis", builder="frame",
        geometry=FRAME_GEOMETRY, inputs=lambda p: {k: p[k] for k in dict.fromkeys(FRAME_GEOMETRY)},
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=_FRAME_COLOR, finish="metal",
    ),
    _axle("front_axle", "Front suspension", "track_front", "front_axle_mount"),
    _axle("rear_axle", "Rear suspension", "track_rear", "rear_axle_mount"),
    _wheel("wheel_fl", "Wheel front left", "front_axle", "left"),
    _wheel("wheel_fr", "Wheel front right", "front_axle", "right"),
    _wheel("wheel_rl", "Wheel rear left", "rear_axle", "left"),
    _wheel("wheel_rr", "Wheel rear right", "rear_axle", "right"),
    _rim("rim_fl", "Rim front left", "front_axle", "left"),
    _rim("rim_fr", "Rim front right", "front_axle", "right"),
    _rim("rim_rl", "Rim rear left", "rear_axle", "left"),
    _rim("rim_rr", "Rim rear right", "rear_axle", "right"),
    _damper("damper_fl", "Damper front left", "front", "left"),
    _damper("damper_fr", "Damper front right", "front", "right"),
    _damper("damper_rl", "Damper rear left", "rear", "left"),
    _damper("damper_rr", "Damper rear right", "rear", "right"),
)  # fmt: skip


COINCIDENCES: tuple[Coincidence, ...] = (
    Coincidence((f"damper_{tower[-2:]}", "upper_eye"), ("body", tower)) for tower in SHOCK_TOWERS
)

# Vertical load paths from the road to the body. Each consecutive pair must be joined by a
# mate or a coincidence; ``integration.check`` verifies this against the definitions above.
LOAD_PATHS: tuple[tuple[str, ...], ...] = (
    (f"wheel_{c}", f"{'front' if c[0] == 'f' else 'rear'}_axle", f"damper_{c}", "body")
    for c in ("fl", "fr", "rl", "rr")
)
