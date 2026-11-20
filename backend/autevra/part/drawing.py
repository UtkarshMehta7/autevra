"""Engineering drawings of a part: orthographic views with hidden lines, on a sheet.

Each view is the kernel's exact hidden-line removal (Open CASCADE HLRBRep): the part's
edges and silhouettes are projected along the view direction and split into visible and
hidden segments. The sheet is ISO A3 landscape in third-angle projection: the front view
(looking along +Y, so X runs right and Z up), the top view above it (looking down -Z), the
right-side view to its right (looking along -X) and an isometric view. Each orthographic
view carries its overall dimensions, and holes seen end-on carry diameter callouts. The
drawing scale is the largest standard scale at which the views fit.
"""

import datetime as dt
import math
from dataclasses import dataclass, field
from xml.sax.saxutils import escape

import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

from autevra.cad import kernel as k

SHEET = (420.0, 297.0)  # ISO A3 landscape, mm
MARGIN = 10.0
TITLE_H = 36.0
SCALES = (10.0, 5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005)

# view name -> (direction the viewer looks along, the sheet's "up" direction in the part)
VIEWS = {
    "front": ((0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    "top": ((0.0, 0.0, -1.0), (0.0, 1.0, 0.0)),
    "right": ((-1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
    "iso": ((-1.0, 1.0, -1.0), (0.0, 0.0, 1.0)),
}

Polyline = list[tuple[float, float]]


@dataclass
class View:
    name: str
    visible: list[Polyline] = field(default_factory=list)
    hidden: list[Polyline] = field(default_factory=list)
    holes: list[tuple[float, float, float]] = field(default_factory=list)  # (u, v, radius)

    def bounds(self) -> tuple[float, float, float, float]:
        pts = [p for line in self.visible + self.hidden for p in line] or [(0.0, 0.0)]
        us, vs = [p[0] for p in pts], [p[1] for p in pts]
        return min(us), min(vs), max(us), max(vs)


def _frame(
    look: tuple[float, float, float], up: tuple[float, float, float]
) -> tuple[gp_Ax2, tuple[float, ...], tuple[float, ...]]:
    """The projector frame: its Z axis points back at the viewer, its X axis is the
    sheet's right; returns it with the sheet's right and up vectors in part space."""
    back = tuple(-c for c in look)
    n = math.sqrt(sum(c * c for c in back))
    back = tuple(c / n for c in back)
    dot = sum(a * b for a, b in zip(up, back, strict=True))
    upv = tuple(u - dot * b for u, b in zip(up, back, strict=True))
    m = math.sqrt(sum(c * c for c in upv))
    upv = tuple(c / m for c in upv)
    right = (
        upv[1] * back[2] - upv[2] * back[1],
        upv[2] * back[0] - upv[0] * back[2],
        upv[0] * back[1] - upv[1] * back[0],
    )
    ax = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*back), gp_Dir(*right))
    return ax, right, upv


def _polylines(compound, tolerance: float) -> list[Polyline]:  # type: ignore[no-untyped-def]
    out: list[Polyline] = []
    if compound is None or compound.IsNull():
        return out
    explorer = TopExp_Explorer(compound, TopAbs_EDGE)
    while explorer.More():
        curve = BRepAdaptor_Curve(TopoDS.Edge_s(explorer.Current()))
        explorer.Next()
        sampler = GCPnts_QuasiUniformDeflection(curve, tolerance)
        if not sampler.IsDone() or sampler.NbPoints() < 2:
            continue
        out.append(
            [(sampler.Value(i).X(), sampler.Value(i).Y()) for i in range(1, sampler.NbPoints() + 1)]
        )
    return out


def project(shape: k.Shape, name: str, tolerance: float = 0.05) -> View:
    """Hidden-line projection of the part along one of the named view directions."""
    look, up = VIEWS[name]
    ax, right, upv = _frame(look, up)
    algo = HLRBRep_Algo()
    algo.Add(shape.wrapped)
    algo.Projector(HLRAlgo_Projector(ax))
    algo.Update()
    algo.Hide()
    hlr = HLRBRep_HLRToShape(algo)
    view = View(name)
    for getter in (hlr.VCompound, hlr.OutLineVCompound, hlr.Rg1LineVCompound):
        view.visible += _polylines(getter(), tolerance)
    for getter in (hlr.HCompound, hlr.OutLineHCompound):
        view.hidden += _polylines(getter(), tolerance)
    if name != "iso":  # circles whose axis is the view direction appear as true circles
        for edge in shape.Edges():
            if edge.geomType() != "CIRCLE":
                continue
            circle = BRepAdaptor_Curve(edge.wrapped).Circle()
            axis = circle.Axis().Direction()
            if abs(abs(axis.X() * look[0] + axis.Y() * look[1] + axis.Z() * look[2]) - 1) > 1e-6:
                continue
            c = circle.Location()
            u = c.X() * right[0] + c.Y() * right[1] + c.Z() * right[2]
            v = c.X() * upv[0] + c.Y() * upv[1] + c.Z() * upv[2]
            if not any(
                abs(u - a) < 1e-3 and abs(v - b) < 1e-3 and abs(circle.Radius() - r) < 1e-3
                for a, b, r in view.holes
            ):
                view.holes.append((u, v, circle.Radius()))
    return view


def _fmt(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _scale_label(s: float) -> str:
    return f"{_fmt(s)}:1" if s >= 1 else f"1:{_fmt(1 / s)}"


@dataclass
class HoleNote:
    """A Hole feature for the drawing: its entry point (part frame) and callout."""

    x: float
    y: float
    z: float
    callout: str
    vertical: bool = True


def _section_y(shape: k.Shape, holes: list[HoleNote]) -> float:
    """Cutting plane for section A-A: through the most common hole row, else the middle."""
    (x0, y0, z0), (x1, y1, z1) = k.bounds(shape)
    rows: dict[float, int] = {}
    for h in holes:
        if h.vertical and y0 < h.y < y1:
            rows[round(h.y, 3)] = rows.get(round(h.y, 3), 0) + 1
    return max(rows, key=lambda y: (rows[y], -abs(y - (y0 + y1) / 2))) if rows else (y0 + y1) / 2


def section_view(
    shape: k.Shape, y: float, tolerance: float = 0.05
) -> tuple[View, list[list[Polyline]]]:
    """Section A-A: the part behind the cutting plane y (looking along +Y, as the front
    view) with hidden lines dropped, and the cut regions as (outer, holes...) rings in the
    front view's (x, z) for hatching."""
    (x0, y0, z0), (x1, y1, z1) = k.bounds(shape)
    pad = 1.0 + 0.01 * max(x1 - x0, z1 - z0)
    keep = k.box((x0 - pad, x1 + pad), (y, y1 + pad), (z0 - pad, z1 + pad))
    half = k.intersect(shape, keep)
    view = project(half, "front", tolerance)
    view.name = "section"
    view.hidden = []
    plane = cq.Face.makePlane(
        4 * (x1 - x0 + z1 - z0) + 10,
        4 * (x1 - x0 + z1 - z0) + 10,
        basePnt=cq.Vector((x0 + x1) / 2, y, (z0 + z1) / 2),
        dir=cq.Vector(0, 1, 0),
    )
    regions = []
    for face in shape.intersect(plane).Faces():
        rings = [face.outerWire(), *face.innerWires()]
        polys = []
        for w in rings:
            polys.append([(q.x, q.z) for q in _wire_points(w, tolerance)])
        regions.append(polys)
    return view, regions


def _wire_points(w: cq.Wire, tol: float) -> list[cq.Vector]:
    from OCP.BRepAdaptor import BRepAdaptor_CompCurve

    curve = BRepAdaptor_CompCurve(w.wrapped)
    s = GCPnts_QuasiUniformDeflection(curve, tol)
    return [
        cq.Vector(s.Value(i).X(), s.Value(i).Y(), s.Value(i).Z())
        for i in range(1, s.NbPoints() + 1)
    ]


def _hatch(regions: list[list[Polyline]], spacing: float) -> list[Polyline]:
    """45 degree hatch lines clipped to the cut regions (part units)."""
    from shapely import LineString, Polygon
    from shapely.ops import unary_union

    polys = []
    for rings in regions:
        if rings and len(rings[0]) >= 3:
            polys.append(Polygon(rings[0], [r for r in rings[1:] if len(r) >= 3]).buffer(0))
    if not polys:
        return []
    area = unary_union(polys)
    minx, miny, maxx, maxy = area.bounds
    out: list[Polyline] = []
    c = minx - (maxy - miny)
    while c < maxx:
        line = LineString([(c, miny), (c + (maxy - miny), maxy)]).intersection(area)
        for g in getattr(line, "geoms", [line]):
            if not g.is_empty and g.geom_type == "LineString":
                out.append(list(g.coords))
        c += spacing * math.sqrt(2)
    return out


# --- GD&T and surface-texture symbols (ISO 1101, ISO 1302), drawn as vectors ---


def _sym(kind: str, x: float, y: float, s: float = 3.0) -> str:
    """A geometric characteristic symbol centred in a cell at (x, y), cell height s."""
    h = s * 0.32
    if kind == "flatness":
        return (
            f'<path class="gd" d="M{x - h * 1.2:.2f},{y + h * 0.5:.2f} '
            f"L{x - h * 0.4:.2f},{y - h * 0.5:.2f} "
            f'L{x + h * 1.2:.2f},{y - h * 0.5:.2f} L{x + h * 0.4:.2f},{y + h * 0.5:.2f} Z"/>'
        )
    if kind == "position":
        return (
            f'<circle class="gd" cx="{x:.2f}" cy="{y:.2f}" r="{h * 0.8:.2f}"/>'
            f'<path class="gd" d="M{x - h * 1.3:.2f},{y:.2f} H{x + h * 1.3:.2f} '
            f"M{x:.2f},{y - h * 1.3:.2f} "
            f'V{y + h * 1.3:.2f}"/>'
        )
    if kind == "perpendicularity":
        return (
            f'<path class="gd" d="M{x - h:.2f},{y + h:.2f} H{x + h:.2f} M{x:.2f},{y + h:.2f} '
            f'V{y - h:.2f}"/>'
        )
    if kind == "parallelism":
        return (
            f'<path class="gd" d="M{x - h * 0.9:.2f},{y + h:.2f} L{x - h * 0.1:.2f},{y - h:.2f} '
            f'M{x + h * 0.1:.2f},{y + h:.2f} L{x + h * 0.9:.2f},{y - h:.2f}"/>'
        )
    return ""


def _fcf(
    x: float, y: float, kind: str, tol: str, datums: tuple[str, ...] = ()
) -> tuple[str, float]:
    """A feature control frame with its top-left corner at (x, y); returns (svg, width)."""
    hgt, cell = 4.4, 5.2
    widths = [cell, 4.0 + 1.7 * len(tol)] + [cell for _ in datums]
    out, cx = [], x
    for i, w in enumerate(widths):
        out.append(f'<rect class="gdf" x="{cx:.2f}" y="{y:.2f}" width="{w:.2f}" height="{hgt}"/>')
        if i == 0:
            out.append(_sym(kind, cx + w / 2, y + hgt / 2, hgt))
        else:
            text = tol if i == 1 else datums[i - 2]
            out.append(
                f'<text class="gdt" x="{cx + w / 2:.2f}" '
                f'y="{y + hgt / 2 + 1.05:.2f}">{escape(text)}</text>'
            )
        cx += w
    return "".join(out), cx - x


def _datum(x: float, y: float, letter: str, side: str) -> str:
    """Datum feature symbol: a filled triangle on the feature at (x, y), a leader and the
    boxed letter, away from the part towards ``side`` (down, left, up, right)."""
    dx, dy = {"down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0)}[side]
    t = 1.4
    if dy:
        tri = f"M{x - t:.2f},{y:.2f} L{x + t:.2f},{y:.2f} L{x:.2f},{y + dy * t * 1.2:.2f} Z"
    else:
        tri = f"M{x:.2f},{y - t:.2f} L{x:.2f},{y + t:.2f} L{x + dx * t * 1.2:.2f},{y:.2f} Z"
    ex, ey = x + dx * 7, y + dy * 7
    bx, by = ex + (dx * 2.5 if dx else 0) - 2.5, ey + (dy * 2.5 if dy else 0) - 2.5
    return (
        f'<path class="gdfill" d="{tri}"/><line class="gd" x1="{x:.2f}" y1="{y:.2f}" x2="{ex:.2f}" '
        f'y2="{ey:.2f}"/>'
        f'<rect class="gdf" x="{bx:.2f}" y="{by:.2f}" width="5" height="5"/>'
        f'<text class="gdt" x="{bx + 2.5:.2f}" y="{by + 3.6:.2f}">{letter}</text>'
    )


def _finish(x: float, y: float, ra: str, removal: bool = True) -> str:
    """ISO 1302 surface texture symbol standing on (x, y) with the Ra value."""
    a = 2.6
    d = (
        f"M{x - a * 0.58:.2f},{y - a:.2f} L{x:.2f},{y:.2f} L{x + a * 1.15:.2f},{y - a * 2:.2f} "
        f"H{x + a * 3.2:.2f}"
    )
    bar = (
        f'<line class="gd" x1="{x - a * 0.58:.2f}" y1="{y - a:.2f}" x2="{x + a * 0.58:.2f}" '
        f'y2="{y - a:.2f}"/>'
    )
    return (
        f'<path class="gd" d="{d}"/>'
        + (bar if removal else "")
        + f'<text class="gdt" x="{x + a * 2.2:.2f}" y="{y - a * 2 - 0.8:.2f}">Ra '
        f"{escape(ra)}</text>"
    )


def drawing_svg(
    shape: k.Shape,
    title: str,
    author: str = "",
    holes: list[HoleNote] | None = None,
    material: str = "",
    mass_kg: float | None = None,
    section: bool = True,
) -> str:
    """An A3 sheet in third-angle projection: front, top and right views with hidden
    lines, section A-A (hatched cut through the hole row), an isometric view, overall and
    hole-position dimensions (basic, boxed, from datums B and C), datums A-C, GD&T frames
    (flatness of the top, perpendicularity of B to A, position of the holes to A|B|C at
    maximum material condition), ISO 1302 surface texture, hole callouts from the Hole
    features, general notes (ISO 2768-mK, ISO 8015) and the title block."""
    holes = holes or []
    views = {name: project(shape, name) for name in VIEWS}
    (x0, y0, z0), (x1, y1, z1) = k.bounds(shape)
    sec = None
    if section:
        try:
            yc = _section_y(shape, holes)
            sv, regions = section_view(shape, yc)
            if sv.visible:
                sec = (yc, sv, regions)
        except Exception:  # the kernel raises many types; the sheet is drawn without it
            sec = None
    size = {"front": (x1 - x0, z1 - z0), "top": (x1 - x0, y1 - y0), "right": (y1 - y0, z1 - z0)}
    iso_b = views["iso"].bounds()
    iso = (iso_b[2] - iso_b[0], iso_b[3] - iso_b[1])
    gap = 30.0
    notes_w = 112.0
    area_w = SHEET[0] - 2 * MARGIN - 3 * gap
    area_h = SHEET[1] - 2 * MARGIN - TITLE_H - 2 * gap - 6
    row_w = size["front"][0] + size["right"][0] + (size["front"][0] if sec else 0)
    scale = next(
        (
            s
            for s in SCALES
            if s * row_w <= area_w
            and s * (size["front"][1] + size["top"][1]) <= area_h
            and s * max(iso[0] * 0.75, 1e-9) <= area_w - s * size["top"][0] - notes_w * 0.3
        ),
        SCALES[-1],
    )
    left = MARGIN + gap
    bottom = SHEET[1] - MARGIN - TITLE_H - gap
    places = {
        "front": (left, bottom - scale * size["front"][1]),
        "top": (left, bottom - scale * size["front"][1] - gap - scale * size["top"][1]),
        "right": (left + scale * size["front"][0] + gap, bottom - scale * size["front"][1]),
    }
    if sec:
        places["section"] = (
            places["right"][0] + scale * size["right"][0] + gap,
            places["front"][1],
        )
    iso_scale = min(
        scale,
        (SHEET[0] - MARGIN - gap - (left + scale * size["top"][0] + gap)) / max(iso[0], 1e-9),
        (places["front"][1] - gap - MARGIN - 6) / max(iso[1], 1e-9),
    )
    places["iso"] = (left + scale * size["top"][0] + gap * 1.5, MARGIN + 8)

    parts: list[str] = []

    def to_sheet(name: str, u: float, v: float, sc: float | None = None) -> tuple[float, float]:
        b = (
            (sec[1] if name == "section" else views[name]).bounds()
            if name != "section" or sec
            else (0, 0, 0, 0)
        )
        o, f = places[name], sc or scale
        return o[0] + f * (u - b[0]), o[1] + f * (b[3] - v)

    def path(line: Polyline, name: str, cls: str, sc: float | None = None) -> str:
        pts = " ".join("{:.2f},{:.2f}".format(*to_sheet(name, u, v, sc)) for u, v in line)
        return f'<polyline class="{cls}" points="{pts}"/>'

    drawn = dict(views)
    if sec:
        drawn["section"] = sec[1]
    for name, view in drawn.items():
        sc = iso_scale if name == "iso" else scale
        b = view.bounds()
        o = places[name]
        parts += [path(line, name, "hid", sc) for line in view.hidden]
        parts += [path(line, name, "vis", sc) for line in view.visible]
        w, h = sc * (b[2] - b[0]), sc * (b[3] - b[1])
        label = {
            "front": "FRONT",
            "top": "TOP",
            "right": "RIGHT",
            "iso": "ISOMETRIC",
            "section": "SECTION A–A",
        }[name]
        parts.append(
            f'<text class="lbl" x="{o[0] + w / 2:.1f}" y="{o[1] + h + 19:.1f}">{label}</text>'
        )
        if name in ("iso", "section"):
            continue
        parts.append(_dimension(o[0], o[1] + h + 8, o[0] + w, o[1] + h + 8, b[2] - b[0], "h"))
        parts.append(_dimension(o[0] - 8, o[1], o[0] - 8, o[1] + h, b[3] - b[1], "v"))

    # section: hatch, and the cutting-plane line A-A on the top view
    if sec:
        yc, sv, regions = sec
        b = sv.bounds()
        parts += [path(line, "section", "hatch") for line in _hatch(regions, 2.5 / scale)]
        tb = views["top"].bounds()
        ax, ay = to_sheet("top", tb[0], yc)
        bx, _ = to_sheet("top", tb[2], yc)
        parts.append(
            f'<line class="cut" x1="{ax - 5:.2f}" y1="{ay:.2f}" x2="{bx + 5:.2f}" y2="{ay:.2f}"/>'
        )
        for xx in (ax - 5, bx + 5):  # arrows point the way the section is viewed (+Y: up the sheet)
            parts.append(
                f'<path class="cutfill" d="M{xx - 1.2:.2f},{ay - 3:.2f} L{xx:.2f},{ay - 6:.2f} '
                f'L{xx + 1.2:.2f},{ay - 3:.2f} Z"/>'
                f'<line class="cutthin" x1="{xx:.2f}" y1="{ay:.2f}" x2="{xx:.2f}" '
                f'y2="{ay - 4:.2f}"/>'
                f'<text class="lbl" x="{xx:.2f}" y="{ay - 7:.2f}">A</text>'
            )

    # datums on extension lines of their faces, clear of the dimensions: A the bottom face
    # and B the left face (front view), C the front face (top view)
    fb = views["front"].bounds()
    fx0, fy1 = to_sheet("front", fb[0], fb[1])
    fx1, fy0 = to_sheet("front", fb[2], fb[3])
    tbb = views["top"].bounds()
    tx0, ty1 = to_sheet("top", tbb[0], tbb[1])
    tx1, ty0 = to_sheet("top", tbb[2], tbb[3])
    reach = min(gap - 6, 16.0)
    parts.append(
        _line(fx1 + 1, fy1, fx1 + reach, fy1, "ext") + _datum(fx1 + reach - 3, fy1, "A", "down")
    )
    parts.append(_line(fx0, fy0 - 1, fx0, fy0 - 16, "ext") + _datum(fx0, fy0 - 13, "B", "left"))
    parts.append(
        _line(tx1 + 1, ty1, tx1 + reach, ty1, "ext") + _datum(tx1 + reach - 3, ty1, "C", "down")
    )
    # GD&T: flatness and finish on the top face, perpendicularity of the left face B to A
    ax_ = fx0 + (fx1 - fx0) * 0.45
    frame, fw = _fcf(ax_, fy0 - 9.5, "flatness", "0.05")
    parts.append(frame + _line(ax_ + 2, fy0 - 5.1, ax_ + 2, fy0, "gd"))
    parts.append(_finish(ax_ + fw + 4, fy0, "1.6"))
    # attached to the extension line of B, between the top view's dimension and its label
    frame, pw = _fcf(fx0, fy0 - 18.6, "perpendicularity", "0.1", ("A",))
    parts.append(frame + _line(fx0, fy0 - 16, fx0, fy0 - 14.2, "ext"))

    # holes in the top view: callouts from the features, positions as basic dimensions
    top = views["top"]
    matched: set[int] = set()
    groups: dict[str, list[HoleNote]] = {}
    parts_done: list[str] = []
    for h in holes:
        if h.vertical:
            groups.setdefault(h.callout, []).append(h)
    for callout, members in groups.items():
        h = members[0]
        cx, cy = to_sheet("top", h.x, h.y)
        r = max(
            (rr for u, v, rr in top.holes if abs(u - h.x) < 1e-3 and abs(v - h.y) < 1e-3),
            default=2.0,
        )
        for i, (u, v, _) in enumerate(top.holes):
            if any(abs(u - m.x) < 1e-3 and abs(v - m.y) < 1e-3 for m in members):
                matched.add(i)
        # leader up and out of the view, past the ordinate dimensions
        lx, ly = cx + scale * r * 0.7 + 4, ty0 - 20 - 9 * len(parts_done)
        parts_done.append(callout)
        count = f"{len(members)}× " if len(members) > 1 else ""
        parts.append(
            _line(cx + scale * r * 0.7, cy - scale * r * 0.7, lx, ly)
            + _line(lx, ly, lx + 3, ly)
            + f'<text class="dimt" x="{lx + 3.5:.2f}" y="{ly - 0.8:.2f}" '
            f'text-anchor="start">{escape(count + callout)}</text>'
        )
        frame, _ = _fcf(lx + 3.5, ly + 0.6, "position", "⌀0.2 Ⓜ", ("A", "B", "C"))
        parts.append(frame)
    for i, (u, v, r) in enumerate(top.holes):
        cx, cy = to_sheet("top", u, v)
        parts.append(
            f'<line class="ctr" x1="{cx - scale * r - 3:.2f}" y1="{cy:.2f}" '
            f'x2="{cx + scale * r + 3:.2f}" y2="{cy:.2f}"/>'
            f'<line class="ctr" x1="{cx:.2f}" y1="{cy - scale * r - 3:.2f}" x2="{cx:.2f}" '
            f'y2="{cy + scale * r + 3:.2f}"/>'
        )
        if i in matched:
            continue
        tx, ty = cx + scale * r * 0.7 + 4, cy - scale * r * 0.7 - 4
        parts.append(
            f'<line class="dim" x1="{cx + scale * r * 0.7:.2f}" y1="{cy - scale * r * 0.7:.2f}" '
            f'x2="{tx:.2f}" y2="{ty:.2f}"/>'
            f'<text class="dimt" x="{tx + 1:.2f}" y="{ty - 1:.2f}" '
            f'text-anchor="start">Ø{_fmt(2 * r)}</text>'
        )
    # basic (boxed) ordinate dimensions of the hole centres from datums B (x) and C (y)
    centres = sorted({(round(u, 3), round(v, 3)) for u, v, _ in top.holes})
    xs = sorted({u for u, _ in centres})
    ys = sorted({v for _, v in centres})
    for u in xs:
        sx, _ = to_sheet("top", u, tbb[3])
        parts.append(
            _line(sx, ty0 - 1, sx, ty0 - 5) + _basic(sx, ty0 - 6.5, u - tbb[0], vertical=True)
        )
    for v in ys:
        _, sy = to_sheet("top", tbb[0], v)
        parts.append(_line(tx1 + 1, sy, tx1 + 12, sy, "ext") + _basic(tx1 + 13, sy, v - tbb[1]))

    # notes and the general surface texture
    nx, ny = MARGIN + 4, SHEET[1] - MARGIN - TITLE_H + 4
    lines = [
        "NOTES",
        "1. DIMENSIONS IN MM. GENERAL TOLERANCES ISO 2768-mK.",
        "2. GEOMETRICAL TOLERANCING ISO 1101; INDEPENDENCY PRINCIPLE ISO 8015.",
        "3. BOXED DIMENSIONS ARE BASIC (THEORETICALLY EXACT).",
        "4. BREAK SHARP EDGES 0.2 × 45°. THREADS ISO 965-1 6H.",
        f"5. MATERIAL: {material.upper() or 'AS SPECIFIED'}.",
    ]
    for i, text in enumerate(lines):
        parts.append(
            f'<text class="note{" b" if i == 0 else ""}" x="{nx:.1f}" '
            f'y="{ny + 4 + i * 5:.1f}">{escape(text)}</text>'
        )
    gx = SHEET[0] - MARGIN - 180.0 - 30
    parts.append(
        _finish(gx, SHEET[1] - MARGIN - 8, "3.2")
        + f'<text class="gdt" x="{gx + 15:.1f}" y="{SHEET[1] - MARGIN - 9.5:.1f}">( √ )</text>'
    )
    parts.append(_title_block(title, scale, author, shape, material, mass_kg))
    w, h = SHEET
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
        f'viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif">'
        "<style>.vis{fill:none;stroke:#111;stroke-width:0.35}"
        ".hid{fill:none;stroke:#555;stroke-width:0.18;stroke-dasharray:1.5 0.8}"
        ".ctr{stroke:#555;stroke-width:0.13;stroke-dasharray:4 0.8 0.6 0.8}"
        ".dim{stroke:#1a4fa0;stroke-width:0.15;fill:none}"
        ".dimt{fill:#1a4fa0;font-size:3px;text-anchor:middle}"
        ".lbl{font-size:3.5px;text-anchor:middle;font-weight:bold}"
        ".hatch{fill:none;stroke:#333;stroke-width:0.13}"
        ".cut{stroke:#111;stroke-width:0.25;stroke-dasharray:6 1 1 1}"
        ".cutthin{stroke:#111;stroke-width:0.3}.cutfill{fill:#111}"
        ".gd,.gdf{fill:none;stroke:#111;stroke-width:0.2}.gdfill{fill:#111}"
        ".gdt{font-size:2.8px;text-anchor:middle;fill:#111}"
        ".bas{fill:none;stroke:#1a4fa0;stroke-width:0.15}.ext{stroke:#1a4fa0;stroke-width:0.13}"
        ".note{font-size:2.6px;fill:#111}.note.b{font-weight:bold}"
        ".tb{fill:none;stroke:#111;stroke-width:0.35}.tbt{font-size:3px}.tbv{font-size:4.2px}"
        "</style>"
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>'
        f'<rect class="tb" x="{MARGIN}" y="{MARGIN}" width="{w - 2 * MARGIN}" '
        f'height="{h - 2 * MARGIN}"/>' + "".join(parts) + "</svg>"
    )


def _basic(x: float, y: float, value: float, vertical: bool = False) -> str:
    """A boxed basic dimension value centred at (x, y)."""
    text = _fmt(value)
    w = 2.2 + 1.6 * len(text)
    if vertical:
        return (
            f'<g transform="rotate(-90 {x:.2f} {y:.2f})"><rect class="bas" x="{x:.2f}" '
            f'y="{y - 1.9:.2f}" '
            f'width="{w:.2f}" height="3.8"/><text class="dimt" x="{x + w / 2:.2f}" '
            f'y="{y + 1.05:.2f}">{text}</text></g>'
        )
    return (
        f'<rect class="bas" x="{x:.2f}" y="{y - 1.9:.2f}" width="{w:.2f}" height="3.8"/>'
        f'<text class="dimt" x="{x + w / 2:.2f}" y="{y + 1.05:.2f}">{text}</text>'
    )


def assembly_svg(
    parts_in: list[tuple[str, k.Shape, str, float]], title: str, author: str = ""
) -> str:
    """An A3 assembly sheet: the placed parts in an isometric hidden-line view, a balloon
    with a leader to each item, and the bill of materials (item, quantity, name, finish,
    volume). ``parts_in``: (name, shape in the project frame, finish, volume cm³); parts
    with the same name and volume are one item."""
    if not parts_in:
        raise ValueError("the project has no parts to draw")
    items: dict[tuple[str, float], list[tuple[str, k.Shape, str, float]]] = {}
    for p in parts_in:
        items.setdefault((p[0], round(p[3], 3)), []).append(p)
    whole = cq.Compound.makeCompound([p[1] for p in parts_in])
    view = project(whole, "iso", 0.2)
    look, up = VIEWS["iso"]
    _, right, upv = _frame(look, up)
    b = view.bounds()
    bom_h = 8.0 + 6.0 * len(items)
    area_w = SHEET[0] - 2 * MARGIN - 60.0
    area_h = SHEET[1] - 2 * MARGIN - TITLE_H - bom_h - 40.0
    scale = min(area_w / max(b[2] - b[0], 1e-9), area_h / max(b[3] - b[1], 1e-9))
    std = next((s for s in SCALES if s <= scale), SCALES[-1])
    ox = MARGIN + 30 + (area_w - std * (b[2] - b[0])) / 2
    oy = MARGIN + 25 + (area_h - std * (b[3] - b[1])) / 2

    def sheet(u: float, v: float) -> tuple[float, float]:
        return ox + std * (u - b[0]), oy + std * (b[3] - v)

    out: list[str] = []
    for cls, lines in (("vis", view.visible),):  # assembly views omit hidden lines
        for line in lines:
            pts = " ".join("{:.2f},{:.2f}".format(*sheet(u, v)) for u, v in line)
            out.append(f'<polyline class="{cls}" points="{pts}"/>')
    cx_sheet = ox + std * (b[2] - b[0]) / 2
    cy_sheet = oy + std * (b[3] - b[1]) / 2
    anchors = []
    for n, members in enumerate(items.values(), start=1):
        c = members[0][1].Center()
        u = c.x * right[0] + c.y * right[1] + c.z * right[2]
        v = c.x * upv[0] + c.y * upv[1] + c.z * upv[2]
        anchors.append((n, *sheet(u, v)))
    # balloons on a ring around the view, in angle order, so leaders do not cross
    rx = std * (b[2] - b[0]) / 2 + 18
    ry = std * (b[3] - b[1]) / 2 + 14
    anchors.sort(key=lambda a: math.atan2(a[2] - cy_sheet, a[1] - cx_sheet))
    for n, ax, ay in anchors:
        ang = math.atan2(ay - cy_sheet, ax - cx_sheet)
        bx, by = cx_sheet + rx * math.cos(ang), cy_sheet + ry * math.sin(ang)
        out.append(
            f'<circle class="gdfill" cx="{ax:.2f}" cy="{ay:.2f}" r="0.6"/>'
            f'<line class="gd" x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}"/>'
            f'<circle class="bal" cx="{bx:.2f}" cy="{by:.2f}" r="4"/>'
            f'<text class="balt" x="{bx:.2f}" y="{by + 1.3:.2f}">{n}</text>'
        )
    # bill of materials above the title block, ruled table
    tx, tw = SHEET[0] - MARGIN - 180.0, 180.0
    ty = SHEET[1] - MARGIN - TITLE_H - bom_h
    cols = [("ITEM", 12), ("QTY", 12), ("PART NAME", 86), ("FINISH", 34), ("VOL. cm³", 36)]
    out.append(f'<rect class="tb" x="{tx}" y="{ty:.2f}" width="{tw}" height="{bom_h:.2f}"/>')
    rows = [
        (str(i), str(len(m)), escape(m[0][0]), escape(m[0][2] or "-"), f"{m[0][3]:.3f}")
        for i, m in enumerate(items.values(), start=1)
    ]
    rows = [(a, b, c, d, f"{float(e):.1f}") for a, b, c, d, e in rows]
    total = sum(p[3] for p in parts_in)
    for r, row in enumerate([tuple(c for c, _ in cols), *rows]):
        y = ty + 6.0 + r * 6.0 - (0 if r else 0)
        cx = tx
        for (_, w), text in zip(cols, row, strict=True):
            out.append(
                f'<text class="{"tbt b" if r == 0 else "tbt"}" x="{cx + 2:.2f}" '
                f'y="{y:.2f}">{text}</text>'
            )
            cx += w
        out.append(f'<line class="tb" x1="{tx}" y1="{y + 2:.2f}" x2="{tx + tw}" y2="{y + 2:.2f}"/>')
    out.append(
        f'<text class="tbt b" x="{tx + 2:.2f}" y="{ty - 2:.2f}">BILL OF MATERIALS · '
        f"{len(parts_in)} parts · {total:.0f} cm³</text>"
    )
    out.append(_assembly_title(title, std, author, len(items)))
    w, h = SHEET
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} '
        f'{h}" '
        'font-family="Helvetica, Arial, sans-serif"><style>'
        ".vis{fill:none;stroke:#111;stroke-width:0.3}"
        ".hid{fill:none;stroke:#999;stroke-width:0.12;stroke-dasharray:1.2 0.8}"
        ".gd{fill:none;stroke:#111;stroke-width:0.2}.gdfill{fill:#111}"
        ".bal{fill:#fff;stroke:#111;stroke-width:0.3}"
        ".balt{font-size:3.6px;text-anchor:middle;font-weight:bold}"
        ".tb{fill:none;stroke:#111;stroke-width:0.3}.tbt{font-size:3px}.tbt.b{font-weight:bold}"
        ".tbv{font-size:4.2px}"
        f'</style><rect width="{w}" height="{h}" fill="#fff"/>'
        f'<rect class="tb" x="{MARGIN}" y="{MARGIN}" width="{w - 2 * MARGIN}" '
        f'height="{h - 2 * MARGIN}"/>' + "".join(out) + "</svg>"
    )


def _assembly_title(title: str, scale: float, author: str, items: int) -> str:
    w, h = SHEET
    x, y = w - MARGIN - 180.0, h - MARGIN - TITLE_H
    rows = [
        ("TITLE", escape(title)),
        ("SCALE", _scale_label(scale)),
        ("UNITS", "mm"),
        ("VIEW", "isometric"),
        ("ITEMS", str(items)),
        ("DATE", dt.date.today().isoformat()),
        ("DRAWN", escape(author or "Autevra")),
        ("SHEET", "A3 assembly"),
    ]
    out = [f'<rect class="tb" x="{x}" y="{y}" width="180" height="{TITLE_H}"/>']
    cw, rh = 90.0, TITLE_H / 4
    for i, (key, value) in enumerate(rows):
        cx, cy = x + (i % 2) * cw, y + (i // 2) * rh
        out.append(
            f'<rect class="tb" x="{cx}" y="{cy}" width="{cw}" height="{rh}"/>'
            f'<text class="tbt" x="{cx + 2}" y="{cy + 3.4}">{key}</text>'
            f'<text class="tbv" x="{cx + 24}" y="{cy + 6.6}">{value}</text>'
        )
    return "".join(out)


def _line(x1: float, y1: float, x2: float, y2: float, cls: str = "dim") -> str:
    return f'<line class="{cls}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>'


def _dimension(xa: float, ya: float, xb: float, yb: float, value: float, kind: str) -> str:
    """A dimension line with arrowheads and extension lines (sheet coordinates, mm)."""
    a = 1.6  # arrowhead length
    if kind == "h":
        ext = _line(xa, ya - 5, xa, ya + 1) + _line(xb, yb - 5, xb, yb + 1)
        heads = (
            f'<path class="dim" d="M{xa + a:.2f},{ya - 0.5:.2f} L{xa:.2f},{ya:.2f} '
            f"L{xa + a:.2f},{ya + 0.5:.2f} M{xb - a:.2f},{yb - 0.5:.2f} L{xb:.2f},{yb:.2f} "
            f'L{xb - a:.2f},{yb + 0.5:.2f}"/>'
        )
        text = f'<text class="dimt" x="{(xa + xb) / 2:.2f}" y="{ya - 1:.2f}">{_fmt(value)}</text>'
    else:
        ext = _line(xa - 1, ya, xa + 5, ya) + _line(xb - 1, yb, xb + 5, yb)
        heads = (
            f'<path class="dim" d="M{xa - 0.5:.2f},{ya + a:.2f} L{xa:.2f},{ya:.2f} '
            f"L{xa + 0.5:.2f},{ya + a:.2f} M{xb - 0.5:.2f},{yb - a:.2f} L{xb:.2f},{yb:.2f} "
            f'L{xb + 0.5:.2f},{yb - a:.2f}"/>'
        )
        my = (ya + yb) / 2
        text = (
            f'<text class="dimt" x="{xa - 1:.2f}" y="{my:.2f}" '
            f'transform="rotate(-90 {xa - 1:.2f} {my:.2f})">{_fmt(value)}</text>'
        )
    return ext + _line(xa, ya, xb, yb) + heads + text


def _title_block(
    title: str,
    scale: float,
    author: str,
    shape: k.Shape,
    material: str = "",
    mass_kg: float | None = None,
) -> str:
    w, h = SHEET
    x, y = w - MARGIN - 180.0, h - MARGIN - TITLE_H
    mass = f"{mass_kg:.3f} kg" if mass_kg is not None else f"{k.volume(shape) / 1000:.1f} cm³"
    rows = [
        ("TITLE", escape(title)),
        ("SCALE", _scale_label(scale)),
        ("MATERIAL", escape(material or "-")),
        ("PROJECTION", "third angle"),
        ("MASS" if mass_kg is not None else "VOLUME", mass),
        ("DATE", dt.date.today().isoformat()),
        ("DRAWN", escape(author or "Autevra")),
        ("SHEET", "A3 1/1 · mm"),
    ]
    out = [f'<rect class="tb" x="{x}" y="{y}" width="180" height="{TITLE_H}"/>']
    cw, rh = 90.0, TITLE_H / 4
    for i, (key, value) in enumerate(rows):
        cx, cy = x + (i % 2) * cw, y + (i // 2) * rh
        out.append(
            f'<rect class="tb" x="{cx}" y="{cy}" width="{cw}" height="{rh}"/>'
            f'<text class="tbt" x="{cx + 2}" y="{cy + 3.4}">{key}</text>'
            f'<text class="tbv" x="{cx + 24}" y="{cy + 6.6}">{value}</text>'
        )
    return "".join(out)
