"""A parametric light aircraft: its geometry (as a Part Design part) and its conceptual
aerodynamics, stability and performance, every number computed from published methods.

Frame and units: the specification is in metres, kilograms and kilowatts; distances along
the aircraft are measured aft from the nose. The generated part follows Part Design's
frame (mm, X forward, Y left, Z up), the nose at the origin.

Methods:
- atmosphere: the International Standard Atmosphere troposphere;
- wing and tail lift slopes, spanwise loading and Oswald efficiency: lifting-line theory
  (``autevra.aero.lifting_line``);
- downwash gradient d(eps)/d(alpha) = 2 a_w / (pi AR_w);
- neutral point (stick fixed, fuselage contribution neglected):
  x_np = (a_w x_ac,w + eta a_t (S_t/S)(1 - d eps/d alpha) x_ac,t) /
         (a_w + eta a_t (S_t/S)(1 - d eps/d alpha)),  static margin (x_np - x_cg) / MAC;
- tail volume coefficients V_H = S_t l_t / (S MAC), V_V = S_v l_v / (S b);
- parasite drag: component build-up C_D0 = sum C_f FF Q S_wet / S (Raymer), turbulent
  skin friction C_f = 0.455 / (log10 Re)^2.58, form factors for wings and bodies, plus
  the fixed landing gear and 5 % for leakage and protuberances;
- polar C_D = C_D0 + C_L^2 / (pi AR e) with the aircraft's Oswald factor
  e = 1.78 (1 - 0.045 AR^0.68) - 0.64 (Raymer; at most the planform's lifting-line span
  efficiency); (L/D)max = sqrt(pi AR e / C_D0) / 2;
- stall speed from C_L,max = 0.9 c_l,max (sea level, flaps up);
- piston power lapse P = P_0 (1.132 sigma - 0.132) (Gagg and Ferrar);
- range and endurance by the Breguet equations for propeller aircraft at the cruise
  lift-to-drag ratio.

Limits: conceptual-design accuracy (typically within 10-20 % of flight data), low subsonic,
no flaps, propeller slipstream, compressibility or trim drag. Not for certification.
"""

import math

from pydantic import BaseModel, Field

from autevra.aero import lifting_line as ll

G = 9.80665


class AircraftSpec(BaseModel):
    name: str = "Light aircraft"
    # wing
    wing_span: float = Field(11.0, gt=1.0, le=80.0)
    wing_root_chord: float = Field(1.63, gt=0.1, le=15.0)
    wing_tip_chord: float = Field(1.13, ge=0.05, le=15.0)
    wing_sweep: float = Field(2.0, ge=-30.0, le=60.0)  # leading edge, degrees
    wing_dihedral: float = Field(2.0, ge=-10.0, le=15.0)
    wing_twist: float = Field(-3.0, ge=-10.0, le=5.0)
    wing_naca: str = Field("2412", pattern=r"^\d{4}$")
    wing_x: float = Field(2.25, ge=0.0, le=60.0)  # root leading edge aft of the nose, m
    high_wing: bool = True
    cl_max_section: float = Field(1.6, gt=0.5, le=3.0)
    # fuselage
    fuselage_length: float = Field(8.2, gt=1.0, le=80.0)
    fuselage_width: float = Field(1.15, gt=0.2, le=8.0)
    fuselage_height: float = Field(1.45, gt=0.2, le=8.0)
    # horizontal tail
    htail_span: float = Field(3.4, gt=0.2, le=30.0)
    htail_root_chord: float = Field(1.2, gt=0.05, le=10.0)
    htail_tip_chord: float = Field(0.8, gt=0.05, le=10.0)
    htail_x: float = Field(6.55, ge=0.0, le=80.0)
    t_tail: bool = False
    # vertical tail
    fin_height: float = Field(1.45, gt=0.2, le=20.0)
    fin_root_chord: float = Field(1.4, gt=0.05, le=10.0)
    fin_tip_chord: float = Field(0.7, gt=0.05, le=10.0)
    fin_sweep: float = Field(35.0, ge=0.0, le=70.0)
    fin_x: float = Field(6.45, ge=0.0, le=80.0)
    # propulsion, mass, mission
    power_kw: float = Field(134.0, gt=1.0, le=5000.0)
    prop_diameter: float = Field(1.9, gt=0.2, le=6.0)
    prop_efficiency: float = Field(0.8, gt=0.3, le=0.95)
    bsfc: float = Field(300.0, gt=150.0, le=600.0)  # g/kWh
    mtow: float = Field(1110.0, gt=10.0, le=100_000.0)  # kg
    fuel_mass: float = Field(130.0, ge=0.0, le=50_000.0)
    x_cg: float = Field(2.8, ge=0.0, le=80.0)  # m aft of the nose
    fixed_gear: bool = True
    tricycle: bool = True
    cruise_speed: float = Field(60.0, gt=10.0, le=250.0)  # m/s true
    cruise_altitude: float = Field(2400.0, ge=0.0, le=11_000.0)  # m


