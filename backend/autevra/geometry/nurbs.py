"""Non-uniform rational B-splines (NURBS): curves and tensor-product surfaces.

A NURBS surface of degree (p, q) over control points P[i][j] with weights w[i][j] and knot
vectors U, V is

    S(u, v) = sum_i sum_j N_i,p(u) N_j,q(v) w_ij P_ij / sum_i sum_j N_i,p(u) N_j,q(v) w_ij

with the B-spline basis N from the Cox-de Boor recursion

    N_i,0(u) = 1 if U_i <= u < U_i+1 else 0
    N_i,p(u) = (u - U_i) / (U_i+p - U_i) N_i,p-1(u) + (U_i+p+1 - u) / (U_i+p+1 - U_i+1) N_i+1,p-1(u)

Evaluation works in homogeneous coordinates Pw = (w P, w), as in Piegl and Tiller, The
NURBS Book (2nd ed., 1997): spans by binary search (A2.1), the non-zero basis functions and
their derivatives (A2.2, A2.3), rational surface derivatives (A4.4), and knot insertion by
Boehm's algorithm (A5.3). Each basis function N_i,p is non-zero only on [U_i, U_i+p+1): a
control point moves the surface only over that local support, which is what makes NURBS
editable. Pure NumPy, no kernel; the tests cross-check it against Open CASCADE.
"""

from dataclasses import dataclass

import numpy as np


class NurbsError(ValueError):
    """An inconsistent NURBS definition (degree, knots and control points do not fit)."""


def clamped_knots(count: int, degree: int) -> list[float]:
    """An open uniform (clamped) knot vector on [0, 1]: the curve starts and ends at its
    first and last control points."""
    if count <= degree:
        raise NurbsError(f"{count} control points are too few for degree {degree}")
    inner = count - degree - 1
    return (
        [0.0] * (degree + 1) + [(i + 1) / (inner + 1) for i in range(inner)] + [1.0] * (degree + 1)
    )


def check_knots(knots: list[float], count: int, degree: int) -> None:
    if degree < 1:
        raise NurbsError("the degree must be at least 1")
    if len(knots) != count + degree + 1:
        raise NurbsError(
            f"a degree-{degree} spline over {count} control points needs {count + degree + 1} "
            f"knots (m = n + p + 1), not {len(knots)}"
        )
    if any(b < a for a, b in zip(knots, knots[1:], strict=False)):
        raise NurbsError("knots must not decrease")
    if knots[degree] >= knots[count]:
        raise NurbsError("the knot vector has no valid parameter range")


def find_span(n: int, p: int, u: float, knots: np.ndarray) -> int:
    """The knot span index i with U_i <= u < U_i+1 (A2.1); n is the last control index."""
    if u >= knots[n + 1]:
        return n
    if u <= knots[p]:
        return p
    lo, hi = p, n + 1
    mid = (lo + hi) // 2
    while u < knots[mid] or u >= knots[mid + 1]:
        if u < knots[mid]:
            hi = mid
        else:
            lo = mid
        mid = (lo + hi) // 2
    return mid


def basis_ders(span: int, u: float, p: int, knots: np.ndarray, d: int) -> np.ndarray:
    """The non-zero basis functions N_span-p..span,p and their derivatives up to order d
    at u (A2.3): ders[k][r] is the k-th derivative of N_span-p+r,p."""
    ndu = np.zeros((p + 1, p + 1))
    ndu[0, 0] = 1.0
    left, right = np.zeros(p + 1), np.zeros(p + 1)
    for j in range(1, p + 1):
        left[j] = u - knots[span + 1 - j]
        right[j] = knots[span + j] - u
        saved = 0.0
        for r in range(j):
            ndu[j, r] = right[r + 1] + left[j - r]  # lower triangle: knot differences
            temp = ndu[r, j - 1] / ndu[j, r]
            ndu[r, j] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        ndu[j, j] = saved
    ders = np.zeros((d + 1, p + 1))
    ders[0] = ndu[:, p]
    a = np.zeros((2, p + 1))
    for r in range(p + 1):
        s1, s2 = 0, 1
        a[0, 0] = 1.0
        for k in range(1, d + 1):
            dv = 0.0
            rk, pk = r - k, p - k
            if r >= k:
                a[s2, 0] = a[s1, 0] / ndu[pk + 1, rk]
                dv = a[s2, 0] * ndu[rk, pk]
            j1 = 1 if rk >= -1 else -rk
            j2 = k - 1 if r - 1 <= pk else p - r
            for j in range(j1, j2 + 1):
                a[s2, j] = (a[s1, j] - a[s1, j - 1]) / ndu[pk + 1, rk + j]
                dv += a[s2, j] * ndu[rk + j, pk]
            if r <= pk:
                a[s2, k] = -a[s1, k - 1] / ndu[pk + 1, r]
                dv += a[s2, k] * ndu[r, pk]
            ders[k, r] = dv
            s1, s2 = s2, s1
    factor = float(p)
    for k in range(1, d + 1):
        ders[k] *= factor
        factor *= p - k
    return ders


