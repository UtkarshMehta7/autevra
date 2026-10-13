import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

import autevra.domains.automotive  # noqa: F401  (registers the built-in domain)
from autevra.config import Settings, normalise_database_url
from autevra.main import create_app

# Set to run the suite against Postgres, e.g.
# AUTEVRA_TEST_DATABASE_URL=postgresql://localhost/autevra_test uv run pytest
TEST_DATABASE_URL = os.environ.get("AUTEVRA_TEST_DATABASE_URL", "")


@pytest.fixture(autouse=True)
def _test_database(monkeypatch: pytest.MonkeyPatch) -> None:
    """With a Postgres test URL, every app in a test uses it, starting from an empty schema."""
    if not TEST_DATABASE_URL:
        return
    url = normalise_database_url(TEST_DATABASE_URL)
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    engine.dispose()
    monkeypatch.setenv("AUTEVRA_DATABASE_URL", url)


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    settings = Settings(data_dir=tmp_path / "data", llm_provider="off", plugin_entry_points=False)
    with TestClient(create_app(settings)) as c:
        yield c


@pytest.fixture
def project(client: TestClient) -> str:
    return client.post("/api/projects", json={"name": "Test car"}).json()["id"]