def isa(h: float) -> dict[str, float]:
    """Temperature (K), pressure (Pa), density (kg/m^3), viscosity (Pa s) and the speed of
    sound at altitude h (m) in the ISA troposphere."""
    t = 288.15 - 0.0065 * h
    p = 101_325.0 * (t / 288.15) ** 5.25588
    rho = p / (287.053 * t)
    mu = 1.458e-6 * t**1.5 / (t + 110.4)  # Sutherland
    return {"T": t, "p": p, "rho": rho, "mu": mu, "a": math.sqrt(1.4 * 287.053 * t),
            "sigma": rho / 1.225}  # fmt: skip


def _planform(span: float, root: float, tip: float, twist: float, naca: str) -> ll.Planform:
    alpha0, a0 = ll.naca_section(naca)
    return ll.Planform(span=span, root_chord=root, tip_chord=tip, twist=twist,
                       alpha0=alpha0, a0=a0)  # fmt: skip


def _mac_station(span_full: float, root: float, tip: float, x_le: float,
                 sweep: float) -> tuple[float, float, float]:  # fmt: skip
    """(MAC, x of its leading edge aft of the nose, its spanwise station)."""
    lam = tip / root
    mac = 2.0 / 3.0 * root * (1 + lam + lam**2) / (1 + lam)
    y = span_full / 6.0 * (1 + 2 * lam) / (1 + lam)
    return mac, x_le + y * math.tan(math.radians(sweep)), y


def _cf(re: float) -> float:
    return 0.455 / math.log10(re) ** 2.58


def _wing_ff(tc: float, mach: float, sweep: float) -> float:
    return (1 + 0.6 / 0.3 * tc + 100 * tc**4) * 1.34 * mach**0.18 * math.cos(
        math.radians(sweep)) ** 0.28  # fmt: skip


