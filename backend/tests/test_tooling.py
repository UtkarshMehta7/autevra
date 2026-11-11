"""Draft analysis: a straight box has vertical walls; a tapered block is drafted."""

import cadquery as cq
import pytest

from autevra import tooling


@pytest.mark.cad
def test_box_walls_have_no_draft() -> None:
    r = tooling.draft(cq.Workplane().box(20, 20, 10).val(), (0, 0, 1), 1.0)
    assert r.area_mm2["insufficient"] == pytest.approx(4 * 20 * 10)
    assert r.area_mm2["perpendicular"] == pytest.approx(2 * 20 * 20)
    assert not r.ok
    sides = {f.side for f in r.faces if f.status == "perpendicular"}
    assert sides == {"cavity", "core"}  # top released up, bottom down


@pytest.mark.cad
def test_tapered_block_is_drafted() -> None:
    # a 3 degree taper on every wall: a loft from a 20 mm square to a smaller one 10 mm up
    top = 20 - 2 * 10 * 0.0524  # tan(3 deg) ~ 0.0524
    solid = cq.Workplane().rect(20, 20).workplane(offset=10).rect(top, top).loft().val()
    r = tooling.draft(solid, (0, 0, 1), 1.0)
    walls = [f for f in r.faces if f.status != "perpendicular"]
    assert all(f.min_draft_deg == pytest.approx(3.0, abs=0.05) for f in walls)
    assert r.ok
    strict = tooling.draft(solid, (0, 0, 1), 5.0)
    assert not strict.ok
