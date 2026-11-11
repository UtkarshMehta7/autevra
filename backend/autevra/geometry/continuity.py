"""Geometric continuity between two surfaces along a shared boundary, and curvature combs.

Surface A's edge u = 1 is joined to surface B's edge u = 0 (both run along v). At samples
along the boundary:

- G0 (position): the gap |A(1, v) - B(0, v)|.
- G1 (tangency): the angle between the unit normals.
- G2 (curvature): the difference of the normal curvatures across the boundary, the
  curvature of the cross-boundary isoparametric curves in the surface normal plane,
  k_n = L / E with L = S_uu . n and E = S_u . S_u (second and first fundamental forms).
- G3 (curvature rate): the difference of dk_n/ds across the boundary, estimated by one-sided
  finite differences inside each patch (an estimate, labelled as such).

Highlights reflected in a surface follow its normals, so a G1 join breaks reflection lines
into a kink-free but visibly "bent" line, and only G2 (and better) keeps them flowing; this
is why automotive Class-A and aerospace lofts specify G2 or G3.

``join`` builds patch B from patch A for a requested continuity (G0, G1 or G2) by solving
B's first control rows from A's derivatives at the shared edge.
"""

from dataclasses import dataclass

import numpy as np

from autevra.geometry.nurbs import Surface, basis_ders, find_span

TOL = {"g0": 1e-3, "g1_deg": 0.05, "g2_rel": 0.02, "g3_rel": 0.05}  # analysis tolerances


@dataclass
class Report:
    samples: int
    gap: float  # max G0 gap, mm
    angle: float  # max normal angle, degrees
    curvature_a: list[float]  # k_n on A's side at each sample (1/mm)
    curvature_b: list[float]
    curvature_jump: float  # max |k_A - k_B|
    rate_jump: float  # max |dk/ds A - dk/ds B| (estimate)
    level: str  # "none", "G0", "G1", "G2" or "G3": the highest met everywhere
    explanation: str

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def _cross(s: Surface, u: float, v: float, normal: np.ndarray | None = None):
    """Normal curvature across the boundary (along u) and the unit normal at (u, v)."""
    skl = s.derivatives(u, v, 2)
    su, sv, suu = skl[1, 0], skl[0, 1], skl[2, 0]
    n = np.cross(su, sv)
    n /= max(float(np.linalg.norm(n)), 1e-12)
    if normal is not None and n @ normal < 0:
        n = -n  # orient B's normal like A's
    k = float(suu @ n) / float(su @ su)
    return k, n, float(np.linalg.norm(su))


def analyse(a: Surface, b: Surface, samples: int = 21) -> Report:
    (ua0, ua1), (va0, va1) = a.domain
    (ub0, ub1), (vb0, vb1) = b.domain
    h = 1e-3
    gaps, angles, ka, kb, rates = [], [], [], [], []
    for t in np.linspace(0.0, 1.0, samples):
        va, vb = va0 + t * (va1 - va0), vb0 + t * (vb1 - vb0)
        pa, pb = a.point(ua1, va), b.point(ub0, vb)
        gaps.append(float(np.linalg.norm(pa - pb)))
        k1, n1, speed_a = _cross(a, ua1, va)
        k2, n2, speed_b = _cross(b, ub0, vb, n1)
        # atan2 keeps tiny angles accurate (arccos of a dot product near 1 does not)
        angles.append(float(np.degrees(np.arctan2(np.linalg.norm(np.cross(n1, n2)), n1 @ n2))))
        ka.append(k1)
        kb.append(k2)
        # dk/ds by one-sided differences inside each patch (s: arc length across)
        k1h = _cross(a, ua1 - h * (ua1 - ua0), va, n1)[0]
        k2h = _cross(b, ub0 + h * (ub1 - ub0), vb, n1)[0]
        rate_a = (k1 - k1h) / (h * (ua1 - ua0) * speed_a)
        rate_b = (k2h - k2) / (h * (ub1 - ub0) * speed_b)
        rates.append(abs(rate_a - rate_b))
    gap, angle = max(gaps), max(angles)
    jump = max(abs(x - y) for x, y in zip(ka, kb, strict=True))
    scale = max(max(abs(x) for x in ka + kb), 1e-6)
    rate = max(rates)
    rate_scale = max(rate, scale / max(_size(a), 1.0), 1e-9)
    level = "none"
    if gap <= TOL["g0"]:
        level = "G0"
        if angle <= TOL["g1_deg"]:
            level = "G1"
            if jump <= TOL["g2_rel"] * scale + 1e-7:
                level = "G2"
                if rate <= TOL["g3_rel"] * rate_scale:
                    level = "G3"
    explanation = {
        "none": "The patches do not meet: there is a gap along the boundary.",
        "G0": "Positional only: the surfaces meet but their tangent planes differ, so the join "
        "shows as a crease and reflections break.",
        "G1": "Tangent: no crease, but the curvature jumps across the join, so reflection "
        "lines bend sharply there (visible on paint).",
        "G2": "Curvature-continuous: reflection lines flow across the join (automotive "
        "Class-A minimum for visible panels).",
        "G3": "Curvature-rate continuous as well (estimated): the highlights also accelerate "
        "smoothly, as on premium Class-A and aerodynamic surfaces.",
    }[level]
    return Report(samples, gap, angle, ka, kb, jump, rate, level, explanation)


