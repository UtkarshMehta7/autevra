import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "../api/client";
import { SolverConsole } from "./SolverConsole";
import type { Sketch, SketchConstraint, SketchEntity, SketchSolve } from "../api/types";

type Pt = [number, number];
type Tool = "select" | "line" | "rect" | "circle" | "arc";

const TOOLS: { id: Tool; label: string; hint: string }[] = [
  { id: "select", label: "Select", hint: "Click to select (shift adds), drag a point to move it" },
  { id: "line", label: "Line", hint: "Click points to draw a chain; click the first point or press Esc to finish" },
  { id: "rect", label: "Rectangle", hint: "Click two opposite corners" },
  { id: "circle", label: "Circle", hint: "Click the centre, then a point on the circle" },
  { id: "arc", label: "Arc", hint: "Click the centre, the start, then the end (counter-clockwise)" },
];

const DIMENSIONS = new Set(["distance", "hdistance", "vdistance", "length", "radius", "diameter", "angle"]);
const KIND_LABEL: Record<string, string> = {
  coincident: "Coincident", horizontal: "Horizontal", vertical: "Vertical", parallel: "Parallel",
  perpendicular: "Perpendicular", equal: "Equal", tangent: "Tangent", point_on: "On curve",
  midpoint: "Midpoint", symmetric: "Symmetric", distance: "Distance", hdistance: "H distance",
  vdistance: "V distance", length: "Length", radius: "Radius", diameter: "Diameter", angle: "Angle",
};
const BIND = (i: number) => `sketch.constraints.${i}.value`;

function nextId(prefix: string, sk: Sketch): string {
  const used = new Set([...sk.points.map((p) => p.id), ...sk.entities.map((e) => e.id)]);
  for (let i = 1; ; i++) if (!used.has(`${prefix}${i}`)) return `${prefix}${i}`;
}

function entityPoints(e: SketchEntity): string[] {
  return e.type === "line" ? [e.a, e.b] : e.type === "circle" ? [e.center] : [e.center, e.start, e.end];
}

/** The constraints that the selection allows, each with its references and (for a
 * dimension) the value measured now, so adding it never moves the sketch. */
export function available(sk: Sketch, sel: string[]): { kind: string; refs: string[]; value?: number }[] {
  const at = (id: string) => sk.points.find((p) => p.id === id)!;
  const ent = (id: string) => sk.entities.find((e) => e.id === id);
  const pts = sel.filter((id) => sk.points.some((p) => p.id === id));
  const lines = sel.filter((id) => ent(id)?.type === "line");
  const rounds = sel.filter((id) => ["circle", "arc"].includes(ent(id)?.type ?? ""));
  const n = sel.length;
  const radius = (id: string) => {
    const e = ent(id)!;
    if (e.type === "circle") return e.radius;
    if (e.type === "arc") { const c = at(e.center), s = at(e.start); return Math.hypot(s.x - c.x, s.y - c.y); }
    return 0;
  };
  const dir = (id: string): Pt => { const e = ent(id) as Extract<SketchEntity, { type: "line" }>; const a = at(e.a), b = at(e.b); return [b.x - a.x, b.y - a.y]; };
  const out: { kind: string; refs: string[]; value?: number }[] = [];
  if (pts.length === 2 && n === 2) {
    const [a, b] = pts.map(at);
    out.push({ kind: "coincident", refs: pts }, { kind: "distance", refs: pts, value: Math.hypot(b.x - a.x, b.y - a.y) },
      { kind: "hdistance", refs: pts, value: b.x - a.x }, { kind: "vdistance", refs: pts, value: b.y - a.y });
  }
  if (lines.length === 1 && n === 1) {
    const [dx, dy] = dir(lines[0]);
    out.push({ kind: "horizontal", refs: lines }, { kind: "vertical", refs: lines }, { kind: "length", refs: lines, value: Math.hypot(dx, dy) });
  }
  if (lines.length === 2 && n === 2) {
    const [u, w] = [dir(lines[0]), dir(lines[1])];
    let ang = (Math.atan2(w[1], w[0]) - Math.atan2(u[1], u[0])) * 180 / Math.PI;
    ang = ((ang % 360) + 360) % 360;
    out.push({ kind: "parallel", refs: lines }, { kind: "perpendicular", refs: lines }, { kind: "equal", refs: lines },
      { kind: "angle", refs: lines, value: ang });
  }
  if (rounds.length === 1 && n === 1) {
    out.push({ kind: "radius", refs: rounds, value: radius(rounds[0]) }, { kind: "diameter", refs: rounds, value: 2 * radius(rounds[0]) });
  }
  if (rounds.length === 2 && n === 2) out.push({ kind: "equal", refs: rounds }, { kind: "tangent", refs: rounds });
  if (lines.length === 1 && rounds.length === 1 && n === 2) out.push({ kind: "tangent", refs: [lines[0], rounds[0]] });
  if (pts.length === 1 && lines.length === 1 && n === 2) {
    out.push({ kind: "point_on", refs: [pts[0], lines[0]] }, { kind: "midpoint", refs: [pts[0], lines[0]] });
  }
  if (pts.length === 1 && rounds.length === 1 && n === 2) out.push({ kind: "point_on", refs: [pts[0], rounds[0]] });
  if (pts.length === 2 && lines.length === 1 && n === 3) out.push({ kind: "symmetric", refs: [pts[0], pts[1], lines[0]] });
  return out;
}

