import pytest

from autevra.domain.rules import validate
from autevra.engineering import spec as sp

TYPICAL_SEATS = {"city_car": "4", "sports_car": "2", "van": "7"}


def _spec(**answers: str | float) -> sp.VehicleSpec:
    s = sp.VehicleSpec()
    for k, v in answers.items():
        assert sp.answer(s, k, v) is None
    return s


@pytest.mark.parametrize("cls", list(sp.TEMPLATES))
def test_every_class_template_is_a_valid_design(cls: str) -> None:
    g = sp.generate(_spec(vehicle_class=cls, seats=TYPICAL_SEATS.get(cls, "5")))
    assert g.violations == [] and validate(g.values) == []
    assert not [c for c in g.checks if c.severity != "info"]


def test_questions_adapt_to_the_answers() -> None:
    petrol = _spec(vehicle_class="sedan", use="family", powertrain="petrol")
    electric = _spec(vehicle_class="sedan", use="family", powertrain="electric")
    applies = lambda s: [q.id for q in sp.QUESTIONS if sp.applicable(q, s)]  # noqa: E731
    assert "battery_capacity" not in applies(petrol)
    assert "battery_capacity" in applies(electric)
    assert sp.next_question(_spec()).id == "vehicle_class"


def test_answers_are_validated_and_optional_ones_can_be_skipped() -> None:
    s = sp.VehicleSpec()
    assert sp.answer(s, "seats", "9") is not None
    assert sp.answer(s, "peak_power", 5000) is not None
    assert sp.answer(s, "vehicle_class", None) is not None  # required
    assert sp.answer(s, "target_mass", None) is None
    assert s.answers["target_mass"].source == "default"


def test_free_text_fills_the_specification_with_units() -> None:
    found = sp.extract(
        "an electric SUV, 300 hp, 2.3 t, 0-100 in 6.5 s, 7 seats, AWD, 20 inch wheels, 90 kWh"
    )
    assert found["vehicle_class"] == "suv" and found["powertrain"] == "electric"
    assert found["peak_power"] == pytest.approx(300 * sp.HP_KW, abs=0.1)
    assert found["target_mass"] == 2300 and found["accel_0_100"] == 6.5
    assert found["seats"] == "7" and found["drivetrain"] == "awd" and found["rim_diameter"] == 20
    assert found["battery_capacity"] == 90


def test_acceleration_lower_bound_matches_closed_form() -> None:
    # Constant power only (traction never limits): t = m v^2 / (2 P eta).
    est = sp.acceleration_lower_bound(100, 1000 - sp.DRIVER_KG, driven_share=100.0)
    v = 100 / 3.6
    assert est["time"] == pytest.approx(1000 * v * v / (2 * 100_000 * sp.ETA), rel=1e-3)
    # Traction only: t = v / (mu g share).
    est = sp.acceleration_lower_bound(10_000, 1000, driven_share=0.5)
    assert est["time"] == pytest.approx(v / (sp.MU * sp.G * 0.5))


def test_impossible_acceleration_is_a_conflict_and_a_feasible_one_is_not_claimed() -> None:
    slow = sp.checks(
        _spec(
            vehicle_class="suv",
            powertrain="electric",
            drivetrain="awd",
            peak_power=150,
            target_mass=2200,
            accel_0_100=6,
        )
    )
    assert [c.severity for c in slow if c.id == "accel_target"] == ["conflict"]
    fast = sp.checks(
        _spec(
            vehicle_class="suv",
            powertrain="electric",
            drivetrain="awd",
            peak_power=300,
            target_mass=2200,
            accel_0_100=6,
        )
    )
    [check] = [c for c in fast if c.id == "accel_target"]
    assert check.severity == "info" and "not claimed" in check.message


def test_battery_and_packaging_warnings() -> None:
    heavy = sp.checks(
        _spec(
            vehicle_class="city_car", powertrain="electric", battery_capacity=100, target_mass=1300
        )
    )
    assert [c.severity for c in heavy if c.id == "battery_mass"] == ["warning"]
    cramped = sp.generate(_spec(vehicle_class="city_car", seats="7"))
    assert any(c.id == "cabin_share" and c.severity == "warning" for c in cramped.checks)


def test_springs_follow_the_target_ride_frequency() -> None:
    from autevra.domain import derived as d

    for ride, hz in sp.RIDE_FRONT_HZ.items():
        g = sp.generate(_spec(vehicle_class="sedan", ride=ride))
        assert d.ride_frequency(g.values, "front") == pytest.approx(hz, abs=0.02)
        assert d.ride_frequency(g.values, "rear") == pytest.approx(hz * 1.1, abs=0.03)
        assert d.damping_ratio(g.values, "front", "bump") == pytest.approx(
            sp.DAMPING[ride][0], abs=0.02
        )


def test_generation_proposes_unapproved_requirements_and_names_sources() -> None:
    g = sp.generate(_spec(vehicle_class="suv", use="off_road", accel_0_100=8))
    assert all(r["approved"] is False for r in g.requirements)
    assert {r.get("quantity") for r in g.requirements} >= {
        "front_ride_frequency",
        "ground_clearance",
    }
    accel = [r for r in g.requirements if r.get("metric") == "accel_time"]
    assert accel and accel[0]["test_id"] == "longitudinal" and accel[0]["limit"] == 8
    assert g.sources["vehicle_mass"].endswith("(default)")
    assert g.values["ground_clearance"] >= 200


@pytest.mark.parametrize("cls", ["hatchback", "sedan", "suv", "pickup", "sports_car", "van"])
def test_generated_designs_pass_the_step_and_hump(cls: str) -> None:
    from autevra.engineering import testing as tst

    g = sp.generate(_spec(vehicle_class=cls, seats=TYPICAL_SEATS.get(cls, "5")))
    for axle in ("front", "rear"):
        for scenario in ("step_25", "hump_75"):
            run = tst.run_test("quarter_car", axle, scenario, g.values)
            assert run.status is tst.RunStatus.PASSED_WITHIN_MODEL, (axle, scenario)
