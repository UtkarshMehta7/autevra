"""Inventory API: browse the shared library (standard parts and published items), size a
standard part (bearing life, bolt preload), install an item in any module's project as a
part, publish a project's part as an item, and see where an item is used."""

import re

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from autevra import dmu, mechanisms, routing, tooling
from autevra.api import access, schemas
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import CommandError
from autevra.inventory import calc, mating
from autevra.inventory.model import Item, ItemSummary, Port, summary
from autevra.inventory.store import Inventory, InventoryError
from autevra.part import imports
from autevra.part.build import build_part, placement_matrix
from autevra.part.features import PartDoc, Placement

router = APIRouter(tags=["inventory"], dependencies=[Depends(access.guard_project)])


def _inventory(ws: Workspace) -> Inventory:
    return Inventory(ws.data_dir)


def _item(ws: Workspace, item_id: str) -> Item:
    try:
        return _inventory(ws).get(item_id)
    except InventoryError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get("/inventory", response_model=list[ItemSummary])
def browse(ws: WorkspaceDep, q: str = Query("", max_length=100),
           category: str = Query("", max_length=40),
           limit: int = Query(300, ge=1, le=1000)) -> list[ItemSummary]:  # fmt: skip
    words = q.lower().split()
    out = []
    for item in _inventory(ws).all():
        text = f"{item.name} {item.family} {item.standard} {item.id}".lower()
        if category and item.category != category:
            continue
        if all(w in text for w in words):
            out.append(summary(item))
        if len(out) >= limit:
            break
    return out


@router.get("/inventory/items/{item_id}", response_model=Item)
def get_item(item_id: str, ws: WorkspaceDep) -> Item:
    return _item(ws, item_id)


@router.get("/inventory/items/{item_id}/usage")
def usage(item_id: str, ws: WorkspaceDep) -> list[dict[str, str]]:
    _item(ws, item_id)
    return _inventory(ws).usage(item_id)


class LifeIn(BaseModel):
    load_kN: float = Field(gt=0, le=10_000)  # noqa: N815 (engineering unit in the name)
    rpm: float = Field(gt=0, le=200_000)


@router.post("/inventory/items/{item_id}/bearing-life")
def bearing_life(item_id: str, body: LifeIn, ws: WorkspaceDep) -> dict[str, float]:
    """ISO 281 basic rating life of a bearing item at an equivalent dynamic load."""
    item = _item(ws, item_id)
    c = item.performance.get("C_kN")
    if c is None:
        raise HTTPException(status_code=422, detail=f"'{item.name}' is not a rolling bearing")
    return calc.bearing_life(c, body.load_kN, body.rpm)


class MateIn(BaseModel):
    part: str  # an installed item's part in the same project
    port: str  # that item's port
    own_port: str  # the new item's port that lands on it


class InstallIn(BaseModel):
    item: str
    at: Placement = Placement()
    mate: MateIn | None = None  # snap by interface instead of placing by coordinates


def _mated(ws: Workspace, project_id: str, item: Item, m: MateIn) -> dict[str, float]:
    """Placement snapping ``item``'s port onto a port of an installed item, after the
    compatibility check (422 with the reason when the ports cannot mate)."""
    inv = _inventory(ws)
    rows = [r for r in inv.usage() if r["project"] == project_id and r["part"] == m.part]
    if not rows:
        raise HTTPException(status_code=422, detail="the target part is not an inventory item")
    target_item = inv.get(rows[-1]["item"], rows[-1]["version"])
    target = next((p for p in target_item.ports if p.name == m.port), None)
    own = next((p for p in item.ports if p.name == m.own_port), None)
    if target is None or own is None:
        raise HTTPException(status_code=422, detail="unknown port")
    ok, why = mating.compatible(own, target)
    if not ok:
        raise HTTPException(status_code=422, detail=f"cannot mate: {why}")
    doc = dict(ws._part_docs(project_id)).get(m.part)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no part '{m.part}'")
    return mating.mate(doc.at.model_dump(), target, own)


@router.post("/projects/{project_id}/inventory/install", response_model=schemas.PartOut)
def install(project_id: str, body: InstallIn, ws: WorkspaceDep) -> schemas.PartOut:
    """Install an inventory item in a project of any module, as a part linked to the item
    version (recorded in where-used)."""
    item = _item(ws, body.item)
    if not item.definition:
        raise HTTPException(status_code=422, detail=f"'{item.name}' has no geometry")
    at = body.at.model_dump()
    if body.mate is not None:
        at = _mated(ws, project_id, item, body.mate)
    doc = PartDoc.model_validate({**item.definition, "name": item.name[:80], "at": at})
    try:
        part = ws.create_part(project_id, doc)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    _inventory(ws).record(item, project_id, part.id)
    return part


