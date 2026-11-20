"""Mechanisms against closed-form references, and swept motion of a part."""

import math

import cadquery as cq
import numpy as np
import pytest

from autevra import dmu
from autevra import mechanisms as mech


def test_grashof_classes() -> None:
    assert mech.grashof(100, 30, 90, 70) == "crank-rocker"
    assert mech.grashof(30, 100, 90, 70) == "double crank (drag link)"
    assert mech.grashof(100, 90, 30, 70) == "Grashof double rocker"
    assert mech.grashof(100, 60, 30, 20) == "non-Grashof triple rocker"
    assert mech.grashof(100, 50, 100, 50) == "change point"


def test_fourbar_closes_and_keeps_link_lengths() -> None:
    fb = mech.FourBar(ground=100, crank=30, coupler=90, rocker=70, steps=90)
    out = mech.fourbar(fb)
    assert out["full_rotation"]
    for p in out["poses"]:
        (bx, by), (cx, cy) = p["b"], p["c"]
        assert math.hypot(bx, by) == pytest.approx(30)
        assert math.hypot(cx - bx, cy - by) == pytest.approx(90)
        assert math.hypot(cx - 100, cy) == pytest.approx(70)


def test_fourbar_transmission_extremes_match_the_cosine_rule() -> None:
    # Extremes occur with the crank in line with the ground: |BD| = g - a and g + a.
    g, a, b, c = 100.0, 30.0, 90.0, 70.0
    out = mech.fourbar(mech.FourBar(ground=g, crank=a, coupler=b, rocker=c, steps=360))

    def mu(d: float) -> float:
        return math.degrees(math.acos((b * b + c * c - d * d) / (2 * b * c)))

    assert out["transmission_min_deg"] == pytest.approx(mu(g - a), abs=1e-3)
    assert out["transmission_max_deg"] == pytest.approx(mu(g + a), abs=1e-3)


def test_rocker_swing_of_a_crank_rocker() -> None:
    # Limits of the rocker: crank and coupler in line (b + a and b - a from A).
    g, a, b, c = 100.0, 30.0, 90.0, 70.0

    def rocker_angle(reach: float) -> float:
        return math.acos((g * g + c * c - reach * reach) / (2 * g * c))

    swing = math.degrees(rocker_angle(b + a) - rocker_angle(b - a))
    out = mech.fourbar(mech.FourBar(ground=g, crank=a, coupler=b, rocker=c, steps=720))
    assert out["rocker_swing_deg"] == pytest.approx(swing, abs=0.02)


def test_parallelogram_coupler_point_traces_a_circle() -> None:
    fb = mech.FourBar(ground=80, crank=40, coupler=80, rocker=40, point_along=40,
                      point_off=10, steps=36)  # fmt: skip
    for th in (10.0, 75.0, 140.0):
        p = mech.fourbar_pose(fb, th)
        assert p is not None
        assert p["coupler_deg"] == pytest.approx(0.0, abs=1e-9)  # coupler stays parallel
        assert math.hypot(p["p"][0] - 40, p["p"][1] - 10) == pytest.approx(40)


def test_non_grashof_linkage_does_not_turn_fully() -> None:
    out = mech.fourbar(mech.FourBar(ground=100, crank=60, coupler=30, rocker=20))
    assert not out["full_rotation"] and 0 < out["assembled_fraction"] < 1


def test_slider_crank_stroke_and_dead_centres() -> None:
    sc = mech.SliderCrank(crank=40, rod=140, rpm=6000, steps=720)
    out = mech.slider_crank(sc)
    assert out["stroke_mm"] == pytest.approx(80)
    assert out["x_max_mm"] == pytest.approx(180) and out["x_min_mm"] == pytest.approx(100)
    # In-line: acceleration at top dead centre is r w^2 (1 + r/l).
    w = 6000 * 2 * math.pi / 60
    assert out["a_max_m_s2"] == pytest.approx(0.040 * w * w * (1 + 40 / 140), rel=1e-6)
    assert out["rows"][0]["v_m_s"] == pytest.approx(0.0, abs=1e-9)


