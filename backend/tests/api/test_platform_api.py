"""Endpoints for the website, workspace and studio views: domains, projects, system, rules."""

from fastapi.testclient import TestClient


def test_domain_registry_is_honest(client: TestClient) -> None:
    domains = {d["id"]: d for d in client.get("/api/domains").json()}
    assert domains["automotive"]["status"] == "available"
    assert "suspension" in domains["automotive"]["component_library"]
    assert any("Quarter-car" in s for s in domains["automotive"]["simulations"])
    air = domains["aerospace"]  # the aircraft module: usable, partially tested
    assert air["status"] == "experimental" and any("lifting-line" in s for s in air["simulations"])
    assert domains["machinery"]["status"] == "experimental"  # the Mechanical module
    assert domains["marine"]["status"] == "experimental"  # the Marine module
    done = ("automotive", "aerospace", "machinery", "marine")
    others = [d for k, d in domains.items() if k not in done]
    assert len(others) == 5 and all(d["status"] == "unavailable" for d in others)
    assert all(d["simulations"] == [] for d in others)


def test_projects_only_in_available_domains(client: TestClient) -> None:
    ok = client.post("/api/projects", json={"name": "car", "domain": "automotive"})
    assert ok.status_code == 201 and ok.json()["domain"] == "automotive"
    plane = client.post("/api/projects", json={"name": "plane", "domain": "aerospace"})
    assert plane.status_code == 201 and plane.json()["domain"] == "aerospace"
    refused = client.post("/api/projects", json={"name": "rover", "domain": "space"})
    assert refused.status_code == 409
    assert client.post("/api/projects", json={"name": "x", "domain": "nope"}).status_code == 409


def test_duplicate_copies_the_design_and_requirements(client: TestClient, project: str) -> None:
    client.post(f"/api/projects/{project}/instructions",
                json={"text": "increase the wheelbase by 100 mm"})  # fmt: skip
    client.post(f"/api/projects/{project}/instructions",
                json={"text": "require the ground clearance to be at least 150 mm"})  # fmt: skip
    copy = client.post(f"/api/projects/{project}/duplicate").json()
    assert copy["values"]["wheelbase"] == 2800 and copy["history_length"] == 0
    assert copy["name"].endswith("(copy)")
    reqs = client.get(f"/api/projects/{copy['id']}/requirements").json()
    assert [r["requirement"]["key"] for r in reqs] == ["REQ-001"]


def test_system_graph_and_rule_status(client: TestClient, project: str) -> None:
    graph = client.get(f"/api/projects/{project}/system").json()
    ids = {n["id"] for n in graph["nodes"]}
    assert {"vehicle", "body", "damper_rl"} <= ids
    kinds = {e["kind"] for e in graph["edges"]}
    assert kinds == {"mounted_to", "coincident", "load_path"}
    axle = next(n for n in graph["nodes"] if n["id"] == "rear_axle")
    hub = next(i for i in axle["interfaces"] if i["name"] == "hub_left")
    assert hub["used_by"] == ["wheel_rl", "rim_rl", "rotor_rl", "caliper_rl"]
    rules = client.get(f"/api/projects/{project}/rules").json()
    assert all(r["passed"] for r in rules) and len(rules) > 20


def test_run_index_and_contact(client: TestClient, project: str) -> None:
    client.post(
        f"/api/projects/{project}/tests/run", json={"target": "rear", "scenario_id": "step_25"}
    )
    runs = client.get("/api/runs").json()
    assert runs and runs[0]["project_id"] == project and runs[0]["project_name"]
    body = {"name": "A", "email": "a@example.com", "topic": "early_access", "message": "hello"}
    sent = client.post("/api/contact", json=body)
    assert sent.status_code == 201 and sent.json()["stored"] and not sent.json()["delivered"]
    bad = client.post("/api/contact", json={"name": "A", "email": "nope", "message": "x"})
    assert bad.status_code == 422


def test_land_vehicle_tools_refuse_other_modules(client: TestClient) -> None:
    """Modules are kept apart: an aircraft project cannot take a wheelbase, a suspension test
    or a vehicle specification."""
    pid = client.post("/api/projects", json={"name": "plane", "domain": "aerospace"}).json()["id"]
    calls = [
        ("post", "instructions", {"text": "increase the wheelbase by 100 mm"}),
        ("post", "commands",
         {"command": {"changes": [{"parameter": "wheelbase", "operation": "set", "value": 2800}]}}),
        ("post", "tests/run", {"target": "rear", "scenario_id": "step_25"}),
        ("get", "rules", None), ("get", "system", None), ("get", "spec", None),
        ("get", "package", None), ("get", "bom", None), ("get", "integration", None),
    ]  # fmt: skip
    for method, path, body in calls:
        url = f"/api/projects/{pid}/{path}"
        r = client.post(url, json=body) if method == "post" else client.get(url)
        assert r.status_code == 422, path
        assert "Land vehicles tool" in r.json()["detail"], path
    # shared and aircraft tools still answer
    assert client.get(f"/api/projects/{pid}/history").status_code == 200
    assert client.get(f"/api/projects/{pid}/product").status_code == 200
    assert client.get(f"/api/projects/{pid}/aircraft/spec").status_code == 200
