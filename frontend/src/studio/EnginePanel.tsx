import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import type { EngineAnalysis, EngineSpec } from "../api/types";

/** Engine workspace (Mechanical module): a piston engine analysed as it is edited (cycle,
 * torque and power from the BMEP curve, slider-crank kinematics, primary and secondary
 * balance), built as coloured parts and published to the shared inventory
 * (backend mech/piston.py, modules/mechanical). */

type NumKey = { [K in keyof EngineSpec]: EngineSpec[K] extends number ? K : never }[keyof EngineSpec];
const FIELDS: [NumKey, string, string, number][] = [
  ["cylinders", "cylinders", "", 1], ["bore", "bore", "mm", 0.5], ["stroke", "stroke", "mm", 0.5],
  ["rod_ratio", "rod / stroke", "", 0.05], ["compression_ratio", "compression ratio", "", 0.1],
  ["bmep_max", "peak BMEP", "bar", 0.5], ["rpm_idle", "idle", "rpm", 50],
  ["rpm_peak_torque", "peak torque at", "rpm", 100], ["rpm_max", "rev limit", "rpm", 100],
];

function Curve({ out }: { out: EngineAnalysis }) {
  const w = 460, h = 220, pad = 34;
  const pts = out.curve;
  const r0 = pts[0].rpm, r1 = pts[pts.length - 1].rpm;
  const tMax = Math.max(...pts.map((p) => p.torque_nm)) * 1.15;
  const pMax = Math.max(...pts.map((p) => p.power_kw)) * 1.15;
  const x = (r: number) => pad + ((r - r0) / (r1 - r0)) * (w - 2 * pad);
  const yT = (t: number) => h - pad - (t / tMax) * (h - 2 * pad);
  const yP = (p: number) => h - pad - (p / pMax) * (h - 2 * pad);
  const path = (f: (p: (typeof pts)[number]) => number) =>
    pts.map((p, i) => `${i ? "L" : "M"}${x(p.rpm).toFixed(1)},${f(p).toFixed(1)}`).join(" ");
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((f) => r0 + f * (r1 - r0));
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="engine-curve" role="img" aria-label="Torque and power curves">
      <line x1={pad} y1={h - pad} x2={w - pad} y2={h - pad} className="axis" />
      {ticks.map((r) => (
        <g key={r}><line x1={x(r)} y1={pad} x2={x(r)} y2={h - pad} className="grid" />
          <text x={x(r)} y={h - pad + 14} textAnchor="middle">{Math.round(r)}</text></g>
      ))}
      <path d={path((p) => yT(p.torque_nm))} className="torque" />
      <path d={path((p) => yP(p.power_kw))} className="power" />
      <text x={pad} y={pad - 10} className="torque-t">torque, N·m (max {out.peak_torque_nm.toFixed(0)})</text>
      <text x={w - pad} y={pad - 10} textAnchor="end" className="power-t">power, kW (max {out.peak_power_kw.toFixed(0)})</text>
      <text x={w / 2} y={h - 4} textAnchor="middle">engine speed, rpm</text>
    </svg>
  );
}

