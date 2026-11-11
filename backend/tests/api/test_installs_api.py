"""An engine designed in the Mechanical module, installed in a car and an aircraft."""

import pytest
from fastapi.testclient import TestClient


def _publish(client: TestClient, spec: dict) -> str:
    pid = client.post("/api/projects", json={"name": "eng", "domain": "machinery"}).json()["id"]
    client.put(f"/api/projects/{pid}/engine/spec", json=spec)
    item = client.post(f"/api/projects/{pid}/engine/publish").json()
    return item["id"], pid  # type: ignore[return-value]


@pytest.mark.cad
def test_install_in_a_car_follows_the_engine_version(client: TestClient, project: str) -> None:
    v6 = {
        "name": "V6 3.0",
        "layout": "V",
        "cylinders": 6,
        "bank_angle": 60,
        "bore": 86,
        "stroke": 86,
        "bmep_max": 13,
        "rpm_peak_torque": 4500,
        "rpm_max": 7000,
    }
    item, eng = _publish(client, v6)
    out = client.post(f"/api/projects/{project}/install-engine", json={"item": item}).json()
    assert out["version"] == "1.0.0" and {c["id"] for c in out["checks"]} == {
        "power_to_weight",
        "fits",
    }
    values = client.get(f"/api/projects/{project}").json()["values"]
    assert values["engine_cylinders"] == 2  # V6
    engine_kw = client.get(f"/api/inventory/items/{item}").json()["performance"]["peak_power_kw"]
    assert values["peak_power"] == pytest.approx(
        engine_kw, abs=0.1
    )  # the car's power is the engine's
    history = client.get(f"/api/projects/{project}/history").json()["entries"]
    assert "install engine" in history[-1]["command"]["instruction"]
    product = client.get(f"/api/projects/{project}/product").json()
    engine = next(c for s in product["breakdown"]["children"] for c in s["children"]
                  if c["template"] == "engine")  # fmt: skip
    assert "inventory item" in engine["basis"]
    # a new engine version: impact shown before the upgrade
    v6["bmep_max"] = 15
    client.put(f"/api/projects/{eng}/engine/spec", json=v6)
    client.post(f"/api/projects/{eng}/engine/publish")
    status = client.get(f"/api/projects/{project}/installed-engine").json()
    assert status["upgrade_available"] and status["impact"]["peak_power_kw"] > 0
    up = client.post(f"/api/projects/{project}/installed-engine/upgrade").json()
    assert up["version"] == "1.1.0"
    assert not client.get(f"/api/projects/{project}/installed-engine").json()["upgrade_available"]


def test_install_in_an_aircraft_checks_the_propeller_tip(client: TestClient) -> None:
    fast = {
        "name": "Racer",
        "cylinders": 4,
        "bore": 90,
        "stroke": 80,
        "rpm_max": 6500,
        "rpm_peak_torque": 4500,
    }
    item, _ = _publish(client, fast)
    plane = client.post("/api/projects", json={"name": "p", "domain": "aerospace"}).json()["id"]
    out = client.post(f"/api/projects/{plane}/install-engine", json={"item": item}).json()
    tip = next(c for c in out["checks"] if c["id"] == "tip_mach")
    assert tip["status"] == "fail"  # a 1.9 m propeller at 6,500 rpm: supersonic tips
    assert client.get(f"/api/projects/{plane}/aircraft/spec").json()["power_kw"] > 50


def test_only_engines_install_as_powertrains(client: TestClient, project: str) -> None:
    r = client.post(f"/api/projects/{project}/install-engine", json={"item": "bearing-6205"})
    assert r.status_code == 422


def test_performance_follows_the_engine(client: TestClient, project: str) -> None:
    item, eng = _publish(client, {"name": "I4", "cylinders": 4, "bore": 86, "stroke": 86})
    client.post(f"/api/projects/{project}/install-engine", json={"item": item})
    slow = client.get(f"/api/projects/{project}/installed-engine/performance").json()
    assert len(slow["gears"]) == 6 and slow["zero_to_100_s"] > 0
    assert slow["zero_to_100_s"] >= slow["cvt_zero_to_100_s"] * 0.95  # gears cannot beat a CVT
    client.put(f"/api/projects/{eng}/engine/spec",
               json={"name": "I4", "cylinders": 4, "bore": 86, "stroke": 86, "turbo": True,
                     "bmep_max": 20, "rpm_peak_torque": 3000})  # fmt: skip
    client.post(f"/api/projects/{eng}/engine/publish")
    client.post(f"/api/projects/{project}/installed-engine/upgrade")
    fast = client.get(f"/api/projects/{project}/installed-engine/performance").json()
    assert fast["zero_to_100_s"] < slow["zero_to_100_s"]  # the turbo version is quicker
