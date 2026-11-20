"""B-rep topology inspection: what a solid is made of and whether it is a closed manifold.

A boundary representation is a graph of topological entities (vertices, edges, loops,
faces, shells, solids) bound to geometry (points, curves, surfaces). This module counts the
entities, checks the Euler-Poincare formula for manifold solids

    V - E + F - (L - F) = 2 (S - G)

(V vertices, E edges, F faces, L loops of which L - F are inner rings, S shells, G genus:
the number of through-holes), finds free edges (on one face only: a gap, the solid is not
watertight) and non-manifold edges (on more than two faces), and lists the kinds of curve
and surface the entities carry. It also computes the curves where a boolean tool meets the
body it is applied to (the section a union, cut or intersection is computed along).

Open CASCADE closes periodic surfaces with seam edges (a cylinder's side meets itself along
one edge, used twice by that face) and collapses a sphere's poles to degenerate edges (no
length): degenerate edges and their pole vertices are left out of the counts, and a seam
counts as two uses by its face, so the formula holds for spheres (G = 0) and tori (G = 1).
"""

from dataclasses import asdict, dataclass, field
from typing import Any

import cadquery as cq
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.GCPnts import GCPnts_AbscissaPoint
from OCP.GeomAbs import GeomAbs_CurveType, GeomAbs_SurfaceType
from OCP.TopAbs import (
    TopAbs_EDGE,
    TopAbs_FACE,
    TopAbs_SHELL,
    TopAbs_SOLID,
    TopAbs_VERTEX,
    TopAbs_WIRE,
)
from OCP.TopExp import TopExp, TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.TopTools import TopTools_IndexedMapOfShape

SURFACE_NAMES = {
    GeomAbs_SurfaceType.GeomAbs_Plane: "plane",
    GeomAbs_SurfaceType.GeomAbs_Cylinder: "cylinder",
    GeomAbs_SurfaceType.GeomAbs_Cone: "cone",
    GeomAbs_SurfaceType.GeomAbs_Sphere: "sphere",
    GeomAbs_SurfaceType.GeomAbs_Torus: "torus",
    GeomAbs_SurfaceType.GeomAbs_BezierSurface: "bezier",
    GeomAbs_SurfaceType.GeomAbs_BSplineSurface: "bspline",
    GeomAbs_SurfaceType.GeomAbs_SurfaceOfRevolution: "revolution",
    GeomAbs_SurfaceType.GeomAbs_SurfaceOfExtrusion: "extrusion",
    GeomAbs_SurfaceType.GeomAbs_OffsetSurface: "offset",
}
CURVE_NAMES = {
    GeomAbs_CurveType.GeomAbs_Line: "line",
    GeomAbs_CurveType.GeomAbs_Circle: "circle",
    GeomAbs_CurveType.GeomAbs_Ellipse: "ellipse",
    GeomAbs_CurveType.GeomAbs_Hyperbola: "hyperbola",
    GeomAbs_CurveType.GeomAbs_Parabola: "parabola",
    GeomAbs_CurveType.GeomAbs_BezierCurve: "bezier",
    GeomAbs_CurveType.GeomAbs_BSplineCurve: "bspline",
    GeomAbs_CurveType.GeomAbs_OffsetCurve: "offset",
}


@dataclass
class Topology:
    vertices: int
    edges: int
    loops: int
    faces: int
    shells: int
    solids: int
    rings: int  # inner loops (holes in faces): loops - faces
    euler: int  # V - E + F - (L - F)
    genus: float  # S - euler / 2: through-holes of a closed manifold (whole when it balances)
    balanced: bool  # the Euler-Poincare formula holds with a whole, non-negative genus
    free_edges: int  # used by one face only: the boundary is open (not watertight)
    nonmanifold_edges: int  # used by more than two faces
    degenerate_edges: int  # collapsed (sphere poles), left out of V and E
    seam_edges: int  # a periodic face meeting itself
    watertight: bool
    valid: bool  # the kernel's own validity check (geometry and topology)
    surfaces: dict[str, int] = field(default_factory=dict)  # face count by surface type
    curves: dict[str, int] = field(default_factory=dict)  # edge count by curve type
    area: float = 0.0  # mm^2
    volume: float = 0.0  # mm^3

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _map(shape: Any, kind: Any) -> TopTools_IndexedMapOfShape:
    out = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, kind, out)
    return out


