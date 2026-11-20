import { useEffect, useState } from "react";
import { api, type DraftReport, type PartingReport, type PfmeaOut } from "../api/client";
import type { PartOut } from "../api/types";

/** Production workspace (every module): the MBOM by station with a process plan,
 * work content and operators at the takt time, unit cost and CO2, reconciliation against
 * the design breakdown, and the design's tolerance stack-ups (worst case, RSS, Cpk) with
 * editable tolerances (backend manufacturing.py, quality.py). Times and rates are
 * indicative concept values, stated as such. */

interface Op { part: string; name: string; process: string; station: string; instances: number; make_min: number; fit_min: number; material: string; cost_eur: number; co2_kg: number; bought_out: boolean }
interface St { name: string; operations: number; work_min: number; operators: number; make_min: number }
interface Plan { stations: St[]; operations: Op[]; takt_s: number; total_cost_eur: number; total_co2_kg: number; material_cost_eur: number; labour_and_machine_eur: number; reconciliation: string[] }
interface Contributor { name: string; nominal: number; plus: number; minus: number; direction: number }
interface StackT { name: string; contributors: Contributor[]; lsl: number | null; usl: number | null }
interface Result { nominal: number; mean: number; worst_case: number[]; rss: number[]; sigma: number; cpk?: number; ppm_out?: number; worst_case_ok?: boolean; contributions: Record<string, number> }

function StackCard({ initial, first }: { initial: StackT; first: Result }) {
  const [stack, setStack] = useState(initial);
  const [res, setRes] = useState(first);
  useEffect(() => {
    const t = window.setTimeout(() => { api.stackup(stack).then((r) => setRes(r as Result)).catch(() => undefined); }, 200);
    return () => window.clearTimeout(t);
  }, [stack]);
  const lo = Math.min(res.worst_case[0], stack.lsl ?? Infinity), hi = Math.max(res.worst_case[1], stack.usl ?? -Infinity);
  const span = hi - lo || 1, pad = span * 0.15;
  const x = (v: number) => (((v - (lo - pad)) / (span + 2 * pad)) * 100).toFixed(2) + "%";
  const setTol = (i: number, key: "plus" | "minus", v: number) =>
    setStack({ ...stack, contributors: stack.contributors.map((c, j) => (j === i ? { ...c, [key]: v } : c)) });
  return (
    <div className="stack">
      <b>{stack.name}</b> <span className="muted small">limits {stack.lsl ?? "—"} … {stack.usl ?? "—"}</span>
      <div className="stack-bar">
        {stack.lsl !== null && <i className="limit" style={{ left: x(stack.lsl) }} />}
        {stack.usl !== null && <i className="limit" style={{ left: x(stack.usl) }} />}
        <span className={`wc ${res.worst_case_ok ? "ok" : "bad"}`} style={{ left: x(res.worst_case[0]), width: `calc(${x(res.worst_case[1])} - ${x(res.worst_case[0])})` }} />
        <span className="rss" style={{ left: x(res.rss[0]), width: `calc(${x(res.rss[1])} - ${x(res.rss[0])})` }} />
      </div>
      <div className="small">
        worst case {res.worst_case[0].toFixed(3)} … {res.worst_case[1].toFixed(3)} {res.worst_case_ok ? "✓" : "✗ outside the limits"} ·
        RSS ±3σ {res.rss[0].toFixed(3)} … {res.rss[1].toFixed(3)} · Cpk <b>{res.cpk?.toFixed(2) ?? "—"}</b>
        {res.ppm_out !== undefined && ` · ${res.ppm_out < 1 ? "< 1" : res.ppm_out.toFixed(0)} ppm outside`}
      </div>
      <table><thead><tr><th>Contributor</th><th className="num">nominal</th><th className="num">+</th><th className="num">−</th><th className="num">share of variance</th></tr></thead>
        <tbody>{stack.contributors.map((c, i) => (
          <tr key={c.name}><td>{c.direction < 0 ? "− " : "+ "}{c.name}</td><td className="num">{c.nominal}</td>
            <td className="num"><input type="number" step={0.01} min={0} value={c.plus} onChange={(e) => setTol(i, "plus", Number(e.target.value))} /></td>
            <td className="num"><input type="number" step={0.01} min={0} value={c.minus} onChange={(e) => setTol(i, "minus", Number(e.target.value))} /></td>
            <td className="num">{((res.contributions[c.name] ?? 0) * 100).toFixed(0)} %</td></tr>
        ))}</tbody></table>
    </div>
  );
}

