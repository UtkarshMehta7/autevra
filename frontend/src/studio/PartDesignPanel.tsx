import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { DesignTable, PartDoc, PartFeature, PartOut, Placement } from "../api/types";
import { DownloadLink } from "../DownloadLink";
import { Sketcher } from "./Sketcher";

/** Defaults for a new feature of each type (mm, degrees). */
const FEATURE_DEFAULTS: Record<string, Omit<PartFeature, "id" | "type">> = {
  box: { size: [100, 100, 100] },
  cylinder: { radius: 50, height: 100, axis: "z" },
  sphere: { radius: 50 },
  extrude: { plane: "xy", points: [[0, 0], [100, 0], [100, 60], [0, 60]], depth: 20, symmetric: false },
  revolve: { points: [[0, 0], [40, 0], [40, 100], [0, 100]], angle: 360 },
  loft: { sections: [{ z: 0, width: 100, height: 100, radius: 20 }, { z: 200, width: 60, height: 60, radius: 20 }], ruled: false },
  sweep: { path: [[0, 0, 0], [300, 0, 0], [300, 200, 0]], radius: 15, wall: 2, bend_radius: 40 },
  sheet_metal: { points: [[0, 50], [0, 0], [120, 0], [120, 50]], thickness: 2, bend_radius: 2, width: 200, k_factor: 0.44 },
  wing: { naca: "2412", root_chord: 1600, tip_chord: 800, span: 5000, sweep: 5, dihedral: 3, twist: -2, both_sides: true },
  shell: { thickness: 3, open_towards: "+z" },
  fillet: { radius: 3, edges: "" },
  chamfer: { size: 2, edges: "" },
  mirror: { plane: "xz" },
  linear_pattern: { count: 3, step: [150, 0, 0] },
  circular_pattern: { count: 6, axis: "z", angle: 360 },
};
const SOLIDS = ["box", "cylinder", "sphere", "extrude", "revolve", "loft", "sweep", "wing", "sheet_metal"];
const LABELS: Record<string, string> = {
  box: "Box", cylinder: "Cylinder", sphere: "Sphere", extrude: "Extrude sketch",
  revolve: "Revolve profile", loft: "Loft sections", sweep: "Sweep tube",
  wing: "Wing (NACA aerofoil)", sheet_metal: "Sheet metal", shell: "Shell",
  fillet: "Fillet edges", chamfer: "Chamfer edges", mirror: "Mirror", linear_pattern: "Linear pattern",
  circular_pattern: "Circular pattern",
};
const CHOICES: Record<string, string[]> = {
  op: ["add", "cut", "intersect"], axis: ["x", "y", "z"], plane: ["xy", "xz", "yz"],
  open_towards: ["none", "+x", "-x", "+y", "-y", "+z", "-z"],
};



function newId(type: string, features: PartFeature[]): string {
  const taken = new Set(features.map((f) => f.id));
  for (let i = 1; ; i++) if (!taken.has(`${type}${i}`)) return `${type}${i}`;
}

function hex(c: [number, number, number] | undefined): string {
  const [r, g, b] = c ?? [0.62, 0.66, 0.72];
  return "#" + [r, g, b].map((v) => Math.round(Math.min(Math.max(v, 0), 1) ** (1 / 2.2) * 255)
    .toString(16).padStart(2, "0")).join("");
}

function rgb(value: string): [number, number, number] {
  const n = [1, 3, 5].map((i) => parseInt(value.slice(i, i + 2), 16) / 255);
  return n.map((v) => +(v ** 2.2).toFixed(4)) as [number, number, number]; // linear for the viewer
}

/** One numeric input that commits on blur or Enter. */
function Num({ value, onCommit, step }: { value: number; onCommit: (v: number) => void; step?: number }) {
  const [text, setText] = useState(String(value));
  useEffect(() => setText(String(value)), [value]);
  const commit = () => { const v = Number(text); if (Number.isFinite(v) && v !== value) onCommit(v); else setText(String(value)); };
  return <input className="num" type="number" value={text} step={step ?? 1} onChange={(e) => setText(e.target.value)}
    onBlur={commit} onKeyDown={(e) => { if (e.key === "Enter") commit(); }} />;
}

/** A JSON list (points, path, sections) edited as text; applied when it parses. */
function JsonField({ value, onCommit }: { value: unknown; onCommit: (v: unknown) => void }) {
  const [text, setText] = useState(JSON.stringify(value));
  const [bad, setBad] = useState(false);
  useEffect(() => { setText(JSON.stringify(value)); setBad(false); }, [value]);
  const commit = () => {
    try { const v = JSON.parse(text); setBad(false); if (JSON.stringify(v) !== JSON.stringify(value)) onCommit(v); }
    catch { setBad(true); }
  };
  return <textarea className={`json ${bad ? "bad" : ""}`} rows={3} value={text}
    onChange={(e) => setText(e.target.value)} onBlur={commit} title="JSON; applied when you leave the field" />;
}

