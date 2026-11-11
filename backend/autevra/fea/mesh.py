"""Volume meshes for linear structural analysis (educational, but every number is real).

Two meshers (plus quadratic TET10 made from the tetrahedra), all measured and reported
rather than assumed good:

- Tetrahedra (TET4): the CAD surface tessellation and an interior BCC lattice of points are
  tetrahedralised by Delaunay (Qhull, via SciPy); a tetrahedron is kept when the kernel's
  solid classifier puts its centroid inside the part. This does not recover the boundary
  exactly on deep concavities (an industrial mesher such as Gmsh or Netgen constrains the
  boundary), so the mesh volume / CAD volume ratio is reported with every mesh.
- Hexahedra (HEX8): a voxel grid; a voxel is kept when its centre is inside the part.
  Stair-stepped boundaries; exact on boxes; the basis of the topology optimisation.

Element quality: the radius ratio q = 3 r_in / r_circ of each tetrahedron (1 for a regular
tetrahedron, near 0 for a sliver).
"""

from dataclasses import dataclass, field

import numpy as np
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN, TopAbs_ON

from autevra.cad import kernel as k

MAX_NODES = 30_000


class MeshError(ValueError):
    """The part cannot be meshed as asked (too fine, too coarse, or empty)."""


@dataclass
class Mesh:
    kind: str  # "tet4", "tet10" or "hex8"
    nodes: np.ndarray  # (N, 3) mm
    elements: np.ndarray  # (E, 4) or (E, 8) node indices
    boundary: np.ndarray  # (F, 3) outward triangles on the surface (for loads and display)
    cad_volume: float
    stats: dict = field(default_factory=dict)
    boundary6: np.ndarray | None = None  # (F, 6) quadratic surface triangles (TET10 only)


def _classifier(shape: k.Shape):  # type: ignore[no-untyped-def]
    cls = BRepClass3d_SolidClassifier(shape.wrapped)

    def inside(p: np.ndarray, tol: float = 1e-3) -> bool:
        cls.Perform(gp_Pnt(float(p[0]), float(p[1]), float(p[2])), tol)
        return cls.State() in (TopAbs_IN, TopAbs_ON)

    return inside


def tet_volumes(nodes: np.ndarray, tets: np.ndarray) -> np.ndarray:
    x = nodes[tets]
    return (
        np.einsum("ij,ij->i", x[:, 1] - x[:, 0], np.cross(x[:, 2] - x[:, 0], x[:, 3] - x[:, 0]))
        / 6.0
    )


def radius_ratio(nodes: np.ndarray, tets: np.ndarray) -> np.ndarray:
    """q = 3 r_in / r_circ per tetrahedron (1: regular, 0: degenerate)."""
    x = nodes[tets]
    vol = np.abs(tet_volumes(nodes, tets))
    faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    area = sum(
        0.5 * np.linalg.norm(np.cross(x[:, b] - x[:, a], x[:, c] - x[:, a]), axis=1)
        for a, b, c in faces
    )
    r_in = 3 * vol / np.maximum(area, 1e-30)
    a, b, c = x[:, 1] - x[:, 0], x[:, 2] - x[:, 0], x[:, 3] - x[:, 0]
    num = (np.sum(a * a, 1)[:, None] * np.cross(b, c) + np.sum(b * b, 1)[:, None] * np.cross(c, a)
           + np.sum(c * c, 1)[:, None] * np.cross(a, b))  # fmt: skip
    r_circ = np.linalg.norm(num, axis=1) / np.maximum(12 * vol, 1e-30)
    return np.clip(3 * r_in / np.maximum(r_circ, 1e-30), 0.0, 1.0)


