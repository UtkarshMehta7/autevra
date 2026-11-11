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
    """Save the specification and create (or update) the aircraft part of the project."""
    put_spec(project_id, spec, ws)
    doc = PartDoc.model_validate(ac.geometry(spec))
    try:
        parts = ws._part_docs(project_id)
        existing = next((pid for pid, d in parts if d.name == doc.name), None)
        if existing is None and parts:  # renamed: the project's aircraft is its first part
            existing = parts[0][0]
        if existing is not None:
            return ws.update_part(project_id, existing, doc)
        return ws.create_part(project_id, doc)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
