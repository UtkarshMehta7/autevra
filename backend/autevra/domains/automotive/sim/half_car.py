"""Half-car (bicycle) ride model: body bounce and pitch on two axles.

    front axle (x = +a)            CG            rear axle (x = -b)
       spring 2k_f, damper 2c_f   body m_s, I_y    spring 2k_r, damper 2c_r
       axle 2m_uf                                  axle 2m_ur
       tyre 2k_t                                   tyre 2k_t
       road z_r(t)                                 road z_r(t - L / v)

States are displacements from static equilibrium (m, rad), positive up; pitch follows
ISO 8855 (rotation about +Y, positive nose down), so the body moves by z - a·theta at the
front axle and z + b·theta at the rear. Both corners of an axle move together. Integrated
with classical fixed-step RK4 and repeated at half the step to measure convergence.

The pitch inertia comes from the dynamic index DI = k_y² / (a·b) (k_y the pitch radius of
gyration); DI = 1 makes the axles' ride motions independent and is typical of cars
(about 0.8 to 1.2). It is an assumption reported with every result, not a measurement.
"""

import math
from dataclasses import asdict, dataclass, field

from autevra.domains.automotive.sim.quarter_car import Road

SOLVER_ID = "autevra.half_car"
SOLVER_VERSION = "1.0.0"
METHOD = "rk4-fixed-step"
G = 9.80665

ASSUMPTIONS = (
    "Body bounce and pitch on two axles; the two corners of each axle move together (no roll).",
    "Pitch inertia from a dynamic index of 1.0 (pitch radius of gyration² = a·b), typical of "
    "cars, not measured.",
    "The rear wheels meet the same road event a wheelbase later (constant speed).",
    "Linear springs and tyres; two-rate dampers (bump / rebound); no friction or anti-pitch "
    "geometry.",
    "Point-contact tyres without damping; they can lift off but not pull the axle down.",
    "No bump-stop or droop-limit model: travel beyond the limits fails the travel criteria.",
)


@dataclass(frozen=True)
class Params:
    """Whole vehicle, SI units; spring, damper and tyre values are per corner."""

    sprung_mass: float  # kg, whole body
    front_to_cg: float  # a, m (front axle ahead of the sprung-mass centre)
    rear_to_cg: float  # b, m
    pitch_inertia: float  # I_y, kg·m²
    front_unsprung_mass: float  # kg per corner
    rear_unsprung_mass: float
    front_spring_rate: float  # N/m per corner (wheel rate)
    rear_spring_rate: float
    front_damping_bump: float  # N·s/m per corner
    front_damping_rebound: float
    rear_damping_bump: float
    rear_damping_rebound: float
    tyre_stiffness: float  # N/m per tyre

    def validate(self) -> list[str]:
        return [f"{k} must be positive (got {v:g})" for k, v in asdict(self).items() if v <= 0]

    @property
    def wheelbase(self) -> float:
        return self.front_to_cg + self.rear_to_cg


def pitch_inertia(sprung_mass: float, a: float, b: float, dynamic_index: float = 1.0) -> float:
    return dynamic_index * sprung_mass * a * b


@dataclass(frozen=True)
class Config:
    dt: float = 0.0005  # s
    duration: float = 3.5  # s (the rear axle meets the event a wheelbase later)
    trace_points: int = 600
    convergence_tolerance: float = 0.005
    check_convergence: bool = True


@dataclass(frozen=True)
class Initial:
    heave: float = 0.0  # m
    pitch: float = 0.0  # rad


@dataclass
class Result:
    metrics: dict[str, float | None]
    trace: dict[str, list[float]]
    numerics: dict[str, float | bool | int]
    warnings: list[str] = field(default_factory=list)
    solver: dict[str, str] = field(
        default_factory=lambda: {"id": SOLVER_ID, "version": SOLVER_VERSION, "method": METHOD}
    )


