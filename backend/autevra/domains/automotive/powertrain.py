"""Powertrain and electrical equipment: what is fitted depends on the powertrain and the
chassis (vehicle frame, mm, ISO 8855; front axle at x = 0, rear axle at x = -wheelbase).

Each builder returns ``None`` when the item is not fitted (no engine in a battery electric
car, no traction battery in a combustion car). The parts are packaging envelopes placed by
stated rules of thumb, not component designs.
"""

from collections.abc import Mapping

import cadquery as cq

from autevra.cad import kernel as k
from autevra.domains.automotive import derived as d

Inputs = Mapping[str, float]
ENGINE_LENGTH = {0: 420.0, 1: 520.0, 2: 560.0, 3: 640.0}  # block length by layout, mm


def _kind(p: Inputs) -> str:
    return d.powertrain(p)


def _wheel_z(p: Inputs) -> float:
    return p["tyre_radius"]


def _front_drive(p: Inputs) -> bool:
    return p["front_drive_share"] > 0.0


def _rear_drive(p: Inputs) -> bool:
    return p["front_drive_share"] < 100.0


def _transverse(p: Inputs) -> bool:
    """Front-wheel-drive layouts mount the engine across the car."""
    return p["front_drive_share"] >= 50.0


# --- Combustion -----------------------------------------------------------------------


def build_engine(p: Inputs) -> k.Shape | None:
    if _kind(p) == "electric":
        return None
    layout = int(round(p["engine_cylinders"]))
    length, z0 = ENGINE_LENGTH[min(max(layout, 0), 3)], _wheel_z(p) - 120.0
    vee = layout >= 2
    across = (-length / 2, length / 2)
    depth = (-80.0, 460.0) if vee else (-60.0, 360.0)
    if _transverse(p):
        block = k.box(depth, across, (z0, z0 + 420.0))
    else:
        block = k.box((60.0 - length, 60.0), (-0.5 * depth[1], 0.5 * depth[1]), (z0, z0 + 420.0))
    head_w = 260.0 if not vee else 180.0
    if _transverse(p):
        heads = [k.box((100.0, 100.0 + head_w), across, (z0 + 420.0, z0 + 540.0))]
    else:
        heads = [k.box((60.0 - length, 60.0), (-head_w / 2 - (150.0 if vee else 0.0),
                                               head_w / 2 - (150.0 if vee else 0.0)),
                       (z0 + 420.0, z0 + 540.0))]  # fmt: skip
        if vee:
            heads.append(k.box((60.0 - length, 60.0), (150.0 - head_w / 2, 150.0 + head_w / 2),
                               (z0 + 420.0, z0 + 540.0)))  # fmt: skip
    return k.fuse(block, *heads)


def build_gearbox(p: Inputs) -> k.Shape | None:
    """Gearbox (combustion), with the motor-generator between engine and gearbox (hybrid)."""
    if _kind(p) == "electric":
        return None
    z = _wheel_z(p)
    layout = int(round(p["engine_cylinders"]))
    length = ENGINE_LENGTH[min(max(layout, 0), 3)]
    if _transverse(p):
        y0 = -length / 2
        box = k.box((-60.0, 300.0), (y0 - 380.0, y0), (z - 160.0, z + 220.0))
        if _kind(p) == "hybrid":
            mg = cq.Solid.makeCylinder(170.0, 110.0, cq.Vector(120.0, y0 - 110.0, z + 30.0),
                                       cq.Vector(0, 1, 0))  # fmt: skip
            box = k.fuse(box, mg)
        return box
    x1 = 60.0 - length
    box = k.box((x1 - 520.0, x1), (-160.0, 160.0), (z - 140.0, z + 200.0))
    if _kind(p) == "hybrid":
        mg = cq.Solid.makeCylinder(170.0, 110.0, cq.Vector(x1 - 110.0, 0, z + 30.0),
                                   cq.Vector(1, 0, 0))  # fmt: skip
        box = k.fuse(box, mg)
    return box


def build_fuel_tank(p: Inputs) -> k.Shape | None:
    if _kind(p) == "electric":
        return None
    gc, half = p["ground_clearance"], p["body_width"] / 2.0
    x = (-p["wheelbase"] + 250.0, -p["wheelbase"] + 850.0)
    return k.box(x, (-0.36 * half, 0.36 * half), (gc + 15.0, gc + 230.0))


