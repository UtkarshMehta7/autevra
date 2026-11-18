"""CNC turning of a part revolved about its Z axis (a two-axis lathe, one setup).

The turned profile is the outer edge of the part's half-section in the XZ plane: r(z), the
largest radius of material at each height. Lathe frame: Z along the spindle with Z0 on the
finished front face (the part's top, z max) and the part towards -Z; X in diameter.

Operations, as a lathe programmer sets them:
1. Face the bar's front to Z0.
2. Rough the outside diameter in passes of depth ap (radial), each cutting towards the
   chuck until it meets the reachable profile plus the finishing allowance. A right-hand
   tool moving towards the chuck reaches the envelope env(z) = max r over [z, front]; the
   material under it (necks and grooves behind a shoulder) is left for the grooving tool.
3. Finish the reachable contour in one pass with tool-nose radius compensation (G42).
4. Groove each neck the turning tool cannot reach with a 3 mm grooving tool (plunges).
5. Part off behind the part.
Feeds per revolution (G99) and constant surface speed (G96) clamped by G50; times from the
spindle speed at each pass's diameter.
"""

import math
from dataclasses import dataclass, field

import cadquery as cq
from pydantic import BaseModel, Field
from shapely import LineString, Polygon
from shapely.ops import unary_union

from autevra.cad import kernel as k
from autevra.cam import tooling as tl
from autevra.part import features as f
from autevra.part.build import build_part

BARS = (
    10,
    12,
    16,
    20,
    25,
    30,
    32,
    36,
    40,
    45,
    50,
    55,
    60,
    65,
    70,
    80,
    90,
    100,
    110,
    120,
    130,
    140,
    150,
    160,
    180,
    200,
    220,
    250,
    280,
    300,
)
VC_TURN = {
    "aluminium 6061-T6": 400.0,
    "steel C45": 200.0,
    "stainless 304": 150.0,
    "cast iron GG25": 180.0,
    "POM (acetal)": 250.0,
}
AP_TURN = {
    "aluminium 6061-T6": 2.0,
    "steel C45": 1.5,
    "stainless 304": 1.0,
    "cast iron GG25": 1.5,
    "POM (acetal)": 2.5,
}
GROOVE_W = 3.0
RAPID = 8000.0


class TurnIn(BaseModel):
    material: tl.MaterialName = "steel C45"
    face_allowance: float = Field(1.0, ge=0.0, le=20.0)
    finish_allowance: float = Field(0.3, ge=0.0, le=3.0)  # radial, left by roughing
    rough_feed: float = Field(0.25, gt=0.01, le=1.0)  # mm/rev
    finish_feed: float = Field(0.1, gt=0.01, le=0.5)
    groove_feed: float = Field(0.05, gt=0.01, le=0.3)
    max_rpm: float = Field(3500.0, ge=200.0, le=12_000.0)
    part_off: bool = True


@dataclass
class TurnOp:
    name: str
    tool: str
    feed_rev: float
    moves: list[tuple[str, list[tuple[float, float]]]] = field(
        default_factory=list
    )  # (kind, [(X dia, Z)])
    css: bool = True
    comp: str = ""  # G41/G42 for the finishing contour

    def lengths(self) -> tuple[float, float]:
        cut = rapid = 0.0
        for kind, pts in self.moves:
            ln = sum(
                math.hypot((b[0] - a[0]) / 2, b[1] - a[1])
                for a, b in zip(pts, pts[1:], strict=False)
            )
            if kind == "rapid":
                rapid += ln
            else:
                cut += ln
        return cut, rapid

    def time_s(self, vc: float, max_rpm: float) -> float:
        t = 0.0
        for kind, pts in self.moves:
            for a, b in zip(pts, pts[1:], strict=False):
                ln = math.hypot((b[0] - a[0]) / 2, b[1] - a[1])
                if kind == "rapid":
                    t += ln / RAPID
                    continue
                dia = max((a[0] + b[0]) / 2, 2.0)
                n = min(1000.0 * vc / (math.pi * dia), max_rpm)
                t += ln / (self.feed_rev * n)
        return 60.0 * t + 6.0


