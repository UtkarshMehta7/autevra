"""Body details: front grille, fender vents and brakes.

The grille and the vents are recessed into the body (the body is cut by the same tools), so
they sit inside its surface and the body's extents do not change. Brake discs and calipers
are built in the wheel frame like the rims (origin at the wheel centre, spin axis along Y,
outboard towards +Y) and sit inside the rim barrel, inboard of the spoke face. The shapes
are representative styling envelopes: no cooling-air flow and no brake sizing or thermal
analysis (the brake test uses its own parameters).
"""

import math
from collections.abc import Mapping, Sequence

from autevra.cad import kernel as k
from autevra.domains.automotive import sculpt
from autevra.domains.automotive.derived import AXLE_RADIUS
from autevra.domains.automotive.styling import FACE_SET, FACE_THICKNESS, RIM_BARREL

Inputs = Mapping[str, float]

GRILLE_STYLES = ("none", "bars", "mesh", "sport")
SIDE_VENTS = ("none", "gills", "slot")
CALIPER_COLOURS = ("black", "silver", "red", "yellow", "blue", "green")
GRILLE_DEPTH = 45.0  # mesh plane behind the nose face, mm
BACK_DEPTH = 80.0  # dark back plate behind the mesh (the recess depth), mm
SURROUND = 16.0  # width of the grille surround, mm
MESH_PITCH = 52.0  # diamond mesh cell, measured across, mm
MESH_BAR = 7.0  # mm
VENT_DEPTH = 14.0  # vent slots cut this deep into the wing, mm


def _choice(p: Inputs, key: str, names: tuple[str, ...]) -> str:
    return names[min(max(int(round(p.get(key, 0))), 0), len(names) - 1)]


def grille_style(p: Inputs) -> str:
    return _choice(p, "grille_style", GRILLE_STYLES)


def side_vents(p: Inputs) -> str:
    return _choice(p, "side_vents", SIDE_VENTS)


# --- Grille ---


def _face(layout) -> list[tuple[float, float]]:  # type: ignore[no-untyped-def]
    """Side profile (x, z) of the nose face: the chin from the floor up to the bumper line,
    then the front face up to the bonnet edge, extended past both ends."""
    (xa, za), (xb, zb), (xc, zc) = layout.profile[1], layout.profile[2], layout.profile[3]
    return [(xa - 200.0, za - 200.0), (xa, za), (xb, zb), (xc, zc), (xc, zc + 200.0)]


def _band(layout, d0: float, d1: float, half_w: float) -> k.Shape:  # type: ignore[no-untyped-def]
    """The layer from d0 to d1 behind the nose face (negative: in front of it), full width."""
    chain = _face(layout)
    outline = [(x - d0, z) for x, z in chain] + [(x - d1, z) for x, z in reversed(chain)]
    return k.prism_y(outline, (-half_w - 10.0, half_w + 10.0))


def _trapezoid(top_w: float, bottom_w: float, z0: float, z1: float) -> list[tuple[float, float]]:
    return [(-bottom_w, z0), (bottom_w, z0), (top_w, z1), (-top_w, z1)]


