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
                               side="cavity" if mean_dot >= 0 else "core", status=status))  # fmt: skip
    totals = {k: round(sum(f.area_mm2 for f in faces if f.status == k), 1)
              for k in ("perpendicular", "drafted", "insufficient")}  # fmt: skip
    return DraftReport(pull=tuple(d.tolist()), min_draft_deg=min_draft_deg, faces=faces,  # type: ignore[arg-type]
                       area_mm2=totals, ok=totals["insufficient"] == 0)  # fmt: skip
