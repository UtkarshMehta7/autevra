"""Verification of the longitudinal solver against closed-form results."""

import pytest

from autevra.sim import longitudinal as lg

BASE = lg.Params(
    mass=1500, power=100e3, efficiency=0.9, front_drive_share=1.0, front_static_share=0.6,
    cg_height=0.55, wheelbase=2.7, drag_area=0.0, rolling_resistance=0.0, mass_factor=1.0,
)  # fmt: skip
V100 = 100 / 3.6


def _p(**kw: float) -> lg.Params:
    return lg.Params(**{**BASE.__dict__, **kw})


def test_pure_power_limit_matches_energy_balance() -> None:
    # Huge friction: never traction-limited; t = m v^2 / (2 P eta) (start speed floor aside).
    r = lg.simulate(_p(), lg.Manoeuvre("accelerate", friction=50))
    assert r.metrics["accel_time"] == pytest.approx(1500 * V100**2 / (2 * 100e3 * 0.9), rel=0.01)


def test_pure_traction_limit_with_load_transfer() -> None:
    # Huge power: always traction-limited. FWD: a = mu g f / (1 + mu h / L).
    r = lg.simulate(_p(power=1e9), lg.Manoeuvre("accelerate", friction=0.8))
    a = 0.8 * lg.G * 0.6 / (1 + 0.8 * 0.55 / 2.7)
    assert r.metrics["accel_time"] == pytest.approx(V100 / a, rel=1e-3)
    assert r.metrics["traction_limited_until"] == pytest.approx(100, abs=0.5)


def test_load_transfer_favours_rear_drive() -> None:
    fwd = lg.simulate(_p(power=1e9), lg.Manoeuvre("accelerate"))
    rwd = lg.simulate(_p(power=1e9, front_drive_share=0.0, front_static_share=0.4),
                      lg.Manoeuvre("accelerate"))  # same driven-axle static load  # fmt: skip
    assert rwd.metrics["accel_time"] < fwd.metrics["accel_time"]
    # A fixed torque split must suit the dynamic loads: a front-biased 60/40 split saturates
    # the front tyres as load moves rearwards, a 40/60 split uses both axles.
    front_biased = _p(power=1e9, front_drive_share=0.6)
    matched = _p(power=1e9, front_drive_share=0.4)
    assert lg.traction_acceleration(front_biased, 1.0, 0) < lg.traction_acceleration(
        _p(front_drive_share=0.0, front_static_share=0.4), 1.0, 0
    )
    assert lg.traction_acceleration(matched, 1.0, 0) > 0.95 * lg.G


def test_braking_distance_matches_closed_form() -> None:
    r = lg.simulate(_p(), lg.Manoeuvre("brake", friction=0.9, brake_build_up=0.0))
    assert r.metrics["stopping_distance"] == pytest.approx(V100**2 / (2 * 0.9 * lg.G), rel=1e-3)
    ramp = lg.simulate(_p(), lg.Manoeuvre("brake", friction=0.9, brake_build_up=0.2))
    # A linear build-up over T adds about v*T/2 (minus the small speed lost meanwhile).
    extra = ramp.metrics["stopping_distance"] - r.metrics["stopping_distance"]
    assert extra == pytest.approx(V100 * 0.2 / 2, rel=0.05)


def test_drag_and_rolling_resistance_slow_acceleration_and_help_braking() -> None:
    clean = lg.simulate(_p(), lg.Manoeuvre("accelerate"))
    loaded = lg.simulate(_p(drag_area=0.8, rolling_resistance=0.012), lg.Manoeuvre("accelerate"))
    assert loaded.metrics["accel_time"] > clean.metrics["accel_time"]
    b_clean = lg.simulate(_p(), lg.Manoeuvre("brake"))
    b_loaded = lg.simulate(_p(drag_area=0.8, rolling_resistance=0.012), lg.Manoeuvre("brake"))
    assert b_loaded.metrics["stopping_distance"] < b_clean.metrics["stopping_distance"]


def test_unreachable_speed_is_reported() -> None:
    r = lg.simulate(_p(power=5e3, drag_area=0.8), lg.Manoeuvre("accelerate", max_time=30))
    assert r.metrics["accel_time"] is None and not r.numerics["converged"]
    assert any("did not finish" in w for w in r.warnings)


def test_convergence_and_validation() -> None:
    r = lg.simulate(_p(drag_area=0.7), lg.Manoeuvre("accelerate"))
    assert r.numerics["converged"] and r.numerics["max_relative_change_at_half_step"] < 1e-3
    with pytest.raises(ValueError, match="front_drive_share"):
        lg.simulate(_p(front_drive_share=1.5), lg.Manoeuvre("accelerate"))