def _openings(p: Inputs, layout) -> list[list[tuple[float, float]]]:  # type: ignore[no-untyped-def]
    """(y, z) outlines of the grille openings on the nose, by style. They stay below the
    head lamps and inside the flat part of the nose in plan."""
    style = grille_style(p)
    if style == "none":
        return []
    hw = p["body_width"] / 2.0
    floor, bumper, nose = layout.profile[1][1], layout.profile[2][1], layout.profile[3][1]
    h, chin = nose - bumper, bumper - floor
    top = nose - max(0.30 * h, 60.0)  # clear of every head lamp signature
    if style == "sport":  # a large trapezoid filling the face, flared at the foot, and intakes
        from autevra.domains.automotive import styling

        if styling.head_lamp_style(p) == "swept":  # slim lamps high on the corners
            top = nose - max(0.26 * h, 55.0)
        bottom = floor + 0.2 * chin
        if top - bottom < 60.0:
            return []
        intake_top = min(bumper + 0.25 * h, top) - 10.0
        out = [_trapezoid(0.40 * hw, 0.48 * hw, bottom, top)]
        if intake_top - bottom > 50.0:
            # Inside the flat part of the nose in plan (its width is the nose taper).
            outer = min(0.64, 0.9 * p.get("nose_taper", 72.0) / 100.0) * hw
            for s in (1.0, -1.0):
                if outer - 0.53 * hw < 40.0:
                    break  # a narrow nose leaves no room for corner intakes
                y0, y1 = sorted((s * 0.53 * hw, s * outer))
                out.append([(y0, bottom + 15.0), (y1, bottom + 15.0), (y1, intake_top),
                            (y0, intake_top)])  # fmt: skip
        return out
    bottom = bumper - 0.45 * chin
    if top - bottom < 50.0:
        return []
    return [_trapezoid(0.30 * hw, 0.30 * hw, bottom, top)]


def _inset(outline: Sequence[tuple[float, float]], t: float) -> list[tuple[float, float]]:
    """A convex outline moved in by about t (towards its centre, per axis)."""
    ys, zs = [y for y, _ in outline], [z for _, z in outline]
    cy, cz = (min(ys) + max(ys)) / 2.0, (min(zs) + max(zs)) / 2.0
    return [(y - math.copysign(t, y - cy), z - math.copysign(t, z - cz)) for y, z in outline]


def grille_tools(p: Inputs, layout) -> list[k.Shape]:  # type: ignore[no-untyped-def]
    """Cutters for the grille openings: each outline, from just in front of the nose face
    to the back plate."""
    openings = _openings(p, layout)
    if not openings:
        return []
    front = p["front_overhang"]
    band = _band(layout, -80.0, BACK_DEPTH, p["body_width"] / 2.0)
    return [k.intersect(k.prism_x(o, (front - 1500.0, front + 100.0)), band) for o in openings]


def _inside(point: tuple[float, float], outline: Sequence[tuple[float, float]]) -> bool:
    """Whether a point is inside a convex outline (either winding)."""
    signs = set()
    for (ay, az), (by, bz) in zip(outline, [*outline[1:], outline[0]], strict=True):
        cross = (by - ay) * (point[1] - az) - (bz - az) * (point[0] - ay)
        if abs(cross) > 1e-9:
            signs.add(cross > 0)
    return len(signs) <= 1


def _mesh(outline: Sequence[tuple[float, float]], style: str, x: tuple[float, float]) -> k.Shape:
    """A plate filling the outline, pierced by a diamond mesh (or by horizontal slots
    between bars). Only whole openings are pierced, so the plate keeps a border."""
    ys, zs = [y for y, _ in outline], [z for _, z in outline]
    y0, y1, z0, z1 = min(ys), max(ys), min(zs), max(zs)
    holes: list[list[tuple[float, float]]] = []
    if style == "bars":
        n = max(2, int((z1 - z0) / 38.0))
        pitch = (z1 - z0) / n
        for i in range(n):
            za, zb = z0 + i * pitch + 5.0, z0 + (i + 1) * pitch - 5.0
            slot = [(y0 + 4.0, za), (y1 - 4.0, za), (y1 - 4.0, zb), (y0 + 4.0, zb)]
            holes.append([(y, z) for y, z in _inset_to(outline, slot)])
    else:
        r = (MESH_PITCH - MESH_BAR * math.sqrt(2.0)) / 2.0  # half diagonal of a hole
        row = 0
        z = z0 + MESH_PITCH / 2.0
        while z < z1:
            y = y0 + (MESH_PITCH / 2.0 if row % 2 else 0.0)
            while y < y1:
                diamond = [(y - r, z), (y, z - r), (y + r, z), (y, z + r)]
                if all(_inside(pt, outline) for pt in diamond):
                    holes.append(diamond)
                y += MESH_PITCH
            z += MESH_PITCH / 2.0
            row += 1
    return k.perforated_prism_x(outline, holes, x)


