import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { InventoryItem, ItemPort, ItemSummary } from "../api/types";

/** Inventory workspace (shared by every module): browse the standard-parts library and
 * published items, read their dimensions, ports and performance, size a bearing by its
 * ISO 281 life, and add an item to the current project as a part (backend inventory/). */

const CATEGORIES = ["", "Engines", "Fasteners", "Bearings", "Profiles", "Published"];

function fmt(v: number | string): string {
  if (typeof v !== "number") return v;
  return Math.abs(v) >= 1000 ? v.toFixed(0) : Math.abs(v) >= 10 ? v.toFixed(1) : v.toPrecision(3);
}

function label(key: string): string {
  return key.replace(/_/g, " ").replace(/\b(mm2|mm3|mm4|kN|Nm|kg)\b/g, (u) =>
    ({ mm2: "(mm²)", mm3: "(mm³)", mm4: "(mm⁴)", kN: "(kN)", Nm: "(N·m)", kg: "(kg)" })[u] ?? u);
}

export function InventoryPanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [rows, setRows] = useState<ItemSummary[]>([]);
  const [item, setItem] = useState<InventoryItem | null>(null);
  const [usage, setUsage] = useState<{ project: string; part: string; version: string }[]>([]);
  const [at, setAt] = useState({ x: 0, y: 0, z: 500 });
  const [load, setLoad] = useState(2);
  const [rpm, setRpm] = useState(1500);
  const [life, setLife] = useState<{ L10_Mrev: number; L10_hours: number } | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [installed, setInstalled] = useState<{ part: string; name: string; ports: ItemPort[] }[]>([]);
  const [mate, setMate] = useState({ part: "", port: "", own_port: "" });
  const [engine, setEngine] = useState<Awaited<ReturnType<typeof api.installedEngine>>>(null);
  const [engineChecks, setEngineChecks] = useState<{ id: string; label: string; status: string; message: string }[]>([]);
  const loadEngine = () => api.installedEngine(projectId).then(setEngine).catch(() => setEngine(null));
  useEffect(() => { loadEngine(); }, [projectId]); // eslint-disable-line react-hooks/exhaustive-deps
  const installEngine = async () => {
    if (!item) return;
    try {
      const out = await api.installEngine(projectId, item.id);
      setEngineChecks(out.checks);
      setMessage(`Installed “${out.name}” v${out.version} as the powertrain; the design's power follows the engine.`);
      loadEngine(); onModelChanged();
    } catch (e) { setMessage(e instanceof Error ? e.message : String(e)); }
  };
  const upgradeEngine = async () => {
    try {
      const out = await api.upgradeEngine(projectId);
      setMessage(`Upgraded the engine to v${out.version}.`);
      loadEngine(); onModelChanged();
    } catch (e) { setMessage(e instanceof Error ? e.message : String(e)); }
  };
  const [perf, setPerf] = useState<Awaited<ReturnType<typeof api.enginePerformance>> | null>(null);
  const runPerformance = () => api.enginePerformance(projectId).then(setPerf)
    .catch((e) => setMessage(e instanceof Error ? e.message : String(e)));
  const loadInstalled = () => api.installedItems(projectId).then(setInstalled).catch(() => setInstalled([]));
  useEffect(() => { loadInstalled(); }, [projectId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const t = window.setTimeout(() => {
      api.inventory(q, category).then(setRows).catch((e) => setMessage(String(e.message ?? e)));
    }, 150);
    return () => window.clearTimeout(t);
  }, [q, category]);

  const open = (id: string) => {
    setLife(null); setMessage(null);
    api.inventoryItem(id).then(setItem).catch((e) => setMessage(String(e.message ?? e)));
    api.itemUsage(id).then(setUsage).catch(() => setUsage([]));
  };
  useEffect(() => {
    if (!item || item.performance.C_kN === undefined) return;
    api.bearingLife(item.id, load, rpm).then(setLife).catch(() => setLife(null));
  }, [item, load, rpm]);

  const install = async () => {
    if (!item) return;
    try {
      const snap = mate.part && mate.port && mate.own_port ? mate : undefined;
      const part = await api.installItem(projectId, item.id, at, snap);
      setMessage(`Added “${part.document.name}” to the project (linked to ${item.id} v${item.version})${snap ? `, its ${snap.own_port} mated to ${snap.port}` : ""}.`);
      loadInstalled();
      onModelChanged();
      api.itemUsage(item.id).then(setUsage).catch(() => undefined);
    } catch (e) { setMessage(e instanceof Error ? e.message : String(e)); }
  };

  return (
    <div className="bench wide inventory">
      <div className="bench-side">
        <input type="search" placeholder="Search: M10 4762, 6205, SHS 40…" value={q} onChange={(e) => setQ(e.target.value)} />
        <div className="chips">
          {CATEGORIES.map((c) => (
            <button key={c || "all"} className={category === c ? "active" : ""} onClick={() => setCategory(c)}>{c || "All"}</button>
          ))}
        </div>
        <div className="inv-list">
          {rows.map((r) => (
            <button key={r.id} className={`inv-row${item?.id === r.id ? " active" : ""}`} onClick={() => open(r.id)}>
              <span>{r.name}</span>
              <span className="muted small">{r.family}{r.mass_kg !== null ? ` · ${fmt(r.mass_kg)} kg` : ""}</span>
            </button>
          ))}
          {rows.length === 0 && <p className="muted small">Nothing matches.</p>}
        </div>
        <p className="muted small">{rows.length} items · standard library plus parts published from projects</p>
      </div>
      <div className="bench-detail">
        {engine && (
          <div className={`check ${engine.upgrade_available ? "warn" : "pass"} inv-engine`}>
            <b>Powertrain:</b> {engine.name} v{engine.version}
            {engine.upgrade_available ? (
              <> · v{engine.latest} released: power {engine.impact.peak_power_kw >= 0 ? "+" : ""}{engine.impact.peak_power_kw} kW,
                torque {engine.impact.peak_torque_nm >= 0 ? "+" : ""}{engine.impact.peak_torque_nm} N·m,
                mass {engine.impact.mass_kg >= 0 ? "+" : ""}{engine.impact.mass_kg} kg <button onClick={upgradeEngine}>Upgrade</button></>
            ) : <span className="muted"> · up to date</span>}
            <button onClick={runPerformance}>Acceleration with this engine</button>
            {perf && (
              <div className="perf">
                <span><b>{perf.zero_to_100_s?.toFixed(1) ?? "—"} s</b> 0–100 km/h</span>
                <span><b>{perf.zero_to_200_s?.toFixed(1) ?? "—"} s</b> 0–200 km/h</span>
                <span><b>{perf.top_speed_kmh.toFixed(0)} km/h</b> top speed</span>
                <span className="muted">{perf.gears.length}-speed, overall ratios {perf.gears.map((g) => g.toFixed(2)).join(" / ")}</span>
                <span className="muted">ideal CVT 0–100: {perf.cvt_zero_to_100_s?.toFixed(1) ?? "—"} s</span>
                <svg viewBox="0 0 300 70" className="perf-trace" role="img" aria-label="Speed against time">
                  <polyline fill="none" points={perf.trace.t.map((t, i) => `${(t / perf.trace.t[perf.trace.t.length - 1]) * 296 + 2},${68 - (perf.trace.v[i] / Math.max(...perf.trace.v)) * 64}`).join(" ")} />
                </svg>
              </div>
            )}
          </div>
        )}
        {!item && <p className="muted">Pick an item to see its dimensions, ports and performance, and add it to this project.</p>}
        {item && (
          <div className="inv-item">
            <h3>{item.name} <span className="muted small">v{item.version} · {item.status}</span></h3>
            <p className="muted small">{item.family} · {item.standard || item.kind} · {item.provenance}</p>
            <div className="inv-grid">
              <section>
                <h4>Parameters</h4>
                <table><tbody>{Object.entries(item.parameters).map(([k, v]) => <tr key={k}><td>{label(k)}</td><td className="num">{fmt(v)}</td></tr>)}</tbody></table>
                <h4>Properties</h4>
                <table><tbody>{Object.entries(item.properties).map(([k, v]) => <tr key={k}><td>{label(k)}</td><td className="num">{fmt(v)}</td></tr>)}</tbody></table>
              </section>
              <section>
                <h4>Performance</h4>
                {Object.keys(item.performance).length === 0 && <p className="muted small">—</p>}
                <table><tbody>{Object.entries(item.performance).map(([k, v]) => <tr key={k}><td>{label(k)}</td><td className="num">{fmt(v)}</td></tr>)}</tbody></table>
                {item.performance.C_kN !== undefined && (
                  <div className="calc">
                    <h4>Rating life (ISO 281)</h4>
                    <label>Equivalent load P <input type="number" value={load} min={0.01} step={0.1} onChange={(e) => setLoad(Number(e.target.value))} /> kN</label>
                    <label>Speed <input type="number" value={rpm} min={1} step={100} onChange={(e) => setRpm(Number(e.target.value))} /> rpm</label>
                    {life && <p><b>L10 = {fmt(life.L10_Mrev)} million revolutions = {fmt(life.L10_hours)} h</b><br />
                      <span className="muted small">L10 = (C/P)³ at 90 % reliability; P = Fr for pure radial load</span></p>}
                  </div>
                )}
              </section>
              <section>
                <h4>Ports (interfaces)</h4>
                <table><tbody>{item.ports.map((p) => (
                  <tr key={p.name}><td>{p.name}</td><td className="muted">{p.kind}</td>
                    <td className="muted small">{Object.entries(p.attributes).map(([k, v]) => `${k} ${fmt(v)}`).join(", ")}</td></tr>
                ))}</tbody></table>
                <h4>Add to this project</h4>
                <div className="place">
                  {(["x", "y", "z"] as const).map((k) => (
                    <label key={k}>{k} <input type="number" value={at[k]} step={10} onChange={(e) => setAt({ ...at, [k]: Number(e.target.value) })} /> mm</label>
                  ))}
                </div>
                <h4>…or snap onto an installed item</h4>
                <div className="place">
                  <label>item <select value={mate.part} onChange={(e) => setMate({ ...mate, part: e.target.value, port: "" })}>
                    <option value="">— place by coordinates —</option>
                    {installed.map((r) => <option key={r.part} value={r.part}>{r.name}</option>)}
                  </select></label>
                  {mate.part && (
                    <>
                      <label>its port <select value={mate.port} onChange={(e) => setMate({ ...mate, port: e.target.value })}>
                        <option value="">choose</option>
                        {installed.find((r) => r.part === mate.part)?.ports.map((p) => <option key={p.name} value={p.name}>{p.name} ({p.kind.replace("mechanical.", "")})</option>)}
                      </select></label>
                      <label>this item's port <select value={mate.own_port} onChange={(e) => setMate({ ...mate, own_port: e.target.value })}>
                        <option value="">choose</option>
                        {item.ports.map((p) => <option key={p.name} value={p.name}>{p.name} ({p.kind.replace("mechanical.", "")})</option>)}
                      </select></label>
                    </>
                  )}
                </div>
                <button className="primary" onClick={install}>{mate.part ? "Snap into place" : "Add to project"}</button>
                {item.category === "Engines" && (
                  <>
                    <h4>Install as the powertrain</h4>
                    <button className="primary" onClick={installEngine}>Install engine</button>
                    {engineChecks.map((c) => <div key={c.id} className={`check ${c.status}`}><b>{c.label}</b>: {c.message}</div>)}
                  </>
                )}
                <h4>Where used</h4>
                {usage.length === 0 ? <p className="muted small">Not installed anywhere yet.</p> : (
                  <ul className="small">{usage.map((u, i) => <li key={i}>project {u.project.slice(0, 8)} · part {u.part.slice(0, 8)} · v{u.version}</li>)}</ul>
                )}
              </section>
            </div>
            {item.notes.length > 0 && <p className="muted small">Notes: {item.notes.join("; ")}</p>}
          </div>
        )}
        {message && <p className="small">{message}</p>}
      </div>
    </div>
  );
}
