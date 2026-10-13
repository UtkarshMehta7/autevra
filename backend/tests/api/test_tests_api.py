"""Critical path: instruction -> validated command -> simulation -> evaluation -> history."""

import pytest
from fastapi.testclient import TestClient


def _say(client: TestClient, pid: str, text: str) -> dict:
    return client.post(f"/api/projects/{pid}/instructions", json={"text": text}).json()


def test_change_damping_and_test_its_response(client: TestClient, project: str) -> None:
    reply = _say(
        client, project, "Increase the rear shock absorber damping by 10% and test its response."
    )
    assert reply["kind"] == "command"
    values = reply["result"]["values"]
    assert values["rear_damping_bump"] == pytest.approx(1430)
    assert values["rear_damping_rebound"] == pytest.approx(2860)
    # Damping changes the dynamic model, not the geometry; the dependency graph says which
    # tests are now stale.
    impact = reply["result"]["impact"]
    assert impact["rebuild"] == [] and impact["move"] == []
    assert "quarter_car:rear" in impact["retest"]
    # One run per scenario on the new design, each compared with the previous revision.
    assert {r["scenario_id"] for r in reply["runs"]} == {"step_25", "hump_75", "pothole_50"}
    assert all(r["target"] == "rear" and r["history_cursor"] == 1 for r in reply["runs"])
    assert len(reply["comparisons"]) == 3
    hump = next(c for c in reply["comparisons"] if "rear_damping_bump" in c["changed_inputs"])
    bump = next(m for m in hump["metrics"] if m["metric"] == "max_bump_travel")
    assert bump["after"] < bump["before"]  # more bump damping resists compression

    runs = client.get(f"/api/projects/{project}/runs").json()
    assert len(runs) == 6  # three new, three baselines on revision 0
    assert sorted(r["history_cursor"] for r in runs) == [0, 0, 0, 1, 1, 1]
    assert all(r["current"] == (r["history_cursor"] == 1) for r in runs)

    # Undo restores the design, and the baseline results apply again.
    _say(client, project, "undo")
    runs = client.get(f"/api/projects/{project}/runs").json()
    assert all(r["current"] == (r["history_cursor"] == 0) for r in runs)


def test_run_record_is_traceable(client: TestClient, project: str) -> None:
    out = client.post(
        f"/api/projects/{project}/tests/run",
        json={"test_id": "quarter_car", "target": "front", "scenario_id": "hump_75"},
    ).json()
    [run] = out["runs"]
    full = client.get(f"/api/projects/{project}/runs/{run['id']}").json()
    assert full["solver"]["id"] == "autevra.quarter_car" and full["solver"]["version"]
    assert full["credibility"] == "numerical_simulation"
    assert full["numerics"]["converged"] is True
    assert full["inputs"]["front_spring_rate"] == {
        "value": 26,
        "unit": "N/mm",
        "label": "Front spring rate",
    }
    assert full["revision"]["history_cursor"] == 0 and full["revision"]["values_hash"]
    assert full["assumptions"] and len(full["trace"]["t"]) > 100
    bump = next(c for c in full["criteria"] if c["id"] == "bump_travel")
    # The limit comes from the design: the arch gap governs the usable bump travel.
    assert bump["limit"] == 35 and "arch_clearance" in bump["limit_parameters"]
    assert full["status"] == (
        "passed_within_model" if all(c["passed"] for c in full["criteria"]) else "failed"
    )


def test_requirements_join_the_verdict(client: TestClient, project: str) -> None:
    created = client.post(
        f"/api/projects/{project}/requirements",
        json={"metric": "peak_body_acceleration", "comparator": "<=", "limit": 1.0, "unit": "m/s²"},
    )
    assert created.status_code == 201
    out = client.post(
        f"/api/projects/{project}/tests/run",
        json={"target": "front", "scenario_id": "step_25"},
    ).json()
    [run] = out["runs"]
    user = [c for c in run["criteria"] if c["source"] == "user"]
    assert len(user) == 1 and user[0]["passed"] is False and run["status"] == "failed"
    bad = client.post(
        f"/api/projects/{project}/requirements",
        json={"metric": "warp_speed", "comparator": "<=", "limit": 1},
    )
    assert bad.status_code == 422


def test_component_status_tracks_staleness(client: TestClient, project: str) -> None:
    def status(cid: str) -> str:
        rows = client.get(f"/api/projects/{project}/components/status").json()
        return next(r["status"] for r in rows if r["component"] == cid)

    assert status("damper_rl") == "not_tested"
    client.post(f"/api/projects/{project}/tests/run", json={"target": "all"})
    client.post(
        f"/api/projects/{project}/tests/run", json={"test_id": "ride_modes", "target": "all"}
    )
    assert status("damper_rl") in ("passed_within_model", "failed")
    _say(client, project, "increase the rear spring rate by 2 N/mm")
    assert status("damper_rl") == "stale"
    assert status("damper_fl") != "stale"  # the front tests do not read rear parameters


def test_test_requests_without_a_change(client: TestClient, project: str) -> None:
    reply = _say(client, project, "run a quarter-car test on the front over a pothole")
    assert reply["kind"] == "test" and len(reply["runs"]) == 1
    assert reply["runs"][0]["scenario_id"] == "pothole_50"
    assert reply["comparisons"] == []  # no earlier revision to compare with


def test_unknown_test_inputs_are_rejected(client: TestClient, project: str) -> None:
    url = f"/api/projects/{project}/tests/run"
    assert client.post(url, json={"target": "middle"}).status_code == 422
    assert client.post(url, json={"target": "front", "scenario_id": "moon"}).status_code == 422
    assert client.get(f"/api/projects/{project}/runs/nope").status_code == 404


def test_integration_report(client: TestClient, project: str) -> None:
    report = client.get(f"/api/projects/{project}/integration").json()
    assert report["counts"].get("fail", 0) == 0
    assert {c["kind"] for c in report["checks"]} >= {
        "interface",
        "connectivity",
        "coincidence",
        "load_path",
        "travel",
        "clearance",
    }
    assert report["not_checked"]


def test_test_catalogue(client: TestClient) -> None:
    tests = {t["id"]: t for t in client.get("/api/tests").json()}
    assert set(tests) == {"quarter_car", "ride_modes"}
    assert tests["ride_modes"]["criteria"] == []  # no invented pass/fail limits
    assert "front_damping_bump" in tests["quarter_car"]["inputs"]["front"]


def test_diagnose_then_fix_then_retest(client: TestClient, project: str) -> None:
    _say(client, project, "test the rear over the hump")
    reply = _say(client, project, "explain why the suspension travel limit was exceeded")
    assert reply["kind"] == "diagnosis" and reply["diagnosis"]["current"] is True
    finding = reply["diagnosis"]["findings"][0]
    assert finding["criterion"] == "bump_travel"
    fix = next(f for f in finding["fixes"] if not f["rule_violations"] and not f["breaks"])
    applied = client.post(f"/api/projects/{project}/commands", json={"command": fix["command"]})
    assert applied.status_code == 200 and applied.json()["changed"] == [fix["parameter"]]
    retest = _say(client, project, "test the rear over the hump")
    assert retest["runs"][0]["status"] == "passed_within_model"
    assert retest["comparisons"][0]["criteria"][0]["before"] is False


def test_diagnose_without_failures_asks_for_a_test(client: TestClient, project: str) -> None:
    reply = _say(client, project, "why did the front test fail?")
    assert reply["kind"] == "clarification" and "Run a test first" in reply["message"]