def build_exhaust(p: Inputs) -> k.Shape | None:
    if _kind(p) == "electric":
        return None
    gc, half = p["ground_clearance"], p["body_width"] / 2.0
    rear = -(p["wheelbase"] + p["rear_overhang"])
    y, z = -0.28 * half, gc + 45.0
    pipe = k.cylinder_x(32.0, (rear + 60.0, 200.0), y=y, z=z)
    muffler = k.box((rear + 180.0, rear + 680.0), (y - 160.0, y + 160.0), (gc + 10.0, gc + 150.0))
    catalyst = k.box((-350.0, 0.0), (y - 90.0, y + 90.0), (gc + 10.0, gc + 150.0))
    return k.fuse(pipe, muffler, catalyst)


def build_radiator(p: Inputs) -> k.Shape:
    """Front cooling module (engine radiator or battery and power-electronics cooling)."""
    front, half, gc = p["front_overhang"], p["body_width"] / 2.0, p["ground_clearance"]
    return k.box(
        (front - 190.0, front - 150.0), (-0.38 * half, 0.38 * half), (gc + 140.0, gc + 560.0)
    )


# --- Electrified ----------------------------------------------------------------------


def build_traction_battery(p: Inputs) -> k.Shape | None:
    kind = _kind(p)
    if kind == "combustion":
        return None
    gc = p["ground_clearance"] + d.PACK_CLEARANCE
    h = d.pack_height(p)
    (x0, x1), (y0, y1) = d.pack_footprint(p)
    if kind == "hybrid":  # compact pack ahead of the rear axle, under the rear seat
        x1 = -p["wheelbase"] + 1050.0
        x0 = x1 - d.HYBRID_PACK_LENGTH
        y0, y1 = 0.6 * y0, 0.6 * y1
    pack = k.box((x0, x1), (y0, y1), (gc, gc + h))
    # Module rows on top, so the pack reads as modules in a tray.
    rows = 4 if kind == "electric" else 2
    pitch = (x1 - x0) / rows
    ridges = [k.box((x0 + i * pitch + 20.0, x0 + (i + 1) * pitch - 20.0), (y0 + 30.0, y1 - 30.0),
                    (gc + h, gc + h + 12.0)) for i in range(rows)]  # fmt: skip
    return k.fuse(pack, *ridges)


def _motor(p: Inputs, x: float) -> k.Shape:
    z = _wheel_z(p)
    housing = cq.Solid.makeCylinder(135.0, 420.0, cq.Vector(x, -210.0, z), cq.Vector(0, 1, 0))
    reducer = k.box((x - 90.0, x + 90.0), (210.0, 330.0), (z - 150.0, z + 150.0))
    return k.fuse(housing, reducer)


def build_front_motor(p: Inputs) -> k.Shape | None:
    if _kind(p) != "electric" or not _front_drive(p):
        return None
    return _motor(p, 230.0)


def build_rear_motor(p: Inputs) -> k.Shape | None:
    if _kind(p) != "electric" or not _rear_drive(p):
        return None
    return _motor(p, -p["wheelbase"] - 230.0)


def build_inverters(p: Inputs) -> k.Shape | None:
    """One inverter on each electric drive (battery electric), or beside the gearbox (hybrid)."""
    kind, z = _kind(p), _wheel_z(p)
    if kind == "combustion":
        return None
    boxes = []
    if kind == "hybrid":
        boxes.append(k.box((320.0, 560.0), (-120.0, 160.0), (z + 120.0, z + 230.0)))
    else:
        for on, x in ((_front_drive(p), 230.0), (_rear_drive(p), -p["wheelbase"] - 230.0)):
            if on:
                boxes.append(k.box((x - 150.0, x + 150.0), (-200.0, 140.0), (z + 140.0, z + 250.0)))
    first, *rest = boxes
    return k.fuse(first, *rest) if rest else first


def build_charger(p: Inputs) -> k.Shape | None:
    """On-board charger and DC-DC converter (battery electric and plug-in hybrid)."""
    if _kind(p) == "combustion":
        return None
    z = _wheel_z(p)
    x = p["front_overhang"] - 520.0
    return k.box((x, x + 280.0), (60.0, 360.0), (z + 160.0, z + 280.0))


