import pytest
from pydantic import ValidationError

from autevra.core.commands import Change, Operation, SetParameters
from autevra.core.parameters import default_values
from autevra.engineering import reqif, trace
from autevra.engineering import requirements as rq
from autevra.engineering import testing as tst

V = default_values()


def _none(test_id: str, target: str, scenario: str) -> tuple[None, bool]:
    return None, False


def _design(**kw: object) -> rq.Requirement:
    return rq.Requirement(kind="design", **kw)


def test_design_requirement_converts_units_and_writes_its_statement() -> None:
    r = _design(quantity="ground_clearance", comparator=">=", limit=15, unit="cm")
    assert (r.limit, r.unit, r.verification) == (150, "mm", "analysis")
    assert r.text == "The ground clearance shall be at least 150 mm."


@pytest.mark.parametrize(
    "kw",
    [
        {"kind": "design", "quantity": "ground_clearance", "limit": 1, "unit": "kg"},
        {"kind": "design", "quantity": "warp_drive", "limit": 1},
        {"kind": "performance", "metric": "speed", "limit": 1},
        {"kind": "performance", "metric": "max_bump_travel", "limit": 1, "unit": "in"},
        {"kind": "performance", "metric": "max_bump_travel", "scenario_id": "moon"},
        {"kind": "text"},
    ],
)
def test_invalid_requirements_are_rejected(kw: dict) -> None:
    with pytest.raises(ValidationError):
        rq.Requirement(**kw)


def test_design_requirement_is_verified_by_analysis() -> None:
    ok = rq.verify(_design(quantity="front_ride_frequency", comparator="<=", limit=1.5), V, _none)
    bad = rq.verify(_design(quantity="ground_clearance", comparator=">=", limit=200), V, _none)
    assert ok.status == "verified" and ok.evidence[0].kind == "analysis"
    assert bad.status == "failed" and bad.evidence[0].measured == 160


def test_performance_requirement_needs_current_runs() -> None:
    r = rq.Requirement(metric="peak_body_acceleration", target="rear", scenario_id="hump_75",
                       comparator="<=", limit=6)  # fmt: skip
    assert rq.verify(r, V, _none).status == "not_verified"
    criterion = r.as_test_requirement()
    assert criterion is not None
    run = tst.run_test("quarter_car", "rear", "hump_75", V, requirements=[criterion])
    current = rq.verify(r, V, lambda *_: (run, True))
    assert current.status == "verified" and current.evidence[0].run_id == run.id
    stale = rq.verify(r, V, lambda *_: (run, False))
    assert stale.status == "stale"


def test_unapproved_and_text_requirements_never_claim_verification() -> None:
    r = _design(quantity="ground_clearance", comparator=">=", limit=100, approved=False)
    assert rq.verify(r, V, _none).status == "not_approved"
    t = rq.Requirement(kind="text", text="The dampers shall be replaceable without tools.")
    assert rq.verify(t, V, _none).status == "manual"


def test_trace_links_parameters_components_and_cases() -> None:
    r = rq.Requirement(metric="max_bump_travel", target="front", comparator="<=", limit=40)
    [row] = trace.matrix([r], V, _none, 0)
    assert "front_damping_bump" in row.parameters and "arch_clearance" in row.parameters
    assert {"damper_fl", "damper_fr", "front_axle"} <= set(row.components)
    assert row.cases == [f"quarter_car:front:{s}" for s in ("step_25", "hump_75", "pothole_50")]


def test_preview_reports_requirement_changes_without_applying() -> None:
    clearance = _design(key="REQ-001", quantity="ground_clearance", comparator=">=", limit=150)
    travel = rq.Requirement(key="REQ-002", metric="max_bump_travel", comparator="<=", limit=40)
    lower = SetParameters(changes=(Change(parameter="ground_clearance",
                                          operation=Operation.DECREASE, value=20),))  # fmt: skip
    p = trace.preview(lower, V, [clearance, travel], _none, 0)
    assert p.valid and p.requirements[0].after == "failed"
    assert V["ground_clearance"] == 160  # nothing applied
    rims = SetParameters(
        changes=(Change(parameter="rim_diameter", operation=Operation.SET, value=20),)
    )
    p = trace.preview(rims, V, [clearance, travel], _none, 0)
    assert any(c.key == "REQ-002" and c.after == "needs_reverification" for c in p.requirements)
    assert any("damper compression" in w for w in p.warnings_added)
    assert {"damper_fl", "wheel_fl", "body"} <= set(p.rebuild)


def test_preview_flags_rule_violations() -> None:
    narrow = SetParameters(
        changes=(Change(parameter="body_width", operation=Operation.SET, value=1600),)
    )
    p = trace.preview(narrow, V, [], _none, 0)
    assert not p.valid and p.summary.startswith("REJECTED")


def test_reqif_round_trip_keeps_fields_and_hierarchy() -> None:
    parent = _design(key="REQ-001", quantity="ground_clearance", comparator=">=", limit=150)
    child = rq.Requirement(key="REQ-002", metric="peak_body_acceleration", target="rear",
                           scenario_id="hump_75", comparator="<=", limit=6, parent=parent.id,
                           rationale="comfort over speed humps", priority="should")  # fmt: skip
    note = rq.Requirement(key="REQ-003", kind="text", text="Serviceable without lifting the body.")
    back = reqif.parse(reqif.export([parent, child, note], "Test"))
    fields = {
        "key", "kind", "quantity", "metric", "target", "scenario_id", "comparator",
        "limit", "unit", "text", "rationale", "priority", "approved", "verification",
    }  # fmt: skip
    for a, b in zip([parent, child, note], back, strict=True):
        assert a.model_dump(include=fields) == b.model_dump(include=fields)
        assert b.source == "reqif"
    assert back[1].parent == back[0].id


def test_reqif_from_another_tool_becomes_text_requirements() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"><CORE-CONTENT><REQ-IF-CONTENT>
<SPEC-TYPES><SPEC-OBJECT-TYPE IDENTIFIER="T"><SPEC-ATTRIBUTES>
<ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="A1" LONG-NAME="ReqIF.Text"/>
</SPEC-ATTRIBUTES></SPEC-OBJECT-TYPE></SPEC-TYPES>
<SPEC-OBJECTS><SPEC-OBJECT IDENTIFIER="SYS-17"><VALUES><ATTRIBUTE-VALUE-XHTML>
<DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>A1</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>
<THE-VALUE><div xmlns="http://www.w3.org/1999/xhtml">The vehicle shall <b>stop</b>
within 40 m.</div></THE-VALUE>
</ATTRIBUTE-VALUE-XHTML></VALUES></SPEC-OBJECT></SPEC-OBJECTS>
</REQ-IF-CONTENT></CORE-CONTENT></REQ-IF>"""
    [r] = reqif.parse(xml)
    assert r.kind == "text" and r.key == "SYS-17"
    assert " ".join(r.text.split()) == "The vehicle shall stop within 40 m."


@pytest.mark.parametrize(
    "xml",
    [
        '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x "y">]><REQ-IF/>',
        "<not-reqif/>",
        "<REQ-IF",
    ],
)
def test_reqif_rejects_unsafe_or_foreign_documents(xml: str) -> None:
    with pytest.raises(reqif.ReqIFError):
        reqif.parse(xml)


def test_keys_are_sequential() -> None:
    assert rq.next_key([]) == "REQ-001"
    assert rq.next_key([_design(key="REQ-007", quantity="wheelbase", limit=1)]) == "REQ-008"
