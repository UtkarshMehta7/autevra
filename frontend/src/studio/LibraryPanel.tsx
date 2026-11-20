import { useEffect, useState } from "react";
import { api, type LibraryEntry } from "../api/client";
import { MODULES } from "./workspaces";

/** Design library (every module): save the current design as a reusable starting point,
 * browse the designs of all modules and start a new project from one. A saved design is a
 * snapshot of the whole project (parameters, parts, module specs, styling, constraints,
 * requirements), so later edits of the project do not change it. */

export function LibraryPanel({ projectId, projectName, onOpen }: { projectId: string; projectName: string; onOpen: (id: string, domain: string) => void }) {
  const [entries, setEntries] = useState<LibraryEntry[]>([]);
  const [filter, setFilter] = useState("");
  const [name, setName] = useState(projectName);
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState("");
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const load = () => api.library().then(setEntries).catch(() => setEntries([]));
  useEffect(() => { load(); }, []);
  useEffect(() => setName(projectName), [projectName]);
  const act = async (f: () => Promise<void>) => {
    setBusy(true); setNote(null);
    try { await f(); } catch (e) { setNote(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };
  const label = (domain: string) => MODULES.find((m) => m.id === domain)?.label ?? domain;
  const shown = entries.filter((e) => !filter || e.domain === filter);
  return (
    <section className="elements-panel library-panel">
      <div className="el-body">
        <div className="el-inputs">
          <h4>Save this design</h4>
          <label className="el-field wide">name<input value={name} onChange={(e) => setName(e.target.value)} /></label>
          <label className="el-field wide">description<textarea rows={3} value={description} onChange={(e) => setDescription(e.target.value)} placeholder="What it is, what it is for, what makes it new" /></label>
          <label className="el-field wide">tags<input value={tags} onChange={(e) => setTags(e.target.value)} placeholder="comma separated" /></label>
          <button disabled={busy || !name.trim()} onClick={() => act(async () => {
            const e = await api.saveToLibrary({ project_id: projectId, name: name.trim(), description, tags: tags.split(",").map((t) => t.trim()).filter(Boolean) });
            setNote(`Saved “${e.name}” (${e.parts} part${e.parts === 1 ? "" : "s"}).`); await load();
          })}>Save to library</button>
          <p className="small muted">A snapshot of everything that defines the design. Use <b>File → Export design</b> to share it as a file.</p>
          {note && <p className="small">{note}</p>}
        </div>
        <div className="el-out">
          <div className="row wrap">
            <h4 style={{ margin: 0 }}>Library</h4>
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="">all modules</option>
              {MODULES.filter((m) => !m.planned).map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}
            </select>
          </div>
          {shown.length === 0 ? <p className="small muted">No saved designs yet. Save one on the left; it appears here for every module's projects.</p> : (
            <div className="library-grid">
              {shown.map((e) => (
                <div key={e.id} className="library-card">
                  <div className="lc-head"><b>{e.name}</b><span className="chip">{label(e.domain)}</span></div>
                  {e.description && <p className="small">{e.description}</p>}
                  <p className="small muted">{e.parts} part{e.parts === 1 ? "" : "s"} · saved {e.created.slice(0, 10)}{e.tags.length ? ` · ${e.tags.join(", ")}` : ""}</p>
                  <div className="row">
                    <button disabled={busy} onClick={() => act(async () => { const p = await api.useLibraryDesign(e.id); onOpen(p.id, p.domain ?? e.domain); })}>New project from this</button>
                    <button disabled={busy} title="Remove from the library (projects made from it stay)" onClick={() => act(async () => { await api.deleteLibraryDesign(e.id); await load(); })}>Remove</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