def profile(shape: k.Shape, samples: int = 600) -> tuple[list[float], list[float], float]:
    """(z values, outer radius r(z)) of the half-section in XZ, and the smallest inner
    radius of material (a bore when above zero). The samples include every corner height of
    the section, so shoulders and groove walls fall on samples."""
    bb = shape.BoundingBox()
    size = 4.0 * max(bb.xlen, bb.zlen) + 10.0
    plane = cq.Face.makePlane(
        size, size, basePnt=cq.Vector(0, 0, bb.center.z), dir=cq.Vector(0, 1, 0)
    )
    polys = []
    for face in shape.intersect(plane).Faces():
        rings = [[(x, z) for x, z in _xz(face.outerWire())]] + [_xz(w) for w in face.innerWires()]
        if len(rings[0]) >= 3:
            polys.append(Polygon(rings[0], [r for r in rings[1:] if len(r) >= 3]).buffer(0))
    region = unary_union(polys).intersection(
        Polygon([(0, -1e6), (1e6, -1e6), (1e6, 1e6), (0, 1e6)])
    )
    if region.is_empty:
        raise ValueError("the part has no material on its axis plane")
    zs, rs, inner = [], [], math.inf
    corners = set()
    for g in getattr(region, "geoms", [region]):
        for ring in [g.exterior, *g.interiors]:
            for _, zc in ring.coords:
                corners.update((zc - 1e-4, zc + 1e-4))
    grid = {bb.zmin + (bb.zmax - bb.zmin) * i / samples for i in range(samples + 1)}
    for z in sorted(grid | corners):
        z = min(max(z, bb.zmin + 1e-4), bb.zmax - 1e-4)
        cut = LineString([(0.0, z), (1e6, z)]).intersection(region)
        if cut.is_empty:
            continue
        xs = [c[0] for g in getattr(cut, "geoms", [cut]) for c in g.coords]
        zs.append(z)
        rs.append(max(xs))
        inner = min(inner, min(xs))
    return zs, rs, inner


def _xz(wire: cq.Wire) -> list[tuple[float, float]]:
    from OCP.BRepAdaptor import BRepAdaptor_CompCurve
    from OCP.GCPnts import GCPnts_QuasiUniformDeflection

    s = GCPnts_QuasiUniformDeflection(BRepAdaptor_CompCurve(wire.wrapped), 0.02)
    return [(s.Value(i).X(), s.Value(i).Z()) for i in range(1, s.NbPoints() + 1)]


