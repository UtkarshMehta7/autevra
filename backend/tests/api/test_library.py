"""Project packages, universal duplicate and the design library across modules."""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.cad

BLOCK = {
    "name": "Block",
    "features": [
        {"id": "b", "type": "box", "size": [80, 60, 30], "at": {"z": 15}},
        {
            "id": "h",
            "type": "hole",
            "diameter": 10,
            "through": True,
            "at": {"x": 20, "y": 10, "z": 30},
        },
    ],
}
PIN = {
    "name": "Pin",
    "at": {"x": 200, "z": 40, "rx": 30},
    "features": [{"id": "s", "type": "cylinder", "radius": 5, "height": 50, "at": {"z": -25}}],
}


def test_package_round_trip_keeps_parts_files_and_remaps_ids(client: TestClient):
    pid = client.post("/api/projects", json={"name": "Jig", "domain": "machinery"}).json()["id"]
    block = client.post(f"/api/projects/{pid}/parts", json=BLOCK).json()["id"]
    pin = client.post(f"/api/projects/{pid}/parts", json=PIN).json()["id"]
    client.put(
        f"/api/projects/{pid}/engine/spec",
        json={
            **client.get(f"/api/projects/{pid}/engine/spec").json(),
            "cylinders": 6,
            "name": "I6",
        },
    )
    client.put(
        f"/api/projects/{pid}/mates",
        json={"constraints": [{"id": "f", "kind": "fix", "part": block}]},
    )
    package = client.get(f"/api/projects/{pid}/snapshot").json()
    assert package["format"] == "autevra-project/1" and len(package["parts"]) == 2
    assert {"engines", "assembly"} <= set(package["files"])
    new = client.post("/api/projects/import", json=package).json()
    parts = client.get(f"/api/projects/{new['id']}/parts").json()
    assert sorted(p["document"]["name"] for p in parts) == ["Block", "Pin"]
    assert {p["id"] for p in parts}.isdisjoint({block, pin})
    fixed = client.get(f"/api/projects/{new['id']}/mates").json()["constraints"][0]["part"]
    assert fixed in {p["id"] for p in parts}  # the constraint follows the copied part
    assert client.get(f"/api/projects/{new['id']}/engine/spec").json()["cylinders"] == 6
    bad = client.post("/api/projects/import", json={"format": "other"})
    assert bad.status_code == 422


def test_duplicate_is_complete_in_every_module(client: TestClient):
    pid = client.post("/api/projects", json={"name": "Plane", "domain": "aerospace"}).json()["id"]
    spec = client.get(f"/api/projects/{pid}/aircraft/spec").json()
    client.put(f"/api/projects/{pid}/aircraft/spec", json={**spec, "wing_span": 12.5})
    client.post(f"/api/projects/{pid}/parts", json=BLOCK)
    dup = client.post(f"/api/projects/{pid}/duplicate").json()
    assert dup["domain"] == "aerospace" and dup["name"] == "Plane (copy)"
    assert client.get(f"/api/projects/{dup['id']}/aircraft/spec").json()["wing_span"] == 12.5
    assert len(client.get(f"/api/projects/{dup['id']}/parts").json()) == 1


def test_library_save_use_list_delete(client: TestClient):
    pid = client.post("/api/projects", json={"name": "Boat", "domain": "marine"}).json()["id"]
    entry = client.post(
        "/api/library",
        json={"project_id": pid, "name": "Pilot boat", "description": "11 m", "tags": ["workboat"]},
    ).json()
    assert entry["domain"] == "marine"
    assert [e["name"] for e in client.get("/api/library?domain=marine").json()] == ["Pilot boat"]
    assert client.get("/api/library?domain=aerospace").json() == []
    used = client.post(f"/api/library/{entry['id']}/use").json()
    assert used["name"] == "Pilot boat" and used["domain"] == "marine"
    assert client.delete(f"/api/library/{entry['id']}").status_code == 204
    assert client.post(f"/api/library/{entry['id']}/use").status_code == 404
    assert client.post("/api/library/..%2Fx/use").status_code == 404
