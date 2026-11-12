"""Mechanisms: planar linkages in closed form, and the motion of a part about a joint.

Four-bar linkage (ground g, crank a, coupler b, rocker c; crank pivot A at the origin,
rocker pivot D at (g, 0)): for a crank angle t the crank pin is B = a (cos t, sin t) and the
coupler-rocker pin C is the intersection of the circle about B (radius b) with the circle
about D (radius c); the assembly branch picks the side of BD. The transmission angle mu at
C follows from the cosine rule on triangle BCD: cos mu = (b^2 + c^2 - |BD|^2) / (2 b c).
The Grashof condition s + l <= p + q decides whether the shortest link turns fully.

Slider-crank (crank r, rod l, offset e): x(t) = r cos t + sqrt(l^2 - (r sin t - e)^2),
with dx/dt and d2x/dt2 differentiated analytically; at constant speed w the slider
velocity is w dx/dt and its acceleration w^2 d2x/dt2.

Swept motion: a placed part is moved through the range of one joint (revolute about an
axis, or prismatic along it) at sampled positions. Against every other part the minimum
distance over the samples is reported with the joint position where it occurs; the
envelope is the union of the sampled poses. Both are sampled results: between samples
the true minimum can be smaller, so the step count is part of the answer.
"""

import math
from typing import Literal

import numpy as np
from pydantic import BaseModel, Field

from autevra import dmu
from autevra.cad import kernel as k

Vec3 = tuple[float, float, float]


# --- four-bar ------------------------------------------------------------------------


class FourBar(BaseModel):
    ground: float = Field(gt=0, le=1e5)
    crank: float = Field(gt=0, le=1e5)
    coupler: float = Field(gt=0, le=1e5)
    rocker: float = Field(gt=0, le=1e5)
    # Coupler point P in the coupler's frame: along BC from B, and to its left.
    point_along: float = Field(0.0, ge=-1e5, le=1e5)
    point_off: float = Field(0.0, ge=-1e5, le=1e5)
    branch: Literal[1, -1] = 1  # +1: C to the left of B->D (open), -1: crossed
    steps: int = Field(72, ge=4, le=720)


def grashof(g: float, a: float, b: float, c: float) -> str:
    links = sorted([g, a, b, c])
    s, p, q, long = links
    if s + long > p + q + 1e-9:
        return "non-Grashof triple rocker"
    if abs(s + long - (p + q)) <= 1e-9:
        return "change point"
    if a == s:
        return "crank-rocker"
    if g == s:
        return "double crank (drag link)"
    if b == s:
        return "Grashof double rocker"
    return "rocker-crank"


def fourbar_pose(fb: FourBar, theta_deg: float) -> dict | None:
    """Joint positions at one crank angle, or None where the linkage cannot assemble."""
    t = math.radians(theta_deg)
    bx, by = fb.crank * math.cos(t), fb.crank * math.sin(t)
    dx, dy = fb.ground - bx, -by
    d = math.hypot(dx, dy)
    if d < 1e-12 or d > fb.coupler + fb.rocker + 1e-9 or d < abs(fb.coupler - fb.rocker) - 1e-9:
        return None
    along = (fb.coupler**2 - fb.rocker**2 + d**2) / (2 * d)
    h = math.sqrt(max(0.0, fb.coupler**2 - along**2))
    ux, uy = dx / d, dy / d
    cx = bx + along * ux - fb.branch * h * uy
    cy = by + along * uy + fb.branch * h * ux
    ex, ey = (cx - bx) / fb.coupler, (cy - by) / fb.coupler
    px = bx + fb.point_along * ex - fb.point_off * ey
    py = by + fb.point_along * ey + fb.point_off * ex
    cos_mu = (fb.coupler**2 + fb.rocker**2 - d**2) / (2 * fb.coupler * fb.rocker)
    return {
        "theta_deg": theta_deg,
        "b": (bx, by),
        "c": (cx, cy),
        "p": (px, py),
        "coupler_deg": math.degrees(math.atan2(ey, ex)),
        "rocker_deg": math.degrees(math.atan2(cy, cx - fb.ground)),
        "transmission_deg": math.degrees(math.acos(max(-1.0, min(1.0, cos_mu)))),
    }


