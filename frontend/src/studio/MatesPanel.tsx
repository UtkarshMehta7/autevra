import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { PartOut } from "../api/types";
import { setOverlay } from "../viewport/overlay";

/** Assembly design (every module): constraints between the project's parts, as in an
 * assembly workbench. Fix the base part, then mate faces: Coincidence (coplanar planes,
 * coaxial cylinders, an axis in a plane), Contact (faces touching), Offset and Angle. Update
 * solves them (Levenberg-Marquardt over each free part's six degrees of freedom) and moves
 * the parts; the degrees of freedom left and any conflicting constraint are reported. */

type Kind = "fix" | "coincidence" | "contact" | "offset" | "angle";
interface FaceRef { part: string; face: number; sig?: unknown }
interface Constraint { id: string; kind: Kind; a?: FaceRef | null; b?: FaceRef | null; part?: string | null; value: number; suppressed?: boolean }
interface Face { index: number; kind: string; label: string; outline: [number, number, number][] }
interface SolveOut { status: { id: string; kind: string; residual: number; ok: boolean }[]; dof: number; dof_by_part: Record<string, number>; conflicts: string[]; moved: string[]; notes: string[]; fixed: string[]; applied: boolean }

const KINDS: { id: Kind; label: string; hint: string }[] = [
  { id: "fix", label: "Fix", hint: "anchor a part where it is" },
  { id: "coincidence", label: "Coincidence", hint: "coaxial cylinders, coplanar planes, or an axis lying in a plane" },
  { id: "contact", label: "Contact", hint: "two planar faces touching, face to face" },
  { id: "offset", label: "Offset", hint: "two planar faces facing each other at a distance" },
  { id: "angle", label: "Angle", hint: "angle between two faces' normals or axes" },
];

