import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import type { AircraftAnalysis, AircraftSpec } from "../api/types";

/** Aircraft workspace: a parametric light aircraft analysed as you edit it (lifting
 * line, drag build-up, neutral point, performance), built as a Part Design part on
 * demand (backend aero/). */

type Field = [keyof AircraftSpec, string, string, number]; // key, label, unit, step

const GROUPS: { title: string; fields: Field[] }[] = [
  { title: "Wing", fields: [["wing_span", "span", "m", 0.1], ["wing_root_chord", "root chord", "m", 0.05],
    ["wing_tip_chord", "tip chord", "m", 0.05], ["wing_sweep", "sweep (LE)", "°", 1], ["wing_dihedral", "dihedral", "°", 0.5],
    ["wing_twist", "twist (tip)", "°", 0.5], ["wing_x", "root LE aft of nose", "m", 0.05], ["cl_max_section", "section c_l,max", "", 0.05]] },
  { title: "Horizontal tail", fields: [["htail_span", "span", "m", 0.1], ["htail_root_chord", "root chord", "m", 0.05],
    ["htail_tip_chord", "tip chord", "m", 0.05], ["htail_x", "root LE aft of nose", "m", 0.05]] },
  { title: "Fin", fields: [["fin_height", "height", "m", 0.05], ["fin_root_chord", "root chord", "m", 0.05],
    ["fin_tip_chord", "tip chord", "m", 0.05], ["fin_sweep", "sweep", "°", 1], ["fin_x", "root LE aft of nose", "m", 0.05]] },
  { title: "Fuselage", fields: [["fuselage_length", "length", "m", 0.1], ["fuselage_width", "width", "m", 0.05],
    ["fuselage_height", "height", "m", 0.05]] },
  { title: "Mass, power, mission", fields: [["mtow", "max take-off mass", "kg", 10], ["fuel_mass", "fuel", "kg", 5],
    ["x_cg", "CG aft of nose", "m", 0.02], ["power_kw", "engine power", "kW", 5], ["prop_diameter", "propeller diameter", "m", 0.05],
    ["prop_efficiency", "propeller efficiency", "", 0.01], ["bsfc", "fuel consumption", "g/kWh", 5],
    ["cruise_speed", "cruise speed (TAS)", "m/s", 1], ["cruise_altitude", "cruise altitude", "m", 100]] },
];

