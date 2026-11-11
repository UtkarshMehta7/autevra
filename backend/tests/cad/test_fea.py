"""Linear statics against closed-form answers."""

import numpy as np
import pytest

from autevra.cad import kernel as k
from autevra.fea import mesh as fm
from autevra.fea import solver as fs

pytestmark = pytest.mark.cad
STEEL = fs.MATERIALS["Structural steel"]


def bar(length: float = 100.0, side: float = 10.0) -> k.Shape:
    return k.box((0, length), (0, side), (0, side))


@pytest.mark.parametrize("kind", ["hex8", "tet4"])
def test_a_bar_in_tension_stretches_pl_over_ea(kind: str) -> None:
    p, length, side = 1000.0, 100.0, 10.0
    mesh = (fm.hex_mesh if kind == "hex8" else fm.tet_mesh)(bar(length, side), 5.0)
    out = fs.solve(mesh, STEEL, ["x-min"], [fs.Load("x-max", force=(p, 0, 0))])
    exact = p * length / (STEEL.youngs * side * side)
    tip = out.displacement[fs.region_nodes(mesh, "x-max"), 0].mean()
    assert tip == pytest.approx(exact, rel=0.03)  # the fixed end restrains Poisson contraction
    sigma = p / (side * side)  # 10 MPa away from the ends
    mid = np.abs(mesh.nodes[mesh.elements].mean(axis=1)[:, 0] - length / 2) < 15
    assert np.median(out.von_mises[mid]) == pytest.approx(sigma, rel=0.05)
    assert out.stats["equilibrium_error"] < 1e-6
    assert out.stats["direct_difference"] < 1e-6
    assert out.stats["cg_converged"]
    assert mesh.stats["volume_ratio"] == pytest.approx(1.0, abs=1e-6)


def test_a_thick_cantilever_matches_timoshenko_beam_theory() -> None:
    length, b, h, p = 200.0, 20.0, 20.0, -500.0
    mesh = fm.hex_mesh(k.box((0, length), (0, b), (0, h)), 5.0)
    out = fs.solve(mesh, STEEL, ["x-min"], [fs.Load("x-max", force=(0, 0, p))])
    inertia, area = b * h**3 / 12, b * h
    shear_mod = STEEL.youngs / (2 * (1 + STEEL.poisson))
    exact = abs(p) * length**3 / (3 * STEEL.youngs * inertia) + abs(p) * length / (
        5 / 6 * shear_mod * area
    )
    tip = -out.displacement[fs.region_nodes(mesh, "x-max"), 2].mean()
    # fully integrated trilinear hexahedra are slightly stiff in bending (shear locking)
    assert 0.85 * exact < tip < 1.02 * exact


def test_stiffness_scales_with_youngs_modulus() -> None:
    mesh = fm.hex_mesh(bar(), 5.0)
    loads = [fs.Load("x-max", force=(0, 0, -100))]
    a = fs.solve(mesh, STEEL, ["x-min"], loads).stats["max_displacement"]
    b = fs.solve(mesh, fs.MATERIALS["Aluminium 6061-T6"], ["x-min"], loads).stats[
        "max_displacement"
    ]
    assert b / a == pytest.approx(210_000 / 69_000, rel=0.03)  # (Poisson differs slightly)


def test_a_constant_strain_tetrahedron_reproduces_uniform_stress() -> None:
    nodes = np.array([[0.0, 0, 0], [10, 0, 0], [0, 10, 0], [0, 0, 10]])
    d = fs.elasticity(STEEL)
    ke, bm, vol = fs.tet4(nodes, np.array([[0, 1, 2, 3]]), d)
    assert vol[0] == pytest.approx(1000 / 6)
    u = np.zeros(12)
    u[0::3] = nodes[:, 0] * 1e-3  # u_x = 0.001 x: uniform strain e_xx = 0.001
    strain = bm[0] @ u
    assert strain == pytest.approx([1e-3, 0, 0, 0, 0, 0], abs=1e-12)
    assert np.allclose(ke[0], ke[0].T) and np.linalg.eigvalsh(ke[0]).min() > -1e-6  # symmetric, PSD