/** A text input that commits on blur or Enter. */
function Text({ value, onCommit, placeholder, size }: { value: string; onCommit: (v: string) => void;
  placeholder?: string; size?: number }) {
  const [text, setText] = useState(value);
  useEffect(() => setText(value), [value]);
  const commit = () => { if (text !== value) onCommit(text); };
  return <input value={text} placeholder={placeholder} size={size} onChange={(ev) => setText(ev.target.value)}
    onBlur={commit} onKeyDown={(ev) => { if (ev.key === "Enter") commit(); }} />;
}

/** Field bindings of a feature: field path -> expression of the part's parameters. */
function Bindings({ bindings, onChange }: { bindings: Record<string, string>; onChange: (b: Record<string, string>) => void }) {
  const [path, setPath] = useState("");
  const [expr, setExpr] = useState("");
  return (
    <div className="bindings">
      <span className="hint">Formulas: bind a field (e.g. <code>radius</code>, <code>size.0</code>,{" "}
        <code>at.x</code>, <code>sections.1.width</code>) to an expression of the part's parameters.</span>
      {Object.entries(bindings).map(([p, x]) => (
        <div key={p} className="binding">
          <code>{p}</code> =
          <Text value={x} size={22} onCommit={(v) => onChange(v ? { ...bindings, [p]: v } : Object.fromEntries(
            Object.entries(bindings).filter(([k]) => k !== p)))} />
          <button title="Remove the formula" onClick={() => onChange(Object.fromEntries(
            Object.entries(bindings).filter(([k]) => k !== p)))}>✕</button>
        </div>
      ))}
      <div className="binding">
        <input placeholder="field" size={12} value={path} onChange={(ev) => setPath(ev.target.value.trim())} /> =
        <input placeholder="expression" size={22} value={expr} onChange={(ev) => setExpr(ev.target.value)} />
        <button disabled={!path || !expr} onClick={() => { onChange({ ...bindings, [path]: expr }); setPath(""); setExpr(""); }}>
          Add formula</button>
      </div>
    </div>
  );
}

/** The part's named parameters: numbers or expressions of earlier parameters. */
function Parameters({ params, onChange }: { params: Record<string, number | string>; onChange: (p: Record<string, number | string>) => void }) {
  const [name, setName] = useState("");
  const parse = (v: string): number | string => (v.trim() !== "" && Number.isFinite(Number(v)) ? Number(v) : v);
  return (
    <div className="bindings">
      {Object.entries(params).map(([n, v]) => (
        <div key={n} className="binding">
          <code>{n}</code> =
          <Text value={String(v)} size={18} onCommit={(t) => onChange({ ...params, [n]: parse(t) })} />
          <button title="Remove the parameter" onClick={() => onChange(Object.fromEntries(
            Object.entries(params).filter(([k]) => k !== n)))}>✕</button>
        </div>
      ))}
      <div className="binding">
        <input placeholder="new parameter" size={14} value={name}
          onChange={(ev) => setName(ev.target.value.replace(/[^A-Za-z0-9_]/g, ""))} />
        <button disabled={!/^[A-Za-z_]/.test(name) || name in params}
          onClick={() => { onChange({ ...params, [name]: 0 }); setName(""); }}>Add parameter</button>
      </div>
    </div>
  );
}