def test_slider_derivatives_match_finite_differences() -> None:
    sc = mech.SliderCrank(crank=35, rod=120, offset=12)
    h = 1e-3
    for th in (20.0, 110.0, 250.0):
        x0, dx, ddx = mech.slider_at(sc, th)
        xp, xm = mech.slider_at(sc, th + h)[0], mech.slider_at(sc, th - h)[0]
        hr = math.radians(h)
        assert dx == pytest.approx((xp - xm) / (2 * hr), rel=1e-6)
        assert ddx == pytest.approx((xp - 2 * x0 + xm) / hr**2, rel=1e-3)


def test_offset_slider_crank_stroke_exceeds_twice_the_crank() -> None:
    out = mech.slider_crank(mech.SliderCrank(crank=40, rod=140, offset=30))
    assert out["stroke_mm"] > 80
    with pytest.raises(ValueError):
        mech.slider_crank(mech.SliderCrank(crank=40, rod=50, offset=30))


def test_joint_motion_matrices() -> None:
    rev = mech.Joint(kind="revolute", origin=(10, 0, 0), axis=(0, 0, 2), lo=0, hi=90, steps=2)
    m = mech.motion(rev, 90.0)
    assert m @ np.array([20.0, 0, 0, 1]) == pytest.approx([10, 10, 0, 1])
    assert m @ np.array([10.0, 0, 5, 1]) == pytest.approx([10, 0, 5, 1])  # on the axis
    pri = mech.Joint(kind="prismatic", axis=(0, 3, 4), lo=0, hi=10, steps=2)
    assert mech.motion(pri, 10.0)[:3, 3] == pytest.approx([0, 6, 8])


def _at(x: float, y: float = 0.0) -> np.ndarray:
    m = np.eye(4)
    m[0, 3], m[1, 3] = x, y
    return m


@pytest.mark.cad
def test_swept_door_finds_the_closest_approach() -> None:
    # A 100 x 10 x 10 arm hinged at the origin about Z, lying along +X; a post on the Y axis.
    arm = dmu.Placed("arm", "Arm", cq.Workplane().box(100, 10, 10).val(), _at(50))
    post = dmu.Placed("post", "Post", cq.Workplane().box(10, 10, 10).val(), _at(0, 118))
    far = dmu.Placed("far", "Far", cq.Workplane().box(10, 10, 10).val(), _at(0, 900))
    joint = mech.Joint(kind="revolute", lo=0, hi=90, steps=10)
    rep = mech.sweep(arm, [post, far], joint, clearance_mm=20.0)
    pairs = {p.other: p for p in rep.pairs}
    # At 90 deg the arm spans y 0-100; the post spans y 113-123: 13 mm apart.
    assert pairs["post"].status == "too close"
    assert pairs["post"].distance_mm == pytest.approx(13.0, abs=1e-3)
    assert pairs["post"].at == pytest.approx(90.0)
    assert pairs["far"].status == "clear" and not pairs["far"].exact
    assert rep.unit == "deg" and rep.box_max[1] == pytest.approx(100.0, abs=0.01)


@pytest.mark.cad
def test_swept_slide_interferes_and_envelope_volume() -> None:
    block = dmu.Placed("b", "Block", cq.Workplane().box(10, 10, 10).val(), _at(0))
    wall = dmu.Placed("w", "Wall", cq.Workplane().box(10, 10, 10).val(), _at(26))
    joint = mech.Joint(kind="prismatic", axis=(1, 0, 0), lo=0, hi=20, steps=5)
    rep = mech.sweep(block, [wall], joint, clearance_mm=2.0, with_volume=True)
    assert rep.pairs[0].status == "interference" and rep.pairs[0].at == pytest.approx(20.0)
    # Steps of 5 mm overlap, so the union is the full 30 x 10 x 10 slot.
    assert rep.envelope_mm3 == pytest.approx(3000.0, rel=1e-6)
    short = mech.sweep(block, [wall], joint.model_copy(update={"hi": 10.0}), clearance_mm=2.0)
    assert short.pairs[0].status == "clear" and short.pairs[0].distance_mm == pytest.approx(6.0)
