"""4 x 4 homogeneous transforms (row-major, translation in the last column, mm)."""

import math

import numpy as np

Matrix = np.ndarray


def identity() -> Matrix:
    return np.eye(4)


def translation(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Matrix:
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def rotation_z(degrees: float) -> Matrix:
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    m = np.eye(4)
    m[:2, :2] = ((c, -s), (s, c))
    return m


def compose(*matrices: Matrix) -> Matrix:
    out = np.eye(4)
    for m in matrices:
        out = out @ m
    return out


def inverse(m: Matrix) -> Matrix:
    """Inverse of a rigid transform."""
    r, t = m[:3, :3], m[:3, 3]
    out = np.eye(4)
    out[:3, :3] = r.T
    out[:3, 3] = -r.T @ t
    return out


def to_list(m: Matrix, digits: int = 9) -> list[list[float]]:
    return [[round(float(v), digits) + 0.0 for v in row] for row in m]
