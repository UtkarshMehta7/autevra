"""Assembly design API: constraints (Fix, Coincidence, Contact, Offset, Angle) between a
project's parts, the faces they can reference, and solving them into part placements."""

import math

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from autevra.api import access
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.assembly import constraints as ac
from autevra.part.build import placement_matrix
from autevra.part.features import Placement

router = APIRouter(tags=["assembly"], dependencies=[Depends(access.guard_project)])


class MatesDoc(BaseModel):
    constraints: list[ac.Constraint] = Field(default_factory=list, max_length=500)


def _path(ws: Workspace, project_id: str):  # noqa: ANN202
    folder = ws.data_dir / "assembly"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{project_id}.json"


def _load(ws: Workspace, project_id: str) -> MatesDoc:
    path = _path(ws, project_id)
    if not path.exists():
        return MatesDoc()
    return MatesDoc.model_validate_json(path.read_text())


def _parts(ws: Workspace, project_id: str) -> dict:
    """Built parts: id -> (doc, shape in the part frame, signatures)."""
    from autevra.api import model_service

    out = {}
    for pid, doc in ws._part_docs(project_id):
        _, report = model_service.build_part(doc, ws.cache)
        if report.shape is not None:
            out[pid] = (doc, report.shape, ac.face_signatures(report.shape))
    return out


@router.get("/projects/{project_id}/mates")
def get_mates(project_id: str, ws: WorkspaceDep) -> MatesDoc:
    ws.project(project_id)
    return _load(ws, project_id)


@router.put("/projects/{project_id}/mates")
def put_mates(project_id: str, body: MatesDoc, ws: WorkspaceDep) -> MatesDoc:
    """Store the constraints; face references get their signature from the current build
    so they survive later edits of the parts."""
    ws.project(project_id)
    built = _parts(ws, project_id)
    ids = [c.id for c in body.constraints]
    if len(ids) != len(set(ids)):
        raise HTTPException(status_code=422, detail="constraint ids must be unique")
    fixed = []
    for c in body.constraints:
        if c.kind == "fix":
            if c.part not in built:
                raise HTTPException(status_code=422, detail=f"{c.id}: no part {c.part}")
            fixed.append(c)
            continue
        refs = []
        for ref in (c.a, c.b):
            if ref is None or ref.part not in built:
                raise HTTPException(status_code=422, detail=f"{c.id}: pick a face on two parts")
            sigs = built[ref.part][2]
            if ref.face >= len(sigs):
                raise HTTPException(status_code=422, detail=f"{c.id}: part has no face {ref.face}")
            refs.append(ref if ref.sig else ref.model_copy(update={"sig": sigs[ref.face]}))
        fixed.append(c.model_copy(update={"a": refs[0], "b": refs[1]}))
    doc = MatesDoc(constraints=fixed)
    _path(ws, project_id).write_text(doc.model_dump_json(indent=1))
    return doc


@router.get("/projects/{project_id}/mates/faces/{part_id}")
def part_faces(project_id: str, part_id: str, ws: WorkspaceDep) -> list[dict]:
    """The part's faces (part frame) with signatures and outlines for highlighting."""
    from autevra.api import model_service

    doc = dict(ws._part_docs(project_id)).get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="no such part")
    _, report = model_service.build_part(doc, ws.cache)
    if report.shape is None:
        raise HTTPException(status_code=422, detail="the part does not build")
    sigs = ac.face_signatures(report.shape)
    outlines = ac.face_outlines(report.shape)
    out = []
    for i, (s, line) in enumerate(zip(sigs, outlines, strict=True)):
        if s.kind == "plane":
            n = s.direction
            axis = max(range(3), key=lambda a: abs(n[a]))
            label = (
                f"plane {'+' if n[axis] > 0 else '−'}{'XYZ'[axis]}"
                if abs(n[axis]) > 0.999
                else "plane"
            )
        elif s.kind == "cylinder":
            label = f"cylinder ⌀{2 * s.radius:.4g}"
        else:
            label = "freeform"
        out.append(
            {
                "index": i,
                "kind": s.kind,
                "label": label,
                "sig": s.model_dump(),
                "outline": [[round(c, 3) for c in p] for p in line],
            }
        )
    return out


class SolveOut(BaseModel):
    status: list[dict]
    dof: int
    dof_by_part: dict[str, int]
    conflicts: list[str]
    moved: list[str]
    notes: list[str]
    fixed: list[str]
    placements: dict[str, Placement]
    applied: bool


@router.post("/projects/{project_id}/mates/solve", response_model=SolveOut)
def solve_mates(project_id: str, ws: WorkspaceDep, apply: bool = Query(True)) -> SolveOut:
    """Solve the stored constraints and (by default) move the parts to the solution; each
    moved part's placement is one undoable edit. Nothing moves when a constraint conflicts."""
    doc = _load(ws, project_id)
    built = _parts(ws, project_id)
    placements = {p: placement_matrix(d.at) for p, (d, _, _) in built.items()}
    sigs = {p: s for p, (_, _, s) in built.items()}
    centres = {}
    for p, (_, shape, _) in built.items():
        c = shape.BoundingBox().center
        centres[p] = (placements[p] @ np.array([c.x, c.y, c.z, 1.0]))[:3]
    try:
        out = ac.solve(doc.constraints, placements, sigs, centres)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    new = {}
    for p in out["moved"]:
        m = out["placements"][p]
        rx, ry, rz = ac.euler_xyz(m)
        new[p] = Placement(
            x=round(m[0, 3], 6),
            y=round(m[1, 3], 6),
            z=round(m[2, 3], 6),
            rx=round(rx, 6),
            ry=round(ry, 6),
            rz=round(rz, 6),
        )
    applied = apply and not out["conflicts"]
    if applied:
        for p, at in new.items():
            d = built[p][0]
            if any(
                not math.isclose(getattr(d.at, k), getattr(at, k), abs_tol=1e-6)
                for k in ("x", "y", "z", "rx", "ry", "rz")
            ):
                ws.update_part(project_id, p, d.model_copy(update={"at": at}))
    return SolveOut(
        status=out["status"],
        dof=out["dof"],
        dof_by_part=out["dof_by_part"],
        conflicts=out["conflicts"],
        moved=out["moved"],
        notes=out["notes"],
        fixed=out["fixed"],
        placements=new,
        applied=applied,
    )