def basis(i: int, p: int, knots: np.ndarray, u: float) -> float:
    """One basis function N_i,p(u) by the Cox-de Boor recursion (for plotting and tests)."""
    last = len(knots) - p - 2  # n
    if i == 0 and u == knots[0] or i == last and u == knots[-1]:
        return 1.0
    if u < knots[i] or u >= knots[i + p + 1]:
        return 0.0
    n = [1.0 if knots[i + j] <= u < knots[i + j + 1] else 0.0 for j in range(p + 1)]
    for k in range(1, p + 1):
        saved = 0.0 if n[0] == 0.0 else ((u - knots[i]) * n[0]) / (knots[i + k] - knots[i])
        for j in range(p - k + 1):
            ul, ur = knots[i + j + 1], knots[i + j + k + 1]
            if n[j + 1] == 0.0:
                n[j] = saved
                saved = 0.0
            else:
                temp = n[j + 1] / (ur - ul)
                n[j] = saved + (ur - u) * temp
                saved = (u - ul) * temp
    return n[0]


@dataclass
class Surface:
    degree_u: int
    degree_v: int
    knots_u: list[float]
    knots_v: list[float]
    control: np.ndarray  # (nu, nv, 3)
    weights: np.ndarray  # (nu, nv), positive

    @classmethod
    def build(
        cls, degree_u: int, degree_v: int, control: list, weights: list | None = None,
        knots_u: list[float] | None = None, knots_v: list[float] | None = None,
    ) -> "Surface":  # fmt: skip
        pts = np.asarray(control, dtype=float)
        if pts.ndim != 3 or pts.shape[2] != 3:
            raise NurbsError("control points must be a grid of (x, y, z)")
        nu, nv = pts.shape[:2]
        w = np.ones((nu, nv)) if weights is None else np.asarray(weights, dtype=float)
        if w.shape != (nu, nv):
            raise NurbsError("one weight per control point")
        if np.any(w <= 0):
            raise NurbsError("weights must be positive")
        ku = clamped_knots(nu, degree_u) if knots_u is None else list(knots_u)
        kv = clamped_knots(nv, degree_v) if knots_v is None else list(knots_v)
        check_knots(ku, nu, degree_u)
        check_knots(kv, nv, degree_v)
        return cls(degree_u, degree_v, ku, kv, pts, w)

    @property
    def domain(self) -> tuple[tuple[float, float], tuple[float, float]]:
        nu, nv = self.weights.shape
        return (
            (self.knots_u[self.degree_u], self.knots_u[nu]),
            (self.knots_v[self.degree_v], self.knots_v[nv]),
        )

    def derivatives(self, u: float, v: float, d: int = 2) -> np.ndarray:
        """SKL[k][l] = d^(k+l) S / du^k dv^l for k + l <= d (A3.6 on Pw, then A4.4)."""
        p, q = self.degree_u, self.degree_v
        ku, kv = np.asarray(self.knots_u), np.asarray(self.knots_v)
        nu, nv = self.weights.shape
        su, sv = find_span(nu - 1, p, u, ku), find_span(nv - 1, q, v, kv)
        du, dv = min(d, p), min(d, q)
        nu_d = basis_ders(su, u, p, ku, du)
        nv_d = basis_ders(sv, v, q, kv, dv)
        pw = np.concatenate(
            [self.control * self.weights[..., None], self.weights[..., None]], axis=2
        )
        block = pw[su - p : su + 1, sv - q : sv + 1]  # (p+1, q+1, 4)
        aders = np.zeros((d + 1, d + 1, 4))  # derivatives of the homogeneous surface
        for k in range(du + 1):
            temp = np.einsum("r,rsc->sc", nu_d[k], block)  # (q+1, 4)
            for m in range(min(d - k, dv) + 1):
                aders[k, m] = nv_d[m] @ temp
        a, w = aders[..., :3], aders[..., 3]
        skl = np.zeros((d + 1, d + 1, 3))
        from math import comb

        for k in range(d + 1):
            for m in range(d - k + 1):
                vv = a[k, m].copy()
                for j in range(1, m + 1):
                    vv -= comb(m, j) * w[0, j] * skl[k, m - j]
                for i in range(1, k + 1):
                    vv -= comb(k, i) * w[i, 0] * skl[k - i, m]
                    v2 = np.zeros(3)
                    for j in range(1, m + 1):
                        v2 += comb(m, j) * w[i, j] * skl[k - i, m - j]
                    vv -= comb(k, i) * v2
                skl[k, m] = vv / w[0, 0]
        return skl

    def point(self, u: float, v: float) -> np.ndarray:
        return self.derivatives(u, v, 0)[0, 0]

    def frame(self, u: float, v: float) -> dict:
        """Point, unit normal, and the Gaussian and mean curvatures (first and second
        fundamental forms) at (u, v)."""
        skl = self.derivatives(u, v, 2)
        s, su, sv = skl[0, 0], skl[1, 0], skl[0, 1]
        suu, suv, svv = skl[2, 0], skl[1, 1], skl[0, 2]
        n = np.cross(su, sv)
        length = float(np.linalg.norm(n))
        if length < 1e-12:  # degenerate (a collapsed edge): no normal, no curvature
            return {"point": s, "normal": np.zeros(3), "gaussian": 0.0, "mean": 0.0}
        n /= length
        e, f, g = su @ su, su @ sv, sv @ sv
        ll, mm, nn = suu @ n, suv @ n, svv @ n
        den = e * g - f * f
        k = (ll * nn - mm * mm) / den
        h = (e * nn - 2 * f * mm + g * ll) / (2 * den)
        return {"point": s, "normal": n, "gaussian": float(k), "mean": float(h)}

    def grid(self, samples_u: int, samples_v: int) -> dict:
        """Points, normals and curvatures on a regular (u, v) grid, and the triangles."""
        (u0, u1), (v0, v1) = self.domain
        us, vs = np.linspace(u0, u1, samples_u), np.linspace(v0, v1, samples_v)
        pts, normals, gauss, mean = [], [], [], []
        for u in us:
            for v in vs:
                fr = self.frame(float(u), float(v))
                pts.append(fr["point"])
                normals.append(fr["normal"])
                gauss.append(fr["gaussian"])
                mean.append(fr["mean"])
        tris = []
        for i in range(samples_u - 1):
            for j in range(samples_v - 1):
                a, b = i * samples_v + j, (i + 1) * samples_v + j
                tris += [a, b, a + 1, a + 1, b, b + 1]
        return {
            "u": us.tolist(), "v": vs.tolist(),
            "points": np.asarray(pts).tolist(), "normals": np.asarray(normals).tolist(),
            "gaussian": gauss, "mean": mean, "triangles": tris,
        }  # fmt: skip

    def insert_knot_u(self, t: float) -> "Surface":
        """Insert u = t once (Boehm): one more column of control points, the same surface."""
        cols = [_insert_curve(self.degree_u, self.knots_u, self._pw()[:, j], t)
                for j in range(self.weights.shape[1])]  # fmt: skip
        knots = cols[0][0]
        pw = np.stack([c[1] for c in cols], axis=1)
        return self._from_pw(pw, knots, self.knots_v)

    def insert_knot_v(self, t: float) -> "Surface":
        rows = [_insert_curve(self.degree_v, self.knots_v, self._pw()[i], t)
                for i in range(self.weights.shape[0])]  # fmt: skip
        knots = rows[0][0]
        pw = np.stack([r[1] for r in rows], axis=0)
        return self._from_pw(pw, self.knots_u, knots)

    def _pw(self) -> np.ndarray:
        return np.concatenate(
            [self.control * self.weights[..., None], self.weights[..., None]], axis=2
        )

    def _from_pw(self, pw: np.ndarray, ku: list[float], kv: list[float]) -> "Surface":
        w = pw[..., 3]
        return Surface(
            self.degree_u, self.degree_v, list(ku), list(kv), pw[..., :3] / w[..., None], w
        )