def solid_pieces(elements: np.ndarray, faces: list[tuple[int, ...]]) -> np.ndarray:
    """Keep-mask of the elements in face-connected pieces of real size.

    Elements joined to the rest only at a node or an edge are mechanisms: they turn freely
    about the hinge, which makes K singular. Such fragments (a few elements left by centroid
    classification at a coarse size, or voxels touching at a corner) are dropped; separate
    bodies of real size stay (each then needs its own support)."""
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components

    n_el, local = len(elements), np.asarray(faces)
    keys = np.sort(elements[:, local].reshape(-1, local.shape[1]), axis=1)
    owner = np.repeat(np.arange(n_el), len(faces))
    _, inv = np.unique(keys, axis=0, return_inverse=True)
    order = np.argsort(inv, kind="stable")
    same = inv[order][1:] == inv[order][:-1]
    a, b = owner[order][:-1][same], owner[order][1:][same]
    graph = sp.coo_matrix((np.ones(len(a)), (a, b)), shape=(n_el, n_el))
    _, label = connected_components(graph, directed=False)
    size = np.bincount(label)
    return size[label] >= max(10, 0.01 * n_el)


def _boundary(elements: np.ndarray, faces: list[tuple[int, ...]], nodes: np.ndarray) -> np.ndarray:
    """Element faces used once (the surface), as outward triangles."""
    local = np.asarray(faces)
    all_faces = elements[:, local].reshape(-1, local.shape[1])
    owner = np.repeat(np.arange(len(elements)), len(faces))
    key = np.sort(all_faces, axis=1)
    _, idx, counts = np.unique(key, axis=0, return_index=True, return_counts=True)
    once = idx[counts == 1]
    tris = []
    centroids = nodes[elements].mean(axis=1)
    for f_i in once:
        f = all_faces[f_i]
        polys = [f] if len(f) == 3 else [f[[0, 1, 2]], f[[0, 2, 3]]]
        c = centroids[owner[f_i]]
        for t in polys:
            p = nodes[t]
            n = np.cross(p[1] - p[0], p[2] - p[0])
            if n @ (p.mean(axis=0) - c) < 0:
                t = t[[0, 2, 1]]
            tris.append(t)
    return np.asarray(tris, dtype=int).reshape(-1, 3)


def _sample_surface(vertices: np.ndarray, triangles: np.ndarray, size: float) -> np.ndarray:
    """Points on the surface about ``size`` apart: each tessellation triangle subdivided
    on a barycentric grid (a coarse tessellation of flat faces has corners only)."""
    out = [vertices]
    for tri in triangles:
        a, b, c = vertices[tri]
        n = int(
            np.ceil(max(np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)) / size)
        )
        if n <= 1:
            continue
        ij = [(i, j) for i in range(n + 1) for j in range(n + 1 - i)]
        w = np.array([(i / n, j / n) for i, j in ij])
        out.append(a + w[:, :1] * (b - a) + w[:, 1:] * (c - a))
    return _thin(np.concatenate(out), 0.7 * size, keep=len(vertices))


def _thin(points: np.ndarray, radius: float, keep: int = 0) -> np.ndarray:
    """Greedy minimum-distance thinning: no two kept points closer than ``radius``.

    The first ``keep`` points (the tessellation's corners, which carry the sharp edges) are
    taken first. Uneven spacing on the surface is what makes Delaunay slivers there."""
    from scipy.spatial import cKDTree

    tree = cKDTree(points)
    taken = np.zeros(len(points), dtype=bool)
    blocked = np.zeros(len(points), dtype=bool)
    order = np.concatenate([np.arange(keep), np.arange(keep, len(points))])
    for i in order:
        if blocked[i] and i >= keep:
            continue
        taken[i] = True
        blocked[tree.query_ball_point(points[i], radius)] = True
    return points[taken]


