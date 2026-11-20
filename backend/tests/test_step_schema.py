"""STEP export in AP214 and AP242, each re-imported with the same geometry."""

from pathlib import Path

import cadquery as cq
import numpy as np
import pytest

from autevra.cad import kernel


@pytest.mark.cad
@pytest.mark.parametrize(("schema", "marker"), [("AP214", "AUTOMOTIVE_DESIGN"),
                                                ("AP242", "AP242_MANAGED_MODEL")])  # fmt: skip
def test_step_schema_round_trip(tmp_path: Path, schema: str, marker: str) -> None:
    box = cq.Workplane().box(10, 20, 30).val()
    path = kernel.export_step([kernel.Part("box", box, np.eye(4), (1.0, 0.0, 0.0))],
                              tmp_path / f"{schema}.step", schema=schema)  # fmt: skip
    assert marker in path.read_text()
    assert kernel.import_step(path).Volume() == pytest.approx(6000.0)


def test_unknown_schema() -> None:
    with pytest.raises(ValueError):
        kernel.export_step([], Path("x.step"), schema="AP999")
