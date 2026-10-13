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


def body_profile(p: Inputs) -> list[tuple[float, float]]:
    """Side profile (x, z) of the lower body: bumper, nose, hood rising to the windscreen
    cowl, beltline, rear deck and tail. Proportions follow the design parameters."""
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    floor, belt = p["body_floor"], p["beltline_height"]
    depth = belt - floor
    centre = (rear + front) / 2.0 + p["cabin_offset"]
    cowl = min(centre + p["cabin_length"] / 2.0, front - 150.0)  # windscreen base
    deck = max(centre - p["cabin_length"] / 2.0, rear + 150.0)  # rear screen base
    arch_top = p["tyre_radius"] + p["arch_radius"]
    # The hood stays above the front wheel arch, below the beltline.
    nose = min(max(floor + 0.62 * depth, arch_top + 40.0), belt - 20.0)
    tail = min(max(floor + 0.78 * depth, arch_top + 40.0), belt - 10.0)
    bumper = floor + 0.25 * depth
    under = min(0.06 * (front - rear), 220.0)
    return [
        (rear + under * 0.6, floor),
        (front - under, floor),
        (front, bumper),
        (front, nose),
        (cowl, belt),
        (deck, belt),
        (rear, tail),
        (rear, floor + 0.3 * depth),
    ]


def build_body(p: Inputs) -> k.Shape:
    """Lower body (side profile x rounded plan view) with wheel wells, plus a raked,
    tapered greenhouse. Extents: overhang to overhang, full width, floor to roof."""
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    half_w = p["body_width"] / 2.0
    floor, belt, roof = p["body_floor"], p["beltline_height"], p["overall_height"]

    side = k.prism_y(body_profile(p), (-half_w, half_w))
    plan = k.prism_z(
        _rounded_outline((rear, front), half_w, 0.32 * half_w, 0.18 * half_w),
        (floor - 1.0, belt + 1.0),
    )
    lower = k.intersect(side, plan)

    # Wheel wells: cylinders around each wheel, cut from the tyre's inner face outwards.
    wheel_z = p["tyre_radius"]
    r = p["arch_radius"]
    wells = []
    for x, track in ((0.0, p["track_front"]), (-p["wheelbase"], p["track_rear"])):
        inner = track / 2.0 - p["tyre_width"] / 2.0 - p["arch_clearance"]
        wells.append(k.cylinder_y(r, (inner, half_w + 1), x=x, z=wheel_z))
        wells.append(k.cylinder_y(r, (-half_w - 1, -inner), x=x, z=wheel_z))
    lower = k.cut(lower, *wells)

    # Greenhouse: ruled loft from the beltline outline to the roof outline; the corners are
    # chamfered so the glasshouse reads as rounded, and the roof is narrower (tumblehome).
    centre = (rear + front) / 2.0 + p["cabin_offset"]
    cab_half, roof_half = p["cabin_length"] / 2.0, p["roof_length"] / 2.0
    cab_w, roof_w = half_w - 40.0, half_w - 150.0

    def outline(z: float, half_len: float, half_wid: float) -> list[tuple[float, float, float]]:
        c = min(0.18 * half_wid, 0.25 * half_len)  # corner chamfer
        return [
            (centre - half_len, -half_wid + c, z), (centre - half_len + c, -half_wid, z),
            (centre + half_len - c, -half_wid, z), (centre + half_len, -half_wid + c, z),
            (centre + half_len, half_wid - c, z), (centre + half_len - c, half_wid, z),
            (centre - half_len + c, half_wid, z), (centre - half_len, half_wid - c, z),
        ]  # fmt: skip

    cabin = k.ruled_loft([outline(belt, cab_half, cab_w), outline(roof, roof_half, roof_w)])
    return k.fuse(lower, cabin)


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
