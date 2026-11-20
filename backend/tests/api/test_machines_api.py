"""Electric machines and gas turbines in the Mechanical module."""

import pytest
from fastapi.testclient import TestClient


def test_motor_and_turbine_analysis(client: TestClient) -> None:
    m = client.post("/api/motors/analyse", json={}).json()
    assert m["peak_power_kw"] > 100 and 0.95 < m["peak_efficiency"] < 0.99
    t = client.post("/api/turbines/analyse", json={"kind": "turboshaft"}).json()
    assert t["shaft_power_kw"] > 0 and t["mass_kg"] > 0
    assert client.post("/api/turbines/analyse",
                       json={"tit_k": 900, "pressure_ratio": 40}).status_code == 422  # fmt: skip


@pytest.mark.cad
def test_electric_project_publish_and_install_makes_a_bev(client: TestClient,
                                                          project: str) -> None:  # fmt: skip
    pid = client.post("/api/projects", json={"name": "m", "domain": "machinery"}).json()["id"]
    assert client.get(f"/api/projects/{pid}/engine/category").json()["category"] == "piston"
    client.put(f"/api/projects/{pid}/engine/category", json={"category": "electric"})
    client.put(f"/api/projects/{pid}/motor/spec", json={"name": "Rear motor"})
    parts = client.post(f"/api/projects/{pid}/machine").json()
    assert len(parts) == 4 and all(not p["errors"] for p in parts)
    product = client.get(f"/api/projects/{pid}/product").json()
    assert "stator_core" in {c["template"] for s in product["breakdown"]["children"]
                             for c in s["children"]}  # fmt: skip
    systems = client.get(f"/api/projects/{pid}/systems").json()
    assert not [i for i in systems["issues"] if i["severity"] == "fail"]
    item = client.post(f"/api/projects/{pid}/motor/publish").json()
    assert item["family"] == "Electric machine"
    refused = client.post(f"/api/projects/{project}/install-engine", json={"item": item["id"]})
    assert refused.status_code == 422 and "skateboard" in refused.json()["detail"]  # rules hold
    client.post(f"/api/projects/{project}/commands", json={"command": {"changes": [
        {"parameter": "chassis_type", "operation": "set", "value": 2}]}})  # fmt: skip
    client.post(f"/api/projects/{project}/install-engine", json={"item": item["id"]})
    values = client.get(f"/api/projects/{project}").json()["values"]
    assert values["powertrain_type"] == 2  # battery electric on a skateboard platform


@pytest.mark.cad
def test_turbine_project(client: TestClient) -> None:
    pid = client.post("/api/projects", json={"name": "t", "domain": "machinery"}).json()["id"]
    client.put(f"/api/projects/{pid}/engine/category", json={"category": "turbine"})
    parts = client.post(f"/api/projects/{pid}/machine").json()
    assert len(parts) == 3 and all(not p["errors"] for p in parts)
    product = client.get(f"/api/projects/{pid}/product").json()
    assert product["configuration"] == {"kind": "Turbojet"}
    loads = client.get(f"/api/projects/{pid}/loads").json()
    assert loads["cases"][0]["id"] == "thrust"
    assert client.get(f"/api/projects/{pid}/manufacturing").json()["plan"]["reconciliation"] == []
    ecr = client.post(f"/api/projects/{pid}/changes", json={
        "title": "hotter", "changes": {"tit_k": 1500}}).json()  # fmt: skip
    client.post(f"/api/projects/{pid}/changes/{ecr['id']}/approve")
    assert client.get(f"/api/projects/{pid}/turbine/spec").json()["tit_k"] == 1500
