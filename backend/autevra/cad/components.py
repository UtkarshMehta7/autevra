"""Component builders: pure functions ``inputs -> solid`` in the component's local frame.

Each builder takes a mapping of named inputs (already resolved from design
parameters by the assembly layer) and returns a kernel shape. Builders never
see the full design, so their dependencies are exactly their inputs.

Local frames:
- body, frame: vehicle frame (ISO 8855, origin on the ground below the front axle).
- axle: origin at the axle centre, axis along Y.
- wheel: origin at the wheel centre, spin axis along Y, outboard face towards +Y.
"""

import math
from collections.abc import Mapping

from autevra.cad import kernel as k

Inputs = Mapping[str, float]

AXLE_RADIUS = 35.0
HUB_INSET = 60.0  # axle ends this far inboard of the wheel centre plane
RIM_BARREL = 12.0  # radial thickness of the rim barrel
SPOKES = 5


def build_body(p: Inputs) -> k.Shape:
    """Lower body with wheel wells, plus a lofted cabin (greenhouse)."""
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    half_w = p["body_width"] / 2.0
    floor, belt, roof = p["body_floor"], p["beltline_height"], p["overall_height"]

    lower = k.box((rear, front), (-half_w, half_w), (floor, belt))

    # Wheel wells: cylinders around each wheel, cut from the tyre's inner face outwards.
    wheel_z = p["tyre_radius"]
    r = p["arch_radius"]
    wells = []
    for x, track in ((0.0, p["track_front"]), (-p["wheelbase"], p["track_rear"])):
        inner = track / 2.0 - p["tyre_width"] / 2.0 - p["arch_clearance"]
        wells.append(k.cylinder_y(r, (inner, half_w + 1), x=x, z=wheel_z))
        wells.append(k.cylinder_y(r, (-half_w - 1, -inner), x=x, z=wheel_z))
    lower = k.cut(lower, *wells)

    # Cabin: ruled loft from the beltline outline to the roof outline.
    centre = (rear + front) / 2.0 + p["cabin_offset"]
    cab_half, roof_half = p["cabin_length"] / 2.0, p["roof_length"] / 2.0
    cab_w, roof_w = half_w - 40.0, half_w - 150.0

    def outline(z: float, half_len: float, half_wid: float) -> list[tuple[float, float, float]]:
        return [
            (centre - half_len, -half_wid, z),
            (centre + half_len, -half_wid, z),
            (centre + half_len, half_wid, z),
            (centre - half_len, half_wid, z),
        ]

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