/**
 * Constrained sketcher: draw lines, rectangles, circles and arcs; add geometric
 * constraints and dimensions from the selection; drag points (the solver keeps the
 * constraints). Fully constrained geometry turns green; conflicting constraints show red.
 * Dimensions can be driven by a formula of the part's parameters.
 */
export function ConstraintSketcher({ sketch, bindings, labels = ["u", "v"], axis = false, onApply }: {
  sketch: Sketch;
  bindings: Record<string, string>;
  labels?: [string, string];
  axis?: boolean; // draw the revolve axis (the vertical axis through the origin)
  onApply: (sketch: Sketch, bindings: Record<string, string>) => void;
}) {
  const [doc, setDoc] = useState<Sketch>(sketch);
  const [binds, setBinds] = useState<Record<string, string>>(bindings);
  const [status, setStatus] = useState<SketchSolve | null>(null);
  const [tool, setTool] = useState<Tool>("select");
  const [sel, setSel] = useState<string[]>([]);
  const [clicks, setClicks] = useState<string[]>([]); // points placed by the current tool
  const [chainStart, setChainStart] = useState<string | null>(null);
  const [cursor, setCursor] = useState<Pt | null>(null);
  const [drag, setDrag] = useState<string | null>(null);
  const [dirty, setDirty] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const svg = useRef<SVGSVGElement>(null);
  const seq = useRef(0);
  const inflight = useRef(false);
  const queued = useRef<{ sk: Sketch; drag?: { point: string; x: number; y: number } } | null>(null);

  useEffect(() => { setDoc(sketch); setBinds(bindings); setDirty(false); }, [sketch, bindings]);

  const fit = useCallback((sk: Sketch) => {
    const xs = sk.points.map((p) => p.x), ys = sk.points.map((p) => p.y);
    for (const e of sk.entities) if (e.type === "circle") {
      const c = sk.points.find((p) => p.id === e.center)!;
      xs.push(c.x - e.radius, c.x + e.radius); ys.push(c.y - e.radius, c.y + e.radius);
    }
    xs.push(0); ys.push(0);
    const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
    const span = Math.max(x1 - x0, y1 - y0, 20) * 1.4;
    return { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, span };
  }, []);
  const [view, setView] = useState(() => fit(sketch));
  const [px, setPx] = useState(1); // model units per screen pixel
  useEffect(() => {
    const el = svg.current;
    if (!el) return;
    const measure = () => { const r = el.getBoundingClientRect(); if (r.width) setPx(Math.max(view.span * 1.6 / r.width, view.span / r.height)); };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, [view]);

  const solve = useCallback(async (sk: Sketch, dragTo?: { point: string; x: number; y: number }) => {
    if (inflight.current) { queued.current = { sk, drag: dragTo }; return; }
    inflight.current = true;
    const id = ++seq.current;
    try {
      const out = await api.solveSketch(sk, dragTo);
      if (id === seq.current) { setDoc(out.sketch); setStatus(out); setError(null); }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      inflight.current = false;
      const next = queued.current;
      queued.current = null;
      if (next) void solve(next.sk, next.drag);
    }
  }, []);
  useEffect(() => { void solve(sketch); }, [sketch, solve]);

  const change = (sk: Sketch, nextBinds = binds) => { setDoc(sk); setBinds(nextBinds); setDirty(true); void solve(sk); };

  // ---- geometry helpers
  const P = (id: string) => doc.points.find((p) => p.id === id)!;
  const w = view.span * 1.6, h = view.span;
  const toModel = (ev: { clientX: number; clientY: number }): Pt => {
    const r = svg.current!.getBoundingClientRect();
    const s = Math.max(w / r.width, h / r.height);
    return [view.cx + (ev.clientX - (r.left + r.width / 2)) * s, view.cy - (ev.clientY - (r.top + r.height / 2)) * s];
  };
  const hitPoint = (m: Pt): string | null => {
    let best: string | null = null, bd = 9 * px;
    for (const p of doc.points) { const d = Math.hypot(p.x - m[0], p.y - m[1]); if (d < bd) { bd = d; best = p.id; } }
    return best;
  };
  const hitEntity = (m: Pt): string | null => {
    let best: string | null = null, bd = 7 * px;
    for (const e of doc.entities) {
      let d = Infinity;
      if (e.type === "line") {
        const a = P(e.a), b = P(e.b), dx = b.x - a.x, dy = b.y - a.y;
        const t = Math.max(0, Math.min(1, ((m[0] - a.x) * dx + (m[1] - a.y) * dy) / Math.max(dx * dx + dy * dy, 1e-9)));
        d = Math.hypot(a.x + t * dx - m[0], a.y + t * dy - m[1]);
      } else {
        const c = P(e.center);
        const r = e.type === "circle" ? e.radius : Math.hypot(P(e.start).x - c.x, P(e.start).y - c.y);
        d = Math.abs(Math.hypot(m[0] - c.x, m[1] - c.y) - r);
      }
      if (d < bd) { bd = d; best = e.id; }
    }
    return best;
  };

  /** A point at m: an existing one when the click is on it, otherwise a new one. */
  const pointAt = (sk: Sketch, m: Pt): [Sketch, string] => {
    const hit = hitPoint(m);
    if (hit) return [sk, hit];
    const id = nextId("p", sk);
    return [{ ...sk, points: [...sk.points, { id, x: Math.round(m[0] * 10) / 10, y: Math.round(m[1] * 10) / 10 }] }, id];
  };
  const addLine = (sk: Sketch, a: string, b: string): Sketch => {
    const id = nextId("l", sk);
    const pa = sk.points.find((p) => p.id === a)!, pb = sk.points.find((p) => p.id === b)!;
    const ang = Math.abs(Math.atan2(pb.y - pa.y, pb.x - pa.x) * 180 / Math.PI);
    const constraints = [...sk.constraints];
    // Smart pick: nearly horizontal or vertical lines get the constraint as drawn.
    if (Math.min(ang, 180 - ang) < 4) constraints.push({ kind: "horizontal", refs: [id] });
    else if (Math.abs(ang - 90) < 4) constraints.push({ kind: "vertical", refs: [id] });
    return { ...sk, entities: [...sk.entities, { type: "line", id, a, b }], constraints };
  };

  const finishChain = () => { setClicks([]); setChainStart(null); };

  const onDown = (ev: React.PointerEvent<SVGSVGElement>) => {
    svg.current?.focus({ preventScroll: true }); // focusing must not scroll the panel mid-drawing
    const m = toModel(ev);
    if (tool === "select") {
      const hp = hitPoint(m), he = hp ? null : hitEntity(m);
      const id = hp ?? he;
      if (!id) { setSel([]); return; }
      setSel((s) => (ev.shiftKey ? (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]) : s.includes(id) ? s : [id]));
      if (hp && !P(hp).fixed) { setDrag(hp); (ev.target as Element).setPointerCapture?.(ev.pointerId); }
      return;
    }
    let sk = doc, id: string;
    if (tool === "line") {
      [sk, id] = pointAt(sk, m);
      if (clicks.length && clicks[0] !== id) {
        sk = addLine(sk, clicks[0], id);
        if (id === chainStart) { change(sk); finishChain(); return; }
      }
      if (!chainStart) setChainStart(id);
      setClicks([id]);
      change(sk);
      return;
    }
    if (tool === "rect") {
      if (!clicks.length) { [sk, id] = pointAt(sk, m); setClicks([id]); setDoc(sk); return; }
      const a = sk.points.find((p) => p.id === clicks[0])!;
      const ids: string[] = [a.id];
      for (const [x, y] of [[m[0], a.y], [m[0], m[1]], [a.x, m[1]]] as Pt[]) {
        const pid = nextId("p", sk);
        sk = { ...sk, points: [...sk.points, { id: pid, x, y }] };
        ids.push(pid);
      }
      const lid: string[] = [];
      for (let i = 0; i < 4; i++) {
        const l = nextId("l", sk);
        lid.push(l);
        sk = { ...sk, entities: [...sk.entities, { type: "line", id: l, a: ids[i], b: ids[(i + 1) % 4] }] };
      }
      sk = { ...sk, constraints: [...sk.constraints, { kind: "horizontal", refs: [lid[0]] }, { kind: "vertical", refs: [lid[1]] },
        { kind: "horizontal", refs: [lid[2]] }, { kind: "vertical", refs: [lid[3]] }] };
      setClicks([]);
      change(sk);
      return;
    }
    if (tool === "circle") {
      if (!clicks.length) { [sk, id] = pointAt(sk, m); setClicks([id]); setDoc(sk); return; }
      const c = sk.points.find((p) => p.id === clicks[0])!;
      const r = Math.max(Math.hypot(m[0] - c.x, m[1] - c.y), 1);
      sk = { ...sk, entities: [...sk.entities, { type: "circle", id: nextId("c", sk), center: c.id, radius: Math.round(r * 10) / 10 }] };
      setClicks([]);
      change(sk);
      return;
    }
    if (tool === "arc") {
      if (clicks.length < 2) { [sk, id] = pointAt(sk, m); setClicks([...clicks, id]); setDoc(sk); return; }
      const c = sk.points.find((p) => p.id === clicks[0])!, s = sk.points.find((p) => p.id === clicks[1])!;
      const r = Math.hypot(s.x - c.x, s.y - c.y), a = Math.atan2(m[1] - c.y, m[0] - c.x);
      let end: string;
      const hit = hitPoint(m);
      if (hit && hit !== s.id && hit !== c.id) end = hit;
      else {
        end = nextId("p", sk);
        sk = { ...sk, points: [...sk.points, { id: end, x: c.x + r * Math.cos(a), y: c.y + r * Math.sin(a) }] };
      }
      sk = { ...sk, entities: [...sk.entities, { type: "arc", id: nextId("a", sk), center: c.id, start: s.id, end }] };
      setClicks([]);
      change(sk);
    }
  };

  const onMove = (ev: React.PointerEvent<SVGSVGElement>) => {
    const m = toModel(ev);
    setCursor(m);
    if (drag) {
      const moved = { ...doc, points: doc.points.map((p) => (p.id === drag ? { ...p, x: m[0], y: m[1] } : p)) };
      setDoc(moved);
      setDirty(true);
      void solve(moved, { point: drag, x: m[0], y: m[1] });
    }
  };
  const onUp = () => { if (drag) setDrag(null); };

  const remove = (ids: string[]) => {
    const gone = new Set(ids);
    let entities = doc.entities.filter((e) => !gone.has(e.id) && !entityPoints(e).some((p) => gone.has(p)));
    const used = new Set(entities.flatMap(entityPoints));
    const points = doc.points.filter((p) => !gone.has(p.id) && (used.has(p.id) || p.fixed));
    const alive = new Set([...points.map((p) => p.id), ...entities.map((e) => e.id)]);
    entities = entities.filter((e) => entityPoints(e).every((p) => alive.has(p)));
    const keep: number[] = [];
    doc.constraints.forEach((c, i) => { if (c.refs.every((r) => alive.has(r))) keep.push(i); });
    change({ points, entities, constraints: keep.map((i) => doc.constraints[i]) }, remap(keep));
    setSel([]);
  };
  /** Bindings after keeping only the constraints at ``keep`` (old indices, in order). */
  const remap = (keep: number[]) => {
    const out: Record<string, string> = {};
    for (const [path, expr] of Object.entries(binds)) {
      const m = /^sketch\.constraints\.(\d+)\.value$/.exec(path);
      if (!m) { out[path] = expr; continue; }
      const j = keep.indexOf(Number(m[1]));
      if (j >= 0) out[BIND(j)] = expr;
    }
    return out;
  };
  const addConstraint = (c: SketchConstraint) => { change({ ...doc, constraints: [...doc.constraints, c] }); };
  const setValue = (i: number, text: string) => {
    const t = text.trim();
    const num = Number(t);
    const nextBinds = { ...binds };
    if (t !== "" && Number.isFinite(num)) {
      delete nextBinds[BIND(i)];
      change({ ...doc, constraints: doc.constraints.map((c, j) => (j === i ? { ...c, value: num } : c)) }, nextBinds);
    } else if (t) {
      nextBinds[BIND(i)] = t; // a formula of the part's parameters, evaluated at the build
      change(doc, nextBinds);
    }
  };

  const onKey = (ev: React.KeyboardEvent) => {
    if (ev.key === "Escape") { finishChain(); setSel([]); }
    if ((ev.key === "Delete" || ev.key === "Backspace") && sel.length) { ev.preventDefault(); remove(sel); }
  };

  const options = useMemo(() => available(doc, sel), [doc, sel]);
  const selPoint = sel.length === 1 ? doc.points.find((p) => p.id === sel[0]) : undefined;
  const selEntities = sel.filter((id) => doc.entities.some((e) => e.id === id));
  const fixedE = new Set(status?.fixed_entities ?? []), fixedP = new Set(status?.fixed_points ?? []);
  const conflictRefs = new Set((status?.conflicting ?? []).flatMap((i) => doc.constraints[i]?.refs ?? []));
  const cls = (id: string, construction?: boolean) => [
    "sk-geo", fixedE.has(id) ? "full" : "", construction ? "construction" : "", sel.includes(id) ? "selected" : "",
    conflictRefs.has(id) ? "conflict" : "",
  ].join(" ");

  // dimension labels
  const labelsSvg = doc.constraints.map((c, i) => {
    if (!DIMENSIONS.has(c.kind)) return null;
    let at: Pt | null = null;
    const ent = doc.entities.find((e) => e.id === c.refs[0]);
    if (["distance", "hdistance", "vdistance"].includes(c.kind)) {
      const a = P(c.refs[0]), b = P(c.refs[1]);
      at = [(a.x + b.x) / 2, (a.y + b.y) / 2];
    } else if (c.kind === "length" && ent?.type === "line") {
      const a = P(ent.a), b = P(ent.b), len = Math.hypot(b.x - a.x, b.y - a.y) || 1;
      at = [(a.x + b.x) / 2 - ((b.y - a.y) / len) * 14 * px, (a.y + b.y) / 2 + ((b.x - a.x) / len) * 14 * px];
    } else if (ent && ent.type !== "line") {
      const ctr = P(ent.center);
      const r = ent.type === "circle" ? ent.radius : Math.hypot(P(ent.start).x - ctr.x, P(ent.start).y - ctr.y);
      at = [ctr.x + r * 0.5, ctr.y + r * 0.5];
    } else if (c.kind === "angle") {
      const [l1, l2] = c.refs.map((id) => doc.entities.find((e) => e.id === id)) as Extract<SketchEntity, { type: "line" }>[];
      const m1 = [(P(l1.a).x + P(l1.b).x) / 2, (P(l1.a).y + P(l1.b).y) / 2], m2 = [(P(l2.a).x + P(l2.b).x) / 2, (P(l2.a).y + P(l2.b).y) / 2];
      at = [(m1[0] + m2[0]) / 2, (m1[1] + m2[1]) / 2];
    }
    if (!at) return null;
    const bound = binds[BIND(i)];
    const unit = c.kind === "angle" ? "°" : "";
    const text = `${c.kind === "diameter" ? "⌀" : c.kind === "radius" ? "R" : ""}${bound ? "ƒ " : ""}${Number(c.value ?? 0).toFixed(1).replace(/\.0$/, "")}${unit}`;
    const bad = status?.conflicting.includes(i);
    return (
      <text key={`d${i}`} x={at[0]} y={-at[1]} className={`sk-dim${bad ? " conflict" : ""}`} fontSize={11 * px}
        textAnchor="middle" dominantBaseline="middle">{text}</text>
    );
  });

  const last = clicks.length ? doc.points.find((p) => p.id === clicks[clicks.length - 1]) : undefined;
  const arcPath = (e: Extract<SketchEntity, { type: "arc" }>) => {
    const c = P(e.center), s = P(e.start), t = P(e.end);
    const r = Math.hypot(s.x - c.x, s.y - c.y);
    let span = Math.atan2(t.y - c.y, t.x - c.x) - Math.atan2(s.y - c.y, s.x - c.x);
    if (span <= 0) span += 2 * Math.PI;
    return `M ${s.x} ${-s.y} A ${r} ${r} 0 ${span > Math.PI ? 1 : 0} 0 ${t.x} ${-t.y}`;
  };
  const statusText = !status ? "Solving…" : !status.ok
    ? `Conflict: constraint${status.conflicting.length > 1 ? "s" : ""} ${status.conflicting.map((i) => i + 1).join(", ")} cannot all be met`
    : status.dof === 0 ? "Fully constrained" : `${status.dof} degree${status.dof > 1 ? "s" : ""} of freedom left`;

  return (
    <div className="csketch">
      <div className="csketch-tools">
        {TOOLS.map((t) => (
          <button key={t.id} className={tool === t.id ? "active" : ""} title={t.hint}
            onClick={() => { setTool(t.id); finishChain(); }}>{t.label}</button>
        ))}
        <span className="sep" />
        <button title="Fit the view" onClick={() => setView(fit(doc))}>Fit</button>
        <span className={`csketch-status ${!status ? "" : !status.ok ? "conflict" : status.dof === 0 ? "full" : ""}`}>
          {statusText}{status && status.redundant > 0 && status.ok ? ` · ${status.redundant} redundant` : ""}
        </span>
      </div>
      <svg ref={svg} tabIndex={0} onKeyDown={onKey} className={`csketch-canvas tool-${tool}`}
        viewBox={`${view.cx - w / 2} ${-view.cy - h / 2} ${w} ${h}`} preserveAspectRatio="xMidYMid meet"
        onPointerDown={onDown} onPointerMove={onMove} onPointerUp={onUp} onPointerLeave={() => { onUp(); setCursor(null); }}
        onDoubleClick={() => tool === "line" && finishChain()}
        onWheel={(ev) => { const f = ev.deltaY > 0 ? 1.15 : 1 / 1.15; setView((v) => ({ ...v, span: v.span * f })); }}>
        <line x1={view.cx - w} x2={view.cx + w} y1={0} y2={0} className="sk-axis" />
        <line y1={-view.cy - h} y2={-view.cy + h} x1={0} x2={0} className={axis ? "sk-axis revolve" : "sk-axis"} />
        <text x={view.cx + w / 2 - 6 * px} y={-4 * px} fontSize={10 * px} textAnchor="end" className="sk-axis-label">{labels[0]}</text>
        <text x={4 * px} y={-view.cy - h / 2 + 12 * px} fontSize={10 * px} className="sk-axis-label">{labels[1]}</text>
        {doc.entities.map((e) => {
          if (e.type === "line") {
            const a = P(e.a), b = P(e.b);
            return <line key={e.id} x1={a.x} y1={-a.y} x2={b.x} y2={-b.y} className={cls(e.id, e.construction)} />;
          }
          if (e.type === "circle") {
            const c = P(e.center);
            return <circle key={e.id} cx={c.x} cy={-c.y} r={e.radius} className={cls(e.id, e.construction)} />;
          }
          return <path key={e.id} d={arcPath(e)} className={cls(e.id, e.construction)} />;
        })}
        {last && cursor && tool === "line" && <line x1={last.x} y1={-last.y} x2={cursor[0]} y2={-cursor[1]} className="sk-preview" />}
        {last && cursor && tool === "rect" && (
          <rect x={Math.min(last.x, cursor[0])} y={-Math.max(last.y, cursor[1])} width={Math.abs(cursor[0] - last.x)}
            height={Math.abs(cursor[1] - last.y)} className="sk-preview" />
        )}
        {clicks.length > 0 && cursor && (tool === "circle" || tool === "arc") && (() => {
          const c = P(clicks[0]);
          const ref = tool === "arc" && clicks[1] ? P(clicks[1]) : { x: cursor[0], y: cursor[1] };
          return <circle cx={c.x} cy={-c.y} r={Math.hypot(ref.x - c.x, ref.y - c.y)} className="sk-preview" />;
        })()}
        {labelsSvg}
        {doc.points.map((p) => {
          const s = (p.fixed ? 4.5 : 3.5) * px;
          const c = ["sk-pt", fixedP.has(p.id) ? "full" : "", sel.includes(p.id) ? "selected" : "", conflictRefs.has(p.id) ? "conflict" : ""].join(" ");
          return p.fixed
            ? <rect key={p.id} x={p.x - s} y={-p.y - s} width={2 * s} height={2 * s} className={c}><title>{`${p.id} (anchored)`}</title></rect>
            : <circle key={p.id} cx={p.x} cy={-p.y} r={s} className={c}><title>{`${p.id}: ${p.x.toFixed(2)}, ${p.y.toFixed(2)}`}</title></circle>;
        })}
      </svg>
      <div className="csketch-side">
        <div className="csketch-constrain">
          <span className="hint">{sel.length ? `Selected: ${sel.join(", ")}` : "Select geometry to constrain it."}</span>
          {options.map((o) => (
            <button key={o.kind + o.refs.join()} onClick={() => addConstraint({ kind: o.kind, refs: o.refs, value: o.value === undefined ? null : Math.round(o.value * 100) / 100 })}>
              {KIND_LABEL[o.kind]}{o.value !== undefined ? ` ${o.value.toFixed(1)}` : ""}
            </button>
          ))}
          {selPoint && (
            <button onClick={() => change({ ...doc, points: doc.points.map((p) => (p.id === selPoint.id ? { ...p, fixed: !p.fixed } : p)) })}>
              {selPoint.fixed ? "Release anchor" : "Anchor (fix)"}
            </button>
          )}
          {selEntities.length > 0 && (
            <button onClick={() => change({ ...doc, entities: doc.entities.map((e) => (sel.includes(e.id) ? { ...e, construction: !e.construction } : e)) })}>
              Construction on/off
            </button>
          )}
          {sel.length > 0 && <button onClick={() => remove(sel)}>Delete</button>}
        </div>
        <table className="csketch-list">
          <tbody>
            {doc.constraints.map((c, i) => {
              const bad = status?.conflicting.includes(i);
              const bound = binds[BIND(i)];
              return (
                <tr key={i} className={bad ? "conflict" : ""} onClick={() => setSel(c.refs)}>
                  <td>{i + 1}</td>
                  <td>{KIND_LABEL[c.kind] ?? c.kind}</td>
                  <td className="refs">{c.refs.join(" · ")}</td>
                  <td>
                    {DIMENSIONS.has(c.kind) && (
                      <input key={`${i}-${c.value}-${bound}`} defaultValue={bound ?? String(c.value ?? "")} size={9}
                        title="A number, or a formula of the part's parameters"
                        onClick={(e) => e.stopPropagation()}
                        onBlur={(e) => setValue(i, e.target.value)}
                        onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }} />
                    )}
                  </td>
                  <td><button title="Delete the constraint" onClick={(e) => {
                    e.stopPropagation();
                    const keep = doc.constraints.map((_, j) => j).filter((j) => j !== i);
                    change({ ...doc, constraints: keep.map((j) => doc.constraints[j]) }, remap(keep));
                  }}>×</button></td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="csketch-apply">
          <button disabled={!dirty || !status?.ok} onClick={() => { onApply(doc, binds); setDirty(false); }}>Apply to the part</button>
          <button disabled={!dirty} onClick={() => { setDoc(sketch); setBinds(bindings); setDirty(false); void solve(sketch); }}>Revert</button>
          {error && <span className="error">{error}</span>}
        </div>
        <SolverConsole status={status} />
      </div>
    </div>
  );
}
