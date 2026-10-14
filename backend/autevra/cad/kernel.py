"""The only module that talks to the CAD kernel (CadQuery on Open CASCADE).

Everything else in Autevra handles ``Shape`` values opaquely and calls the
functions here, so swapping CadQuery for build123d or raw OCP stays local.
Units are millimetres; axes follow ISO 8855 (X forward, Y left, Z up).
"""

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

import cadquery as cq
from OCP.BRep import BRep_Tool
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from OCP.gp import gp_Trsf
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

Shape = cq.Shape
Matrix = Sequence[Sequence[float]]  # 4 x 4, row-major, translation in the last column

_Y = cq.Vector(0, 1, 0)
_X = cq.Vector(1, 0, 0)
_Z = cq.Vector(0, 0, 1)


class KernelError(RuntimeError):
    """The kernel failed to build valid geometry."""


def box(x: tuple[float, float], y: tuple[float, float], z: tuple[float, float]) -> Shape:
    """Axis-aligned box between the given (min, max) extents."""
    return cq.Solid.makeBox(x[1] - x[0], y[1] - y[0], z[1] - z[0], pnt=cq.Vector(x[0], y[0], z[0]))


def cylinder_y(radius: float, y: tuple[float, float], x: float = 0.0, z: float = 0.0) -> Shape:
    """Solid cylinder whose axis is parallel to Y, from y[0] to y[1]."""
    return cq.Solid.makeCylinder(radius, y[1] - y[0], pnt=cq.Vector(x, y[0], z), dir=_Y)


def cylinder_x(radius: float, x: tuple[float, float], y: float = 0.0, z: float = 0.0) -> Shape:
    return cq.Solid.makeCylinder(radius, x[1] - x[0], pnt=cq.Vector(x[0], y, z), dir=_X)


def cylinder_z(radius: float, z: tuple[float, float], x: float = 0.0, y: float = 0.0) -> Shape:
    return cq.Solid.makeCylinder(radius, z[1] - z[0], pnt=cq.Vector(x, y, z[0]), dir=_Z)


def ring_z(outer: float, inner: float, z: tuple[float, float]) -> Shape:
    """Hollow cylinder (annulus) on the Z axis."""
    return cut(cylinder_z(outer, z), cylinder_z(inner, (z[0] - 1, z[1] + 1)))


def ring_x(outer: float, inner: float, x: tuple[float, float], z: float = 0.0) -> Shape:
    """Hollow cylinder on an axis parallel to X at height ``z``."""
    return cut(cylinder_x(outer, x, z=z), cylinder_x(inner, (x[0] - 1, x[1] + 1), z=z))


def helical_coil(radius: float, height: float, turns: float, wire: float, z0: float) -> Shape:
    """Round wire swept along a helix about Z, from ``z0`` to ``z0 + height``."""
    if height / turns <= wire:
        raise KernelError("coil pitch is not larger than the wire diameter (coils overlap)")
    path = cq.Wire.makeHelix(height / turns, height, radius, center=cq.Vector(0, 0, z0))
    profile = cq.Wire.makeCircle(wire / 2.0, cq.Vector(radius, 0, z0), _Y)
    coil = cq.Solid.sweep(profile, [], path, isFrenet=True)
    if not coil.isValid():
        raise KernelError("kernel produced an invalid coil")
    return coil


def ring_y(outer: float, inner: float, y: tuple[float, float]) -> Shape:
    """Hollow cylinder (annulus) on the Y axis."""
    return cut(cylinder_y(outer, y), cylinder_y(inner, (y[0] - 1, y[1] + 1)))


def rect_tube_x(
    x: tuple[float, float], y: tuple[float, float], z: tuple[float, float], wall: float
) -> Shape:
    """Open-ended hollow rectangular tube running along X."""
    outer = box(x, y, z)
    inner = box((x[0] - 1, x[1] + 1), (y[0] + wall, y[1] - wall), (z[0] + wall, z[1] - wall))
    return cut(outer, inner)


def rect_tube_y(
    x: tuple[float, float], y: tuple[float, float], z: tuple[float, float], wall: float
) -> Shape:
    """Open-ended hollow rectangular tube running along Y."""
    outer = box(x, y, z)
    inner = box((x[0] + wall, x[1] - wall), (y[0] - 1, y[1] + 1), (z[0] + wall, z[1] - wall))
    return cut(outer, inner)