def body_frequencies(p: Params) -> tuple[float, float]:
    """Undamped bounce and pitch frequencies of the body on the ride rates (spring and tyre in
    series, unsprung masses neglected), Hz, from the 2-DOF characteristic equation."""
    kf = 2 * p.front_spring_rate * p.tyre_stiffness / (p.front_spring_rate + p.tyre_stiffness)
    kr = 2 * p.rear_spring_rate * p.tyre_stiffness / (p.rear_spring_rate + p.tyre_stiffness)
    a, b, m, i = p.front_to_cg, p.rear_to_cg, p.sprung_mass, p.pitch_inertia
    k11, k12, k22 = kf + kr, -kf * a + kr * b, kf * a * a + kr * b * b
    # det([k11 - w²m, k12], [k12, k22 - w²I]) = 0
    qa, qb, qc = m * i, -(k11 * i + k22 * m), k11 * k22 - k12 * k12
    disc = math.sqrt(qb * qb - 4 * qa * qc)
    w1, w2 = math.sqrt((-qb - disc) / (2 * qa)), math.sqrt((-qb + disc) / (2 * qa))
    return w1 / (2 * math.pi), w2 / (2 * math.pi)


def _integrate(p: Params, road: Road, config: Config, initial: Initial, dt: float) -> dict:
    m, iy, a, b = p.sprung_mass, p.pitch_inertia, p.front_to_cg, p.rear_to_cg
    muf, mur = 2 * p.front_unsprung_mass, 2 * p.rear_unsprung_mass
    kf, kr, kt = 2 * p.front_spring_rate, 2 * p.rear_spring_rate, 2 * p.tyre_stiffness
    cfb, cfr = 2 * p.front_damping_bump, 2 * p.front_damping_rebound
    crb, crr = 2 * p.rear_damping_bump, 2 * p.rear_damping_rebound
    load_f = m * G * b / (a + b) + muf * G  # static tyre loads per axle
    load_r = m * G * a / (a + b) + mur * G
    delay = (a + b) / road.speed
    zr_at = road.displacement

    def accel(z, vz, th, w, zf, vf, zrr, vr, rf, rr):  # type: ignore[no-untyped-def]
        bf, vbf = z - a * th, vz - a * w  # body at the axles
        br, vbr = z + b * th, vz + b * w
        rate_f, rate_r = vf - vbf, vr - vbr  # > 0: compression
        fsf = kf * (zf - bf) + (cfb if rate_f > 0 else cfr) * rate_f
        fsr = kr * (zrr - br) + (crb if rate_r > 0 else crr) * rate_r
        tf = load_f + kt * (rf - zf)
        tr = load_r + kt * (rr - zrr)
        tf = (tf if tf > 0.0 else 0.0) - load_f
        tr = (tr if tr > 0.0 else 0.0) - load_r
        return (fsf + fsr) / m, (-a * fsf + b * fsr) / iy, (tf - fsf) / muf, (tr - fsr) / mur

    steps = round(config.duration / dt)
    z, vz, th, w = initial.heave, 0.0, initial.pitch, 0.0
    zf = vf = zrr = vr = 0.0
    names = ("t", "road_f", "road_r", "heave", "pitch", "axle_f", "axle_r", "acc", "pitch_acc",
             "tyre_f", "tyre_r")  # fmt: skip
    out = {k: [0.0] * (steps + 1) for k in names}

    def record(j: int, t: float, rf: float, rr: float) -> None:
        az, ath, _, _ = accel(z, vz, th, w, zf, vf, zrr, vr, rf, rr)
        out["t"][j], out["road_f"][j], out["road_r"][j] = t, rf, rr
        out["heave"][j], out["pitch"][j], out["axle_f"][j], out["axle_r"][j] = z, th, zf, zrr
        out["acc"][j], out["pitch_acc"][j] = az, ath
        out["tyre_f"][j] = max(0.0, load_f + kt * (rf - zf))
        out["tyre_r"][j] = max(0.0, load_r + kt * (rr - zrr))

    record(0, 0.0, zr_at(0.0), zr_at(-delay))
    h2, h6 = dt / 2.0, dt / 6.0
    for i in range(steps):
        t = i * dt
        f0, fh, f1 = zr_at(t), zr_at(t + h2), zr_at(t + dt)
        r0, rh, r1 = zr_at(t - delay), zr_at(t + h2 - delay), zr_at(t + dt - delay)
        s0 = (z, vz, th, w, zf, vf, zrr, vr)
        k1 = accel(*s0, f0, r0)
        s1 = (z + h2 * vz, vz + h2 * k1[0], th + h2 * w, w + h2 * k1[1],
              zf + h2 * vf, vf + h2 * k1[2], zrr + h2 * vr, vr + h2 * k1[3])  # fmt: skip
        k2 = accel(*s1, fh, rh)
        s2 = (z + h2 * s1[1], vz + h2 * k2[0], th + h2 * s1[3], w + h2 * k2[1],
              zf + h2 * s1[5], vf + h2 * k2[2], zrr + h2 * s1[7], vr + h2 * k2[3])  # fmt: skip
        k3 = accel(*s2, fh, rh)
        s3 = (z + dt * s2[1], vz + dt * k3[0], th + dt * s2[3], w + dt * k3[1],
              zf + dt * s2[5], vf + dt * k3[2], zrr + dt * s2[7], vr + dt * k3[3])  # fmt: skip
        k4 = accel(*s3, f1, r1)
        z += h6 * (vz + 2 * s1[1] + 2 * s2[1] + s3[1])
        th += h6 * (w + 2 * s1[3] + 2 * s2[3] + s3[3])
        zf += h6 * (vf + 2 * s1[5] + 2 * s2[5] + s3[5])
        zrr += h6 * (vr + 2 * s1[7] + 2 * s2[7] + s3[7])
        vz += h6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        w += h6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        vf += h6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        vr += h6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
        record(i + 1, (i + 1) * dt, f1, r1)
    out["load_f"], out["load_r"], out["dt"] = load_f, load_r, dt
    out["a"], out["b"] = a, b
    return out


