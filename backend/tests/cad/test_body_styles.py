"""Body styles: each one builds a valid single solid with the design's extents, and the
styles differ where they should (checked on the layout, without CAD, and on the solid)."""

import pytest

from autevra.cad import kernel as k
from autevra.core.parameters import REGISTRY, default_values
from autevra.domains.automotive import builders as c
from autevra.domains.automotive import derived as d
from autevra.domains.automotive.spec import TEMPLATES

STYLE = {name: i for i, name in enumerate(c.BODY_STYLES)}


def _inputs(style: str, **changes: float) -> dict[str, float]:
    p = default_values() | changes | {"body_style": STYLE[style]}
    return p | {
        "body_floor": d.body_floor_height(p),
        "tyre_radius": d.tyre_radius(p),
        "arch_radius": d.arch_radius(p),
    }


def test_the_parameter_offers_every_style_in_builder_order() -> None:
    spec = REGISTRY["body_style"]
    assert [o.lower().replace(" ", "_") for o in spec.options] == list(c.BODY_STYLES)
    assert (spec.min, spec.max, spec.step) == (0, len(c.BODY_STYLES) - 1, 1)


def test_two_box_styles_carry_the_roof_further_back_than_a_sedan() -> None:
    sedan, hatch, suv = (c.body_layout(_inputs(s)) for s in ("sedan", "hatchback", "suv"))
    assert hatch.roof[0] < sedan.roof[0] and suv.roof[0] < hatch.roof[0]
    assert hatch.glass[0] < sedan.glass[0]


def test_a_coupe_rear_screen_runs_further_back_than_a_sedan_one() -> None:
    sedan, coupe = c.body_layout(_inputs("sedan")), c.body_layout(_inputs("coupe"))
    assert coupe.roof[0] - coupe.glass[0] > 1.5 * (sedan.roof[0] - sedan.glass[0])


def test_only_the_pickup_has_an_open_bed_behind_the_cab() -> None:
    layouts = {s: c.body_layout(_inputs(s)) for s in c.BODY_STYLES}
    assert [s for s, lay in layouts.items() if lay.bed] == ["pickup"]
    (bed_rear, bed_front), _ = layouts["pickup"].bed
    assert bed_front < layouts["pickup"].glass[0]  # the bed ends before the cab begins


def test_a_box_truck_cargo_box_stands_above_its_cab() -> None:
    truck = c.body_layout(_inputs("box_truck"))
    assert truck.cargo is not None and truck.roof_z < default_values()["overall_height"]
    assert truck.cargo[1] < truck.glass[0]


def test_a_van_greenhouse_spans_almost_the_whole_body() -> None:
    p = _inputs("van")
    van = c.body_layout(p)
    length = p["wheelbase"] + p["front_overhang"] + p["rear_overhang"]
    assert van.glass[1] - van.glass[0] > 0.75 * length


@pytest.mark.cad
@pytest.mark.parametrize("style", c.BODY_STYLES)
def test_every_style_builds_one_valid_solid_with_the_design_extents(style: str) -> None:
    p = _inputs(style)
    body = c.build_body(p)
    assert k.is_valid(body) and k.solid_count(body) == 1
    (x0, y0, _), (x1, y1, z1) = k.bounds(body)
    assert x0 == pytest.approx(-(p["wheelbase"] + p["rear_overhang"]), abs=1)
    assert x1 == pytest.approx(p["front_overhang"], abs=1)
    assert (y0, y1) == (pytest.approx(-p["body_width"] / 2), pytest.approx(p["body_width"] / 2))
    assert z1 == pytest.approx(p["overall_height"], abs=1)


@pytest.mark.cad
def test_the_pickup_bed_removes_material_and_the_truck_box_adds_it() -> None:
    sedan = k.volume(c.build_body(_inputs("sedan")))
    assert k.volume(c.build_body(_inputs("box_truck"))) > 1.2 * sedan
    van = k.volume(c.build_body(_inputs("van")))
    assert k.volume(c.build_body(_inputs("pickup"))) < van


@pytest.mark.cad
@pytest.mark.parametrize("template", sorted(TEMPLATES))
@pytest.mark.parametrize("style", ["sedan", "hatchback", "suv", "pickup", "van", "box_truck"])
def test_every_template_builds_in_every_style(template: str, style: str) -> None:
    values = {k_: v for k_, v in TEMPLATES[template].items() if k_ in REGISTRY}
    body = c.build_body(_inputs(style, **values))
    assert k.is_valid(body) and k.solid_count(body) == 1


@pytest.mark.cad
@pytest.mark.parametrize("style", c.BODY_STYLES)
def test_glazing_sits_inside_the_window_openings(style: str) -> None:
    p = _inputs(style)
    glass, body = c.build_glass(p), c.build_body(p)
    assert k.is_valid(glass) and k.solid_count(glass) == 1
    (gx0, gy0, gz0), (gx1, gy1, gz1) = k.bounds(glass)
    (bx0, by0, _), (bx1, by1, bz1) = k.bounds(body)
    assert bx0 < gx0 and gx1 < bx1 and by0 < gy0 and gy1 < by1 and gz1 < bz1
    assert gz0 == pytest.approx(p["beltline_height"])


def test_glazing_ignores_the_wheels_and_track() -> None:
    from autevra.domains.automotive.vehicle import GLASS_GEOMETRY

    assert "track_front" not in GLASS_GEOMETRY and "rim_diameter" not in GLASS_GEOMETRY
    assert "body_style" in GLASS_GEOMETRY and "cabin_length" in GLASS_GEOMETRY
