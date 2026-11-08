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

import functools
import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

import cadquery as cq

from autevra.cad import kernel as k
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import sculpt

Inputs = Mapping[str, float]
SURFACES = ("styled", "draft")
STATIONS = 40  # sections along the car
SECTION_POINTS = 40  # points round each section (the skin is faceted between them)
STEP = 100.0  # guide-curve sampling step, mm
GLASS_INSET = 8.0  # the glazing sits this far inside the skin, mm


LOW_MEMORY = 1 << 30  # bytes: below this the styled surface is off in "auto" mode


def _memory_limit() -> int | None:
    """The container's memory limit in bytes (cgroup v2 or v1), or None when unlimited."""
    for path in ("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        try:
            text = Path(path).read_text().strip()
        except OSError:
            continue
        if text.isdigit() and int(text) < 1 << 60:  # cgroup v1 reports "no limit" as huge
            return int(text)
        return None
    return None


@functools.cache
def styled_allowed() -> bool:
    from autevra.config import Settings

    mode = Settings().styled_surface.strip().lower()
    if mode in ("on", "off"):
        return mode == "on"
    limit = _memory_limit()
    return limit is None or limit >= LOW_MEMORY


def surface(p: Inputs) -> str:
    if not styled_allowed():
        return "draft"
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
    if has_cabin and not layout.open and rear < (r0 + r1) / 2.0 < front:
        xs = sorted({*xs, (r0 + r1) / 2.0})  # sample the crown of the roof arc itself
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
    # Raised wings: outside the cabin the wing crowns stay on the top line and the bonnet
    # (and an open car's deck) sinks between them, so the wings read as ridges over the
    # wheels. Capped on shallow sections near the nose and the tail.
    # The bonnet still clears the engine allowance (its top is 420 mm over the wheel
    # centre, see ``powertrain.build_engine``) by 25 mm.
    engine_top = p.get("tyre_radius", 330.0) + 420.0 + 25.0
    dip = min(0.8 * p.get("fender_rise", 0.0), 0.3 * (zt - zb), max(zt - engine_top, 0.0))
    dip *= 1.0 - cw
    # On the bonnet (ahead of the windscreen base) a power dome rises from the valley floor
    # between two creases; the deck of an open car stays a plain valley.
    cowl = b.body_layout(p).glass[1]
    dome = min(max(p.get("bonnet_dome", 0.0), 0.0), 100.0) / 100.0
    bulge = dome * dip * _smoothstep(cowl, cowl + 350.0, x) * (1.0 - _smoothstep(
        g.front - 450.0, g.front - 120.0, x))  # fmt: skip
    # Body roundness softens the sill and the shoulder (the widest point stays put, so the
    # extents never change): 0 = crisp, 1 = full.
    rnd = min(max(p.get("body_roundness", 45.0) / 100.0, 0.0), 1.0)
    # The wings also swell up over each wheel (the front more than the rear haunch), by up
    # to half the fender rise, outside the cabin.
    reach = 1.1 * p.get("arch_radius", 380.0)
    swell = sum(share * math.exp(-(((x - xa) / reach) ** 2))
                for xa, share in ((0.0, 1.0), (-p["wheelbase"], 0.7)))  # fmt: skip
    lift = 0.5 * p.get("fender_rise", 0.0) * swell * (1.0 - cw)
    # Wing crease: from the head lamp along the wing and the doors into the rear haunch the
    # widest point rises into a sharp line (climbing gently towards the haunch) and the
    # flank below it is drawn in, so the line catches the light; the width stays the same.
    wb = p["wheelbase"]
    crease = min(max(p.get("wing_crease", 0.0), 0.0), 100.0) / 100.0
    crease *= _smoothstep(-wb + 150.0, -wb + 750.0, x) * (1.0 - _smoothstep(
        g.front - 380.0, g.front - 120.0, x))  # fmt: skip
    rise = 0.3 + 0.3 * _smoothstep(g.front - 400.0, -wb + 600.0, x)  # up towards the haunch
    z_line = zs + 30.0 + crease * rise * max(zbelt - zs - 30.0, 0.0)
    half = [
        (0.0, zb), ((0.7 - 0.3 * rnd) * w_bot, zb), (w_bot, zb + 10.0 + 50.0 * rnd),
        ((0.998 - 0.03 * rnd - 0.035 * crease) * w, zs - 40.0 + 0.5 * crease * (z_line - zs)),
        (w, z_line), ((0.99 - 0.035 * rnd) * w, max(zbelt, z_line + 20.0)),
        (wtop + (0.975 * w - wtop) * 0.45, zbelt + 0.55 * (zt - zbelt) + 0.3 * lift),
        (wtop, zt - 0.12 * (zt - zbelt) - 8.0 + 0.8 * lift),
        (0.6 * wtop, zt - 4.0 - 0.1 * dip + lift),  # the wing crown
        (0.32 * wtop, zt - 2.0 - 0.85 * dip),  # into the bonnet valley: a crease
        (0.16 * wtop, zt - dip + 0.9 * bulge), (0.0, zt - dip + bulge),  # the power dome
    ]  # fmt: skip
    # A shallow section (near the tail or the nose) must not fold back on itself: keep the
    # points rising from the sill to the wing crown and the widths positive; the valley
    # may then fall to the centre line.
    crown = len(half) - 4
    fixed = [half[0], half[1]]
    for i, (y, z) in enumerate(half[2:], start=2):
        if i > crown and dip > 0.0:
            fixed.append((y, min(z, fixed[crown][1])))
            continue
        step = 4.0 if i <= crown else 0.0  # past the crown: no overshoot above the roof
        fixed.append((max(y, 1.0), max(z, fixed[-1][1] + step)))
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
    # A station at the highest point of the silhouette, so the facets reach the overall
    # height exactly (the nearest station moves there; the end stations stay put).
    fine = [rear + (front - rear) * i / 400 for i in range(401)]
    peak = max(fine, key=g.top)
    near = min(range(3, STATIONS - 3), key=lambda i: abs(xs[i] - peak))
    xs[near] = peak
    if inset:
        xs = [rear + inset] + xs[1:-1] + [front - inset]
    # Round the nose and tail over three sections on each end; a full front face keeps the
    # nose sections nearly whole, so the front stands as a broad fascia.
    ends = {0: (0.45, 0.55), 1: (0.82, 0.85), 2: (0.95, 0.96)}
    face = min(max(p.get("front_face", 0.0), 0.0), 100.0) / 100.0
    full = {0: (0.86, 0.9), 1: (0.97, 0.98), 2: (0.995, 0.997)}
    nose_ends = {i: (a + face * (fa - a), b_ + face * (fb - b_))
                 for i, ((a, b_), (fa, fb)) in enumerate(zip(ends.values(), full.values()))}  # fmt: skip
    wires = []
    for i, x in enumerate(xs):
        loop = section_points(p, g, x, inset)
        end = nose_ends.get(STATIONS - 1 - i) if i > STATIONS // 2 else ends.get(i)
        if end is not None:
            sy, sz = end
            zc = sum(z for _, z in loop) / len(loop)
            loop = [(y * sy, zc + (z - zc) * sz) for y, z in loop]
        # The spline through the section points can dip a little below the sill or rise
        # above the crown between them: keep it inside the section's own height.
        # and the samples can miss the widest point: scale them back to the section's width.
        lo, hi = min(z for _, z in loop), max(z for _, z in loop)
        dense = _resample(loop, SECTION_POINTS)
        wy = max(abs(y) for y, _ in loop) / max(max(abs(y) for y, _ in dense), 1e-9)
        wires.append([(x, y * wy, min(max(z, lo), hi)) for y, z in dense])
    # Planar and bilinear facets between dense sections: robust, fast booleans (B-spline
    # skins made the kernel's booleans fail on several styles); the viewer shades across
    # the facets, so the surface reads as smooth.
    return _outward(k.ruled_loft(wires))


def _resample(loop: list[tuple[float, float]], n: int) -> list[tuple[float, float]]:
    """n points on the closed Catmull-Rom curve through the loop, evenly spaced in the
    curve parameter (the same count at every station, as a ruled loft needs)."""
    m = len(loop)
    out = []
    for j in range(n):
        t = j * m / n
        i, u = int(t), t - int(t)
        p0, p1, p2, p3 = (loop[(i - 1) % m], loop[i % m], loop[(i + 1) % m], loop[(i + 2) % m])
        u2, u3 = u * u, u * u * u

        def cr(c: int, p0=p0, p1=p1, p2=p2, p3=p3, u=u, u2=u2, u3=u3) -> float:  # noqa: ANN001
            a2 = 2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]
            a3 = -p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]
            return 0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * u + a2 * u2 + a3 * u3)

        out.append((cr(0), cr(1)))
    return out  # type: ignore[return-value]


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
    # Windscreen and rear screen. The rear screen stops short of the greenhouse base so a
    # rim of skin stays at the tail (on two-box bodies the base is at the very back).
    for x in ((r1 - 1.0, g1 + 10.0), (g0 + 60.0, r0 + 1.0)):
        if x[1] - x[0] > 1.0 and roof_w - pillar > 50.0:
            tools.append(k.box(x, (-roof_w + pillar, roof_w - pillar), z))
    return tools


