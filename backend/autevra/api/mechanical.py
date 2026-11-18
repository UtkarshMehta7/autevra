"""Mechanical module API: analyse a piston engine, keep each engine project's
specification, build the engine as coloured parts, and publish it to the shared inventory
as a product item with the engine interface (crank output, mounts) and its torque curve.
Engines live only in Mechanical projects: the modules are kept apart."""

import json
import re
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException

from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import CommandError
from autevra.inventory.model import Item, Port
from autevra.inventory.store import Inventory, InventoryError
from autevra.mech import electric as em
from autevra.mech import piston as pk
from autevra.mech import turbine as gt
from autevra.modules.mechanical import geometry, machines
from autevra.part.features import PartDoc

router = APIRouter(tags=["mechanical"], dependencies=[Depends(access.guard_project)])


@router.get("/engines/spec")
def spec_schema() -> dict:
    return {"defaults": pk.EngineSpec().model_dump(), "schema": pk.EngineSpec.model_json_schema()}


@router.get("/engines/presets")
def engine_presets() -> dict:
    from autevra import reference

    return reference.ENGINES


@router.post("/engines/analyse")
def analyse(spec: pk.EngineSpec) -> dict:
    return pk.analyse(spec)


def _engine_project(ws: Workspace, project_id: str) -> None:
    if ws.project(project_id).domain != "machinery":
        raise HTTPException(status_code=422, detail="engines are designed in Mechanical "
                            "projects; create one in the Mechanical module")  # fmt: skip


def _spec_path(ws: Workspace, project_id: str) -> Path:
    path = Path(ws.data_dir) / "engines" / f"{project_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@router.get("/projects/{project_id}/engine/spec")
def get_spec(project_id: str, ws: WorkspaceDep) -> pk.EngineSpec:
    _engine_project(ws, project_id)
    path = _spec_path(ws, project_id)
    if path.exists():
        return pk.EngineSpec.model_validate(json.loads(path.read_text()))
    return pk.EngineSpec(name=ws.project(project_id).name)


@router.put("/projects/{project_id}/engine/spec")
def put_spec(project_id: str, spec: pk.EngineSpec, ws: WorkspaceDep) -> pk.EngineSpec:
    _engine_project(ws, project_id)
    _spec_path(ws, project_id).write_text(spec.model_dump_json(indent=1))
    return spec


@router.post("/projects/{project_id}/engine", response_model=list[schemas.PartOut])
def build(project_id: str, spec: pk.EngineSpec, ws: WorkspaceDep) -> list[schemas.PartOut]:
    """Save the specification and create (or update) the engine's parts by name; parts of an
    earlier engine design that no longer apply (a removed turbo) are deleted."""
    put_spec(project_id, spec, ws)
    docs = [PartDoc.model_validate(d) for d in geometry.parts(spec)]
    try:
        existing = ws._part_docs(project_id)
        by_suffix = {d.name.split(": ", 1)[-1]: pid for pid, d in existing if ": " in d.name}
        out = []
        for doc in docs:
            pid = by_suffix.pop(doc.name.split(": ", 1)[-1], None)
            out.append(ws.update_part(project_id, pid, doc) if pid
                       else ws.create_part(project_id, doc))  # fmt: skip
        for pid in by_suffix.values():
            ws.delete_part(project_id, pid)
        return out
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


