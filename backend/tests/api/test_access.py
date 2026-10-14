from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from autevra.api.access import HEADER, SlidingWindow
from autevra.config import Settings
from autevra.main import create_app

ALICE = {HEADER: "a" * 32}
BOB = {HEADER: "b" * 32}


def _client(tmp_path: Path, **overrides) -> TestClient:  # type: ignore[no-untyped-def]
    settings = Settings(
        data_dir=tmp_path / "data", llm_provider="off", plugin_entry_points=False, **overrides
    )
    return TestClient(create_app(settings))


@pytest.fixture
def public(tmp_path: Path) -> Iterator[TestClient]:
    with _client(tmp_path, workspace_isolation=True, max_projects_per_workspace=3) as c:
        yield c


def test_visitors_see_only_their_own_projects(public: TestClient) -> None:
    mine = public.post("/api/projects", json={"name": "mine"}, headers=ALICE).json()["id"]
    public.post("/api/projects", json={"name": "theirs"}, headers=BOB)

    assert [p["name"] for p in public.get("/api/projects", headers=ALICE).json()] == ["mine"]
    assert [p["name"] for p in public.get("/api/projects", headers=BOB).json()] == ["theirs"]
    assert public.get(f"/api/projects/{mine}", headers=ALICE).status_code == 200


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get", ""),
        ("patch", ""),
        ("delete", ""),
        ("get", "/model"),
        ("get", "/history"),
        ("post", "/undo"),
        ("post", "/duplicate"),
        ("get", "/export.step"),
    ],
)
def test_another_workspace_gets_not_found(public: TestClient, method: str, path: str) -> None:
    pid = public.post("/api/projects", json={"name": "mine"}, headers=ALICE).json()["id"]
    kwargs = {"json": {"name": "x"}} if method == "patch" else {}
    reply = getattr(public, method)(f"/api/projects/{pid}{path}", headers=BOB, **kwargs)
    assert reply.status_code == 404
    assert public.get(f"/api/projects/{pid}", headers=ALICE).json()["name"] == "mine"


def test_duplicate_belongs_to_the_visitor(public: TestClient) -> None:
    pid = public.post("/api/projects", json={"name": "mine"}, headers=ALICE).json()["id"]
    copy = public.post(f"/api/projects/{pid}/duplicate", headers=ALICE).json()["id"]
    assert public.get(f"/api/projects/{copy}", headers=ALICE).status_code == 200
    assert public.get(f"/api/projects/{copy}", headers=BOB).status_code == 404


def test_run_index_is_per_visitor(public: TestClient) -> None:
    pid = public.post("/api/projects", json={"name": "mine"}, headers=ALICE).json()["id"]
    public.post(f"/api/projects/{pid}/tests/run", json={"target": "rear"}, headers=ALICE)
    assert public.get("/api/runs", headers=ALICE).json()
    assert public.get("/api/runs", headers=BOB).json() == []


def test_requests_without_a_valid_key_are_refused(public: TestClient) -> None:
    assert public.get("/api/projects").status_code == 400
    assert public.get("/api/projects", headers={HEADER: "short"}).status_code == 400
    # Catalogue and health need no workspace.
    assert public.get("/api/parameters").status_code == 200
    assert public.get("/api/health").status_code == 200


def test_project_quota_per_workspace(public: TestClient) -> None:
    for i in range(3):
        assert (
            public.post("/api/projects", json={"name": f"p{i}"}, headers=ALICE).status_code == 201
        )
    over = public.post("/api/projects", json={"name": "p3"}, headers=ALICE)
    assert over.status_code == 429 and "3 projects" in over.json()["detail"]
    assert public.post("/api/projects", json={"name": "b"}, headers=BOB).status_code == 201


def test_without_isolation_everything_is_shared(client: TestClient) -> None:
    client.post("/api/projects", json={"name": "one"}, headers=ALICE)
    client.post("/api/projects", json={"name": "two"})
    assert {p["name"] for p in client.get("/api/projects").json()} == {"one", "two"}


def test_writes_are_rate_limited_per_client(tmp_path: Path) -> None:
    with _client(tmp_path, write_limit_per_minute=3) as c:
        codes = [c.post("/api/projects", json={"name": f"p{i}"}).status_code for i in range(4)]
        assert codes == [201, 201, 201, 429]
        limited = c.post("/api/projects", json={"name": "x"})
        assert int(limited.headers["Retry-After"]) >= 1
        assert c.get("/api/projects").status_code == 200  # reads are never limited


def test_contact_form_has_its_own_limit(tmp_path: Path) -> None:
    body = {"name": "A", "email": "a@example.com", "topic": "question", "message": "hello there"}
    with _client(tmp_path, contact_limit_per_hour=1) as c:
        assert c.post("/api/contact", json=body).status_code == 201
        assert c.post("/api/contact", json=body).status_code == 429
        assert c.post("/api/projects", json={"name": "p"}).status_code == 201


def test_sliding_window_frees_up_and_bounds_its_memory() -> None:
    w = SlidingWindow(limit=2, window=10.0, max_keys=3)
    assert w.retry_after("k", now=0) == 0 and w.retry_after("k", now=1) == 0
    assert w.retry_after("k", now=2) == pytest.approx(8.0)
    assert w.retry_after("k", now=10.5) == 0  # the first event has left the window
    for i in range(10):
        w.retry_after(f"ip{i}", now=20)
    assert len(w._events) <= 3
