"""Stress-life fatigue of steels (Shigley, Mechanical Engineering Design, ch. 6).

- Rotating-beam endurance limit Se' = 0.5 Sut for Sut <= 1400 MPa, else 700 MPa.
- Marin factors Se = ka kb kc kd ke Se': surface ka = a Sut^b (ground 1.58/-0.085,
  machined or cold-drawn 4.51/-0.265, hot-rolled 57.7/-0.718, as-forged 272/-0.995);
  size kb = 1.24 d^-0.107 (2.79 <= d <= 51 mm), 1.51 d^-0.157 (51 < d <= 254 mm), 1 for
  axial load; load kc = 1 bending, 0.85 axial, 0.59 torsion; temperature kd from the
  Shigley 4th-order fit (eq. 6-27, T in deg F, 70-1000 F); reliability ke (table 6-5).
- Notch: Kf = 1 + q (Kt - 1), applied to the alternating and mean stresses.
- Mean-stress criteria for the factor of safety n: modified Goodman
  1/n = sa/Se + sm/Sut; Soderberg 1/n = sa/Se + sm/Sy; Gerber
  n = 1/2 (Sut/sm)^2 (sa/Se) [-1 + sqrt(1 + (2 sm Se / (Sut sa))^2)]; ASME elliptic
  1/n^2 = (sa/Se)^2 + (sm/Sy)^2; Langer first-cycle yield ny = Sy / (sa + sm). A
  compressive mean stress takes n = Se / sa (no benefit credited).
- S-N line (Basquin) between 10^3 and 10^6 cycles: S = a N^b with a = (f Sut)^2 / Se,
  b = -log10(f Sut / Se) / 3 and f = 0.9; stresses at or below Se have infinite life.
- Rainflow counting per ASTM E1049-85 (three-point rule), half cycles for the residue;
  each cycle's equivalent fully reversed stress by Goodman sar = sa / (1 - sm / Sut); damage
  by the Palmgren-Miner rule D = sum n_i / N_i.
"""

import math
from typing import Literal

from pydantic import BaseModel, Field

SURFACE = {
    "ground": (1.58, -0.085),
    "machined": (4.51, -0.265),
    "cold-drawn": (4.51, -0.265),
    "hot-rolled": (57.7, -0.718),
    "as-forged": (272.0, -0.995),
}
LOADING = {"bending": 1.0, "axial": 0.85, "torsion": 0.59}
RELIABILITY = {
    50.0: 1.0,
    90.0: 0.897,
    95.0: 0.868,
    99.0: 0.814,
    99.9: 0.753,
    99.99: 0.702,
    99.999: 0.659,
    99.9999: 0.620,
}
F_1000 = 0.9


def endurance_raw(sut: float) -> float:
    return 0.5 * sut if sut <= 1400.0 else 700.0


def size_factor(d: float | None, loading: str) -> float:
    if loading == "axial" or d is None:
        return 1.0
    if d < 2.79:
        return 1.0
    if d <= 51.0:
        return 1.24 * d**-0.107
    return 1.51 * min(d, 254.0) ** -0.157


def temperature_factor(t_c: float) -> float:
    tf = min(max(t_c * 9.0 / 5.0 + 32.0, 70.0), 1000.0)
    return 0.975 + 0.432e-3 * tf - 0.115e-5 * tf**2 + 0.104e-8 * tf**3 - 0.595e-12 * tf**4


def reliability_factor(r: float) -> float:
    keys = sorted(RELIABILITY)
    if r in RELIABILITY:
        return RELIABILITY[r]
    lo = max((k for k in keys if k <= r), default=keys[0])
    hi = min((k for k in keys if k >= r), default=keys[-1])
    if lo == hi:
        return RELIABILITY[lo]
    t = (r - lo) / (hi - lo)
    return RELIABILITY[lo] + t * (RELIABILITY[hi] - RELIABILITY[lo])


