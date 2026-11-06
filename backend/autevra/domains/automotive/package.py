"""Vehicle package: the dimensions a package drawing carries, computed from the design.

Ground-clearance angles follow their usual definitions, evaluated on the model (not a
certified measurement): the approach (departure) angle is the steepest line tangent to the
front (rear) tyre that clears every low point ahead of (behind) it; the breakover angle is
the sum of the angles of the two lines from the lowest point mid-wheelbase tangent to each
tyre. Tyres are their unloaded circles on flat ground (no tyre deflection or suspension
sag). Low points are the body's side profile, the chassis frame's underside and the tow
bar when fitted.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass

from autevra.domains.automotive import builders as b
from autevra.domains.automotive import derived as d
from autevra.domains.automotive import exterior, interior

Values = Mapping[str, float]
H_POINT_BELOW_CUSHION = 100.0  # H-point below the cushion top (allowance), mm
H_POINT_FROM_HINGE = 130.0  # H-point ahead of the backrest hinge (allowance), mm


@dataclass(frozen=True)
class PackageValue:
    id: str
    label: str
    value: float
    unit: str
    note: str = ""


def _body_inputs(values: Values) -> dict[str, float]:
    from autevra.assembly.model import BY_ID

    return BY_ID["body"].resolve_inputs(values)


def _tangent_angle(point: tuple[float, float], centre: tuple[float, float],
                   radius: float) -> float | None:  # fmt: skip
    """Angle (degrees, 0..90) to the horizontal of the line through ``point`` tangent to
    the tyre circle with the circle above the line (the ground side); None when the point
    is inside the circle."""
    (px, pz), (cx, cz) = point, centre
    dx, dz = cx - px, cz - pz
    dist = math.hypot(dx, dz)
    if dist <= radius:
        return None
    psi, off = math.atan2(dz, dx), math.asin(radius / dist)
    best = None
    for beta in (psi + off, psi - off):
        # Line through the point with direction beta; keep the one under the centre.
        if abs(math.cos(beta)) < 1e-12:
            continue
        slope = math.tan(beta)
        if cz > pz + slope * (cx - px):
            angle = abs(math.degrees(math.atan(slope)))
            best = angle if best is None else min(best, angle)
    return best


def low_points(values: Values) -> list[tuple[float, float]]:
    """Points (x, z) that can touch the ground on a slope: the body's side profile, the
    frame underside along its length and the tow bar's lowest point when fitted."""
    p = _body_inputs(values)
    layout = b.body_layout(p)
    pts = list(layout.profile)
    gc = values["ground_clearance"]
    front = values["front_overhang"] - 150.0
    rear = -(values["wheelbase"] + values["rear_overhang"] - 150.0)
    steps = 40
    pts += [(rear + (front - rear) * i / steps, gc) for i in range(steps + 1)]
    if int(round(values.get("tow_bar", 0))):
        x_rear = -(values["wheelbase"] + values["rear_overhang"])
        pts.append((x_rear - 145.0, exterior.BALL_HEIGHT - 60.0 - 20.0))  # ball platform
    return pts


def clearance_angles(values: Values) -> dict[str, float]:
    radius = d.tyre_radius(values)
    wb = values["wheelbase"]
    pts = low_points(values)
    front_c, rear_c = (0.0, radius), (-wb, radius)
    approach = [a for x, z in pts if x > 0.0 and (a := _tangent_angle((x, z), front_c, radius))
                is not None]  # fmt: skip
    departure = [a for x, z in pts if x < -wb
                 and (a := _tangent_angle((x, z), rear_c, radius)) is not None]  # fmt: skip
    mid = -wb / 2.0
    lowest = min(z for x, z in pts if abs(x - mid) <= 0.25 * wb)
    apex = (mid, lowest)
    breakover = (_tangent_angle(apex, front_c, radius) or 0.0) + (
        _tangent_angle(apex, rear_c, radius) or 0.0
    )
    return {
        "approach_angle": min(approach) if approach else 90.0,
        "departure_angle": min(departure) if departure else 90.0,
        "breakover_angle": breakover,
    }


def seating(values: Values) -> dict[str, float]:
    """Front-seat H-point (x, z), from the seat package (allowances, not an SAE manikin)."""
    p = _body_inputs(values) | {k: values[k] for k in interior_inputs()}
    c = interior.cabin(p)
    x_front, _ = interior.seat_positions(p)[0]
    hinge = x_front - 500.0
    return {
        "h_point_x": hinge + H_POINT_FROM_HINGE,
        "h_point_z": interior.cushion_top(c) - H_POINT_BELOW_CUSHION,
        "headroom": interior.front_headroom(p),
    }


