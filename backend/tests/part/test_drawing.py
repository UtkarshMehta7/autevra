"""Engineering drawings: hidden-line views, dimensions and the title block."""

import pytest

from autevra.cad import kernel as k
from autevra.part import drawing

pytestmark = pytest.mark.cad


def _bracket() -> k.Shape:
    body = k.fuse(k.box((0, 80), (0, 40), (0, 10)), k.box((0, 10), (0, 40), (0, 70)))
    return k.cut(body, k.cylinder_z(6, (-1, 11), x=50, y=20))


def test_views_project_to_the_parts_extents() -> None:
    s = _bracket()
    front, top, right = (drawing.project(s, n) for n in ("front", "top", "right"))

    def size(v: drawing.View) -> tuple[float, float]:
        u0, v0, u1, v1 = v.bounds()
        return round(u1 - u0, 3), round(v1 - v0, 3)

    assert size(front) == (80, 70) and size(top) == (80, 40) and size(right) == (40, 70)
    assert front.hidden  # the bolt hole is hidden behind the foot in the front view
    assert [round(2 * r, 3) for *_, r in top.holes] == [12.0]  # seen end-on from above
    assert not front.holes


def test_the_sheet_carries_dimensions_and_an_escaped_title() -> None:
    svg = drawing.drawing_svg(_bracket(), "Bracket <A&B>")
    assert svg.startswith("<svg") and "Bracket &lt;A&amp;B&gt;" in svg
    for text in (">80<", ">70<", ">40<", "Ø12", "third angle", "FRONT", "ISOMETRIC"):
        assert text in svg
