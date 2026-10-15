"""HTTP routes. Thin: validation by Pydantic, logic in ``Workspace``."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, Response

from autevra import domains
from autevra.api import access, schemas
from autevra.api.service import ProposalNotFoundError, Workspace, _derived
from autevra.core import parameters, templates
from autevra.core.commands import CommandError
from autevra.core.design import CommandRejectedError
from autevra.domains import DomainDef
from autevra.engineering import loop as eloop
from autevra.engineering import optimize as opt
from autevra.engineering import testing as tst
from autevra.engineering.diagnosis import Diagnosis
from autevra.engineering.trace import ImpactPreview
from autevra.part.features import FEATURE_TYPES, PartDoc
from autevra.storage.parts import PartNotFoundError
from autevra.storage.repository import ProjectNotFoundError
from autevra.storage.runs import RunNotFoundError

router = APIRouter(prefix="/api", dependencies=[Depends(access.guard_project)])


def workspace(request: Request) -> Workspace:
    return request.app.state.workspace


WorkspaceDep = Annotated[Workspace, Depends(workspace)]
VisitorDep = Annotated[access.Visitor, Depends(access.visitor)]


@router.get("/parameters", response_model=schemas.Catalogue)
def catalogue() -> schemas.Catalogue:
    return schemas.Catalogue(
        parameters=list(parameters.REGISTRY.values()), derived=_derived(parameters.default_values())
    )


@router.get("/projects", response_model=list[schemas.ProjectSummary])
def list_projects(ws: WorkspaceDep, who: VisitorDep) -> list[schemas.ProjectSummary]:
    return ws.list_projects(who.owner, all_owners=who.all_owners)


@router.post("/projects", response_model=schemas.ProjectState, status_code=201)
def create_project(
    body: schemas.ProjectCreate, ws: WorkspaceDep, who: VisitorDep, request: Request
) -> schemas.ProjectState:
    access.check_project_quota(request, who)
    try:
        return ws.create_project(body.name, body.domain, who.owner, body.template)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None


@router.post(
    "/projects/{project_id}/duplicate", response_model=schemas.ProjectState, status_code=201
)
def duplicate_project(
    project_id: str,
    ws: WorkspaceDep,
    who: VisitorDep,
    request: Request,
    body: schemas.ProjectRename | None = None,
) -> schemas.ProjectState:
    access.check_project_quota(request, who)
    return ws.duplicate_project(project_id, body.name if body else None, who.owner)


@router.get("/projects/{project_id}/system", response_model=schemas.SystemGraph)
def system_graph(project_id: str, ws: WorkspaceDep) -> schemas.SystemGraph:
    """Components, interfaces and typed relationships of the assembly."""
    return ws.system_graph(project_id)


@router.get("/projects/{project_id}/rules", response_model=list[schemas.RuleStatus])
def rule_status(project_id: str, ws: WorkspaceDep) -> list[schemas.RuleStatus]:
    return ws.rule_status(project_id)


@router.get("/runs", response_model=list[schemas.RunIndexItem])
def all_runs(ws: WorkspaceDep, who: VisitorDep) -> list[schemas.RunIndexItem]:
    """Recent runs across the visitor's projects (all projects locally)."""
    return ws.all_runs(owner=who.owner, all_owners=who.all_owners)


@router.get("/templates", response_model=list[schemas.TemplateOut])
def list_templates() -> list[schemas.TemplateOut]:
    """Starting designs for new projects (one per vehicle class in the automotive domain)."""
    return [
        schemas.TemplateOut(id=t.id, label=t.label, description=t.description)
        for t in templates.TEMPLATES.values()
    ]


@router.get("/domains", response_model=list[DomainDef])
def list_domains() -> list[DomainDef]:
    return domains.registry()


@router.post("/contact", response_model=schemas.ContactOut, status_code=201)
def contact(body: schemas.ContactIn, ws: WorkspaceDep) -> schemas.ContactOut:
    return ws.contact(body)


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


@router.get("/plugins")
def plugins() -> list[dict]:
    """Loaded plugins and what each one adds."""
    from autevra import extensions

    return [
        {
            "name": p.name,
            "version": p.version,
            "description": p.description,
            "parameters": [x.id for x in p.parameters],
            "components": [c.id for c in p.components],
            "rules": [r.id for r, _ in p.rules],
            "tests": [t.id for t in p.tests],
        }
        for p in extensions.LOADED.values()
        if domains.get(p.name) is None  # domain modules are listed by /domains
    ]


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


