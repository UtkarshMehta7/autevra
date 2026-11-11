from fastapi.testclient import TestClient


def test_browse_size_install_and_where_used(client: TestClient, project: str) -> None:
    rows = client.get("/api/inventory", params={"q": "6205"}).json()
    assert [r["id"] for r in rows] == ["bearing-6205"]
    bolts = client.get("/api/inventory", params={"category": "Fasteners", "q": "m10 4762"}).json()
    assert bolts and all(r["family"] == "Socket head cap screw" for r in bolts)
    life = client.post("/api/inventory/items/bearing-6205/bearing-life",
                       json={"load_kN": 1.48, "rpm": 1000}).json()  # fmt: skip
    assert round(life["L10_Mrev"]) == 1000
    assert client.post("/api/inventory/items/iso4032-m10/bearing-life",
                       json={"load_kN": 1, "rpm": 1}).status_code == 422  # fmt: skip
    part = client.post(f"/api/projects/{project}/inventory/install",
                       json={"item": "bearing-6205", "at": {"x": 100}}).json()  # fmt: skip
    assert part["document"]["name"].startswith("6205")
    assert client.get("/api/inventory/items/bearing-6205/usage").json()[0]["project"] == project
    assert client.get("/api/inventory/items/nope").status_code == 404


def test_installs_in_an_aircraft_project_too(client: TestClient) -> None:
    pid = client.post("/api/projects", json={"name": "plane", "domain": "aerospace"}).json()["id"]
    r = client.post(f"/api/projects/{pid}/inventory/install", json={"item": "iso4017-m8x30"})
    assert r.status_code == 200


def test_publish_a_part_as_an_item(client: TestClient, project: str) -> None:
    doc = {"name": "Bracket", "features": [{"id": "b", "type": "box", "size": [100, 50, 10]}]}
    part = client.post(f"/api/projects/{project}/parts", json=doc).json()
    first = client.post(f"/api/projects/{project}/parts/{part['id']}/publish").json()
    again = client.post(f"/api/projects/{project}/parts/{part['id']}/publish").json()
    assert first["version"] == "1.0.0" and again["version"] == "1.1.0"
    assert abs(first["properties"]["mass_kg"] - 100 * 50 * 10 * 7850e-9) < 1e-3
    listed = client.get("/api/inventory", params={"category": "Published"}).json()
    assert [r["version"] for r in listed] == ["1.1.0"]
