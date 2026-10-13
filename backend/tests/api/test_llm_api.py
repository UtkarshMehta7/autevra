"""LLM proposals through the API: never applied without explicit confirmation."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from autevra.config import Settings
from autevra.main import create_app
from tests.ai.fakes import FakeLLM, proposal


@pytest.fixture
def llm() -> FakeLLM:
    return FakeLLM()


@pytest.fixture
def api(tmp_path: Path, llm: FakeLLM) -> Iterator[TestClient]:
    with TestClient(create_app(Settings(data_dir=tmp_path / "d"), llm=llm)) as c:
        yield c


@pytest.fixture
def pid(api: TestClient) -> str:
    return api.post("/api/projects", json={"name": "LLM car"}).json()["id"]


def _say(api: TestClient, pid: str, text: str) -> dict:
    return api.post(f"/api/projects/{pid}/instructions", json={"text": text}).json()


def _wheelbase(api: TestClient, pid: str) -> float:
    return api.get(f"/api/projects/{pid}").json()["values"]["wheelbase"]


def test_proposal_is_not_applied_until_confirmed(api: TestClient, pid: str, llm: FakeLLM) -> None:
    llm.answers.append(proposal(("wheelbase", "increase", 4, "in")))
    reply = _say(api, pid, "stretch the gap between the hubs by four inches")
    assert reply["kind"] == "proposal" and reply["interpreted_by"] == "llm"
    assert reply["preview"] == {"wheelbase": pytest.approx(2801.6)}
    assert _wheelbase(api, pid) == 2700  # nothing applied yet

    confirmed = api.post(f"/api/projects/{pid}/proposals/{reply['proposal_id']}/confirm")
    assert confirmed.status_code == 200
    assert _wheelbase(api, pid) == pytest.approx(2801.6)
    entry = api.get(f"/api/projects/{pid}/history").json()["entries"][0]
    assert entry["command"]["source"] == "llm"
    # A proposal can be used once.
    again = api.post(f"/api/projects/{pid}/proposals/{reply['proposal_id']}/confirm")
    assert again.status_code == 404


def test_rejected_proposal_changes_nothing(api: TestClient, pid: str, llm: FakeLLM) -> None:
    llm.answers.append(proposal(("ground_clearance", "decrease", 20, "mm")))
    reply = _say(api, pid, "slam it 20 mm closer to the tarmac")
    assert reply["kind"] == "proposal"
    url = f"/api/projects/{pid}/proposals/{reply['proposal_id']}"
    assert api.post(f"{url}/reject").status_code == 204
    assert api.post(f"{url}/confirm").status_code == 404
    assert api.get(f"/api/projects/{pid}").json()["values"]["ground_clearance"] == 160


def test_proposal_breaking_a_rule_is_rejected_up_front(
    api: TestClient, pid: str, llm: FakeLLM
) -> None:
    llm.answers.append(proposal(("body_width", "set", 1700, "mm")))
    reply = _say(api, pid, "slim the shell right down to 1700 mm")
    assert reply["kind"] == "rejected" and reply["interpreted_by"] == "llm"
    assert reply["violations"][0]["rule"] == "tyres_within_body"
    assert reply["proposal_id"] is None


def test_proposal_of_another_project_cannot_be_confirmed(
    api: TestClient, pid: str, llm: FakeLLM
) -> None:
    llm.answers.append(proposal(("wheelbase", "increase", 50, "mm")))
    reply = _say(api, pid, "stretch the gap between the hubs by 50 mm")
    other = api.post("/api/projects", json={"name": "Other"}).json()["id"]
    response = api.post(f"/api/projects/{other}/proposals/{reply['proposal_id']}/confirm")
    assert response.status_code == 404


def test_rules_still_apply_directly(api: TestClient, pid: str, llm: FakeLLM) -> None:
    reply = _say(api, pid, "increase the wheelbase by 100 mm")
    assert reply["kind"] == "command" and reply["interpreted_by"] == "rules"
    assert _wheelbase(api, pid) == 2800
    assert llm.calls == []


def test_out_of_scope_and_unmodelled(api: TestClient, pid: str) -> None:
    assert _say(api, pid, "write me a poem about the sea")["kind"] == "out_of_scope"
    reply = _say(api, pid, "make the suspension softer")
    assert reply["kind"] == "clarification" and "rebound damping" in reply["message"]


def test_llm_status(api: TestClient, client: TestClient) -> None:
    assert api.get("/api/llm").json()["available"] is True
    off = client.get("/api/llm").json()
    assert off["provider"] == "off" and off["available"] is False
