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


def _frame(look: tuple[float, float, float], up: tuple[float, float, float]
           ) -> tuple[gp_Ax2, tuple[float, ...], tuple[float, ...]]:  # fmt: skip
    """The projector frame: its Z axis points back at the viewer, its X axis is the
    sheet's right; returns it with the sheet's right and up vectors in part space."""
    back = tuple(-c for c in look)
    n = math.sqrt(sum(c * c for c in back))
    back = tuple(c / n for c in back)
    dot = sum(a * b for a, b in zip(up, back, strict=True))
    upv = tuple(u - dot * b for u, b in zip(up, back, strict=True))
    m = math.sqrt(sum(c * c for c in upv))
    upv = tuple(c / m for c in upv)
    right = (upv[1] * back[2] - upv[2] * back[1], upv[2] * back[0] - upv[0] * back[2],
             upv[0] * back[1] - upv[1] * back[0])  # fmt: skip
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
        out.append([(sampler.Value(i).X(), sampler.Value(i).Y())
                    for i in range(1, sampler.NbPoints() + 1)])  # fmt: skip
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
            if not any(abs(u - a) < 1e-3 and abs(v - b) < 1e-3 and abs(circle.Radius() - r) < 1e-3
                       for a, b, r in view.holes):  # fmt: skip
                view.holes.append((u, v, circle.Radius()))
    return view


def _fmt(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _scale_label(s: float) -> str:
    return f"{_fmt(s)}:1" if s >= 1 else f"1:{_fmt(1 / s)}"


def drawing_svg(shape: k.Shape, title: str, author: str = "") -> str:
    views = {name: project(shape, name) for name in VIEWS}
    (x0, y0, z0), (x1, y1, z1) = k.bounds(shape)
    size = {"front": (x1 - x0, z1 - z0), "top": (x1 - x0, y1 - y0), "right": (y1 - y0, z1 - z0)}
    iso_b = views["iso"].bounds()
    iso = (iso_b[2] - iso_b[0], iso_b[3] - iso_b[1])
    gap = 26.0  # room for the dimensions between views
    area_w = SHEET[0] - 2 * MARGIN - 2 * gap
    area_h = SHEET[1] - 2 * MARGIN - TITLE_H - 2 * gap
    scale = next((s for s in SCALES
                  if s * (size["front"][0] + size["right"][0] + iso[0] * 0.8) <= area_w
                  and s * (size["front"][1] + size["top"][1]) <= area_h), SCALES[-1])  # fmt: skip
    # third-angle layout: top above front, right to the right of front, iso top right
    left = MARGIN + gap
    bottom = SHEET[1] - MARGIN - TITLE_H - gap
    places = {
        "front": (left, bottom - scale * size["front"][1]),
        "top": (left, bottom - scale * size["front"][1] - gap - scale * size["top"][1]),
        "right": (left + scale * size["front"][0] + gap, bottom - scale * size["front"][1]),
    }
    places["iso"] = (places["right"][0] + scale * size["right"][0] + gap,
                     MARGIN + gap)  # fmt: skip

    parts: list[str] = []

    def path(line: Polyline, origin: tuple[float, float], b: tuple[float, ...], cls: str) -> str:
        ox, oy = origin
        pts = " ".join(f"{ox + scale * (u - b[0]):.2f},{oy + scale * (b[3] - v):.2f}"
                       for u, v in line)  # fmt: skip
        return f'<polyline class="{cls}" points="{pts}"/>'

    for name, view in views.items():
        b = view.bounds()
        o = places[name]
        parts += [path(line, o, b, "hid") for line in view.hidden]
        parts += [path(line, o, b, "vis") for line in view.visible]
        w, h = scale * (b[2] - b[0]), scale * (b[3] - b[1])
        label = {"front": "FRONT", "top": "TOP", "right": "RIGHT", "iso": "ISOMETRIC"}[name]
        parts.append(
            f'<text class="lbl" x="{o[0] + w / 2:.1f}" y="{o[1] + h + 18:.1f}">{label}</text>'
        )
        if name == "iso":
            continue
        parts.append(_dimension(o[0], o[1] + h + 7, o[0] + w, o[1] + h + 7, b[2] - b[0], "h"))
        parts.append(_dimension(o[0] - 7, o[1], o[0] - 7, o[1] + h, b[3] - b[1], "v"))
        for u, v, r in view.holes:
            cx, cy = o[0] + scale * (u - b[0]), o[1] + scale * (b[3] - v)
            parts.append(f'<line class="ctr" x1="{cx - scale * r - 3:.2f}" y1="{cy:.2f}" '
                         f'x2="{cx + scale * r + 3:.2f}" y2="{cy:.2f}"/>'
                         f'<line class="ctr" x1="{cx:.2f}" y1="{cy - scale * r - 3:.2f}" '
                         f'x2="{cx:.2f}" y2="{cy + scale * r + 3:.2f}"/>')  # fmt: skip
            tx, ty = cx + scale * r * 0.7 + 4, cy - scale * r * 0.7 - 4
            parts.append(f'<line class="dim" x1="{cx + scale * r * 0.7:.2f}" '
                         f'y1="{cy - scale * r * 0.7:.2f}" x2="{tx:.2f}" y2="{ty:.2f}"/>'
                         f'<text class="dimt" x="{tx + 1:.2f}" y="{ty - 1:.2f}" '
                         f'text-anchor="start">Ø{_fmt(2 * r)}</text>')  # fmt: skip
    parts.append(_title_block(title, scale, author, shape))
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
        ".tb{fill:none;stroke:#111;stroke-width:0.35}.tbt{font-size:3px}.tbv{font-size:4.2px}"
        "</style>"
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>'
        f'<rect class="tb" x="{MARGIN}" y="{MARGIN}" width="{w - 2 * MARGIN}" '
        f'height="{h - 2 * MARGIN}"/>' + "".join(parts) + "</svg>"
    )


