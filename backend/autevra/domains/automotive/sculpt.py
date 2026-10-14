"""Sculpted lower body: one smooth freeform surface lofted through cross-sections along the
car (vehicle frame, mm, ISO 8855).

The same generator makes every body style. Guide curves set each section: the style's side
profile gives the bottom and top of the section at each station, the plan view narrows the
nose and the tail, and the waist between the wheels is pulled in so the body is fullest
over the wheels (haunches). Each section is a superellipse-like loop with a tucked sill and
a waist easing in towards the beltline; the loft through the sections is a B-spline surface
(smooth, no facets). Shape controls (``haunch``, ``nose_taper``, ``tail_taper``,
``sill_tuck``, ``body_roundness``) are design parameters, so any style can be pushed towards
any other. The section at the widest station reaches the full body width, so the design
extents are kept exactly.
"""

import math
from collections.abc import Mapping, Sequence

import cadquery as cq

from autevra.cad import kernel as k

Inputs = Mapping[str, float]

# Stations along the body, as a share of its length from the rear: dense at the ends for a
# rounded nose and tail.
STATIONS = (0.0, 0.012, 0.04, 0.09, 0.17, 0.3, 0.42, 0.5, 0.58, 0.7, 0.83, 0.91, 0.96,
            0.988, 1.0)  # fmt: skip
POINTS = 32  # points per section loop
END_ZONE = 0.07  # share of the length over which the plan rounds into the nose or tail


def envelope(profile: Sequence[tuple[float, float]], x: float) -> tuple[float, float]:
    """Lowest and highest z of a closed (x, z) profile on the vertical line at x."""
    zs: list[float] = []
    n = len(profile)
    for i in range(n):
        (x0, z0), (x1, z1) = profile[i], profile[(i + 1) % n]
        if abs(x1 - x0) < 1e-9:
            if abs(x - x0) < 1e-6:
                zs += [z0, z1]
            continue
        if min(x0, x1) - 1e-6 <= x <= max(x0, x1) + 1e-6:
            t = (x - x0) / (x1 - x0)
            zs.append(z0 + t * (z1 - z0))
    return min(zs), max(zs)


def section_points(x: float, z_bottom: float, z_top: float, half_w: float, sill: float,
                   waist: float, roundness: float) -> list[tuple[float, float, float]]:  # fmt: skip
    """Closed superellipse loop of POINTS points, starting at the bottom centre: full width
    at the shoulder (45% up), the sill tucked in by ``sill`` and the top eased in by
    ``waist``. ``roundness`` 0 is nearly boxy (exponent 10), 1 is elliptical (exponent 2)."""
    q = 2.0 / (10.0 - 8.0 * roundness)  # superellipse |y|^n + |z|^n = 1, q = 2 / n
    shoulder = z_bottom + 0.45 * (z_top - z_bottom)
    pts = []
    for i in range(POINTS):
        t = 2.0 * math.pi * i / POINTS - math.pi / 2.0
        c, s = math.cos(t), math.sin(t)
        y = math.copysign(abs(c) ** q, c)
        if s < 0.0:  # lower half, with the sill tucked in
            z = shoulder - abs(s) ** q * (shoulder - z_bottom)
            w = half_w - sill * s * s
        else:  # upper half, easing in towards the top
            z = shoulder + abs(s) ** q * (z_top - shoulder)
            w = half_w - waist * s * s
        pts.append((x, y * w, z))
    return pts


def _section(points: list[tuple[float, float, float]]) -> cq.Wire:
    edge = cq.Edge.makeSpline([cq.Vector(*q) for q in points], periodic=True)
    return cq.Wire.assembleEdges([edge])


def smooth_profile(profile: Sequence[tuple[float, float]], rounds: int = 3,
                   keep: float = 1e-6) -> list[tuple[float, float]]:  # fmt: skip
    """Corner-cut (Chaikin) the closed side profile into a smooth silhouette. Each pass
    replaces every edge by points at 1/4 and 3/4 along it, so an edge lying on an extreme
    (the vertical front and rear faces, the flat floor, the beltline) stays on it and the
    extents are kept."""
    pts = list(profile)
    for _ in range(rounds):
        out = []
        n = len(pts)
        for i in range(n):
            (x0, z0), (x1, z1) = pts[i], pts[(i + 1) % n]
            if abs(x1 - x0) < keep and abs(z1 - z0) < keep:
                continue
            out.append((0.75 * x0 + 0.25 * x1, 0.75 * z0 + 0.25 * z1))
            out.append((0.25 * x0 + 0.75 * x1, 0.25 * z0 + 0.75 * z1))
        pts = out
    return pts


ARCH_ZONE = 500.0  # the body keeps its full width this far either side of each axle, mm


