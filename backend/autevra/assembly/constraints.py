"""Assembly constraints between a project's parts, as in an assembly design workbench:
Fix, Coincidence, Contact, Offset and Angle on planar faces and cylinder axes.

Geometry references. A constraint names a face of a part by its index in the B-rep face
map of the built part, and stores the face's signature (surface type, normal or axis,
centre, area, radius) in the part frame. When the part is edited and the indices move
(the topological naming problem), the reference is re-matched to the face of the same type
whose signature is nearest, and the report says so.

Entities (world frame, after the part's placement): a planar face gives a plane (a point
and the outward normal n); a cylindrical face gives an axis (a point and a direction d).

Residuals:
- Coincidence: planes coplanar with the same normal (n_a - n_b = 0, (p_b - p_a) . n_a = 0);
  axes coaxial (d_a x d_b = 0, (p_b - p_a) x d_a = 0); a plane and an axis: the axis lies in
  the plane (d . n = 0, (p_axis - p_plane) . n = 0).
- Contact: planes face to face (n_a + n_b = 0, (p_b - p_a) . n_a = 0).
- Offset: planes face to face at a distance (n_a + n_b = 0, (p_b - p_a) . n_a = value).
- Angle: between the plane normals or axis directions, n_a . n_b = cos(value).
- Fix: the part does not move.

Solving. Each part not fixed gets six unknowns, a small rotation vector and a translation
applied about its centre on top of its current placement; the residuals are minimised by
Levenberg-Marquardt (scipy least_squares) from the current placements, so the parts move as
little as the constraints need. Remaining degrees of freedom come from the rank of the
Jacobian at the solution (6 n_free - rank, and per part 6 - the rank of its columns);
a constraint whose residual stays above the tolerance is reported as conflicting.
"""

import math
from typing import Literal

import cadquery as cq
import numpy as np
from pydantic import BaseModel, Field
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

from autevra.cad import kernel as k

TOL = 1e-4  # mm and radians


class FaceSig(BaseModel):
    kind: Literal["plane", "cylinder", "other"]
    centre: tuple[float, float, float]
    direction: tuple[float, float, float]  # plane normal or cylinder axis
    point: tuple[float, float, float]  # on the plane or the axis
    area: float
    radius: float = 0.0


class FaceRef(BaseModel):
    part: str = Field(min_length=1, max_length=64)
    face: int = Field(ge=0, le=100_000)
    sig: FaceSig | None = None


class Constraint(BaseModel):
    id: str = Field(min_length=1, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    kind: Literal["fix", "coincidence", "contact", "offset", "angle"]
    a: FaceRef | None = None  # fix: the part only
    b: FaceRef | None = None
    part: str | None = None  # fix
    value: float = 0.0  # offset (mm) or angle (degrees)
    suppressed: bool = False


def face_signatures(shape: k.Shape) -> list[FaceSig]:
    """Every face of the shape in B-rep map order, with its geometric signature."""
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_SurfaceType
    from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
    from OCP.TopExp import TopExp
    from OCP.TopoDS import TopoDS
    from OCP.TopTools import TopTools_IndexedMapOfShape

    faces = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape.wrapped, TopAbs_FACE, faces)
    out = []
    for i in range(1, faces.Extent() + 1):
        topo = TopoDS.Face_s(faces.FindKey(i))
        face = cq.Face(topo)
        surf = BRepAdaptor_Surface(topo)
        c = face.Center()
        area = face.Area()
        kind, direction, point, radius = "other", (0.0, 0.0, 0.0), (c.x, c.y, c.z), 0.0
        if surf.GetType() == GeomAbs_SurfaceType.GeomAbs_Plane:
            n = surf.Plane().Axis().Direction()
            sign = -1.0 if topo.Orientation() == TopAbs_REVERSED else 1.0
            kind, direction = "plane", (sign * n.X(), sign * n.Y(), sign * n.Z())
        elif surf.GetType() == GeomAbs_SurfaceType.GeomAbs_Cylinder:
            cyl = surf.Cylinder()
            ax = cyl.Axis()
            d, p = ax.Direction(), ax.Location()
            dv = np.array([d.X(), d.Y(), d.Z()])
            pv = np.array([p.X(), p.Y(), p.Z()])
            foot = pv + dv * float(np.dot(np.array([c.x, c.y, c.z]) - pv, dv))
            kind, direction, point, radius = "cylinder", tuple(dv), tuple(foot), cyl.Radius()
        out.append(
            FaceSig(
                kind=kind,
                centre=(c.x, c.y, c.z),
                direction=direction,
                point=point,
                area=area,
                radius=radius,
            )
        )
    return out