def interior_inputs() -> tuple[str, ...]:
    return ("seat_rows", "interior_trim", "driving_side", "seat_height", "seat_recline",
            "dash_zone", "row_pitch")  # fmt: skip


def package(values: Values) -> list[PackageValue]:
    angles = clearance_angles(values)
    seat = seating(values)
    radius = d.tyre_radius(values)
    out = [
        PackageValue("overall_length", "Overall length", d.overall_length(values), "mm"),
        PackageValue("overall_width", "Overall width (body)", values["body_width"], "mm",
                     "excluding mirrors"),
        PackageValue("width_over_mirrors", "Width over mirrors",
                     exterior.width_over_mirrors(values), "mm"),
        PackageValue("overall_height", "Overall height", values["overall_height"], "mm",
                     "to the roof panel, unladen"),
        PackageValue("wheelbase", "Wheelbase", values["wheelbase"], "mm"),
        PackageValue("front_overhang", "Front overhang", values["front_overhang"], "mm"),
        PackageValue("rear_overhang", "Rear overhang", values["rear_overhang"], "mm"),
        PackageValue("track_front", "Front track", values["track_front"], "mm"),
        PackageValue("track_rear", "Rear track", values["track_rear"], "mm"),
        PackageValue("ground_clearance", "Ground clearance", values["ground_clearance"], "mm",
                     "frame underside, unladen"),
        PackageValue("tyre_diameter", "Tyre diameter", 2.0 * radius, "mm", "unloaded"),
        PackageValue("approach_angle", "Approach angle", angles["approach_angle"], "deg",
                     "tangent to the unloaded front tyre"),
        PackageValue("departure_angle", "Departure angle", angles["departure_angle"], "deg",
                     "tangent to the unloaded rear tyre"),
        PackageValue("breakover_angle", "Breakover angle", angles["breakover_angle"], "deg",
                     "from the lowest point mid-wheelbase"),
        PackageValue("h_point_height", "Front H-point height", seat["h_point_z"], "mm",
                     "above the ground; seat allowance, not a manikin measurement"),
        PackageValue("h_point_x", "Front H-point from front axle", seat["h_point_x"], "mm",
                     "negative is behind the axle"),
        PackageValue("front_headroom", "Front headroom", seat["headroom"], "mm",
                     "seated-height allowance"),
    ]  # fmt: skip
    return out


# --- Package drawing (SVG) ---------------------------------------------------------------


def _fmt(v: float) -> str:
    return f"{v:.1f}"


def _poly(points: list[tuple[float, float]], cls: str, closed: bool = True) -> str:
    tag = "polygon" if closed else "polyline"
    pts = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)
    return f'<{tag} class="{cls}" points="{pts}"/>'


def _dim(x0: float, y0: float, x1: float, y1: float, text: str, offset: float) -> str:
    """A linear dimension between two points, drawn ``offset`` away (perpendicular)."""
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / length * offset, dx / length * offset
    a, b = (x0 + nx, y0 + ny), (x1 + nx, y1 + ny)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    angle = math.degrees(math.atan2(dy, dx))
    if angle > 90 or angle < -90:
        angle += 180
    return (
        f'<line class="ext" x1="{_fmt(x0)}" y1="{_fmt(y0)}" x2="{_fmt(a[0])}" y2="{_fmt(a[1])}"/>'
        f'<line class="ext" x1="{_fmt(x1)}" y1="{_fmt(y1)}" x2="{_fmt(b[0])}" y2="{_fmt(b[1])}"/>'
        f'<line class="dim" x1="{_fmt(a[0])}" y1="{_fmt(a[1])}" x2="{_fmt(b[0])}" '
        f'y2="{_fmt(b[1])}" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
        f'<text class="dimtext" x="{_fmt(mx)}" y="{_fmt(my - 25)}" '
        f'transform="rotate({_fmt(angle)} {_fmt(mx)} {_fmt(my)})">{text}</text>'
    )


