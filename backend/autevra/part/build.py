"""Build a part's feature tree into one solid with OCCT (CadQuery).

Features run in order. A failing feature is reported with its id and stops the build at
that point (the result so far is kept), so a mistake late in the tree never loses the
earlier work and the user sees which feature to fix.
"""

import math
from dataclasses import dataclass, field

import cadquery as cq

from autevra.assembly.transforms import Matrix
from autevra.cad import kernel as k
from autevra.part import features as f

_AXIS = {f.Axis.X: cq.Vector(1, 0, 0), f.Axis.Y: cq.Vector(0, 1, 0), f.Axis.Z: cq.Vector(0, 0, 1)}


@dataclass
class FeatureError:
    feature: str
    message: str


@dataclass
class BuildResult:
    shape: k.Shape | None
    errors: list[FeatureError] = field(default_factory=list)
    built: list[str] = field(default_factory=list)  # ids of features applied


def placement_matrix(at: f.Placement) -> Matrix:
    """4x4 transform of a placement: rotate about X, then Y, then Z, then translate."""
    import numpy as np

    def rot(axis: int, deg: float) -> np.ndarray:
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        m = np.eye(4)
        i, j = [(1, 2), (2, 0), (0, 1)][axis]
        m[i, i], m[i, j], m[j, i], m[j, j] = c, -s, s, c
        return m

    m = rot(2, at.rz) @ rot(1, at.ry) @ rot(0, at.rx)
    m[:3, 3] = (at.x, at.y, at.z)
    return m


def _place(shape: k.Shape, at: f.Placement) -> k.Shape:
    return shape.moved(k.location(placement_matrix(at)))


def _plane_point(plane: f.Plane, u: float, v: float) -> cq.Vector:
    return {f.Plane.XY: cq.Vector(u, v, 0), f.Plane.XZ: cq.Vector(u, 0, v),
            f.Plane.YZ: cq.Vector(0, u, v)}[plane]  # fmt: skip


def _normal(plane: f.Plane) -> cq.Vector:
    return {f.Plane.XY: cq.Vector(0, 0, 1), f.Plane.XZ: cq.Vector(0, 1, 0),
            f.Plane.YZ: cq.Vector(1, 0, 0)}[plane]  # fmt: skip


def _solid(feat: f.Box | f.Cylinder | f.Sphere | f.Extrude | f.Revolve | f.Loft | f.Sweep
           ) -> k.Shape:  # fmt: skip
    match feat:
        case f.Box(size=(sx, sy, sz)):
            return cq.Solid.makeBox(sx, sy, sz, pnt=cq.Vector(-sx / 2, -sy / 2, -sz / 2))
        case f.Cylinder():
            d = _AXIS[feat.axis]
            return cq.Solid.makeCylinder(feat.radius, feat.height, d * (-feat.height / 2), d)
        case f.Sphere():
            return cq.Solid.makeSphere(feat.radius, angleDegrees1=-90)
        case f.Extrude():
            pts = [_plane_point(feat.plane, u, v) for u, v in feat.points]
            face = cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True))
            n = _normal(feat.plane)
            solid = cq.Solid.extrudeLinear(face, n * feat.depth)
            return solid.translate(n * (-feat.depth / 2)) if feat.symmetric else solid
        case f.Revolve():
            pts = [cq.Vector(r, 0, z) for r, z in feat.points]
            face = cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True))
            return cq.Solid.revolve(face, feat.angle, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
        case f.Loft():
            wires = []
            for s in feat.sections:
                r = min(s.radius, 0.499 * min(s.width, s.height))
                wires.append(k.rounded_rect((-s.width / 2, s.width / 2), s.height / 2, r, r, s.z))
            return cq.Solid.makeLoft(wires, ruled=feat.ruled)
        case f.Sweep():
            return _sweep(feat)
        case f.Wing():
            return _wing(feat)
    raise ValueError(f"unknown feature type {feat.type}")


def naca4(code: str, n: int = 40) -> list[tuple[float, float]]:
    """Unit-chord NACA four-digit section, (x, z) from the trailing edge over the upper
    surface to the leading edge and back along the lower surface (x from 0 at the leading
    edge to 1 at the trailing edge). Standard thickness distribution (open trailing edge)
    and mean camber line; points spaced by cosine for a well-resolved leading edge."""
    m, p, t = int(code[0]) / 100.0, int(code[1]) / 10.0, int(code[2:]) / 100.0
    xs = [0.5 * (1.0 - math.cos(math.pi * i / n)) for i in range(n + 1)]
    upper, lower = [], []
    for x in xs:
        yt = 5.0 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3
                        - 0.1015 * x**4)  # fmt: skip
        if m == 0.0:
            yc, dyc = 0.0, 0.0
        elif x < p:
            yc, dyc = m / p**2 * (2 * p * x - x**2), 2 * m / p**2 * (p - x)
        else:
            yc = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x**2)
            dyc = 2 * m / (1 - p) ** 2 * (p - x)
        th = math.atan(dyc)
        upper.append((x - yt * math.sin(th), yc + yt * math.cos(th)))
        lower.append((x + yt * math.sin(th), yc - yt * math.cos(th)))
    return [*reversed(upper), *lower[1:]]


def _section(code: str, chord: float, x_le: float, y: float, z: float, twist: float) -> cq.Wire:
    """One aerofoil wire at span station y: chord running aft (-X) from the leading edge at
    x_le, rotated by ``twist`` degrees about the quarter chord (nose up positive)."""
    c, s = math.cos(math.radians(twist)), math.sin(math.radians(twist))
    pts = []
    for u, w in naca4(code):
        dx, dz = (0.25 - u) * chord, w * chord  # relative to the quarter chord, X forward
        pts.append(cq.Vector(x_le - 0.25 * chord + dx * c - dz * s, y, z + dx * s + dz * c))
    edges = [cq.Edge.makeSpline(pts)]
    if (pts[0] - pts[-1]).Length > 1e-6:  # close the (thin) open trailing edge
        edges.append(cq.Edge.makeLine(pts[-1], pts[0]))
    return cq.Wire.assembleEdges(edges)


