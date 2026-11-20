"""Review gates, baselines and engineering change on every module."""

from fastapi.testclient import TestClient


def test_gates_are_computed_from_the_model(client: TestClient, project: str) -> None:
    gates = client.get(f"/api/projects/{project}/reviews").json()
    assert [g["gate"] for g in gates] == [
        "Concept review",
        "Preliminary review",
        "Critical review",
        "Verification",
        "Release",
    ]
    concept = gates[0]
    assert all("criterion" in c and "detail" in c for c in concept["criteria"])
    assert gates[-1]["passed"] is False  # nothing released yet


def test_baseline_compare_and_change_order(client: TestClient, project: str) -> None:
    bl = client.post(f"/api/projects/{project}/baselines",
                     json={"name": "Concept freeze", "gate": "Concept review"}).json()  # fmt: skip
    assert bl["id"] == "BL-001" and bl["mass_kg"] > 0
    ecr = client.post(f"/api/projects/{project}/changes", json={
        "title": "Longer wheelbase for rear legroom", "reason": "packaging",
        "changes": {"wheelbase": 2800}}).json()  # fmt: skip
    assert ecr["id"] == "ECR-001" and ecr["status"] == "open"
    assert ecr["impact"]["values"]["wheelbase"] == [2700.0, 2800]
    assert ecr["impact"]["mass_kg"] > 0  # a longer car is heavier
    # nothing applied before the decision
    assert client.get(f"/api/projects/{project}").json()["values"]["wheelbase"] == 2700
    done = client.post(f"/api/projects/{project}/changes/ECR-001/approve").json()
    assert done["status"] == "approved" and done["eco"] == "ECO-001"
    assert client.get(f"/api/projects/{project}").json()["values"]["wheelbase"] == 2800
    history = client.get(f"/api/projects/{project}/history").json()["entries"]
    assert history[-1]["command"]["instruction"].startswith("ECO-001")
    assert client.post(f"/api/projects/{project}/changes/ECR-001/reject").status_code == 409
    diff = client.get(f"/api/projects/{project}/baselines/BL-001/compare").json()
    assert diff["values"]["wheelbase"] == [2700.0, 2800.0]
    assert client.post(f"/api/projects/{project}/changes", json={
        "title": "x", "changes": {"no_such_value": 1}}).status_code == 422  # fmt: skip


def test_change_on_an_engine_project(client: TestClient) -> None:
    pid = client.post("/api/projects", json={"name": "e", "domain": "machinery"}).json()["id"]
    ecr = client.post(f"/api/projects/{pid}/changes", json={
        "title": "Bigger bore", "changes": {"bore": 90}}).json()  # fmt: skip
    assert ecr["impact"]["mass_kg"] > 0
    client.post(f"/api/projects/{pid}/changes/{ecr['id']}/approve")
    assert client.get(f"/api/projects/{pid}/engine/spec").json()["bore"] == 90