class FatigueIn(BaseModel):
    sut: float = Field(600.0, gt=50.0, le=3000.0)  # MPa
    sy: float = Field(450.0, gt=20.0, le=3000.0)
    se: float | None = Field(None, gt=1.0)  # corrected endurance limit; estimated if absent
    surface: Literal["ground", "machined", "cold-drawn", "hot-rolled", "as-forged"] = "machined"
    diameter: float | None = Field(25.0, gt=0.0, le=1000.0)  # mm, for the size factor
    loading: Literal["bending", "axial", "torsion"] = "bending"
    temperature_c: float = Field(20.0, ge=-60.0, le=540.0)
    reliability: float = Field(50.0, ge=50.0, le=99.9999)
    kt: float = Field(1.0, ge=1.0, le=10.0)
    notch_sensitivity: float = Field(1.0, ge=0.0, le=1.0)
    sigma_a: float = Field(100.0, ge=0.0)  # nominal alternating stress, MPa
    sigma_m: float = Field(0.0)  # nominal mean stress, MPa


def endurance(f: FatigueIn) -> dict[str, float]:
    if f.se is not None:
        return {"Se_prime": f.se, "ka": 1.0, "kb": 1.0, "kc": 1.0, "kd": 1.0, "ke": 1.0, "Se": f.se}
    a, b = SURFACE[f.surface]
    ka = a * f.sut**b
    kb = size_factor(f.diameter, f.loading)
    kc = LOADING[f.loading]
    kd = temperature_factor(f.temperature_c)
    ke = reliability_factor(f.reliability)
    raw = endurance_raw(f.sut)
    return {
        "Se_prime": raw,
        "ka": ka,
        "kb": kb,
        "kc": kc,
        "kd": kd,
        "ke": ke,
        "Se": ka * kb * kc * kd * ke * raw,
    }


def safety_factors(sa: float, sm: float, se: float, sut: float, sy: float) -> dict[str, float]:
    """Factors of safety by each criterion (inf when the stress is zero)."""
    inf = math.inf
    if sa <= 0 and sm <= 0:
        return {
            "goodman": inf,
            "soderberg": inf,
            "gerber": inf,
            "asme_elliptic": inf,
            "langer": inf,
        }
    langer = sy / (sa + abs(sm)) if sa + abs(sm) > 0 else inf
    if sm <= 0:
        n = se / sa if sa > 0 else inf
        return {"goodman": n, "soderberg": n, "gerber": n, "asme_elliptic": n, "langer": langer}
    goodman = 1.0 / (sa / se + sm / sut)
    soderberg = 1.0 / (sa / se + sm / sy)
    if sa > 0:
        gerber = (
            0.5
            * (sut / sm) ** 2
            * (sa / se)
            * (-1.0 + math.sqrt(1.0 + (2.0 * sm * se / (sut * sa)) ** 2))
        )
    else:
        gerber = sut / sm
    elliptic = 1.0 / math.sqrt((sa / se) ** 2 + (sm / sy) ** 2)
    return {
        "goodman": goodman,
        "soderberg": soderberg,
        "gerber": gerber,
        "asme_elliptic": elliptic,
        "langer": langer,
    }


def sn_constants(sut: float, se: float) -> tuple[float, float]:
    a = (F_1000 * sut) ** 2 / se
    b = -math.log10(F_1000 * sut / se) / 3.0
    return a, b


def cycles_to_failure(s_rev: float, sut: float, se: float) -> float:
    """Life in cycles at a fully reversed stress (inf at or below the endurance limit)."""
    if s_rev <= se:
        return math.inf
    if s_rev >= sut:
        return 1.0
    a, b = sn_constants(sut, se)
    n = (s_rev / a) ** (1.0 / b)
    if n < 1e3:  # low-cycle region: straight line in log-log from (1, Sut) to (1e3, f Sut)
        s1000 = F_1000 * sut
        n = 10.0 ** (3.0 * math.log10(sut / s_rev) / math.log10(sut / s1000))
    return n


