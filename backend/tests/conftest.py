from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from autevra.config import Settings
from autevra.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    settings = Settings(data_dir=tmp_path / "data")
    with TestClient(create_app(settings)) as c:
        yield c


@pytest.fixture
def project(client: TestClient) -> str:
    return client.post("/api/projects", json={"name": "Test car"}).json()["id"]
