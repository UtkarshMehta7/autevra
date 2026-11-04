"""Styled body: the whole car as one smooth skin, lofted through cross-sections that follow
designer-style guide curves (vehicle frame, mm, ISO 8855).

Guide curves, all derived from the body style's layout and the shape controls:

- top line: the side silhouette (nose, bonnet, windscreen, roof arc, rear screen or
  fastback, tail) as one smoothed curve, scaled so the roof keeps the overall height;
- bottom line: the underbody, smoothed;
- plan: the half width along the car (``sculpt.width_at``: haunches, nose and tail taper);
- cabin weight: 0 over the bonnet and the deck, 1 under the roof, blending through the
  screens. It moves each section from a wide crowned bonnet (with a dip between the
  wings when ``fender_rise`` is set) to a narrow glasshouse drawn in by the tumblehome.

The skin is one B-spline loft (smooth, no facets). Window openings follow the roof line,
glazing is a thin shell inset from the skin, lamps are cut from the skin so they follow
its curvature, and the cabin and wheel wells are cut as in the draft body. The extents are
clipped to the design's, so length, width and height are exact.
"""

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass

import cadquery as cq

from autevra.cad import kernel as k
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import sculpt

Inputs = Mapping[str, float]
SURFACES = ("styled", "draft")
STATIONS = 34  # sections along the car
STEP = 100.0  # guide-curve sampling step, mm
GLASS_INSET = 8.0  # the glazing sits this far inside the skin, mm


def surface(p: Inputs) -> str:
    return SURFACES[min(max(int(round(p.get("surface_quality", 0))), 0), len(SURFACES) - 1)]