@router.get("/tests", response_model=list[schemas.TestDefinitionOut])
def test_catalogue() -> list[schemas.TestDefinitionOut]:
    return [
        schemas.TestDefinitionOut(
            id=t.id,
            name=t.name,
            description=t.description,
            solver=t.solver,
            credibility=t.credibility.value,
            targets=list(t.targets),
            components={k: list(v) for k, v in t.components.items()},
            inputs={target: list(t.inputs(target)) for target in t.targets},
            scenarios=[schemas.ScenarioOut(**sc.__dict__) for sc in t.scenarios],
            criteria=[schemas.CriterionOut(**c.__dict__) for c in t.criteria],
            metrics={
                k: {"label": m[0], "unit": m[1], "lower_is_better": m[2]}
                for k, m in t.metrics.items()
            },
            assumptions=list(t.assumptions),
        )
        for t in tst.DEFINITIONS.values()
    ]


@router.post("/projects/{project_id}/tests/run", response_model=schemas.TestRunResponse)
def run_tests(
    project_id: str, body: schemas.TestRunRequest, ws: WorkspaceDep
) -> schemas.TestRunResponse:
    definition = tst.DEFINITIONS.get(body.test_id)
    if definition is None or body.target not in (*definition.targets, "all"):
        raise HTTPException(status_code=422, detail="unknown test or target")
    if body.scenario_id and body.scenario_id not in {sc.id for sc in definition.scenarios}:
        raise HTTPException(status_code=422, detail=f"unknown scenario '{body.scenario_id}'")
    targets = list(definition.targets) if body.target == "all" else [body.target]
    return ws.run_tests(project_id, body.test_id, targets, body.scenario_id)


@router.post("/projects/{project_id}/tests/retest", response_model=schemas.TestRunResponse)
def retest_stale(project_id: str, ws: WorkspaceDep) -> schemas.TestRunResponse:
    """Rerun every previously run test case whose result is out of date."""
    return ws.retest_stale(project_id)


@router.get("/projects/{project_id}/runs", response_model=list[schemas.RunSummary])
def list_runs(
    project_id: str,
    ws: WorkspaceDep,
    test_id: str | None = None,
    target: str | None = None,
    scenario_id: str | None = None,
) -> list[schemas.RunSummary]:
    return ws.list_runs(project_id, test_id, target, scenario_id)


@router.get("/projects/{project_id}/runs/compare", response_model=tst.Comparison)
def compare_runs(
    project_id: str, baseline: str, candidate: str, ws: WorkspaceDep
) -> tst.Comparison:
    return ws.compare_runs(project_id, baseline, candidate)


@router.get("/projects/{project_id}/runs/{run_id}/diagnosis", response_model=Diagnosis)
def diagnose_run(project_id: str, run_id: str, ws: WorkspaceDep) -> Diagnosis:
    return ws.diagnose(project_id, run_id)


@router.get("/projects/{project_id}/runs/{run_id}", response_model=tst.RunRecord)
def get_run(project_id: str, run_id: str, ws: WorkspaceDep) -> tst.RunRecord:
    return ws.get_run(project_id, run_id)


@router.get(
    "/projects/{project_id}/components/status", response_model=list[schemas.ComponentTestStatus]
)
def component_status(project_id: str, ws: WorkspaceDep) -> list[schemas.ComponentTestStatus]:
    return ws.component_status(project_id)


@router.get("/projects/{project_id}/requirements", response_model=list[schemas.RequirementOut])
def list_requirements(project_id: str, ws: WorkspaceDep) -> list[schemas.RequirementOut]:
    """Requirements with their verification, linked parameters, components and test cases."""
    return ws.requirements(project_id)


