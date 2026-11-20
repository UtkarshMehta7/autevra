"""Wing structure sizing against hand formulas, and level 2 in the breakdown."""

import math

import pytest

from autevra import materials, modules
from autevra.aero import aircraft as ac
from autevra.modules.aircraft import structure as st
from autevra.product.breakdown import configure, rollup


def test_plate_buckling_formula() -> None:
    # k pi^2 E (t/b)^2 / (12 (1 - nu^2)) for a 1 mm x 100 mm aluminium panel
    got = st.plate_buckling_stress(0.001, 0.1, 72e9, 0.33)
    assert got == pytest.approx(4 * math.pi**2 * 72e9 * 1e-4 / (12 * (1 - 0.33**2)))


def test_caps_and_effective_skin_carry_the_moment() -> None:
    v = ac.AircraftSpec().model_dump()
    r = st.size_wing(v)
    al = materials.get("2024_t3")
    allow = al.yield_mpa / 1.5  # MPa
    area = r["cap_area_mm2"] + 2 * r["effective_width_mm"] * r["skin_mm"]  # mm²
    force = area * allow  # N
    assert force * r["spar_depth_mm"] / 1000 == pytest.approx(r["root_bending_nm"], rel=1e-6)
    shear = r["web_mm"] / 1000 * r["spar_depth_mm"] / 1000 * 0.55 * al.yield_mpa * 1e6 / 1.5
    assert shear == pytest.approx(r["root_shear_n"], rel=1e-6)


def test_aerobatic_wing_is_heavier_and_close_to_the_statistics() -> None:
    v = ac.AircraftSpec().model_dump()
    normal = st.size_wing(v)["total_kg"]
    aero = st.size_wing({**v, "category": "Aerobatic"})["total_kg"]
    assert aero > normal
    # Raymer's whole-wing statistic for this aircraft is about 140 kg (with flaps and
    # ailerons); the sized box should be of the same order
    assert 100 < normal < 220


def test_sized_parts_are_engineered_in_the_breakdown() -> None:
    m = modules.get("aircraft")
    v = ac.AircraftSpec().model_dump()
    opts = m.options(v)
    c = opts.resolve(m.current(v))
    r = rollup(configure(m.breakdown(m.configure(v, c)), c, opts.names()))
    wing = next(s for s in r.children if s.id == "ata57")
    levels = {p.id: (p.maturity, p.mass_source) for p in wing.children}
    assert levels["spar_front"] == (2, "computed") and levels["wing_skin"] == (2, "computed")
    assert r.rollup.maturity[2] > 0
