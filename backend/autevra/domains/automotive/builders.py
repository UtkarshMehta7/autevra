"""Component builders: pure functions ``inputs -> solid`` in the component's local frame.

Each builder takes a mapping of named inputs (already resolved from design
parameters by the assembly layer) and returns a kernel shape. Builders never
see the full design, so their dependencies are exactly their inputs.

Local frames:
- body, frame: vehicle frame (ISO 8855, origin on the ground below the front axle).
- axle: origin at the axle centre, axis along Y.
- wheel: origin at the wheel centre, spin axis along Y, outboard face towards +Y.
- damper: origin at the lower eye centre, axis along +Z, upper eye at z = length.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass

from autevra.cad import kernel as k
from autevra.domains.automotive.derived import AXLE_RADIUS, SPRING_ACTIVE_COILS, SPRING_SEAT_OFFSET

Inputs = Mapping[str, float]
HUB_INSET = 60.0  # axle ends this far inboard of the wheel centre plane
RIM_BARREL = 12.0  # radial thickness of the rim barrel
SPOKES = 5


def _rounded_outline(
    x: tuple[float, float], half_w: float, r_front: float, r_rear: float, n: int = 6
) -> list[tuple[float, float]]:
    """Plan-view outline (x, y) of a rectangle whose four corners are rounded."""
    rear, front = x
    pts: list[tuple[float, float]] = []
    for cx, cy, r, a0 in (
        (front - r_front, half_w - r_front, r_front, 0.0),  # front left
        (rear + r_rear, half_w - r_rear, r_rear, 90.0),  # rear left
        (rear + r_rear, -half_w + r_rear, r_rear, 180.0),  # rear right
        (front - r_front, -half_w + r_front, r_front, 270.0),  # front right
    ):
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# Body styles, in the order of the ``body_style`` parameter's options.
BODY_STYLES = ("sedan", "hatchback", "suv", "coupe", "pickup", "van", "box_truck")


def body_style(p: Inputs) -> str:
    index = int(round(p.get("body_style", 0.0)))
    return BODY_STYLES[min(max(index, 0), len(BODY_STYLES) - 1)]


@dataclass(frozen=True)
class BodyLayout:
    """Where the parts of a body style sit (vehicle frame, mm). ``build_body`` turns it
    into solids; tests check the proportions without building CAD."""

    style: str
    profile: list[tuple[float, float]]  # side profile (x, z) of the lower body
    glass: tuple[float, float]  # greenhouse x extent at the beltline (rear, front)
    roof: tuple[float, float]  # roof panel x extent (rear, front)
    roof_z: float
    bed: tuple[tuple[float, float], float] | None = None  # open bed: x extent, floor z
    cargo: tuple[float, float] | None = None  # closed cargo box x extent (floor to roof)


def body_layout(p: Inputs) -> BodyLayout:
    """Proportions of each style from the design parameters.

    Cabin length, roof length and cabin offset place the greenhouse for the car styles
    and the cab of a pickup. A van's greenhouse spans the body and a box truck's cab is
    sized from the cabin length; their windscreens rise from a short nose.
    """
    style = body_style(p)
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    length = front - rear
    floor, belt, top = p["body_floor"], p["beltline_height"], p["overall_height"]
    depth, glass_h = belt - floor, top - belt
    centre = (rear + front) / 2.0 + p["cabin_offset"]
    # The wheel arches shape only the lower profile; the glazing is built without them.
    arch_top = p.get("tyre_radius", 0.0) + p.get("arch_radius", 0.0)
    under = min(0.06 * length, 220.0)
    bumper = floor + 0.25 * depth
    tail_low = floor + 0.3 * depth

    def nose_at(share: float) -> float:  # hood height at the nose, above the front arch
        return min(max(floor + share * depth, arch_top + 40.0), belt - 20.0)

    cowl = min(centre + p["cabin_length"] / 2.0, front - 150.0)  # windscreen base
    deck = max(centre - p["cabin_length"] / 2.0, rear + 150.0)  # rear screen base
    rake = max((p["cabin_length"] - p["roof_length"]) / 2.0, 0.25 * glass_h)  # windscreen run
    front_end = [(rear + under * 0.6, floor), (front - under, floor), (front, bumper)]

    def clamp_roof(r0: float, r1: float) -> tuple[float, float]:
        r1 = max(r1, r0 + 300.0)
        return (r0, r1)

    if style == "sedan":
        tail = min(max(floor + 0.78 * depth, arch_top + 40.0), belt - 10.0)
        roof = (centre - p["roof_length"] / 2.0, centre + p["roof_length"] / 2.0)
        profile = [*front_end, (front, nose_at(0.62)), (cowl, belt), (deck, belt),
                   (rear, tail), (rear, tail_low)]  # fmt: skip
        return BodyLayout(style, profile, (deck, cowl), roof, top)

    if style in ("hatchback", "suv"):
        upright = style == "suv"
        back = rear + 60.0
        roof = clamp_roof(back + (0.12 if upright else 0.45) * glass_h, cowl - rake)
        profile = [*front_end, (front, nose_at(0.8 if upright else 0.62)), (cowl, belt),
                   (back, belt), (rear, belt - 60.0), (rear, tail_low)]  # fmt: skip
        return BodyLayout(style, profile, (back, cowl), roof, top)

    if style == "coupe":
        # Fastback: a full roof, then a long, shallow rear screen running far towards the tail.
        tail = min(max(floor + 0.82 * depth, arch_top + 40.0), belt - 10.0)
        roof_front = cowl - rake
        roof = clamp_roof(roof_front - p["roof_length"], roof_front)
        back = max(rear + 0.12 * length, min(deck, roof[0]) - 1.2 * glass_h)
        profile = [*front_end, (front, nose_at(0.55)), (cowl, belt), (back, belt),
                   (rear, tail), (rear, tail_low)]  # fmt: skip
        return BodyLayout(style, profile, (back, cowl), roof, top)

    if style == "pickup":
        cab_rear = deck
        roof = clamp_roof(cab_rear + 40.0, cowl - rake)
        bed_floor = min(max(floor + 0.3 * depth, arch_top + 20.0), belt - 120.0)
        profile = [*front_end, (front, nose_at(0.75)), (cowl, belt), (rear, belt),
                   (rear, tail_low)]  # fmt: skip
        return BodyLayout(style, profile, (cab_rear, cowl), roof, top,
                          bed=((rear + 50.0, cab_rear - 60.0), bed_floor))  # fmt: skip

    # Van and box truck: short nose, long raked windscreen.
    cowl = front - max(250.0, 0.45 * p["front_overhang"])
    screen = 0.55 * glass_h
    profile_front = [*front_end, (front, nose_at(0.75)), (cowl, belt)]
    if style == "van":
        profile = [*profile_front, (rear, belt), (rear, tail_low)]
        roof = clamp_roof(rear + 60.0, cowl - screen)
        return BodyLayout(style, profile, (rear + 40.0, cowl), roof, top)

    cab_depth = min(max(0.5 * p["cabin_length"], 1300.0), 0.4 * length)
    cab_rear = cowl - cab_depth
    cab_top = top - 0.15 * glass_h  # the cargo box stands above the cab
    profile = [*profile_front, (cab_rear, belt), (cab_rear, tail_low)]
    roof = clamp_roof(cab_rear + 30.0, cowl - 0.45 * (cab_top - belt))
    return BodyLayout(style, profile, (cab_rear, cowl), roof, cab_top,
                      cargo=(rear, cab_rear - 80.0))  # fmt: skip


def body_profile(p: Inputs) -> list[tuple[float, float]]:
    """Side profile (x, z) of the lower body for the design's body style."""
    return body_layout(p).profile