def plan(doc: f.PartDoc, cfg: TurnIn) -> dict:
    built = build_part(doc)
    if built.shape is None or built.errors:
        raise ValueError("the part does not build; fix it in Part Design first")
    shape = built.shape
    bb = shape.BoundingBox()
    if (
        abs(bb.center.x) > 0.01 * max(bb.xlen, 1)
        or abs(bb.center.y) > 0.01 * max(bb.ylen, 1)
        or abs(bb.xlen - bb.ylen) > 0.01 * max(bb.xlen, 1)
    ):
        raise ValueError("turning needs a part revolved about its own Z axis (a Shaft or Revolve)")
    zs, rs, inner = profile(shape)
    front, back = bb.zmax, bb.zmin
    length = front - back
    r_max = max(rs)
    bar = next((b for b in BARS if b >= 2.0 * r_max + 2.0), None)
    if bar is None:
        raise ValueError(f"part diameter {2 * r_max:.0f} mm is beyond the bar sizes (300 mm)")
    rb = bar / 2.0
    vc = VC_TURN[cfg.material]
    ap = AP_TURN[cfg.material]
    lz = lambda z: z - front  # noqa: E731  (lathe Z: front face at 0)
    # reachable envelope from the front (a right-hand tool cutting towards the chuck)
    env, best = [], 0.0
    for r in reversed(rs):
        best = max(best, r)
        env.append(best)
    env.reverse()
    ops: list[TurnOp] = []
    warnings, notes = [], []
    # 1 facing
    face = TurnOp("Face the front", "T01 CNMG 120408 (80° rhombic) right-hand", cfg.rough_feed)
    zf = cfg.face_allowance
    if zf > 0:
        face.moves += [
            ("rapid", [(bar + 4.0, 2.0), (bar + 2.0, 0.0)]),
            ("feed", [(bar + 2.0, 0.0), (-1.0, 0.0)]),
            ("rapid", [(-1.0, 0.0), (-1.0, 1.0), (bar + 4.0, 2.0)]),
        ]
        ops.append(face)
    # 2 roughing passes
    rough = TurnOp(
        f"Rough OD (ap {ap:g} mm, leave {cfg.finish_allowance:g} mm)", face.tool, cfg.rough_feed
    )
    r = rb - ap
    target = [e + cfg.finish_allowance for e in env]
    passes = 0
    while r > min(target) - 1e-9 and passes < 500:
        z_end = None
        for z, t in zip(reversed(zs), reversed(target), strict=True):  # from the front back
            if t >= r - 1e-9:
                z_end = z
                break
            z_end = z
        if z_end is not None and front - z_end > 0.05:
            x = 2.0 * r
            ze = lz(min(z_end + cfg.finish_allowance, front))  # axial stock on the shoulder
            rough.moves += [
                ("rapid", [(x + 2.0, 1.0), (x, 1.0)]),
                ("feed", [(x, 1.0), (x, ze), (x + 1.0, ze + 0.5)]),
                ("rapid", [(x + 1.0, ze + 0.5), (x + 1.0, 1.0)]),
            ]
            passes += 1
        r -= ap
    if rough.moves:
        ops.append(rough)
    # 3 finishing contour along the envelope (G42)
    fin = TurnOp(
        "Finish contour (G42 nose compensation)",
        "T02 VNMG 160404 (35° rhombic) right-hand",
        cfg.finish_feed,
    )
    contour = [(2.0 * e, lz(z)) for z, e in zip(reversed(zs), reversed(env), strict=True)]
    simplified = list(LineString([(x, z) for x, z in contour]).simplify(0.005).coords)
    start = (simplified[0][0], 1.0)
    fin.moves += [
        ("rapid", [(start[0] + 4.0, 2.0), start]),
        ("feed", [start, *simplified, (simplified[-1][0] + 2.0, simplified[-1][1])]),
        ("rapid", [(simplified[-1][0] + 2.0, simplified[-1][1]), (bar + 4.0, 2.0)]),
    ]
    fin.comp = "G42"
    ops.append(fin)
    # 4 grooves: where the profile dips under the envelope
    grooves = []
    in_groove = False
    for z, rr, e in zip(zs, rs, env, strict=True):
        if e - rr > 0.05:
            if not in_groove:
                grooves.append([z, z, rr, e])
                in_groove = True
            g = grooves[-1]
            g[1], g[2], g[3] = z, min(g[2], rr), max(g[3], e)
        else:
            in_groove = False
    if grooves:
        gop = TurnOp(
            f"Groove {len(grooves)} neck(s) ({GROOVE_W:g} mm grooving tool)",
            f"T03 grooving insert {GROOVE_W:g} mm",
            cfg.groove_feed,
        )
        for z0, z1, r_min, r_top in grooves:
            if z1 - z0 < GROOVE_W - 1e-6:
                warnings.append(
                    f"A groove {z1 - z0:.2f} mm wide at z {z0:.1f} is narrower than the "
                    f"{GROOVE_W:g} mm grooving tool: not programmed (it would cut the walls); "
                    f"use a {math.floor((z1 - z0) * 10) / 10:g} mm insert or wider."
                )
                continue
            # plunges from wall to wall: the first touches z0, the last z1, overlapping
            lo, hi = z0 + GROOVE_W / 2, max(z1 - GROOVE_W / 2, z0 + GROOVE_W / 2)
            count = max(1, math.ceil((hi - lo) / (0.8 * GROOVE_W)) + 1) if hi > lo + 1e-9 else 1
            for j in range(count):
                zc = lo + (hi - lo) * (j / (count - 1) if count > 1 else 0.0)
                gop.moves += [
                    ("rapid", [(2 * r_top + 2.0, lz(zc))]),
                    ("feed", [(2 * r_top + 2.0, lz(zc)), (2 * r_min, lz(zc))]),
                    ("rapid", [(2 * r_min, lz(zc)), (2 * r_top + 2.0, lz(zc))]),
                ]
        if gop.moves:
            ops.append(gop)
    # 5 part off
    if cfg.part_off:
        po = TurnOp("Part off", f"T03 grooving insert {GROOVE_W:g} mm", cfg.groove_feed)
        zp = lz(back) - GROOVE_W / 2
        r_back = rs[0] if zs else rb
        po.moves += [
            ("rapid", [(bar + 4.0, 2.0), (bar + 2.0, zp)]),
            ("feed", [(bar + 2.0, zp), (2 * r_back, zp), (0.0, zp)]),
            ("rapid", [(0.0, zp), (bar + 4.0, zp)]),
        ]
        ops.append(po)
    if inner > 0.1:
        warnings.append(
            f"The part has a bore (smallest radius {inner:.1f} mm): drill and bore it in a second "
            "operation; only the outside is programmed here."
        )
    notes.append(
        f"Bar ⌀{bar} mm, {length + cfg.face_allowance + GROOVE_W + 3:.0f} mm per part "
        f"(length + facing + parting + 3 mm grip margin)."
    )
    stock_len = length + cfg.face_allowance
    stock_vol = math.pi * rb * rb * stock_len
    vol = shape.Volume()
    return {
        "bar": bar,
        "length": length,
        "profile": list(zip(zs, rs, strict=True)),
        "envelope": env,
        "operations": ops,
        "warnings": warnings,
        "notes": notes,
        "vc": vc,
        "stock_volume": stock_vol,
        "removed_volume": stock_vol - vol,
        "volume": vol,
        "grooves": grooves,
        "front": front,
    }


