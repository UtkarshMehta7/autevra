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

Turbofan transports (propulsion "turbofan") replace four of these: lift slopes by the
compressible swept-wing formula of the DATCOM, wave drag by the Korn equation, maximum
thrust by Howe's lapse model and range by the jet Breguet equation; see those functions.
Their spanwise loading plot still comes from the unswept lifting line (indicative only),
and high-lift devices, trim drag and engine-out cases are not modelled.

Limits: conceptual-design accuracy (typically within 10-20 % of flight data), low subsonic,
no flaps, propeller slipstream, compressibility or trim drag. Not for certification.
"""

import math
from typing import Literal

from pydantic import BaseModel, Field, model_validator

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
    power_kw: float = Field(134.0, gt=1.0, le=5000.0)  # piston aircraft
    prop_diameter: float = Field(1.9, gt=0.2, le=6.0)
    prop_efficiency: float = Field(0.8, gt=0.3, le=0.95)
    bsfc: float = Field(300.0, gt=150.0, le=600.0)  # g/kWh
    mtow: float = Field(1110.0, gt=10.0, le=700_000.0)  # kg
    fuel_mass: float = Field(130.0, ge=0.0, le=400_000.0)
    x_cg: float = Field(2.8, ge=0.0, le=80.0)  # m aft of the nose
    fixed_gear: bool = True
    tricycle: bool = True
    cruise_speed: float = Field(60.0, gt=10.0, le=300.0)  # m/s true
    cruise_altitude: float = Field(2400.0, ge=0.0, le=15_000.0)  # m
    # turbofan transports (propulsion "turbofan"); ignored for piston aircraft
    propulsion: Literal["piston", "turbofan"] = "piston"
    engines: int = Field(1, ge=1, le=4)
    thrust_kn: float = Field(0.0, ge=0.0, le=600.0)  # static sea-level thrust per engine
    bypass_ratio: float = Field(8.0, ge=3.0, le=12.0)
    tsfc: float = Field(15.5, gt=5.0, le=40.0)  # cruise, mg of fuel per newton-second
    nacelle_diameter: float = Field(2.5, gt=0.3, le=5.0)
    nacelle_length: float = Field(4.5, gt=0.5, le=10.0)
    engine_span_fraction: float = Field(0.33, ge=0.1, le=0.8)  # inboard engine, of semi-span
    korn_factor: float = Field(0.95, ge=0.85, le=0.97)  # 0.87 conventional, 0.95 supercritical

    @model_validator(mode="after")
    def _propulsion(self) -> "AircraftSpec":
        if self.propulsion == "turbofan" and self.thrust_kn <= 0:
            raise ValueError("a turbofan aircraft needs the static thrust per engine")
        if self.propulsion == "piston" and self.cruise_altitude > 11_000:
            raise ValueError("the piston power model ends at 11 000 m")
        return self

    @property
    def jet(self) -> bool:
        return self.propulsion == "turbofan"


def isa(h: float) -> dict[str, float]:
    """Temperature (K), pressure (Pa), density (kg/m^3), viscosity (Pa s) and the speed of
    sound at altitude h (m) in the ISA troposphere and lower stratosphere (to 20 km)."""
    t = 288.15 - 0.0065 * min(h, 11_000.0)
    p = 101_325.0 * (t / 288.15) ** 5.25588
    if h > 11_000.0:  # isothermal lower stratosphere
        p *= math.exp(-G * (h - 11_000.0) / (287.053 * t))
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
    lam_w = spec.wing_tip_chord / spec.wing_root_chord
    sweep_c4 = _sweep_at(spec.wing_sweep, 0.25, spec.wing_root_chord, lam_w, spec.wing_span)
    if spec.jet:  # swept wings at high subsonic speed: lifting line does not apply
        a_w = swept_lift_slope(ar, mach, _sweep_at(spec.wing_sweep, 0.5, spec.wing_root_chord,
                                                   lam_w, spec.wing_span))  # fmt: skip
        a_t = swept_lift_slope(htail.aspect_ratio, mach, 25.0)
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
    if spec.jet:
        fine = spec.nacelle_length / spec.nacelle_diameter
        for i in range(spec.engines):
            add(
                f"nacelle {i + 1}",
                spec.nacelle_length,
                math.pi * spec.nacelle_diameter * spec.nacelle_length,
                1 + 0.35 / fine,
                1.3,
            )
    gear = (0.18 if spec.fixed_gear else 0.0) / s  # D/q of a faired fixed tricycle gear, m^2
    cd0 = 1.05 * (sum(c["cd0"] for c in comps) + gear)
    if spec.jet:
        # Oswald factor of a transport (Kroo): inviscid span efficiency u = 0.99, fuselage
        # interference s = 1 - 2 (d/b)^2, and lift-dependent viscous drag K C_D0 C_L^2 with
        # K = 0.38:  e = 1 / (pi AR K C_D0 + 1 / (u s)). Raymer's straight-wing estimate
        # above is for light aircraft and is not used here.
        s_f = 1 - 2 * (spec.fuselage_width / spec.wing_span) ** 2
        e = 1 / (math.pi * ar * 0.38 * cd0 + 1 / (0.99 * s_f))
    wave = korn_wave_drag(mach, cl, tc_w, sweep_c4, spec.korn_factor) if spec.jet else None
    cd_wave = wave["cd_wave"] if wave else 0.0
    cd = cd0 + cl**2 / (math.pi * ar * e) + cd_wave
    drag = q * s * cd
    ld_max = 0.5 * math.sqrt(math.pi * ar * e / cd0)
    v_ldmax = math.sqrt(2 * w / (rho * s) * math.sqrt(1 / (math.pi * ar * e * cd0)))
    # --- performance
    p_req = drag * v / spec.prop_efficiency / 1000.0  # kW
    p_avail = spec.power_kw * max(1.132 * air["sigma"] - 0.132, 0.0)
    cl_max = 0.9 * spec.cl_max_section * (math.cos(math.radians(sweep_c4)) if spec.jet else 1.0)
    v_stall = math.sqrt(2 * w / (1.225 * s * cl_max))
    w1 = (spec.mtow - spec.fuel_mass) * G
    ratio = w / w1 if w1 > 0 else 1.0
    if spec.jet:
        # Breguet for jets: thrust-specific consumption c in kg of fuel per newton-second
        c_jet = spec.tsfc * 1e-6
        endurance = (cl / cd) / (c_jet * G) * math.log(ratio)
        range_m = endurance * v
        t_static = spec.engines * spec.thrust_kn * 1000.0
        t_avail = t_static * thrust_lapse(mach, air["sigma"], spec.bypass_ratio)
        jet = {"thrust_required_kn": drag / 1000.0, "thrust_available_kn": t_avail / 1000.0,
               "thrust_to_weight": t_static / w, "cd_wave": cd_wave} | (wave or {})  # fmt: skip
        checks = _jet_checks(margin, v_h, v_v, v_stall, drag, t_avail, mach, wave or {},
                             t_static / w)  # fmt: skip
        climb = jet_climb(spec, w, s, cd0, math.pi * ar * e, tc_w, sweep_c4, cl_max)
    else:
        c_spec = spec.bsfc / 1000.0 / 3.6e6  # kg per joule of shaft work
        range_m = spec.prop_efficiency / (c_spec * G) * (cl / cd) * math.log(ratio)
        endurance = range_m / v
        jet = {}
        checks = _checks(spec, margin, v_h, v_v, v_stall, p_req, p_avail, w / s)
        climb = climb_performance(w, s, cd0, math.pi * ar * e, spec.power_kw,
                                  spec.prop_efficiency, cl_max, spec.cruise_altitude)  # fmt: skip
    # Tail and balance guidance: areas for typical volume coefficients, and the centre of
    # gravity range that keeps the static margin between 5 and 25 % MAC.
    sizing = {
        "htail_area_for_vh_0_7": 0.7 * s * mac / l_t if l_t > 0 else None,
        "fin_area_for_vv_0_04": 0.04 * s * spec.wing_span / l_v if l_v > 0 else None,
        "cg_aft_limit": x_np - 0.05 * mac,
        "cg_forward_limit": x_np - 0.25 * mac,
    }
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
            "propulsion": spec.propulsion,
            **jet,
        },
        "climb": climb,
        "sizing": sizing,
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


def _sweep_at(sweep_le: float, fraction: float, root: float, taper: float,
              span: float) -> float:  # fmt: skip
    """Sweep (degrees) of the line at a chord fraction of a trapezoidal wing, from its
    leading-edge sweep."""
    return math.degrees(math.atan(math.tan(math.radians(sweep_le))
                                  - fraction * 2 * root * (1 - taper) / span))  # fmt: skip


def swept_lift_slope(aspect_ratio: float, mach: float, sweep_half_chord: float) -> float:
    """Lift-curve slope per radian of a swept wing in subsonic compressible flow (the
    Helmbold-Diederich form used in the USAF DATCOM, section lift slope 2 pi):
    a = 2 pi AR / (2 + sqrt(4 + AR^2 beta^2 (1 + tan^2 L / beta^2))), beta^2 = 1 - M^2."""
    beta2 = 1 - mach**2
    t2 = math.tan(math.radians(sweep_half_chord)) ** 2
    return 2 * math.pi * aspect_ratio / (2 + math.sqrt(4 + aspect_ratio**2 * (beta2 + t2)))


def korn_wave_drag(mach: float, cl: float, tc: float, sweep: float, kappa: float) -> dict:
    """Wave drag by the Korn equation with simple sweep theory (Mason): the drag-divergence
    Mach number M_dd = kappa / cos L - (t/c) / cos^2 L - C_L / (10 cos^3 L), the critical
    Mach number M_crit = M_dd - (0.1 / 80)^(1/3), and Lock's fourth-power rise
    C_D,wave = 20 (M - M_crit)^4 above it. ``kappa`` is the aerofoil technology factor."""
    c = math.cos(math.radians(sweep))
    m_dd = kappa / c - tc / c**2 - cl / (10 * c**3)
    m_crit = m_dd - (0.1 / 80) ** (1 / 3)
    return {"m_dd": m_dd, "m_crit": m_crit,
            "cd_wave": 20 * (mach - m_crit) ** 4 if mach > m_crit else 0.0}  # fmt: skip


def thrust_lapse(mach: float, sigma: float, bypass: float) -> float:
    """Maximum thrust of a high-bypass turbofan over its static sea-level thrust, by Howe's
    empirical model: tau = (K1 + K2 R + (K3 + K4 R) M) sigma^0.7 with R the bypass ratio.
    Coefficients for R of 3-6 and of 8, each for M below and above 0.4; an estimate of the
    installed engine's rating, to be replaced by the engine deck when one is available."""
    if bypass < 7.0:
        k = (1.0, 0.0, -0.6, -0.04) if mach < 0.4 else (0.88, -0.016, -0.3, 0.0)
    else:
        k = (1.0, 0.0, -0.595, -0.03) if mach < 0.4 else (0.89, -0.014, -0.3, 0.005)
    return max((k[0] + k[1] * bypass + (k[2] + k[3] * bypass) * mach) * sigma**0.7, 0.0)


