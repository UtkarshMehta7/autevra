"""The standard-parts library, generated from dimension tables of the standards.

Dimensions are the standards' nominal values (ISO 4762, ISO 4017, ISO 4032, ISO 7089,
ISO 15 boundary dimensions, EN 10219 / EN 10210 section sizes). Bearing load ratings are
typical catalogue values for steel deep-groove ball bearings; they differ by manufacturer
by up to about 10 %, so a design should use its supplier's figures. Geometry is simplified
for display and clearance (no thread form, bearing rings without balls, sharp-cornered
sections); masses come from that geometry in steel, except bearings (catalogue-like
estimate: ring annulus x 0.65).
"""

import math
from functools import cache

from autevra.inventory import calc
from autevra.inventory.model import Item, Port

STEEL = calc.STEEL * 1e-9  # kg/mm3

# metric coarse thread: size -> (d, pitch, ISO 4762 head dk, k, socket s,
#                                ISO 4017 across flats, head height, ISO 4032 nut m,
#                                ISO 7089 washer d1, d2, h)
METRIC: dict[str, tuple[float, ...]] = {
    "M3": (3, 0.5, 5.5, 3, 2.5, 5.5, 2.0, 2.4, 3.2, 7, 0.5),
    "M4": (4, 0.7, 7, 4, 3, 7, 2.8, 3.2, 4.3, 9, 0.8),
    "M5": (5, 0.8, 8.5, 5, 4, 8, 3.5, 4.7, 5.3, 10, 1.0),
    "M6": (6, 1.0, 10, 6, 5, 10, 4.0, 5.2, 6.4, 12, 1.6),
    "M8": (8, 1.25, 13, 8, 6, 13, 5.3, 6.8, 8.4, 16, 1.6),
    "M10": (10, 1.5, 16, 10, 8, 16, 6.4, 8.4, 10.5, 20, 2.0),
    "M12": (12, 1.75, 18, 12, 10, 18, 7.5, 10.8, 13, 24, 2.5),
    "M16": (16, 2.0, 24, 16, 14, 24, 10.0, 14.8, 17, 30, 3.0),
    "M20": (20, 2.5, 30, 20, 17, 30, 12.5, 18.0, 21, 37, 3.0),
    "M24": (24, 3.0, 36, 24, 19, 36, 15.0, 21.5, 25, 44, 4.0),
}
LENGTHS = (8, 10, 12, 16, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 150)

# deep-groove ball bearings: designation -> (d, D, B, C kN, C0 kN)
BEARINGS: dict[str, tuple[float, float, float, float, float]] = {
    "6000": (10, 26, 8, 4.75, 1.96), "6001": (12, 28, 8, 5.4, 2.36),
    "6002": (15, 32, 9, 5.85, 2.85), "6003": (17, 35, 10, 6.37, 3.25),
    "6004": (20, 42, 12, 9.95, 5.0), "6005": (25, 47, 12, 11.9, 6.55),
    "6006": (30, 55, 13, 13.8, 8.3), "6007": (35, 62, 14, 16.8, 10.2),
    "6008": (40, 68, 15, 17.8, 11.6), "6010": (50, 80, 16, 22.9, 16.0),
    "6200": (10, 30, 9, 5.4, 2.36), "6201": (12, 32, 10, 7.28, 3.1),
    "6202": (15, 35, 11, 8.06, 3.75), "6203": (17, 40, 12, 9.95, 4.75),
    "6204": (20, 47, 14, 13.5, 6.55), "6205": (25, 52, 15, 14.8, 7.8),
    "6206": (30, 62, 16, 20.3, 11.2), "6207": (35, 72, 17, 27.0, 15.3),
    "6208": (40, 80, 18, 32.5, 19.0), "6210": (50, 90, 20, 37.1, 23.2),
}  # fmt: skip