export function ProductionPanel({ projectId, version }: { projectId: string; version?: number }) {
  const [out, setOut] = useState<{ plan: Plan; stackups: { stack: StackT; result: Result }[] } | null>(null);
  const [takt, setTakt] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [grid, setGrid] = useState(0.3);
  const [lca, setLca] = useState<{ production_kg: number; use_kg: number; end_of_life_kg: number; total_kg: number;
    use: { unit: string; energy_per_unit_kwh: number; carrier: string; co2_per_unit_kg: number; life_units: number; basis: string } | null } | null>(null);
  useEffect(() => { api.lca(projectId, grid).then((r) => setLca(r as never)).catch(() => setLca(null)); }, [projectId, version, grid]);
  useEffect(() => {
    api.manufacturing(projectId, takt ?? undefined).then((r) => { setOut(r as never); setError(null); })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)));
  }, [projectId, version, takt]);
  if (!out) return <div className="bench wide">{error ?? "Planning production…"}</div>;
  const p = out.plan;
  const maxWork = Math.max(...p.stations.map((s) => s.work_min), p.takt_s / 60);
  return (
    <div className="production">
      <div className="figures">
        <div><b>€{p.total_cost_eur.toFixed(0)}</b><span>unit cost (material €{p.material_cost_eur.toFixed(0)}, labour and machines €{p.labour_and_machine_eur.toFixed(0)}, bought-out the rest)</span></div>
        <div><b>{p.total_co2_kg.toFixed(0)} kg</b><span>CO₂e, materials and purchased parts</span></div>
        <div><b>{p.stations.reduce((a, s) => a + s.operators, 0)}</b><span>assembly operators at the takt</span></div>
        <label>takt <input type="number" value={takt ?? p.takt_s} min={5} step={10} onChange={(e) => setTakt(Number(e.target.value))} /> s</label>
        <div className={p.reconciliation.length ? "check fail" : "check pass"}>{p.reconciliation.length ? p.reconciliation.join("; ") : "MBOM reconciled: every design part used exactly once"}</div>
      </div>
      <p className="muted small">Indicative concept rates and times (stated per process in the backend); a real plan uses the plant's own.</p>
      {lca && (
        <div className="lca">
          <h4>Life cycle (kg CO₂e)</h4>
          <div className="lca-bar">
            {[["production", lca.production_kg], ["use", lca.use_kg]].map(([k, v]) => (
              <span key={k as string} className={`seg ${k}`} style={{ flex: Math.max(Number(v), 0.0001) }} title={`${k}: ${Number(v).toFixed(0)} kg`} />
            ))}
          </div>
          <div className="small">
            production <b>{lca.production_kg.toFixed(0)}</b> · use <b>{lca.use_kg.toFixed(0)}</b>
            {lca.use && <> ({(lca.use.co2_per_unit_kg * (lca.use.unit === "km" ? 1000 : 1)).toFixed(lca.use.unit === "km" ? 0 : 1)} {lca.use.unit === "km" ? "g/km" : `kg per ${lca.use.unit}`} over {lca.use.life_units.toLocaleString()} {lca.use.unit}{lca.use.unit === "km" ? "" : "s"}, {lca.use.carrier})</>}
            · end-of-life credit <b>{lca.end_of_life_kg.toFixed(0)}</b> · total <b>{lca.total_kg.toFixed(0)}</b>
            {lca.use?.carrier === "electricity" && <label> · grid <input type="number" step={0.05} min={0} value={grid} onChange={(e) => setGrid(Number(e.target.value))} /> kg/kWh</label>}
          </div>
          {lca.use && <div className="muted small">Use phase: {lca.use.basis}. Indicative factors; a certified LCA uses licensed datasets.</div>}
        </div>
      )}
      <div className="prod-grid">
        <section>
          <h4>Stations (assembly work content vs takt)</h4>
          {p.stations.map((s) => (
            <div key={s.name} className="station">
              <span className="sname">{s.name}</span>
              <span className="bar"><i style={{ width: `${(s.work_min / maxWork) * 100}%` }} /></span>
              <span className="small">{s.work_min.toFixed(1)} min · {s.operators} op. · {s.operations} parts{s.make_min ? ` · fab ${s.make_min.toFixed(0)} min` : ""}</span>
            </div>
          ))}
          <h4>Tolerance stack-ups</h4>
          {out.stackups.map((s) => <StackCard key={s.stack.name} initial={s.stack} first={s.result} />)}
        </section>
        <section>
          <h4>Process plan ({p.operations.length} parts)</h4>
          <table className="bd-table"><thead><tr><th>Part</th><th>Station</th><th>Process</th><th className="num">make min</th><th className="num">fit min</th><th className="num">€</th><th className="num">CO₂ kg</th></tr></thead>
            <tbody>{[...p.operations].sort((a, b) => b.cost_eur - a.cost_eur).map((o) => (
              <tr key={o.part}><td>{o.name}{o.instances > 1 ? ` ×${o.instances}` : ""}</td><td className="muted">{o.station}</td>
                <td>{o.bought_out ? <span className="muted">bought-out</span> : o.process}</td>
                <td className="num">{o.make_min || ""}</td><td className="num">{o.fit_min}</td>
                <td className="num">{o.cost_eur.toFixed(0)}</td><td className="num">{o.co2_kg.toFixed(1)}</td></tr>
            ))}</tbody></table>
        </section>
      </div>
      <ToolingCheck projectId={projectId} version={version} />
      <ProcessFmea projectId={projectId} version={version} />
    </div>
  );
}

