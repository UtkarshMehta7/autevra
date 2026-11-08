import { useCallback, useEffect, useRef, useState } from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router";
import { api, ApiError, backendHint } from "../api/client";
import type {
  Command, CommandResult, Comparison, Diagnosis, ComponentTestStatus, HistoryEntry, IntegrationReport, LLMStatus,
  LoopResult, ModelPayload, RunRecord as RunRecordType, ParameterDef, ProjectState, ProjectSummary, Requirement, RequirementRow,
  RunSummary, SpecDesign, SpecState, StudyResult,
  TestDefinition, Variable,
} from "../api/types";
import type { ChatTurn } from "../panels/AiPanel";
import { CommandBar } from "../panels/CommandBar";
import { ComponentTree } from "../panels/ComponentTree";
import { HistoryPanel } from "../panels/HistoryPanel";
import { IntegrationPanel } from "../panels/IntegrationPanel";
import { PropertyEditor } from "../panels/PropertyEditor";
import { RequirementsPanel } from "../panels/RequirementsPanel";
import { SpecPanel } from "../panels/SpecPanel";
import { StudiesPanel } from "../panels/StudiesPanel";
import { TestBench } from "../panels/TestBench";
import type { Animation } from "../viewport/animation";
import { geometryCache, Viewport } from "../viewport/Viewport";
import { AiEngineeringPanel } from "./AiEngineeringPanel";
import { DigitalPanel } from "./DigitalPanel";
import { ManufacturingPanel } from "./ManufacturingPanel";
import { PackagePanel } from "./PackagePanel";
import { StylingPanel } from "./StylingPanel";
import { PartDesignPanel } from "./PartDesignPanel";
import { SystemsPanel } from "./SystemsPanel";
import { WORKSPACES, type WorkspaceId } from "./workspaces";
import { clampDock, clampSide, DEFAULT_LAYOUT, type Layout, useLayout } from "./layout";
import { Splitter } from "./Splitter";
import { ReferencePanel } from "./Reference";

import { remember } from "./lastProject";
import { DownloadLink } from "../DownloadLink";

// Startup runs once per page load (React StrictMode runs effects twice in development).
let startup: Promise<{
  parameters: ParameterDef[]; projects: ProjectSummary[]; tests: TestDefinition[];
}> | null = null;
function loadStartup() {
  startup ??= (async () => {
    const [catalogue, list, tests] = await Promise.all([
      api.catalogue(), api.listProjects(), api.tests()]);
    return { parameters: catalogue.parameters, projects: list, tests };
  })();
  startup.catch(() => (startup = null));
  return startup;
}

/** The engineering studio: one project, one shared model state, routed workspaces. */
export function Studio() {
  const { projectId = "", workspace = "design" } = useParams();
  const navigate = useNavigate();
  const known = WORKSPACES.find((w) => w.id === workspace);
  if (!known) return <Navigate to={`/studio/${projectId}/design`} replace />;
  return <StudioView projectId={projectId} workspace={known.id} navigate={navigate} />;
}