@router.post(
    "/projects/{project_id}/requirements", response_model=schemas.RequirementOut, status_code=201
)
def add_requirement(
    project_id: str, body: schemas.RequirementIn, ws: WorkspaceDep
) -> schemas.RequirementOut:
    try:
        return ws.add_requirement(project_id, body)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.patch(
    "/projects/{project_id}/requirements/{requirement_id}", response_model=schemas.RequirementOut
)
def update_requirement(
    project_id: str, requirement_id: str, body: dict, ws: WorkspaceDep
) -> schemas.RequirementOut:
    allowed = set(schemas.RequirementIn.model_fields)
    if set(body) - allowed:
        raise HTTPException(
            status_code=422, detail=f"unknown fields: {sorted(set(body) - allowed)}"
        )
    try:
        return ws.update_requirement(project_id, requirement_id, body)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.delete("/projects/{project_id}/requirements/{requirement_id}", status_code=204)
def delete_requirement(project_id: str, requirement_id: str, ws: WorkspaceDep) -> None:
    ws.delete_requirement(project_id, requirement_id)


@router.post(
    "/projects/{project_id}/requirements/verify", response_model=list[schemas.RequirementOut]
)
def verify_requirements(project_id: str, ws: WorkspaceDep) -> list[schemas.RequirementOut]:
    return ws.verify_requirements(project_id)


@router.get("/projects/{project_id}/requirements.reqif")
def export_reqif(project_id: str, ws: WorkspaceDep) -> Response:
    xml = ws.export_reqif(project_id)
    return Response(
        xml,
        media_type="application/xml",
        headers={"Content-Disposition": 'attachment; filename="requirements.reqif"'},
    )


@router.post(
    "/projects/{project_id}/requirements.reqif", response_model=list[schemas.RequirementOut]
)
async def import_reqif(
    project_id: str, request: Request, ws: WorkspaceDep
) -> list[schemas.RequirementOut]:
    body = await request.body()
    try:
        return ws.import_reqif(project_id, body)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/preview", response_model=ImpactPreview)
def preview_command(
    project_id: str, body: schemas.CommandRequest, ws: WorkspaceDep
) -> ImpactPreview:
    try:
        return ws.preview(project_id, body.command)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.get("/projects/{project_id}/integration", response_model=schemas.IntegrationOut)
def integration_report(project_id: str, ws: WorkspaceDep) -> schemas.IntegrationOut:
    return ws.integration(project_id)


@router.post("/projects/{project_id}/optimize", response_model=opt.StudyResult)
def optimize(project_id: str, body: opt.Study, ws: WorkspaceDep) -> opt.StudyResult:
    try:
        return ws.optimize(project_id, body)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/loop", response_model=eloop.LoopResult)
def engineering_loop(project_id: str, body: eloop.Goal, ws: WorkspaceDep) -> eloop.LoopResult:
    try:
        return ws.engineering_loop(project_id, body)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.get("/optimize/defaults")
def optimize_defaults(target: str = "rear", test_id: str = "quarter_car") -> dict:
    values = parameters.default_values()
    return {"variables": [v.model_dump() for v in opt.default_variables(test_id, target, values)]}


@router.get("/projects/{project_id}/loops", response_model=list[eloop.LoopResult])
def list_loops(project_id: str, ws: WorkspaceDep) -> list[eloop.LoopResult]:
    return ws.loops(project_id)


@router.get("/projects/{project_id}/studies", response_model=list[opt.StudyResult])
def list_studies(project_id: str, ws: WorkspaceDep) -> list[opt.StudyResult]:
    return ws.studies(project_id)


@router.post(
    "/projects/{project_id}/studies/{study_id}/accept",
    response_model=schemas.CommandResult,
    responses={422: {"model": schemas.Rejection}},
)
def accept_study(
    project_id: str, study_id: str, ws: WorkspaceDep
) -> schemas.CommandResult | JSONResponse:
    try:
        result = ws.decide_study(project_id, study_id, accept=True)
    except CommandRejectedError as exc:
        rejection = schemas.Rejection(detail=str(exc), violations=exc.violations)
        return JSONResponse(status_code=422, content=rejection.model_dump(mode="json"))
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None
    assert result is not None
    return result


@router.post(
    "/projects/{project_id}/studies/{study_id}/choose/{index}", response_model=opt.StudyResult
)
def choose_candidate(
    project_id: str, study_id: str, index: int, ws: WorkspaceDep
) -> opt.StudyResult:
    try:
        return ws.choose_candidate(project_id, study_id, index)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None


