import pytest
from fastapi.testclient import TestClient


def test_vessel_analysis(client: TestClient) -> None:
    out = client.post("/api/marine/analyse", json={}).json()
    assert out["hydrostatics"]["gm_m"] > 0.15 and len(out["gz"]) == 17
    assert all(c["pass"] for c in out["criteria"])
    assert out["resistance"][0]["speed_kn"] < out["resistance"][-1]["speed_kn"]


@pytest.mark.cad
def test_marine_project_build_and_views(client: TestClient) -> None:
    car = client.post("/api/projects", json={"name": "car"}).json()["id"]
    assert client.get(f"/api/projects/{car}/vessel/spec").status_code == 422  # kept apart
    pid = client.post("/api/projects", json={"name": "Boat", "domain": "marine"}).json()["id"]
    parts = client.post(f"/api/projects/{pid}/vessel", json={"twin_shaft": True}).json()
    assert len(parts) == 6 and all(not p["errors"] for p in parts)
    product = client.get(f"/api/projects/{pid}/product").json()
    assert product["module"] == "marine" and product["configuration"]["propulsion"] == "Twin shaft"
    assert client.get(f"/api/projects/{pid}/loads").json()["compliance"][0]["status"] == "shown"
    assert client.get(f"/api/projects/{pid}/manufacturing").json()["plan"]["reconciliation"] == []
    assert client.get(f"/api/projects/{pid}/reviews").json()[0]["gate"] == "Concept review"
