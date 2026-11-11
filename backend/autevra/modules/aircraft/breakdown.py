"""The light aircraft's breakdown, organised by ATA chapter.

Group masses: Raymer's general-aviation weight equations (D. P. Raymer, *Aircraft Design:
A Conceptual Approach*, general aviation group weights), in their native units (lb, ft,
lb/ft²) and converted to kg. Each group is split into its parts by stated shares
(allocations, level 0). Assumptions: ultimate load factor 1.5 x the category's limit load
factor; ultimate landing load factor 1.5 x 3.0; dry engine 0.88 kg/kW (air-cooled
flat-four); uninstalled avionics 18 kg (basic VFR panel); no integral tanks; an
unpressurised cabin. Accuracy: conceptual, typically within 10-20 % of actual group masses;
the default aircraft gives 742 kg empty against a published 760 kg for its reference type.

CG positions are estimates for each group (wing at 40 % of the MAC, tails at 40 % of
their root chord, engine just aft of the propeller, crew and payload at the seats).
"""

import math
from typing import Any

from autevra.aero import aircraft as ac
from autevra.modules import Check, Values
from autevra.product import templates as tpl
from autevra.product.breakdown import Node, RolledNode
from autevra.product.breakdown import configure as configure_tree
from autevra.product.options import Configuration, OptionFamily, OptionRule, Options
from autevra.product.templates import PartTemplate

MODULE = "aircraft"
LB = 2.20462  # lb per kg
FT = 3.28084  # ft per m
PSF = 0.0208854  # lb/ft² per Pa
CATEGORIES = {"Normal": 3.8, "Utility": 4.4, "Aerobatic": 6.0}  # limit load factors
PILOT = 77.0  # kg, standard occupant


def options(values: Values) -> Options:
    return Options(
        families=[
            OptionFamily(id="category", label="Certification category",
                         choices=list(CATEGORIES),
                         description="sets the limit load factor (3.8 / 4.4 / 6.0 g)"),
            OptionFamily(id="gear", label="Landing gear", choices=["Fixed", "Retractable"]),
            OptionFamily(id="undercarriage", label="Undercarriage layout",
                         choices=["Tricycle", "Tailwheel"]),
            OptionFamily(id="wing", label="Wing position", choices=["High wing", "Low wing"],
                         affects_mass=False),
            OptionFamily(id="tail", label="Tail", choices=["Conventional", "T-tail"],
                         affects_mass=False),
        ],
        rules=[
            OptionRule(id="aerobatic_fixed_gear", when="category == 'Aerobatic'",
                       then="gear == 'Fixed'",
                       message="aerobatic variants keep the fixed gear (simpler, stronger "
                       "structure for the 6 g case)"),
        ],
    )  # fmt: skip


def current(values: Values) -> dict[str, str]:
    return {
        "category": str(values.get("category", "Normal")),
        "gear": "Fixed" if values.get("fixed_gear", True) else "Retractable",
        "undercarriage": "Tricycle" if values.get("tricycle", True) else "Tailwheel",
        "wing": "High wing" if values.get("high_wing", True) else "Low wing",
        "tail": "T-tail" if values.get("t_tail", False) else "Conventional",
    }


def configure(values: Values, config: Configuration) -> dict[str, Any]:
    out = dict(values)
    c = {**current(values), **config}
    out.update(category=c["category"], fixed_gear=c["gear"] == "Fixed",
               tricycle=c["undercarriage"] == "Tricycle", high_wing=c["wing"] == "High wing",
               t_tail=c["tail"] == "T-tail")  # fmt: skip
    return out


# --- part templates (M1: identity, process, functions; mass by allocation) -------------

