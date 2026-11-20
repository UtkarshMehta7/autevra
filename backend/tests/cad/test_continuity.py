"""Continuity analysis against joins built to a known continuity."""

import numpy as np
import pytest

from autevra.geometry import continuity as ct
from autevra.geometry import nurbs as nb


def patch(nu: int = 5, nv: int = 4, p: int = 3) -> nb.Surface:
    ctrl = [[[i * 20.0, j * 25.0, 8.0 * np.sin(i * 0.9) + 3.0 * j] for j in range(nv)]
            for i in range(nu)]  # fmt: skip
    return nb.Surface.build(p, 2, ctrl)


@pytest.mark.parametrize(("target", "level"), [("G0", "G0"), ("G1", "G1"), ("G2", "G2")])
def test_joins_measure_as_built(target: str, level: str) -> None:
    a = patch()
    b = ct.join(a, target, bend=15.0)  # B bends away beyond what its continuity fixes
    report = ct.analyse(a, b)
    assert report.gap < 1e-9
    assert report.level == level, report
    if target == "G0":
        assert report.angle > 1.0
    if target == "G1":
        assert report.angle < 1e-6 and report.curvature_jump > 1e-4
    if target == "G2":
        assert report.curvature_jump < 1e-9


def test_a_gap_is_not_even_g0() -> None:
    a = patch()
    b = ct.join(a, "G2")
    b.control[:, :, 2] += 1.0  # lift B off A
    assert ct.analyse(a, b).level == "none"


def test_a_comb_follows_the_normal_curvature() -> None:
    r = 50.0
    s = 2**-0.5
    arc = [[r, 0.0], [r, r], [0.0, r]]
    cyl = nb.Surface.build(2, 1, [[[x, y, z] for z in (0.0, 30.0)] for x, y in arc],
                           [[1, 1], [s, s], [1, 1]])  # fmt: skip
    teeth = ct.comb(cyl, 0.5, samples=9)
    assert all(abs(abs(k) - 1 / r) < 1e-9 for k in teeth["curvature"])
