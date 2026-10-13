from pathlib import Path

import pytest

from autevra.core.commands import Change, Operation, SetParameters
from autevra.core.design import DesignState
from autevra.storage.database import Database, migrate
from autevra.storage.repository import ProjectNotFoundError, ProjectRepository


@pytest.fixture
def db(tmp_path: Path) -> Database:
    url = f"sqlite:///{tmp_path / 'test.db'}"
    migrate(url)
    return Database(url)


def _inc(pid: str, value: float) -> SetParameters:
    return SetParameters(
        changes=(Change(parameter=pid, operation=Operation.INCREASE, value=value),)
    )


def test_create_load_round_trip(db: Database) -> None:
    with db.session() as s:
        info = ProjectRepository(s).create("Car")
    with db.session() as s:
        state = ProjectRepository(s).load(info.id)
    assert state.values["wheelbase"] == 2700
    assert state.history == [] and state.cursor == 0


def test_history_undo_and_redo_branch_persist(db: Database) -> None:
    with db.session() as s:
        pid = ProjectRepository(s).create("Car").id
    for step in (_inc("wheelbase", 100), _inc("wheelbase", 50)):
        with db.session() as s:
            repo = ProjectRepository(s)
            state = repo.load(pid)
            state.apply(step)
            repo.save(pid, state)
    with db.session() as s:
        repo = ProjectRepository(s)
        state = repo.load(pid)
        state.undo()
        repo.save(pid, state)
    with db.session() as s:
        state = ProjectRepository(s).load(pid)
    assert state.values["wheelbase"] == 2800
    assert len(state.history) == 2 and state.cursor == 1
    # A new command replaces the redo branch in the database too.
    with db.session() as s:
        repo = ProjectRepository(s)
        state = repo.load(pid)
        state.apply(_inc("body_width", 20))
        repo.save(pid, state)
    with db.session() as s:
        state = ProjectRepository(s).load(pid)
    assert [e.changes[0].parameter for e in state.history] == ["wheelbase", "body_width"]
    assert state.replay() == state.values


def test_missing_project(db: Database) -> None:
    with db.session() as s, pytest.raises(ProjectNotFoundError):
        ProjectRepository(s).load("nope")


def test_delete_cascades(db: Database) -> None:
    with db.session() as s:
        repo = ProjectRepository(s)
        state = DesignState()
        state.apply(_inc("wheelbase", 10))
        pid = repo.create("Car", state).id
    with db.session() as s:
        ProjectRepository(s).delete(pid)
    with db.session() as s:
        assert ProjectRepository(s).list() == []


def test_projects_saved_before_new_parameters_load_with_defaults(tmp_path) -> None:  # type: ignore[no-untyped-def]
    import json

    from autevra.core.parameters import default_values
    from autevra.storage.database import Database, migrate
    from autevra.storage.models import ProjectRow
    from autevra.storage.repository import ProjectRepository

    url = f"sqlite:///{tmp_path / 'old.db'}"
    migrate(url)
    db = Database(url)
    old = {k: v for k, v in default_values().items() if "damping" not in k} | {"wheelbase": 2800}
    with db.session() as s:
        s.add(ProjectRow(id="p" * 32, name="old", values_json=json.dumps(old), cursor=0))
    with db.session() as s:
        values = ProjectRepository(s).load("p" * 32).values
    assert values["wheelbase"] == 2800
    assert values["front_damping_bump"] == default_values()["front_damping_bump"]
