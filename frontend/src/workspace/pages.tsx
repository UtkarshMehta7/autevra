import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router";
import { api, backendHint } from "../api/client";
import type { DomainDef, LLMStatus, ProjectSummary, RunIndexItem, TestDefinition } from "../api/types";
import { STATUS_SHORT } from "../state/engineering";
import { llmLabel } from "../state/llm";
import { DownloadLink } from "../DownloadLink";

const when = (iso: string) => new Date(iso).toLocaleString();

function useLoad<T>(load: () => Promise<T>): [T | null, () => void, string | null] {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const reload = useCallback(() => {
    load().then((d) => { setData(d); setError(null); }).catch((e) => setError((e as Error).message));
  }, [load]);
  useEffect(reload, [reload]);
  return [data, reload, error];
}

/** On the hosted demo, projects belong to this browser (a key in its local storage). */
function BrowserWorkspaceNote() {
  const local = ["localhost", "127.0.0.1", "[::1]"].includes(globalThis.location?.hostname ?? "");
  if (local) return null;
  return <p className="hint">Projects on this demo are private to this browser: they are kept
    with a key stored here, so another browser, a private window or clearing site data starts
    an empty workspace. There are no accounts yet.</p>;
}

function Problem({ error }: { error: string | null }) {
  return error ? <p className="bad-text">Backend unreachable: {error}. {backendHint()}</p> : null;
}

