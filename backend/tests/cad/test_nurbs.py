"""NURBS mathematics: basis properties, exact conics, knot insertion, derivatives, and a
cross-check against Open CASCADE's B-spline surfaces."""

import math

import numpy as np
import pytest

from autevra.geometry import nurbs as nb


def wavy(nu: int = 5, nv: int = 4, p: int = 3, q: int = 2) -> nb.Surface:
    rng = np.random.default_rng(3)
    ctrl = [[[i * 10.0, j * 10.0, float(rng.uniform(-4, 4))] for j in range(nv)] for i in range(nu)]
    w = rng.uniform(0.5, 2.0, (nu, nv))
    return nb.Surface.build(p, q, ctrl, w)


def test_basis_functions_are_a_partition_of_unity_with_local_support() -> None:
    knots = np.asarray([0, 0, 0, 0.2, 0.5, 0.5, 0.8, 1, 1, 1], dtype=float)
    p, count = 2, 7
    for u in np.linspace(0, 1, 37):
        vals = [nb.basis(i, p, knots, float(u)) for i in range(count)]
        assert sum(vals) == pytest.approx(1.0)
        assert min(vals) >= -1e-12
        for i, val in enumerate(vals):  # N_i,p is zero outside [U_i, U_i+p+1)
            if not knots[i] <= u <= knots[i + p + 1]:
                assert val == 0.0
    span = nb.find_span(count - 1, p, 0.6, knots)
    ders = nb.basis_ders(span, 0.6, p, knots, 1)
    assert ders[0].sum() == pytest.approx(1.0) and ders[1].sum() == pytest.approx(0.0, abs=1e-12)


def test_a_rational_quarter_circle_cylinder_is_exact() -> None:
    r, h, s = 50.0, 80.0, math.sqrt(0.5)
    arc = [[r, 0.0], [r, r], [0.0, r]]
    ctrl = [[[x, y, z] for z in (0.0, h)] for x, y in arc]
    weights = [[1.0, 1.0], [s, s], [1.0, 1.0]]
    surf = nb.Surface.build(2, 1, ctrl, weights)
    for u in np.linspace(0, 1, 9):
        for v in (0.0, 0.5, 1.0):
            pt = surf.point(float(u), v)
            assert math.hypot(pt[0], pt[1]) == pytest.approx(r, abs=1e-9)
            fr = surf.frame(float(u), v)
            assert fr["gaussian"] == pytest.approx(0.0, abs=1e-9)
            assert abs(fr["mean"]) == pytest.approx(1 / (2 * r), rel=1e-6)


def test_knot_insertion_adds_control_points_and_keeps_the_surface() -> None:
    surf = wavy()
    more = surf.insert_knot_u(0.37).insert_knot_v(0.61)
    assert more.control.shape[:2] == (surf.control.shape[0] + 1, surf.control.shape[1] + 1)
    for u in np.linspace(0, 1, 7):
        for v in np.linspace(0, 1, 7):
            assert more.point(float(u), float(v)) == pytest.approx(
                surf.point(float(u), float(v)), abs=1e-9
            )


def test_derivatives_match_finite_differences() -> None:
    surf, u, v, h = wavy(), 0.43, 0.29, 1e-6
    skl = surf.derivatives(u, v, 2)
    du = (surf.point(u + h, v) - surf.point(u - h, v)) / (2 * h)
    dv = (surf.point(u, v + h) - surf.point(u, v - h)) / (2 * h)
    duu = (surf.point(u + 1e-4, v) - 2 * surf.point(u, v) + surf.point(u - 1e-4, v)) / 1e-8
    assert skl[1, 0] == pytest.approx(du, rel=1e-5, abs=1e-6)
    assert skl[0, 1] == pytest.approx(dv, rel=1e-5, abs=1e-6)
    assert skl[2, 0] == pytest.approx(duu, rel=1e-3, abs=1e-3)


def test_bad_definitions_are_rejected() -> None:
    with pytest.raises(nb.NurbsError):
        nb.Surface.build(3, 1, [[[0, 0, 0], [0, 1, 0]], [[1, 0, 0], [1, 1, 0]]])  # too few in u
    with pytest.raises(nb.NurbsError):
        nb.Surface.build(1, 1, [[[0, 0, 0], [0, 1, 0]], [[1, 0, 0], [1, 1, 0]]], [[1, 1], [1, -1]])
    with pytest.raises(nb.NurbsError):
        nb.check_knots([0, 0, 1, 0.5, 1], 3, 1)


@pytest.mark.cad
def test_evaluation_matches_open_cascade() -> None:
    from OCP.Geom import Geom_BSplineSurface
    from OCP.gp import gp_Pnt
    from OCP.TColgp import TColgp_Array2OfPnt
    from OCP.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal, TColStd_Array2OfReal

    surf = wavy().insert_knot_u(0.4)  # a non-uniform knot vector
    nu, nv = surf.weights.shape
    poles, weights = TColgp_Array2OfPnt(1, nu, 1, nv), TColStd_Array2OfReal(1, nu, 1, nv)
    for i in range(nu):
        for j in range(nv):
            poles.SetValue(i + 1, j + 1, gp_Pnt(*surf.control[i, j]))
            weights.SetValue(i + 1, j + 1, float(surf.weights[i, j]))

    def occ_knots(knots: list[float]) -> tuple:
        values = sorted(set(knots))
        k, m = TColStd_Array1OfReal(1, len(values)), TColStd_Array1OfInteger(1, len(values))
        for i, t in enumerate(values):
            k.SetValue(i + 1, t)
            m.SetValue(i + 1, sum(1 for x in knots if x == t))
        return k, m

    (ku, mu), (kv, mv) = occ_knots(surf.knots_u), occ_knots(surf.knots_v)
    occ = Geom_BSplineSurface(poles, weights, ku, kv, mu, mv, surf.degree_u, surf.degree_v)
    rng = np.random.default_rng(11)
    for u, v in rng.uniform(0, 1, (25, 2)):
        p = occ.Value(float(u), float(v))
        assert surf.point(float(u), float(v)) == pytest.approx([p.X(), p.Y(), p.Z()], abs=1e-9)
