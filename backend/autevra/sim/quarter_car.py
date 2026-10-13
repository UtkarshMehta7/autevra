"""Quarter-car model: one corner of the vehicle as two masses on springs.

    body (sprung mass m_s)
      |  spring k (linear) and damper (c_bump in compression, c_rebound in extension)
    wheel (unsprung mass m_u)
      |  tyre: linear point contact k_t, no damping, can lift off (no tension)
    road  z_r(t)

States are displacements from static equilibrium, positive up (m, m/s). Integrated with
classical fixed-step 4th-order Runge-Kutta. Each run is repeated at half the step to measure
numerical convergence.

Assumptions and limits (reported with every result):
- vertical motion of one corner only: no pitch, roll or coupling to the other corners;
- linear spring and tyre, bilinear (two-rate) damper, no friction or bump-stop model;
- point-contact tyre: no enveloping of short obstacles, so sharp inputs are overestimated;
- the model is only physical while wheel travel stays within the travel limits; exceeding
  them is reported as a failed criterion, not simulated as a bump-stop impact.
"""

import math
from dataclasses import asdict, dataclass, field

SOLVER_ID = "autevra.quarter_car"
SOLVER_VERSION = "1.0.0"
METHOD = "rk4-fixed-step"
G = 9.80665

ASSUMPTIONS = (
    "Vertical motion of one corner: no pitch, roll or coupling between corners.",
    "Linear spring and tyre; two-rate damper (bump / rebound); no friction.",
    "Point-contact tyre without damping; it can lift off but not pull the wheel down.",
    "No bump-stop or droop-limit model: travel beyond the limits fails the travel criteria.",
    "Short obstacles are not filtered by the tyre footprint, so peaks are conservative.",
)


@dataclass(frozen=True)
class Params:
    """One corner, SI units."""

    sprung_mass: float  # kg
    unsprung_mass: float  # kg
    spring_rate: float  # N/m (wheel rate)
    damping_bump: float  # N·s/m
    damping_rebound: float  # N·s/m
    tyre_stiffness: float  # N/m

    def validate(self) -> list[str]:
        errors = [f"{k} must be positive (got {v:g})" for k, v in asdict(self).items() if v <= 0]
        return errors


@dataclass(frozen=True)
class Road:
    """Road height under the tyre as the car passes at constant speed (SI units).

    ``step``: rises by ``height`` over ``length`` (half-cosine ramp).
    ``bump``: full-cosine bump of ``height`` over ``length``.
    ``pothole``: full-cosine dip of depth ``height`` over ``length``.
    ``flat``: no input.
    """

    kind: str
    height: float = 0.0  # m
    length: float = 1.0  # m
    speed: float = 10.0  # m/s
    start: float = 0.1  # s, time the tyre reaches the event

    @property
    def event_duration(self) -> float:
        return self.length / self.speed

    @property
    def final_height(self) -> float:
        return self.height if self.kind == "step" else 0.0

    def displacement(self, t: float) -> float:
        if self.kind == "flat" or t <= self.start:
            return 0.0
        s = (t - self.start) / self.event_duration
        if self.kind == "step":
            return self.height if s >= 1.0 else self.height * (1.0 - math.cos(math.pi * s)) / 2
        if s >= 1.0:
            return 0.0
        shape = (1.0 - math.cos(2.0 * math.pi * s)) / 2.0
        return self.height * shape if self.kind == "bump" else -self.height * shape


@dataclass(frozen=True)
class Config:
    dt: float = 0.0005  # s
    duration: float = 3.0  # s
    trace_points: int = 600
    convergence_tolerance: float = 0.005  # relative change of key metrics at dt / 2
    check_convergence: bool = True  # False only for perturbation studies around a checked run


@dataclass(frozen=True)
class Initial:
    body: float = 0.0  # m from equilibrium
    wheel: float = 0.0


@dataclass
class Result:
    metrics: dict[str, float | None]
    trace: dict[str, list[float]]
    numerics: dict[str, float | bool | int]
    warnings: list[str] = field(default_factory=list)
    solver: dict[str, str] = field(
        default_factory=lambda: {"id": SOLVER_ID, "version": SOLVER_VERSION, "method": METHOD}
    )


def natural_frequencies(p: Params) -> tuple[float, float]:
    """Undamped 2-DOF natural frequencies (body bounce, wheel hop), Hz."""
    ms, mu, k, kt = p.sprung_mass, p.unsprung_mass, p.spring_rate, p.tyre_stiffness
    a = ms * mu
    b = -(ms * (k + kt) + mu * k)
    c = k * kt
    disc = math.sqrt(b * b - 4 * a * c)
    w1, w2 = math.sqrt((-b - disc) / (2 * a)), math.sqrt((-b + disc) / (2 * a))
    return w1 / (2 * math.pi), w2 / (2 * math.pi)


