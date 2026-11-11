"""Aircraft workspace API: analyse a parametric aircraft (aerodynamics, stability,
performance) and build it as a Part Design part in a project."""

from fastapi import APIRouter, Depends, HTTPException

from autevra.aero import aircraft as ac
from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
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
        raise HTTPException(
            status_code=422, detail=f"cannot analyse this aircraft: {exc}"
        ) from None


@router.post("/projects/{project_id}/aircraft", response_model=schemas.PartOut)
def build(project_id: str, spec: ac.AircraftSpec, ws: WorkspaceDep) -> schemas.PartOut:
    """Create (or update, by name) the aircraft as a Part Design part of the project."""
    # placed 6 m to the left of the origin: a project also holds its vehicle there
    doc = PartDoc.model_validate(ac.geometry(spec) | {"at": {"y": 6000.0}})
    try:
        existing = next((pid for pid, d in ws._part_docs(project_id) if d.name == doc.name), None)
        if existing is not None:
            return ws.update_part(project_id, existing, doc)
        return ws.create_part(project_id, doc)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
