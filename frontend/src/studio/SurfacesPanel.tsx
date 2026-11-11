import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "../api/client";
import type { ContinuityReport, NurbsEvaluation, NurbsSurface } from "../api/types";
import { type SurfaceColour, SurfaceView } from "./SurfaceView";

/** Surface laboratory: NURBS surfaces with their mathematics on show. Drag a control point
 * (or edit its coordinates and weight) and watch the surface deform only over the point's
 * local support; see the basis functions and knot vectors behind it; insert knots; and
 * join a second patch at G0, G1 or G2 and measure the continuity. Evaluation and analysis
 * run in the backend (geometry/nurbs.py, geometry/continuity.py), which is tested against
 * Open CASCADE. */

type Sel = { patch: number; i: number; j: number };

const PRESETS: Record<string, () => NurbsSurface> = {
  "Wave patch (bicubic)": () => ({
    degree_u: 3, degree_v: 3,
    control: grid(6, 5, (i, j) => [i * 40, j * 40, 18 * Math.sin(i * 1.1) * Math.cos(j * 0.8)]),
  }),
  "Saddle (biquadratic)": () => ({
    degree_u: 2, degree_v: 2,
    control: grid(4, 4, (i, j) => [i * 50, j * 50, 12 * ((i - 1.5) ** 2 - (j - 1.5) ** 2)]),
  }),
  "Quarter cylinder (rational, exact)": () => {
    const r = 80, s = Math.SQRT1_2;
    const arc: [number, number][] = [[r, 0], [r, r], [0, r]];
    return {
      degree_u: 2, degree_v: 1,
      control: arc.map(([x, y]) => [[x, y, 0], [x, y, 120]] as [number, number, number][]),
      weights: [[1, 1], [s, s], [1, 1]],
    };
  },
};

function grid(nu: number, nv: number, f: (i: number, j: number) => [number, number, number]) {
  return Array.from({ length: nu }, (_, i) => Array.from({ length: nv }, (_, j) => f(i, j)));
}

function useEvaluation(surface: NurbsSurface | null, selected: [number, number] | null) {
  const [out, setOut] = useState<NurbsEvaluation | null>(null);
  const [error, setError] = useState<string | null>(null);
  const busy = useRef(false);
  const queued = useRef<{ s: NurbsSurface; sel: [number, number] | null } | null>(null);
  const run = useCallback(async (s: NurbsSurface, sel: [number, number] | null) => {
    if (busy.current) { queued.current = { s, sel }; return; }
    busy.current = true;
    try {
      setOut(await api.evaluateSurface(s, 33, sel));
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      busy.current = false;
      const next = queued.current;
      queued.current = null;
      if (next) void run(next.s, next.sel);
    }
  }, []);
  useEffect(() => { if (surface) void run(surface, selected); }, [surface, selected, run]);
  return { out, error };
}