def test_unsupported_parts_are_refused() -> None:
    mesh = fm.hex_mesh(bar(), 10.0)
    with pytest.raises(ValueError):
        fs.solve(mesh, STEEL, [], [fs.Load("x-max", force=(1, 0, 0))])


def test_quadratic_tetrahedra_shape_functions_partition_unity() -> None:
    for xi in [np.array([0.1, 0.2, 0.3]), np.array([0.25, 0.25, 0.25]), np.zeros(3)]:
        assert fs._tet10_dn(xi).sum(axis=0) == pytest.approx(np.zeros(3), abs=1e-12)


def test_quadratic_tetrahedra_pass_the_patch_test() -> None:
    """A TET10 mesh under a linear displacement field reproduces the uniform strain."""
    mesh = fm.to_tet10(fm.tet_mesh(bar(40, 10), 5.0))
    d = fs.elasticity(STEEL)
    _, bm, vol = fs.tet10(mesh.nodes, mesh.elements, d)
    u = np.zeros(3 * len(mesh.nodes))
    u[0::3] = 1e-3 * mesh.nodes[:, 0] + 2e-4 * mesh.nodes[:, 1]  # e_xx 1e-3, gamma_xy 2e-4
    dofs = (mesh.elements[:, :, None] * 3 + np.arange(3)).reshape(len(mesh.elements), -1)
    strain = np.einsum("eij,ej->ei", bm, u[dofs])
    assert strain == pytest.approx(np.tile([1e-3, 0, 0, 2e-4, 0, 0], (len(strain), 1)), abs=1e-12)
    assert vol.sum() == pytest.approx(40 * 10 * 10, rel=1e-6)


def test_quadratic_tetrahedra_bend_like_a_beam_where_linear_ones_lock() -> None:
    length, b, h, p = 200.0, 20.0, 20.0, -1000.0
    base = fm.tet_mesh(k.box((0, length), (0, b), (0, h)), 10.0)
    loads = [fs.Load("x-max", force=(0, 0, p))]
    inertia, area = b * h**3 / 12, b * h
    shear_mod = STEEL.youngs / (2 * (1 + STEEL.poisson))
    exact = abs(p) * length**3 / (3 * STEEL.youngs * inertia) + abs(p) * length / (
        5 / 6 * shear_mod * area
    )
    quad = fm.to_tet10(base)
    out = fs.solve(quad, STEEL, ["x-min"], loads)
    tip = -out.displacement[fs.region_nodes(quad, "x-max"), 2].mean()
    assert tip == pytest.approx(exact, rel=0.04)
    assert out.stats["equilibrium_error"] < 1e-6
    lin = fs.solve(base, STEEL, ["x-min"], loads)
    assert -lin.displacement[fs.region_nodes(base, "x-max"), 2].mean() < 0.5 * exact  # locking


def test_tetrahedra_are_well_shaped() -> None:
    mesh = fm.tet_mesh(k.box((0, 100), (0, 30), (0, 30)), 5.0)
    assert mesh.stats["quality_mean"] > 0.6
    assert mesh.stats["slivers"] < 0.1 * mesh.stats["elements"]


def test_pieces_hinged_at_a_corner_are_dropped() -> None:
    block = [(i, j, kk) for i in range(4) for j in range(4) for kk in range(4)]
    mesh = fm.voxel_mesh(np.zeros(3), np.ones(3), np.array([*block, (4, 4, 4)]), 65.0)
    assert mesh.stats["elements"] == 64 and mesh.stats["dropped_fragments"] == 1
    out = fs.solve(mesh, STEEL, ["x-min"], [fs.Load("x-max", force=(0, 0, -10))])
    assert out.stats["cg_converged"]
