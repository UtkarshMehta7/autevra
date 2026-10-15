import math

import pytest

from autevra.cad import kernel as k
from autevra.part import features as f
from autevra.part.build import build_part, sheet_flat

pytestmark = pytest.mark.cad


def _sheet(**fields: object) -> f.SheetMetal:
    return f.SheetMetal.model_validate({"id": "s", **fields})


def test_u_channel_flat_length_uses_the_k_factor_bend_allowance() -> None:
    s = _sheet(points=[[0, 50], [0, 0], [100, 0], [100, 50]], thickness=2, bend_radius=2,
               width=80, k_factor=0.44)  # fmt: skip
    flat, angles, setbacks = sheet_flat(s)
    assert angles == pytest.approx([90, 90]) and setbacks == pytest.approx([3, 3])
    expected = (50 - 3) + (100 - 6) + (50 - 3) + 2 * (math.pi / 2) * (2 + 0.44 * 2)
    assert flat == pytest.approx(expected)


def test_the_solid_is_the_mid_plane_length_times_thickness_and_width() -> None:
    s = _sheet(points=[[0, 50], [0, 0], [100, 0], [100, 50]], thickness=2, bend_radius=2, width=80)
    result = build_part(f.PartDoc(features=[s]))
    assert not result.errors and k.solid_count(result.shape) == 1
    mid_length = 188 + 2 * (math.pi / 2) * 3  # straight + mid-plane arcs (R = r + t/2)
    assert k.volume(result.shape) == pytest.approx(mid_length * 2 * 80, rel=1e-4)
    assert result.info["s"]["bends"] == 2 and result.info["s"]["flat_width"] == 80


def test_a_flat_strip_has_no_bends() -> None:
    flat, angles, _ = sheet_flat(_sheet(points=[[0, 0], [120, 0]]))
    assert flat == pytest.approx(120) and angles == []


def test_a_bend_radius_too_large_for_a_flange_is_reported() -> None:
    s = _sheet(points=[[0, 5], [0, 0], [100, 0]], thickness=2, bend_radius=10)
    result = build_part(f.PartDoc(features=[s]))
    assert result.errors and "bend radius too large for flange 1" in result.errors[0].message


def test_zero_length_flanges_are_rejected() -> None:
    with pytest.raises(ValueError):
        _sheet(points=[[0, 0], [0, 0], [10, 0]])
