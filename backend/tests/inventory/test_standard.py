"""Standard parts: dimensions, calculations against hand values, and buildable geometry."""

import math

import pytest

from autevra.inventory import calc
from autevra.inventory.standard import catalogue
from autevra.part.build import build_part
from autevra.part.features import PartDoc


def test_stress_area_matches_iso_898_tables() -> None:
    # ISO 898-1 tabulates As = 58.0 mm² for M10 and 84.3 mm² for M12
    assert calc.stress_area(10, 1.5) == pytest.approx(58.0, abs=0.1)
    assert calc.stress_area(12, 1.75) == pytest.approx(84.3, abs=0.1)


def test_bolt_preload_and_torque_by_hand() -> None:
    cap = calc.bolt_capacity(10, 1.5, "8.8")
    preload = 0.7 * 640 * calc.stress_area(10, 1.5)  # N
    assert cap["preload_kN"] == pytest.approx(preload / 1e3)
    assert cap["torque_Nm"] == pytest.approx(0.2 * preload * 10 / 1e3)  # about 52 N·m
    assert 45 < cap["torque_Nm"] < 60


def test_bearing_life_iso_281() -> None:
    life = calc.bearing_life(14.8, 1.48, 1000)  # C / P = 10
    assert life["L10_Mrev"] == pytest.approx(1000.0)
    assert life["L10_hours"] == pytest.approx(1000e6 / 60_000)
    roller = calc.bearing_life(10, 5, 100, roller=True)
    assert roller["L10_Mrev"] == pytest.approx(2 ** (10 / 3))
    with pytest.raises(ValueError):
        calc.bearing_life(10, 0, 100)


def test_hollow_section_properties() -> None:
    s = calc.shs(40, 3)
    assert s["area_mm2"] == pytest.approx(40**2 - 34**2)
    assert s["I_mm4"] == pytest.approx((40**4 - 34**4) / 12)
    c = calc.chs(48.3, 3.2)
    assert c["area_mm2"] == pytest.approx(math.pi / 4 * (48.3**2 - 41.9**2))
    with pytest.raises(ValueError):
        calc.shs(10, 6)


def test_catalogue_contents() -> None:
    cat = catalogue()
    assert len(cat) > 200
    assert {"iso4762-m10x40", "iso4017-m8x30", "iso4032-m10", "iso7089-m10", "bearing-6205",
            "shs-40x40x3", "chs-48.3x3.2"} <= set(cat)  # fmt: skip
    b = cat["bearing-6205"]
    assert b.parameters["d"] == 25 and b.parameters["D"] == 52 and b.performance["C_kN"] == 14.8
    assert 0.1 < b.properties["mass_kg"] < 0.16  # catalogue mass of a 6205 is about 0.13 kg
    assert {p.kind for p in cat["iso4762-m10x40"].ports} == {"mechanical.seat", "mechanical.thread"}


@pytest.mark.cad
@pytest.mark.parametrize("item_id", ["iso4762-m10x40", "iso4017-m8x30", "iso4032-m10",
                                     "iso7089-m10", "bearing-6205", "shs-40x40x3",
                                     "chs-48.3x3.2"])  # fmt: skip
def test_every_family_builds(item_id: str) -> None:
    out = build_part(PartDoc.model_validate(catalogue()[item_id].definition))
    assert not out.errors, out.errors
