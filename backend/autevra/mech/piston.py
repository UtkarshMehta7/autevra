"""Reciprocating piston engines: geometry, ideal cycles, slider-crank kinematics, inertia
balance of any cylinder arrangement, torque and power from a BMEP curve, and a statistical
mass estimate.

Methods (all open, stated with their limits):
- displacement V_d = pi/4 B^2 S z; mean piston speed c_m = 2 S n;
- air-standard cycle efficiencies: Otto eta = 1 - r^(1-gamma); Diesel
  eta = 1 - r^(1-gamma) (rc^gamma - 1) / (gamma (rc - 1)); with gamma = 1.4 (air standard)
  and 1.3 (a fuel-air approximation closer to real working fluid);
- four-stroke torque T = p_me V_d / (4 pi), power P = T omega, with the brake mean
  effective pressure following a stated curve shape between idle and the speed limit;
- slider-crank with crank radius r and rod length l (lambda = r / l): exact piston
  position, and the classical two-term series for the inertia force
  F = m_rec r w^2 (cos t + lambda cos 2t) per cylinder along its axis;
- balance: the primary and secondary inertia forces of every cylinder are summed as
  vectors in the plane normal to the crankshaft over a full revolution (any inline, V or
  opposed arrangement and crank-pin phasing), with their moments about the engine's
  centre; results are the largest resultant over the revolution, in units of one
  cylinder's primary amplitude m_rec r w^2 (forces) or that times the bore pitch
  (moments); rotating masses are taken as counterweighted;
- reciprocating mass and engine mass from statistical fits to modern automotive engines
  (stated tolerance about 20 %).

Limits: ideal cycles bound real efficiency (real brake efficiency is roughly half to two
thirds of the air-standard value); the BMEP curve is an assumed shape, not a combustion
model; no gas-exchange, friction-map or knock modelling.
"""

import math
from typing import Literal

import numpy as np
from pydantic import BaseModel, Field, model_validator

Layout = Literal["inline", "V", "boxer"]


class EngineSpec(BaseModel):
    name: str = "I4 2.0 petrol"
    fuel: Literal["petrol", "diesel"] = "petrol"
    layout: Layout = "inline"
    cylinders: int = Field(4, ge=1, le=16)
    bank_angle: float = Field(90.0, ge=15.0, le=180.0)  # V engines, degrees
    flat_plane: bool = False  # V8: flat-plane crank instead of cross-plane
    bore: float = Field(86.0, gt=20.0, le=400.0)  # mm
    stroke: float = Field(86.0, gt=20.0, le=500.0)  # mm
    rod_ratio: float = Field(1.65, ge=1.3, le=2.5)  # rod length / stroke
    compression_ratio: float = Field(10.5, ge=6.0, le=25.0)
    turbo: bool = False
    bmep_max: float = Field(12.5, gt=4.0, le=35.0)  # bar, peak brake mean effective pressure
    rpm_peak_torque: float = Field(4300.0, ge=800.0, le=15_000.0)
    rpm_max: float = Field(6800.0, ge=1500.0, le=20_000.0)
    rpm_idle: float = Field(800.0, ge=300.0, le=2000.0)

    @model_validator(mode="after")
    def _consistent(self) -> "EngineSpec":
        if self.layout in ("V", "boxer") and self.cylinders % 2:
            raise ValueError(f"a {self.layout} engine needs an even number of cylinders")
        if not self.rpm_idle < self.rpm_peak_torque < self.rpm_max:
            raise ValueError("speeds must rise: idle < peak torque < maximum")
        return self


# --- crank-pin phasing per arrangement (degrees of crank rotation) ----------------------