def gcode(ops: list[TurnOp], cfg: TurnIn, title: str, vc: float) -> str:
    def n(v: float) -> str:
        s = f"{v:.3f}".rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s

    from autevra.cam.gcode import _ascii

    out = [
        "%",
        f"O2000 ({_ascii(title)[:40]})",
        "(LATHE: X DIAMETER, Z0 FINISHED FRONT FACE)",
        "G21 G18 G40 G99",
        f"G50 S{round(cfg.max_rpm)}",
    ]
    tool = None
    for op in ops:
        out.append(f"({_ascii(op.name)})")
        if op.tool != tool:
            num = op.tool.split()[0][1:]
            out += [f"({_ascii(op.tool)})", f"T{num}{num}"]
            tool = op.tool
        out += [f"G96 S{round(vc)} M3", "M8"]
        last = None
        for kind, pts in op.moves:
            for i, (x, z) in enumerate(pts):
                pos = f"X{n(x)} Z{n(z)}"
                if pos == last:
                    continue
                if kind == "rapid":
                    out.append(f"G0 {pos}")
                else:
                    word = f" F{n(op.feed_rev)}" if i <= 1 else ""
                    out.append(f"G1 {op.comp + ' ' if op.comp and i == 1 else ''}{pos}{word}")
                last = pos
        if op.comp:
            out.append("G40")
        out += ["M9", "G28 U0 W0"]
    out += ["M5", "M30", "%"]
    return "\n".join(out) + "\n"
