"""Linear static structural analysis: K u = F.

Small-strain, linear-elastic, isotropic, static. For each element the stiffness

    K_e = integral over the element of B^T D B dV

(B: strain-displacement matrix from the shape-function gradients, D: the isotropic
elasticity matrix from Young's modulus E and Poisson's ratio nu) is computed exactly for the
constant-strain tetrahedron (TET4), by 4-point Gauss quadrature for the quadratic
tetrahedron (TET10) and by 2 x 2 x 2 Gauss quadrature for the trilinear hexahedron (HEX8).
The element matrices are assembled into a sparse global stiffness K (compressed sparse rows);
fixed degrees of freedom are eliminated; the reduced system is
solved by the conjugate gradient method with a Jacobi (diagonal) preconditioner, and its
relative residual |F - K u| / |F| is recorded at every iteration. Small systems are also
solved directly as a cross-check.

Results: displacements; element strains and stresses sigma = D B u; von Mises stress
sqrt(((s1-s2)^2 + (s2-s3)^2 + (s3-s1)^2) / 2); principal stresses (eigenvalues of the
stress tensor); reactions R = K u - F at the supports and the equilibrium error
|sum R + sum F| / |sum F|; compliance F . u; factor of safety yield / max von Mises.

An educational solver, not a validated industrial code: linear TET4 elements are stiff in
bending (they lock) and need fine meshes; stresses are element-constant (TET4) or
centroidal (HEX8) and averaged to nodes for display; no contact, plasticity, large
deformation or dynamics.
"""

import time
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from autevra.fea.mesh import Mesh


@dataclass
class Material:
    name: str
    youngs: float  # MPa (N/mm^2)
    poisson: float
    density: float  # kg/m^3
    yield_strength: float  # MPa


MATERIALS = {
    "Structural steel": Material("Structural steel", 210_000, 0.30, 7850, 250),
    "Aluminium 6061-T6": Material("Aluminium 6061-T6", 69_000, 0.33, 2700, 276),
    "Titanium Ti-6Al-4V": Material("Titanium Ti-6Al-4V", 114_000, 0.34, 4430, 880),
    "ABS plastic": Material("ABS plastic", 2_300, 0.35, 1050, 40),
}


def elasticity(m: Material) -> np.ndarray:
    """Isotropic D (Voigt order xx, yy, zz, xy, yz, zx; engineering shear strains)."""
    e, v = m.youngs, m.poisson
    c = e / ((1 + v) * (1 - 2 * v))
    d = np.zeros((6, 6))
    d[:3, :3] = c * v
    np.fill_diagonal(d[:3, :3], c * (1 - v))
    d[3:, 3:] = np.eye(3) * c * (1 - 2 * v) / 2
    return d


def _b_matrix(grad: np.ndarray) -> np.ndarray:
    """B (E, 6, 3n) from shape-function gradients grad (E, 3, n)."""
    e, _, n = grad.shape
    b = np.zeros((e, 6, 3 * n))
    gx, gy, gz = grad[:, 0], grad[:, 1], grad[:, 2]
    b[:, 0, 0::3], b[:, 1, 1::3], b[:, 2, 2::3] = gx, gy, gz
    b[:, 3, 0::3], b[:, 3, 1::3] = gy, gx
    b[:, 4, 1::3], b[:, 4, 2::3] = gz, gy
    b[:, 5, 0::3], b[:, 5, 2::3] = gz, gx
    return b


