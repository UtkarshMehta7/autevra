"""Component builders produce valid single solids whose size follows the parameters."""

import pytest

from autevra.cad import components as c
from autevra.cad import kernel as k
from autevra.core import derived as d
from autevra.core.parameters import default_values

pytestmark = pytest.mark.cad


def _body_inputs(**changes: float) -> dict[str, float]:
    p = default_values() | changes
    return p | {
        "body_floor": d.body_floor_height(p),
        "tyre_radius": d.tyre_radius(p),
        "arch_radius": d.arch_radius(p),
    }


def _approx_bounds(shape: k.Shape) -> tuple[tuple[float, ...], tuple[float, ...]]:
    lo, hi = k.bounds(shape)
    return tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi)


def test_body_spans_overhangs_wheelbase_width_and_height() -> None:
    body = c.build_body(_body_inputs())
    assert k.is_valid(body) and k.solid_count(body) == 1
    assert _approx_bounds(body) == ((-3700, -910, 270), (900, 910, 1450))


def test_body_lengthens_with_wheelbase() -> None:
    short = c.build_body(_body_inputs())
    long = c.build_body(_body_inputs(wheelbase=2800))
    assert k.bounds(long)[0][0] == pytest.approx(k.bounds(short)[0][0] - 100)
    assert k.bounds(long)[1][0] == pytest.approx(k.bounds(short)[1][0])
    assert k.volume(long) > k.volume(short)


def test_wheel_wells_are_cut_from_the_body() -> None:
    p = _body_inputs()
    with_wells = k.volume(c.build_body(p))
    without = k.volume(c.build_body(p | {"arch_radius": 1.0, "tyre_radius": -10.0}))
    assert with_wells < without


def test_frame_rails_are_hollow_rectangular_sections() -> None:
    p = default_values()
    frame = c.build_frame(p)
    assert k.is_valid(frame) and k.solid_count(frame) == 1
    lo, hi = k.bounds(frame)
    assert (lo[1], hi[1]) == pytest.approx((-485, 485))  # rail spacing 900 + rail width 70
    assert (lo[2], hi[2]) == pytest.approx((160, 270))  # ground clearance + rail height
    # One rail: hollow section area 70*110 - 62*102 = 1376 mm^2.
    rail_length = hi[0] - lo[0]
    assert k.volume(frame) > 2 * 1376 * rail_length
    assert k.volume(frame) < 2 * 70 * 110 * rail_length  # far less than solid rails


def test_axle_spans_track_minus_hub_inset() -> None:
    axle = c.build_axle({"track": 1560})
    lo, hi = k.bounds(axle)
    assert (lo[1], hi[1]) == pytest.approx((-720, 720))


def test_wheel_matches_tyre_size() -> None:
    p = default_values()
    wheel = c.build_wheel(
        {
            "tyre_radius": d.tyre_radius(p),
            "rim_radius": d.rim_diameter_mm(p) / 2,
            "tyre_width": p["tyre_width"],
        }
    )
    assert k.is_valid(wheel) and k.solid_count(wheel) == 1
    lo, hi = k.bounds(wheel)
    assert hi[0] - lo[0] == pytest.approx(d.tyre_diameter(p), abs=0.01)  # 656.8 mm
    assert hi[2] - lo[2] == pytest.approx(d.tyre_diameter(p), abs=0.01)
    assert hi[1] - lo[1] == pytest.approx(p["tyre_width"], abs=0.01)


def test_step_export_contains_named_parts(tmp_path) -> None:
    wheel = c.build_axle({"track": 1560})
    identity = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 300], [0, 0, 0, 1]]
    path = k.export_step(
        [k.Part("front_axle", wheel, identity, (0.3, 0.3, 0.3))], tmp_path / "a.step"
    )
    text = path.read_text()
    assert "front_axle" in text
    reimported = k.import_step(path)
    assert k.bounds(reimported)[0][2] == pytest.approx(265)


def _damper_inputs(**changes: float) -> dict[str, float]:
    from autevra.assembly.vehicle import BY_ID

    return BY_ID["damper_fl"].resolve_inputs(default_values() | changes)


def test_damper_is_a_valid_solid_between_its_eyes() -> None:
    inputs = _damper_inputs()
    damper = c.build_damper(inputs)
    assert k.is_valid(damper) and k.solid_count(damper) == 1
    (_, _, z0), (_, _, z1) = k.bounds(damper)
    assert z0 == pytest.approx(-c.EYE_OUTER, abs=0.01)
    assert z1 == pytest.approx(inputs["length"] + c.EYE_OUTER, abs=0.01)


def test_spring_rate_changes_the_coil_but_damping_does_not() -> None:
    base = _damper_inputs()
    assert _damper_inputs(front_damping_bump=4000) == base  # dynamics only
    stiffer = _damper_inputs(front_spring_rate=40)
    assert stiffer["wire_diameter"] > base["wire_diameter"]
    assert k.volume(c.build_damper(stiffer)) > k.volume(c.build_damper(base))


def test_overlapping_coils_are_rejected() -> None:
    with pytest.raises(k.KernelError):
        k.helical_coil(50, 60, 8, 10, 0)


def test_body_builds_for_random_valid_designs() -> None:
    """Robustness: the body is a valid single solid across the valid design space."""
    import random

    from autevra.assembly.vehicle import BY_ID
    from autevra.core.parameters import REGISTRY
    from autevra.core.rules import validate

    rng, built = random.Random(7), 0
    geometry = BY_ID["body"].geometry
    while built < 25:
        v = default_values()
        for pid in geometry:
            spec = REGISTRY[pid]
            v[pid] = round(rng.uniform(spec.min, spec.max) / spec.step) * spec.step
        if validate(v):
            continue
        body = c.build_body(BY_ID["body"].resolve_inputs(v))
        assert k.is_valid(body) and k.solid_count(body) == 1
        built += 1


def test_body_profile_keeps_the_hood_above_the_front_arch() -> None:
    from autevra.assembly.vehicle import BY_ID

    inputs = BY_ID["body"].resolve_inputs(default_values() | {"rim_diameter": 22})
    profile = c.body_profile(inputs)
    nose = profile[3][1]
    assert (
        nose >= inputs["tyre_radius"] + inputs["arch_radius"] + 40 - 1e-6
        or nose == inputs["beltline_height"] - 20
    )
