"""Structures endpoints."""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.cad


def test_a_demo_cantilever_runs_and_reports_its_numbers(client: TestClient) -> None:
    body = {"demo": "cantilever", "element": "hex8", "size": 10, "supports": ["x-min"],
            "loads": [{"region": "x-max", "force": [0, 0, -1000]}]}  # fmt: skip
    r = client.post("/api/structures/run", json=body)
    assert r.status_code == 200, r.text
    out = r.json()
    s = out["stats"]
    assert s["cg_converged"] and s["equilibrium_error"] < 1e-6
    assert s["k_shape"][0] == 3 * out["mesh"]["stats"]["nodes"]
    assert len(out["fields"]["von_mises"]) == len(out["mesh"]["nodes"])
    assert s["factor_of_safety"] > 0 and out["assumptions"]


def test_bad_requests_are_refused(client: TestClient) -> None:
    r = client.post("/api/structures/run", json={"demo": "cantilever", "supports": []})
    assert r.status_code == 422
    assert client.post("/api/structures/run", json={"demo": "nope"}).status_code == 422
    assert client.get("/api/structures/catalogue").json()["regions"][0] == "x-min"


def test_topology_optimisation_runs_and_reports_its_history(client: TestClient) -> None:
    body = {"case": "cantilever", "nx": 30, "ny": 10, "volfrac": 0.4, "max_iter": 20}
    r = client.post("/api/structures/topology", json=body)
    assert r.status_code == 200, r.text
    out = r.json()
    assert len(out["density"]) == 300 and out["snapshots"][-1] and out["equations"]
    assert out["history"][-1]["compliance"] < out["history"][0]["compliance"]
    assert client.get("/api/structures/topology/catalogue").json()["cases"]["mbb"]
    too_big = client.post("/api/structures/topology", json={**body, "ny": 20, "nz": 30})
    assert too_big.status_code == 422