def tet4(
    nodes: np.ndarray, tets: np.ndarray, d: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Element stiffness (E, 12, 12), B (E, 6, 12) and volumes of constant-strain tetrahedra."""
    x = nodes[tets]
    jac = np.stack([x[:, 1] - x[:, 0], x[:, 2] - x[:, 0], x[:, 3] - x[:, 0]], axis=1)  # dx/dxi
    det = np.linalg.det(jac)
    dn = np.array([[-1.0, -1.0, -1.0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])  # dN/dxi (4, 3)
    grad = np.linalg.solve(jac, np.broadcast_to(dn.T, (len(tets), 3, 4)))  # dN/dx (E, 3, 4)
    b = _b_matrix(grad)
    vol = det / 6.0
    ke = np.einsum("e,eji,jk,ekl->eil", vol, b, d, b)
    return ke, b, vol


_TET10_GAUSS = np.array([[0.1381966011250105] * 3, [0.5854101966249685, 0.1381966011250105,
    0.1381966011250105], [0.1381966011250105, 0.5854101966249685, 0.1381966011250105],
    [0.1381966011250105, 0.1381966011250105, 0.5854101966249685]])  # fmt: skip
_TET10_EDGES = [(0, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3)]


def _tet10_dn(xi: np.ndarray) -> np.ndarray:
    """dN/dxi (10, 3) of the quadratic tetrahedron: corners L_i (2 L_i - 1), mid-edges
    4 L_i L_j, with volume coordinates L = (1 - xi - eta - zeta, xi, eta, zeta)."""
    lam = np.array([1 - xi.sum(), xi[0], xi[1], xi[2]])
    dl = np.array([[-1.0, -1.0, -1.0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])  # dL_i/dxi
    out = np.zeros((10, 3))
    for i in range(4):
        out[i] = (4 * lam[i] - 1) * dl[i]
    for m, (i, j) in enumerate(_TET10_EDGES):
        out[4 + m] = 4 * (lam[i] * dl[j] + lam[j] * dl[i])
    return out


def tet10(
    nodes: np.ndarray, tets: np.ndarray, d: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Quadratic tetrahedra by 4-point Gauss quadrature (exact for the straight-sided
    element's quadratic B^T D B); B averaged over the Gauss points for element stresses."""
    x = nodes[tets]  # (E, 10, 3)
    ke = np.zeros((len(tets), 30, 30))
    b_mean = np.zeros((len(tets), 6, 30))
    vol = np.zeros(len(tets))
    for xi in _TET10_GAUSS:
        dn = _tet10_dn(xi)
        jac = np.einsum("na,enb->eab", dn, x)
        det = np.linalg.det(jac)
        b = _b_matrix(np.linalg.solve(jac, np.broadcast_to(dn.T, (len(tets), 3, 10))))
        w = det / 24.0  # reference volume 1/6, four equal weights
        ke += np.einsum("e,eji,jk,ekl->eil", w, b, d, b)
        b_mean += b / 4.0
        vol += w
    return ke, b_mean, vol


_HEX_NAT = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                     [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=float)  # fmt: skip


def _hex_dn(xi: np.ndarray) -> np.ndarray:
    """dN/dxi (8, 3) of the trilinear hexahedron at natural point xi."""
    s = _HEX_NAT
    out = np.zeros((8, 3))
    for a in range(3):
        b_, c_ = [i for i in range(3) if i != a]
        out[:, a] = s[:, a] * (1 + s[:, b_] * xi[b_]) * (1 + s[:, c_] * xi[c_]) / 8.0
    return out


def hex8(
    nodes: np.ndarray, hexes: np.ndarray, d: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Element stiffness by 2x2x2 Gauss quadrature, the centroid B, and volumes."""
    x = nodes[hexes]  # (E, 8, 3)
    g = 1 / np.sqrt(3.0)
    ke = np.zeros((len(hexes), 24, 24))
    vol = np.zeros(len(hexes))
    for xi in np.array(np.meshgrid([-g, g], [-g, g], [-g, g])).T.reshape(-1, 3):
        dn = _hex_dn(xi)
        jac = np.einsum("na,enb->eab", dn, x)  # (E, 3, 3): d x_b / d xi_a
        det = np.linalg.det(jac)
        grad = np.linalg.solve(jac, np.broadcast_to(dn.T, (len(hexes), 3, 8)))
        b = _b_matrix(grad)
        ke += np.einsum("e,eji,jk,ekl->eil", det, b, d, b)
        vol += det
    dn0 = _hex_dn(np.zeros(3))
    jac0 = np.einsum("na,enb->eab", dn0, x)
    b0 = _b_matrix(np.linalg.solve(jac0, np.broadcast_to(dn0.T, (len(hexes), 3, 8))))
    return ke, b0, vol


def assemble(n_nodes: int, elements: np.ndarray, ke: np.ndarray) -> sp.csr_matrix:
    dofs = (elements[:, :, None] * 3 + np.arange(3)).reshape(len(elements), -1)  # (E, 3n)
    rows = np.repeat(dofs, dofs.shape[1], axis=1).ravel()
    cols = np.tile(dofs, (1, dofs.shape[1])).ravel()
    return sp.coo_matrix((ke.ravel(), (rows, cols)), shape=(3 * n_nodes, 3 * n_nodes)).tocsr()


REGIONS = ("x-min", "x-max", "y-min", "y-max", "z-min", "z-max")


def region_nodes(mesh: Mesh, region: str, tol: float | None = None) -> np.ndarray:
    """Nodes on a face of the part's bounding box (e.g. "x-min": the -X end).

    Nodes on that plane; when the part only touches the plane at a point or an edge (a
    rounded end), the band widens to half an element so there is something to hold."""
    axis = "xyz".index(region[0])
    lo, hi = mesh.nodes[:, axis].min(), mesh.nodes[:, axis].max()
    target = lo if region.endswith("min") else hi
    gap = np.abs(mesh.nodes[:, axis] - target)
    if tol is not None:
        return np.flatnonzero(gap <= tol)
    on = np.flatnonzero(gap <= 1e-5 * max(hi - lo, 1.0))
    if len(on) >= 3:
        return on
    return np.flatnonzero(gap <= 0.5 * mesh.stats.get("size", 0.02 * (hi - lo)))


def region_triangles(mesh: Mesh, region: str) -> np.ndarray:
    on = np.zeros(len(mesh.nodes), dtype=bool)
    on[region_nodes(mesh, region)] = True
    return mesh.boundary[on[mesh.boundary].all(axis=1)]


def _quadratic(mesh: Mesh, tris: np.ndarray) -> np.ndarray:
    """The mid-edge nodes (F, 3) of the given corner triangles of a TET10 mesh."""
    assert mesh.boundary6 is not None
    index = {tuple(sorted(t)): i for i, t in enumerate(mesh.boundary.tolist())}
    rows = [index[tuple(sorted(t))] for t in tris.tolist()]
    return mesh.boundary6[rows, 3:]


@dataclass
class Load:
    region: str
    force: tuple[float, float, float] = (0.0, 0.0, 0.0)  # N, total over the region
    pressure: float = 0.0  # MPa (N/mm^2), positive pushes into the surface


@dataclass
class Result:
    displacement: np.ndarray  # (N, 3) mm
    von_mises: np.ndarray  # (E,) MPa
    principal: np.ndarray  # (E, 3) MPa, descending
    strain_eq: np.ndarray  # (E,) equivalent (von Mises) strain
    nodal_vm: np.ndarray  # (N,) volume-weighted averages for display
    stats: dict = field(default_factory=dict)


def solve(mesh: Mesh, material: Material, supports: list[str], loads: list[Load],
          tol: float = 1e-8, max_iter: int = 4_000) -> Result:  # fmt: skip
    t0 = time.perf_counter()
    d = elasticity(material)
    element = {"tet4": tet4, "tet10": tet10, "hex8": hex8}[mesh.kind]
    ke, b, vol = element(mesh.nodes, mesh.elements, d)
    k_mat = assemble(len(mesh.nodes), mesh.elements, ke)
    t_assemble = time.perf_counter() - t0
    n = 3 * len(mesh.nodes)
    f = np.zeros(n)
    applied = np.zeros(3)
    for load in loads:
        tris = region_triangles(mesh, load.region)
        if len(tris) == 0:
            raise ValueError(f"no surface on {load.region} to load")
        p = mesh.nodes[tris]
        cross = np.cross(p[:, 1] - p[:, 0], p[:, 2] - p[:, 0])
        area = 0.5 * np.linalg.norm(cross, axis=1)
        normal = cross / np.maximum(2 * area[:, None], 1e-30)
        # nodes that carry the load: corners for linear triangles; for the 6-node triangles of
        # TET10 the consistent load of a uniform traction is zero at the corners and a third
        # at each mid-edge node
        carry = tris if mesh.boundary6 is None else _quadratic(mesh, tris)
        share = np.zeros(len(mesh.nodes))
        np.add.at(share, carry.ravel(), np.repeat(area / 3.0, 3))
        if any(load.force):
            total = share.sum()
            for c in range(3):
                f[c::3] += load.force[c] * share / total
            applied += np.asarray(load.force, dtype=float)
        if load.pressure:
            tri_force = -load.pressure * area[:, None] * normal  # into the surface
            for c in range(3):
                np.add.at(f[c::3], carry.ravel(), np.repeat(tri_force[:, c] / 3.0, 3))
            applied += tri_force.sum(axis=0)
    fixed_nodes = (
        np.unique(np.concatenate([region_nodes(mesh, r) for r in supports]))
        if supports
        else np.array([], int)
    )
    if len(fixed_nodes) == 0:
        raise ValueError("add at least one support: an unsupported part moves as a rigid body")
    fixed = (fixed_nodes[:, None] * 3 + np.arange(3)).ravel()
    free = np.setdiff1d(np.arange(n), fixed)
    kff = k_mat[free][:, free].tocsr()
    rhs = f[free]
    history: list[float] = []
    norm_b = float(np.linalg.norm(rhs)) or 1.0

    def track(xk: np.ndarray) -> None:
        history.append(float(np.linalg.norm(rhs - kff @ xk)) / norm_b)

    jacobi = sp.diags(1.0 / kff.diagonal())
    t1 = time.perf_counter()
    uf, info = spla.cg(kff, rhs, rtol=tol, maxiter=max_iter, M=jacobi, callback=track)
    t_cg = time.perf_counter() - t1
    direct_diff = None
    method = "Jacobi-preconditioned conjugate gradient on the reduced K (supports eliminated)"
    if info != 0 or len(free) <= 15_000:
        # sparse LU: the cross-check on small systems, the answer when CG stalls (badly
        # shaped elements make K ill-conditioned, and Jacobi preconditioning is weak)
        ud = spla.spsolve(kff.tocsc(), rhs)
        direct_diff = float(np.linalg.norm(ud - uf) / max(np.linalg.norm(ud), 1e-30))
        if info != 0:
            uf = ud
            method = (
                f"conjugate gradient stopped at {max_iter} iterations without converging "
                "(ill-conditioned K: refine or coarsen the mesh); displacements from the "
                "sparse direct (LU) solve"
            )
    u = np.zeros(n)
    u[free] = uf
    reaction = k_mat @ u - f
    reaction_sum = np.array([reaction[fixed][c::3].sum() for c in range(3)])
    equilibrium = float(
        np.linalg.norm(reaction_sum + applied) / max(np.linalg.norm(applied), 1e-30)
    )
    # stresses
    dofs = (mesh.elements[:, :, None] * 3 + np.arange(3)).reshape(len(mesh.elements), -1)
    strain = np.einsum("eij,ej->ei", b, u[dofs])
    stress = strain @ d.T
    sx, sy, sz, txy, tyz, tzx = stress.T
    vm = np.sqrt(
        0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (txy**2 + tyz**2 + tzx**2)
    )
    tensor = np.stack(
        [np.stack([sx, txy, tzx], -1), np.stack([txy, sy, tyz], -1), np.stack([tzx, tyz, sz], -1)],
        1,
    )
    principal = np.sort(np.linalg.eigvalsh(tensor), axis=1)[:, ::-1]
    # equivalent (von Mises) strain: sqrt(2/3 e':e'), e' the deviatoric tensor strain
    ex, ey, ez, gxy, gyz, gzx = strain.T
    mean = (ex + ey + ez) / 3
    dev = (ex - mean) ** 2 + (ey - mean) ** 2 + (ez - mean) ** 2 + 0.5 * (gxy**2 + gyz**2 + gzx**2)
    strain_eq = np.sqrt(2 / 3 * dev)
    weight = np.zeros(len(mesh.nodes))
    acc = np.zeros(len(mesh.nodes))
    per = mesh.elements.shape[1]
    np.add.at(weight, mesh.elements.ravel(), np.repeat(np.abs(vol), per))
    np.add.at(acc, mesh.elements.ravel(), np.repeat(np.abs(vol) * vm, per))
    nodal_vm = acc / np.maximum(weight, 1e-30)
    disp = u.reshape(-1, 3)
    max_vm = float(vm.max())
    mass = float(np.abs(vol).sum()) * 1e-9 * material.density  # mm^3 -> m^3
    stats = {
        "dofs": n, "free_dofs": int(len(free)), "fixed_dofs": int(len(fixed)),
        "k_shape": [n, n], "k_nnz": int(k_mat.nnz), "k_density": k_mat.nnz / float(n * n),
        "k_memory_mb": (k_mat.data.nbytes + k_mat.indices.nbytes + k_mat.indptr.nbytes) / 1e6,
        "element_matrix": list(ke.shape[1:]),
        "cg_iterations": len(history), "cg_converged": info == 0, "cg_residuals": history[-400:],
        "cg_final_residual": history[-1] if history else 0.0,
        "direct_difference": direct_diff,
        "time_assemble": t_assemble, "time_solve": t_cg,
        "applied_force": applied.tolist(), "reaction_force": reaction_sum.tolist(),
        "equilibrium_error": equilibrium,
        "compliance": float(f @ u),  # N mm (twice the strain energy)
        "max_displacement": float(np.linalg.norm(disp, axis=1).max()),
        "max_von_mises": max_vm,
        "max_principal": float(principal[:, 0].max()),
        "min_principal": float(principal[:, 2].min()),
        "factor_of_safety": material.yield_strength / max_vm if max_vm > 0 else None,
        "mass_kg": mass,
        "method": method,
    }  # fmt: skip
    return Result(disp, vm, principal, strain_eq, nodal_vm, stats)
