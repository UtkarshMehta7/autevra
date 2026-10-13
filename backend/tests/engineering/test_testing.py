from autevra.core.parameters import default_values
from autevra.engineering import testing as tst
from tests.assembly.test_graph import NO_GEOMETRY


def test_every_parameter_without_geometry_feeds_a_test() -> None:
    read = {p for t in tst.DEFINITIONS.values() for target in t.targets for p in t.inputs(target)}
    assert NO_GEOMETRY - read == {"max_steer_angle"}  # used by the later steering sweep


def test_no_criteria_means_no_verdict() -> None:
    run = tst.run_test("ride_modes", "front", "modal", default_values())
    assert run.status is tst.RunStatus.NO_CRITERIA
    assert run.credibility is tst.Credibility.ANALYTICAL_ESTIMATE


def test_unapproved_requirements_are_ignored() -> None:
    req = tst.Requirement("r1", "quarter_car", "*", "*", "peak_body_acceleration", "<=", 0.1,
                          "m/s²", approved=False)  # fmt: skip
    run = tst.run_test("quarter_car", "front", "step_25", default_values(), requirements=[req])
    assert all(c.source != "user" for c in run.criteria)


def test_same_inputs_same_results_and_hash() -> None:
    a = tst.run_test("quarter_car", "rear", "hump_75", default_values())
    b = tst.run_test("quarter_car", "rear", "hump_75", default_values() | {"cabin_length": 2400})
    assert a.revision.inputs_hash == b.revision.inputs_hash  # cabin length is not an input
    assert a.revision.values_hash != b.revision.values_hash
    assert a.metrics == b.metrics


def test_affected_tests_follow_their_inputs() -> None:
    assert tst.tests_affected(["wheelbase"]) == [("longitudinal", "vehicle")]  # load transfer
    assert tst.tests_affected(["cabin_length"]) == []
    assert ("quarter_car", "front") in tst.tests_affected(["rim_diameter"])  # usable travel
    assert ("longitudinal", "vehicle") in tst.tests_affected(["peak_power"])
    assert tst.tests_affected(["front_damping_bump"]) == [
        ("quarter_car", "front"),
        ("ride_modes", "front"),
    ]
