"""Project repository: loads and saves ``DesignState`` (values, history, cursor)."""

import json
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from autevra.domain import parameters
from autevra.domain.design import DesignState, HistoryEntry
from autevra.storage.models import HistoryRow, ProjectRow


class ProjectNotFoundError(LookupError):
    pass


@dataclass(frozen=True)
class ProjectInfo:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    domain: str = "automotive"


def _info(row: ProjectRow) -> ProjectInfo:
    return ProjectInfo(row.id, row.name, row.created_at, row.updated_at, row.domain)


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self, name: str, state: DesignState | None = None, domain: str = "automotive"
    ) -> ProjectInfo:
        state = state or DesignState()
        row = ProjectRow(
            id=uuid4().hex,
            name=name,
            values_json=json.dumps(state.values),
            cursor=state.cursor,
            domain=domain,
        )
        self.session.add(row)
        self.session.flush()
        self._sync_history(row, state)
        return _info(row)

    def list(self) -> list[ProjectInfo]:
        rows = self.session.scalars(select(ProjectRow).order_by(ProjectRow.updated_at.desc()))
        return [_info(r) for r in rows]

    def _row(self, project_id: str) -> ProjectRow:
        row = self.session.get(ProjectRow, project_id)
        if row is None:
            raise ProjectNotFoundError(project_id)
        return row

    def info(self, project_id: str) -> ProjectInfo:
        return _info(self._row(project_id))

    def load(self, project_id: str) -> DesignState:
        row = self._row(project_id)
        stored = json.loads(row.values_json)
        # Projects saved before a parameter existed get its default; retired ids are dropped.
        values = parameters.default_values() | {
            k: v for k, v in stored.items() if k in parameters.REGISTRY
        }
        return DesignState(
            values=values,
            history=[HistoryEntry.model_validate_json(h.entry_json) for h in row.history],
            cursor=row.cursor,
        )

    def save(self, project_id: str, state: DesignState) -> None:
        row = self._row(project_id)
        row.values_json = json.dumps(state.values)
        row.cursor = state.cursor
        self._sync_history(row, state)

    def rename(self, project_id: str, name: str) -> ProjectInfo:
        row = self._row(project_id)
        row.name = name
        self.session.flush()
        return _info(row)

    def delete(self, project_id: str) -> None:
        self.session.delete(self._row(project_id))

    def _sync_history(self, row: ProjectRow, state: DesignState) -> None:
        """Keep the common prefix of entries, replace the rest (O(changed entries))."""
        stored = self.session.execute(
            select(HistoryRow.seq, HistoryRow.id)
            .where(HistoryRow.project_id == row.id)
            .order_by(HistoryRow.seq)
        ).all()
        keep = 0
        for (seq, entry_id), entry in zip(stored, state.history, strict=False):
            if seq != keep or entry_id != entry.id:
                break
            keep += 1
        self.session.execute(
            delete(HistoryRow).where(HistoryRow.project_id == row.id, HistoryRow.seq >= keep)
        )
        for seq, entry in enumerate(state.history[keep:], start=keep):
            self.session.add(
                HistoryRow(
                    id=entry.id,
                    project_id=row.id,
                    seq=seq,
                    entry_json=entry.model_dump_json(),
                    created_at=entry.created_at,
                )
            )
        self.session.flush()
