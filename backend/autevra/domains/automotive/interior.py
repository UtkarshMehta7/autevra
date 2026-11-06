"""Interior: cabin packaging and builders for seats, dashboard, steering wheel, console and
display, placed from the body style's greenhouse (vehicle frame, mm, ISO 8855).

Packaging uses allowances (stated, not measured) that are design parameters: the dashboard
zone behind the windscreen base, the pitch per seat row, the seat height and the backrest
recline. The seat shapes are representative envelopes for packaging and appearance, not
seat designs.
"""

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace

import cadquery as cq

from autevra.cad import kernel as k
from autevra.domains.automotive import builders as b

Inputs = Mapping[str, float]

DASH_ZONE = 350.0  # default dashboard depth behind the windscreen base, mm
ROW_PITCH = 850.0  # default length taken by one row of seats, mm
SEAT_HEIGHT = 280.0  # default cushion top above the cabin floor, mm
FLOOR_PAN = 90.0  # floor thickness above the body floor, mm
WALL = 80.0  # body side wall left beside the cabin, mm
RECLINE = 22.0  # default backrest angle from vertical, degrees
# Head height above the cushion top for a large adult at the default recline (allowance,
# not a standard figure): H-point about 100 mm below the cushion top, torso and head about
# 815 mm above it when reclined 25 degrees. The head height scales with the cosine of the
# recline (the torso pivots about the hip).
SEATED_HEIGHT = 715.0  # mm
TRIMS = ("standard", "comfort", "premium")


def trim(p: Inputs) -> str:
    return TRIMS[min(max(int(round(p.get("interior_trim", 1))), 0), 2)]


@dataclass(frozen=True)
class Cabin:
    rear: float  # x of the rear of the passenger space
    cowl: float  # x of the windscreen base (front of the passenger space)
    floor: float  # z of the cabin floor
    belt: float
    half_w: float  # inner half width
    roof: float  # z under the roof
    rows: int
    driver_y: float  # + left (left-hand drive), - right
    dash: float = DASH_ZONE  # dashboard zone, mm
    pitch: float = ROW_PITCH  # seat row pitch, mm
    seat: float = SEAT_HEIGHT  # cushion top above the floor (before the low-cabin cap), mm
    recline: float = RECLINE  # backrest angle from vertical, degrees


def cabin(p: Inputs) -> Cabin:
    layout = b.body_layout(p)
    g0, g1 = layout.glass
    half_w = p["body_width"] / 2.0
    lhd = int(round(p.get("driving_side", 0))) == 0
    return Cabin(
        rear=g0 + 40.0, cowl=g1, floor=p["body_floor"] + FLOOR_PAN, belt=p["beltline_height"],
        half_w=half_w - WALL - p.get("haunch", 30.0), roof=layout.roof_z - 70.0,
        rows=min(max(int(round(p.get("seat_rows", 2))), 1), 3),
        driver_y=(1.0 if lhd else -1.0) * 0.42 * half_w,
        dash=p.get("dash_zone", DASH_ZONE), pitch=p.get("row_pitch", ROW_PITCH),
        seat=p.get("seat_height", SEAT_HEIGHT), recline=p.get("seat_recline", RECLINE),
    )  # fmt: skip


def cushion_top(c: Cabin) -> float:
    return c.floor + min(c.seat, 0.28 * (c.roof - c.floor))


def seated_height(c: Cabin) -> float:
    """Head top above the cushion for a large adult at the cabin's recline, mm."""
    return SEATED_HEIGHT * math.cos(math.radians(c.recline)) / math.cos(math.radians(RECLINE))


def required_length(c: Cabin) -> float:
    return c.dash + c.pitch * c.rows


def cavity(p: Inputs) -> tuple[tuple[float, float], ...]:
    """Box cut from the body for the passenger space (x, y, z extents)."""
    c = cabin(p)
    return ((c.rear, c.cowl - 30.0), (-c.half_w, c.half_w), (c.floor, c.belt + 60.0))


def seat_positions(p: Inputs) -> list[tuple[float, float]]:
    """(x of the cushion front, y of the seat centre) for every seat, front row first."""
    c = cabin(p)
    out = []
    for row in range(c.rows):
        front = c.cowl - c.dash - c.pitch * row - 150.0
        for side in (1.0, -1.0):
            out.append((front, side * 0.42 * (c.half_w + WALL)))
    return out


def _seat(c: Cabin, x_front: float, y: float, level: str) -> k.Shape:
    """Cushion on a base, and a backrest (with headrest on posts, or integrated for Premium)
    reclined about the hinge at the rear of the cushion; one solid per seat."""
    width = 540.0 if level == "premium" else 500.0
    y0, y1 = y - width / 2, y + width / 2
    top = cushion_top(c)
    x0 = x_front - 500.0  # hinge line (rear of the cushion)
    lower = [
        k.box((x0, x_front), (y0, y1), (top - 110.0, top)),
        k.box((x_front - 420.0, x_front - 80.0), (y0 + 60.0, y1 - 60.0), (c.floor, top - 100.0)),
    ]
    # The reclined seat must clear the roof liner by 60 mm: scale the backrest (and the
    # headrest) down in a low cabin instead of letting it pass through the roof.
    head = 0.0 if level == "premium" else 240.0
    nominal = (760.0 if level == "premium" else 620.0) + head
    allowed = (c.roof - 60.0 - top) / math.cos(math.radians(c.recline))
    scale = min(1.0, allowed / nominal)
    back_h, head = (nominal - head) * scale, head * scale
    upper = [k.box((x0 - 110.0, x0), (y0, y1), (top - 40.0, top + back_h))]  # overlaps the hinge
    if head:
        for post in (y - 70.0, y + 70.0):
            upper.append(k.box((x0 - 70.0, x0 - 50.0), (post - 8.0, post + 8.0),
                               (top + back_h - 10.0, top + back_h + 0.25 * head)))  # fmt: skip
        upper.append(k.box((x0 - 100.0, x0 - 20.0), (y - 130.0, y + 130.0),
                           (top + back_h + 0.2 * head, top + back_h + head)))  # fmt: skip
    if level in ("comfort", "premium"):
        for edge in (y0, y1 - 60.0):  # side bolsters
            upper.append(k.box((x0 - 140.0, x0), (edge, edge + 60.0),
                               (top, top + 0.8 * back_h)))  # fmt: skip
            if level == "premium":
                lower.append(k.box((x0 + 20.0, x_front - 40.0), (edge, edge + 60.0),
                                   (top - 20.0, top + 50.0)))  # fmt: skip
    back = k.rotate_y(k.fuse(*upper), -c.recline, (x0, 0.0, top))
    return k.fuse(*lower, back)