export function SurfacesPanel() {
  const [preset, setPreset] = useState("Wave patch (bicubic)");
  const [a, setA] = useState<NurbsSurface>(() => PRESETS["Wave patch (bicubic)"]());
  const [b, setB] = useState<NurbsSurface | null>(null);
  const [sel, setSel] = useState<Sel | null>({ patch: 0, i: 2, j: 2 });
  const [colour, setColour] = useState<SurfaceColour>("shaded");
  const [lattice, setLattice] = useState(true);
  const [target, setTarget] = useState<"G0" | "G1" | "G2">("G2");
  const [bend, setBend] = useState(20);
  const [combScale, setCombScale] = useState(3000);
  const [report, setReport] = useState<ContinuityReport | null>(null);
  const [knot, setKnot] = useState({ direction: "u" as "u" | "v", t: 0.5 });
  const [note, setNote] = useState<string | null>(null);

  const selA = sel?.patch === 0 ? ([sel.i, sel.j] as [number, number]) : null;
  const selB = sel?.patch === 1 ? ([sel.i, sel.j] as [number, number]) : null;
  const evA = useEvaluation(a, selA);
  const evB = useEvaluation(b, selB);

  useEffect(() => {
    if (!b) { setReport(null); return; }
    let live = true;
    api.surfaceContinuity(a, b, combScale).then((r) => live && setReport(r)).catch(() => live && setReport(null));
    return () => { live = false; };
  }, [a, b, combScale]);

  const current = sel?.patch === 1 ? b : a;
  const setCurrent = (s: NurbsSurface) => (sel?.patch === 1 ? setB(s) : setA(s));
  const ev = sel?.patch === 1 ? evB.out : evA.out;
  const full = ev?.surface;

  const movePoint = (s: Sel, to: [number, number, number]) => {
    const src = s.patch === 1 ? b : a;
    if (!src) return;
    const control = src.control.map((row, i) => row.map((p, j) => (i === s.i && j === s.j ? to : p)));
    (s.patch === 1 ? setB : setA)({ ...src, control });
  };
  const setWeight = (w: number) => {
    if (!sel || !current || !full) return;
    const weights = full.weights.map((row, i) => row.map((x, j) => (i === sel.i && j === sel.j ? w : x)));
    setCurrent({ ...current, weights });
  };
  const loadPreset = (name: string) => {
    setPreset(name);
    setA(PRESETS[name]());
    setB(null);
    setSel({ patch: 0, i: 1, j: 1 });
    setNote(null);
  };
  const insert = async () => {
    if (!current) return;
    try {
      const out = await api.insertKnot(full ?? current, knot.direction, knot.t);
      setCurrent(out.surface);
      setNote(`Inserted ${knot.direction} = ${knot.t}: one more ${knot.direction === "u" ? "row" : "column"} of control points; the shape moved by at most ${out.max_shape_change.toExponential(1)} mm (Boehm's algorithm keeps it).`);
    } catch (e) {
      setNote(e instanceof Error ? e.message : String(e));
    }
  };
  const buildJoin = async () => {
    try {
      const out = await api.joinSurface(evA.out?.surface ?? a, target, bend);
      setB(out.surface);
      setNote(`Patch B built to ${target} across A's u = 1 edge: its first ${target === "G0" ? 1 : target === "G1" ? 2 : 3} control row(s) are solved from A's derivatives there.`);
    } catch (e) {
      setNote(e instanceof Error ? e.message : String(e));
    }
  };

  const patches = useMemo(() => [
    ...(evA.out ? [{ evaluation: evA.out, editable: true, tint: 0x8fa3b8 }] : []),
    ...(b && evB.out ? [{ evaluation: evB.out, editable: true, tint: 0x9fb89a }] : []),
  ], [evA.out, evB.out, b]);

  const point = sel && full ? full.control[sel.i]?.[sel.j] : undefined;
  const weight = sel && full ? full.weights[sel.i]?.[sel.j] : undefined;

  return (
    <div className="bench wide surfaces-lab">
      <div className="lab-view">
        <SurfaceView patches={patches} colour={colour} selected={sel} onSelect={setSel} lattice={lattice}
          onDrag={(s, to) => movePoint(s, to)} combs={report?.combs} />
        <div className="lab-toolbar">
          {(["shaded", "gaussian", "mean"] as SurfaceColour[]).map((c) => (
            <button key={c} className={colour === c ? "on" : ""} onClick={() => setColour(c)}
              title={c === "shaded" ? "Shaded; the selected point's local support in amber"
                : c === "gaussian" ? "Gaussian curvature K = (LN − M²)/(EG − F²): blue < 0 (saddle), red > 0 (dome)"
                : "Mean curvature H = (EN − 2FM + GL)/2(EG − F²)"}>
              {c === "shaded" ? "Support" : c === "gaussian" ? "Gaussian K" : "Mean H"}
            </button>
          ))}
          <label><input type="checkbox" checked={lattice} onChange={(e) => setLattice(e.target.checked)} /> lattice</label>
        </div>
        {(evA.error || evB.error) && <div className="error">{evA.error ?? evB.error}</div>}
      </div>
      <div className="lab-side">
        <div className="row">
          <select value={preset} onChange={(e) => loadPreset(e.target.value)}>
            {Object.keys(PRESETS).map((k) => <option key={k}>{k}</option>)}
          </select>
          {(["u", "v"] as const).map((d) => (
            <label key={d} title={`Degree in ${d}`}>{d === "u" ? "p" : "q"}
              <select value={d === "u" ? a.degree_u : a.degree_v} onChange={(e) => {
                const deg = Number(e.target.value);
                setA({ ...a, ...(d === "u" ? { degree_u: deg, knots_u: undefined } : { degree_v: deg, knots_v: undefined }) });
              }}>
                {[1, 2, 3, 4, 5].filter((k) => k < (d === "u" ? a.control.length : a.control[0].length))
                  .map((k) => <option key={k}>{k}</option>)}
              </select>
            </label>
          ))}
        </div>
        <div className="math">
          <div>S(u,v) = ΣᵢΣⱼ Nᵢ,ₚ(u) Nⱼ,q(v) wᵢⱼ Pᵢⱼ / ΣᵢΣⱼ Nᵢ,ₚ(u) Nⱼ,q(v) wᵢⱼ</div>
          {full && <div>degree ({full.degree_u}, {full.degree_v}) · {full.control.length} × {full.control[0].length} control points</div>}
          {full && <div>U = [{full.knots_u.map((k) => +k.toFixed(3)).join(", ")}]</div>}
          {full && <div>V = [{full.knots_v.map((k) => +k.toFixed(3)).join(", ")}]</div>}
          {sel && point && ev?.support && (
            <>
              <div className="sel-head">{sel.patch === 1 ? "B" : "A"} P{sel.i},{sel.j} = ({point.map((x) => x.toFixed(1)).join(", ")}) · w = {weight?.toFixed(3)}</div>
              <div>moves S only on u ∈ [{ev.support.u[0].toFixed(3)}, {ev.support.u[1].toFixed(3)}) × v ∈ [{ev.support.v[0].toFixed(3)}, {ev.support.v[1].toFixed(3)})</div>
              <div className="muted">(the support of N{sel.i},{full?.degree_u}(u) · N{sel.j},{full?.degree_v}(v))</div>
            </>
          )}
        </div>
        {sel && point && (
          <div className="row point-edit">
            {(["x", "y", "z"] as const).map((axis, k) => (
              <label key={axis}>{axis}
                <input type="number" step={1} value={+point[k].toFixed(2)} onChange={(e) => {
                  const p = [...point] as [number, number, number];
                  p[k] = Number(e.target.value);
                  movePoint(sel, p);
                }} />
              </label>
            ))}
            <label title="Weight: pulls the surface towards the point (rational)">w
              <input type="range" min={0.1} max={5} step={0.05} value={weight ?? 1} onChange={(e) => setWeight(Number(e.target.value))} />
            </label>
          </div>
        )}
        {ev && (
          <div className="basis-row">
            <div className="basis-col">
              <BasisPlot title="Nᵢ,ₚ(u)" table={ev.basis_u} knots={ev.surface.knots_u} highlight={sel?.i} />
              <BasisPlot title="Nⱼ,q(v)" table={ev.basis_v} knots={ev.surface.knots_v} highlight={sel?.j} />
            </div>
            <ParamSpace ev={ev} />
          </div>
        )}
        <div className="row">
          <strong>Knot insertion</strong>
          <select value={knot.direction} onChange={(e) => setKnot({ ...knot, direction: e.target.value as "u" | "v" })}>
            <option>u</option><option>v</option>
          </select>
          <input type="number" min={0.01} max={0.99} step={0.05} value={knot.t} style={{ width: 64 }}
            onChange={(e) => setKnot({ ...knot, t: Number(e.target.value) })} />
          <button onClick={insert}>Insert</button>
        </div>
        <div className="row">
          <strong>Continuity</strong>
          <select value={target} onChange={(e) => setTarget(e.target.value as "G0" | "G1" | "G2")}>
            <option>G0</option><option>G1</option><option>G2</option>
          </select>
          <label title="Lift B's free rows">bend <input type="number" value={bend} style={{ width: 56 }} onChange={(e) => setBend(Number(e.target.value))} /></label>
          <button onClick={buildJoin}>{b ? "Rebuild B" : "Join patch B"}</button>
          {b && <button onClick={() => { setB(null); setSel({ patch: 0, i: 1, j: 1 }); }}>Remove B</button>}
        </div>
        {report && (
          <div className="math continuity">
            <div className={`level level-${report.report.level}`}>Measured: {report.report.level === "none" ? "no continuity" : report.report.level}</div>
            <div>G0 gap max |A(1,v) − B(0,v)| = {report.report.gap.toExponential(2)} mm {report.report.gap <= report.tolerances.g0 ? "✓" : "✗"}</div>
            <div>G1 normal angle max ∠(nA, nB) = {report.report.angle.toExponential(2)}° {report.report.angle <= report.tolerances.g1_deg ? "✓" : "✗"}</div>
            <div>G2 normal-curvature jump max |κA − κB| = {report.report.curvature_jump.toExponential(2)} /mm</div>
            <div>G3 curvature-rate jump (estimate) = {report.report.rate_jump.toExponential(2)} /mm²</div>
            <div className="muted">κₙ = (S_uu · n)/(S_u · S_u) across the join; combs drawn ×{combScale}</div>
            <p>{report.report.explanation}</p>
            <label>comb scale <input type="range" min={0} max={20000} step={500} value={combScale}
              onChange={(e) => setCombScale(Number(e.target.value))} /></label>
          </div>
        )}
        {note && <p className="hint">{note}</p>}
        <p className="hint">Drag a lattice point in the view (or edit it here). The amber region is where that
          point moves the surface: its local support, the product of its two basis functions' non-zero spans.</p>
      </div>
    </div>
  );
}

