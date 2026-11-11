"""Fault trees from the architecture."""

import math

import pytest
from fastapi.testclient import TestClient

from autevra.product.breakdown import Node
from autevra.product.fault_tree import fault_tree
from autevra.product.systems import Architecture, Block, Function


def test_or_gates_add_rates() -> None:
    arch = Architecture(functions=[Function(id="f", name="do"), Function(id="g", name="sub",
                                                                         parent="f")],
                        blocks=[Block(id="a", name="A", functions=["f"], templates=["ta"]),
                                Block(id="b", name="B", functions=["g"], templates=["tb"])],
                        flows=[])  # fmt: skip
    root = Node(id="p", name="P", kind="product", children=[
        Node(id="pa", name="PA", template="ta", process="inventory", instances=2),
        Node(id="pb", name="PB", template="tb", process="casting")])  # fmt: skip
    t = fault_tree(arch, root, "f", exposure_h=1000)
    assert t.rate_per_h == pytest.approx(2 * 10e-6 + 0.2e-6)
    assert t.probability == pytest.approx(1 - math.exp(-t.rate_per_h * 1000))
    assert t.gates[0].block == "a" and t.gates[0].importance == pytest.approx(20 / 20.2)


def test_api_targets(client: TestClient, project: str) -> None:
    out = client.get(f"/api/projects/{project}/systems/fault-tree/decelerate").json()
    assert out["tree"]["top_event"] == "loss of decelerate and hold"
    assert out["target"]["class"] == "catastrophic" and out["target"]["met"] is False
    plane = client.post("/api/projects", json={"name": "p", "domain": "aerospace"}).json()["id"]
    pitch = client.get(f"/api/projects/{plane}/systems/fault-tree/control_pitch").json()
    assert pitch["target"]["scheme"].startswith("CS-23")
    assert client.get(f"/api/projects/{plane}/systems/fault-tree/nope").status_code == 404
