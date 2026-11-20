"""Interface mating: place an item by snapping one of its ports onto a port of an installed
item, after checking that the two ports can mate.

Frames: a port's frame is given in its item's coordinates (``at``: translation, then
rotations about X, Y, Z in degrees, as part placements). Mating makes the two port frames
coincide: the new item's placement S satisfies S · own = target_world, so
S = target_world · own⁻¹.

Compatibility (by kind, with dimensional checks):
- thread ↔ thread: same size and pitch (a nut on a screw);
- thread ↔ bore: the bore clears the thread (d ≤ bore ≤ 1.3 d; a washer or a clearance hole);
- shaft ↔ bore: equal diameters within 0.1 mm (a bearing bore on a shaft, an outer ring
  in a housing);
- end ↔ end: equal section (profiles joined end to end).
"""

import math

import numpy as np

from autevra.inventory.model import Port

PAIRS = {
    frozenset({"mechanical.thread"}),
    frozenset({"mechanical.thread", "mechanical.bore"}),
    frozenset({"mechanical.shaft", "mechanical.bore"}),
    frozenset({"mechanical.end"}),
}


def _num(port: Port, key: str) -> float | None:
    v = port.attributes.get(key)
    return float(v) if isinstance(v, int | float) else None


def _thread_d(port: Port) -> float | None:
    size = port.attributes.get("size")
    return float(str(size)[1:]) if isinstance(size, str) and size.startswith("M") else None


def compatible(own: Port, target: Port) -> tuple[bool, str]:
    """Whether two ports can mate, with the reason."""
    kinds = frozenset({own.kind, target.kind})
    if kinds not in PAIRS:
        return False, f"a {own.kind} port cannot mate with a {target.kind} port"
    if kinds == frozenset({"mechanical.thread"}):
        same = (own.attributes.get("size") == target.attributes.get("size")
                and own.attributes.get("pitch") == target.attributes.get("pitch"))  # fmt: skip
        return (same, "threads match" if same else
                f"thread {own.attributes.get('size')} does not fit "
                f"{target.attributes.get('size')}")  # fmt: skip
    if kinds == frozenset({"mechanical.thread", "mechanical.bore"}):
        thread, bore = (own, target) if own.kind == "mechanical.thread" else (target, own)
        d, b = _thread_d(thread), _num(bore, "diameter")
        if d is None or b is None:
            return False, "missing thread size or bore diameter"
        if b < d:
            return False, f"bore Ø{b:g} mm is smaller than the M{d:g} thread"
        if b > 1.3 * d:
            return False, f"bore Ø{b:g} mm is too loose for M{d:g} (over 1.3 d)"
        return True, f"M{d:g} through a Ø{b:g} mm bore"
    if kinds == frozenset({"mechanical.shaft", "mechanical.bore"}):
        a, b = _num(own, "diameter"), _num(target, "diameter")
        if a is None or b is None:
            return False, "missing diameters"
        ok = abs(a - b) <= 0.1
        return ok, f"Ø{a:g} mm in Ø{b:g} mm" + ("" if ok else ": diameters differ")
    return True, "section ends meet"


def matrix(at: dict[str, float]) -> np.ndarray:
    """Placement matrix: rotate about X, then Y, then Z, then translate (as parts)."""

    def rot(axis: int, deg: float) -> np.ndarray:
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        m = np.eye(4)
        i, j = [(1, 2), (2, 0), (0, 1)][axis]
        m[i, i], m[i, j], m[j, i], m[j, j] = c, -s, s, c
        return m

    m = rot(2, at.get("rz", 0.0)) @ rot(1, at.get("ry", 0.0)) @ rot(0, at.get("rx", 0.0))
    m[:3, 3] = (at.get("x", 0.0), at.get("y", 0.0), at.get("z", 0.0))
    return m


def placement(m: np.ndarray) -> dict[str, float]:
    """The placement (x, y, z, rx, ry, rz) of a rigid transform (inverse of ``matrix``)."""
    r = m[:3, :3]
    ry = math.degrees(math.asin(max(-1.0, min(1.0, -r[2, 0]))))
    if abs(r[2, 0]) < 1 - 1e-9:
        rx = math.degrees(math.atan2(r[2, 1], r[2, 2]))
        rz = math.degrees(math.atan2(r[1, 0], r[0, 0]))
    else:  # gimbal lock: put the whole turn in rz
        rx, rz = 0.0, math.degrees(math.atan2(-r[0, 1], r[1, 1]))
    out = {"x": m[0, 3], "y": m[1, 3], "z": m[2, 3], "rx": rx, "ry": ry, "rz": rz}
    return {k: round(float(v), 6) + 0.0 for k, v in out.items()}


def mate(part_at: dict[str, float], target: Port, own: Port) -> dict[str, float]:
    """Placement of the new item so that its ``own`` port lands on ``target`` (a port of an
    installed item placed at ``part_at``)."""
    world = matrix(part_at) @ matrix(target.at)
    return placement(world @ np.linalg.inv(matrix(own.at)))