def tet_mesh(shape: k.Shape, size: float) -> Mesh:
    from scipy.spatial import Delaunay

    (x0, y0, z0), (x1, y1, z1) = k.bounds(shape)
    extent = np.array([x1 - x0, y1 - y0, z1 - z0])
    if size <= 0 or np.prod(extent / size + 1) > 4 * MAX_NODES:
        raise MeshError(
            f"an element size of {size:g} mm is too fine for this part; try a larger one"
        )
    surf = k.tessellate(shape, tolerance=max(size / 8.0, 0.05), angular=0.35)
    surface = _sample_surface(np.asarray(surf.vertices, dtype=float).reshape(-1, 3),
                              np.asarray(surf.indices, dtype=int).reshape(-1, 3), size)  # fmt: skip
    pts = [surface]
    inside = _classifier(shape)
    # interior body-centred cubic lattice, kept off the surface to avoid slivers: a cubic
    # lattice is cospherical everywhere (Delaunay then splits each cube into flat slivers);
    # the BCC lattice tetrahedralises into well-shaped tetrahedra. Cube edge 2^(1/3) size
    # keeps the point density at one per size^3.
    a_bcc = size * 2 ** (1 / 3)
    lo, hi = np.array([x0, y0, z0]), np.array([x1, y1, z1])
    axes = [np.arange(lo[i] + a_bcc / 2, hi[i], a_bcc) for i in range(3)]
    if all(len(ax) for ax in axes):
        from scipy.spatial import cKDTree

        cubic = np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1).reshape(-1, 3)
        grid = np.concatenate([cubic, cubic + a_bcc / 2])
        grid = grid[np.all(grid < hi, axis=1)]
        near, _ = cKDTree(surface).query(grid)
        grid = grid[near > 0.6 * size]
        keep = [p for p in grid if inside(p)]
        if keep:
            pts.append(np.asarray(keep))
    nodes = np.unique(np.round(np.concatenate(pts), 6), axis=0)
    if len(nodes) > MAX_NODES:
        raise MeshError(
            f"{len(nodes)} nodes is more than this demo solves ({MAX_NODES}); use a larger size"
        )
    tets = Delaunay(nodes, qhull_options="QJ Qbb Qc").simplices
    vol = tet_volumes(nodes, tets)
    tets[vol < 0] = tets[vol < 0][:, [0, 2, 1, 3]]  # positive orientation
    vol = np.abs(vol)
    centroids = nodes[tets].mean(axis=1)
    keep = np.array([v > 1e-9 * size**3 and inside(c) for v, c in zip(vol, centroids, strict=True)])
    tets = tets[keep]
    if len(tets) == 0:
        raise MeshError("no elements inside the part; try a smaller size")
    pieces = solid_pieces(tets, TET_FACES)
    dropped = int(np.sum(~pieces))
    tets = tets[pieces]
    used = np.unique(tets)
    remap = -np.ones(len(nodes), dtype=int)
    remap[used] = np.arange(len(used))
    nodes, tets = nodes[used], remap[tets]
    q = radius_ratio(nodes, tets)
    cad = k.volume(shape)
    mesh_vol = float(tet_volumes(nodes, tets).sum())
    boundary = _boundary(tets, TET_FACES, nodes)
    return Mesh("tet4", nodes, tets, boundary, cad, {
        "nodes": len(nodes), "elements": len(tets), "size": size,
        "volume_ratio": mesh_vol / cad if cad else 0.0,
        "quality_min": float(q.min()), "quality_mean": float(q.mean()),
        "slivers": int(np.sum(q < 0.1)), "dropped_fragments": dropped,
        "method": "Delaunay tetrahedralisation (Qhull) of the spaced surface samples and an "
        "interior BCC lattice; tetrahedra kept by centroid classification against the "
        "B-rep; fragments hinged to the body at a node or an edge dropped",
    })  # fmt: skip


TET_FACES = [(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)]
HEX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


def hex_mesh(shape: k.Shape, size: float) -> Mesh:
    (x0, y0, z0), (x1, y1, z1) = k.bounds(shape)
    n = np.maximum(np.round(np.array([x1 - x0, y1 - y0, z1 - z0]) / size).astype(int), 1)
    if np.prod(n + 1) > MAX_NODES * 2:
        raise MeshError(
            f"an element size of {size:g} mm is too fine for this part; try a larger one"
        )
    h = np.array([x1 - x0, y1 - y0, z1 - z0]) / n
    inside = _classifier(shape)
    cells = [(i, j, kk) for i in range(n[0]) for j in range(n[1]) for kk in range(n[2])
             if inside(np.array([x0, y0, z0]) + (np.array([i, j, kk]) + 0.5) * h)]  # fmt: skip
    if not cells:
        raise MeshError("no voxels inside the part; try a smaller size")
    return voxel_mesh(np.array([x0, y0, z0]), h, np.asarray(cells), k.volume(shape))


