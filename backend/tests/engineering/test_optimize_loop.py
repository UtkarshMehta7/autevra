import pytest

from autevra.core.parameters import default_values
from autevra.core.rules import validate
from autevra.engineering import loop as eloop
from autevra.engineering import optimize as opt
from autevra.engineering import testing as tst

ROOMY = default_values() | {"arch_clearance": 45}


def _study(**kw: object) -> opt.Study:
    base = dict(
        target="rear", scenarios=["step_25", "hump_75"],
        objectives=[opt.Objective(metric="rms_body_acceleration")],
        variables=opt.default_variables("quarter_car", "rear", ROOMY), budget=30,
    )  # fmt: skip
    return opt.Study(**(base | kw))


@pytest.fixture(scope="module")
def comfort() -> opt.StudyResult:
    return opt.run_study(_study(), ROOMY)


def test_best_design_beats_baseline_and_is_verified(comfort: opt.StudyResult) -> None:
    assert comfort.status == "proposed" and comfort.best is not None
    assert comfort.improvement["rms_body_acceleration"] < 0
    assert all(v["status"] == "passed_within_model" and v["converged"] for v in comfort.verified)
    assert comfort.command is not None and comfort.command.source == "optimizer"


def test_candidates_respect_bounds_and_budget(comfort: opt.StudyResult) -> None:
    assert len(comfort.candidates) <= 30
    bounds = {v.parameter: (v.lower, v.upper) for v in comfort.study.variables}
    for c in comfort.candidates:
        for p, x in c.values.items():
            lo, hi = bounds[p]
            assert round(lo, 3) - 1e-9 <= x <= round(hi, 3) + 1e-9


def test_baseline_is_preserved_and_scored(comfort: opt.StudyResult) -> None:
    assert comfort.baseline.phase == "baseline"
    assert comfort.baseline.values == {
        v.parameter: ROOMY[v.parameter] for v in comfort.study.variables
    }
    assert comfort.baseline.objectives


def test_scores_come_from_simulation(comfort: opt.StudyResult) -> None:
    best = comfort.best
    assert best is not None
    design = ROOMY | best.values
    metrics = [
        tst.quick_evaluate("quarter_car", "rear", sc, design)[0] for sc in ("step_25", "hump_75")
    ]
    assert best.objectives["rms_body_acceleration"] == pytest.approx(
        max(m["rms_body_acceleration"] for m in metrics)
    )


def test_invalid_candidates_are_never_simulated() -> None:
    v = ROOMY | {"spring_coil_diameter": 190}  # soft springs then break the spring index rule
    wide = [opt.Variable(parameter="rear_spring_rate", lower=5, upper=40)]
    result = opt.run_study(_study(variables=wide, budget=20), v)
    rejected = [c for c in result.candidates if c.rule_violations]
    assert rejected and not any(c.simulated for c in rejected)
    assert all(validate(v | c.values) == [] for c in result.candidates if c.simulated)


def test_two_objectives_give_a_pareto_set_not_a_single_best() -> None:
    objectives = [
        opt.Objective(metric="rms_body_acceleration"),
        opt.Objective(metric="max_bump_travel"),
    ]
    result = opt.run_study(_study(objectives=objectives, scenarios=["hump_75"]), ROOMY)
    assert result.best is None and result.command is None and len(result.pareto) >= 2


def test_reproducible_with_the_same_seed() -> None:
    a, b = opt.run_study(_study(budget=12), ROOMY), opt.run_study(_study(budget=12), ROOMY)
    assert [c.values for c in a.candidates] == [c.values for c in b.candidates]


def test_infeasible_study_names_the_blocking_criterion() -> None:
    result = opt.run_study(_study(scenarios=["pothole_50"], budget=12), default_values())
    assert result.status == "no_feasible_design" and "Tyre stays on the road" in (
        result.blocking or ""
    )


def test_study_inputs_are_validated() -> None:
    with pytest.raises(ValueError, match="not an input"):
        opt.run_study(
            _study(variables=[opt.Variable(parameter="wheelbase", lower=2500, upper=2900)]), ROOMY
        )
    with pytest.raises(ValueError, match="unknown metric"):
        opt.run_study(_study(objectives=[opt.Objective(metric="speed")]), ROOMY)


def test_loop_fixes_what_it_can_and_stops_honestly() -> None:
    result = eloop.run_loop(eloop.Goal(target="rear"), default_values())
    first, last = result.iterations[0], result.iterations[-1]
    assert "wheel arch clearance" in first.decision
    assert result.outcome == "needs_decision" and "needs an engineering decision" in last.decision
    assert result.command is not None  # the partial improvement is still offered for approval
    assert {c.parameter for c in result.command.changes} == {"arch_clearance"}


def test_loop_reaches_all_pass_and_optimises() -> None:
    goal = eloop.Goal(target="rear", scenarios=["step_25", "hump_75"],
                      objective=opt.Objective(metric="rms_body_acceleration"))  # fmt: skip
    result = eloop.run_loop(goal, default_values())
    assert result.outcome == "all_pass" and result.optimization is not None
    assert result.optimization.improvement["rms_body_acceleration"] < 0


def test_loop_with_nothing_to_do() -> None:
    result = eloop.run_loop(eloop.Goal(target="rear", scenarios=["step_25"]), default_values())
    assert result.outcome == "already_passing" and result.status == "nothing_to_apply"
