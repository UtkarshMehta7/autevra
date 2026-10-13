from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import autevra.domains.automotive  # noqa: F401  (registers the built-in domain)
from autevra.config import Settings
from autevra.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    settings = Settings(data_dir=tmp_path / "data", llm_provider="off", plugin_entry_points=False)
    with TestClient(create_app(settings)) as c:
        yield c


@pytest.fixture
def project(client: TestClient) -> str:
    return client.post("/api/projects", json={"name": "Test car"}).json()["id"]
