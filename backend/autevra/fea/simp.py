"""Topology optimisation by SIMP (solid isotropic material with penalisation).

The design domain is a regular grid of elements, each with a density x_e in [x_min, 1].
Young's modulus is interpolated as

    E(x_e) = E_min + x_e^p (E_0 - E_min)        (p, the penalty, typically 3)

which makes intermediate densities uneconomical, so the optimum is close to solid/void.
The problem (minimum compliance for a volume budget) is

    minimise   c(x) = F^T u = sum_e E(x_e) u_e^T k_0 u_e
    subject to K(x) u = F,   sum_e x_e v_e = f V,   x_min <= x_e <= 1

with sensitivities  dc/dx_e = -p x_e^(p-1) (E_0 - E_min) u_e^T k_0 u_e  (the adjoint of the
self-adjoint compliance problem). Sensitivities are smoothed by a distance-weighted filter
of radius r_min (against checkerboards and mesh dependence) and the design is updated by
the optimality criteria (OC) method: x_e <- x_e (-dc/dx_e / (lambda dV/dx_e))^(1/2), within a
move limit, with the Lagrange multiplier lambda found by bisection so the volume is met.

2D: four-node bilinear plane-stress squares (Q4, 2 x 2 Gauss). 3D: eight-node trilinear
cubes (HEX8, from ``autevra.fea.solver``). Every element has the same k_0, so K is
assembled from one matrix scaled per element. Educational, after Sigmund's 99-line code
and Andreassen et al.'s 88-line code; every number reported is computed.
"""

import time
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from autevra.fea import solver as fs

MAX_ELEMENTS_2D = 20_000
MAX_ELEMENTS_3D = 12_000


def q4_stiffness(nu: float) -> np.ndarray:
    """k_0 (8 x 8) of a unit-modulus, unit-thickness, unit-square plane-stress Q4 element,
    by 2 x 2 Gauss quadrature. Node order (0,0), (1,0), (1,1), (0,1); dofs (u, v) per node."""
    d = np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]]) / (1 - nu**2)
    corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], dtype=float)
    g = 1 / np.sqrt(3.0)
    k = np.zeros((8, 8))
    for xi, eta in ((-g, -g), (g, -g), (g, g), (-g, g)):
        dn = np.stack([corners[:, 0] * (1 + corners[:, 1] * eta) / 4,
                       corners[:, 1] * (1 + corners[:, 0] * xi) / 4], axis=0)  # fmt: skip
        grad = 2.0 * dn  # d/dx = 2 d/dxi on a unit square (jacobian 1/2)
        b = np.zeros((3, 8))
        b[0, 0::2], b[1, 1::2] = grad[0], grad[1]
        b[2, 0::2], b[2, 1::2] = grad[1], grad[0]
        k += b.T @ d @ b * 0.25  # det J = 1/4
    return k


def hex_stiffness(nu: float) -> np.ndarray:
    """k_0 (24 x 24) of a unit-modulus unit cube (HEX8, 2 x 2 x 2 Gauss)."""
    nodes = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                      [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], dtype=float)  # fmt: skip
    ke, _, _ = fs.hex8(nodes, np.arange(8)[None], fs.elasticity(fs.Material("unit", 1.0, nu, 1, 1)))
    return ke[0]


@dataclass
class Problem:
    """A grid design domain with supports and loads at grid nodes (unit element size)."""

    shape: tuple[int, ...]  # (nx, ny) or (nx, ny, nz) elements
    fixed: np.ndarray  # fixed dof indices
    force: np.ndarray  # global force vector
    name: str = ""
    passive_void: np.ndarray | None = None  # element mask kept empty (holes)
    description: str = ""


def _node_id(shape: tuple[int, ...], *idx: np.ndarray) -> np.ndarray:
    """Node numbers on the (nx+1) x (ny+1) [x (nz+1)] grid, x fastest."""
    if len(shape) == 2:
        i, j = idx
        return j * (shape[0] + 1) + i
    i, j, kk = idx
    return (kk * (shape[1] + 1) + j) * (shape[0] + 1) + i