/** Process FMEA generated from the plan (backend pfmea.py): generic failure modes of each
 * part's process and of its fitting step, severity carried over from the design FMEA. */
function ProcessFmea({ projectId, version }: { projectId: string; version?: number }) {
  const [out, setOut] = useState<PfmeaOut | null>(null);
  const [show, setShow] = useState<"high" | "medium" | "low">("high");
  const [station, setStation] = useState("");
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api.pfmea(projectId).then((r) => { setOut(r); setError(null); }).catch((e) => setError(String(e.message ?? e)));
  }, [projectId, version]);
  if (error) return <p className="error">{error}</p>;
  if (!out) return <p className="small muted">Generating the process FMEA…</p>;
  const s = out.summary;
  const rows = out.rows.filter((r) => r.priority === show && (!station || r.station === station));
  return (
    <section className="pfmea">
      <h4>Process FMEA ({s.rows} failure modes from the process plan)</h4>
      <p className="small muted">Generic modes per process and fitting step; severity is raised to the design FMEA's worst rating for {s.linked_to_design} rows. Occurrence and detection are starting ratings, to be replaced by plant data.</p>
      <div className="row">
        {(["high", "medium", "low"] as const).map((p) => (
          <button key={p} className={show === p ? "on" : ""} onClick={() => setShow(p)}>{p} priority · {s.by_priority[p]}</button>
        ))}
        <select value={station} onChange={(e) => setStation(e.target.value)} aria-label="station">
          <option value="">every station</option>
          {Object.entries(s.stations).map(([name, st]) => <option key={name} value={name}>{name} · {st.high} high · max RPN {st.max_rpn}</option>)}
        </select>
      </div>
      <table className="bd-table pfmea-table"><thead><tr><th>Part</th><th>Step</th><th>Failure mode</th><th>Effect</th><th>Cause</th><th>Prevention</th><th>Detection</th><th className="num">S</th><th className="num">O</th><th className="num">D</th><th className="num">RPN</th></tr></thead>
        <tbody>{rows.slice(0, 80).map((r, i) => (
          <tr key={i}><td>{r.name}<div className="muted">{r.station}</div></td><td>{r.step}</td><td>{r.mode}</td><td>{r.effect}</td><td>{r.cause}</td><td>{r.prevention}</td><td>{r.detection_control}</td>
            <td className="num" title={r.severity_from === "generic" ? "generic severity" : `from the design failure: ${r.severity_from}`}>{r.severity}{r.severity_from !== "generic" ? "*" : ""}</td>
            <td className="num">{r.occurrence}</td><td className="num">{r.detection}</td><td className="num"><b>{r.rpn}</b></td></tr>
        ))}</tbody></table>
      {rows.length > 80 && <p className="small muted">Showing the 80 highest of {rows.length}; pick a station to narrow it.</p>}
      {rows.length === 0 && <p className="small muted">No {show}-priority rows{station ? " at this station" : ""}.</p>}
      <p className="small muted">* severity carried over from the design FMEA of the block the part realises.</p>
    </section>
  );
}