export function AircraftPanel({ projectId, onModelChanged }: { projectId?: string; onModelChanged: () => void }) {
  const [spec, setSpec] = useState<AircraftSpec | null>(null);
  const [out, setOut] = useState<AircraftAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [built, setBuilt] = useState<string | null>(null);
  const timer = useRef<number | undefined>(undefined);

  useEffect(() => { api.aircraftSpec().then((s) => setSpec(s.defaults)).catch((e) => setError(String(e.message ?? e))); }, []);
  useEffect(() => {
    if (!spec) return;
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      api.analyseAircraft(spec).then((r) => { setOut(r); setError(null); })
        .catch((e) => setError(e instanceof Error ? e.message : String(e)));
    }, 250);
  }, [spec]);

  if (!spec) return <div className="bench wide">{error ?? "Loading the aircraft…"}</div>;
  const set = (key: keyof AircraftSpec, value: number | boolean | string) => setSpec({ ...spec, [key]: value });
  const build = async () => {
    if (!projectId) return;
    setBusy(true);
    try {
      const part = await api.buildAircraft(projectId, spec);
      setBuilt(`Built as the part “${part.document.name}” (${part.document.features.length} features) — see it in the 3D view and Part Design`);
      onModelChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };
  const g = out?.geometry, a = out?.aero, st = out?.stability, p = out?.performance;

  return (
    <div className="bench wide aircraft">
      <div className="aircraft-form">
        <div className="row">
          <label>name <input value={spec.name} onChange={(e) => set("name", e.target.value)} /></label>
          <label>wing section NACA <input value={spec.wing_naca} maxLength={4} style={{ width: 52 }}
            onChange={(e) => /^\d{0,4}$/.test(e.target.value) && set("wing_naca", e.target.value)} /></label>
        </div>
        <div className="row">
          {(["high_wing", "t_tail", "tricycle", "fixed_gear"] as const).map((k) => (
            <label key={k}><input type="checkbox" checked={spec[k] as boolean} onChange={(e) => set(k, e.target.checked)} />
              {{ high_wing: "high wing", t_tail: "T-tail", tricycle: "tricycle gear", fixed_gear: "fixed gear" }[k]}</label>
          ))}
        </div>
        {GROUPS.map((grp) => (
          <fieldset key={grp.title}>
            <legend>{grp.title}</legend>
            {grp.fields.map(([key, label, unit, step]) => (
              <label key={key}>{label}
                <input type="number" step={step} value={spec[key] as number}
                  onChange={(e) => e.target.value !== "" && set(key, Number(e.target.value))} />
                <span className="muted">{unit}</span>
              </label>
            ))}
          </fieldset>
        ))}
        <div className="row">
          <button className="primary" disabled={busy || !projectId} onClick={build}>{busy ? "Building…" : "Build as a part"}</button>
          {built && <span className="good-text">{built}</span>}
        </div>
        {error && <div className="error">{error}</div>}
      </div>
      {out && g && a && st && p && (
        <div className="aircraft-results lab-side">
          <div className="checks">
            {out.checks.map((c) => (
              <div key={c.name} className={`check ${c.status}`} title={c.why}>
                <strong>{c.name}</strong> {c.value.toFixed(c.unit === "" ? 3 : 1)} {c.unit}
                <span className="muted"> (guide {c.range[0]}–{c.range[1] >= 1e8 ? "∞" : c.range[1]})</span>
                <span className="badge">{c.status}</span>
              </div>
            ))}
          </div>
          <div className="math">
            <div>S = {g.wing_area.toFixed(2)} m², AR = b²/S = {g.aspect_ratio.toFixed(2)}, λ = {g.taper.toFixed(2)}, MAC = {g.mac.toFixed(3)} m at y = {g.mac_y.toFixed(2)} m</div>
            <div>Lifting line: a_w = {a.wing_lift_slope.toFixed(3)} /rad, a_t = {a.tail_lift_slope.toFixed(3)} /rad, span efficiency {a.span_efficiency.toFixed(3)}, α₀ = {a.zero_lift_angle.toFixed(2)}°</div>
            <div>Cruise at {out.atmosphere.altitude.toFixed(0)} m: ρ = {out.atmosphere.rho.toFixed(4)} kg/m³, M = {out.atmosphere.mach.toFixed(3)}, q = {out.atmosphere.q.toFixed(0)} Pa → C_L = W/(qS) = {a.cl_cruise.toFixed(3)} at α = {a.alpha_cruise.toFixed(2)}°</div>
            <div>C_D = C_D0 + C_L²/(π AR e) = {a.cd0.toFixed(4)} + {(a.cd_cruise - a.cd0).toFixed(4)} = {a.cd_cruise.toFixed(4)} (e = {a.oswald_e.toFixed(3)}) → L/D = {a.l_over_d.toFixed(2)}, (L/D)max = {a.ld_max.toFixed(2)} at {a.v_ld_max.toFixed(1)} m/s</div>
            <div>dε/dα = 2a_w/(πAR) = {a.downwash_gradient.toFixed(3)}; x_ac,w = {st.x_ac_wing.toFixed(3)} m, x_ac,t = {st.x_ac_tail.toFixed(3)} m → x_np = {st.x_np.toFixed(3)} m, x_cg = {st.x_cg.toFixed(3)} m</div>
            <div>Static margin (x_np − x_cg)/MAC = {(100 * st.static_margin).toFixed(1)} %; V_H = {st.v_h.toFixed(3)}, V_V = {st.v_v.toFixed(4)}</div>
            <div>Power required DV/η = {p.power_required.toFixed(1)} kW of {p.power_available.toFixed(1)} kW available · V_stall = {p.v_stall.toFixed(1)} m/s ({(p.v_stall / 0.514444).toFixed(0)} kt) · W/S = {p.wing_loading.toFixed(1)} kg/m²</div>
            <div>Breguet: range {p.range_km.toFixed(0)} km, endurance {p.endurance_h.toFixed(1)} h at cruise</div>
          </div>
          <div className="aircraft-charts">
            <SpanLoading y={a.span_y} cl={a.span_cl} span={spec.wing_span} />
            <Polar polar={a.polar} cd0={a.cd0} cruise={[a.cd_cruise, a.cl_cruise]} />
            <Stations mac={[g.mac_x, g.mac]} cg={st.x_cg} np={st.x_np} length={spec.fuselage_length} />
          </div>
          <table className="drag-table">
            <thead><tr><th>component</th><th>Re</th><th>C_f</th><th>FF</th><th>Q</th><th>S_wet m²</th><th>ΔC_D0</th></tr></thead>
            <tbody>
              {a.components.map((c) => (
                <tr key={c.name}><td>{c.name}</td><td>{c.re.toExponential(2)}</td><td>{c.cf.toFixed(5)}</td><td>{c.ff.toFixed(3)}</td>
                  <td>{c.q.toFixed(2)}</td><td>{c.s_wet.toFixed(2)}</td><td>{c.cd0.toFixed(5)}</td></tr>
              ))}
              <tr><td>landing gear</td><td colSpan={5} className="muted">D/q = 0.18 m² faired fixed tricycle</td><td>{a.gear_cd0.toFixed(5)}</td></tr>
              <tr><td><strong>C_D0</strong></td><td colSpan={5} className="muted">× 1.05 leakage and protuberances</td><td><strong>{a.cd0.toFixed(5)}</strong></td></tr>
            </tbody>
          </table>
          <details>
            <summary>Assumptions</summary>
            <ul className="assumptions">{out.assumptions.map((x) => <li key={x}>{x}</li>)}</ul>
          </details>
        </div>
      )}
    </div>
  );
}