def _size(s: Surface) -> float:
    pts = s.control.reshape(-1, 3)
    return float(np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))


def join(a: Surface, target: str, bend: float = 0.0) -> Surface:
    """A patch B continuing A across its u = 1 edge with continuity ``target`` (G0, G1 or
    G2): same degrees and knots, B's first control rows solved from A's derivatives at the
    edge (column by column, so S_u, and for G2 S_uu, match for every v: C1 / C2, which
    imply G1 / G2). G0 adds a deliberate crease. ``bend`` lifts B's free rows. Non-rational
    patches only (all weights 1)."""
    if not np.allclose(a.weights, 1.0):
        raise ValueError("joins are built for non-rational patches (all weights 1)")
    p = a.degree_u
    ka = np.asarray(a.knots_u)
    rows, n = a.control.shape[0], a.control.shape[0] - 1
    (_, u1), _ = a.domain
    end = basis_ders(find_span(n, p, u1, ka), u1, p, ka, min(2, p))  # A at u = 1
    start = basis_ders(p, ka[p], p, ka, min(2, p))  # B (same knots) at u = 0
    tail = a.control[n - p : n + 1]  # the rows A's end derivatives depend on
    out = np.zeros_like(a.control)
    out[0] = a.control[-1]
    # continue A's end direction for the free rows
    d1 = np.einsum("r,rjc->jc", end[1], tail)  # S_u along the edge, per column
    step = d1 / max(float(np.linalg.norm(d1, axis=1).mean()), 1e-9)
    spacing = float(np.linalg.norm(a.control[-1] - a.control[-2], axis=1).mean())
    for i in range(1, rows):
        out[i] = out[0] + step * spacing * i
    fixed = 1
    if target in ("G1", "G2") and p >= 1:
        out[1] = (d1 - start[1][0] * out[0]) / start[1][1]
        fixed = 2
    if target == "G2" and p >= 2 and rows > 2:
        d2 = np.einsum("r,rjc->jc", end[2], tail)
        out[2] = (d2 - start[2][0] * out[0] - start[2][1] * out[1]) / start[2][2]
        fixed = 3
    if target == "G0" and rows > 1:
        out[1] = out[1] + np.array([0.0, 0.0, 0.6 * spacing])  # a deliberate crease
        fixed = 2
    for i in range(fixed, rows):
        out[i] = out[i] + np.array([0.0, 0.0, bend]) * (i - fixed + 1)
    return Surface(a.degree_u, a.degree_v, list(a.knots_u), list(a.knots_v), out,
                   np.ones_like(a.weights))  # fmt: skip


def comb(s: Surface, v: float, samples: int = 40, scale: float = 1.0) -> dict:
    """Curvature comb of the u-isocurve at v: the curve and, at each sample, a tooth along
    the surface normal of length scale * k_n (k_n: normal curvature along u)."""
    (u0, u1), _ = s.domain
    pts, tips, ks = [], [], []
    for u in np.linspace(u0, u1, samples):
        k, n, _ = _cross(s, float(u), v)
        p = s.point(float(u), v)
        pts.append(p.tolist())
        tips.append((p - scale * k * n).tolist())
        ks.append(k)
    return {"points": pts, "tips": tips, "curvature": ks}
