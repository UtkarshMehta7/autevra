"""Styling parts: rim designs and lamp signatures.

Rims are built in the wheel frame (origin at the wheel centre, spin axis along Y, outboard
face towards +Y). Lamps are built in the vehicle frame on the flat part of the front and
rear faces; the body is recessed by the same solids, so the lamps sit flush and the body
extents do not change. The shapes are representative styling envelopes, not lamp optics
(no photometry) or wheel structures (no strength or mass analysis beyond their volume).
"""

import math
from collections.abc import Mapping

from autevra.cad import kernel as k
from autevra.domains.automotive.derived import AXLE_RADIUS

Inputs = Mapping[str, float]

RIM_BARREL = 12.0  # radial thickness of the rim barrel, mm
FACE_THICKNESS = 18.0  # mm
FACE_SET = 15.0  # dish: the face sits this far inboard of the rim's outer edge, mm
WHEEL_DESIGNS = ("five_spoke", "multi_spoke", "twin_spoke", "mesh", "aero", "steel")
HEAD_LAMP_STYLES = ("strip", "matrix", "round", "split")
TAIL_LAMP_STYLES = ("bar", "clusters", "vertical")
LAMP_DEPTH = 15.0  # lamps sit in recesses this deep, flush with the body face, mm


def _choice(p: Inputs, key: str, names: tuple[str, ...]) -> str:
    return names[min(max(int(round(p.get(key, 0))), 0), len(names) - 1)]


def wheel_design(p: Inputs) -> str:
    return _choice(p, "wheel_design", WHEEL_DESIGNS)


def head_lamp_style(p: Inputs) -> str:
    return _choice(p, "head_lamp_style", HEAD_LAMP_STYLES)


def tail_lamp_style(p: Inputs) -> str:
    return _choice(p, "tail_lamp_style", TAIL_LAMP_STYLES)


# --- Rims ---


def _spoke(angle: float, r0: float, r1: float, w0: float, w1: float,
           y: tuple[float, float]) -> k.Shape:  # fmt: skip
    """Tapered spoke from radius r0 (width w0) to r1 (width w1), turned by angle degrees
    about the spin axis."""
    outline = [(r0, -w0 / 2), (r1, -w1 / 2), (r1, w1 / 2), (r0, w0 / 2)]
    return k.rotate_y(k.prism_y(outline, y), angle, (0.0, 0.0, 0.0))


def _holes(count: int, pitch: float, radius: float, y: tuple[float, float],
           phase: float = 0.0) -> list[k.Shape]:  # fmt: skip
    out = []
    for i in range(count):
        a = 2 * math.pi * i / count + math.radians(phase)
        out.append(k.cylinder_y(radius, (y[0] - 1, y[1] + 1), x=pitch * math.cos(a),
                                z=pitch * math.sin(a)))  # fmt: skip
    return out


def build_rim(p: Inputs) -> k.Shape:
    """Rim barrel and a face by design: five spokes, ten slim spokes, five twin spokes, a
    mesh (inner and outer spoke sets joined by a ring), a closed aero disc with small vents,
    or a plain steel disc with round holes and a hub cap."""
    rim_r, half = p["rim_radius"], p["tyre_width"] / 2.0
    face_r = rim_r - RIM_BARREL
    y0 = half * 0.95 - FACE_THICKNESS - FACE_SET
    y = (y0, y0 + FACE_THICKNESS)
    barrel = k.ring_y(rim_r, face_r, (-half * 0.95, half * 0.95))
    bore = k.cylinder_y(AXLE_RADIUS + 5.0, (y[0] - 1, y[1] + 1))
    design = wheel_design(p)
    hub_r = 0.30 * face_r
    hub = k.cylinder_y(hub_r, y)
    reach = face_r + 2.0  # spokes run into the barrel so the rim is one solid
    if design in ("aero", "steel"):
        disc = k.cylinder_y(face_r + 1.0, y)
        if design == "aero":
            vents = _holes(10, 0.80 * face_r, 0.06 * face_r, y)
            return k.fuse(barrel, k.cut(disc, *vents, bore))
        holes = _holes(6, 0.62 * face_r, 0.11 * face_r, y, phase=30.0)
        cap = k.cylinder_y(0.36 * face_r, (y[1] - 1.0, y[1] + 14.0))
        return k.fuse(barrel, k.cut(k.fuse(disc, cap), *holes, bore))
    spokes: list[k.Shape] = []
    if design == "five_spoke":
        spokes = [_spoke(72.0 * i, 0.8 * hub_r, reach, 0.34 * face_r, 0.26 * face_r, y)
                  for i in range(5)]  # fmt: skip
    elif design == "multi_spoke":
        spokes = [_spoke(36.0 * i, 0.8 * hub_r, reach, 0.12 * face_r, 0.08 * face_r, y)
                  for i in range(10)]  # fmt: skip
    elif design == "twin_spoke":
        spokes = [_spoke(72.0 * i + s, 0.8 * hub_r, reach, 0.13 * face_r, 0.09 * face_r, y)
                  for i in range(5) for s in (-7.0, 7.0)]  # fmt: skip
    else:  # mesh
        ring_r = 0.62 * face_r
        spokes = [_spoke(36.0 * i, 0.8 * hub_r, ring_r + 5.0, 0.11 * face_r, 0.08 * face_r, y)
                  for i in range(10)]  # fmt: skip
        spokes += [_spoke(18.0 * i + 9.0, ring_r - 5.0, reach, 0.06 * face_r, 0.06 * face_r, y)
                   for i in range(20)]  # fmt: skip
        spokes.append(k.ring_y(ring_r + 12.0, ring_r - 12.0, y))
    face = k.cut(k.fuse(hub, *spokes), bore)
    return k.fuse(barrel, face)


