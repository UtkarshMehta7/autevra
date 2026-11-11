"""A road vehicle's breakdown: systems → subsystems → parts, generated from the design
parameters, with a parametric mass estimate and a CG position for every part.

Mass estimates are level-0 statistics for modern passenger cars and light trucks, each
with its basis stated on the part (e.g. body-in-white 36 kg per m² of plan area for a
unibody, tyre 0.047 kg per mm of section width, rim 0.62 kg per inch of diameter). They
are independent of the vehicle-mass parameter, so the roll-up *checks* that parameter
instead of copying it. Accuracy: concept level, typically within 10-15 % of a production
car's kerb mass; individual parts vary more.

Frame: x rearward from the front axle line, y to the left, z up from the ground (m).
"""

from typing import Any

from autevra.domains.automotive import derived as auto
from autevra.modules import Check, Values
from autevra.product import templates as tpl
from autevra.product.breakdown import Node, RolledNode
from autevra.product.options import Configuration, OptionFamily, OptionRule, Options
from autevra.product.templates import PartTemplate

MODULE = "land"
TEST_LOAD = 75.0  # kg, driver in the test condition (vehicle_mass is kerb plus load)

# option family -> (parameter, choices in the parameter's index order)
CHOICES: dict[str, tuple[str, tuple[str, ...]]] = {
    "powertrain": ("powertrain_type", ("Combustion", "Hybrid", "Battery electric")),
    "engine": ("engine_cylinders", ("3-cylinder", "4-cylinder", "V6", "V8")),
    "drive_side": ("driving_side", ("Left-hand drive", "Right-hand drive")),
    "roof": ("roof_type", ("Solid", "Panoramic glass", "Sunroof")),
    "tow_bar": ("tow_bar", ("None", "Fitted")),
    "mirrors": ("mirror_type", ("Conventional", "Camera")),
    "spoiler": ("rear_spoiler", ("None", "Roof spoiler", "Boot lip", "Wing")),
    "roof_rails": ("roof_rails", ("None", "Rails", "Rails with crossbars")),
}
LABELS = {"powertrain": "Powertrain", "engine": "Engine", "drive_side": "Driving side",
          "roof": "Roof", "tow_bar": "Tow bar", "mirrors": "Mirrors",
          "spoiler": "Rear spoiler", "roof_rails": "Roof rails"}  # fmt: skip
ENGINE_MASS = {"3-cylinder": 95.0, "4-cylinder": 130.0, "V6": 175.0, "V8": 215.0}


def options(values: Values) -> Options:
    fams = []
    for fid, (_, choices) in CHOICES.items():
        fams.append(OptionFamily(
            id=fid, label=LABELS[fid], choices=list(choices),
            applies="powertrain != 'Battery electric'" if fid == "engine" else "",
            affects_mass=fid not in ("drive_side",)))  # fmt: skip
    return Options(families=fams, rules=[
        OptionRule(id="v8_combustion_only", when="engine == 'V8'",
                   then="powertrain == 'Combustion'",
                   message="the V8 is offered with the combustion powertrain only"),
    ])  # fmt: skip


def _choice(values: Values, fid: str) -> str:
    param, choices = CHOICES[fid]
    i = int(round(float(values.get(param, 0))))
    return choices[min(max(i, 0), len(choices) - 1)]


def current(values: Values) -> dict[str, str]:
    out = {fid: _choice(values, fid) for fid in CHOICES}
    if out["powertrain"] == "Battery electric":
        out.pop("engine")
    return out


def configure(values: Values, config: Configuration) -> dict[str, Any]:
    out = dict(values)
    for fid, choice in config.items():
        param, choices = CHOICES[fid]
        out[param] = float(choices.index(choice))
    return out


# --- part templates ----------------------------------------------------------------------