_INLINE: dict[int, list[float]] = {
    1: [0], 2: [0, 180], 3: [0, 120, 240], 4: [0, 180, 180, 0], 5: [0, 144, 216, 288, 72],
    6: [0, 120, 240, 240, 120, 0], 8: [0, 180, 90, 270, 270, 90, 180, 0],
}  # fmt: skip
FIRING: dict[tuple[str, int], str] = {
    ("inline", 1): "1", ("inline", 2): "1-2", ("inline", 3): "1-3-2",
    ("inline", 4): "1-3-4-2", ("inline", 5): "1-2-4-5-3", ("inline", 6): "1-5-3-6-2-4",
    ("inline", 8): "1-6-2-5-8-3-7-4", ("V", 6): "1-4-2-5-3-6", ("V", 8): "1-5-4-8-6-3-7-2",
    ("V", 12): "1-7-5-11-3-9-6-12-2-8-4-10", ("boxer", 4): "1-3-2-4",
    ("boxer", 6): "1-6-2-4-3-5",
}  # fmt: skip


def _pins(n: int) -> list[float]:
    if n in _INLINE:
        return list(_INLINE[n])
    return [i * 720.0 / n % 360 for i in range(n)]  # even spacing as a fallback


def cylinders(spec: EngineSpec) -> list[dict[str, float]]:
    """Every cylinder: crank-pin angle (deg), axis angle from vertical (deg), position
    along the crankshaft (in bore pitches, centred on the engine) and bank (-1, 0, 1)."""
    n = spec.cylinders
    out = []
    if spec.layout == "inline":
        for i, pin in enumerate(_pins(n)):
            out.append({"pin": pin, "axis": 0.0, "z": i - (n - 1) / 2, "bank": 0.0})
        return out
    pairs = n // 2
    if spec.layout == "V":
        cross_plane = pairs == 4 and not spec.flat_plane  # V8: pins at 0, 90, 270, 180
        row = [0.0, 90.0, 270.0, 180.0] if cross_plane else _pins(pairs)
        half = spec.bank_angle / 2
        for i, pin in enumerate(row):  # two cylinders share each crank pin
            for bank in (-1.0, 1.0):
                out.append({"pin": pin, "axis": bank * half, "z": i - (pairs - 1) / 2 + 0.25 * bank,
                            "bank": bank})  # fmt: skip
        return out
    # boxer: opposed pairs on pins 180° apart, the pair's cylinders slightly staggered
    row = _pins(pairs) if pairs > 1 else [0.0]
    for i, pin in enumerate(row):
        for k, bank in enumerate((-1.0, 1.0)):
            out.append({"pin": (pin + 180.0 * k) % 360, "axis": 90.0 * bank,
                        "z": i - (pairs - 1) / 2 + 0.25 * bank, "bank": bank})  # fmt: skip
    return out


def balance(spec: EngineSpec, samples: int = 720) -> dict[str, float]:
    """Largest resultant primary and secondary inertia forces and moments over a crank
    revolution, in units of one cylinder's primary amplitude (moments: times bore pitch)."""
    lam = 1.0 / (2.0 * spec.rod_ratio)  # r / l
    theta = np.linspace(0.0, 2 * np.pi, samples, endpoint=False)
    res: dict[str, np.ndarray] = {k: np.zeros((samples, 2)) for k in ("F1", "F2", "M1", "M2")}
    for c in cylinders(spec):
        a = math.radians(c["axis"])
        axis = np.array([math.sin(a), math.cos(a)])  # direction of the cylinder in the plane
        t = theta + math.radians(c["pin"]) - a  # crank angle seen from this cylinder
        f1, f2 = np.cos(t), lam * np.cos(2 * t)
        res["F1"] += np.outer(f1, axis)
        res["F2"] += np.outer(f2, axis)
        res["M1"] += np.outer(f1 * c["z"], axis)
        res["M2"] += np.outer(f2 * c["z"], axis)
    out = {k: float(np.max(np.linalg.norm(v, axis=1))) for k, v in res.items()}
    return {"primary_force": out["F1"], "secondary_force": out["F2"],
            "primary_moment": out["M1"], "secondary_moment": out["M2"]}  # fmt: skip


# --- geometry, cycles, performance ---------------------------------------------------


def displacement_l(spec: EngineSpec) -> float:
    return math.pi / 4 * spec.bore**2 * spec.stroke * spec.cylinders / 1e6


