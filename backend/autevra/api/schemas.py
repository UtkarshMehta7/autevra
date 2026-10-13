"""Request and response schemas for the HTTP API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from autevra.domain.commands import SetParameters
from autevra.domain.design import HistoryEntry
from autevra.domain.parameters import ParameterDef
from autevra.domain.rules import Violation


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
    "command", "undo", "redo", "query", "clarification", "rejected", "proposal", "out_of_scope"
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