def _metrics(run: dict) -> dict[str, float | None]:
    a, b = run["a"], run["b"]
    front_travel = [
        zf - (z - a * th)
        for zf, z, th in zip(run["axle_f"], run["heave"], run["pitch"], strict=True)
    ]  # noqa: E501
    rear_travel = [
        zr - (z + b * th)
        for zr, z, th in zip(run["axle_r"], run["heave"], run["pitch"], strict=True)
    ]  # noqa: E501
    acc, pacc, pitch = run["acc"], run["pitch_acc"], run["pitch"]
    n = len(acc)
    return {
        "peak_heave_acceleration": max(abs(x) for x in acc),
        "rms_heave_acceleration": math.sqrt(sum(x * x for x in acc) / n),
        "peak_pitch_acceleration": math.degrees(max(abs(x) for x in pacc)),
        "rms_pitch_acceleration": math.degrees(math.sqrt(sum(x * x for x in pacc) / n)),
        "peak_pitch_angle": math.degrees(max(abs(x) for x in pitch)),
        "front_max_bump_travel": max(0.0, max(front_travel)) * 1000.0,
        "front_max_rebound_travel": max(0.0, -min(front_travel)) * 1000.0,
        "rear_max_bump_travel": max(0.0, max(rear_travel)) * 1000.0,
        "rear_max_rebound_travel": max(0.0, -min(rear_travel)) * 1000.0,
        "front_min_tyre_load_ratio": min(run["tyre_f"]) / run["load_f"],
        "rear_min_tyre_load_ratio": min(run["tyre_r"]) / run["load_r"],
        "lift_off_time": run["dt"]
        * sum(1 for f, r in zip(run["tyre_f"], run["tyre_r"], strict=True) if f <= 0.0 or r <= 0.0),
    }


METRICS = {  # id -> (label, unit, lower is better)
    "peak_heave_acceleration": ("Peak body heave acceleration", "m/s²", True),
    "rms_heave_acceleration": ("RMS body heave acceleration", "m/s²", True),
    "peak_pitch_acceleration": ("Peak pitch acceleration", "deg/s²", True),
    "rms_pitch_acceleration": ("RMS pitch acceleration", "deg/s²", True),
    "peak_pitch_angle": ("Peak pitch angle", "deg", True),
    "front_max_bump_travel": ("Front max bump travel", "mm", True),
    "front_max_rebound_travel": ("Front max rebound travel", "mm", True),
    "rear_max_bump_travel": ("Rear max bump travel", "mm", True),
    "rear_max_rebound_travel": ("Rear max rebound travel", "mm", True),
    "front_min_tyre_load_ratio": ("Front min tyre load / static load", "", False),
    "rear_min_tyre_load_ratio": ("Rear min tyre load / static load", "", False),
    "lift_off_time": ("Time with a tyre off the road", "s", True),
}

