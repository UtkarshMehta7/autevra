"""Product structure API: the project's breakdown for one configuration, with roll-ups,
maturity and the checks against the product model; the option families and rules; and
the mass envelope across every valid configuration.

The module comes from the project's domain, so a project only ever sees its own module's
options, templates and breakdown."""

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from autevra import modules
from autevra.api import access
from autevra.api.aerospace import get_spec
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.product import templates
from autevra.product.breakdown import LEVELS, RolledNode, check_ids, configure, rollup
from autevra.product.options import ApplicabilityError, OptionFamily, OptionRule

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
    else:
        values = dict(ws.project(project_id).values)
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


@router.get("/projects/{project_id}/product", response_model=ProductOut)
def product(project_id: str, ws: WorkspaceDep,
            config: str = Query("", max_length=2000)) -> ProductOut:  # fmt: skip
    """The breakdown in the design's own configuration, or with ``config`` (a JSON object of
    option choices) applied on top of it."""
    module, values = _module(ws, project_id)
    opts = module.options(values)
    own = module.current(values)
    try:
        override = json.loads(config) if config else {}
        if not isinstance(override, dict):
            raise ValueError("config must be a JSON object")
        chosen = opts.resolve({**own, **override})
    except (ValueError, ApplicabilityError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
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