def topology(shape: cq.Shape) -> Topology:
    """Count and check the topology of a shape (normally one or more solids)."""
    s = shape.wrapped
    edges = _map(s, TopAbs_EDGE)
    faces = _map(s, TopAbs_FACE)
    wires = _map(s, TopAbs_WIRE)
    shells = _map(s, TopAbs_SHELL)
    solids = _map(s, TopAbs_SOLID)

    # Edge uses: every occurrence of an edge in a face's boundary (a seam occurs twice in
    # its own face). Walking the faces' edges is fast; OCP's Python iteration over OCCT
    # shape lists (edge -> faces ancestor maps) is about 1000 times slower.
    uses = [0] * (edges.Extent() + 1)
    seams = 0
    for i in range(1, faces.Extent() + 1):
        local: dict[int, int] = {}
        walk = TopExp_Explorer(faces.FindKey(i), TopAbs_EDGE)
        while walk.More():
            idx = edges.FindIndex(walk.Current())
            uses[idx] += 1
            local[idx] = local.get(idx, 0) + 1
            walk.Next()
        seams += sum(1 for n in local.values() if n >= 2)
    free = nonmanifold = degenerate = 0
    curves: dict[str, int] = {}
    poles = TopTools_IndexedMapOfShape()  # vertices only on degenerate edges
    real_vertices = TopTools_IndexedMapOfShape()
    for i in range(1, edges.Extent() + 1):
        edge = TopoDS.Edge_s(edges.FindKey(i))
        if BRep_Tool.Degenerated_s(edge):
            degenerate += 1
            TopExp.MapShapes_s(edge, TopAbs_VERTEX, poles)
            continue
        TopExp.MapShapes_s(edge, TopAbs_VERTEX, real_vertices)
        if uses[i] == 1:
            free += 1
        elif uses[i] > 2:
            nonmanifold += 1
        name = CURVE_NAMES.get(BRepAdaptor_Curve(edge).GetType(), "other")
        curves[name] = curves.get(name, 0) + 1

    surfaces: dict[str, int] = {}
    for i in range(1, faces.Extent() + 1):
        name = SURFACE_NAMES.get(
            BRepAdaptor_Surface(TopoDS.Face_s(faces.FindKey(i))).GetType(), "other"
        )
        surfaces[name] = surfaces.get(name, 0) + 1

    v = real_vertices.Extent()
    e = edges.Extent() - degenerate
    f, loops, n_shells = faces.Extent(), wires.Extent(), shells.Extent()
    rings = loops - f
    euler = v - e + f - rings
    genus = n_shells - euler / 2.0
    balanced = genus >= 0 and abs(genus - round(genus)) < 1e-9
    try:
        area = shape.Area()
    except Exception:  # an open or broken shape may have no well-defined area
        area = 0.0
    try:
        vol = shape.Volume() if solids.Extent() else 0.0
    except Exception:
        vol = 0.0
    return Topology(
        vertices=v, edges=e, loops=loops, faces=f, shells=n_shells, solids=solids.Extent(),
        rings=rings, euler=euler, genus=genus, balanced=balanced, free_edges=free,
        nonmanifold_edges=nonmanifold, degenerate_edges=degenerate, seam_edges=seams,
        watertight=free == 0 and nonmanifold == 0 and n_shells > 0,
        valid=BRepCheck_Analyzer(s).IsValid(), surfaces=surfaces, curves=curves,
        area=area, volume=vol,
    )  # fmt: skip


@dataclass
class Section:
    """Where a boolean tool meets the body: the intersection curves the boolean follows."""

    curves: int
    length: float  # mm
    polylines: list[list[tuple[float, float, float]]]  # sampled points along each curve

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def section(body: cq.Shape, tool: cq.Shape, samples: int = 24, max_points: int = 6000) -> Section:
    """The intersection curves of two shapes' boundaries, sampled for display."""
    op = BRepAlgoAPI_Section(body.wrapped, tool.wrapped, False)
    op.ComputePCurveOn1(False)
    op.Approximation(False)
    op.Build()
    if not op.IsDone():
        return Section(curves=0, length=0.0, polylines=[])
    edges = _map(op.Shape(), TopAbs_EDGE)
    count = edges.Extent()
    per = max(2, min(samples, max_points // max(count, 1)))
    lines, total = [], 0.0
    for i in range(1, count + 1):
        curve = BRepAdaptor_Curve(TopoDS.Edge_s(edges.FindKey(i)))
        t0, t1 = curve.FirstParameter(), curve.LastParameter()
        total += GCPnts_AbscissaPoint.Length_s(curve)
        pts = []
        for j in range(per):
            p = curve.Value(t0 + (t1 - t0) * j / (per - 1))
            pts.append((p.X(), p.Y(), p.Z()))
        lines.append(pts)
    return Section(curves=count, length=total, polylines=lines)
