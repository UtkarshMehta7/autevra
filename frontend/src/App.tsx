import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from "./api/client";
import type {
  CommandResult, HistoryEntry, LLMStatus, ModelPayload, ParameterDef, ProjectState,
  ProjectSummary,
} from "./api/types";
import { AiPanel, type ChatTurn } from "./panels/AiPanel";
import { ComponentTree } from "./panels/ComponentTree";
import { HistoryPanel } from "./panels/HistoryPanel";
import { PropertyEditor } from "./panels/PropertyEditor";
import { geometryCache, Viewport } from "./viewport/Viewport";

const LAST_PROJECT = "autevra.lastProject";

// Startup runs once per page load (React StrictMode runs effects twice in development).
let startup: Promise<{ parameters: ParameterDef[]; projects: ProjectSummary[] }> | null = null;
function loadStartup() {
  startup ??= (async () => {
    const [catalogue, list] = await Promise.all([api.catalogue(), api.listProjects()]);
    const projects = list.length > 0 ? list : [await api.createProject("My first vehicle")];
    return { parameters: catalogue.parameters, projects };
  })();
  startup.catch(() => (startup = null));
  return startup;
}

function remember(id: string) {
  try { localStorage.setItem(LAST_PROJECT, id); } catch { /* storage unavailable */ }
}
function recall(): string | null {
  try { return localStorage.getItem(LAST_PROJECT); } catch { return null; }
}

export function App() {
  const [parameters, setParameters] = useState<ParameterDef[]>([]);
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [project, setProject] = useState<ProjectState | null>(null);
  const [model, setModel] = useState<ModelPayload | null>(null);
  const [history, setHistory] = useState<{ entries: HistoryEntry[]; cursor: number }>({
    entries: [], cursor: 0 });
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [highlighted, setHighlighted] = useState<string[]>([]);
  const [xray, setXray] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState("Connecting…");
  const [llm, setLlm] = useState<LLMStatus | null>(null);
  const highlightTimer = useRef<number | undefined>(undefined);
  // Actions run strictly one after another, in the order the user issued them.
  const queue = useRef<Promise<void>>(Promise.resolve());
  const pending = useRef(0);

  const refresh = useCallback(async (id: string) => {
    const started = performance.now();
    const [state, hist, mdl] = await Promise.all([
      api.project(id), api.history(id), api.model(id, geometryCache.keys()),
    ]);
    setProject(state);
    setHistory(hist);
    setModel(mdl);
    setStatus(`Model updated in ${Math.round(performance.now() - started)} ms · ` +
      `${Object.keys(mdl.geometries).length} geometry download(s)`);
  }, []);

  const open = useCallback(async (id: string) => {
    remember(id);
    setTurns([]);
    setSelected(null);
    await refresh(id);
  }, [refresh]);

  useEffect(() => {
    const poll = () => { api.llmStatus().then(setLlm).catch(() => setLlm(null)); };
    poll();
    const timer = window.setInterval(poll, 30000);
    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const { parameters: defs, projects: all } = await loadStartup();
        setParameters(defs);
        setProjects(all);
        const last = recall();
        await open(all.find((p) => p.id === last)?.id ?? all[0].id);
      } catch (e) {
        setStatus(`Backend unreachable: ${(e as Error).message}. Start it with "make dev".`);
      }
    })();
  }, [open]);

  const flash = (result: CommandResult | null) => {
    if (!result) return;
    window.clearTimeout(highlightTimer.current);
    setHighlighted([...result.impact.rebuild, ...result.impact.move]);
    highlightTimer.current = window.setTimeout(() => setHighlighted([]), 1800);
  };

  const run = (action: () => Promise<CommandResult | null>) => {
    if (!project) {
      setStatus("Still loading the project; try again in a moment.");
      return;
    }
    const id = project.id;
    pending.current += 1;
    setBusy(true);
    queue.current = queue.current.then(async () => {
      setError(null);
      try {
        flash(await action());
      } catch (e) {
        const err = e as ApiError;
        setError(err.violations?.length ? err.violations.map((v) => v.message).join("; ")
          : err.message);
      }
      try {
        await refresh(id);
      } finally {
        pending.current -= 1;
        if (pending.current === 0) setBusy(false);
      }
    });
  };

  const setParameter = (parameter: string, value: number) =>
    run(() => api.command(project!.id, {
      changes: [{ parameter, operation: "set", value }], source: "ui" }));

  const undo = () => run(() => api.undo(project!.id));
  const redo = () => run(() => api.redo(project!.id));

  const send = (text: string) =>
    run(async () => {
      try {
        const reply = await api.instruct(project!.id, text);
        setTurns((t) => [...t, { text, reply }]);
        return reply.result;
      } catch (e) {
        setTurns((t) => [...t, { text, reply: { kind: "error", message: (e as Error).message } }]);
        return null;
      }
    });

  const decide = (turn: number, confirm: boolean) => {
    const reply = turns[turn]?.reply;
    if (!project || !reply || reply.kind !== "proposal" || !reply.proposal_id) return;
    const proposal = reply.proposal_id;
    const mark = (decision: ChatTurn["decision"]) =>
      setTurns((all) => all.map((t, i) => (i === turn ? { ...t, decision } : t)));
    run(async () => {
      try {
        if (!confirm) {
          await api.reject(project.id, proposal);
          mark("rejected");
          return null;
        }
        const result = await api.confirm(project.id, proposal);
        mark("confirmed");
        return result;
      } catch (e) {
        mark("failed");
        throw e;
      }
    });
  };

  const newProject = async () => {
    const name = `Vehicle ${projects.length + 1}`;
    const created = await api.createProject(name);
    setProjects(await api.listProjects());
    await open(created.id);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (target.tagName === "INPUT" || !(e.metaKey || e.ctrlKey) || e.key.toLowerCase() !== "z") return;
      e.preventDefault();
      if (e.shiftKey) { if (project?.can_redo) redo(); } else if (project?.can_undo) undo();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  return (
    <div className="app">
      <header>
        <strong className="brand">Autevra</strong>
        <select value={project?.id ?? ""} onChange={(e) => open(e.target.value)}>
          {projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <button onClick={newProject}>New</button>
        <span className="spacer" />
        <button onClick={undo} disabled={!project?.can_undo || busy} title="Undo (⌘Z)">Undo</button>
        <button onClick={redo} disabled={!project?.can_redo || busy} title="Redo (⇧⌘Z)">Redo</button>
        <label className="toggle">
          <input type="checkbox" checked={xray} onChange={(e) => setXray(e.target.checked)} />
          X-ray body
        </label>
        {project && <a className="button" href={api.stepUrl(project.id)}>Export STEP</a>}
      </header>
      <aside className="left">
        <ComponentTree parts={model?.parts ?? []} selected={selected} highlighted={highlighted}
          onSelect={setSelected} />
        <HistoryPanel entries={history.entries} cursor={history.cursor} />
      </aside>
      <main>
        <Viewport model={model} selected={selected} highlighted={highlighted} xray={xray}
          onSelect={setSelected} />
        <div className="status">{busy ? "Rebuilding…" : status}</div>
      </main>
      <aside className="right">
        <AiPanel turns={turns} busy={busy} llm={llm} onSend={send} onDecide={decide} />
        {project && (
          <PropertyEditor parameters={parameters} values={project.values} derived={project.derived}
            error={error} onSet={setParameter} />
        )}
      </aside>
    </div>
  );
}