_T = (
    ("frame", "Fuselage frame", "53-10", "sheet metal", ("carry structural loads",)),
    ("stringer", "Fuselage stringer", "53-10", "extrusion", ("carry structural loads",)),
    ("fuselage_skin", "Fuselage skin", "53-30", "sheet metal", ("carry structural loads",)),
    ("firewall", "Firewall", "53-10", "sheet metal", ("protect occupants",)),
    ("cabin_floor", "Cabin floor", "53-20", "sheet metal", ("carry structural loads",)),
    ("door", "Cabin door", "52-10", "sheet metal", ("protect occupants",)),
    ("windscreen", "Windscreen and windows", "56-10", "moulding", ("protect occupants",)),
    ("tail_cone", "Tail cone", "53-40", "sheet metal", ("carry structural loads",)),
    ("spar", "Wing spar", "57-10", "machining", ("generate lift", "carry structural loads")),
    ("rib", "Wing rib", "57-10", "sheet metal", ("generate lift",)),
    ("wing_skin", "Wing skin", "57-30", "sheet metal", ("generate lift",)),
    ("leading_edge", "Wing leading edge", "57-40", "sheet metal", ("generate lift",)),
    ("wing_tip", "Wing tip", "57-30", "moulding", ("generate lift",)),
    ("aileron", "Aileron", "57-60", "sheet metal", ("control attitude and trajectory",)),
    ("flap", "Flap", "57-50", "sheet metal", ("generate lift",)),
    ("stabiliser", "Horizontal stabiliser", "55-10", "sheet metal",
     ("control attitude and trajectory",)),
    ("elevator", "Elevator", "55-20", "sheet metal", ("control attitude and trajectory",)),
    ("fin", "Fin", "55-30", "sheet metal", ("control attitude and trajectory",)),
    ("rudder", "Rudder", "55-40", "sheet metal", ("control attitude and trajectory",)),
    ("main_leg", "Main gear leg", "32-10", "forging", ("support on the ground",)),
    ("main_wheel", "Main wheel, tyre and brake", "32-40", "inventory",
     ("support on the ground",)),
    ("nose_leg", "Nose gear leg", "32-20", "forging", ("support on the ground",)),
    ("nose_wheel", "Nose wheel and tyre", "32-40", "inventory", ("support on the ground",)),
    ("tailwheel", "Tailwheel assembly", "32-20", "assembly", ("support on the ground",)),
    ("retraction", "Gear retraction system", "32-30", "assembly",
     ("support on the ground",)),
    ("engine", "Piston engine", "72-00", "inventory", ("provide thrust",)),
    ("propeller", "Propeller", "61-10", "inventory", ("provide thrust",)),
    ("engine_mount", "Engine mount", "71-20", "weldment", ("provide thrust",)),
    ("cowling", "Engine cowling", "71-10", "composite", ("provide thrust",)),
    ("exhaust", "Exhaust system", "78-10", "tube", ("provide thrust",)),
    ("engine_accessories", "Baffles, induction and accessories", "73-00", "assembly",
     ("provide thrust",)),
    ("fuel_tank", "Fuel tank", "28-10", "sheet metal", ("store and supply fuel",)),
    ("fuel_lines", "Fuel lines", "28-20", "tube", ("store and supply fuel",)),
    ("fuel_pump", "Fuel pumps and selector", "28-20", "inventory", ("store and supply fuel",)),
    ("fuel_gauging", "Fuel quantity gauging", "28-40", "inventory",
     ("store and supply fuel", "indicate and alert")),
    ("control_column", "Control column", "27-00", "machining",
     ("control attitude and trajectory",)),
    ("rudder_pedals", "Rudder pedals", "27-20", "machining",
     ("control attitude and trajectory",)),
    ("control_cables", "Control cables and pulleys", "27-00", "standard",
     ("control attitude and trajectory",)),
    ("pushrods", "Pushrods and bellcranks", "27-00", "machining",
     ("control attitude and trajectory",)),
    ("trim", "Trim system", "27-30", "assembly", ("control attitude and trajectory",)),
    ("brake_hydraulics", "Brake master cylinders and lines", "32-40", "tube",
     ("support on the ground",)),
    ("alternator", "Alternator", "24-30", "inventory", ("supply electrical power",)),
    ("battery", "Battery", "24-30", "inventory", ("supply electrical power",)),
    ("harness", "Wiring harness", "24-60", "assembly", ("supply electrical power",)),
    ("electrical_bus", "Bus and circuit breakers", "24-50", "assembly",
     ("supply electrical power",)),
    ("displays", "Flight displays", "31-00", "inventory", ("navigate and communicate",
                                                          "indicate and alert")),
    ("radios", "Radios and transponder", "23-00", "inventory", ("navigate and communicate",)),
    ("pitot_static", "Antennas and pitot-static", "34-10", "inventory",
     ("navigate and communicate",)),
    ("seat", "Seat", "25-10", "assembly", ("protect occupants",)),
    ("restraints", "Harnesses and restraints", "25-10", "standard", ("protect occupants",)),
    ("linings", "Cabin linings and insulation", "25-20", "moulding", ("protect occupants",)),
    ("baggage", "Baggage area", "25-50", "sheet metal", ("carry payload",)),
)  # fmt: skip
GEOMETRY = {
    "fuselage_skin": "fuselage",
    "wing_skin": "wing",
    "stabiliser": "tailplane",
    "fin": "fin",
    "propeller": "propeller",
}  # parts with level-1 geometry today
tpl.register(*(PartTemplate(id=i, module=MODULE, name=n, code=c, process=p, functions=f,
                            max_maturity=1 if i in GEOMETRY else 0)
               for i, n, c, p, f in _T))  # fmt: skip


