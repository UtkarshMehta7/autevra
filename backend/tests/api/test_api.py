"""HTTP API, including the Phase 1 acceptance test."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from autevra.cad import kernel

pytestmark = pytest.mark.cad


def _instruct(client: TestClient, project: str, text: str) -> dict:
    response = client.post(f"/api/projects/{project}/instructions", json={"text": text})
    assert response.status_code == 200, response.text
    return response.json()


def _model(client: TestClient, project: str) -> dict:
    response = client.get(f"/api/projects/{project}/model")
    assert response.status_code == 200
    return response.json()


def _translation(model: dict, part_id: str) -> list[float]:
    part = next(p for p in model["parts"] if p["id"] == part_id)
    return [row[3] for row in part["matrix"][:3]]


def _body_x_extent(model: dict) -> tuple[float, float]:
    body = next(p for p in model["parts"] if p["id"] == "body")
    xs = model["geometries"][body["geometry"]]["vertices"][0::3]
    return min(xs), max(xs)


def _step_x_extent(client: TestClient, project: str, tmp_path: Path) -> tuple[float, float]:
    response = client.get(f"/api/projects/{project}/export.step")
    assert response.status_code == 200
    assert response.headers["content-disposition"].endswith('Test-car.step"')
    path = tmp_path / "export.step"
    path.write_bytes(response.content)
    lo, hi = kernel.bounds(kernel.import_step(path))
    return lo[0], hi[0]


def test_acceptance_increase_wheelbase_by_100_mm(
    client: TestClient, project: str, tmp_path: Path
) -> None:
    before = _model(client, project)
    step_before = _step_x_extent(client, project, tmp_path)

    reply = _instruct(client, project, "increase the wheelbase by 100 mm")
    assert reply["kind"] == "command"
    assert reply["result"]["values"]["wheelbase"] == 2800
    assert set(reply["result"]["impact"]["rebuild"]) == {"body", "frame"}
    rear_group = {"rear_axle", "wheel_rl", "wheel_rr", "damper_rl", "damper_rr"}
    assert set(reply["result"]["impact"]["move"]) == rear_group

    after = _model(client, project)
    # Rear axle, rear wheels and rear dampers move back by 100 mm; the front ones stay.
    for part in rear_group:
        assert _translation(after, part)[0] == pytest.approx(_translation(before, part)[0] - 100)
    for part in ("front_axle", "wheel_fl", "wheel_fr", "damper_fl", "damper_fr"):
        assert _translation(after, part) == pytest.approx(_translation(before, part))
    # The body lengthens by 100 mm at the rear.
    (b0, b1), (a0, a1) = _body_x_extent(before), _body_x_extent(after)
    assert a1 - a0 == pytest.approx(b1 - b0 + 100, abs=0.01)
    assert a1 == pytest.approx(b1, abs=0.01)
    # The STEP export reflects it.
    step_after = _step_x_extent(client, project, tmp_path)
    assert step_after[0] == pytest.approx(step_before[0] - 100, abs=0.01)
    assert step_after[1] == pytest.approx(step_before[1], abs=0.01)

    # Undo restores 2700 mm, the geometry and the export.
    reply = _instruct(client, project, "undo")
    assert reply["kind"] == "undo"
    assert client.get(f"/api/projects/{project}").json()["values"]["wheelbase"] == 2700
    restored = _model(client, project)
    assert _translation(restored, "wheel_rl") == pytest.approx(_translation(before, "wheel_rl"))
    assert _step_x_extent(client, project, tmp_path) == pytest.approx(step_before, abs=0.01)


def test_model_deduplicates_and_skips_known_geometry(client: TestClient, project: str) -> None:
    model = _model(client, project)
    assert len(model["parts"]) == 12
    assert len(model["geometries"]) == 6  # body, frame, axle, wheel, front and rear damper
    keys = ",".join(model["geometries"])
    partial = client.get(f"/api/projects/{project}/model", params={"known": keys}).json()
    assert partial["geometries"] == {}
    assert len(partial["parts"]) == 12


def test_typed_command_endpoint_and_rejection(client: TestClient, project: str) -> None:
    ok = client.post(
        f"/api/projects/{project}/commands",
        json={
            "command": {
                "changes": [{"parameter": "ground_clearance", "operation": "set", "value": 180}],
                "source": "ui",
            }
        },
    )
    assert ok.status_code == 200
    assert ok.json()["values"]["ground_clearance"] == 180

    bad = client.post(
        f"/api/projects/{project}/commands",
        json={
            "command": {"changes": [{"parameter": "body_width", "operation": "set", "value": 1700}]}
        },
    )
    assert bad.status_code == 422
    assert bad.json()["violations"][0]["rule"] == "tyres_within_body"

    unknown = client.post(
        f"/api/projects/{project}/commands",
        json={"command": {"changes": [{"parameter": "colour", "operation": "set", "value": 1}]}},
    )
    assert unknown.status_code == 422


def test_instruction_rejected_by_rules(client: TestClient, project: str) -> None:
    reply = _instruct(client, project, "set the body width to 1700 mm")
    assert reply["kind"] == "rejected"
    assert reply["violations"][0]["rule"] == "tyres_within_body"
    assert client.get(f"/api/projects/{project}").json()["values"]["body_width"] == 1820


def test_query_and_clarification(client: TestClient, project: str) -> None:
    reply = _instruct(client, project, "how long is the car?")
    assert reply["kind"] == "query"
    assert reply["answer"] == {"overall_length": 4600}
    assert reply["message"] == "Overall length: 4600.0 mm"
    reply = _instruct(client, project, "make it longer")
    assert reply["kind"] == "clarification"
    assert reply["suggestions"]


def test_undo_redo_endpoints_and_history(client: TestClient, project: str) -> None:
    _instruct(client, project, "lower the car by 20 mm")
    assert client.post(f"/api/projects/{project}/undo").json()["values"]["ground_clearance"] == 160
    assert client.post(f"/api/projects/{project}/redo").json()["values"]["ground_clearance"] == 140
    history = client.get(f"/api/projects/{project}/history").json()
    assert history["cursor"] == 1
    assert history["entries"][0]["command"]["instruction"] == "lower the car by 20 mm"
    nothing = _instruct(client, project, "redo")
    assert nothing["message"] == "Nothing to redo."


def test_project_crud_and_404(client: TestClient) -> None:
    created = client.post("/api/projects", json={"name": "A"}).json()
    assert created["values"]["wheelbase"] == 2700
    assert any(d["id"] == "overall_length" and d["value"] == 4600 for d in created["derived"])
    assert client.patch(f"/api/projects/{created['id']}", json={"name": "B"}).json()["name"] == "B"
    assert [p["name"] for p in client.get("/api/projects").json()] == ["B"]
    assert client.delete(f"/api/projects/{created['id']}").status_code == 204
    assert client.get(f"/api/projects/{created['id']}").status_code == 404


def test_catalogue(client: TestClient) -> None:
    body = client.get("/api/parameters").json()
    ids = [p["id"] for p in body["parameters"]]
    assert "wheelbase" in ids and "rear_damping_rebound" in ids and len(ids) == 48


def test_state_survives_app_restart(tmp_path: Path) -> None:
    from autevra.config import Settings
    from autevra.main import create_app

    settings = Settings(data_dir=tmp_path / "data", llm_provider="off")
    with TestClient(create_app(settings)) as c:
        pid = c.post("/api/projects", json={"name": "Persist"}).json()["id"]
        _instruct(c, pid, "increase the wheelbase by 100 mm")
    with TestClient(create_app(settings)) as c:
        state = c.get(f"/api/projects/{pid}").json()
        assert state["values"]["wheelbase"] == 2800 and state["can_undo"]
        _instruct(c, pid, "undo")
        assert c.get(f"/api/projects/{pid}").json()["values"]["wheelbase"] == 2700