def analyse(spec: AircraftSpec) -> dict:
    air = isa(spec.cruise_altitude)
    rho, v = air["rho"], spec.cruise_speed
    q = 0.5 * rho * v**2
    mach = v / air["a"]
    w = spec.mtow * G
    # --- wing and tails by lifting line
    wing = _planform(spec.wing_span, spec.wing_root_chord, spec.wing_tip_chord,
                     spec.wing_twist, spec.wing_naca)  # fmt: skip
    htail = _planform(spec.htail_span, spec.htail_root_chord, spec.htail_tip_chord, 0.0, "0012")
    s, ar = wing.area, wing.aspect_ratio
    a_w, a_t = ll.lift_slope(wing), ll.lift_slope(htail)
    mac, x_mac, y_mac = _mac_station(spec.wing_span, spec.wing_root_chord,
                                     spec.wing_tip_chord, spec.wing_x, spec.wing_sweep)  # fmt: skip
    mac_t, x_mac_t, _ = _mac_station(spec.htail_span, spec.htail_root_chord,
                                     spec.htail_tip_chord, spec.htail_x, 8.0)  # fmt: skip
    s_t = htail.area
    x_ac_w, x_ac_t = x_mac + 0.25 * mac, x_mac_t + 0.25 * mac_t
    l_t = x_ac_t - spec.x_cg
    fin_area = spec.fin_height * (spec.fin_root_chord + spec.fin_tip_chord) / 2
    mac_v, x_mac_v, _ = _mac_station(2 * spec.fin_height, spec.fin_root_chord,
                                     spec.fin_tip_chord, spec.fin_x, spec.fin_sweep)  # fmt: skip
    l_v = x_mac_v + 0.25 * mac_v - spec.x_cg
    v_h, v_v = s_t * l_t / (s * mac), fin_area * l_v / (s * spec.wing_span)
    # --- stability
    eta = 0.9  # tail dynamic-pressure ratio
    deps = 2 * a_w / (math.pi * ar)
    tail = eta * a_t * (s_t / s) * (1 - deps)
    x_np = (a_w * x_ac_w + tail * x_ac_t) / (a_w + tail)
    margin = (x_np - spec.x_cg) / mac
    # --- cruise lift and the spanwise loading
    cl = w / (q * s)
    alpha_root = math.degrees(cl / a_w) + (math.degrees(-ll.solve(wing, 0.0).cl / a_w))
    loading = ll.solve(wing, alpha_root)
    e_span = loading.e  # the planform's span efficiency (lifting line)
    # the whole aircraft's Oswald factor (fuselage and viscous losses): Raymer's estimate
    # for straight wings, never above the planform's own efficiency
    e = min(e_span, 1.78 * (1 - 0.045 * ar**0.68) - 0.64)
    # --- parasite drag build-up
    tc_w = int(spec.wing_naca[2:]) / 100.0
    exposed = s - spec.fuselage_width * spec.wing_root_chord
    comps = []

    def add(name: str, length: float, swet: float, ff: float, qf: float) -> None:
        re = rho * v * length / air["mu"]
        cf = _cf(re)
        comps.append({"name": name, "re": re, "cf": cf, "ff": ff, "q": qf, "s_wet": swet,
                      "cd0": cf * ff * qf * swet / s})  # fmt: skip

    add("wing", mac, exposed * (1.977 + 0.52 * tc_w), _wing_ff(tc_w, mach, spec.wing_sweep), 1.0)
    add("horizontal tail", mac_t, s_t * (1.977 + 0.52 * 0.12), _wing_ff(0.12, mach, 8.0), 1.04)
    add("fin", mac_v, fin_area * (1.977 + 0.52 * 0.12),
        _wing_ff(0.12, mach, spec.fin_sweep), 1.04)  # fmt: skip
    d_eq = math.sqrt(spec.fuselage_width * spec.fuselage_height)
    f = spec.fuselage_length / d_eq
    add("fuselage", spec.fuselage_length, 0.75 * math.pi * d_eq * spec.fuselage_length,
        1 + 60 / f**3 + f / 400, 1.0)  # fmt: skip
    gear = (0.18 if spec.fixed_gear else 0.0) / s  # D/q of a faired fixed tricycle gear, m^2
    cd0 = 1.05 * (sum(c["cd0"] for c in comps) + gear)
    cd = cd0 + cl**2 / (math.pi * ar * e)
    drag = q * s * cd
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)
    v_ldmax = math.sqrt(2 * w / (rho * s) * math.sqrt(1 / (math.pi * ar * e * cd0)))
    # --- performance
    p_req = drag * v / spec.prop_efficiency / 1000.0  # kW
    p_avail = spec.power_kw * max(1.132 * air["sigma"] - 0.132, 0.0)
    cl_max = 0.9 * spec.cl_max_section
    v_stall = math.sqrt(2 * w / (1.225 * s * cl_max))
    c_spec = spec.bsfc / 1000.0 / 3.6e6  # kg per joule of shaft work
    w1 = (spec.mtow - spec.fuel_mass) * G
    ratio = w / w1 if w1 > 0 else 1.0
    range_m = spec.prop_efficiency / (c_spec * G) * (cl / cd) * math.log(ratio)
    endurance = range_m / v
    checks = _checks(spec, margin, v_h, v_v, v_stall, p_req, p_avail, w / s)
    return {
        "atmosphere": air | {"altitude": spec.cruise_altitude, "mach": mach, "q": q},
        "geometry": {
            "wing_area": s,
            "aspect_ratio": ar,
            "taper": wing.taper,
            "mac": mac,
            "mac_x": x_mac,
            "mac_y": y_mac,
            "htail_area": s_t,
            "fin_area": fin_area,
            "tail_arm": l_t,
            "fin_arm": l_v,
            "wetted_area": sum(c["s_wet"] for c in comps),
        },
        "aero": {
            "wing_lift_slope": a_w,
            "tail_lift_slope": a_t,
            "downwash_gradient": deps,
            "oswald_e": e,
            "span_efficiency": e_span,
            "cl_cruise": cl,
            "alpha_cruise": alpha_root,
            "cd0": cd0,
            "cd_cruise": cd,
            "l_over_d": cl / cd,
            "ld_max": ld_max,
            "v_ld_max": v_ldmax,
            "zero_lift_angle": wing.alpha0,
            "components": comps,
            "gear_cd0": gear,
            "span_y": loading.y.tolist(),
            "span_cl": loading.cl_local.tolist(),
            "polar": [
                {"cl": c, "cd": cd0 + c**2 / (math.pi * ar * e)}
                for c in [i * 0.05 for i in range(0, int(cl_max / 0.05) + 1)]
            ],
        },  # fmt: skip
        "stability": {
            "x_ac_wing": x_ac_w,
            "x_ac_tail": x_ac_t,
            "x_np": x_np,
            "x_cg": spec.x_cg,
            "static_margin": margin,
            "v_h": v_h,
            "v_v": v_v,
            "eta": eta,
        },
        "performance": {
            "wing_loading": spec.mtow / s,
            "power_loading": spec.mtow / spec.power_kw,
            "drag": drag,
            "power_required": p_req,
            "power_available": p_avail,
            "v_stall": v_stall,
            "cl_max": cl_max,
            "range_km": range_m / 1000.0,
            "endurance_h": endurance / 3600.0,
        },
        "checks": checks,
        "assumptions": [
            "Conceptual design methods (lifting line, Raymer component drag build-up, Breguet): "
            "expect 10-20 % against flight data.",
            "Low subsonic, clean (no flaps), no propeller slipstream, trim drag or "
            "compressibility; fuselage moment and downwash lag neglected in the neutral point.",
            "Fully turbulent skin friction; tail dynamic-pressure ratio 0.9; horizontal tail "
            "NACA 0012.",
            "Design-guidance ranges come from conceptual-design texts; not a certification "
            "analysis.",
        ],
    }


