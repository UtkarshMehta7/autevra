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
