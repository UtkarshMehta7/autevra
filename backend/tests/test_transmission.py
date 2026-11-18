"""Stepped transmission design: ratio rules, a transaxle whose pairs all sit on one
centre distance, ISO 6336-style life factors, traction with load transfer, performance."""

import math

import pytest
from fastapi.testclient import TestClient

from autevra.elements import transmission as tr


def test_first_gear_takes_the_larger_of_grade_and_launch():
    t = tr.TransmissionIn()
    overall, _, final = tr.ratios(t)
    e = t.engine
    launch = e.redline_rpm * math.pi / 30 * t.tyre_radius_m / (60 / 3.6)
    a = math.atan(0.35)
    grade = (
        t.mass_kg
        * tr.G
        * (t.rolling_resistance * math.cos(a) + math.sin(a))
        * t.tyre_radius_m
        / (e.peak_torque_Nm * t.driveline_efficiency)
    )
    assert overall[0] == pytest.approx(max(launch, grade))
    assert overall[-1] / final == pytest.approx(t.top_gearbox_ratio)


def test_top_speed_balances_power_and_road_load():
    t = tr.TransmissionIn()
    _, v, _ = tr.ratios(t)
    p = t.engine.peak_power_kW * 1000 * t.driveline_efficiency
    assert tr.road_load(t, v) * v == pytest.approx(p, rel=1e-6)


def test_geometric_and_progressive_steps():
    geo, _, _ = tr.ratios(tr.TransmissionIn(progression="geometric"))
    steps = [a / b for a, b in zip(geo, geo[1:], strict=False)]
    assert max(steps) == pytest.approx(min(steps))
    pro, _, _ = tr.ratios(tr.TransmissionIn(progression="progressive", phi2=1.08))
    steps = [a / b for a, b in zip(pro, pro[1:], strict=False)]
    assert all(s1 > s2 for s1, s2 in zip(steps, steps[1:], strict=False))  # closer at the top
    assert steps[-2] / steps[-1] == pytest.approx(1.08)


def test_every_pair_sits_on_the_centre_distance():
    out = tr.design(tr.TransmissionIn(centre_distance=85.0))
    seen = set()
    for g in out["gears"]:
        p = g["pair"]
        assert (p["d1"] + p["d2"]) / 2 == pytest.approx(85.0, abs=1e-9)
        assert 15 <= p["helix_deg"] <= 35
        assert abs(p["error_pct"]) < 4.0
        assert (p["z1"], p["z2"]) not in seen
        seen.add((p["z1"], p["z2"]))
    assert out["gears"][0]["pair"]["load_cycles"] < out["gears"][-1]["pair"]["load_cycles"]


def test_life_factors():
    assert tr.life_factors(1e3) == (pytest.approx(2.5, rel=1e-3), 1.6)
    assert tr.life_factors(3e6)[0] == pytest.approx(1.0)
    assert tr.life_factors(1e9) == (1.0, 1.0)
    y, z = tr.life_factors(1e5)
    assert y == pytest.approx((3e6 / 1e5) ** (math.log(2.5) / math.log(3e3))) and z == pytest.approx(1.6)


def test_rating_against_allowables():
    out = tr.design(tr.TransmissionIn(face_width=24.0))
    for g in out["gears"]:
        p = g["pair"]
        if not p.get("overloaded"):
            assert p["sigma_F"] <= p["sigma_FP"] and p["sigma_H"] <= p["sigma_HP"]
        assert p["sigma_FP"] == pytest.approx(500 * 2 * p["Y_NT"] / 1.3)
    narrow = tr.design(tr.TransmissionIn(face_width=8.0))
    assert any("no standard module passes" in w for w in narrow["warnings"])


def test_traction_with_load_transfer():
    base = tr.TransmissionIn(
        mass_kg=2000, driven_axle_share=0.5, cg_height_m=0.5, wheelbase_m=2.5, grip=1.0
    )
    w = 2000 * tr.G
    rear = tr.traction_limit(base.model_copy(update={"drive": "rear"}))
    front = tr.traction_limit(base.model_copy(update={"drive": "front"}))
    awd = tr.traction_limit(base.model_copy(update={"drive": "all", "driven_axle_share": 1.0}))
    assert rear == pytest.approx(w * 0.5 / 0.8) and front == pytest.approx(w * 0.5 / 1.2)
    assert awd == pytest.approx(w) and front < rear < awd


def test_performance_ordering_and_sanity():
    eng = {
        "idle_rpm": 800,
        "peak_torque_Nm": 816,
        "torque_from_rpm": 1800,
        "torque_to_rpm": 4000,
        "peak_power_kW": 360,
        "power_rpm": 6000,
        "redline_rpm": 6500,
    }
    base = {
        "mass_kg": 2100,
        "tyre_radius_m": 0.336,
        "drag_area_m2": 0.73,
        "engine": eng,
        "gears": 8,
        "grip": 1.1,
        "cg_height_m": 0.48,
        "wheelbase_m": 2.93,
    }
    times = {
        d: tr.design(
            tr.TransmissionIn(**base, drive=d, driven_axle_share=1.0 if d == "all" else 0.5)
        )["zero_to_100_s"]
        for d in ("front", "rear", "all")
    }
    assert times["all"] < times["rear"] < times["front"]
    assert 3.5 < times["all"] < 6.0
    small = tr.design(
        tr.TransmissionIn(
            mass_kg=1200,
            drag_area_m2=0.62,
            gears=5,
            engine={
                "peak_torque_Nm": 140,
                "torque_from_rpm": 2000,
                "torque_to_rpm": 4200,
                "peak_power_kW": 66,
                "power_rpm": 5500,
                "redline_rpm": 6200,
            },
        )
    )
    assert 175 < small["v_max_kmh"] < 195 and 11 < small["zero_to_100_s"] < 16


def test_engine_curve_checks():
    with pytest.raises(ValueError, match="above the"):
        tr.EngineCurve(peak_torque_Nm=320, torque_to_rpm=4500, peak_power_kW=150)
    with pytest.raises(ValueError, match="must rise"):
        tr.EngineCurve(torque_from_rpm=5000, torque_to_rpm=4000)
    e = tr.EngineCurve()
    assert e.torque(3000) == e.peak_torque_Nm
    assert e.torque(e.power_rpm) == pytest.approx(
        e.peak_power_kW * 1000 / (e.power_rpm * math.pi / 30)
    )


def test_api(client: TestClient, project: str):
    out = client.post("/api/elements/transmission", json={"gears": 7}).json()
    assert len(out["gears"]) == 7 and out["traction"]
    inp = client.get(f"/api/projects/{project}/elements/transmission-inputs").json()
    assert inp["mass_kg"] > 0 and inp["drive"] in ("front", "rear", "all")
    assert client.post("/api/elements/transmission", json={**inp, "gears": 6}).status_code == 200
