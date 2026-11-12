import { useEffect, useMemo, useState } from "react";
import { api, type FourBarOut, type SliderCrankOut, type SweepReport } from "../api/client";
import type { PartOut } from "../api/types";

/** Mechanisms (Reviews workspace, every module): move a part through a joint's range and
 * report its closest approach to every other part, add the swept envelope as a part, and
 * closed-form linkage calculators (backend autevra/mechanisms.py). */

const num = (v: string) => (Number.isFinite(Number(v)) ? Number(v) : 0);

function Field({ label, value, onChange, step = 1, unit }: { label: string; value: number; onChange: (v: number) => void; step?: number; unit?: string }) {
  return <label>{label} <input type="number" value={value} step={step} onChange={(e) => onChange(num(e.target.value))} />{unit ? ` ${unit}` : ""}</label>;
}

function SweptMotion({ projectId, version, onModelChanged }: { projectId: string; version?: number; onModelChanged: () => void }) {
  const [parts, setParts] = useState<PartOut[]>([]);
  const [part, setPart] = useState("");
  const [joint, setJoint] = useState({ kind: "revolute", origin: [0, 0, 0], axis: [0, 0, 1], lo: -30, hi: 30, steps: 13 });
  const [required, setRequired] = useState(5);
  const [report, setReport] = useState<SweepReport | null>(null);
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const loadParts = () => api.parts(projectId).then((p) => { setParts(p); setPart((cur) => cur || (p[0]?.id ?? "")); }).catch(() => undefined);
  useEffect(() => { loadParts(); }, [projectId, version]);  // eslint-disable-line react-hooks/exhaustive-deps
  const vec = (key: "origin" | "axis", i: number, v: number) => setJoint({ ...joint, [key]: joint[key].map((x, j) => (j === i ? v : x)) });
  const run = async (f: () => Promise<void>) => {
    setBusy(true); setNote(null);
    try { await f(); } catch (e) { setNote(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };
  const unit = joint.kind === "revolute" ? "°" : "mm";
  return (
    <section className="mech-sweep">
      <h4>Swept motion (clearance through a joint's range)</h4>
      {parts.length === 0 ? <p className="small muted">Add parts to the project (Part Design, Inventory or Routing) to move one of them.</p> : (
        <>
          <div className="row wrap">
            <label>part <select value={part} onChange={(e) => { setPart(e.target.value); setReport(null); }}>
              {parts.map((p) => <option key={p.id} value={p.id}>{p.document.name}</option>)}
            </select></label>
            <label>joint <select value={joint.kind} onChange={(e) => setJoint({ ...joint, kind: e.target.value })}>
              <option value="revolute">revolute (hinge)</option><option value="prismatic">prismatic (slide)</option>
            </select></label>
            <Field label="from" value={joint.lo} onChange={(v) => setJoint({ ...joint, lo: v })} unit={unit} />
            <Field label="to" value={joint.hi} onChange={(v) => setJoint({ ...joint, hi: v })} unit={unit} />
            <Field label="positions" value={joint.steps} onChange={(v) => setJoint({ ...joint, steps: Math.max(2, Math.min(73, Math.round(v))) })} />
          </div>
          <div className="row wrap">
            <span className="vec">axis point {[0, 1, 2].map((i) => <input key={i} type="number" aria-label={`axis point ${"xyz"[i]}`} value={joint.origin[i]} onChange={(e) => vec("origin", i, num(e.target.value))} />)} mm</span>
            <span className="vec">axis direction {[0, 1, 2].map((i) => <input key={i} type="number" aria-label={`axis direction ${"xyz"[i]}`} value={joint.axis[i]} onChange={(e) => vec("axis", i, num(e.target.value))} />)}</span>
            <Field label="required clearance" value={required} onChange={setRequired} unit="mm" />
            <button disabled={busy || !part} onClick={() => run(async () => setReport(await api.sweep(projectId, part, joint, required)))}>{busy ? "Moving…" : "Check the motion"}</button>
            <button disabled={busy || !part} onClick={() => run(async () => { const p = await api.addEnvelope(projectId, part, joint); setNote(`Added "${p.document.name}" to the project.`); await loadParts(); onModelChanged(); })}>Add envelope as a part</button>
          </div>
        </>
      )}
      {report && (
        <>
          <p className="small">
            {report.pairs.filter((p) => p.status === "clear").length} of {report.pairs.length} parts stay clear over {report.positions.length} sampled positions
            ({report.positions[0]} to {report.positions[report.positions.length - 1]} {report.unit}). Envelope box {report.box_min.map((v, i) => `${v.toFixed(0)}…${report.box_max[i].toFixed(0)}`).join(" × ")} mm.
            Between samples the true minimum can be smaller: raise the positions to tighten it.
          </p>
          <table className="bd-table"><tbody>
            {report.pairs.filter((p) => p.status !== "clear").map((p) => (
              <tr key={p.other}><td>{p.other_name}</td>
                <td><span className={`status ${p.status === "too close" ? "open" : "not-shown"}`}>{p.status}</span></td>
                <td className="num">{p.distance_mm.toFixed(1)} mm</td><td className="num">at {p.at} {report.unit}</td></tr>
            ))}
          </tbody></table>
        </>
      )}
      {note && <p className="small">{note}</p>}
    </section>
  );
}

function FourBar() {
  const [links, setLinks] = useState({ ground: 100, crank: 30, coupler: 90, rocker: 70, point_along: 45, point_off: 30 });
  const [out, setOut] = useState<FourBarOut | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(true);
  useEffect(() => {
    const t = setTimeout(() => api.fourbar({ ...links, steps: 120 }).then((o) => { setOut(o); setError(null); }).catch((e) => setError(String(e.message ?? e))), 150);
    return () => clearTimeout(t);
  }, [links]);
  const n = out?.poses.length ?? 0;
  useEffect(() => {
    if (!playing || n === 0) return undefined;
    const id = setInterval(() => setFrame((f) => (f + 1) % n), 50);
    return () => clearInterval(id);
  }, [playing, n]);
  const view = useMemo(() => {
    if (!out || n === 0) return null;
    const pts = out.poses.flatMap((p) => [p.b, p.c, p.p]).concat([[0, 0], [links.ground, 0]]);
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const pad = 12, x0 = Math.min(...xs) - pad, x1 = Math.max(...xs) + pad, y0 = Math.min(...ys) - pad, y1 = Math.max(...ys) + pad;
    return { box: `${x0} ${-y1} ${x1 - x0} ${y1 - y0}`, w: (x1 - x0) / 220 };
  }, [out, n, links.ground]);
  const pose = out && n ? out.poses[frame % n] : null;
  const set = (k: keyof typeof links) => (v: number) => setLinks({ ...links, [k]: v });
  return (
    <section className="mech-linkage">
      <h4>Four-bar linkage</h4>
      <div className="row wrap">
        <Field label="ground" value={links.ground} onChange={set("ground")} unit="mm" />
        <Field label="crank" value={links.crank} onChange={set("crank")} unit="mm" />
        <Field label="coupler" value={links.coupler} onChange={set("coupler")} unit="mm" />
        <Field label="rocker" value={links.rocker} onChange={set("rocker")} unit="mm" />
        <Field label="coupler point along" value={links.point_along} onChange={set("point_along")} unit="mm" />
        <Field label="off" value={links.point_off} onChange={set("point_off")} unit="mm" />
        <button onClick={() => setPlaying(!playing)}>{playing ? "Pause" : "Play"}</button>
      </div>
      {out && (
        <div className="mech-body">
          {view && pose && (
            <svg viewBox={view.box} className="mech-svg" role="img" aria-label="four-bar linkage">
              <polyline points={[...out.poses, out.poses[0]].map((p) => `${p.p[0]},${-p.p[1]}`).join(" ")} fill="none" stroke="var(--accent)" strokeWidth={view.w} strokeDasharray={out.full_rotation ? undefined : `${view.w * 3}`} opacity={0.7} />
              <line x1={0} y1={0} x2={links.ground} y2={0} stroke="var(--muted)" strokeWidth={view.w * 2} strokeDasharray={`${view.w * 4}`} />
              <polygon points={`${pose.b[0]},${-pose.b[1]} ${pose.c[0]},${-pose.c[1]} ${pose.p[0]},${-pose.p[1]}`} fill="rgba(79,143,230,0.18)" stroke="var(--text)" strokeWidth={view.w * 2} strokeLinejoin="round" />
              <line x1={0} y1={0} x2={pose.b[0]} y2={-pose.b[1]} stroke="#e6a23c" strokeWidth={view.w * 3} strokeLinecap="round" />
              <line x1={links.ground} y1={0} x2={pose.c[0]} y2={-pose.c[1]} stroke="#67c28a" strokeWidth={view.w * 3} strokeLinecap="round" />
              {[[0, 0], [links.ground, 0], pose.b, pose.c].map((p, i) => <circle key={i} cx={p[0]} cy={-p[1]} r={view.w * 3} fill="var(--panel)" stroke="var(--text)" strokeWidth={view.w} />)}
              <circle cx={pose.p[0]} cy={-pose.p[1]} r={view.w * 2.5} fill="var(--accent)" />
            </svg>
          )}
          <div className="mech-facts small">
            <span>class <b>{out.class}</b></span>
            <span>crank turns fully <b>{out.full_rotation ? "yes" : `no (${(out.assembled_fraction * 100).toFixed(0)} % of a turn)`}</b></span>
            {out.transmission_min_deg !== undefined && <span>transmission angle <b>{out.transmission_min_deg.toFixed(1)}° – {out.transmission_max_deg?.toFixed(1)}°</b></span>}
            {out.rocker_swing_deg !== undefined && <span>rocker swing <b>{out.rocker_swing_deg.toFixed(1)}°</b></span>}
            {pose && <span>now: crank {pose.theta_deg.toFixed(0)}°, transmission {pose.transmission_deg.toFixed(0)}°</span>}
            {out.warnings.map((w) => <span key={w} className="bad">{w}</span>)}
          </div>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </section>
  );
}

function Curve({ rows, pick, color, label }: { rows: SliderCrankOut["rows"]; pick: (row: SliderCrankOut["rows"][number]) => number; color: string; label: string }) {
  const vals = rows.map(pick), lo = Math.min(...vals), hi = Math.max(...vals), span = hi - lo || 1;
  const pts = rows.map((_row, i) => `${(i / (rows.length - 1)) * 300},${58 - ((vals[i] - lo) / span) * 54}`).join(" ");
  return (
    <svg viewBox="0 0 300 62" className="mech-curve" role="img" aria-label={label}>
      {lo < 0 && hi > 0 && <line x1={0} x2={300} y1={58 - ((0 - lo) / span) * 54} y2={58 - ((0 - lo) / span) * 54} stroke="var(--line)" strokeWidth={1} />}
      <polyline points={pts} fill="none" stroke={color} strokeWidth={1.6} />
      <text x={2} y={10} fill="var(--muted)" fontSize={9}>{label}</text>
    </svg>
  );
}

function SliderCrank() {
  const [sc, setSc] = useState({ crank: 40, rod: 140, offset: 0, rpm: 6000 });
  const [out, setOut] = useState<SliderCrankOut | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const t = setTimeout(() => api.sliderCrank({ ...sc, steps: 120 }).then((o) => { setOut(o); setError(null); }).catch((e) => { setOut(null); setError(String(e.message ?? e)); }), 150);
    return () => clearTimeout(t);
  }, [sc]);
  const set = (k: keyof typeof sc) => (v: number) => setSc({ ...sc, [k]: v });
  return (
    <section className="mech-linkage">
      <h4>Slider-crank</h4>
      <div className="row wrap">
        <Field label="crank" value={sc.crank} onChange={set("crank")} unit="mm" />
        <Field label="rod" value={sc.rod} onChange={set("rod")} unit="mm" />
        <Field label="offset" value={sc.offset} onChange={set("offset")} unit="mm" />
        <Field label="speed" value={sc.rpm} onChange={set("rpm")} step={100} unit="rpm" />
      </div>
      {out && (
        <div className="mech-body">
          <div className="mech-curves">
            <Curve rows={out.rows} pick={(r) => r.x_mm} color="var(--accent)" label="position, mm (one turn)" />
            <Curve rows={out.rows} pick={(r) => r.v_m_s} color="#67c28a" label="velocity, m/s" />
            <Curve rows={out.rows} pick={(r) => r.a_m_s2} color="#e6a23c" label="acceleration, m/s²" />
          </div>
          <div className="mech-facts small">
            <span>stroke <b>{out.stroke_mm.toFixed(2)} mm</b></span>
            <span>rod ratio l/r <b>{out.rod_ratio.toFixed(2)}</b></span>
            <span>peak slider speed <b>{out.v_max_m_s.toFixed(1)} m/s</b></span>
            <span>peak acceleration <b>{out.a_max_m_s2.toFixed(0)} m/s² ({(out.a_max_m_s2 / 9.80665).toFixed(0)} g)</b></span>
          </div>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </section>
  );
}

export function MechanismsPanel(props: { projectId: string; version?: number; onModelChanged: () => void }) {
  return (
    <div className="mechanisms">
      <SweptMotion {...props} />
      <div className="rev-grid"><FourBar /><SliderCrank /></div>
    </div>
  );
}
