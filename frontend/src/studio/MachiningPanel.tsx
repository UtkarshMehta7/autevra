import { useEffect, useMemo, useState } from "react";
import { api, type CamOut } from "../api/client";
import type { PartOut } from "../api/types";
import { setOverlay } from "../viewport/overlay";

/** Machining workspace (shared by every module): plan 2.5-axis milling and drilling of a
 * part from a stock block (backend autevra/cam), show the toolpaths over the part in the 3D
 * view and download the ISO G-code program. */

const MATERIALS = ["aluminium 6061-T6", "steel C45", "stainless 304", "cast iron GG25", "POM (acetal)"];
const MILLS = [3, 4, 6, 8, 10, 12, 16, 20];

const mmss = (s: number) => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, "0")}`;

function NumField({ label, value, onChange, unit, step = 1 }: { label: string; value: number; onChange: (v: number) => void; unit?: string; step?: number }) {
  return (
    <label className="el-field">{label}
      <span><input type="number" value={value} step={step} onChange={(e) => { const v = Number(e.target.value); if (Number.isFinite(v)) onChange(v); }} />{unit && <em>{unit}</em>}</span>
    </label>
  );
}

export function MachiningPanel({ projectId, version }: { projectId: string; version?: number }) {
  const [parts, setParts] = useState<PartOut[]>([]);
  const [part, setPart] = useState("");
  const [cfg, setCfg] = useState({ material: MATERIALS[0], side_margin: 3, top_margin: 1, bottom_skin: 3, corner_radius: 5, radial_stock: 0.3, max_rpm: 12000, machine_kw: 7.5 });
  const [rough, setRough] = useState<number | null>(null);
  const [finish, setFinish] = useState<number | null>(null);
  const [out, setOut] = useState<CamOut | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [show, setShow] = useState<Set<number>>(new Set());

  useEffect(() => {
    api.parts(projectId).then((list) => {
      const solids = list.filter((p) => p.volume != null);
      setParts(solids);
      setPart((cur) => (solids.some((p) => p.id === cur) ? cur : solids[0]?.id ?? ""));
    }).catch(() => setParts([]));
  }, [projectId, version]);
  useEffect(() => () => setOverlay(null), []);

  const run = async () => {
    if (!part) return;
    setBusy(true); setError(null);
    try {
      const o = await api.cam(projectId, part, { ...cfg, rough_tool: rough, finish_tool: finish });
      setOut(o);
      setShow(new Set(o.operations.map((_, i) => i)));
    } catch (e) { setError(e instanceof Error ? e.message : String(e)); setOut(null); } finally { setBusy(false); }
  };

  useEffect(() => {
    if (!out || !part) { setOverlay(null); return; }
    const polylines = out.operations.flatMap((op, i) => (show.has(i) ? op.paths : []));
    setOverlay({ partId: `part_${part}`, polylines, color: 0x4fd1ff });
  }, [out, show, part]);

  const download = () => {
    if (!out) return;
    const name = (parts.find((p) => p.id === part)?.document.name ?? "part").replace(/[^A-Za-z0-9_-]+/g, "-");
    const url = URL.createObjectURL(new Blob([out.gcode], { type: "text/plain" }));
    const a = document.createElement("a");
    a.href = url; a.download = `${name}.nc`; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  const preview = useMemo(() => out?.gcode.split("\n").slice(0, 60).join("\n") ?? "", [out]);
  const stock = out?.stock;

  return (
    <section className="elements-panel machining-panel">
      <p className="small muted el-method">One setup, tool along −Z, work zero at the stock's min corner and top. Cutting data are typical carbide starting values for the material: check them against your tool maker and simulate the program before running it.</p>
      <div className="el-body">
        <div className="el-inputs">
          {parts.length === 0 ? <p className="small muted">Add a part (Part Design, Inventory, Machine elements or STEP import) to machine it.</p> : (
            <label className="el-field">part
              <select value={part} onChange={(e) => { setPart(e.target.value); setOut(null); }}>
                {parts.map((p) => <option key={p.id} value={p.id}>{p.document.name}</option>)}
              </select>
            </label>
          )}
          <label className="el-field">material
            <select value={cfg.material} onChange={(e) => setCfg({ ...cfg, material: e.target.value })}>
              {MATERIALS.map((m) => <option key={m}>{m}</option>)}
            </select>
          </label>
          <NumField label="stock: sides" value={cfg.side_margin} unit="mm" onChange={(v) => setCfg({ ...cfg, side_margin: Math.max(v, 0) })} />
          <NumField label="stock: top" value={cfg.top_margin} unit="mm" step={0.5} onChange={(v) => setCfg({ ...cfg, top_margin: Math.max(v, 0) })} />
          <NumField label="bottom skin" value={cfg.bottom_skin} unit="mm" onChange={(v) => setCfg({ ...cfg, bottom_skin: Math.max(v, 0) })} />
          <label className="el-field">roughing tool
            <select value={rough ?? ""} onChange={(e) => setRough(e.target.value ? Number(e.target.value) : null)}>
              <option value="">auto</option>{MILLS.map((d) => <option key={d} value={d}>⌀{d} end mill</option>)}
            </select>
          </label>
          <label className="el-field">finishing tool
            <select value={finish ?? ""} onChange={(e) => setFinish(e.target.value ? Number(e.target.value) : null)}>
              <option value="">auto</option>{MILLS.map((d) => <option key={d} value={d}>⌀{d} end mill</option>)}
            </select>
          </label>
          <NumField label="max inside corner R" value={cfg.corner_radius} unit="mm" step={0.5} onChange={(v) => setCfg({ ...cfg, corner_radius: Math.max(v, 0.6) })} />
          <NumField label="radial stock (rough)" value={cfg.radial_stock} unit="mm" step={0.1} onChange={(v) => setCfg({ ...cfg, radial_stock: Math.max(v, 0) })} />
          <NumField label="spindle max" value={cfg.max_rpm} unit="rpm" step={1000} onChange={(v) => setCfg({ ...cfg, max_rpm: Math.max(v, 500) })} />
          <NumField label="spindle power" value={cfg.machine_kw} unit="kW" step={0.5} onChange={(v) => setCfg({ ...cfg, machine_kw: Math.max(v, 0.1) })} />
          <button disabled={busy || !part} onClick={run}>{busy ? "Planning toolpaths…" : "Generate program"}</button>
          {error && <p className="el-warn bad">{error}</p>}
        </div>
        <div className="el-out">
          {!out && !busy && <p className="small muted">Generate a program to see the operations, the toolpaths over the part (3D view) and the G-code.</p>}
          {out && stock && <>
            <div className="cam-tiles">
              <div><b>{mmss(out.time_s)}</b><span>cycle time (min:s)</span></div>
              <div><b>{out.tools.length}</b><span>tools</span></div>
              <div><b>{(out.removed_volume / 1e3).toFixed(0)} cm³</b><span>removed ({(100 * out.removed_volume / out.stock_volume).toFixed(0)} % of stock)</span></div>
              <div><b>{out.mass_kg.toFixed(2)} kg</b><span>part, from {out.stock_mass_kg.toFixed(2)} kg stock</span></div>
              <div><b>{(stock[3] - stock[0]).toFixed(0)}×{(stock[4] - stock[1]).toFixed(0)}×{(stock[5] - stock[2]).toFixed(0)}</b><span>stock (mm)</span></div>
              <div><b>{out.gcode_lines}</b><span>G-code lines</span></div>
            </div>
            {out.warnings.length > 0 && <ul className="el-warn">{out.warnings.map((w) => <li key={w}>{w}</li>)}</ul>}
            {out.notes.length > 0 && <ul className="small cam-notes">{out.notes.map((w) => <li key={w}>{w}</li>)}</ul>}
            <table className="bd-table"><thead><tr><th>show</th><th>operation</th><th>tool</th><th className="num">rpm</th><th className="num">feed mm/min</th><th className="num">cut mm</th><th className="num">time</th><th className="num">kW</th></tr></thead><tbody>
              {out.operations.map((op, i) => (
                <tr key={i}>
                  <td><input type="checkbox" checked={show.has(i)} aria-label={`Show toolpath of ${op.name}`}
                    onChange={(e) => { const next = new Set(show); if (e.target.checked) next.add(i); else next.delete(i); setShow(next); }} /></td>
                  <td>{op.name}{op.cycle ? ` · ${op.cycle}` : ""}</td><td>{op.tool_label}</td>
                  <td className="num">{op.rpm.toFixed(0)}</td><td className="num">{op.feed.toFixed(0)}</td>
                  <td className="num">{op.cut_mm.toFixed(0)}</td><td className="num">{mmss(op.time_s)}</td>
                  <td className="num">{op.power_kw ? op.power_kw.toFixed(2) : "—"}</td>
                </tr>
              ))}
            </tbody></table>
            <div className="row wrap">
              <button onClick={download}>Download G-code (.nc)</button>
              <button onClick={() => setShow(new Set())}>Hide toolpaths</button>
              <button onClick={() => setShow(new Set(out.operations.map((_, i) => i)))}>Show all toolpaths</button>
            </div>
            <details><summary className="small">G-code preview (first 60 lines of {out.gcode_lines})</summary><pre className="gcode">{preview}</pre></details>
          </>}
        </div>
      </div>
    </section>
  );
}
