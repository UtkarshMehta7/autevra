import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { PartDoc, PartFeature, PartOut, Placement } from "../api/types";

/** Defaults for a new feature of each type (mm, degrees). */
const FEATURE_DEFAULTS: Record<string, Omit<PartFeature, "id" | "type">> = {
  box: { size: [100, 100, 100] },
  cylinder: { radius: 50, height: 100, axis: "z" },
  sphere: { radius: 50 },
  extrude: { plane: "xy", points: [[0, 0], [100, 0], [100, 60], [0, 60]], depth: 20, symmetric: false },
  revolve: { points: [[0, 0], [40, 0], [40, 100], [0, 100]], angle: 360 },
  loft: { sections: [{ z: 0, width: 100, height: 100, radius: 20 }, { z: 200, width: 60, height: 60, radius: 20 }], ruled: false },
  sweep: { path: [[0, 0, 0], [300, 0, 0], [300, 200, 0]], radius: 15, wall: 2, bend_radius: 40 },
  wing: { naca: "2412", root_chord: 1600, tip_chord: 800, span: 5000, sweep: 5, dihedral: 3, twist: -2, both_sides: true },
  shell: { thickness: 3, open_towards: "+z" },
  fillet: { radius: 3, edges: "" },
  chamfer: { size: 2, edges: "" },
  mirror: { plane: "xz" },
  linear_pattern: { count: 3, step: [150, 0, 0] },
  circular_pattern: { count: 6, axis: "z", angle: 360 },
};
const SOLIDS = ["box", "cylinder", "sphere", "extrude", "revolve", "loft", "sweep", "wing"];
const LABELS: Record<string, string> = {
  box: "Box", cylinder: "Cylinder", sphere: "Sphere", extrude: "Extrude sketch",
  revolve: "Revolve profile", loft: "Loft sections", sweep: "Sweep tube",
  wing: "Wing (NACA aerofoil)", shell: "Shell",
  fillet: "Fillet edges", chamfer: "Chamfer edges", mirror: "Mirror", linear_pattern: "Linear pattern",
  circular_pattern: "Circular pattern",
};
const CHOICES: Record<string, string[]> = {
  op: ["add", "cut", "intersect"], axis: ["x", "y", "z"], plane: ["xy", "xz", "yz"],
  open_towards: ["none", "+x", "-x", "+y", "-y", "+z", "-z"],
};

/** Starting parts from several domains, to edit rather than start from nothing. */
const PRESETS: Record<string, PartDoc> = {
  "Blank part": { name: "Part", features: [{ id: "base", type: "box", size: [200, 100, 50] }] },
  "Mounting bracket": { name: "Bracket", parameters: { width: 200, thickness: 15, hole: "width / 25" }, features: [
    { id: "plate", type: "box", size: [200, 200, 15], bindings: { "size.0": "width", "size.1": "width", "size.2": "thickness" } },
    { id: "hole", type: "cylinder", op: "cut", radius: 8, height: 40, at: { x: 70 },
      bindings: { radius: "hole", "at.x": "width / 2 - 3 * hole" } },
    { id: "holes", type: "circular_pattern", count: 4 },
    { id: "round", type: "fillet", radius: 2 }] },
  "Bottle (consumer product)": { name: "Bottle", finish: "trim", features: [
    { id: "body", type: "revolve", points: [[0, 0], [40, 0], [40, 180], [15, 220], [15, 250], [0, 250]] },
    { id: "hollow", type: "shell", thickness: 2, open_towards: "+z" }] },
  "Pipe run (plant)": { name: "Pipe run", features: [
    { id: "run", type: "sweep", path: [[0, 0, 0], [800, 0, 0], [800, 600, 0], [800, 600, 500]],
      radius: 40, wall: 4, bend_radius: 120 }] },
  "Fuselage (aerospace)": { name: "Fuselage", features: [
    { id: "skin", type: "loft", at: { ry: 90 }, sections: [
      { z: 0, width: 200, height: 200, radius: 99 }, { z: 2000, width: 2400, height: 2600, radius: 1150 },
      { z: 14000, width: 2400, height: 2600, radius: 1150 }, { z: 18000, width: 600, height: 900, radius: 290 }] }] },
  "Light aircraft (aerospace)": {"name": "Light aircraft", "color": [0.85, 0.86, 0.88], "finish": "paint", "features": [{"id": "fuselage", "type": "loft", "at": {"ry": -90}, "sections": [{"z": 0, "width": 300, "height": 300, "radius": 149}, {"z": 1500, "width": 1200, "height": 1400, "radius": 550}, {"z": 4500, "width": 1200, "height": 1400, "radius": 550}, {"z": 8000, "width": 200, "height": 400, "radius": 90}]}, {"id": "wing", "type": "wing", "naca": "2412", "root_chord": 1600, "tip_chord": 1000, "span": 4500, "sweep": 2, "dihedral": 5, "twist": -2, "at": {"x": -2200, "z": -350}}, {"id": "tailplane", "type": "wing", "naca": "0010", "root_chord": 900, "tip_chord": 600, "span": 1600, "sweep": 8, "dihedral": 0, "twist": 0, "at": {"x": -6900, "z": 150}}, {"id": "fin", "type": "wing", "naca": "0010", "root_chord": 1100, "tip_chord": 600, "span": 1300, "sweep": 30, "dihedral": 0, "twist": 0, "both_sides": false, "at": {"x": -6800, "z": 250, "rx": 90}}]},
  "Turbine disc (propulsion)": { name: "Turbine disc", features: [
    { id: "disc", type: "revolve", points: [[30, -20], [300, -8], [300, 8], [30, 20]] },
    { id: "blade", type: "box", size: [80, 6, 40], at: { x: 330, rx: 20 } },
    { id: "blades", type: "circular_pattern", count: 36 }] },
  "Conveyor frame (machinery)": { name: "Conveyor frame", features: [
    { id: "rail", type: "box", size: [3000, 60, 60] },
    { id: "leg", type: "box", size: [60, 60, 800], at: { x: -1440, z: -430 } },
    { id: "legs", type: "linear_pattern", count: 5, step: [720, 0, 0] },
    { id: "pair", type: "mirror", plane: "xz" }], at: { y: 400 } },
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
            const preset = PRESETS[e.target.value];
            if (preset) run(() => api.createPart(projectId, structuredClone(preset)));
          }}>
            <option value="">choose a starting point…</option>
            {Object.keys(PRESETS).map((k) => <option key={k}>{k}</option>)}
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
