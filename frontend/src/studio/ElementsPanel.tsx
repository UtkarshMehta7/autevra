import { useEffect, useMemo, useRef, useState } from "react";
import { api, type ElementOut } from "../api/client";

/** Machine elements workspace (shared by every module): bolted joints, fillet welds,
 * fatigue (Goodman family, S-N life, rainflow damage), helical springs and spur gear pairs.
 * Calculations run in the backend (autevra/elements); each result names its method. */

type Kind = "bolt" | "weld" | "fatigue" | "fatigue/history" | "spring" | "gears";
type Tab = "bolt" | "weld" | "fatigue" | "spring" | "gears";

const TABS: { id: Tab; label: string; method: string }[] = [
  { id: "bolt", label: "Bolted joint", method: "ISO 898-1 strength, T = K·F·d, Shigley joint stiffness and Goodman bolt fatigue" },
  { id: "weld", label: "Fillet weld", method: "Throat a = 0.707·z; EN 1993-1-8 directional method" },
  { id: "fatigue", label: "Fatigue", method: "Marin factors, Goodman / Soderberg / Gerber / ASME elliptic, Basquin S-N, ASTM E1049 rainflow, Miner" },
  { id: "spring", label: "Spring", method: "EN 13906-1 rate and stress (Bergsträsser), solid height, buckling, surge" },
  { id: "gears", label: "Spur gears", method: "ISO 21771 geometry with profile shift, contact ratio, undercut; Lewis bending, nominal Hertz stress" },
];

// ISO 261 coarse threads: [d, pitch]
const THREADS: [number, number][] = [[3, 0.5], [4, 0.7], [5, 0.8], [6, 1], [8, 1.25], [10, 1.5], [12, 1.75], [16, 2], [20, 2.5], [24, 3], [30, 3.5], [36, 4]];

const num = (o: ElementOut | Record<string, unknown> | null | undefined, k: string) => {
  const v = o?.[k];
  return typeof v === "number" ? v : NaN;
};
const fmt = (v: number, digits = 3) => {
  if (!Number.isFinite(v)) return v === Infinity ? "∞" : "—";
  const a = Math.abs(v);
  if (a >= 1e6) return v.toExponential(2);
  if (a >= 1000) return v.toFixed(0);
  return Number(v.toPrecision(digits + (a >= 100 ? 1 : 0))).toString();
};

function Num({ label, value, onChange, step = 1, unit, min }: { label: string; value: number; onChange: (v: number) => void; step?: number; unit?: string; min?: number }) {
  return (
    <label className="el-field">{label}
      <span><input type="number" value={value} step={step} min={min} onChange={(e) => { const v = Number(e.target.value); if (Number.isFinite(v)) onChange(v); }} />{unit && <em>{unit}</em>}</span>
    </label>
  );
}

