"""Verification of the quarter-car solver against closed-form results."""

import math

import numpy as np
import pytest

from autevra.core import derived as d
from autevra.core.parameters import default_values
from autevra.sim import quarter_car as q

P = q.Params(
    sprung_mass=395, unsprung_mass=45, spring_rate=26_000, damping_bump=1500,
    damping_rebound=3000, tyre_stiffness=200_000,
)  # fmt: skip
LINEAR = q.Params(**{**P.__dict__, "damping_rebound": 1500})


def _exact_free_response(p: q.Params, x0: np.ndarray, times: list[float]) -> np.ndarray:
    """Linear 2-DOF free vibration: x(t) = expm(A t) x0, via the eigen-decomposition of A."""
    ms, mu, k, c, kt = (
        p.sprung_mass,
        p.unsprung_mass,
        p.spring_rate,
        p.damping_bump,
        p.tyre_stiffness,
    )
    a = np.array([
        [0, 1, 0, 0],
        [-k / ms, -c / ms, k / ms, c / ms],
        [0, 0, 0, 1],
        [k / mu, c / mu, -(k + kt) / mu, -c / mu],
    ])  # fmt: skip
    lam, vec = np.linalg.eig(a)
    coeff = np.linalg.solve(vec, x0)
    return np.array([np.real(vec @ (coeff * np.exp(lam * t))) for t in times])


def test_flat_road_stays_at_equilibrium() -> None:
    result = q.simulate(P, q.Road("flat"))
    assert result.metrics["peak_body_acceleration"] == 0
    assert result.metrics["min_tyre_load_ratio"] == pytest.approx(1)
    assert max(abs(z) for z in result.trace["body_mm"]) == 0


def test_free_vibration_matches_the_exact_linear_solution() -> None:
    result = q.simulate(LINEAR, q.Road("flat"), initial=q.Initial(body=0.01))
    exact = _exact_free_response(LINEAR, np.array([0.01, 0, 0, 0]), result.trace["t"])
    body = np.array(result.trace["body_mm"]) / 1000
    wheel = np.array(result.trace["wheel_mm"]) / 1000
    assert np.max(np.abs(body - exact[:, 0])) < 1e-6  # metres: under a micrometre
    assert np.max(np.abs(wheel - exact[:, 2])) < 1e-6


def test_natural_frequencies_match_the_characteristic_equation() -> None:
    body, hop = q.natural_frequencies(P)
    for f in (body, hop):
        w2 = (2 * math.pi * f) ** 2
        ms, mu, k, kt = P.sprung_mass, P.unsprung_mass, P.spring_rate, P.tyre_stiffness
        assert (k - ms * w2) * (k + kt - mu * w2) - k * k == pytest.approx(0, abs=1e-3 * k * kt)
    # The textbook ride frequency (spring and tyre in series) is within 1 % of the body mode.
    assert d.ride_frequency(default_values(), "front") == pytest.approx(body, rel=0.01)


def test_step_settles_at_the_new_road_height() -> None:
    result = q.simulate(
        P, q.Road("step", height=0.025, length=0.25, speed=8.0), q.Config(duration=5)
    )
    assert result.trace["body_mm"][-1] == pytest.approx(25, abs=0.05)
    assert result.trace["wheel_mm"][-1] == pytest.approx(25, abs=0.05)
    assert result.metrics["settling_time"] is not None
    assert result.metrics["step_overshoot"] > 0


def test_half_step_convergence_is_measured() -> None:
    result = q.simulate(P, q.Road("bump", height=0.05, length=1.0, speed=8.0))
    assert result.numerics["converged"] is True
    assert result.numerics["max_relative_change_at_half_step"] < 1e-3


def test_damper_uses_bump_rate_in_compression() -> None:
    road = q.Road("bump", height=0.05, length=0.5, speed=10.0)
    stiff_bump = q.simulate(q.Params(**{**P.__dict__, "damping_bump": 6000}), road)
    stiff_rebound = q.simulate(q.Params(**{**P.__dict__, "damping_rebound": 6000}), road)
    base = q.simulate(P, road)
    # More bump damping resists compression; more rebound damping does not.
    assert stiff_bump.metrics["max_bump_travel"] < base.metrics["max_bump_travel"]
    assert stiff_rebound.metrics["max_bump_travel"] == pytest.approx(
        base.metrics["max_bump_travel"], rel=0.05
    )


def test_tyre_lift_off_is_detected_and_flagged() -> None:
    result = q.simulate(P, q.Road("pothole", height=0.05, length=0.6, speed=40 / 3.6))
    assert result.metrics["min_tyre_load_ratio"] == 0
    assert result.metrics["lift_off_time"] > 0
    assert any("left the road" in w for w in result.warnings)


def test_runs_are_deterministic() -> None:
    road = q.Road("pothole", height=0.04, length=0.6, speed=10.0)
    assert q.simulate(P, road).metrics == q.simulate(P, road).metrics


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="sprung_mass"):
        q.simulate(q.Params(**{**P.__dict__, "sprung_mass": -1}), q.Road("flat"))
    with pytest.raises(ValueError, match="road kind"):
        q.simulate(P, q.Road("cobbles"))


def test_coarse_time_step_is_flagged() -> None:
    result = q.simulate(P, q.Road("bump", 0.05, 1.0, 8.0), q.Config(dt=0.01, duration=1))
    assert any("coarse" in w for w in result.warnings)