def _roof_over(p: Inputs, c: Cabin) -> Callable[[float], float]:
    """Roof liner height at x: the styled roofline (which arches and falls towards a
    fastback) less the liner allowance, or the draft roof panel."""
    from autevra.domains.automotive import styled

    if styled.surface(p) != "styled":
        return lambda x: c.roof
    g = styled.guides(p, b.body_layout(p))
    return lambda x: min(c.roof, g.top(x) - 70.0)


def build_seats(p: Inputs) -> k.Shape:
    c, level = cabin(p), trim(p)
    roof_at = _roof_over(p, c)
    # Each seat is sized for the roof above its backrest (a 2+2 under a fastback gets
    # lower rear backrests instead of passing through the roof).
    seats = [_seat(replace(c, roof=roof_at(x - 560.0)), x, y, level) for x, y in seat_positions(p)]
    first, *rest = seats
    return k.fuse(first, *rest) if rest else first


def build_dashboard(p: Inputs) -> k.Shape:
    c = cabin(p)
    x = (c.cowl - c.dash - 30.0, c.cowl - 30.0)
    top = c.belt + 40.0
    dash = k.box(x, (-c.half_w, c.half_w), (top - 280.0, top))
    # Knee room: a recess under the dash across the front seats.
    recess = k.box((x[0] - 1.0, x[0] + 140.0), (-c.half_w + 40.0, c.half_w - 40.0),
                   (top - 281.0, top - 160.0))  # fmt: skip
    return k.cut(dash, recess)


def build_display(p: Inputs) -> k.Shape:
    """Central display on the dashboard face; Premium adds a wide screen across to the driver
    and an ambient light line along the dashboard."""
    c, level = cabin(p), trim(p)
    face = c.cowl - c.dash - 30.0
    top = c.belt + 40.0
    if level == "premium":
        side = math.copysign(1.0, c.driver_y)  # +1 left-hand drive
        # From just past the centre on the passenger side to beyond the driver's wheel.
        y0, y1 = sorted((-side * 0.15 * c.half_w, c.driver_y + side * 260.0))
        screen = k.box((face - 18.0, face), (y0, y1), (top + 5.0, top + 145.0))
        ambient = k.box((face - 6.0, face), (-c.half_w + 60.0, c.half_w - 60.0),
                        (top - 120.0, top - 108.0))  # fmt: skip
        return k.fuse(screen, ambient)
    width = 300.0 if level == "comfort" else 200.0
    return k.box((face - 18.0, face), (-width / 2, width / 2), (top + 5.0, top + 5.0 + 0.6 * width))


def build_steering_wheel(p: Inputs) -> k.Shape:
    c = cabin(p)
    tilt = math.radians(65.0)  # wheel axis from horizontal: the rim faces the driver
    centre = cq.Vector(c.cowl - c.dash - 260.0, c.driver_y, c.belt + 20.0)
    axis = cq.Vector(math.cos(tilt), 0.0, math.sin(tilt))
    rim = cq.Solid.makeTorus(180.0, 16.0, centre, axis)
    hub = cq.Solid.makeCylinder(55.0, 60.0, centre - axis * 30.0, axis)
    column = cq.Solid.makeCylinder(25.0, 320.0, centre + axis * 20.0,
                                   cq.Vector(1.0, 0.0, -0.35).normalized())  # fmt: skip
    spokes = [
        k.box((centre.x - 12.0, centre.x + 12.0), (c.driver_y - 175.0, c.driver_y + 175.0),
              (centre.z - 10.0, centre.z + 10.0)),
    ]  # fmt: skip
    return k.fuse(rim, hub, column, *spokes)


def build_console(p: Inputs) -> k.Shape:
    c, level = cabin(p), trim(p)
    front_x = seat_positions(p)[0][0]
    height = {"standard": 140.0, "comfort": 260.0, "premium": 330.0}[level]
    x = (front_x - 520.0, c.cowl - c.dash - 30.0)
    console = k.box(x, (-110.0, 110.0), (c.floor, c.floor + height))
    if level == "premium":  # armrest between the front seats
        console = k.fuse(console, k.box((x[0], x[0] + 280.0), (-120.0, 120.0),
                                        (c.floor + height, c.floor + height + 70.0)))  # fmt: skip
    return console


def front_headroom(p: Inputs) -> float:
    """Roof liner above the head of a seated adult in the front row, mm (negative: the head
    would touch the roof). Uses the seated-height allowance above the cushion."""
    c = cabin(p)
    return c.roof - cushion_top(c) - seated_height(c)