def status(n: float) -> str:
    return "fail" if n < 1.0 else "marginal" if n < 1.5 else "ok"


def check(f: FatigueIn) -> dict:
    end = endurance(f)
    se = end["Se"]
    kf = 1.0 + f.notch_sensitivity * (f.kt - 1.0)
    sa, sm = kf * f.sigma_a, kf * f.sigma_m
    factors = safety_factors(sa, sm, se, f.sut, f.sy)
    s_rev = sa / (1.0 - sm / f.sut) if 0 < sm < f.sut else sa
    life = cycles_to_failure(s_rev, f.sut, se) if sm < f.sut else 1.0
    warnings = []
    if f.sy > f.sut:
        warnings.append("Yield strength above the ultimate: check the material data.")
    if factors["langer"] < 1.0:
        warnings.append("Yields on the first cycle (Langer factor < 1).")
    a, b = sn_constants(f.sut, se)
    return {
        **end,
        "Kf": kf,
        "sigma_a": sa,
        "sigma_m": sm,
        "factors": factors,
        "status": status(factors["goodman"]),
        "reversed_equivalent": s_rev,
        "life_cycles": life,
        "sn_a": a,
        "sn_b": b,
        "warnings": warnings,
    }


def rainflow(series: list[float]) -> list[dict[str, float]]:
    """ASTM E1049-85 rainflow count: (range, mean, count) with count 1 or 0.5."""
    rev: list[float] = []
    for x in series:  # turning points only
        if rev and x == rev[-1]:
            continue
        if len(rev) >= 2 and (rev[-1] - rev[-2]) * (x - rev[-1]) > 0:
            rev[-1] = x
        else:
            rev.append(x)
    out: list[dict[str, float]] = []
    stack: list[float] = []
    for x in rev:
        stack.append(x)
        while len(stack) >= 3:
            r_x = abs(stack[-1] - stack[-2])
            r_y = abs(stack[-2] - stack[-3])
            if r_x < r_y:
                break
            if len(stack) == 3:
                out.append({"range": r_y, "mean": (stack[0] + stack[1]) / 2.0, "count": 0.5})
                stack.pop(0)
            else:
                out.append({"range": r_y, "mean": (stack[-2] + stack[-3]) / 2.0, "count": 1.0})
                last = stack.pop()
                stack.pop()
                stack.pop()
                stack.append(last)
    for i in range(len(stack) - 1):
        out.append(
            {
                "range": abs(stack[i + 1] - stack[i]),
                "mean": (stack[i + 1] + stack[i]) / 2.0,
                "count": 0.5,
            }
        )
    return out


class HistoryIn(BaseModel):
    series: list[float] = Field(min_length=2, max_length=100_000)  # stress, MPa
    sut: float = Field(600.0, gt=50.0, le=3000.0)
    se: float = Field(200.0, gt=1.0)  # corrected endurance limit, MPa
    repeats: float = Field(1.0, gt=0.0)  # times the history is applied


def damage(h: HistoryIn) -> dict:
    cycles = rainflow(h.series)
    rows, total = [], 0.0
    for c in cycles:
        sa, sm = c["range"] / 2.0, c["mean"]
        s_rev = sa / (1.0 - sm / h.sut) if 0 < sm < h.sut else (sa if sm <= 0 else math.inf)
        n_f = cycles_to_failure(s_rev, h.sut, h.se) if math.isfinite(s_rev) else 1.0
        d = 0.0 if math.isinf(n_f) else c["count"] / n_f
        total += d
        rows.append(
            {**c, "amplitude": sa, "reversed_equivalent": s_rev, "life_cycles": n_f, "damage": d}
        )
    per_pass = total
    return {
        "cycles": rows,
        "damage_per_pass": per_pass,
        "damage": per_pass * h.repeats,
        "passes_to_failure": (1.0 / per_pass) if per_pass > 0 else math.inf,
        "status": "fail" if per_pass * h.repeats >= 1.0 else "ok",
    }
