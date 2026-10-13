"""Request and response schemas for the HTTP API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from autevra.domain.commands import SetParameters
from autevra.domain.design import HistoryEntry
from autevra.domain.parameters import ParameterDef
from autevra.domain.rules import Violation
from autevra.engineering.testing import Comparison, RunRecord, RunStatus


class ProjectCreate(BaseModel):
    name: str = Field(default="Untitled vehicle", min_length=1, max_length=200)


class ProjectRename(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ProjectSummary(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class DerivedValue(BaseModel):
    id: str
    label: str
    unit: str
    value: float
    controlled_by: tuple[str, ...]


class ProjectState(ProjectSummary):
    values: dict[str, float]
    derived: list[DerivedValue]
    can_undo: bool
    can_redo: bool
    history_length: int
    cursor: int


class Catalogue(BaseModel):
    parameters: list[ParameterDef]
    derived: list[DerivedValue]


class ImpactOut(BaseModel):
    rebuild: list[str]
    move: list[str]
    retest: list[str] = []  # "test_id:target" whose results this change makes stale


class CommandResult(BaseModel):
    changed: list[str]
    values: dict[str, float]
    impact: ImpactOut
    entry: HistoryEntry | None
    can_undo: bool
    can_redo: bool


class CommandRequest(BaseModel):
    command: SetParameters


class Rejection(BaseModel):
    detail: str
    violations: list[Violation]


class InstructionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


InstructionKind = Literal[
    "command",
    "undo",
    "redo",
    "query",
    "clarification",
    "rejected",
    "proposal",
    "out_of_scope",
    "test",
]


class InstructionResult(BaseModel):
    kind: InstructionKind
    message: str
    interpreted_by: Literal["rules", "llm"] = "rules"
    command: SetParameters | None = None
    proposal_id: str | None = None
    preview: dict[str, float] = {}
    result: CommandResult | None = None
    suggestions: list[str] = []
    assumptions: list[str] = []
    violations: list[Violation] = []
    answer: dict[str, float] = {}
    runs: list["RunSummary"] = []
    comparisons: list[Comparison] = []


class HistoryOut(BaseModel):
    entries: list[HistoryEntry]
    cursor: int


class LLMStatusOut(BaseModel):
    provider: str
    model: str
    url: str
    available: bool
    detail: str
    models: list[str]


class RunSummary(BaseModel):
    id: str
    test_id: str
    test_name: str
    target: str
    scenario_id: str
    scenario_label: str
    status: RunStatus
    credibility: str
    created_at: datetime
    history_cursor: int
    current: bool  # True if the design inputs this test reads are unchanged since the run
    failed: list[str]  # labels of failed criteria
    warnings: list[str]

    @classmethod
    def of(cls, run: RunRecord, current: bool) -> "RunSummary":
        return cls(
            id=run.id, test_id=run.test_id, test_name=run.test_name, target=run.target,
            scenario_id=run.scenario["id"], scenario_label=run.scenario["label"],
            status=run.status, credibility=run.credibility.value, created_at=run.created_at,
            history_cursor=run.revision.history_cursor, current=current,
            failed=[c.label for c in run.criteria if c.passed is False], warnings=run.warnings,
        )  # fmt: skip


class TestRunRequest(BaseModel):
    test_id: str = "quarter_car"
    target: str
    scenario_id: str | None = None  # None: every scenario of the test


class TestRunResponse(BaseModel):
    runs: list[RunRecord]
    comparisons: list[Comparison] = []


class ScenarioOut(BaseModel):
    id: str
    label: str
    road: str
    height_mm: float
    length_m: float
    speed_kmh: float
    duration_s: float
    note: str


class CriterionOut(BaseModel):
    id: str
    label: str
    metric: str
    comparator: str
    unit: str
    limit: float | None
    limit_from: str | None
    source: str


class TestDefinitionOut(BaseModel):
    id: str
    name: str
    description: str
    solver: str
    credibility: str
    targets: list[str]
    components: dict[str, list[str]]
    inputs: dict[str, list[str]]
    scenarios: list[ScenarioOut]
    criteria: list[CriterionOut]
    metrics: dict[str, dict]
    assumptions: list[str]


class ComponentTestStatus(BaseModel):
    component: str
    status: str
    tests: list[dict]  # per (test, target, scenario): status, run id, current


class RequirementIn(BaseModel):
    test_id: str = "quarter_car"
    target: Literal["front", "rear", "*"] = "*"
    scenario_id: str = "*"
    metric: str
    comparator: Literal["<=", "<", ">=", ">"]
    limit: float
    unit: str = ""
    note: str = ""


class RequirementOut(RequirementIn):
    id: str
    approved: bool


class CheckOut(BaseModel):
    id: str
    kind: str
    status: str
    message: str
    components: list[str]
    parameters: list[str]
    measured: float | None
    limit: float | None
    unit: str


class IntegrationOut(BaseModel):
    checks: list[CheckOut]
    counts: dict[str, int]
    not_checked: list[str]


InstructionResult.model_rebuild()