SHS_SIZES = ((20, 2), (25, 2), (30, 2), (30, 3), (40, 2), (40, 3), (40, 4), (50, 3), (50, 4),
             (60, 3), (60, 4), (80, 4), (80, 5), (100, 4), (100, 5), (100, 6))  # fmt: skip
CHS_SIZES = ((21.3, 2.6), (26.9, 2.6), (33.7, 3.2), (42.4, 3.2), (48.3, 3.2), (60.3, 3.6),
             (76.1, 3.6), (88.9, 4.0), (114.3, 4.5))  # fmt: skip
PROFILE_LENGTH = 1000.0  # mm, one metre: mass and properties per metre


def _doc(name: str, features: list[dict], color: tuple[float, float, float],
         finish: str = "metal") -> dict:  # fmt: skip
    return {"name": name, "color": list(color), "finish": finish, "features": features}


def _socket_screw(size: str, length: float) -> Item:
    d, p, dk, k, s, *_ = METRIC[size]
    head = math.pi / 4 * (dk * dk - s * s * 1.1) * k  # hexagon socket recess approximated
    mass = (head + math.pi / 4 * d * d * length) * STEEL
    cap = calc.bolt_capacity(d, p, "12.9")
    return Item(
        id=f"iso4762-{size.lower()}x{length:g}", family="Socket head cap screw",
        category="Fasteners", name=f"ISO 4762 {size} x {length:g} - 12.9",
        standard="ISO 4762 / ISO 898-1", parameters={"size": size, "d": d, "pitch": p,
                                                     "length": length, "class": "12.9"},
        properties={"mass_kg": round(mass, 5), "material": "alloy steel, class 12.9"},
        performance={k_: round(v, 3) for k_, v in cap.items()},
        ports=[Port(name="head_seat", kind="mechanical.seat", at={"z": 0.0},
                    attributes={"diameter": dk}),
               Port(name="thread", kind="mechanical.thread", at={"z": -length},
                    attributes={"size": size, "pitch": p})],
        definition=_doc(f"{size}x{length:g} cap screw", [
            {"id": "head", "name": "Head", "type": "cylinder", "radius": dk / 2, "height": k,
             "at": {"z": k / 2}},
            {"id": "socket", "name": "Socket", "type": "extrude", "op": "cut",
             "points": _hexagon(s), "depth": 0.6 * k, "at": {"z": 0.45 * k}},
            {"id": "shank", "name": "Shank", "type": "cylinder", "radius": d / 2,
             "height": length, "at": {"z": -length / 2}},
        ], (0.12, 0.12, 0.13)),
        notes=["thread form not modelled; preload at 70 % of yield, torque with K = 0.2"],
    )  # fmt: skip


def _hexagon(across_flats: float) -> list[list[float]]:
    r = across_flats / math.sqrt(3)  # corner radius of a hexagon from its width
    return [[r * math.cos(math.radians(30 + 60 * i)), r * math.sin(math.radians(30 + 60 * i))]
            for i in range(6)]  # fmt: skip


def _hex_bolt(size: str, length: float) -> Item:
    d, p, _dk, _k, _s, af, kh, *_ = METRIC[size]
    hexa = 3 * math.sqrt(3) / 2 * (af / math.sqrt(3)) ** 2
    mass = (hexa * kh + math.pi / 4 * d * d * length) * STEEL
    cap = calc.bolt_capacity(d, p, "8.8")
    return Item(
        id=f"iso4017-{size.lower()}x{length:g}", family="Hexagon head screw",
        category="Fasteners", name=f"ISO 4017 {size} x {length:g} - 8.8",
        standard="ISO 4017 / ISO 898-1",
        parameters={"size": size, "d": d, "pitch": p, "length": length, "class": "8.8"},
        properties={"mass_kg": round(mass, 5), "material": "steel, class 8.8, zinc plated"},
        performance={k_: round(v, 3) for k_, v in cap.items()},
        ports=[Port(name="head_seat", kind="mechanical.seat", at={"z": 0.0},
                    attributes={"across_flats": af}),
               Port(name="thread", kind="mechanical.thread", at={"z": -length},
                    attributes={"size": size, "pitch": p})],
        definition=_doc(f"{size}x{length:g} hex bolt", [
            {"id": "head", "name": "Head", "type": "extrude", "points": _hexagon(af),
             "depth": kh},
            {"id": "shank", "name": "Shank", "type": "cylinder", "radius": d / 2,
             "height": length, "at": {"z": -length / 2}},
        ], (0.7, 0.72, 0.74)),
        notes=["thread form not modelled; preload at 70 % of yield, torque with K = 0.2"],
    )  # fmt: skip