def jet_climb(spec: AircraftSpec, weight: float, area: float, cd0: float, pi_ar_e: float,
              tc: float, sweep_c4: float, cl_max: float) -> dict:  # fmt: skip
    """Climb of a turbofan aircraft at maximum mass: rate of climb (T - D) V / W, best over
    speed at each altitude (between 1.2 times the stall speed and the cruise Mach number),
    and the ceilings where it falls to 1.5 m/s (300 ft/min, service) and to zero."""
    t_static = spec.engines * spec.thrust_kn * 1000.0
    m_cruise = spec.cruise_speed / isa(spec.cruise_altitude)["a"]

    def at(h: float) -> dict:
        air = isa(h)
        rho = air["rho"]
        v_lo = 1.2 * math.sqrt(2 * weight / (rho * area * cl_max))
        v_hi = m_cruise * air["a"]
        best = {"altitude": h, "v": v_lo, "roc": -1e9}
        for i in range(41):
            v = v_lo + (v_hi - v_lo) * i / 40 if v_hi > v_lo else v_lo
            m = v / air["a"]
            cl = weight / (0.5 * rho * v * v * area)
            cd = cd0 + cl**2 / pi_ar_e + korn_wave_drag(m, cl, tc, sweep_c4,
                                                        spec.korn_factor)["cd_wave"]  # fmt: skip
            drag = 0.5 * rho * v * v * area * cd
            roc = (t_static * thrust_lapse(m, air["sigma"], spec.bypass_ratio) - drag) * v / weight
            if roc > best["roc"]:
                best = {"altitude": h, "v": v, "roc": roc}
        return best

    def ceiling(target: float) -> float:
        top = 15_000.0
        if at(0.0)["roc"] <= target:
            return 0.0
        if at(top)["roc"] > target:
            return top
        lo, hi = 0.0, top
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if at(mid)["roc"] > target else (lo, mid)
        return 0.5 * (lo + hi)

    sea = at(0.0)
    return {
        "roc_sea_level": sea["roc"],
        "v_best_climb": sea["v"],
        "climb_gradient_sea_level": sea["roc"] / sea["v"],
        "roc_cruise_altitude": at(spec.cruise_altitude)["roc"],
        "service_ceiling": ceiling(1.5),
        "absolute_ceiling": ceiling(0.0),
        "curve": [at(float(h)) for h in range(0, 15_001, 1500)],
    }


