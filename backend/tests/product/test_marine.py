"""The Marine module: breakdown, options, architecture, loads."""

import pytest

from autevra import manufacturing, modules
from autevra.marine import hull as hk
from autevra.product.breakdown import configure, rollup
from autevra.product.systems import chain, trace


def _rolled(values: dict, override: dict | None = None):  # type: ignore[no-untyped-def]
    m = modules.get("marine")
    opts = m.options(values)
    c = opts.resolve({**m.current(values), **(override or {})})
    vals = m.configure(values, c)
    root = configure(m.breakdown(vals), c, opts.names())
    assert m.architecture is not None
    return rollup(root), root, m.architecture(vals).configured(c, opts.names()), vals


def test_breakdown_sums_to_the_displacement() -> None:
    s = hk.HullSpec()
    rolled, *_ = _rolled(s.model_dump())
    assert rolled.rollup.mass == pytest.approx(hk.hydrostatics(s)["displacement_t"] * 1000,
                                               rel=1e-6)  # fmt: skip


@pytest.mark.parametrize("override", [{}, {"propulsion": "Twin shaft", "thruster": "Fitted"},
                                      {"material": "GRP"}])  # fmt: skip
def test_fully_allocated_in_every_configuration(override: dict) -> None:
    _, root, arch, vals = _rolled(hk.HullSpec().model_dump(), override)
    assert [i for i in trace(arch, root) if i.severity == "fail"] == []
    props = next(n for n in root.walk() if n.template == "propeller")
    assert props.instances == (2 if vals["twin_shaft"] else 1)
    assert ("thruster" in {n.template for n in root.walk()}) == vals["bow_thruster"]


def test_lighter_hull_material_leaves_more_deadweight() -> None:
    steel, *_ = _rolled(hk.HullSpec().model_dump())
    al, *_ = _rolled(hk.HullSpec().model_dump(), {"material": "Aluminium"})
    dw = lambda r: next(c for c in r.children if c.id == "deadweight").rollup.mass  # noqa: E731
    assert dw(al) > dw(steel)


def test_propulsion_chain_and_plan() -> None:
    _, root, arch, vals = _rolled(hk.HullSpec().model_dump())
    order = [s.block for s in chain(arch, "propel", root)]
    assert order.index("engine") < order.index("gearbox") < order.index("shaft")
    assert order.index("shaft") < order.index("propeller")
    m = modules.get("marine")
    plan = manufacturing.plan(root, dict(m.stations), list(m.station_order), 3600)
    assert plan.reconciliation == []
    assert m.compliance is not None and m.compliance(vals)[0].status == "shown"