def fourbar(fb: FourBar) -> dict:
    poses = [fourbar_pose(fb, 360.0 * i / fb.steps) for i in range(fb.steps)]
    ok = [p for p in poses if p is not None]
    kind = grashof(fb.ground, fb.crank, fb.coupler, fb.rocker)
    out: dict = {"class": kind, "full_rotation": len(ok) == len(poses), "poses": ok,
                 "assembled_fraction": round(len(ok) / len(poses), 4)}  # fmt: skip
    if not ok:
        out["warnings"] = ["the links cannot be assembled at any crank angle"]
        return out
    mus = [p["transmission_deg"] for p in ok]
    # Unwrap the rocker angle so its swing is not split at +/-180 degrees.
    rock = np.degrees(np.unwrap(np.radians([p["rocker_deg"] for p in ok])))
    worst = max(abs(90.0 - min(mus)), abs(90.0 - max(mus)))
    out |= {
        "transmission_min_deg": round(min(mus), 3),
        "transmission_max_deg": round(max(mus), 3),
        "rocker_swing_deg": round(float(rock.max() - rock.min()), 3),
        "warnings": ([f"transmission angle departs {worst:.0f} deg from 90 deg; beyond about "
                      "50 deg the rocker is driven poorly"] if worst > 50.0 else []),
    }  # fmt: skip
    return out


# --- slider-crank --------------------------------------------------------------------


class SliderCrank(BaseModel):
    crank: float = Field(gt=0, le=1e5)  # mm
    rod: float = Field(gt=0, le=1e5)  # mm
    offset: float = Field(0.0, ge=-1e5, le=1e5)  # mm
    rpm: float = Field(1000.0, ge=0, le=1e6)
    steps: int = Field(72, ge=4, le=720)


def slider_at(sc: SliderCrank, theta_deg: float) -> tuple[float, float, float]:
    """Slider position (mm) and its first and second derivatives with crank angle (rad)."""
    t = math.radians(theta_deg)
    s = sc.crank * math.sin(t) - sc.offset
    root = math.sqrt(sc.rod**2 - s**2)
    ds, dds = sc.crank * math.cos(t), -sc.crank * math.sin(t)
    x = sc.crank * math.cos(t) + root
    dx = -sc.crank * math.sin(t) - s * ds / root
    ddx = -sc.crank * math.cos(t) - (ds**2 + s * dds) / root - (s * ds) ** 2 / root**3
    return x, dx, ddx


def slider_crank(sc: SliderCrank) -> dict:
    if sc.rod <= sc.crank + abs(sc.offset):
        raise ValueError("the rod must be longer than the crank plus the offset")
    w = sc.rpm * 2 * math.pi / 60.0
    rows = []
    for i in range(sc.steps):
        th = 360.0 * i / sc.steps
        x, dx, ddx = slider_at(sc, th)
        rows.append({"theta_deg": th, "x_mm": x, "v_m_s": w * dx / 1000.0,
                     "a_m_s2": w * w * ddx / 1000.0})  # fmt: skip
    # Dead centres: crank and rod in line (extended and folded).
    top = math.sqrt((sc.rod + sc.crank) ** 2 - sc.offset**2)
    bottom = math.sqrt((sc.rod - sc.crank) ** 2 - sc.offset**2)
    return {
        "stroke_mm": round(top - bottom, 6),
        "x_max_mm": round(top, 6),
        "x_min_mm": round(bottom, 6),
        "rod_ratio": round(sc.rod / sc.crank, 4),
        "v_max_m_s": round(max(abs(r["v_m_s"]) for r in rows), 4),
        "a_max_m_s2": round(max(abs(r["a_m_s2"]) for r in rows), 3),
        "rows": rows,
    }


# --- swept motion of a placed part ---------------------------------------------------


class Joint(BaseModel):
    kind: Literal["revolute", "prismatic"] = "revolute"
    origin: Vec3 = (0.0, 0.0, 0.0)  # a point on the axis, project frame, mm
    axis: Vec3 = (0.0, 0.0, 1.0)
    lo: float = Field(-30.0, ge=-1e5, le=1e5)  # degrees (revolute) or mm (prismatic)
    hi: float = Field(30.0, ge=-1e5, le=1e5)
    steps: int = Field(13, ge=2, le=73)