def _jet_checks(margin: float, v_h: float, v_v: float, v_stall: float, drag: float,
                t_avail: float, mach: float, wave: dict, t_w: float) -> list[dict]:  # fmt: skip
    def check(name: str, value: float, lo: float, hi: float, unit: str, hard: bool,
              why: str) -> dict:  # fmt: skip
        ok = lo <= value <= hi
        return {"name": name, "value": value, "range": [lo, hi], "unit": unit,
                "status": "pass" if ok else ("fail" if hard else "warn"), "why": why}  # fmt: skip

    return [
        check("Static margin", 100 * margin, 5.0, 40.0, "% MAC", True,
              "positive: stable; transports fly at 10-35 % depending on loading"),
        check("Horizontal tail volume", v_h, 0.7, 1.3, "", False,
              "jet transports are typically near 1.0"),
        check("Vertical tail volume", v_v, 0.05, 0.12, "", False,
              "jet transports are typically near 0.08"),
        check("Thrust margin at cruise", (t_avail - drag) / 1000.0, 0.0, 1e9, "kN", True,
              "the engines must provide the cruise drag at altitude"),
        check("Cruise Mach against drag divergence", mach - wave.get("m_dd", 1.0), -1.0, 0.0,
              "", False, "cruising above the drag-divergence Mach number costs fuel quickly"),
        check("Static thrust to weight", t_w, 0.25, 0.45, "", False,
              "twin-engine transports are typically near 0.3"),
        check("Stall speed (sea level, clean)", v_stall / 0.514444, 0.0, 220.0, "kt", False,
              "clean stall of a transport at maximum mass; high-lift devices are not modelled"),
    ]  # fmt: skip