function Pick<T extends string>({ label, value, options, onChange }: { label: string; value: T; options: readonly T[] | { value: T; label: string }[]; onChange: (v: T) => void }) {
  return (
    <label className="el-field">{label}
      <select value={value} onChange={(e) => onChange(e.target.value as T)}>
        {options.map((o) => typeof o === "string" ? <option key={o} value={o}>{o}</option> : <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </label>
  );
}

/** Calls the backend whenever the inputs change (debounced). */
function useCalc(kind: Kind, body: unknown): { out: ElementOut | null; error: string | null } {
  const [out, setOut] = useState<ElementOut | null>(null);
  const [error, setError] = useState<string | null>(null);
  const key = JSON.stringify(body);
  const seq = useRef(0);
  useEffect(() => {
    const mine = ++seq.current;
    const t = setTimeout(() => {
      api.element(kind, JSON.parse(key))
        .then((o) => { if (mine === seq.current) { setOut(o); setError(null); } })
        .catch((e: unknown) => { if (mine === seq.current) setError(e instanceof Error ? e.message : String(e)); });
    }, 180);
    return () => clearTimeout(t);
  }, [kind, key]);
  return { out, error };
}

function Results({ rows }: { rows: [string, number | string, string?, ("good" | "warn" | "bad")?][] }) {
  return (
    <table className="bd-table el-results"><tbody>
      {rows.map(([label, v, unit, tone]) => (
        <tr key={label}><td>{label}</td><td className={`num ${tone ?? ""}`}>{typeof v === "number" ? fmt(v) : v}</td><td className="muted">{unit ?? ""}</td></tr>
      ))}
    </tbody></table>
  );
}

function Warnings({ out, error }: { out: ElementOut | null; error: string | null }) {
  if (error) return <p className="el-warn bad">{error}</p>;
  if (!out) return <p className="small muted">Calculating…</p>;
  if (!out.warnings?.length) return <p className="el-ok">All checks pass.</p>;
  return <ul className="el-warn">{out.warnings.map((w) => <li key={w}>{w}</li>)}</ul>;
}

const tone = (n: number, ok = 1.5): "good" | "warn" | "bad" => (n < 1 ? "bad" : n < ok ? "warn" : "good");

// ---------- bolted joint ----------

function JointDiagram({ d }: { d: Record<string, number> }) {
  const fi = d.preload_kN, db = d.bolt_stretch_um, dm = d.member_compression_um, dp = d.extra_stretch_um ?? 0;
  const fb = d.bolt_load_kN ?? fi, fm = d.member_load_kN ?? fi;
  const W = 300, H = 170, pad = 26;
  const xMax = db + dm, yMax = Math.max(fb, fi) * 1.15;
  const X = (u: number) => pad + ((u + db) / xMax) * (W - 2 * pad);
  const Y = (f: number) => H - pad - (f / yMax) * (H - 2 * pad);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="el-chart" role="img" aria-label="Joint diagram">
      <line x1={pad} y1={Y(0)} x2={W - pad} y2={Y(0)} className="axis" />
      <line x1={X(-db)} y1={Y(0)} x2={X(dp)} y2={Y(fb)} className="s-bolt" />
      <line x1={X(0) - 0.0001} y1={Y(fi)} x2={X(dm)} y2={Y(0)} className="s-member" />
      <line x1={X(0)} y1={Y(0)} x2={X(0)} y2={Y(fi)} className="guide" />
      {dp > 0 && <>
        <line x1={X(dp)} y1={Y(fm)} x2={X(dp)} y2={Y(fb)} className="s-load" />
        <circle cx={X(dp)} cy={Y(fb)} r={3} className="dot-bolt" />
        <circle cx={X(dp)} cy={Y(fm)} r={3} className="dot-member" />
        <text x={X(dp) + 5} y={(Y(fb) + Y(fm)) / 2 + 3} className="lbl">P</text>
      </>}
      <circle cx={X(0)} cy={Y(fi)} r={3} className="dot" />
      <text x={X(0) - 4} y={Y(fi) - 6} textAnchor="end" className="lbl">Fi {fmt(fi)} kN</text>
      <text x={X(-db) + 4} y={Y(0) - 6} className="lbl s-bolt-t">bolt</text>
      <text x={X(dm) - 4} y={Y(0) - 6} textAnchor="end" className="lbl s-member-t">members</text>
      <text x={W / 2} y={H - 6} textAnchor="middle" className="lbl muted">deformation (µm): bolt stretch {fmt(db)}, member compression {fmt(dm)}</text>
    </svg>
  );
}

function BoltTab() {
  const [thread, setThread] = useState(5);
  const [b, setB] = useState({ grade: "8.8", nut_factor: 0.2, preload_fraction: 0.9, grip: 30, load_kN: 10, shear_kN: 0, friction: 0.2, shear_planes: 1 });
  const [d, pitch] = THREADS[thread];
  const { out, error } = useCalc("bolt", { ...b, d, pitch });
  const diag = out?.diagram as Record<string, number> | undefined;
  return (
    <div className="el-body">
      <div className="el-inputs">
        <label className="el-field">thread
          <select value={thread} onChange={(e) => setThread(Number(e.target.value))}>
            {THREADS.map(([dd, pp], i) => <option key={dd} value={i}>M{dd}×{pp}</option>)}
          </select>
        </label>
        <Pick label="property class" value={b.grade} options={["8.8", "10.9", "12.9"]} onChange={(v) => setB({ ...b, grade: v })} />
        <Num label="nut factor K" value={b.nut_factor} step={0.01} onChange={(v) => setB({ ...b, nut_factor: v })} />
        <Num label="preload" value={Math.round(b.preload_fraction * 100)} unit="% proof" onChange={(v) => setB({ ...b, preload_fraction: Math.min(Math.max(v, 10), 100) / 100 })} />
        <Num label="grip length" value={b.grip} unit="mm" onChange={(v) => setB({ ...b, grip: v })} />
        <Num label="tensile load / bolt" value={b.load_kN} unit="kN" onChange={(v) => setB({ ...b, load_kN: Math.max(v, 0) })} />
        <Num label="shear load / bolt" value={b.shear_kN} unit="kN" onChange={(v) => setB({ ...b, shear_kN: Math.max(v, 0) })} />
        <Num label="slip factor μ" value={b.friction} step={0.05} onChange={(v) => setB({ ...b, friction: v })} />
      </div>
      <div className="el-out">
        {out && <Results rows={[
          ["stress area As", num(out, "stress_area_mm2"), "mm²"],
          ["proof load", num(out, "proof_load_kN"), "kN"],
          ["preload Fi", num(out, "preload_kN"), "kN"],
          ["tightening torque", num(out, "torque_Nm"), "N·m"],
          ["joint constant C", num(out, "joint_constant"), ""],
          ["separation load", num(out, "separation_load_kN"), "kN"],
          ...(b.load_kN > 0 ? [
            ["bolt load Fb", num(out, "bolt_load_kN"), "kN"],
            ["yield factor", num(out, "yield_factor"), "", tone(num(out, "yield_factor"), 1.0)],
            ["separation factor", num(out, "separation_factor"), "", tone(num(out, "separation_factor"))],
            ["bolt fatigue factor", num(out, "fatigue_factor"), "", tone(num(out, "fatigue_factor"))],
          ] as [string, number, string, ("good" | "warn" | "bad")?][] : []),
          ...(b.shear_kN > 0 ? [["slip factor", num(out, "slip_factor"), "", tone(num(out, "slip_factor"), 1.25)]] as [string, number, string, ("good" | "warn" | "bad")][] : []),
        ]} />}
        {diag && <JointDiagram d={diag} />}
        <Warnings out={out} error={error} />
      </div>
    </div>
  );
}

// ---------- weld ----------

function WeldTab() {
  const [w, setW] = useState({ leg: 5, length: 100, force_kN: 40, direction: "longitudinal", lines: 2, allowable: 150, steel: "S355" });
  const { out, error } = useCalc("weld", w);
  const throat = num(out, "throat_mm");
  return (
    <div className="el-body">
      <div className="el-inputs">
        <Num label="leg z" value={w.leg} unit="mm" step={0.5} onChange={(v) => setW({ ...w, leg: v })} />
        <Num label="length per weld" value={w.length} unit="mm" onChange={(v) => setW({ ...w, length: v })} />
        <Num label="welds sharing the load" value={w.lines} onChange={(v) => setW({ ...w, lines: Math.max(1, Math.round(v)) })} />
        <Num label="force" value={w.force_kN} unit="kN" onChange={(v) => setW({ ...w, force_kN: Math.max(v, 0) })} />
        <Pick label="load direction" value={w.direction} options={[{ value: "longitudinal", label: "along the weld" }, { value: "transverse", label: "across the weld" }]} onChange={(v) => setW({ ...w, direction: v })} />
        <Pick label="parent steel" value={w.steel} options={["S235", "S275", "S355", "S460"]} onChange={(v) => setW({ ...w, steel: v })} />
        <Num label="simple allowable" value={w.allowable} unit="MPa" onChange={(v) => setW({ ...w, allowable: v })} />
      </div>
      <div className="el-out">
        {out && <Results rows={[
          ["throat a", throat, "mm"],
          ["throat area", num(out, "throat_area_mm2"), "mm²"],
          ["throat shear τ = F/(a·L)", num(out, "tau"), "MPa", num(out, "tau") > w.allowable ? "bad" : "good"],
          ["σ⊥ / τ⊥ / τ∥", `${fmt(num(out, "sigma_perp"))} / ${fmt(num(out, "tau_perp"))} / ${fmt(num(out, "tau_par"))}`, "MPa"],
          ["equivalent √(σ⊥² + 3(τ⊥² + τ∥²))", num(out, "equivalent"), "MPa"],
          ["limit fu / (βw·γM2)", num(out, "limit"), "MPa"],
          ["utilisation", num(out, "utilisation"), "", num(out, "utilisation") > 1 ? "bad" : num(out, "utilisation") > 0.9 ? "warn" : "good"],
          ["capacity", num(out, "capacity_kN"), "kN"],
        ]} />}
        {out && Number.isFinite(throat) && (
          <svg viewBox="0 0 160 110" className="el-chart small-chart" role="img" aria-label="Fillet weld section">
            <rect x={20} y={70} width={130} height={14} className="plate" />
            <rect x={20} y={10} width={14} height={60} className="plate" />
            <polygon points={`34,70 ${34 + 45},70 34,${70 - 45}`} className="bead" />
            <line x1={34} y1={70} x2={34 + 22.5} y2={70 - 22.5} className="guide" />
            <text x={60} y={42} className="lbl">a = {fmt(throat)} mm</text>
            <text x={50} y={98} className="lbl muted">z = {w.leg} mm</text>
          </svg>
        )}
        <Warnings out={out} error={error} />
      </div>
    </div>
  );
}

// ---------- fatigue ----------

function Haigh({ out, sut, sy }: { out: ElementOut; sut: number; sy: number }) {
  const se = num(out, "Se"), sa = num(out, "sigma_a"), sm = Math.max(num(out, "sigma_m"), 0);
  const W = 320, H = 200, pad = 30;
  const xMax = sut * 1.05, yMax = Math.max(se, sa, sy * 0.6) * 1.2;
  const X = (v: number) => pad + (v / xMax) * (W - pad - 10);
  const Y = (v: number) => H - pad - (v / yMax) * (H - pad - 10);
  const gerber = Array.from({ length: 31 }, (_, i) => { const m = (sut * i) / 30; return `${X(m)},${Y(se * (1 - (m / sut) ** 2))}`; }).join(" ");
  const ellipse = Array.from({ length: 31 }, (_, i) => { const m = (sy * i) / 30; return `${X(m)},${Y(se * Math.sqrt(Math.max(1 - (m / sy) ** 2, 0)))}`; }).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="el-chart" role="img" aria-label="Haigh diagram">
      <line x1={pad} y1={Y(0)} x2={W - 8} y2={Y(0)} className="axis" />
      <line x1={pad} y1={Y(0)} x2={pad} y2={8} className="axis" />
      <polyline points={gerber} className="c-gerber" />
      <polyline points={ellipse} className="c-ellipse" />
      <line x1={X(0)} y1={Y(se)} x2={X(sy)} y2={Y(0)} className="c-soderberg" />
      <line x1={X(0)} y1={Y(se)} x2={X(sut)} y2={Y(0)} className="c-goodman" />
      <line x1={X(0)} y1={Y(Math.min(sy, yMax))} x2={X(sy)} y2={Y(0)} className="c-langer" />
      {sa + sm > 0 && <line x1={X(0)} y1={Y(0)} x2={X(sm * 3)} y2={Y(sa * 3)} className="guide" />}
      <circle cx={X(sm)} cy={Y(sa)} r={4} className={`dot ${tone(num(out.factors as Record<string, number>, "goodman"))}`} />
      <text x={X(0) + 4} y={Y(se) - 4} className="lbl">Se {fmt(se)}</text>
      <text x={X(sut)} y={Y(0) + 12} textAnchor="end" className="lbl">Sut {fmt(sut)}</text>
      <text x={X(sy)} y={Y(0) + 12} textAnchor="middle" className="lbl muted">Sy</text>
      <text x={W / 2} y={H - 4} textAnchor="middle" className="lbl muted">mean stress σm (MPa) →   ↑ alternating σa</text>
      <g className="legend" transform={`translate(${W - 118},12)`}>
        {[["c-goodman", "Goodman"], ["c-gerber", "Gerber"], ["c-soderberg", "Soderberg"], ["c-ellipse", "ASME elliptic"], ["c-langer", "Langer (yield)"]].map(([c, l], i) => (
          <g key={c} transform={`translate(0,${i * 12})`}><line x1={0} y1={0} x2={14} y2={0} className={c} /><text x={18} y={3} className="lbl">{l}</text></g>
        ))}
      </g>
    </svg>
  );
}

