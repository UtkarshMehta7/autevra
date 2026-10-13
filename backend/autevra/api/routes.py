"""HTTP routes. Thin: validation by Pydantic, logic in ``Workspace``."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse

from autevra.api import schemas
from autevra.api.service import ProposalNotFoundError, Workspace, _derived
from autevra.domain import parameters
from autevra.domain.commands import CommandError
from autevra.domain.design import CommandRejectedError
from autevra.storage.repository import ProjectNotFoundError

router = APIRouter(prefix="/api")


def workspace(request: Request) -> Workspace:
    return request.app.state.workspace


WorkspaceDep = Annotated[Workspace, Depends(workspace)]


@router.get("/parameters", response_model=schemas.Catalogue)
def catalogue() -> schemas.Catalogue:
    return schemas.Catalogue(
        parameters=list(parameters.REGISTRY.values()), derived=_derived(parameters.default_values())
    )


@router.get("/projects", response_model=list[schemas.ProjectSummary])
def list_projects(ws: WorkspaceDep) -> list[schemas.ProjectSummary]:
    return ws.list_projects()


@router.post("/projects", response_model=schemas.ProjectState, status_code=201)
def create_project(body: schemas.ProjectCreate, ws: WorkspaceDep) -> schemas.ProjectState:
    return ws.create_project(body.name)


@router.get("/projects/{project_id}", response_model=schemas.ProjectState)
def get_project(project_id: str, ws: WorkspaceDep) -> schemas.ProjectState:
    return ws.project(project_id)


@router.patch("/projects/{project_id}", response_model=schemas.ProjectState)
def rename_project(
    project_id: str, body: schemas.ProjectRename, ws: WorkspaceDep
) -> schemas.ProjectState:
    return ws.rename(project_id, body.name)


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str, ws: WorkspaceDep) -> None:
    ws.delete(project_id)


@router.get("/projects/{project_id}/parameters", response_model=schemas.ProjectState)
def project_parameters(project_id: str, ws: WorkspaceDep) -> schemas.ProjectState:
    return ws.project(project_id)


@router.post(
    "/projects/{project_id}/commands",
    response_model=schemas.CommandResult,
    responses={422: {"model": schemas.Rejection}},
)
def apply_command(
    project_id: str, body: schemas.CommandRequest, ws: WorkspaceDep
) -> schemas.CommandResult | JSONResponse:
    try:
        return ws.apply(project_id, body.command)
    except CommandRejectedError as exc:
        rejection = schemas.Rejection(detail=str(exc), violations=exc.violations)
        return JSONResponse(status_code=422, content=rejection.model_dump(mode="json"))
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/instructions", response_model=schemas.InstructionResult)
def instruct(
    project_id: str, body: schemas.InstructionRequest, ws: WorkspaceDep
) -> schemas.InstructionResult:
    try:
        return ws.instruct(project_id, body.text)
    except CommandError as exc:
        return schemas.InstructionResult(kind="clarification", message=str(exc))


@router.post(
    "/projects/{project_id}/proposals/{proposal_id}/confirm",
    response_model=schemas.CommandResult,
    responses={422: {"model": schemas.Rejection}},
)
def confirm_proposal(
    project_id: str, proposal_id: str, ws: WorkspaceDep
) -> schemas.CommandResult | JSONResponse:
    try:
        return ws.confirm(project_id, proposal_id)
    except CommandRejectedError as exc:
        rejection = schemas.Rejection(detail=str(exc), violations=exc.violations)
        return JSONResponse(status_code=422, content=rejection.model_dump(mode="json"))


@router.post("/projects/{project_id}/proposals/{proposal_id}/reject", status_code=204)
def reject_proposal(project_id: str, proposal_id: str, ws: WorkspaceDep) -> None:
    ws.reject(project_id, proposal_id)


@router.get("/llm", response_model=schemas.LLMStatusOut)
def llm_status(ws: WorkspaceDep) -> schemas.LLMStatusOut:
    return ws.llm_status()


@router.post("/projects/{project_id}/undo", response_model=schemas.CommandResult)
def undo(project_id: str, ws: WorkspaceDep) -> schemas.CommandResult:
    return ws.undo(project_id)


@router.post("/projects/{project_id}/redo", response_model=schemas.CommandResult)
def redo(project_id: str, ws: WorkspaceDep) -> schemas.CommandResult:
    return ws.redo(project_id)


@router.get("/projects/{project_id}/history", response_model=schemas.HistoryOut)
def history(project_id: str, ws: WorkspaceDep) -> schemas.HistoryOut:
    return ws.history(project_id)


@router.get("/projects/{project_id}/model")
def model(
    project_id: str,
    ws: WorkspaceDep,
    known: Annotated[str, Query(description="comma-separated geometry keys")] = "",
) -> dict:
    return ws.model(project_id, {k for k in known.split(",") if k})


@router.get("/projects/{project_id}/export.step")
def export_step(project_id: str, ws: WorkspaceDep) -> FileResponse:
    path = ws.export_step(project_id)
    name = ws.project(project_id).name
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in name).strip("-") or "vehicle"
    return FileResponse(path, media_type="application/step", filename=f"{safe}.step")


def not_found_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"project '{exc}' not found"})


def proposal_not_found_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404, content={"detail": f"proposal '{exc}' not found or expired"}
    )


EXCEPTION_HANDLERS = {
    ProjectNotFoundError: not_found_handler,
    ProposalNotFoundError: proposal_not_found_handler,
}
