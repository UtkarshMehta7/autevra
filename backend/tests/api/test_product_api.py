import json

from fastapi.testclient import TestClient


def test_land_product_breakdown_and_configuration(client: TestClient, project: str) -> None:
    out = client.get(f"/api/projects/{project}/product").json()
    assert out["module"] == "land" and out["templates"] > 60
    assert out["breakdown"]["rollup"]["parts"] > 40
    assert {f["id"] for f in out["families"]} >= {"powertrain", "engine", "tow_bar"}
    ev = client.get(
        f"/api/projects/{project}/product",
        params={"config": json.dumps({"powertrain": "Battery electric"})},
    ).json()
    assert ev["configuration"]["powertrain"] == "Battery electric"
    assert "engine" not in ev["configuration"]
    assert ev["design_configuration"]["powertrain"] == "Combustion"  # the design is unchanged
    bad = client.get(f"/api/projects/{project}/product", params={"config": '{"x": "y"}'})
    assert bad.status_code == 422
    rule = client.get(
        f"/api/projects/{project}/product",
        params={"config": json.dumps({"powertrain": "Hybrid", "engine": "V8"})},
    )
    assert rule.json()["violations"]


def test_aircraft_product_is_its_own_module(client: TestClient) -> None:
    pid = client.post("/api/projects", json={"name": "plane", "domain": "aerospace"}).json()["id"]
    out = client.get(f"/api/projects/{pid}/product").json()
    assert out["module"] == "aircraft" and out["breakdown"]["code"] == "Aircraft"
    codes = {c["code"] for c in out["breakdown"]["children"]}
    assert {"ATA 53", "ATA 57", "ATA 32"} <= codes
    env = client.get(f"/api/projects/{pid}/product/envelope").json()
    assert env["configurations"] >= 4 and env["mass_min"] <= env["mass_max"]
