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


def _double_taper() -> cq.Shape:
    # 40 x 20 at the mid-plane, tapering to 36 x 16 at z = +10 and z = -10
    up = cq.Workplane().rect(40, 20).workplane(offset=10).rect(36, 16).loft()
    down = cq.Workplane().rect(40, 20).workplane(offset=-10).rect(36, 16).loft()
    return up.union(down).val()


@pytest.mark.cad
def test_parting_line_of_a_double_tapered_block() -> None:
    r = tooling.parting(_double_taper(), (0, 0, 1), cavity_pressure_mpa=40.0)
    assert (r.cavity_faces, r.core_faces, r.wall_faces) == (5, 5, 0)
    assert r.parting_edges == 4 and r.parting_length_mm == pytest.approx(2 * (40 + 20))
    assert r.flat and r.parting_height_mm == pytest.approx((0.0, 0.0), abs=1e-6)
    # the flux of the pull through the cavity half is the mid-plane area
    assert r.projected_area_mm2 == pytest.approx(40 * 20, rel=1e-4)
    assert r.clamp_kn == pytest.approx(32.0, rel=1e-4)
    assert not r.undercuts and r.verdict.startswith("opens straight in a two-plate")


@pytest.mark.cad
def test_side_slot_is_an_undercut_only_across_the_pull() -> None:
    slot = cq.Workplane().box(10, 40, 6).translate((15, 0, 0))  # open on the +x side
    part = _double_taper().cut(slot.val())
    r = tooling.parting(part, (0, 0, 1))
    assert len(r.undercuts) == 2 and {u.side for u in r.undercuts} == {"cavity", "core"}
    assert "undercut" in r.verdict
    # pulled along x the slot opens with the tool: nothing is trapped
    assert not tooling.parting(part, (1, 0, 0)).undercuts


@pytest.mark.cad
def test_box_has_walls_and_no_parting_edges() -> None:
    r = tooling.parting(cq.Workplane().box(20, 20, 10).val())
    assert (r.cavity_faces, r.core_faces, r.wall_faces) == (1, 1, 4)
    assert r.parting_edges == 0 and "need draft" in r.verdict
    assert r.projected_area_mm2 == pytest.approx(400)