def _smoothstep(a: float, b_: float, x: float) -> float:
    if b_ == a:
        return 1.0 if x >= a else 0.0
    t = min(max((x - a) / (b_ - a), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def _pchip(xs: list[float], ys: list[float]) -> Callable[[float], float]:
    """Monotone cubic interpolation (Fritsch-Carlson): smooth, no overshoot."""
    n = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    delta = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = delta[0], delta[-1]
    for i in range(1, n - 1):
        if delta[i - 1] * delta[i] <= 0.0:
            m[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / delta[i - 1] + w2 / delta[i])

    def f(x: float) -> float:
        x = min(max(x, xs[0]), xs[-1])
        i = 0
        while i < n - 2 and x > xs[i + 1]:
            i += 1
        t = (x - xs[i]) / h[i]
        h00, h10 = 2 * t**3 - 3 * t**2 + 1, t**3 - 2 * t**2 + t
        h01, h11 = -2 * t**3 + 3 * t**2, t**3 - t**2
        return h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1]

    return f


def _smooth(values: list[float], passes: int = 2) -> list[float]:
    out = list(values)
    for _ in range(passes):
        out = [out[0]] + [0.25 * out[i - 1] + 0.5 * out[i] + 0.25 * out[i + 1]
                          for i in range(1, len(out) - 1)] + [out[-1]]  # fmt: skip
    return out


@dataclass(frozen=True)
class Guides:
    top: Callable[[float], float]
    bottom: Callable[[float], float]
    width: Callable[[float], float]
    cabin: Callable[[float], float]
    rear: float
    front: float
    roof_z: float


def guides(p: Inputs, layout: b.BodyLayout) -> Guides:
    profile = layout.profile
    xs_p = [x for x, _ in profile]
    rear, front = min(xs_p), max(xs_p)
    belt = p["beltline_height"]
    (g0, g1), (r0, r1) = layout.glass, layout.roof
    has_cabin = (
        not layout.open and layout.cargo is None or (layout.cargo is not None and g1 - g0 > 1.0)
    )
    roof_z = layout.roof_z
    arc = p.get("roof_arc", 40.0)

    def greenhouse(x: float) -> float:
        if not has_cabin or layout.open or x <= g0 or x >= g1:
            return -math.inf
        if x < r0:
            return belt + (roof_z - arc - belt) * (x - g0) / max(r0 - g0, 1.0)
        if x > r1:
            return belt + (roof_z - arc - belt) * (g1 - x) / max(g1 - r1, 1.0)
        mid = (r0 + r1) / 2.0
        half = max((r1 - r0) / 2.0, 1.0)
        return roof_z - arc * ((x - mid) / half) ** 2  # the roof arc

    count = max(int((front - rear) / STEP), 8)
    xs = [rear + (front - rear) * i / count for i in range(count + 1)]
    lows, tops = [], []
    for x in xs:
        z0, z1 = sculpt.envelope(profile, min(max(x, rear + 0.5), front - 0.5))
        lows.append(z0)
        tops.append(max(z1, greenhouse(x)))
    top_max = max(tops)
    tops = _smooth(tops)
    low_t, high_t = min(tops), max(tops)
    if high_t > low_t:  # keep the overall height exact after smoothing
        tops = [low_t + (t - low_t) * (top_max - low_t) / (high_t - low_t) for t in tops]
    lows = _smooth(lows)

    def cabin(x: float) -> float:
        if not has_cabin or layout.open:
            return 0.0
        return (1.0 - _smoothstep(r1, g1, x)) * _smoothstep(g0, r0, x)

    # Plan: the draft plan law sampled at its key stations and joined smoothly (the draft
    # law has kinks at the arch zones, which show as ripples in a smooth skin's highlights).
    wb, fo, ro = p["wheelbase"], p["front_overhang"], p["rear_overhang"]
    a = sculpt.ARCH_ZONE
    keys = sorted({rear, rear + 0.08 * ro, rear + 0.4 * ro, -wb - a, -wb, -wb / 2.0, 0.0,
                   min(a, 0.5 * fo), front - 0.4 * fo, front - 0.08 * fo, front})  # fmt: skip
    keys = [x for x in keys if rear <= x <= front]
    width = _pchip(keys, [sculpt.width_at(p, x, (rear, front)) for x in keys])
    from autevra.domains.automotive import styling_curves as sc

    top_f, bottom_f = _pchip(xs, tops), _pchip(xs, lows)
    if (pts := sc.from_inputs(p, "top")) is not None:
        top_f = _pchip([x for x, _ in pts], [z for _, z in pts])
    if (pts := sc.from_inputs(p, "bottom")) is not None:
        bottom_f = _pchip([x for x, _ in pts], [z for _, z in pts])
    if (pts := sc.from_inputs(p, "plan")) is not None:
        width = _pchip([x for x, _ in pts], [min(y, p["body_width"] / 2.0) for _, y in pts])
    return Guides(
        top=top_f, bottom=bottom_f, width=width, cabin=cabin,
        rear=rear, front=front, roof_z=top_max,
    )  # fmt: skip


def section_points(p: Inputs, g: Guides, x: float, inset: float = 0.0) -> list[tuple[float, float]]:
    """(y, z) loop of one section, from the bottom centre round the right side to the top
    and back down the left side (the same number of points at every station)."""
    zt, zb, w = g.top(x) - inset, g.bottom(x) + inset, g.width(x) - inset
    cw = g.cabin(x)
    belt = p["beltline_height"]
    zbelt = (1.0 - cw) * (zt - 0.12 * (zt - zb)) + cw * min(belt, zt - 60.0)
    zs = zb + 0.52 * (zbelt - zb)
    half_w = p["body_width"] / 2.0
    roof_w = max(b.roof_half_width(p) * w / half_w, 0.4 * w)
    wtop = (1.0 - cw) * 0.8 * w + cw * roof_w
    tuck = min(p.get("sill_tuck", 60.0), 0.3 * w)
    w_bot = w - tuck
    # Bonnet dip between raised wings (outside the cabin only).
    dip = 0.6 * p.get("fender_rise", 0.0) * (1.0 - cw)
    half = [
        (0.0, zb), (0.55 * w_bot, zb), (w_bot, zb + 30.0), (0.995 * w, zs - 40.0),
        (w, zs + 30.0), (0.975 * w, zbelt),
        (wtop + (0.975 * w - wtop) * 0.45, zbelt + 0.55 * (zt - zbelt)),
        (wtop, zt - 0.12 * (zt - zbelt) - 8.0), (0.55 * wtop, zt - 4.0 - 0.7 * dip),
        (0.0, zt - dip),
    ]  # fmt: skip
    # A shallow section (near the tail or the nose) must not fold back on itself: keep the
    # points rising from the sill to the roof and the widths positive.
    fixed = [half[0], half[1]]
    for y, z in half[2:]:
        fixed.append((max(y, 1.0) if z < half[-1][1] else y, max(z, fixed[-1][1] + 4.0)))
    half = fixed
    left = [(-y, z) for y, z in reversed(half[1:-1])]
    return half + left


def skin(p: Inputs, layout: b.BodyLayout, inset: float = 0.0) -> k.Shape:
    """The smooth skin (optionally inset by ``inset`` all round), not yet clipped."""
    g = guides(p, layout)
    rear, front = g.rear, g.front
    # Stations: denser towards the ends, but never closer than about 1 % of the length
    # (sections a few millimetres apart fold the surface and break later booleans).
    shares = [0.6 * i / (STATIONS - 1) + 0.4 * (0.5 - 0.5 * math.cos(math.pi * i / (STATIONS - 1)))
              for i in range(STATIONS)]  # fmt: skip
    xs = [rear + (front - rear) * u for u in shares]
    if inset:
        xs = [rear + inset] + xs[1:-1] + [front - inset]
    # Round the nose and tail over three sections on each end.
    ends = {0: (0.45, 0.55), 1: (0.82, 0.85), 2: (0.95, 0.96)}
    wires = []
    for i, x in enumerate(xs):
        loop = section_points(p, g, x, inset)
        end = ends.get(min(i, STATIONS - 1 - i))
        if end is not None:
            sy, sz = end
            zc = sum(z for _, z in loop) / len(loop)
            loop = [(y * sy, zc + (z - zc) * sz) for y, z in loop]
        pts = [cq.Vector(x, y, z) for y, z in loop]
        wires.append(cq.Wire.assembleEdges([cq.Edge.makeSpline(pts, periodic=True)]))
    return _outward(cq.Solid.makeLoft(wires, ruled=False))


def _outward(solid: k.Shape) -> k.Shape:
    """The loft can come out inside-out (its faces oriented inwards), which makes every
    later boolean return nothing: orient the closed skin so it encloses its volume."""
    from OCP.BRepLib import BRepLib
    from OCP.TopoDS import TopoDS

    occ = TopoDS.Solid_s(solid.wrapped)
    BRepLib.OrientClosedSolid_s(occ)
    return cq.Solid(occ)


def _clip(p: Inputs, g: Guides, shape: k.Shape) -> k.Shape:
    half_w = p["body_width"] / 2.0
    return k.intersect(shape, k.box((g.rear, g.front), (-half_w, half_w), (0.0, g.roof_z)))


def window_tools(p: Inputs, layout: b.BodyLayout, g: Guides) -> list[k.Shape]:
    """Openings for the side windows (following the roof line), windscreen and rear
    screen; the same shapes select the glass panes."""
    if layout.open or layout.glass[1] - layout.glass[0] < 1.0:
        return []
    (g0, g1), (r0, r1) = layout.glass, layout.roof
    belt, pillar = p["beltline_height"], b.PILLAR
    half_w = p["body_width"] / 2.0
    roof_w = b.roof_half_width(p)
    x0, x1 = r0 + pillar, r1 - pillar
    tools = []
    if x1 - x0 > 100.0:
        n = 4  # the roof arc is gentle: a few points keep the boolean cheap
        top = [
            (x0 + (x1 - x0) * i / n, g.top(x0 + (x1 - x0) * i / n) - pillar) for i in range(n + 1)
        ]
        outline = [(x0, belt + 0.6 * pillar), *top, (x1, belt + 0.6 * pillar)]
        tools.append(k.prism_y(outline, (-half_w - 10.0, half_w + 10.0)))
    z = (belt + 0.6 * pillar, g.roof_z - 0.5 * pillar)
    for x in ((r1 - 1.0, g1 + 10.0), (g0 - 10.0, r0 + 1.0)):  # windscreen, rear screen
        if x[1] - x[0] > 1.0 and roof_w - pillar > 50.0:
            tools.append(k.box(x, (-roof_w + pillar, roof_w - pillar), z))
    return tools


def lamp_tools(p: Inputs, layout: b.BodyLayout, end: str) -> list[k.Shape]:
    """Deep cutters behind the lamps' face outline (one envelope per side of the car, so
    the booleans on the skin stay few): cut from the skin they leave lamp lenses that
    follow its curvature."""
    from autevra.domains.automotive import styling

    sign = 1.0 if end == "head" else -1.0
    face = p["front_overhang"] if end == "head" else -(p["wheelbase"] + p["rear_overhang"])
    xr = tuple(sorted((face + sign * 60.0, face - sign * 90.0)))
    round_head = end == "head" and styling.head_lamp_style(p) == "round"
    groups: dict[str, list[tuple[float, float, float, float]]] = {}
    for solid in styling.lamp_solids(p, end, layout):
        (_, y0, z0), (_, y1, z1) = k.bounds(solid)
        side = "left" if y0 > 1.0 else "right" if y1 < -1.0 else "centre"
        groups.setdefault(side, []).append((y0, y1, z0, z1))
    out = []
    for boxes in groups.values():
        y0, y1 = min(bx[0] for bx in boxes), max(bx[1] for bx in boxes)
        z0, z1 = min(bx[2] for bx in boxes), max(bx[3] for bx in boxes)
        if round_head:
            out.append(k.cylinder_x((z1 - z0) / 2.0, xr, y=(y0 + y1) / 2.0, z=(z0 + z1) / 2.0))
        else:
            out.append(k.box(xr, (y0, y1), (z0, z1)))
    return out


def build_styled_body(p: Inputs) -> k.Shape:
    from autevra.domains.automotive import exterior, interior

    layout = b.body_layout(p)
    g = guides(p, layout)
    half_w = p["body_width"] / 2.0
    floor, belt = p["body_floor"], p["beltline_height"]
    body = _clip(p, g, skin(p, layout))
    extra = []
    if layout.open:  # windscreen surround of an open car
        extra.append(b._window_frame(p, layout))
    if layout.cargo is not None:
        extra.append(k.box(layout.cargo, (-half_w, half_w), (floor, p["overall_height"])))
    if extra:
        body = k.fuse(body, *extra)
    if layout.bed is not None:
        (b0, b1), bed_floor = layout.bed
        body = k.cut(
            body, k.box((b0, b1), (-half_w + 50.0, half_w - 50.0), (bed_floor, belt + 5.0))
        )
    wheel_z, r = p["tyre_radius"], p["arch_radius"]
    wells = []
    for x, track in ((0.0, p["track_front"]), (-p["wheelbase"], p["track_rear"])):
        inner = track / 2.0 - p["tyre_width"] / 2.0 - p["arch_clearance"]
        wells.append(k.cylinder_y(r, (inner, half_w + 1), x=x, z=wheel_z))
        wells.append(k.cylinder_y(r, (-half_w - 1, -inner), x=x, z=wheel_z))
    lamps = [*lamp_tools(p, layout, "head"), *lamp_tools(p, layout, "tail")]
    cabin = k.box(*interior.cavity(p))
    opening = exterior.roof_opening(p, layout)
    roof = [k.box(*opening)] if opening is not None else []
    return k.cut(body, *wells, *lamps, cabin, *window_tools(p, layout, g), *roof)


def build_styled_glass(p: Inputs) -> k.Shape | None:
    layout = b.body_layout(p)
    if layout.open:
        return b._open_top(p, layout, k.cut(
            b._greenhouse(p, layout, inset=GLASS_INSET),
            b._greenhouse(p, layout, inset=GLASS_INSET + 6.0)))  # fmt: skip
    g = guides(p, layout)
    tools = window_tools(p, layout, g)
    if not tools:
        return None
    # The skin, inset to sit just inside the openings, within the openings, hollowed by the
    # cabin's air space: the outer face follows the body exactly; the inner face is
    # simplified (a nested-skin boolean is not robust in the kernel).
    panes = k.intersect(
        skin(p, layout, GLASS_INSET), k.fuse(*tools) if len(tools) > 1 else tools[0]
    )
    (g0, g1) = layout.glass
    roof_w = b.roof_half_width(p)
    air = k.box((g0 + 40.0, g1 - 40.0), (-(roof_w - 20.0), roof_w - 20.0),
                (p["beltline_height"] + 0.6 * b.PILLAR - 1.0, g.roof_z - 20.0))  # fmt: skip
    panes = k.cut(panes, air)
    return panes if k.solid_count(panes) else None


def build_styled_lamps(p: Inputs, end: str) -> k.Shape | None:
    layout = b.body_layout(p)
    tools = lamp_tools(p, layout, end)
    if not tools:
        return None
    lenses = k.intersect(skin(p, layout), k.fuse(*tools) if len(tools) > 1 else tools[0])
    return lenses if k.solid_count(lenses) else None


# --- Robustness: fall back to the draft surface when the kernel cannot build the skin ----

_TRIED: dict[tuple, k.Shape | None] = {}  # styled body by inputs (None: not buildable)


def try_body(p: Inputs) -> k.Shape | None:
    """The styled body, or None when the kernel cannot build it for these inputs (the
    body, glazing and lamps then all use the draft surface, so they always match)."""
    key = tuple(sorted(p.items()))
    if key not in _TRIED:
        try:
            _TRIED[key] = build_styled_body(p)
        except Exception:  # the kernel raises many types; draft is the safe answer
            _TRIED[key] = None
        while len(_TRIED) > 32:
            _TRIED.pop(next(iter(_TRIED)))
    return _TRIED[key]


def styled_ok(p: Inputs) -> bool:
    return surface(p) == "styled" and try_body(p) is not None