function FatigueTab() {
  const [f, setF] = useState({ sut: 600, sy: 450, surface: "machined", diameter: 25, loading: "bending", reliability: 90, kt: 1.8, notch_sensitivity: 0.85, sigma_a: 80, sigma_m: 120 });
  const { out, error } = useCalc("fatigue", f);
  const [series, setSeries] = useState("0, 250, -40, 180, 20, 300, -120, 90, -60, 0");
  const [repeats, setRepeats] = useState(10000);
  const parsed = useMemo(() => series.split(/[\s,;]+/).map(Number).filter((v) => Number.isFinite(v)), [series]);
  const se = num(out, "Se");
  const hist = useCalc("fatigue/history", { series: parsed.length >= 2 ? parsed : [0, 1], sut: f.sut, se: Number.isFinite(se) ? se : f.sut / 2, repeats });
  const factors = (out?.factors ?? {}) as Record<string, number>;
  return (
    <div className="el-body">
      <div className="el-inputs">
        <Num label="ultimate Sut" value={f.sut} unit="MPa" step={10} onChange={(v) => setF({ ...f, sut: v })} />
        <Num label="yield Sy" value={f.sy} unit="MPa" step={10} onChange={(v) => setF({ ...f, sy: v })} />
        <Pick label="surface" value={f.surface} options={["ground", "machined", "cold-drawn", "hot-rolled", "as-forged"]} onChange={(v) => setF({ ...f, surface: v })} />
        <Num label="diameter" value={f.diameter} unit="mm" onChange={(v) => setF({ ...f, diameter: v })} />
        <Pick label="loading" value={f.loading} options={["bending", "axial", "torsion"]} onChange={(v) => setF({ ...f, loading: v })} />
        <Pick label="reliability" value={String(f.reliability)} options={["50", "90", "95", "99", "99.9", "99.99"]} onChange={(v) => setF({ ...f, reliability: Number(v) })} />
        <Num label="stress concentration Kt" value={f.kt} step={0.1} onChange={(v) => setF({ ...f, kt: Math.max(v, 1) })} />
        <Num label="notch sensitivity q" value={f.notch_sensitivity} step={0.05} onChange={(v) => setF({ ...f, notch_sensitivity: Math.min(Math.max(v, 0), 1) })} />
        <Num label="alternating σa" value={f.sigma_a} unit="MPa" step={5} onChange={(v) => setF({ ...f, sigma_a: Math.max(v, 0) })} />
        <Num label="mean σm" value={f.sigma_m} unit="MPa" step={5} onChange={(v) => setF({ ...f, sigma_m: v })} />
      </div>
      <div className="el-out">
        {out && <>
          <p className="small el-marin">Se = ka {fmt(num(out, "ka"))} · kb {fmt(num(out, "kb"))} · kc {fmt(num(out, "kc"))} · kd {fmt(num(out, "kd"))} · ke {fmt(num(out, "ke"))} · Se′ {fmt(num(out, "Se_prime"))} = <b>{fmt(se)} MPa</b>; Kf = {fmt(num(out, "Kf"))}</p>
          <Results rows={[
            ["Goodman", factors.goodman, "", tone(factors.goodman)],
            ["Gerber", factors.gerber, "", tone(factors.gerber)],
            ["Soderberg", factors.soderberg, "", tone(factors.soderberg)],
            ["ASME elliptic", factors.asme_elliptic, "", tone(factors.asme_elliptic)],
            ["Langer first-cycle yield", factors.langer, "", tone(factors.langer, 1.2)],
            ["life (Goodman equivalent)", num(out, "life_cycles"), "cycles"],
          ]} />
          <Haigh out={out} sut={f.sut} sy={f.sy} />
        </>}
        <Warnings out={out} error={error} />
        <h4>Load history (rainflow + Miner)</h4>
        <label className="el-field wide">stress history, MPa
          <textarea rows={2} value={series} onChange={(e) => setSeries(e.target.value)} />
        </label>
        <Num label="repeats" value={repeats} step={1000} onChange={(v) => setRepeats(Math.max(v, 1))} />
        {hist.out && (
          <>
            <p className="small">{(hist.out.cycles as unknown[]).length} cycles counted; damage per pass {fmt(num(hist.out, "damage_per_pass"))}, after {repeats} repeats <b className={num(hist.out, "damage") >= 1 ? "bad" : "good"}>D = {fmt(num(hist.out, "damage"))}</b>; {fmt(num(hist.out, "passes_to_failure"))} passes to failure.</p>
            <table className="bd-table"><thead><tr><th>range</th><th>mean</th><th>count</th><th>σar</th><th>N</th><th>damage</th></tr></thead><tbody>
              {(hist.out.cycles as Record<string, number>[]).map((c, i) => (
                <tr key={i}><td className="num">{fmt(c.range)}</td><td className="num">{fmt(c.mean)}</td><td className="num">{c.count}</td><td className="num">{fmt(c.reversed_equivalent)}</td><td className="num">{fmt(c.life_cycles)}</td><td className="num">{fmt(c.damage)}</td></tr>
              ))}
            </tbody></table>
          </>
        )}
      </div>
    </div>
  );
}

