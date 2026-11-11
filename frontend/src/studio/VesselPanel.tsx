import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";

/** Vessel workspace (Marine module): a parametric displacement hull analysed as it is
 * edited: hydrostatics, the GZ curve against the IMO intact stability criteria, and the
 * viscous resistance (a lower bound: wave-making not modelled yet); built as coloured parts
 * (backend marine/hull.py, modules/marine). */

interface Spec { name: string; length: number; beam: number; draft: number; depth: number; cp: number; cm: number; transom: number; kg: number; speed_kn: number; material: string; twin_shaft: boolean; bow_thruster: boolean }
interface Out {
  hydrostatics: Record<string, number>; gz: { angle: number; gz_m: number }[];
  criteria: { criterion: string; value: number; limit: number; unit: string; pass: boolean }[];
  resistance: Record<string, number>[];
}
type NumKey = Exclude<keyof Spec, "name" | "material" | "twin_shaft" | "bow_thruster">;
const FIELDS: [NumKey, string, string, number][] = [
  ["length", "waterline length", "m", 0.1], ["beam", "beam", "m", 0.05], ["draft", "draft", "m", 0.05],
  ["depth", "depth to deck", "m", 0.05], ["cp", "prismatic Cp", "", 0.01], ["cm", "midship Cm", "", 0.01],
  ["transom", "transom / beam", "", 0.05], ["kg", "KG (CG above keel)", "m", 0.05], ["speed_kn", "design speed", "kn", 0.5],
];

