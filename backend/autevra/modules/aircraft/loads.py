"""Aircraft flight and landing loads, and the compliance rows they support.

Method (the classic prescriptive light-aircraft rules, CS-23 Amdt 4 / 14 CFR 23 before
amendment 23-64; the current CS-23 is objective-based with ASTM F3116 as one means of
compliance, which keeps these numbers):
- limit manoeuvring load factors by category: +3.8 / +4.4 / +6.0 (normal, utility,
  aerobatic), negative 0.4 n (0.5 n aerobatic);
- design speeds: V_C at least 33 sqrt(W/S) kn (36 aerobatic), V_D at least 1.40 V_C,min
  (1.50 utility, 1.55 aerobatic) and at least 1.25 V_C; V_A = V_S sqrt(n);
- gust load factor (Pratt): n = 1 + K_g U_de V a / (498 W/S) with V in kn, U_de in ft/s
  (50 at V_C, 25 at V_D), W/S in lb/ft², K_g = 0.88 mu / (5.3 + mu),
  mu = 2 (W/S) / (rho c a g) (slug/ft³, ft, 32.17 ft/s²);
- wing root bending (limit, each side): the lift of an elliptic distribution on the wing,
  less the wing's own weight (inertia relief), acting at 4/(3 pi) of the semi-span;
  spar caps sized on the 2024-T3 minimum yield with the factor of safety 1.5 and a spar
  depth of 90 % of the root aerofoil thickness;
- landing: limit descent velocity V = 4.4 (W/S)^0.25 ft/s within 7-10 ft/s, absorbed over
  the gear stroke with an efficiency (spring steel 0.5, oleo 0.75), plus 1 g.
"""

import math

from autevra import materials
from autevra.aero import aircraft as ac
from autevra.modules import Values
from autevra.modules.aircraft.breakdown import CATEGORIES, group_masses
from autevra.product.loads import Compliance, LoadAt, LoadCase

KN = 1.943844  # kn per m/s
LB, FT = 2.20462, 3.28084
FOS = 1.5


def _spec(values: Values) -> ac.AircraftSpec:
    return ac.AircraftSpec.model_validate({k: v for k, v in values.items()
                                           if k in ac.AircraftSpec.model_fields})  # fmt: skip


def envelope(values: Values) -> dict:
    s = _spec(values)
    category = str(values.get("category", "Normal"))
    n_pos = CATEGORIES[category]
    n_neg = -(0.5 if category == "Aerobatic" else 0.4) * n_pos
    out = ac.analyse(s)
    geo, aero = out["geometry"], out["aero"]
    ws_si = s.mtow * 9.80665 / geo["wing_area"]  # N/m²
    ws = s.mtow * LB / (geo["wing_area"] * FT**2)  # lb/ft²
    vs = float(out["performance"]["v_stall"])  # m/s, sea level
    vc_min = (36 if category == "Aerobatic" else 33) * math.sqrt(ws) / KN
    vc = max(s.cruise_speed, vc_min)
    vd_factor = {"Normal": 1.40, "Utility": 1.50, "Aerobatic": 1.55}[category]
    vd = max(vd_factor * vc_min, 1.25 * vc)
    va = vs * math.sqrt(n_pos)
    a = float(aero["wing_lift_slope"])  # per rad
    rho_slug = 0.0023769
    mu = 2 * ws / (rho_slug * geo["mac"] * FT * a * 32.17)
    kg = 0.88 * mu / (5.3 + mu)

    def gust(v: float, ude: float) -> float:
        return kg * ude * v * KN * a / (498 * ws)

    gust_c, gust_d = gust(vc, 50.0), gust(vd, 25.0)
    n_design = max(n_pos, 1 + gust_c, 1 + gust_d)
    stall = [(round(v, 2), round((v / vs) ** 2, 3)) for v in
             [vs * (1 + 0.05 * i) for i in range(int((va / vs - 1) / 0.05) + 1)]]  # fmt: skip
    return {"category": category, "n_pos": n_pos, "n_neg": n_neg, "vs": vs, "va": va,
            "vc": vc, "vc_min": vc_min, "vd": vd, "wing_loading_pa": ws_si,
            "gust_vc": [1 + gust_c, 1 - gust_c], "gust_vd": [1 + gust_d, 1 - gust_d],
            "kg": kg, "mu": mu, "n_design": n_design, "stall_line": stall}  # fmt: skip


