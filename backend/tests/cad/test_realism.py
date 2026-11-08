"""Designer controls for realistic sporty bodies: nose rake, bonnet dome, lower trim, and
the open cockpit closed behind the last seat row."""

import pytest

from autevra.assembly.model import BY_ID
from autevra.cad import kernel as k
from autevra.core.parameters import REGISTRY, default_values
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import details as dt
from autevra.domains.automotive import interior, powertrain, spec, styled

pytestmark = pytest.mark.cad

GT = spec.TEMPLATES["roadster"] | {
    "wheelbase": 2930, "front_overhang": 960, "rear_overhang": 1080, "body_width": 1960,
    "overall_height": 1360, "beltline_height": 900, "ground_clearance": 110,
    "track_front": 1680, "track_rear": 1660, "rim_diameter": 21, "tyre_width": 265,
    "tyre_aspect_ratio": 30, "cabin_length": 2350, "cabin_offset": -250, "seat_rows": 2,
    "seat_height": 200, "seat_recline": 26, "grille_style": 3, "head_lamp_style": 4,
    "fender_rise": 140, "nose_taper": 72,
}  # fmt: skip


def _body(extra: dict[str, float] | None = None) -> dict[str, float]:
    return BY_ID["body"].resolve_inputs(default_values() | GT | (extra or {}))


def test_the_trim_options_follow_the_builder_order() -> None:
    assert len(REGISTRY["lower_trim"].options) == len(dt.LOWER_TRIMS)


@pytest.mark.parametrize("style", ["sedan", "sports_car", "roadster", "supercar", "suv"])
def test_nose_rake_sets_the_bonnet_edge_back_and_keeps_the_extents(style: str) -> None:
    v = default_values() | spec.TEMPLATES[style]
    upright = b.body_layout(BY_ID["body"].resolve_inputs(v | {"nose_rake": 0.0}))
    raked = b.body_layout(BY_ID["body"].resolve_inputs(v | {"nose_rake": 50.0}))
    front = v["front_overhang"]
    assert upright.profile[3][0] == pytest.approx(front)  # an upright face
    (_, bumper), (x_nose, nose) = raked.profile[2], raked.profile[3]
    assert x_nose == pytest.approx(front - 0.5 * (nose - bumper))
    assert max(x for x, _ in raked.profile) == pytest.approx(front)  # the bumper line stays


def test_lamps_and_grille_follow_a_raked_nose() -> None:
    p = _body({"nose_rake": 60.0})
    lamps = b.build_lamps(p, "head")
    assert lamps is not None and k.solid_count(lamps) == 2  # one slanted lamp a side
    (x0, _, z0), (x1, _, z1) = k.bounds(lamps)
    layout = b.body_layout(p)
    assert x1 <= p["front_overhang"] and z1 <= layout.profile[3][1]
    grille = dt.build_grille(p)
    assert grille is not None


def test_swept_lamps_rise_towards_the_outer_corner() -> None:
    p = _body()
    from autevra.domains.automotive import styling

    outline = styling.swept_outline(p, b.body_layout(p), 1.0)
    (yi, zi), (yo, zo) = outline[0], outline[1]
    assert yo > yi and zo > zi  # the outer end is higher


def test_bonnet_dome_rises_between_the_creases() -> None:
    p = _body({"bonnet_dome": 0.0})
    g = styled.guides(p, b.body_layout(p))
    x = -250.0  # on the bonnet, just ahead of the windscreen base

    def centre_and_crease(q: dict[str, float]) -> tuple[float, float]:
        loop = styled.section_points(q, g, x)
        half = len(loop) // 2
        return loop[half][1], loop[half - 2][1]  # the centre line, the crease

    flat_centre, flat_crease = centre_and_crease(p)
    crown = max(z for _, z in styled.section_points(p, g, x))
    centre, crease = centre_and_crease(p | {"bonnet_dome": 60.0})
    assert crease == pytest.approx(flat_crease)
    # The dome stands up from the valley floor, above its creases, below the wing crowns.
    assert centre - flat_centre > 40.0
    assert crease < centre < crown