@router.post("/projects/{project_id}/parts/{part_id}/publish", response_model=Item)
def publish(project_id: str, part_id: str, ws: WorkspaceDep) -> Item:
    """Release a project's part as a new version of an inventory item (steel assumed for
    the mass until materials are assigned)."""
    parts = dict(ws._part_docs(project_id))
    doc = parts.get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no part '{part_id}'")
    slug = re.sub(r"[^a-z0-9]+", "-", doc.name.lower()).strip("-")[:40] or "part"
    built = ws._part_out(project_id, part_id)  # the built part (cached), for its volume
    volume = next(reversed(built.topology.values()), {}).get("volume", 0.0) if built.topology \
        else 0.0  # fmt: skip
    item = Item(id=f"part-{project_id[:8]}-{slug}", kind="part", family="Published part",
                category="Published", name=doc.name, standard="",
                status="working", properties={"mass_kg": round(volume * calc.STEEL * 1e-9, 4),
                                              "material": "steel (assumed)"},
                definition=doc.model_dump(mode="json"),
                provenance=f"project {project_id}, part {part_id}")  # fmt: skip
    try:
        return _inventory(ws).publish(item)
    except InventoryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.get("/projects/{project_id}/inventory/installed")
def installed(project_id: str, ws: WorkspaceDep) -> list[dict]:
    """The inventory items installed in a project that still exist, with their ports (the
    targets an item can be mated to)."""
    parts = dict(ws._part_docs(project_id))
    inv = _inventory(ws)
    out = []
    for r in inv.usage():
        if r["project"] != project_id or r["part"] not in parts:
            continue
        try:
            item = inv.get(r["item"], r["version"])
        except InventoryError:
            continue
        out.append({"part": r["part"], "name": parts[r["part"]].name, "item": item.id,
                    "version": item.version,
                    "ports": [p.model_dump() for p in item.ports]})  # fmt: skip
    return out


@router.post("/projects/{project_id}/import-step", response_model=schemas.PartOut)
async def import_step(project_id: str, request: Request, ws: WorkspaceDep,
                      name: str = Query("Imported part", min_length=1, max_length=80)
                      ) -> schemas.PartOut:  # fmt: skip
    """Import a STEP file (raw body) as a part of any module's project. The file is kept in
    the import store by its SHA-256, so the part regenerates exactly."""
    try:
        sha, solids = imports.store(await request.body())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    doc = PartDoc.model_validate({"name": name, "color": [0.6, 0.62, 0.66], "finish": "metal",
                                  "features": [{"id": "imported", "name": f"STEP ({solids} "
                                                f"solid{'s' if solids > 1 else ''})",
                                                "type": "imported", "file": sha}]})  # fmt: skip
    try:
        return ws.create_part(project_id, doc)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/inventory/items/{item_id}/ports", response_model=Item)
def add_port(item_id: str, port: Port, ws: WorkspaceDep) -> Item:
    """Add an interface to a published (user) item, released as a new version: how an
    imported part gets the ports it mates and installs by."""
    item = _item(ws, item_id)
    if item.kind == "standard":
        raise HTTPException(status_code=422, detail="standard items have fixed interfaces")
    if any(p.name == port.name for p in item.ports):
        raise HTTPException(status_code=422, detail=f"'{item.name}' already has a port "
                            f"'{port.name}'")  # fmt: skip
    try:
        return _inventory(ws).publish(item.model_copy(update={"ports": [*item.ports, port]}))
    except InventoryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.get("/projects/{project_id}/clearance", response_model=list[dmu.Pair])
def clearance(project_id: str, ws: WorkspaceDep,
              required: float = Query(5.0, ge=0.0, le=1000.0)) -> list[dmu.Pair]:  # fmt: skip
    """Clearance matrix of the project's parts (digital mock-up)."""
    placed = []
    for pid, doc in ws._part_docs(project_id):
        built = build_part(doc)
        if built.shape is None:
            continue
        placed.append(dmu.Placed(id=pid, name=doc.name, shape=built.shape,
                                 matrix=placement_matrix(doc.at)))  # fmt: skip
    if len(placed) > 40:
        raise HTTPException(status_code=422, detail="the clearance matrix is limited to 40 "
                            "parts (run it on a sub-assembly)")  # fmt: skip
    return dmu.matrix(placed, required)


# --- routing -------------------------------------------------------------------------


@router.post("/routing/harness")
def route_harness(body: routing.HarnessIn) -> dict:
    return routing.harness(body)


@router.post("/routing/pipe")
def route_pipe(body: routing.PipeIn) -> dict:
    return routing.pipe(body)


