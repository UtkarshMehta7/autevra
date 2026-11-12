"""Tooling checks for moulded and cast parts: draft analysis against a pull direction.

For every face the surface normal n is sampled on a 3 x 3 grid of its parameter range
(points of trimmed surfaces may fall outside the trim; the sample is an estimate). The
draft angle is the angle between the face and the pull direction d:
draft = 90 deg - angle(n, d) for faces released towards +d (cavity side), measured on |n.d|.
Classes per face (by the worst sample):
- "perpendicular": faces across the pull (|n.d| ~ 1, e.g. tops and parting faces);
- "drafted": walls with |draft| >= the minimum;
- "insufficient": walls with |draft| below the minimum (vertical walls drag in the tool);
and each face's side: "cavity" (n.d > 0) or "core" (n.d < 0). Areas are summed per class.
A typical minimum draft is 1-2 degrees for moulded plastics and 1-3 for die castings.
"""

import math

import cadquery as cq
import numpy as np
from pydantic import BaseModel


class DraftFace(BaseModel):
    index: int
    area_mm2: float
    min_draft_deg: float
    side: str
    status: str


class DraftReport(BaseModel):
    pull: tuple[float, float, float]
    min_draft_deg: float
    faces: list[DraftFace]
    area_mm2: dict[str, float]
    ok: bool


def draft(
    shape: cq.Shape, pull: tuple[float, float, float] = (0.0, 0.0, 1.0), min_draft_deg: float = 1.0
) -> DraftReport:
    d = np.array(pull, dtype=float)
    d /= np.linalg.norm(d)
    faces = []
    for i, face in enumerate(shape.Faces()):
        u0, u1, v0, v1 = face._uvBounds()
        drafts, dots = [], []
        for fu in (0.2, 0.5, 0.8):
            for fv in (0.2, 0.5, 0.8):
                n, _ = face.normalAt(u0 + fu * (u1 - u0), v0 + fv * (v1 - v0))
                nv = np.array([n.x, n.y, n.z])
                nv /= np.linalg.norm(nv) or 1.0
                dot = float(nv @ d)
                dots.append(dot)
                drafts.append(math.degrees(math.asin(min(1.0, abs(dot)))))
        worst = min(drafts)
        mean_dot = float(np.mean(dots))
        if worst >= 89.0:
            status = "perpendicular"
        elif worst >= min_draft_deg:
            status = "drafted"
        else:
            status = "insufficient"
        faces.append(DraftFace(index=i, area_mm2=round(face.Area(), 2),
                               min_draft_deg=round(worst, 3),
                               side="cavity" if mean_dot >= 0 else "core",
                               status=status))  # fmt: skip
    totals = {k: round(sum(f.area_mm2 for f in faces if f.status == k), 1)
              for k in ("perpendicular", "drafted", "insufficient")}  # fmt: skip
    return DraftReport(pull=tuple(d.tolist()), min_draft_deg=min_draft_deg, faces=faces,  # type: ignore[arg-type]
                       area_mm2=totals, ok=totals["insufficient"] == 0)  # fmt: skip


# --- parting line, undercuts and clamp force -----------------------------------------


class Undercut(BaseModel):
    index: int
    side: str
    area_mm2: float  # the blocked part of the face (sampled)


class PartingReport(BaseModel):
    pull: tuple[float, float, float]
    cavity_faces: int
    core_faces: int
    wall_faces: int  # parallel to the pull: no draft, either half could form them
    parting_edges: int
    parting_length_mm: float
    parting_height_mm: tuple[float, float]  # extent of the parting line along the pull
    flat: bool
    projected_area_mm2: float
    clamp_kn: float
    undercuts: list[Undercut]
    verdict: str