function FacePick({ parts, value, onChange, faces }: { parts: PartOut[]; value: FaceRef | null; onChange: (r: FaceRef | null) => void; faces: Record<string, Face[]> }) {
  const list = value ? faces[value.part] ?? [] : [];
  return (
    <span className="mate-pick">
      <select value={value?.part ?? ""} onChange={(e) => onChange(e.target.value ? { part: e.target.value, face: 0 } : null)}>
        <option value="">part…</option>
        {parts.map((p) => <option key={p.id} value={p.id}>{p.document.name}</option>)}
      </select>
      {value && (
        <select value={value.face} onChange={(e) => onChange({ part: value.part, face: Number(e.target.value) })}>
          {list.map((f) => <option key={f.index} value={f.index}>#{f.index} {f.label}</option>)}
        </select>
      )}
    </span>
  );
}

export function MatesPanel({ projectId, version, onModelChanged }: { projectId: string; version?: number; onModelChanged: () => void }) {
  const [parts, setParts] = useState<PartOut[]>([]);
  const [faces, setFaces] = useState<Record<string, Face[]>>({});
  const [list, setList] = useState<Constraint[]>([]);
  const [kind, setKind] = useState<Kind>("coincidence");
  const [a, setA] = useState<FaceRef | null>(null);
  const [b, setB] = useState<FaceRef | null>(null);
  const [fixPart, setFixPart] = useState("");
  const [value, setValue] = useState(0);
  const [report, setReport] = useState<SolveOut | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const name = useCallback((id?: string | null) => parts.find((p) => p.id === id)?.document.name ?? id ?? "?", [parts]);
  const faceLabel = (r?: FaceRef | null) => r ? `${name(r.part)} #${r.face} ${faces[r.part]?.find((f) => f.index === r.face)?.label ?? ""}` : "";

  useEffect(() => {
    api.parts(projectId).then((p) => { const solids = p.filter((x) => x.volume != null); setParts(solids); setFixPart((cur) => cur || solids[0]?.id || ""); }).catch(() => setParts([]));
    api.mates(projectId).then((d) => setList(d.constraints as Constraint[])).catch(() => setList([]));
  }, [projectId, version]);
  useEffect(() => () => setOverlay(null), []);

  const loadFaces = useCallback((part: string) => {
    if (!part || faces[part]) return;
    api.mateFaces(projectId, part).then((f) => setFaces((cur) => ({ ...cur, [part]: f as Face[] }))).catch(() => undefined);
  }, [projectId, faces]);
  useEffect(() => { if (a) loadFaces(a.part); if (b) loadFaces(b.part); }, [a, b, loadFaces]);
  useEffect(() => { for (const c of list) { if (c.a) loadFaces(c.a.part); if (c.b) loadFaces(c.b.part); } }, [list, loadFaces]);

  const highlight = (r: FaceRef | null) => {
    const f = r ? faces[r.part]?.find((x) => x.index === r.face) : undefined;
    setOverlay(r && f && f.outline.length > 1 ? { partId: `part_${r.part}`, polylines: [[...f.outline, f.outline[0]]], color: 0x4fd1ff } : null);
  };
  useEffect(() => highlight(b ?? a), [a, b, faces]); // eslint-disable-line react-hooks/exhaustive-deps

  const save = async (next: Constraint[]) => {
    setBusy(true); setError(null);
    try { const d = await api.saveMates(projectId, { constraints: next }); setList(d.constraints as Constraint[]); return true; }
    catch (e) { setError(e instanceof Error ? e.message : String(e)); return false; } finally { setBusy(false); }
  };
  const add = async () => {
    const id = `${kind}${list.filter((c) => c.kind === kind).length + 1}`;
    const c: Constraint = kind === "fix" ? { id, kind, part: fixPart, value: 0 } : { id, kind, a, b, value };
    if (await save([...list, c])) { setA(null); setB(null); }
  };
  const update = async () => {
    setBusy(true); setError(null);
    try {
      const r = await api.solveMates(projectId) as SolveOut;
      setReport(r);
      if (r.applied && r.moved.length) onModelChanged();
    } catch (e) { setError(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };
  const status = (id: string) => report?.status.find((s) => s.id === id);
  const ready = kind === "fix" ? !!fixPart : !!(a && b && a.part !== b.part);

  return (
    <section className="elements-panel mates-panel">
      <p className="small muted el-method">Fix the base part, then pick a face on each of two parts. Update solves every constraint together and moves the parts (undo per part in Part Design). Faces are matched again by their shape when a part is edited.</p>
      {parts.length < 2 && <p className="small muted">Add at least two parts (Part Design, Inventory, Machine elements or STEP import) to constrain them.</p>}
      <div className="el-body">
        <div className="el-inputs">
          <label className="el-field">constraint
            <select value={kind} onChange={(e) => setKind(e.target.value as Kind)}>
              {KINDS.map((k) => <option key={k.id} value={k.id}>{k.label}</option>)}
            </select>
          </label>
          <p className="small muted">{KINDS.find((k) => k.id === kind)?.hint}</p>
          {kind === "fix" ? (
            <label className="el-field">part
              <select value={fixPart} onChange={(e) => setFixPart(e.target.value)}>
                {parts.map((p) => <option key={p.id} value={p.id}>{p.document.name}</option>)}
              </select>
            </label>
          ) : <>
            <label className="el-field wide">first face <FacePick parts={parts} value={a} onChange={setA} faces={faces} /></label>
            <label className="el-field wide">second face <FacePick parts={parts} value={b} onChange={setB} faces={faces} /></label>
            {(kind === "offset" || kind === "angle") && (
              <label className="el-field">{kind === "offset" ? "distance" : "angle"}
                <span><input type="number" value={value} onChange={(e) => setValue(Number(e.target.value) || 0)} /><em>{kind === "offset" ? "mm" : "°"}</em></span>
              </label>
            )}
          </>}
          <button disabled={busy || !ready} onClick={add}>Add constraint</button>
          <button disabled={busy || list.length === 0} onClick={update}>{busy ? "Solving…" : "Update (solve and move parts)"}</button>
          {error && <p className="el-warn bad">{error}</p>}
        </div>
        <div className="el-out">
          {list.length === 0 ? <p className="small muted">No constraints yet.</p> : (
            <table className="bd-table"><thead><tr><th>id</th><th>type</th><th>between</th><th className="num">value</th><th>status</th><th /></tr></thead><tbody>
              {list.map((c, i) => {
                const st = status(c.id);
                return (
                  <tr key={c.id} className={c.suppressed ? "muted" : ""} onMouseEnter={() => highlight(c.a ?? null)} onMouseLeave={() => highlight(b ?? a)}>
                    <td>{c.id}</td><td>{c.kind}</td>
                    <td className="wrap">{c.kind === "fix" ? name(c.part) : `${faceLabel(c.a)} ↔ ${faceLabel(c.b)}`}</td>
                    <td className="num">{c.kind === "offset" ? `${c.value} mm` : c.kind === "angle" ? `${c.value}°` : ""}</td>
                    <td className={st ? (st.ok ? "good" : "bad") : "muted"}>{st ? (st.ok ? "✓ satisfied" : `✗ conflict (${st.residual.toExponential(1)})`) : "—"}</td>
                    <td>
                      <button title="Suppress or activate" onClick={() => save(list.map((x, j) => (j === i ? { ...x, suppressed: !x.suppressed } : x)))}>{c.suppressed ? "on" : "off"}</button>
                      <button title="Delete" onClick={() => save(list.filter((_, j) => j !== i))}>✕</button>
                    </td>
                  </tr>
                );
              })}
            </tbody></table>
          )}
          {report && <>
            <div className="cam-tiles">
              <div><b className={report.conflicts.length ? "bad" : "good"}>{report.conflicts.length ? `${report.conflicts.length} conflict${report.conflicts.length > 1 ? "s" : ""}` : "solved"}</b><span>{report.applied ? `${report.moved.length} part(s) moved` : "nothing moved"}</span></div>
              <div><b>{report.dof}</b><span>degrees of freedom left</span></div>
            </div>
            <table className="bd-table"><thead><tr><th>part</th><th className="num">DOF left</th><th>state</th></tr></thead><tbody>
              {Object.entries(report.dof_by_part).map(([p, d]) => (
                <tr key={p}><td>{name(p)}</td><td className="num">{d}</td>
                  <td className={d === 0 ? "good" : "warn"}>{report.fixed.includes(p) ? "fixed" : d === 0 ? "fully constrained" : d === 6 ? "free (no constraint)" : "under-constrained"}</td></tr>
              ))}
            </tbody></table>
            {report.notes.length > 0 && <ul className="small cam-notes">{report.notes.map((n) => <li key={n}>{n}</li>)}</ul>}
          </>}
        </div>
      </div>
    </section>
  );
}