_CONVERGENCE = {
    "peak_heave_acceleration": 0.01, "peak_pitch_acceleration": 0.5,
    "front_max_bump_travel": 0.01, "rear_max_bump_travel": 0.01,
    "front_min_tyre_load_ratio": 0.001, "rear_min_tyre_load_ratio": 0.001,
}  # fmt: skip


def _downsample(run: dict, points: int) -> dict[str, list[float]]:
    n = len(run["t"])
    stride = max(1, math.ceil(n / points))
    idx = list(range(0, n, stride))
    if idx[-1] != n - 1:
        idx.append(n - 1)
    a, b = run["a"], run["b"]
    return {
        "t": [round(run["t"][i], 5) for i in idx],
        "road_front_mm": [round(run["road_f"][i] * 1000, 4) for i in idx],
        "road_rear_mm": [round(run["road_r"][i] * 1000, 4) for i in idx],
        "heave_mm": [round(run["heave"][i] * 1000, 4) for i in idx],
        "pitch_deg": [round(math.degrees(run["pitch"][i]), 5) for i in idx],
        "front_travel_mm": [
            round((run["axle_f"][i] - run["heave"][i] + a * run["pitch"][i]) * 1000, 4) for i in idx
        ],
        "rear_travel_mm": [
            round((run["axle_r"][i] - run["heave"][i] - b * run["pitch"][i]) * 1000, 4) for i in idx
        ],
        "heave_acc": [round(run["acc"][i], 5) for i in idx],
        "front_axle_mm": [round(run["axle_f"][i] * 1000, 4) for i in idx],
        "rear_axle_mm": [round(run["axle_r"][i] * 1000, 4) for i in idx],
        "front_tyre_load_ratio": [round(run["tyre_f"][i] / run["load_f"], 5) for i in idx],
        "rear_tyre_load_ratio": [round(run["tyre_r"][i] / run["load_r"], 5) for i in idx],
    }


def simulate(
    p: Params, road: Road, config: Config | None = None, initial: Initial | None = None
) -> Result:
    config = config or Config()
    initial = initial or Initial()
    errors = p.validate()
    if road.kind not in ("flat", "step", "bump", "pothole"):
        errors.append(f"unknown road kind '{road.kind}'")
    if road.speed <= 0 or road.length <= 0:
        errors.append("road speed and length must be positive")
    if errors:
        raise ValueError("; ".join(errors))

    warnings: list[str] = []
    delay = p.wheelbase / road.speed
    if road.start + delay + road.event_duration >= config.duration:
        warnings.append("the run ends before the rear axle has crossed the event")
    run = _integrate(p, road, config, initial, config.dt)
    metrics = _metrics(run)
    finite = all(math.isfinite(v) for k in ("heave", "pitch") for v in run[k])
    worst = 0.0
    if config.check_convergence:
        fine = _metrics(_integrate(p, road, config, initial, config.dt / 2))
        for key, floor in _CONVERGENCE.items():
            x, y = metrics[key], fine[key]
            assert x is not None and y is not None
            worst = max(worst, abs(x - y) / max(abs(y), floor))
    converged = finite and worst <= config.convergence_tolerance
    if not finite:
        warnings.append("the solution diverged (non-finite values)")
    elif config.check_convergence and not converged:
        warnings.append(f"metrics changed by {worst:.2%} when the time step was halved")
    if metrics["lift_off_time"]:
        warnings.append("a tyre left the road; the result is valid within the model")
    return Result(
        metrics=metrics,
        trace=_downsample(run, config.trace_points),
        numerics={
            "dt": config.dt,
            "steps": len(run["t"]) - 1,
            "duration": config.duration,
            "converged": converged,
            "convergence_checked": config.check_convergence,
            "max_relative_change_at_half_step": round(worst, 6),
            "finite": finite,
            "rear_delay_s": round(delay, 5),
        },  # fmt: skip
        warnings=warnings,
    )
