"""Part Design parts: one row per part, holding its feature document and undo/redo."""

import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from autevra.storage.models import PartRow

HISTORY_LIMIT = 50  # earlier documents kept per part for undo


class PartNotFoundError(LookupError):
    pass


class PartRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _row(self, project_id: str, part_id: str) -> PartRow:
        row = self.session.get(PartRow, part_id)
        if row is None or row.project_id != project_id:
            raise PartNotFoundError(part_id)
        return row

    def list(self, project_id: str) -> list[tuple[str, str]]:
        """(part id, document JSON) in display order."""
        rows = self.session.scalars(
            select(PartRow)
            .where(PartRow.project_id == project_id)
            .order_by(PartRow.position, PartRow.created_at)
        )
        return [(r.id, r.document_json) for r in rows]

    def count(self, project_id: str) -> int:
        return len(self.list(project_id))

    def create(self, project_id: str, document_json: str) -> str:
        part_id = uuid.uuid4().hex
        self.session.add(
            PartRow(
                id=part_id,
                project_id=project_id,
                position=self.count(project_id),
                document_json=document_json,
                undo_json="[]",
                redo_json="[]",
            )  # fmt: skip
        )
        self.session.flush()
        return part_id

    def get(self, project_id: str, part_id: str) -> tuple[str, bool, bool]:
        """Document JSON, can undo, can redo."""
        row = self._row(project_id, part_id)
        return row.document_json, row.undo_json != "[]", row.redo_json != "[]"

    def update(self, project_id: str, part_id: str, document_json: str) -> None:
        """Replace the document; the old one goes on the undo stack, redo is cleared."""
        row = self._row(project_id, part_id)
        if document_json == row.document_json:
            return
        undo = json.loads(row.undo_json)
        undo.append(row.document_json)
        row.undo_json = json.dumps(undo[-HISTORY_LIMIT:])
        row.redo_json = "[]"
        row.document_json = document_json
        self.session.flush()

    def step(self, project_id: str, part_id: str, back: bool) -> bool:
        """Undo (back) or redo one edit; False when there is nothing to do."""
        row = self._row(project_id, part_id)
        src, dst = (row.undo_json, row.redo_json) if back else (row.redo_json, row.undo_json)
        source, target = json.loads(src), json.loads(dst)
        if not source:
            return False
        target.append(row.document_json)
        row.document_json = source.pop()
        if back:
            row.undo_json, row.redo_json = json.dumps(source), json.dumps(target)
        else:
            row.redo_json, row.undo_json = json.dumps(source), json.dumps(target)
        self.session.flush()
        return True

    def delete(self, project_id: str, part_id: str) -> None:
        self.session.delete(self._row(project_id, part_id))
        self.session.flush()
