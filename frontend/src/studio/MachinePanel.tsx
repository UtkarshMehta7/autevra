import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import { EnginePanel } from "./EnginePanel";

/** Engine workspace with the engine category (Mechanical module): piston engines (the
 * EnginePanel), electric machines (torque from air-gap shear stress, envelope, efficiency
 * map) and gas turbines (station-by-station turbojet or turboshaft cycle). The category is
 * saved with the project and selects its breakdown, architecture and loads. */

type Category = "piston" | "electric" | "turbine";
type Spec = Record<string, number | string | boolean>;

function useSpec(load: () => Promise<unknown>, save: (s: Spec) => Promise<unknown>, analyse: (s: Spec) => Promise<unknown>) {
  const [spec, setSpec] = useState<Spec | null>(null);
  const [out, setOut] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const timer = useRef<number | undefined>(undefined);
  useEffect(() => { load().then((s) => setSpec(s as Spec)).catch((e) => setError(String(e.message ?? e))); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!spec) return;
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      analyse(spec).then((r) => { setOut(r as Record<string, unknown>); setError(null); })
        .catch((e) => setError(e instanceof Error ? e.message : String(e)));
      save(spec).catch(() => undefined);
    }, 250);
  }, [spec]); // eslint-disable-line react-hooks/exhaustive-deps
  return { spec, setSpec, out, error };
}

function Fields({ spec, setSpec, fields }: { spec: Spec; setSpec: (s: Spec) => void; fields: [string, string, string, number][] }) {
  return (
    <div className="fields">
      {fields.map(([k, label, unit, step]) => (
        <label key={k}><span>{label}</span>
          <input type="number" value={Number(spec[k])} step={step} onChange={(e) => setSpec({ ...spec, [k]: Number(e.target.value) })} />
          <span className="muted">{unit}</span></label>
      ))}
    </div>
  );
}