def drawing_svg(values: Values, title: str = "Package drawing") -> str:
    """Side, top and front views with the main package dimensions (mm), as SVG. Views are
    to scale (first-angle arrangement is not claimed; views are labelled)."""
    from autevra.domains.automotive import sculpt

    p = _body_inputs(values)
    layout = b.body_layout(p)
    radius = d.tyre_radius(values)
    wb, fo, ro = values["wheelbase"], values["front_overhang"], values["rear_overhang"]
    rear, front = -(wb + ro), fo
    height, half_w = values["overall_height"], values["body_width"] / 2.0
    belt = values["beltline_height"]
    angles = clearance_angles(values)

    # Side view: x to the left is forward in a drawing convention with the nose at left.
    def side(x: float, z: float) -> tuple[float, float]:
        return (-x, -z)

    profile = sculpt.smooth_profile(layout.profile, share=0.06 + 0.16 * values.get(
        "body_roundness", 45.0) / 100.0)  # fmt: skip
    (g0, g1), (r0, r1) = layout.glass, layout.roof
    greenhouse = [(g0, belt), (r0, layout.roof_z), (r1, layout.roof_z), (g1, belt)]
    side_parts = [
        _poly([side(x, z) for x, z in profile], "body"),
        _poly([side(x, z) for x, z in greenhouse], "glass"),
    ]
    if layout.cargo is not None:
        c0, c1 = layout.cargo
        side_parts.append(_poly([side(c0, values["body_floor"] if "body_floor" in values
                                      else p["body_floor"]), side(c1, p["body_floor"]),
                                 side(c1, height), side(c0, height)], "body"))  # fmt: skip
    for xa in (0.0, -wb):
        cx, cy = side(xa, radius)
        side_parts.append(
            f'<circle class="tyre" cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(radius)}"/>'
        )
        side_parts.append(f'<circle class="centre" cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="12"/>')
    side_parts.append(
        f'<line class="ground" x1="{_fmt(-front - 600)}" y1="0" x2="{_fmt(-rear + 600)}" y2="0"/>'
    )
    # Approach and departure lines from the tyre tangent points, at the computed angles.
    for xa, angle, sign in ((0.0, angles["approach_angle"], 1.0),
                            (-wb, angles["departure_angle"], -1.0)):  # fmt: skip
        a = math.radians(angle)
        tx, tz = xa + sign * radius * math.sin(a), radius - radius * math.cos(a)
        ex = tx + sign * 1400.0 * math.cos(a)
        ez = tz + 1400.0 * math.sin(a)
        (sx, sy), (fx, fy) = side(tx, tz), side(ex, ez)
        side_parts.append(
            f'<line class="angle" x1="{_fmt(sx)}" y1="{_fmt(sy)}" x2="{_fmt(fx)}" y2="{_fmt(fy)}"/>'
        )
        side_parts.append(
            f'<text class="note" x="{_fmt(fx)}" y="{_fmt(fy - 30)}">{angle:.1f}°</text>'
        )
    side_parts += [
        _dim(*side(0.0, 0.0), *side(-wb, 0.0), f"{wb:.0f}", 260.0),
        _dim(*side(front, 0.0), *side(0.0, 0.0), f"{fo:.0f}", 260.0),
        _dim(*side(-wb, 0.0), *side(rear, 0.0), f"{ro:.0f}", 260.0),
        _dim(*side(front, 0.0), *side(rear, 0.0), f"{front - rear:.0f}", 560.0),
        _dim(*side(rear, 0.0), *side(rear, height), f"{height:.0f}", 320.0),
        _dim(*side(-wb / 2, 0.0), *side(-wb / 2, values["ground_clearance"]),
             f"{values['ground_clearance']:.0f}", 0.0),
    ]  # fmt: skip
    seat = seating(values)
    hx, hz = side(seat["h_point_x"], seat["h_point_z"])
    side_parts.append(f'<circle class="hpoint" cx="{_fmt(hx)}" cy="{_fmt(hz)}" r="35"/>')
    side_parts.append(
        f'<text class="note" x="{_fmt(hx + 50)}" y="{_fmt(hz - 50)}">'
        f"H-point {seat['h_point_z']:.0f}</text>"
    )

    # Top view (below the side view): x forward to the left, y left up.
    top_y = height + 1600.0 + half_w

    def top(x: float, y: float) -> tuple[float, float]:
        return (-x, top_y - y)

    plan = sculpt.plan_points(p, (rear, front), 0.0, 0.0)
    top_parts = [_poly([top(x, y) for x, y, _ in plan], "body")]
    for xa, track in ((0.0, values["track_front"]), (-wb, values["track_rear"])):
        for s in (1.0, -1.0):
            yc = s * track / 2.0
            w = values["tyre_width"]
            top_parts.append(_poly([top(xa + radius, yc - w / 2), top(xa - radius, yc - w / 2),
                                    top(xa - radius, yc + w / 2), top(xa + radius, yc + w / 2)],
                                   "tyre"))  # fmt: skip
    top_parts += [
        _dim(*top(front, half_w), *top(front, -half_w), f"{2 * half_w:.0f}", 300.0),
        _dim(*top(0.0, values["track_front"] / 2), *top(0.0, -values["track_front"] / 2),
             f"{values['track_front']:.0f}", -250.0),
        _dim(*top(-wb, values["track_rear"] / 2), *top(-wb, -values["track_rear"] / 2),
             f"{values['track_rear']:.0f}", 250.0),
    ]  # fmt: skip

    # Front view (right of the side view): y left to the right, z up.
    fx0 = -rear + 1800.0 + half_w

    def fr(y: float, z: float) -> tuple[float, float]:
        return (fx0 + y, -z)

    roof_w = b.roof_half_width(p)
    sill = values["ground_clearance"] + 80.0
    outline = [fr(-half_w, sill), fr(half_w, sill), fr(half_w, belt), fr(roof_w, height),
               fr(-roof_w, height), fr(-half_w, belt)]  # fmt: skip
    front_parts = [_poly(outline, "body")]
    for s in (1.0, -1.0):
        yc, w = s * values["track_front"] / 2.0, values["tyre_width"]
        front_parts.append(_poly([fr(yc - w / 2, 0), fr(yc + w / 2, 0), fr(yc + w / 2, 2 * radius),
                                  fr(yc - w / 2, 2 * radius)], "tyre"))  # fmt: skip
    front_parts.append(_dim(*fr(-half_w, 0), *fr(half_w, 0), f"{2 * half_w:.0f}", 260.0))

    x_min, x_max = -front - 900.0, fx0 + half_w + 700.0
    y_min, y_max = -height - 700.0, top_y + half_w + 900.0  # dimensions sit below the ground
    labels = [
        f'<text class="view" x="{_fmt(-front)}" y="{_fmt(-height - 350)}">SIDE VIEW (LEFT)</text>',
        f'<text class="view" x="{_fmt(-front)}" y="{_fmt(top_y - half_w - 450)}">TOP VIEW</text>',
        f'<text class="view" x="{_fmt(fx0 - half_w)}" y="{_fmt(-height - 350)}">FRONT VIEW</text>',
        f'<text class="titleblock" x="{_fmt(x_min + 100)}" y="{_fmt(y_max - 250)}">{title} · '
        f"dimensions in mm · unladen, tyres unloaded · approach {angles['approach_angle']:.1f}° "
        f"· departure {angles['departure_angle']:.1f}° "
        f"· breakover {angles['breakover_angle']:.1f}°</text>",
    ]
    style = (
        "<style>"
        ".body{fill:none;stroke:#1d2733;stroke-width:9}"
        ".glass{fill:#d9e6f2;stroke:#1d2733;stroke-width:6}"
        ".tyre{fill:#e7e9ec;stroke:#1d2733;stroke-width:7}"
        ".centre{fill:#1d2733}.ground{stroke:#6b7785;stroke-width:6;stroke-dasharray:60 30}"
        ".angle{stroke:#c0392b;stroke-width:6;stroke-dasharray:40 20}"
        ".hpoint{fill:none;stroke:#2e86de;stroke-width:8}"
        ".dim{stroke:#2c3e50;stroke-width:4}.ext{stroke:#95a5a6;stroke-width:3}"
        ".dimtext{font:80px sans-serif;fill:#2c3e50;text-anchor:middle}"
        ".note{font:70px sans-serif;fill:#c0392b}.view{font:bold 90px sans-serif;fill:#2c3e50}"
        ".titleblock{font:80px sans-serif;fill:#2c3e50}"
        "</style>"
    )
    defs = ('<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            'fill="#2c3e50"/></marker></defs>')  # fmt: skip
    body = "".join([*side_parts, *top_parts, *front_parts, *labels])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_fmt(x_min)} {_fmt(y_min)} '
        f'{_fmt(x_max - x_min)} {_fmt(y_max - y_min)}" style="background:#ffffff">'
        f"{style}{defs}{body}</svg>"
    )
