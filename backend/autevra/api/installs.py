"""Install an inventory engine as the powertrain of a land vehicle or an aircraft.

The engine stays linked to its item version: the consumer's design takes the engine's
power (and, in its breakdown, the engine's mass), compatibility is checked for the
consumer's domain, and a newer released version shows its impact before an explicit
upgrade. Parameter changes go through the consumer's own command history.

Checks (concept level, each with its basis):
- land vehicles: power-to-weight; the engine's length against the space available
  (transverse front engine: body width less 0.6 m for wheels and gearbox; longitudinal
  front engine: front overhang plus a quarter of the wheelbase less 0.25 m for radiator and
  bumper; mid engine: 45 % of the wheelbase);
- aircraft: propeller tip Mach number at the engine's maximum speed (direct drive) and the
  cruise speed, against the usual 0.85 (warn to 0.92); engine mass fraction of MTOW.
"""

import json
import math
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from autevra.aero import aircraft as ac
from autevra.api import access
from autevra.api.aerospace import get_spec, put_spec
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import Change, CommandError, Operation, SetParameters, Source
from autevra.inventory.model import Item
from autevra.inventory.store import Inventory, InventoryError

router = APIRouter(tags=["installs"], dependencies=[Depends(access.guard_project)])


class InstallEngineIn(BaseModel):
    item: str
    version: str | None = None


def _path(ws: Workspace, project_id: str) -> Path:
    path = Path(ws.data_dir) / "installs" / f"{project_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def installed(ws: Workspace, project_id: str) -> dict[str, str] | None:
    path = _path(ws, project_id)
    return json.loads(path.read_text()).get("engine") if path.exists() else None


def engine_values(ws: Workspace, project_id: str) -> dict[str, Any]:
    """Design values a consumer's breakdown reads from its installed engine."""
    link = installed(ws, project_id)
    if not link:
        return {}
    try:
        item = Inventory(ws.data_dir).get(link["item"], link["version"])
    except InventoryError:
        return {}
    return {"installed_engine_mass_kg": float(item.properties.get("mass_kg", 0.0)),
            "installed_engine_label": f"{item.name} v{item.version}"}  # fmt: skip


def _engine(ws: Workspace, item_id: str, version: str | None) -> Item:
    try:
        item = Inventory(ws.data_dir).get(item_id, version)
    except InventoryError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None
    if item.category != "Engines" or not any(p.kind == "mechanical.shaft" for p in item.ports):
        raise HTTPException(status_code=422, detail=f"'{item.name}' is not an engine with a "
                            "crank output")  # fmt: skip
    return item


def _length_mm(item: Item) -> float:
    p = item.parameters
    n, b = float(p.get("cylinders", 4)), float(p.get("bore", 86))
    banks = 1 if p.get("layout", "inline") == "inline" else 2
    return (n / banks) * 1.2 * b + 0.35 * b + 0.75 * b  # block + flywheel and pulley


def _check(cid: str, label: str, status: str, message: str) -> dict[str, str]:
    return {"id": cid, "label": label, "status": status, "message": message}


def land_checks(item: Item, values: dict[str, float]) -> list[dict[str, str]]:
    kw = float(item.performance["peak_power_kw"])
    mass = values["vehicle_mass"]
    out = [
        _check(
            "power_to_weight",
            "Power to weight",
            "pass",
            f"{kw / mass * 1000:.0f} kW/t with {kw:.0f} kW in {mass:.0f} kg",
        )
    ]
    length = _length_mm(item)
    style = int(round(values.get("body_style", 0)))
    rear = values.get("front_drive_share", 0.0) < 100.0
    if style == 11:  # supercar: mid engine
        space, basis = 0.45 * values["wheelbase"], "45 % of the wheelbase (mid engine)"
    elif rear:
        space = values["front_overhang"] + 0.25 * values["wheelbase"] - 250
        basis = "front overhang + a quarter of the wheelbase - 0.25 m (longitudinal)"
    else:
        space, basis = values["body_width"] - 600, "body width - 0.6 m (transverse)"
    status = "pass" if length <= space else "warn" if length <= 1.1 * space else "fail"
    out.append(
        _check(
            "fits",
            "Engine bay",
            status,
            f"engine {length:.0f} mm long vs {space:.0f} mm available ({basis})",
        )
    )
    return out


def aircraft_checks(item: Item, spec: ac.AircraftSpec) -> list[dict[str, str]]:
    rpm = float(item.parameters.get("rpm_max", 2700))
    a = ac.isa(spec.cruise_altitude)["a"]
    tip = math.pi * spec.prop_diameter * rpm / 60
    mach = math.hypot(tip, spec.cruise_speed) / a
    status = "pass" if mach <= 0.85 else "warn" if mach <= 0.92 else "fail"
    out = [_check("tip_mach", "Propeller tip Mach", status,
                  f"{mach:.2f} at {rpm:.0f} rpm direct drive with a {spec.prop_diameter:.2f} m "
                  "propeller (keep under about 0.85; a reduction gearbox lowers it)")]  # fmt: skip
    frac = float(item.properties.get("mass_kg", 0)) / spec.mtow
    out.append(
        _check(
            "mass_fraction",
            "Engine mass fraction",
            "pass" if frac <= 0.22 else "warn",
            f"{frac:.0%} of MTOW (light aircraft engines about 10-20 %)",
        )
    )
    return out


