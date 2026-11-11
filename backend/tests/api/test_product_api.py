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


def test_systems_view_and_requirement_allocation(client: TestClient, project: str) -> None:
    client.post(f"/api/projects/{project}/instructions",
                json={"text": "require the ground clearance to be at least 150 mm"})  # fmt: skip
    out = client.get(f"/api/projects/{project}/systems").json()
    assert out["module"] == "land" and len(out["functions"]) > 10
    assert any(i["kind"] == "unallocated_requirement" for i in out["issues"])
    key = out["requirements"][0]["key"]
    r = client.put(f"/api/projects/{project}/systems/allocations",
                   json={"requirement": key, "function": "ride"})  # fmt: skip
    assert r.status_code == 200 and r.json() == {key: "ride"}
    out = client.get(f"/api/projects/{project}/systems").json()
    assert not any(i["kind"] == "unallocated_requirement" for i in out["issues"])
    ride = next(f for f in out["functions"] if f["id"] == "ride")
    assert key in ride["requirements"]
    bad = client.put(f"/api/projects/{project}/systems/allocations",
                     json={"requirement": key, "function": "fly"})  # fmt: skip
    assert bad.status_code == 422
    steps = client.get(f"/api/projects/{project}/systems/chain/decelerate").json()
    assert [s["block"] for s in steps][0] == "driver"


def test_loads_and_materials_for_each_module(client: TestClient, project: str) -> None:
    land = client.get(f"/api/projects/{project}/loads").json()
    assert {c["id"] for c in land["cases"]} == {"bump", "braking", "cornering", "pothole"}
    assert any("R13-H" in r["clause"] for r in land["compliance"])
    plane = client.post("/api/projects", json={"name": "p", "domain": "aerospace"}).json()["id"]
    air = client.get(f"/api/projects/{plane}/loads").json()
    assert air["envelope"]["n_pos"] == 3.8 and any(c["id"] == "landing" for c in air["cases"])
    engine = client.post("/api/projects", json={"name": "e", "domain": "machinery"}).json()["id"]
    assert client.get(f"/api/projects/{engine}/loads").json()["cases"][0]["id"] == "firing"
    mats = client.get("/api/materials").json()
    assert {"s355", "2024_t3", "ti6al4v"} <= {m["id"] for m in mats}


def test_manufacturing_plan_and_stackup_api(client: TestClient, project: str) -> None:
    out = client.get(f"/api/projects/{project}/manufacturing").json()
    assert out["plan"]["takt_s"] == 60 and out["plan"]["reconciliation"] == []
    assert {s["name"] for s in out["plan"]["stations"]} >= {"Body shop", "Trim"}
    assert out["stackups"][0]["result"]["worst_case_ok"] is False  # door gap: RSS only
    plane = client.post("/api/projects", json={"name": "p", "domain": "aerospace"}).json()["id"]
    assert client.get(f"/api/projects/{plane}/manufacturing").json()["plan"]["takt_s"] == 14400
    r = client.post("/api/quality/stackup", json={"name": "s", "contributors": [
        {"name": "a", "nominal": 5, "plus": 0.1, "minus": 0.1}]}).json()  # fmt: skip
    assert r["worst_case"] == [4.9, 5.1]
