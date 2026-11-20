"""Surface laboratory endpoints."""

from fastapi.testclient import TestClient


def grid(nu: int = 4, nv: int = 4) -> list:
    return [[[i * 10.0, j * 10.0, (i - 1.5) ** 2 - (j - 1.5) ** 2] for j in range(nv)]
            for i in range(nu)]  # fmt: skip


def test_evaluate_reports_grid_basis_and_support(client: TestClient) -> None:
    body = {"surface": {"degree_u": 3, "degree_v": 2, "control": grid()}, "samples": 9,
            "selected": [1, 2]}  # fmt: skip
    r = client.post("/api/surfaces/evaluate", json=body)
    assert r.status_code == 200, r.text
    out = r.json()
    assert len(out["grid"]["points"]) == 81 and len(out["grid"]["triangles"]) == 8 * 8 * 6
    assert len(out["basis_u"]["functions"]) == 4 and len(out["basis_v"]["functions"]) == 4
    assert out["support"]["u"] == [0.0, 1.0] and out["support"]["v"] == [0.0, 1.0]
    r = client.post(
        "/api/surfaces/evaluate",
        json={"surface": {"degree_u": 5, "degree_v": 1, "control": grid()}},
    )
    assert r.status_code == 422


def test_knot_insertion_keeps_the_shape(client: TestClient) -> None:
    body = {
        "surface": {"degree_u": 3, "degree_v": 2, "control": grid()},
        "direction": "u",
        "t": 0.4,
    }
    out = client.post("/api/surfaces/insert-knot", json=body).json()
    assert len(out["surface"]["control"]) == 5 and out["max_shape_change"] < 1e-9


def test_a_g2_join_measures_g2(client: TestClient) -> None:
    a = {"degree_u": 3, "degree_v": 2, "control": grid(5, 4)}
    b = client.post("/api/surfaces/join", json={"surface": a, "target": "G2", "bend": 5}).json()[
        "surface"
    ]
    out = client.post("/api/surfaces/continuity", json={"a": a, "b": b}).json()
    assert out["report"]["level"] in ("G2", "G3") and len(out["combs"]) == 6
