"""Wing structure sizing (level 2): spar caps, spar web and skins from the governing limit
load case, with the factor of safety 1.5 on 2024-T3 minimum values.

Method (classical thin-walled beam idealisation, root section, stated):
- bending: the caps carry the root bending moment as a couple, F = 1.5 M / h, with the spar
  depth h = 90 % of the root aerofoil thickness;
- shear: the web carries the root shear, shear flow q = 1.5 V / h, thickness t_w = q /
  (0.55 F_ty) (allowable shear stress taken as 0.55 of the tensile yield);
- skins: light-aircraft practice, post-buckled: 0.8 mm upper and lower (minimum gauge for
  handling and hail), buckling between stringers at sigma_cr = k pi^2 E (t/b)^2 / (12 (1 -
  nu^2)), k = 4, b = 150 mm; after buckling an effective width w_e = 1.9 t sqrt(E / sigma)
  next to each side of a cap (von Karman) works with the cap, so the caps are sized for
  A_cap + 2 w_e t = F / (F_ty / 1.5);
- mass: caps and web tapering linearly to the tip (factor 0.6 on the root sections), skins
  over the planform (both surfaces), ribs at the breakdown's rib count as 1 mm webs of
  chord x 0.8 depth; times a non-optimum factor 1.25 for joints, fasteners, cut-outs and
  stringers not modelled (a concept-design allowance).
Limits: root section only (no spanwise check), no torsion box or aileron loads, no
fatigue or damage tolerance; good for concept mass and the first check of the sections.
"""

import math

from autevra import materials
from autevra.aero import aircraft as ac
from autevra.modules import Values
from autevra.modules.aircraft import loads as air_loads

FOS = 1.5
NON_OPTIMUM = 1.25
STRINGER_PITCH = 0.15  # m
SKIN = 0.8e-3  # m
MIN_GAUGE = 0.6e-3  # m


def plate_buckling_stress(t: float, b: float, e: float, nu: float, k: float = 4.0) -> float:
    return k * math.pi**2 * e * (t / b) ** 2 / (12 * (1 - nu * nu))


def size_wing(values: Values) -> dict:
    s = ac.AircraftSpec.model_validate({k: v for k, v in values.items()
                                        if k in ac.AircraftSpec.model_fields})  # fmt: skip
    cases = [c for c in air_loads.cases(values) if c.id != "landing"]
    gov = max(cases, key=lambda c: abs(c.results["root_bending_nm"]))
    m_root = abs(gov.results["root_bending_nm"])
    v_root = abs(gov.results["shear_n"])
    al = materials.get("2024_t3")
    fty = al.yield_mpa * 1e6
    e = al.youngs_modulus_gpa * 1e9
    h = 0.9 * int(s.wing_naca[2:]) / 100 * s.wing_root_chord
    allow = fty / FOS
    w_eff = 1.9 * SKIN * math.sqrt(e / allow)  # effective skin width each side of a cap
    skin_eff = 2 * w_eff * SKIN
    cap = max(m_root / h / allow - skin_eff, 0.0)  # m² each cap (beyond the skin)
    web = max(FOS * v_root / h / (0.55 * fty), MIN_GAUGE)
    sigma = allow  # caps and effective skin work at the allowable at limit x 1.5
    t_skin = SKIN
    sigma_cr = plate_buckling_stress(SKIN, STRINGER_PITCH, e, al.poisson)
    semi = s.wing_span / 2
    area = s.wing_span * (s.wing_root_chord + s.wing_tip_chord) / 2
    rho = al.density
    rib_pairs = max(round(semi / 0.35), 4)
    mean_chord = area / s.wing_span
    masses = {
        "spar_caps": 2 * 2 * cap * semi * 0.6 * rho,  # two caps, two sides
        "spar_web": 2 * web * h * semi * 0.6 * rho,
        "wing_skin": 2 * area * t_skin * rho,  # upper and lower
        "ribs": 2 * rib_pairs * 1e-3 * mean_chord * 0.8 * h * rho,
    }
    masses = {k: v * NON_OPTIMUM for k, v in masses.items()}
    return {
        "governing_case": gov.id, "root_bending_nm": m_root, "root_shear_n": v_root,
        "spar_depth_mm": h * 1000, "cap_area_mm2": cap * 1e6, "web_mm": web * 1000,
        "skin_mm": t_skin * 1000, "working_stress_mpa": sigma / 1e6,
        "skin_buckling_mpa": sigma_cr / 1e6, "effective_width_mm": w_eff * 1000,
        "masses_kg": masses, "total_kg": sum(masses.values()),
        "material": al.name, "basis": f"{al.basis} values, {al.source}",
    }  # fmt: skip