def head_outlines(p: Inputs, layout: b.BodyLayout) -> list[tuple[float, list[tuple[float, float]]]]:
    """(side, (y, z) outline) of each head lamp: the swept lamps' own slanted outline, else
    the bounding rectangle of that side's lamp units."""
    from autevra.domains.automotive import styling

    if styling.head_lamp_style(p) == "swept":
        return [(s, styling.swept_outline(p, layout, s)) for s in (1.0, -1.0)]
    out = []
    for s in (1.0, -1.0):
        boxes = [k.bounds(x) for x in styling.lamp_solids(p, "head", layout)]
        boxes = [bx for bx in boxes if s * bx[0][1] > 1.0]
        if boxes:
            y0, y1 = min(bx[0][1] for bx in boxes), max(bx[1][1] for bx in boxes)
            z0, z1 = min(bx[0][2] for bx in boxes), max(bx[1][2] for bx in boxes)
            out.append((s, [(y0, z0), (y1, z0), (y1, z1), (y0, z1)]))
    return out


def _head_x(p: Inputs, layout: b.BodyLayout) -> tuple[float, float]:
    face = p["front_overhang"]
    depth = 90.0 + max(face - layout.profile[3][0], 0.0)  # a raked face sets the lamps back
    return (face - depth, face + 60.0)