def _nut(size: str) -> Item:
    d, p, *_rest = METRIC[size]
    af, m = METRIC[size][5], METRIC[size][7]
    hexa = 3 * math.sqrt(3) / 2 * (af / math.sqrt(3)) ** 2
    mass = (hexa - math.pi / 4 * d * d) * m * STEEL
    return Item(
        id=f"iso4032-{size.lower()}", family="Hexagon nut", category="Fasteners",
        name=f"ISO 4032 {size} - 8", standard="ISO 4032",
        parameters={"size": size, "d": d, "pitch": p, "height": m},
        properties={"mass_kg": round(mass, 5), "material": "steel, class 8"},
        ports=[Port(name="thread", kind="mechanical.thread", attributes={"size": size,
                                                                         "pitch": p})],
        definition=_doc(f"{size} nut", [
            {"id": "body", "name": "Body", "type": "extrude", "points": _hexagon(af),
             "depth": m},
            {"id": "hole", "name": "Hole", "type": "cylinder", "op": "cut", "radius": d / 2,
             "height": m * 3, "at": {"z": m / 2}},
        ], (0.7, 0.72, 0.74)),
    )  # fmt: skip


def _washer(size: str) -> Item:
    d1, d2, h = METRIC[size][8], METRIC[size][9], METRIC[size][10]
    mass = math.pi / 4 * (d2 * d2 - d1 * d1) * h * STEEL
    return Item(
        id=f"iso7089-{size.lower()}", family="Plain washer", category="Fasteners",
        name=f"ISO 7089 {size[1:]} - 200 HV", standard="ISO 7089",
        parameters={"size": size, "d1": d1, "d2": d2, "h": h},
        properties={"mass_kg": round(mass, 6), "material": "steel, 200 HV"},
        ports=[Port(name="bore", kind="mechanical.bore", attributes={"diameter": d1})],
        definition=_doc(f"{size} washer", [
            {"id": "ring", "name": "Ring", "type": "revolve",
             "points": [[d1 / 2, 0], [d2 / 2, 0], [d2 / 2, h], [d1 / 2, h]]}], (0.75, 0.76, 0.78)),
    )  # fmt: skip


def _bearing(code: str) -> Item:
    d, big_d, b, c, c0 = BEARINGS[code]
    ring = 0.3 * (big_d - d) / 2 * 2
    mass = math.pi / 4 * (big_d**2 - d**2) * b * STEEL * 0.65
    inner = [[d / 2, -b / 2], [d / 2 + ring / 2, -b / 2], [d / 2 + ring / 2, b / 2],
             [d / 2, b / 2]]  # fmt: skip
    outer = [[big_d / 2 - ring / 2, -b / 2], [big_d / 2, -b / 2], [big_d / 2, b / 2],
             [big_d / 2 - ring / 2, b / 2]]  # fmt: skip
    return Item(
        id=f"bearing-{code}", family="Deep groove ball bearing", category="Bearings",
        name=f"{code} deep groove ball bearing ({d:g} x {big_d:g} x {b:g})",
        standard="ISO 15 (boundary dimensions), ISO 281 (rating life)",
        parameters={"designation": code, "d": d, "D": big_d, "B": b},
        properties={"mass_kg": round(mass, 4), "material": "bearing steel"},
        performance={"C_kN": c, "C0_kN": c0},
        ports=[Port(name="bore", kind="mechanical.bore", attributes={"diameter": d}),
               Port(name="outer", kind="mechanical.shaft", attributes={"diameter": big_d})],
        definition=_doc(f"{code} bearing", [
            {"id": "inner", "name": "Inner ring", "type": "revolve", "points": inner},
            {"id": "outer", "name": "Outer ring", "type": "revolve", "points": outer},
        ], (0.78, 0.79, 0.8), "polished"),
        notes=["C and C0 are typical catalogue values (±10 % between manufacturers)",
               "rings shown without balls and cage"],
    )  # fmt: skip