function Motor({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const { spec, setSpec, out, error } = useSpec(() => api.getMotorSpec(projectId), (s) => api.saveMotorSpec(projectId, s), api.analyseMotor);
  const [note, setNote] = useState<string | null>(null);
  if (!spec) return <p>{error ?? "Loading…"}</p>;
  const o = out as { peak_power_kw: number; peak_torque_nm: number; continuous_power_kw: number; mass_kg: number; power_density_kw_per_kg: number; peak_efficiency: number;
    curve: { rpm: number; torque_nm: number; power_kw: number }[]; efficiency_map: { rpm: number[]; torque_nm: number[]; eta: (number | null)[][] };
    checks: { id: string; label: string; status: string; message: string }[] } | null;
  return (
    <div className="bench wide engine">
      <div className="bench-side">
        <label className="row">name <input value={String(spec.name)} onChange={(e) => setSpec({ ...spec, name: e.target.value })} /></label>
        <Fields spec={spec} setSpec={setSpec} fields={[["stator_diameter", "stator diameter", "mm", 5], ["stack_length", "stack length", "mm", 5],
          ["rotor_ratio", "rotor / stator", "", 0.01], ["poles", "poles", "", 2], ["shear_peak_kpa", "peak shear stress", "kPa", 1],
          ["shear_continuous_kpa", "continuous shear", "kPa", 1], ["base_rpm", "base speed", "rpm", 100], ["max_rpm", "maximum speed", "rpm", 500], ["voltage", "DC link", "V", 10]]} />
        <div className="buttons">
          <button className="primary" onClick={async () => { const p = await api.buildMachine(projectId); onModelChanged(); setNote(`Built ${(p as unknown[]).length} parts.`); }}>Build machine</button>
          <button onClick={async () => { const it = (await api.publishMotor(projectId)) as { name: string; version: string }; setNote(`Published “${it.name}” v${it.version}: install it in a car (it becomes battery electric) or an aircraft.`); }}>Publish to inventory</button>
        </div>
        {note && <p className="small">{note}</p>}{error && <p className="error">{error}</p>}
      </div>
      <div className="bench-detail">
        {o && (
          <>
            <div className="figures">
              <div><b>{o.peak_power_kw.toFixed(0)} kW</b><span>peak ({o.continuous_power_kw.toFixed(0)} continuous)</span></div>
              <div><b>{o.peak_torque_nm.toFixed(0)} N·m</b><span>peak torque</span></div>
              <div><b>{o.mass_kg.toFixed(1)} kg</b><span>{o.power_density_kw_per_kg.toFixed(1)} kW/kg</span></div>
              <div><b>{(o.peak_efficiency * 100).toFixed(1)} %</b><span>peak efficiency</span></div>
            </div>
            <div className="engine-grid">
              <section>
                <h4>Efficiency map (torque vs speed)</h4>
                <div className="effmap" style={{ gridTemplateColumns: `repeat(${o.efficiency_map.rpm.length}, 1fr)` }}>
                  {[...o.efficiency_map.eta].reverse().flatMap((row, i) => row.map((e, j) => (
                    <i key={`${i}-${j}`} title={e === null ? "outside the envelope" : `${(e * 100).toFixed(1)} %`}
                      style={{ background: e === null ? "transparent" : `hsl(${Math.max(0, (e - 0.8) / 0.18) * 120}, 60%, 42%)` }} />
                  )))}
                </div>
                <p className="muted small">Red 80 % → green 98 %; blank: beyond the peak torque–speed envelope. Loss model stated in the backend.</p>
              </section>
              <section>
                <h4>Checks</h4>
                {o.checks.map((c) => <div key={c.id} className={`check ${c.status}`}><span className="badge">{c.status}</span><b>{c.label}</b><br />{c.message}</div>)}
              </section>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function Turbine({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const { spec, setSpec, out, error } = useSpec(() => api.getTurbineSpec(projectId), (s) => api.saveTurbineSpec(projectId, s), api.analyseTurbine);
  if (!spec) return <p>{error ?? "Loading…"}</p>;
  const o = out as Record<string, number> & { stations: Record<string, { T_K: number; p_kPa: number }> } | null;
  return (
    <div className="bench wide engine">
      <div className="bench-side">
        <label className="row">name <input value={String(spec.name)} onChange={(e) => setSpec({ ...spec, name: e.target.value })} /></label>
        <div className="row3"><label>type <select value={String(spec.kind)} onChange={(e) => setSpec({ ...spec, kind: e.target.value })}>
          <option value="turbojet">turbojet</option><option value="turboshaft">turboshaft</option></select></label></div>
        <Fields spec={spec} setSpec={setSpec} fields={[["pressure_ratio", "pressure ratio", "", 0.5], ["tit_k", "turbine entry T", "K", 10],
          ["mass_flow", "mass flow", "kg/s", 0.5], ["eta_c", "compressor η", "", 0.01], ["eta_t", "turbine η", "", 0.01],
          ["mach", "flight Mach", "", 0.05], ["altitude", "altitude", "m", 500]]} />
        <div className="buttons"><button className="primary" onClick={async () => { await api.buildMachine(projectId); onModelChanged(); }}>Build engine</button></div>
        {error && <p className="error">{error}</p>}
      </div>
      <div className="bench-detail">
        {o && (
          <>
            <div className="figures">
              {o.thrust_kn !== undefined && <div><b>{o.thrust_kn.toFixed(2)} kN</b><span>thrust ({o.specific_thrust.toFixed(0)} N·s/kg)</span></div>}
              {o.tsfc_g_per_kn_s !== undefined && <div><b>{o.tsfc_g_per_kn_s.toFixed(1)}</b><span>TSFC g/(kN·s)</span></div>}
              {o.shaft_power_kw !== undefined && <div><b>{o.shaft_power_kw.toFixed(0)} kW</b><span>shaft power ({o.sfc_g_per_kwh.toFixed(0)} g/kWh)</span></div>}
              <div><b>{(o.thermal_efficiency * 100).toFixed(1)} %</b><span>thermal efficiency</span></div>
              <div><b>{o.mass_kg.toFixed(0)} kg</b><span>statistical mass</span></div>
            </div>
            <h4>Stations</h4>
            <table><thead><tr><th>station</th><th className="num">T K</th><th className="num">p kPa</th></tr></thead>
              <tbody>{Object.entries(o.stations).map(([k, v]) => <tr key={k}><td>{({ 0: "ambient", 2: "compressor inlet", 3: "compressor exit", 4: "turbine entry", 5: "turbine exit" } as Record<string, string>)[k] ?? k}</td><td className="num">{v.T_K}</td><td className="num">{v.p_kPa}</td></tr>)}</tbody></table>
            <p className="muted small">Design-point cycle with constant specific heats per stream; no cooling bleed or off-design matching.</p>
          </>
        )}
      </div>
    </div>
  );
}

export function MachinePanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [cat, setCat] = useState<Category | null>(null);
  useEffect(() => { api.engineCategory(projectId).then((r) => setCat(r.category as Category)).catch(() => setCat("piston")); }, [projectId]);
  if (!cat) return <div className="bench wide">Loading…</div>;
  const choose = async (c: Category) => { await api.setEngineCategory(projectId, c); setCat(c); };
  return (
    <div className="machine">
      <div className="bench-controls">
        {(["piston", "electric", "turbine"] as Category[]).map((c) => (
          <button key={c} className={cat === c ? "active" : ""} onClick={() => choose(c)}>
            {{ piston: "Piston engine", electric: "Electric machine", turbine: "Gas turbine" }[c]}</button>
        ))}
        <span className="muted small">The category selects the breakdown, architecture and loads of this project.</span>
      </div>
      {cat === "piston" && <EnginePanel key="p" projectId={projectId} onModelChanged={onModelChanged} />}
      {cat === "electric" && <Motor key="e" projectId={projectId} onModelChanged={onModelChanged} />}
      {cat === "turbine" && <Turbine key="t" projectId={projectId} onModelChanged={onModelChanged} />}
    </div>
  );
}