def face_outlines(shape: k.Shape, tol: float = 0.5) -> list[list[tuple[float, float, float]]]:
    """The outer boundary of every face, sampled, in the same order as face_signatures."""
    from OCP.BRepAdaptor import BRepAdaptor_CompCurve
    from OCP.BRepTools import BRepTools
    from OCP.GCPnts import GCPnts_QuasiUniformDeflection
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp
    from OCP.TopoDS import TopoDS
    from OCP.TopTools import TopTools_IndexedMapOfShape

    faces = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape.wrapped, TopAbs_FACE, faces)
    out = []
    for i in range(1, faces.Extent() + 1):
        wire = BRepTools.OuterWire_s(TopoDS.Face_s(faces.FindKey(i)))
        pts: list[tuple[float, float, float]] = []
        try:
            sampler = GCPnts_QuasiUniformDeflection(BRepAdaptor_CompCurve(wire), tol)
            pts = [
                (sampler.Value(j).X(), sampler.Value(j).Y(), sampler.Value(j).Z())
                for j in range(1, sampler.NbPoints() + 1)
            ]
        except Exception:  # degenerate wires (sphere poles) have nothing to draw
            pts = []
        out.append(pts)
    return out


def resolve(ref: FaceRef, sigs: list[FaceSig]) -> tuple[int, bool]:
    """The face index for a reference: its own index when the signature still matches,
    else the nearest face of the same type (re-matched = True)."""
    if ref.sig is None:
        if ref.face >= len(sigs):
            raise ValueError(f"part {ref.part} has no face {ref.face}")
        return ref.face, False

    def distance(s: FaceSig) -> float:
        if s.kind != ref.sig.kind:
            return math.inf
        dc = np.linalg.norm(np.subtract(s.centre, ref.sig.centre))
        dd = 1.0 - abs(float(np.dot(s.direction, ref.sig.direction)))
        da = abs(s.area - ref.sig.area) / max(ref.sig.area, 1e-9)
        dr = abs(s.radius - ref.sig.radius)
        return dc + 100.0 * dd + 10.0 * da + dr

    if ref.face < len(sigs) and distance(sigs[ref.face]) < 1e-3:
        return ref.face, False
    best = min(range(len(sigs)), key=lambda i: distance(sigs[i]), default=None)
    if best is None or math.isinf(distance(sigs[best])):
        raise ValueError(f"part {ref.part}: no {ref.sig.kind} face left to match face {ref.face}")
    return best, True


def _world(sig: FaceSig, m: np.ndarray) -> tuple[str, np.ndarray, np.ndarray]:
    r, t = m[:3, :3], m[:3, 3]
    return sig.kind, r @ np.array(sig.point) + t, r @ np.array(sig.direction)


def _residual(kind: str, ea: tuple, eb: tuple, value: float) -> list[float]:
    ka, pa, da = ea
    kb, pb, db = eb
    if kind == "angle":
        return [float(np.dot(da, db)) - math.cos(math.radians(value))]
    if ka == "plane" and kb == "plane":
        if kind == "coincidence":
            return [*(da - db), float(np.dot(pb - pa, da))]
        dist = value if kind == "offset" else 0.0
        return [*(da + db), float(np.dot(pb - pa, da)) - dist]
    if ka == "cylinder" and kb == "cylinder":
        if kind != "coincidence":
            raise ValueError(f"{kind} needs two planar faces")
        return [*np.cross(da, db), *np.cross(pb - pa, da)]
    if {ka, kb} == {"plane", "cylinder"} and kind == "coincidence":
        (pp, nn), (pc, dc) = ((pa, da), (pb, db)) if ka == "plane" else ((pb, db), (pa, da))
        return [float(np.dot(dc, nn)), float(np.dot(pc - pp, nn))]
    raise ValueError(f"{kind} is not defined between a {ka} and a {kb}")


def _pose(base: np.ndarray, x: np.ndarray, centre: np.ndarray) -> np.ndarray:
    """A small rotation (rotation vector x[:3]) about the part's centre, then a translation
    x[3:], applied on top of the base placement."""
    delta = np.eye(4)
    rot = Rotation.from_rotvec(x[:3]).as_matrix()
    delta[:3, :3] = rot
    delta[:3, 3] = centre - rot @ centre + x[3:]
    return delta @ base