class SweepPair(BaseModel):
    other: str
    other_name: str
    status: str  # interference | contact | too close | clear
    distance_mm: float
    at: float  # joint position of the minimum
    exact: bool


class SweepReport(BaseModel):
    part: str
    unit: str
    positions: list[float]
    box_min: Vec3
    box_max: Vec3
    pairs: list[SweepPair]
    envelope_mm3: float | None = None


def motion(joint: Joint, q: float) -> np.ndarray:
    """4x4 transform of the joint at position q, applied in the project frame."""
    axis = np.array(joint.axis, dtype=float)
    norm = np.linalg.norm(axis)
    if norm < 1e-12:
        raise ValueError("the joint axis has zero length")
    n = axis / norm
    m = np.eye(4)
    if joint.kind == "prismatic":
        m[:3, 3] = n * q
        return m
    a = math.radians(q)
    kx = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    r = np.eye(3) + math.sin(a) * kx + (1 - math.cos(a)) * (kx @ kx)  # Rodrigues
    o = np.array(joint.origin, dtype=float)
    m[:3, :3] = r
    m[:3, 3] = o - r @ o
    return m


def positions(joint: Joint) -> list[float]:
    return [float(q) for q in np.linspace(joint.lo, joint.hi, joint.steps)]


def envelope(moving: dmu.Placed, joint: Joint) -> k.Shape:
    """Union of the part at every sampled joint position, in the project frame."""
    poses = [moving.shape.moved(k.location(motion(joint, q) @ moving.matrix))
             for q in positions(joint)]  # fmt: skip
    return k.fuse(poses[0], *poses[1:]) if len(poses) > 1 else poses[0]


def sweep(moving: dmu.Placed, others: list[dmu.Placed], joint: Joint,
          clearance_mm: float = 5.0, with_volume: bool = False) -> SweepReport:  # fmt: skip
    qs = positions(joint)
    mats = [motion(joint, q) @ moving.matrix for q in qs]
    boxes = [dmu._box(dmu.Placed(moving.id, moving.name, moving.shape, m)) for m in mats]
    lo = np.min([b[0] for b in boxes], axis=0)
    hi = np.max([b[1] for b in boxes], axis=0)
    pairs = []
    for other in others:
        olo, ohi = dmu._box(other)
        gap = float(np.linalg.norm(np.maximum(0.0, np.maximum(lo - ohi, olo - hi))))
        if gap > clearance_mm:
            pairs.append(SweepPair(other=other.id, other_name=other.name, status="clear",
                                   distance_mm=round(gap, 2), at=qs[0], exact=False))  # fmt: skip
            continue
        best, at = math.inf, qs[0]
        for q, m, (blo, bhi) in zip(qs, mats, boxes, strict=True):
            # A pose whose own box is further away than the best so far cannot improve it.
            if float(np.linalg.norm(np.maximum(0.0, np.maximum(blo - ohi, olo - bhi)))) >= best:
                continue
            dist = k.min_distance(moving.shape, m, other.shape, other.matrix)
            if dist < best:
                best, at = dist, q
            if best <= 1e-6:
                break
        status = "clear"
        if best <= 1e-6:
            status = "contact"
            try:
                common = k.intersect(
                    moving.shape.moved(k.location(motion(joint, at) @ moving.matrix)),
                    other.shape.moved(k.location(other.matrix)))  # fmt: skip
                if k.volume(common) > 1.0:
                    status = "interference"
            except Exception:  # noqa: BLE001 (a failed boolean is reported as contact)
                pass
        elif best < clearance_mm:
            status = "too close"
        pairs.append(SweepPair(other=other.id, other_name=other.name, status=status, exact=True,
                               distance_mm=round(best, 3), at=round(at, 3)))  # fmt: skip
    order = {"interference": 0, "contact": 1, "too close": 2, "clear": 3}
    pairs.sort(key=lambda p: (order[p.status], p.distance_mm))
    volume = k.volume(envelope(moving, joint)) if with_volume else None
    return SweepReport(part=moving.id, unit="deg" if joint.kind == "revolute" else "mm",
                       positions=[round(q, 3) for q in qs], box_min=tuple(np.round(lo, 2)),
                       box_max=tuple(np.round(hi, 2)), pairs=pairs,
                       envelope_mm3=None if volume is None else round(volume, 1))  # fmt: skip
