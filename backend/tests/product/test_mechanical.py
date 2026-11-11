"""The Mechanical module's engine: breakdown, options and architecture."""

import pytest

from autevra import modules
from autevra.mech import piston as pk
from autevra.product.breakdown import configure, rollup
from autevra.product.systems import chain, trace


def _rolled(values: dict, override: dict | None = None):  # type: ignore[no-untyped-def]
    m = modules.get("mechanical")
    opts = m.options(values)
    config = opts.resolve({**m.current(values), **(override or {})})
    vals = m.configure(values, config)
    root = configure(m.breakdown(vals), config, opts.names())
    assert m.architecture is not None
    return rollup(root), root, m.architecture(vals).configured(config, opts.names()), vals


def test_engine_module_is_its_own() -> None:
    assert modules.for_domain("machinery").id == "mechanical"


@pytest.mark.parametrize("kw", [{}, {"layout": "V", "cylinders": 8, "turbo": True},
                                {"fuel": "diesel", "cylinders": 6, "compression_ratio": 17,
                                 "turbo": True, "bmep_max": 22, "rpm_peak_torque": 2000,
                                 "rpm_max": 4800}])  # fmt: skip
def test_breakdown_sums_to_the_engine_mass_and_is_fully_allocated(kw: dict) -> None:
    spec = pk.EngineSpec(**kw)
    rolled, root, arch, _ = _rolled(spec.model_dump())
    assert rolled.rollup.mass == pytest.approx(pk.mass_kg(spec), rel=1e-6)
    parts = {n.template: n for n in root.walk() if n.kind == "part"}
    assert parts["piston"].instances == spec.cylinders
    assert parts["valve"].instances == 4 * spec.cylinders
    assert ("turbocharger" in parts) == spec.turbo
    assert ("spark_plug" in parts) == (spec.fuel == "petrol")
    assert ("glow_plug" in parts) == (spec.fuel == "diesel")
    assert [i for i in trace(arch, root) if i.severity == "fail"] == []


def test_configuration_switches_fuel_and_aspiration() -> None:
    values = pk.EngineSpec().model_dump()
    _, root, _, vals = _rolled(values, {"fuel": "Diesel", "aspiration": "Turbocharged"})
    assert vals["fuel"] == "diesel" and vals["turbo"] is True
    templates = {n.template for n in root.walk()}
    assert {"glow_plug", "turbocharger", "intercooler"} <= templates
    assert "spark_plug" not in templates


def test_energy_chain_end_to_end() -> None:
    _, root, arch, _ = _rolled(pk.EngineSpec(turbo=True).model_dump())
    order = [s.block for s in chain(arch, "convert", root)]
    assert order.index("intake") < order.index("chambers") < order.index("cranktrain")
    assert order.index("cranktrain") < order.index("flywheel") < order.index("consumer")
