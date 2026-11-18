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


def _block_with_holes() -> tuple[k.Shape, list[drawing.HoleNote]]:
    body = k.box((0, 120), (0, 60), (0, 30))
    for x in (30, 70):
        body = k.cut(body, k.cylinder_z(4.5, (-1, 31), x=x, y=30))
    notes = [drawing.HoleNote(x, 30, 30, "⌀9 THRU") for x in (30, 70)]
    return body, notes


def test_section_cuts_through_the_hole_row_and_hatches_the_solid() -> None:
    shape, notes = _block_with_holes()
    assert drawing._section_y(shape, notes) == 30
    view, regions = drawing.section_view(shape, 30)
    # the cut face is the block's section minus the two holes: three solid regions
    assert len(regions) == 3
    hatch = drawing._hatch(regions, 2.5)
    assert hatch and all(len(line) == 2 for line in hatch)
    u0, v0, u1, v1 = view.bounds()
    assert (round(u1 - u0, 3), round(v1 - v0, 3)) == (120, 30)


def test_sheet_has_datums_gdt_callouts_and_basic_dimensions() -> None:
    shape, notes = _block_with_holes()
    svg = drawing.drawing_svg(shape, "Block", holes=notes, material="EN AW-6082 T6", mass_kg=0.5)
    for text in (
        "SECTION A–A",
        "2× ⌀9 THRU",
        ">A<",
        ">B<",
        ">C<",
        "Ra 1.6",
        "Ra 3.2",
        "ISO 2768-mK",
        "EN AW-6082 T6",
        "0.500 kg",
        'class="hatch"',
        'class="bas"',
    ):
        assert text in svg, text
    # basic dimensions of the hole centres from datum B: 30 and 70; from C: 30
    assert svg.count('class="bas"') == 3
    import re

    xs = [float(v) for v in re.findall(r'\bx[12]?="(-?[\d.]+)"', svg)]
    assert min(xs) >= 0 and max(xs) <= drawing.SHEET[0] - drawing.MARGIN + 1e-6


def test_assembly_sheet_balloons_and_bom() -> None:
    a = k.box((0, 50), (0, 50), (0, 10))
    b = k.box((60, 80), (0, 20), (0, 20))
    svg = drawing.assembly_svg(
        [
            ("Plate", a, "metal", 25.0),
            ("Block", b, "paint", 8.0),
            ("Block", b.translate((0, 30, 0)), "paint", 8.0),
        ],
        "Fixture",
    )
    assert "BILL OF MATERIALS · 3 parts · 41 cm³" in svg
    assert svg.count('class="bal"') == 2  # two items: the blocks are one item, quantity 2
    assert ">Plate<" in svg and ">2<" in svg
    with pytest.raises(ValueError):
        drawing.assembly_svg([], "Empty")