def climb_at(
    weight: float,
    area: float,
    cd0: float,
    pi_ar_e: float,
    power_kw: float,
    prop_efficiency: float,
    cl_max: float,
    altitude: float,
) -> dict:
    """Best rate of climb at an altitude: excess power over weight, maximised over speed.

    Power required P = 1/2 rho V^3 S C_D0 + 2 W^2 / (rho V S pi AR e); it is least at
    V_mp = sqrt(2 W / (rho S)) (1 / (3 C_D0 pi AR e))^(1/4). With constant propeller
    efficiency the available power does not depend on speed, so the best climb is at V_mp,
    or at 1.1 times the stall speed if that is faster.
    """
    air = isa(altitude)
    rho = air["rho"]
    v_mp = math.sqrt(2 * weight / (rho * area)) * (1 / (3 * cd0 * pi_ar_e)) ** 0.25
    v_stall = math.sqrt(2 * weight / (rho * area * cl_max))
    v = max(v_mp, 1.1 * v_stall)
    required = 0.5 * rho * v**3 * area * cd0 + 2 * weight**2 / (rho * v * area * pi_ar_e)
    available = prop_efficiency * power_kw * 1000.0 * max(1.132 * air["sigma"] - 0.132, 0.0)
    return {"altitude": altitude, "v": v, "v_min_power": v_mp, "roc": (available - required)
            / weight, "power_required_kw": required / 1000.0,
            "power_available_kw": available / 1000.0}  # fmt: skip