def otto_efficiency(r: float, gamma: float = 1.4) -> float:
    return 1.0 - r ** (1.0 - gamma)


def diesel_efficiency(r: float, cutoff: float = 2.0, gamma: float = 1.4) -> float:
    return 1.0 - r ** (1.0 - gamma) * (cutoff**gamma - 1.0) / (gamma * (cutoff - 1.0))


def bmep_curve(spec: EngineSpec, rpm: float) -> float:
    """Assumed brake mean effective pressure shape (bar). Naturally aspirated: rising as
    1 - 0.30 x^2 to the peak at the peak-torque speed. Turbocharged: a plateau from 55 % of
    that speed (boost threshold), falling as 1 - 0.6 x^2 below it. Above the peak-torque
    speed both fall as 1 - d x^2 to the limit (d = 0.28 natural, 0.35 turbo)."""
    n_t, n_max = spec.rpm_peak_torque, spec.rpm_max
    if rpm <= n_t:
        if spec.turbo:
            knee = 0.55 * n_t
            f = 1.0 if rpm >= knee else 1.0 - 0.6 * ((knee - rpm) / knee) ** 2
        else:
            f = 1.0 - 0.30 * ((n_t - rpm) / n_t) ** 2
        return spec.bmep_max * f
    drop = 0.35 if spec.turbo else 0.28
    return spec.bmep_max * (1.0 - drop * ((rpm - n_t) / (n_max - n_t)) ** 2)


def torque_nm(spec: EngineSpec, rpm: float) -> float:
    return bmep_curve(spec, rpm) * 1e5 * displacement_l(spec) * 1e-3 / (4 * math.pi)


def curve(spec: EngineSpec, points: int = 40) -> list[dict[str, float]]:
    rpms = np.linspace(spec.rpm_idle, spec.rpm_max, points)
    return [{"rpm": float(n), "torque_nm": float(torque_nm(spec, n)),
             "power_kw": float(torque_nm(spec, n) * 2 * math.pi * n / 60 / 1e3),
             "bmep_bar": float(bmep_curve(spec, n))} for n in rpms]  # fmt: skip


def piston_position(spec: EngineSpec, crank_deg: float) -> float:
    """Distance of the piston pin below top dead centre (mm), exact slider-crank."""
    r = spec.stroke / 2
    rod = spec.rod_ratio * spec.stroke
    t = math.radians(crank_deg)
    return r * (1 - math.cos(t)) + rod - math.sqrt(rod**2 - (r * math.sin(t)) ** 2)


def reciprocating_mass_kg(spec: EngineSpec) -> float:
    """Piston, pin and rings plus a third of the rod: about 0.62 g per cm³ of bore cubed for
    modern petrol engines; diesel pistons about 35 % heavier (statistical, about 20 %)."""
    base = 0.62e-6 * spec.bore**3
    return base * (1.35 if spec.fuel == "diesel" else 1.0)


def mass_kg(spec: EngineSpec) -> float:
    """Dry engine mass (statistical fit to modern aluminium-head automotive engines,
    about 20 %): 30 kg + 17 kg per cylinder + 22 kg per litre; diesel x1.25; turbo x1.08."""
    m = 30.0 + 17.0 * spec.cylinders + 22.0 * displacement_l(spec)
    return m * (1.25 if spec.fuel == "diesel" else 1.0) * (1.08 if spec.turbo else 1.0)