def test_lower_trim_is_a_band_round_the_foot_of_the_body() -> None:
    def inputs(trim: float) -> dict[str, float]:
        return BY_ID["lower_trim"].resolve_inputs(default_values() | GT | {"lower_trim": trim})

    assert dt.build_lower_trim(inputs(0.0)) is None  # body colour
    p = inputs(1.0)
    trim = dt.build_lower_trim(p)
    assert trim is not None
    (x0, y0, z0), (x1, y1, z1) = k.bounds(trim)
    floor = p["body_floor"]
    assert z0 >= floor - dt.TRIM_PROUD - 1.0 and z1 <= floor + 171.0
    assert y1 > p["body_width"] / 2.0 - 200.0  # it reaches the sills
    assert x1 > p["front_overhang"] - 100.0  # and the splitter under the nose
    # A band, not a floor plate: nothing in the middle of the underbody.
    assert k.volume(k.intersect(trim, k.box((-2000.0, -1000.0), (-200.0, 200.0),
                                            (floor - 10.0, floor + 50.0)))) == 0.0  # fmt: skip


def test_an_open_cockpit_ends_behind_the_last_row_ahead_of_the_rear_dampers() -> None:
    p = _body()
    (rear, _), _, _ = interior.cavity(p)
    last_row = min(x for x, _ in interior.seat_positions(p))
    assert rear < last_row - 500.0  # behind the last hinge line
    damper_front = -p["wheelbase"] + 70.0  # the rear damper's forward face, about
    assert rear > damper_front  # the deck covers the rear suspension


def test_cooling_module_sits_under_a_low_raked_nose() -> None:
    v = default_values() | GT | {"nose_rake": 60.0}
    p = BY_ID["body"].resolve_inputs(v)
    rad = powertrain.build_radiator(BY_ID["radiator"].resolve_inputs(v))
    (x0, _, _), (x1, _, z1) = k.bounds(rad)
    g = styled.guides(p, b.body_layout(p))
    assert z1 < g.top(x1)


@pytest.mark.parametrize(("style", "count"), [("roadster", 1), ("sports_car", 1), ("sedan", 2),
                                              ("suv", 2), ("van", 0)])  # fmt: skip
def test_doors_sit_between_the_arches_by_style(style: str, count: int) -> None:
    v = default_values() | spec.TEMPLATES[style] | {"door_lines": 2.0}
    p = BY_ID["body"].resolve_inputs(v)
    doors = dt.doors(p, b.body_layout(p))
    assert len(doors) == count
    for x0, x1 in doors:
        assert -p["wheelbase"] + p["arch_radius"] < x0 < x1 < -p["arch_radius"]


def test_door_lines_cut_shut_lines_and_handles_into_the_body() -> None:
    assert dt.door_tools(_body({"door_lines": 0.0}), b.body_layout(_body())) == []
    p = _body({"door_lines": 2.0})
    layout = b.body_layout(p)
    lines = dt.door_tools(p | {"door_lines": 1.0}, layout)
    with_handles = dt.door_tools(p, layout)
    assert len(lines) == 6  # three edges of one door, both sides
    assert len(with_handles) == 8  # and a handle recess on each side
    body = b.build_body(p)
    plain = b.build_body(p | {"door_lines": 0.0})
    assert 0.0 < k.volume(plain) - k.volume(body) < 0.002 * k.volume(plain)


def test_smoked_housings_frame_the_head_lamps() -> None:
    def inputs(housing: float) -> dict[str, float]:
        v = default_values() | GT | {"lamp_housing": housing}
        return BY_ID["lamp_housings"].resolve_inputs(v)

    assert styled.build_lamp_housings(inputs(0.0)) is None
    p = inputs(1.0)
    eye = styled.build_lamp_housings(p)
    assert eye is not None and k.solid_count(eye) >= 2  # one each side
    lamps = b.build_lamps(p, "head")
    assert k.volume(k.intersect(eye, lamps)) < 1.0  # round the lens, not over it
    (_, _, z0), (_, _, z1) = k.bounds(eye)
    (_, _, lz0), (_, _, lz1) = k.bounds(lamps)
    assert z0 < lz0 - 40.0  # the dark eye opens below the lamp line
