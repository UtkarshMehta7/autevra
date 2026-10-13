"""Test runs and requirements. Runs are append-only: a design change never edits them."""

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from autevra.engineering.requirements import Requirement as RequirementRecord
from autevra.engineering.requirements import next_key
from autevra.engineering.testing import Requirement, RunRecord
from autevra.storage.models import RequirementRow, StudyRow, TestRunRow


class RunNotFoundError(LookupError):
    pass


class RunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, project_id: str, record: RunRecord) -> RunRecord:
        self.session.add(
            TestRunRow(
                id=record.id,
                project_id=project_id,
                test_id=record.test_id,
                target=record.target,
                scenario_id=record.scenario["id"],
                status=record.status.value,
                values_hash=record.revision.values_hash,
                inputs_hash=record.revision.inputs_hash,
                created_at=record.created_at,
                record_json=record.model_dump_json(),
            )
        )
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
    def requirement_records(self, project_id: str) -> list[RequirementRecord]:
        rows = self.session.scalars(
            select(RequirementRow)
            .where(RequirementRow.project_id == project_id)
            .order_by(RequirementRow.created_at)
        )
        out = []
        for row in rows:
            data = json.loads(row.requirement_json)
            if "kind" not in data:  # stored before Phase 4: a test criterion
                data = {
                    "kind": "performance",
                    "verification": "test",
                    **data,
                    "note": data.get("note", ""),
                }
            out.append(RequirementRecord.model_validate(data | {"id": row.id}))
        for i, record in enumerate(out):  # give pre-Phase-4 records a stable key
            if not record.key:
                out[i] = record.model_copy(update={"key": f"REQ-{i + 1:03d}"})
        return out

    def requirements(self, project_id: str) -> list[Requirement]:
        """Approved performance requirements, in the criterion form used by test verdicts."""
        out = []
        for record in self.requirement_records(project_id):
            criterion = record.as_test_requirement()
            if criterion is not None:
                out.append(criterion)
        return out

    def add_requirement(self, project_id: str, record: RequirementRecord) -> RequirementRecord:
        existing = self.requirement_records(project_id)
        if not record.key:
            record = record.model_copy(update={"key": next_key(existing)})
        if any(r.key == record.key for r in existing):
            raise ValueError(f"requirement key {record.key} already exists")
        self.session.add(
            RequirementRow(
                id=record.id,
                project_id=project_id,
                created_at=record.created_at,
                requirement_json=record.model_dump_json(),
            )
        )
        self.session.flush()
        return record

    def update_requirement(self, project_id: str, record: RequirementRecord) -> RequirementRecord:
        row = self.session.get(RequirementRow, record.id)
        if row is None or row.project_id != project_id:
            raise RunNotFoundError(record.id)
        row.requirement_json = record.model_dump_json()
        self.session.flush()
        return record

    def delete_requirement(self, project_id: str, requirement_id: str) -> None:
        row = self.session.get(RequirementRow, requirement_id)
        if row is None or row.project_id != project_id:
            raise RunNotFoundError(requirement_id)
        self.session.delete(row)


class StudyRepository:
    """Studies are stored as self-describing JSON records keyed by kind."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(
        self, project_id: str, kind: str, study_id: str, status: str, record_json: str
    ) -> None:
        row = self.session.get(StudyRow, study_id)
        if row is None:
            self.session.add(
                StudyRow(
                    id=study_id,
                    project_id=project_id,
                    kind=kind,
                    status=status,
                    record_json=record_json,
                )
            )
        else:
            row.status, row.record_json = status, record_json
        self.session.flush()

    def get(self, project_id: str, study_id: str) -> tuple[str, str]:
        row = self.session.get(StudyRow, study_id)
        if row is None or row.project_id != project_id:
            raise RunNotFoundError(study_id)
        return row.kind, row.record_json

    def find(self, project_id: str, kind: str, limit: int = 50) -> list[str]:
        rows = self.session.scalars(
            select(StudyRow)
            .where(StudyRow.project_id == project_id, StudyRow.kind == kind)
            .order_by(StudyRow.created_at.desc())
            .limit(limit)
        )
        return [r.record_json for r in rows]
