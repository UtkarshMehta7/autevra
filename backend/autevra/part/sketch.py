"""Constrained 2D sketches: points, lines, circles and arcs held by geometric and
dimensional constraints, solved numerically (damped Gauss-Newton / Levenberg-Marquardt,
smallest move from the current positions), with a degrees-of-freedom analysis that tells
which points are fully constrained and which constraints conflict.

Coordinates are (u, v) in the sketch plane, millimetres; angles are degrees.
"""

import math
from typing import Annotated, Literal

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, model_validator

Coord = Annotated[float, Field(ge=-50_000.0, le=50_000.0)]
Id = Annotated[str, Field(min_length=1, max_length=24, pattern=r"^[A-Za-z0-9_]+$")]


class SPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Id
    x: Coord = 0.0
    y: Coord = 0.0
    fixed: bool = False  # anchored: the solver never moves it


class Line(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: Literal["line"] = "line"
    id: Id
    a: Id
    b: Id
    construction: bool = False  # reference geometry, not part of a profile


class Circle(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: Literal["circle"] = "circle"
    id: Id
    center: Id
    radius: float = Field(10.0, gt=0.0, le=50_000.0)
    construction: bool = False


class Arc(BaseModel):
    """Counter-clockwise from ``start`` to ``end`` about ``center`` (both ends at the same
    radius: the solver keeps them there)."""

    model_config = ConfigDict(frozen=True)

    type: Literal["arc"] = "arc"
    id: Id
    center: Id
    start: Id
    end: Id
    construction: bool = False


Entity = Annotated[Line | Circle | Arc, Field(discriminator="type")]

# Constraint kinds and what they refer to (p = point, l = line, c = circle or arc).
KINDS: dict[str, tuple[str, bool]] = {
    "coincident": ("pp", False),
    "horizontal": ("l", False),
    "vertical": ("l", False),
    "parallel": ("ll", False),
    "perpendicular": ("ll", False),
    "equal": ("ee", False),  # two lines (length) or two circles/arcs (radius)
    "tangent": ("ec", False),  # line-circle or circle-circle
    "point_on": ("pe", False),  # a point on a line (infinite) or a circle/arc
    "midpoint": ("pl", False),
    "symmetric": ("ppl", False),  # two points mirrored about a line
    "distance": ("pp", True),
    "hdistance": ("pp", True),  # signed: b.x - a.x
    "vdistance": ("pp", True),  # signed: b.y - a.y
    "length": ("l", True),
    "radius": ("c", True),
    "diameter": ("c", True),
    "angle": ("ll", True),  # from the first line to the second, counter-clockwise
}
Kind = Literal[
    "coincident", "horizontal", "vertical", "parallel", "perpendicular", "equal", "tangent",
    "point_on", "midpoint", "symmetric", "distance", "hdistance", "vdistance", "length",
    "radius", "diameter", "angle",
]  # fmt: skip


class Constraint(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: Kind
    refs: list[Id] = Field(min_length=1, max_length=3)
    value: float | None = None  # dimensions only (mm or degrees)

    @model_validator(mode="after")
    def _shape(self) -> "Constraint":
        pattern, dimensional = KINDS[self.kind]
        if len(self.refs) != len(pattern):
            raise ValueError(f"{self.kind} takes {len(pattern)} reference(s)")
        if dimensional and self.value is None:
            raise ValueError(f"{self.kind} needs a value")
        if self.kind in ("distance", "length", "radius", "diameter") and (self.value or 0) <= 0:
            raise ValueError(f"{self.kind} must be above zero")
        return self


class Sketch(BaseModel):
    model_config = ConfigDict(frozen=True)

    points: list[SPoint] = Field(default_factory=list, max_length=400)
    entities: list[Entity] = Field(default_factory=list, max_length=300)
    constraints: list[Constraint] = Field(default_factory=list, max_length=600)

    @model_validator(mode="after")
    def _references(self) -> "Sketch":
        pids = [p.id for p in self.points]
        eids = [e.id for e in self.entities]
        if len(set(pids)) != len(pids) or len(set(eids)) != len(eids):
            raise ValueError("sketch point and entity ids must be unique")
        if set(pids) & set(eids):
            raise ValueError("a sketch point and an entity share an id")
        known = set(pids)
        for e in self.entities:
            used = (
                [e.a, e.b]
                if isinstance(e, Line)
                else ([e.center] if isinstance(e, Circle) else [e.center, e.start, e.end])
            )
            missing = [p for p in used if p not in known]
            if missing:
                raise ValueError(f"{e.id} refers to unknown point(s) {missing}")
        kinds = {p.id: "p" for p in self.points} | {
            e.id: ("l" if isinstance(e, Line) else "c") for e in self.entities
        }
        for i, c in enumerate(self.constraints):
            if c.kind == "equal" and len({kinds.get(r) for r in c.refs}) != 1:
                raise ValueError(f"constraint {i} (equal): pick two lines or two circles/arcs")
            pattern = KINDS[c.kind][0]
            for ref, want in zip(c.refs, pattern, strict=True):
                got = kinds.get(ref)
                ok = got is not None and (
                    want == got or want == "e" and got in "lc" or want == "c" and got == "c"
                )
                if not ok:
                    raise ValueError(
                        f"constraint {i} ({c.kind}): '{ref}' is not a valid "
                        f"{
                            {
                                'p': 'point',
                                'l': 'line',
                                'c': 'circle or arc',
                                'e': 'line, circle or arc',
                            }[want]
                        }"
                    )
        return self


# ---------------------------------------------------------------------------- solving


class Iteration(BaseModel):
    """One step of the damped Gauss-Newton solve."""

    step: int
    cost: float  # sum of squared residuals |f|^2 at the trial point
    max_residual: float  # the largest single residual at the trial point
    damping: float  # lambda used for this step
    step_norm: float  # |dx|
    accepted: bool  # the trial lowered the cost (else lambda grows and the step is retried)


class Equation(BaseModel):
    """A constraint as the equations the solver drives to zero."""

    index: int | None  # the constraint's index (None: an arc's own equal-radius equation)
    kind: str
    text: str  # the equation(s), with the sketch's point and entity names
    rows: int  # equations it contributes (rows of the Jacobian)
    residual: float  # the largest of its residuals at the solution


class SolveResult(BaseModel):
    sketch: Sketch
    ok: bool  # every constraint met
    dof: int  # remaining degrees of freedom (0 = fully constrained)
    redundant: int  # constraint equations that add nothing (consistent over-constraint)
    conflicting: list[int]  # indices of constraints not met
    fixed_points: list[str]  # points the constraints pin down completely
    fixed_entities: list[str]  # entities whose every point (and radius) is pinned
    residual: float
    # Inspection: the nonlinear system F(x) = 0 and how the solver converged.
    method: str = ""
    unknowns: int = 0  # n: free point coordinates and circle radii
    equations: list[Equation] = []  # m rows in all
    rank: int = 0  # of the Jacobian at the solution (DOF = n - rank, redundant = m - rank)
    iterations: list[Iteration] = []
    converged: bool = False


class _System:
    """Unknowns: x, y of every free point and the radius of every circle."""

    def __init__(self, sk: Sketch) -> None:
        self.sk = sk
        self.point = {p.id: p for p in sk.points}
        self.entity = {e.id: e for e in sk.entities}
        self.index: dict[str, int] = {}
        x0: list[float] = []
        for p in sk.points:
            if not p.fixed:
                self.index[p.id] = len(x0)
                x0 += [p.x, p.y]
        for e in sk.entities:
            if isinstance(e, Circle):
                self.index[e.id] = len(x0)
                x0.append(e.radius)
        self.x0 = np.array(x0, dtype=float)
        # tangency kind (outside / inside / line) decided once from the starting shape
        self.tangent_inside: dict[int, bool] = {}
        for i, c in enumerate(sk.constraints):
            if c.kind == "tangent" and all(self._is_round(r) for r in c.refs):
                x = self.x0
                d = float(
                    np.linalg.norm(self.p(c.refs[0], x, "center") - self.p(c.refs[1], x, "center"))
                )
                r1, r2 = self.r(c.refs[0], x), self.r(c.refs[1], x)
                self.tangent_inside[i] = abs(d - abs(r1 - r2)) < abs(d - (r1 + r2))

    def _is_round(self, eid: str) -> bool:
        return isinstance(self.entity.get(eid), Circle | Arc)

    def xy(self, pid: str, x: np.ndarray) -> np.ndarray:
        i = self.index.get(pid)
        if i is None:
            p = self.point[pid]
            return np.array([p.x, p.y])
        return x[i : i + 2]

    def p(self, eid: str, x: np.ndarray, part: str) -> np.ndarray:
        return self.xy(getattr(self.entity[eid], part), x)

    def r(self, eid: str, x: np.ndarray) -> float:
        e = self.entity[eid]
        if isinstance(e, Circle):
            return float(x[self.index[e.id]])
        return float(np.linalg.norm(self.xy(e.start, x) - self.xy(e.center, x)))

    def ends(self, lid: str, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        e = self.entity[lid]
        return self.xy(e.a, x), self.xy(e.b, x)

    def residuals(
        self, x: np.ndarray, values: list[float | None] | None = None
    ) -> list[np.ndarray]:
        """One array of residuals per constraint, then one per arc (equal end radii)."""
        out: list[np.ndarray] = []
        for i, c in enumerate(self.sk.constraints):
            v = c.value if values is None else values[i]
            out.append(np.atleast_1d(np.asarray(self._one(i, c, v, x), dtype=float)))
        for e in self.sk.entities:
            if isinstance(e, Arc):
                c, s, t = self.xy(e.center, x), self.xy(e.start, x), self.xy(e.end, x)
                out.append(np.array([np.linalg.norm(t - c) - np.linalg.norm(s - c)]))
        return out

    def _one(self, i: int, c: Constraint, v: float | None, x: np.ndarray):  # noqa: C901
        refs = c.refs
        unit = lambda d: d / max(float(np.linalg.norm(d)), 1e-9)  # noqa: E731
        match c.kind:
            case "coincident":
                return self.xy(refs[0], x) - self.xy(refs[1], x)
            case "horizontal":
                a, b = self.ends(refs[0], x)
                return b[1] - a[1]
            case "vertical":
                a, b = self.ends(refs[0], x)
                return b[0] - a[0]
            case "parallel" | "perpendicular" | "angle":
                a, b = self.ends(refs[0], x)
                p, q = self.ends(refs[1], x)
                u, w = unit(b - a), unit(q - p)
                cross, dot = u[0] * w[1] - u[1] * w[0], float(u @ w)
                if c.kind == "parallel":
                    return cross
                if c.kind == "perpendicular":
                    return dot
                t = math.radians(v or 0.0)
                return cross * math.cos(t) - dot * math.sin(t)  # sin(angle - target)
            case "equal":
                if self.entity[refs[0]].type == "line" and self.entity[refs[1]].type == "line":
                    a, b = self.ends(refs[0], x)
                    p, q = self.ends(refs[1], x)
                    return np.linalg.norm(b - a) - np.linalg.norm(q - p)
                return self.r(refs[0], x) - self.r(refs[1], x)
            case "tangent":
                if self.entity[refs[0]].type == "line":
                    a, b = self.ends(refs[0], x)
                    cc = self.p(refs[1], x, "center")
                    d = b - a
                    dist = abs(d[0] * (cc - a)[1] - d[1] * (cc - a)[0]) / max(
                        float(np.linalg.norm(d)), 1e-9
                    )
                    return dist - self.r(refs[1], x)
                d = float(
                    np.linalg.norm(self.p(refs[0], x, "center") - self.p(refs[1], x, "center"))
                )
                r1, r2 = self.r(refs[0], x), self.r(refs[1], x)
                return d - abs(r1 - r2) if self.tangent_inside.get(i) else d - (r1 + r2)
            case "point_on":
                pt = self.xy(refs[0], x)
                if self.entity[refs[1]].type == "line":
                    a, b = self.ends(refs[1], x)
                    d = b - a
                    return (d[0] * (pt - a)[1] - d[1] * (pt - a)[0]) / max(
                        float(np.linalg.norm(d)), 1e-9
                    )
                return np.linalg.norm(pt - self.p(refs[1], x, "center")) - self.r(refs[1], x)
            case "midpoint":
                a, b = self.ends(refs[1], x)
                return self.xy(refs[0], x) - (a + b) / 2
            case "symmetric":
                p, q = self.xy(refs[0], x), self.xy(refs[1], x)
                a, b = self.ends(refs[2], x)
                d = unit(b - a)
                m = (p + q) / 2 - a
                return np.array([d[0] * m[1] - d[1] * m[0], float((q - p) @ d)])
            case "distance":
                return np.linalg.norm(self.xy(refs[1], x) - self.xy(refs[0], x)) - (v or 0.0)
            case "hdistance":
                return self.xy(refs[1], x)[0] - self.xy(refs[0], x)[0] - (v or 0.0)
            case "vdistance":
                return self.xy(refs[1], x)[1] - self.xy(refs[0], x)[1] - (v or 0.0)
            case "length":
                a, b = self.ends(refs[0], x)
                return np.linalg.norm(b - a) - (v or 0.0)
            case "radius":
                return self.r(refs[0], x) - (v or 0.0)
            case "diameter":
                return 2 * self.r(refs[0], x) - (v or 0.0)
        raise ValueError(c.kind)

    def vector(self, x: np.ndarray) -> np.ndarray:
        parts = self.residuals(x)
        return np.concatenate(parts) if parts else np.zeros(0)

    def jacobian(self, x: np.ndarray) -> np.ndarray:
        f0 = self.vector(x)
        jac = np.zeros((f0.size, x.size))
        for j in range(x.size):
            h = 1e-6 * max(1.0, abs(x[j]))
            xp = x.copy()
            xp[j] += h
            jac[:, j] = (self.vector(xp) - f0) / h
        return jac

    def solve(self, x: np.ndarray, cost_of_moving: np.ndarray | None = None,
              iterations: int = 100) -> np.ndarray:  # fmt: skip
        """Damped minimum-move Gauss-Newton: each step solves
        (J W J^T + lam I) y = -f, dx = W J^T y, with W the inverse cost of moving each
        unknown, so an under-constrained sketch keeps its drawn shape (and a dragged point
        stays under the cursor while the others give way)."""
        inv = np.ones(x.size) if cost_of_moving is None else 1.0 / cost_of_moving
        lam = 1e-3
        f = self.vector(x)
        cost = float(f @ f)
        self.history: list[Iteration] = []
        for step in range(iterations):
            if cost < 1e-20 or x.size == 0:
                break
            jac = self.jacobian(x)
            a_mat = (jac * inv) @ jac.T + lam * np.eye(jac.shape[0])
            try:
                dx = inv * (jac.T @ np.linalg.solve(a_mat, -f))
            except np.linalg.LinAlgError:
                dx = np.linalg.lstsq(jac, -f, rcond=None)[0]
            trial = x + dx
            ft = self.vector(trial)
            ct = float(ft @ ft)
            self.history.append(Iteration(
                step=step + 1, cost=ct, max_residual=float(np.max(np.abs(ft))) if ft.size else 0.0,
                damping=lam, step_norm=float(np.linalg.norm(dx)), accepted=ct < cost,
            ))  # fmt: skip
            if ct < cost:
                x, f, cost = trial, ft, ct
                lam = max(lam / 3, 1e-12)
            else:
                lam *= 10
                if lam > 1e8:
                    break
        return x

    def write(self, x: np.ndarray) -> Sketch:
        points = [p.model_copy(update={"x": round(float(x[self.index[p.id]]), 6),
                                       "y": round(float(x[self.index[p.id] + 1]), 6)})
                  if p.id in self.index else p for p in self.sk.points]  # fmt: skip
        entities = [e.model_copy(update={"radius": round(float(x[self.index[e.id]]), 6)})
                    if isinstance(e, Circle) else e for e in self.sk.entities]  # fmt: skip
        return self.sk.model_copy(update={"points": points, "entities": entities})


TOL = 1e-6


def solve(sk: Sketch, drag: tuple[str, float, float] | None = None) -> SolveResult:
    """Move the sketch the least to meet its constraints. ``drag`` (point, x, y) puts that
    point at the cursor and makes it costly to move, so it stays there as far as the
    constraints allow while the rest of the sketch follows."""
    weights = None
    if drag is not None:
        pid, dx, dy = drag
        target = next((p for p in sk.points if p.id == pid and not p.fixed), None)
        if target is not None:
            sk = sk.model_copy(update={"points": [
                p.model_copy(update={"x": dx, "y": dy}) if p is target else p
                for p in sk.points]})  # fmt: skip
    system = _System(sk)
    if drag is not None and drag[0] in system.index:
        weights = np.ones(system.x0.size)
        i = system.index[drag[0]]
        weights[i : i + 2] = 1e4
    x = system.solve(system.x0.copy(), weights)
    parts = system.residuals(x)
    conflicting = [i for i, r in enumerate(parts[: len(sk.constraints)])
                   if float(np.max(np.abs(r))) > 1e-4]  # fmt: skip
    arcs_bad = any(float(np.max(np.abs(r))) > 1e-4 for r in parts[len(sk.constraints) :])
    f = np.concatenate(parts) if parts else np.zeros(0)
    jac = system.jacobian(x) if x.size and f.size else np.zeros((f.size, x.size))
    rank = int(np.linalg.matrix_rank(jac, tol=1e-6)) if jac.size else 0
    # a variable is pinned when it has no component in the Jacobian's null space
    if x.size:
        _, s, vt = np.linalg.svd(jac if jac.size else np.zeros((1, x.size)))
        null = vt[rank:]
        free = np.abs(null).max(axis=0) > 1e-6 if null.size else np.zeros(x.size, bool)
    else:
        free = np.zeros(0, bool)
    pinned = lambda i: not bool(free[i])  # noqa: E731
    fixed_points = [
        p.id
        for p in sk.points
        if p.fixed or (pinned(system.index[p.id]) and pinned(system.index[p.id] + 1))
    ]
    fp = set(fixed_points)
    fixed_entities = []
    for e in sk.entities:
        pts = (
            [e.a, e.b]
            if isinstance(e, Line)
            else ([e.center] if isinstance(e, Circle) else [e.center, e.start, e.end])
        )
        if all(q in fp for q in pts) and (not isinstance(e, Circle) or pinned(system.index[e.id])):
            fixed_entities.append(e.id)
    residual = float(np.max(np.abs(f))) if f.size else 0.0
    equations = _equations(sk, parts)
    return SolveResult(
        sketch=system.write(x),
        ok=not conflicting and not arcs_bad,
        dof=int(x.size - rank),
        redundant=int(f.size - rank),
        conflicting=conflicting,
        fixed_points=fixed_points,
        fixed_entities=fixed_entities,
        residual=residual,
        method="Damped minimum-move Gauss-Newton (Levenberg-Marquardt): each step solves "
        "(J W Jᵀ + λI) y = −F, Δx = W Jᵀ y; λ shrinks after a step that lowers |F|² and "
        "grows after one that does not. J by forward differences.",
        unknowns=int(x.size),
        equations=equations,
        rank=rank,
        iterations=getattr(system, "history", []),
        converged=residual <= TOL * 100,
    )


def _equations(sk: Sketch, parts: list[np.ndarray]) -> list[Equation]:
    """Each constraint written as the equation(s) the solver drives to zero."""
    entity = {e.id: e for e in sk.entities}

    def pt(pid: str) -> str:
        return f"P{pid}"

    def seg(lid: str) -> tuple[str, str]:
        e = entity[lid]
        return pt(e.a), pt(e.b)  # type: ignore[union-attr]

    def centre(eid: str) -> str:
        return pt(entity[eid].center)  # type: ignore[union-attr]

    def unit(lid: str) -> str:
        a, b = seg(lid)
        return f"û({a}{b})"

    def text(c: Constraint) -> str:  # noqa: C901
        r, v = c.refs, c.value
        match c.kind:
            case "coincident":
                return f"{pt(r[0])} − {pt(r[1])} = 0"
            case "horizontal":
                a, b = seg(r[0])
                return f"y({b}) − y({a}) = 0"
            case "vertical":
                a, b = seg(r[0])
                return f"x({b}) − x({a}) = 0"
            case "parallel":
                return f"{unit(r[0])} × {unit(r[1])} = 0"
            case "perpendicular":
                return f"{unit(r[0])} · {unit(r[1])} = 0"
            case "angle":
                u, w = unit(r[0]), unit(r[1])
                return f"({u} × {w}) cos {v:g}° − ({u} · {w}) sin {v:g}° = 0"
            case "equal":
                if entity[r[0]].type == "line" and entity[r[1]].type == "line":
                    (a, b), (p, q) = seg(r[0]), seg(r[1])
                    return f"|{b} − {a}| − |{q} − {p}| = 0"
                return f"r({r[0]}) − r({r[1]}) = 0"
            case "tangent":
                if entity[r[0]].type == "line":
                    a, b = seg(r[0])
                    return f"dist({centre(r[1])}, {a}{b}) − r({r[1]}) = 0"
                return f"|{centre(r[0])} − {centre(r[1])}| − (r({r[0]}) ± r({r[1]})) = 0"
            case "point_on":
                if entity[r[1]].type == "line":
                    a, b = seg(r[1])
                    return f"({b} − {a}) × ({pt(r[0])} − {a}) / |{b} − {a}| = 0"
                return f"|{pt(r[0])} − {centre(r[1])}| − r({r[1]}) = 0"
            case "midpoint":
                a, b = seg(r[1])
                return f"{pt(r[0])} − ({a} + {b})/2 = 0"
            case "symmetric":
                p, q = pt(r[0]), pt(r[1])
                return f"midpoint({p}, {q}) on {r[2]}; ({q} − {p}) · {unit(r[2])} = 0"
            case "distance":
                return f"|{pt(r[1])} − {pt(r[0])}| − {v:g} = 0"
            case "hdistance":
                return f"x({pt(r[1])}) − x({pt(r[0])}) − {v:g} = 0"
            case "vdistance":
                return f"y({pt(r[1])}) − y({pt(r[0])}) − {v:g} = 0"
            case "length":
                a, b = seg(r[0])
                return f"|{b} − {a}| − {v:g} = 0"
            case "radius":
                return f"r({r[0]}) − {v:g} = 0"
            case "diameter":
                return f"2 r({r[0]}) − {v:g} = 0"
        return c.kind

    out = []
    for i, c in enumerate(sk.constraints):
        res = parts[i] if i < len(parts) else np.zeros(1)
        out.append(Equation(index=i, kind=c.kind, text=text(c), rows=int(res.size),
                            residual=float(np.max(np.abs(res))) if res.size else 0.0))  # fmt: skip
    arcs = [e for e in sk.entities if isinstance(e, Arc)]
    for e, res in zip(arcs, parts[len(sk.constraints) :], strict=False):
        c, a, b = pt(e.center), pt(e.start), pt(e.end)
        out.append(Equation(
            index=None, kind="arc", text=f"|{b} − {c}| − |{a} − {c}| = 0",
            rows=int(res.size), residual=float(np.max(np.abs(res))) if res.size else 0.0,
        ))  # fmt: skip
    return out


# ---------------------------------------------------------------------------- profiles


def _arc_points(c: np.ndarray, s: np.ndarray, e: np.ndarray) -> tuple[float, float, float]:
    r = float(np.linalg.norm(s - c))
    a0 = math.atan2(s[1] - c[1], s[0] - c[0])
    a1 = math.atan2(e[1] - c[1], e[0] - c[0])
    if a1 <= a0 + 1e-9:
        a1 += 2 * math.pi
    return r, a0, a1


def loops(
    sk: Sketch, tol: float = 1e-4
) -> list[list[tuple[str, tuple[float, float], tuple[float, float], tuple[float, float] | None]]]:
    """Closed chains of the profile geometry (lines and arcs, construction left out),
    each a list of (entity id, start, end, mid point for an arc or None); circles are
    loops of their own (start = end, mid = the opposite point). Raises with the open ends
    when a chain does not close."""
    pts = {p.id: (p.x, p.y) for p in sk.points}
    edges = []
    out = []
    for e in sk.entities:
        if e.construction:
            continue
        if isinstance(e, Line):
            edges.append((e.id, pts[e.a], pts[e.b], None))
        elif isinstance(e, Arc):
            c, s, t = (np.array(pts[q]) for q in (e.center, e.start, e.end))
            r, a0, a1 = _arc_points(c, s, t)
            m = (a0 + a1) / 2
            edges.append((e.id, pts[e.start], pts[e.end],
                          (c[0] + r * math.cos(m), c[1] + r * math.sin(m))))  # fmt: skip
        else:
            cx, cy = pts[e.center]
            out.append([(e.id, (cx + e.radius, cy), (cx + e.radius, cy), (cx - e.radius, cy))])
    near = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1]) < tol  # noqa: E731
    left = list(edges)
    while left:
        first = left.pop(0)
        chain = [first]
        while not near(chain[-1][2], chain[0][1]):
            end = chain[-1][2]
            nxt = next((i for i, g in enumerate(left) if near(g[1], end) or near(g[2], end)), None)
            if nxt is None:
                raise ValueError(
                    f"the profile is open at ({end[0]:.1f}, {end[1]:.1f}): "
                    "join every end to another or mark it construction"
                )
            g = left.pop(nxt)
            chain.append(g if near(g[1], end) else (g[0], g[2], g[1], g[3]))
        out.append(chain)
    return out


def _area(chain) -> float:
    pts = []
    for _, s, _, m in chain:
        pts.append(s)
        if m is not None:
            pts.append(m)
    return 0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1], strict=True))


