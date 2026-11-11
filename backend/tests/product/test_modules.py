"""Both modules' breakdowns: complete, consistent and checked against references."""

import pytest

from autevra import modules
from autevra.aero import aircraft as ac
from autevra.core.parameters import default_values
from autevra.domains import load_builtin
from autevra.modules.aircraft.breakdown import group_masses
from autevra.product import templates
from autevra.product.breakdown import check_ids, configure, rollup

load_builtin()


def _rolled(module_id: str, values: dict, override: dict | None = None):  # type: ignore[no-untyped-def]
    m = modules.get(module_id)
    opts = m.options(values)
    config = opts.resolve({**m.current(values), **(override or {})})
    vals = m.configure(values, config)
    full = m.breakdown(vals)
    check_ids(full)
    return rollup(configure(full, config, opts.names())), m.checks(vals, rollup(
        configure(full, config, opts.names()))), config  # fmt: skip


def test_modules_are_separate() -> None:
    assert modules.for_domain("automotive").id == "land"
    assert modules.for_domain("aerospace").id == "aircraft"
    assert modules.for_domain("marine") is None
    land, air = set(templates.of("land")), set(templates.of("aircraft"))
    assert len(land) > 60 and len(air) > 45


def test_aircraft_empty_mass_matches_the_reference_type() -> None:
    """The default aircraft is sized like a Cessna 172S (MTOW 1,111 kg, published empty
    mass about 760 kg); Raymer's GA equations should land within 10 %."""
    empty = sum(v for k, v in group_masses(ac.AircraftSpec(), 3.8).items() if k != "engine_dry")
    assert empty == pytest.approx(760, rel=0.10)


def test_aircraft_breakdown_balances_to_mtow_and_follows_options() -> None:
    v = ac.AircraftSpec().model_dump()
    r, checks, _ = _rolled("aircraft", v)
    assert r.rollup.mass == pytest.approx(1110.0)  # empty + fuel + payload = MTOW
    ids = {n.id for n in r.children for n in [n, *n.children]}
    assert "nose_leg" in ids and "tailwheel" not in ids and "retraction" not in ids
    r2, _, _ = _rolled("aircraft", v, {"undercarriage": "Tailwheel", "gear": "Retractable"})
    ids2 = {c.id for s in r2.children for c in s.children}
    assert "tailwheel" in ids2 and "retraction" in ids2 and "nose_leg" not in ids2
    utility, _, _ = _rolled("aircraft", v, {"category": "Utility"})
    wing = lambda root: next(s for s in root.children if s.id == "ata57").rollup.mass  # noqa: E731
    assert wing(utility) > wing(r)  # a higher load factor makes a heavier wing
    assert {c.id for c in checks} == {"empty_mass", "useful_load", "cg"}
    ribs = next(c for s in r.children for c in s.children if c.id == "rib")
    assert ribs.instances >= 8  # repeated parts are instances of one template


def test_aircraft_too_heavy_to_fly_fails_useful_load() -> None:
    v = ac.AircraftSpec(mtow=850.0).model_dump()
    _, checks, _ = _rolled("aircraft", v)
    assert next(c for c in checks if c.id == "useful_load").status == "fail"


def test_aircraft_rule_aerobatic_fixed_gear() -> None:
    m = modules.get("aircraft")
    opts = m.options({})
    assert opts.violations({"category": "Aerobatic", "gear": "Retractable"})


def test_land_breakdown_kerb_mass_is_plausible_and_options_switch_parts() -> None:
    v = default_values()
    ice, checks, cfg = _rolled("land", v)
    assert cfg["powertrain"] == "Combustion"
    # a mid-size combustion saloon: kerb mass (minus the 75 kg driver) 1,150-1,600 kg
    assert 1150 < ice.rollup.mass - 75 < 1600
    bev, _, cfg = _rolled("land", v, {"powertrain": "Battery electric"})
    assert "engine" not in cfg
    parts = lambda r: {n.template for n in _walk(r)}  # noqa: E731
    assert "traction_battery" in parts(bev) and "engine" not in parts(bev)
    assert "exhaust" in parts(ice) and "traction_battery" not in parts(ice)
    tow, _, _ = _rolled("land", v, {"tow_bar": "Fitted"})
    assert tow.rollup.mass == pytest.approx(ice.rollup.mass + 18.0)
    assert {c.id for c in checks} == {"mass", "front_share", "cg_height"}
    # parts with generated geometry are at level 1, the rest at level 0
    assert ice.rollup.maturity[1] > 0 and ice.rollup.maturity[0] > 0


def test_land_v8_rule() -> None:
    m = modules.get("land")
    opts = m.options(default_values())
    assert opts.violations({"powertrain": "Hybrid", "engine": "V8"})
    assert not opts.violations({"powertrain": "Combustion", "engine": "V8"})


def _walk(r):  # type: ignore[no-untyped-def]
    yield r
    for c in r.children:
        yield from _walk(c)