// ---------- spring ----------

function SpringSketch({ d, D, n, L0, Ls }: { d: number; D: number; n: number; L0: number; Ls: number }) {
  const H = 150, scale = Math.min(110 / L0, 60 / (D + d));
  const turns = Math.max(1, Math.round(n + 2));
  const pts: string[] = [];
  const x0 = 50, yBase = H - 15;
  for (let i = 0; i <= turns * 24; i += 1) {
    const t = i / 24;
    pts.push(`${x0 + (D / 2) * scale * Math.sin(t * 2 * Math.PI)},${yBase - (t / turns) * L0 * scale}`);
  }
  return (
    <svg viewBox={`0 0 160 ${H}`} className="el-chart small-chart" role="img" aria-label="Spring">
      <polyline points={pts.join(" ")} className="coil" style={{ strokeWidth: Math.max(d * scale, 1) }} />
      <line x1={110} y1={yBase} x2={110} y2={yBase - L0 * scale} className="guide" />
      <text x={114} y={yBase - (L0 * scale) / 2} className="lbl">L0 {fmt(L0)}</text>
      <line x1={130} y1={yBase} x2={130} y2={yBase - Ls * scale} className="s-bolt" />
      <text x={114} y={yBase - Ls * scale - 4} className="lbl muted">Ls {fmt(Ls)}</text>
    </svg>
  );
}