def _insert_curve(
    p: int, knots: list[float], pw: np.ndarray, t: float
) -> tuple[list[float], np.ndarray]:
    """Boehm's knot insertion on a homogeneous control polygon pw (n+1, 4)."""
    k = np.asarray(knots)
    n = len(pw) - 1
    if not k[p] < t < k[n + 1]:
        raise NurbsError("insert knots strictly inside the parameter range")
    span = find_span(n, p, t, k)
    mult = int(np.sum(np.isclose(k, t)))
    if mult >= p:
        raise NurbsError(
            f"the knot {t:g} already has multiplicity {mult}; at most {p} for degree {p}"
        )
    out = np.zeros((n + 2, pw.shape[1]))
    out[: span - p + 1] = pw[: span - p + 1]
    out[span + 1 :] = pw[span:]
    for i in range(span - p + 1, span + 1):
        alpha = (t - k[i]) / (k[i + p] - k[i])
        out[i] = alpha * pw[i] + (1 - alpha) * pw[i - 1]
    new = [*knots[: span + 1], t, *knots[span + 1 :]]
    return new, out


def basis_table(knots: list[float], degree: int, count: int, samples: int = 101) -> dict:
    """Every basis function N_i,p sampled over the parameter range (for plotting)."""
    k = np.asarray(knots)
    t0, t1 = k[degree], k[count]
    ts = np.linspace(t0, t1, samples)
    functions = [[basis(i, degree, k, float(t)) for t in ts] for i in range(count)]
    return {"t": ts.tolist(), "functions": functions}
