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


# --- VDI 2230 Part 1 (2015), single bolt, concentric clamping and loading ---

# limiting surface pressure p_G under the head, MPa (VDI 2230 table A9, selection)
SURFACE_PRESSURE = {
    "S235": 490.0,
    "S355": 760.0,
    "C45": 630.0,
    "42CrMo4": 850.0,
    "EN-GJL-250": 850.0,
    "EN-GJS-500": 900.0,
    "AlMgSi1 F31": 360.0,
    "AlZnMgCu0.5 F50": 370.0,
}
# embedding per interface, µm, for axial load and Rz < 10 µm (VDI 2230 table 5)
EMBED_THREAD, EMBED_HEAD, EMBED_INNER = 3.0, 2.5, 1.5


class VdiIn(BaseModel):
    d: float = Field(14.0, gt=3.0, le=64.0)
    pitch: float = Field(1.5, gt=0.3, le=6.0)
    grade: Literal["8.8", "10.9", "12.9"] = "10.9"
    mu_thread: float = Field(0.12, ge=0.04, le=0.3)  # mu_G
    mu_head: float = Field(0.12, ge=0.04, le=0.3)  # mu_K
    alpha_a: float = Field(1.6, ge=1.0, le=4.0)  # tightening factor: torque wrench 1.6-1.8
    utilisation: float = Field(0.9, gt=0.3, le=1.0)  # nu, of the yield stress in assembly
    head_bearing: float | None = Field(None, gt=0.0)  # d_w, mm (default 1.5 d)
    hole: float | None = Field(None, gt=0.0)  # D_ha, mm (default ISO 273 medium ~ 1.1 d)
    grip: float = Field(25.0, gt=1.0, le=1000.0)
    inner_interfaces: int = Field(1, ge=0, le=10)  # plate-to-plate interfaces
    load_introduction: float = Field(0.5, gt=0.0, le=1.0)  # n
    axial_kN: float = Field(10.0, ge=0.0)  # F_A max per bolt  # noqa: N815
    shear_kN: float = Field(5.0, ge=0.0)  # F_Q max per bolt  # noqa: N815
    mu_interface: float = Field(0.15, gt=0.0, le=1.0)  # mu_T between the plates
    seal_kN: float = Field(0.0, ge=0.0)  # extra clamp load for sealing  # noqa: N815
    member: str = Field("S355", max_length=30)