function SpringTab() {
  const [s, setS] = useState({ d: 2, D: 16, n: 8, free_length: 60, ends: "closed-ground", wire: "music", force: 40, support: "fixed-fixed" });
  const { out, error } = useCalc("spring", s);
  return (
    <div className="el-body">
      <div className="el-inputs">
        <Num label="wire d" value={s.d} unit="mm" step={0.1} onChange={(v) => setS({ ...s, d: v })} />
        <Num label="mean coil D" value={s.D} unit="mm" onChange={(v) => setS({ ...s, D: v })} />
        <Num label="active coils n" value={s.n} step={0.5} onChange={(v) => setS({ ...s, n: Math.max(v, 1) })} />
        <Num label="free length L0" value={s.free_length} unit="mm" onChange={(v) => setS({ ...s, free_length: v })} />
        <Pick label="ends" value={s.ends} options={["closed-ground", "closed", "plain", "plain-ground"]} onChange={(v) => setS({ ...s, ends: v })} />
        <Pick label="wire" value={s.wire} options={["music", "hard-drawn", "oil-tempered", "chrome-vanadium", "chrome-silicon"]} onChange={(v) => setS({ ...s, wire: v })} />
        <Pick label="end support" value={s.support} options={["fixed-fixed", "fixed-pinned", "pinned-pinned", "fixed-free"]} onChange={(v) => setS({ ...s, support: v })} />
        <Num label="working load" value={s.force} unit="N" onChange={(v) => setS({ ...s, force: Math.max(v, 0) })} />
      </div>
      <div className="el-out">
        {out && <div className="el-split">
          <Results rows={[
            ["rate k", num(out, "rate_N_per_mm"), "N/mm"],
            ["index D/d", num(out, "index"), "", num(out, "index") < 4 || num(out, "index") > 20 ? "warn" : "good"],
            ["stress factor (Bergsträsser)", num(out, "bergstrasser"), ""],
            ["solid length Ls", num(out, "solid_length"), "mm"],
            ["force at solid", num(out, "force_at_solid"), "N"],
            ["shear at solid", num(out, "tau_solid"), "MPa", num(out, "tau_solid") > num(out, "allowable_shear") ? "bad" : "good"],
            ["allowable shear", num(out, "allowable_shear"), "MPa"],
            ["deflection at load", num(out, "deflection"), "mm"],
            ["working factor", num(out, "working_factor"), "", tone(num(out, "working_factor"), 1.2)],
            ["surge frequency", num(out, "surge_hz"), "Hz"],
            ["buckling free length", num(out, "buckling_free_length"), "mm"],
          ]} />
          <SpringSketch d={s.d} D={s.D} n={s.n} L0={s.free_length} Ls={num(out, "solid_length")} />
        </div>}
        <Warnings out={out} error={error} />
      </div>
    </div>
  );
}

