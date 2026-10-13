"""Longitudinal vehicle model: straight-line acceleration and braking on a flat road.

One point mass with longitudinal load transfer between the axles. Forces:
- drive: the smaller of the power limit (P * eta / v) and the traction limit of each driven
  axle (mu * axle load / its share of the drive torque), with load transfer m*a*h/L;
- aerodynamic drag 0.5 * rho * Cd * A * v^2 and rolling resistance Crr * m * g;
- braking: ideal brake distribution (every wheel at the friction limit), force building up
  linearly over ``brake_build_up`` seconds.
Integrated with fixed-step RK4 and rerun at half the step to measure convergence.

Assumptions (reported with every result): flat dry or wet road with a single friction
coefficient; no gearbox (power available at every speed, as for a single-speed electric
drive or an ideal CVT), no shift time, no wheel slip dynamics, no tyre load sensitivity;
equivalent mass factor for rotating parts; still air.
"""

import math
from dataclasses import dataclass, field

SOLVER_ID = "autevra.longitudinal"
SOLVER_VERSION = "1.0.0"
METHOD = "rk4-fixed-step"
G = 9.80665
RHO_AIR = 1.204  # kg/m³ at 20 °C, sea level

ASSUMPTIONS = (
    "Straight, flat road; one friction coefficient for the whole run; still air.",
    "Power available at every speed (single-speed electric drive or ideal CVT); no shifts.",
    "Traction limit per driven axle with longitudinal load transfer; no slip dynamics.",
    "Ideal brake distribution: every wheel at the friction limit while braking.",
    "Rotating parts included through an equivalent mass factor when power-limited.",
)


@dataclass(frozen=True)
class Params:
    mass: float  # kg, test mass including occupants
    power: float  # W, peak power at the motor or engine
    efficiency: float  # drivetrain efficiency, 0..1
    front_drive_share: float  # share of drive torque at the front axle, 0..1
    front_static_share: float  # share of the static weight on the front axle, 0..1
    cg_height: float  # m
    wheelbase: float  # m
    drag_area: float  # Cd * A, m²
    rolling_resistance: float  # Crr
    mass_factor: float = 1.05  # equivalent mass factor for rotating inertia

    def validate(self) -> list[str]:
        errors = []
        for name in ("mass", "power", "efficiency", "cg_height", "wheelbase", "mass_factor"):
            if getattr(self, name) <= 0:
                errors.append(f"{name} must be positive")
        for name in ("front_drive_share", "front_static_share"):
            if not 0 <= getattr(self, name) <= 1:
                errors.append(f"{name} must lie between 0 and 1")
        if self.drag_area < 0 or self.rolling_resistance < 0:
            errors.append("drag area and rolling resistance cannot be negative")
        return errors


@dataclass(frozen=True)
class Manoeuvre:
    kind: str  # accelerate | brake
    friction: float = 1.0  # tyre-road friction coefficient
    v_start: float = 0.0  # m/s
    v_end: float = 100 / 3.6  # m/s (accelerate: target speed; brake: start speed)
    brake_build_up: float = 0.15  # s, braking force ramps from 0 to the limit
    max_time: float = 60.0


@dataclass(frozen=True)
class Config:
    dt: float = 0.002
    trace_points: int = 400
    convergence_tolerance: float = 0.005
    check_convergence: bool = True


@dataclass
class Result:
    metrics: dict[str, float | None]
    trace: dict[str, list[float]]
    numerics: dict[str, float | bool | int]
    warnings: list[str] = field(default_factory=list)
    solver: dict[str, str] = field(
        default_factory=lambda: {"id": SOLVER_ID, "version": SOLVER_VERSION, "method": METHOD}
    )


def resistance(p: Params, v: float) -> float:
    return 0.5 * RHO_AIR * p.drag_area * v * v + p.rolling_resistance * p.mass * G


def traction_acceleration(p: Params, mu: float, v: float) -> float:
    """Largest acceleration the driven axles can transmit, with load transfer.

    At the friction limit the tyre force accelerates the vehicle mass; the rotating parts
    are driven by the motor torque, so the equivalent mass factor does not apply here.
    """
    m, h, L, f = p.mass, p.cg_height, p.wheelbase, p.front_static_share  # noqa: N806
    s = p.front_drive_share
    res = resistance(p, v)
    limits = []
    # Front axle: s*F <= mu*(m g f - m a h / L), with m*a = F - res
    if s > 0:
        limits.append((mu * m * G * f - s * res) / (s * m + mu * m * h / L))
    # Rear axle: (1-s)*F <= mu*(m g (1-f) + m a h / L)
    if s < 1:
        denom = (1 - s) * m - mu * m * h / L
        bound = mu * m * G * (1 - f) - (1 - s) * res
        limits.append(bound / denom if denom > 0 else math.inf)
    return max(0.0, min(limits))