export function EnginePanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [spec, setSpec] = useState<EngineSpec | null>(null);
  const [out, setOut] = useState<EngineAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const timer = useRef<number | undefined>(undefined);
  const loaded = useRef(false);

  useEffect(() => {
    api.getEngineSpec(projectId).then((s) => { setSpec(s); loaded.current = true; })
      .catch((e) => setError(String(e.message ?? e)));
  }, [projectId]);
  useEffect(() => {
    if (!spec) return;
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      api.analyseEngine(spec).then((r) => { setOut(r); setError(null); })
        .catch((e) => setError(e instanceof Error ? e.message : String(e)));
      if (loaded.current) api.saveEngineSpec(projectId, spec).catch(() => undefined);
    }, 250);
  }, [spec, projectId]);

  if (!spec) return <div className="bench wide">{error ?? "Loading the engine…"}</div>;
  const set = <K extends keyof EngineSpec>(k: K, v: EngineSpec[K]) => setSpec({ ...spec, [k]: v });
  const act = async (f: () => Promise<string>) => {
    setBusy(true);
    try { setNote(await f()); } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    setBusy(false);
  };
  const build = () => act(async () => {
    const parts = await api.buildEngine(projectId, spec);
    onModelChanged();
    return `Built ${parts.length} parts: block, heads, cam covers, intake, exhaust, sump, flywheel, pulley${spec.turbo ? ", turbocharger" : ""}.`;
  });
  const publish = () => act(async () => {
    const item = await api.publishEngine(projectId);
    return `Published “${item.name}” v${item.version} to the inventory: vehicles, aircraft and boats can install it by its crank output and mounts.`;
  });

  return (
    <div className="bench wide engine">
      <div className="bench-side">
        <label className="row">name <input value={spec.name} onChange={(e) => set("name", e.target.value)} /></label>
        <div className="row3">
          <label>layout <select value={spec.layout} onChange={(e) => set("layout", e.target.value as EngineSpec["layout"])}>
            <option value="inline">inline</option><option value="V">V</option><option value="boxer">opposed (boxer)</option></select></label>
          <label>fuel <select value={spec.fuel} onChange={(e) => set("fuel", e.target.value as EngineSpec["fuel"])}>
            <option value="petrol">petrol</option><option value="diesel">diesel</option></select></label>
          <label className="check"><input type="checkbox" checked={spec.turbo} onChange={(e) => set("turbo", e.target.checked)} /> turbo</label>
        </div>
        {spec.layout === "V" && (
          <div className="row3">
            <label>bank angle <input type="number" value={spec.bank_angle} step={5} onChange={(e) => set("bank_angle", Number(e.target.value))} /> °</label>
            {spec.cylinders === 8 && <label className="check"><input type="checkbox" checked={spec.flat_plane} onChange={(e) => set("flat_plane", e.target.checked)} /> flat-plane crank</label>}
          </div>
        )}
        <div className="fields">
          {FIELDS.map(([k, label, unit, step]) => (
            <label key={k}><span>{label}</span>
              <input type="number" value={spec[k]} step={step} onChange={(e) => set(k, Number(e.target.value) as never)} />
              <span className="muted">{unit}</span></label>
          ))}
        </div>
        <div className="buttons">
          <button className="primary" disabled={busy} onClick={build}>Build engine</button>
          <button disabled={busy} onClick={publish}>Publish to inventory</button>
        </div>
        {note && <p className="small">{note}</p>}
        {error && <p className="error">{error}</p>}
      </div>
      <div className="bench-detail">
        {out && (
          <>
            <div className="figures">
              <div><b>{out.displacement_l.toFixed(2)} L</b><span>displacement</span></div>
              <div><b>{out.peak_power_kw.toFixed(0)} kW</b><span>at {out.peak_power_rpm.toFixed(0)} rpm ({(out.peak_power_kw * 1.341).toFixed(0)} hp)</span></div>
              <div><b>{out.peak_torque_nm.toFixed(0)} N·m</b><span>{out.torque_band_rpm[1] - out.torque_band_rpm[0] > 200
                ? `${out.torque_band_rpm[0].toFixed(0)}–${out.torque_band_rpm[1].toFixed(0)} rpm`
                : `at ${out.peak_torque_rpm.toFixed(0)} rpm`}</span></div>
              <div><b>{out.specific_power_kw_per_l.toFixed(0)} kW/L</b><span>specific power</span></div>
              <div><b>{out.mass_kg.toFixed(0)} kg</b><span>dry (estimate)</span></div>
              <div><b>{out.firing_order}</b><span>firing order</span></div>
            </div>
            <Curve out={out} />
            <div className="engine-grid">
              <section>
                <h4>Checks</h4>
                {out.checks.map((c) => <div key={c.id} className={`check ${c.status}`}><span className="badge">{c.status}</span><b>{c.label}</b><br />{c.message}</div>)}
              </section>
              <section>
                <h4>Balance (units of one cylinder's primary force)</h4>
                <table><tbody>
                  {Object.entries(out.balance).map(([k, v]) => (
                    <tr key={k}><td>{k.replace("_", " ")}</td><td className="num">{v < 1e-9 ? "0 (balanced)" : v.toFixed(3)}</td>
                      <td className="num muted">{out.balance_n[k] !== undefined && v > 1e-9 ? `${(out.balance_n[k] / 1000).toFixed(1)} kN at the rev limit` : ""}</td></tr>
                  ))}
                </tbody></table>
                <h4>Cycle and kinematics</h4>
                <table><tbody>
                  <tr><td>air-standard efficiency</td><td className="num">{(out.efficiency.air_standard * 100).toFixed(1)} %</td></tr>
                  <tr><td>fuel-air approximation (γ = 1.3)</td><td className="num">{(out.efficiency.fuel_air_approx * 100).toFixed(1)} %</td></tr>
                  <tr><td>mean piston speed at the limit</td><td className="num">{out.mean_piston_speed_ms.toFixed(1)} m/s</td></tr>
                  <tr><td>rod length</td><td className="num">{out.kinematics.rod_length_mm.toFixed(1)} mm</td></tr>
                  <tr><td>λ = r / l</td><td className="num">{out.kinematics.lambda.toFixed(3)}</td></tr>
                  <tr><td>reciprocating mass per cylinder</td><td className="num">{out.kinematics.reciprocating_mass_kg.toFixed(3)} kg</td></tr>
                </tbody></table>
                <p className="muted small">Ideal cycles bound real efficiency (real brake efficiency is roughly half to two thirds of them); the BMEP curve is an assumed shape, not a combustion model.</p>
              </section>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
