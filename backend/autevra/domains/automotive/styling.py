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
WHEEL_DESIGNS = ("five_spoke", "multi_spoke", "twin_spoke", "mesh", "aero", "steel", "y_spoke")
HEAD_LAMP_STYLES = ("strip", "matrix", "round", "split", "swept")
TAIL_LAMP_STYLES = ("bar", "clusters", "vertical", "swept")
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
    elif design == "y_spoke":  # five stems, each forking into two arms near the rim
        for i in range(5):
            stem = _spoke(72.0 * i, 0.8 * hub_r, 0.62 * face_r, 0.2 * face_r, 0.15 * face_r, y)
            spokes.append(stem)
            for fork in (-11.0, 11.0):
                spokes.append(_spoke(72.0 * i + fork, 0.52 * face_r, reach, 0.085 * face_r,
                                     0.07 * face_r, y))  # fmt: skip
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


def tail_band(p: Inputs, layout) -> tuple[float, float]:  # type: ignore[no-untyped-def]
    """(bottom, top) z of the rear face that carries the tail lamps."""
    floor, belt = p["body_floor"], p["beltline_height"]
    rear = -(p["wheelbase"] + p["rear_overhang"])
    at_rear = [zz for xx, zz in layout.profile if abs(xx - rear) < 1e-6]
    bottom, top = (min(at_rear), max(at_rear)) if at_rear else (floor, floor)
    if layout.cargo is not None or top - bottom < 60.0:  # box truck: low on the box
        bottom, top = floor + 0.25 * (belt - floor), floor + 0.55 * (belt - floor)
    return bottom, top


def tail_swept_outline(p: Inputs, layout, side: float) -> list[tuple[float, float]]:  # type: ignore[no-untyped-def]
    """(y, z) outline of a swept tail lamp on one side: a slim band rising from inboard
    towards the upper outer corner of the tail."""
    half_w = p["body_width"] / 2.0
    bottom, top = tail_band(p, layout)
    h = top - bottom
    upper = top - 0.1 * h
    t, rise = max(0.11 * h, 26.0), 0.14 * h
    yi, yo = side * 0.34 * half_w, side * 0.80 * half_w
    return [(yi, upper - rise - t), (yo, upper - t), (yo, upper), (yi, upper - rise)]


def swept_outline(p: Inputs, layout, side: float) -> list[tuple[float, float]]:  # type: ignore[no-untyped-def]
    """(y, z) outline of a swept head lamp on one side (+1 left): a slanted band that rises
    from a slim inner end and thickens towards the outer corner of the nose, which it wraps
    (on a styled nose the corner curves back, so the lamp runs on into the top of the wing)."""
    half_w = p["body_width"] / 2.0
    bumper, nose = layout.profile[2][1], layout.profile[3][1]
    h = nose - bumper
    top = nose - 0.08 * h
    t_in, t_out = max(0.1 * h, 22.0), max(0.2 * h, 36.0)  # thickness at each end
    rise = 0.16 * h
    yi, yo = side * 0.36 * half_w, side * 0.84 * half_w
    return [(yi, top - rise - t_in), (yo, top - t_out), (yo, top), (yi, top - rise)]


LAMP_HOUSINGS = ("none", "smoked")


def lamp_housing(p: Inputs) -> str:
    i = int(round(p.get("lamp_housing", 0.0)))
    return LAMP_HOUSINGS[min(max(i, 0), len(LAMP_HOUSINGS) - 1)]


def housing_outline(p: Inputs, layout, side: float,  # type: ignore[no-untyped-def]
                    lamp: list[tuple[float, float]]) -> list[tuple[float, float]]:  # fmt: skip
    """(y, z) outline of a smoked head lamp housing round one side's lamp outline: the lamp
    runs along its top edge and the dark eye opens below it, a little wider at each end."""
    bumper, nose = layout.profile[2][1], layout.profile[3][1]
    drop = max(0.32 * (nose - bumper), 45.0)
    ys = [y for y, _ in lamp]
    yi, yo = (min(ys), max(ys)) if side > 0 else (max(ys), min(ys))
    grow = 25.0 * side

    def z_at(y: float, top: bool) -> float:  # the lamp's top or bottom edge at y
        pts = sorted(lamp, key=lambda q: abs(q[0] - y))[:2]
        return max(z for _, z in pts) if top else min(z for _, z in pts)

    return [(yi - grow, z_at(yi, False) - drop), (yo + grow, z_at(yo, False) - 0.5 * drop),
            (yo + grow, z_at(yo, True) + 4.0), (yi - grow, z_at(yi, True) + 4.0)]  # fmt: skip


def lamp_solids(p: Inputs, end: str, layout) -> list[k.Shape]:  # type: ignore[no-untyped-def]
    """Lamp solids at the front ("head") or rear ("tail") face, by signature.

    Head: slim LED strips joined by a light line, segmented matrix units, round lamps, a
    split layout (a thin daytime running strip above a separate main lamp), or slim swept
    lamps reaching the upper corners (they wrap round the curved corner of a styled nose). Tail: a
    full-width light bar, separate clusters at the corners, or vertical lamps at the corners.
    """
    rear = -(p["wheelbase"] + p["rear_overhang"])
    half_w = p["body_width"] / 2.0
    if end == "head":
        (xb, bumper), (xn, nose) = layout.profile[2], layout.profile[3]
        h = nose - bumper
        top = nose - 0.08 * h
        # On the (possibly raked) front face, at the lamps' height.
        xf = xb + (xn - xb) * (top - 0.1 * h - bumper) / max(h, 1.0)
        x = (xf - LAMP_DEPTH, xf)
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
            elif style == "swept":  # slim lamps rising towards the upper corners
                out.append(k.prism_x(swept_outline(p, layout, s), x))
            else:  # split
                out.append(k.box(x, span(0.26, 0.66), (top - 14.0, top)))
                lower = (top - 0.62 * h, top - 0.32 * h)
                out.append(k.box(x, span(0.36, 0.62), lower))
        if style in ("strip", "matrix"):
            out.append(k.box(x, (-0.26 * half_w - 1.0, 0.26 * half_w + 1.0), (top - 12.0, top)))
        return out
    bottom, top = tail_band(p, layout)
    h = top - bottom
    x = (rear, rear + LAMP_DEPTH)
    style = tail_lamp_style(p)
    if style == "swept":
        return [k.prism_x(tail_swept_outline(p, layout, s), x) for s in (1.0, -1.0)]
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
