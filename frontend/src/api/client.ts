import type {
  Command,
  Comparison,
  ComponentTestStatus,
  Diagnosis,
  ImpactPreview,
  DesignTemplate,
  DomainDef,
  IntegrationReport,
  RuleStatus,
  RunIndexItem,
  SystemGraph,
  Requirement,
  RequirementRow,
  LoopResult,
  Study,
  StudyResult,
  Variable,
  RunRecord,
  SpecDesign,
  SpecState,
  RunSummary,
  TestDefinition,
  TestRunResponse,
  CommandResult,
  HistoryEntry,
  InstructionResult,
  LLMStatus,
  ModelPayload,
  ParameterDef,
  PartDoc,
  PartOut,
  DerivedValue,
  ProjectState,
  ProjectSummary,
  Violation,
} from "./types";

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly violations: Violation[] = [],
  ) {
    super(message);
  }
}

// Same origin by default (Vite proxy, nginx, Netlify rewrite). A separately hosted
// backend is set at build time: VITE_API_URL=https://api.example.com
const API = `${(import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "")}/api`;

// A free hosted backend (Hugging Face Spaces) sleeps when unused and takes a minute or
// two to start. While it does, requests fail at the network level or with 502-504.
// Reads are retried for up to WAKE_LIMIT_MS and listeners are told the backend is waking;
// writes are never retried, so nothing is applied twice.
const WAKE_STATUSES = new Set([502, 503, 504]);
const WAKE_LIMIT_MS = 180_000;
const wakeListeners = new Set<(waking: boolean) => void>();
let waking = false;

function setWaking(value: boolean) {
  if (waking === value) return;
  waking = value;
  wakeListeners.forEach((listener) => listener(value));
}

export function onBackendWaking(listener: (waking: boolean) => void): () => void {
  wakeListeners.add(listener);
  listener(waking);
  return () => wakeListeners.delete(listener);
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function send(url: string, init: RequestInit): Promise<Response> {
  const idempotent = (init.method ?? "GET").toUpperCase() === "GET";
  const started = Date.now();
  for (let attempt = 0; ; attempt++) {
    let response: Response | undefined;
    try {
      response = await fetch(url, init);
    } catch (error) {
      if (!idempotent || Date.now() - started > WAKE_LIMIT_MS) {
        setWaking(false);
        throw error;
      }
    }
    if (response && (!idempotent || !WAKE_STATUSES.has(response.status)
        || Date.now() - started > WAKE_LIMIT_MS)) {
      setWaking(false);
      return response;
    }
    setWaking(true);
    await sleep(Math.min(2000 * (attempt + 1), 8000));
  }
}

// A public instance keeps each visitor's projects apart by a random key generated in this
// browser and sent with every request. Locally the backend ignores it.
const WORKSPACE_KEY = "autevra.workspace";
let memoryKey = "";

function newKey(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

export function workspaceKey(): string {
  try {
    const stored = localStorage.getItem(WORKSPACE_KEY);
    if (stored) return stored;
    const key = newKey();
    localStorage.setItem(WORKSPACE_KEY, key);
    return key;
  } catch {
    // Storage blocked (private mode, sandbox): keep a key for this page's lifetime.
    memoryKey ||= newKey();
    return memoryKey;
  }
}

const workspaceHeader = () => ({ "X-Autevra-Workspace": workspaceKey() });

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await send(`${API}${path}`, {
    ...init,
    headers: { "content-type": "application/json", ...workspaceHeader(), ...init?.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : response.statusText;
    throw new ApiError(detail, response.status, body.violations ?? []);
  }
  if (response.status === 204) return undefined as T;
  // A static host answers unknown paths with index.html; say so instead of a JSON parse error.
  if (!(response.headers.get("content-type") ?? "").includes("json")) {
    throw new ApiError(`${API} returned a web page instead of data, so the API address is wrong`,
      response.status);
  }
  return response.json();
}

/** Download an API file (STEP, ReqIF) with the workspace header, which a plain link cannot send. */
export async function download(url: string): Promise<void> {
  const response = await send(url, { headers: workspaceHeader() });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiError(typeof body.detail === "string" ? body.detail : response.statusText,
      response.status);
  }
  const disposition = response.headers.get("content-disposition") ?? "";
  const name = /filename="?([^";]+)"?/.exec(disposition)?.[1] ?? url.split("/").pop() ?? "download";
  const href = URL.createObjectURL(await response.blob());
  const link = Object.assign(document.createElement("a"), { href, download: name });
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(href), 1000);
}

