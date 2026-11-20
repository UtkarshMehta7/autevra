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
def test_aircraft_live_in_their_own_projects(client: TestClient) -> None:
    assert client.get("/api/aero/spec").json()["defaults"]["wing_naca"] == "2412"
    r = client.post("/api/aero/analyse", json={"wing_span": 12.0})
    assert r.status_code == 200 and r.json()["geometry"]["wing_area"] > 15
    assert client.post("/api/aero/analyse", json={"wing_span": -1}).status_code == 422
    car = client.post("/api/projects", json={"name": "A car"}).json()["id"]
    assert client.post(f"/api/projects/{car}/aircraft", json={}).status_code == 422  # no mixing
    plane = client.post("/api/projects", json={"name": "Trainer", "domain": "aerospace"}).json()
    pid = plane["id"]
    assert plane["domain"] == "aerospace"
    assert client.get(f"/api/projects/{pid}/aircraft/spec").json()["name"] == "Trainer"
    first = client.post(f"/api/projects/{pid}/aircraft", json={"name": "Trainer"})
    assert first.status_code == 200, first.text
    again = client.post(f"/api/projects/{pid}/aircraft", json={"name": "Trainer", "wing_span": 12})
    assert again.json()["id"] == first.json()["id"]  # updated in place
    assert client.get(f"/api/projects/{pid}/aircraft/spec").json()["wing_span"] == 12  # kept
    model = client.get(f"/api/projects/{pid}/model").json()
    # the aircraft's own parts (airframe, canopy, propeller, spinner, gear, wheels), no vehicle
    assert [p["category"] for p in model["parts"]] == ["custom"] * 6


def test_climb_is_best_at_the_minimum_power_speed_and_ceilings_are_ordered() -> None:
    import math

    w, s, cd0, k, cl_max = 1110 * ac.G, 15.2, 0.03, math.pi * 8 * 0.8, 1.44
    c = ac.climb_at(w, s, cd0, k, 134.0, 0.8, cl_max, 0.0)
    # at the minimum-power speed induced drag is three times the parasite drag
    rho = ac.isa(0.0)["rho"]
    q = 0.5 * rho * c["v_min_power"] ** 2
    cl = w / (q * s)
    assert cl**2 / k == pytest.approx(3 * cd0, rel=1e-9)

    # ... and the power required there is below that at nearby speeds
    def power(v: float) -> float:
        return 0.5 * rho * v**3 * s * cd0 + 2 * w**2 / (rho * v * s * k)

    assert power(c["v_min_power"]) < min(power(c["v_min_power"] * 0.97),
                                         power(c["v_min_power"] * 1.03))  # fmt: skip
    assert c["roc"] == pytest.approx((c["power_available_kw"] * 1e3 - power(c["v"])) / w)
    # a fixed-pitch propeller is less efficient in the climb than its 0.8 at cruise, so the
    # best climb speed lies above the minimum-power speed
    assert 0.55 < c["prop_efficiency"] < 0.8
    assert c["v"] > c["v_min_power"]
    assert c["prop_diameter"] == pytest.approx(0.5588 * (134 / 0.7457) ** 0.25)
    assert ac.prop_efficiency_at(80.0, 134e3, rho, 1.9, 0.8) == 0.8  # capped at cruise speeds
    out = ac.climb_performance(w, s, cd0, k, 134.0, 0.8, cl_max, 2400.0)
    assert 3.0 < out["roc_sea_level"] < 7.0  # a 180 hp four-seater climbs 700-1300 ft/min
    assert 0 < out["roc_cruise_altitude"] < out["roc_sea_level"]
    assert 3000 < out["service_ceiling"] < out["absolute_ceiling"] < 11_000
    at_service = ac.climb_at(w, s, cd0, k, 134.0, 0.8, cl_max, out["service_ceiling"])
    assert at_service["roc"] == pytest.approx(0.5, abs=1e-4)
    rocs = [p["roc"] for p in out["curve"]]
    assert rocs == sorted(rocs, reverse=True)
    weak = ac.climb_performance(w, s, cd0, k, 20.0, 0.8, cl_max, 0.0)
    assert weak["service_ceiling"] == 0.0 and weak["roc_sea_level"] < 0.5


def test_tail_and_cg_guidance_is_consistent_with_the_analysis() -> None:
    out = ac.analyse(ac.AircraftSpec())
    g, st, z = out["geometry"], out["stability"], out["sizing"]
    assert z["htail_area_for_vh_0_7"] == pytest.approx(g["htail_area"] * 0.7 / st["v_h"])
    assert z["fin_area_for_vv_0_04"] == pytest.approx(g["fin_area"] * 0.04 / st["v_v"])
    assert z["cg_aft_limit"] - z["cg_forward_limit"] == pytest.approx(0.2 * g["mac"])
    moved = ac.analyse(ac.AircraftSpec(x_cg=z["cg_aft_limit"]))
    assert moved["stability"]["static_margin"] == pytest.approx(0.05, abs=1e-6)
    assert out["climb"]["service_ceiling"] > ac.AircraftSpec().cruise_altitude


def test_isa_continues_into_the_stratosphere() -> None:
    low, high = ac.isa(11_000), ac.isa(12_000)
    assert high["T"] == pytest.approx(216.65) == low["T"]
    assert high["p"] / low["p"] == pytest.approx(0.8542, abs=2e-4)  # exp(-g dh / (R T))
    assert ac.isa(10_668)["rho"] == pytest.approx(0.3796, abs=1e-3)  # 35 000 ft


