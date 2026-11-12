"""Electric machine and gas-turbine kernels against closed-form results."""

import math

import pytest

from autevra.mech import electric as em
from autevra.mech import turbine as gt


def test_torque_from_shear_stress() -> None:
    s = em.MotorSpec(stator_diameter=200, rotor_ratio=0.6, stack_length=100)
    dr, length = 0.12, 0.1
    assert em.torque(s, 50) == pytest.approx(math.pi / 2 * 50e3 * dr**2 * length)


def test_constant_power_above_base_speed_and_efficiency() -> None:
    s = em.MotorSpec()
    t = em.torque(s, s.shear_peak_kpa)
    p_base = t * s.base_rpm
    assert em.envelope_torque(s, 2 * s.base_rpm) * 2 * s.base_rpm == pytest.approx(p_base)
    t_cont = em.torque(s, s.shear_continuous_kpa)
    eta = em.efficiency(s, s.base_rpm, t_cont)  # rated point: 2.5 + 1.2 + small losses
    assert eta == pytest.approx(1 / (1 + 0.025 + 0.012 + 0.005 * (5000 / 16000) ** 2), rel=1e-6)
    out = em.analyse(s)
    assert 0.95 < out["peak_efficiency"] < 0.99
    assert 2 < out["power_density_kw_per_kg"] < 8  # automotive range


def test_ideal_turbojet_matches_brayton() -> None:
    """With perfect components, no losses and one gas, the thermal efficiency at rest (all
    exhaust kinetic energy counted) tends to 1 - PR^-(gamma-1)/gamma."""
    ideal = {
        "eta_c": 1,
        "eta_t": 1,
        "eta_b": 1,
        "eta_n": 1,
        "eta_m": 1,
        "burner_loss": 0,
        "inlet_recovery": 1,
        "cp_h": 1005,
        "gamma_h": 1.4,
    }
    s = gt.TurbineSpec(pressure_ratio=10, tit_k=1400, **ideal)
    out = gt.cycle(s)
    assert out["thermal_efficiency"] == pytest.approx(gt.ideal_brayton_efficiency(10), rel=0.03)


def test_real_turbojet_and_turboshaft() -> None:
    jet = gt.cycle(gt.TurbineSpec())
    assert 0.015 < jet["fuel_air_ratio"] < 0.03
    assert 600 < jet["specific_thrust"] < 1000  # N per kg/s, typical turbojets
    assert 20 < jet["tsfc_g_per_kn_s"] < 40
    shaft = gt.cycle(gt.TurbineSpec(kind="turboshaft"))
    assert 250 < shaft["sfc_g_per_kwh"] < 450  # small turboshafts
    hot = gt.cycle(gt.TurbineSpec(tit_k=1600))
    assert hot["specific_thrust"] > jet["specific_thrust"]
    with pytest.raises(ValueError):
        gt.cycle(gt.TurbineSpec(tit_k=900, pressure_ratio=40))