@router.post("/projects/{project_id}/studies/{study_id}/reject", status_code=204)
def reject_study(project_id: str, study_id: str, ws: WorkspaceDep) -> None:
    try:
        ws.decide_study(project_id, study_id, accept=False)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None


@router.get("/projects/{project_id}/spec", response_model=schemas.SpecState)
def get_spec(project_id: str, ws: WorkspaceDep) -> schemas.SpecState:
    return ws.spec(project_id)


@router.post("/projects/{project_id}/spec/answers", response_model=schemas.SpecState)
def answer_spec(project_id: str, body: schemas.SpecAnswer, ws: WorkspaceDep) -> schemas.SpecState:
    try:
        return ws.spec_answer(project_id, body.question, body.value)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/spec/text", response_model=schemas.SpecState)
def spec_from_text(project_id: str, body: schemas.SpecText, ws: WorkspaceDep) -> schemas.SpecState:
    return ws.spec_text(project_id, body.text)[0]


@router.delete("/projects/{project_id}/spec", response_model=schemas.SpecState)
def reset_spec(project_id: str, ws: WorkspaceDep) -> schemas.SpecState:
    return ws.spec_reset(project_id)


@router.post("/projects/{project_id}/spec/design", response_model=schemas.SpecDesign)
def spec_design(project_id: str, ws: WorkspaceDep) -> schemas.SpecDesign:
    try:
        return ws.spec_design(project_id)
    except CommandError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@router.post("/projects/{project_id}/spec/apply", response_model=schemas.SpecApplied)
def spec_apply(project_id: str, ws: WorkspaceDep) -> schemas.SpecApplied:
    try:
        return ws.spec_apply(project_id)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None
    except CommandRejectedError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


# --- Part Design ---


@router.get("/part-features")
def part_features() -> dict:
    """The feature types and the JSON schema of a part document (for editors and tools)."""
    return {"types": list(FEATURE_TYPES), "schema": PartDoc.model_json_schema()}


@router.get("/part-presets")
def part_presets() -> dict[str, PartDoc]:
    """Starting-point parts from several domains (aerospace, consumer products, tooling,
    plant and machinery)."""
    from autevra.part.presets import presets

    return presets()


@router.get("/projects/{project_id}/parts", response_model=list[schemas.PartOut])
def list_parts(project_id: str, ws: WorkspaceDep) -> list[schemas.PartOut]:
    return ws.parts(project_id)


@router.post("/projects/{project_id}/parts", response_model=schemas.PartOut, status_code=201)
def create_part(project_id: str, body: PartDoc, ws: WorkspaceDep) -> schemas.PartOut:
    try:
        return ws.create_part(project_id, body)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None


@router.put("/projects/{project_id}/parts/{part_id}", response_model=schemas.PartOut)
def update_part(project_id: str, part_id: str, body: PartDoc, ws: WorkspaceDep) -> schemas.PartOut:
    return ws.update_part(project_id, part_id, body)


@router.post("/projects/{project_id}/parts/{part_id}/undo", response_model=schemas.PartOut)
def undo_part(project_id: str, part_id: str, ws: WorkspaceDep) -> schemas.PartOut:
    try:
        return ws.step_part(project_id, part_id, back=True)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None


@router.post("/projects/{project_id}/parts/{part_id}/redo", response_model=schemas.PartOut)
def redo_part(project_id: str, part_id: str, ws: WorkspaceDep) -> schemas.PartOut:
    try:
        return ws.step_part(project_id, part_id, back=False)
    except CommandError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None


@router.delete("/projects/{project_id}/parts/{part_id}", status_code=204)
def delete_part(project_id: str, part_id: str, ws: WorkspaceDep) -> None:
    ws.delete_part(project_id, part_id)


def part_not_found_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"part '{exc}' not found"})


def run_not_found_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"'{exc}' not found"})


def not_found_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"project '{exc}' not found"})


def proposal_not_found_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404, content={"detail": f"proposal '{exc}' not found or expired"}
    )


EXCEPTION_HANDLERS = {
    ProjectNotFoundError: not_found_handler,
    ProposalNotFoundError: proposal_not_found_handler,
    RunNotFoundError: run_not_found_handler,
    PartNotFoundError: part_not_found_handler,
}
