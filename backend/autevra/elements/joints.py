"""Bolted joints and fillet welds.

Bolted joint (tension joint, one bolt):
- Thread geometry ISO 724: d2 = d - 0.649519 P, d3 = d - 1.226869 P; tensile stress area
  As = pi/4 ((d2 + d3) / 2)^2 (ISO 898-1).
- Strength from the property class (ISO 898-1: Rm, Rp0.2, proof stress Sp); preload as a
  fraction of the proof load (0.9 Sp As by default, a common reusable-joint rule) or as a
  given force; tightening torque T = K Fi d with the nut factor K.
- Stiffness (Shigley, Mechanical Engineering Design, ch. 8): bolt kb = Ad At E /
  (Ad lt + At ld) for an unthreaded shank ld and threaded length lt in the grip; members
  of one material by the 30 deg frustum (Wileman): km = 0.5774 pi E d /
  (2 ln(5 (0.5774 l + 0.5 d) / (0.5774 l + 2.5 d))). Joint constant C = kb / (kb + km).
- Under an external tensile load P per bolt: bolt load Fb = Fi + C P, member load
  Fm = Fi - (1 - C) P; yield factor np = Sp At / (C P + Fi), load factor
  nL = (Sp At - Fi) / (C P), separation factor n0 = Fi / ((1 - C) P).
- Bolt fatigue for a load fluctuating 0..P: Goodman line from the preload (Shigley eq. 8-38)
  nf = Se (Sut - sigma_i) / (Sut sigma_a + Se (sigma_m - sigma_i)) with the fully corrected
  endurance strength of rolled threads (Shigley table 8-17: 8.8 129, 10.9 162, 12.9 190 MPa).
- Shear (friction-grip) joint: slip resistance Fs = mu Fi n_s per bolt.

Fillet welds:
- Throat a = z cos 45 deg for leg z. Simple check tau = F / (a L) against an allowable.
- EN 1993-1-8 directional method (4.5.3.2): sigma_perp, tau_perp, tau_par on the throat;
  sqrt(sigma_perp^2 + 3 (tau_perp^2 + tau_par^2)) <= fu / (beta_w gamma_M2) and
  sigma_perp <= 0.9 fu / gamma_M2. A longitudinal weld carries tau_par = F / (a L); a
  transverse weld sigma_perp = tau_perp = F / (sqrt 2 a L).
"""

import math
from typing import Literal

from pydantic import BaseModel, Field

from autevra.inventory.calc import PROPERTY_CLASSES

E_STEEL = 207_000.0  # MPa (Shigley)
# Fully corrected endurance strength of rolled threads, MPa (Shigley table 8-17).
BOLT_ENDURANCE = {"8.8": 129.0, "10.9": 162.0, "12.9": 190.0}


def thread(d: float, pitch: float) -> dict[str, float]:
    """ISO 724 basic diameters and the ISO 898-1 tensile stress area of a metric thread."""
    if d <= 0 or pitch <= 0 or pitch >= d / 2:
        raise ValueError("diameter and pitch must be positive, pitch under d / 2")
    d2 = d - 0.649519 * pitch
    d3 = d - 1.226869 * pitch
    return {"d2": d2, "d3": d3, "stress_area_mm2": math.pi / 4.0 * ((d2 + d3) / 2.0) ** 2}


def strengths(d: float, grade: str) -> tuple[float, float, float]:
    """(Rm, Rp0.2, Sp) in MPa for a property class; 8.8 above M16 has lower values."""
    if grade not in PROPERTY_CLASSES:
        raise ValueError(f"unknown property class {grade!r} (8.8, 10.9 or 12.9)")
    if grade == "8.8" and d > 16:
        return 830.0, 660.0, 600.0
    return PROPERTY_CLASSES[grade]


