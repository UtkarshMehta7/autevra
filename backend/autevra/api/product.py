"""Product structure API: the project's breakdown for one configuration, with roll-ups,
maturity and the checks against the product model; the option families and rules; and
the mass envelope across every valid configuration.

The module comes from the project's domain, so a project only ever sees its own module's
options, templates and breakdown."""

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from autevra import manufacturing, materials, modules, quality
from autevra.api import access
from autevra.api.aerospace import get_spec
from autevra.api.installs import engine_values
from autevra.api.mechanical import get_spec as engine_spec
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.product import templates
from autevra.product.breakdown import LEVELS, RolledNode, check_ids, configure, rollup
from autevra.product.options import ApplicabilityError, OptionFamily, OptionRule
from autevra.product.systems import (
    Architecture,
    Block,
    ChainStep,
    Flow,
    Function,
    IcdRow,
    TraceIssue,
    chain,
    icd,
    trace,
)

router = APIRouter(tags=["product"], dependencies=[Depends(access.guard_project)])


class ProductOut(BaseModel):
    module: str
    module_name: str
    frame: str
    levels: list[str]
    families: list[OptionFamily]
    rules: list[OptionRule]
    design_configuration: dict[str, str]  # the design's own choices
    configuration: dict[str, str]  # the configuration shown
    violations: list[str]
    breakdown: RolledNode
    checks: list[modules.Check]
    templates: int


class Envelope(BaseModel):
    configurations: int
    mass_min: float
    mass_max: float
    lightest: dict[str, str]
    heaviest: dict[str, str]
    cg_x_min: float
    cg_x_max: float


def _module(ws: Workspace, project_id: str) -> tuple[modules.ModuleDef, dict[str, Any]]:
    domain = ws.project(project_id).domain
    module = modules.for_domain(domain)
    if module is None:
        raise HTTPException(status_code=422, detail=f"no product structure for '{domain}'")
    if module.id == "aircraft":
        values: dict[str, Any] = get_spec(project_id, ws).model_dump()
    elif module.id == "mechanical":
        values = engine_spec(project_id, ws).model_dump()
    else:
        values = dict(ws.project(project_id).values)
    if module.id in ("land", "aircraft"):
        values.update(engine_values(ws, project_id))  # an engine installed from the inventory
    return module, values


def _rolled(module: modules.ModuleDef, values: dict[str, Any],
            config: dict[str, str]) -> tuple[RolledNode, dict[str, Any]]:  # fmt: skip
    opts = module.options(values)
    vals = module.configure(values, config)
    full = module.breakdown(vals)
    check_ids(full)
    shown = configure(full, config, opts.names())
    assert shown is not None
    return rollup(shown), vals


