"""Rough sketch to 3D: stroke fitting, intent inference, the three ways to make a solid,
and a recognition benchmark on jittered strokes (a regression guard)."""

import math
import random

import pytest
from fastapi.testclient import TestClient

from autevra.part import freehand as fh
from autevra.part.build import build_part
from autevra.part.features import PartDoc

pytestmark = pytest.mark.cad


def wob(pts, a, seed=3):  # noqa: ANN001, ANN201
    rnd = random.Random(seed)
    return [(x + rnd.uniform(-a, a), y + rnd.uniform(-a, a)) for x, y in pts]


def line(a, b, n=22):  # noqa: ANN001, ANN201
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n)]


def arc(c, r, t0, t1, n=26):  # noqa: ANN001, ANN201
    return [
        (c[0] + r * math.cos(t0 + (t1 - t0) * i / n), c[1] + r * math.sin(t0 + (t1 - t0) * i / n))
        for i in range(n)
    ]


def poly(pts, n=20):  # noqa: ANN001, ANN201
    out = []
    for a, b in zip(pts, pts[1:], strict=False):
        out += line(a, b, n)
    return [*out, pts[-1]]


def test_circle_fit_is_exact_on_a_circle():
    c, r, res = fh.fit_circle(__import__("numpy").array(arc((3, -2), 7.5, 0, 5)))
    assert (c[0], c[1], r) == (
        pytest.approx(3),
        pytest.approx(-2),
        pytest.approx(7.5),
    ) and res < 1e-9


def test_rough_rectangle_becomes_an_exact_constrained_rectangle():
    out = fh.clean_view(
        [wob(poly([(0, 0), (101, 2), (99, 61), (1, 59), (1.5, 1)]), 0.7)], None, None
    )
    assert out["counts"] == {"line": 4, "arc": 0, "circle": 0} and out["closed"]
    kinds = [c.kind for c in out["sketch"].constraints]
    assert kinds.count("horizontal") == 2 and kinds.count("vertical") == 2
    xs = sorted({round(p.x, 6) for p in out["sketch"].points})
    assert len(xs) == 2  # the solver made the sides exactly vertical


def test_extrude_plate_with_holes():
    rect = wob(poly([(0, 0), (101, 2), (99, 61), (1, 59), (1.5, 1)]), 0.7)
    circ = wob(arc((50, 30), 12, 0, 2 * math.pi * 1.02, 41), 0.4)
    doc, report = fh.part(fh.FreehandIn(views={"top": [rect, circ]}, mode="extrude", depth=10))
    shape = build_part(PartDoc.model_validate(doc)).shape
    bb = shape.BoundingBox()
    assert bb.zlen == pytest.approx(10)
    hole = report["top"]["counts"]["circle"] == 1
    assert hole and shape.Volume() == pytest.approx(
        bb.xlen * bb.ylen * 10 - math.pi * 12**2 * 10, rel=0.03
    )


def test_two_views_make_an_l_bracket():
    front = wob(poly([(0, 0), (80, 1), (79, 12), (14, 11), (15, 60), (1, 59), (0.5, 0.5)]), 0.6)
    top = wob(poly([(0, 0), (81, 0), (80, 40), (0, 41), (0.3, 0.2)]), 0.6)
    doc, _ = fh.part(fh.FreehandIn(views={"front": [front], "top": [top]}, mode="views"))
    assert [f["op"] for f in doc["features"]] == ["add", "intersect"]
    shape = build_part(PartDoc.model_validate(doc)).shape
    bb = shape.BoundingBox()
    l_area = bb.xlen * 12 + 14 * (bb.zlen - 12)  # base plus upright, approximately
    assert shape.Volume() == pytest.approx(l_area * bb.ylen, rel=0.08)


def test_revolve_about_the_left_edge():
    prof = wob(poly([(0, 0), (30, 0), (30, 80), (0, 80), (0, 0.5)]), 0.4)
    doc, _ = fh.part(fh.FreehandIn(views={"front": [prof]}, mode="revolve"))
    shape = build_part(PartDoc.model_validate(doc)).shape
    pts = doc["features"][0]["sketch"]["points"]
    r = max(p["x"] for p in pts) - min(p["x"] for p in pts)
    h = max(p["y"] for p in pts) - min(p["y"] for p in pts)
    assert r == pytest.approx(30, abs=1.0) and h == pytest.approx(80, abs=1.0)  # as drawn
    assert shape.Volume() == pytest.approx(math.pi * r**2 * h, rel=1e-6)  # a cylinder


def test_open_outline_is_refused_with_a_reason():
    with pytest.raises(ValueError, match="no closed outline"):
        fh.part(fh.FreehandIn(views={"top": [line((0, 0), (100, 0)) + line((100, 0), (100, 60))]}))


def test_recognition_benchmark():
    shapes = {
        "slot": (
            [
                *line((0, 0), (130, 0)),
                *arc((130, 50), 50, -math.pi / 2, math.pi / 2),
                *line((130, 100), (0, 100)),
                *line((0, 100), (0, 1)),
                (0.5, 0.4),
            ],
            {"line": 3, "arc": 1, "circle": 0},
        ),
        "rect": (
            poly([(0, 0), (101, 2), (99, 61), (1, 59), (1.5, 1)]),
            {"line": 4, "arc": 0, "circle": 0},
        ),
        "L": (
            poly([(0, 0), (80, 1), (79, 12), (14, 11), (15, 60), (1, 59), (0.5, 0.5)]),
            {"line": 6, "arc": 0, "circle": 0},
        ),
    }
    ok = total = 0
    for seed in range(10):
        for amp in (0.6, 1.2, 2.0):
            for pts, want in shapes.values():
                total += 1
                ok += fh.clean_view([wob(pts, amp, seed)], None, None)["counts"] == want
    assert ok >= 72, f"recognised {ok} of {total}"


def test_api(client: TestClient, project: str):
    rect = wob(poly([(0, 0), (101, 2), (99, 61), (1, 59), (1.5, 1)]), 0.7)
    clean = client.post("/api/freehand/clean", json={"strokes": [rect]}).json()
    assert clean["closed"] and clean["sketch"]["entities"]
    part = client.post(
        f"/api/projects/{project}/freehand", json={"views": {"top": [rect]}, "depth": 5}
    ).json()
    assert part["volume"] == pytest.approx(clean_area(clean) * 5, rel=0.05)


def clean_area(clean: dict) -> float:
    xs = [p["x"] for p in clean["sketch"]["points"]]
    ys = [p["y"] for p in clean["sketch"]["points"]]
    return (max(xs) - min(xs)) * (max(ys) - min(ys))


def test_new_parts_are_placed_beside_the_others(client: TestClient, project: str):
    rect = wob(poly([(0, 0), (101, 2), (99, 61), (1, 59), (1.5, 1)]), 0.7)
    a = client.post(
        f"/api/projects/{project}/freehand", json={"views": {"top": [rect]}, "depth": 5}
    ).json()
    b = client.post(
        f"/api/projects/{project}/freehand", json={"views": {"top": [rect]}, "depth": 5}
    ).json()
    a_right = a["document"]["at"]["x"] + a["bounds"][1][0]
    b_left = b["document"]["at"]["x"] + b["bounds"][0][0]
    assert b_left == pytest.approx(a_right + 20.0, abs=1e-3)