def cases(values: Values) -> list[LoadCase]:
    s = _spec(values)
    env = envelope(values)
    g = group_masses(s, env["n_pos"])
    wing_kg = g["wing"]
    semi = s.wing_span / 2
    arm = 4 / (3 * math.pi) * semi
    out: list[LoadCase] = []
    for cid, name, n in (("manoeuvre", "Positive manoeuvre at V_A", env["n_pos"]),
                         ("gust_vc", "Positive gust at V_C (50 ft/s)", env["gust_vc"][0]),
                         ("gust_vd", "Positive gust at V_D (25 ft/s)", env["gust_vd"][0]),
                         ("negative", "Negative manoeuvre", env["n_neg"])):  # fmt: skip
        lift_side = n * (s.mtow - wing_kg) * 9.80665 / 2  # N per side, inertia relief
        moment = lift_side * arm
        out.append(LoadCase(
            id=cid, name=name, kind="limit", factors={"n": round(n, 3)},
            method="CS-23 Amdt 4 / FAR 23 legacy load factors; elliptic lift, inertia relief",
            loads=[LoadAt(location="wing root (each side)", fz=round(lift_side),
                          mx=round(moment))],
            results={"root_bending_nm": round(moment), "shear_n": round(lift_side)}))  # fmt: skip
    # spar caps sized by the governing positive case
    gov = max(out, key=lambda c: c.results["root_bending_nm"])
    al = materials.get("2024_t3")
    depth = 0.9 * int(s.wing_naca[2:]) / 100 * s.wing_root_chord  # m
    cap_force = FOS * gov.results["root_bending_nm"] / depth  # N, ultimate
    area = cap_force / (al.yield_mpa * 1e6) * 1e6  # mm² per cap
    gov.results.update(
        {
            "spar_depth_mm": round(depth * 1000),
            "cap_area_mm2": round(area),
            "cap_mass_kg": round(2 * area * 1e-6 * semi * al.density * 0.6, 1),
        }
    )
    # landing
    ws = s.mtow * LB / (ac.analyse(s)["geometry"]["wing_area"] * FT**2)
    v_ft = min(max(4.4 * ws**0.25, 7.0), 10.0)
    v = v_ft / FT
    stroke, eta = (0.20, 0.5) if s.fixed_gear else (0.25, 0.75)
    n_land = 1 + v * v / (2 * 9.80665 * eta * stroke)
    per_main = n_land * s.mtow * 9.80665 * (0.9 if s.tricycle else 0.85) / 2
    out.append(LoadCase(
        id="landing", name="Level landing", kind="limit",
        factors={"descent_ms": round(v, 2), "n": round(n_land, 2)},
        method="descent velocity 4.4 (W/S)^0.25 ft/s (7-10), stroke energy with efficiency "
        f"{eta}, +1 g",
        loads=[LoadAt(location="main gear (each)", fz=round(per_main))],
        results={"n_landing": round(n_land, 2)}))  # fmt: skip
    return out


def compliance(values: Values) -> list[Compliance]:
    s = _spec(values)
    env = envelope(values)
    vs_kn = env["vs"] * KN
    rows = [
        Compliance(clause="CS-23 Amdt 4, 23.49(c)", requirement="stall speed (flaps up here) "
                   "at most 61 kn for a single-engine aeroplane", means="analysis",
                   evidence=f"V_S = {vs_kn:.1f} kn (clean; flaps would lower it)",
                   status="shown" if vs_kn <= 61 else "not shown"),
        Compliance(clause="CS-23 Amdt 4, 23.337", requirement="limit manoeuvring load factors "
                   "of the category", means="analysis",
                   evidence=f"{env['category']}: +{env['n_pos']:.1f} / {env['n_neg']:.2f} g used "
                   "in the load cases", status="shown"),
        Compliance(clause="CS-23 Amdt 4, 23.335", requirement="design speeds V_C, V_D, V_A "
                   "within the minimum rules", means="analysis",
                   evidence=f"V_C {env['vc'] * KN:.0f} kn (min {env['vc_min'] * KN:.0f}), V_D "
                   f"{env['vd'] * KN:.0f} kn, V_A {env['va'] * KN:.0f} kn", status="shown"),
        Compliance(clause="CS-23 Amdt 4, 23.333 / 23.341", requirement="gust load factors at "
                   "V_C and V_D", means="analysis",
                   evidence=f"n = {env['gust_vc'][0]:.2f} at V_C, {env['gust_vd'][0]:.2f} at V_D "
                   f"(K_g {env['kg']:.3f})", status="shown"),
        Compliance(clause="CS-23 Amdt 4, 23.303", requirement="factor of safety 1.5 on limit "
                   "loads", means="analysis", evidence="spar caps sized at 1.5 x limit on the "
                   "2024-T3 minimum yield", status="shown"),
        Compliance(clause="CS-23 Amdt 4, 23.473", requirement="landing load conditions",
                   means="analysis", evidence="level landing estimate from the descent velocity "
                   "rule; tail-down and one-wheel cases still to do", status="open"),
        Compliance(clause="CS-23 Amdt 4, 23.629", requirement="freedom from flutter",
                   means="analysis", evidence="needs a flutter analysis or ground vibration "
                   "test (planned)", status="open"),
    ]  # fmt: skip
    del s
    return rows
