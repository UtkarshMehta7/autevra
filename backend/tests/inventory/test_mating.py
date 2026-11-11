import numpy as np
import pytest

from autevra.inventory import mating
from autevra.inventory.model import Port
from autevra.inventory.standard import catalogue


@pytest.mark.parametrize("at", [{}, {"x": 5, "y": -3, "z": 7, "rx": 30, "ry": -20, "rz": 75},
                                {"rx": 90}, {"ry": 45, "rz": 180}])  # fmt: skip
def test_placement_round_trips(at: dict) -> None:
    m = mating.matrix(at)
    assert np.allclose(mating.matrix(mating.placement(m)), m, atol=1e-9)


def test_mated_port_frames_coincide() -> None:
    target = Port(name="t", kind="mechanical.bore", at={"x": 10, "z": 5, "rx": 90})
    own = Port(name="o", kind="mechanical.shaft", at={"z": -20})
    part_at = {"x": 100, "rz": 30}
    s = mating.mate(part_at, target, own)
    world_target = mating.matrix(part_at) @ mating.matrix(target.at)
    world_own = mating.matrix(s) @ mating.matrix(own.at)
    assert np.allclose(world_own, world_target, atol=1e-6)


def test_compatibility_rules() -> None:
    cat = catalogue()
    bolt = next(p for p in cat["iso4762-m10x40"].ports if p.name == "thread")
    nut10 = cat["iso4032-m10"].ports[0]
    nut12 = cat["iso4032-m12"].ports[0]
    washer10 = cat["iso7089-m10"].ports[0]
    washer24 = cat["iso7089-m24"].ports[0]
    bore = next(p for p in cat["bearing-6205"].ports if p.name == "bore")
    assert mating.compatible(nut10, bolt)[0]
    assert not mating.compatible(nut12, bolt)[0]
    assert mating.compatible(washer10, bolt)[0]
    assert not mating.compatible(washer24, bolt)[0]  # too loose
    assert not mating.compatible(bore, bolt)[0]  # a 25 mm bore is far too loose for M10
    assert "cannot mate" in mating.compatible(
        Port(name="a", kind="mechanical.seat"), bolt)[1]  # fmt: skip
