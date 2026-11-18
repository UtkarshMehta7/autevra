"""Machine elements API (shared by every module): bolted joints, fillet welds, fatigue
(stress-life and rainflow damage), helical springs and spur gear pairs; a gear pair can
be added to a project as two parts in mesh."""

from fastapi import APIRouter, Depends, HTTPException

from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
from autevra.core.commands import CommandError
from autevra.elements import fatigue, gears, joints, springs
from autevra.part.features import PartDoc

router = APIRouter(tags=["elements"], dependencies=[Depends(access.guard_project)])


def _run(fn, body):  # noqa: ANN001, ANN202
    try:
        return fn(body)
    except (ValueError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/elements/bolt")
def bolt(body: joints.BoltJointIn) -> dict:
    return _run(joints.bolt_joint, body)


@router.post("/elements/weld")
def weld(body: joints.FilletWeldIn) -> dict:
    return _run(joints.fillet_weld, body)


@router.post("/elements/fatigue")
def fatigue_check(body: fatigue.FatigueIn) -> dict:
    return _run(fatigue.check, body)


@router.post("/elements/fatigue/history")
def fatigue_history(body: fatigue.HistoryIn) -> dict:
    return _run(fatigue.damage, body)


@router.post("/elements/spring")
def spring(body: springs.SpringIn) -> dict:
    return _run(springs.spring, body)


@router.post("/elements/gears")
def gear_pair(body: gears.GearPairIn) -> dict:
    out = _run(gears.pair, body)
    for key, g in (("gear1", out["gear1"]), ("gear2", out["gear2"])):
        out[key] = {
            **g,
            "outline": gears.tooth_outline(
                body.module, g["z"], g["x"], body.pressure_angle, g["da"], g["df"]
            ),
        }
    return out


@router.post("/projects/{project_id}/elements/gears", response_model=list[schemas.PartOut])
def add_gears(project_id: str, body: gears.GearPairIn, ws: WorkspaceDep) -> list[schemas.PartOut]:
    """Add the gear pair to the project as two parts placed in mesh."""
    try:
        return [
            ws.create_part(project_id, PartDoc.model_validate(p)) for p in gears.pair_parts(body)
        ]
    except (ValueError, CommandError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