def housing_tools(p: Inputs, layout: b.BodyLayout) -> list[k.Shape]:
    """Cutters for the smoked head lamp housings (empty without them)."""
    from autevra.domains.automotive import styling

    if styling.lamp_housing(p) == "none":
        return []
    xr = _head_x(p, layout)
    return [k.prism_x(styling.housing_outline(p, layout, s, o), xr)
            for s, o in head_outlines(p, layout)]  # fmt: skip


def build_lamp_housings(p: Inputs) -> k.Shape | None:
    """The dark eye of each smoked head lamp: the skin inside the housing outline, round
    the lamp lens."""
    if not styled_ok(p):
        return None
    layout = b.body_layout(p)
    tools = housing_tools(p, layout)
    if not tools:
        return None
    eye = k.intersect(skin(p, layout), k.fuse(*tools) if len(tools) > 1 else tools[0])
    lenses = lamp_tools(p, layout, "head")
    eye = k.cut(eye, *lenses)
    return eye if k.solid_count(eye) else None


def lamp_tools(p: Inputs, layout: b.BodyLayout, end: str) -> list[k.Shape]:
    """Deep cutters behind the lamps' face outline (one envelope per side of the car, so
    the booleans on the skin stay few): cut from the skin they leave lamp lenses that
    follow its curvature."""
    from autevra.domains.automotive import styling

    sign = 1.0 if end == "head" else -1.0
    face = p["front_overhang"] if end == "head" else -(p["wheelbase"] + p["rear_overhang"])
    depth = 90.0 if end == "head" else 70.0
    if end == "head":  # a raked face sets the lamps back: reach behind its leading edge
        depth += max(face - layout.profile[3][0], 0.0)
    xr = tuple(sorted((face + sign * 60.0, face - sign * depth)))
    round_head = end == "head" and styling.head_lamp_style(p) == "round"
    if end == "head" and styling.head_lamp_style(p) == "swept":  # slanted: their own outline
        return [k.prism_x(styling.swept_outline(p, layout, s), xr) for s in (1.0, -1.0)]
    if end == "tail" and styling.tail_lamp_style(p) == "swept":
        return [k.prism_x(styling.tail_swept_outline(p, layout, s), xr) for s in (1.0, -1.0)]
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
    lamps = [
        *lamp_tools(p, layout, "head"),
        *lamp_tools(p, layout, "tail"),
        *housing_tools(p, layout),
    ]
    cabin = k.box(*interior.cavity(p))
    opening = exterior.roof_opening(p, layout)
    roof = [k.box(*opening)] if opening is not None else []
    from autevra.domains.automotive import details

    trims = [
        *details.grille_tools(p, layout),
        *details.vent_tools(p),
        *details.door_tools(p, layout),
    ]
    body = k.cut(body, *wells, *lamps, cabin, *window_tools(p, layout, g), *roof, *trims)
    if layout.open:  # windscreen surround of an open car, on a strip at the cowl
        (_, g1) = layout.glass
        roof_w = b.roof_half_width(p)
        strip = k.box((g1 - 60.0, g1 + 10.0), (-roof_w, roof_w), (belt - 300.0, belt + 5.0))
        body = k.fuse(body, b._window_frame(p, layout), strip)
    return _main_solids(body)


