"""Machining API: plan 2.5-axis milling and drilling of a project's part from a stock
block, with toolpaths for the 3D preview and the G-code program."""

import math

from fastapi import APIRouter, Depends, HTTPException

from autevra.api import access
from autevra.api.routes import WorkspaceDep
from autevra.cam import gcode, milling

router = APIRouter(tags=["machining"], dependencies=[Depends(access.guard_project)])


def _decimate(pts: list[tuple[float, float, float]], limit: int) -> list[list[float]]:
    step = max(1, math.ceil(len(pts) / limit))
    keep = pts[::step]
    if keep[-1] != pts[-1]:
        keep.append(pts[-1])
    return [[round(c, 3) for c in p] for p in keep]


@router.post("/projects/{project_id}/parts/{part_id}/cam")
def machine_part(project_id: str, part_id: str, body: milling.CamIn, ws: WorkspaceDep) -> dict:
    doc = dict(ws._part_docs(project_id)).get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"no part '{part_id}'")
    try:
        plan = milling.plan(doc, body)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    ops = plan["operations"]
    program = gcode.post(ops, plan["setup"], title=doc.name)
    out_ops = []
    for op in ops:
        cut, rapid = op.lengths()
        out_ops.append(
            {
                "name": op.name,
                "tool": op.tool.number,
                "tool_label": op.tool.label,
                "rpm": op.speeds.rpm,
                "feed": op.speeds.feed,
                "ap": op.speeds.ap,
                "ae": op.speeds.ae,
                "cut_mm": cut,
                "rapid_mm": rapid,
                "time_s": op.time_s(),
                "power_kw": op.power_kw,
                "cycle": op.cycle["code"] if op.cycle else None,
                "notes": op.notes,
                "paths": [
                    _decimate(m.pts, 400) for m in op.moves if m.kind != "rapid" and len(m.pts) > 1
                ],
            }
        )
    s = plan["setup"]
    return {
        "stock": s.stock,
        "part_box": s.part_box,
        "safe_z": s.safe_z,
        "material": plan["material"],
        "tools": [
            {"number": t.number, "label": t.label, "kind": t.kind, "diameter": t.diameter}
            for t in plan["tools"]
        ],
        "operations": out_ops,
        "warnings": plan["warnings"],
        "notes": plan["notes"],
        "levels": plan["levels"],
        "time_s": plan["time_s"],
        "stock_volume": plan["stock_volume"],
        "removed_volume": plan["removed_volume"],
        "rest_area": plan["rest_area"],
        "mass_kg": plan["mass_kg"],
        "stock_mass_kg": plan["stock_mass_kg"],
        "gcode": program,
        "gcode_lines": program.count("\n"),
    }
