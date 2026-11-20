"""Digital mock-up: the clearance matrix of a project's parts.

For every pair of placed parts: when their bounding boxes are further apart than the
required clearance, the pair is clear (the box gap is a lower bound on the distance);
otherwise the exact minimum distance is computed on the B-reps (OCCT BRepExtrema), and
touching or overlapping pairs get their interference volume (B-rep intersection). Each
pair is classed as interference (volume above 1 mm³), contact, too close (below the
required clearance) or clear. Parts designed to overlap (a canopy seated in a fuselage) are
reported like any other; the engineer marks them as intended.
"""

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from pydantic import BaseModel

from autevra.cad import kernel as k


@dataclass(frozen=True)
class Placed:
    id: str
    name: str
    shape: k.Shape
    matrix: np.ndarray


class Pair(BaseModel):
    a: str
    b: str
    a_name: str
    b_name: str
    status: str  # interference | contact | too close | clear
    distance_mm: float
    interference_mm3: float = 0.0
    exact: bool


def _box(p: Placed) -> tuple[np.ndarray, np.ndarray]:
    lo, hi = k.bounds(p.shape)
    corners = np.array([[x, y, z, 1.0] for x in (lo[0], hi[0]) for y in (lo[1], hi[1])
                        for z in (lo[2], hi[2])])  # fmt: skip
    world = (p.matrix @ corners.T).T[:, :3]
    return world.min(axis=0), world.max(axis=0)


def matrix(parts: list[Placed], clearance_mm: float = 5.0) -> list[Pair]:
    boxes = {p.id: _box(p) for p in parts}
    out = []
    for a, b in combinations(parts, 2):
        (alo, ahi), (blo, bhi) = boxes[a.id], boxes[b.id]
        gap = float(np.linalg.norm(np.maximum(0.0, np.maximum(alo - bhi, blo - ahi))))
        if gap > clearance_mm:
            out.append(Pair(a=a.id, b=b.id, a_name=a.name, b_name=b.name, status="clear",
                            distance_mm=round(gap, 2), exact=False))  # fmt: skip
            continue
        dist = k.min_distance(a.shape, a.matrix, b.shape, b.matrix)
        volume = 0.0
        if dist <= 1e-6:
            try:
                common = k.intersect(a.shape.moved(k.location(a.matrix)),
                                     b.shape.moved(k.location(b.matrix)))  # fmt: skip
                volume = k.volume(common)
            except Exception:  # noqa: BLE001 (a failed boolean is reported as contact)
                volume = 0.0
        status = ("interference" if volume > 1.0 else "contact" if dist <= 1e-6 else
                  "too close" if dist < clearance_mm else "clear")  # fmt: skip
        out.append(Pair(a=a.id, b=b.id, a_name=a.name, b_name=b.name, status=status,
                        distance_mm=round(dist, 3), interference_mm3=round(volume, 1),
                        exact=True))  # fmt: skip
    order = {"interference": 0, "contact": 1, "too close": 2, "clear": 3}
    return sorted(out, key=lambda p: (order[p.status], p.distance_mm))
