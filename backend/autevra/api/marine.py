"""Marine module API: analyse a hull (hydrostatics, GZ curve and IMO criteria, total
resistance against speed), keep each marine project's specification, and build the vessel
as coloured parts. Vessels live only in Marine projects."""

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import CommandError
from autevra.marine import hull as hk
from autevra.modules.marine import geometry
from autevra.part.features import PartDoc

router = APIRouter(tags=["marine"], dependencies=[Depends(access.guard_project)])


class VesselSpec(hk.HullSpec):
    twin_shaft: bool = False
    bow_thruster: bool = False


class Analysis(BaseModel):
    hydrostatics: dict
    gz: list[dict[str, float]]
    criteria: list[dict]
    resistance: list[dict[str, float]]


@router.post("/marine/analyse", response_model=Analysis)
def analyse(spec: VesselSpec) -> Analysis:
    hs = hk.hydrostatics(spec)
    gz = hk.gz_curve(spec, [float(a) for a in range(0, 81, 5)])
    speeds = [spec.speed_kn * f for f in (0.5, 0.625, 0.75, 0.875, 1.0, 1.125, 1.25)]
    return Analysis(hydrostatics={k: v for k, v in hs.items() if not isinstance(v, list)},
                    gz=gz, criteria=hk.imo_criteria(spec, gz),
                    resistance=[{"speed_kn": v, **{k: x for k, x in hk.resistance(spec, v).items()}}
                                for v in speeds])  # fmt: skip


def _marine_project(ws: Workspace, project_id: str) -> None:
    if ws.project(project_id).domain != "marine":
        raise HTTPException(status_code=422, detail="vessels are designed in Marine projects; "
                            "create one in the Marine module")  # fmt: skip


def _spec_path(ws: Workspace, project_id: str) -> Path:
    path = Path(ws.data_dir) / "vessels" / f"{project_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@router.get("/projects/{project_id}/vessel/spec")
def get_spec(project_id: str, ws: WorkspaceDep) -> VesselSpec:
    _marine_project(ws, project_id)
    path = _spec_path(ws, project_id)
    if path.exists():
        return VesselSpec.model_validate(json.loads(path.read_text()))
    return VesselSpec(name=ws.project(project_id).name)


@router.put("/projects/{project_id}/vessel/spec")
def put_spec(project_id: str, spec: VesselSpec, ws: WorkspaceDep) -> VesselSpec:
    _marine_project(ws, project_id)
    _spec_path(ws, project_id).write_text(spec.model_dump_json(indent=1))
    return spec


@router.post("/projects/{project_id}/vessel", response_model=list[schemas.PartOut])
def build(project_id: str, spec: VesselSpec, ws: WorkspaceDep) -> list[schemas.PartOut]:
    put_spec(project_id, spec, ws)
    docs = [PartDoc.model_validate(d) for d in geometry.parts(spec, spec.twin_shaft)]
    try:
        existing = {d.name.split(": ", 1)[-1]: pid for pid, d in ws._part_docs(project_id)
                    if ": " in d.name}  # fmt: skip
        out = []
        for doc in docs:
            pid = existing.pop(doc.name.split(": ", 1)[-1], None)
            out.append(ws.update_part(project_id, pid, doc) if pid
                       else ws.create_part(project_id, doc))  # fmt: skip
        return out
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