class BoltJointIn(BaseModel):
    d: float = Field(10.0, gt=1.0, le=100.0)  # nominal diameter, mm
    pitch: float = Field(1.5, gt=0.2, le=8.0)  # mm
    grade: Literal["8.8", "10.9", "12.9"] = "8.8"
    nut_factor: float = Field(0.2, gt=0.05, le=0.4)
    preload_fraction: float = Field(0.9, gt=0.1, le=1.0)  # of proof load
    preload_kN: float | None = Field(None, gt=0.0)  # overrides the fraction  # noqa: N815
    grip: float = Field(30.0, gt=0.5, le=1000.0)  # clamped length l, mm
    threaded_in_grip: float | None = Field(None, ge=0.0)  # lt; default: fully threaded
    e_bolt: float = Field(E_STEEL, gt=1000.0)
    e_member: float = Field(E_STEEL, gt=1000.0)
    load_kN: float = Field(0.0, ge=0.0)  # external tensile load per bolt  # noqa: N815
    shear_kN: float = Field(0.0, ge=0.0)  # transverse load per bolt (friction grip)  # noqa: N815
    friction: float = Field(0.2, gt=0.0, le=1.0)  # slip factor between plates
    shear_planes: int = Field(1, ge=1, le=4)


def member_stiffness(d: float, grip: float, e: float) -> float:
    """Clamped members of one material, 30 deg frustum (N/mm)."""
    t = 0.5774 * grip
    return 0.5774 * math.pi * e * d / (2.0 * math.log(5.0 * (t + 0.5 * d) / (t + 2.5 * d)))


def bolt_joint(j: BoltJointIn) -> dict:
    th = thread(j.d, j.pitch)
    a_t = th["stress_area_mm2"]
    a_d = math.pi / 4.0 * j.d**2
    rm, rp, sp = strengths(j.d, j.grade)
    proof = sp * a_t  # N
    fi = j.preload_kN * 1e3 if j.preload_kN else j.preload_fraction * proof
    lt = j.grip if j.threaded_in_grip is None else min(j.threaded_in_grip, j.grip)
    ld = j.grip - lt
    kb = a_d * a_t * j.e_bolt / (a_d * lt + a_t * ld)
    km = member_stiffness(j.d, j.grip, j.e_member)
    c = kb / (kb + km)
    p = j.load_kN * 1e3
    out: dict = {
        **th,
        "proof_load_kN": proof / 1e3,
        "yield_load_kN": rp * a_t / 1e3,
        "ultimate_load_kN": rm * a_t / 1e3,
        "Rm": rm,
        "Rp": rp,
        "Sp": sp,
        "preload_kN": fi / 1e3,
        "preload_stress": fi / a_t,
        "torque_Nm": j.nut_factor * fi * j.d / 1e3,
        "kb_N_per_mm": kb,
        "km_N_per_mm": km,
        "joint_constant": c,
        "separation_load_kN": fi / (1.0 - c) / 1e3,
    }
    warnings: list[str] = []
    if fi > proof:
        warnings.append("Preload exceeds the proof load: the bolt yields on tightening.")
    if p > 0:
        fb, fm = fi + c * p, fi - (1.0 - c) * p
        sig_a = c * p / (2.0 * a_t)
        sig_i = fi / a_t
        se = BOLT_ENDURANCE[j.grade]
        nf = se * (rm - sig_i) / (sig_a * (rm + se))  # sigma_m - sigma_i = sigma_a
        out |= {
            "bolt_load_kN": fb / 1e3,
            "member_load_kN": fm / 1e3,
            "yield_factor": proof / fb,
            "load_factor": (proof - fi) / (c * p),
            "separation_factor": fi / ((1.0 - c) * p),
            "stress_amplitude": sig_a,
            "endurance_strength": se,
            "fatigue_factor": nf,
        }
        if fm <= 0:
            warnings.append(
                "Joint separates under the external load: all of it passes to the bolt."
            )
        if fb > proof:
            warnings.append("Bolt load exceeds the proof load under the external load.")
        if nf < 1.0:
            warnings.append(
                f"Bolt fatigue factor {nf:.2f} < 1 for a load cycling 0..{j.load_kN:g} kN."
            )
    if j.shear_kN > 0:
        slip = j.friction * fi * j.shear_planes
        out |= {"slip_resistance_kN": slip / 1e3, "slip_factor": slip / (j.shear_kN * 1e3)}
        if slip < j.shear_kN * 1e3:
            warnings.append(
                "Transverse load exceeds the friction-grip slip resistance: "
                "the joint slips into bearing."
            )
    out["warnings"] = warnings
    out["diagram"] = joint_diagram(fi, kb, km, p)
    return out