def _checks(spec: AircraftSpec, margin: float, v_h: float, v_v: float, v_stall: float,
            p_req: float, p_avail: float, w_s: float) -> list[dict]:  # fmt: skip
    """Design guidance: pass, warn or fail with the value and the expected range."""

    def check(name: str, value: float, lo: float, hi: float, unit: str, hard: bool,
              why: str) -> dict:  # fmt: skip
        ok = lo <= value <= hi
        return {"name": name, "value": value, "range": [lo, hi], "unit": unit,
                "status": "pass" if ok else ("fail" if hard else "warn"), "why": why}  # fmt: skip

    return [
        check("Static margin", 100 * margin, 5.0, 25.0, "% MAC", True,
              "positive and modest: stable without heavy stick forces"),
        check("Horizontal tail volume", v_h, 0.45, 1.0, "", False,
              "general aviation designs are typically near 0.7"),
        check("Vertical tail volume", v_v, 0.025, 0.07, "", False,
              "general aviation designs are typically near 0.04"),
        check("Stall speed (sea level, clean)", v_stall / 0.514444, 0.0, 61.0, "kt", False,
              "single-engine aeroplanes of this class stall at or below 61 kt"),
        check("Power margin at cruise", p_avail - p_req, 0.0, 1e9, "kW", True,
              "the engine must provide the power the cruise needs at altitude"),
    ]  # fmt: skip


