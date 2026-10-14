"""Suspension linkages by type, in the axle frame (origin on the axle centre line at wheel
centre height; X forward, Y left, Z up; ISO 8855).

The hub interfaces (wheel mounting) and the damper mounts are the same for every type, so
the wheels, coil-over dampers and the ride simulations are unchanged: the type sets the
linkage geometry shown and exported. The ride models treat every type as a vertical corner
(no camber, toe or anti-geometry); that is a stated limitation.
"""

from collections.abc import Mapping

import cadquery as cq

from autevra.cad import kernel as k
from autevra.domains.automotive.derived import AXLE_RADIUS

Inputs = Mapping[str, float]
HUB_INSET = 60.0  # the hub carrier sits this far inboard of the wheel centre plane, mm
FRONT_TYPES = ("beam", "macpherson", "double_wishbone", "multilink")
REAR_TYPES = ("beam", "twist_beam", "multilink", "double_wishbone")


def kind(p: Inputs) -> str:
    types = FRONT_TYPES if p["axle"] == 0 else REAR_TYPES
    return types[min(max(int(round(p["suspension"])), 0), len(types) - 1)]


def _rod(a: tuple[float, float, float], b: tuple[float, float, float], r: float) -> k.Shape:
    va, vb = cq.Vector(*a), cq.Vector(*b)
    axis = vb - va
    return cq.Solid.makeCylinder(r, axis.Length, va, axis.normalized())


def _knuckle(y: float) -> k.Shape:
    return k.box((-55.0, 55.0), (y - 35.0 if y > 0 else y - 5.0, y + 5.0 if y > 0 else y + 35.0),
                 (-150.0, 150.0))  # fmt: skip


def _perch(y_shock: float, z_arm: float) -> k.Shape:
    """Spring-and-damper perch from the arm up to the damper's lower mount."""
    return _rod((0.0, y_shock, z_arm), (0.0, y_shock, AXLE_RADIUS), 16.0)


def build_suspension(p: Inputs) -> k.Shape:
    t = kind(p)
    half = p["track"] / 2.0 - HUB_INSET
    if t == "beam":
        return k.cylinder_y(AXLE_RADIUS, (-half, half))
    inner = p["rail_spacing"] / 2.0 - 70.0  # inboard pivots on the frame or subframe
    shock = p["rail_spacing"] / 2.0
    parts: list[k.Shape] = []
    for s in (1.0, -1.0):
        y_k, y_i, y_s = s * (half - 20.0), s * inner, s * shock
        parts.append(_knuckle(s * half))
        if t == "twist_beam":  # trailing arm from a front pivot to the hub carrier
            parts.append(_rod((420.0, s * (inner + 40.0), -20.0), (0.0, y_k, -20.0), 30.0))
            parts.append(_rod((0.0, s * (shock - 40.0), -20.0), (0.0, y_k, -20.0), 22.0))  # seat
            parts.append(_perch(y_s, -20.0))
            continue
        z_low = -115.0
        lower_front = _rod((170.0, y_i, z_low), (0.0, y_k, z_low), 18.0)
        lower_rear = _rod((-170.0, y_i, z_low), (0.0, y_k, z_low), 18.0)
        seat = _rod((0.0, s * (shock - 40.0), z_low), (0.0, y_k, z_low), 20.0)  # spring seat link
        parts += [lower_front, lower_rear, seat, _perch(y_s, z_low)]
        if t == "macpherson":  # tie rod to the steering rack
            parts.append(_rod((-140.0, y_i, -40.0), (-45.0, y_k, -40.0), 11.0))
        if t == "double_wishbone":
            z_up = 120.0
            parts.append(_rod((140.0, y_i, z_up), (0.0, y_k, z_up), 15.0))
            parts.append(_rod((-140.0, y_i, z_up), (0.0, y_k, z_up), 15.0))
        if t == "multilink":
            for a, b in (((180.0, y_i, 110.0), (20.0, y_k, 115.0)),
                         ((-180.0, y_i, 100.0), (-20.0, y_k, 110.0)),
                         ((-150.0, y_i, -40.0), (-45.0, y_k, -40.0))):  # fmt: skip
                parts.append(_rod(a, b, 12.0))
    if t == "twist_beam":  # torsion beam joining the arms, reaching into each arm
        x = 240.0
        y_arm = (inner + 40.0) + (420.0 - x) / 420.0 * ((half - 20.0) - (inner + 40.0))
        parts.append(k.cylinder_y(40.0, (-(y_arm + 10.0), y_arm + 10.0), x=x, z=-20.0))
    first, *rest = parts
    return k.fuse(first, *rest)
