import pytest

from autevra.domain import derived
from autevra.domain.parameters import default_values


def test_overall_length_is_sum_of_wheelbase_and_overhangs() -> None:
    assert derived.overall_length(default_values()) == 4600


def test_tyre_geometry_225_50_r17() -> None:
    p = default_values()
    assert derived.tyre_sidewall(p) == pytest.approx(112.5)
    # 17 in * 25.4 + 2 * 112.5 = 656.8 mm
    assert derived.tyre_diameter(p) == pytest.approx(656.8)
    assert derived.tyre_radius(p) == pytest.approx(328.4)
    assert derived.arch_top_height(p) == pytest.approx(328.4 + 363.4)


def test_body_and_cabin_ranges() -> None:
    p = default_values()
    assert derived.body_x_range(p) == (-3700, 900)
    # Body centre -1400, cabin offset -150, half length 1250.
    assert derived.cabin_x_range(p) == (-2800, -300)


def test_compute_all_lists_every_derived_value() -> None:
    values = derived.compute_all(default_values())
    assert set(values) == set(derived.DERIVED)
    assert derived.DERIVED["overall_length"].controlled_by == (
        "front_overhang",
        "wheelbase",
        "rear_overhang",
    )