def parting(
    shape: cq.Shape,
    pull: tuple[float, float, float] = (0.0, 0.0, 1.0),
    cavity_pressure_mpa: float = 40.0,
    samples_per_face: int = 40,
) -> PartingReport:
    """Split a part's faces between the two halves of a straight-pull tool.

    Each face is meshed; a triangle belongs to the cavity half when its normal has a
    component along the pull (n.d > 0.01), to the core half when against it, and is a wall
    otherwise. The parting line is the set of edges shared by a cavity face and a core
    face. A face is undercut where a ray from it in its release direction (+d for cavity,
    -d for core) meets the part again: that area cannot leave a two-plate tool and needs a
    side action, a lifter or a design change. The projected area is the sum of n.d dA over
    the cavity half, and the clamp force is that area times the cavity pressure (30-60 MPa
    is usual for injection moulding; the value is the caller's). Undercut area is sampled
    (up to ``samples_per_face`` triangles per face).
    """
    from OCP.gp import gp_Dir, gp_Lin, gp_Pnt
    from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector

    from autevra.cad import kernel as k

    d = np.array(pull, dtype=float)
    d /= np.linalg.norm(d)
    caster = IntCurvesFace_ShapeIntersector()
    caster.Load(shape.wrapped, 1e-6)
    lo, hi = k.bounds(shape)
    reach = 2.0 * float(np.linalg.norm(np.array(hi) - np.array(lo))) + 1.0

    sides: list[str] = []
    undercuts: list[Undercut] = []
    projected = 0.0
    for i, face in enumerate(shape.Faces()):
        mesh = k.tessellate(face, 0.2)
        v = np.array(mesh.vertices).reshape(-1, 3)
        tri = np.array(mesh.indices, dtype=int).reshape(-1, 3)
        if len(tri) == 0:
            sides.append("wall")
            continue
        cross = np.cross(v[tri[:, 1]] - v[tri[:, 0]], v[tri[:, 2]] - v[tri[:, 0]])
        areas = 0.5 * np.linalg.norm(cross, axis=1)
        dots = (cross @ d) / np.maximum(2.0 * areas, 1e-12)
        flux = float(np.sum(dots * areas))
        mean = flux / max(float(areas.sum()), 1e-12)
        side = "cavity" if mean > 0.01 else "core" if mean < -0.01 else "wall"
        sides.append(side)
        if side == "wall":
            continue
        if side == "cavity":
            projected += flux
        sign = 1.0 if side == "cavity" else -1.0
        centres = v[tri].mean(axis=1)
        picks = range(0, len(tri), max(1, len(tri) // samples_per_face))
        blocked = seen = 0.0
        for j in picks:
            if abs(dots[j]) < 0.01:
                continue
            seen += areas[j]
            p = centres[j] + sign * d * 0.02
            line = gp_Lin(gp_Pnt(*p), gp_Dir(*(sign * d)))
            caster.Perform(line, 0.0, reach)
            if caster.IsDone() and caster.NbPnt() > 0:
                blocked += areas[j]
        if seen > 0 and blocked / seen > 0.02:
            undercuts.append(Undercut(index=i, side=side,
                                      area_mm2=round(face.Area() * blocked / seen, 1)))  # fmt: skip

    # Parting line: edges shared by a cavity face and a core face.
    owners: dict[int, tuple[cq.Edge, set[str]]] = {}
    for face, side in zip(shape.Faces(), sides, strict=True):
        for edge in face.Edges():
            owners.setdefault(edge.hashCode(), (edge, set()))[1].add(side)
    line = [e for e, s in owners.values() if {"cavity", "core"} <= s]
    heights = [float(np.array(p.toTuple()) @ d) for e in line
               for p in (e.startPoint(), e.endPoint(), e.positionAt(0.5))]  # fmt: skip
    span = (round(min(heights), 3), round(max(heights), 3)) if heights else (0.0, 0.0)
    walls = sides.count("wall")
    if undercuts:
        verdict = (f"{len(undercuts)} face(s) are undercut along this pull: side actions, "
                   "lifters or a design change are needed")  # fmt: skip
    elif not line and walls:
        verdict = ("opens straight, but the walls are parallel to the pull: the parting can "
                   "sit anywhere along them, and they need draft")  # fmt: skip
    elif walls:
        verdict = "opens straight; walls parallel to the pull need draft"
    else:
        verdict = "opens straight in a two-plate tool"
    return PartingReport(
        pull=tuple(d.tolist()),  # type: ignore[arg-type]
        cavity_faces=sides.count("cavity"), core_faces=sides.count("core"), wall_faces=walls,
        parting_edges=len(line), parting_length_mm=round(sum(e.Length() for e in line), 2),
        parting_height_mm=span, flat=bool(heights) and span[1] - span[0] < 1e-3,
        projected_area_mm2=round(projected, 1),
        clamp_kn=round(projected * cavity_pressure_mpa / 1000.0, 2),
        undercuts=undercuts, verdict=verdict)  # fmt: skip
