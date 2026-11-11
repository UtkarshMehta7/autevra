"""The parametric aircraft: analysis sanity, guidance checks, geometry and the API."""

import pytest
from fastapi.testclient import TestClient

from autevra.aero import aircraft as ac
from autevra.part.build import build_part
from autevra.part.features import PartDoc


def test_the_isa_atmosphere() -> None:
    sea, high = ac.isa(0.0), ac.isa(11_000.0)
    assert sea["rho"] == pytest.approx(1.225, abs=1e-3) and sea["T"] == pytest.approx(288.15)
    assert high["T"] == pytest.approx(216.65) and high["rho"] == pytest.approx(0.3639, rel=0.01)


def test_a_light_aircraft_lands_in_the_expected_ranges() -> None:
    r = ac.analyse(ac.AircraftSpec())
    assert 0.022 < r["aero"]["cd0"] < 0.040  # light single-engine aircraft
    assert 9 < r["aero"]["ld_max"] < 16
    assert 0.7 < r["aero"]["oswald_e"] <= r["aero"]["span_efficiency"] <= 1.0
    assert 20 < r["performance"]["v_stall"] < 35  # m/s
    assert all(c["status"] == "pass" for c in r["checks"])


def test_moving_the_cg_aft_erodes_the_static_margin_to_the_neutral_point() -> None:
    base = ac.analyse(ac.AircraftSpec())
    x_np = base["stability"]["x_np"]
    at_np = ac.analyse(ac.AircraftSpec(x_cg=x_np))
    assert at_np["stability"]["static_margin"] == pytest.approx(0.0, abs=1e-9)
    aft = ac.analyse(ac.AircraftSpec(x_cg=x_np + 0.2))
    assert next(c for c in aft["checks"] if c["name"] == "Static margin")["status"] == "fail"


def test_a_bigger_tail_moves_the_neutral_point_aft() -> None:
    small = ac.analyse(ac.AircraftSpec(htail_span=2.6))["stability"]["x_np"]
    large = ac.analyse(ac.AircraftSpec(htail_span=4.2))["stability"]["x_np"]
    assert large > small


@pytest.mark.cad
@pytest.mark.parametrize("variant", [{}, {"high_wing": False, "t_tail": True, "tricycle": False}])
def test_the_geometry_builds_as_a_part(variant: dict) -> None:
    doc = PartDoc.model_validate(ac.geometry(ac.AircraftSpec(**variant)))
    out = build_part(doc)
    assert not out.errors, out.errors
    assert out.shape is not None


@pytest.mark.cad
def test_the_api_analyses_and_builds_the_aircraft(client: TestClient) -> None:
    assert client.get("/api/aero/spec").json()["defaults"]["wing_naca"] == "2412"
    r = client.post("/api/aero/analyse", json={"wing_span": 12.0})
    assert r.status_code == 200 and r.json()["geometry"]["wing_area"] > 15
    assert client.post("/api/aero/analyse", json={"wing_span": -1}).status_code == 422
    project = client.post("/api/projects", json={"name": "Aircraft test"}).json()["id"]
    first = client.post(f"/api/projects/{project}/aircraft", json={})
    assert first.status_code == 200, first.text
    again = client.post(f"/api/projects/{project}/aircraft", json={"wing_span": 12.0})
    assert again.json()["id"] == first.json()["id"]  # updated in place, by name
