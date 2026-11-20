"""Classical laminate theory: ply stiffness, the laminate's A, B, D matrices and its
effective in-plane engineering constants.

Each orthotropic ply (E1, E2, G12, nu12, thickness) has the reduced stiffness Q; rotated by
its angle theta it becomes Q-bar = T^-1 Q T^-T (Reuter form), and through the thickness
A = sum Qbar_k (z_k - z_k-1), B = 1/2 sum Qbar_k (z_k^2 - z_k-1^2),
D = 1/3 sum Qbar_k (z_k^3 - z_k-1^3). For a symmetric laminate (B = 0) the in-plane
constants follow from a = A^-1: Ex = 1 / (h a11), Ey = 1 / (h a22), Gxy = 1 / (h a66),
nu_xy = -a12 / a11. Ply data default to a typical carbon/epoxy (T300-class) unidirectional
ply; strengths and failure (first-ply, Tsai-Wu) are not computed here.
"""

import math

import numpy as np
from pydantic import BaseModel, Field


class Ply(BaseModel):
    angle: float = Field(ge=-90, le=90)
    e1_gpa: float = 181.0
    e2_gpa: float = 10.3
    g12_gpa: float = 7.17
    nu12: float = 0.28
    thickness_mm: float = Field(0.125, gt=0, le=5)


class Laminate(BaseModel):
    plies: list[Ply] = Field(min_length=1, max_length=200)


def q_matrix(p: Ply) -> np.ndarray:
    e1, e2, g12 = p.e1_gpa * 1e3, p.e2_gpa * 1e3, p.g12_gpa * 1e3  # MPa
    nu21 = p.nu12 * e2 / e1
    d = 1 - p.nu12 * nu21
    return np.array([[e1 / d, p.nu12 * e2 / d, 0], [p.nu12 * e2 / d, e2 / d, 0], [0, 0, g12]])


def q_bar(p: Ply) -> np.ndarray:
    c, s = math.cos(math.radians(p.angle)), math.sin(math.radians(p.angle))
    t = np.array([[c * c, s * s, 2 * s * c], [s * s, c * c, -2 * s * c],
                  [-s * c, s * c, c * c - s * s]])  # fmt: skip
    r = np.diag([1.0, 1.0, 2.0])  # Reuter: engineering to tensor shear strain
    return np.linalg.inv(t) @ q_matrix(p) @ r @ t @ np.linalg.inv(r)


def abd(lam: Laminate) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    h = sum(p.thickness_mm for p in lam.plies)
    z = -h / 2
    a, b, d = np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))
    for p in lam.plies:
        z1 = z + p.thickness_mm
        qb = q_bar(p)
        a += qb * (z1 - z)
        b += qb * (z1**2 - z**2) / 2
        d += qb * (z1**3 - z**3) / 3
        z = z1
    return a, b, d, h


def analyse(lam: Laminate) -> dict:
    a, b, d, h = abd(lam)
    ai = np.linalg.inv(a)
    symmetric = bool(np.allclose(b, 0, atol=1e-6 * max(1.0, float(np.abs(a).max()))))
    return {"thickness_mm": h, "symmetric": symmetric,
            "ex_gpa": 1 / (h * ai[0, 0]) / 1e3, "ey_gpa": 1 / (h * ai[1, 1]) / 1e3,
            "gxy_gpa": 1 / (h * ai[2, 2]) / 1e3, "nuxy": -ai[0, 1] / ai[0, 0],
            "A": a.round(1).tolist(), "B": b.round(1).tolist(),
            "D": d.round(1).tolist()}  # fmt: skip