F_CARRY, F_PROTECT = "carry occupants and cargo", "protect occupants and road users"
F_PROPEL, F_ENERGY = "propel", "store and supply energy"
F_STOP, F_STEER, F_RIDE = "decelerate and hold", "steer", "support and isolate from the road"
F_HEAT, F_VISION, F_COMFORT = "manage heat", "provide vision and visibility", "provide comfort"
F_HMI, F_SENSE = "inform and control", "sense the environment"
_T = (
    # id, name, code, process, functions, component with level-1 geometry today
    ("side_frame", "Body side frame (pillars, sill, roof rail)", "body.biw", "sheet metal",
     (F_CARRY, F_PROTECT), "body"),
    ("floor", "Floor (front, centre, rear)", "body.biw", "sheet metal", (F_CARRY,), ""),
    ("front_structure", "Front structure (rails, crush cans, towers, dash)", "body.biw",
     "sheet metal", (F_PROTECT,), ""),
    ("rear_structure", "Rear structure (rails, wheelhouses, panel)", "body.biw",
     "sheet metal", (F_PROTECT,), ""),
    ("roof_panel", "Roof panel and bows", "body.biw", "sheet metal", (F_PROTECT,), ""),
    ("crossmember", "Crossmembers", "body.biw", "sheet metal", (F_CARRY,), ""),
    ("bumper_beam", "Bumper beam", "body.biw", "extrusion", (F_PROTECT,), ""),
    ("ladder_frame", "Ladder frame", "chassis.frame", "weldment", (F_CARRY,), "frame"),
    ("skateboard", "Skateboard platform", "chassis.frame", "extrusion", (F_CARRY, F_ENERGY),
     "frame"),
    ("front_subframe", "Front subframe", "chassis.subframe", "weldment", (F_RIDE,), ""),
    ("rear_subframe", "Rear subframe", "chassis.subframe", "weldment", (F_RIDE,), ""),
    ("front_door", "Front door", "body.closures", "sheet metal", (F_CARRY, F_PROTECT), ""),
    ("rear_door", "Rear door", "body.closures", "sheet metal", (F_CARRY, F_PROTECT), ""),
    ("bonnet", "Bonnet", "body.closures", "sheet metal", (F_PROTECT,), ""),
    ("tailgate", "Tailgate", "body.closures", "sheet metal", (F_CARRY,), ""),
    ("boot_lid", "Boot lid", "body.closures", "sheet metal", (F_CARRY,), ""),
    ("cargo_doors", "Cargo doors", "body.closures", "sheet metal", (F_CARRY,), ""),
    ("bumper_fascia", "Bumper fascia", "body.exterior", "moulding", (F_PROTECT,), "lower_trim"),
    ("grille", "Grille", "body.exterior", "moulding", (F_HEAT,), "grille"),
    ("fender", "Front wing (fender)", "body.exterior", "sheet metal", (F_PROTECT,), ""),
    ("door_mirror", "Door mirror", "body.exterior", "moulding", (F_VISION,), "mirrors"),
    ("camera_mirror", "Camera mirror and display", "body.exterior", "inventory", (F_VISION,),
     "mirrors"),
    ("roof_spoiler", "Roof spoiler", "body.exterior", "moulding", (F_PROPEL,), "spoiler"),
    ("boot_lip", "Boot lip spoiler", "body.exterior", "moulding", (F_PROPEL,), "spoiler"),
    ("rear_wing", "Rear wing", "body.exterior", "composite", (F_PROPEL,), "spoiler"),
    ("roof_rail", "Roof rails", "body.exterior", "extrusion", (F_CARRY,), "roof_rails"),
    ("crossbar", "Roof crossbars", "body.exterior", "extrusion", (F_CARRY,), "roof_rails"),
    ("tow_bar", "Tow bar", "body.exterior", "weldment", (F_CARRY,), "tow_bar"),
    ("windscreen", "Windscreen", "body.glazing", "glass", (F_VISION,), "glass"),
    ("side_glass", "Side glass", "body.glazing", "glass", (F_VISION,), "glass"),
    ("backlight", "Rear window", "body.glazing", "glass", (F_VISION,), "glass"),
    ("panoramic_roof", "Panoramic glass roof", "body.glazing", "glass", (F_COMFORT,), ""),
    ("sunroof", "Sunroof module", "body.glazing", "assembly", (F_COMFORT,), ""),
    ("head_lamp", "Head lamp", "body.lighting", "moulding", (F_VISION,), "head_lamps"),
    ("tail_lamp", "Tail lamp", "body.lighting", "moulding", (F_VISION,), "tail_lamps"),
    ("suspension_corner", "Suspension corner (arms, knuckle, spring, bushes)",
     "chassis.suspension", "forging", (F_RIDE,), ""),
    ("beam_axle", "Beam axle", "chassis.suspension", "weldment", (F_RIDE,), "front_axle"),
    ("damper", "Damper", "chassis.suspension", "inventory", (F_RIDE,), "damper_fl"),
    ("anti_roll_bar", "Anti-roll bar and links", "chassis.suspension", "tube", (F_RIDE,), ""),
    ("steering_rack", "Steering rack and EPS", "chassis.steering", "assembly", (F_STEER,), ""),
    ("steering_column", "Steering column", "chassis.steering", "assembly", (F_STEER,), ""),
    ("steering_wheel", "Steering wheel", "chassis.steering", "moulding", (F_STEER, F_HMI),
     "steering_wheel"),
    ("brake_disc", "Brake disc", "chassis.brakes", "casting", (F_STOP,), "rotor_fl"),
    ("caliper", "Brake caliper", "chassis.brakes", "casting", (F_STOP,), "caliper_fl"),
    ("brake_hydraulics", "Brake hydraulics and ESC", "chassis.brakes", "assembly", (F_STOP,),
     ""),
    ("rim", "Rim", "chassis.wheels", "casting", (F_RIDE,), "rim_fl"),
    ("tyre", "Tyre", "chassis.wheels", "inventory", (F_RIDE,), "wheel_fl"),
    ("engine", "Engine (Mechanical module item)", "powertrain.engine", "inventory",
     (F_PROPEL,), "engine"),
    ("transmission", "Transmission", "powertrain.transmission", "inventory", (F_PROPEL,),
     "gearbox"),
    ("motor", "Electric motor", "powertrain.motor", "inventory", (F_PROPEL,), "front_motor"),
    ("inverter", "Inverter", "powertrain.motor", "inventory", (F_PROPEL,), "inverters"),
    ("reduction_gear", "Reduction gear", "powertrain.transmission", "inventory", (F_PROPEL,),
     ""),
    ("engine_mounts", "Powertrain mounts", "powertrain.mounts", "casting", (F_PROPEL, F_RIDE),
     ""),
    ("half_shaft", "Half-shaft", "driveline", "forging", (F_PROPEL,), ""),
    ("propshaft", "Propeller shaft", "driveline", "tube", (F_PROPEL,), ""),
    ("rear_differential", "Rear differential", "driveline", "casting", (F_PROPEL,), ""),
    ("traction_battery", "Traction battery pack", "energy.battery", "assembly", (F_ENERGY,),
     "traction_battery"),
    ("fuel_tank", "Fuel tank and filler", "energy.fuel", "moulding", (F_ENERGY,), "fuel_tank"),
    ("fuel", "Fuel (90 % fill)", "energy.fuel", "inventory", (F_ENERGY,), ""),
    ("battery_12v", "12 V battery", "energy.lv", "inventory", (F_ENERGY,), "battery_12v"),
    ("exhaust", "Exhaust system", "exhaust", "tube", (F_PROPEL,), "exhaust"),
    ("radiator", "Radiator, condenser and fans", "thermal", "assembly", (F_HEAT,), "radiator"),
    ("battery_thermal", "Battery chiller and pumps", "thermal", "assembly", (F_HEAT,), ""),
    ("hvac", "HVAC unit and ducts", "interior.hvac", "assembly", (F_COMFORT,), ""),
    ("harness", "Wiring harness", "electrical", "assembly", (F_HMI,), "harness"),
    ("ecus", "Control units", "electrical", "inventory", (F_HMI,), "ecus"),
    ("adas_sensors", "ADAS sensors", "electrical.adas", "inventory", (F_SENSE,), ""),
    ("hv_cables", "High-voltage cables", "electrical.hv", "assembly", (F_ENERGY,), "hv_cables"),
    ("charger", "On-board charger and port", "electrical.hv", "inventory", (F_ENERGY,),
     "charger"),
    ("front_seat", "Front seat", "interior.seats", "assembly", (F_CARRY, F_COMFORT), "seats"),
    ("rear_seat_row", "Rear seat row", "interior.seats", "assembly", (F_CARRY, F_COMFORT),
     "seats"),
    ("instrument_panel", "Instrument panel and cross-car beam", "interior.cockpit",
     "moulding", (F_HMI,), "dashboard"),
    ("console", "Centre console", "interior.cockpit", "moulding", (F_COMFORT,), "console"),
    ("display", "Displays", "interior.cockpit", "inventory", (F_HMI,), "display"),
    ("door_trim", "Door trim", "interior.trim", "moulding", (F_COMFORT,), ""),
    ("headliner", "Headliner", "interior.trim", "moulding", (F_COMFORT,), ""),
    ("carpet", "Carpet and insulation", "interior.trim", "moulding", (F_COMFORT,), ""),
    ("restraints", "Airbags and seat belts", "interior.restraints", "inventory", (F_PROTECT,),
     ""),
)  # fmt: skip
GEOMETRY = {t[0]: t[5] for t in _T if t[5]}
tpl.register(*(PartTemplate(id=i, module=MODULE, name=n, code=c, process=p, functions=f,
                            max_maturity=1 if g else 0)
               for i, n, c, p, f, g in _T))  # fmt: skip


