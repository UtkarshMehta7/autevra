"""Helical compression springs of round wire (EN 13906-1; Shigley ch. 10).

- Rate k = G d^4 / (8 D^3 n) for wire d, mean coil diameter D and n active coils; spring
  index C = D / d, recommended 4..20 (EN 13906-1).
- Shear stress tau = K 8 F D / (pi d^3) with the Bergstrasser factor
  K = (4C + 2) / (4C - 3) (stress correction used by EN 13906-1); Wahl factor also given.
- Ends: closed and ground nt = n + 2, Ls = nt d; closed nt = n + 2, Ls = (nt + 1) d;
  plain nt = n, Ls = (n + 1) d; plain and ground nt = n + 1, Ls = nt d.
- Minimum tensile strength Sut = A / d^m (Shigley table 10-4); allowable shear at solid
  height 0.45 Sut for music wire and hard-drawn, 0.50 Sut for the alloy wires (no set
  removal).
- Buckling: absolutely stable when L0 < 2.63 D / alpha with alpha 0.5 (both ends on flat
  parallel plates), 0.707 (one end pivoted), 1 (both pivoted), 2 (one end free).
- First surge frequency f = (1/2) sqrt(k / m) for both ends against flat plates, with the
  active-coil mass m = pi^2 d^2 D n rho / 4.
"""

import math
from typing import Literal

from pydantic import BaseModel, Field

# wire: (A MPa·mm^m, m, G MPa, allowable fraction of Sut at solid)
WIRES = {
    "music": (2211.0, 0.145, 81_700.0, 0.45),
    "hard-drawn": (1783.0, 0.190, 79_300.0, 0.45),
    "oil-tempered": (1855.0, 0.187, 77_200.0, 0.50),
    "chrome-vanadium": (2005.0, 0.168, 77_200.0, 0.50),
    "chrome-silicon": (1974.0, 0.108, 77_200.0, 0.50),
}
ALPHA = {"fixed-fixed": 0.5, "fixed-pinned": 0.707, "pinned-pinned": 1.0, "fixed-free": 2.0}
RHO_STEEL = 7.85e-9  # tonne/mm3 so that k [N/mm] / m [t] gives 1/s^2


class SpringIn(BaseModel):
    d: float = Field(2.0, gt=0.05, le=80.0)  # wire, mm
    D: float = Field(16.0, gt=0.2, le=1000.0)  # mean coil diameter, mm
    n: float = Field(8.0, ge=1.0, le=200.0)  # active coils
    free_length: float = Field(60.0, gt=0.5, le=5000.0)
    ends: Literal["closed-ground", "closed", "plain", "plain-ground"] = "closed-ground"
    wire: Literal["music", "hard-drawn", "oil-tempered", "chrome-vanadium", "chrome-silicon"] = (
        "music"
    )
    shear_modulus: float | None = Field(None, gt=1000.0)  # overrides the wire's G
    force: float = Field(0.0, ge=0.0)  # working load, N
    support: Literal["fixed-fixed", "fixed-pinned", "pinned-pinned", "fixed-free"] = "fixed-fixed"


def spring(s: SpringIn) -> dict:
    a_coef, m_exp, g_wire, frac = WIRES[s.wire]
    g = s.shear_modulus or g_wire
    c = s.D / s.d
    if c <= 1.0:
        raise ValueError("mean coil diameter must exceed the wire diameter")
    k = g * s.d**4 / (8.0 * s.D**3 * s.n)
    kb = (4.0 * c + 2.0) / (4.0 * c - 3.0)
    kw = (4.0 * c - 1.0) / (4.0 * c - 4.0) + 0.615 / c
    nt, ls = {
        "closed-ground": (s.n + 2.0, (s.n + 2.0) * s.d),
        "closed": (s.n + 2.0, (s.n + 3.0) * s.d),
        "plain": (s.n, (s.n + 1.0) * s.d),
        "plain-ground": (s.n + 1.0, (s.n + 1.0) * s.d),
    }[s.ends]
    sut = a_coef / s.d**m_exp
    ssy = frac * sut
    travel_solid = s.free_length - ls
    f_solid = k * max(travel_solid, 0.0)

    def tau(force: float) -> float:
        return kb * 8.0 * force * s.D / (math.pi * s.d**3)

    mass = math.pi**2 * s.d**2 * s.D * s.n * RHO_STEEL / 4.0
    alpha = ALPHA[s.support]
    critical_l0 = 2.63 * s.D / alpha
    out: dict = {
        "rate_N_per_mm": k,
        "index": c,
        "bergstrasser": kb,
        "wahl": kw,
        "total_coils": nt,
        "solid_length": ls,
        "travel_to_solid": travel_solid,
        "force_at_solid": f_solid,
        "tau_solid": tau(f_solid),
        "Sut": sut,
        "allowable_shear": ssy,
        "shear_modulus": g,
        "pitch": (s.free_length - (nt - s.n) * s.d) / s.n,
        "active_mass_g": mass * 1e6,
        "surge_hz": 0.5 * math.sqrt(k / mass),
        "buckling_free_length": critical_l0,
        "wire_length_mm": math.pi * s.D * nt,
    }
    warnings = []
    if not 4.0 <= c <= 20.0:
        warnings.append(f"Spring index D/d = {c:.3g} outside 4–20 (EN 13906-1).")
    if travel_solid <= 0:
        warnings.append("Free length is at or below the solid length.")
    if out["tau_solid"] > ssy:
        warnings.append(
            f"Shear at solid {out['tau_solid']:.0f} MPa exceeds {ssy:.0f} MPa: "
            "the spring takes a set when closed."
        )
    if s.free_length >= critical_l0:
        warnings.append(
            f"Free length {s.free_length:g} mm ≥ {critical_l0:.0f} mm: may buckle; "
            "guide it on a rod or in a tube."
        )
    if s.force > 0:
        defl = s.force / k
        out |= {
            "deflection": defl,
            "working_length": s.free_length - defl,
            "tau_working": tau(s.force),
            "working_factor": ssy / tau(s.force),
        }
        if defl >= travel_solid:
            warnings.append("Working load closes the spring solid.")
    out["warnings"] = warnings
    return out
