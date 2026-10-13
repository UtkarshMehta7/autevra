import pytest

from autevra.domain.parameters import default_values
from autevra.domain.rules import validate
from autevra.engineering import diagnosis as dg
from autevra.engineering import testing as tst


@pytest.fixture(scope="module")
def hump() -> dg.Diagnosis:
    v = default_values()
    return dg.diagnose(tst.run_test("quarter_car", "rear", "hump_75", v), v, current=True)


def test_failed_travel_names_the_governing_limit(hump: dg.Diagnosis) -> None:
    [finding] = hump.findings
    assert finding.criterion == "bump_travel" and finding.status == "failed"
    assert finding.governing_parameter == "arch_clearance"
    assert "the arch governs" in finding.limit_source
    assert finding.measured is not None and finding.measured > finding.limit


def test_effects_are_measured_and_ranked(hump: dg.Diagnosis) -> None:
    effects = hump.findings[0].effects
    assert effects[0].parameter == "arch_clearance" and effects[0].better_direction == "increase"
    damping = next(e for e in effects if e.parameter == "rear_damping_bump")
    assert damping.better_direction == "increase" and damping.evidence == "confirmed_in_model"
    # Front-only parameters are not inputs of the rear test at all.
    assert all(not e.parameter.startswith("front_") or e.parameter == "front_mass_distribution"
               for e in effects)  # fmt: skip
    assert hump.evidence["perturbation_runs"] > 20


def test_suggested_fix_is_valid_and_resolves_in_a_full_run(hump: dg.Diagnosis) -> None:
    fix = next(f for f in hump.findings[0].fixes if not f.rule_violations and not f.breaks)
    fixed = default_values() | {fix.parameter: fix.to_value}
    assert validate(fixed) == []
    rerun = tst.run_test("quarter_car", "rear", "hump_75", fixed)
    assert next(c for c in rerun.criteria if c.id == "bump_travel").passed is True


def test_saturated_tyre_contact_uses_the_lift_off_proxy() -> None:
    v = default_values()
    found = dg.diagnose(tst.run_test("quarter_car", "rear", "pothole_50", v), v, current=True)
    [finding] = found.findings
    assert finding.criterion == "tyre_contact" and "lift off time" in finding.limit_source
    assert any(e.evidence != "none" for e in finding.effects)


def test_passing_run_reports_tightest_margin_without_fixes() -> None:
    v = default_values()
    found = dg.diagnose(tst.run_test("quarter_car", "rear", "step_25", v), v, current=True)
    [finding] = found.findings
    assert finding.status == "tightest_margin" and finding.fixes == []
    assert "not physical root causes" in found.caveats[0]
