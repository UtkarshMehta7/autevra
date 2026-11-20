"""Clearance matrix: clear, too close, contact and interference."""

import cadquery as cq
import numpy as np
import pytest

from autevra import dmu


def _at(x: float) -> np.ndarray:
    m = np.eye(4)
    m[0, 3] = x
    return m


@pytest.mark.cad
def test_clearance_classes() -> None:
    box = cq.Workplane().box(10, 10, 10).val()
    parts = [dmu.Placed("a", "A", box, _at(0)), dmu.Placed("b", "B", box, _at(13)),
             dmu.Placed("c", "C", box, _at(23)), dmu.Placed("d", "D", box, _at(5)),
             dmu.Placed("e", "E", box, _at(100))]  # fmt: skip
    pairs = {(p.a, p.b): p for p in dmu.matrix(parts, clearance_mm=5.0)}
    assert pairs[("a", "b")].status == "too close"
    assert pairs[("a", "b")].distance_mm == pytest.approx(3)  # A spans -5-5, B 8-18
    assert pairs[("a", "d")].status == "interference"
    assert pairs[("a", "d")].interference_mm3 == pytest.approx(500, rel=1e-3)  # 5 x 10 x 10
    assert pairs[("b", "c")].status == "contact"  # B spans 8-18 and C 18-28: faces touch
    assert pairs[("a", "e")].status == "clear" and not pairs[("a", "e")].exact