def _inset_to(outline: Sequence[tuple[float, float]],
              slot: list[tuple[float, float]]) -> list[tuple[float, float]]:  # fmt: skip
    """A horizontal slot shortened at each end to stay inside a trapezoid outline."""
    (ya, za), (yb, _), (_, zb), _ = slot
    out = []
    for z in (za, zb):
        left = min(y for y in _span(outline, z))
        right = max(y for y in _span(outline, z))
        out.append((max(ya, left + 6.0), min(yb, right - 6.0), z))
    (l0, r0, za), (l1, r1, zb) = out
    return [(l0, za), (r0, za), (r1, zb), (l1, zb)]


def _span(outline: Sequence[tuple[float, float]], z: float) -> list[float]:
    """Where a horizontal line at z crosses a convex outline."""
    out = []
    for (ay, az), (by, bz) in zip(outline, [*outline[1:], outline[0]], strict=True):
        if min(az, bz) <= z <= max(az, bz) and az != bz:
            out.append(ay + (by - ay) * (z - az) / (bz - az))
    return out or [0.0]


def build_grille(p: Inputs) -> k.Shape | None:
    """Grille surround, mesh or bars, and a dark back plate, in the recesses the body
    leaves for them."""
    from autevra.domains.automotive import builders as b

    layout = b.body_layout(p)
    openings = _openings(p, layout)
    if not openings:
        return None
    style = grille_style(p)
    front, hw = p["front_overhang"], p["body_width"] / 2.0
    x = (front - p.get("front_overhang", 900.0) + 50.0, front + 100.0)
    parts = []
    for i, o in enumerate(openings):
        region = k.prism_x(o, x)
        ring = k.cut(region, k.prism_x(_inset(o, SURROUND), x))
        parts.append(k.intersect(ring, _band(layout, 6.0, BACK_DEPTH, hw)))  # surround
        parts.append(k.intersect(region, _band(layout, BACK_DEPTH - 6.0, BACK_DEPTH, hw)))
        pattern = "bars" if style == "bars" and i == 0 else "mesh"  # intakes are meshed
        mesh = _mesh(_inset(o, SURROUND - 2.0), pattern, x)
        parts.append(k.intersect(mesh, _band(layout, GRILLE_DEPTH - 10.0, GRILLE_DEPTH, hw)))
    grille = k.fuse(*parts)
    from autevra.domains.automotive import styled

    if styled.styled_ok(p):
        # A styled nose rounds off towards its tip: keep the grille inside the skin there,
        # as the lamp lenses are.
        grille = k.intersect(grille, styled.skin(p, layout))
    return grille if k.solid_count(grille) else None


# --- Fender vents ---


def _vent_outlines(p: Inputs) -> list[list[tuple[float, float]]]:
    """(x, z) outlines of the vent slots on the front wing, behind the wheel arch."""
    style = side_vents(p)
    if style == "none":
        return []
    r, wheel_z = p["arch_radius"], p["tyre_radius"]
    zc = min(wheel_z + 0.55 * r, p["beltline_height"] - 140.0)
    x_end = -(r + 60.0)
    lean = 22.0  # the slots lean forward at the top
    if style == "slot":
        return [[(x_end - 320.0, zc - 12.0), (x_end, zc - 12.0), (x_end + lean, zc + 12.0),
                 (x_end - 320.0 + lean, zc + 12.0)]]  # fmt: skip
    out = []
    for i in range(3):
        x1 = x_end - i * 130.0
        out.append([(x1 - 105.0, zc - 9.0), (x1, zc - 9.0), (x1 + lean, zc + 9.0),
                    (x1 - 105.0 + lean, zc + 9.0)])  # fmt: skip
    return out


def _wing_y(p: Inputs, x: float) -> float:
    """Body side (half width) at x on the front wing, just inside the surface."""
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    return 0.95 * sculpt.width_at(p, x, (rear, front)) - 6.0


