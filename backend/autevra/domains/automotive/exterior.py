"""Exterior options: door mirrors, roof rails, spoilers and a tow bar, placed from the body
style's greenhouse and side profile (vehicle frame, mm, ISO 8855). The roof opening for a
panoramic roof or sunroof is cut from the body itself (``roof_opening``).

These are representative styling and packaging envelopes. The body dimensions keep their
definitions: body width excludes the mirrors, overall height is to the roof panel (rails
and spoilers excluded) and overall length excludes the tow bar; the derived width over the
mirrors reports the mirrors' reach. No aerodynamic effect of a spoiler and no towing
capacity are modelled.
"""

from collections.abc import Mapping

import cadquery as cq

from autevra.cad import kernel as k
from autevra.domains.automotive import builders as b

Inputs = Mapping[str, float]

ROOF_TYPES = ("solid", "panoramic", "sunroof")
ROOF_RAILS = ("none", "rails", "crossbars")
SPOILERS = ("none", "roof", "boot_lip", "wing")
BOOT_STYLES = ("sedan", "coupe")  # styles with a boot deck for a lip or a wing
MIRRORS = ("conventional", "camera")
MIRROR_REACH = {"conventional": 210.0, "camera": 130.0}  # beyond the body side, mm
BALL_HEIGHT = 400.0  # typical tow ball centre height above the ground, mm (not a standard)


def _choice(p: Inputs, key: str, names: tuple[str, ...]) -> str:
    return names[min(max(int(round(p.get(key, 0))), 0), len(names) - 1)]


def roof_type(p: Inputs) -> str:
    return _choice(p, "roof_type", ROOF_TYPES)


def spoiler(p: Inputs) -> str:
    return _choice(p, "rear_spoiler", SPOILERS)


def mirror_type(p: Inputs) -> str:
    return _choice(p, "mirror_type", MIRRORS)


def roof_opening(p: Inputs, layout: b.BodyLayout) -> tuple[tuple[float, float], ...] | None:
    """Box cut from the roof panel for a panoramic roof or a sunroof (the glazing below
    shows through), or None for a solid roof."""
    kind = roof_type(p)
    if kind == "solid":
        return None
    (r0, r1), top = layout.roof, layout.roof_z
    roof_w = p["body_width"] / 2.0 - 150.0
    x0, x1 = r0 + b.PILLAR + 40.0, r1 - b.PILLAR - 40.0
    half = roof_w - b.PILLAR - 30.0
    if kind == "sunroof":  # a smaller panel over the front seats
        x0, half = max(x0, x1 - min(700.0, 0.45 * (r1 - r0))), min(0.55 * roof_w, 450.0)
    if x1 - x0 < 200.0:
        return None  # roof too short for an opening
    return ((x0, x1), (-half, half), (top - b.PILLAR - 1.0, top + 1.0))


def _mirror_x(layout: b.BodyLayout) -> float:
    """Mirrors sit on the A-pillar base, between the windscreen base and the side window."""
    (_, g1), (_, r1) = layout.glass, layout.roof
    return min(g1 - 80.0, max((g1 + r1) / 2.0, r1 - b.PILLAR + 70.0))


def build_mirrors(p: Inputs) -> k.Shape:
    layout = b.body_layout(p)
    xm, belt = _mirror_x(layout), p["beltline_height"]
    side = p["body_width"] / 2.0 - 40.0  # greenhouse side at the beltline
    reach = MIRROR_REACH[mirror_type(p)]
    parts = []
    for s in (1.0, -1.0):

        def y(a: float, c: float, s: float = s) -> tuple[float, float]:
            return tuple(sorted((s * a, s * c)))  # type: ignore[return-value]

        if mirror_type(p) == "camera":  # slim stalk and a camera pod
            parts.append(k.box((xm - 25.0, xm + 25.0), y(side - 40.0, side + reach - 50.0),
                               (belt + 55.0, belt + 80.0)))  # fmt: skip
            parts.append(k.box((xm - 40.0, xm + 45.0), y(side + reach - 70.0, side + reach),
                               (belt + 45.0, belt + 95.0)))  # fmt: skip
        else:  # arm and housing
            parts.append(k.box((xm - 30.0, xm + 30.0), y(side - 40.0, side + 60.0),
                               (belt + 40.0, belt + 80.0)))  # fmt: skip
            parts.append(k.box((xm - 60.0, xm + 60.0), y(side + 40.0, side + reach),
                               (belt + 30.0, belt + 180.0)))  # fmt: skip
    return k.fuse(*parts)


