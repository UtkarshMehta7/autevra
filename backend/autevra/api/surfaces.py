"""Surface laboratory API: NURBS evaluation with its mathematics exposed (basis functions,
knots, curvature), knot insertion, and continuity analysis between two patches. The
mathematics is in ``autevra.geometry`` (no kernel)."""

from typing import Annotated, Literal

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from autevra.geometry import continuity as ct
from autevra.geometry import nurbs as nb

router = APIRouter(prefix="/surfaces", tags=["surfaces"])

Coord = Annotated[float, Field(ge=-1e6, le=1e6)]


class SurfaceIn(BaseModel):
    degree_u: int = Field(ge=1, le=7)
    degree_v: int = Field(ge=1, le=7)
    control: list[list[tuple[Coord, Coord, Coord]]] = Field(min_length=2, max_length=24)
    weights: list[list[Annotated[float, Field(gt=0, le=100)]]] | None = None
    knots_u: list[float] | None = None
    knots_v: list[float] | None = None

    def surface(self) -> nb.Surface:
        try:
            control = [[list(p) for p in row] for row in self.control]
            return nb.Surface.build(self.degree_u, self.degree_v, control, self.weights,
                                    self.knots_u, self.knots_v)  # fmt: skip
        except nb.NurbsError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from None


def _out(s: nb.Surface) -> dict:
    return {
        "degree_u": s.degree_u, "degree_v": s.degree_v,
        "control": s.control.tolist(), "weights": s.weights.tolist(),
        "knots_u": s.knots_u, "knots_v": s.knots_v,
    }  # fmt: skip


class EvaluateIn(BaseModel):
    surface: SurfaceIn
    samples: int = Field(default=33, ge=3, le=81)
    selected: tuple[int, int] | None = None  # a control point (i, j) to report the support of


@router.post("/evaluate")
def evaluate(body: EvaluateIn) -> dict:
    """The surface sampled on a (u, v) grid with normals and Gaussian and mean curvature;
    the basis functions in u and v; and for a selected control point its local support
    (the knot spans where its basis functions are non-zero, i.e. where moving it moves
    the surface)."""
    s = body.surface.surface()
    nu, nv = s.weights.shape
    out = {
        "surface": _out(s),
        "grid": s.grid(body.samples, body.samples),
        "basis_u": nb.basis_table(s.knots_u, s.degree_u, nu),
        "basis_v": nb.basis_table(s.knots_v, s.degree_v, nv),
        "domain": s.domain,
        "support": None,
    }
    if body.selected is not None:
        i, j = body.selected
        if not (0 <= i < nu and 0 <= j < nv):
            raise HTTPException(status_code=422, detail="no such control point")
        out["support"] = {
            "u": (s.knots_u[i], s.knots_u[i + s.degree_u + 1]),
            "v": (s.knots_v[j], s.knots_v[j + s.degree_v + 1]),
            "point": s.control[i, j].tolist(), "weight": float(s.weights[i, j]),
        }  # fmt: skip
    return out


class InsertIn(BaseModel):
    surface: SurfaceIn
    direction: Literal["u", "v"]
    t: float


@router.post("/insert-knot")
def insert_knot(body: InsertIn) -> dict:
    """Insert one knot (Boehm): one more row or column of control points, the same shape."""
    s = body.surface.surface()
    try:
        out = s.insert_knot_u(body.t) if body.direction == "u" else s.insert_knot_v(body.t)
    except nb.NurbsError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    before = [s.point(*uv).tolist() for uv in _probe(s)]
    after = [out.point(*uv).tolist() for uv in _probe(s)]
    drift = float(np.max(np.abs(np.asarray(before) - np.asarray(after))))
    return {"surface": _out(out), "max_shape_change": drift}


def _probe(s: nb.Surface) -> list[tuple[float, float]]:
    (u0, u1), (v0, v1) = s.domain
    return [(u0 + (u1 - u0) * a, v0 + (v1 - v0) * b) for a in (0.1, 0.5, 0.9) for b in (0.2, 0.7)]


class JoinIn(BaseModel):
    surface: SurfaceIn
    target: Literal["G0", "G1", "G2"]
    bend: float = Field(default=0.0, ge=-1e4, le=1e4)


@router.post("/join")
def join(body: JoinIn) -> dict:
    """A second patch continuing the first across its u = 1 edge, built to G0, G1 or G2."""
    try:
        return {"surface": _out(ct.join(body.surface.surface(), body.target, body.bend))}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


class ContinuityIn(BaseModel):
    a: SurfaceIn
    b: SurfaceIn
    samples: int = Field(default=21, ge=3, le=101)
    comb_scale: float = Field(default=2000.0, ge=0, le=1e7)


@router.post("/continuity")
def continuity(body: ContinuityIn) -> dict:
    """Continuity across A's u = 1 edge and B's u = 0 edge (G0 gap, G1 normal angle, G2
    normal-curvature jump, G3 estimate), with curvature combs across the join."""
    a, b = body.a.surface(), body.b.surface()
    report = ct.analyse(a, b, body.samples)
    (_, (va0, va1)), (_, (vb0, vb1)) = a.domain, b.domain
    combs = []
    for t in (0.0, 0.5, 1.0):
        combs.append(ct.comb(a, va0 + t * (va1 - va0), scale=body.comb_scale))
        combs.append(ct.comb(b, vb0 + t * (vb1 - vb0), scale=body.comb_scale))
    return {"report": report.as_dict(), "tolerances": ct.TOL, "combs": combs}