def _wing(feat: f.Wing) -> k.Shape:
    sweep, dihedral = math.radians(feat.sweep), math.radians(feat.dihedral)
    root = _section(feat.naca, feat.root_chord, 0.0, 0.0, 0.0, 0.0)

    def tip(side: float) -> cq.Wire:
        return _section(feat.naca, feat.tip_chord, -feat.span * math.tan(sweep),
                        side * feat.span, feat.span * math.tan(dihedral), feat.twist)  # fmt: skip

    # Both sides as one loft through the root (no boolean across the shared root face,
    # which the kernel does not fuse exactly for spline surfaces).
    wires = [tip(-1.0), root, tip(1.0)] if feat.both_sides else [root, tip(1.0)]
    return cq.Solid.makeLoft(wires, ruled=True)


def _sweep(feat: f.Sweep) -> k.Shape:
    pts = [cq.Vector(*q) for q in feat.path]
    path = cq.Wire.makePolygon(pts)
    if feat.bend_radius > 0.0 and len(pts) > 2:
        path = path.fillet(feat.bend_radius, path.Vertices()[1:-1])
    start, direction = pts[0], (pts[1] - pts[0]).normalized()
    outer = cq.Wire.makeCircle(feat.radius, start, direction)
    inner = [cq.Wire.makeCircle(feat.radius - feat.wall, start, direction)] if feat.wall else []
    return cq.Solid.sweep(outer, inner, path, makeSolid=True, transitionMode="round")


def _modify(shape: k.Shape, feat: f.Shell | f.Fillet | f.Mirror) -> k.Shape:
    match feat:
        case f.Fillet():
            return shape.fillet(feat.radius, shape.Edges())
        case f.Shell():
            if feat.open_towards == "none":
                faces: list[cq.Face] = []
            else:
                sign = 1.0 if feat.open_towards[0] == "+" else -1.0
                d = _AXIS[f.Axis(feat.open_towards[1])] * sign
                faces = [fc for fc in shape.Faces() if fc.normalAt().dot(d) > 0.999]
                if not faces:
                    raise ValueError(f"no flat face points {feat.open_towards} to open")
            solids = shape.Solids()
            if len(solids) != 1:
                raise ValueError("shell needs a single solid")
            return solids[0].hollow(faces, -feat.thickness, kind="intersection")
        case f.Mirror():
            plane = {f.Plane.XY: "XY", f.Plane.XZ: "XZ", f.Plane.YZ: "YZ"}[feat.plane]
            return k.fuse(shape, shape.mirror(plane))
    raise ValueError(f"unknown feature type {feat.type}")


def _copies(tool: k.Shape, feat: f.LinearPattern | f.CircularPattern) -> list[k.Shape]:
    """Copies of the previous solid feature for a pattern (the original excluded)."""
    if isinstance(feat, f.LinearPattern):
        step = cq.Vector(*feat.step)
        return [tool.translate(step * i) for i in range(1, feat.count)]
    full = abs(feat.angle - 360.0) < 1e-9
    each = feat.angle / (feat.count if full else feat.count - 1)
    axis = _AXIS[feat.axis]
    return [tool.rotate(cq.Vector(0, 0, 0), axis, each * i) for i in range(1, feat.count)]


def _apply(result: k.Shape | None, op: f.Op, tools: list[k.Shape]) -> k.Shape:
    if result is None:
        if op is not f.Op.ADD:
            raise ValueError("the first solid must add material")
        first, *rest = tools
        return k.fuse(first, *rest) if rest else first
    if op is f.Op.ADD:
        return k.fuse(result, *tools)
    if op is f.Op.CUT:
        return k.cut(result, *tools)
    out = result
    for tool in tools:
        out = k.intersect(out, tool)
    return out


def _message(exc: Exception) -> str:
    text = str(exc).strip()
    return text or f"the geometry kernel could not build this feature ({type(exc).__name__})"


def build_part(doc: f.PartDoc) -> BuildResult:
    """The part's solid in its own frame (the part placement is applied by the caller)."""
    result: k.Shape | None = None
    last: tuple[k.Shape, f.Op] | None = None  # the previous solid feature, for patterns
    out = BuildResult(shape=None)
    for feat in doc.features:
        if feat.suppressed:
            continue
        try:
            if feat.type in f.SOLID_TYPES:
                tool = _place(_solid(feat), feat.at)  # type: ignore[arg-type]
                op = feat.op  # type: ignore[union-attr]
                result = _apply(result, op, [tool])
                last = (tool, op)
            elif feat.type in ("linear_pattern", "circular_pattern"):
                if last is None:
                    raise ValueError("a pattern repeats the solid feature before it; add one")
                tool, op = last
                result = _apply(result, op, _copies(tool, feat))  # type: ignore[arg-type]
            else:
                if result is None:
                    raise ValueError("add a solid before this modifier")
                result = _modify(result, feat)  # type: ignore[arg-type]
            if result is None or not k.is_valid(result) or k.solid_count(result) == 0:
                raise ValueError("the result is empty or invalid")
        except Exception as exc:  # the kernel raises many types; report, keep earlier work
            out.errors.append(FeatureError(feat.id, _message(exc)))
            break
        out.built.append(feat.id)
        out.shape = result
    return out