def geometry(spec: AircraftSpec) -> dict:
    """The aircraft as a Part Design document (mm): fuselage loft, wing, tails, propeller
    disc and spinner, and the landing gear."""
    mm = 1000.0
    length, wid, hei = (
        spec.fuselage_length * mm,
        spec.fuselage_width * mm,
        spec.fuselage_height * mm,
    )
    r = min(wid, hei) / 2 - 1
    sections = [
        {"z": 0, "width": 0.3 * wid, "height": 0.3 * hei, "radius": 0.15 * min(wid, hei) - 1},
        {"z": 0.16 * length, "width": wid, "height": 0.9 * hei, "radius": 0.9 * r},
        {"z": 0.45 * length, "width": wid, "height": hei, "radius": r},
        {"z": length, "width": 0.12 * wid, "height": 0.35 * hei, "radius": 0.05 * min(wid, hei)},
    ]  # fmt: skip
    wing_z = (0.42 if spec.high_wing else -0.38) * hei
    tail_z = 0.1 * hei + (spec.fin_height * mm * 0.95 if spec.t_tail else 0.0)
    features: list[dict] = [
        {"id": "fuselage", "name": "Fuselage", "type": "loft", "at": {"ry": -90},
         "sections": sections},
        {"id": "wing", "name": "Wing", "type": "wing", "naca": spec.wing_naca,
         "root_chord": spec.wing_root_chord * mm, "tip_chord": spec.wing_tip_chord * mm,
         "span": spec.wing_span / 2 * mm, "sweep": spec.wing_sweep,
         "dihedral": spec.wing_dihedral, "twist": spec.wing_twist,
         "at": {"x": -spec.wing_x * mm, "z": wing_z}},
        {"id": "tailplane", "name": "Horizontal tail", "type": "wing", "naca": "0012",
         "root_chord": spec.htail_root_chord * mm, "tip_chord": spec.htail_tip_chord * mm,
         "span": spec.htail_span / 2 * mm, "sweep": 8, "dihedral": 0, "twist": 0,
         "at": {"x": -spec.htail_x * mm, "z": tail_z}},
        {"id": "fin", "name": "Fin", "type": "wing", "naca": "0012",
         "root_chord": spec.fin_root_chord * mm, "tip_chord": spec.fin_tip_chord * mm,
         "span": spec.fin_height * mm, "sweep": spec.fin_sweep, "dihedral": 0, "twist": 0,
         "both_sides": False, "at": {"x": -spec.fin_x * mm, "z": 0.2 * hei, "rx": 90}},
        {"id": "spinner", "name": "Spinner", "type": "sphere", "radius": 0.14 * min(wid, hei),
         "at": {"x": 40}},
        {"id": "propeller", "name": "Propeller (two blades)", "type": "box",
         "size": [35, spec.prop_diameter * mm, 130], "at": {"x": 70, "rx": 15}},
    ]  # fmt: skip
    gear_z = -hei / 2 - 0.45 * mm
    wheels = ([(-0.08 * length, 0.0, "nose")] if spec.tricycle else
              [(-0.92 * length, 0.0, "tail")])  # fmt: skip
    main_x = -(spec.x_cg + (0.35 if spec.tricycle else -0.45)) * mm
    wheels += [(main_x, 1.1 * wid, "left main"), (main_x, -1.1 * wid, "right main")]
    for i, (x, y, label) in enumerate(wheels):
        small = label == "tail"
        rad = 120 if small else 200
        z = gear_z + (0.25 * mm if small else 0.0)
        features.append({"id": f"wheel{i}", "name": f"{label.title()} wheel", "type": "cylinder",
                         "radius": rad, "height": 120, "axis": "y",
                         "at": {"x": x, "y": y, "z": z}})  # fmt: skip
        # a slim sprung leg from the fuselage belly to the wheel hub
        y0, z0 = 0.0, -hei / 2 + 60
        dy, dz = y - y0, z - z0
        leg = math.hypot(dy, dz)
        features.append({"id": f"leg{i}", "name": f"{label.title()} leg", "type": "box",
                         "size": [70, leg, 35],
                         "at": {"x": x, "y": (y + y0) / 2, "z": (z + z0) / 2,
                                "rx": math.degrees(math.atan2(dz, dy))}})  # fmt: skip
    return {"name": spec.name, "color": [0.9, 0.91, 0.93], "finish": "paint", "features": features}
