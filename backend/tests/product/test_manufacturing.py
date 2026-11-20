"""Manufacturing plan and tolerance stack-ups."""

import math

import pytest

from autevra import manufacturing, modules, quality
from autevra.core.parameters import default_values
from autevra.domains import load_builtin
from autevra.mech import piston as pk
from autevra.product.breakdown import Node, configure

load_builtin()


def test_stackup_worst_case_and_rss_by_hand() -> None:
    stack = quality.Stack(name="gap", lsl=0.0, usl=1.0, contributors=[
        quality.Contributor(name="a", nominal=10.0, plus=0.2, minus=0.2),
        quality.Contributor(name="b", nominal=9.5, plus=0.1, minus=0.1, direction=-1),
        quality.Contributor(name="c", nominal=0.0, plus=0.3, minus=0.1),  # asymmetric
    ])  # fmt: skip
    out = quality.analyse(stack)
    assert out["nominal"] == pytest.approx(0.5)
    assert out["mean"] == pytest.approx(0.6)  # c re-centred by +0.1
    assert out["worst_case"] == pytest.approx([0.6 - 0.5, 0.6 + 0.5])
    sigma = math.sqrt((0.2 / 3) ** 2 + (0.1 / 3) ** 2 + (0.2 / 3) ** 2)
    assert out["sigma"] == pytest.approx(sigma)
    assert out["cpk"] == pytest.approx(min(0.4, 0.6) / (3 * sigma))
    assert sum(out["contributions"].values()) == pytest.approx(1.0)
    assert out["worst_case_ok"] is False  # 0.1-1.1 exceeds the 1.0 upper limit


def test_plan_reconciles_and_counts_every_part() -> None:
    root = Node(id="p", name="P", kind="product", children=[
        Node(id="a", name="A", process="casting", mass=10.0, instances=2, code="x.a"),
        Node(id="b", name="B", process="standard", mass=1.0, code="y.b"),
    ])  # fmt: skip
    plan = manufacturing.plan(root, {"x": "Station X"}, ["Station X"], 60)
    assert plan.reconciliation == []
    assert [s.name for s in plan.stations] == ["Station X", "Final assembly"]
    a = next(o for o in plan.operations if o.part == "a")
    assert a.make_min == pytest.approx(2 * (3.5 + 0.45 * 5.0))
    assert a.material_kg == pytest.approx(10.0 * 1.15)
    b = next(o for o in plan.operations if o.part == "b")
    assert b.bought_out and b.make_min == 0


@pytest.mark.parametrize("module_id", ["land", "mechanical"])
def test_every_module_plans_cleanly(module_id: str) -> None:
    m = modules.get(module_id)
    v = default_values() if module_id == "land" else pk.EngineSpec().model_dump()
    opts = m.options(v)
    c = opts.resolve(m.current(v))
    root = configure(m.breakdown(m.configure(v, c)), c, opts.names())
    plan = manufacturing.plan(root, dict(m.stations), list(m.station_order), 60)
    assert plan.reconciliation == [] and plan.total_cost_eur > 0 and plan.total_co2_kg > 0
    assert m.stackups is not None and all("cpk" in quality.analyse(s) for s in m.stackups(v))
