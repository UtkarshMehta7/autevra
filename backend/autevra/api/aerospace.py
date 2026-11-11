"""Aircraft module API: analyse a parametric aircraft (aerodynamics, stability,
performance), keep each aircraft project's specification, and build the aircraft as a
Part Design part. Aircraft live only in aircraft (aerospace) projects: the modules are kept
apart."""

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from autevra.aero import aircraft as ac
from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import CommandError
from autevra.part.features import PartDoc

router = APIRouter(tags=["aerospace"], dependencies=[Depends(access.guard_project)])


@router.get("/aero/spec")
def spec_schema() -> dict:
    """The specification's fields (defaults, limits) for the form."""
    return {"defaults": ac.AircraftSpec().model_dump(),
            "schema": ac.AircraftSpec.model_json_schema()}  # fmt: skip


@router.post("/aero/analyse")
def analyse(spec: ac.AircraftSpec) -> dict:
    try:
        return ac.analyse(spec)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        detail = f"cannot analyse this aircraft: {exc}"
        raise HTTPException(status_code=422, detail=detail) from None


def _aircraft_project(ws: Workspace, project_id: str) -> None:
    if ws.project(project_id).domain != "aerospace":
        raise HTTPException(status_code=422, detail="aircraft are designed in Aircraft "
                            "projects; create one in the Aircraft module")  # fmt: skip


def _spec_path(ws: Workspace, project_id: str) -> Path:
    path = Path(ws.data_dir) / "aircraft" / f"{project_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@router.get("/projects/{project_id}/aircraft/spec")
def get_spec(project_id: str, ws: WorkspaceDep) -> ac.AircraftSpec:
    """The project's aircraft specification (the defaults until one is saved)."""
    _aircraft_project(ws, project_id)
    path = _spec_path(ws, project_id)
    if path.exists():
        return ac.AircraftSpec.model_validate(json.loads(path.read_text()))
    return ac.AircraftSpec(name=ws.project(project_id).name)


@router.put("/projects/{project_id}/aircraft/spec")
def put_spec(project_id: str, spec: ac.AircraftSpec, ws: WorkspaceDep) -> ac.AircraftSpec:
    _aircraft_project(ws, project_id)
    _spec_path(ws, project_id).write_text(spec.model_dump_json(indent=1))
    return spec


@router.post("/projects/{project_id}/aircraft", response_model=schemas.PartOut)
def build(project_id: str, spec: ac.AircraftSpec, ws: WorkspaceDep) -> schemas.PartOut:
    """Save the specification and create (or update) the aircraft's parts: the airframe
    (returned) plus canopy, propeller, spinner, gear and wheels, each in its own colour."""
    put_spec(project_id, spec, ws)
    docs = [PartDoc.model_validate(d) for d in ac.parts(spec)]
    try:
        parts = ws._part_docs(project_id)
        by_name = {d.name: pid for pid, d in parts}
        known = {d.name for d in docs[1:]}
        airframe_id = by_name.get(docs[0].name)
        if airframe_id is None:  # renamed: the airframe is the project's first other part
            airframe_id = next((pid for pid, d in parts if d.name not in known), None)
        out = (ws.update_part(project_id, airframe_id, docs[0]) if airframe_id
               else ws.create_part(project_id, docs[0]))  # fmt: skip
        for doc in docs[1:]:
            pid = by_name.get(doc.name)
            if pid:
                ws.update_part(project_id, pid, doc)
            else:
                ws.create_part(project_id, doc)
        return out
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