@router.post("/projects/{project_id}/install-engine")
def install_engine(project_id: str, body: InstallEngineIn, ws: WorkspaceDep) -> dict:
    """Install a released engine (or a given version) as the project's powertrain."""
    item = _engine(ws, body.item, body.version)
    domain = ws.project(project_id).domain
    kw = float(item.performance["peak_power_kw"])
    if domain == "automotive":
        values = dict(ws.project(project_id).values)
        n = int(item.parameters.get("cylinders", 4))
        cyl = 0 if n <= 3 else 1 if n <= 5 else 2 if n <= 6 else 3
        changes = [
            Change(
                parameter="peak_power",
                operation=Operation.SET,
                value=round(min(max(kw, 20.0), 1000.0), 1),
            ),
            Change(parameter="engine_cylinders", operation=Operation.SET, value=cyl),
        ]
        if values.get("powertrain_type", 0) == 2:  # electric: becomes a combustion car
            changes.append(Change(parameter="powertrain_type", operation=Operation.SET,
                                  value=0))  # fmt: skip
        command = SetParameters(
            changes=tuple(changes),
            source=Source.API,
            instruction=f"install engine {item.name} v{item.version}",
        )
        try:
            ws.apply(project_id, command)
        except (CommandError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from None
        checks = land_checks(item, dict(ws.project(project_id).values))
    elif domain == "aerospace":
        spec = get_spec(project_id, ws).model_copy(update={"power_kw": round(kw, 1)})
        put_spec(project_id, spec, ws)
        checks = aircraft_checks(item, spec)
    else:
        raise HTTPException(status_code=422, detail="engines are installed in Land vehicles "
                            "or Aircraft projects")  # fmt: skip
    _path(ws, project_id).write_text(json.dumps(
        {"engine": {"item": item.id, "version": item.version}}, indent=1))  # fmt: skip
    Inventory(ws.data_dir).record(item, project_id, "powertrain")
    return {"item": item.id, "version": item.version, "name": item.name, "checks": checks}


@router.get("/projects/{project_id}/installed-engine")
def installed_engine(project_id: str, ws: WorkspaceDep) -> dict | None:
    """The installed engine, the latest released version and the impact of upgrading."""
    link = installed(ws, project_id)
    if not link:
        return None
    inv = Inventory(ws.data_dir)
    current = inv.get(link["item"], link["version"])
    latest = inv.get(link["item"])

    def delta(key: str, where: str = "performance") -> float:
        a, b = getattr(current, where).get(key, 0.0), getattr(latest, where).get(key, 0.0)
        return round(float(b) - float(a), 2)

    impact = {"mass_kg": delta("mass_kg", "properties"),
              "peak_power_kw": delta("peak_power_kw"),
              "peak_torque_nm": delta("peak_torque_nm")}  # fmt: skip
    return {"item": current.id, "name": current.name, "version": current.version,
            "latest": latest.version, "upgrade_available": latest.version != current.version,
            "impact": impact}  # fmt: skip


@router.post("/projects/{project_id}/installed-engine/upgrade")
def upgrade(project_id: str, ws: WorkspaceDep) -> dict:
    link = installed(ws, project_id)
    if not link:
        raise HTTPException(status_code=404, detail="no engine installed")
    return install_engine(project_id, InstallEngineIn(item=link["item"]), ws)


@router.get("/projects/{project_id}/installed-engine/performance")
def performance(project_id: str, ws: WorkspaceDep) -> dict:
    """Full-throttle acceleration of a land vehicle through a stepped gearbox driven by the
    installed engine's own torque curve, next to the ideal constant-power (CVT) result: the
    vehicle's performance follows the engine version."""
    from autevra.domains.automotive import derived as d
    from autevra.domains.automotive import tests as vt
    from autevra.domains.automotive.sim import geared as gd
    from autevra.domains.automotive.sim import longitudinal as lon

    if ws.project(project_id).domain != "automotive":
        raise HTTPException(status_code=422, detail="acceleration runs for land vehicles")
    link = installed(ws, project_id)
    if not link:
        raise HTTPException(status_code=404, detail="no engine installed")
    item = Inventory(ws.data_dir).get(link["item"], link["version"])
    curve = item.maps.get("torque_curve", [])
    if len(curve) < 3:
        raise HTTPException(status_code=422, detail="the engine publishes no torque curve")
    values = dict(ws.project(project_id).values)
    params = vt.longitudinal_params(values)
    eng = gd.Engine(tuple(p["rpm"] for p in curve), tuple(p["torque_nm"] for p in curve))
    radius = d.tyre_radius(values) / 1000.0 * 0.97  # dynamic radius about 3 % under free
    geared = gd.performance(params, eng, radius)
    cvt = lon.simulate(params, lon.Manoeuvre(kind="accelerate"))
    return {"engine": f"{item.name} v{item.version}", **geared,
            "cvt_zero_to_100_s": cvt.metrics.get("accel_time")}  # fmt: skip
