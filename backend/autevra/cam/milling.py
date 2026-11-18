"""2.5-axis machining of a part in one setup (tool along -Z), in the part's own frame.

Strategy, as a CAM programmer would set it up:

1. Stock: the part's bounding box plus margins (sides, top) and a bottom skin that holds
   the part until it is faced off in a second setup (reported).
2. Facing from the stock top to the part top (zig-zag, 70 % stepover).
3. Roughing by Z levels: levels every ap from the part top down, plus every horizontal
   floor of the part, so floors come out at their exact height. At each level the
   material to keep is the part's *shadow* from above (the union of its sections at that
   level and higher), so the tool never undercuts an overhang. The tool centre follows
   contour-parallel rings offset from the kept region by r + radial stock, then by the
   stepover (0.4 D <= r, so the bands overlap and leave no cusps), ordered from the
   outside in (pockets from the centre out), climb milling (spindle M3: around the part
   clockwise, inside pockets counter-clockwise). Closed rings inside the material are
   entered by a ramp (3 deg) from the level above; open ones start in the air outside
   the stock.
4. Finishing: one ring at exactly r from the walls at every level, no radial stock.
5. Rest material: what the tool cannot reach at a level (pockets or corners narrower
   than the tool) is measured and reported, with its location, for a smaller tool.
6. Holes from the part's Hole features (axis along -Z): spot drill, drill (G81, or G83
   peck deeper than 3 d), rigid tap (G84) for tapped holes, helical counterbore milling
   and a 90 deg countersink with the spot drill. Holes are left out of the milled shape
   so the end mill does not chase them.
"""

import math
from dataclasses import dataclass, field

import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_CompCurve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from pydantic import BaseModel, Field
from shapely import LineString, MultiLineString, Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import substring, unary_union

from autevra.cad import kernel as k
from autevra.cam import tooling as tl
from autevra.part import features as f
from autevra.part.build import build_part, hole_geometry

EPS = 0.01  # mm above a level when slicing, so a floor is not sliced on its own face
RAMP_DEG = 3.0
RAPID = 10_000.0  # mm/min
TOOL_CHANGE_S = 8.0


class CamIn(BaseModel):
    material: tl.MaterialName = "aluminium 6061-T6"
    side_margin: float = Field(3.0, ge=0.0, le=200.0)
    top_margin: float = Field(1.0, ge=0.0, le=100.0)
    bottom_skin: float = Field(3.0, ge=0.0, le=100.0)
    rough_tool: float | None = Field(None, gt=0.5, le=50.0)  # end mill diameter; auto if None
    finish_tool: float | None = Field(None, gt=0.5, le=50.0)
    corner_radius: float = Field(5.0, gt=0.5, le=50.0)  # largest inside-corner radius allowed
    radial_stock: float = Field(0.3, ge=0.0, le=5.0)
    stepdown: float | None = Field(None, gt=0.05, le=50.0)  # overrides k_ap * D
    max_rpm: float = Field(12_000.0, ge=500.0, le=60_000.0)
    machine_kw: float = Field(7.5, gt=0.1, le=200.0)
    clearance: float = Field(5.0, gt=0.5, le=100.0)  # safe plane above the stock top
    tolerance: float = Field(0.02, ge=0.001, le=0.5)  # chordal, slicing and offsets


@dataclass
class Move:
    kind: str  # rapid | feed | plunge
    pts: list[tuple[float, float, float]]
    feed: float = 0.0


@dataclass
class Operation:
    name: str
    tool: tl.Tool
    speeds: tl.Speeds
    moves: list[Move] = field(default_factory=list)
    cycle: dict | None = None  # canned drilling cycle for the post-processor
    notes: list[str] = field(default_factory=list)
    power_kw: float = 0.0

    def lengths(self) -> tuple[float, float]:
        cut = rapid = 0.0
        for m in self.moves:
            length = sum(math.dist(a, b) for a, b in zip(m.pts, m.pts[1:], strict=False))
            if m.kind == "rapid":
                rapid += length
            else:
                cut += length
        return cut, rapid

    def time_s(self) -> float:
        cut_time = 0.0
        rapid = 0.0
        for m in self.moves:
            length = sum(math.dist(a, b) for a, b in zip(m.pts, m.pts[1:], strict=False))
            if m.kind == "rapid":
                rapid += length
            else:
                cut_time += length / max(m.feed, 1e-6)
        return 60.0 * (cut_time + rapid / RAPID) + TOOL_CHANGE_S


