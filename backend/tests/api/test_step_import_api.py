"""STEP import: a part from a supplier file, published with picked interfaces."""

from pathlib import Path

import cadquery as cq
import numpy as np
import pytest
from fastapi.testclient import TestClient

from autevra.cad import kernel


@pytest.mark.cad
def test_import_publish_add_port_and_install(client: TestClient, project: str,
                                             tmp_path: Path) -> None:  # fmt: skip
    solid = cq.Workplane().box(40, 40, 10).faces(">Z").hole(10).val()
    step = kernel.export_step([kernel.Part("bracket", solid, np.eye(4), (0.5, 0.5, 0.5))],
                              tmp_path / "bracket.step", schema="AP242")  # fmt: skip
    part = client.post(f"/api/projects/{project}/import-step", params={"name": "Bracket"},
                       content=step.read_bytes()).json()  # fmt: skip
    assert part["document"]["features"][0]["type"] == "imported" and not part["errors"]
    vol = list(part["topology"].values())[-1]["volume"]
    assert vol == pytest.approx(40 * 40 * 10 - np.pi * 25 * 10, rel=1e-3)
    bad = client.post(f"/api/projects/{project}/import-step", content=b"not a step file")
    assert bad.status_code == 422
    item = client.post(f"/api/projects/{project}/parts/{part['id']}/publish").json()
    port = {
        "name": "bolt_hole",
        "kind": "mechanical.bore",
        "at": {"z": 5},
        "attributes": {"diameter": 10.5},
    }
    v2 = client.post(f"/api/inventory/items/{item['id']}/ports", json=port).json()
    assert v2["version"] == "1.1.0" and v2["ports"][0]["name"] == "bolt_hole"
    # the imported item now installs and mates like any other: an M10 bolt through the hole
    placed = client.post(f"/api/projects/{project}/inventory/install",
                         json={"item": item["id"]}).json()  # fmt: skip
    bolt = client.post(f"/api/projects/{project}/inventory/install", json={
        "item": "iso4017-m10x40",
        "mate": {"part": placed["id"], "port": "bolt_hole", "own_port": "thread"}})  # fmt: skip
    assert bolt.status_code == 200, bolt.text


@pytest.mark.cad
def test_mechanism_endpoints_sweep_and_envelope(client: TestClient, project: str,
                                                tmp_path: Path) -> None:  # fmt: skip
    links = {"ground": 100, "crank": 30, "coupler": 90, "rocker": 70}
    fb = client.post("/api/mechanisms/fourbar", json=links).json()
    assert fb["class"] == "crank-rocker" and fb["full_rotation"]
    sc = client.post("/api/mechanisms/slider-crank", json={"crank": 40, "rod": 140}).json()
    assert sc["stroke_mm"] == pytest.approx(80)
    assert client.post("/api/mechanisms/slider-crank",
                       json={"crank": 40, "rod": 30}).status_code == 422  # fmt: skip

    box = cq.Workplane().box(10, 10, 10).val()
    ids = []
    for name, x in (("Block", 0.0), ("Wall", 26.0)):
        at = np.eye(4)
        at[0, 3] = x
        step = kernel.export_step([kernel.Part(name, box, at, (0.5, 0.5, 0.5))],
                                  tmp_path / f"{name}.step")  # fmt: skip
        ids.append(client.post(f"/api/projects/{project}/import-step", params={"name": name},
                               content=step.read_bytes()).json()["id"])  # fmt: skip
    joint = {"kind": "prismatic", "axis": [1, 0, 0], "lo": 0, "hi": 20, "steps": 5}
    rep = client.post(f"/api/projects/{project}/parts/{ids[0]}/sweep",
                      json={"joint": joint, "required": 2}).json()  # fmt: skip
    wall = next(p for p in rep["pairs"] if p["other"] == ids[1])
    assert wall["status"] == "interference" and wall["at"] == pytest.approx(20)
    env = client.post(f"/api/projects/{project}/parts/{ids[0]}/envelope", json=joint)
    assert env.status_code == 200, env.text
    vol = list(env.json()["topology"].values())[-1]["volume"]
    assert vol == pytest.approx(3000, rel=1e-6)
    assert client.post(f"/api/projects/{project}/parts/nope/sweep",
                       json={"joint": joint}).status_code == 404  # fmt: skip


@pytest.mark.cad
def test_draft_and_parting_of_an_imported_part(client: TestClient, project: str,
                                               tmp_path: Path) -> None:  # fmt: skip
    solid = cq.Workplane().rect(40, 20).workplane(offset=10).rect(36, 16).loft().val()
    step = kernel.export_step([kernel.Part("cap", solid, np.eye(4), (0.5, 0.5, 0.5))],
                              tmp_path / "cap.step")  # fmt: skip
    pid = client.post(f"/api/projects/{project}/import-step", params={"name": "Cap"},
                      content=step.read_bytes()).json()["id"]  # fmt: skip
    r = client.get(f"/api/projects/{project}/parts/{pid}/parting",
                   params={"pull": "z", "pressure": 50}).json()  # fmt: skip
    assert r["parting_edges"] == 4 and r["flat"] and not r["undercuts"]
    assert r["clamp_kn"] == pytest.approx(40 * 20 * 50 / 1000, rel=1e-3)
    assert client.get(f"/api/projects/{project}/parts/{pid}/draft").json()["ok"]
    assert client.get(f"/api/projects/{project}/parts/nope/parting").status_code == 404