def element_nodes(shape: tuple[int, ...]) -> np.ndarray:
    if len(shape) == 2:
        nx, ny = shape
        i, j = np.meshgrid(np.arange(nx), np.arange(ny), indexing="xy")
        i, j = i.ravel(), j.ravel()  # element e = j * nx + i
        return np.stack([_node_id(shape, i, j), _node_id(shape, i + 1, j),
                         _node_id(shape, i + 1, j + 1), _node_id(shape, i, j + 1)], 1)  # fmt: skip
    nx, ny, nz = shape
    kk, j, i = np.meshgrid(np.arange(nz), np.arange(ny), np.arange(nx), indexing="ij")
    i, j, kk = i.ravel(), j.ravel(), kk.ravel()  # element e = (k * ny + j) * nx + i
    c = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    return np.stack([_node_id(shape, i + a, j + b_, kk + c_) for a, b_, c_ in c], 1)


def preset(name: str, shape: tuple[int, ...]) -> Problem:
    """Classic load cases (unit load). 2D: y up; 3D: z up, y across."""
    dim = len(shape)
    n_nodes = int(np.prod(np.array(shape) + 1))
    f = np.zeros(dim * n_nodes)
    nx = shape[0]
    grid = np.meshgrid(*[np.arange(s + 1) for s in shape], indexing="ij")
    ids = _node_id(shape, *[g.ravel() for g in grid])
    coords = np.stack([g.ravel() for g in grid], 1)
    up = dim - 1  # vertical axis

    def dofs(mask: np.ndarray, axes: tuple[int, ...]) -> np.ndarray:
        return (ids[mask][:, None] * dim + np.array(axes)).ravel()

    def at(mask: np.ndarray, axis: int, total: float) -> None:
        nodes = ids[mask]
        np.add.at(f, nodes * dim + axis, total / len(nodes))

    x, vert = coords[:, 0], coords[:, up]
    top, bottom = vert == shape[up], vert == 0
    all_axes = tuple(range(dim))
    if name == "mbb":  # half MBB beam: symmetry at x = 0, roller at the far bottom corner
        fixed = np.concatenate([dofs(x == 0, (0,)), dofs((x == nx) & bottom, (up,))])
        if dim == 3:  # hold the sideways (y) rigid motion along one bottom edge
            fixed = np.concatenate([fixed, dofs((coords[:, 1] == 0) & bottom, (1,))])
        at((x == 0) & top, up, -1.0)
        desc = "Half MBB beam: load at the top of the symmetry line, roller at the far corner"
    elif name == "cantilever":
        fixed = dofs(x == 0, all_axes)
        at((x == nx) & (vert == shape[up] // 2), up, -1.0)
        desc = "Cantilever: clamped left edge, downward load mid-height at the free end"
    elif name == "bridge":  # supports at both bottom corners, distributed load on the deck
        fixed = np.concatenate([dofs((x == 0) & bottom, all_axes),
                                dofs((x == nx) & bottom, all_axes)])  # fmt: skip
        at(top, up, -1.0)
        desc = "Bridge: pinned bottom corners, uniform load on the top deck"
    elif name == "bracket":  # clamped left edge, load at the far bottom corner
        fixed = dofs(x == 0, all_axes)
        at((x == nx) & bottom, up, -1.0)
        desc = "Bracket: clamped left edge, load at the lower far corner"
    else:
        raise ValueError(f"unknown load case '{name}'")
    return Problem(shape, np.unique(fixed), f, name, None, desc)


PRESETS = {
    "mbb": "Half MBB beam (symmetric simply supported beam)",
    "cantilever": "Cantilever, end load",
    "bridge": "Bridge, distributed deck load",
    "bracket": "Bracket, corner load",
}


def _filter_matrix(shape: tuple[int, ...], rmin: float) -> sp.csr_matrix:
    """H_ef = max(0, rmin - dist(e, f)), rows normalised later."""
    centres = np.stack(
        [g.ravel() for g in np.meshgrid(*[np.arange(s) + 0.5 for s in shape[::-1]],
                                         indexing="ij")][::-1], 1)  # fmt: skip
    from scipy.spatial import cKDTree

    tree = cKDTree(centres)
    pairs = tree.query_pairs(rmin, output_type="ndarray")
    d = np.linalg.norm(centres[pairs[:, 0]] - centres[pairs[:, 1]], axis=1)
    n = len(centres)
    rows = np.concatenate([pairs[:, 0], pairs[:, 1], np.arange(n)])
    cols = np.concatenate([pairs[:, 1], pairs[:, 0], np.arange(n)])
    vals = np.concatenate([rmin - d, rmin - d, np.full(n, rmin)])
    return sp.csr_matrix((vals, (rows, cols)), shape=(n, n))


@dataclass
class Result:
    density: np.ndarray  # final (E,)
    snapshots: list[np.ndarray] = field(default_factory=list)  # (E,) every few iterations
    snapshot_iters: list[int] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def optimise(problem: Problem, volfrac: float = 0.4, penal: float = 3.0, rmin: float = 1.5,
             max_iter: int = 80, tol: float = 0.01, move: float = 0.2, nu: float = 0.3,
             e_min: float = 1e-9, snapshot_every: int = 2) -> Result:  # fmt: skip
    t_start = time.perf_counter()
    shape, dim = problem.shape, len(problem.shape)
    n_el = int(np.prod(shape))
    limit = MAX_ELEMENTS_2D if dim == 2 else MAX_ELEMENTS_3D
    if n_el > limit:
        raise ValueError(f"{n_el} elements is more than this demo optimises ({limit})")
    k0 = q4_stiffness(nu) if dim == 2 else hex_stiffness(nu)
    en = element_nodes(shape)
    edofs = (en[:, :, None] * dim + np.arange(dim)).reshape(n_el, -1)
    n_dof = dim * int(np.prod(np.array(shape) + 1))
    rows = np.repeat(edofs, edofs.shape[1], axis=1).ravel()
    cols = np.tile(edofs, (1, edofs.shape[1])).ravel()
    free = np.setdiff1d(np.arange(n_dof), problem.fixed)
    h = _filter_matrix(shape, rmin)
    hs = np.asarray(h.sum(axis=1)).ravel()
    x = np.full(n_el, volfrac)
    void = problem.passive_void
    if void is not None:
        x[void] = 0.0
    result = Result(density=x)
    u = np.zeros(n_dof)
    change, it = 1.0, 0
    t_solve = 0.0
    while change > tol and it < max_iter:
        it += 1
        stiff = e_min + x**penal * (1 - e_min)
        k = sp.coo_matrix((np.kron(stiff, k0.ravel()), (rows, cols)), shape=(n_dof, n_dof)).tocsc()
        t0 = time.perf_counter()
        kff = k[free][:, free]
        if dim == 2:
            u[free] = spla.spsolve(kff, problem.force[free])
        else:  # Jacobi-preconditioned CG, warm-started from the previous design's field
            m = sp.diags(1.0 / kff.diagonal())
            u[free], _ = spla.cg(kff, problem.force[free], x0=u[free], rtol=1e-6, M=m,
                                 maxiter=4000)  # fmt: skip
        t_solve += time.perf_counter() - t0
        ue = u[edofs]
        energy = np.einsum("ei,ij,ej->e", ue, k0, ue)  # u_e^T k_0 u_e
        compliance = float((stiff * energy).sum())
        dc = -penal * x ** (penal - 1) * (1 - e_min) * energy
        dc = (h @ (x * dc)) / hs / np.maximum(1e-3, x)  # sensitivity filter (Sigmund)
        # optimality criteria: bisect the multiplier so the volume constraint holds
        lo, hi = 1e-9, 1e9
        target = volfrac * n_el
        while (hi - lo) / (hi + lo) > 1e-4:
            mid = 0.5 * (lo + hi)
            new = np.clip(x * np.sqrt(np.maximum(-dc, 0) / mid), np.maximum(0.0, x - move),
                          np.minimum(1.0, x + move))  # fmt: skip
            new = np.maximum(new, 1e-3)
            if void is not None:
                new[void] = 1e-3
            if new.sum() > target:
                lo = mid
            else:
                hi = mid
        change = float(np.abs(new - x).max())
        x = new
        grey = float(np.mean((x > 0.1) & (x < 0.9)))
        result.history.append({"iter": it, "compliance": compliance, "volume": float(x.mean()),
                               "change": change, "grey": grey, "lambda": mid})  # fmt: skip
        if it % snapshot_every == 1 or snapshot_every == 1:
            result.snapshots.append(x.copy())
            result.snapshot_iters.append(it)
    result.snapshots.append(x.copy())
    result.snapshot_iters.append(it)
    result.density = x
    result.stats = {
        "elements": n_el, "dofs": n_dof, "free_dofs": int(len(free)),
        "k_nnz_per_element": int(k0.size), "iterations": it, "converged": change <= tol,
        "final_change": change, "final_compliance": result.history[-1]["compliance"],
        "initial_compliance": result.history[0]["compliance"],
        "volume_fraction": float(x.mean()), "grey_fraction": result.history[-1]["grey"],
        "filter_neighbours": float(h.nnz / n_el), "time_solve": t_solve,
        "time_total": time.perf_counter() - t_start,
        "solver": "sparse direct (LU)" if dim == 2 else "Jacobi-preconditioned CG, warm start",
    }  # fmt: skip
    return result