def climb_performance(
    weight: float,
    area: float,
    cd0: float,
    pi_ar_e: float,
    power_kw: float,
    prop_efficiency: float,
    cl_max: float,
    cruise_altitude: float,
) -> dict:
    """Rate of climb against altitude and the ceilings: service where the best rate of climb
    falls to 0.5 m/s (100 ft/min), absolute where it reaches zero (bisection; ISA
    troposphere, so ceilings above 11 km are reported as 11 km)."""
    args = (weight, area, cd0, pi_ar_e, power_kw, prop_efficiency, cl_max)

    def ceiling(target: float) -> float:
        if climb_at(*args, 0.0)["roc"] <= target:
            return 0.0
        if climb_at(*args, 11_000.0)["roc"] > target:
            return 11_000.0
        lo, hi = 0.0, 11_000.0
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if climb_at(*args, mid)["roc"] > target else (lo, mid)
        return 0.5 * (lo + hi)

    sea = climb_at(*args, 0.0)
    return {
        "roc_sea_level": sea["roc"],
        "v_best_climb": sea["v"],
        "climb_gradient_sea_level": sea["roc"] / sea["v"],
        "roc_cruise_altitude": climb_at(*args, cruise_altitude)["roc"],
        "service_ceiling": ceiling(0.5),
        "absolute_ceiling": ceiling(0.0),
        "curve": [climb_at(*args, h) for h in range(0, 11_001, 1000)],
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
    """The airframe as a Part Design document (mm): a smooth eight-station fuselage loft,
    the NACA wing and tails. ``parts`` adds the canopy, propeller, spinner and gear as
    separate coloured parts."""
    if spec.jet:
        return _jet_parts(spec)[0]
    mm = 1000.0
    length, wid, hei = (spec.fuselage_length * mm, spec.fuselage_width * mm,
                        spec.fuselage_height * mm)  # fmt: skip
    # (station / length, width / max width, height / max height): a rounded nose, a full
    # cabin and a tapering tail cone; each section nearly elliptical
    stations = (
        (0.0, 0.30, 0.34),
        (0.05, 0.64, 0.66),
        (0.13, 0.92, 0.88),
        (0.25, 1.0, 0.98),
        (0.45, 1.0, 1.0),
        (0.62, 0.80, 0.80),
        (0.80, 0.48, 0.58),
        (1.0, 0.13, 0.34),
    )
    sections = [{"z": t * length, "width": w * wid, "height": h * hei,
                 "radius": 0.47 * min(w * wid, h * hei)} for t, w, h in stations]  # fmt: skip
    wing_z = (0.42 if spec.high_wing else -0.38) * hei
    tail_z = 0.06 * hei + (spec.fin_height * mm * 0.95 if spec.t_tail else 0.0)
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
         "both_sides": False, "at": {"x": -spec.fin_x * mm, "z": 0.02 * hei, "rx": 90}},
    ]  # fmt: skip
    return {"name": spec.name, "color": [0.93, 0.94, 0.95], "finish": "paint",
            "features": features}  # fmt: skip