def voxel_mesh(origin: np.ndarray, h: np.ndarray, cells: np.ndarray, cad_volume: float) -> Mesh:
    """HEX8 elements on the given voxel cells (i, j, k), with shared corner nodes."""
    cells = np.asarray(cells)
    corners = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])  # fmt: skip
    all_corners = (cells[:, None, :] + corners[None]).reshape(-1, 3)
    uniq, inv = np.unique(all_corners, axis=0, return_inverse=True)
    elements = inv.reshape(-1, 8)
    pieces = solid_pieces(elements, HEX_FACES)
    dropped = int(np.sum(~pieces))
    if dropped:
        cells = cells[pieces]
        all_corners = (cells[:, None, :] + corners[None]).reshape(-1, 3)
        uniq, inv = np.unique(all_corners, axis=0, return_inverse=True)
        elements = inv.reshape(-1, 8)
    nodes = origin + uniq * h
    if len(nodes) > MAX_NODES:
        raise MeshError(
            f"{len(nodes)} nodes is more than this demo solves ({MAX_NODES}); use a larger size"
        )
    boundary = _boundary(elements, HEX_FACES, nodes)
    vol = float(len(cells) * np.prod(h))
    return Mesh("hex8", nodes, elements, boundary, cad_volume, {
        "nodes": len(nodes), "elements": len(elements), "size": float(h.max()),
        "volume_ratio": vol / cad_volume if cad_volume else 1.0,
        "quality_min": float(h.min() / h.max()), "quality_mean": float(h.min() / h.max()),
        "slivers": 0, "dropped_fragments": dropped,
        "method": "voxel grid; voxels kept when their centre is inside the B-rep",
    })  # fmt: skip


TET10_EDGES = [(0, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3)]  # midside nodes 4..9


def to_tet10(mesh: Mesh) -> Mesh:
    """Quadratic tetrahedra: a node at the middle of every edge of a TET4 mesh (straight
    sides). Boundary triangles become 6-node triangles (corners, then mid-edges ab, bc, ca)."""
    pairs = np.sort(mesh.elements[:, TET10_EDGES].reshape(-1, 2), axis=1)
    edges, inv = np.unique(pairs, axis=0, return_inverse=True)
    mid = len(mesh.nodes) + inv.reshape(-1, 6)
    nodes = np.concatenate([mesh.nodes, mesh.nodes[edges].mean(axis=1)])
    if len(nodes) > 2 * MAX_NODES:
        raise MeshError(
            f"{len(nodes)} TET10 nodes is more than this demo solves ({2 * MAX_NODES}); "
            "use a larger size"
        )
    lookup = {(int(a), int(b)): len(mesh.nodes) + i for i, (a, b) in enumerate(edges)}

    def m(a: np.ndarray, b: np.ndarray) -> list[int]:
        return [lookup[(min(x, y), max(x, y))] for x, y in zip(a.tolist(), b.tolist(), strict=True)]

    t = mesh.boundary
    boundary6 = np.column_stack([t, m(t[:, 0], t[:, 1]), m(t[:, 1], t[:, 2]), m(t[:, 2], t[:, 0])])
    method = mesh.stats["method"] + "; mid-edge nodes added for quadratic TET10"
    stats = {**mesh.stats, "nodes": len(nodes), "corner_nodes": len(mesh.nodes), "method": method}
    elements = np.hstack([mesh.elements, mid])
    return Mesh("tet10", nodes, elements, mesh.boundary, mesh.cad_volume, stats, boundary6)