// ---------- gears ----------

type GearOut = { z: number; d: number; da: number; df: number; db: number; x: number; outline: [number, number][]; tip_thickness: number; undercut: boolean };

function gearPath(g: GearOut, cx: number, cy: number, rot: number, S: (v: number) => number): string {
  const teeth: string[] = [];
  for (let i = 0; i < g.z; i += 1) {
    const a = rot + (i * 2 * Math.PI) / g.z;
    const c = Math.cos(a), s = Math.sin(a);
    const pts = g.outline.map(([x, y]) => `${S(cx + x * c - y * s)},${-S(cy + x * s + y * c)}`);
    teeth.push(`M${pts.join("L")}Z`);
  }
  return teeth.join("");
}

function GearMesh({ out, m }: { out: ElementOut; m: number }) {
  const g1 = out.gear1 as GearOut, g2 = out.gear2 as GearOut, a = num(out, "centre_distance");
  const r1 = g1.da / 2, r2 = g2.da / 2;
  const span = r1 + a + r2, h = 2 * Math.max(r1, r2);
  const W = 420, H = Math.max(140, Math.min(260, (W * h) / span));
  const k = Math.min((W - 20) / span, (H - 20) / h);
  const S = (v: number) => v * k;
  const ox = 10 + S(r1), oy = H / 2;
  const rot1 = -Math.PI / 2, rot2 = Math.PI / 2 + Math.PI / g2.z;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="el-chart gear-chart" role="img" aria-label="Gear pair in mesh">
      <g transform={`translate(${ox},${oy})`}>
        <circle r={S(g1.df / 2)} className="gear g1" />
        <path d={gearPath(g1, 0, 0, rot1, S)} className="gear g1" />
        <circle r={S(g1.d / 2)} className="pitch" />
        <circle r={S(g1.db / 2)} className="base" />
        <circle cx={S(a)} r={S(g2.df / 2)} className="gear g2" />
        <path d={gearPath(g2, a, 0, rot2, S)} className="gear g2" />
        <circle cx={S(a)} r={S(g2.d / 2)} className="pitch" />
        <circle cx={S(a)} r={S(g2.db / 2)} className="base" />
        <line x1={0} y1={0} x2={S(a)} y2={0} className="guide" />
        <circle r={2.5} className="dot" /><circle cx={S(a)} r={2.5} className="dot" />
      </g>
      <text x={8} y={14} className="lbl">m {m} · a = {fmt(a)} mm · εα = {fmt(num(out, "contact_ratio"))} · pitch circles dashed, base circles dotted</text>
    </svg>
  );
}