PILLAR = 70.0  # pillar and roof-rail width left around the window openings, mm
GLASS_INSET = 25.0  # glazing sits this far inside the greenhouse surface, mm


def _greenhouse(p: Inputs, layout: BodyLayout, inset: float = 0.0) -> k.Shape:
    """Ruled loft from the beltline outline to the roof outline; the corners are chamfered
    so the glasshouse reads as rounded, and the roof is narrower (tumblehome)."""
    half_w = p["body_width"] / 2.0
    belt = p["beltline_height"]
    cab_w, roof_w = half_w - 40.0 - inset, half_w - 150.0 - inset

    def outline(
        z: float, x: tuple[float, float], half_wid: float
    ) -> list[tuple[float, float, float]]:
        r, f = x[0] + inset, x[1] - inset
        c = min(0.18 * half_wid, 0.25 * (f - r) / 2.0)  # corner chamfer
        return [
            (r, -half_wid + c, z), (r + c, -half_wid, z), (f - c, -half_wid, z),
            (f, -half_wid + c, z), (f, half_wid - c, z), (f - c, half_wid, z),
            (r + c, half_wid, z), (r, half_wid - c, z),
        ]  # fmt: skip

    top = layout.roof_z - inset
    return k.ruled_loft([outline(belt, layout.glass, cab_w), outline(top, layout.roof, roof_w)])


def _window_frame(p: Inputs, layout: BodyLayout) -> k.Shape:
    """The greenhouse with the side windows, windscreen and rear screen cut out, leaving
    the pillars and the roof; the glazing component fills the openings from inside."""
    half_w = p["body_width"] / 2.0
    belt, top = p["beltline_height"], layout.roof_z
    z = (belt + PILLAR * 0.6, top - PILLAR)
    roof_w = half_w - 150.0
    (g0, g1), (r0, r1) = layout.glass, layout.roof
    side = k.box((r0 + PILLAR, r1 - PILLAR), (-half_w - 10.0, half_w + 10.0), z)
    screens = [
        k.box((r1 - 1.0, g1 + 10.0), (-roof_w + PILLAR, roof_w - PILLAR), z),  # windscreen
        k.box((g0 - 10.0, r0 + 1.0), (-roof_w + PILLAR, roof_w - PILLAR), z),  # rear screen
    ]
    return k.cut(_greenhouse(p, layout), side, *screens)