# --- Raymer general-aviation group weights (lb) ----------------------------------------


def group_masses(s: ac.AircraftSpec, n_limit: float) -> dict[str, float]:
    """Group masses in kg (Raymer's general-aviation equations)."""
    geo = ac.analyse(s)["geometry"]
    wdg = s.mtow * LB
    nz = 1.5 * n_limit
    rho = ac.isa(s.cruise_altitude)["rho"]
    q = 0.5 * rho * s.cruise_speed**2 * PSF
    cos = lambda deg: math.cos(math.radians(deg))  # noqa: E731
    tc_w = int(s.wing_naca[2:]) / 100

    sw = geo["wing_area"] * FT**2
    lam = s.wing_tip_chord / s.wing_root_chord
    # quarter-chord sweep from the leading-edge sweep
    tan_le = math.tan(math.radians(s.wing_sweep))
    sweep_c4 = math.degrees(math.atan(tan_le - (1 - lam) * s.wing_root_chord /
                                      (2 * s.wing_span)))  # fmt: skip
    a = geo["aspect_ratio"]
    w_wing = (0.036 * sw**0.758 * (s.fuel_mass * LB) ** 0.0035
              * (a / cos(sweep_c4) ** 2) ** 0.6 * q**0.006 * lam**0.04
              * (100 * tc_w / cos(sweep_c4)) ** -0.3 * (nz * wdg) ** 0.49)  # fmt: skip

    sht = geo["htail_area"] * FT**2
    aht = s.htail_span**2 / geo["htail_area"]
    w_ht = (0.016 * (nz * wdg) ** 0.414 * q**0.168 * sht**0.896 * (100 * 0.12) ** -0.12
            * aht**0.043 * (s.htail_tip_chord / s.htail_root_chord) ** -0.02)  # fmt: skip

    svt = geo["fin_area"] * FT**2
    avt = s.fin_height**2 / geo["fin_area"]
    ht_hv = 1.0 if s.t_tail else 0.0
    w_vt = (0.073 * (1 + 0.2 * ht_hv) * (nz * wdg) ** 0.376 * q**0.122 * svt**0.873
            * (100 * 0.12 / cos(s.fin_sweep)) ** -0.49 * (avt / cos(s.fin_sweep) ** 2) ** 0.357
            * (s.fin_tip_chord / s.fin_root_chord) ** 0.039)  # fmt: skip

    lf = s.fuselage_length * FT
    d = (s.fuselage_width + s.fuselage_height) / 2 * FT
    sf = math.pi * d * lf * 0.75  # wetted area of a tapering body (estimate)
    lt = max(s.htail_x - s.wing_x, 0.5) * FT
    w_fus = 0.052 * sf**1.086 * (nz * wdg) ** 0.177 * lt**-0.051 * (lf / d) ** -0.072 * q**0.241

    nl = 1.5 * 3.0
    lm = 0.62 * s.fuselage_height * 39.37  # strut length, inches
    w_mlg = 0.095 * (nl * wdg) ** 0.768 * (lm / 12) ** 0.409
    w_nlg = 0.125 * (nl * wdg) ** 0.566 * (0.55 * s.fuselage_height * 39.37 / 12) ** 0.845

    w_en_dry = 0.88 * s.power_kw * LB
    w_en = 2.575 * w_en_dry**0.922

    vt = s.fuel_mass / 0.72 / 3.785  # US gallons of avgas
    w_fs = 2.49 * vt**0.726 * 2**0.242
    w_fc = 0.053 * lf**1.536 * (s.wing_span * FT) ** 0.371 * (nz * wdg * 1e-4) ** 0.80
    w_hyd = 0.001 * wdg
    w_av = 2.117 * (18.0 * LB) ** 0.933
    w_el = 12.57 * (w_fs + w_av) ** 0.51
    w_furn = 0.0582 * wdg - 65
    lb = {"wing": w_wing, "htail": w_ht, "vtail": w_vt, "fuselage": w_fus,
          "main_gear": w_mlg, "nose_gear": w_nlg, "engine_installed": w_en,
          "engine_dry": w_en_dry, "fuel_system": w_fs, "flight_controls": w_fc,
          "hydraulics": w_hyd, "avionics": w_av, "electrical": w_el,
          "furnishings": max(w_furn, 0.0)}  # fmt: skip
    return {k: v / LB for k, v in lb.items()}