function StudioView({ projectId, workspace, navigate }: {
  projectId: string; workspace: WorkspaceId; navigate: ReturnType<typeof useNavigate>;
}) {
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
  const [tests, setTests] = useState<TestDefinition[]>([]);
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [comparisons, setComparisons] = useState<Comparison[]>([]);
  const [selectedRun, setSelectedRun] = useState<string | null>(null);
  const [testStatus, setTestStatus] = useState<ComponentTestStatus[]>([]);
  const [collapsed, setCollapsed] = useState(false);
  const [reference, setReference] = useState(() => {
    try { return localStorage.getItem("autevra.reference.open") === "1"; } catch { return false; }
  });
  const showReference = (open: boolean) => {
    setReference(open);
    try { localStorage.setItem("autevra.reference.open", open ? "1" : "0"); } catch { /* blocked */ }
  };
  // Resizable panels: side panel widths, dock height and a focus mode for the viewport.
  const { layout, set: setLayout, toggleSide } = useLayout();
  const dragStart = useRef<Layout>(layout);
  const beginDrag = () => { dragStart.current = layout; };
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (["INPUT", "TEXTAREA", "SELECT"].includes(t.tagName) || t.isContentEditable) return;
      if (e.key === "Escape" && layout.focus) setLayout({ focus: false });
      if (e.key.toLowerCase() === "f" && !e.metaKey && !e.ctrlKey && !e.altKey) {
        setLayout({ focus: !layout.focus });
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [layout.focus, setLayout]);
  const [missing, setMissing] = useState(false);
  const go = useCallback((ws: WorkspaceId) => {
    setCollapsed(false);
    navigate(`/studio/${projectId}/${ws}`);
  }, [navigate, projectId]);
  const [specState, setSpecState] = useState<SpecState | null>(null);
  const [specDesign, setSpecDesign] = useState<SpecDesign | null>(null);
  const [requirements, setRequirements] = useState<RequirementRow[]>([]);
  const [studies, setStudies] = useState<StudyResult[]>([]);
  const [loops, setLoops] = useState<LoopResult[]>([]);
  const [integration, setIntegration] = useState<IntegrationReport | null>(null);
  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [animation, setAnimation] = useState<Animation | null>(null);
  const [live, setLive] = useState(true);
  const liveRef = useRef(true);
  liveRef.current = live;
  const highlightTimer = useRef<number | undefined>(undefined);
  // Actions run strictly one after another, in the order the user issued them.
  const queue = useRef<Promise<void>>(Promise.resolve());
  const pending = useRef(0);

  const refresh = useCallback(async (id: string) => {
    const started = performance.now();
    const [state, hist, mdl, runList, status, studyList, loopList] = await Promise.all([
      api.project(id), api.history(id), api.model(id, geometryCache.keys()), api.runs(id),
      api.componentStatus(id), api.studies(id), api.loops(id),
    ]);
    api.requirements(id).then(setRequirements).catch(() => setRequirements([]));
    api.spec(id).then(setSpecState).catch(() => setSpecState(null));
    setStudies(studyList);
    setLoops(loopList);
    setProject(state);
    setHistory(hist);
    setModel(mdl);
    setRuns(runList);
    setTestStatus(status);
    setIntegration(null); // re-checked on demand: the design may have changed
    setStatus(`Model updated in ${Math.round(performance.now() - started)} ms · ` +
      `${Object.keys(mdl.geometries).length} geometry download(s)`);
  }, []);

  const open = useCallback(async (id: string) => {
    remember(id);
    setTurns([]);
    setSelected(null);
    setSelectedRun(null);
    setComparisons([]);
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
        const { parameters: defs, projects: all, tests: catalogue } = await loadStartup();
        setParameters(defs);
        setTests(catalogue);
        setProjects(all);
        setMissing(false);
        await open(projectId);
      } catch (e) {
        if ((e as ApiError).status === 404) setMissing(true);
        else setStatus(`Backend unreachable: ${(e as Error).message}. ${backendHint()}`);
      }
    })();
  }, [open, projectId]);

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
        const result = await action();
        flash(result);
        // Live simulation: tests already run on this project follow every design change.
        if (liveRef.current && result && result.changed.length > 0) {
          const out = await api.retest(id);
          if (out.runs.length) {
            setComparisons(out.comparisons);
            setStatus(`Live simulation: reran ${out.runs.length} test case(s)`);
          }
        }
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
        if (reply.studies?.length || reply.loops?.length) go("optimization");
        if (reply.kind === "requirement" || reply.kind === "verification") go("requirements");
        if (reply.kind === "spec") { setSpecDesign(null); go("design"); }
        if (reply.runs?.length) {
          setComparisons(reply.comparisons ?? []);
          setSelectedRun(reply.runs[0].id);
          setDiagnosis(reply.diagnosis ?? null);
          go("simulation");
        }
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

  const runTests = (testId: string, target: string, scenarioId: string | null) =>
    run(async () => {
      const out = await api.runTests(project!.id, { test_id: testId, target, scenario_id: scenarioId });
      setComparisons(out.comparisons);
      setSelectedRun(out.runs[0]?.id ?? null);
      return null;
    });

  const optimize = (target: string, scenarios: string[], metric: string,
    sense: "minimize" | "maximize", second: string | null, variables: Variable[], budget: number) =>
    run(async () => {
      await api.optimize(project!.id, {
        test_id: "quarter_car", target, scenarios, budget, variables,
        objectives: [{ metric, sense }, ...(second ? [{ metric: second, sense: "minimize" as const }] : [])],
      });
      return null;
    });
  const engineeringLoop = (target: string, scenarios: string[], metric: string | null) =>
    run(async () => {
      await api.loop(project!.id, { target, scenarios,
        objective: metric ? { metric, sense: "minimize" } : null });
      return null;
    });
  const decideStudy = (studyId: string, accept: boolean) =>
    run(async () => {
      if (!accept) { await api.rejectStudy(project!.id, studyId); return null; }
      return api.acceptStudy(project!.id, studyId);
    });
  const specAction = (action: () => Promise<SpecState>) =>
    run(async () => { setSpecState(await action()); setSpecDesign(null); return null; });
  const generateDesign = () =>
    run(async () => { setSpecDesign(await api.specDesign(project!.id)); return null; });
  const applyDesign = () =>
    run(async () => {
      const out = await api.specApply(project!.id);
      setSpecDesign(null);
      return out.result;
    });

  const requirementAction = (action: () => Promise<unknown>) =>
    run(async () => { await action(); return null; });

  const chooseCandidate = (studyId: string, index: number) =>
    run(async () => { await api.chooseCandidate(project!.id, studyId, index); return null; });

  // A diagnosis fix goes through the same validated command path as any edit.
  const applyFix = (command: Command) => run(() => api.command(project!.id, command));

  const checkIntegration = useCallback(() => {
    if (!project) return;
    setIntegration(null);
    api.integration(project.id).then(setIntegration).catch((e) => setError((e as Error).message));
  }, [project]);

  useEffect(() => {
    if (workspace === "assembly" && !integration && !busy) checkIntegration();
  }, [workspace, integration, busy, checkIntegration]);

  const statuses = Object.fromEntries(testStatus.map((s) => [s.component, s.status]));
  const focusTarget = selected?.match(/_(f|r)[lr]$|^(front|rear)_axle$/)
    ? (selected.includes("front") || /_f[lr]$/.test(selected) ? "front" : "rear") : null;

  const play = (run: RunRecordType) => {
    if (!project) return;
    if (run.trace.speed_kmh) {
      const tyre = project.derived.find((d) => d.id === "tyre_diameter")?.value ?? 650;
      setAnimation({ kind: "longitudinal", label: `${run.scenario.label}`, tyreRadius: tyre / 2,
        t: run.trace.t, distance: run.trace.distance_m, speed: run.trace.speed_kmh });
    } else if (run.trace.heave_mm) {
      const inputs = (run.config.solver_inputs ?? {}) as Record<string, number>;
      setAnimation({ kind: "half_car", label: `half-car, ${run.scenario.label}`,
        wheelbase: project.values.wheelbase, cgX: -(inputs.front_to_cg ?? 1.3) * 1000,
        t: run.trace.t, heave: run.trace.heave_mm, pitch: run.trace.pitch_deg,
        frontAxle: run.trace.front_axle_mm, rearAxle: run.trace.rear_axle_mm,
        road: run.trace.road_front_mm, exaggeration: 3 });
    } else {
      setAnimation({ kind: "quarter_car", label: `${run.target} quarter-car, ${run.scenario.label}`,
        axle: run.target as "front" | "rear", wheelbase: project.values.wheelbase,
        t: run.trace.t, body: run.trace.body_mm, wheel: run.trace.wheel_mm,
        road: run.trace.road_mm, exaggeration: 3 });
    }
  };

  const newProject = async () => {
    const name = `Vehicle ${projects.length + 1}`;
    const created = await api.createProject(name);
    setProjects(await api.listProjects());
    startup = null;
    navigate(`/studio/${created.id}/${workspace}`);
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

  if (missing) {
    return (
      <div className="notice-page">
        <h1>Project not found</h1>
        <p>The project <code>{projectId}</code> does not exist (it may have been deleted).</p>
        <p><Link className="button primary" to="/app/projects">Open the project list</Link></p>
      </div>
    );
  }

  return (
    <div className={`app${layout.focus ? " focus" : ""}`} style={layout.focus ? undefined : {
      gridTemplateColumns: `${layout.left}px 5px minmax(0, 1fr) 5px ${layout.right}px`,
      gridTemplateRows: `auto minmax(0, 1fr) 5px ${collapsed ? "auto" : `${layout.dock}px`}`,
    }}>
      <header>
        <Link to="/" className="brand" title="AUTEVRA website">Autevra</Link>
        <Link to="/app" className="button subtle" title="Projects, models and runs">Workspace</Link>
        <select value={project?.id ?? ""} onChange={(e) => navigate(`/studio/${e.target.value}/${workspace}`)}>
          {projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <button onClick={newProject}>New</button>
        <CommandBar turns={turns} busy={busy} llm={llm} onSend={send} onDecide={decide} />
        <button onClick={undo} disabled={!project?.can_undo || busy} title="Undo (⌘Z)">Undo</button>
        <button onClick={redo} disabled={!project?.can_redo || busy} title="Redo (⇧⌘Z)">Redo</button>
        <label className="toggle">
          <input type="checkbox" checked={xray} onChange={(e) => setXray(e.target.checked)} />
          X-ray body
        </label>
        {project && <DownloadLink className="button" href={api.stepUrl(project.id)}>Export STEP</DownloadLink>}
        <span className="layout-buttons" role="group" aria-label="Panels">
          <button className={layout.left > 0 && !layout.focus ? "on" : ""} onClick={() => toggleSide("left")}
            disabled={layout.focus} title="Show or hide the component tree">Tree</button>
          <button className={!collapsed && !layout.focus ? "on" : ""} onClick={() => setCollapsed(!collapsed)}
            disabled={layout.focus} title="Show or hide the workspace tabs panel">Tabs</button>
          <button className={layout.right > 0 && !layout.focus ? "on" : ""} onClick={() => toggleSide("right")}
            disabled={layout.focus} title="Show or hide the parameters">Parameters</button>
          <button className={reference ? "on" : ""} onClick={() => showReference(!reference)}
            title="Show a reference photo beside the 3D view (paste, drop or load)">Reference</button>
          <button className={layout.focus ? "on" : ""} onClick={() => setLayout({ focus: !layout.focus })}
            title="Give the 3D view the whole window (F; Esc to leave)">Focus view</button>
        </span>
      </header>
      <Splitter orientation="vertical" area="lsplit" label="Component tree width" onStart={beginDrag}
        onDrag={(dx) => setLayout({ left: clampSide(dragStart.current.left + dx, "left") })}
        onReset={() => setLayout({ left: DEFAULT_LAYOUT.left })} />
      <Splitter orientation="vertical" area="rsplit" label="Parameters width" onStart={beginDrag}
        onDrag={(dx) => setLayout({ right: clampSide(dragStart.current.right - dx, "right") })}
        onReset={() => setLayout({ right: DEFAULT_LAYOUT.right })} />
      <Splitter orientation="horizontal" area="hsplit" label="Workspace panel height"
        onStart={() => { beginDrag(); if (collapsed) setCollapsed(false); }}
        onDrag={(dy) => setLayout({ dock: clampDock(dragStart.current.dock - dy, window.innerHeight) })}
        onReset={() => setLayout({ dock: DEFAULT_LAYOUT.dock })} />
      <aside className="left">
        <ComponentTree parts={model?.parts ?? []} selected={selected} highlighted={highlighted}
          statuses={statuses} onSelect={setSelected} />
        <HistoryPanel entries={history.entries} cursor={history.cursor} />
      </aside>
      <main className={reference && project ? "with-ref" : undefined}>
        {reference && project && <ReferencePanel project={project.id} onClose={() => showReference(false)} />}
        <Viewport model={model} selected={selected} highlighted={highlighted} xray={xray}
          animation={animation} onStop={() => setAnimation(null)} onSelect={setSelected} />
        <div className="status">{busy ? "Working…" : status}</div>
      </main>
      <section className={`dock${collapsed ? " closed" : ""}`}>
        <nav className="tabs" aria-label="Studio workspaces">
          {WORKSPACES.map((w) => (
            <button key={w.id} className={workspace === w.id ? "active" : ""} onClick={() => go(w.id)}
              title={w.description}>
              {w.label}{w.id === "requirements" ? ` (${requirements.length})` : ""}
            </button>
          ))}
          <span className="spacer" />
          <label className="toggle" title="Rerun tests already run on this project after every change">
            <input type="checkbox" checked={live} onChange={(e) => setLive(e.target.checked)} />
            Live simulation
          </label>
          <button onClick={() => setCollapsed(!collapsed)}>{collapsed ? "Show" : "Hide"}</button>
          <button onClick={() => setLayout({ focus: true })} title="Give the 3D view the whole window (F)">Focus view</button>
        </nav>
        {project && !collapsed && workspace === "simulation" && (
          <TestBench projectId={project.id} definitions={tests} runs={runs}
            comparisons={comparisons} selected={selectedRun} busy={busy}
            focusTarget={focusTarget} onSelect={setSelectedRun} onRun={runTests}
            onApply={applyFix} onPlay={play} diagnosis={diagnosis} />
        )}
        {project && !collapsed && workspace === "optimization" && (
          <StudiesPanel definition={tests.find((t) => t.id === "quarter_car")} parameters={parameters}
            values={project.values} studies={studies} loops={loops} busy={busy}
            onOptimize={optimize} onLoop={engineeringLoop} onDecide={decideStudy}
            onChoose={chooseCandidate} />
        )}
        {project && !collapsed && workspace === "design" && (
          <SpecPanel state={specState} design={specDesign} parameters={parameters}
            values={project.values} busy={busy}
            onAnswer={(q, v) => specAction(() => api.specAnswer(project.id, q, v))}
            onText={(t) => specAction(() => api.specText(project.id, t))}
            onReset={() => specAction(() => api.specReset(project.id))}
            onDesign={generateDesign} onApply={applyDesign} />
        )}
        {project && !collapsed && workspace === "requirements" && (
          <RequirementsPanel rows={requirements} parameters={parameters} derived={project.derived}
            test={tests.find((t) => t.id === "quarter_car")} reqifUrl={api.reqifUrl(project.id)}
            busy={busy}
            onAdd={(body: Partial<Requirement>) => requirementAction(() => api.addRequirement(project.id, body))}
            onUpdate={(rid, body) => requirementAction(() => api.updateRequirement(project.id, rid, body))}
            onDelete={(rid) => requirementAction(() => api.deleteRequirement(project.id, rid))}
            onVerify={() => requirementAction(() => api.verifyRequirements(project.id))}
            onImport={(xml) => requirementAction(() => api.importReqif(project.id, xml))} />
        )}
        {project && !collapsed && workspace === "part-design" && (
          <PartDesignPanel projectId={project.id} onModelChanged={() => refresh(project.id)} />
        )}
        {project && !collapsed && workspace === "styling" && (
          <StylingPanel projectId={project.id} version={history.cursor} onModelChanged={() => refresh(project.id)} />
        )}
        {project && !collapsed && workspace === "package" && (
          <PackagePanel projectId={project.id} version={history.cursor} />
        )}
        {project && !collapsed && workspace === "assembly" && (
          <div className="split">
            <IntegrationPanel report={integration} onRefresh={checkIntegration} busy={busy} />
            <SystemsPanel projectId={project.id} version={history.cursor} compact
              onSelect={setSelected} />
          </div>
        )}
        {project && !collapsed && workspace === "ai-engineering" && (
          <AiEngineeringPanel turns={turns} llm={llm} onSend={send} />
        )}
        {project && !collapsed && workspace === "systems" && (
          <SystemsPanel projectId={project.id} version={history.cursor} onSelect={setSelected} />
        )}
        {project && !collapsed && workspace === "manufacturing" && (
          <ManufacturingPanel projectId={project.id} version={history.cursor}
            stepUrl={api.stepUrl(project.id)} reqifUrl={api.reqifUrl(project.id)} />
        )}
        {project && !collapsed && workspace === "digital-engineering" && (
          <DigitalPanel history={history} runs={runs} studies={studies} loops={loops}
            requirements={requirements} onOpenRun={(id) => { setSelectedRun(id); go("simulation"); }} />
        )}
      </section>
      <aside className="right">
        {project && (
          <PropertyEditor parameters={parameters} values={project.values} derived={project.derived}
            error={error} onSet={setParameter} />
        )}
      </aside>
    </div>
  );
}