def _integrate(p: Params, road: Road, config: Config, initial: Initial, dt: float) -> dict:
    """Classical RK4 with scalar locals (no per-step allocations): ~4x faster than tuples."""
    ms, mu, k, kt = p.sprung_mass, p.unsprung_mass, p.spring_rate, p.tyre_stiffness
    cb, cr = p.damping_bump, p.damping_rebound
    preload = (ms + mu) * G
    zr_at = road.displacement

    def accel(zs: float, vs: float, zu: float, vu: float, zr: float) -> tuple[float, float]:
        rate = vu - vs
        f_susp = k * (zu - zs) + (cb if rate > 0 else cr) * rate
        f_tyre = preload + kt * (zr - zu)
        f_tyre = (f_tyre if f_tyre > 0.0 else 0.0) - preload
        return f_susp / ms, (f_tyre - f_susp) / mu

    steps = round(config.duration / dt)
    zs, vs, zu, vu = initial.body, 0.0, initial.wheel, 0.0
    ts, roads, bodies, wheels, accs, tyres = ([0.0] * (steps + 1) for _ in range(6))
    zr0 = zr_at(0.0)
    a0 = accel(zs, vs, zu, vu, zr0)[0]
    roads[0], bodies[0], wheels[0], accs[0] = zr0, zs, zu, a0
    tyres[0] = max(0.0, preload + kt * (zr0 - zu))
    h2, h6 = dt / 2.0, dt / 6.0
    for i in range(steps):
        t = i * dt
        r0, rh, r1 = zr_at(t), zr_at(t + h2), zr_at(t + dt)
        a1s, a1u = accel(zs, vs, zu, vu, r0)
        a2s, a2u = accel(zs + h2 * vs, vs + h2 * a1s, zu + h2 * vu, vu + h2 * a1u, rh)
        v2s, v2u = vs + h2 * a1s, vu + h2 * a1u
        a3s, a3u = accel(zs + h2 * v2s, vs + h2 * a2s, zu + h2 * v2u, vu + h2 * a2u, rh)
        v3s, v3u = vs + h2 * a2s, vu + h2 * a2u
        a4s, a4u = accel(zs + dt * v3s, vs + dt * a3s, zu + dt * v3u, vu + dt * a3u, r1)
        v4s, v4u = vs + dt * a3s, vu + dt * a3u
        zs += h6 * (vs + 2 * v2s + 2 * v3s + v4s)
        zu += h6 * (vu + 2 * v2u + 2 * v3u + v4u)
        vs += h6 * (a1s + 2 * a2s + 2 * a3s + a4s)
        vu += h6 * (a1u + 2 * a2u + 2 * a3u + a4u)
        j = i + 1
        ts[j], roads[j], bodies[j], wheels[j] = j * dt, r1, zs, zu
        accs[j] = accel(zs, vs, zu, vu, r1)[0]
        tyre = preload + kt * (r1 - zu)
        tyres[j] = tyre if tyre > 0.0 else 0.0
    return {
        "t": ts,
        "road": roads,
        "body": bodies,
        "wheel": wheels,
        "body_acc": accs,
        "tyre": tyres,
        "preload": preload,
        "dt": dt,
    }


def _settling_time(run: dict, road: Road) -> float | None:
    """Time after the tyre meets the event until the body stays within the settling band:
    5 % of the event height or 1 mm, whichever is larger."""
    band = max(0.05 * abs(road.height), 0.001)
    final = road.final_height
    last_outside = None
    for t, z in zip(run["t"], run["body"], strict=True):
        if abs(z - final) > band:
            last_outside = t
    if last_outside is None:
        return 0.0
    if last_outside >= run["t"][-1] - run["dt"]:
        return None  # still moving at the end of the run
    return max(0.0, last_outside - road.start)


