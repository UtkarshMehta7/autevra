"""Stepped-gearbox acceleration from an engine torque curve."""

import pytest

from autevra.domains.automotive.sim import geared as gd
from autevra.domains.automotive.sim import longitudinal as lon
from autevra.mech import piston as pk


def _engine(spec: pk.EngineSpec) -> gd.Engine:
    c = pk.curve(spec, 60)
    return gd.Engine(tuple(x["rpm"] for x in c), tuple(x["torque_nm"] for x in c))


def _car(power: float, mass: float = 1345, front: float = 1.0) -> lon.Params:
    return lon.Params(mass=mass, power=power, efficiency=0.9, front_drive_share=front,
                      front_static_share=0.61, cg_height=0.52, wheelbase=2.51, drag_area=0.66,
                      rolling_resistance=0.012)  # fmt: skip


def test_matches_a_published_compact_car() -> None:
    """A 2.0 litre naturally aspirated four (about 90 kW) in a 1,270 kg front-drive hatch
    plus driver: published 0-100 km/h about 10.5-11 s (VW Golf IV 2.0)."""
    eng = _engine(pk.EngineSpec(bore=82.5, stroke=92.8, bmep_max=11.8, rpm_peak_torque=3200,
                                rpm_max=6500))  # fmt: skip
    p = _car(eng.peak_power[0])
    out = gd.performance(p, eng, 0.31)
    assert out["zero_to_100_s"] == pytest.approx(10.8, abs=1.0)


def test_gears_never_beat_the_ideal_cvt_and_top_speed_balances_power() -> None:
    eng = _engine(pk.EngineSpec())
    p = _car(eng.peak_power[0])
    geared = gd.performance(p, eng, 0.31)
    cvt = lon.simulate(p, lon.Manoeuvre(kind="accelerate")).metrics["accel_time"]
    assert geared["zero_to_100_s"] >= cvt * 0.98
    v = geared["top_speed_kmh"] / 3.6
    assert eng.peak_power[0] * p.efficiency == pytest.approx(lon.resistance(p, v) * v, rel=1e-3)


def test_gear_design_rules() -> None:
    eng = _engine(pk.EngineSpec())
    gears = gd.design_gears(_car(eng.peak_power[0]), eng, 0.31)
    assert len(gears) == 6 and gears == sorted(gears, reverse=True)
    ratios = [a / b for a, b in zip(gears, gears[1:], strict=False)]
    assert max(ratios) == pytest.approx(min(ratios))  # geometric progression
    big = _engine(pk.EngineSpec(layout="V", cylinders=8, turbo=True, bmep_max=22,
                                rpm_peak_torque=3000, rpm_max=7000))  # fmt: skip
    assert len(gd.design_gears(_car(big.peak_power[0]), big, 0.33)) == 8