def build_charge_port(p: Inputs) -> k.Shape | None:
    """Charging inlet on the rear quarter panel, left side, flush with the body side."""
    if _kind(p) == "combustion":
        return None
    half, floor = p["body_width"] / 2.0, p["body_floor"]
    belt = p["beltline_height"]
    x = -p["wheelbase"] - 0.45 * p["rear_overhang"]
    z = floor + 0.42 * (belt - floor)
    return k.box((x - 70.0, x + 70.0), (half - 14.0, half + 1.0), (z - 55.0, z + 55.0))


def build_hv_cables(p: Inputs) -> k.Shape | None:
    """Orange high-voltage cables from the battery to each electric drive or inverter."""
    kind = _kind(p)
    if kind == "combustion":
        return None
    gc = p["ground_clearance"] + d.PACK_CLEARANCE
    z, h = _wheel_z(p), d.pack_height(p)
    (x0, x1), _ = d.pack_footprint(p)
    if kind == "hybrid":
        x1 = -p["wheelbase"] + 1050.0
        x0 = x1 - d.HYBRID_PACK_LENGTH
    cables = []
    for y in (90.0, 140.0):
        if kind == "hybrid" or _front_drive(p):
            end = 320.0 if kind == "hybrid" else 230.0
            cables.append(k.cylinder_x(14.0, (x1, end), y=y, z=gc + 0.5 * h))
            rise = max(z + 140.0 - gc - 0.5 * h, 1.0)  # up to the drive unit
            base = cq.Vector(end, y, gc + 0.5 * h)
            cables.append(cq.Solid.makeCylinder(14.0, rise, base, cq.Vector(0, 0, 1)))
        if kind == "electric" and _rear_drive(p):
            end = -p["wheelbase"] - 230.0
            cables.append(k.cylinder_x(14.0, (end, x0), y=y, z=gc + 0.5 * h))
    first, *rest = cables
    return k.fuse(first, *rest) if rest else first


# --- Low-voltage electrical (every vehicle) ---------------------------------------------


def build_battery_12v(p: Inputs) -> k.Shape:
    z = _wheel_z(p)
    x = p["front_overhang"] - 420.0
    y = -0.55 * p["body_width"] / 2.0
    return k.box((x, x + 260.0), (y - 90.0, y + 90.0), (z + 120.0, z + 300.0))


def build_ecus(p: Inputs) -> k.Shape:
    """Control units: engine or vehicle controller under the bonnet, body and gateway
    controllers behind the dashboard, and (electrified) the battery management system."""
    z, belt = _wheel_z(p), p["beltline_height"]
    cowl_x = -100.0  # behind the front axle line, under the dashboard
    boxes = [
        k.box((p["front_overhang"] - 720.0, p["front_overhang"] - 560.0), (-300.0, -140.0),
              (z + 180.0, z + 240.0)),
        k.box((cowl_x - 260.0, cowl_x - 120.0), (-180.0, 180.0), (belt - 330.0, belt - 290.0)),
    ]  # fmt: skip
    if _kind(p) != "combustion":
        (x0, _), (y0, _) = d.pack_footprint(p)
        gc = p["ground_clearance"] + d.PACK_CLEARANCE
        boxes.append(k.box((x0 + 40.0, x0 + 220.0), (y0 + 40.0, y0 + 200.0),
                           (gc + d.pack_height(p), gc + d.pack_height(p) + 40.0)))  # fmt: skip
    return k.fuse(*boxes)


def build_harness(p: Inputs) -> k.Shape:
    """Main wiring trunk along the left sill, with a riser to the dashboard and branches to
    the front and rear lamps."""
    half, floor, belt = p["body_width"] / 2.0, p["body_floor"], p["beltline_height"]
    front, rear = p["front_overhang"] - 120.0, -(p["wheelbase"] + p["rear_overhang"]) + 120.0
    y, z = half - 140.0, floor + 30.0
    trunk = k.cylinder_x(11.0, (rear, front), y=y, z=z)
    riser = cq.Solid.makeCylinder(
        9.0, max(belt - 300.0 - z, 1.0), cq.Vector(-150.0, y, z), cq.Vector(0, 0, 1)
    )
    across_front = k.cylinder_y(8.0, (-y, y), x=front, z=z)
    across_rear = k.cylinder_y(8.0, (-y, y), x=rear, z=z)
    return k.fuse(trunk, riser, across_front, across_rear)