def ruled_loft(sections: Sequence[Sequence[tuple[float, float, float]]]) -> Shape:
    """Solid lofted through closed polygons (straight lines between sections)."""
    wires = [cq.Wire.makePolygon([cq.Vector(*p) for p in s], close=True) for s in sections]
    return cq.Solid.makeLoft(wires, ruled=True)


def rounded_rect(
    x: tuple[float, float], half_w: float, r_front: float, r_rear: float, z: float
) -> cq.Wire:
    """Closed plan outline at height ``z``: four straight edges and four exact corner arcs
    (front corners of radius ``r_front`` at max x, rear corners ``r_rear``)."""
    rear, front = x
    rf, rr = max(r_front, 0.1), max(r_rear, 0.1)

    def v(px: float, py: float) -> cq.Vector:
        return cq.Vector(px, py, z)

    def arc(cx: float, cy: float, r: float, a0: float) -> cq.Edge:
        a = [math.radians(a0 + d) for d in (0.0, 45.0, 90.0)]
        p0, pm, p1 = (v(cx + r * math.cos(t), cy + r * math.sin(t)) for t in a)
        return cq.Edge.makeThreePointArc(p0, pm, p1)

    edges = [
        cq.Edge.makeLine(v(front, -half_w + rf), v(front, half_w - rf)),
        arc(front - rf, half_w - rf, rf, 0.0),
        cq.Edge.makeLine(v(front - rf, half_w), v(rear + rr, half_w)),
        arc(rear + rr, half_w - rr, rr, 90.0),
        cq.Edge.makeLine(v(rear, half_w - rr), v(rear, -half_w + rr)),
        arc(rear + rr, -half_w + rr, rr, 180.0),
        cq.Edge.makeLine(v(rear + rr, -half_w), v(front - rf, -half_w)),
        arc(front - rf, -half_w + rf, rf, 270.0),
    ]
    return cq.Wire.assembleEdges(edges)


def smooth_loft(sections: Sequence[cq.Wire], ruled: bool = False) -> Shape:
    """Solid through exact section outlines (no overshoot within a section). Smooth between
    sections, or ``ruled``: straight bands meeting in crisp character lines, and about five
    times cheaper in later booleans. Sections need the same edge structure."""
    return cq.Solid.makeLoft(list(sections), ruled=ruled)


def prism_y(profile: Sequence[tuple[float, float]], y: tuple[float, float]) -> Shape:
    """Solid from a closed (x, z) profile in the XZ plane, extruded from y[0] to y[1]."""
    pts = [cq.Vector(x, y[0], z) for x, z in profile]
    face = cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True))
    return cq.Solid.extrudeLinear(face, cq.Vector(0, y[1] - y[0], 0))


def prism_z(outline: Sequence[tuple[float, float]], z: tuple[float, float]) -> Shape:
    """Solid from a closed (x, y) outline in the XY plane, extruded from z[0] to z[1]."""
    pts = [cq.Vector(x, y, z[0]) for x, y in outline]
    face = cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True))
    return cq.Solid.extrudeLinear(face, cq.Vector(0, 0, z[1] - z[0]))


def intersect(shape: Shape, other: Shape) -> Shape:
    return _clean(shape.intersect(other))


def cut(shape: Shape, *tools: Shape) -> Shape:
    return _clean(shape.cut(*tools))


def fuse(shape: Shape, *others: Shape) -> Shape:
    return _clean(shape.fuse(*others))


def fillet_circular_edges_outer(shape: Shape, edge_radius: float, radius: float) -> Shape:
    """Fillet the circular edges of radius ``edge_radius`` (e.g. tyre shoulders)."""
    edges = [
        e
        for e in shape.Edges()
        if e.geomType() == "CIRCLE" and abs(e.radius() - edge_radius) < 1e-6
    ]
    return _clean(shape.fillet(radius, edges))


def translate(shape: Shape, dx: float, dy: float, dz: float) -> Shape:
    return shape.translate(cq.Vector(dx, dy, dz))


def rotate_y(shape: Shape, degrees: float, centre: tuple[float, float, float]) -> Shape:
    c = cq.Vector(*centre)
    return shape.rotate(c, c + _Y, degrees)


