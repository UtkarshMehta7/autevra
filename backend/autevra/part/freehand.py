"""Rough sketch to 3D: freehand strokes cleaned into a constrained sketch, then a solid.

Cleaning, view by view (strokes in mm, y up):
1. Each stroke's own jitter is measured (against a lightly smoothed copy) and sets how
   loosely it is read (at least 3 x the jitter); it is then split at its corners
   (Ramer-Douglas-Peucker on the raw points); every
   piece is a straight line when the points stay within ``tolerance`` of its chord, else a
   circular arc from an algebraic least-squares circle fit (Kasa) that is visibly curved,
   else it is split further. Neighbouring pieces are merged again when one chord still fits
   them (a shaky straight edge) or one circle does with the tangent continuous at the joint.
   A closed stroke whose points keep a near-constant distance from their centroid is a
   circle.
2. End points closer than ``snap`` merge into one sketch point; a chain whose two free
   ends are within 3 snap is closed with a line.
3. Intent is inferred where the drawing is close to it: lines within 6 degrees of
   horizontal or vertical, pairs of lines within 5 degrees of parallel or perpendicular,
   lengths within 6 % of each other, arcs meeting a line within 10 degrees of tangency,
   circles with centres within snap of each other (concentric) or radii within 6 %.
4. The constraint solver moves the drawing the least to meet them (the first point is
   fixed); a constraint the solver cannot meet with the others is dropped and reported.

3D: ``extrude`` pads the profile; ``revolve`` turns it about the vertical axis through its
left-most point; ``views`` intersects the front (XZ), top (XY) and side (YZ) profiles, each
padded right through the others (a visual hull, as a draughtsman reads three views); the
views are scaled so their shared extents agree. The result is an ordinary Part Design part,
so every sketch stays editable in the constraint sketcher.
"""

import math
from typing import Literal

import numpy as np
from pydantic import BaseModel, Field

from autevra.part import sketch as sk

Stroke = list[tuple[float, float]]
VIEW_PLANE = {"top": "xy", "front": "xz", "side": "yz"}


class FreehandIn(BaseModel):
    views: dict[Literal["front", "top", "side"], list[Stroke]] = Field(min_length=1)
    mode: Literal["extrude", "revolve", "views"] = "extrude"
    depth: float = Field(40.0, gt=0.1, le=10_000.0)
    tolerance: float | None = Field(None, gt=0.0)  # mm; default 1.5 % of the drawing
    snap: float | None = Field(None, gt=0.0)  # mm; default 4 % of the drawing
    name: str = Field("Sketched part", max_length=80)


# ---------- fitting ----------


def _cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """z of the 2D cross product (broadcasts over rows)."""
    return a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]


def _rdp(pts: np.ndarray, eps: float) -> list[int]:
    if len(pts) < 3:
        return list(range(len(pts)))
    a, b = pts[0], pts[-1]
    ab = b - a
    n = np.linalg.norm(ab)
    d = (np.abs(_cross(ab, pts - a)) / n) if n > 1e-12 else np.linalg.norm(pts - a, axis=1)
    i = int(np.argmax(d))
    if d[i] <= eps:
        return [0, len(pts) - 1]
    left = _rdp(pts[: i + 1], eps)
    right = _rdp(pts[i:], eps)
    return left[:-1] + [j + i for j in right]