function SpanLoading({ y, cl, span }: { y: number[]; cl: number[]; span: number }) {
  const W = 300, H = 110, L = 30;
  const half = span / 2;
  const pts = y.map((v, i) => [-v, cl[i]] as const).concat([[half, 0]]);
  const hi = Math.max(...cl, 0.01) * 1.15;
  const x = (v: number) => L + (v / half) * (W - L - 8);
  const yy = (v: number) => H - 18 - (v / hi) * (H - 30);
  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Spanwise lift coefficient">
      <text x={L} y={10} className="chart-title">local c_l along the semi-span (lifting line)</text>
      <line x1={L} x2={W - 6} y1={yy(0)} y2={yy(0)} className="grid" />
      <path fill="none" stroke="#6fa8ff" strokeWidth={1.6} d={pts.map(([a, b], i) => `${i ? "L" : "M"}${x(a).toFixed(1)},${yy(b).toFixed(1)}`).join("")} />
      <text x={L - 3} y={yy(hi / 1.15) + 3} textAnchor="end" className="tick">{(hi / 1.15).toFixed(2)}</text>
      <text x={L} y={H - 4} className="tick">root</text><text x={W - 6} y={H - 4} textAnchor="end" className="tick">tip {half.toFixed(2)} m</text>
    </svg>
  );
}

function Polar({ polar, cd0, cruise }: { polar: { cl: number; cd: number }[]; cd0: number; cruise: [number, number] }) {
  const W = 300, H = 120, L = 34;
  const cdHi = Math.max(...polar.map((p) => p.cd)) * 1.05, clHi = Math.max(...polar.map((p) => p.cl)) * 1.05;
  const x = (cd: number) => L + (cd / cdHi) * (W - L - 8);
  const y = (cl: number) => H - 16 - (cl / clHi) * (H - 28);
  // the tangent from the origin touches the polar at (L/D)max
  const best = polar.reduce((b, p) => (p.cl / p.cd > b.cl / b.cd ? p : b), polar[1] ?? polar[0]);
  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Drag polar">
      <text x={L} y={10} className="chart-title">drag polar C_L vs C_D (C_D0 = {cd0.toFixed(4)})</text>
      <line x1={L} x2={W - 6} y1={y(0)} y2={y(0)} className="grid" /><line x1={L} x2={L} y1={8} y2={y(0)} className="grid" />
      <path fill="none" stroke="#6fa8ff" strokeWidth={1.6} d={polar.map((p, i) => `${i ? "L" : "M"}${x(p.cd).toFixed(1)},${y(p.cl).toFixed(1)}`).join("")} />
      <line x1={x(0)} y1={y(0)} x2={x(best.cd * 1.6)} y2={y(best.cl * 1.6)} stroke="#58c08a" strokeDasharray="3 2" strokeWidth={1} />
      <circle cx={x(cruise[0])} cy={y(cruise[1])} r={3} fill="#ffc94a"><title>cruise</title></circle>
      <text x={x(best.cd) + 4} y={y(best.cl) + 10} className="tick">(L/D)max</text>
      <text x={x(cruise[0]) + 5} y={y(cruise[1]) + 3} className="tick">cruise</text>
    </svg>
  );
}

function Stations({ mac, cg, np, length }: { mac: [number, number]; cg: number; np: number; length: number }) {
  const W = 300, H = 62, L = 8;
  const x = (v: number) => L + (v / length) * (W - 2 * L);
  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="CG and neutral point">
      <text x={L} y={10} className="chart-title">along the fuselage (nose left): MAC, CG, neutral point</text>
      <rect x={x(0)} y={26} width={x(length) - x(0)} height={10} rx={5} fill="#2a3442" />
      <rect x={x(mac[0])} y={22} width={x(mac[0] + mac[1]) - x(mac[0])} height={18} fill="rgba(111,168,255,0.25)" stroke="#6fa8ff" strokeWidth={0.8} />
      <line x1={x(cg)} x2={x(cg)} y1={16} y2={46} stroke="#ffc94a" strokeWidth={2} />
      <line x1={x(np)} x2={x(np)} y1={16} y2={46} stroke="#58c08a" strokeWidth={2} />
      <text x={x(cg)} y={56} textAnchor="middle" className="tick">CG</text>
      <text x={x(np)} y={56} textAnchor="middle" className="tick">NP</text>
    </svg>
  );
}