def _main_solids(shape: k.Shape) -> k.Shape:
    """Drop slivers (under 0.1 % of the body's volume) that the cuts can leave between
    neighbouring openings."""
    solids = shape.Solids()
    if len(solids) <= 1:
        return shape
    volumes = [k.volume(s_) for s_ in solids]
    keep = [s_ for s_, v in zip(solids, volumes, strict=True) if v >= 1e-3 * max(volumes)]
    return keep[0] if len(keep) == 1 else cq.Compound.makeCompound(keep)


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
    from autevra.domains.automotive import exterior

    opening = exterior.roof_opening(p, layout)
    if opening is not None:  # a flush roof pane, cut from the skin like the opening
        roof = k.intersect(skin(p, layout), k.box(*opening))
        pieces = [*panes.Solids(), *roof.Solids()]
        panes = cq.Compound.makeCompound(pieces) if pieces else panes
    return panes if k.solid_count(panes) else None


def build_styled_lamps(p: Inputs, end: str) -> k.Shape | None:
    layout = b.body_layout(p)
    tools = lamp_tools(p, layout, end)
    if not tools:
        return None
    outer = skin(p, layout)
    if layout.cargo is not None and end == "tail":  # the tail lamps sit on the cargo box
        half_w = p["body_width"] / 2.0
        outer = k.box(layout.cargo, (-half_w, half_w), (p["body_floor"], p["overall_height"]))
    lenses = k.intersect(outer, k.fuse(*tools) if len(tools) > 1 else tools[0])
    return lenses if k.solid_count(lenses) else None


# --- Robustness: fall back to the draft surface when the kernel cannot build the skin ----

_TRIED: dict[tuple, k.Shape | None] = {}  # styled body by inputs (None: not buildable)


def try_body(p: Inputs) -> k.Shape | None:
    """The styled body, or None when the kernel cannot build it for these inputs (the
    body, glazing and lamps then all use the draft surface, so they always match)."""
    key = tuple(sorted(p.items()))
    if key not in _TRIED:
        try:
            shape = build_styled_body(p)
            # One valid solid or nothing: a body in pieces (unusual style mixes) is not
            # worth showing, the draft surface always builds as one.
            ok = k.is_valid(shape) and k.solid_count(shape) == 1
            _TRIED[key] = shape if ok else None
        except Exception:  # the kernel raises many types; draft is the safe answer
            _TRIED[key] = None
        while len(_TRIED) > 32:
            _TRIED.pop(next(iter(_TRIED)))
    return _TRIED[key]


def styled_ok(p: Inputs) -> bool:
    return surface(p) == "styled" and try_body(p) is not None
