import pytest
from fastapi.testclient import TestClient


def test_engine_analysis(client: TestClient) -> None:
    out = client.post("/api/engines/analyse", json={"cylinders": 6}).json()
    assert out["balance"]["primary_moment"] < 1e-9 and out["displacement_l"] > 2.9
    assert client.post("/api/engines/analyse",
                       json={"layout": "V", "cylinders": 5}).status_code == 422  # fmt: skip


@pytest.mark.cad
def test_engine_project_build_publish_and_breakdown(client: TestClient) -> None:
    car = client.post("/api/projects", json={"name": "car"}).json()["id"]
    assert client.get(f"/api/projects/{car}/engine/spec").status_code == 422  # kept apart
    pid = client.post("/api/projects", json={"name": "V8", "domain": "machinery"}).json()["id"]
    spec = {
        "name": "V8",
        "layout": "V",
        "cylinders": 8,
        "bore": 92,
        "stroke": 93,
        "turbo": True,
        "bmep_max": 20,
        "rpm_peak_torque": 3000,
        "rpm_max": 6500,
    }
    parts = client.post(f"/api/projects/{pid}/engine", json=spec).json()
    assert len(parts) == 9 and all(not p["errors"] for p in parts)  # incl. the turbo
    spec["turbo"] = False
    again = client.post(f"/api/projects/{pid}/engine", json=spec).json()
    assert len(again) == 8  # the turbo part removed
    names = [p["document"]["name"] for p in client.get(f"/api/projects/{pid}/parts").json()]
    assert len(names) == 8 and not any("turbo" in n for n in names)
    item = client.post(f"/api/projects/{pid}/engine/publish").json()
    assert item["category"] == "Engines" and item["version"] == "1.0.0"
    assert {p["kind"] for p in item["ports"]} == {"mechanical.shaft", "mechanical.mount"}
    assert len(item["maps"]["torque_curve"]) > 20
    product = client.get(f"/api/projects/{pid}/product").json()
    assert product["module"] == "mechanical" and product["breakdown"]["rollup"]["parts"] > 30
    systems = client.get(f"/api/projects/{pid}/systems").json()
    assert not [i for i in systems["issues"] if i["severity"] == "fail"]
    # the published engine is an inventory item any module can find
    listed = client.get("/api/inventory", params={"category": "Engines"}).json()
    assert [r["id"] for r in listed] == [item["id"]]