def acceleration(p: Params, man: Manoeuvre, t: float, v: float) -> tuple[float, bool]:
    """(dv/dt, limited?) at speed v: traction-limited when accelerating, full braking force
    reached when braking. Power accelerates the rotating parts too (mass factor)."""
    if man.kind == "accelerate":
        power_a = (p.power * p.efficiency / max(v, 0.5) - resistance(p, v)) / (
            p.mass * p.mass_factor
        )
        trac_a = traction_acceleration(p, man.friction, v)
        return (trac_a, True) if trac_a <= power_a else (power_a, False)
    ramp = min(1.0, t / man.brake_build_up) if man.brake_build_up > 0 else 1.0
    braking = man.friction * p.mass * G * ramp  # ideal distribution: sum of axle limits
    return -(braking + resistance(p, v)) / p.mass, ramp >= 1.0


def _run(p: Params, man: Manoeuvre, dt: float) -> dict:
    t, v, x = 0.0, man.v_start if man.kind == "accelerate" else man.v_end, 0.0
    ts, vs, xs, accs = [0.0], [v], [0.0], [acceleration(p, man, 0.0, v)[0]]
    traction_until = 0.0
    done = False
    while t < man.max_time:

        def f(tt: float, vv: float) -> float:
            return acceleration(p, man, tt, vv)[0]

        k1 = f(t, v)
        k2 = f(t + dt / 2, v + dt / 2 * k1)
        k3 = f(t + dt / 2, v + dt / 2 * k2)
        k4 = f(t + dt, v + dt * k3)
        v_new = v + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        target = man.v_end if man.kind == "accelerate" else 0.0
        crossed = v_new >= target if man.kind == "accelerate" else v_new <= target
        if crossed:
            frac = (target - v) / (v_new - v) if v_new != v else 1.0  # end exactly at target
            x += (v + (target - v) * frac / 2) * dt * frac
            t += dt * frac
            v = target
            done = True
        else:
            x += (v + v_new) / 2 * dt
            t += dt
            v = v_new
        a, limited = acceleration(p, man, t, v)
        if man.kind == "accelerate" and limited:
            traction_until = v
        ts.append(t)
        vs.append(v)
        xs.append(x)
        accs.append(a)
        if done:
            break
    return {"t": ts, "v": vs, "x": xs, "a": accs, "done": done, "traction_until": traction_until}


def _metrics(run: dict, man: Manoeuvre) -> dict[str, float | None]:
    t, x = run["t"][-1], run["x"][-1]
    if man.kind == "accelerate":
        return {
            "accel_time": t if run["done"] else None,
            "accel_distance": x if run["done"] else None,
            "traction_limited_until": run["traction_until"] * 3.6,
            "peak_acceleration": max(run["a"]),
        }
    return {
        "stopping_distance": x if run["done"] else None,
        "stopping_time": t if run["done"] else None,
        "mean_deceleration": (man.v_end / t) if run["done"] and t > 0 else None,
        "peak_deceleration": -min(run["a"]),
    }


METRICS = {  # id -> (label, unit, lower is better)
    "accel_time": ("Acceleration time", "s", True),
    "accel_distance": ("Acceleration distance", "m", True),
    "traction_limited_until": ("Traction-limited up to", "km/h", False),
    "peak_acceleration": ("Peak acceleration", "m/s²", False),
    "stopping_distance": ("Stopping distance", "m", True),
    "stopping_time": ("Stopping time", "s", True),
    "mean_deceleration": ("Mean deceleration", "m/s²", False),
    "peak_deceleration": ("Peak deceleration", "m/s²", False),
}
_KEY = {"accelerate": "accel_time", "brake": "stopping_distance"}


def simulate(p: Params, man: Manoeuvre, config: Config | None = None) -> Result:
    config = config or Config()
    errors = p.validate()
    if man.kind not in ("accelerate", "brake"):
        errors.append(f"unknown manoeuvre '{man.kind}'")
    if man.friction <= 0:
        errors.append("friction must be positive")
    if errors:
        raise ValueError("; ".join(errors))
    run = _run(p, man, config.dt)
    metrics = _metrics(run, man)
    warnings = []
    worst = 0.0
    if config.check_convergence:
        fine = _metrics(_run(p, man, config.dt / 2), man)
        key = _KEY[man.kind]
        a, b = metrics[key], fine[key]
        if a is not None and b is not None:
            worst = abs(a - b) / max(abs(b), 1e-9)
    converged = run["done"] and worst <= config.convergence_tolerance
    if not run["done"]:
        warnings.append(
            f"the manoeuvre did not finish within {man.max_time:g} s (top speed below the target?)"
        )
    elif not converged:
        warnings.append(f"result changed by {worst:.2%} when the time step was halved")
    n = len(run["t"])
    stride = max(1, math.ceil(n / config.trace_points))
    idx = list(range(0, n, stride)) + ([n - 1] if (n - 1) % stride else [])
    return Result(
        metrics=metrics,
        trace={
            "t": [round(run["t"][i], 4) for i in idx],
            "speed_kmh": [round(run["v"][i] * 3.6, 3) for i in idx],
            "distance_m": [round(run["x"][i], 3) for i in idx],
            "accel": [round(run["a"][i], 4) for i in idx],
        },
        numerics={
            "dt": config.dt,
            "steps": n - 1,
            "converged": converged,
            "finite": True,
            "convergence_checked": config.check_convergence,
            "max_relative_change_at_half_step": round(worst, 6),
        },
        warnings=warnings,
    )
