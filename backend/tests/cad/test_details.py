import pytest

from autevra.ai.rule_parser import Kind, parse
from autevra.assembly.model import BY_ID
from autevra.cad import kernel as k
from autevra.core.parameters import REGISTRY, default_values
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import details as dt
from autevra.domains.automotive import spec, styled, styling, vehicle

pytestmark = pytest.mark.cad

# An open 2+2 grand tourer with every new detail (the studio's "Open GT 2+2").
GT = spec.TEMPLATES["roadster"] | {
    "wheelbase": 2930, "front_overhang": 960, "rear_overhang": 1080, "body_width": 1960,
    "overall_height": 1360, "beltline_height": 900, "ground_clearance": 120,
    "track_front": 1680, "track_rear": 1660, "rim_diameter": 20, "tyre_width": 265,
    "cabin_length": 2350, "cabin_offset": -250, "seat_rows": 2, "seat_height": 200,
    "seat_recline": 26, "grille_style": 3, "side_vents": 1, "caliper_colour": 3,
    "paint_colour": 12,
}  # fmt: skip


def _flat(shape: k.Shape) -> list[float]:
    return [c for corner in k.bounds(shape) for c in corner]


def test_the_parameters_offer_every_detail_in_builder_order() -> None:
    assert len(REGISTRY["grille_style"].options) == len(dt.GRILLE_STYLES)
    assert len(REGISTRY["side_vents"].options) == len(dt.SIDE_VENTS)
    assert len(REGISTRY["caliper_colour"].options) == len(vehicle.CALIPERS)
    assert len(REGISTRY["paint_colour"].options) == len(vehicle.PAINT)


@pytest.mark.parametrize("template", ["sedan", "suv", "roadster", "supercar", "van"])
@pytest.mark.parametrize("style", range(len(dt.GRILLE_STYLES)))
def test_grilles_sit_in_their_recess(template: str, style: int) -> None:
    v = default_values() | spec.TEMPLATES[template] | {"grille_style": float(style)}
    inputs = BY_ID["body"].resolve_inputs(v) | {"surface_quality": 1.0}  # the draft surface
    body = b.build_body(inputs)
    assert k.is_valid(body) and k.solid_count(body) == 1
    grille = dt.build_grille(BY_ID["grille"].resolve_inputs(v))
    if style == 0:
        assert grille is None
        return
    assert grille is not None and k.is_valid(grille)
    assert _flat(k.fuse(body, grille)) == pytest.approx(_flat(body), abs=0.01)  # flush
    assert k.volume(k.intersect(body, grille)) == pytest.approx(0, abs=1)


def test_the_gt_builds_one_styled_body_with_every_recess() -> None:
    v = default_values() | GT
    body = styled.try_body(BY_ID["body"].resolve_inputs(v))
    assert body is not None and k.solid_count(body) == 1
    plain = styled.try_body(
        BY_ID["body"].resolve_inputs(v | {"grille_style": 0.0, "side_vents": 0.0})
    )
    assert plain is not None and k.volume(body) < k.volume(plain)  # the recesses are cut
    for cid, fn in (("grille", dt.build_grille), ("side_vents", dt.build_side_vents)):
        part = fn(BY_ID[cid].resolve_inputs(v))
        assert part is not None
        assert k.volume(k.intersect(body, part)) == pytest.approx(0, abs=1), cid


@pytest.mark.parametrize("vents", [1, 2])
def test_vents_are_cut_into_both_front_wings(vents: int) -> None:
    v = default_values() | spec.TEMPLATES["sedan"] | {"side_vents": float(vents)}
    inserts = dt.build_side_vents(BY_ID["side_vents"].resolve_inputs(v))
    assert inserts is not None
    assert k.solid_count(inserts) == (6 if vents == 1 else 2)
    (x0, y0, _), (x1, y1, _) = k.bounds(inserts)
    assert x1 < 0 and y0 < 0 < y1  # behind the front axle, on both sides
    body = b.build_body(BY_ID["body"].resolve_inputs(v) | {"surface_quality": 1.0})
    assert k.volume(k.intersect(body, inserts)) == pytest.approx(0, abs=1)