/** Design table: variants of the part as rows of parameter values; the active row drives it. */
function DesignTableEditor({ table, params, onChange, csvUrl, onImport }: {
  table: DesignTable | null | undefined; params: Record<string, number | string>;
  onChange: (t: DesignTable | null) => void; csvUrl: string; onImport: (csv: string) => void;
}) {
  const numeric = Object.entries(params).filter(([, v]) => typeof v === "number") as [string, number][];
  if (!table) {
    return (
      <div className="bindings">
        <span className="hint">A design table holds named variants (rows) of the part's numeric parameters.</span>
        <div className="binding">
          <button disabled={numeric.length === 0} onClick={() => onChange({
            columns: numeric.map(([n]) => n), rows: [{ name: "default", values: numeric.map(([, v]) => v) }], active: "default",
          })}>Create from the parameters</button>
          <label className="button">Import CSV<input type="file" accept=".csv,text/csv" hidden
            onChange={(ev) => ev.target.files?.[0]?.text().then(onImport)} /></label>
        </div>
      </div>
    );
  }
  const setRow = (i: number, row: DesignTable["rows"][number]) =>
    onChange({ ...table, rows: table.rows.map((r, j) => (j === i ? row : r)) });
  const uniqueName = () => { for (let i = table.rows.length + 1; ; i++) if (!table.rows.some((r) => r.name === `V${i}`)) return `V${i}`; };
  return (
    <div className="bindings design-table">
      <table>
        <thead><tr><th>active</th><th>variant</th>{table.columns.map((c) => <th key={c}>{c}</th>)}<th /></tr></thead>
        <tbody>
          {table.rows.map((row, i) => (
            <tr key={row.name} className={row.name === table.active ? "active" : ""}>
              <td><input type="radio" checked={row.name === table.active} onChange={() => onChange({ ...table, active: row.name })} /></td>
              <td><Text value={row.name} size={8} onCommit={(n) => {
                if (!n || table.rows.some((r) => r.name === n)) return;
                onChange({ ...table, active: table.active === row.name ? n : table.active,
                  rows: table.rows.map((r, j) => (j === i ? { ...r, name: n } : r)) });
              }} /></td>
              {row.values.map((v, j) => (
                <td key={j}><Num value={v} onCommit={(n) => setRow(i, { ...row, values: row.values.map((o, k) => (k === j ? n : o)) })} /></td>
              ))}
              <td><button title="Delete variant" onClick={() => onChange({ ...table,
                active: table.active === row.name ? null : table.active,
                rows: table.rows.filter((_, j) => j !== i) })}>✕</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="binding">
        <button onClick={() => {
          const base = table.rows.find((r) => r.name === table.active) ?? table.rows[table.rows.length - 1];
          onChange({ ...table, rows: [...table.rows, { name: uniqueName(), values: base ? [...base.values] : table.columns.map(() => 0) }] });
        }}>Add variant</button>
        <DownloadLink className="button" href={csvUrl}>Export CSV</DownloadLink>
        <label className="button">Import CSV<input type="file" accept=".csv,text/csv" hidden
          onChange={(ev) => ev.target.files?.[0]?.text().then(onImport)} /></label>
        <button title="Remove the design table (parameters keep their own values)" onClick={() => onChange(null)}>Remove table</button>
      </div>
    </div>
  );
}

function PlacementFields({ at, onCommit }: { at: Placement | undefined; onCommit: (p: Placement) => void }) {
  const p = at ?? {};
  return (
    <div className="placement">
      {(["x", "y", "z", "rx", "ry", "rz"] as const).map((k) => (
        <label key={k}>{k}<Num value={p[k] ?? 0} onCommit={(v) => onCommit({ ...p, [k]: v })} /></label>
      ))}
    </div>
  );
}

function FeatureFields({ feature, onChange }: { feature: PartFeature; onChange: (f: PartFeature) => void }) {
  const set = (key: string, value: unknown) => onChange({ ...feature, [key]: value });
  const keys = Object.keys({ ...FEATURE_DEFAULTS[feature.type], ...feature })
    .filter((k) => !["id", "type", "suppressed", "op", "at", "name", "bindings"].includes(k));
  const bound = feature.bindings ?? {};
  return (
    <div className="feature-fields">
      <label>Name<input value={feature.name ?? ""} placeholder={feature.id}
        onChange={(e) => set("name", e.target.value)} /></label>
      {keys.map((key) => {
        const value = feature[key] ?? FEATURE_DEFAULTS[feature.type]?.[key];
        if (CHOICES[key]) {
          return <label key={key}>{key.replace("_", " ")}<select value={String(value)}
            onChange={(e) => set(key, e.target.value)}>{CHOICES[key].map((c) => <option key={c}>{c}</option>)}</select></label>;
        }
        if (typeof value === "boolean") {
          return <label key={key}>{key.replace("_", " ")}<input type="checkbox" checked={value}
            onChange={(e) => set(key, e.target.checked)} /></label>;
        }
        if (typeof value === "string") {
          return <label key={key}>{key.replace("_", " ")}<input key={value} defaultValue={value} size={6}
            onBlur={(e) => { if (e.target.value !== value) set(key, e.target.value); }}
            onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }} /></label>;
        }
        if (typeof value === "number" && bound[key]) {
          return <label key={key}>{key.replace("_", " ")}<span className="formula" title="Set by a formula below">ƒ {bound[key]}</span></label>;
        }
        if (typeof value === "number") {
          return <label key={key}>{key.replace("_", " ")}<Num value={value} onCommit={(v) => set(key, v)} /></label>;
        }
        if (Array.isArray(value) && value.every((v) => typeof v === "number")) {
          return (
            <label key={key}>{key}<span className="tuple">{value.map((v, i) => (
              <Num key={i} value={v as number} onCommit={(n) => set(key, value.map((o, j) => (j === i ? n : o)))} />
            ))}</span></label>
          );
        }
        if (key === "points" && ["extrude", "revolve", "sheet_metal"].includes(feature.type) && Array.isArray(value)) {
          const plane = feature.type === "sheet_metal" ? "xz" : String(feature.plane ?? "xy");
          return (
            <label key={key} className="wide">profile
              <Sketcher points={value as [number, number][]} axis={feature.type === "revolve"}
                open={feature.type === "sheet_metal"}
                labels={feature.type === "revolve" ? ["r", "z"] : [plane[0], plane[1]] as [string, string]}
                onCommit={(v) => set(key, v)} />
              <JsonField value={value} onCommit={(v) => set(key, v)} />
            </label>
          );
        }
        return <label key={key} className="wide">{key}<JsonField value={value} onCommit={(v) => set(key, v)} /></label>;
      })}
      {"edges" in feature || ["fillet", "chamfer"].includes(feature.type) ? (
        <span className="hint">Edges: empty for all, or a selector such as <code>|Z</code> (parallel to Z),{" "}
          <code>&gt;Z</code> (top), <code>&lt;X or &gt;X</code>, <code>not |Z</code>.</span>
      ) : null}
      <Bindings bindings={bound} onChange={(b) => set("bindings", b)} />
      {SOLIDS.includes(feature.type) && (
        <>
          <span className="hint">Placement of this feature (mm, degrees)</span>
          <PlacementFields at={feature.at as Placement | undefined} onCommit={(p) => set("at", p)} />
        </>
      )}
    </div>
  );
}

export function PartDesignPanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [parts, setParts] = useState<PartOut[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [feature, setFeature] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  // Starting points from several domains, served by the backend (each one builds).
  const [presets, setPresets] = useState<Record<string, PartDoc>>({});
  useEffect(() => { api.partPresets().then(setPresets).catch(() => setPresets({})); }, []);

  useEffect(() => {
    api.parts(projectId).then((list) => {
      setParts(list);
      setSelected((s) => s ?? list[0]?.id ?? null);
    }).catch((e) => setError(String(e.message ?? e)));
  }, [projectId]);

  const part = parts.find((p) => p.id === selected) ?? null;

  const run = useCallback(async (action: () => Promise<PartOut | void>, removed?: string) => {
    setBusy(true);
    setError(null);
    try {
      const out = await action();
      if (out) {
        setParts((list) => list.some((p) => p.id === out.id)
          ? list.map((p) => (p.id === out.id ? out : p)) : [...list, out]);
        setSelected(out.id);
      }
      if (removed) setParts((list) => list.filter((p) => p.id !== removed));
      onModelChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }, [onModelChanged]);

  const save = (doc: PartDoc) => part && run(() => api.updatePart(projectId, part.id, doc));
  const doc = part?.document;
  const features = doc?.features ?? [];
  const failed = part?.errors[0]?.feature;

  const editFeature = (index: number, next: PartFeature | null) => {
    if (!doc) return;
    const list = [...features];
    if (next) list[index] = next; else list.splice(index, 1);
    save({ ...doc, features: list });
  };
  const move = (index: number, by: number) => {
    if (!doc) return;
    const list = [...features];
    const [f] = list.splice(index, 1);
    list.splice(Math.min(Math.max(index + by, 0), list.length), 0, f);
    save({ ...doc, features: list });
  };
  const addFeature = (type: string) => {
    if (!doc || !type) return;
    const f: PartFeature = { id: newId(type, features), type, ...structuredClone(FEATURE_DEFAULTS[type]) };
    setFeature(f.id);
    save({ ...doc, features: [...features, f] });
  };

  return (
    <div className="bench wide part-design">
      <div className="bench-side">
        <strong>Parts</strong>
        <ul className="plain part-list">
          {parts.map((p) => (
            <li key={p.id}>
              <button className={p.id === selected ? "active" : ""} onClick={() => setSelected(p.id)}>
                {p.document.name}{p.errors.length > 0 && <span className="bad-text"> ●</span>}
              </button>
            </li>
          ))}
        </ul>
        <label className="new-part">New part
          <select value="" disabled={busy} onChange={(e) => {
            const preset = presets[e.target.value];
            if (preset) run(() => api.createPart(projectId, structuredClone(preset)));
          }}>
            <option value="">choose a starting point…</option>
            {Object.keys(presets).map((k) => <option key={k}>{k}</option>)}
          </select>
        </label>
        <p className="hint">Parts are built from an ordered feature tree with the Open CASCADE
          kernel, placed in the vehicle frame (X forward, Y left, Z up, mm), shown in the 3D view
          and included in the STEP export.</p>
      </div>
      <div className="bench-detail">
        {error && <div className="error">{error}</div>}
        {!part && <p className="hint">Choose a starting point to create a part.</p>}
        {part && doc && (
          <>
            <div className="part-head">
              <input className="part-name" value={doc.name} onChange={(e) =>
                setParts((list) => list.map((p) => (p.id === part.id
                  ? { ...p, document: { ...doc, name: e.target.value } } : p)))}
                onBlur={(e) => save({ ...doc, name: e.target.value || "Part" })} />
              <input type="color" value={hex(doc.color)} title="Colour"
                onChange={(e) => save({ ...doc, color: rgb(e.target.value) })} />
              <button disabled={busy || !part.can_undo} onClick={() => run(() => api.undoPart(projectId, part.id))}>Undo</button>
              <button disabled={busy || !part.can_redo} onClick={() => run(() => api.redoPart(projectId, part.id))}>Redo</button>
              <button disabled={busy} onClick={() => run(() => api.deletePart(projectId, part.id), part.id)}>Delete part</button>
              <span className="hint">
                {part.volume != null ? `${(part.volume / 1e3).toFixed(1)} cm³` : "nothing built"}
                {part.bounds && ` · ${part.bounds[1].map((v, i) => (v - part.bounds![0][i]).toFixed(0)).join(" × ")} mm`}
              </span>
            </div>
            <strong>Parameters</strong>
            <Parameters params={doc.parameters ?? {}} onChange={(parameters) => save({ ...doc, parameters })} />
            {part.errors[0]?.feature === "parameters" && <div className="bad-text">{part.errors[0].message}</div>}
            <strong>Design table</strong>
            <DesignTableEditor table={doc.design_table} params={doc.parameters ?? {}}
              onChange={(design_table) => save({ ...doc, design_table })}
              csvUrl={api.partTableUrl(projectId, part.id)}
              onImport={(csv) => run(() => api.setPartTable(projectId, part.id, csv))} />
            <span className="hint">Part placement in the vehicle frame</span>
            <PlacementFields at={doc.at} onCommit={(at) => save({ ...doc, at })} />
            <strong>Feature tree</strong>
            <ol className="feature-tree">
              {features.map((f, i) => (
                <li key={f.id} className={`${f.id === feature ? "open" : ""} ${f.suppressed ? "suppressed" : ""} ${f.id === failed ? "failed" : ""}`}>
                  <div className="row">
                    <button className="name" onClick={() => setFeature(f.id === feature ? null : f.id)}>
                      {LABELS[f.type] ?? f.type} <em>{f.name || f.id}</em>
                    </button>
                    {SOLIDS.includes(f.type) && (
                      <select value={f.op ?? "add"} onChange={(e) => editFeature(i, { ...f, op: e.target.value as PartFeature["op"] })}>
                        {CHOICES.op.map((o) => <option key={o}>{o}</option>)}
                      </select>
                    )}
                    <label title="Suppress: keep in the tree, skip in the build">
                      <input type="checkbox" checked={!f.suppressed} onChange={(e) => editFeature(i, { ...f, suppressed: !e.target.checked })} />on
                    </label>
                    <button disabled={i === 0} onClick={() => move(i, -1)} title="Move up">↑</button>
                    <button disabled={i === features.length - 1} onClick={() => move(i, 1)} title="Move down">↓</button>
                    <button onClick={() => editFeature(i, null)} title="Delete feature">✕</button>
                  </div>
                  {f.id === failed && <div className="bad-text">{part.errors[0].message}</div>}
                  {part.info?.[f.id]?.flat_length != null && (
                    <div className="hint">Flat pattern: {part.info[f.id].flat_length.toFixed(1)} × {part.info[f.id].flat_width.toFixed(0)} mm,
                      {" "}{part.info[f.id].bends} bend(s) (K-factor allowance)</div>
                  )}
                  {f.id === feature && <FeatureFields feature={f} onChange={(next) => editFeature(i, next)} />}
                </li>
              ))}
            </ol>
            <label>Add feature
              <select value="" disabled={busy} onChange={(e) => addFeature(e.target.value)}>
                <option value="">choose…</option>
                {Object.keys(FEATURE_DEFAULTS).map((t) => <option key={t} value={t}>{LABELS[t]}</option>)}
              </select>
            </label>
          </>
        )}
      </div>
    </div>
  );
}