def test_swept_lift_slope_limits() -> None:
    import math

    # unswept, incompressible: Helmbold's formula; very high aspect ratio tends to 2 pi
    assert ac.swept_lift_slope(6, 0.0, 0.0) == pytest.approx(
        2 * math.pi * 6 / (2 + math.sqrt(4 + 36)))  # fmt: skip
    assert ac.swept_lift_slope(1e6, 0.0, 0.0) == pytest.approx(2 * math.pi, rel=1e-4)
    # sweep lowers the slope, Mach number raises it
    assert ac.swept_lift_slope(9, 0.0, 30) < ac.swept_lift_slope(9, 0.0, 0)
    assert ac.swept_lift_slope(9, 0.8, 30) > ac.swept_lift_slope(9, 0.0, 30)
    assert ac._sweep_at(30.0, 0.0, 10, 0.2, 60) == pytest.approx(30.0)
    assert ac._sweep_at(30.0, 1.0, 10, 1.0, 60) == pytest.approx(30.0)  # untapered


def test_korn_drag_divergence_and_wave_drag() -> None:
    w = ac.korn_wave_drag(0.84, 0.5, 0.11, 31.6, 0.95)
    c = 0.85171  # cos 31.6 deg
    assert w["m_dd"] == pytest.approx(0.95 / c - 0.11 / c**2 - 0.5 / (10 * c**3), abs=1e-4)
    assert w["m_dd"] - w["m_crit"] == pytest.approx(0.1077, abs=1e-4)
    # by construction the drag rise slope at M_dd is 0.1 and the drag is 20 * 0.1077^4
    at_dd = ac.korn_wave_drag(w["m_dd"], 0.5, 0.11, 31.6, 0.95)["cd_wave"]
    assert at_dd == pytest.approx(20 * 0.1077**4, rel=2e-3)
    assert ac.korn_wave_drag(0.6, 0.5, 0.11, 31.6, 0.95)["cd_wave"] == 0.0
    # thicker, more lift or less sweep: divergence comes earlier
    assert ac.korn_wave_drag(0.84, 0.5, 0.14, 31.6, 0.95)["m_dd"] < w["m_dd"]
    assert ac.korn_wave_drag(0.84, 0.5, 0.11, 20.0, 0.95)["m_dd"] < w["m_dd"]


def test_thrust_lapse_is_one_at_rest_and_falls_with_speed_and_height() -> None:
    assert ac.thrust_lapse(0.0, 1.0, 9.0) == pytest.approx(1.0)
    assert ac.thrust_lapse(0.3, 1.0, 9.0) < 1.0
    cruise = ac.thrust_lapse(0.84, ac.isa(10_668)["sigma"], 9.0)
    assert 0.15 < cruise < 0.30  # cruise thrust of a big fan is a fifth to a quarter of static


def test_the_777_preset_lands_near_the_published_aircraft() -> None:
    from autevra.aero.presets import PRESETS

    spec = PRESETS["Boeing 777-300ER (twin-jet transport)"]
    out = ac.analyse(spec)
    g, a, p = out["geometry"], out["aero"], out["performance"]
    assert g["wing_area"] == pytest.approx(436.8, rel=1e-3)  # the published reference area
    assert out["atmosphere"]["mach"] == pytest.approx(0.84, abs=0.005)
    assert 17.0 < a["l_over_d"] < 21.0  # long-range twins cruise near 19
    assert 0.012 < a["cd0"] < 0.019
    assert p["thrust_available_kn"] > p["thrust_required_kn"]
    assert 0.28 < p["thrust_to_weight"] < 0.31
    # all fuel burned without reserves bounds the published 13 650 km design range from above
    assert 13_650 < p["range_km"] < 19_000
    assert all(c["status"] != "fail" for c in out["checks"])
    assert out["climb"]["service_ceiling"] > spec.cruise_altitude
    with pytest.raises(ValueError):
        ac.AircraftSpec(propulsion="turbofan")  # needs a thrust


@pytest.mark.cad
def test_the_777_builds_as_valid_parts_at_full_size() -> None:
    from autevra.aero.presets import PRESETS
    from autevra.cad import kernel as k

    spec = PRESETS["Boeing 777-300ER (twin-jet transport)"]
    docs = ac.parts(spec)
    assert [d["name"] for d in docs][1:] == ["Flight deck glazing", "Engines", "Fan faces",
                                            "Landing gear", "Wheels"]  # fmt: skip
    airframe = build_part(PartDoc.model_validate(docs[0]))
    assert not airframe.errors and airframe.shape is not None
    lo, hi = k.bounds(airframe.shape)
    assert hi[1] - lo[1] == pytest.approx(64_800, abs=5)  # the span, mm
    assert 73_900 <= hi[0] - lo[0] < 76_000  # fuselage, plus the swept tailplane tips
    wheels = build_part(PartDoc.model_validate(docs[5]))
    assert not wheels.errors and len(docs[5]["features"]) == 14  # 2 nose + 2 x 6 main
    engines = build_part(PartDoc.model_validate(docs[2]))
    elo, ehi = k.bounds(engines.shape)
    assert ehi[2] < 0 and ehi[1] == pytest.approx(-elo[1])  # under the wing, symmetric
    assert 8_000 < ehi[1] < 14_000  # inboard of mid-span, as on the aircraft


def test_transport_masses_are_near_the_published_empty_mass() -> None:
    from autevra.aero.presets import PRESETS
    from autevra.modules.aircraft import breakdown as b

    g = b.transport_masses(PRESETS["Boeing 777-300ER (twin-jet transport)"])
    empty = sum(v for key, v in g.items() if key != "engine_dry")
    assert empty == pytest.approx(167_829, rel=0.15)  # statistical method: within 15 %
    assert g["engine_dry"] / 2 == pytest.approx(8_283, rel=0.15)  # one GE90-115B, dry
    assert g["wing"] > g["fuselage"] > g["main_gear"] > g["htail"]