def _chosen(module: modules.ModuleDef, values: dict[str, Any], config: str) -> dict[str, str]:
    """The configuration to show: the design's own, with ``config`` (JSON) on top."""
    opts = module.options(values)
    try:
        override = json.loads(config) if config else {}
        if not isinstance(override, dict):
            raise ValueError("config must be a JSON object")
        return opts.resolve({**module.current(values), **override})
    except (ValueError, ApplicabilityError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.get("/projects/{project_id}/product", response_model=ProductOut)
def product(project_id: str, ws: WorkspaceDep,
            config: str = Query("", max_length=2000)) -> ProductOut:  # fmt: skip
    """The breakdown in the design's own configuration, or with ``config`` (a JSON object of
    option choices) applied on top of it."""
    module, values = _module(ws, project_id)
    opts = module.options(values)
    own = module.current(values)
    chosen = _chosen(module, values, config)
    root, vals = _rolled(module, values, chosen)
    return ProductOut(
        module=module.id, module_name=module.name, frame=module.frame, levels=list(LEVELS),
        families=opts.families, rules=opts.rules, design_configuration=own,
        configuration=chosen, violations=opts.violations(chosen), breakdown=root,
        checks=module.checks(vals, root), templates=len(templates.of(module.id)),
    )  # fmt: skip


@router.get("/projects/{project_id}/product/envelope", response_model=Envelope)
def envelope(project_id: str, ws: WorkspaceDep) -> Envelope:
    """Mass and longitudinal CG over every valid configuration (options that change mass;
    the others held at the design's choice)."""
    module, values = _module(ws, project_id)
    opts = module.options(values)
    own = module.current(values)
    rows: list[tuple[float, float, dict[str, str]]] = []
    fixed = {f.id: own[f.id] for f in opts.families if not f.affects_mass and f.id in own}
    for config in opts.enumerate(only_mass=True):
        config = opts.resolve({**config, **fixed})
        root, _ = _rolled(module, values, config)
        rows.append((root.rollup.mass, root.rollup.cg[0], config))
    if not rows:
        raise HTTPException(status_code=422, detail="no valid configuration")
    light, heavy = min(rows, key=lambda r: r[0]), max(rows, key=lambda r: r[0])
    return Envelope(configurations=len(rows), mass_min=light[0], mass_max=heavy[0],
                    lightest=light[2], heaviest=heavy[2],
                    cg_x_min=min(r[1] for r in rows), cg_x_max=max(r[1] for r in rows))  # fmt: skip


# --- systems layer: functions, logical blocks, flows, interfaces, FMEA, trace -----------


class FailureRow(BaseModel):
    id: str
    function: str
    block: str
    mode: str
    effect: str
    severity: int
    occurrence: int
    detection: int
    rpn: int
    priority: str
    action: str


class SystemsOut(BaseModel):
    module: str
    configuration: dict[str, str]
    functions: list[Function]
    blocks: list[Block]
    flows: list[Flow]
    icd: list[IcdRow]
    failure_modes: list[FailureRow]
    issues: list[TraceIssue]
    requirements: list[dict[str, str]]  # {key, text, function}
    allocations: dict[str, str]  # requirement key -> function id


def _allocations_path(ws: Workspace, project_id: str) -> Path:
    path = Path(ws.data_dir) / "allocations" / f"{project_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _allocations(ws: Workspace, project_id: str) -> dict[str, str]:
    path = _allocations_path(ws, project_id)
    return json.loads(path.read_text()) if path.exists() else {}


def _architecture(module: modules.ModuleDef, values: dict[str, Any], config: dict[str, str],
                  allocations: dict[str, str]) -> Architecture:  # fmt: skip
    if module.architecture is None:
        raise HTTPException(status_code=422, detail=f"no architecture for '{module.name}'")
    arch = module.architecture(values).configured(config, module.options(values).names())
    by_function: dict[str, list[str]] = {}
    for req, fid in allocations.items():
        by_function.setdefault(fid, []).append(req)
    functions = [f.model_copy(update={"requirements": [*f.requirements,
                                                      *by_function.get(f.id, [])]})
                 for f in arch.functions]  # fmt: skip
    return arch.model_copy(update={"functions": functions})


def _requirements(ws: Workspace, project_id: str) -> list[dict[str, str]]:
    rows = ws.requirements(project_id)
    return [{"key": r.requirement.key, "text": r.requirement.text} for r in rows]


@router.get("/projects/{project_id}/systems", response_model=SystemsOut)
def systems(project_id: str, ws: WorkspaceDep,
            config: str = Query("", max_length=2000)) -> SystemsOut:  # fmt: skip
    """The product's functions, logical blocks and typed flows in one configuration, its
    interface rows and design FMEA, and the allocation gaps between the layers."""
    module, values = _module(ws, project_id)
    chosen = _chosen(module, values, config)
    allocations = _allocations(ws, project_id)
    arch = _architecture(module, values, chosen, allocations)
    reqs = _requirements(ws, project_id)
    for r in reqs:
        r["function"] = allocations.get(r["key"], "")
    issues = trace(arch, root_node(module, values, chosen), [r["key"] for r in reqs])
    return SystemsOut(
        module=module.id, configuration=chosen, functions=arch.functions, blocks=arch.blocks,
        flows=arch.flows, icd=icd(arch),
        failure_modes=[FailureRow(**m.model_dump(), rpn=m.rpn, priority=m.priority)
                       for m in arch.failure_modes],
        issues=issues, requirements=reqs, allocations=allocations,
    )  # fmt: skip


def root_node(module: modules.ModuleDef, values: dict[str, Any], config: dict[str, str]):  # type: ignore[no-untyped-def]
    """The configured (not rolled-up) breakdown."""
    opts = module.options(values)
    shown = configure(module.breakdown(module.configure(values, config)), config, opts.names())
    assert shown is not None
    return shown


@router.get("/projects/{project_id}/systems/chain/{function_id}", response_model=list[ChainStep])
def function_chain(project_id: str, function_id: str, ws: WorkspaceDep,
                   config: str = Query("", max_length=2000)) -> list[ChainStep]:  # fmt: skip
    """The blocks performing a function, ordered along their flows, with their parts."""
    module, values = _module(ws, project_id)
    chosen = _chosen(module, values, config)
    arch = _architecture(module, values, chosen, {})
    if function_id not in {f.id for f in arch.functions}:
        raise HTTPException(status_code=404, detail=f"no function '{function_id}'")
    return chain(arch, function_id, root_node(module, values, chosen))


class AllocationIn(BaseModel):
    requirement: str
    function: str  # "" removes the allocation


@router.put("/projects/{project_id}/systems/allocations", response_model=dict[str, str])
def allocate(project_id: str, body: AllocationIn, ws: WorkspaceDep) -> dict[str, str]:
    """Allocate a requirement of the project to a function (traced in the systems view)."""
    module, values = _module(ws, project_id)
    keys = {r["key"] for r in _requirements(ws, project_id)}
    if body.requirement not in keys:
        raise HTTPException(status_code=404, detail=f"no requirement '{body.requirement}'")
    if module.architecture is None:
        raise HTTPException(status_code=422, detail=f"no architecture for '{module.name}'")
    fids = {f.id for f in module.architecture(values).functions}
    if body.function and body.function not in fids:
        raise HTTPException(status_code=422, detail=f"no function '{body.function}'")
    allocations = _allocations(ws, project_id)
    if body.function:
        allocations[body.requirement] = body.function
    else:
        allocations.pop(body.requirement, None)
    _allocations_path(ws, project_id).write_text(json.dumps(allocations, indent=1))
    return allocations


# --- loads, regulations and materials ------------------------------------------------


@router.get("/materials")
def list_materials() -> list[materials.Material]:
    """The materials database: minimum (standard) or typical values, with their source."""
    return list(materials.MATERIALS.values())


@router.get("/projects/{project_id}/loads")
def project_loads(project_id: str, ws: WorkspaceDep) -> dict:
    """The module's load cases for the design, its compliance rows (clause references with
    our own wording) and, for aircraft, the V-n envelope."""
    module, values = _module(ws, project_id)
    if module.loads is None:
        raise HTTPException(status_code=422, detail=f"no load cases for '{module.name}'")
    out: dict = {"module": module.id, "cases": [c.model_dump() for c in module.loads(values)],
                 "compliance": [c.model_dump() for c in module.compliance(values)]
                 if module.compliance else []}  # fmt: skip
    if module.id == "aircraft":
        from autevra.modules.aircraft.loads import envelope

        out["envelope"] = envelope(values)
    return out


# --- manufacturing and quality -------------------------------------------------------


TAKT = {"land": 60.0, "mechanical": 90.0, "aircraft": 4 * 3600.0}  # s, typical rates


@router.get("/projects/{project_id}/manufacturing")
def manufacturing_plan(project_id: str, ws: WorkspaceDep,
                       takt: float | None = Query(None, ge=5, le=86_400),
                       config: str = Query("", max_length=2000)) -> dict:  # fmt: skip
    """The MBOM by station with a process plan, line balance at the takt time, cost and CO2,
    the reconciliation against the design breakdown, and the design's tolerance stack-ups."""
    module, values = _module(ws, project_id)
    chosen = _chosen(module, values, config)
    root = root_node(module, values, chosen)
    order = list(module.station_order)
    final = next((st for st in order if st.startswith("Final")), order[-1] if order else
                 "Final assembly")  # fmt: skip
    plan = manufacturing.plan(root, dict(module.stations), order,
                              takt or TAKT.get(module.id, 60.0), final)  # fmt: skip
    stacks = module.stackups(module.configure(values, chosen)) if module.stackups else []
    return {"module": module.id, "plan": plan.model_dump(),
            "stackups": [{"stack": s.model_dump(), "result": quality.analyse(s)}
                         for s in stacks]}  # fmt: skip


@router.post("/quality/stackup")
def stackup(stack: quality.Stack) -> dict:
    return quality.analyse(stack)