def engine_item(spec: pk.EngineSpec, item_id: str, provenance: str) -> Item:
    """The engine as an inventory product: the engine interface (crank output at the
    flywheel face, three mounts), mass, peak figures and the torque curve."""
    out = pk.analyse(spec)
    b = spec.bore
    banks = 1 if spec.layout == "inline" else 2
    length = (spec.cylinders // banks) * 1.2 * b + 0.35 * b
    deck = spec.stroke / 2 + spec.rod_ratio * spec.stroke + 0.55 * b
    flange = -(length / 2 + 0.36 * b)
    ports = [
        Port(name="crank_output", kind="mechanical.shaft", at={"x": flange, "ry": -90},
             attributes={"diameter": round(0.9 * b, 1), "speed_min": spec.rpm_idle,
                         "speed_max": spec.rpm_max,
                         "torque_max": round(out["peak_torque_nm"], 1)}),
        *[Port(name=f"mount_{k}", kind="mechanical.mount", at={"x": x, "y": y, "z": 0.2 * deck},
               attributes={"load_rating_n": round(9.81 * out["mass_kg"] * 3, 0)})
          for k, (x, y) in enumerate([(length / 2, 0.0), (-length / 2, 0.9 * b * banks),
                                      (-length / 2, -0.9 * b * banks)])],
    ]  # fmt: skip
    curve = [{"rpm": p["rpm"], "torque_nm": round(p["torque_nm"], 2),
              "power_kw": round(p["power_kw"], 3)} for p in out["curve"]]  # fmt: skip
    return Item(
        id=item_id, kind="product", family="Piston engine", category="Engines",
        name=f"{spec.name} ({out['displacement_l']:.1f} L {spec.layout} {spec.cylinders}, "
        f"{out['peak_power_kw']:.0f} kW)",
        standard="Autevra Mechanical module", status="working",
        parameters={k: v for k, v in spec.model_dump().items() if isinstance(v, int | float | str)
                    and not isinstance(v, bool)},
        properties={"mass_kg": round(out["mass_kg"], 1), "fuel": spec.fuel,
                    "aspiration": "turbocharged" if spec.turbo else "natural"},
        performance={"displacement_l": round(out["displacement_l"], 3),
                     "peak_torque_nm": round(out["peak_torque_nm"], 1),
                     "peak_torque_rpm": round(out["peak_torque_rpm"]),
                     "peak_power_kw": round(out["peak_power_kw"], 1),
                     "peak_power_rpm": round(out["peak_power_rpm"]),
                     "mean_piston_speed_ms": round(out["mean_piston_speed_ms"], 2)},
        maps={"torque_curve": curve}, ports=ports,
        definition={"name": spec.name, "color": [0.66, 0.68, 0.70], "finish": "metal",
                    "features": [f for d in geometry.parts(spec) for f in d["features"]][:200]},
        notes=["masses and performance are concept-level estimates (see the engine analysis)",
               f"balance: {', '.join(f'{k} {v:.2f}' for k, v in out['balance'].items())}"],
        provenance=provenance,
    )  # fmt: skip


@router.post("/projects/{project_id}/engine/publish", response_model=Item)
def publish(project_id: str, ws: WorkspaceDep) -> Item:
    """Release the project's engine as a new version of an inventory product item, which
    vehicles, aircraft and boats can then install by its interface."""
    spec = get_spec(project_id, ws)
    slug = re.sub(r"[^a-z0-9]+", "-", spec.name.lower()).strip("-")[:40] or "engine"
    item = engine_item(spec, f"engine-{project_id[:8]}-{slug}", f"Mechanical project {project_id}")
    try:
        return Inventory(ws.data_dir).publish(item)
    except InventoryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


# --- engine categories: electric machines and gas turbines ---------------------------

Category = Literal["piston", "electric", "turbine"]


def _cat_path(ws: Workspace, project_id: str) -> Path:
    return _spec_path(ws, project_id).with_suffix(".category")


def category(ws: Workspace, project_id: str) -> str:
    path = _cat_path(ws, project_id)
    return path.read_text().strip() if path.exists() else "piston"


@router.get("/projects/{project_id}/engine/category")
def get_category(project_id: str, ws: WorkspaceDep) -> dict[str, str]:
    _engine_project(ws, project_id)
    return {"category": category(ws, project_id)}


@router.put("/projects/{project_id}/engine/category")
def set_category(project_id: str, body: dict[str, Category], ws: WorkspaceDep) -> dict[str, str]:
    _engine_project(ws, project_id)
    _cat_path(ws, project_id).write_text(body["category"])
    return {"category": body["category"]}


@router.post("/motors/analyse")
def analyse_motor(spec: em.MotorSpec) -> dict:
    return em.analyse(spec)


@router.post("/turbines/analyse")
def analyse_turbine(spec: gt.TurbineSpec) -> dict:
    try:
        out = gt.cycle(spec)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    return {**out, "mass_kg": machines.turbine_mass(spec)}


def _other_path(ws: Workspace, project_id: str, kind: str) -> Path:
    path = Path(ws.data_dir) / kind / f"{project_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@router.get("/projects/{project_id}/motor/spec")
def get_motor(project_id: str, ws: WorkspaceDep) -> em.MotorSpec:
    _engine_project(ws, project_id)
    path = _other_path(ws, project_id, "motors")
    return em.MotorSpec.model_validate_json(path.read_text()) if path.exists() else \
        em.MotorSpec(name=ws.project(project_id).name)  # fmt: skip


@router.put("/projects/{project_id}/motor/spec")
def put_motor(project_id: str, spec: em.MotorSpec, ws: WorkspaceDep) -> em.MotorSpec:
    _engine_project(ws, project_id)
    _other_path(ws, project_id, "motors").write_text(spec.model_dump_json(indent=1))
    return spec


@router.get("/projects/{project_id}/turbine/spec")
def get_turbine(project_id: str, ws: WorkspaceDep) -> gt.TurbineSpec:
    _engine_project(ws, project_id)
    path = _other_path(ws, project_id, "turbines")
    return gt.TurbineSpec.model_validate_json(path.read_text()) if path.exists() else \
        gt.TurbineSpec(name=ws.project(project_id).name)  # fmt: skip


@router.put("/projects/{project_id}/turbine/spec")
def put_turbine(project_id: str, spec: gt.TurbineSpec, ws: WorkspaceDep) -> gt.TurbineSpec:
    _engine_project(ws, project_id)
    _other_path(ws, project_id, "turbines").write_text(spec.model_dump_json(indent=1))
    return spec


def values(ws: Workspace, project_id: str) -> dict:
    """The design values of the project's engine, whatever its category."""
    cat = category(ws, project_id)
    spec = {"electric": get_motor, "turbine": get_turbine}.get(cat, get_spec)(project_id, ws)
    return {**spec.model_dump(), "category": cat}


@router.post("/projects/{project_id}/machine", response_model=list[schemas.PartOut])
def build_machine(project_id: str, ws: WorkspaceDep) -> list[schemas.PartOut]:
    """Build the project's electric machine or gas turbine as coloured parts."""
    cat = category(ws, project_id)
    if cat == "electric":
        docs = machines.electric_parts(get_motor(project_id, ws))
    elif cat == "turbine":
        docs = machines.turbine_parts(get_turbine(project_id, ws))
    else:
        return build(project_id, get_spec(project_id, ws), ws)
    try:
        existing = {d.name.split(": ", 1)[-1]: pid for pid, d in ws._part_docs(project_id)
                    if ": " in d.name}  # fmt: skip
        out = []
        for d in docs:
            doc = PartDoc.model_validate(d)
            pid = existing.pop(doc.name.split(": ", 1)[-1], None)
            out.append(ws.update_part(project_id, pid, doc) if pid
                       else ws.create_part(project_id, doc))  # fmt: skip
        for pid in existing.values():
            ws.delete_part(project_id, pid)
        return out
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/motor/publish", response_model=Item)
def publish_motor(project_id: str, ws: WorkspaceDep) -> Item:
    """Release the project's electric machine to the inventory (category Engines), with
    its torque curve and the shaft and mount interfaces."""
    s = get_motor(project_id, ws)
    out = em.analyse(s)
    slug = re.sub(r"[^a-z0-9]+", "-", s.name.lower()).strip("-")[:40] or "motor"
    length = s.stack_length * 1.35
    item = Item(
        id=f"motor-{project_id[:8]}-{slug}", kind="product", family="Electric machine",
        category="Engines", name=f"{s.name} ({out['peak_power_kw']:.0f} kW PMSM)",
        standard="Autevra Mechanical module", status="working",
        parameters={k: v for k, v in s.model_dump().items() if isinstance(v, int | float | str)
                    and not isinstance(v, bool)} | {"rpm_max": s.max_rpm},
        properties={"mass_kg": round(out["mass_kg"], 1), "type": "PMSM",
                    "voltage": s.voltage},
        performance={"peak_power_kw": round(out["peak_power_kw"], 1),
                     "peak_torque_nm": round(out["peak_torque_nm"], 1),
                     "continuous_power_kw": round(out["continuous_power_kw"], 1),
                     "peak_efficiency": out["peak_efficiency"]},
        maps={"torque_curve": [{"rpm": p["rpm"], "torque_nm": round(p["torque_nm"], 2),
                                "power_kw": round(p["power_kw"], 3)} for p in out["curve"]]},
        ports=[Port(name="crank_output", kind="mechanical.shaft", at={"x": -length / 2},
                    attributes={"diameter": round(s.stator_diameter * 0.16, 1),
                                "speed_max": s.max_rpm,
                                "torque_max": round(out["peak_torque_nm"], 1)}),
               *[Port(name=f"mount_{i}", kind="mechanical.mount",
                      at={"y": sy * s.stator_diameter * 0.6})
                 for i, sy in enumerate((-1, 1))]],
        definition={"name": s.name, "color": [0.62, 0.64, 0.67], "finish": "metal",
                    "features": [f for d in machines.electric_parts(s) for f in d["features"]]},
        provenance=f"Mechanical project {project_id}",
    )  # fmt: skip
    try:
        return Inventory(ws.data_dir).publish(item)
    except InventoryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