@router.post("/projects/{project_id}/routes", response_model=schemas.PartOut)
def add_route(project_id: str, body: dict, ws: WorkspaceDep) -> schemas.PartOut:
    """Add a harness or pipe route to a project as a part (body: {"harness": ...} or
    {"pipe": ...})."""
    try:
        out = (routing.harness(routing.HarnessIn.model_validate(body["harness"])) if "harness"
               in body else routing.pipe(routing.PipeIn.model_validate(body["pipe"])))  # fmt: skip
        return ws.create_part(project_id, PartDoc.model_validate(out["part"]))
    except (KeyError, ValueError, CommandError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.get("/projects/{project_id}/parts/{part_id}/draft", response_model=tooling.DraftReport)
def part_draft(
    project_id: str,
    part_id: str,
    ws: WorkspaceDep,
    min_draft: float = Query(1.0, ge=0.0, le=45.0),
    pull: str = Query("z", pattern="^[+-]?[xyz]$"),
) -> tooling.DraftReport:
    """Draft analysis of a part against a pull direction (tooling check)."""
    doc = dict(ws._part_docs(project_id)).get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no part '{part_id}'")
    built = build_part(doc)
    if built.shape is None:
        raise HTTPException(status_code=422, detail="the part does not build")
    sign = -1.0 if pull.startswith("-") else 1.0
    axis = {"x": (sign, 0.0, 0.0), "y": (0.0, sign, 0.0), "z": (0.0, 0.0, sign)}[pull[-1]]
    return tooling.draft(built.shape, axis, min_draft)


@router.get("/projects/{project_id}/parts/{part_id}/parting",
            response_model=tooling.PartingReport)  # fmt: skip
def part_parting(
    project_id: str,
    part_id: str,
    ws: WorkspaceDep,
    pull: str = Query("z", pattern="^[+-]?[xyz]$"),
    pressure: float = Query(40.0, ge=1.0, le=300.0),
) -> tooling.PartingReport:
    """Parting line, undercuts and clamp force of a part in a straight-pull tool."""
    doc = dict(ws._part_docs(project_id)).get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no part '{part_id}'")
    built = build_part(doc)
    if built.shape is None:
        raise HTTPException(status_code=422, detail="the part does not build")
    sign = -1.0 if pull.startswith("-") else 1.0
    axis = {"x": (sign, 0.0, 0.0), "y": (0.0, sign, 0.0), "z": (0.0, 0.0, sign)}[pull[-1]]
    return tooling.parting(built.shape, axis, pressure)


# --- mechanisms ----------------------------------------------------------------------


@router.post("/mechanisms/fourbar")
def mechanism_fourbar(body: mechanisms.FourBar) -> dict:
    return mechanisms.fourbar(body)


@router.post("/mechanisms/slider-crank")
def mechanism_slider_crank(body: mechanisms.SliderCrank) -> dict:
    try:
        return mechanisms.slider_crank(body)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


class SweepIn(BaseModel):
    joint: mechanisms.Joint
    required: float = Field(5.0, ge=0.0, le=1000.0)
    volume: bool = False


def _placed(ws: Workspace, project_id: str) -> list[dmu.Placed]:
    placed = []
    for pid, doc in ws._part_docs(project_id):
        built = build_part(doc)
        if built.shape is not None:
            placed.append(dmu.Placed(id=pid, name=doc.name, shape=built.shape,
                                     matrix=placement_matrix(doc.at)))  # fmt: skip
    return placed


def _moving(ws: Workspace, project_id: str, part_id: str) -> tuple[dmu.Placed, list[dmu.Placed]]:
    placed = _placed(ws, project_id)
    moving = next((p for p in placed if p.id == part_id), None)
    if moving is None:
        raise HTTPException(status_code=404, detail=f"no built part '{part_id}'")
    return moving, [p for p in placed if p.id != part_id]


@router.post("/projects/{project_id}/parts/{part_id}/sweep",
             response_model=mechanisms.SweepReport)  # fmt: skip
def part_sweep(project_id: str, part_id: str, body: SweepIn,
               ws: WorkspaceDep) -> mechanisms.SweepReport:  # fmt: skip
    """Move a part through a joint's range and report its closest approach to every other
    part of the project (sampled positions)."""
    moving, others = _moving(ws, project_id, part_id)
    if len(others) > 40:
        raise HTTPException(status_code=422, detail="the swept check is limited to 40 other "
                            "parts (run it on a sub-assembly)")  # fmt: skip
    try:
        return mechanisms.sweep(moving, others, body.joint, body.required, body.volume)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/parts/{part_id}/envelope", response_model=schemas.PartOut)
def part_envelope(project_id: str, part_id: str, joint: mechanisms.Joint,
                  ws: WorkspaceDep) -> schemas.PartOut:  # fmt: skip
    """Add the swept envelope of a part (union of its sampled poses) to the project as a
    part, kept in the import store so it regenerates exactly."""
    import tempfile
    from pathlib import Path

    import cadquery as cq

    moving, _ = _moving(ws, project_id, part_id)
    try:
        solid = mechanisms.envelope(moving, joint)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "envelope.step"
            cq.exporters.export(solid, str(target))
            sha, _n = imports.store(target.read_bytes())
        unit = "deg" if joint.kind == "revolute" else "mm"
        doc = PartDoc.model_validate({
            "name": f"Envelope of {moving.name}"[:80], "color": [0.95, 0.55, 0.2],
            "finish": "glass",
            "features": [{"id": "imported", "type": "imported", "file": sha,
                          "name": f"Swept {joint.lo:g} to {joint.hi:g} {unit}, "
                                  f"{joint.steps} poses"}]})  # fmt: skip
        return ws.create_part(project_id, doc)
    except (ValueError, CommandError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
