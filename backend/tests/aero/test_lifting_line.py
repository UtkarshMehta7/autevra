"""Lifting-line theory against its closed-form results."""

import math

import pytest

from autevra.aero import lifting_line as ll


def _elliptic(ar: float = 8.0) -> ll.Planform:
    span = 10.0
    return ll.Planform(span=span, root_chord=4 * span / (math.pi * ar), tip_chord=0.0,
                       elliptic=True)  # fmt: skip


@pytest.mark.parametrize("ar", [4.0, 8.0, 12.0])
def test_an_elliptic_wing_has_e_of_one_and_the_textbook_lift_slope(ar: float) -> None:
    wing = _elliptic(ar)
    assert wing.aspect_ratio == pytest.approx(ar)
    s = ll.solve(wing, 4.0)
    a0 = 2 * math.pi
    assert s.e == pytest.approx(1.0, abs=1e-9)
    assert ll.lift_slope(wing) == pytest.approx(a0 / (1 + a0 / (math.pi * ar)), rel=1e-9)
    assert s.cdi == pytest.approx(s.cl**2 / (math.pi * ar), rel=1e-9)
    # the loading is elliptic: the local lift coefficient is the same at every station
    assert max(s.cl_local) - min(s.cl_local) < 1e-9


def test_taper_near_0_4_gives_the_most_efficient_trapezoid() -> None:
    def e(lam: float) -> float:
        return ll.solve(ll.Planform(10.0, 2 / (1 + lam), 2 * lam / (1 + lam)), 5.0).e

    values = {lam: e(lam) for lam in (0.0, 0.2, 0.4, 0.6, 1.0)}
    assert max(values, key=values.get) == 0.4
    assert values[1.0] == pytest.approx(0.921, abs=0.002)  # rectangular, AR 10 (converged)


def test_the_solution_is_converged_and_linear_in_alpha() -> None:
    wing = ll.Planform(span=11.0, root_chord=1.6, tip_chord=0.9, twist=-2.0, alpha0=-2.08)
    coarse, fine = ll.solve(wing, 6.0, n=40), ll.solve(wing, 6.0, n=160)  # root kink: slower
    assert coarse.cl == pytest.approx(fine.cl, rel=1e-4)
    a, b, c = (ll.solve(wing, x).cl for x in (0.0, 4.0, 8.0))
    assert b - a == pytest.approx(c - b, rel=1e-9)
    # washout unloads the tips: the local lift coefficient falls towards them
    s = ll.solve(wing, 6.0)
    mid = len(s.y) - 1
    assert s.cl_local[0] < s.cl_local[mid]


def test_naca_zero_lift_angles_from_thin_aerofoil_theory() -> None:
    assert ll.naca_section("0012") == (0.0, 2 * math.pi)
    assert ll.naca_section("2412")[0] == pytest.approx(-2.077, abs=0.01)  # published ~ -2.1
    assert ll.naca_section("4412")[0] == pytest.approx(2 * ll.naca_section("2412")[0])


def test_mean_aerodynamic_chord_of_a_trapezoid() -> None:
    wing = ll.Planform(span=10.0, root_chord=2.0, tip_chord=1.0)
    mac, y = wing.mean_aerodynamic_chord()
    assert mac == pytest.approx(2 / 3 * 2 * (1 + 0.5 + 0.25) / 1.5)
    assert y == pytest.approx(10 / 6 * 2 / 1.5)