def analyse(spec: EngineSpec) -> dict:
    vd = displacement_l(spec)
    pts = curve(spec, 60)
    peak_t = max(pts, key=lambda p: p["torque_nm"])
    peak_p = max(pts, key=lambda p: p["power_kw"])
    flat = [p["rpm"] for p in pts if p["torque_nm"] >= 0.995 * peak_t["torque_nm"]]
    r = spec.compression_ratio
    ideal = diesel_efficiency(r) if spec.fuel == "diesel" else otto_efficiency(r)
    fuel_air = (diesel_efficiency(r, gamma=1.3) if spec.fuel == "diesel"
                else otto_efficiency(r, gamma=1.3))  # fmt: skip
    piston_speed = 2 * spec.stroke / 1000 * spec.rpm_max / 60
    m_rec = reciprocating_mass_kg(spec)
    omega = 2 * math.pi * spec.rpm_max / 60
    primary_amp = m_rec * spec.stroke / 2000 * omega**2  # N, one cylinder at max speed
    bal = balance(spec)
    checks = []

    def check(cid: str, label: str, ok: bool, warn: bool, msg: str) -> None:
        checks.append({"id": cid, "label": label,
                       "status": "pass" if ok else "warn" if warn else "fail",
                       "message": msg})  # fmt: skip

    check(
        "piston_speed",
        "Mean piston speed",
        piston_speed <= 22,
        piston_speed <= 25,
        f"{piston_speed:.1f} m/s at {spec.rpm_max:.0f} rpm (production engines stay under "
        "about 20-22 m/s; racing about 25)",
    )
    bs = spec.bore / spec.stroke
    check(
        "bore_stroke",
        "Bore / stroke",
        0.75 <= bs <= 1.35,
        0.6 <= bs <= 1.6,
        f"{bs:.2f} (automotive engines 0.8-1.3)",
    )
    limit = 28.0 if spec.fuel == "diesel" else (26.0 if spec.turbo else 14.0)
    check(
        "bmep",
        "Peak BMEP",
        spec.bmep_max <= limit,
        spec.bmep_max <= limit * 1.15,
        f"{spec.bmep_max:.1f} bar (typical limit {limit:.0f} bar for this kind of engine)",
    )
    rmax = 18.0 if spec.fuel == "diesel" else (11.0 if spec.turbo else 13.5)
    rmin = 14.0 if spec.fuel == "diesel" else 8.0
    check(
        "compression",
        "Compression ratio",
        rmin <= r <= rmax,
        rmin - 1 <= r <= rmax + 1.5,
        f"{r:.1f} (typical {rmin:.0f}-{rmax:.1f} for {'diesel' if spec.fuel == 'diesel' else 'turbo petrol' if spec.turbo else 'petrol'}; higher risks "  # noqa: E501
        f"{'excessive peak pressure' if spec.fuel == 'diesel' else 'knock'})",
    )
    free = bal["primary_force"] < 1e-6 and bal["secondary_force"] < 1e-6
    check("balance", "Free forces", free, bal["primary_force"] < 1e-6,
          "no free primary or secondary force" if free else
          f"free forces: primary {bal['primary_force']:.2f}, secondary "
          f"{bal['secondary_force']:.2f} (x one cylinder's primary); balance shafts or mounts "
          "must handle them")  # fmt: skip
    return {
        "displacement_l": vd, "firing_order": FIRING.get((spec.layout, spec.cylinders), "even"),
        "peak_torque_nm": peak_t["torque_nm"], "peak_torque_rpm": peak_t["rpm"],
        "torque_band_rpm": [min(flat), max(flat)],  # within 0.5 % of the peak
        "peak_power_kw": peak_p["power_kw"], "peak_power_rpm": peak_p["rpm"],
        "specific_power_kw_per_l": peak_p["power_kw"] / vd,
        "mean_piston_speed_ms": piston_speed,
        "efficiency": {"air_standard": ideal, "fuel_air_approx": fuel_air},
        "kinematics": {"crank_radius_mm": spec.stroke / 2,
                       "rod_length_mm": spec.rod_ratio * spec.stroke,
                       "lambda": 1 / (2 * spec.rod_ratio),
                       "reciprocating_mass_kg": m_rec,
                       "primary_force_one_cylinder_n": primary_amp},
        "balance": bal, "balance_n": {k: v * primary_amp for k, v in bal.items()
                                       if k.endswith("force")},
        "mass_kg": mass_kg(spec), "curve": pts, "checks": checks,
        "cylinders": cylinders(spec),
    }  # fmt: skip
