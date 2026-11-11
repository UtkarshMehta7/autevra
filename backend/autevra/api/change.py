"""Reviews, baselines and engineering change (every module).

- Review gates are computed from the model, never prepared by hand: each gate is a list of
  criteria evaluated on the breakdown, the trace, the loads, the compliance matrix and the
  manufacturing plan (architecture, section 11).
- A baseline is a named, frozen snapshot of the design values and their headline results,
  taken at a gate; the current design can be compared with any baseline.
- An engineering change request (ECR) proposes value changes; its impact on mass, CG,
  checks, compliance and unit cost is computed on a copy before anyone approves it. The
  change order (ECO) applies the approved changes through the design's own path (the
  command history for land vehicles, the saved specification for aircraft and engines).
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from autevra import manufacturing, modules
from autevra.api import access
from autevra.api.product import _architecture, _module, _requirements, root_node
from autevra.api.routes import WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import Change, CommandError, Operation, SetParameters, Source
from autevra.product.breakdown import rollup
from autevra.product.systems import trace

router = APIRouter(tags=["change"], dependencies=[Depends(access.guard_project)])
GATES = ("Concept review", "Preliminary review", "Critical review", "Verification", "Release")


def _folder(ws: Workspace, project_id: str, kind: str) -> Path:
    path = Path(ws.data_dir) / kind / project_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def snapshot(ws: Workspace, project_id: str, values: dict[str, Any] | None = None) -> dict:
    """Headline results of the design (or of ``values`` in its place)."""
    module, own = _module(ws, project_id)
    vals = own if values is None else {**own, **values}
    config = module.options(vals).resolve(module.current(vals))
    root = root_node(module, vals, config)
    rolled = rollup(root)
    configured = module.configure(vals, config)
    checks = {c.id: c.status for c in module.checks(configured, rolled)}
    compliance = {c.clause: c.status for c in module.compliance(configured)} \
        if module.compliance else {}  # fmt: skip
    order = list(module.station_order)
    plan = manufacturing.plan(root, dict(module.stations), order, 60.0)
    return {"values": {k: v for k, v in vals.items() if isinstance(v, int | float | str | bool)},
            "mass_kg": round(rolled.rollup.mass, 2),
            "cg": [round(x, 4) for x in rolled.rollup.cg], "parts": rolled.rollup.parts,
            "maturity": rolled.rollup.maturity, "checks": checks, "compliance": compliance,
            "unit_cost_eur": plan.total_cost_eur, "co2_kg": plan.total_co2_kg,
            "configuration": config}  # fmt: skip


def compare(before: dict, after: dict) -> dict:
    changed = {k: [before["values"].get(k), v] for k, v in after["values"].items()
               if before["values"].get(k) != v}  # fmt: skip
    status = lambda a, b: {k: [a.get(k), v] for k, v in b.items() if a.get(k) != v}  # noqa: E731
    return {"values": changed,
            "mass_kg": round(after["mass_kg"] - before["mass_kg"], 2),
            "cg_x_m": round(after["cg"][0] - before["cg"][0], 4),
            "unit_cost_eur": round(after["unit_cost_eur"] - before["unit_cost_eur"], 2),
            "co2_kg": round(after["co2_kg"] - before["co2_kg"], 1),
            "checks": status(before["checks"], after["checks"]),
            "compliance": status(before["compliance"], after["compliance"])}  # fmt: skip


# --- review gates ----------------------------------------------------------------------


@router.get("/projects/{project_id}/reviews")
def reviews(project_id: str, ws: WorkspaceDep) -> list[dict]:
    """Every gate with its criteria evaluated on the current design."""
    module, values = _module(ws, project_id)
    config = module.options(values).resolve(module.current(values))
    root = root_node(module, values, config)
    rolled = rollup(root)
    parts = [n for n in root.walk() if n.kind == "part"]
    issues = []
    if module.architecture is not None:
        arch = _architecture(module, values, config, {})
        issues = trace(arch, root, [r["key"] for r in _requirements(ws, project_id)])
        unmitigated = [m for m in arch.failure_modes if m.priority == "high" and not m.action]
    else:
        unmitigated = []
    fails = [i for i in issues if i.severity == "fail"]
    configured = module.configure(values, config)
    compliance = module.compliance(configured) if module.compliance else []
    plan = manufacturing.plan(root, dict(module.stations), list(module.station_order), 60.0)
    baselines = _baselines(ws, project_id)
    at_least = lambda level: sum(p.maturity >= level for p in parts)  # noqa: E731
    critical = sorted(parts, key=lambda p: p.mass, reverse=True)[: max(1, len(parts) // 5)]

    def crit(text: str, ok: bool, detail: str) -> dict:
        return {"criterion": text, "met": ok, "detail": detail}

    gates = [
        [crit("every part allocated in the breakdown", len(parts) > 0,
              f"{len(parts)} part types at level 0 or above"),
         crit("every function performed by a block", not any(
             i.kind == "unallocated_function" for i in fails), f"{len(fails)} trace failures"),
         crit("within the mass budget", not rolled.rollup.over_budget,
              "over budget: " + ", ".join(rolled.rollup.over_budget) if
              rolled.rollup.over_budget else f"{rolled.rollup.mass:.0f} kg")],
        [crit("the heaviest fifth of the parts engineered (L2)",
              all(p.maturity >= 2 for p in critical),
              f"{sum(p.maturity >= 2 for p in critical)} of {len(critical)} critical parts at L2"),
         crit("load cases computed", module.loads is not None and bool(module.loads(configured)),
              "module load cases"),
         crit("interfaces between blocks defined", module.architecture is not None,
              "interface rows generated from the flows"),
         crit("a baseline taken", bool(baselines), f"{len(baselines)} baselines")],
        [crit("every part manufacturable (L3)", at_least(3) == len(parts),
              f"{at_least(3)} of {len(parts)} parts at L3"),
         crit("MBOM reconciled with the design", not plan.reconciliation,
              "; ".join(plan.reconciliation) or "every part used exactly once"),
         crit("high-priority failure modes have actions", not unmitigated,
              f"{len(unmitigated)} without an action")],
        [crit("every compliance row shown", all(c.status == "shown" for c in compliance),
              f"{sum(c.status == 'shown' for c in compliance)} of {len(compliance)} shown"),
         crit("no failing design check", all(c.status != "fail" for c in
                                             module.checks(configured, rolled)),
              "breakdown checks against the product model")],
        [crit("every part released (L4)", at_least(4) == len(parts),
              f"{at_least(4)} of {len(parts)} parts released")],
    ]  # fmt: skip
    return [{"gate": g, "criteria": c, "passed": all(x["met"] for x in c)}
            for g, c in zip(GATES, gates, strict=True)]  # fmt: skip


# --- baselines -------------------------------------------------------------------------


class BaselineIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    gate: Literal["Concept review", "Preliminary review", "Critical review", "Verification",
                  "Release", "none"] = "none"  # fmt: skip


def _baselines(ws: Workspace, project_id: str) -> list[dict]:
    folder = _folder(ws, project_id, "baselines")
    return [json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))]


@router.get("/projects/{project_id}/baselines")
def list_baselines(project_id: str, ws: WorkspaceDep) -> list[dict]:
    return [{k: b[k] for k in ("id", "name", "gate", "created_at", "mass_kg")}
            for b in _baselines(ws, project_id)]  # fmt: skip


@router.post("/projects/{project_id}/baselines", status_code=201)
def take_baseline(project_id: str, body: BaselineIn, ws: WorkspaceDep) -> dict:
    existing = _baselines(ws, project_id)
    bid = f"BL-{len(existing) + 1:03d}"
    record = {"id": bid, "name": body.name, "gate": body.gate,
              "created_at": datetime.now(UTC).isoformat(), **snapshot(ws, project_id)}  # fmt: skip
    (_folder(ws, project_id, "baselines") / f"{bid}.json").write_text(json.dumps(record))
    return record


@router.get("/projects/{project_id}/baselines/{baseline_id}/compare")
def compare_baseline(project_id: str, baseline_id: str, ws: WorkspaceDep) -> dict:
    found = next((b for b in _baselines(ws, project_id) if b["id"] == baseline_id), None)
    if found is None:
        raise HTTPException(status_code=404, detail=f"no baseline '{baseline_id}'")
    return {"baseline": baseline_id, **compare(found, snapshot(ws, project_id))}


# --- engineering change ----------------------------------------------------------------


class ChangeRequestIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    reason: str = Field("", max_length=1000)
    changes: dict[str, float | bool | str] = Field(min_length=1)


def _requests(ws: Workspace, project_id: str) -> list[dict]:
    folder = _folder(ws, project_id, "changes")
    return [json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))]


def _save(ws: Workspace, project_id: str, record: dict) -> None:
    (_folder(ws, project_id, "changes") / f"{record['id']}.json").write_text(json.dumps(record))


@router.get("/projects/{project_id}/changes")
def list_changes(project_id: str, ws: WorkspaceDep) -> list[dict]:
    return _requests(ws, project_id)


@router.post("/projects/{project_id}/changes", status_code=201)
def request_change(project_id: str, body: ChangeRequestIn, ws: WorkspaceDep) -> dict:
    """Raise an ECR: its impact is computed on a copy of the design before any decision."""
    _, values = _module(ws, project_id)
    unknown = [k for k in body.changes if k not in values]
    if unknown:
        raise HTTPException(status_code=422, detail=f"unknown design values: {unknown}")
    try:
        impact = compare(snapshot(ws, project_id), snapshot(ws, project_id, body.changes))
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=f"the change is not valid: {exc}") from None
    record = {"id": f"ECR-{len(_requests(ws, project_id)) + 1:03d}", "title": body.title,
              "reason": body.reason, "changes": body.changes, "status": "open",
              "created_at": datetime.now(UTC).isoformat(), "impact": impact}  # fmt: skip
    _save(ws, project_id, record)
    return record


@router.post("/projects/{project_id}/changes/{change_id}/{decision}")
def decide(project_id: str, change_id: str, decision: Literal["approve", "reject"],
           ws: WorkspaceDep) -> dict:  # fmt: skip
    """Approve (the ECO applies the changes through the design's own path) or reject."""
    record = next((r for r in _requests(ws, project_id) if r["id"] == change_id), None)
    if record is None:
        raise HTTPException(status_code=404, detail=f"no change '{change_id}'")
    if record["status"] != "open":
        raise HTTPException(status_code=409, detail=f"{change_id} is already {record['status']}")
    if decision == "approve":
        _apply(ws, project_id, record)
        record["status"] = "approved"
        record["eco"] = change_id.replace("ECR", "ECO")
    else:
        record["status"] = "rejected"
    record["decided_at"] = datetime.now(UTC).isoformat()
    _save(ws, project_id, record)
    return record


def _apply(ws: Workspace, project_id: str, record: dict) -> None:
    module = modules.for_domain(ws.project(project_id).domain)
    assert module is not None
    if module.id == "land":
        changes = tuple(Change(parameter=k, operation=Operation.SET, value=float(v))
                        for k, v in record["changes"].items())  # fmt: skip
        try:
            ws.apply(project_id, SetParameters(changes=changes, source=Source.API,
                                               instruction=f"{record['id'].replace('ECR', 'ECO')}"
                                               f": {record['title']}"))  # fmt: skip
        except (CommandError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from None
        return
    if module.id == "aircraft":
        from autevra.api.aerospace import get_spec, put_spec

        spec = get_spec(project_id, ws)
        put_spec(project_id, spec.model_validate({**spec.model_dump(), **record["changes"]}), ws)
        return
    from autevra.api.mechanical import get_spec as engine_spec
    from autevra.api.mechanical import put_spec as put_engine

    spec = engine_spec(project_id, ws)
    put_engine(project_id, spec.model_validate({**spec.model_dump(), **record["changes"]}), ws)