def _inside(pt: tuple[float, float], chain) -> bool:
    poly = []
    for _, s, _, m in chain:
        poly.append(s)
        if m is not None:
            poly.append(m)
    x, y = pt
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1], strict=True):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def regions(sk: Sketch):
    """Profile loops nested into faces: [(outer loop, [hole loops])], outer loops at even
    depth, holes at odd depth (a loop inside a hole is a new island)."""
    chains = loops(sk)
    if not chains:
        raise ValueError("the sketch has no closed profile")
    order = sorted(range(len(chains)), key=lambda i: abs(_area(chains[i])))

    def probe(chain):
        _, s, e, m = chain[0]
        return m if m is not None else ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2)

    parent: dict[int, int | None] = {}
    for i in order:
        ps = probe(chains[i])
        holders = [j for j in order if j != i and abs(_area(chains[j])) > abs(_area(chains[i]))
                   and _inside(ps, chains[j])]  # fmt: skip
        parent[i] = min(holders, key=lambda j: abs(_area(chains[j]))) if holders else None

    def depth(i: int) -> int:
        d, j = 0, parent[i]
        while j is not None:
            d, j = d + 1, parent[j]
        return d

    faces = []
    for i in order:
        if depth(i) % 2 == 0:
            holes = [chains[j] for j in order if parent[j] == i]
            faces.append((chains[i], holes))
    return faces
