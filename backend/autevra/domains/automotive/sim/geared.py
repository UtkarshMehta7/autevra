"""Full-throttle acceleration through a stepped gearbox, driven by an engine torque curve.

Gear design (stated rules, concept level): the top gear puts the engine at its
peak-power speed at the power-limited top speed; first gear makes the peak engine torque
just reach the driven axles' static friction limit; the gears between follow a geometric
progression. Six gears below 250 kW, eight above.

Simulation: one point mass; wheel force = T(n) i eta / r_dyn, limited by the traction of
the driven axles with load transfer (``longitudinal.traction_acceleration``); drag and
rolling resistance; rotating inertia through a mass factor that grows with the overall
ratio (1.04 + 0.0025 i^2, a common estimate); upshift at the rev limit or when the next
gear gives more wheel force, with a shift time without drive; explicit integration at a
fixed small step. Limits: no clutch slip at launch (engine held at the peak-torque speed
until the gear's road speed exceeds it), no tyre slip dynamics, no turbo lag.
"""

import math
from dataclasses import dataclass

from autevra.domains.automotive.sim import longitudinal as lon

G = lon.G


@dataclass(frozen=True)
class Engine:
    rpm: tuple[float, ...]
    torque: tuple[float, ...]  # N·m at each speed

    def at(self, n: float) -> float:
        rpm, tq = self.rpm, self.torque
        if n <= rpm[0]:
            return tq[0]
        if n >= rpm[-1]:
            return 0.0
        for i in range(1, len(rpm)):
            if n <= rpm[i]:
                f = (n - rpm[i - 1]) / (rpm[i] - rpm[i - 1])
                return tq[i - 1] + f * (tq[i] - tq[i - 1])
        return 0.0

    @property
    def peak_power(self) -> tuple[float, float]:
        """(W, rpm) at peak power."""
        best = max(zip(self.rpm, self.torque, strict=True), key=lambda p: p[0] * p[1])
        return best[1] * best[0] * 2 * math.pi / 60, best[0]

    @property
    def peak_torque(self) -> tuple[float, float]:
        n, t = max(zip(self.rpm, self.torque, strict=True), key=lambda p: p[1])
        return t, n


def top_speed(p: lon.Params, power: float) -> float:
    """Speed where the drive power equals the road load (m/s), by bisection."""
    lo, hi = 1.0, 150.0
    for _ in range(80):
        v = (lo + hi) / 2
        if power * p.efficiency > lon.resistance(p, v) * v:
            lo = v
        else:
            hi = v
    return lo


def design_gears(p: lon.Params, eng: Engine, radius: float, mu: float = 1.0) -> list[float]:
    power, n_pp = eng.peak_power
    v_top = top_speed(p, power)
    top = (n_pp * 2 * math.pi / 60) * radius / v_top
    t_max, _ = eng.peak_torque
    driven = p.front_drive_share * p.front_static_share + (1 - p.front_drive_share) * (
        1 - p.front_static_share
    )  # share of weight on the driven wheels (static)
    first = mu * p.mass * G * max(driven, 0.3) * radius / (t_max * p.efficiency)
    gears = 6 if power < 250e3 else 8
    first = min(max(first, top * 2.8), top * 6.5)  # keep a plausible spread
    step = (first / top) ** (1 / (gears - 1))
    return [first / step**k for k in range(gears)]


def accelerate(p: lon.Params, eng: Engine, radius: float, gears: list[float],
               v_end: float = 100 / 3.6, mu: float = 1.0, shift_time: float = 0.2,
               dt: float = 0.002, max_time: float = 60.0) -> dict:  # fmt: skip
    rpm_max = eng.rpm[-1] * 0.995
    _, n_launch = eng.peak_torque
    t = v = x = 0.0
    gear, shifting = 0, 0.0
    shifts: list[float] = []
    trace: dict[str, list[float]] = {"t": [], "v": [], "gear": [], "rpm": []}

    def wheel_force(g: int, speed: float) -> tuple[float, float]:
        n = max(speed / radius * gears[g] * 60 / (2 * math.pi), n_launch if g == 0 else 0.0)
        return eng.at(min(n, eng.rpm[-1])) * gears[g] * p.efficiency / radius, n

    while v < v_end and t < max_time:
        force, n = wheel_force(gear, v)
        if shifting > 0:
            force, shifting = 0.0, shifting - dt
        elif gear + 1 < len(gears):
            nxt, _ = wheel_force(gear + 1, v)
            if n >= rpm_max or nxt > force:
                gear += 1
                shifts.append(t)
                shifting = shift_time
                force = 0.0
        if n >= rpm_max and gear + 1 >= len(gears):
            break  # flat out in top gear
        mass_factor = 1.04 + 0.0025 * gears[gear] ** 2
        power_a = (force - lon.resistance(p, v)) / (p.mass * mass_factor)
        a = min(power_a, lon.traction_acceleration(p, mu, v)) if force > 0 else \
            -lon.resistance(p, v) / p.mass  # fmt: skip
        v = max(v + a * dt, 0.0)
        x += v * dt
        t += dt
        if not trace["t"] or t - trace["t"][-1] >= 0.05:
            trace["t"].append(round(t, 3))
            trace["v"].append(round(v * 3.6, 2))
            trace["gear"].append(gear + 1)
            trace["rpm"].append(round(n))
    reached = v >= v_end
    return {"time_s": t if reached else None, "distance_m": x, "shifts": len(shifts),
            "trace": trace, "reached": reached}  # fmt: skip


def performance(p: lon.Params, eng: Engine, radius: float, mu: float = 1.0) -> dict:
    gears = design_gears(p, eng, radius, mu)
    power, n_pp = eng.peak_power
    to100 = accelerate(p, eng, radius, gears, 100 / 3.6, mu)
    to200 = accelerate(p, eng, radius, gears, 200 / 3.6, mu)
    return {
        "gears": [round(g, 3) for g in gears],
        "top_speed_kmh": top_speed(p, power) * 3.6,
        "zero_to_100_s": to100["time_s"], "zero_to_200_s": to200["time_s"],
        "trace": to100["trace"] if to200["time_s"] is None else to200["trace"],
        "peak_power_kw": power / 1e3, "peak_power_rpm": n_pp,
        "assumptions": [
            "stepped gearbox designed from the top speed and the launch traction limit",
            "upshift at the rev limit or when the next gear gives more wheel force; "
            "0.2 s shift without drive",
            "launch with the engine held at its peak-torque speed (no clutch model)",
            "flat road, still air, one friction coefficient (1.0)"],
    }  # fmt: skip