export function Dashboard() {
  const [projects, , e1] = useLoad(api.listProjects);
  const [runs] = useLoad(api.allRuns);
  return (
    <>
      <h1>Dashboard</h1>
      <Problem error={e1} />
      <div className="ws-grid">
        <section className="ws-card">
          <h2>Recent projects</h2>
          {(projects ?? []).slice(0, 6).map((p) => (
            <div key={p.id} className="ws-row">
              <Link to={`/studio/${p.id}/design`}>{p.name}</Link>
              <small className="hint">{p.domain} · {when(p.updated_at)}</small>
            </div>
          ))}
          {projects?.length === 0 && <p className="hint">No projects yet.</p>}
          <Link to="/app/projects" className="button">All projects</Link>
        </section>
        <section className="ws-card">
          <h2>Recent simulation runs</h2>
          {(runs ?? []).slice(0, 8).map((r) => (
            <div key={r.id} className="ws-row">
              <span className={`status-pill ${r.current ? r.status : "stale"}`}>{r.current ? STATUS_SHORT[r.status] : "stale"}</span>
              <span>{r.project_name}: {r.test_name}, {r.target}, {r.scenario_label}</span>
            </div>
          ))}
          {runs?.length === 0 && <p className="hint">No runs yet: run a test in the studio's Simulation workspace.</p>}
          <Link to="/app/simulations" className="button">Simulation history</Link>
        </section>
      </div>
    </>
  );
}

export function Projects() {
  const navigate = useNavigate();
  const [projects, reload, error] = useLoad(api.listProjects);
  const [name, setName] = useState("");
  const [templates] = useLoad(api.templates);
  const [template, setTemplate] = useState("");
  const [renaming, setRenaming] = useState<string | null>(null);
  const [newName, setNewName] = useState("");
  const [confirm, setConfirm] = useState<ProjectSummary | null>(null);
  const create = async () => {
    const chosen = templates?.find((t) => t.id === template);
    const fallback = chosen ? chosen.label : `Vehicle ${(projects?.length ?? 0) + 1}`;
    const p = await api.createProject(name.trim() || fallback, "automotive", chosen?.id);
    navigate(`/studio/${p.id}/design`);
  };
  return (
    <>
      <h1>Projects</h1>
      <BrowserWorkspaceNote />
      <Problem error={error} />
      <form className="bench-controls" onSubmit={(e) => { e.preventDefault(); create(); }}>
        <input placeholder="New project name" value={name} onChange={(e) => setName(e.target.value)} />
        <select value={template} onChange={(e) => setTemplate(e.target.value)} aria-label="Start from">
          <option value="">Default design (sedan)</option>
          {(templates ?? []).map((t) => <option key={t.id} value={t.id}>{t.label}</option>)}
        </select>
        <button className="primary" type="submit">Create automotive project</button>
      </form>
      <table className="site-table">
        <thead><tr><th>Name</th><th>Domain</th><th>Updated</th><th /></tr></thead>
        <tbody>
          {(projects ?? []).map((p) => (
            <tr key={p.id}>
              <td>{renaming === p.id ? (
                <form onSubmit={async (e) => { e.preventDefault(); await api.renameProject(p.id, newName); setRenaming(null); reload(); }}>
                  <input autoFocus value={newName} onChange={(e) => setNewName(e.target.value)} />
                  <button type="submit">Save</button>
                </form>
              ) : <Link to={`/studio/${p.id}/design`}>{p.name}</Link>}</td>
              <td>{p.domain}</td>
              <td className="hint">{when(p.updated_at)}</td>
              <td className="actions">
                <Link className="button" to={`/studio/${p.id}/design`}>Open</Link>
                <button onClick={() => { setRenaming(p.id); setNewName(p.name); }}>Rename</button>
                <button onClick={async () => { await api.duplicateProject(p.id); reload(); }}>Duplicate</button>
                <button className="danger" onClick={() => setConfirm(p)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {confirm && (
        <div className="dialog" role="dialog" aria-modal="true" aria-labelledby="confirm-title">
          <div className="dialog-box">
            <h2 id="confirm-title">Delete “{confirm.name}”?</h2>
            <p>This permanently removes the project, its history, test runs, studies and requirements.</p>
            <div className="decision">
              <button className="danger" onClick={async () => { await api.deleteProject(confirm.id); setConfirm(null); reload(); }}>Delete permanently</button>
              <button onClick={() => setConfirm(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export function Models() {
  const navigate = useNavigate();
  const [templates] = useLoad(api.templates);
  const [tests] = useLoad(api.tests);
  const [catalogue] = useLoad(api.catalogue);
  const [plugins] = useLoad(api.plugins);
  const groups = new Map<string, number>();
  for (const p of catalogue?.parameters ?? []) groups.set(p.group, (groups.get(p.group) ?? 0) + 1);
  return (
    <>
      <h1>Models and templates</h1>
      <div className="ws-grid">
        <section className="ws-card">
          <h2>Vehicle templates</h2>
          <p className="hint">Each is the design the specification interview generates for the
            class: body style, proportions, wheels, springs and dampers, rule-checked.</p>
          <ul className="plain">{(templates ?? []).map((t) => (
            <li key={t.id}>
              <button onClick={async () => {
                const p = await api.createProject(t.label, "automotive", t.id);
                navigate(`/studio/${p.id}/design`);
              }}>Start</button> <strong>{t.label}</strong>
              <small className="hint"> {t.description}</small>
            </li>
          ))}</ul>
        </section>
        <section className="ws-card">
          <h2>Automotive vehicle model</h2>
          <p>Ladder-frame vehicle: body with glazing, frame, two beam axles, four wheels, four
            coil-over dampers, in seven body styles.</p>
          <ul className="plain">{[...groups].map(([g, n]) => <li key={g}>{g}: {n} parameters</li>)}</ul>
        </section>
        <section className="ws-card">
          <h2>Test definitions</h2>
          <ul className="plain">{(tests ?? []).map((t: TestDefinition) => (
            <li key={t.id}><strong>{t.name}</strong> <small className="hint">{t.credibility.replace(/_/g, " ")} · {t.scenarios.length} scenario(s)</small></li>
          ))}</ul>
        </section>
        <section className="ws-card">
          <h2>Plugins</h2>
          {plugins?.length ? plugins.map((p) => (
            <div key={p.name}><strong>{p.name}</strong> {p.version}<p className="hint">{p.description}</p></div>
          )) : <p className="hint">No plugins loaded. Example: start with <code>AUTEVRA_PLUGINS=autevra.contrib.brake_discs</code>.</p>}
        </section>
      </div>
    </>
  );
}

export function DomainsPage() {
  const navigate = useNavigate();
  const [domains] = useLoad(api.domains);
  return (
    <>
      <h1>Domains</h1>
      <p className="hint">Only domains marked available can host projects.</p>
      <div className="domain-list">
        {(domains ?? []).map((d: DomainDef) => (
          <div key={d.id} className="domain-row">
            <div><strong>{d.name}</strong><p className="hint">{d.description}</p></div>
            {d.status === "available" ? (
              <button className="primary" onClick={async () => {
                const p = await api.createProject(`${d.name} project`, d.id);
                navigate(`/studio/${p.id}/design`);
              }}>Start a project</button>
            ) : <span className={`badge-status ${d.status}`}>Roadmap only</span>}
          </div>
        ))}
      </div>
    </>
  );
}

export function Simulations() {
  const [runs, reload] = useLoad(api.allRuns);
  const [filter, setFilter] = useState("");
  const shown = (runs ?? []).filter((r: RunIndexItem) => !filter || r.test_id === filter);
  return (
    <>
      <h1>Simulation history</h1>
      <div className="bench-controls">
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="">all tests</option>
          {[...new Set((runs ?? []).map((r) => r.test_id))].map((t) => <option key={t}>{t}</option>)}
        </select>
        <button onClick={reload}>Refresh</button>
      </div>
      <table className="site-table">
        <thead><tr><th>Status</th><th>Project</th><th>Test</th><th>Scenario</th><th>Revision</th><th>Credibility</th><th>When</th></tr></thead>
        <tbody>
          {shown.map((r) => (
            <tr key={r.id}>
              <td><span className={`status-pill ${r.current ? r.status : "stale"}`}>{r.current ? STATUS_SHORT[r.status] : "stale"}</span></td>
              <td><Link to={`/studio/${r.project_id}/simulation`}>{r.project_name}</Link></td>
              <td>{r.test_name} · {r.target}</td>
              <td>{r.scenario_label}</td>
              <td>{r.history_cursor}</td>
              <td className="hint">{r.credibility.replace(/_/g, " ")}</td>
              <td className="hint">{when(r.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {shown.length === 0 && <p className="hint">No runs yet.</p>}
    </>
  );
}

export function Files() {
  const [projects] = useLoad(api.listProjects);
  return (
    <>
      <h1>Files</h1>
      <p className="hint">Exports are generated from the current design when downloaded. Uploading
        CAD or document files is not supported yet; requirements can be imported as ReqIF in the
        studio.</p>
      <table className="site-table">
        <thead><tr><th>Project</th><th>CAD</th><th>Requirements</th></tr></thead>
        <tbody>
          {(projects ?? []).map((p) => (
            <tr key={p.id}>
              <td>{p.name}</td>
              <td><DownloadLink className="button" href={api.stepUrl(p.id)}>STEP AP214</DownloadLink></td>
              <td><DownloadLink className="button" href={api.reqifUrl(p.id)}>ReqIF</DownloadLink></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export function Settings() {
  const [llm, setLlm] = useState<LLMStatus | null>(null);
  useEffect(() => { api.llmStatus().then(setLlm).catch(() => setLlm(null)); }, []);
  return (
    <>
      <h1>Settings</h1>
      <section className="ws-card">
        <h2>Local language model</h2>
        <p>{llmLabel(llm)} {llm?.detail && <span className="hint">— {llm.detail}</span>}</p>
        <p className="hint">Configured on the backend with environment variables
          (<code>AUTEVRA_LLM_PROVIDER</code>, <code>AUTEVRA_LLM_MODEL</code>, <code>AUTEVRA_LLM_URL</code>).
          Set the provider to <code>off</code> for a fully deterministic app. No hosted inference is used.</p>
        {llm?.models?.length ? <p className="hint">Models installed: {llm.models.join(", ")}</p> : null}
      </section>
      <section className="ws-card">
        <h2>Plugins</h2>
        <p className="hint">Enable plugins with <code>AUTEVRA_PLUGINS</code> (comma-separated
          modules) or by installing packages with the <code>autevra.plugins</code> entry point.</p>
      </section>
      <section className="ws-card">
        <h2>Accounts</h2>
        <p className="hint">This build is single-user and local; there are no accounts or sign-in.</p>
      </section>
    </>
  );
}
