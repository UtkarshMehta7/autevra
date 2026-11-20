"""Piston-engine kernel against closed-form results."""

import math

import pytest

from autevra.mech import piston as p


def _bal(**kw: object) -> dict[str, float]:
    return p.balance(p.EngineSpec(**kw))  # type: ignore[arg-type]


def test_displacement_and_torque_from_bmep() -> None:
    spec = p.EngineSpec(bore=86, stroke=86, cylinders=4)
    vd = math.pi / 4 * 86**2 * 86 * 4 / 1e6
    assert p.displacement_l(spec) == pytest.approx(vd)
    # T = p_me V_d / (4 pi) at the peak-torque speed
    assert p.torque_nm(spec, spec.rpm_peak_torque) == pytest.approx(
        12.5e5 * vd * 1e-3 / (4 * math.pi))  # fmt: skip


def test_cycle_efficiencies() -> None:
    assert p.otto_efficiency(10) == pytest.approx(1 - 10**-0.4)
    assert p.otto_efficiency(10) == pytest.approx(0.6019, abs=1e-4)
    # with a cutoff ratio of 1 the Diesel cycle tends to the Otto cycle
    assert p.diesel_efficiency(18, cutoff=1.0001) == pytest.approx(p.otto_efficiency(18), abs=1e-4)
    assert p.diesel_efficiency(18) < p.otto_efficiency(18)


def test_slider_crank_positions() -> None:
    spec = p.EngineSpec(stroke=90, rod_ratio=1.6)
    assert p.piston_position(spec, 0) == pytest.approx(0.0, abs=1e-9)
    assert p.piston_position(spec, 180) == pytest.approx(90.0)
    r, rod = 45.0, 144.0  # at 90° the piston is past mid-stroke by l - sqrt(l² - r²)
    assert p.piston_position(spec, 90) == pytest.approx(r + rod - math.sqrt(rod**2 - r**2))


LAM = 1 / (2 * 1.65)


@pytest.mark.parametrize(("kw", "expected"), [
    ({"cylinders": 1}, {"primary_force": 1, "secondary_force": LAM}),
    ({"cylinders": 3}, {"primary_force": 0, "secondary_force": 0,
                        "primary_moment": math.sqrt(3)}),
    ({"cylinders": 4}, {"primary_force": 0, "secondary_force": 4 * LAM, "primary_moment": 0,
                        "secondary_moment": 0}),
    ({"cylinders": 5}, {"primary_force": 0, "secondary_force": 0}),
    ({"cylinders": 6}, {"primary_force": 0, "secondary_force": 0, "primary_moment": 0,
                        "secondary_moment": 0}),
    ({"layout": "V", "cylinders": 8}, {"primary_force": 0, "secondary_force": 0,
                                       "primary_moment": math.sqrt(10), "secondary_moment": 0}),
    ({"layout": "V", "cylinders": 8, "flat_plane": True},
     {"primary_force": 0, "secondary_force": 4 * math.sqrt(2) * LAM, "primary_moment": 0}),
    ({"layout": "V", "cylinders": 12, "bank_angle": 60},
     {"primary_force": 0, "secondary_force": 0, "primary_moment": 0, "secondary_moment": 0}),
    ({"layout": "boxer", "cylinders": 4}, {"primary_force": 0, "secondary_force": 0,
                                           "primary_moment": 0}),
    ({"layout": "boxer", "cylinders": 6}, {"primary_force": 0, "secondary_force": 0,
                                           "primary_moment": 0, "secondary_moment": 0}),
])  # fmt: skip
def test_balance_matches_textbook_results(kw: dict, expected: dict) -> None:
    got = _bal(**kw)
    for key, value in expected.items():
        assert got[key] == pytest.approx(value, abs=1e-6), key


def test_inline_five_primary_couple() -> None:
    # the 1-2-4-5-3 inline five keeps a small primary couple (about 0.45 x pitch)
    assert _bal(cylinders=5)["primary_moment"] == pytest.approx(0.449, abs=0.01)


def test_invalid_specs_are_rejected() -> None:
    with pytest.raises(ValueError):
        p.EngineSpec(layout="V", cylinders=5)
    with pytest.raises(ValueError):
        p.EngineSpec(rpm_peak_torque=7000, rpm_max=6500)


def test_analysis_checks() -> None:
    out = p.analyse(p.EngineSpec(rpm_max=9000))  # 25.8 m/s piston speed: too fast
    ps = next(c for c in out["checks"] if c["id"] == "piston_speed")
    assert ps["status"] == "fail"
    v12 = p.analyse(p.EngineSpec(layout="V", cylinders=12, bank_angle=60))
    assert next(c for c in v12["checks"] if c["id"] == "balance")["status"] == "pass"
    assert 100 < p.mass_kg(p.EngineSpec()) < 180  # a 2.0 litre four: about 130-150 kg