/** Tooling check of one part (backend tooling.py): draft against a pull direction, and the
 * parting line, undercuts and clamp force of a straight-pull tool. */
function ToolingCheck({ projectId, version }: { projectId: string; version?: number }) {
  const [parts, setParts] = useState<PartOut[]>([]);
  const [part, setPart] = useState("");
  const [pull, setPull] = useState("z");
  const [minDraft, setMinDraft] = useState(1);
  const [pressure, setPressure] = useState(40);
  const [out, setOut] = useState<{ draft: DraftReport; parting: PartingReport } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api.parts(projectId).then((p) => { setParts(p); setPart((cur) => (p.some((x) => x.id === cur) ? cur : p[0]?.id ?? "")); }).catch(() => undefined);
  }, [projectId, version]);
  const run = async () => {
    setBusy(true);
    try {
      const [draft, parting] = await Promise.all([api.partDraft(projectId, part, pull, minDraft), api.partParting(projectId, part, pull, pressure)]);
      setOut({ draft, parting }); setError(null);
    } catch (e) { setOut(null); setError(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };
  const d = out?.draft, pt = out?.parting;
  return (
    <section className="pfmea tooling">
      <h4>Tooling check (moulded or cast part)</h4>
      {parts.length === 0 ? <p className="small muted">Add a part to the project (Part Design, Inventory or STEP import) to check its draft and parting line.</p> : (
        <div className="row">
          <label>part <select value={part} onChange={(e) => { setPart(e.target.value); setOut(null); }}>{parts.map((p) => <option key={p.id} value={p.id}>{p.document.name}</option>)}</select></label>
          <label>pull <select value={pull} onChange={(e) => setPull(e.target.value)}>{["z", "-z", "x", "-x", "y", "-y"].map((a) => <option key={a} value={a}>{a.startsWith("-") ? a : `+${a}`}</option>)}</select></label>
          <label>minimum draft <input type="number" min={0} max={45} step={0.5} value={minDraft} onChange={(e) => setMinDraft(Number(e.target.value))} /> °</label>
          <label>cavity pressure <input type="number" min={1} max={300} step={5} value={pressure} onChange={(e) => setPressure(Number(e.target.value))} /> MPa</label>
          <button disabled={busy || !part} onClick={run}>{busy ? "Checking…" : "Check draft and parting"}</button>
        </div>
      )}
      {d && pt && (
        <div className="prod-kpis">
          <div><b className={pt.undercuts.length ? "bad" : ""}>{pt.undercuts.length}</b><span>undercut faces{pt.undercuts.length ? ` (${pt.undercuts.reduce((a, u) => a + u.area_mm2, 0).toFixed(0)} mm²)` : ""}</span></div>
          <div><b className={d.ok ? "" : "bad"}>{(d.area_mm2.insufficient / 100).toFixed(1)} cm²</b><span>below {d.min_draft_deg}° draft</span></div>
          <div><b>{pt.parting_length_mm.toFixed(0)} mm</b><span>parting line, {pt.parting_edges} edges, {pt.parting_edges === 0 ? "undefined" : pt.flat ? "flat" : `stepped over ${(pt.parting_height_mm[1] - pt.parting_height_mm[0]).toFixed(1)} mm`}</span></div>
          <div><b>{(pt.projected_area_mm2 / 100).toFixed(1)} cm²</b><span>projected area</span></div>
          <div><b>{pt.clamp_kn.toFixed(0)} kN</b><span>clamp force ({(pt.clamp_kn / 9.80665).toFixed(1)} t)</span></div>
          <div><b>{pt.cavity_faces} / {pt.core_faces} / {pt.wall_faces}</b><span>cavity / core / wall faces</span></div>
        </div>
      )}
      {pt && <p className="small">{pt.verdict}.</p>}
      {error && <p className="error">{error}</p>}
    </section>
  );
}
