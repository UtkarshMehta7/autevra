"""Half-car verification: decoupling at dynamic index 1 against the verified quarter car,
closed-form frequencies, pitch sign, wheelbase delay and numerical convergence."""

import math

import pytest

from autevra.domains.automotive.sim import half_car as hc
from autevra.domains.automotive.sim import quarter_car as qc

M, A, B = 1400.0, 1.2, 1.5


def _params(dynamic_index: float = 1.0, **changes: float) -> hc.Params:
    base = dict(
        sprung_mass=M, front_to_cg=A, rear_to_cg=B,
        pitch_inertia=hc.pitch_inertia(M, A, B, dynamic_index),
        front_unsprung_mass=40.0, rear_unsprung_mass=45.0,
        front_spring_rate=28000.0, rear_spring_rate=32000.0,
        front_damping_bump=1500.0, front_damping_rebound=3200.0,
        rear_damping_bump=1600.0, rear_damping_rebound=3400.0,
        tyre_stiffness=250000.0,
    )  # fmt: skip
    return hc.Params(**(base | changes))


def _corner(p: hc.Params, axle: str) -> qc.Params:
    share = p.rear_to_cg if axle == "front" else p.front_to_cg
    return qc.Params(
        sprung_mass=p.sprung_mass * share / p.wheelbase / 2,
        unsprung_mass=getattr(p, f"{axle}_unsprung_mass"),
        spring_rate=getattr(p, f"{axle}_spring_rate"),
        damping_bump=getattr(p, f"{axle}_damping_bump"),
        damping_rebound=getattr(p, f"{axle}_damping_rebound"),
        tyre_stiffness=p.tyre_stiffness,
    )


ROAD = qc.Road("step", 0.025, 0.25, 30 / 3.6)


def test_flat_road_stays_at_equilibrium() -> None:
    r = hc.simulate(_params(), qc.Road("flat"), hc.Config(duration=1.0))
    assert r.metrics["peak_heave_acceleration"] < 1e-12
    assert r.metrics["peak_pitch_angle"] < 1e-12


@pytest.mark.parametrize("road", [ROAD, qc.Road("bump", 0.075, 3.7, 25 / 3.6),
                                  qc.Road("pothole", 0.05, 0.6, 40 / 3.6)])  # fmt: skip
def test_at_dynamic_index_one_each_axle_is_its_quarter_car(road: qc.Road) -> None:
    p = _params()
    cfg = hc.Config(duration=3.5)
    run = hc._integrate(p, road, cfg, hc.Initial(), cfg.dt)
    front = qc._integrate(_corner(p, "front"), road, qc.Config(duration=3.5), qc.Initial(), cfg.dt)
    body_front = [z - A * th for z, th in zip(run["heave"], run["pitch"], strict=True)]
    assert max(abs(x - y) for x, y in zip(body_front, front["body"], strict=True)) < 1e-9
    assert max(abs(x - y) for x, y in zip(run["axle_f"], front["wheel"], strict=True)) < 1e-9

    delay = p.wheelbase / road.speed
    rear_road = qc.Road(road.kind, road.height, road.length, road.speed, road.start + delay)
    rear = qc._integrate(_corner(p, "rear"), rear_road, qc.Config(duration=3.5), qc.Initial(),
                         cfg.dt)  # fmt: skip
    body_rear = [z + B * th for z, th in zip(run["heave"], run["pitch"], strict=True)]
    assert max(abs(x - y) for x, y in zip(body_rear, rear["body"], strict=True)) < 1e-6


def test_body_frequencies_match_the_axle_ride_frequencies_at_index_one() -> None:
    p = _params()
    bounce, pitch = hc.body_frequencies(p)
    expected = []
    for axle in ("front", "rear"):
        c = _corner(p, axle)
        ride = c.spring_rate * c.tyre_stiffness / (c.spring_rate + c.tyre_stiffness)
        expected.append(math.sqrt(ride / c.sprung_mass) / (2 * math.pi))
    assert sorted((bounce, pitch)) == pytest.approx(sorted(expected), rel=1e-9)


def _eigen_frequencies(p: hc.Params) -> list[float]:
    """Exact undamped frequencies of the 4-DOF linear system (heave, pitch, two axles), Hz."""
    import numpy as np

    a, b = p.front_to_cg, p.rear_to_cg
    kf, kr, kt = 2 * p.front_spring_rate, 2 * p.rear_spring_rate, 2 * p.tyre_stiffness
    mass = np.diag([p.sprung_mass, p.pitch_inertia, 2 * p.front_unsprung_mass,
                    2 * p.rear_unsprung_mass])  # fmt: skip
    k = np.array([
        [kf + kr, -kf * a + kr * b, -kf, -kr],
        [-kf * a + kr * b, kf * a * a + kr * b * b, kf * a, -kr * b],
        [-kf, kf * a, kf + kt, 0.0],
        [-kr, -kr * b, 0.0, kr + kt],
    ])  # fmt: skip
    w2 = np.linalg.eigvals(np.linalg.solve(mass, k)).real
    return sorted(float(np.sqrt(x) / (2 * np.pi)) for x in w2)


def test_free_pitch_oscillates_at_the_exact_eigenfrequency() -> None:
    """Undamped, axle rates balanced (k_f·a = k_r·b) so pitch is a clean body mode."""
    p = _params(dynamic_index=1.2, front_damping_bump=1e-9, front_damping_rebound=1e-9,
                rear_damping_bump=1e-9, rear_damping_rebound=1e-9)  # fmt: skip
    p = hc.Params(**{**p.__dict__, "rear_spring_rate": p.front_spring_rate * A / B})
    cfg = hc.Config(dt=0.0005, duration=6.0)
    run = hc._integrate(p, qc.Road("flat"), cfg, hc.Initial(pitch=0.005), cfg.dt)
    th, t = run["pitch"], run["t"]
    crossings = [t[i] for i in range(1, len(th)) if th[i - 1] > 0 >= th[i]]
    measured = (len(crossings) - 1) / (crossings[-1] - crossings[0])
    body_modes = _eigen_frequencies(p)[:2]
    assert min(abs(measured - f) / f for f in body_modes) < 0.01
    # The quick closed form (unsprung masses neglected) is within a few per cent.
    assert min(abs(measured - f) / f for f in hc.body_frequencies(p)) < 0.05


def test_front_wheel_meets_a_step_first_so_the_nose_rises() -> None:
    p = _params(dynamic_index=1.1)
    r = hc.simulate(p, ROAD)
    delay = p.wheelbase / ROAD.speed
    t, pitch = r.trace["t"], r.trace["pitch_deg"]
    before_rear = [x for x, tt in zip(pitch, t, strict=True) if tt < ROAD.start + delay]
    assert min(before_rear) < -0.1  # ISO 8855: negative pitch is nose up
    assert r.numerics["rear_delay_s"] == pytest.approx(delay, abs=1e-5)


def test_default_scenarios_converge() -> None:
    for road in (ROAD, qc.Road("bump", 0.075, 3.7, 25 / 3.6)):
        r = hc.simulate(_params(dynamic_index=1.1), road)
        assert r.numerics["converged"], r.warnings
