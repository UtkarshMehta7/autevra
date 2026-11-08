import math

import pytest
from fastapi.testclient import TestClient

from autevra.cad import kernel as k
from autevra.part import features as f
from autevra.part import sketch as sk
from autevra.part.build import build_part


def rectangle(w: float = 100.0, h: float = 60.0, skew: float = 7.0) -> dict:
    """A roughly drawn rectangle (corners off by ``skew``) with an anchored corner."""
    return {
        "points": [
            {"id": "p0", "x": 0, "y": 0, "fixed": True},
            {"id": "p1", "x": w + skew, "y": skew},
            {"id": "p2", "x": w - skew, "y": h + skew},
            {"id": "p3", "x": -skew, "y": h - skew},
        ],
        "entities": [
            {"type": "line", "id": "l0", "a": "p0", "b": "p1"},
            {"type": "line", "id": "l1", "a": "p1", "b": "p2"},
            {"type": "line", "id": "l2", "a": "p2", "b": "p3"},
            {"type": "line", "id": "l3", "a": "p3", "b": "p0"},
        ],
        "constraints": [
            {"kind": "horizontal", "refs": ["l0"]},
            {"kind": "vertical", "refs": ["l1"]},
            {"kind": "horizontal", "refs": ["l2"]},
            {"kind": "vertical", "refs": ["l3"]},
            {"kind": "length", "refs": ["l0"], "value": w},
            {"kind": "length", "refs": ["l1"], "value": h},
        ],
    }


def at(result: sk.SolveResult, pid: str) -> tuple[float, float]:
    p = next(p for p in result.sketch.points if p.id == pid)
    return p.x, p.y


def test_a_dimensioned_rectangle_is_fully_constrained() -> None:
    out = sk.solve(sk.Sketch.model_validate(rectangle()))
    assert out.ok and out.dof == 0 and out.redundant == 0
    assert at(out, "p2") == pytest.approx((100.0, 60.0), abs=1e-6)
    assert set(out.fixed_points) == {"p0", "p1", "p2", "p3"}
    assert set(out.fixed_entities) == {"l0", "l1", "l2", "l3"}


def test_dropping_a_dimension_leaves_one_degree_of_freedom() -> None:
    data = rectangle()
    data["constraints"].pop()  # no height
    out = sk.solve(sk.Sketch.model_validate(data))
    assert out.ok and out.dof == 1
    assert "p0" in out.fixed_points and "p1" in out.fixed_points  # the width still pins these
    assert "p2" not in out.fixed_points
    # the smallest move keeps the drawn height (about 60 + skew), not a collapsed one
    assert 55.0 < at(out, "p2")[1] < 75.0


def test_conflicts_are_reported_by_constraint() -> None:
    data = rectangle()
    data["constraints"].append({"kind": "length", "refs": ["l2"], "value": 80.0})
    out = sk.solve(sk.Sketch.model_validate(data))
    assert not out.ok and out.conflicting  # opposite sides of a rectangle cannot differ


def test_a_consistent_extra_constraint_is_redundant_not_a_conflict() -> None:
    data = rectangle()
    data["constraints"].append({"kind": "parallel", "refs": ["l0", "l2"]})
    out = sk.solve(sk.Sketch.model_validate(data))
    assert out.ok and out.dof == 0 and out.redundant == 1


def test_circles_arcs_tangency_and_angles() -> None:
    data = {
        "points": [
            {"id": "o", "x": 0, "y": 0, "fixed": True},
            {"id": "a", "x": -50, "y": 40},
            {"id": "b", "x": 50, "y": 33},
            {"id": "c", "x": 10, "y": 5},
        ],
        "entities": [
            {"type": "line", "id": "top", "a": "a", "b": "b"},
            {"type": "circle", "id": "c1", "center": "o", "radius": 22},
            {"type": "line", "id": "slant", "a": "o", "b": "c"},
        ],
        "constraints": [
            {"kind": "horizontal", "refs": ["top"]},
            {"kind": "tangent", "refs": ["top", "c1"]},
            {"kind": "diameter", "refs": ["c1"], "value": 60},
            {"kind": "angle", "refs": ["top", "slant"], "value": 30},
            {"kind": "length", "refs": ["slant"], "value": 40},
        ],
    }
    out = sk.solve(sk.Sketch.model_validate(data))
    assert out.ok
    assert at(out, "a")[1] == pytest.approx(30.0, abs=1e-5)  # tangent to r = 30, above
    cx, cy = at(out, "c")
    assert math.degrees(math.atan2(cy, cx)) == pytest.approx(30.0, abs=1e-4)
    assert math.hypot(cx, cy) == pytest.approx(40.0, abs=1e-5)


def test_dragging_moves_the_point_where_the_constraints_allow() -> None:
    data = rectangle()
    data["constraints"].pop()  # height free
    out = sk.solve(sk.Sketch.model_validate(data), drag=("p2", 130.0, 90.0))
    assert out.ok
    assert at(out, "p2") == pytest.approx((100.0, 90.0), abs=0.01)  # width held, height follows
    assert at(out, "p3") == pytest.approx((0.0, 90.0), abs=0.01)