def _jet_parts(spec: AircraftSpec) -> list[dict]:
    """A turbofan transport as Part Design documents (mm): the airframe (circular fuselage
    with a rounded nose and a tapering tail, low swept wing, tails), flight-deck glazing,
    the nacelles and pylons under the wing, and retractable gear shown extended."""
    mm = 1000.0
    length, dia = spec.fuselage_length * mm, spec.fuselage_width * mm
    hei = spec.fuselage_height * mm
    # (station / length, size / diameter, centre height / diameter): nose, constant cabin,
    # then a tail cone swept up to clear the runway at rotation
    stations = ((0.0, 0.10, -0.10), (0.012, 0.36, -0.08), (0.035, 0.62, -0.05),
                (0.065, 0.84, -0.02), (0.105, 0.97, 0.0), (0.14, 1.0, 0.0), (0.68, 1.0, 0.0),
                (0.78, 0.86, 0.05), (0.88, 0.58, 0.15), (0.95, 0.34, 0.24),
                (1.0, 0.14, 0.30))  # fmt: skip
    # under the "ry": -90 placement a section's width is vertical and its height lateral
    sections = [{"z": t * length, "width": f * hei, "height": f * dia, "dx": c * hei,
                 "radius": 0.499 * f * min(dia, hei)} for t, f, c in stations]  # fmt: skip
    half = spec.wing_span / 2
    wing_z = (0.36 if spec.high_wing else -0.30) * hei
    tan_le = math.tan(math.radians(spec.wing_sweep))
    tan_di = math.tan(math.radians(spec.wing_dihedral))
    tail_z = 0.26 * hei + (spec.fin_height * mm * 0.95 if spec.t_tail else 0.0)
    airframe = {"name": spec.name, "color": [0.94, 0.95, 0.96], "finish": "paint", "features": [
        {"id": "fuselage", "name": "Fuselage", "type": "loft", "at": {"ry": -90},
         "sections": sections},
        {"id": "wing", "name": "Wing", "type": "wing", "naca": spec.wing_naca,
         "root_chord": spec.wing_root_chord * mm, "tip_chord": spec.wing_tip_chord * mm,
         "span": half * mm, "sweep": spec.wing_sweep, "dihedral": spec.wing_dihedral,
         "twist": spec.wing_twist, "at": {"x": -spec.wing_x * mm, "z": wing_z}},
        {"id": "tailplane", "name": "Horizontal tail", "type": "wing", "naca": "0010",
         "root_chord": spec.htail_root_chord * mm, "tip_chord": spec.htail_tip_chord * mm,
         "span": spec.htail_span / 2 * mm, "sweep": 37, "dihedral": 7, "twist": 0,
         "at": {"x": -spec.htail_x * mm, "z": tail_z}},
        {"id": "fin", "name": "Fin", "type": "wing", "naca": "0010",
         "root_chord": spec.fin_root_chord * mm, "tip_chord": spec.fin_tip_chord * mm,
         "span": spec.fin_height * mm, "sweep": spec.fin_sweep, "dihedral": 0, "twist": 0,
         "both_sides": False, "at": {"x": -spec.fin_x * mm, "z": 0.40 * hei, "rx": 90}},
    ]}  # fmt: skip

    # flight-deck glazing: a dark band that follows the nose, each section as wide as the
    # fuselage is at the band's height (plus 1 % so it shows through the skin)
    def body(t: float) -> tuple[float, float]:
        """Fuselage size factor and centre height (of the diameter) at a station."""
        for (t0, f0, c0), (t1, f1, c1) in zip(stations, stations[1:], strict=False):
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                return f0 + u * (f1 - f0), c0 + u * (c1 - c0)
        return 1.0, 0.0

    band_z, bands = 0.17 * hei, []
    for t, tall in ((0.026, 0.05), (0.038, 0.13), (0.052, 0.15), (0.064, 0.09)):
        f, c = body(t)
        up = band_z - c * hei
        reach = math.sqrt(max((f * dia / 2) ** 2 - (up * dia / hei) ** 2, (0.05 * dia) ** 2))
        bands.append({"z": (t - 0.026) * length, "width": tall * hei, "height": 2.02 * reach,
                      "radius": 0.3 * tall * hei})  # fmt: skip
    glazing = {"name": "Flight deck glazing", "color": [0.05, 0.07, 0.10], "finish": "glass",
               "features": [{"id": "glazing", "name": "Windscreen", "type": "loft",
                             "at": {"x": -0.026 * length, "z": band_z, "ry": -90},
                             "sections": bands}]}  # fmt: skip
    # engines: under the wing, symmetric pairs from the inboard station outward
    nd, nl = spec.nacelle_diameter * mm, spec.nacelle_length * mm
    pairs = max(spec.engines // 2, 1)
    nacelles, pylons, fans = [], [], []
    for i in range(pairs):
        frac = spec.engine_span_fraction + i * 0.28
        for side in (1, -1):
            y = side * frac * half * mm
            x_le = (spec.wing_x + frac * half * tan_le) * mm
            chord = (spec.wing_root_chord
                     + (spec.wing_tip_chord - spec.wing_root_chord) * frac) * mm  # fmt: skip
            z_wing = wing_z + frac * half * mm * tan_di
            x0, zc = -(x_le - 0.62 * nl), z_wing - 0.60 * nd
            tag = f"{i}{'l' if side > 0 else 'r'}"
            nacelles.append({"id": f"nacelle{tag}", "name": "Nacelle", "type": "loft",
                             "at": {"x": x0, "y": y, "z": zc, "ry": -90},
                             "sections": [
                                 {"z": 0, "width": 0.90 * nd, "height": 0.90 * nd,
                                  "radius": 0.449 * nd},
                                 {"z": 0.18 * nl, "width": nd, "height": nd, "radius": 0.499 * nd},
                                 {"z": 0.55 * nl, "width": 0.96 * nd, "height": 0.96 * nd,
                                  "radius": 0.479 * nd},
                                 {"z": 0.80 * nl, "width": 0.62 * nd, "height": 0.62 * nd,
                                  "radius": 0.309 * nd},
                                 {"z": nl, "width": 0.36 * nd, "height": 0.36 * nd,
                                  "radius": 0.179 * nd}]})  # fmt: skip
            fans.append({"id": f"fan{tag}", "name": "Fan face", "type": "cylinder",
                         "radius": 0.40 * nd, "height": 0.02 * nl, "axis": "x",
                         "at": {"x": x0 + 0.004 * nl, "y": y, "z": zc}})  # fmt: skip
            pylons.append({"id": f"pylon{tag}", "name": "Pylon", "type": "box",
                           "size": [0.55 * nl, 0.10 * nd, 0.42 * nd],
                           "at": {"x": -(x_le + 0.02 * chord), "y": y,
                                  "z": z_wing - 0.20 * nd}})  # fmt: skip
    if spec.engines % 2:  # a centre engine in the tail
        nacelles.append({"id": "nacellec", "name": "Centre nacelle", "type": "cylinder",
                         "radius": nd / 2, "height": nl, "axis": "x",
                         "at": {"x": -(spec.fin_x * mm), "z": 0.75 * hei}})  # fmt: skip
    engines = {"name": "Engines", "color": [0.80, 0.82, 0.85], "finish": "metal",
               "features": nacelles + pylons}  # fmt: skip
    fan_part = {"name": "Fan faces", "color": [0.07, 0.07, 0.08], "finish": "paint_matte",
                "features": fans}  # fmt: skip
    # gear: twin nose wheels and main bogies (two wheels per axle; three axles when heavy)
    rad = 0.105 * dia
    ground = -0.5 * hei - 0.36 * hei  # wheel-centre height
    axles = 3 if spec.mtow > 250_000 else 2 if spec.mtow > 40_000 else 1
    x_main = -(spec.x_cg + 0.045 * spec.fuselage_length) * mm
    y_main = 0.085 * spec.wing_span * mm
    legs, wheels = [], []

    def wheel(tag: str, x: float, y: float) -> None:
        wheels.append({"id": f"wheel{tag}", "name": "Wheel", "type": "revolve",
                       "points": [[0.38 * rad, -0.30 * rad], [0.85 * rad, -0.34 * rad],
                                  [rad, -0.22 * rad], [rad, 0.22 * rad],
                                  [0.85 * rad, 0.34 * rad], [0.38 * rad, 0.30 * rad]],
                       "at": {"x": x, "y": y, "z": ground, "rx": 90}})  # fmt: skip

    def leg(tag: str, x: float, y: float, top: float) -> None:
        legs.append({"id": f"leg{tag}", "name": "Strut", "type": "cylinder",
                     "radius": 0.16 * rad, "height": top - ground,
                     "at": {"x": x, "y": y, "z": (top + ground) / 2}})  # fmt: skip

    x_nose = -0.075 * length
    for j, y in enumerate((-0.42 * rad, 0.42 * rad)):
        wheel(f"n{j}", x_nose, y)
    leg("n", x_nose, 0.0, -0.40 * hei)
    for side, name in ((1, "l"), (-1, "r")):
        for a in range(axles):
            x = x_main + (a - (axles - 1) / 2) * 2.25 * rad
            for j, dy in enumerate((-0.55 * rad, 0.55 * rad)):
                wheel(f"m{name}{a}{j}", x, side * y_main + dy)
        leg(f"m{name}", x_main, side * y_main, wing_z + 0.085 * spec.wing_span * mm * tan_di)
        if axles > 1:
            legs.append({"id": f"bogie{name}", "name": "Bogie beam", "type": "box",
                         "size": [(axles - 1) * 2.25 * rad + 0.5 * rad, 0.22 * rad, 0.22 * rad],
                         "at": {"x": x_main, "y": side * y_main, "z": ground}})  # fmt: skip
    gear = {"name": "Landing gear", "color": [0.55, 0.57, 0.6], "finish": "metal", "features": legs}
    tyres = {"name": "Wheels", "color": [0.03, 0.03, 0.035], "finish": "rubber", "features": wheels}
    return [airframe, glazing, engines, fan_part, gear, tyres]


def parts(spec: AircraftSpec) -> list[dict]:
    """Every part of the aircraft as Part Design documents (mm), each with its own colour
    and finish: airframe, canopy, propeller, spinner, gear legs and wheels (piston), or
    airframe, glazing, engines and gear (turbofan transport)."""
    if spec.jet:
        return _jet_parts(spec)
    mm = 1000.0
    length, wid, hei = (spec.fuselage_length * mm, spec.fuselage_width * mm,
                        spec.fuselage_height * mm)  # fmt: skip
    # canopy: a glass blister along the cabin roof, from the windscreen base aft
    x0 = max(spec.wing_x - 1.05, 0.12 * spec.fuselage_length) * mm
    canopy = {"name": "Canopy", "color": [0.06, 0.09, 0.13], "finish": "glass", "features": [
        {"id": "canopy", "name": "Canopy", "type": "loft", "at": {"x": -x0, "z": 0.30 * hei,
                                                                   "ry": -90},
         "sections": [{"z": 0, "width": 0.50 * wid, "height": 0.06 * hei, "radius": 10},
                      {"z": 550, "width": 0.84 * wid, "height": 0.50 * hei,
                       "radius": 0.2 * wid},
                      {"z": 1350, "width": 0.88 * wid, "height": 0.52 * hei,
                       "radius": 0.2 * wid},
                      {"z": 1950, "width": 0.62 * wid, "height": 0.16 * hei, "radius": 40}]},
    ]}  # fmt: skip
    radius = spec.prop_diameter / 2 * mm
    hub = 0.12 * min(wid, hei)
    propeller = {"name": "Propeller", "color": [0.08, 0.08, 0.09], "finish": "paint_matte",
                 "features": [
        # two twisted aerofoil blades in the disc plane, chord along Z, at 20° pitch
        {"id": "blades", "name": "Blades", "type": "wing", "naca": "4412",
         "root_chord": 0.09 * radius * 2, "tip_chord": 0.045 * radius * 2,
         "span": radius, "sweep": 3, "dihedral": 0, "twist": -12, "both_sides": True,
         "at": {"x": 200, "z": 0.04 * radius, "ry": 70, "rx": 15}},  # clear of the cowl
    ]}  # fmt: skip
    spinner = {"name": "Spinner", "color": [0.62, 0.07, 0.07], "finish": "paint",
               "features": [{"id": "spinner", "name": "Spinner", "type": "loft",
                             "at": {"x": 260, "ry": -90},
                             "sections": [{"z": 0, "width": 30, "height": 30, "radius": 14},
                                          {"z": 150, "width": 2 * hub, "height": 2 * hub,
                                           "radius": hub - 1},
                                          {"z": 290, "width": 2.2 * hub, "height": 2.2 * hub,
                                           "radius": 1.1 * hub - 1}]}]}  # fmt: skip
    gear_z = -hei / 2 - 0.45 * mm
    wheels_at = ([(-0.08 * length, 0.0, "nose")] if spec.tricycle else
                 [(-0.92 * length, 0.0, "tail")])  # fmt: skip
    main_x = -(spec.x_cg + (0.35 if spec.tricycle else -0.45)) * mm
    wheels_at += [(main_x, 1.1 * wid, "left main"), (main_x, -1.1 * wid, "right main")]
    legs, wheels = [], []
    for i, (x, y, label) in enumerate(wheels_at):
        small = label == "tail"
        rad = 120 if small else 200
        z = gear_z + (0.25 * mm if small else 0.0)
        wheels.append({"id": f"wheel{i}", "name": f"{label.title()} wheel", "type": "revolve",
                       "points": [[0.35 * rad, -55], [0.8 * rad, -60], [rad, -40],
                                  [rad, 40], [0.8 * rad, 60], [0.35 * rad, 55]],
                       "at": {"x": x, "y": y, "z": z, "rx": 90}})  # fmt: skip
        # a slim sprung leg from inside the fuselage belly to the wheel hub
        y0, z0 = 0.0, -0.25 * hei
        dy, dz = y - y0, z - z0
        leg = math.hypot(dy, dz)
        legs.append({"id": f"leg{i}", "name": f"{label.title()} leg", "type": "box",
                     "size": [70, leg, 32],
                     "at": {"x": x, "y": (y + y0) / 2, "z": (z + z0) / 2,
                            "rx": math.degrees(math.atan2(dz, dy))}})  # fmt: skip
    gear = {"name": "Landing gear", "color": [0.55, 0.57, 0.6], "finish": "metal", "features": legs}
    tyres = {"name": "Wheels", "color": [0.03, 0.03, 0.035], "finish": "rubber", "features": wheels}
    return [geometry(spec), canopy, propeller, spinner, gear, tyres]