def build_glass(p: Inputs) -> k.Shape:
    """Glazing: the greenhouse volume just inside the body's window openings."""
    return _greenhouse(p, body_layout(p), inset=GLASS_INSET)


LAMP_DEPTH = 15.0  # lamps sit in recesses this deep, flush with the body face, mm


def lamp_boxes(p: Inputs, end: str) -> list[tuple[tuple[float, float], ...]]:
    """(x, y, z) extents of the two lamps at the front ("head") or rear ("tail") face,
    placed on the flat part of that face between the rounded corners. The body is
    recessed by the same boxes, so the lamps are flush and the extents do not change."""
    layout = body_layout(p)
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    half_w = p["body_width"] / 2.0
    floor, belt = p["body_floor"], p["beltline_height"]
    if end == "head":
        bumper, nose = layout.profile[2][1], layout.profile[3][1]
        h = nose - bumper
        z = (bumper + 0.45 * h, nose - 0.1 * h)
        x = (front - LAMP_DEPTH, front)
        y_in, y_out = 0.30 * half_w, 0.62 * half_w
    else:
        at_rear = [zz for xx, zz in layout.profile if abs(xx - rear) < 1e-6]
        top, bottom = (max(at_rear), min(at_rear)) if at_rear else (floor, floor)
        if layout.cargo is not None or top - bottom < 60.0:  # box truck: low on the box
            bottom, top = floor + 0.25 * (belt - floor), floor + 0.55 * (belt - floor)
        h = top - bottom
        z = (top - 0.5 * h, top - 0.15 * h)
        x = (rear, rear + LAMP_DEPTH)
        y_in, y_out = 0.50 * half_w, 0.76 * half_w
    return [(x, (y_in, y_out), z), (x, (-y_out, -y_in), z)]


def build_lamps(p: Inputs, end: str) -> k.Shape:
    left, right = (k.box(*b) for b in lamp_boxes(p, end))
    return k.fuse(left, right)


def build_head_lamps(p: Inputs) -> k.Shape:
    return build_lamps(p, "head")


def build_tail_lamps(p: Inputs) -> k.Shape:
    return build_lamps(p, "tail")


def build_body(p: Inputs) -> k.Shape:
    """Lower body (side profile x rounded plan view) and the window frame of a raked, tapered
    greenhouse, shaped by the body style (an open bed for a pickup, a cargo box for a box
    truck), with wheel wells. Extents: overhang to overhang, full width, floor to roof."""
    layout = body_layout(p)
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    half_w = p["body_width"] / 2.0
    floor, belt = p["body_floor"], p["beltline_height"]
    square_back = layout.style in ("pickup", "van", "box_truck", "suv")

    side = k.prism_y(layout.profile, (-half_w, half_w))
    plan = k.prism_z(
        _rounded_outline(
            (rear, front), half_w, 0.32 * half_w, (0.08 if square_back else 0.18) * half_w
        ),
        (floor - 1.0, belt + 1.0),
    )
    parts = [k.intersect(side, plan)]

    parts.append(_window_frame(p, layout))
    if layout.cargo is not None:
        parts.append(k.box(layout.cargo, (-half_w, half_w), (floor, p["overall_height"])))
    body = k.fuse(*parts)

    if layout.bed is not None:
        (b0, b1), bed_floor = layout.bed
        body = k.cut(
            body, k.box((b0, b1), (-half_w + 50.0, half_w - 50.0), (bed_floor, belt + 5.0))
        )

    lamps = [k.box(*b) for end in ("head", "tail") for b in lamp_boxes(p, end)]
    body = k.cut(body, *lamps)

    # Wheel wells: cylinders around each wheel, cut from the tyre's inner face outwards.
    wheel_z = p["tyre_radius"]
    r = p["arch_radius"]
    wells = []
    for x, track in ((0.0, p["track_front"]), (-p["wheelbase"], p["track_rear"])):
        inner = track / 2.0 - p["tyre_width"] / 2.0 - p["arch_clearance"]
        wells.append(k.cylinder_y(r, (inner, half_w + 1), x=x, z=wheel_z))
        wells.append(k.cylinder_y(r, (-half_w - 1, -inner), x=x, z=wheel_z))
    return k.cut(body, *wells)