def test_validation_rejects_bad_references() -> None:
    data = rectangle()
    data["constraints"].append({"kind": "radius", "refs": ["l0"], "value": 5})
    with pytest.raises(ValueError, match="circle or arc"):
        sk.Sketch.model_validate(data)
    data["constraints"][-1] = {"kind": "equal", "refs": ["l0", "c9"]}
    with pytest.raises(ValueError):
        sk.Sketch.model_validate(data)


def plate_with_hole() -> dict:
    data = rectangle()
    data["points"].append({"id": "hc", "x": 48, "y": 33})
    data["entities"].append({"type": "circle", "id": "hole", "center": "hc", "radius": 10})
    data["constraints"] += [
        {"kind": "hdistance", "refs": ["p0", "hc"], "value": 50},
        {"kind": "vdistance", "refs": ["p0", "hc"], "value": 30},
        {"kind": "radius", "refs": ["hole"], "value": 12},
    ]
    return data


def test_profiles_nest_holes_in_their_outline() -> None:
    solved = sk.solve(sk.Sketch.model_validate(plate_with_hole())).sketch
    faces = sk.regions(solved)
    assert len(faces) == 1 and len(faces[0][1]) == 1


def test_an_open_profile_is_reported() -> None:
    data = rectangle()
    data["entities"].pop()
    data["constraints"].pop(3)  # the vertical on the removed side
    with pytest.raises(ValueError, match="open"):
        sk.loops(sk.Sketch.model_validate(data))


@pytest.mark.cad
def test_pad_and_pocket_from_sketches_with_bound_dimensions() -> None:
    doc = f.PartDoc.model_validate({
        "parameters": {"w": 120},
        "features": [
            {"id": "pad", "type": "pad", "sketch": plate_with_hole(), "depth": 10,
             "bindings": {"sketch.constraints.4.value": "w"}},
        ],
    })  # fmt: skip
    result = build_part(doc)
    assert not result.errors
    (x0, y0, z0), (x1, y1, z1) = k.bounds(result.shape)
    assert (x1 - x0, y1 - y0, z1 - z0) == pytest.approx((120, 60, 10), abs=1e-3)
    expected = 120 * 60 * 10 - math.pi * 12**2 * 10
    assert k.volume(result.shape) == pytest.approx(expected, rel=1e-4)


@pytest.mark.cad
def test_shaft_revolves_an_arc_profile() -> None:
    data = {
        "points": [
            {"id": "a", "x": 0, "y": 0, "fixed": True},
            {"id": "b", "x": 20, "y": 0},
            {"id": "c", "x": 20, "y": 40},
            {"id": "d", "x": 0, "y": 40},
            {"id": "m", "x": 0, "y": 20, "fixed": True},
        ],
        "entities": [
            {"type": "line", "id": "base", "a": "a", "b": "b"},
            {"type": "arc", "id": "bulge", "center": "m", "start": "b", "end": "c"},
            {"type": "line", "id": "lid", "a": "c", "b": "d"},
            {"type": "line", "id": "axis", "a": "d", "b": "a"},
        ],
        "constraints": [
            {"kind": "horizontal", "refs": ["base"]},
            {"kind": "horizontal", "refs": ["lid"]},
            {"kind": "vertical", "refs": ["axis"]},
            {"kind": "length", "refs": ["base"], "value": 20},
        ],
    }
    out = sk.solve(sk.Sketch.model_validate(data))
    assert out.ok
    doc = f.PartDoc.model_validate({"features": [
        {"id": "s", "type": "shaft", "sketch": data, "plane": "xz"}]})  # fmt: skip
    result = build_part(doc)
    assert not result.errors, result.errors
    # a sphere-like solid of revolution, about the Z axis
    (x0, y0, _), (x1, y1, _) = k.bounds(result.shape)
    assert x1 - x0 == pytest.approx(y1 - y0, abs=1e-3)


def test_sketch_solve_api(client: TestClient) -> None:
    out = client.post("/api/sketch/solve", json={"sketch": rectangle()})
    assert out.status_code == 200
    body = out.json()
    assert body["ok"] and body["dof"] == 0
    drag = client.post("/api/sketch/solve", json={
        "sketch": rectangle(), "drag": {"point": "p2", "x": 140, "y": 99}})  # fmt: skip
    assert drag.json()["ok"]  # fully constrained: the point snaps back
    bad = client.post("/api/sketch/solve", json={"sketch": {"points": [], "entities": [
        {"type": "line", "id": "l", "a": "x", "b": "y"}]}})  # fmt: skip
    assert bad.status_code == 422


def test_a_solve_reports_its_equations_rank_and_convergence() -> None:
    # A rectangle-ish quad with horizontal, vertical and length constraints, one point fixed.
    out = sk.solve(sk.Sketch.model_validate(rectangle()))
    assert out.ok and out.converged
    assert out.unknowns == 6  # three free points, x and y each
    rows = sum(e.rows for e in out.equations)
    assert out.dof == out.unknowns - out.rank
    assert out.redundant == rows - out.rank
    assert all(e.residual < 1e-4 for e in out.equations)
    assert any("y(" in e.text for e in out.equations if e.kind == "horizontal")
    assert out.iterations and out.iterations[-1].accepted
    costs = [it.cost for it in out.iterations if it.accepted]
    assert costs == sorted(costs, reverse=True)  # accepted steps only ever lower |F|^2
