"""Design library and project packages, the same for every module.

A project package is one JSON snapshot of a design (parameters, the user's parts, the
module design files, styling, specification, requirements). The library keeps packages
of the user's own designs as reusable starting points; a design is used by restoring its
package into a new project. Packages also move designs between installations (export,
import)."""

import datetime as dt
import json
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field

from autevra.api import access, schemas
from autevra.api.routes import VisitorDep, WorkspaceDep
from autevra.api.service import Workspace
from autevra.core.commands import CommandError

router = APIRouter(tags=["library"], dependencies=[Depends(access.guard_project)])


class SaveIn(BaseModel):
    project_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=120)
    description: str = Field("", max_length=2000)
    tags: list[str] = Field(default_factory=list, max_length=20)


class Entry(BaseModel):
    id: str
    name: str
    description: str
    domain: str
    tags: list[str]
    created: str
    parts: int
    source: str  # the project it was saved from


def _folder(ws: Workspace):  # noqa: ANN202
    folder = ws.data_dir / "library"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _load(ws: Workspace, entry_id: str) -> dict:
    if not entry_id.isalnum():
        raise HTTPException(status_code=404, detail="no such design")
    path = _folder(ws) / f"{entry_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="no such design")
    return json.loads(path.read_text())


@router.get("/projects/{project_id}/snapshot")
def export_package(project_id: str, ws: WorkspaceDep) -> Response:
    """The project as a package (JSON) to keep, share or import elsewhere."""
    package = ws.snapshot(project_id)
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in package["name"]).strip("-")
    return Response(
        json.dumps(package, indent=1),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{safe or "design"}.autevra.json"'},
    )


@router.post("/projects/import", response_model=schemas.ProjectState, status_code=201)
def import_package(
    package: dict, ws: WorkspaceDep, who: VisitorDep, request: Request
) -> schemas.ProjectState:
    access.check_project_quota(request, who)
    try:
        return ws.restore(package, owner=who.owner)
    except (CommandError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=f"cannot import: {exc}") from None


@router.get("/library", response_model=list[Entry])
def list_library(ws: WorkspaceDep, domain: str = "") -> list[Entry]:
    out = []
    for path in sorted(_folder(ws).glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        data = json.loads(path.read_text())
        if domain and data["domain"] != domain:
            continue
        out.append(Entry(**{k: data[k] for k in Entry.model_fields}))
    return out


@router.post("/library", response_model=Entry, status_code=201)
def save_to_library(body: SaveIn, ws: WorkspaceDep) -> Entry:
    """Save a project's current design to the library (a snapshot: later edits of the
    project do not change it)."""
    package = ws.snapshot(body.project_id)
    package["source_id"] = body.project_id
    entry = {
        "id": uuid4().hex[:12],
        "name": body.name,
        "description": body.description,
        "domain": package["domain"],
        "tags": body.tags,
        "created": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "parts": len(package["parts"]),
        "source": body.project_id,
        "package": package,
    }
    (_folder(ws) / f"{entry['id']}.json").write_text(json.dumps(entry))
    return Entry(**{k: entry[k] for k in Entry.model_fields})


@router.post("/library/{entry_id}/use", response_model=schemas.ProjectState, status_code=201)
def use_design(
    entry_id: str, ws: WorkspaceDep, who: VisitorDep, request: Request
) -> schemas.ProjectState:
    """A new project from a library design."""
    access.check_project_quota(request, who)
    data = _load(ws, entry_id)
    try:
        return ws.restore(data["package"], name=data["name"], owner=who.owner)
    except (CommandError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.delete("/library/{entry_id}", status_code=204)
def delete_design(entry_id: str, ws: WorkspaceDep) -> None:
    _load(ws, entry_id)
    (_folder(ws) / f"{entry_id}.json").unlink()