def _n(tid: str, mass: float, basis: str, cg: tuple[float, float, float], *,
       idx: str = "", instances: int = 1, applicability: str = "",
       name: str = "") -> Node:  # fmt: skip
    t = tpl.get(MODULE, tid)
    geometry = GEOMETRY.get(tid, "")
    return Node(id=f"{tid}{idx}", name=name or t.name, kind="part", code=t.code,
                template=tid, process=t.process, functions=list(t.functions),
                applicability=applicability, instances=instances,
                maturity=1 if geometry else 0, mass=max(mass, 0.0), mass_source="estimated",
                basis=basis, cg=cg, geometry=geometry)  # fmt: skip


def _sys(sid: str, name: str, children: list[Node], code: str = "", *,
         kind: str = "system", applicability: str = "") -> Node:  # fmt: skip
    return Node(id=sid, name=name, kind=kind, code=code or sid,  # type: ignore[arg-type]
                children=children, applicability=applicability)  # fmt: skip


TWO_DOOR = {"Coupe", "Roadster", "Supercar", "Box truck"}
TAILGATE = {"Hatchback", "SUV", "Estate", "Crossover", "MPV", "Van", "Pickup"}
BOOT_LID = {"Sedan", "Coupe", "Roadster", "Supercar"}
OPEN_TOP = {"Roadster"}