/** What to try when the backend cannot be reached, depending on where the app runs. */
export function backendHint(): string {
  const local = ["localhost", "127.0.0.1", "[::1]"].includes(globalThis.location?.hostname ?? "");
  return local
    ? 'Start it with "make dev".'
    : "The hosted backend may be starting after a pause; reload in a minute.";
}

const post = <T>(path: string, body?: unknown) =>
  request<T>(path, { method: "POST", body: body === undefined ? undefined : JSON.stringify(body) });

export const api = {
  catalogue: () => request<{ parameters: ParameterDef[]; derived: DerivedValue[] }>("/parameters"),
  listProjects: () => request<ProjectSummary[]>("/projects"),
  createProject: (name: string, domain = "automotive", template?: string) =>
    post<ProjectState>("/projects", { name, domain, template }),
  templates: () => request<DesignTemplate[]>("/templates"),
  renameProject: (id: string, name: string) =>
    request<ProjectState>(`/projects/${id}`, { method: "PATCH", body: JSON.stringify({ name }) }),
  deleteProject: (id: string) => request<void>(`/projects/${id}`, { method: "DELETE" }),
  duplicateProject: (id: string) => post<ProjectState>(`/projects/${id}/duplicate`),
  domains: () => request<DomainDef[]>("/domains"),
  allRuns: () => request<RunIndexItem[]>("/runs"),
  system: (id: string) => request<SystemGraph>(`/projects/${id}/system`),
  rules: (id: string) => request<RuleStatus[]>(`/projects/${id}/rules`),
  plugins: () => request<{ name: string; version: string; description: string; parameters: string[];
    components: string[]; rules: string[]; tests: string[] }[]>("/plugins"),
  contact: (body: { name: string; email: string; topic: string; message: string }) =>
    post<{ id: string; stored: boolean; delivered: boolean; note: string }>("/contact", body),
  project: (id: string) => request<ProjectState>(`/projects/${id}`),
  command: (id: string, command: Command) => post<CommandResult>(`/projects/${id}/commands`, { command }),
  instruct: (id: string, text: string) => post<InstructionResult>(`/projects/${id}/instructions`, { text }),
  confirm: (id: string, proposal: string) =>
    post<CommandResult>(`/projects/${id}/proposals/${proposal}/confirm`),
  reject: (id: string, proposal: string) =>
    post<void>(`/projects/${id}/proposals/${proposal}/reject`),
  llmStatus: () => request<LLMStatus>("/llm"),
  undo: (id: string) => post<CommandResult>(`/projects/${id}/undo`),
  redo: (id: string) => post<CommandResult>(`/projects/${id}/redo`),
  history: (id: string) => request<{ entries: HistoryEntry[]; cursor: number }>(`/projects/${id}/history`),
  model: (id: string, known: Iterable<string>) =>
    request<ModelPayload>(`/projects/${id}/model?known=${encodeURIComponent([...known].join(","))}`),
  stepUrl: (id: string) => `${API}/projects/${id}/export.step`,
  tests: () => request<TestDefinition[]>("/tests"),
  runTests: (id: string, body: { test_id: string; target: string; scenario_id?: string | null }) =>
    post<TestRunResponse>(`/projects/${id}/tests/run`, body),
  retest: (id: string) => post<TestRunResponse>(`/projects/${id}/tests/retest`),
  runs: (id: string) => request<RunSummary[]>(`/projects/${id}/runs`),
  run: (id: string, run: string) => request<RunRecord>(`/projects/${id}/runs/${run}`),
  compare: (id: string, baseline: string, candidate: string) =>
    request<Comparison>(`/projects/${id}/runs/compare?baseline=${baseline}&candidate=${candidate}`),
  diagnosis: (id: string, run: string) => request<Diagnosis>(`/projects/${id}/runs/${run}/diagnosis`),
  componentStatus: (id: string) => request<ComponentTestStatus[]>(`/projects/${id}/components/status`),
  optimize: (id: string, study: Study) => post<StudyResult>(`/projects/${id}/optimize`, study),
  loop: (id: string, goal: { target: string; scenarios: string[] | null;
    objective: { metric: string; sense: string } | null }) => post<LoopResult>(`/projects/${id}/loop`, goal),
  studies: (id: string) => request<StudyResult[]>(`/projects/${id}/studies`),
  loops: (id: string) => request<LoopResult[]>(`/projects/${id}/loops`),
  acceptStudy: (id: string, study: string) => post<CommandResult>(`/projects/${id}/studies/${study}/accept`),
  rejectStudy: (id: string, study: string) => post<void>(`/projects/${id}/studies/${study}/reject`),
  chooseCandidate: (id: string, study: string, index: number) =>
    post<StudyResult>(`/projects/${id}/studies/${study}/choose/${index}`),
  optimizeDefaults: (target: string) =>
    request<{ variables: Variable[] }>(`/optimize/defaults?target=${target}`),
  requirements: (id: string) => request<RequirementRow[]>(`/projects/${id}/requirements`),
  addRequirement: (id: string, body: Partial<Requirement>) =>
    post<RequirementRow>(`/projects/${id}/requirements`, body),
  updateRequirement: (id: string, req: string, body: Partial<Requirement>) =>
    request<RequirementRow>(`/projects/${id}/requirements/${req}`, { method: "PATCH", body: JSON.stringify(body) }),
  deleteRequirement: (id: string, req: string) =>
    request<void>(`/projects/${id}/requirements/${req}`, { method: "DELETE" }),
  verifyRequirements: (id: string) => post<RequirementRow[]>(`/projects/${id}/requirements/verify`),
  importReqif: (id: string, xml: string) =>
    request<RequirementRow[]>(`/projects/${id}/requirements.reqif`, {
      method: "POST", body: xml, headers: { "content-type": "application/xml" } }),
  reqifUrl: (id: string) => `${API}/projects/${id}/requirements.reqif`,
  preview: (id: string, command: Command) => post<ImpactPreview>(`/projects/${id}/preview`, { command }),
  spec: (id: string) => request<SpecState>(`/projects/${id}/spec`),
  specAnswer: (id: string, question: string, value: string | number | null) =>
    post<SpecState>(`/projects/${id}/spec/answers`, { question, value }),
  specText: (id: string, text: string) => post<SpecState>(`/projects/${id}/spec/text`, { text }),
  specReset: (id: string) => request<SpecState>(`/projects/${id}/spec`, { method: "DELETE" }),
  specDesign: (id: string) => post<SpecDesign>(`/projects/${id}/spec/design`),
  specApply: (id: string) => post<{ result: CommandResult; requirements: string[] }>(`/projects/${id}/spec/apply`),
  partPresets: () => request<Record<string, PartDoc>>("/part-presets"),
  parts: (id: string) => request<PartOut[]>(`/projects/${id}/parts`),
  createPart: (id: string, doc: PartDoc) => post<PartOut>(`/projects/${id}/parts`, doc),
  updatePart: (id: string, part: string, doc: PartDoc) =>
    request<PartOut>(`/projects/${id}/parts/${part}`, { method: "PUT", body: JSON.stringify(doc) }),
  undoPart: (id: string, part: string) => post<PartOut>(`/projects/${id}/parts/${part}/undo`),
  redoPart: (id: string, part: string) => post<PartOut>(`/projects/${id}/parts/${part}/redo`),
  deletePart: (id: string, part: string) =>
    request<void>(`/projects/${id}/parts/${part}`, { method: "DELETE" }),
  integration: (id: string) => request<IntegrationReport>(`/projects/${id}/integration`),
};