def fit_circle(pts: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Kasa fit: centre, radius and the largest radial residual (every point must lie on
    the arc, so a straight run with a bend at its end is not taken for a flat arc)."""
    x, y = pts[:, 0], pts[:, 1]
    a = np.column_stack([x, y, np.ones_like(x)])
    b = -(x * x + y * y)
    (d, e, f), *_ = np.linalg.lstsq(a, b, rcond=None)
    c = np.array([-d / 2, -e / 2])
    r = math.sqrt(max(c @ c - f, 1e-12))
    res = float(np.max(np.abs(np.linalg.norm(pts - c, axis=1) - r)))  # worst point
    return c, r, res


def _chord_dev(pts: np.ndarray) -> float:
    a, b = pts[0], pts[-1]
    ab = b - a
    n = np.linalg.norm(ab)
    if n < 1e-12:
        return float(np.max(np.linalg.norm(pts - a, axis=1)))
    return float(np.max(np.abs(_cross(ab, pts - a)) / n))


def _segments(stroke: np.ndarray, tol: float) -> list[dict]:
    """Lines and arcs along an open stroke."""
    out: list[dict] = []
    corners = _rdp(stroke, tol)
    # merge runs of short RDP pieces that together trace one arc
    i = 0
    while i < len(corners) - 1:
        j = len(corners) - 1
        while j > i:
            piece = stroke[corners[i] : corners[j] + 1]
            if j == i + 1 and _chord_dev(piece) <= 1.5 * tol:
                out.append(
                    {
                        "kind": "line",
                        "a": piece[0],
                        "b": piece[-1],
                        "span": (corners[i], corners[j]),
                    }
                )
                break
            if len(piece) >= 5 and _smooth(stroke, corners[i : j + 1]):
                c, r, res = fit_circle(piece)
                sweep = _sweep(piece, c)
                if (
                    res <= 1.5 * tol
                    and r < 50 * np.linalg.norm(piece[-1] - piece[0]) + 1e-9
                    and abs(sweep) > 0.25
                    and _chord_dev(piece) >= 1.5 * tol
                ):
                    out.append(
                        {
                            "kind": "arc",
                            "a": piece[0],
                            "b": piece[-1],
                            "c": c,
                            "r": r,
                            "ccw": sweep > 0,
                            "span": (corners[i], corners[j]),
                        }
                    )
                    break
            j -= 1
        if j == i:  # nothing fitted: keep the RDP chord
            out.append(
                {
                    "kind": "line",
                    "a": stroke[corners[i]],
                    "b": stroke[corners[i + 1]],
                    "span": (corners[i], corners[i + 1]),
                }
            )
            j = i + 1
        i = j
    return _merge_arcs(stroke, out, tol)


def _tangent_continuous(stroke: np.ndarray, joint: int, limit_deg: float, k: int = 3) -> bool:
    """The stroke turns gently through ``joint``: the local directions just before and
    just after it (over k points) differ by less than ``limit_deg``."""
    lo, hi = max(joint - k, 0), min(joint + k, len(stroke) - 1)
    if joint - lo < 1 or hi - joint < 1:
        return True
    u, w = stroke[joint] - stroke[lo], stroke[hi] - stroke[joint]
    return abs(math.atan2(float(_cross(u, w)), float(u @ w))) <= math.radians(limit_deg)


def _merge_arcs(stroke: np.ndarray, segs: list[dict], tol: float) -> list[dict]:
    """Neighbouring pieces whose raw points fit one circle, meeting without a sharp turn,
    become one arc (an arc first fitted as an arc and a short chord, say)."""
    changed = True
    while changed and len(segs) > 1:
        changed = False
        for k in range(len(segs) - 1):
            a, b = segs[k], segs[k + 1]
            if a["kind"] == "line" and b["kind"] == "line":
                # one shaky straight edge split in pieces: merge while one chord still fits them
                i0, i1 = a["span"][0], b["span"][1]
                if _chord_dev(stroke[i0 : i1 + 1]) <= 1.5 * tol:
                    segs[k : k + 2] = [
                        {"kind": "line", "a": stroke[i0], "b": stroke[i1], "span": (i0, i1)}
                    ]
                    changed = True
                    break
                continue
            i0, i1 = a["span"][0], b["span"][1]
            piece = stroke[i0 : i1 + 1]
            joint = a["span"][1]
            if len(piece) < 5 or not _tangent_continuous(stroke, joint, 35.0):
                continue
            c, r, res = fit_circle(piece)
            sweep = _sweep(piece, c)
            if (
                res <= (2.0 if a["kind"] == b["kind"] == "arc" else 1.5) * tol
                and abs(sweep) > 0.25
                and _chord_dev(piece) >= 1.5 * tol
                and r < 50 * np.linalg.norm(piece[-1] - piece[0]) + 1e-9
            ):
                segs[k : k + 2] = [
                    {
                        "kind": "arc",
                        "a": piece[0],
                        "b": piece[-1],
                        "c": c,
                        "r": r,
                        "ccw": sweep > 0,
                        "span": (i0, i1),
                    }
                ]
                changed = True
                break
    return segs


def _smooth(stroke: np.ndarray, idx: list[int], limit_deg: float = 40.0) -> bool:
    """No sharp corner inside: every turn between consecutive RDP pieces is gentle and
    they all turn the same way (an arc, not a zig-zag)."""
    if len(idx) < 3:
        return True
    turns = []
    for a, b, c in zip(idx, idx[1:], idx[2:], strict=False):
        u, w = stroke[b] - stroke[a], stroke[c] - stroke[b]
        turns.append(math.atan2(float(_cross(u, w)), float(u @ w)))
    return all(abs(t) <= math.radians(limit_deg) for t in turns) and (
        all(t >= -1e-9 for t in turns) or all(t <= 1e-9 for t in turns)
    )


def _sweep(piece: np.ndarray, c: np.ndarray) -> float:
    ang = np.unwrap(np.arctan2(piece[:, 1] - c[1], piece[:, 0] - c[0]))
    return float(ang[-1] - ang[0])


def _smooth_stroke(pts: np.ndarray, passes: int = 2) -> np.ndarray:
    """Hand jitter off a stroke: a (1, 2, 1) / 4 filter run ``passes`` times, the two ends
    kept where they were drawn."""
    out = pts.copy()
    for _ in range(passes):
        if len(out) < 5:
            break
        inner = (out[:-2] + 2 * out[1:-1] + out[2:]) / 4.0
        out = np.vstack([out[:1], inner, out[-1:]])
    return out


def classify(strokes: list[Stroke], tol: float) -> list[dict]:
    items: list[dict] = []
    for raw in strokes:
        pts = np.array(raw, float)
        # this stroke's own jitter sets how loosely it is read
        noise = (
            float(np.sqrt(np.mean(np.sum((pts - _smooth_stroke(pts, 1)) ** 2, axis=1))))
            if len(pts) >= 5
            else 0.0
        )
        stol = max(tol, 3.0 * noise)
        if len(pts) < 2:
            continue
        size = float(np.max(np.ptp(pts, axis=0)))
        closed = np.linalg.norm(pts[0] - pts[-1]) < max(0.12 * size, stol * 3)
        if closed and len(pts) >= 8:
            c, r, res = fit_circle(pts)
            spread = float(np.std(np.linalg.norm(pts - c, axis=1)) / max(r, 1e-9))
            if spread < 0.12 and res < max(stol * 2, 0.08 * r):
                items.append({"kind": "circle", "c": c, "r": r})
                continue
        if closed:
            pts = np.vstack([pts, pts[:1]])
        items += _segments(pts, stol)
    return items


# ---------- topology and intent ----------


def build_sketch(items: list[dict], snap: float) -> tuple[sk.Sketch, list[str]]:
    points: list[list[float]] = []
    weights: list[int] = []

    def pid(p: np.ndarray) -> int:
        for k, q in enumerate(points):
            if math.dist(q, p) <= snap:
                w = weights[k]
                points[k] = [(q[0] * w + p[0]) / (w + 1), (q[1] * w + p[1]) / (w + 1)]
                weights[k] += 1
                return k
        points.append([float(p[0]), float(p[1])])
        weights.append(1)
        return len(points) - 1

    ents: list[dict] = []
    for it in items:
        if it["kind"] == "circle":
            ents.append({"type": "circle", "cxy": it["c"], "r": it["r"]})
        elif it["kind"] == "line":
            a, b = pid(it["a"]), pid(it["b"])
            if a != b:
                ents.append({"type": "line", "a": a, "b": b})
        else:
            a, b = pid(it["a"]), pid(it["b"])
            if a != b:
                s, e = (a, b) if it["ccw"] else (b, a)
                ents.append({"type": "arc", "s": s, "e": e, "cxy": it["c"], "r": it["r"]})
    notes: list[str] = []
    # close a chain whose free ends are near each other
    degree: dict[int, int] = {}
    for e in ents:
        for k in ("a", "b", "s", "e"):
            if k in e:
                degree[e[k]] = degree.get(e[k], 0) + 1
    free = [k for k, d in degree.items() if d == 1]
    if len(free) == 2 and math.dist(points[free[0]], points[free[1]]) <= 3 * snap:
        ents.append({"type": "line", "a": free[0], "b": free[1]})
        notes.append("Closed the outline where its ends nearly met.")
    elif len(free) >= 2:
        notes.append(
            f"{len(free)} open end(s): the outline is not closed, so it cannot become a solid yet."
        )
    # sketch model
    pts = [{"id": f"p{k}", "x": round(x, 4), "y": round(y, 4)} for k, (x, y) in enumerate(points)]
    entities, cons = [], []
    for n, e in enumerate(ents):
        if e["type"] == "line":
            entities.append({"type": "line", "id": f"l{n}", "a": f"p{e['a']}", "b": f"p{e['b']}"})
        else:
            cid = f"c{n}"
            pts.append(
                {"id": cid, "x": round(float(e["cxy"][0]), 4), "y": round(float(e["cxy"][1]), 4)}
            )
            if e["type"] == "circle":
                entities.append(
                    {"type": "circle", "id": f"o{n}", "center": cid, "radius": round(e["r"], 4)}
                )
            else:
                entities.append(
                    {
                        "type": "arc",
                        "id": f"a{n}",
                        "center": cid,
                        "start": f"p{e['s']}",
                        "end": f"p{e['e']}",
                    }
                )
    if pts:
        pts[0]["fixed"] = True
    xy = {p["id"]: np.array([p["x"], p["y"]]) for p in pts}
    lines = [e for e in entities if e["type"] == "line"]
    rounds = [e for e in entities if e["type"] in ("circle", "arc")]

    def direction(e: dict) -> np.ndarray:
        d = xy[e["b"]] - xy[e["a"]]
        return d / max(np.linalg.norm(d), 1e-12)

    def length(e: dict) -> float:
        return float(np.linalg.norm(xy[e["b"]] - xy[e["a"]]))

    deg = math.radians
    oriented: set[str] = set()
    for e in lines:
        d = direction(e)
        if abs(d[1]) <= math.sin(deg(6)):
            cons.append({"kind": "horizontal", "refs": [e["id"]]})
            oriented.add(e["id"])
        elif abs(d[0]) <= math.sin(deg(6)):
            cons.append({"kind": "vertical", "refs": [e["id"]]})
            oriented.add(e["id"])
    free_lines = [e for e in lines if e["id"] not in oriented]
    for i, e in enumerate(free_lines):
        for f in free_lines[i + 1 :]:
            c = abs(float(_cross(direction(e), direction(f))))
            if c <= math.sin(deg(5)):
                cons.append({"kind": "parallel", "refs": [e["id"], f["id"]]})
            elif abs(float(direction(e) @ direction(f))) <= math.sin(deg(5)):
                cons.append({"kind": "perpendicular", "refs": [e["id"], f["id"]]})
    for i, e in enumerate(lines):
        for f in lines[i + 1 :]:
            le, lf = length(e), length(f)
            if abs(le - lf) <= 0.06 * max(le, lf):
                cons.append({"kind": "equal", "refs": [e["id"], f["id"]]})
    for r in rounds:
        if r["type"] != "arc":
            continue
        c = xy[r["center"]]
        for end in (r["start"], r["end"]):
            for e in lines:
                if end not in (e["a"], e["b"]):
                    continue
                radial = xy[end] - c
                radial /= max(np.linalg.norm(radial), 1e-12)
                if abs(float(radial @ direction(e))) <= math.sin(deg(10)):
                    cons.append({"kind": "tangent", "refs": [e["id"], r["id"]]})
    circles = [r for r in rounds if r["type"] == "circle"]
    for i, a in enumerate(rounds):
        for b in rounds[i + 1 :]:
            if math.dist(xy[a["center"]], xy[b["center"]]) <= snap:
                cons.append({"kind": "concentric", "refs": [a["id"], b["id"]]})
            elif (
                a in circles
                and b in circles
                and abs(a["radius"] - b["radius"]) <= 0.06 * max(a["radius"], b["radius"])
            ):
                cons.append({"kind": "equal", "refs": [a["id"], b["id"]]})
    return _solve_greedy(pts, entities, cons, notes)


def _solve_greedy(
    pts: list, entities: list, cons: list, notes: list[str]
) -> tuple[sk.Sketch, list[str]]:
    """Add the inferred constraints one by one, dropping any the solver cannot meet."""
    kept: list[dict] = []
    current = sk.Sketch.model_validate({"points": pts, "entities": entities, "constraints": []})
    dropped = 0
    for c in cons:
        trial = current.model_copy(
            update={"constraints": [*current.constraints, sk.Constraint.model_validate(c)]}
        )
        try:
            res = sk.solve(trial)
        except Exception:  # the solver raises on degenerate input
            dropped += 1
            continue
        if res.ok:
            current = res.sketch
            kept.append(c)
        else:
            dropped += 1
    counts: dict[str, int] = {}
    for c in kept:
        counts[c["kind"]] = counts.get(c["kind"], 0) + 1
    if counts:
        notes.append("Inferred " + ", ".join(f"{n} {k}" for k, n in counts.items()) + ".")
    if dropped:
        notes.append(
            f"{dropped} suggested constraint(s) dropped (they conflicted with the others)."
        )
    return current, notes


def clean_view(strokes: list[Stroke], tolerance: float | None, snap: float | None) -> dict:
    allpts = np.array([p for s in strokes for p in s], float)
    if len(allpts) < 2:
        raise ValueError("draw at least one stroke")
    size = float(np.max(np.ptp(allpts, axis=0))) or 1.0
    tol = tolerance or 0.015 * size
    snp = snap or 0.04 * size
    items = classify(strokes, tol)
    sketch, notes = build_sketch(items, snp)
    try:
        regions = sk.regions(sketch)
    except ValueError:
        regions = []
    return {
        "sketch": sketch,
        "notes": notes,
        "closed": bool(regions),
        "tolerance": tol,
        "snap": snp,
        "counts": {
            k: sum(1 for e in sketch.entities if e.type == k) for k in ("line", "arc", "circle")
        },
    }


# ---------- 3D ----------


def _bounds(s: sk.Sketch) -> tuple[float, float, float, float]:
    xs, ys = [], []
    by_id = {p.id: p for p in s.points}
    for e in s.entities:
        if e.type == "circle":
            c = by_id[e.center]
            xs += [c.x - e.radius, c.x + e.radius]
            ys += [c.y - e.radius, c.y + e.radius]
        elif e.type == "arc":
            c, a, b = by_id[e.center], by_id[e.start], by_id[e.end]
            r = math.dist((c.x, c.y), (a.x, a.y))
            t0 = math.atan2(a.y - c.y, a.x - c.x)
            t1 = math.atan2(b.y - c.y, b.x - c.x)
            while t1 <= t0:
                t1 += 2 * math.pi
            for k in range(33):  # the arc itself, counter-clockwise from start to end
                t = t0 + (t1 - t0) * k / 32
                xs.append(c.x + r * math.cos(t))
                ys.append(c.y + r * math.sin(t))
        else:
            for q in (by_id[e.a], by_id[e.b]):
                xs.append(q.x)
                ys.append(q.y)
    return min(xs), min(ys), max(xs), max(ys)


def _transform(s: sk.Sketch, sx: float, sy: float, dx: float, dy: float) -> sk.Sketch:
    """Scale (non-uniformly) and move a sketch; constraints that a non-uniform scale would
    break (equal, tangent, concentric radii) are dropped when sx != sy."""
    pts = [
        p.model_copy(update={"x": round(p.x * sx + dx, 4), "y": round(p.y * sy + dy, 4)})
        for p in s.points
    ]
    ents = []
    for e in s.entities:
        if e.type == "circle":
            ents.append(e.model_copy(update={"radius": e.radius * math.sqrt(abs(sx * sy))}))
        else:
            ents.append(e)
    keep = (
        s.constraints
        if math.isclose(sx, sy, rel_tol=1e-6)
        else [
            c
            for c in s.constraints
            if c.kind in ("horizontal", "vertical", "parallel", "perpendicular")
        ]
    )
    return sk.Sketch(points=pts, entities=ents, constraints=keep)


def part(body: FreehandIn) -> tuple[dict, dict]:
    """(PartDoc dict, report) for the sketches."""
    cleaned = {
        v: clean_view(strokes, body.tolerance, body.snap)
        for v, strokes in body.views.items()
        if strokes
    }
    if not cleaned:
        raise ValueError("draw at least one view")
    report = {
        v: {"notes": c["notes"], "closed": c["closed"], "counts": c["counts"]}
        for v, c in cleaned.items()
    }
    for v, c in cleaned.items():
        if not c["closed"]:
            raise ValueError(f"the {v} view has no closed outline: {' '.join(c['notes'])}")
    feats: list[dict] = []
    if body.mode == "extrude" or (body.mode == "views" and len(cleaned) == 1):
        view, c = next(iter(cleaned.items()))
        s = c["sketch"]
        x0, y0, x1, y1 = _bounds(s)
        s = _transform(s, 1, 1, -(x0 + x1) / 2, -y0)  # centred, sitting on the plane's v = 0
        feats.append(
            {
                "id": "pad",
                "name": f"Pad of the {view} sketch",
                "type": "pad",
                "plane": VIEW_PLANE[view],
                "sketch": s.model_dump(),
                "depth": body.depth,
                "symmetric": True,
            }
        )
    elif body.mode == "revolve":
        view, c = next(iter(cleaned.items()))
        s = c["sketch"]
        x0, y0, x1, y1 = _bounds(s)
        s = _transform(s, 1, 1, -x0, -y0)  # the left-most point on the axis u = 0
        feats.append(
            {
                "id": "shaft",
                "name": f"Revolve of the {view} sketch",
                "type": "shaft",
                "plane": "xz",
                "sketch": s.model_dump(),
                "angle": 360.0,
            }
        )
    else:
        # extents per world axis from the views that show them; the front view sets X and Z
        b = {v: _bounds(c["sketch"]) for v, c in cleaned.items()}
        span = {}
        if "front" in b:
            span["x"], span["z"] = b["front"][2] - b["front"][0], b["front"][3] - b["front"][1]
        if "top" in b:
            span.setdefault("x", b["top"][2] - b["top"][0])
            span["y"] = b["top"][3] - b["top"][1]
        if "side" in b:
            span.setdefault("y", b["side"][2] - b["side"][0])
            span.setdefault("z", b["side"][3] - b["side"][1])
        axes = {"front": ("x", "z"), "top": ("x", "y"), "side": ("y", "z")}
        first = True
        for v, c in cleaned.items():
            u, w = axes[v]
            bx = b[v]
            su = span.get(u, bx[2] - bx[0]) / max(bx[2] - bx[0], 1e-9)
            sw = span.get(w, bx[3] - bx[1]) / max(bx[3] - bx[1], 1e-9)
            # centre u (X and Y about 0), w from 0 (Z up from the ground; Y centred)
            du = -(bx[0] + bx[2]) / 2 * su
            dw = -bx[1] * sw if w == "z" else -(bx[1] + bx[3]) / 2 * sw
            s = _transform(c["sketch"], su, sw, du, dw)
            normal_axis = ({"x", "y", "z"} - {u, w}).pop()
            depth = 2.2 * max(span.get(normal_axis, body.depth), 1.0)
            feats.append(
                {
                    "id": f"view_{v}",
                    "name": f"{v.capitalize()} view",
                    "type": "pad",
                    "op": "add" if first else "intersect",
                    "plane": VIEW_PLANE[v],
                    "sketch": s.model_dump(),
                    "depth": depth,
                    "symmetric": True,
                }
            )
            first = False
            if su != sw:
                report[v]["notes"].append(f"Scaled to match the other views ({su:.2f} × {sw:.2f}).")
    doc = {"name": body.name, "features": feats, "color": [0.7, 0.72, 0.76]}
    return doc, report