def _shs(b: float, t: float) -> Item:
    props = calc.shs(b, t)
    half, inner = b / 2, b / 2 - t
    sq = lambda h: [[-h, -h], [h, -h], [h, h], [-h, h]]  # noqa: E731
    return Item(
        id=f"shs-{b:g}x{b:g}x{t:g}", family="Square hollow section", category="Profiles",
        name=f"SHS {b:g} x {b:g} x {t:g}", standard="EN 10219 (sizes)",
        parameters={"b": b, "t": t, "length": PROFILE_LENGTH},
        properties={"mass_kg": round(props["mass_kg_per_m"] * PROFILE_LENGTH / 1000, 3),
                    "material": "S355 steel"},
        performance={k: round(v, 2) for k, v in props.items()},
        ports=[Port(name="end_a", kind="mechanical.end", at={"z": 0}),
               Port(name="end_b", kind="mechanical.end", at={"z": PROFILE_LENGTH})],
        definition=_doc(f"SHS {b:g}x{t:g}", [
            {"id": "outer", "name": "Outer", "type": "extrude", "points": sq(half),
             "depth": PROFILE_LENGTH},
            {"id": "bore", "name": "Bore", "type": "extrude", "op": "cut", "points": sq(inner),
             "depth": PROFILE_LENGTH * 1.01, "at": {"z": -PROFILE_LENGTH * 0.005}},
        ], (0.35, 0.37, 0.4)),
        notes=["per metre; sharp corners (EN 10219 corner radii ignored)"],
    )  # fmt: skip


def _chs(d: float, t: float) -> Item:
    props = calc.chs(d, t)
    return Item(
        id=f"chs-{d:g}x{t:g}", family="Circular hollow section", category="Profiles",
        name=f"CHS {d:g} x {t:g}", standard="EN 10210 / EN 10219 (sizes)",
        parameters={"d": d, "t": t, "length": PROFILE_LENGTH},
        properties={"mass_kg": round(props["mass_kg_per_m"] * PROFILE_LENGTH / 1000, 3),
                    "material": "S355 steel"},
        performance={k: round(v, 2) for k, v in props.items()},
        ports=[Port(name="end_a", kind="mechanical.end", at={"z": 0}),
               Port(name="end_b", kind="mechanical.end", at={"z": PROFILE_LENGTH})],
        definition=_doc(f"CHS {d:g}x{t:g}", [
            {"id": "tube", "name": "Tube", "type": "revolve",
             "points": [[d / 2 - t, 0], [d / 2, 0], [d / 2, PROFILE_LENGTH],
                        [d / 2 - t, PROFILE_LENGTH]]}], (0.35, 0.37, 0.4)),
        notes=["per metre"],
    )  # fmt: skip


@cache
def catalogue() -> dict[str, Item]:
    items: list[Item] = []
    for size, row in METRIC.items():
        d = row[0]
        for length in LENGTHS:
            if 2 * d <= length <= 10 * d:
                items += [_socket_screw(size, length), _hex_bolt(size, length)]
        items += [_nut(size), _washer(size)]
    items += [_bearing(code) for code in BEARINGS]
    items += [_shs(b, t) for b, t in SHS_SIZES] + [_chs(d, t) for d, t in CHS_SIZES]
    return {i.id: i for i in items}
