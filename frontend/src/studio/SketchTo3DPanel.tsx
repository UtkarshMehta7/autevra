import { type ReactElement, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "../api/client";

/** Sketch to 3D (every module): draw rough strokes with a mouse, pen or finger in one or
 * more views; Autevra fits lines, arcs and circles, joins the ends, infers horizontal,
 * vertical, parallel, perpendicular, equal, tangent and concentric, solves the sketch, and
 * builds a solid by extruding it, revolving it, or intersecting the front, top and side
 * views. The result is an ordinary Part Design part with editable constraint sketches. */

type View = "top" | "front" | "side";
type Pt = [number, number];
type Mode = "extrude" | "revolve" | "views";
interface Cleaned { sketch: { points: { id: string; x: number; y: number }[]; entities: { type: string; id: string; a?: string; b?: string; center?: string; start?: string; end?: string; radius?: number }[]; constraints: { kind: string }[] }; notes: string[]; closed: boolean; counts: Record<string, number> }

const W = 640, H = 400;
const VIEW_HINT: Record<View, string> = {
  top: "Top view (looking down): X right, Y up the page",
  front: "Front view: X right, Z up the page",
  side: "Side view (from the right): Y right, Z up the page",
};

export function SketchTo3DPanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [view, setView] = useState<View>("top");
  const [strokes, setStrokes] = useState<Record<View, Pt[][]>>({ top: [], front: [], side: [] });
  const [drawing, setDrawing] = useState<Pt[] | null>(null);
  const [width, setWidth] = useState(200); // mm across the canvas
  const [mode, setMode] = useState<Mode>("extrude");
  const [depth, setDepth] = useState(20);
  const [name, setName] = useState("Sketched part");
  const [cleaned, setCleaned] = useState<Partial<Record<View, Cleaned>>>({});
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const svg = useRef<SVGSVGElement | null>(null);
  const k = width / W; // mm per canvas unit

  const toMm = useCallback((e: React.PointerEvent): Pt => {
    const r = svg.current!.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width) * W, y = ((e.clientY - r.top) / r.height) * H;
    return [+(x * k).toFixed(2), +((H - y) * k).toFixed(2)];
  }, [k]);
  const toPx = (p: Pt) => `${(p[0] / k).toFixed(1)},${(H - p[1] / k).toFixed(1)}`;

  const clean = useCallback(async (v: View, list: Pt[][]) => {
    if (!list.length) { setCleaned((c) => ({ ...c, [v]: undefined })); return; }
    try {
      const out = await api.freehandClean({ strokes: list }) as Cleaned;
      setCleaned((c) => ({ ...c, [v]: out }));
    } catch (e) { setNote(e instanceof Error ? e.message : String(e)); }
  }, []);
  useEffect(() => { const t = setTimeout(() => clean(view, strokes[view]), 250); return () => clearTimeout(t); }, [strokes, view, clean]);

  // The stroke being drawn lives in a ref: pointer events can arrive faster than React
  // re-renders, and every point must be kept.
  const live = useRef<Pt[] | null>(null);
  const down = (e: React.PointerEvent) => {
    try { (e.target as Element).setPointerCapture?.(e.pointerId); } catch { /* some pointers cannot be captured */ }
    live.current = [toMm(e)];
    setDrawing([...live.current]);
  };
  const move = (e: React.PointerEvent) => {
    if (!live.current) return;
    live.current.push(toMm(e));
    setDrawing([...live.current]);
  };
  const up = () => {
    const stroke = live.current;
    live.current = null;
    if (stroke && stroke.length > 2) setStrokes((s) => ({ ...s, [view]: [...s[view], stroke] }));
    setDrawing(null);
  };

  const sk = cleaned[view]?.sketch;
  const geometry = useMemo(() => {
    if (!sk) return null;
    const p = Object.fromEntries(sk.points.map((q) => [q.id, q]));
    const out: ReactElement[] = [];
    for (const e of sk.entities) {
      if (e.type === "line" && e.a && e.b) {
        out.push(<line key={e.id} x1={p[e.a].x / k} y1={H - p[e.a].y / k} x2={p[e.b].x / k} y2={H - p[e.b].y / k} className="fh-geo" />);
      } else if (e.type === "circle" && e.center) {
        out.push(<circle key={e.id} cx={p[e.center].x / k} cy={H - p[e.center].y / k} r={(e.radius ?? 0) / k} className="fh-geo" />);
      } else if (e.type === "arc" && e.center && e.start && e.end) {
        const c = p[e.center], s = p[e.start], t = p[e.end];
        const r = Math.hypot(s.x - c.x, s.y - c.y) / k;
        let a0 = Math.atan2(s.y - c.y, s.x - c.x), a1 = Math.atan2(t.y - c.y, t.x - c.x);
        while (a1 <= a0) a1 += 2 * Math.PI;
        const large = a1 - a0 > Math.PI ? 1 : 0;
        // counter-clockwise in model space is clockwise on screen (y flipped): sweep flag 0
        out.push(<path key={e.id} d={`M${s.x / k},${H - s.y / k} A${r},${r} 0 ${large} 0 ${t.x / k},${H - t.y / k}`} className="fh-geo" />);
      }
    }
    for (const q of sk.points) if (!q.id.startsWith("c")) out.push(<circle key={`v${q.id}`} cx={q.x / k} cy={H - q.y / k} r={2.5} className="fh-vertex" />);
    return out;
  }, [sk, k]);

  const views = (Object.keys(strokes) as View[]).filter((v) => strokes[v].length);
  const create = async () => {
    setBusy(true); setNote(null);
    try {
      const use: Partial<Record<View, Pt[][]>> = mode === "views" ? Object.fromEntries(views.map((v) => [v, strokes[v]])) : { [view]: strokes[view] };
      const part = await api.freehandPart(projectId, { views: use, mode, depth, name });
      setNote(`Created “${part.document.name}” (${part.volume != null ? `${(part.volume / 1000).toFixed(1)} cm³` : "no solid"}). Open Part Design to edit its sketches, add holes, fillets, patterns…`);
      onModelChanged();
    } catch (e) { setNote(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };

  const c = cleaned[view];
  return (
    <section className="elements-panel freehand-panel">
      <div className="el-body">
        <div className="el-inputs">
          <div className="el-tabs">
            {(["top", "front", "side"] as View[]).map((v) => (
              <button key={v} className={v === view ? "active" : ""} onClick={() => setView(v)}>{v[0].toUpperCase() + v.slice(1)}{strokes[v].length ? ` (${strokes[v].length})` : ""}</button>
            ))}
          </div>
          <p className="small muted">{VIEW_HINT[view]}. Draw roughly: corners, straight runs, arcs and circles are recognised and tidied.</p>
          <label className="el-field">drawing width<span><input type="number" value={width} onChange={(e) => setWidth(Math.max(1, Number(e.target.value) || 1))} /><em>mm</em></span></label>
          <label className="el-field">make
            <select value={mode} onChange={(e) => setMode(e.target.value as Mode)}>
              <option value="extrude">extrude this view</option>
              <option value="revolve">revolve this view (about its left edge)</option>
              <option value="views">combine the drawn views (front · top · side)</option>
            </select>
          </label>
          {mode === "extrude" && <label className="el-field">thickness<span><input type="number" value={depth} onChange={(e) => setDepth(Math.max(0.1, Number(e.target.value) || 1))} /><em>mm</em></span></label>}
          <label className="el-field wide">name<input value={name} onChange={(e) => setName(e.target.value)} /></label>
          <div className="row wrap">
            <button disabled={!strokes[view].length} onClick={() => setStrokes((s) => ({ ...s, [view]: s[view].slice(0, -1) }))}>Undo stroke</button>
            <button disabled={!strokes[view].length} onClick={() => setStrokes((s) => ({ ...s, [view]: [] }))}>Clear view</button>
          </div>
          <button className="primary" disabled={busy || !views.length || (mode === "views" ? views.length < 2 : !strokes[view].length)} onClick={create}>
            {busy ? "Building…" : mode === "views" ? `Create 3D part from ${views.length} views` : "Create 3D part"}
          </button>
          {c && <ul className="small cam-notes">
            <li>{c.counts.line} line(s), {c.counts.arc} arc(s), {c.counts.circle} circle(s), {c.sketch.constraints.length} constraint(s)</li>
            {c.notes.map((n) => <li key={n}>{n}</li>)}
            <li className={c.closed ? "good" : "bad"}>{c.closed ? "Closed profile: ready for 3D" : "Not closed yet"}</li>
          </ul>}
          {note && <p className="small">{note}</p>}
        </div>
        <div className="el-out">
          <svg ref={svg} viewBox={`0 0 ${W} ${H}`} className="fh-canvas" onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerLeave={up}
            role="img" aria-label={`Drawing area, ${view} view`}>
            {Array.from({ length: 33 }, (_, i) => <line key={`gx${i}`} x1={i * 20} y1={0} x2={i * 20} y2={H} className="fh-grid" />)}
            {Array.from({ length: 21 }, (_, i) => <line key={`gy${i}`} x1={0} y1={i * 20} x2={W} y2={i * 20} className="fh-grid" />)}
            {strokes[view].map((s, i) => <polyline key={i} points={s.map(toPx).join(" ")} className="fh-stroke" />)}
            {drawing && <polyline points={drawing.map(toPx).join(" ")} className="fh-stroke live" />}
            {geometry}
            <text x={8} y={H - 8} className="lbl muted">{(20 * k).toFixed(1)} mm grid</text>
          </svg>
          <p className="small muted">Grey: your strokes. Blue: the cleaned, constrained geometry that becomes the part.</p>
        </div>
      </div>
    </section>
  );
}
