"""A project's styling curves: one document per project, with undo and redo."""

import json

from sqlalchemy.orm import Session

from autevra.storage.models import StylingRow

HISTORY_LIMIT = 50
EMPTY = "{}"


class StylingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, project_id: str) -> tuple[str, bool, bool]:
        """Document JSON ("{}" when none), can undo, can redo."""
        row = self.session.get(StylingRow, project_id)
        if row is None:
            return EMPTY, False, False
        return row.document_json, row.undo_json != "[]", row.redo_json != "[]"

    def set(self, project_id: str, document_json: str) -> None:
        row = self.session.get(StylingRow, project_id)
        if row is None:
            self.session.add(StylingRow(project_id=project_id, document_json=document_json,
                                        undo_json=json.dumps([EMPTY]), redo_json="[]"))  # fmt: skip
        elif document_json != row.document_json:
            undo = json.loads(row.undo_json) + [row.document_json]
            row.undo_json = json.dumps(undo[-HISTORY_LIMIT:])
            row.redo_json = "[]"
            row.document_json = document_json
        self.session.flush()

    def step(self, project_id: str, back: bool) -> bool:
        row = self.session.get(StylingRow, project_id)
        if row is None:
            return False
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