function BasisPlot({ title, table, knots, highlight }: {
  title: string; table: { t: number[]; functions: number[][] }; knots: number[]; highlight?: number;
}) {
  const W = 300, H = 74, L = 6, B = 12;
  const t0 = table.t[0], t1 = table.t[table.t.length - 1];
  const x = (t: number) => L + ((t - t0) / Math.max(t1 - t0, 1e-9)) * (W - 2 * L);
  const y = (v: number) => 4 + (1 - v) * (H - B - 4);
  return (
    <svg className="chart basis" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Basis functions ${title}`}>
      <text x={W - 4} y={11} textAnchor="end" className="chart-title">{title}</text>
      {[...new Set(knots)].map((k) => (
        <line key={k} x1={x(k)} x2={x(k)} y1={4} y2={H - B} className="knot" />
      ))}
      {table.functions.map((f, i) => (
        <path key={i} className={i === highlight ? "fn on" : "fn"}
          d={f.map((v, k) => `${k ? "L" : "M"}${x(table.t[k]).toFixed(1)},${y(v).toFixed(1)}`).join("")} />
      ))}
      <text x={L} y={H - 1} className="tick">{t0}</text>
      <text x={W - L} y={H - 1} textAnchor="end" className="tick">{t1}</text>
    </svg>
  );
}

function ParamSpace({ ev }: { ev: NurbsEvaluation }) {
  const S = 120;
  const [[u0, u1], [v0, v1]] = ev.domain;
  const x = (u: number) => 6 + ((u - u0) / Math.max(u1 - u0, 1e-9)) * (S - 12);
  const y = (v: number) => S - 6 - ((v - v0) / Math.max(v1 - v0, 1e-9)) * (S - 12);
  const sup = ev.support;
  return (
    <svg className="chart param" viewBox={`0 0 ${S} ${S}`} role="img" aria-label="Parameter space (u, v)">
      <rect x={6} y={6} width={S - 12} height={S - 12} className="domain" />
      {sup && <rect x={x(sup.u[0])} y={y(sup.v[1])} width={x(sup.u[1]) - x(sup.u[0])} height={y(sup.v[0]) - y(sup.v[1])} className="support" />}
      {[...new Set(ev.surface.knots_u)].map((k) => <line key={`u${k}`} x1={x(k)} x2={x(k)} y1={6} y2={S - 6} className="knot" />)}
      {[...new Set(ev.surface.knots_v)].map((k) => <line key={`v${k}`} y1={y(k)} y2={y(k)} x1={6} x2={S - 6} className="knot" />)}
      <text x={S / 2} y={S - 0.5} textAnchor="middle" className="tick">u</text>
      <text x={1} y={S / 2} className="tick">v</text>
    </svg>
  );
}
