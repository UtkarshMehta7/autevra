"""Process FMEA: generic modes per process, severity linked to the design FMEA."""

from autevra import pfmea
from autevra.manufacturing import Operation
from autevra.product.systems import Architecture, Block, FailureMode, Function


def _op(part: str, process: str, bought: bool = False) -> Operation:
    return Operation(part=part, name=part.title(), process=process, station="Body shop",
                     instances=1, make_min=1.0, fit_min=0.5, material="s355", material_kg=1.0,
                     cost_eur=1.0, co2_kg=1.0, bought_out=bought)  # fmt: skip


def test_rows_per_process_and_fit() -> None:
    rows = pfmea.generate([_op("rail", "weldment"), _op("bolt", "standard", bought=True)], {})
    rail = [r for r in rows if r.part == "rail"]
    bolt = [r for r in rows if r.part == "bolt"]
    assert len(rail) == len(pfmea.MODES["weldment"]) + len(pfmea.FIT)
    assert len(bolt) == len(pfmea.FIT) and all(r.step == "fit" for r in bolt)
    assert all(r.rpn == r.severity * r.occurrence * r.detection for r in rows)
    assert all(r.severity_from == "generic" for r in rows)
    weld = next(r for r in rail if r.mode.startswith("lack of fusion"))
    assert (weld.severity, weld.occurrence, weld.detection, weld.rpn) == (8, 4, 6, 192)
    assert weld.priority == "medium"


def test_design_severity_raises_function_and_strength_modes_only() -> None:
    arch = Architecture(
        functions=[Function(id="stop", name="Stop")], flows=[],
        blocks=[Block(id="brake", name="Brakes", functions=["stop"], templates=["caliper"])],
        failure_modes=[FailureMode(id="f1", function="stop", block="brake", severity=10,
                                   mode="loss of braking", effect="cannot stop",
                                   occurrence=2, detection=3)])  # fmt: skip
    rows = pfmea.generate([_op("cal_fl", "casting")], {"cal_fl": "caliper"}, arch)
    porosity = next(r for r in rows if "porosity" in r.mode)
    assert porosity.severity == 10 and porosity.severity_from == "loss of braking"
    assert porosity.priority == "high"  # severity 10 with occurrence 5
    fit = next(r for r in rows if r.mode.startswith("dimension out"))
    assert fit.severity == 5 and fit.severity_from == "generic"  # a fit mode stays generic
    assert rows[0].priority == "high"  # sorted worst first
    s = pfmea.summary(rows)
    assert s["rows"] == len(rows) and sum(s["by_priority"].values()) == len(rows)
    assert s["linked_to_design"] >= 3 and s["stations"]["Body shop"]["max_rpn"] == 300


def test_every_made_process_has_modes() -> None:
    from autevra.manufacturing import PROCESS

    made = {name for name, row in PROCESS.items() if not row[5]}
    assert made == set(pfmea.MODES)
    for rows in [*pfmea.MODES.values(), pfmea.FIT]:
        for row in rows:
            assert row[2] in pfmea.SEVERITY and 1 <= row[6] <= 10 and 1 <= row[7] <= 10