# ---------- geometry ----------


def _ring(wire: cq.Wire, tol: float) -> list[tuple[float, float]]:
    curve = BRepAdaptor_CompCurve(wire.wrapped)
    disc = GCPnts_QuasiUniformDeflection(curve, tol)
    return [(disc.Value(i).X(), disc.Value(i).Y()) for i in range(1, disc.NbPoints() + 1)]


def section(shape: k.Shape, z: float, tol: float) -> Polygon:
    """The part's cross-section at height z as planar regions (with holes)."""
    bb = shape.BoundingBox()
    size = 4.0 * max(bb.xlen, bb.ylen) + 10.0
    plane = cq.Face.makePlane(
        size, size, basePnt=cq.Vector(bb.center.x, bb.center.y, z), dir=cq.Vector(0, 0, 1)
    )
    polys = []
    for face in shape.intersect(plane).Faces():
        outer = _ring(face.outerWire(), tol)
        if len(outer) < 3:
            continue
        holes = [r for r in (_ring(w, tol) for w in face.innerWires()) if len(r) >= 3]
        polys.append(Polygon(outer, holes).buffer(0))
    return unary_union(polys) if polys else Polygon()


def horizontal_faces(shape: k.Shape) -> tuple[list[float], list[float]]:
    """Heights of the planar faces facing up (floors) and down (ceilings, overhangs)."""
    ups, downs = [], []
    for fc in shape.Faces():
        if fc.geomType() != "PLANE":
            continue
        n = fc.normalAt()
        if n.z > 1 - 1e-6:
            ups.append(fc.Center().z)
        elif n.z < -1 + 1e-6:
            downs.append(fc.Center().z)
    return ups, downs


def _dedupe(values: list[float], gap: float = 0.05) -> list[float]:
    out: list[float] = []
    for v in sorted(values, reverse=True):
        if not out or out[-1] - v > gap:
            out.append(v)
    return out


def _pieces(geom) -> list[list[tuple[float, float]]]:  # noqa: ANN001
    if geom.is_empty:
        return []
    if isinstance(geom, LineString):
        return [list(geom.coords)]
    if isinstance(geom, MultiLineString):
        return [list(g.coords) for g in geom.geoms]
    if hasattr(geom, "geoms"):
        return [p for g in geom.geoms for p in _pieces(g)]
    return []


def _boundary_climb(region) -> list[LineString]:  # noqa: ANN001
    """Boundary rings of an offset region oriented for climb milling with M3: exteriors
    clockwise, interiors counter-clockwise."""
    polys = [region] if isinstance(region, Polygon) else list(getattr(region, "geoms", []))
    rings = []
    for p in polys:
        if p.is_empty:
            continue
        p = orient(p, sign=-1.0)
        rings.append(LineString(p.exterior.coords))
        rings.extend(LineString(i.coords) for i in p.interiors)
    return rings


# ---------- toolpaths ----------


@dataclass
class Setup:
    stock: tuple[float, float, float, float, float, float]  # x0 y0 z0 x1 y1 z1
    part_box: tuple[float, float, float, float, float, float]
    safe_z: float


def _level_paths(
    keep, r: float, leave: float, step: float, touch: Polygon, stock: Polygon, finish: bool
) -> tuple[list[list[tuple[float, float]]], float, Polygon]:
    """Tool-centre paths at one level (outside in), the rest-material area and its shape."""
    paths: list[tuple[float, list[tuple[float, float]]]] = []
    if finish:
        dists = [r]
    else:
        dists, d = [], r + leave
        while d < 1e5:
            dists.append(d)
            region = keep.buffer(d, quad_segs=12)
            if region.contains(touch):
                break
            d += step
    cut = []
    for d in dists:
        region = keep.buffer(d, quad_segs=12)
        for ring in _boundary_climb(region):
            for piece in _pieces(ring.intersection(touch)):
                if len(piece) >= 2:
                    paths.append((d, piece))
                    cut.append(LineString(piece).buffer(r, quad_segs=8))
    paths.sort(key=lambda t: -t[0])
    target = stock.difference(keep.buffer(leave + 0.01))
    reached = unary_union(cut) if cut else Polygon()
    rest = target.difference(reached) if not finish else Polygon()
    rest = rest.buffer(-0.05).buffer(0.05) if not rest.is_empty else rest  # ignore slivers
    return [p for _, p in paths], rest.area, rest


