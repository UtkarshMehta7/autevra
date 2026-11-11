"""SIMP topology optimisation against the textbook benchmark."""

import numpy as np
import pytest

from autevra.fea import simp


def test_q4_element_is_symmetric_with_three_rigid_body_modes() -> None:
    k = simp.q4_stiffness(0.3)
    assert np.allclose(k, k.T)
    eig = np.linalg.eigvalsh(k)
    assert np.sum(np.abs(eig) < 1e-10) == 3 and eig.min() > -1e-10
    assert k[0, 0] == pytest.approx(0.4945054945, rel=1e-6)  # Sigmund's KE(1)


def test_hex_element_has_six_rigid_body_modes() -> None:
    eig = np.linalg.eigvalsh(simp.hex_stiffness(0.3))
    assert np.sum(np.abs(eig) < 1e-10) == 6 and eig.min() > -1e-10


def test_the_mbb_beam_matches_the_99_line_code() -> None:
    """Sigmund (2001), 60 x 20, volume 0.5, penalty 3, rmin 1.5: compliance about 203."""
    r = simp.optimise(simp.preset("mbb", (60, 20)), volfrac=0.5, penal=3.0, rmin=1.5,
                      max_iter=200)  # fmt: skip
    assert r.stats["converged"]
    assert r.stats["final_compliance"] == pytest.approx(203.0, rel=0.01)
    assert r.stats["volume_fraction"] == pytest.approx(0.5, abs=1e-3)
    comp = [h["compliance"] for h in r.history]
    assert comp[-1] < 0.5 * comp[0]  # the optimiser does reduce compliance
    x = r.density.reshape(20, 60)
    assert x[19, 0] > 0.9 and x[0, 59] > 0.9  # material at the load and at the support


@pytest.mark.parametrize("case", ["cantilever", "bridge", "bracket"])
def test_every_preset_runs_in_2d(case: str) -> None:
    r = simp.optimise(simp.preset(case, (30, 12)), volfrac=0.4, max_iter=30)
    assert r.stats["volume_fraction"] == pytest.approx(0.4, abs=2e-3)
    assert r.history[-1]["compliance"] < r.history[0]["compliance"]


def test_a_3d_cantilever_optimises() -> None:
    r = simp.optimise(simp.preset("cantilever", (16, 6, 4)), volfrac=0.3, max_iter=25)
    assert r.stats["volume_fraction"] == pytest.approx(0.3, abs=2e-3)
    assert r.history[-1]["compliance"] < 0.6 * r.history[0]["compliance"]
    assert len(r.density) == 16 * 6 * 4


def test_oversized_domains_are_refused() -> None:
    with pytest.raises(ValueError):
        simp.optimise(simp.preset("mbb", (300, 100)))