def vdi2230(v: VdiIn) -> dict:
    """VDI 2230 check of a bolted joint: permissible assembly preload (R7), tightening
    torque (R8), preload scatter, embedding loss (R4), required and residual clamp load,
    working stress (R8/R9), fatigue of rolled threads (R9) and surface pressure (R10)."""
    th = thread(v.d, v.pitch)
    d2, d3 = th["d2"], th["d3"]
    a0 = th["stress_area_mm2"]
    d0 = (d2 + d3) / 2.0
    rm, rp, _ = strengths(v.d, v.grade)
    dw = v.head_bearing or 1.5 * v.d
    dha = v.hole or 1.1 * v.d
    if dw <= dha:
        raise ValueError("head bearing diameter must exceed the hole")
    dkm = (dw + dha) / 2.0
    # R7: permissible assembly preload (equivalent stress nu Rp with thread torsion)
    k = 1.5 * d2 / d0 * (v.pitch / (math.pi * d2) + 1.155 * v.mu_thread)
    fm_zul = a0 * v.utilisation * rp / math.sqrt(1.0 + 3.0 * k * k)
    # R8: tightening torque M_A = F_M (0.16 P + 0.58 d2 mu_G + D_Km / 2 mu_K)
    lever = 0.16 * v.pitch + 0.58 * d2 * v.mu_thread + dkm / 2.0 * v.mu_head
    torque = fm_zul * lever / 1000.0
    fm_min = fm_zul / v.alpha_a
    # stiffness and load factor
    kb = a0 * E_STEEL / v.grip  # threaded over the grip (conservative)
    km = member_stiffness(v.d, v.grip, E_STEEL)
    phi = v.load_introduction * kb / (kb + km)
    # R4: embedding loss F_Z = f_Z / (delta_S + delta_P)
    fz_um = EMBED_THREAD + EMBED_HEAD + v.inner_interfaces * EMBED_INNER
    f_z = fz_um * 1e-3 * kb * km / (kb + km)
    fa, fq = v.axial_kN * 1e3, v.shear_kN * 1e3
    f_k_req = max(fq / v.mu_interface, v.seal_kN * 1e3)
    f_kr = fm_min - f_z - (1.0 - phi) * fa  # residual clamp load at the worst case
    # working state: maximum bolt force and equivalent stress (residual torsion k_tau = 0.5)
    fs_max = fm_zul + phi * fa
    sigma = fs_max / a0
    tau = (fm_zul * (0.16 * v.pitch + 0.58 * d2 * v.mu_thread)) / (math.pi / 16.0 * d0**3)
    sigma_red = math.sqrt(sigma**2 + 3.0 * (0.5 * tau) ** 2)
    # R9: alternating stress against rolled-thread endurance (rolled before heat treatment)
    sigma_a = phi * fa / (2.0 * a0)
    sigma_asv = 0.85 * (150.0 / v.d + 45.0)
    # R10: surface pressure under the head at the permissible preload
    ap = math.pi / 4.0 * (dw**2 - dha**2)
    p_max = (fm_zul + phi * fa) / ap
    p_g = SURFACE_PRESSURE.get(v.member)
    out = {
        "d2": d2,
        "d3": d3,
        "stress_area_mm2": a0,
        "Rp": rp,
        "Rm": rm,
        "D_Km": dkm,
        "F_M_zul_kN": fm_zul / 1e3,
        "F_M_min_kN": fm_min / 1e3,
        "torque_Nm": torque,
        "thread_torque_Nm": fm_zul * (0.16 * v.pitch + 0.58 * d2 * v.mu_thread) / 1e3,
        "head_torque_Nm": fm_zul * dkm / 2.0 * v.mu_head / 1e3,
        "phi": phi,
        "embedding_um": fz_um,
        "F_Z_kN": f_z / 1e3,
        "F_K_req_kN": f_k_req / 1e3,
        "F_KR_min_kN": f_kr / 1e3,
        "clamp_margin": f_kr / f_k_req if f_k_req > 0 else math.inf,
        "F_S_max_kN": fs_max / 1e3,
        "sigma_red": sigma_red,
        "S_F": rp / sigma_red,
        "sigma_a": sigma_a,
        "sigma_ASV": sigma_asv,
        "S_D": sigma_asv / sigma_a if sigma_a else math.inf,
        "p_max": p_max,
        "p_G": p_g,
        "S_P": p_g / p_max if p_g else None,
    }
    warnings = []
    if f_kr < f_k_req:
        warnings.append(
            f"Residual clamp load {f_kr / 1e3:.1f} kN is below the {f_k_req / 1e3:.1f} kN needed "
            "(slip or leakage): use more or larger bolts, a better tightening method, "
            "or more friction."
        )
    if f_kr <= 0:
        warnings.append("The joint opens under the axial load at the lowest preload.")
    if sigma_red > rp:
        warnings.append(f"Working stress {sigma_red:.0f} MPa exceeds the yield {rp:.0f} MPa.")
    if sigma_a > sigma_asv:
        warnings.append(
            f"Alternating stress {sigma_a:.0f} MPa exceeds the thread endurance "
            f"{sigma_asv:.0f} MPa."
        )
    if p_g and p_max > p_g:
        warnings.append(
            f"Surface pressure {p_max:.0f} MPa under the head exceeds {p_g:.0f} MPa "
            f"for {v.member}: "
            "add a hardened washer or a flange head."
        )
    if p_g is None:
        warnings.append(f"No limiting surface pressure on file for '{v.member}'.")
    out["warnings"] = warnings
    return out
