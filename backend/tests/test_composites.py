"""Classical laminate theory against identities of the theory."""

import pytest

from autevra import composites as cl


def _lam(angles: list[float]) -> cl.Laminate:
    return cl.Laminate(plies=[cl.Ply(angle=a) for a in angles])


def test_unidirectional_recovers_the_ply() -> None:
    out = cl.analyse(_lam([0, 0, 0, 0]))
    assert out["ex_gpa"] == pytest.approx(181.0, rel=1e-6)
    assert out["ey_gpa"] == pytest.approx(10.3, rel=1e-6)
    assert out["gxy_gpa"] == pytest.approx(7.17, rel=1e-6)
    assert out["nuxy"] == pytest.approx(0.28, rel=1e-6)
    rotated = cl.analyse(_lam([90, 90]))
    assert rotated["ex_gpa"] == pytest.approx(10.3, rel=1e-6)


def test_quasi_isotropic_is_in_plane_isotropic() -> None:
    out = cl.analyse(_lam([0, 45, -45, 90, 90, -45, 45, 0]))
    assert out["symmetric"]
    assert out["ex_gpa"] == pytest.approx(out["ey_gpa"], rel=1e-9)
    assert out["gxy_gpa"] == pytest.approx(out["ex_gpa"] / (2 * (1 + out["nuxy"])), rel=1e-6)
    assert 60 < out["ex_gpa"] < 80  # carbon/epoxy QI laminates: about 70 GPa


def test_unsymmetric_laminate_couples() -> None:
    assert not cl.analyse(_lam([0, 90]))["symmetric"]