def width_at(p: Inputs, x: float, x_range: tuple[float, float]) -> float:
    """Plan half width at x: full width around each wheel arch (so the widest points are
    not lost to the wheel wells), narrowing over each overhang into the nose and the tail,
    and pulled in by ``haunch`` between the arches (the waist between the haunches)."""
    rear, front = x_range
    half_w = p["body_width"] / 2.0
    wb, a = p["wheelbase"], ARCH_ZONE
    nose, tail = p.get("nose_taper", 72.0) / 100.0, p.get("tail_taper", 82.0) / 100.0
    # Overhangs: a curve that is gentle next to the arch and quick at the very end (a
    # boat-shaped plan view).
    share = 1.0
    if x > a:
        t = min(1.0, (x - a) / max(front - a, 1.0))
        share = 1.0 - (1.0 - nose) * (0.35 * t**2 + 0.65 * t**8)
    elif x < -wb - a:
        t = min(1.0, (-wb - a - x) / max(-wb - a - rear, 1.0))
        share = 1.0 - (1.0 - tail) * (0.35 * t**2 + 0.65 * t**8)
    # Waist between the arches.
    span = wb - 2.0 * a
    between = 0.0
    if span > 0.0 and -wb + a < x < -a:
        between = math.sin(math.pi * (-a - x) / span)
    return half_w * share - p.get("haunch", 30.0) * between


PLAN_POINTS = 48  # points along each side of a plan outline


def plan_points(p: Inputs, x_range: tuple[float, float], z: float,
                inset: float) -> list[tuple[float, float, float]]:  # fmt: skip
    """Closed plan outline at height z: the plan law (boat-shaped, haunches over the wheels)
    moved in by ``inset``, as a dense polygon (ruled lofts between polygons stay planar
    or bilinear, which keeps the later booleans fast; the viewer shades across the facets).
    Points are denser at the ends and fall on the ends of the full-width arch zones."""
    rear, front = x_range
    n = PLAN_POINTS // 2
    xs = {rear + (0.5 - 0.5 * math.cos(math.pi * i / n)) * (front - rear) for i in range(n + 1)}
    wb, a = p["wheelbase"], ARCH_ZONE
    for xa in (a, -a, -wb + a, -wb - a):  # the ends of the full-width zones
        if rear < xa < front:
            xs = {x for x in xs if abs(x - xa) > 60.0} | {xa}
    inner = sorted(x for x in xs if rear < x < front)
    left = [(x, width_at(p, x, x_range) - inset, z) for x in inner]
    right = [(x, -y, z) for x, y, _ in reversed(left)]
    return [(rear, 0.0, z), *left, (front, 0.0, z), *right]


def lower_body(p: Inputs, profile: Sequence[tuple[float, float]]) -> k.Shape:
    """Lower body: the style's side profile (extruded across) intersected with a ruled loft
    through smooth plan curves at the sill, shoulder, waist and beltline, so the plan is
    boat-shaped with haunches and the section tucks in at the sill and eases in towards the
    beltline, with crisp character lines between."""
    xs = [x for x, _ in profile]
    rear, front = min(xs), max(xs)
    floor = min(z for _, z in profile)
    belt = max(z for _, z in profile)
    depth = belt - floor
    roundness = p.get("body_roundness", 45.0) / 100.0
    sill = p.get("sill_tuck", 60.0)
    pad = 2.0  # the plan curves reach just past the ends; the side trim sets the extents
    levels = (
        (floor - 1.0, sill),
        (floor + (0.25 + 0.1 * roundness) * depth, 0.25 * sill * roundness),
        (floor + 0.55 * depth, 0.0),  # shoulder: full width
        (floor + 0.85 * depth, 10.0 + 20.0 * roundness),
        (belt + 1.0, 25.0 + 20.0 * roundness),  # waist eases in towards the beltline
    )
    sections = [plan_points(p, (rear - pad, front + pad), z, inset) for z, inset in levels]
    loft = k.ruled_loft(sections)
    half_w = p["body_width"] / 2.0
    return k.intersect(k.prism_y(profile, (-half_w, half_w)), loft)


def fenders(p: Inputs, profile: Sequence[tuple[float, float]]) -> list[k.Shape]:
    """Raised wings over each wheel arch when the bonnet drops below the arch line
    (``fender_rise`` > 0): a hump in side view, from the body side in to the fender width,
    following the plan outline. Where the body is already higher (the cabin, a tall deck)
    the hump stays inside it and changes nothing."""
    rise = p.get("fender_rise", 0.0)
    if rise <= 0.0:
        return []
    xs = [x for x, _ in profile]
    rear, front = min(xs), max(xs)
    floor = min(z for _, z in profile)
    top = p["tyre_radius"] + p["arch_radius"] + 40.0  # the arch clearance line
    half_w = p["body_width"] / 2.0
    reach = p["arch_radius"] + 220.0  # wing length either side of the axle
    width = min(0.32 * half_w, 320.0)  # wing width in from the body side
    base = floor + 0.3 * (top - floor)
    outline = plan_points(p, (rear - 2.0, front + 2.0), 0.0, 0.0)
    plan = k.prism_z([(x, y) for x, y, _ in outline], (floor - 1.0, top + 1.0))
    out = []
    for xa in (0.0, -p["wheelbase"]):
        x0, x1 = max(xa - reach, rear), min(xa + reach, front)
        if x1 - x0 < 200.0:
            continue
        hump = []
        for i in range(17):
            u = i / 16
            x = x0 + u * (x1 - x0)
            lift = (0.5 - 0.5 * math.cos(2.0 * math.pi * u)) ** 0.45  # a broad, rounded crest
            hump.append((x, base + (top - base) * lift))
        hump = [(x0, base), *hump[1:-1], (x1, base)]
        for s in (1.0, -1.0):
            y = (half_w - width, half_w + 1.0) if s > 0 else (-half_w - 1.0, -half_w + width)
            out.append(k.intersect(k.prism_y(hump, y), plan))
    return out