# --- Lamps ---


def lamp_solids(p: Inputs, end: str, layout) -> list[k.Shape]:  # type: ignore[no-untyped-def]
    """Lamp solids at the front ("head") or rear ("tail") face, by signature.

    Head: slim LED strips joined by a light line, segmented matrix units, round lamps, or a
    split layout (a thin daytime running strip above a separate main lamp). Tail: a
    full-width light bar, separate clusters at the corners, or vertical lamps at the corners.
    """
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    half_w = p["body_width"] / 2.0
    floor, belt = p["body_floor"], p["beltline_height"]
    if end == "head":
        bumper, nose = layout.profile[2][1], layout.profile[3][1]
        h = nose - bumper
        top = nose - 0.08 * h
        x = (front - LAMP_DEPTH, front)
        style = head_lamp_style(p)
        out: list[k.Shape] = []
        for s in (1.0, -1.0):

            def span(a: float, b: float, s: float = s) -> tuple[float, float]:
                return tuple(sorted((s * a * half_w, s * b * half_w)))  # type: ignore[return-value]

            if style == "strip":
                out.append(k.box(x, span(0.26, 0.62), (top - max(0.16 * h, 30.0), top)))
            elif style == "matrix":
                band = (top - max(0.24 * h, 40.0), top)
                n, a0, a1, gap = 5, 0.26, 0.62, 8.0 / half_w
                w = (a1 - a0 - (n - 1) * gap) / n
                for i in range(n):
                    a = a0 + i * (w + gap)
                    out.append(k.box(x, span(a, a + w), band))
            elif style == "round":
                r = min(0.32 * h, 0.13 * half_w, 120.0)
                out.append(k.cylinder_x(r, x, y=s * 0.46 * half_w, z=top - r))
            else:  # split
                out.append(k.box(x, span(0.26, 0.66), (top - 14.0, top)))
                lower = (top - 0.62 * h, top - 0.32 * h)
                out.append(k.box(x, span(0.36, 0.62), lower))
        if style in ("strip", "matrix"):
            out.append(k.box(x, (-0.26 * half_w - 1.0, 0.26 * half_w + 1.0), (top - 12.0, top)))
        return out
    at_rear = [zz for xx, zz in layout.profile if abs(xx - rear) < 1e-6]
    top, bottom = (max(at_rear), min(at_rear)) if at_rear else (floor, floor)
    if layout.cargo is not None or top - bottom < 60.0:  # box truck: low on the box
        bottom, top = floor + 0.25 * (belt - floor), floor + 0.55 * (belt - floor)
    h = top - bottom
    x = (rear, rear + LAMP_DEPTH)
    style = tail_lamp_style(p)
    if style == "bar":
        bar = (top - 0.12 * h - max(0.14 * h, 35.0), top - 0.12 * h)
        return [k.box(x, (-0.78 * half_w, 0.78 * half_w), bar)]
    if style == "clusters":
        band = (top - 0.12 * h - max(0.30 * h, 60.0), top - 0.12 * h)
        return [k.box(x, (0.46 * half_w, 0.78 * half_w), band),
                k.box(x, (-0.78 * half_w, -0.46 * half_w), band)]  # fmt: skip
    band = (bottom + 0.15 * h, top - 0.08 * h)  # vertical
    return [k.box(x, (0.66 * half_w, 0.78 * half_w), band),
            k.box(x, (-0.78 * half_w, -0.66 * half_w), band)]  # fmt: skip