def euler_xyz(m: np.ndarray) -> tuple[float, float, float]:
    """(rx, ry, rz) degrees with R = Rz Ry Rx (the part placement convention)."""
    r = m[:3, :3]
    ry = math.asin(max(-1.0, min(1.0, -r[2, 0])))
    if abs(math.cos(ry)) > 1e-9:
        rx = math.atan2(r[2, 1], r[2, 2])
        rz = math.atan2(r[1, 0], r[0, 0])
    else:  # gimbal lock: put the whole rotation about Z
        rx = 0.0
        rz = math.atan2(-r[0, 1], r[1, 1])
    return math.degrees(rx), math.degrees(ry), math.degrees(rz)


def solve(
    constraints: list[Constraint],
    placements: dict[str, np.ndarray],
    signatures: dict[str, list[FaceSig]],
    centres: dict[str, np.ndarray],
) -> dict:
    """Solve the constraints; returns new placements, per-constraint status and DOF."""
    active = [c for c in constraints if not c.suppressed]
    fixed = {c.part for c in active if c.kind == "fix" and c.part}
    unknown = [
        p
        for p in placements
        if p not in fixed
        and any(
            c.kind != "fix" and (c.a and c.a.part == p or c.b and c.b.part == p) for c in active
        )
    ]
    index = {p: i for i, p in enumerate(unknown)}
    notes: list[str] = []
    refs: list[tuple[Constraint, int, int]] = []
    for c in active:
        if c.kind == "fix":
            if c.part not in placements:
                raise ValueError(f"fix: no part {c.part}")
            continue
        if c.a is None or c.b is None:
            raise ValueError(f"{c.id}: {c.kind} needs two faces")
        if c.a.part == c.b.part:
            raise ValueError(f"{c.id}: both faces are on the same part")
        for ref in (c.a, c.b):
            if ref.part not in placements:
                raise ValueError(f"{c.id}: no part {ref.part}")
        ia, ma = resolve(c.a, signatures[c.a.part])
        ib, mb = resolve(c.b, signatures[c.b.part])
        if ma or mb:
            notes.append(f"{c.id}: a face moved after an edit and was matched again by its shape.")
        refs.append((c, ia, ib))

    def poses(x: np.ndarray) -> dict[str, np.ndarray]:
        out = dict(placements)
        for p, i in index.items():
            out[p] = _pose(placements[p], x[6 * i : 6 * i + 6], centres[p])
        return out

    def residuals(x: np.ndarray) -> np.ndarray:
        ps = poses(x)
        res: list[float] = []
        for c, ia, ib in refs:
            ea = _world(signatures[c.a.part][ia], ps[c.a.part])
            eb = _world(signatures[c.b.part][ib], ps[c.b.part])
            res += _residual(c.kind, ea, eb, c.value)
        return np.array(res or [0.0])

    x0 = np.zeros(6 * len(unknown))
    if unknown:
        # scale: a rotation of 1 rad and a move of the part's size weigh alike
        sol = least_squares(
            residuals,
            x0,
            method="lm" if len(residuals(x0)) >= len(x0) else "trf",
            xtol=1e-12,
            ftol=1e-12,
            gtol=1e-12,
            max_nfev=2000,
        )
        x = sol.x
        jac = sol.jac
    else:
        x = x0
        jac = np.zeros((len(residuals(x0)), 0))
    ps = poses(x)
    status = []
    for c, ia, ib in refs:
        ea = _world(signatures[c.a.part][ia], ps[c.a.part])
        eb = _world(signatures[c.b.part][ib], ps[c.b.part])
        r = float(np.max(np.abs(_residual(c.kind, ea, eb, c.value))))
        status.append({"id": c.id, "kind": c.kind, "residual": r, "ok": r < TOL, "faces": [ia, ib]})
    for c in active:
        if c.kind == "fix":
            status.append({"id": c.id, "kind": "fix", "residual": 0.0, "ok": True, "faces": []})
    rank = int(np.linalg.matrix_rank(jac, tol=1e-7)) if jac.size else 0
    per_part = {}
    for p, i in index.items():
        cols = jac[:, 6 * i : 6 * i + 6] if jac.size else np.zeros((1, 6))
        per_part[p] = 6 - int(np.linalg.matrix_rank(cols, tol=1e-7))
    for p in placements:
        if p in fixed:
            per_part[p] = 0
        elif p not in index:
            per_part[p] = 6
    conflicts = [s["id"] for s in status if not s["ok"]]
    if not fixed and unknown:
        notes.append(
            "No part is fixed: the solution moves parts relative to each other only; "
            "fix the base part to anchor the assembly."
        )
    return {
        "placements": ps,
        "status": status,
        "dof": 6 * len(unknown) - rank,
        "dof_by_part": per_part,
        "conflicts": conflicts,
        "moved": unknown,
        "notes": notes,
        "fixed": sorted(fixed),
    }
