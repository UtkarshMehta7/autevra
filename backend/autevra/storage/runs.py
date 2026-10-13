"""Test runs and requirements. Runs are append-only: a design change never edits them."""

import dataclasses
import json
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from autevra.engineering.testing import Requirement, RunRecord
from autevra.storage.models import RequirementRow, TestRunRow


class RunNotFoundError(LookupError):
    pass


class RunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, project_id: str, record: RunRecord) -> RunRecord:
        self.session.add(TestRunRow(
            id=record.id, project_id=project_id, test_id=record.test_id, target=record.target,
            scenario_id=record.scenario["id"], status=record.status.value,
            values_hash=record.revision.values_hash, inputs_hash=record.revision.inputs_hash,
            created_at=record.created_at, record_json=record.model_dump_json(),
        ))  # fmt: skip
        self.session.flush()
        return record

    def get(self, project_id: str, run_id: str) -> RunRecord:
        row = self.session.get(TestRunRow, run_id)
        if row is None or row.project_id != project_id:
            raise RunNotFoundError(run_id)
        return RunRecord.model_validate_json(row.record_json)

    def find(
        self,
        project_id: str,
        test_id: str | None = None,
        target: str | None = None,
        scenario_id: str | None = None,
        limit: int = 200,
    ) -> list[RunRecord]:
        q = select(TestRunRow).where(TestRunRow.project_id == project_id)
        if test_id:
            q = q.where(TestRunRow.test_id == test_id)
        if target:
            q = q.where(TestRunRow.target == target)
        if scenario_id:
            q = q.where(TestRunRow.scenario_id == scenario_id)
        rows = self.session.scalars(q.order_by(TestRunRow.created_at.desc()).limit(limit))
        return [RunRecord.model_validate_json(r.record_json) for r in rows]

    def latest_by_inputs(self, project_id: str, inputs_hash: str) -> RunRecord | None:
        row = self.session.scalars(
            select(TestRunRow)
            .where(TestRunRow.project_id == project_id, TestRunRow.inputs_hash == inputs_hash)
            .order_by(TestRunRow.created_at.desc())
            .limit(1)
        ).first()
        return None if row is None else RunRecord.model_validate_json(row.record_json)

    # --- requirements ---
    def requirements(self, project_id: str) -> list[Requirement]:
        rows = self.session.scalars(
            select(RequirementRow)
            .where(RequirementRow.project_id == project_id)
            .order_by(RequirementRow.created_at)
        )
        return [Requirement(**json.loads(r.requirement_json)) for r in rows]

    def add_requirement(self, project_id: str, requirement: Requirement) -> Requirement:
        if not requirement.id:
            requirement = dataclasses.replace(requirement, id=uuid4().hex[:12])
        self.session.add(RequirementRow(
            id=requirement.id, project_id=project_id,
            requirement_json=json.dumps(dataclasses.asdict(requirement)),
        ))  # fmt: skip
        self.session.flush()
        return requirement

    def delete_requirement(self, project_id: str, requirement_id: str) -> None:
        row = self.session.get(RequirementRow, requirement_id)
        if row is None or row.project_id != project_id:
            raise RunNotFoundError(requirement_id)
        self.session.delete(row)
