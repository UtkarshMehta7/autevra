"""Interior: seats per row, driving side, trim and packaging inside the cabin."""

import pytest

from autevra.cad import kernel as k
from autevra.core.parameters import default_values
from autevra.domains.automotive import interior as i
from autevra.domains.automotive import vehicle

pytestmark = pytest.mark.cad


def _inputs(**changes: float) -> dict[str, float]:
    p = default_values() | changes
    return vehicle._interior_inputs(p)


@pytest.mark.parametrize("rows", [1, 2])
def test_two_seats_per_row(rows: int) -> None:
    seats = i.build_seats(_inputs(seat_rows=rows))
    assert k.is_valid(seats) and k.solid_count(seats) == 2 * rows


def test_the_steering_wheel_follows_the_driving_side() -> None:
    (_, y0, _), (_, y1, _) = k.bounds(i.build_steering_wheel(_inputs(driving_side=0)))
    assert (y0 + y1) / 2 > 200  # left-hand drive: driver on the left (+Y, ISO 8855)
    (_, y0, _), (_, y1, _) = k.bounds(i.build_steering_wheel(_inputs(driving_side=1)))
    assert (y0 + y1) / 2 < -200


@pytest.mark.parametrize("trim", [0, 1, 2])
def test_every_interior_part_sits_inside_the_cabin(trim: int) -> None:
    p = _inputs(interior_trim=trim)
    c = i.cabin(p)
    for build in (i.build_seats, i.build_dashboard, i.build_display, i.build_steering_wheel,
                  i.build_console):  # fmt: skip
        part = build(p)
        assert k.is_valid(part)
        (x0, y0, z0), (x1, y1, z1) = k.bounds(part)
        assert c.rear - 120 <= x0 and x1 <= c.cowl, build.__name__  # recline may lean back
        assert -c.half_w - 1 <= y0 and y1 <= c.half_w + 1, build.__name__
        assert c.floor - 1 <= z0 and z1 <= c.roof, build.__name__


def test_premium_has_the_wide_display_and_standard_the_small_one() -> None:
    small = k.volume(i.build_display(_inputs(interior_trim=0)))
    wide = k.volume(i.build_display(_inputs(interior_trim=2)))
    assert wide > 3 * small


def test_upholstery_colour_is_appearance_only() -> None:
    from autevra.api.model_service import build_model
    from autevra.cad.cache import GeometryCache

    cache = GeometryCache()
    values = default_values()
    build_model(values, cache)
    cache.reset_stats()
    parts = {p.id: p for p in build_model(values | {"interior_colour": 4}, cache).parts}
    assert cache.stats.builds == []
    assert parts["seats"].color == vehicle.UPHOLSTERY[4]
