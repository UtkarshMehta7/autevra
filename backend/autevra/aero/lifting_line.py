"""Prandtl's lifting-line theory, solved by Glauert's Fourier-series method.

A straight (unswept quarter-chord) wing of span b is modelled as a bound vortex line with a
spanwise circulation Gamma(y). With the spanwise station y = -(b/2) cos(theta) and

    Gamma(theta) = 2 b V sum_n A_n sin(n theta)         (n odd for a symmetric wing),

the lifting-line equation at each station becomes, with c the local chord, a the local
two-dimensional lift-curve slope and alpha the local geometric angle of attack (including
twist) measured from the section's zero-lift angle alpha_0:

    alpha - alpha_0 = sum_n A_n sin(n theta) (4 b / (a c) + n / sin(theta))

which is solved in a least-squares sense at N collocation stations (N unknowns: an exact
solve). Then

    C_L  = pi AR A_1
    C_Di = pi AR sum_n n A_n^2 = C_L^2 / (pi AR e),   e = 1 / (1 + delta),
    delta = sum_{n>1} n (A_n / A_1)^2,

and the local lift coefficient is c_l(y) = 2 Gamma / (V c). For an elliptic planform every
A_n but A_1 vanishes, so e = 1 and C_L,alpha = a / (1 + a / (pi AR)): the classic results the
solver is checked against.

Limits (stated with every result): incompressible, attached flow, high aspect ratio
(AR >~ 4), no sweep correction beyond the planform, linear section lift (no stall).
"""

import math
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Planform:
    """A trapezoidal (or elliptic) wing, one side mirrored. Lengths in metres, angles in
    degrees. Twist is the tip's incidence relative to the root (negative: washout), linear
    along the span. ``alpha0`` is the section zero-lift angle (negative for cambered
    sections); ``a0`` the section lift-curve slope per radian (2 pi thin-aerofoil)."""

    span: float
    root_chord: float
    tip_chord: float
    twist: float = 0.0
    alpha0: float = 0.0
    a0: float = 2.0 * math.pi
    elliptic: bool = False

    @property
    def area(self) -> float:
        if self.elliptic:
            return math.pi * self.span * self.root_chord / 4.0
        return self.span * (self.root_chord + self.tip_chord) / 2.0

    @property
    def aspect_ratio(self) -> float:
        return self.span**2 / self.area

    @property
    def taper(self) -> float:
        return self.tip_chord / self.root_chord

    def chord(self, y: np.ndarray) -> np.ndarray:
        eta = np.abs(2.0 * y / self.span)
        if self.elliptic:
            return self.root_chord * np.sqrt(np.clip(1.0 - eta**2, 0.0, 1.0))
        return self.root_chord + (self.tip_chord - self.root_chord) * eta

    def mean_aerodynamic_chord(self) -> tuple[float, float]:
        """(MAC, its spanwise station y) of the trapezoid: (2/3) c_r (1 + l + l^2)/(1 + l)."""
        lam = self.taper
        mac = 2.0 / 3.0 * self.root_chord * (1 + lam + lam**2) / (1 + lam)
        y = self.span / 6.0 * (1 + 2 * lam) / (1 + lam)
        return mac, y


@dataclass
class Solution:
    alpha: float  # degrees
    cl: float
    cdi: float
    e: float
    coefficients: np.ndarray  # A_n for n = 1, 3, 5, ...
    y: np.ndarray  # stations, m
    cl_local: np.ndarray  # local lift coefficient
    circulation: np.ndarray  # Gamma / (b V), dimensionless
    stats: dict = field(default_factory=dict)


def solve(wing: Planform, alpha: float, n: int = 40) -> Solution:
    """The lift distribution at angle of attack ``alpha`` (degrees, at the root)."""
    k = np.arange(1, n + 1)
    theta = k * math.pi / (2 * n + 1)  # (0, pi/2]: one half of the symmetric wing
    theta = theta[theta <= math.pi / 2 + 1e-12]
    odd = 2 * np.arange(len(theta)) + 1  # n = 1, 3, 5, ...
    y = -wing.span / 2.0 * np.cos(theta)
    c = wing.chord(y)
    eta = np.abs(2.0 * y / wing.span)
    local = np.radians(alpha + wing.twist * eta - wing.alpha0)
    sin_nt = np.sin(np.outer(theta, odd))
    m = sin_nt * (4.0 * wing.span / (wing.a0 * c))[:, None] + sin_nt * odd / np.sin(theta)[:, None]
    coef = np.linalg.solve(m, local)
    ar = wing.aspect_ratio
    cl = math.pi * ar * coef[0]
    cdi = math.pi * ar * float(np.sum(odd * coef**2))
    delta = float(np.sum(odd[1:] * (coef[1:] / coef[0]) ** 2)) if coef[0] != 0 else 0.0
    gamma = 2.0 * (sin_nt @ coef)  # Gamma / (b V)
    cl_local = 2.0 * gamma * wing.span / c
    return Solution(alpha, cl, cdi, 1.0 / (1.0 + delta), coef, y, cl_local, gamma, {
        "stations": len(theta), "area": wing.area, "aspect_ratio": ar,
        "residual": float(np.linalg.norm(m @ coef - local)),
    })  # fmt: skip


def lift_slope(wing: Planform) -> float:
    """dC_L/d alpha per radian (the solution is linear in alpha)."""
    return (solve(wing, 1.0).cl - solve(wing, 0.0).cl) / math.radians(1.0)


def naca_section(code: str) -> tuple[float, float]:
    """(zero-lift angle in degrees, lift-curve slope per radian) of a NACA four-digit
    section by thin-aerofoil theory: alpha_0 = -(1/pi) integral of dz/dx (cos t - 1) dt on
    the mean line; a_0 = 2 pi (thickness effects ignored)."""
    m, p = int(code[0]) / 100.0, int(code[1]) / 10.0
    if m == 0.0:
        return 0.0, 2.0 * math.pi
    t = np.linspace(0.0, math.pi, 4001)
    x = 0.5 * (1 - np.cos(t))
    slope = np.where(x < p, 2 * m / p**2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x))
    a0 = -np.trapezoid(slope * (np.cos(t) - 1.0), t) / math.pi
    return math.degrees(a0), 2.0 * math.pi