function GearsTab({ projectId, onModelChanged }: { projectId?: string; onModelChanged: () => void }) {
  const [g, setG] = useState({ module: 2, z1: 18, z2: 42, pressure_angle: 20, x1: 0, x2: 0, face_width: 20, torque_Nm: 60, rpm: 1500, bore1: 12, bore2: 20 });
  const { out, error } = useCalc("gears", g);
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const g1 = out?.gear1 as GearOut | undefined, g2 = out?.gear2 as GearOut | undefined;
  const add = async () => {
    if (!projectId) return;
    setBusy(true); setNote(null);
    try {
      const parts = await api.addGears(projectId, g);
      setNote(`Added ${parts.map((p) => `"${p.document.name}"`).join(" and ")} to the project, placed in mesh.`);
      onModelChanged();
    } catch (e) { setNote(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };
  return (
    <div className="el-body">
      <div className="el-inputs">
        <Num label="module m" value={g.module} unit="mm" step={0.25} onChange={(v) => setG({ ...g, module: v })} />
        <Num label="pinion teeth z1" value={g.z1} onChange={(v) => setG({ ...g, z1: Math.max(6, Math.round(v)) })} />
        <Num label="gear teeth z2" value={g.z2} onChange={(v) => setG({ ...g, z2: Math.max(6, Math.round(v)) })} />
        <Pick label="pressure angle" value={String(g.pressure_angle)} options={["14.5", "20", "25"]} onChange={(v) => setG({ ...g, pressure_angle: Number(v) })} />
        <Num label="profile shift x1" value={g.x1} step={0.05} onChange={(v) => setG({ ...g, x1: v })} />
        <Num label="profile shift x2" value={g.x2} step={0.05} onChange={(v) => setG({ ...g, x2: v })} />
        <Num label="face width b" value={g.face_width} unit="mm" onChange={(v) => setG({ ...g, face_width: v })} />
        <Num label="pinion torque" value={g.torque_Nm} unit="N·m" onChange={(v) => setG({ ...g, torque_Nm: Math.max(v, 0) })} />
        <Num label="pinion speed" value={g.rpm} unit="rpm" step={100} onChange={(v) => setG({ ...g, rpm: Math.max(v, 0) })} />
        <Num label="pinion bore" value={g.bore1} unit="mm" onChange={(v) => setG({ ...g, bore1: Math.max(v, 0) })} />
        <Num label="gear bore" value={g.bore2} unit="mm" onChange={(v) => setG({ ...g, bore2: Math.max(v, 0) })} />
        <button disabled={busy || !projectId || !out || !!error} onClick={add}>{busy ? "Building gears…" : "Add gear pair to the project"}</button>
        {note && <p className="small">{note}</p>}
      </div>
      <div className="el-out">
        {out && g1 && g2 && <>
          <GearMesh out={out} m={g.module} />
          <table className="bd-table el-results"><thead><tr><th /><th className="num">pinion</th><th className="num">gear</th><th /></tr></thead><tbody>
            {([["teeth", "z", ""], ["reference d", "d", "mm"], ["tip da", "da", "mm"], ["root df", "df", "mm"], ["base db", "db", "mm"], ["tip thickness", "tip_thickness", "mm"]] as const).map(([l, k, u]) => (
              <tr key={k}><td>{l}</td><td className="num">{fmt(g1[k])}</td><td className="num">{fmt(g2[k])}</td><td className="muted">{u}</td></tr>
            ))}
            <tr><td>undercut</td><td className={`num ${g1.undercut ? "bad" : "good"}`}>{g1.undercut ? "yes" : "no"}</td><td className={`num ${g2.undercut ? "bad" : "good"}`}>{g2.undercut ? "yes" : "no"}</td><td /></tr>
          </tbody></table>
          <Results rows={[
            ["ratio u", num(out, "ratio"), ""],
            ["centre distance", num(out, "centre_distance"), "mm"],
            ["working pressure angle", num(out, "working_pressure_angle"), "°"],
            ["contact ratio εα", num(out, "contact_ratio"), "", num(out, "contact_ratio") < 1.2 ? "bad" : num(out, "contact_ratio") < 1.4 ? "warn" : "good"],
            ...(g.torque_Nm > 0 ? [
              ["tangential force", num(out, "tangential_force_N"), "N"],
              ["pitch-line speed", num(out, "pitch_line_velocity"), "m/s"],
              ["power", num(out, "power_kW"), "kW"],
              ["Lewis bending, pinion", num(out, "bending_pinion"), "MPa"],
              ["Lewis bending, gear", num(out, "bending_gear"), "MPa"],
              ["nominal contact stress σH0", num(out, "contact_stress"), "MPa"],
            ] as [string, number, string][] : []),
          ]} />
        </>}
        <Warnings out={out} error={error} />
      </div>
    </div>
  );
}

export function ElementsPanel({ projectId, onModelChanged }: { projectId?: string; onModelChanged: () => void }) {
  const [tab, setTab] = useState<Tab>(() => {
    try { return (localStorage.getItem("autevra.elements.tab") as Tab) || "gears"; } catch { return "gears"; }
  });
  const pick = (t: Tab) => { setTab(t); try { localStorage.setItem("autevra.elements.tab", t); } catch { /* storage unavailable */ } };
  const meta = TABS.find((t) => t.id === tab) ?? TABS[0];
  return (
    <section className="elements-panel">
      <div className="el-tabs" role="tablist">
        {TABS.map((t) => <button key={t.id} role="tab" aria-selected={t.id === tab} className={t.id === tab ? "active" : ""} onClick={() => pick(t.id)}>{t.label}</button>)}
      </div>
      <p className="small muted el-method">{meta.method}. Design estimates for sizing, not certification.</p>
      {tab === "bolt" && <BoltTab />}
      {tab === "weld" && <WeldTab />}
      {tab === "fatigue" && <FatigueTab />}
      {tab === "spring" && <SpringTab />}
      {tab === "gears" && <GearsTab projectId={projectId} onModelChanged={onModelChanged} />}
    </section>
  );
}
