"""Hole wizard (ISO metric), slot and draft features: removed volumes against closed
forms, the table values and the callouts."""

import math

import pytest

from autevra.part import holes
from autevra.part.build import build_part
from autevra.part.features import PartDoc

BLOCK = {"id": "block", "type": "box", "size": [80, 60, 30], "at": {"z": 15}}
V0 = 80 * 60 * 30


def removed(feature: dict) -> tuple[float, dict]:
    built = build_part(PartDoc.model_validate({"features": [BLOCK, feature]}))
    assert not built.errors, built.errors
    assert built.shape is not None and built.shape.isValid()
    return V0 - built.shape.Volume(), built.info.get(feature["id"], {})


def test_simple_blind_hole_with_drill_point():
    v, info = removed({"id": "h", "type": "hole", "diameter": 8, "depth": 15, "at": {"z": 30}})
    cone = math.pi * 16 * (4 / math.tan(math.radians(59))) / 3
    assert v == pytest.approx(math.pi * 16 * 15 + cone, rel=1e-6)
    assert info["callout"] == "⌀8"


def test_flat_bottom_hole():
    v, _ = removed(
        {"id": "h", "type": "hole", "diameter": 10, "depth": 12, "bottom": "flat", "at": {"z": 30}}
    )
    assert v == pytest.approx(math.pi * 25 * 12, rel=1e-6)


@pytest.mark.parametrize(("fit", "d"), [("fine", 8.4), ("medium", 9.0), ("coarse", 10.0)])
def test_clearance_hole_iso_273(fit, d):
    v, info = removed(
        {
            "id": "h",
            "type": "hole",
            "kind": "clearance",
            "size": "M8",
            "fit": fit,
            "through": True,
            "at": {"z": 30},
        }
    )
    assert v == pytest.approx(math.pi * (d / 2) ** 2 * 30, rel=1e-6)
    assert info["drill"] == d


def test_tapped_hole_tap_drill_and_thread_depth():
    v, info = removed(
        {
            "id": "h",
            "type": "hole",
            "kind": "tapped",
            "size": "M10",
            "depth": 20,
            "bottom": "flat",
            "at": {"z": 30},
        }
    )
    assert v == pytest.approx(math.pi * 4.25**2 * 20, rel=1e-6)
    assert info["thread"] == "M10×1.5"
    assert info["thread_depth"] == pytest.approx(17.0)


def test_counterbore_din_974():
    v, info = removed(
        {
            "id": "h",
            "type": "hole",
            "kind": "counterbore",
            "size": "M8",
            "through": True,
            "at": {"z": 30},
        }
    )
    assert info["cbore_diameter"] == 15.0 and info["cbore_depth"] == 8.4
    expected = math.pi * 7.5**2 * 8.4 + math.pi * 4.5**2 * (30 - 8.4)
    assert v == pytest.approx(expected, rel=1e-6)
    assert "⌴⌀15" in str(info["callout"])


def test_countersink_cone():
    v, info = removed(
        {
            "id": "h",
            "type": "hole",
            "kind": "countersink",
            "size": "M6",
            "through": True,
            "at": {"z": 30},
        }
    )
    r, rs = 3.3, 13.44 / 2
    h = rs - r  # 90 degrees: cone height = radius difference
    cone = math.pi * h * (rs**2 + rs * r + r**2) / 3
    assert v == pytest.approx(cone + math.pi * r**2 * (30 - h), rel=1e-6)
    assert info["csink_diameter"] == 13.44


def test_hole_errors():
    built = build_part(
        PartDoc.model_validate(
            {
                "features": [
                    BLOCK,
                    {
                        "id": "h",
                        "type": "hole",
                        "kind": "counterbore",
                        "size": "M8",
                        "depth": 5,
                        "cbore_depth": 8,
                        "at": {"z": 30},
                    },
                ]
            }
        )
    )
    assert built.errors and "counterbore" in built.errors[0].message
    with pytest.raises(ValueError):
        holes.size("M7")


def test_slot_volume():
    v, _ = removed(
        {"id": "h", "type": "slot", "length": 40, "width": 10, "depth": 8, "at": {"z": 30}}
    )
    assert v == pytest.approx((30 * 10 + math.pi * 25) * 8, rel=1e-6)


def test_draft_tapers_sides_towards_the_pull():
    built = build_part(
        PartDoc.model_validate({"features": [BLOCK, {"id": "d", "type": "draft", "angle": 3}]})
    )
    assert not built.errors
    shape = built.shape
    top = max(shape.Faces(), key=lambda fc: fc.Center().z)
    bb = top.BoundingBox()
    shrink = 2 * 30 * math.tan(math.radians(3))
    assert bb.xlen == pytest.approx(80 - shrink, abs=1e-3)
    assert bb.ylen == pytest.approx(60 - shrink, abs=1e-3)
    assert shape.BoundingBox().xlen == pytest.approx(80, abs=1e-6)  # base on the neutral plane


def test_draft_needs_parallel_faces():
    built = build_part(
        PartDoc.model_validate(
            {
                "features": [
                    {"id": "s", "type": "sphere", "radius": 20},
                    {"id": "d", "type": "draft", "angle": 2},
                ]
            }
        )
    )
    assert built.errors and "parallel" in built.errors[0].message


def test_draft_cylinder():
    built = build_part(
        PartDoc.model_validate(
            {
                "features": [
                    {"id": "c", "type": "cylinder", "radius": 30, "height": 40, "at": {"z": 20}},
                    {"id": "d", "type": "draft", "angle": 5},
                ]
            }
        )
    )
    assert not built.errors
    r_top = 30 - 40 * math.tan(math.radians(5))
    h = 40
    frustum = math.pi * h * (30**2 + 30 * r_top + r_top**2) / 3
    assert built.shape.Volume() == pytest.approx(frustum, rel=1e-6)
