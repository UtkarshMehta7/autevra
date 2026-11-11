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
