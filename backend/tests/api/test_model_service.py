"""Model building: de-duplicated geometry, selective rebuild and STEP export."""

import re
from pathlib import Path

import pytest

from autevra.api.model_service import build_model, export_step, mesh_payload
from autevra.cad import kernel
from autevra.cad.cache import GeometryCache
from autevra.domain.parameters import default_values

pytestmark = pytest.mark.cad


def test_four_wheels_share_one_geometry() -> None:
    cache = GeometryCache()
    model = build_model(default_values(), cache)
    wheels = {p.geometry for p in model.parts if p.category == "wheel"}
    assert len(wheels) == 1
    # body, frame, one axle shape (equal tracks), one wheel shape
    assert sorted(cache.stats.builds) == ["axle", "body", "frame", "wheel"]
    payload = mesh_payload(model, cache)
    assert len(payload["geometries"]) == 4
    assert len(payload["parts"]) == 8


def test_wheelbase_change_rebuilds_only_body_and_frame() -> None:
    cache = GeometryCache()
    p = default_values()
    build_model(p, cache)
    cache.reset_stats()
    build_model(p | {"wheelbase": 2800}, cache)
    assert sorted(cache.stats.builds) == ["body", "frame"]


def test_unchanged_design_rebuilds_nothing() -> None:
    cache = GeometryCache()
    build_model(default_values(), cache)
    cache.reset_stats()
    build_model(default_values(), cache)
    assert cache.stats.builds == []


def _step_bounds(path: Path) -> tuple[tuple[float, ...], tuple[float, ...]]:
    return kernel.bounds(kernel.import_step(path))


def test_step_export_reflects_wheelbase(tmp_path: Path) -> None:
    cache = GeometryCache()
    p = default_values()
    a = export_step(build_model(p, cache), tmp_path / "a.step")
    b = export_step(build_model(p | {"wheelbase": 2800}, cache), tmp_path / "b.step")
    (alo, ahi), (blo, bhi) = _step_bounds(a), _step_bounds(b)
    assert alo[0] == pytest.approx(-3700, abs=0.01)
    assert blo[0] == pytest.approx(-3800, abs=0.01)
    assert ahi[0] == pytest.approx(bhi[0], abs=0.01)
    names = set(re.findall(r"'(wheel_[a-z]{2}|body|frame|front_axle|rear_axle)'", a.read_text()))
    assert names == {
        "body",
        "frame",
        "front_axle",
        "rear_axle",
        "wheel_fl",
        "wheel_fr",
        "wheel_rl",
        "wheel_rr",
    }
