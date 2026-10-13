"""Suspension derived values follow their textbook relations and the packaging."""

import math

import pytest

from autevra.core import derived as d
from autevra.core.parameters import default_values


def test_sprung_corner_mass_splits_axle_load() -> None:
    p = default_values()
    assert d.sprung_corner_mass(p, "front") == pytest.approx(1600 * 0.55 / 2 - 45)
    assert d.sprung_corner_mass(p, "rear") == pytest.approx(1600 * 0.45 / 2 - 55)


def test_ride_frequency_uses_spring_and_tyre_in_series() -> None:
    p = default_values()
    k = 26 * 200 / (26 + 200) * 1000  # N/m
    expected = math.sqrt(k / d.sprung_corner_mass(p, "front")) / (2 * math.pi)
    assert d.ride_frequency(p, "front") == pytest.approx(expected)
    assert 1.0 < d.ride_frequency(p, "front") < 1.5


def test_damping_ratio_is_fraction_of_critical() -> None:
    p = default_values()
    critical = 2 * math.sqrt(26_000 * d.sprung_corner_mass(p, "front"))
    assert d.damping_ratio(p, "front", "bump") == pytest.approx(1500 / critical)


def test_wire_diameter_reproduces_the_spring_rate() -> None:
    p = default_values()
    wire = d.spring_wire_diameter(p, "front")
    rate = d.SPRING_SHEAR_MODULUS * wire**4 / (8 * 100**3 * d.SPRING_ACTIVE_COILS)
    assert rate == pytest.approx(26)
    assert d.spring_wire_diameter(p | {"front_spring_rate": 52}, "front") > wire


def test_damper_length_is_set_by_the_mounts() -> None:
    p = default_values()
    assert d.damper_installed_length(p, "front") == pytest.approx(
        670 - (d.tyre_radius(p) + d.AXLE_RADIUS)
    )


def test_arch_gap_governs_bump_travel_by_default() -> None:
    p = default_values()
    assert d.available_bump_travel(p, "front") == 35  # arch clearance, not the 60 mm bump stop
    assert d.available_bump_travel(p | {"arch_clearance": 80}, "front") == 60
    assert d.available_rebound_travel(p, "rear") == 70


def test_bigger_wheels_take_damper_travel() -> None:
    """Same ride height, larger tyre: the axle sits higher and the damper is shorter."""
    p = default_values() | {"arch_clearance": 80}
    big = p | {"rim_diameter": 20}
    shorter = d.damper_installed_length(p, "front") - d.damper_installed_length(big, "front")
    assert shorter == pytest.approx(d.tyre_radius(big) - d.tyre_radius(p))
    limits = d.travel_limits(big, "front")
    assert d.available_bump_travel(big, "front") == pytest.approx(limits["damper_compression"][0])
    assert d.available_bump_travel(big, "front") < 60