def joint_diagram(fi: float, kb: float, km: float, p: float) -> dict:
    """Joint (triangle) diagram in kN and µm: the bolt line rises from (0,0) to the preload
    at its stretch, the member line falls from the preload to zero at the member
    compression; an external load P adds C P to the bolt and takes (1 - C) P off the members."""
    db, dm = fi / kb * 1e3, fi / km * 1e3  # µm
    out = {"preload_kN": fi / 1e3, "bolt_stretch_um": db, "member_compression_um": dm}
    if p > 0:
        dp = p / (kb + km) * 1e3
        out |= {
            "extra_stretch_um": dp,
            "bolt_load_kN": (fi + kb * dp / 1e3) / 1e3,
            "member_load_kN": max(fi - km * dp / 1e3, 0.0) / 1e3,
        }
    return out


# EN 10025 structural steels, t <= 40 mm: (fu MPa, correlation factor beta_w)
WELD_STEELS = {
    "S235": (360.0, 0.8),
    "S275": (430.0, 0.85),
    "S355": (490.0, 0.9),
    "S460": (540.0, 1.0),
}


class FilletWeldIn(BaseModel):
    leg: float = Field(5.0, gt=0.5, le=50.0)  # z, mm
    length: float = Field(100.0, gt=1.0, le=10_000.0)  # effective length, mm
    force_kN: float = Field(20.0, ge=0.0)  # noqa: N815
    direction: Literal["longitudinal", "transverse"] = "longitudinal"
    lines: int = Field(1, ge=1, le=8)  # identical welds sharing the load
    allowable: float = Field(150.0, gt=0.0)  # simple shear allowable on the throat, MPa
    steel: Literal["S235", "S275", "S355", "S460"] = "S355"
    gamma_m2: float = Field(1.25, ge=1.0, le=2.0)


def _weld_stresses(f: float, area: float, direction: str) -> tuple[float, float, float]:
    tau = f / area
    if direction == "longitudinal":
        return 0.0, 0.0, tau
    return tau / math.sqrt(2.0), tau / math.sqrt(2.0), 0.0


def fillet_weld(w: FilletWeldIn) -> dict:
    a = w.leg * math.cos(math.radians(45.0))
    area = a * w.length * w.lines
    f = w.force_kN * 1e3
    tau = f / area
    fu, beta = WELD_STEELS[w.steel]
    lim = fu / (beta * w.gamma_m2)
    lim_perp = 0.9 * fu / w.gamma_m2

    def utilisation(force: float) -> tuple[float, float, float, float, float]:
        s_perp, t_perp, t_par = _weld_stresses(force, area, w.direction)
        vm = math.sqrt(s_perp**2 + 3.0 * (t_perp**2 + t_par**2))
        return max(vm / lim, s_perp / lim_perp), s_perp, t_perp, t_par, vm

    util, s_perp, t_perp, t_par, vm = utilisation(f)
    capacity = 1.0 / utilisation(1.0)[0]  # stresses are linear in the force
    warnings = []
    if tau > w.allowable:
        warnings.append(f"Throat shear {tau:.1f} MPa exceeds the {w.allowable:g} MPa allowable.")
    if util > 1.0:
        warnings.append(f"EN 1993-1-8 directional check fails (utilisation {util:.2f}).")
    if w.length < max(30.0, 6.0 * a):
        warnings.append(
            "Weld shorter than max(30 mm, 6a): EN 1993-1-8 ignores it as load-carrying."
        )
    return {
        "throat_mm": a,
        "throat_area_mm2": area,
        "tau": tau,
        "sigma_perp": s_perp,
        "tau_perp": t_perp,
        "tau_par": t_par,
        "equivalent": vm,
        "limit": lim,
        "limit_perp": lim_perp,
        "utilisation": util,
        "fu": fu,
        "beta_w": beta,
        "capacity_kN": capacity / 1e3,
        "warnings": warnings,
    }
