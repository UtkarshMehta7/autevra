"""Life-cycle assessment: stages add up, credits apply, and the use phase follows physics."""

import pytest
from fastapi.testclient import TestClient

from autevra import manufacturing, sustainability
from autevra.product.breakdown import Node


def test_stages_and_recycling_credit() -> None:
    root = Node(id="p", name="P", kind="product", children=[
        Node(id="a", name="A", process="sheet metal", mass=100.0, code="x")])  # fmt: skip
    plan = manufacturing.plan(root, {}, [], 60)
    use = sustainability.UsePhase(unit="km", energy_per_unit_kwh=0.2, carrier="electricity",
                                  co2_per_unit_kg=0.06, life_units=1000, basis="test")  # fmt: skip
    a = sustainability.assess(plan, use)
    bought = 100 * 1.45  # sheet metal buy-to-fly
    assert a.end_of_life_kg == pytest.approx(-bought * 0.85 * (1.9 - 0.6), abs=0.1)
    assert a.use_kg == pytest.approx(60.0)
    assert a.total_kg == pytest.approx(a.production_kg + a.use_kg + a.end_of_life_kg, abs=0.2)


def test_lca_api_for_cars_and_electric_cars(client: TestClient, project: str) -> None:
    ice = client.get(f"/api/projects/{project}/lca").json()
    assert ice["use"]["carrier"] == "petrol" and ice["shares"]["use"] > 0.5
    per_km = ice["use"]["co2_per_unit_kg"] * 1000  # g/km
    assert 80 < per_km < 250  # a petrol car on a mixed cycle
    clean = client.get(f"/api/projects/{project}/lca", params={"grid": 0.0}).json()
    assert clean["use_kg"] == ice["use_kg"]  # petrol does not depend on the grid
    plane = client.post("/api/projects", json={"name": "p", "domain": "aerospace"}).json()["id"]
    air = client.get(f"/api/projects/{plane}/lca").json()
    assert air["use"]["unit"] == "flight hour" and 60 < air["use"]["co2_per_unit_kg"] < 200