def build_frame(p: Inputs) -> k.Shape:
    """Ladder frame: two hollow rectangular rails joined by hollow cross members."""
    front = p["front_overhang"] - 150.0
    rear = -(p["wheelbase"] + p["rear_overhang"] - 150.0)
    w, h, t = p["rail_width"], p["rail_height"], p["rail_wall"]
    z = (p["ground_clearance"], p["ground_clearance"] + h)
    half = p["rail_spacing"] / 2.0

    rails = [k.rect_tube_x((rear, front), (y - w / 2, y + w / 2), z, t) for y in (half, -half)]

    # Cross members between the rails' inner faces: both ends, and evenly in between.
    inner = half - w / 2.0
    cm_depth = w  # cross member extent along X
    count = 5
    xs = [rear + (front - rear - cm_depth) * i / (count - 1) for i in range(count)]
    members = [k.rect_tube_y((x, x + cm_depth), (-inner, inner), z, t) for x in xs]
    return k.fuse(rails[0], rails[1], *members)


def build_axle(p: Inputs) -> k.Shape:
    """Beam axle along Y, ending just inboard of each wheel centre plane."""
    half = p["track"] / 2.0 - HUB_INSET
    return k.cylinder_y(AXLE_RADIUS, (-half, half))


def build_wheel(p: Inputs) -> k.Shape:
    """Tyre and rim as one solid: filleted tyre ring, rim barrel and a spoked disc."""
    tyre_r = p["tyre_radius"]
    rim_r = p["rim_radius"]
    width = p["tyre_width"]
    sidewall = tyre_r - rim_r
    half = width / 2.0

    tyre = k.ring_y(tyre_r, rim_r, (-half, half))
    tyre = k.fillet_circular_edges_outer(tyre, tyre_r, min(sidewall * 0.45, half * 0.6))

    barrel = k.ring_y(rim_r, rim_r - RIM_BARREL, (-half * 0.95, half * 0.95))

    disc_t = 18.0
    disc_y = half * 0.95 - disc_t - 15.0  # dish: the face sits slightly inboard of the outer edge
    disc = k.cylinder_y(rim_r - RIM_BARREL + 1, (disc_y, disc_y + disc_t))
    hole_r = (rim_r - RIM_BARREL) * 0.22
    pitch = (rim_r - RIM_BARREL) * 0.58
    holes = [
        k.cylinder_y(
            hole_r,
            (disc_y - 1, disc_y + disc_t + 1),
            x=pitch * math.cos(2 * math.pi * i / SPOKES),
            z=pitch * math.sin(2 * math.pi * i / SPOKES),
        )
        for i in range(SPOKES)
    ]
    hub_bore = k.cylinder_y(AXLE_RADIUS + 5, (disc_y - 1, disc_y + disc_t + 1))
    disc = k.cut(disc, *holes, hub_bore)
    return k.fuse(tyre, barrel, disc)


EYE_OUTER, EYE_INNER, EYE_WIDTH = 18.0, 8.0, 30.0
ROD_RADIUS = 11.0
SEAT_THICKNESS = 6.0
BODY_OVERHEAD = 35.0  # damper body length beyond the stroke (piston and seal head)


def build_damper(p: Inputs) -> k.Shape:
    """Coil-over damper: eyes, body tube, rod, spring seats and a swept helical spring.

    The spring wire diameter is an input derived from the spring rate, so a rate change
    shows as a thicker or thinner coil. Damping coefficients do not change geometry.
    """
    length, stroke = p["length"], p["stroke"]
    body_r = p["body_diameter"] / 2.0
    half_eye = EYE_WIDTH / 2.0
    lower_eye = k.ring_x(EYE_OUTER, EYE_INNER, (-half_eye, half_eye))
    upper_eye = k.ring_x(EYE_OUTER, EYE_INNER, (-half_eye, half_eye), z=length)
    body_top = EYE_OUTER + stroke + BODY_OVERHEAD
    body = k.cylinder_z(body_r, (EYE_OUTER - 4.0, body_top))
    rod = k.cylinder_z(ROD_RADIUS, (body_top, length - EYE_OUTER + 4.0))

    coil_r, wire = p["coil_diameter"] / 2.0, p["wire_diameter"]
    seat_r = coil_r + wire / 2.0 + 8.0
    low = SPRING_SEAT_OFFSET
    high = length - SPRING_SEAT_OFFSET
    seats = [
        k.ring_z(seat_r, body_r - 1.0, (low - SEAT_THICKNESS, low)),
        k.ring_z(seat_r, ROD_RADIUS - 1.0, (high, high + SEAT_THICKNESS)),
    ]
    # The end coils sink 1 mm into the seats so the spring fuses with them into one solid.
    coil = k.helical_coil(
        coil_r, high - low - wire + 2.0, SPRING_ACTIVE_COILS + 2.0, wire, low + wire / 2.0 - 1.0
    )
    return k.fuse(lower_eye, body, rod, upper_eye, *seats, coil)