# --- the breakdown ---------------------------------------------------------------------


def _part(tid: str, total: float, share: float, basis: str, cg: tuple[float, float, float],
          *, idx: str = "", instances: int = 1, applicability: str = "",
          envelope: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Node:  # fmt: skip
    t = tpl.get(MODULE, tid)
    geometry = GEOMETRY.get(tid, "")
    return Node(id=f"{tid}{idx}", name=t.name, kind="part", code=f"ATA {t.code}",
                template=tid, process=t.process, functions=list(t.functions),
                applicability=applicability, instances=instances,
                maturity=1 if geometry else 0, mass=max(total * share, 0.0),
                mass_source="allocated", basis=f"{share:.0%} of {basis}", cg=cg,
                envelope=envelope, geometry=geometry)  # fmt: skip


def _system(sid: str, name: str, code: str, parts: list[Node], *, applicability: str = "",
            functions: tuple[str, ...] = ()) -> Node:  # fmt: skip
    return Node(id=sid, name=name, kind="system", code=code, children=parts,
                applicability=applicability, functions=list(functions))  # fmt: skip


def breakdown(values: Values) -> Node:
    s = ac.AircraftSpec.model_validate({k: v for k, v in values.items()
                                        if k in ac.AircraftSpec.model_fields})  # fmt: skip
    n_limit = CATEGORIES[str(values.get("category", "Normal"))]
    g = group_masses(s, n_limit)
    geo = ac.analyse(s)["geometry"]
    h = s.fuselage_height
    z_wing = 0.55 * h if s.high_wing else -0.35 * h
    x_wing = geo["mac_x"] + 0.4 * geo["mac"]
    x_ht = s.htail_x + 0.4 * s.htail_root_chord
    x_vt = s.fin_x + 0.4 * s.fin_root_chord + 0.4 * s.fin_height * math.tan(
        math.radians(s.fin_sweep))  # fmt: skip
    z_ht = (0.5 * h + s.fin_height) if s.t_tail else 0.1 * h
    x_main = s.x_cg + (0.35 if s.tricycle else -0.45)
    x_seat1, x_seat2 = s.wing_x + 0.15, s.wing_x + 1.05
    lf = s.fuselage_length
    semi = s.wing_span / 2
    rib_pairs = max(round(semi / 0.35), 4)
    frames = max(round(lf / 0.5), 6)
    basis = "Raymer GA {} group weight"
    fus, wing = g["fuselage"], g["wing"]
    ht, vt = g["htail"], g["vtail"]
    gear_mlg, gear_nlg = g["main_gear"], g["nose_gear"]
    eng_inst, eng_dry = g["engine_installed"], g["engine_dry"]
    engine_basis = "the dry engine (0.88 kg/kW)"
    if isinstance(values.get("installed_engine_mass_kg"), int | float):  # from the inventory
        eng_dry = float(values["installed_engine_mass_kg"])
        engine_basis = f"inventory item {values.get('installed_engine_label', '')}"
    rest = max(eng_inst - eng_dry, 0.0)

    structure = [
        _system(
            "ata53",
            "Fuselage",
            "ATA 53",
            [
                _part(
                    "frame",
                    fus,
                    0.20,
                    basis.format("fuselage"),
                    (0.45 * lf, 0, 0),
                    instances=frames,
                    envelope=(0.03, s.fuselage_width, h),
                ),
                _part(
                    "stringer",
                    fus,
                    0.10,
                    basis.format("fuselage"),
                    (0.5 * lf, 0, 0),
                    instances=16,
                    envelope=(0.7 * lf, 0.02, 0.02),
                ),
                _part(
                    "fuselage_skin",
                    fus,
                    0.40,
                    basis.format("fuselage"),
                    (0.45 * lf, 0, 0),
                    envelope=(lf, s.fuselage_width, h),
                ),
                _part("firewall", fus, 0.05, basis.format("fuselage"), (1.0, 0, 0)),
                _part(
                    "cabin_floor",
                    fus,
                    0.08,
                    basis.format("fuselage"),
                    (s.wing_x + 0.6, 0, -0.35 * h),
                ),
                _part(
                    "door", fus, 0.07, basis.format("fuselage"), (s.wing_x + 0.4, 0, 0), instances=2
                ),
                _part(
                    "windscreen", fus, 0.06, basis.format("fuselage"), (s.wing_x - 0.3, 0, 0.3 * h)
                ),
                _part("tail_cone", fus, 0.04, basis.format("fuselage"), (0.85 * lf, 0, 0)),
            ],
            functions=("carry structural loads", "protect occupants"),
        ),
        _system(
            "ata57",
            "Wings",
            "ATA 57",
            [
                _part(
                    "spar",
                    wing,
                    0.18,
                    basis.format("wing"),
                    (s.wing_x + 0.25 * s.wing_root_chord, 0, z_wing),
                    idx="_front",
                    instances=2,
                ),
                _part(
                    "spar",
                    wing,
                    0.10,
                    basis.format("wing"),
                    (s.wing_x + 0.7 * s.wing_root_chord, 0, z_wing),
                    idx="_rear",
                    instances=2,
                ),
                _part(
                    "rib",
                    wing,
                    0.15,
                    basis.format("wing"),
                    (x_wing, 0, z_wing),
                    instances=2 * rib_pairs,
                ),
                _part(
                    "wing_skin",
                    wing,
                    0.35,
                    basis.format("wing"),
                    (x_wing, 0, z_wing),
                    envelope=(s.wing_root_chord, s.wing_span, 0.15),
                ),
                _part(
                    "leading_edge",
                    wing,
                    0.06,
                    basis.format("wing"),
                    (s.wing_x + 0.05, 0, z_wing),
                    instances=2,
                ),
                _part(
                    "wing_tip", wing, 0.02, basis.format("wing"), (x_wing, 0, z_wing), instances=2
                ),
                _part(
                    "aileron",
                    wing,
                    0.07,
                    basis.format("wing"),
                    (s.wing_x + 0.85 * s.wing_root_chord, 0, z_wing),
                    instances=2,
                ),
                _part(
                    "flap",
                    wing,
                    0.07,
                    basis.format("wing"),
                    (s.wing_x + 0.85 * s.wing_root_chord, 0, z_wing),
                    instances=2,
                ),
            ],
            functions=("generate lift",),
        ),
        _system(
            "ata55",
            "Stabilisers",
            "ATA 55",
            [
                _part("stabiliser", ht, 0.70, basis.format("horizontal tail"), (x_ht, 0, z_ht)),
                _part(
                    "elevator",
                    ht,
                    0.30,
                    basis.format("horizontal tail"),
                    (x_ht + 0.4 * s.htail_root_chord, 0, z_ht),
                ),
                _part("fin", vt, 0.70, basis.format("vertical tail"), (x_vt, 0, 0.5 * h + 0.5)),
                _part(
                    "rudder",
                    vt,
                    0.30,
                    basis.format("vertical tail"),
                    (x_vt + 0.4 * s.fin_root_chord, 0, 0.5 * h + 0.5),
                ),
            ],
            functions=("control attitude and trajectory",),
        ),
    ]
    gear_total = gear_mlg + gear_nlg
    gear = _system(
        "ata32",
        "Landing gear",
        "ATA 32",
        [
            _part(
                "main_leg",
                gear_mlg,
                0.55,
                basis.format("main gear"),
                (x_main, 0, -0.9 * h),
                instances=2,
            ),
            _part(
                "main_wheel",
                gear_mlg,
                0.45,
                basis.format("main gear"),
                (x_main, 0, -1.1 * h),
                instances=2,
            ),
            _part(
                "nose_leg",
                gear_nlg,
                0.60,
                basis.format("nose gear"),
                (0.75, 0, -0.8 * h),
                applicability="undercarriage == 'Tricycle'",
            ),
            _part(
                "nose_wheel",
                gear_nlg,
                0.40,
                basis.format("nose gear"),
                (0.75, 0, -1.05 * h),
                applicability="undercarriage == 'Tricycle'",
            ),
            _part(
                "tailwheel",
                gear_nlg,
                0.25,
                "a nose gear (assumed)",
                (lf - 0.4, 0, -0.4 * h),
                applicability="undercarriage == 'Tailwheel'",
            ),
            _part(
                "retraction",
                gear_total,
                0.14,
                "the gear groups (assumed)",
                (x_main - 0.3, 0, -0.5 * h),
                applicability="gear == 'Retractable'",
            ),
        ],
        functions=("support on the ground",),
    )
    power = _system(
        "ata71",
        "Powerplant",
        "ATA 71-80",
        [
            _part("engine", eng_dry, 1.0, engine_basis, (0.75, 0, 0)),
            _part(
                "propeller", rest, 0.35, "the installation (Raymer installed engine)", (0.05, 0, 0)
            ),
            _part("engine_mount", rest, 0.15, "the installation", (1.0, 0, 0)),
            _part("cowling", rest, 0.20, "the installation", (0.6, 0, 0.1)),
            _part("exhaust", rest, 0.10, "the installation", (0.8, 0, -0.3 * h)),
            _part("engine_accessories", rest, 0.20, "the installation", (0.9, 0, 0)),
        ],
        functions=("provide thrust",),
    )
    fs, fc = g["fuel_system"], g["flight_controls"]
    systems = [
        _system(
            "ata28",
            "Fuel",
            "ATA 28",
            [
                _part(
                    "fuel_tank",
                    fs,
                    0.55,
                    basis.format("fuel system"),
                    (x_wing, 0, z_wing),
                    instances=2,
                ),
                _part("fuel_lines", fs, 0.20, basis.format("fuel system"), (s.wing_x, 0, 0)),
                _part("fuel_pump", fs, 0.15, basis.format("fuel system"), (1.2, 0, -0.2 * h)),
                _part("fuel_gauging", fs, 0.10, basis.format("fuel system"), (x_wing, 0, z_wing)),
            ],
            functions=("store and supply fuel",),
        ),
        _system(
            "ata27",
            "Flight controls",
            "ATA 27",
            [
                _part(
                    "control_column",
                    fc,
                    0.20,
                    basis.format("flight controls"),
                    (x_seat1 - 0.5, 0, 0),
                    instances=2,
                ),
                _part(
                    "rudder_pedals",
                    fc,
                    0.15,
                    basis.format("flight controls"),
                    (x_seat1 - 0.9, 0, -0.3 * h),
                    instances=2,
                ),
                _part(
                    "control_cables", fc, 0.30, basis.format("flight controls"), (0.6 * lf, 0, 0)
                ),
                _part("pushrods", fc, 0.20, basis.format("flight controls"), (0.5 * lf, 0, 0)),
                _part("trim", fc, 0.15, basis.format("flight controls"), (0.75 * lf, 0, 0)),
            ],
            functions=("control attitude and trajectory",),
        ),
        _system(
            "ata29",
            "Hydraulics (brakes)",
            "ATA 29",
            [
                _part(
                    "brake_hydraulics",
                    g["hydraulics"],
                    1.0,
                    basis.format("hydraulics"),
                    (x_main - 0.5, 0, -0.5 * h),
                ),
            ],
        ),
        _system(
            "ata24",
            "Electrical",
            "ATA 24",
            [
                _part("alternator", g["electrical"], 0.25, basis.format("electrical"), (0.7, 0, 0)),
                _part("battery", g["electrical"], 0.35, basis.format("electrical"), (1.2, 0, 0)),
                _part(
                    "harness", g["electrical"], 0.30, basis.format("electrical"), (0.35 * lf, 0, 0)
                ),
                _part(
                    "electrical_bus",
                    g["electrical"],
                    0.10,
                    basis.format("electrical"),
                    (x_seat1 - 0.6, 0, 0),
                ),
            ],
            functions=("supply electrical power",),
        ),
        _system(
            "ata34",
            "Avionics",
            "ATA 22/23/31/34",
            [
                _part(
                    "displays",
                    g["avionics"],
                    0.50,
                    basis.format("avionics"),
                    (x_seat1 - 0.6, 0, 0.1 * h),
                ),
                _part(
                    "radios", g["avionics"], 0.30, basis.format("avionics"), (x_seat1 - 0.6, 0, 0)
                ),
                _part(
                    "pitot_static",
                    g["avionics"],
                    0.20,
                    basis.format("avionics"),
                    (x_wing, 0, z_wing),
                ),
            ],
            functions=("navigate and communicate",),
        ),
        _system(
            "ata25",
            "Cabin and equipment",
            "ATA 25",
            [
                _part(
                    "seat",
                    g["furnishings"],
                    0.60,
                    basis.format("furnishings"),
                    ((x_seat1 + x_seat2) / 2, 0, -0.2 * h),
                    instances=4,
                ),
                _part(
                    "restraints",
                    g["furnishings"],
                    0.10,
                    basis.format("furnishings"),
                    ((x_seat1 + x_seat2) / 2, 0, 0),
                    instances=4,
                ),
                _part(
                    "linings",
                    g["furnishings"],
                    0.20,
                    basis.format("furnishings"),
                    (s.wing_x + 0.6, 0, 0),
                ),
                _part(
                    "baggage",
                    g["furnishings"],
                    0.10,
                    basis.format("furnishings"),
                    (x_seat2 + 0.8, 0, -0.2 * h),
                ),
            ],
            functions=("protect occupants", "carry payload"),
        ),
    ]
    _engineer_wing(values, structure)  # level 2: spars, ribs and skins sized by the loads
    empty_children = [*structure, gear, power, *systems]
    opts = options(values)
    own = configure_tree(
        Node(id="empty", name="", kind="product", children=empty_children),
        current(values),
        opts.names(),
    )  # this design's own configuration
    empty = sum(n.mass for n in own.walk()) if own is not None else 0.0
    payload = s.mtow - empty - s.fuel_mass
    load = _system("load", "Fuel, crew and payload", "Useful load", [
        Node(id="fuel", name="Fuel", kind="system", code="Useful load", mass=s.fuel_mass,
             mass_source="estimated", basis="specified fuel mass", cg=(x_wing, 0, z_wing)),
        Node(id="payload", name="Crew, passengers and baggage", kind="system",
             code="Useful load", mass=max(payload, 0.0), mass_source="estimated",
             basis="MTOW less empty mass and fuel", cg=(s.wing_x + 0.55, 0, -0.1 * h)),
    ])  # fmt: skip
    return Node(id="aircraft", name=s.name, kind="product", code="Aircraft",
                budget=s.mtow, children=[*empty_children, load])  # fmt: skip


def checks(values: Values, root: RolledNode) -> list[Check]:
    s = ac.AircraftSpec.model_validate({k: v for k, v in values.items()
                                        if k in ac.AircraftSpec.model_fields})  # fmt: skip
    load = next(c for c in root.children if c.id == "load")
    empty = root.rollup.mass - load.rollup.mass
    payload = next(c for c in load.children if c.id == "payload").rollup.mass
    out = [Check(id="empty_mass", label="Empty mass", status="pass",
                 message=f"{empty:.0f} kg estimated ({empty / s.mtow:.0%} of MTOW), Raymer GA "
                 "group weights; conceptual accuracy, typically within 10-20 %")]  # fmt: skip
    if payload < PILOT:
        out.append(Check(id="useful_load", label="Useful load", status="fail",
                         message=f"MTOW {s.mtow:.0f} kg leaves {max(payload, 0):.0f} kg after "
                         f"fuel: not enough for one {PILOT:.0f} kg occupant"))  # fmt: skip
    else:
        out.append(Check(id="useful_load", label="Useful load", status="pass",
                         message=f"{payload:.0f} kg for crew, passengers and baggage "
                         f"({payload / PILOT:.1f} standard occupants) with "
                         f"{s.fuel_mass:.0f} kg fuel"))  # fmt: skip
    geo = ac.analyse(s)["geometry"]
    dx = root.rollup.cg[0] - s.x_cg
    pct = abs(dx) / geo["mac"]
    status = "pass" if pct <= 0.05 else "warn" if pct <= 0.25 else "fail"
    out.append(Check(id="cg", label="Centre of gravity", status=status,
                     message=f"breakdown CG at MTOW {root.rollup.cg[0]:.2f} m vs "
                     f"{s.x_cg:.2f} m in the specification ({dx:+.2f} m, {pct:.0%} MAC); "
                     "part positions are level-0 estimates; the stability analysis uses "
                     "the specification's value"))  # fmt: skip
    return out


def _engineer_wing(values: Values, structure: list[Node]) -> None:
    """Replace the allocated masses of the spars, ribs and skins with the masses sized from
    the governing load case (``structure.size_wing``) and raise them to level 2."""
    from autevra.modules.aircraft.structure import size_wing  # local: structure needs loads

    try:
        sized = size_wing(values)
    except (ValueError, ZeroDivisionError):
        return
    m = sized["masses_kg"]
    basis = (f"sized for {sized['governing_case']} ({sized['material']}, "
             f"{sized['basis']}, factor 1.5)")  # fmt: skip
    wing = next(c for c in structure if c.id == "ata57")
    computed = {"spar_front": 0.75 * (m["spar_caps"] + m["spar_web"]),
                "spar_rear": 0.25 * (m["spar_caps"] + m["spar_web"]),
                "rib": m["ribs"], "wing_skin": m["wing_skin"]}  # fmt: skip
    for part in wing.children:
        if part.id in computed:
            part.mass = computed[part.id]
            part.mass_source = "computed"
            part.basis = basis
            part.maturity = 2
