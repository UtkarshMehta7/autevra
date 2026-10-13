import pytest

from autevra.api import model_service
from autevra.assembly import vehicle
from autevra.assembly.vehicle import Coincidence
from autevra.cad.cache import GeometryCache
from autevra.core.parameters import default_values
from autevra.engineering import integration as ig
from autevra.engineering.integration import Status


def _by_kind(checks: list[ig.Check], kind: str) -> list[ig.Check]:
    return [c for c in checks if c.kind == kind]


def test_default_assembly_is_connected_and_closed() -> None:
    checks = ig.structural_checks(default_values())
    assert all(c.status is Status.PASS for c in checks), [c.message for c in checks]
    assert len(_by_kind(checks, "coincidence")) == 4
    assert len(_by_kind(checks, "load_path")) == 4
    assert len(_by_kind(checks, "interface")) == len(vehicle.COMPONENTS) - 1


def test_upper_eyes_meet_towers_for_any_valid_wheel_size() -> None:
    for rim in (15, 17, 20):
        checks = _by_kind(ig.structural_checks(default_values() | {"rim_diameter": rim}),
                          "coincidence")  # fmt: skip
        assert all(c.status is Status.PASS and c.measured == pytest.approx(0) for c in checks)


def test_a_misplaced_mount_is_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    wrong = (Coincidence(("damper_fl", "upper_eye"), ("body", "shock_tower_fr")),)
    monkeypatch.setattr(ig, "COINCIDENCES", wrong)
    [check] = _by_kind(ig.structural_checks(default_values()), "coincidence")
    assert check.status is Status.FAIL and check.measured == pytest.approx(900)


def test_incompatible_interfaces_are_detected() -> None:
    assert ("hub", "lower_eye") not in ig.COMPATIBLE
    assert ig.interface_kind("shock_tower_rl") == "shock_tower"
    assert ig.interface_kind("front_axle_mount") == "axle_mount"


def test_broken_load_path_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ig, "LOAD_PATHS", (("wheel_fl", "rear_axle", "damper_fl", "body"),))
    [check] = _by_kind(ig.structural_checks(default_values()), "load_path")
    assert check.status is Status.FAIL and "wheel_fl and rear_axle" in check.message


def test_travel_warning_names_the_governing_parameter() -> None:
    warnings = [c for c in ig.travel_checks(default_values()) if c.status is Status.WARNING]
    assert {c.id for c in warnings} == {"travel:front_bump", "travel:rear_bump"}
    assert all("arch_clearance" in c.parameters for c in warnings)
    roomy = ig.travel_checks(default_values() | {"arch_clearance": 80})
    assert all(c.status is Status.PASS for c in roomy)


@pytest.mark.cad
def test_exact_clearances_match_the_parameters() -> None:
    p = default_values()
    model = model_service.build_model(p, GeometryCache())
    checks = {c.id: c for c in ig.clearance_checks(model)}
    assert all(c.status is Status.PASS for c in checks.values())
    # The tyre-to-arch distance measured on the solids equals the arch clearance parameter.
    assert checks["clearance:wheel_fl:body"].measured == pytest.approx(
        p["arch_clearance"], abs=0.05
    )


@pytest.mark.cad
def test_clearance_failure_is_detected_on_real_geometry() -> None:
    p = default_values() | {"rail_spacing": 1240}
    checks = {c.id: c for c in ig.clearance_checks(model_service.build_model(p, GeometryCache()))}
    assert checks["clearance:wheel_fl:damper_fl"].status is Status.FAIL
