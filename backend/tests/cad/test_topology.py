"""Topology inspection against shapes whose topology is known exactly."""

import cadquery as cq
import pytest

from autevra.cad import kernel as k
from autevra.cad import topology as t

pytestmark = pytest.mark.cad


def test_a_box_has_8_vertices_12_edges_6_faces_and_no_holes() -> None:
    top = t.topology(k.box((0, 10), (0, 20), (0, 30)))
    assert (top.vertices, top.edges, top.faces, top.loops) == (8, 12, 6, 6)
    assert (top.shells, top.solids, top.rings) == (1, 1, 0)
    assert top.euler == 2 and top.genus == 0 and top.balanced
    assert top.watertight and top.valid and top.free_edges == 0
    assert top.surfaces == {"plane": 6} and top.curves == {"line": 12}
    assert top.volume == pytest.approx(6000.0)
    assert top.area == pytest.approx(2 * (200 + 300 + 600))


def test_a_box_with_a_through_hole_has_genus_one() -> None:
    body = k.cut(k.box((0, 40), (0, 40), (0, 10)), k.cylinder_z(5, (-1, 11), x=20, y=20))
    top = t.topology(body)
    assert top.genus == 1 and top.balanced
    assert top.rings == 2  # the hole's circle in the top and the bottom face
    assert top.surfaces["cylinder"] == 1 and top.seam_edges == 1
    assert top.watertight


def test_a_blind_hole_keeps_genus_zero() -> None:
    body = k.cut(k.box((0, 40), (0, 40), (0, 10)), k.cylinder_z(5, (5, 11), x=20, y=20))
    top = t.topology(body)
    assert top.genus == 0 and top.balanced and top.rings == 1


def test_sphere_and_torus_balance_with_seams_and_poles() -> None:
    sphere = t.topology(cq.Solid.makeSphere(10, angleDegrees1=-90))  # the default is a dome
    assert sphere.degenerate_edges == 2 and sphere.genus == 0 and sphere.balanced
    torus = t.topology(cq.Solid.makeTorus(20, 5))
    assert torus.genus == 1 and torus.balanced and torus.watertight


def test_a_single_face_is_open() -> None:
    face = cq.Face.makePlane(10, 10)
    top = t.topology(face)
    assert top.free_edges == 4 and not top.watertight and top.solids == 0


def test_two_solids_sharing_an_edge_are_non_manifold() -> None:
    a = k.box((0, 10), (0, 10), (0, 10))
    b = k.box((10, 20), (10, 20), (0, 10))  # touching along the edge x = y = 10
    top = t.topology(a.fuse(b))
    assert top.nonmanifold_edges >= 1 and not top.watertight


def test_a_section_follows_the_boolean_contact_curve() -> None:
    body = k.box((0, 40), (0, 40), (0, 10))
    tool = k.cylinder_z(5, (-1, 11), x=20, y=20)
    sec = t.section(body, tool)
    # The cylinder crosses the top and the bottom face along a circle of radius 5.
    assert sec.curves >= 2
    assert sec.length == pytest.approx(2 * 2 * 3.141592653589793 * 5, rel=1e-3)
    assert all(len(line) >= 2 for line in sec.polylines)