def _line(x1: float, y1: float, x2: float, y2: float, cls: str = "dim") -> str:
    return f'<line class="{cls}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>'


def _dimension(xa: float, ya: float, xb: float, yb: float, value: float, kind: str) -> str:
    """A dimension line with arrowheads and extension lines (sheet coordinates, mm)."""
    a = 1.6  # arrowhead length
    if kind == "h":
        ext = _line(xa, ya - 5, xa, ya + 1) + _line(xb, yb - 5, xb, yb + 1)
        heads = (f'<path class="dim" d="M{xa + a:.2f},{ya - 0.5:.2f} L{xa:.2f},{ya:.2f} '
                 f'L{xa + a:.2f},{ya + 0.5:.2f} M{xb - a:.2f},{yb - 0.5:.2f} L{xb:.2f},{yb:.2f} '
                 f'L{xb - a:.2f},{yb + 0.5:.2f}"/>')  # fmt: skip
        text = f'<text class="dimt" x="{(xa + xb) / 2:.2f}" y="{ya - 1:.2f}">{_fmt(value)}</text>'
    else:
        ext = _line(xa - 1, ya, xa + 5, ya) + _line(xb - 1, yb, xb + 5, yb)
        heads = (f'<path class="dim" d="M{xa - 0.5:.2f},{ya + a:.2f} L{xa:.2f},{ya:.2f} '
                 f'L{xa + 0.5:.2f},{ya + a:.2f} M{xb - 0.5:.2f},{yb - a:.2f} L{xb:.2f},{yb:.2f} '
                 f'L{xb + 0.5:.2f},{yb - a:.2f}"/>')  # fmt: skip
        my = (ya + yb) / 2
        text = (f'<text class="dimt" x="{xa - 1:.2f}" y="{my:.2f}" '
                f'transform="rotate(-90 {xa - 1:.2f} {my:.2f})">{_fmt(value)}</text>')  # fmt: skip
    return ext + _line(xa, ya, xb, yb) + heads + text


def _title_block(title: str, scale: float, author: str, shape: k.Shape) -> str:
    w, h = SHEET
    x, y = w - MARGIN - 180.0, h - MARGIN - TITLE_H
    rows = [
        ("TITLE", escape(title)), ("SCALE", _scale_label(scale)),
        ("UNITS", "mm"), ("PROJECTION", "third angle"),
        ("VOLUME", f"{k.volume(shape) / 1000:.1f} cm³"),
        ("DATE", dt.date.today().isoformat()), ("DRAWN", escape(author or "Autevra")),
        ("SHEET", "A3 1/1"),
    ]  # fmt: skip
    out = [f'<rect class="tb" x="{x}" y="{y}" width="180" height="{TITLE_H}"/>']
    cw, rh = 90.0, TITLE_H / 4
    for i, (key, value) in enumerate(rows):
        cx, cy = x + (i % 2) * cw, y + (i // 2) * rh
        out.append(f'<rect class="tb" x="{cx}" y="{cy}" width="{cw}" height="{rh}"/>'
                   f'<text class="tbt" x="{cx + 2}" y="{cy + 3.4}">{key}</text>'
                   f'<text class="tbv" x="{cx + 24}" y="{cy + 6.6}">{value}</text>')  # fmt: skip
    return "".join(out)