def _ramp_moves(
    ring: list[tuple[float, float]], z_from: float, z_to: float, feed: float, plunge: float
) -> list[Move]:
    line = LineString(ring)
    per = line.length
    drop = z_from - z_to
    ramp_len = drop / math.tan(math.radians(RAMP_DEG))
    pts: list[tuple[float, float, float]] = []
    s = 0.0
    n = max(int(ramp_len / max(per / max(len(ring), 1), 0.5)), 8)
    for i in range(n + 1):
        s = ramp_len * i / n
        p = line.interpolate(s % per if per > 0 else 0.0)
        pts.append((p.x, p.y, z_from - drop * i / n))
    end = ramp_len % per if per > 0 else 0.0
    loop = list(substring(line, end, per).coords) + list(substring(line, 0.0, end).coords)[1:]
    return [Move("plunge", pts, plunge), Move("feed", [(x, y, z_to) for x, y in loop], feed)]


def _mill_level(
    op: Operation,
    paths: list[list[tuple[float, float]]],
    z: float,
    z_above: float,
    setup: Setup,
    stock: Polygon,
) -> None:
    sp = op.speeds
    inner = stock.buffer(-0.01)
    for piece in paths:
        closed = math.dist(piece[0], piece[-1]) < 1e-6
        x0, y0 = piece[0]
        op.moves.append(Move("rapid", [(x0, y0, setup.safe_z), (x0, y0, z_above + 1.0)]))
        starts_in_material = inner.contains(LineString(piece[:2]).interpolate(0.0))
        if closed and starts_in_material and z_above - z > 1e-6:
            op.moves.extend(_ramp_moves(piece, z_above, z, sp.feed, sp.plunge))
        else:
            op.moves.append(Move("plunge", [(x0, y0, z_above + 1.0), (x0, y0, z)], sp.plunge))
            op.moves.append(Move("feed", [(x, y, z) for x, y in piece], sp.feed))
        last = op.moves[-1].pts[-1]
        op.moves.append(Move("rapid", [last, (last[0], last[1], setup.safe_z)]))


def _end_mill(number: int, d: float, mat: tl.CuttingData) -> tl.Tool:
    return tl.Tool(number, "end mill", d, mat.flutes)


