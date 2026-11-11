"""Systems layer: functions → blocks → parts with typed flows, traced end to end."""

import pytest

from autevra import modules
from autevra.aero import aircraft as ac
from autevra.core.parameters import default_values
from autevra.domains import load_builtin
from autevra.product.breakdown import Node, configure
from autevra.product.systems import (
    Architecture,
    Block,
    FailureMode,
    Flow,
    Function,
    chain,
    icd,
    trace,
)

load_builtin()


def _configured(module_id: str, values: dict, override: dict | None = None):  # type: ignore[no-untyped-def]
    m = modules.get(module_id)
    opts = m.options(values)
    config = opts.resolve({**m.current(values), **(override or {})})
    root = configure(m.breakdown(m.configure(values, config)), config, opts.names())
    assert m.architecture is not None
    return m.architecture(values).configured(config, opts.names()), root


def test_architecture_rejects_dangling_references() -> None:
    with pytest.raises(ValueError, match="unknown block"):
        Architecture(
            functions=[],
            blocks=[],
            flows=[Flow(id="f", kind="signal", source="a", target="b", item="x")],
        )
    with pytest.raises(ValueError, match="unknown functions"):
        Architecture(functions=[], blocks=[Block(id="a", name="A", functions=["nope"],
                                                 templates=[])], flows=[])  # fmt: skip


def test_trace_finds_each_kind_of_gap() -> None:
    arch = Architecture(
        functions=[Function(id="f1", name="do one"), Function(id="f2", name="do two")],
        blocks=[Block(id="b1", name="B1", functions=["f1"], templates=["t_missing"])],
        flows=[],
        failure_modes=[FailureMode(id="m", function="f1", block="b1", mode="breaks",
                                   effect="bad", severity=10, occurrence=5, detection=5)],
    )  # fmt: skip
    root = Node(id="p", name="P", kind="product", children=[
        Node(id="x", name="X", template="t_orphan")])  # fmt: skip
    kinds = {i.kind for i in trace(arch, root, ["REQ-001"])}
    assert kinds == {"unallocated_function", "unrealised_block", "orphan_part",
                     "unmitigated_failure", "unallocated_requirement"}  # fmt: skip


def test_fmea_priority() -> None:
    m = FailureMode(id="m", function="f", block="b", mode="x", effect="y", severity=10,
                    occurrence=2, detection=7)  # fmt: skip
    assert m.rpn == 140 and m.priority == "high"
    low = m.model_copy(update={"severity": 3, "occurrence": 2, "detection": 2})
    assert low.priority == "low"


@pytest.mark.parametrize("override", [{}, {"powertrain": "Battery electric"},
                                      {"powertrain": "Hybrid"}])  # fmt: skip
def test_land_architecture_is_fully_allocated(override: dict) -> None:
    arch, root = _configured("land", default_values(), override)
    issues = [i for i in trace(arch, root) if i.severity == "fail"]
    assert issues == []
    assert [i for i in trace(arch, root) if i.kind == "orphan_part"] == []


def test_land_braking_chain_end_to_end() -> None:
    arch, root = _configured("land", default_values())
    steps = chain(arch, "decelerate", root)
    order = [s.block for s in steps]
    assert order.index("pedal") < order.index("modulator") < order.index("calipers")
    assert order.index("calipers") < order.index("discs") < order.index("wheels")
    assert all(s.parts for s in steps if not s.external)
    kinds = {f.kind for s in steps for f in s.flows_out}
    assert {"mechanical", "fluid", "signal"} <= kinds
    rows = icd(arch)
    assert any(r.item == "caliper pressure" and r.kind == "fluid" for r in rows)


def test_land_electric_drops_fuel_and_exhaust_blocks() -> None:
    arch, _ = _configured("land", default_values(), {"powertrain": "Battery electric"})
    ids = {b.id for b in arch.blocks}
    assert "traction_storage" in ids and "fuel_storage" not in ids and "exhaust" not in ids
    assert all(f.source in ids and f.target in ids for f in arch.flows)


@pytest.mark.parametrize("override", [{}, {"undercarriage": "Tailwheel"}])
def test_aircraft_architecture_and_pitch_chain(override: dict) -> None:
    arch, root = _configured("aircraft", ac.AircraftSpec().model_dump(), override)
    assert [i for i in trace(arch, root) if i.severity == "fail"] == []
    steps = chain(arch, "control_pitch", root)
    order = [s.block for s in steps]
    assert order.index("column") < order.index("circuit") < order.index("elevator")
    assert order.index("elevator") < order.index("stabiliser")
    elevator = next(s for s in steps if s.block == "elevator")
    assert elevator.parts and elevator.parts[0]["mass"] > 0