def vent_tools(p: Inputs) -> list[k.Shape]:
    tools = []
    half_w = p["body_width"] / 2.0
    for o in _vent_outlines(p):
        y = _wing_y(p, sum(x for x, _ in o) / len(o)) - VENT_DEPTH
        tools += [k.prism_y(o, (y, half_w + 20.0)), k.prism_y(o, (-half_w - 20.0, -y))]
    return tools


def build_side_vents(p: Inputs) -> k.Shape | None:
    """Dark inserts at the bottom of the vent slots."""
    parts = []
    for o in _vent_outlines(p):
        y = _wing_y(p, sum(x for x, _ in o) / len(o)) - VENT_DEPTH
        parts += [k.prism_y(o, (y, y + 4.0)), k.prism_y(o, (-y - 4.0, -y))]  # in the slot
    return k.fuse(*parts) if parts else None


# --- Door shut lines and handles ---

DOOR_LINES = ("none", "lines", "lines_handles")
SHUT_GAP = 4.0  # width of a shut line, mm
SHUT_DEPTH = 25.0  # how far the shut-line cut reaches in from the skin, mm
TWO_DOOR_STYLES = ("coupe", "roadster", "supercar")


def door_lines(p: Inputs) -> str:
    return _choice(p, "door_lines", DOOR_LINES)


def doors(p: Inputs, layout) -> list[tuple[float, float]]:  # type: ignore[no-untyped-def]
    """(rear x, front x) of each door on one side, front door first. Two long doors on
    coupes, roadsters and supercars, else a front and (with a second seat row) a rear door;
    vans and trucks keep their own panels (none here). Doors stay between the wheel arches,
    behind any wing vents."""
    if layout.cargo is not None or layout.style in ("van", "mpv", "box_truck"):
        return []
    arch = p["arch_radius"]
    front = min(layout.glass[1] - 40.0, -arch - 60.0)
    vents = _vent_outlines(p)
    if vents:
        front = min(front, min(x for o in vents for x, _ in o) - 60.0)
    limit = -p["wheelbase"] + arch + 60.0  # ahead of the rear wheel arch
    if layout.style in TWO_DOOR_STYLES or layout.style == "pickup" and p.get("seat_rows", 2) < 2:
        return [(max(front - 1250.0, limit), front)] if front - limit > 600.0 else []
    out = [(max(front - 1050.0, limit), front)]
    if p.get("seat_rows", 2) >= 2 and out[0][0] - limit > 500.0:
        out.append((max(out[0][0] - 950.0, limit), out[0][0]))
    return out


def door_tools(p: Inputs, layout) -> list[k.Shape]:  # type: ignore[no-untyped-def]
    """Cutters for the shut lines round each door (the front and rear edges from the sill
    to the beltline, and the bottom edge) and, with handles, a shallow flush-handle recess
    near the top rear of each door; both sides of the car."""
    style = door_lines(p)
    if style == "none":
        return []
    rear_x, front_x = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    floor, belt, hw = p["body_floor"], p["beltline_height"], p["body_width"] / 2.0
    bottom = floor + 0.2 * (belt - floor)

    def side(x: float) -> float:  # just inside the body side at x
        return 0.95 * sculpt.width_at(p, x, (rear_x, front_x)) - 6.0

    out: list[k.Shape] = []
    for x0, x1 in doors(p, layout):
        g = SHUT_GAP / 2.0
        y_in = min(side(x0), side(x1)) - SHUT_DEPTH
        pieces = [((x1 - g, x1 + g), (bottom, belt + 10.0)),
                  ((x0 - g, x0 + g), (bottom, belt + 10.0)),
                  ((x0 - g, x1 + g), (bottom - g, bottom + g))]  # fmt: skip
        if style == "lines_handles":
            hx = (x0 + 90.0, x0 + 260.0)
            hz = (belt - 110.0, belt - 80.0)
            y_h = side(sum(hx) / 2.0) - 8.0
            out += [k.box(hx, (y_h, hw + 20.0), hz), k.box(hx, (-hw - 20.0, -y_h), hz)]
        for xs, zs in pieces:
            out += [k.box(xs, (y_in, hw + 20.0), zs), k.box(xs, (-hw - 20.0, -y_in), zs)]
    return out