def plan(doc: f.PartDoc, cam: CamIn) -> dict:
    """Machining plan for a part document: setup, operations and warnings."""
    mat = tl.MATERIALS[cam.material]
    holes = [h for h in doc.features if isinstance(h, f.Hole) and not h.suppressed]
    milled_doc = doc.model_copy(
        update={
            "features": [
                ft.model_copy(update={"suppressed": True}) if isinstance(ft, f.Hole) else ft
                for ft in doc.features
            ]
        }
    )
    full = build_part(doc)
    milled = build_part(milled_doc)
    if full.shape is None or milled.shape is None or full.errors:
        raise ValueError("the part does not build; fix it in Part Design first")
    shape = milled.shape
    bb = full.shape.BoundingBox()
    x0, y0, x1, y1 = (
        bb.xmin - cam.side_margin,
        bb.ymin - cam.side_margin,
        bb.xmax + cam.side_margin,
        bb.ymax + cam.side_margin,
    )
    z_top, z_bot = bb.zmax + cam.top_margin, bb.zmin - cam.bottom_skin
    setup = Setup(
        (x0, y0, z_bot, x1, y1, z_top),
        (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax),
        z_top + cam.clearance,
    )
    stock = box(x0, y0, x1, y1)
    warnings: list[str] = []
    notes: list[str] = []

    # tools: roughing as large as the part allows, finishing = roughing unless chosen
    span = min(bb.xlen, bb.ylen)
    d_rough = cam.rough_tool or max(
        [d for d in tl.END_MILLS if d <= max(span / 3.0, 3.0)], default=3.0
    )
    d_finish = cam.finish_tool or d_rough
    tools: list[tl.Tool] = []

    def tool_for(kind: str, d: float, pitch: float = 0.0, angle: float = 0.0) -> tl.Tool:
        for t in tools:
            if t.kind == kind and abs(t.diameter - d) < 1e-9 and abs(t.pitch - pitch) < 1e-9:
                return t
        flutes = mat.flutes if kind == "end mill" else 2
        t = tl.Tool(len(tools) + 1, kind, d, flutes, pitch, angle)  # type: ignore[arg-type]
        tools.append(t)
        return t

    ops: list[Operation] = []
    rough = tool_for("end mill", d_rough)
    sp_r = tl.mill_speeds(rough, mat, cam.max_rpm)
    ap = cam.stepdown or sp_r.ap

    # 1 facing
    if cam.top_margin > 1e-6:
        face = Operation("Face the stock top", rough, sp_r)
        levels = []
        z = z_top
        while z - ap > bb.zmax + 1e-6:
            z -= ap
            levels.append(z)
        levels.append(bb.zmax)
        step = 0.7 * rough.diameter
        r = rough.diameter / 2.0
        for z in levels:
            ys, y = [], y0 + 0.3 * r
            while y < y1 + 0.3 * r:
                ys.append(y)
                y += step
            pts = []
            for i, yy in enumerate(ys):
                xa, xb = (
                    (x0 - r - 1.0, x1 + r + 1.0) if i % 2 == 0 else (x1 + r + 1.0, x0 - r - 1.0)
                )
                pts += [(xa, yy, z), (xb, yy, z)]
            face.moves += [
                Move(
                    "rapid", [(pts[0][0], pts[0][1], setup.safe_z), (pts[0][0], pts[0][1], z + 1.0)]
                ),
                Move("plunge", [(pts[0][0], pts[0][1], z + 1.0), pts[0]], sp_r.plunge),
                Move("feed", pts, sp_r.feed),
                Move("rapid", [pts[-1], (pts[-1][0], pts[-1][1], setup.safe_z)]),
            ]
        face.power_kw = tl.power_kw(min(cam.top_margin, ap), step, sp_r.feed, mat.kc)
        ops.append(face)

    # 2-3 roughing and finishing by Z levels
    ups, downs = horizontal_faces(shape)
    floors = [z for z in ups if bb.zmin + 1e-6 < z < bb.zmax - 1e-6]
    levels, z = [], bb.zmax
    while z - ap > bb.zmin + 1e-6:
        z -= ap
        levels.append(z)
    levels = _dedupe([*levels, *floors, bb.zmin])
    samples = sorted(
        {
            *(lv + EPS for lv in levels),
            *(c - EPS for c in downs if c > bb.zmin + EPS),
            *(c + EPS for c in ups if c < bb.zmax - EPS),
            bb.zmax - EPS,
        }
    )
    slices = {s: section(shape, s, cam.tolerance) for s in samples}

    def shadow(level: float):  # noqa: ANN202
        return unary_union([g for s, g in slices.items() if s >= level and not g.is_empty])

    r_r = rough.diameter / 2.0
    touch_r = stock.buffer(r_r + 0.5, join_style="mitre")
    rough_op = Operation(
        f"Rough by Z levels (ap {ap:.2f} mm, stock {cam.radial_stock:g} mm)", rough, sp_r
    )
    z_above = bb.zmax if cam.top_margin > 1e-6 else z_top
    per_level = []  # (level, keep, rest region after roughing)
    for lv in levels:
        keep = shadow(lv)
        if keep.is_empty:
            continue
        paths, rest_area, rest = _level_paths(
            keep, r_r, cam.radial_stock, 0.4 * rough.diameter, touch_r, stock, finish=False
        )
        _mill_level(rough_op, paths, lv, z_above, setup, stock)
        per_level.append((lv, z_above, keep, rest if rest_area > 1.0 else Polygon()))
        z_above = lv
    rough_op.power_kw = tl.power_kw(ap, 0.4 * rough.diameter, sp_r.feed, mat.kc)
    ops.append(rough_op)

    def unreached(d: float) -> list[tuple[float, float, Polygon]]:
        """(level, area, region) a d end mill cannot reach, with no radial stock."""
        out = []
        touch = stock.buffer(d / 2.0 + 0.5, join_style="mitre")
        for lv, _, keep, _ in per_level:
            _, _, region = _level_paths(keep, d / 2.0, 0.0, 0.4 * d, touch, stock, finish=False)
            # the cusp a round tool leaves in a sharp inside corner has an inscribed radius of
            # 0.17 r: erode it away, so only real unreached material (slots, pockets) counts
            real = region.buffer(-0.09 * d).buffer(0.09 * d) if not region.is_empty else region
            if real.area > 1.0:
                out.append((lv, real.area, real))
        return out

    rest_after_rough = [(lv, r) for lv, _, _, r in per_level if not r.is_empty]
    if cam.finish_tool is None:
        limit = min(d_rough, 2.0 * cam.corner_radius)
        cands = sorted((x for x in tl.END_MILLS if x <= limit), reverse=True) or [tl.END_MILLS[0]]
        for cand in cands:
            d_finish = cand
            if not unreached(cand):
                break
    if any(not r.is_empty for _, r in rest_after_rough) or d_finish < d_rough:
        notes.append(
            f"Inside corners come out with R{d_finish / 2:g} (the ⌀{d_finish:g} finishing tool); "
            "sharper corners need a smaller tool or EDM."
        )
    finish_tool = tool_for("end mill", d_finish)
    r_f = finish_tool.diameter / 2.0
    sp_f0 = tl.mill_speeds(finish_tool, mat, cam.max_rpm)
    touch_f = stock.buffer(r_f + 0.5, join_style="mitre")
    if rest_after_rough and d_finish < d_rough:
        rest_op = Operation(
            f"Rest machining (corners and pockets the ⌀{d_rough:g} left)", finish_tool, sp_f0
        )
        for lv, z_prev, keep, rest in per_level:
            if rest.is_empty:
                continue
            paths, _, _ = _level_paths(
                keep,
                r_f,
                cam.radial_stock,
                0.4 * finish_tool.diameter,
                touch_f,
                stock,
                finish=False,
            )
            zone = rest.buffer(r_f + 0.5)
            clipped = [
                pc
                for path in paths
                for pc in _pieces(LineString(path).intersection(zone))
                if len(pc) >= 2
            ]
            _mill_level(rest_op, clipped, lv, z_prev, setup, stock)
        rest_op.power_kw = tl.power_kw(sp_f0.ap, sp_f0.ae, sp_f0.feed, mat.kc)
        if rest_op.moves:
            ops.append(rest_op)
    sp_f = tl.Speeds(
        sp_f0.rpm,
        0.8 * sp_f0.feed,
        sp_f0.plunge,
        sp_f0.ap,
        0.1 * finish_tool.diameter,
        sp_f0.capped,
    )
    finish_op = Operation("Finish walls (contour at every level)", finish_tool, sp_f)
    for lv, _, keep, _ in per_level:
        fpaths, _, _ = _level_paths(keep, r_f, 0.0, 0.0, touch_f, stock, finish=True)
        _mill_level(finish_op, fpaths, lv, lv, setup, stock)
    finish_op.power_kw = tl.power_kw(min(ap, sp_f0.ap), sp_f.ae, sp_f.feed, mat.kc)
    ops.append(finish_op)
    left = unreached(finish_tool.diameter) if rest_after_rough else []
    rest_total = sum(a for _, a, _ in left)
    if left:

        def describe(lv: float, a: float, g) -> str:  # noqa: ANN001
            parts = list(getattr(g, "geoms", [g]))
            big = max(parts, key=lambda q: q.area)
            more = f" in {len(parts)} places" if len(parts) > 1 else ""
            c = big.centroid
            return f"z {lv:.1f}: {a:.0f} mm²{more} (largest near {c.x:.0f}, {c.y:.0f})"

        where = "; ".join(describe(lv, a, g) for lv, a, g in left[:3])
        warnings.append(
            "Material no end mill in the library reaches (inside corners sharper than ⌀3, "
            f"or narrow slots): {where}. Add corner radii, or plan EDM."
        )

    # 6 holes
    vertical = [h for h in holes if abs(h.at.rx) < 1e-9 and abs(h.at.ry) < 1e-9]
    if len(vertical) < len(holes):
        warnings.append(
            f"{len(holes) - len(vertical)} hole(s) are not along -Z and need another setup."
        )
    from shapely import Point

    def entry(h: f.Hole) -> tuple[float, float]:
        """Entry height (local top of the material at the hole) and the extra depth."""
        pt = Point(h.at.x, h.at.y)
        tops = [z for z, g in slices.items() if not g.is_empty and g.contains(pt)]
        if not tops:
            return h.at.z, 0.0
        s_max = max(tops)
        top = min([w for w in [*ups, bb.zmax] if w > s_max - EPS + 1e-6], default=bb.zmax)
        if h.at.z < top - 0.05:
            warnings.append(
                f"Hole {h.name or h.id} starts {top - h.at.z:.1f} mm below the material top at "
                f"({h.at.x:g}, {h.at.y:g}); it is drilled from the top (z {top:.1f})."
            )
            return top, top - h.at.z
        return h.at.z, 0.0

    if vertical:
        spot = tool_for("spot drill", 10.0, angle=90.0)
        sp_s = tl.drill_speeds(spot, mat, cam.max_rpm)
        entries = {h.id: entry(h) for h in vertical}
        pts = [(h.at.x, h.at.y, entries[h.id][0]) for h in vertical]
        spot_depth = max(0.5 * hole_geometry(h)["drill"] + 0.2 for h in vertical)  # type: ignore[arg-type]
        spot_op = Operation("Spot drill (90°)", spot, sp_s)
        spot_op.cycle = {"code": "G81", "points": pts, "depth": spot_depth, "r": 2.0}
        spot_op.moves = _cycle_moves(pts, spot_depth, 2.0, setup.safe_z, sp_s.feed)
        ops.append(spot_op)
        for h in vertical:
            g = hole_geometry(h)
            d = float(g["drill"])
            z_in, extra = entries[h.id]
            through_depth = z_in - bb.zmin + 0.3 * d + 1.0
            depth = (
                through_depth if h.through else h.depth + extra + 0.3 * d * (h.bottom == "drill")
            )
            drill = tool_for("drill", d, angle=118.0)
            sp_d = tl.drill_speeds(drill, mat, cam.max_rpm)
            code = "G83" if depth > 3.0 * d else "G81"
            op = Operation(
                f"Drill ⌀{d:g} {'peck ' if code == 'G83' else ''}({h.name or h.id})", drill, sp_d
            )
            op.cycle = {
                "code": code,
                "points": [(h.at.x, h.at.y, z_in)],
                "depth": depth,
                "r": 2.0,
                "peck": d if code == "G83" else 0.0,
            }
            op.moves = _cycle_moves([(h.at.x, h.at.y, z_in)], depth, 2.0, setup.safe_z, sp_d.feed)
            vc = math.pi * d * sp_d.rpm / 1000.0
            op.power_kw = (sp_d.feed / sp_d.rpm) * vc * d * mat.kc / 240_000.0  # Sandvik drilling
            ops.append(op)
            if h.through and h.at.z - bb.zmin > 1e-6:
                op.notes.append("Breaks through into the bottom skin (1 mm + tip).")
            if h.kind == "tapped":
                tap = tool_for("tap", float(h.size[1:]), pitch=float(g["pitch"]))
                sp_t = tl.drill_speeds(tap, mat, cam.max_rpm)
                pitch = float(g["pitch"])
                hole_len = h.at.z - bb.zmin if h.through else h.depth
                tdepth = extra + (
                    h.thread_depth or (hole_len if h.through else max(hole_len - 2 * pitch, pitch))
                )
                top = Operation(f"Rigid tap {g['thread']} ({h.name or h.id})", tap, sp_t)
                top.cycle = {
                    "code": "G84",
                    "points": [(h.at.x, h.at.y, z_in)],
                    "depth": tdepth,
                    "r": 3.0,
                }
                top.moves = _cycle_moves(
                    [(h.at.x, h.at.y, z_in)], tdepth, 3.0, setup.safe_z, sp_t.feed
                )
                ops.append(top)
            if "cbore_diameter" in g:
                cd, ct = float(g["cbore_diameter"]), float(g["cbore_depth"])
                em = tool_for(
                    "end mill", max([x for x in tl.END_MILLS if x <= 0.7 * cd], default=3.0)
                )
                sp_e = tl.mill_speeds(em, mat, cam.max_rpm)
                cb = Operation(f"Counterbore ⌀{cd:g}×{ct:g} helical ({h.name or h.id})", em, sp_e)
                cb.moves = _helix(
                    h.at.x,
                    h.at.y,
                    z_in,
                    (cd - em.diameter) / 2.0,
                    ct,
                    0.5 * em.diameter,
                    setup.safe_z,
                    sp_e.feed,
                )
                ops.append(cb)
            if "csink_diameter" in g:
                sd = float(g["csink_diameter"])
                if sd > spot.diameter:
                    warnings.append(
                        f"Countersink ⌀{sd:g} is larger than the ⌀{spot.diameter:g} spot drill."
                    )
                cs = Operation(f"Countersink ⌀{sd:g}×90° ({h.name or h.id})", spot, sp_s)
                cs.cycle = {
                    "code": "G82",
                    "points": [(h.at.x, h.at.y, z_in)],
                    "depth": sd / 2.0,
                    "r": 2.0,
                    "dwell": 0.3,
                }
                cs.moves = _cycle_moves(
                    [(h.at.x, h.at.y, z_in)], sd / 2.0, 2.0, setup.safe_z, sp_s.feed
                )
                ops.append(cs)

    # process order (a hole is spotted, drilled, then counterbored or countersunk, then
    # tapped); within each phase operations sharing a tool run together
    def phase(op: Operation) -> int:
        if op.tool.kind == "spot drill" and op.cycle and op.cycle["code"] == "G81":
            return 1
        if op.tool.kind == "drill":
            return 2
        if op.name.startswith(("Counterbore", "Countersink")):
            return 3
        return 4 if op.tool.kind == "tap" else 0

    first: dict[tuple[int, int], int] = {}
    for i, op in enumerate(ops):
        first.setdefault((phase(op), op.tool.number), i)
    ops.sort(key=lambda o: (phase(o), first[(phase(o), o.tool.number)]))
    for op in ops:
        if op.speeds.capped:
            warnings.append(
                f"{op.tool.label}: spindle limited to {cam.max_rpm:g} rpm (feeds scaled with it)."
            )
        if op.power_kw > cam.machine_kw:
            warnings.append(
                f"{op.name}: about {op.power_kw:.1f} kW, above the {cam.machine_kw:g} kW spindle."
            )
    if cam.bottom_skin > 0:
        notes.append(f"Setup 2: flip the part and face off the {cam.bottom_skin:g} mm bottom skin.")
    stock_vol = (x1 - x0) * (y1 - y0) * (z_top - z_bot)
    removed = stock_vol - full.shape.Volume()
    total_time = sum(op.time_s() for op in ops)
    return {
        "setup": setup,
        "tools": tools,
        "operations": ops,
        "warnings": list(dict.fromkeys(warnings)),
        "notes": notes,
        "stock_volume": stock_vol,
        "removed_volume": removed,
        "rest_area": rest_total,
        "time_s": total_time,
        "material": cam.material,
        "levels": levels,
        "mass_kg": full.shape.Volume() * 1e-9 * mat.density,
        "stock_mass_kg": stock_vol * 1e-9 * mat.density,
    }