def build_roof_rails(p: Inputs) -> k.Shape | None:
    kind = _choice(p, "roof_rails", ROOF_RAILS)
    if kind == "none":
        return None
    layout = b.body_layout(p)
    (r0, r1), top = layout.roof, layout.roof_z
    y_rail = p["body_width"] / 2.0 - 150.0 - 70.0
    x0, x1 = r0 + 80.0, r1 - 80.0
    if x1 - x0 < 300.0:
        return None  # roof too short for rails
    parts = []
    for s in (1.0, -1.0):
        y = (s * y_rail - 15.0, s * y_rail + 15.0)
        parts.append(k.box((x0, x1), y, (top + 30.0, top + 55.0)))
        for x in (x0, x1 - 80.0):  # feet into the roof panel
            parts.append(k.box((x, x + 80.0), y, (top - 10.0, top + 31.0)))
    if kind == "crossbars":
        for share in (0.3, 0.7):
            x = x0 + share * (x1 - x0)
            parts.append(k.box((x - 20.0, x + 20.0), (-y_rail - 15.0, y_rail + 15.0),
                               (top + 54.0, top + 80.0)))  # fmt: skip
    return k.fuse(*parts)


def _tail_top(p: Inputs, layout: b.BodyLayout) -> float:
    rear = -(p["wheelbase"] + p["rear_overhang"])
    return max(z for x, z in layout.profile if abs(x - rear) < 1e-6)


def build_spoiler(p: Inputs) -> k.Shape | None:
    """Roof spoiler at the rear edge of the roof (a cab-top air deflector on a box truck),
    or a boot lip or wing on a sedan or coupe deck (other styles: not fitted, and a design
    rule reports it)."""
    kind = spoiler(p)
    if kind == "none":
        return None
    layout = b.body_layout(p)
    half_w = p["body_width"] / 2.0
    rear = -(p["wheelbase"] + p["rear_overhang"])
    (r0, r1), top = layout.roof, layout.roof_z
    if kind == "roof":
        y = (-(half_w - 180.0), half_w - 180.0)
        if layout.cargo is not None:  # deflector from the cab roof up to the box top
            box_top = p["overall_height"]
            return k.prism_y([(r1 - 100.0, top - 5.0), (r0 + 30.0, top - 5.0),
                              (r0 + 30.0, box_top - 20.0)], y)  # fmt: skip
        return k.prism_y([(r0 + 150.0, top - 5.0), (r0 + 150.0, top + 10.0),
                          (r0 - 150.0, top + 25.0), (r0 - 150.0, top + 5.0)], y)  # fmt: skip
    if layout.style not in BOOT_STYLES:
        return None
    tail = _tail_top(p, layout)
    if kind == "boot_lip":
        return k.prism_y([(rear + 200.0, tail - 3.0), (rear + 200.0, tail + 3.0),
                          (rear + 15.0, tail + 35.0), (rear + 15.0, tail - 3.0)],
                         (-(half_w - 120.0), half_w - 120.0))  # fmt: skip
    parts = [
        k.prism_y([(rear + 40.0, tail + 180.0), (rear + 300.0, tail + 195.0),
                   (rear + 300.0, tail + 205.0), (rear + 40.0, tail + 215.0)],
                  (-(half_w - 100.0), half_w - 100.0)),
    ]  # fmt: skip
    for s in (1.0, -1.0):  # posts from the deck to the wing
        y = s * 0.55 * half_w
        parts.append(k.box((rear + 130.0, rear + 170.0), (y - 10.0, y + 10.0),
                           (tail - 10.0, tail + 190.0)))  # fmt: skip
    return k.fuse(*parts)


def build_tow_bar(p: Inputs) -> k.Shape | None:
    """Neck from inside the rear bumper to a ball at about BALL_HEIGHT; a drop plate brings
    the ball down on a high body."""
    if int(round(p.get("tow_bar", 0))) == 0:
        return None
    rear = -(p["wheelbase"] + p["rear_overhang"])
    zn = max(p["body_floor"] + 40.0, BALL_HEIGHT - 60.0)  # neck centre, inside the body
    parts = [k.box((rear - 130.0, rear + 120.0), (-22.0, 22.0), (zn - 20.0, zn + 20.0))]
    base = zn
    if zn > BALL_HEIGHT - 40.0:  # drop plate down to the ball platform
        base = BALL_HEIGHT - 60.0
        parts.append(k.box((rear - 150.0, rear - 90.0), (-22.0, 22.0), (base - 20.0, zn + 20.0)))
    x_ball = rear - 120.0
    parts.append(k.cylinder_z(12.0, (base + 15.0, base + 50.0), x=x_ball))
    parts.append(cq.Solid.makeSphere(25.0, cq.Vector(x_ball, 0.0, base + 60.0), angleDegrees1=-90))
    return k.fuse(*parts)


def width_over_mirrors(p: Inputs) -> float:
    return p["body_width"] - 80.0 + 2.0 * MIRROR_REACH[mirror_type(p)]
