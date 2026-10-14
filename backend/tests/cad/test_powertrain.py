"""Chassis architectures and powertrain equipment: what is fitted, and where."""

import pytest

from autevra.api.model_service import build_model
from autevra.cad import kernel as k
from autevra.cad.cache import GeometryCache
from autevra.core.parameters import default_values
from autevra.domains.automotive import derived as d

pytestmark = pytest.mark.cad
COMBUSTION = {"engine", "gearbox", "fuel_tank", "exhaust"}
ELECTRIC = {"traction_battery", "inverters", "charger", "charge_port", "hv_cables"}
ALWAYS = {"radiator", "battery_12v", "ecus", "harness"}


def _fitted(**changes: float) -> set[str]:
    model = build_model(default_values() | changes, GeometryCache())
    for part in model.parts:
        assert k.is_valid(model.shapes[part.geometry]), part.id
    return {p.id for p in model.parts if p.category in ("powertrain", "electrical")}


def test_combustion_has_engine_and_fuel_but_no_traction_battery() -> None:
    assert _fitted(powertrain_type=0) == COMBUSTION | ALWAYS


def test_hybrid_carries_both_systems() -> None:
    assert _fitted(powertrain_type=1, battery_capacity=14) == COMBUSTION | ELECTRIC | ALWAYS


@pytest.mark.parametrize(("share", "motors"), [(100, {"front_motor"}), (0, {"rear_motor"}),
                                               (40, {"front_motor", "rear_motor"})])  # fmt: skip
def test_electric_motors_follow_the_driven_axles(share: float, motors: set[str]) -> None:
    fitted = _fitted(powertrain_type=2, chassis_type=2, front_drive_share=share)
    assert fitted == ELECTRIC | ALWAYS | motors


@pytest.mark.parametrize("chassis", [0, 1, 2])
def test_every_chassis_frame_is_valid(chassis: int) -> None:
    model = build_model(default_values() | {"chassis_type": chassis, "powertrain_type": 2},
                        GeometryCache())  # fmt: skip
    frame = next(p for p in model.parts if p.id == "frame")
    assert k.is_valid(model.shapes[frame.geometry])


def test_floor_heights_by_architecture() -> None:
    v = default_values()
    ladder = d.body_floor_height(v | {"chassis_type": 0})
    unibody = d.body_floor_height(v | {"chassis_type": 1})
    skate = d.body_floor_height(v | {"chassis_type": 2, "powertrain_type": 2})
    assert unibody < ladder  # integrated floor structure sits low
    assert skate > unibody  # the battery is under the floor


def test_battery_mass_and_range_follow_the_capacity() -> None:
    v = default_values() | {"powertrain_type": 2, "chassis_type": 2}
    assert d.battery_mass(v | {"battery_capacity": 80}) == pytest.approx(80 / d.PACK_KWH_PER_KG)
    assert d.electric_range(v | {"battery_capacity": 100}) > d.electric_range(
        v | {"battery_capacity": 50}
    )
    assert d.electric_range(v | {"powertrain_type": 0}) == 0