@pytest.mark.parametrize("rim", [14, 17, 21])
def test_brakes_sit_inside_the_wheel_without_touching_it(rim: int) -> None:
    v = default_values() | {"rim_diameter": float(rim), "wheel_design": 1.0}
    disc = dt.build_brake_disc(BY_ID["rotor_fl"].resolve_inputs(v))
    caliper = dt.build_brake_caliper(BY_ID["caliper_fl"].resolve_inputs(v))
    for part in (disc, caliper):
        assert k.is_valid(part) and k.solid_count(part) == 1
    rim_shape = styling.build_rim(BY_ID["rim_fl"].resolve_inputs(v))
    tyre = b.build_wheel(BY_ID["wheel_fl"].resolve_inputs(v))
    for part in (disc, caliper):
        for other in (rim_shape, tyre):
            assert k.volume(k.intersect(part, other)) == pytest.approx(0, abs=1)
    assert k.volume(k.intersect(disc, caliper)) == pytest.approx(0, abs=1)  # it straddles


def test_caliper_colour_changes_appearance_without_a_rebuild() -> None:
    v = default_values()
    caliper = BY_ID["caliper_fl"]
    assert "caliper_colour" not in caliper.geometry
    colours = {caliper.resolve_appearance(v | {"caliper_colour": float(i)}) for i in range(6)}
    assert len(colours) == 6


def test_an_open_car_keeps_only_thin_a_pillars() -> None:
    v = default_values() | GT
    inputs = BY_ID["glass"].resolve_inputs(v)
    layout = b.body_layout(inputs)
    frame = b._window_frame(inputs, layout)
    (_, g1), (_, r1) = layout.glass, layout.roof
    belt, top = inputs["beltline_height"], layout.roof_z
    # Halfway up, more than two pillar widths behind the raked screen: nothing there.
    zm = (belt + top) / 2.0
    screen = g1 - (g1 - r1) * (zm + 30.0 - belt) / (top - belt)  # at the top of the probe
    behind = k.box((r1, screen - 2 * b.PILLAR * 1.5), (-2000.0, 2000.0), (zm - 30.0, zm + 30.0))
    assert k.volume(k.intersect(frame, behind)) == pytest.approx(0, abs=1)
    assert k.solid_count(frame) >= 1  # the screen surround itself is kept


@pytest.mark.parametrize(
    ("text", "parameter", "option"),
    [
        ("fit a sport grille", "grille_style", "Sport mesh"),
        ("give it a mesh grille", "grille_style", "Mesh"),
        ("fit gills", "side_vents", "Three gills"),
        ("make the brake calipers yellow", "caliper_colour", "Yellow"),
        ("paint it sage green", "paint_colour", "Sage Green"),
    ],
)
def test_detail_phrases_set_the_choice(text: str, parameter: str, option: str) -> None:
    result = parse(text)
    assert result.kind is Kind.COMMAND, (text, result.question)
    assert result.command is not None
    (change,) = result.command.changes
    assert change.parameter == parameter
    assert REGISTRY[parameter].options[int(change.value)] == option


def test_plain_green_still_means_the_paint() -> None:
    result = parse("make it green")
    assert result.command is not None
    (change,) = result.command.changes
    assert change.parameter == "paint_colour"
    assert REGISTRY["paint_colour"].options[int(change.value)] == "Forest Green"


@pytest.mark.parametrize(
    ("mode", "limit", "allowed"),
    [("on", 512 << 20, True), ("off", None, False), ("auto", None, True),
     ("auto", 512 << 20, False), ("auto", 4 << 30, True)],
)  # fmt: skip
def test_low_memory_hosts_use_the_draft_surface(
    monkeypatch: pytest.MonkeyPatch, mode: str, limit: int | None, allowed: bool
) -> None:
    monkeypatch.setenv("AUTEVRA_STYLED_SURFACE", mode)
    monkeypatch.setattr(styled, "_memory_limit", lambda: limit)
    styled.styled_allowed.cache_clear()
    try:
        assert styled.styled_allowed() is allowed
        assert styled.surface({"surface_quality": 0.0}) == ("styled" if allowed else "draft")
    finally:
        styled.styled_allowed.cache_clear()


def test_raised_wings_stand_above_the_bonnet_over_the_wheels() -> None:
    v = default_values() | GT | {"fender_rise": 140.0}
    inputs = BY_ID["body"].resolve_inputs(v)
    g = styled.guides(inputs, b.body_layout(inputs))

    def crown_and_centre(p: dict[str, float], x: float) -> tuple[float, float]:
        loop = styled.section_points(p, g, x)
        return max(z for _, z in loop), loop[len(loop) // 2][1]  # the top point is mid-loop

    crown, centre = crown_and_centre(inputs, 0.0)  # over the front wheel
    assert crown - centre > 60.0  # the bonnet sits well below the wing crowns
    flat_crown, flat_centre = crown_and_centre(inputs | {"fender_rise": 0.0}, 0.0)
    assert flat_crown == pytest.approx(flat_centre, abs=5.0)  # no rise: a plain bonnet
    assert crown > flat_crown  # the wing swells up over the wheel