def _clean(shape: Shape) -> Shape:
    shape = shape.clean()
    if not shape.isValid():
        raise KernelError("kernel produced invalid geometry")
    return shape


def volume(shape: Shape) -> float:
    return shape.Volume()


def is_valid(shape: Shape) -> bool:
    return shape.isValid()


def bounds(shape: Shape) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    bb = cq.BoundBox._fromTopoDS(shape.wrapped, optimal=True)  # tight box, not the fast loose one
    return (bb.xmin, bb.ymin, bb.zmin), (bb.xmax, bb.ymax, bb.zmax)


def solid_count(shape: Shape) -> int:
    return len(shape.Solids())


@dataclass(frozen=True)
class Mesh:
    vertices: list[float]  # flat x, y, z
    indices: list[int]  # flat triangle vertex indices


def tessellate(shape: Shape, tolerance: float = 0.5, angular: float = 0.3) -> Mesh:
    """Triangle mesh of a shape (same result as ``cq.Shape.tessellate``, much faster).

    CadQuery's version iterates OCCT arrays through Python iterators, which costs several
    milliseconds per face; indexed access and a face explorer avoid that.
    """
    if not BRepTools.Triangulation_s(shape.wrapped, tolerance):
        BRepMesh_IncrementalMesh(shape.wrapped, tolerance, True, angular)
    vertices: list[float] = []
    indices: list[int] = []
    offset = 0
    explorer = TopExp_Explorer(shape.wrapped, TopAbs_FACE)
    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        explorer.Next()
        loc = TopLoc_Location()
        poly = BRep_Tool.Triangulation_s(face, loc)
        if poly is None:
            continue
        trsf = loc.Transformation()
        for i in range(1, poly.NbNodes() + 1):
            p = poly.Node(i).Transformed(trsf)
            vertices += (p.X(), p.Y(), p.Z())
        reverse = face.Orientation() == TopAbs_REVERSED
        for i in range(1, poly.NbTriangles() + 1):
            a, b, c = poly.Triangle(i).Get()
            indices += (
                (a + offset - 1, c + offset - 1, b + offset - 1)
                if reverse
                else (a + offset - 1, b + offset - 1, c + offset - 1)
            )
        offset += poly.NbNodes()
    return Mesh(vertices=vertices, indices=indices)


def location(matrix: Matrix) -> cq.Location:
    t = gp_Trsf()
    m = matrix
    t.SetValues(
        m[0][0], m[0][1], m[0][2], m[0][3],
        m[1][0], m[1][1], m[1][2], m[1][3],
        m[2][0], m[2][1], m[2][2], m[2][3],
    )  # fmt: skip
    return cq.Location(t)


def min_distance(a: Shape, a_matrix: Matrix, b: Shape, b_matrix: Matrix) -> float:
    """Exact minimum distance between two placed shapes (OCCT BRepExtrema), mm.

    Overlapping solids give 0, including one solid fully inside the other.
    """
    placed_a, placed_b = a.moved(location(a_matrix)), b.moved(location(b_matrix))
    dist = BRepExtrema_DistShapeShape(placed_a.wrapped, placed_b.wrapped)
    if not dist.IsDone():
        raise KernelError("distance computation failed")
    # Boundaries apart: still overlapping if one solid contains the other.
    if dist.Value() > 1e-9 and (_contains(placed_a, placed_b) or _contains(placed_b, placed_a)):
        return 0.0
    return dist.Value()


def _contains(outer: Shape, inner: Shape) -> bool:
    point = inner.Vertices()[0].Center() if inner.Vertices() else inner.Center()
    return outer.isInside(point)


@dataclass(frozen=True)
class Part:
    name: str
    shape: Shape
    matrix: Matrix
    color: tuple[float, float, float]


def export_step(parts: Iterable[Part], path: Path, name: str = "vehicle") -> Path:
    """Write an assembly STEP file: one named, placed and coloured solid per part."""
    assembly = cq.Assembly(name=name)
    for part in parts:
        assembly.add(
            part.shape, name=part.name, loc=location(part.matrix), color=cq.Color(*part.color)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    assembly.export(str(path), exportType="STEP")
    return path


def import_step(path: Path) -> Shape:
    return cq.importers.importStep(str(path)).val()
