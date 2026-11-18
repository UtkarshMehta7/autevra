"""Machine elements API (shared by every module): bolted joints, fillet welds, fatigue
(stress-life and rainflow damage), helical springs and spur gear pairs; a gear pair can
be added to a project as two parts in mesh."""

from fastapi import APIRouter, Depends, HTTPException

from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
from autevra.core.commands import CommandError
from autevra.elements import fatigue, gears, joints, springs, transmission
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


@router.post("/elements/transmission")
def transmission_design(body: transmission.TransmissionIn) -> dict:
    return _run(transmission.design, body)


@router.get("/projects/{project_id}/elements/transmission-inputs")
def transmission_inputs(project_id: str, ws: WorkspaceDep) -> dict:
    """Transmission inputs taken from a land-vehicle project: mass, tyre rolling radius
    (0.97 of the unloaded radius), drag area, rolling resistance, driveline efficiency,
    the load on the driven axle(s), and an engine curve consistent with the peak power
    (turbocharged petrol shape: plateau 1800-4000 rpm, power at 6000, redline 6500)."""
    from autevra.domains.automotive import derived as d

    state = ws.project(project_id)
    p = dict(state.values)
    needed = ("vehicle_mass", "peak_power", "rim_diameter", "tyre_width", "tyre_aspect_ratio")
    if any(k not in p for k in needed):
        raise HTTPException(status_code=422, detail="not a land-vehicle project")
    radius = (p["rim_diameter"] * 25.4 + 2 * p["tyre_width"] * p["tyre_aspect_ratio"] / 100) / 2000
    front = p.get("front_drive_share", 100.0)
    fm = p.get("front_mass_distribution", 55.0) / 100.0
    drive = "all" if 0.0 < front < 100.0 else ("front" if front >= 100.0 else "rear")
    share = 1.0 if drive == "all" else (fm if drive == "front" else 1.0 - fm)
    power = p["peak_power"]
    torque = 0.95 * power * 1000.0 / (4000.0 * 3.141592653589793 / 30.0)
    notes = []
    if d.powertrain(p) != "combustion":
        notes.append(
            "This vehicle is electric or hybrid: a single reduction usually suffices; "
            "the stepped design here is for comparison."
        )
    return {
        "mass_kg": p["vehicle_mass"],
        "tyre_radius_m": 0.97 * radius,
        "drag_area_m2": p.get("drag_coefficient", 0.32) * d.frontal_area(p),
        "rolling_resistance": p.get("rolling_resistance", 0.012),
        "driveline_efficiency": p.get("drivetrain_efficiency", 90.0) / 100.0,
        "driven_axle_share": share,
        "drive": drive,
        "cg_height_m": p.get("cg_height", 550.0) / 1000.0,
        "wheelbase_m": p.get("wheelbase", 2700.0) / 1000.0,
        "engine": {
            "idle_rpm": 800,
            "peak_torque_Nm": round(torque),
            "torque_from_rpm": 1800,
            "torque_to_rpm": 4000,
            "peak_power_kW": power,
            "power_rpm": 6000,
            "redline_rpm": 6500,
        },
        "notes": notes,
    }
