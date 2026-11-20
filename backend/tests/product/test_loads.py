"""Load cases, compliance and materials against hand calculations."""

import math

import pytest

from autevra import materials
from autevra.aero import aircraft as ac
from autevra.core.parameters import default_values
from autevra.domains import load_builtin
from autevra.mech import piston as pk
from autevra.modules.aircraft import loads as air
from autevra.modules.land import loads as land
from autevra.modules.mechanical import loads as eng

load_builtin()
G = 9.80665


def test_land_cases_are_in_equilibrium_with_the_weight() -> None:
    v = default_values()
    weight = v["vehicle_mass"] * G
    cases = {c.id: c for c in land.cases(v)}
    assert sum(x.fz for x in cases["bump"].loads) == pytest.approx(3 * weight, abs=4)
    braking = cases["braking"]
    assert sum(x.fz for x in braking.loads) == pytest.approx(weight, abs=4)
    assert sum(x.fx for x in braking.loads) == pytest.approx(weight, abs=4)  # 1 g
    front = sum(x.fz for x in braking.loads if x.location.endswith(("FL", "FR")))
    static_front = weight * v["front_mass_distribution"] / 100
    transfer = weight * v["cg_height"] / v["wheelbase"]
    assert front == pytest.approx(static_front + transfer, abs=4)
    corner = cases["cornering"]
    assert sum(x.fy for x in corner.loads) == pytest.approx(weight, abs=4)  # towards the turn
    right = sum(x.fz for x in corner.loads if x.location[-1] == "R")
    assert right > weight / 2  # load moves to the outside wheels


def test_braking_regulation_row() -> None:
    row = land.compliance(default_values())[0]
    assert "R13-H" in row.clause and row.status == "shown"
    assert 0 < land.stopping_distance(default_values()) <= 70


def test_aircraft_gust_load_factor_by_hand() -> None:
    v = ac.AircraftSpec().model_dump()
    env = air.envelope(v)
    out = ac.analyse(ac.AircraftSpec())
    ws = 1110 * 2.20462 / (out["geometry"]["wing_area"] * 3.28084**2)
    a = out["aero"]["wing_lift_slope"]
    mu = 2 * ws / (0.0023769 * out["geometry"]["mac"] * 3.28084 * a * 32.17)
    kg = 0.88 * mu / (5.3 + mu)
    n = 1 + kg * 50 * env["vc"] * 1.943844 * a / (498 * ws)
    assert env["gust_vc"][0] == pytest.approx(n)
    assert env["va"] == pytest.approx(env["vs"] * math.sqrt(3.8))
    assert env["vd"] >= 1.4 * env["vc_min"] and env["n_neg"] == pytest.approx(-1.52)


def test_aircraft_categories_raise_the_loads() -> None:
    base = ac.AircraftSpec().model_dump()
    normal = {c.id: c for c in air.cases(base)}["manoeuvre"].results["root_bending_nm"]
    aero = {c.id: c for c in air.cases({**base, "category": "Aerobatic"})}
    assert aero["manoeuvre"].results["root_bending_nm"] > normal
    assert any(c.results.get("cap_area_mm2") for c in aero.values())


def test_engine_gas_force_by_hand() -> None:
    spec = pk.EngineSpec(bore=86)
    firing = eng.cases(spec.model_dump())[0]
    assert firing.results["gas_force_n"] == pytest.approx(75e5 * math.pi / 4 * 0.086**2, abs=1)
    diesel = eng.cases(pk.EngineSpec(fuel="diesel", compression_ratio=17).model_dump())[0]
    assert diesel.results["gas_force_n"] > firing.results["gas_force_n"]


def test_materials_state_their_basis() -> None:
    assert all(m.source for m in materials.MATERIALS.values())
    s355 = materials.get("s355")
    assert (s355.yield_mpa, s355.ultimate_mpa, s355.basis) == (355, 470, "minimum")
    assert materials.margin_of_safety(100, s355) == pytest.approx(355 / 150 - 1)
    cfrp = materials.get("cfrp_qi")
    assert materials.margin_of_safety(100, cfrp) == pytest.approx(600 / 150 - 1)  # no yield