def _cycle_moves(
    pts: list[tuple[float, float, float]], depth: float, r: float, safe: float, feed: float
) -> list[Move]:
    moves: list[Move] = []
    for x, y, z in pts:
        moves += [
            Move("rapid", [(x, y, safe), (x, y, z + r)]),
            Move("feed", [(x, y, z + r), (x, y, z - depth)], feed),
            Move("rapid", [(x, y, z - depth), (x, y, safe)]),
        ]
    return moves


def _helix(
    cx: float,
    cy: float,
    ztop: float,
    radius: float,
    depth: float,
    pitch: float,
    safe: float,
    feed: float,
) -> list[Move]:
    if radius <= 0:
        return []
    turns = max(depth / pitch, 1.0)
    n = int(48 * turns)
    pts = [
        (
            cx + radius * math.cos(2 * math.pi * i / 48),
            cy + radius * math.sin(2 * math.pi * i / 48),
            ztop + 0.5 - (depth + 0.5) * i / n,
        )
        for i in range(n + 1)
    ]
    pts += [
        (
            cx + radius * math.cos(2 * math.pi * i / 48),
            cy + radius * math.sin(2 * math.pi * i / 48),
            ztop - depth,
        )
        for i in range(49)
    ]
    return [
        Move("rapid", [(pts[0][0], pts[0][1], safe), pts[0]]),
        Move("plunge", pts, 0.5 * feed),
        Move("rapid", [pts[-1], (pts[-1][0], pts[-1][1], safe)]),
    ]