def _metrics(run: dict, road: Road) -> dict[str, float | None]:
    compression = [w - b for w, b in zip(run["wheel"], run["body"], strict=True)]
    acc = run["body_acc"]
    tyre, preload, dt = run["tyre"], run["preload"], run["dt"]
    final = road.final_height
    peak_body = max(run["body"], key=lambda z: abs(z - final))
    overshoot = None
    if road.kind == "step" and road.height:
        overshoot = max(0.0, (max(run["body"]) - road.height) / road.height * 100.0)
    return {
        "peak_body_acceleration": max(abs(a) for a in acc),
        "rms_body_acceleration": math.sqrt(sum(a * a for a in acc) / len(acc)),
        "max_bump_travel": max(0.0, max(compression)) * 1000.0,
        "max_rebound_travel": max(0.0, -min(compression)) * 1000.0,
        "peak_body_displacement": abs(peak_body - final) * 1000.0,
        "min_tyre_load_ratio": min(tyre) / preload,
        "max_tyre_load_ratio": max(tyre) / preload,
        "lift_off_time": sum(dt for x in tyre if x <= 0.0),
        "settling_time": _settling_time(run, road),
        "step_overshoot": overshoot,
    }


METRICS = {  # id -> (label, unit, lower is better)
    "peak_body_acceleration": ("Peak body acceleration", "m/s²", True),
    "rms_body_acceleration": ("RMS body acceleration", "m/s²", True),
    "max_bump_travel": ("Max bump (compression) travel", "mm", True),
    "max_rebound_travel": ("Max rebound (extension) travel", "mm", True),
    "peak_body_displacement": ("Peak body displacement", "mm", True),
    "min_tyre_load_ratio": ("Min tyre load / static load", "", False),
    "max_tyre_load_ratio": ("Max tyre load / static load", "", True),
    "lift_off_time": ("Time with the tyre off the road", "s", True),
    "settling_time": ("Body settling time", "s", True),
    "step_overshoot": ("Body overshoot on a step", "%", True),
}

# Metrics compared at dt and dt/2 to judge convergence (with an absolute floor).
_CONVERGENCE = {
    "peak_body_acceleration": 0.01, "rms_body_acceleration": 0.01, "max_bump_travel": 0.01,
    "max_rebound_travel": 0.01, "min_tyre_load_ratio": 0.001,
}  # fmt: skip


def _downsample(run: dict, points: int) -> dict[str, list[float]]:
    n = len(run["t"])
    stride = max(1, math.ceil(n / points))
    idx = list(range(0, n, stride))
    if idx[-1] != n - 1:
        idx.append(n - 1)
    compression = [run["wheel"][i] - run["body"][i] for i in idx]
    return {
        "t": [round(run["t"][i], 5) for i in idx],
        "road_mm": [round(run["road"][i] * 1000, 4) for i in idx],
        "body_mm": [round(run["body"][i] * 1000, 4) for i in idx],
        "wheel_mm": [round(run["wheel"][i] * 1000, 4) for i in idx],
        "travel_mm": [round(c * 1000, 4) for c in compression],
        "body_acc": [round(run["body_acc"][i], 5) for i in idx],
        "tyre_load_ratio": [round(run["tyre"][i] / run["preload"], 5) for i in idx],
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
    hop = natural_frequencies(p)[1]
    stability = config.dt * 2 * math.pi * hop  # RK4 is accurate well below ~0.5
    if stability > 0.3:
        warnings.append(f"time step {config.dt:g} s is coarse for the {hop:.1f} Hz wheel hop")
    if road.event_duration < 10 * config.dt:
        warnings.append("the road event is shorter than ten time steps")

    run = _integrate(p, road, config, initial, config.dt)
    fine = _integrate(p, road, config, initial, config.dt / 2)
    metrics, fine_metrics = _metrics(run, road), _metrics(fine, road)

    finite = all(math.isfinite(v) for series in ("body", "wheel", "body_acc") for v in run[series])
    worst = 0.0
    for key, floor in _CONVERGENCE.items():
        a, b = metrics[key], fine_metrics[key]
        assert a is not None and b is not None
        worst = max(worst, abs(a - b) / max(abs(b), floor))
    converged = finite and worst <= config.convergence_tolerance
    if not finite:
        warnings.append("the solution diverged (non-finite values)")
    elif not converged:
        warnings.append(f"metrics changed by {worst:.2%} when the time step was halved")
    if metrics["settling_time"] is None:
        warnings.append(f"the body had not settled after {config.duration:g} s")
    if metrics["lift_off_time"]:
        warnings.append("the tyre left the road; the result is valid within the model")
    return Result(
        metrics=metrics,
        trace=_downsample(run, config.trace_points),
        numerics={
            "dt": config.dt,
            "steps": len(run["t"]) - 1,
            "duration": config.duration,
            "converged": converged,
            "max_relative_change_at_half_step": round(worst, 6),
            "step_to_wheel_hop_ratio": round(stability, 5),
            "finite": finite,
        },  # fmt: skip
        warnings=warnings,
    )
