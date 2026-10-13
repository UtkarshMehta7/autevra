"""Workspace service: the one place where commands, persistence and CAD meet.

All mutations and CAD builds run under one lock: the kernel is used from a
single thread at a time and jobs stay sequential (8 GB memory budget).
"""

import threading
from collections.abc import Iterable
from pathlib import Path

from autevra.ai import rule_parser
from autevra.ai.rule_parser import Kind
from autevra.api import model_service, schemas
from autevra.assembly import graph
from autevra.cad.cache import GeometryCache
from autevra.domain import derived, parameters
from autevra.domain.commands import SetParameters
from autevra.domain.design import ApplyResult, CommandRejectedError, DesignState
from autevra.storage.database import Database
from autevra.storage.repository import ProjectInfo, ProjectRepository


def _derived(values: dict[str, float]) -> list[schemas.DerivedValue]:
    computed = derived.compute_all(values)
    return [
        schemas.DerivedValue(
            id=d.id,
            label=d.label,
            unit=d.unit,
            value=round(computed[d.id], 3),
            controlled_by=d.controlled_by,
        )
        for d in derived.DERIVED.values()
    ]


def _state(info: ProjectInfo, state: DesignState) -> schemas.ProjectState:
    return schemas.ProjectState(
        id=info.id,
        name=info.name,
        created_at=info.created_at,
        updated_at=info.updated_at,
        values=state.values,
        derived=_derived(state.values),
        can_undo=state.can_undo,
        can_redo=state.can_redo,
        history_length=len(state.history),
        cursor=state.cursor,
    )


def _result(state: DesignState, applied: ApplyResult) -> schemas.CommandResult:
    return _command_result(state, applied.changed, applied.entry)


def _command_result(state: DesignState, changed: Iterable[str], entry) -> schemas.CommandResult:  # type: ignore[no-untyped-def]
    changed = list(changed)
    impact = graph.impact(changed)
    return schemas.CommandResult(
        changed=changed,
        values=state.values,
        impact=schemas.ImpactOut(rebuild=sorted(impact.rebuild), move=sorted(impact.move)),
        entry=entry,
        can_undo=state.can_undo,
        can_redo=state.can_redo,
    )


def _format(pid: str, values: dict[str, float]) -> str:
    if pid in parameters.REGISTRY:
        spec = parameters.REGISTRY[pid]
        return f"{spec.label}: {values[pid]:g} {spec.unit}"
    spec = derived.DERIVED[pid]
    return f"{spec.label}: {derived.compute(pid, values):.1f} {spec.unit}"


class Workspace:
    def __init__(self, db: Database, data_dir: Path) -> None:
        self.db = db
        self.data_dir = data_dir
        self.cache = GeometryCache()
        self._lock = threading.RLock()

    # --- projects ---
    def create_project(self, name: str) -> schemas.ProjectState:
        with self.db.session() as s:
            repo = ProjectRepository(s)
            info = repo.create(name)
            return _state(info, repo.load(info.id))

    def list_projects(self) -> list[schemas.ProjectSummary]:
        with self.db.session() as s:
            return [schemas.ProjectSummary(**vars(i)) for i in ProjectRepository(s).list()]

    def project(self, project_id: str) -> schemas.ProjectState:
        with self.db.session() as s:
            repo = ProjectRepository(s)
            return _state(repo.info(project_id), repo.load(project_id))

    def rename(self, project_id: str, name: str) -> schemas.ProjectState:
        with self.db.session() as s:
            repo = ProjectRepository(s)
            info = repo.rename(project_id, name)
            return _state(info, repo.load(project_id))

    def delete(self, project_id: str) -> None:
        with self.db.session() as s:
            ProjectRepository(s).delete(project_id)

    def history(self, project_id: str) -> schemas.HistoryOut:
        with self.db.session() as s:
            state = ProjectRepository(s).load(project_id)
            return schemas.HistoryOut(entries=state.history, cursor=state.cursor)

    # --- commands ---
    def apply(self, project_id: str, command: SetParameters) -> schemas.CommandResult:
        """Validate and apply; raises CommandRejectedError (state untouched) or CommandError."""
        with self._lock, self.db.session() as s:
            repo = ProjectRepository(s)
            state = repo.load(project_id)
            applied = state.apply(command)
            repo.save(project_id, state)
            return _result(state, applied)

    def undo(self, project_id: str) -> schemas.CommandResult:
        return self._step(project_id, redo=False)

    def redo(self, project_id: str) -> schemas.CommandResult:
        return self._step(project_id, redo=True)

    def _step(self, project_id: str, redo: bool) -> schemas.CommandResult:
        with self._lock, self.db.session() as s:
            repo = ProjectRepository(s)
            state = repo.load(project_id)
            entry = state.redo() if redo else state.undo()
            repo.save(project_id, state)
            changed = [c.parameter for c in entry.changes] if entry else []
            return _command_result(state, changed, entry)

    def instruct(self, project_id: str, text: str) -> schemas.InstructionResult:
        interpretation = rule_parser.parse(text)
        match interpretation.kind:
            case Kind.UNDO | Kind.REDO:
                redo = interpretation.kind is Kind.REDO
                result = self._step(project_id, redo=redo)
                word = "Redid" if redo else "Undid"
                message = (
                    f"{word} the change to {', '.join(result.changed)}."
                    if result.changed
                    else f"Nothing to {'redo' if redo else 'undo'}."
                )
                return schemas.InstructionResult(
                    kind=interpretation.kind.value, message=message, result=result
                )
            case Kind.QUERY:
                values = self.project(project_id).values
                answer = {
                    pid: (values[pid] if pid in values else derived.compute(pid, values))
                    for pid in interpretation.query
                }
                message = "; ".join(_format(pid, values) for pid in interpretation.query)
                return schemas.InstructionResult(kind="query", message=message, answer=answer)
            case Kind.CLARIFICATION:
                return schemas.InstructionResult(
                    kind="clarification",
                    message=interpretation.question or "",
                    suggestions=interpretation.suggestions,
                )
        command = interpretation.command
        assert command is not None
        try:
            result = self.apply(project_id, command)
        except CommandRejectedError as exc:
            return schemas.InstructionResult(
                kind="rejected",
                message=f"I can't apply that: {exc}",
                command=command,
                violations=exc.violations,
                assumptions=interpretation.assumptions,
            )
        if result.changed:
            values = result.values
            message = "Set " + "; ".join(_format(p, values) for p in result.changed) + "."
        else:
            message = "No change: the design already has those values."
        return schemas.InstructionResult(
            kind="command",
            message=message,
            command=command,
            result=result,
            assumptions=interpretation.assumptions,
        )

    # --- geometry ---
    def model(self, project_id: str, known: set[str]) -> dict:
        values = self.project(project_id).values
        with self._lock:
            model = model_service.build_model(values, self.cache)
            return model_service.mesh_payload(model, self.cache, skip=known)

    def export_step(self, project_id: str) -> Path:
        values = self.project(project_id).values
        with self._lock:
            model = model_service.build_model(values, self.cache)
            return model_service.export_step(
                model, self.data_dir / "exports" / f"{project_id}.step"
            )