def breakdown(values: Values) -> Node:
    p = {k: float(v) for k, v in values.items()}
    mm = 0.001
    wb, fo, ro = p["wheelbase"] * mm, p["front_overhang"] * mm, p["rear_overhang"] * mm
    length, width, height = fo + wb + ro, p["body_width"] * mm, p["overall_height"] * mm
    gc = p["ground_clearance"] * mm
    styles = ("Sedan", "Hatchback", "SUV", "Coupe", "Pickup", "Van", "Box truck", "Estate",
              "Crossover", "MPV", "Roadster", "Supercar")  # fmt: skip
    style = styles[min(max(int(round(p["body_style"])), 0), len(styles) - 1)]
    chassis = ("Ladder frame", "Unibody", "Skateboard")[int(round(p["chassis_type"]))]
    front_susp = ("Beam axle", "MacPherson strut", "Double wishbone",
                  "Multi-link")[int(round(p["front_suspension"]))]  # fmt: skip
    rear_susp = ("Beam axle", "Twist beam", "Multi-link",
                 "Double wishbone")[int(round(p["rear_suspension"]))]  # fmt: skip
    rows = int(round(p["seat_rows"]))
    rim_in, tyre_w = p["rim_diameter"], p["tyre_width"]
    mid_engine = style == "Supercar"
    front_share = p["front_drive_share"] / 100.0
    plan = length * width
    z_body = gc + 0.45 * (height - gc)
    x_mid = wb / 2
    tf, tr = p["track_front"] * mm, p["track_rear"] * mm
    two_door = style in TWO_DOOR

    # --- body structure ----------------------------------------------------------------
    if chassis == "Unibody":
        biw = 36.0 * plan
        biw_basis = "unibody body-in-white 36 kg/m² of plan area"
    elif chassis == "Ladder frame":
        biw = 30.0 * plan
        biw_basis = "body shell on a frame 30 kg/m² of plan area"
    else:
        biw = 24.0 * plan
        biw_basis = "upper body on a skateboard 24 kg/m² of plan area"
    if style in OPEN_TOP:
        biw *= 1.08
        biw_basis += ", +8 % open-car reinforcement"
    body_parts = [
        _n("side_frame", biw * 0.30, f"30 % of {biw_basis}", (x_mid, 0, z_body), instances=2),
        _n("floor", biw * 0.20, f"20 % of {biw_basis}", (x_mid, 0, gc + 0.05)),
        _n("front_structure", biw * 0.20, f"20 % of {biw_basis}", (-0.3 * fo, 0, z_body)),
        _n("rear_structure", biw * 0.12, f"12 % of {biw_basis}", (wb + 0.3 * ro, 0, z_body)),
        _n("crossmember", biw * 0.06, f"6 % of {biw_basis}", (x_mid, 0, gc + 0.1), instances=3),
        _n("bumper_beam", biw * 0.06, f"6 % of {biw_basis}", (x_mid, 0, gc + 0.3), instances=2),
    ]
    if style not in OPEN_TOP:
        body_parts.append(_n("roof_panel", biw * 0.06, f"6 % of {biw_basis}",
                             (x_mid, 0, height - 0.02)))  # fmt: skip
    structure = []
    if chassis == "Ladder frame":
        frame_len = 0.85 * length
        structure.append(_n("ladder_frame", 34.0 * frame_len, "ladder frame 34 kg per metre",
                            (x_mid, 0, gc + 0.12)))  # fmt: skip
    elif chassis == "Skateboard":
        structure.append(_n("skateboard", 22.0 * wb * (tf + tr) / 2,
                            "skateboard platform 22 kg/m² of wheelbase x track",
                            (x_mid, 0, gc + 0.08)))  # fmt: skip
    else:
        structure += [_n("front_subframe", 20.0, "typical front subframe", (0.0, 0, gc + 0.15)),
                      _n("rear_subframe", 18.0, "typical rear subframe",
                         (wb, 0, gc + 0.15))]  # fmt: skip
    body = _sys(
        "body",
        "Body",
        [
            _sys("body.biw", "Body-in-white", body_parts, kind="subsystem"),
            *(
                [_sys("chassis.frame", "Frame and subframes", structure, kind="subsystem")]
                if structure
                else []
            ),
            _sys(
                "body.closures",
                "Closures",
                [
                    _n(
                        "front_door",
                        22.0,
                        "typical front door assembly 22 kg",
                        (0.35 * wb, 0, z_body),
                        instances=2,
                    ),
                    *(
                        []
                        if two_door
                        else [
                            _n(
                                "rear_door",
                                18.0,
                                "typical rear door assembly 18 kg",
                                (0.7 * wb, 0, z_body),
                                instances=2,
                            )
                        ]
                    ),
                    _n("bonnet", 14.0, "typical steel bonnet 14 kg", (-0.2 * fo, 0, height * 0.75)),
                    *(
                        [
                            _n(
                                "tailgate",
                                18.0,
                                "typical tailgate 18 kg",
                                (wb + 0.8 * ro, 0, height * 0.7),
                            )
                        ]
                        if style in TAILGATE
                        else []
                    ),
                    *(
                        [
                            _n(
                                "boot_lid",
                                11.0,
                                "typical boot lid 11 kg",
                                (wb + 0.6 * ro, 0, height * 0.7),
                            )
                        ]
                        if style in BOOT_LID
                        else []
                    ),
                    *(
                        [_n("cargo_doors", 40.0, "cargo doors 40 kg", (wb + ro, 0, height * 0.5))]
                        if style == "Box truck"
                        else []
                    ),
                ],
                kind="subsystem",
            ),
            _sys(
                "body.exterior",
                "Exterior",
                [
                    _n(
                        "bumper_fascia",
                        5.5,
                        "moulded fascia 5.5 kg",
                        (-fo, 0, gc + 0.3),
                        idx="_front",
                    ),
                    _n(
                        "bumper_fascia",
                        5.0,
                        "moulded fascia 5 kg",
                        (wb + ro, 0, gc + 0.3),
                        idx="_rear",
                    ),
                    _n("grille", 2.0, "grille 2 kg", (-fo, 0, gc + 0.45)),
                    _n("fender", 3.0, "steel front wing 3 kg", (0.0, 0, z_body), instances=2),
                    _n(
                        "door_mirror",
                        2.0,
                        "door mirror 2 kg",
                        (0.15 * wb, 0, height * 0.7),
                        instances=2,
                        applicability="mirrors == 'Conventional'",
                    ),
                    _n(
                        "camera_mirror",
                        0.8,
                        "camera arm and display 0.8 kg",
                        (0.15 * wb, 0, height * 0.7),
                        instances=2,
                        applicability="mirrors == 'Camera'",
                    ),
                    _n(
                        "roof_spoiler",
                        3.0,
                        "roof spoiler 3 kg",
                        (wb + ro * 0.8, 0, height),
                        applicability="spoiler == 'Roof spoiler'",
                    ),
                    _n(
                        "boot_lip",
                        1.5,
                        "boot lip 1.5 kg",
                        (wb + ro * 0.9, 0, height * 0.75),
                        applicability="spoiler == 'Boot lip'",
                    ),
                    _n(
                        "rear_wing",
                        6.0,
                        "rear wing with stays 6 kg",
                        (wb + ro * 0.85, 0, height * 0.85),
                        applicability="spoiler == 'Wing'",
                    ),
                    _n(
                        "roof_rail",
                        4.0,
                        "roof rails 4 kg",
                        (x_mid, 0, height + 0.03),
                        applicability="roof_rails != 'None'",
                    ),
                    _n(
                        "crossbar",
                        3.0,
                        "crossbars 3 kg",
                        (x_mid, 0, height + 0.06),
                        applicability="roof_rails == 'Rails with crossbars'",
                    ),
                    _n(
                        "tow_bar",
                        18.0,
                        "detachable tow bar 18 kg",
                        (wb + ro, 0, gc + 0.25),
                        applicability="tow_bar == 'Fitted'",
                    ),
                ],
                kind="subsystem",
            ),
            _sys(
                "body.glazing",
                "Glazing",
                [
                    _n(
                        "windscreen",
                        13.0,
                        "laminated windscreen 13 kg",
                        (0.15 * wb, 0, height * 0.8),
                    ),
                    _n(
                        "side_glass",
                        3.5,
                        "tempered side glass 3.5 kg each",
                        (x_mid, 0, height * 0.8),
                        instances=2 if two_door else 4,
                    ),
                    *(
                        []
                        if style in OPEN_TOP
                        else [
                            _n(
                                "backlight",
                                7.0,
                                "rear window 7 kg",
                                (wb + 0.4 * ro, 0, height * 0.8),
                            )
                        ]
                    ),
                    *(
                        []
                        if style in OPEN_TOP
                        else [
                            _n(
                                "panoramic_roof",
                                25.0,
                                "panoramic glass roof and frame 25 kg",
                                (x_mid, 0, height),
                                applicability="roof == 'Panoramic glass'",
                            ),
                            _n(
                                "sunroof",
                                18.0,
                                "sunroof module 18 kg",
                                (0.4 * wb, 0, height),
                                applicability="roof == 'Sunroof'",
                            ),
                        ]
                    ),
                ],
                kind="subsystem",
            ),
            _sys(
                "body.lighting",
                "Lighting",
                [
                    _n(
                        "head_lamp",
                        3.5,
                        "LED head lamp 3.5 kg",
                        (-0.85 * fo, 0, gc + 0.5),
                        instances=2,
                    ),
                    _n(
                        "tail_lamp",
                        1.5,
                        "tail lamp 1.5 kg",
                        (wb + 0.9 * ro, 0, gc + 0.6),
                        instances=2,
                    ),
                ],
                kind="subsystem",
            ),
        ],
        "body",
    )

    # --- chassis -------------------------------------------------------------------------
    corner = {"Beam axle": 0.0, "MacPherson strut": 15.0, "Double wishbone": 19.0,
              "Multi-link": 20.0, "Twist beam": 0.0}  # fmt: skip

    def axle(prefix: str, kind: str, x: float, label: str) -> list[Node]:
        if kind == "Beam axle":
            return [_n("beam_axle", 60.0, "beam axle with springs 60 kg", (x, 0, rim_in * 0.0127),
                       idx=prefix, name=f"{label} beam axle")]  # fmt: skip
        if kind == "Twist beam":
            return [
                _n(
                    "beam_axle",
                    30.0,
                    "twist-beam axle with springs 30 kg",
                    (x, 0, rim_in * 0.0127),
                    idx=prefix,
                    name=f"{label} twist beam",
                )
            ]
        return [_n("suspension_corner", corner[kind], f"{kind.lower()} corner {corner[kind]:g} kg",
                   (x, 0, rim_in * 0.0127 + 0.05), idx=prefix, instances=2,
                   name=f"{label} suspension corner ({kind.lower()})")]  # fmt: skip

    disc_f, disc_r = 0.42 * rim_in, 0.32 * rim_in
    rim_kg, tyre_kg = 0.62 * rim_in, 0.047 * tyre_w
    z_hub = rim_in * 0.0127 + 0.04
    chassis_sys = _sys(
        "chassis",
        "Chassis",
        [
            _sys(
                "chassis.suspension",
                "Suspension",
                [
                    *axle("_front", front_susp, 0.0, "Front"),
                    *axle("_rear", rear_susp, wb, "Rear"),
                    _n(
                        "damper",
                        3.0,
                        "damper 3 kg",
                        (0.0, 0, z_hub + 0.2),
                        idx="_front",
                        instances=2,
                        name="Front damper",
                    ),
                    _n(
                        "damper",
                        2.8,
                        "damper 2.8 kg",
                        (wb, 0, z_hub + 0.2),
                        idx="_rear",
                        instances=2,
                        name="Rear damper",
                    ),
                    _n("anti_roll_bar", 5.0, "anti-roll bar and links 5 kg", (0.0, 0, z_hub)),
                ],
                kind="subsystem",
            ),
            _sys(
                "chassis.steering",
                "Steering",
                [
                    _n("steering_rack", 12.0, "rack with electric assist 12 kg", (0.05, 0, z_hub)),
                    _n(
                        "steering_column",
                        6.0,
                        "column and intermediate shaft 6 kg",
                        (0.3 * wb, 0, height * 0.55),
                    ),
                    _n(
                        "steering_wheel",
                        2.5,
                        "steering wheel with airbag 2.5 kg",
                        (0.38 * wb, 0, height * 0.6),
                    ),
                ],
                kind="subsystem",
            ),
            _sys(
                "chassis.brakes",
                "Brakes",
                [
                    _n(
                        "brake_disc",
                        disc_f,
                        "front disc 0.42 kg per inch of rim",
                        (0.0, 0, z_hub),
                        idx="_front",
                        instances=2,
                        name="Front brake disc",
                    ),
                    _n(
                        "brake_disc",
                        disc_r,
                        "rear disc 0.32 kg per inch of rim",
                        (wb, 0, z_hub),
                        idx="_rear",
                        instances=2,
                        name="Rear brake disc",
                    ),
                    _n(
                        "caliper",
                        4.5,
                        "front caliper 4.5 kg",
                        (0.0, 0, z_hub),
                        idx="_front",
                        instances=2,
                        name="Front caliper",
                    ),
                    _n(
                        "caliper",
                        3.0,
                        "rear caliper 3 kg",
                        (wb, 0, z_hub),
                        idx="_rear",
                        instances=2,
                        name="Rear caliper",
                    ),
                    _n(
                        "brake_hydraulics",
                        6.0,
                        "master cylinder, booster, lines, ESC 6 kg",
                        (0.2 * wb, 0, height * 0.5),
                    ),
                ],
                kind="subsystem",
            ),
            _sys(
                "chassis.wheels",
                "Wheels and tyres",
                [
                    _n(
                        "rim",
                        4 * rim_kg,
                        "cast rim 0.62 kg per inch of diameter",
                        (x_mid, 0, z_hub),
                        instances=4,
                    ),
                    _n(
                        "tyre",
                        4 * tyre_kg,
                        "tyre 0.047 kg per mm of section width",
                        (x_mid, 0, z_hub),
                        instances=4,
                    ),
                ],
                kind="subsystem",
            ),
        ],
        "chassis",
    )

    # --- powertrain and energy --------------------------------------------------------------
    x_engine = 0.62 * wb if mid_engine else -0.1
    ice = "powertrain != 'Battery electric'"
    bev = "powertrain == 'Battery electric'"
    hev = "powertrain == 'Hybrid'"
    engine_nodes = [
        _n(
            "engine",
            m,
            f"typical {c} petrol engine, dry {m:g} kg",
            (x_engine, 0, gc + 0.45),
            idx=f"_{i}",
            name=f"Engine, {c}",
            applicability=f"{ice} and engine == '{c}'",
        )  # fmt: skip
        for i, (c, m) in enumerate(ENGINE_MASS.items())
    ]
    motor_kw = p["peak_power"]
    battery = auto.battery_mass(p)
    driven_front, driven_rear = front_share > 0.0, front_share < 1.0
    power = _sys(
        "powertrain",
        "Powertrain",
        [
            *engine_nodes,
            _n(
                "transmission",
                75.0,
                "automatic transmission 75 kg",
                (x_engine + (0.25 if not mid_engine else 0.45), 0, gc + 0.35),
                applicability=ice,
            ),
            _n("engine_mounts", 6.0, "powertrain mounts 6 kg", (x_engine, 0, gc + 0.4)),
            _n(
                "motor",
                0.28 * motor_kw,
                "electric motor 0.28 kg/kW of peak power",
                (wb if driven_rear else 0.0, 0, gc + 0.3),
                applicability=bev,
            ),
            _n(
                "motor",
                30.0,
                "hybrid motor-generator 30 kg",
                (x_engine + 0.3, 0, gc + 0.35),
                idx="_hybrid",
                name="Hybrid motor-generator",
                applicability=hev,
            ),
            _n(
                "inverter",
                10.0,
                "inverter 10 kg",
                (wb if driven_rear else 0.0, 0, gc + 0.45),
                applicability="powertrain != 'Combustion'",
            ),
            _n(
                "reduction_gear",
                25.0,
                "single-speed reduction gear 25 kg",
                (wb if driven_rear else 0.0, 0, gc + 0.25),
                applicability=bev,
            ),
            _n(
                "exhaust",
                22.0,
                "exhaust with catalyst and silencers 22 kg",
                (x_mid, 0, gc + 0.05),
                applicability=ice,
            ),
        ],
        "powertrain",
    )
    driveline = _sys(
        "driveline",
        "Driveline",
        [
            *(
                [
                    _n(
                        "half_shaft",
                        12.0,
                        "two half-shafts 6 kg each",
                        (0.0, 0, z_hub),
                        idx="_front",
                        instances=2,
                        name="Front half-shaft",
                    )
                ]
                if driven_front
                else []
            ),
            *(
                [
                    _n(
                        "half_shaft",
                        12.0,
                        "two half-shafts 6 kg each",
                        (wb, 0, z_hub),
                        idx="_rear",
                        instances=2,
                        name="Rear half-shaft",
                    )
                ]
                if driven_rear
                else []
            ),
            *(
                [
                    _n(
                        "propshaft",
                        12.0,
                        "propeller shaft 12 kg",
                        (x_mid, 0, gc + 0.15),
                        applicability=ice,
                    ),
                    _n(
                        "rear_differential",
                        25.0,
                        "rear differential 25 kg",
                        (wb, 0, z_hub),
                        applicability=ice,
                    ),
                ]
                if driven_rear and not mid_engine
                else []
            ),
        ],
        "driveline",
    )
    energy = _sys(
        "energy",
        "Energy storage",
        [
            _n(
                "traction_battery",
                battery,
                "pack energy density of the vehicle model",
                (x_mid, 0, gc + 0.12),
                applicability="powertrain != 'Combustion'",
            ),
            _n(
                "fuel_tank",
                12.0,
                "plastic fuel tank and filler 12 kg",
                (0.8 * wb, 0, gc + 0.15),
                applicability=ice,
            ),
            _n(
                "fuel",
                45.0,
                "50 L tank at 90 % (kerb condition), 0.745 kg/L",
                (0.8 * wb, 0, gc + 0.15),
                applicability=ice,
            ),
            _n("battery_12v", 15.0, "12 V battery 15 kg", (-0.3 * fo, 0, gc + 0.5)),
        ],
        "energy",
    )
    thermal = _sys(
        "thermal",
        "Thermal",
        [
            _n("radiator", 12.0, "radiator, condenser and fans 12 kg", (-0.8 * fo, 0, gc + 0.35)),
            _n(
                "battery_thermal",
                9.0,
                "battery chiller, pumps and plates 9 kg",
                (0.2 * wb, 0, gc + 0.4),
                applicability="powertrain != 'Combustion'",
            ),
            _n("hvac", 16.0, "HVAC unit and ducts 16 kg", (0.2 * wb, 0, height * 0.5)),
        ],
        "thermal",
    )
    electrical = _sys(
        "electrical",
        "Electrical and electronics",
        [
            _n("harness", 28.0, "low-voltage harness 28 kg", (x_mid, 0, z_body)),
            _n("ecus", 8.0, "control units 8 kg", (0.25 * wb, 0, height * 0.5)),
            _n(
                "adas_sensors",
                3.0,
                "radar, camera and ultrasonic sensors 3 kg",
                (-0.5 * fo, 0, gc + 0.5),
            ),
            _n(
                "hv_cables",
                8.0,
                "high-voltage cables 8 kg",
                (x_mid, 0, gc + 0.1),
                applicability="powertrain != 'Combustion'",
            ),
            _n(
                "charger",
                7.0,
                "on-board charger and port 7 kg",
                (wb + 0.3 * ro, 0, gc + 0.4),
                applicability="powertrain != 'Combustion'",
            ),
        ],
        "electrical",
    )
    seat_x = [0.45 * wb, 0.45 * wb + p["row_pitch"] * mm, 0.45 * wb + 2 * p["row_pitch"] * mm]
    z_seat = p["seat_height"] * mm if "seat_height" in p else gc + 0.35
    interior = _sys(
        "interior",
        "Interior",
        [
            _n(
                "front_seat",
                20.0,
                "front seat with tracks and recliner 20 kg",
                (seat_x[0], 0, z_seat),
                instances=2,
            ),
            *[
                _n(
                    "rear_seat_row",
                    30.0 if r == 1 else 25.0,
                    "rear bench 30 kg" if r == 1 else "third-row seats 25 kg",
                    (seat_x[min(r, 2)], 0, z_seat),
                    idx=f"_{r + 1}",
                    name=f"Seat row {r + 1}",
                )
                for r in range(1, rows)
            ],
            _n(
                "instrument_panel",
                30.0,
                "instrument panel 22 kg and cross-car beam 8 kg",
                (0.25 * wb, 0, height * 0.55),
            ),
            _n("console", 6.0, "centre console 6 kg", (0.4 * wb, 0, gc + 0.45)),
            _n("display", 3.0, "displays 3 kg", (0.25 * wb, 0, height * 0.65)),
            _n(
                "door_trim",
                2.5,
                "door trim 2.5 kg each",
                (0.5 * wb, 0, z_body),
                instances=2 if two_door else 4,
            ),
            *(
                []
                if style in OPEN_TOP
                else [_n("headliner", 4.0, "headliner 4 kg", (x_mid, 0, height - 0.05))]
            ),
            _n("carpet", 12.0, "carpet and acoustic insulation 12 kg", (x_mid, 0, gc + 0.15)),
            _n(
                "restraints",
                8.0 + 1.2 * 2 * rows,
                "airbags 8 kg and 1.2 kg per belt (two per row)",
                (0.45 * wb, 0, z_body),
            ),
        ],
        "interior",
    )
    load = Node(id="test_load", name="Driver (test condition)", kind="system", code="load",
                mass=TEST_LOAD, mass_source="estimated", basis="one 75 kg occupant",
                cg=(seat_x[0], 0.0, z_seat + 0.2))  # fmt: skip
    return Node(id="vehicle", name=f"{style} ({chassis.lower()})", kind="product",
                code="vehicle", budget=p["vehicle_mass"],
                children=[body, chassis_sys, power, driveline, energy, thermal, electrical,
                          interior, load])  # fmt: skip