# --- Lower trim ---

LOWER_TRIMS = ("body", "gloss_black")
TRIM_PROUD = 4.0  # the trim stands this far proud of the body skin, mm


def lower_trim(p: Inputs) -> str:
    return _choice(p, "lower_trim", LOWER_TRIMS)


def build_lower_trim(p: Inputs) -> k.Shape | None:
    """A contrasting band round the foot of the styled body: the front splitter under the
    grille, the side skirts along the sills and the rear valance (one piece, standing
    ``TRIM_PROUD`` off the skin, cut round the wheel arches and the grille openings)."""
    from autevra.domains.automotive import builders as b
    from autevra.domains.automotive import styled

    if lower_trim(p) == "body" or not styled.styled_ok(p):
        return None
    layout = b.body_layout(p)
    floor, belt, hw = p["body_floor"], p["beltline_height"], p["body_width"] / 2.0
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    height = min(max(0.2 * (belt - floor), 70.0), 170.0)
    band = k.box((rear - 50.0, front + 50.0), (-hw - 50.0, hw + 50.0),
                 (floor - 20.0, floor + height))  # fmt: skip
    trim = k.intersect(styled.skin(p, layout, -TRIM_PROUD), band)
    wheel_z, r = p["tyre_radius"], p["arch_radius"] + TRIM_PROUD
    wells = [k.cylinder_y(r, (-hw - 60.0, hw + 60.0), x=x, z=wheel_z)
             for x in (0.0, -p["wheelbase"])]  # fmt: skip
    # Only a band round the edge: the floor in between stays the body's.
    inner = k.box((rear + 220.0, front - 260.0), (-hw + 130.0, hw - 130.0),
                  (floor - 30.0, floor + height + 1.0))  # fmt: skip
    trim = k.cut(trim, inner, *wells, *grille_tools(p, layout))
    return trim if k.solid_count(trim) else None


# --- Brakes ---


def _brake_frame(p: Inputs) -> tuple[float, tuple[float, float]]:
    """Disc outer radius and its y extent (wheel frame), inside the rim and inboard of the
    spoke face."""
    face_r = p["rim_radius"] - RIM_BARREL
    face_inner = p["tyre_width"] / 2.0 * 0.95 - FACE_THICKNESS - FACE_SET
    disc_r = face_r - 30.0
    thickness = min(32.0, 0.12 * disc_r)
    return disc_r, (face_inner - 14.0 - thickness, face_inner - 14.0)


def build_brake_disc(p: Inputs) -> k.Shape:
    """Ventilated-looking disc: a ring with a hat that reaches out to the hub face."""
    disc_r, y = _brake_frame(p)
    ring = k.ring_y(disc_r, 0.55 * disc_r, y)
    hat = k.ring_y(0.58 * disc_r, AXLE_RADIUS + 8.0, (y[0] + 4.0, y[1] + 12.0))
    groove = k.ring_y(0.70 * disc_r, 0.68 * disc_r, (y[1] - 1.0, y[1] + 1.0))
    return k.cut(k.fuse(ring, hat), groove)


def build_brake_caliper(p: Inputs) -> k.Shape:
    """Caliper straddling the top of the disc: an annular sector reaching over the disc's
    edge, its bridge kept inside the rim barrel."""
    disc_r, (y0, y1) = _brake_frame(p)
    span = math.radians(26.0)
    r_out = disc_r + 16.0
    wedge = k.prism_y([(0.0, 0.0), (2 * r_out * math.sin(-span), 2 * r_out * math.cos(span)),
                       (2 * r_out * math.sin(span), 2 * r_out * math.cos(span))],
                      (y0 - 24.0, y1 + 10.0))  # fmt: skip
    body = k.intersect(k.ring_y(r_out, disc_r - 52.0, (y0 - 24.0, y1 + 10.0)), wedge)
    slot = k.ring_y(disc_r + 3.0, disc_r - 55.0, (y0 - 2.0, y1 + 2.0))  # the disc runs here
    return k.cut(body, slot)