function GzChart({ gz, gm }: { gz: Out["gz"]; gm: number }) {
  const w = 440, h = 200, pad = 32;
  const max = Math.max(...gz.map((p) => p.gz_m), 0.25) * 1.15, min = Math.min(...gz.map((p) => p.gz_m), 0);
  const x = (a: number) => pad + (a / 80) * (w - 2 * pad);
  const y = (v: number) => h - pad - ((v - min) / (max - min)) * (h - 2 * pad);
  const path = gz.map((p, i) => `${i ? "L" : "M"}${x(p.angle).toFixed(1)},${y(p.gz_m).toFixed(1)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="gz" role="img" aria-label="GZ curve">
      <line x1={pad} y1={y(0)} x2={w - pad} y2={y(0)} className="axis" />
      {[0, 20, 30, 40, 60, 80].map((a) => <g key={a}><line x1={x(a)} y1={pad} x2={x(a)} y2={h - pad} className="grid" /><text x={x(a)} y={h - pad + 13} textAnchor="middle">{a}°</text></g>)}
      <line x1={x(0)} y1={y(0)} x2={x(57.3)} y2={y(gm)} className="gm" />
      <line x1={pad} y1={y(0.2)} x2={w - pad} y2={y(0.2)} className="limit" />
      <path d={path} className="curve" />
      <text x={pad} y={pad - 8}>GZ (m) · dashed: GM slope and the 0.20 m criterion</text>
    </svg>
  );
}

export function VesselPanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [spec, setSpec] = useState<Spec | null>(null);
  const [out, setOut] = useState<Out | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const timer = useRef<number | undefined>(undefined);
  const loaded = useRef(false);
  useEffect(() => {
    api.getVesselSpec(projectId).then((s) => { setSpec(s as Spec); loaded.current = true; })
      .catch((e) => setError(String(e.message ?? e)));
  }, [projectId]);
  useEffect(() => {
    if (!spec) return;
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      api.analyseVessel(spec).then((r) => { setOut(r as Out); setError(null); })
        .catch((e) => setError(e instanceof Error ? e.message : String(e)));
      if (loaded.current) api.saveVesselSpec(projectId, spec).catch(() => undefined);
    }, 300);
  }, [spec, projectId]);
  if (!spec) return <div className="bench wide">{error ?? "Loading the vessel…"}</div>;
  const set = <K extends keyof Spec>(k: K, v: Spec[K]) => setSpec({ ...spec, [k]: v });
  const build = async () => {
    try {
      const parts = await api.buildVessel(projectId, spec);
      setNote(`Built ${(parts as unknown[]).length} parts: hull, deckhouse, windows, mast, propeller${spec.twin_shaft ? "s" : ""} and rudder${spec.twin_shaft ? "s" : ""}.`);
      onModelChanged();
    } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
  };
  const hs = out?.hydrostatics;
  const design = out?.resistance.find((r) => Math.abs(r.speed_kn - spec.speed_kn) < 1e-6);
  return (
    <div className="bench wide engine vessel">
      <div className="bench-side">
        <label className="row">name <input value={spec.name} onChange={(e) => set("name", e.target.value)} /></label>
        <div className="row3">
          <label>material <select value={spec.material} onChange={(e) => set("material", e.target.value)}>
            <option value="steel">steel</option><option value="aluminium">aluminium</option><option value="grp">GRP</option></select></label>
          <label className="check"><input type="checkbox" checked={spec.twin_shaft} onChange={(e) => set("twin_shaft", e.target.checked)} /> twin shaft</label>
          <label className="check"><input type="checkbox" checked={spec.bow_thruster} onChange={(e) => set("bow_thruster", e.target.checked)} /> bow thruster</label>
        </div>
        <div className="fields">
          {FIELDS.map(([k, label, unit, step]) => (
            <label key={k}><span>{label}</span>
              <input type="number" value={spec[k]} step={step} onChange={(e) => set(k, Number(e.target.value))} />
              <span className="muted">{unit}</span></label>
          ))}
        </div>
        <div className="buttons"><button className="primary" onClick={build}>Build vessel</button></div>
        {note && <p className="small">{note}</p>}
        {error && <p className="error">{error}</p>}
      </div>
      <div className="bench-detail">
        {hs && out && (
          <>
            <div className="figures">
              <div><b>{hs.displacement_t.toFixed(1)} t</b><span>displacement</span></div>
              <div><b>{hs.gm_m.toFixed(2)} m</b><span>GM (KM {hs.km_m.toFixed(2)} m)</span></div>
              <div><b>{hs.cb.toFixed(3)}</b><span>block coefficient</span></div>
              <div><b>{hs.tpc_t.toFixed(3)} t/cm</b><span>immersion</span></div>
              <div><b>{hs.lcb_m.toFixed(2)} m</b><span>LCB from AP</span></div>
              {design && <div><b>≥ {design.delivered_power_kw_lower_bound.toFixed(0)} kW</b><span>delivered power at {spec.speed_kn} kn (Fn {design.froude.toFixed(2)}, viscous only)</span></div>}
            </div>
            <div className="engine-grid">
              <section>
                <h4>Intact stability</h4>
                <GzChart gz={out.gz} gm={hs.gm_m} />
                {out.criteria.map((c) => (
                  <div key={c.criterion} className={`check ${c.pass ? "pass" : "fail"}`}>
                    <span className="badge">{c.pass ? "pass" : "fail"}</span>{c.criterion}: <b>{c.value.toFixed(3)}</b> {c.unit} (≥ {c.limit})
                  </div>
                ))}
                <p className="muted small">IMO IS Code 2008 Part A 2.2 general criteria; downflooding and the weather criterion not yet included.</p>
              </section>
              <section>
                <h4>Resistance (viscous: ITTC-1957 friction with form factor)</h4>
                <table><thead><tr><th>kn</th><th className="num">Fn</th><th className="num">R kN</th><th className="num">P_E kW</th><th className="num">P_D kW</th></tr></thead>
                  <tbody>{out.resistance.map((r) => (
                    <tr key={r.speed_kn}><td>{r.speed_kn.toFixed(1)}</td><td className="num">{r.froude.toFixed(2)}</td>
                      <td className="num">{(r.viscous_resistance_n / 1000).toFixed(2)}</td><td className="num">{r.effective_power_kw_lower_bound.toFixed(1)}</td>
                      <td className="num">{r.delivered_power_kw_lower_bound.toFixed(1)}</td></tr>
                  ))}</tbody></table>
                <p className="muted small">Lower bound: wave-making resistance is not modelled yet and grows quickly above Fn ≈ 0.25–0.3. Delivered power assumes a propulsive efficiency of 0.6.</p>
                <h4>Hydrostatics at the design draft</h4>
                <table><tbody>
                  {["volume_m3", "kb_m", "bm_m", "bml_m", "waterplane_m2", "lcf_m", "mct_tm"].map((k) => <tr key={k}><td>{k.replace(/_/g, " ")}</td><td className="num">{hs[k].toFixed(3)}</td></tr>)}
                </tbody></table>
              </section>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