def checks(values: Values, root: RolledNode) -> list[Check]:
    p = {k: float(v) for k, v in values.items()}
    mass, cg = root.rollup.mass, root.rollup.cg
    target = p["vehicle_mass"]
    err = (mass - target) / target
    status = "pass" if abs(err) <= 0.075 else "warn" if abs(err) <= 0.15 else "fail"
    out = [Check(id="mass", label="Vehicle mass", status=status,
                 message=f"parts sum to {mass:.0f} kg (kerb plus a 75 kg driver) vs "
                 f"{target:.0f} kg in the design ({err:+.1%}); the ride, performance and "
                 "pitch analyses use the design's value")]  # fmt: skip
    wb = p["wheelbase"] / 1000
    front = 1 - cg[0] / wb
    dist = p["front_mass_distribution"] / 100
    d = (front - dist) * 100
    status = "pass" if abs(d) <= 3 else "warn" if abs(d) <= 7 else "fail"
    out.append(Check(id="front_share", label="Front axle share", status=status,
                     message=f"parts give {front:.0%} on the front axle vs {dist:.0%} in the "
                     f"design ({d:+.1f} points)"))  # fmt: skip
    dz = cg[2] * 1000 - p["cg_height"]
    status = "pass" if abs(dz) <= 50 else "warn"
    out.append(Check(id="cg_height", label="CG height", status=status,
                     message=f"parts give {cg[2] * 1000:.0f} mm vs {p['cg_height']:.0f} mm in "
                     f"the design ({dz:+.0f} mm); part heights are level-0 estimates"))  # fmt: skip
    return out
