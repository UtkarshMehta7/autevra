import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import type { FeaCatalogue, FeaMesh, FeaRequest, FeaResult, PartOut } from "../api/types";
import { type FeaField, FeaView, rainbow } from "./FeaView";
import { TopologyPanel } from "./TopologyPanel";

/** Structures workspace: linear static finite element analysis of a demo geometry or a Part
 * Design part, with the computation on show: mesh statistics and quality, the size and
 * sparsity of K, conjugate-gradient convergence, the equilibrium check, and the results
 * (backend fea/). */

const FIELDS: Record<FeaField, { label: string; unit: string }> = {
  von_mises: { label: "von Mises stress", unit: "MPa" },
  magnitude: { label: "Displacement |u|", unit: "mm" },
  principal_1: { label: "Max principal stress σ₁", unit: "MPa" },
  strain_eq: { label: "Equivalent strain", unit: "" },
};

export function StructuresPanel({ projectId }: { projectId?: string }) {
  const [catalogue, setCatalogue] = useState<FeaCatalogue | null>(null);
  const [parts, setParts] = useState<PartOut[]>([]);
  const [source, setSource] = useState("demo:cantilever");
  const [req, setReq] = useState<FeaRequest>({
    element: "tet10", size: 8, material: { name: "Structural steel" },
    supports: ["x-min"], loads: [{ region: "x-max", force: [0, 0, -1000], pressure: 0 }],
  });
  const [result, setResult] = useState<FeaResult | null>(null);
  const [preview, setPreview] = useState<FeaMesh | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [field, setField] = useState<FeaField>("von_mises");
  const [scale, setScale] = useState<number | null>(null);
  const [edges, setEdges] = useState(true);

  useEffect(() => { api.feaCatalogue().then(setCatalogue).catch(() => setCatalogue(null)); }, []);
  useEffect(() => {
    if (projectId) api.parts(projectId).then(setParts).catch(() => setParts([]));
  }, [projectId]);

  const material = catalogue?.materials[req.material.name];
  const target = () => {
    const [kind, id] = source.split(":");
    return kind === "part" && projectId ? { body: req, part: { project: projectId, part: id } } : { body: { ...req, demo: id } };
  };
  const run = async () => {
    setBusy(true);
    setError(null);
    try {
      const { body, part } = target();
      const out = await api.runFea(body, part);
      setResult(out);
      setPreview(out.mesh);
      setScale(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };
  const meshOnly = async () => {
    setBusy(true);
    setError(null);
    try {
      const { body, part } = target();
      setPreview((await api.feaMesh(body, part)).mesh);
      setResult(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };
  // Face roles from the request: supports and the load region on the part's own faces.
  const faceOf = (region: string) => (region.startsWith("face:") ? Number(region.slice(5)) : null);
  const roles: Record<number, "support" | "load"> = {};
  for (const r of req.supports) { const f = faceOf(r); if (f != null) roles[f] = "support"; }
  { const f = faceOf(req.loads[0].region); if (f != null) roles[f] = "load"; }
  // A click on a face cycles it: free -> support -> load -> free (one loaded face).
  const pickFace = (face: number) => {
    const region = `face:${face}`;
    // the first face picked as a support replaces the bounding-box supports
    const faces = req.supports.some((r) => r.startsWith("face:"));
    const supports = req.supports.filter((r) => r !== region && (faces || roles[face] !== undefined || r.startsWith("face:")));
    const loads = [...req.loads];
    if (roles[face] === undefined) supports.push(region);
    else if (roles[face] === "support") loads[0] = { ...loads[0], region };
    else loads[0] = { ...loads[0], region: "x-max" }; // a load face goes back to free
    setReq({ ...req, supports, loads });
    setResult(null);
  };
  const faceLabel = (region: string) => {
    const f = faceOf(region);
    const face = f != null ? preview?.faces[f] : undefined;
    return face ? `face ${f} (${face.type}, ${(face.area / 100).toFixed(1)} cm²)` : region;
  };

  const autoScale = useMemo(() => {
    if (!result) return 1;
    const xs = result.mesh.nodes.map((n) => n[0]), ys = result.mesh.nodes.map((n) => n[1]), zs = result.mesh.nodes.map((n) => n[2]);
    const size = Math.max(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys), Math.max(...zs) - Math.min(...zs));
    return result.stats.max_displacement > 0 ? +(0.08 * size / result.stats.max_displacement).toPrecision(2) : 1;
  }, [result]);
  const shown = scale ?? autoScale;
  const load = req.loads[0];
  const setLoad = (patch: Partial<FeaRequest["loads"][number]>) => setReq({ ...req, loads: [{ ...load, ...patch }] });
  const values = result?.fields[field] ?? [];
  const lo = values.length ? Math.min(...values) : 0, hi = values.length ? Math.max(...values) : 0;
  const s = result?.stats;

  return (
    <div className="bench wide surfaces-lab structures">
      <div className="lab-view">
        <FeaView result={result} preview={preview} field={field} scale={shown} edges={edges}
          roles={roles} onPick={pickFace} />
        <div className="lab-toolbar">
          {(Object.keys(FIELDS) as FeaField[]).map((f) => (
            <button key={f} className={field === f ? "on" : ""} onClick={() => setField(f)}>{FIELDS[f].label}</button>
          ))}
          <label><input type="checkbox" checked={edges} onChange={(e) => setEdges(e.target.checked)} /> mesh</label>
        </div>
        {result && (
          <div className="legend">
            <div className="bar" style={{ background: `linear-gradient(to right, ${[0, 0.25, 0.5, 0.75, 1].map((t) => `rgb(${rainbow(t).map((c) => Math.round(c * 255)).join(",")})`).join(",")})` }} />
            <div className="ends"><span>{fmt(lo)}</span><span>{FIELDS[field].unit}</span><span>{fmt(hi)}</span></div>
            <label>deformation ×{shown}
              <input type="range" min={0} max={Math.max(autoScale * 4, 1)} step={autoScale / 20 || 0.1} value={shown}
                onChange={(e) => setScale(Number(e.target.value))} />
            </label>
          </div>
        )}
        {busy && <div className="lab-busy">Meshing, assembling K and solving…</div>}
      </div>
      <div className="lab-side">
        <div className="row">
          <select value={source} onChange={(e) => {
            setSource(e.target.value);
            setPreview(null);
            setResult(null);
            setReq({ ...req, supports: ["x-min"], loads: [{ ...req.loads[0], region: "x-max" }] });
          }}>
            {catalogue && Object.entries(catalogue.demos).map(([k, v]) => <option key={k} value={`demo:${k}`}>{v}</option>)}
            {parts.filter((p) => p.volume).map((p) => <option key={p.id} value={`part:${p.id}`}>Part: {p.document.name}</option>)}
          </select>
        </div>
        <div className="row">
          <label>elements
            <select value={req.element} onChange={(e) => setReq({ ...req, element: e.target.value as FeaRequest["element"] })}>
              <option value="tet10">TET10 (quadratic tetrahedra)</option>
              <option value="tet4">TET4 (linear tetrahedra)</option>
              <option value="hex8">HEX8 (voxels)</option>
            </select>
          </label>
          <label>size <input type="number" min={0.5} step={0.5} value={req.size} style={{ width: 60 }}
            onChange={(e) => setReq({ ...req, size: Number(e.target.value) })} /> mm</label>
        </div>
        <div className="row">
          <label>material
            <select value={req.material.name} onChange={(e) => setReq({ ...req, material: { name: e.target.value } })}>
              {catalogue && Object.keys(catalogue.materials).map((m) => <option key={m}>{m}</option>)}
            </select>
          </label>
          {material && (
            <span className="muted">E {material.youngs.toLocaleString()} MPa · ν {material.poisson} · ρ {material.density} kg/m³ · σy {material.yield_strength} MPa</span>
          )}
        </div>
        <div className="row">
          <strong>Supports</strong>
          {(catalogue?.regions ?? []).map((r) => (
            <label key={r}><input type="checkbox" checked={req.supports.includes(r)} onChange={(e) => setReq({
              ...req, supports: e.target.checked ? [...req.supports, r] : req.supports.filter((x) => x !== r) })} />{r}</label>
          ))}
          {req.supports.filter((r) => r.startsWith("face:")).map((r) => (
            <span key={r} className="chip support">{faceLabel(r)}
              <button title="Remove" onClick={() => setReq({ ...req, supports: req.supports.filter((x) => x !== r) })}>×</button></span>
          ))}
        </div>
        <div className="row">
          <strong>Load on</strong>
          <select value={load.region} onChange={(e) => setLoad({ region: e.target.value })}>
            {(catalogue?.regions ?? []).map((r) => <option key={r}>{r}</option>)}
            {load.region.startsWith("face:") && <option value={load.region}>{faceLabel(load.region)}</option>}
          </select>
          {(["Fx", "Fy", "Fz"] as const).map((n, i) => (
            <label key={n}>{n} <input type="number" step={100} value={load.force[i]} style={{ width: 70 }} onChange={(e) => {
              const f = [...load.force] as [number, number, number];
              f[i] = Number(e.target.value);
              setLoad({ force: f });
            }} /></label>
          ))}
          <span className="muted">N</span>
          <label>p <input type="number" step={0.5} value={load.pressure} style={{ width: 56 }}
            onChange={(e) => setLoad({ pressure: Number(e.target.value) })} /> MPa</label>
        </div>
        <div className="row">
          <button disabled={busy} onClick={meshOnly} title="Mesh the part to pick faces: click a face for a support, again for the load, again to clear">Mesh (pick faces)</button>
          <button className="primary" disabled={busy || req.supports.length === 0} onClick={run}>{busy ? "Solving…" : "Mesh and solve"}</button>
          {error && <span className="error">{error}</span>}
        </div>
        {result && s && (
          <>
            <div className="math">
              <div>K u = F — {s.dofs.toLocaleString()} DOFs ({s.free_dofs.toLocaleString()} free, {s.fixed_dofs.toLocaleString()} fixed)</div>
              <div>Kₑ = ∫ Bᵀ D B dV: {s.element_matrix.join(" × ")} per element ({result.mesh.kind.toUpperCase()})</div>
              <div>K: {s.k_shape[0].toLocaleString()} × {s.k_shape[1].toLocaleString()}, {s.k_nnz.toLocaleString()} non-zeros ({(s.k_density * 100).toFixed(3)} % dense, {s.k_memory_mb.toFixed(1)} MB in CSR)</div>
              <div>Mesh: {result.mesh.stats.nodes.toLocaleString()} nodes, {result.mesh.stats.elements.toLocaleString()} elements · volume {(result.mesh.stats.volume_ratio * 100).toFixed(1)} % of the CAD solid · quality q min {result.mesh.stats.quality_min.toFixed(2)}, mean {result.mesh.stats.quality_mean.toFixed(2)}{result.mesh.stats.slivers ? `, ${result.mesh.stats.slivers} slivers` : ""}</div>
              <div className={s.cg_converged ? "good-text" : "bad-text"}>CG: {s.cg_iterations} iterations, |F − Ku|/|F| = {s.cg_final_residual.toExponential(2)} {s.cg_converged ? "converged" : "not converged"}{s.direct_difference != null && ` · direct solve differs by ${s.direct_difference.toExponential(1)}`}</div>
              <div className={s.equilibrium_error < 1e-6 ? "good-text" : "bad-text"}>Equilibrium: ΣF = ({s.applied_force.map(fmt).join(", ")}) N, ΣR = ({s.reaction_force.map(fmt).join(", ")}) N, error {s.equilibrium_error.toExponential(1)}</div>
            </div>
            <Residuals values={s.cg_residuals} total={s.cg_iterations} />
            <div className="math results">
              <div>max |u| = {fmt(s.max_displacement)} mm · max σ_vM = {fmt(s.max_von_mises)} MPa</div>
              <div>σ₁ max = {fmt(s.max_principal)} MPa · σ₃ min = {fmt(s.min_principal)} MPa</div>
              <div className={(s.factor_of_safety ?? 99) >= 1.5 ? "good-text" : (s.factor_of_safety ?? 99) >= 1 ? "" : "bad-text"}>
                factor of safety σy / σ_vM,max = {s.factor_of_safety ? s.factor_of_safety.toFixed(2) : "∞"}</div>
              <div>mass {s.mass_kg.toFixed(3)} kg · compliance F·u = {fmt(s.compliance)} N·mm · assembly {(s.time_assemble * 1000).toFixed(0)} ms, solve {(s.time_solve * 1000).toFixed(0)} ms</div>
            </div>
            <details>
              <summary>Assumptions (educational solver)</summary>
              <ul className="assumptions">{result.assumptions.map((a) => <li key={a}>{a}</li>)}</ul>
              <p className="muted">Mesher: {result.mesh.stats.method}. Solver: {s.method}.</p>
            </details>
          </>
        )}
      </div>
    </div>
  );
}

function fmt(v: number): string {
  const a = Math.abs(v);
  return a === 0 ? "0" : a >= 1e4 || a < 1e-2 ? v.toExponential(2) : v.toPrecision(4);
}

function Residuals({ values, total }: { values: number[]; total: number }) {
  if (!values.length) return null;
  const W = 300, H = 80, L = 30;
  const ys = values.map((v) => Math.log10(Math.max(v, 1e-16)));
  const lo = Math.min(...ys, -9), hi = Math.max(...ys, 0);
  const x = (i: number) => L + (i / Math.max(values.length - 1, 1)) * (W - L - 6);
  const y = (v: number) => 6 + (1 - (v - lo) / Math.max(hi - lo, 1e-9)) * (H - 20);
  return (
    <svg className="chart convergence" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Conjugate gradient convergence">
      <text x={L} y={10} className="chart-title">log₁₀ |F − Ku| / |F| per CG iteration</text>
      {[hi, lo].map((v) => (
        <g key={v}><line x1={L} x2={W - 4} y1={y(v)} y2={y(v)} className="grid" />
          <text x={L - 4} y={y(v) + 3} textAnchor="end" className="tick">{v.toFixed(0)}</text></g>
      ))}
      <path className="series" d={ys.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join("")} />
      <text x={W - 4} y={H - 3} textAnchor="end" className="tick">{total > values.length ? `last ${values.length} of ${total}` : total} iterations</text>
    </svg>
  );
}

/** The Structures workspace: static analysis of a part, or topology optimisation. */
export function StructuresWorkspace({ projectId }: { projectId?: string }) {
  const [mode, setMode] = useState<"analysis" | "topology">("analysis");
  return (
    <div className="structures-workspace">
      <div className="mode-switch">
        <button className={mode === "analysis" ? "on" : ""} onClick={() => setMode("analysis")}>Static analysis (FEA)</button>
        <button className={mode === "topology" ? "on" : ""} onClick={() => setMode("topology")}>Topology optimisation (SIMP)</button>
      </div>
      {mode === "analysis" ? <StructuresPanel projectId={projectId} /> : <TopologyPanel />}
    </div>
  );
}
