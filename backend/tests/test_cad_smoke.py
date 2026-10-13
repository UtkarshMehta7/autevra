"""Smoke test: the CAD kernel builds a solid and writes a valid STEP file."""

from pathlib import Path

import cadquery as cq
import pytest

pytestmark = pytest.mark.cad


def test_cadquery_builds_filleted_solid_and_exports_step(tmp_path: Path) -> None:
    solid = cq.Workplane("XY").box(100, 60, 40).edges("|Z").fillet(5)
    shape = solid.val()
    assert shape.isValid()
    # Box volume minus four fillet corners: 100*60*40 - 4 * (5^2 - pi*5^2/4) * 40
    expected = 100 * 60 * 40 - 4 * (25 - 3.141592653589793 * 25 / 4) * 40
    assert shape.Volume() == pytest.approx(expected, rel=1e-6)

    path = tmp_path / "smoke.step"
    cq.exporters.export(solid, str(path))
    text = path.read_text()
    assert text.startswith("ISO-10303-21;")
    assert "MANIFOLD_SOLID_BREP" in text

    reimported = cq.importers.importStep(str(path)).val()
    assert reimported.Volume() == pytest.approx(expected, rel=1e-6)
