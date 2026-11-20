"""Harness and pipe routing checks against hand calculations."""

import math

import pytest

from autevra import routing


def test_length_and_turning() -> None:
    length, turn = routing.length_and_turns([(0, 0, 0), (100, 0, 0), (100, 100, 0)])
    assert length == pytest.approx(200) and turn == pytest.approx(90)


def test_voltage_drop_and_bundle() -> None:
    h = routing.HarnessIn(points=[(0, 0, 0), (1000, 0, 0), (1000, 2000, 0)], bend_radius=40,
                          conductors=[routing.Conductor(name="pump", area_mm2=2.5,
                                                        current_a=10)])  # fmt: skip
    out = routing.harness(h)
    assert out["conductors"][0]["drop_v"] == pytest.approx(2 * 10 * 0.0175 * 3.0 / 2.5)
    d = 1.2 * math.sqrt(4 * 2.5 / math.pi) + 0.5
    assert out["bundle_mm"] == pytest.approx(1.15 * d)
    status = {c["id"]: c["status"] for c in out["checks"]}
    assert status["drop"] == "fail"  # 0.42 V is 3.5 % of 12 V, above the 3 % limit
    assert status["bend"] == "pass"  # 40 mm >= 6 x the 3.0 mm bundle
    tight = routing.harness(h.model_copy(update={"bend_radius": 10}))
    assert {c["id"]: c["status"] for c in tight["checks"]}["bend"] == "fail"


def test_pipe_pressure_drop_turbulent() -> None:
    p = routing.PipeIn(points=[(0, 0, 0), (2000, 0, 0)], outer_mm=12, wall_mm=1, flow_lpm=10)
    out = routing.pipe(p)
    d = 0.010
    v = 10 / 60_000 / (math.pi / 4 * d * d)
    re = v * d / 1.0e-6
    f = 0.316 * re**-0.25
    assert out["regime"] == "turbulent"
    assert out["pressure_drop_kpa"] == pytest.approx(f * 2.0 / d * 998 * v * v / 2 / 1000)


def test_pipe_laminar_oil() -> None:
    out = routing.pipe(routing.PipeIn(points=[(0, 0, 0), (1000, 0, 0)], fluid="engine oil",
                                      flow_lpm=2, outer_mm=12, wall_mm=1))  # fmt: skip
    assert out["regime"] == "laminar" and out["friction_factor"] == pytest.approx(
        64 / out["reynolds"]
    )
