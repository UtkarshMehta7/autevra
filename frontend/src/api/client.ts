import type {
  BomLine, Command, CommandResult, Comparison, ComponentTestStatus, DerivedValue, DesignTemplate, Diagnosis, DomainDef, FeatureTemplate, HistoryEntry, ImpactPreview, InstructionResult, IntegrationReport, LLMStatus, LoopResult, ModelPayload, PackageValue, ParameterDef, PartDoc, PartOut, ProjectState, ProjectSummary, Requirement, RequirementRow, RuleStatus, RunIndexItem, RunRecord, RunSummary, Sketch, SketchSolve, SpecDesign, SpecState, Study, StudyResult, Styling, SystemGraph, TestDefinition, TestRunResponse, Variable, Violation, NurbsSurface, NurbsEvaluation, ContinuityReport, FeaRequest, FeaResult, FeaCatalogue, FeaMesh, TopologyRequest, TopologyResult, AircraftSpec, AircraftAnalysis, ProductEnvelope, ProductOut, SystemsOut, ChainStep, ItemSummary, InventoryItem, ItemPort, EngineSpec, EngineAnalysis } from "./types";

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

/** A machining plan: setup, operations with toolpaths (part frame, mm) and the G-code. */
export interface CamOp {
  name: string; tool: number; tool_label: string; rpm: number; feed: number; ap: number; ae: number;
  cut_mm: number; rapid_mm: number; time_s: number; power_kw: number; cycle: string | null; notes: string[];
  paths: [number, number, number][][];
}
export interface CamOut {
  stock: number[]; part_box: number[]; safe_z: number; material: string;
  tools: { number: number; label: string; kind: string; diameter: number }[];
  operations: CamOp[]; warnings: string[]; notes: string[]; levels: number[]; time_s: number;
  stock_volume: number; removed_volume: number; rest_area: number; mass_kg: number; stock_mass_kg: number;
  gcode: string; gcode_lines: number;
}

/** A machine-element calculation: numbers, nested results and warnings. */
export type ElementOut = { warnings: string[]; [key: string]: unknown };

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
  glbUrl: (id: string) => `${API}/projects/${id}/export.glb`,
  stlUrl: (id: string) => `${API}/projects/${id}/export.stl`,
  assemblyDrawingUrl: (id: string) => `${API}/projects/${id}/drawing.svg`,
  igesUrl: (id: string) => `${API}/projects/${id}/export.igs`,
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
  styling: (id: string) => request<Styling>(`/projects/${id}/styling`),
  setStyling: (id: string, doc: Record<string, [number, number][]>) =>
    request<Styling>(`/projects/${id}/styling`, { method: "PUT", body: JSON.stringify(doc) }),
  undoStyling: (id: string) => post<Styling>(`/projects/${id}/styling/undo`),
  redoStyling: (id: string) => post<Styling>(`/projects/${id}/styling/redo`),
  package: (id: string) => request<PackageValue[]>(`/projects/${id}/package`),
  packageSvgUrl: (id: string) => `${API}/projects/${id}/package.svg`,
  packageSvg: async (id: string): Promise<string> => {
    const response = await send(`${API}/projects/${id}/package.svg`, { headers: workspaceHeader() });
    if (!response.ok) throw new ApiError(response.statusText, response.status);
    return response.text();
  },
  bom: (id: string) => request<BomLine[]>(`/projects/${id}/bom`),
  bomUrl: (id: string) => `${API}/projects/${id}/bom.csv`,
  featureTemplates: () => request<FeatureTemplate[]>("/feature-templates"),
  saveFeatureTemplate: (body: { project_id: string; part_id: string; name: string; feature_ids: string[]; description?: string }) =>
    post<FeatureTemplate>("/feature-templates", body),
  deleteFeatureTemplate: (id: string) => request<void>(`/feature-templates/${id}`, { method: "DELETE" }),
  insertFeatureTemplate: (id: string, part: string, body: { template: string; prefix: string;
    inputs: Record<string, number | string>; offset: [number, number, number] }) =>
    post<PartOut>(`/projects/${id}/parts/${part}/insert-template`, body),
  solveSketch: (sketch: Sketch, drag?: { point: string; x: number; y: number }) =>
    post<SketchSolve>("/sketch/solve", { sketch, drag: drag ?? null }),
  partPresets: () => request<Record<string, PartDoc>>("/part-presets"),
  // Surface laboratory (NURBS mathematics, continuity)
  evaluateSurface: (surface: NurbsSurface, samples = 33, selected: [number, number] | null = null) =>
    post<NurbsEvaluation>("/surfaces/evaluate", { surface, samples, selected }),
  insertKnot: (surface: NurbsSurface, direction: "u" | "v", t: number) =>
    post<{ surface: Required<NurbsSurface>; max_shape_change: number }>("/surfaces/insert-knot", { surface, direction, t }),
  joinSurface: (surface: NurbsSurface, target: "G0" | "G1" | "G2", bend: number) =>
    post<{ surface: Required<NurbsSurface> }>("/surfaces/join", { surface, target, bend }),
  aircraftSpec: () => request<{ defaults: AircraftSpec }>("/aero/spec"),
  analyseAircraft: (spec: AircraftSpec) => post<AircraftAnalysis>("/aero/analyse", spec),
  aircraftPresets: () => request<Record<string, AircraftSpec>>("/aero/presets"),
  getAircraftSpec: (id: string) => request<AircraftSpec>(`/projects/${id}/aircraft/spec`),
  analyseEngine: (spec: EngineSpec) => post<EngineAnalysis>("/engines/analyse", spec),
  getEngineSpec: (id: string) => request<EngineSpec>(`/projects/${id}/engine/spec`),
  analyseVessel: (spec: unknown) => post<unknown>("/marine/analyse", spec),
  engineCategory: (id: string) => request<{ category: string }>(`/projects/${id}/engine/category`),
  setEngineCategory: (id: string, category: string) =>
    request<{ category: string }>(`/projects/${id}/engine/category`, { method: "PUT", body: JSON.stringify({ category }) }),
  analyseMotor: (spec: unknown) => post<unknown>("/motors/analyse", spec),
  analyseTurbine: (spec: unknown) => post<unknown>("/turbines/analyse", spec),
  getMotorSpec: (id: string) => request<unknown>(`/projects/${id}/motor/spec`),
  saveMotorSpec: (id: string, spec: unknown) => request<unknown>(`/projects/${id}/motor/spec`, { method: "PUT", body: JSON.stringify(spec) }),
  getTurbineSpec: (id: string) => request<unknown>(`/projects/${id}/turbine/spec`),
  saveTurbineSpec: (id: string, spec: unknown) => request<unknown>(`/projects/${id}/turbine/spec`, { method: "PUT", body: JSON.stringify(spec) }),
  buildMachine: (id: string) => post<unknown>(`/projects/${id}/machine`, {}),
  publishMotor: (id: string) => post<unknown>(`/projects/${id}/motor/publish`, {}),
  getVesselSpec: (id: string) => request<unknown>(`/projects/${id}/vessel/spec`),
  saveVesselSpec: (id: string, spec: unknown) =>
    request<unknown>(`/projects/${id}/vessel/spec`, { method: "PUT", body: JSON.stringify(spec) }),
  buildVessel: (id: string, spec: unknown) => post<unknown>(`/projects/${id}/vessel`, spec),
  saveEngineSpec: (id: string, spec: EngineSpec) =>
    request<EngineSpec>(`/projects/${id}/engine/spec`, { method: "PUT", body: JSON.stringify(spec) }),
  buildEngine: (id: string, spec: EngineSpec) => post<PartOut[]>(`/projects/${id}/engine`, spec),
  publishEngine: (id: string) => post<InventoryItem>(`/projects/${id}/engine/publish`, {}),
  product: (id: string, config?: Record<string, string>) =>
    request<ProductOut>(`/projects/${id}/product${config && Object.keys(config).length
      ? `?config=${encodeURIComponent(JSON.stringify(config))}` : ""}`),
  productEnvelope: (id: string) => request<ProductEnvelope>(`/projects/${id}/product/envelope`),
  systems: (id: string) => request<SystemsOut>(`/projects/${id}/systems`),
  projectLoads: (id: string) => request<unknown>(`/projects/${id}/loads`),
  faultTree: (id: string, fn: string, exposure = 1) =>
    request<unknown>(`/projects/${id}/systems/fault-tree/${encodeURIComponent(fn)}?exposure=${exposure}`),
  materials: () => request<unknown[]>("/materials"),
  laminate: (angles: number[], thickness: number) =>
    post<{ thickness_mm: number; symmetric: boolean; ex_gpa: number; ey_gpa: number; gxy_gpa: number; nuxy: number }>(
      "/composites/laminate", { plies: angles.map((angle) => ({ angle, thickness_mm: thickness })) }),
  manufacturing: (id: string, takt?: number) => request<unknown>(`/projects/${id}/manufacturing${takt ? `?takt=${takt}` : ""}`),
  partDraft: (id: string, part: string, pull: string, min: number) => request<DraftReport>(`/projects/${id}/parts/${part}/draft?pull=${encodeURIComponent(pull)}&min_draft=${min}`),
  partParting: (id: string, part: string, pull: string, pressure: number) => request<PartingReport>(`/projects/${id}/parts/${part}/parting?pull=${encodeURIComponent(pull)}&pressure=${pressure}`),
  pfmea: (id: string) => request<PfmeaOut>(`/projects/${id}/pfmea`),
  stackup: (stack: unknown) => post<unknown>("/quality/stackup", stack),
  lca: (id: string, grid: number) => request<unknown>(`/projects/${id}/lca?grid=${grid}`),
  reviews: (id: string) => request<unknown[]>(`/projects/${id}/reviews`),
  clearance: (id: string, required: number) => request<unknown[]>(`/projects/${id}/clearance?required=${required}`),
  fourbar: (body: unknown) => post<FourBarOut>("/mechanisms/fourbar", body),
  element: (kind: "bolt" | "weld" | "fatigue" | "fatigue/history" | "spring" | "gears" | "transmission", body: unknown) =>
    post<ElementOut>(`/elements/${kind}`, body),
  transmissionInputs: (id: string) => request<Record<string, unknown>>(`/projects/${id}/elements/transmission-inputs`),
  addGears: (id: string, body: unknown) => post<PartOut[]>(`/projects/${id}/elements/gears`, body),
  cam: (id: string, part: string, body: unknown) => post<CamOut>(`/projects/${id}/parts/${part}/cam`, body),
  sliderCrank: (body: unknown) => post<SliderCrankOut>("/mechanisms/slider-crank", body),
  sweep: (id: string, part: string, joint: unknown, required: number) =>
    post<SweepReport>(`/projects/${id}/parts/${part}/sweep`, { joint, required, volume: false }),
  addEnvelope: (id: string, part: string, joint: unknown) => post<PartOut>(`/projects/${id}/parts/${part}/envelope`, joint),
  baselines: (id: string) => request<unknown[]>(`/projects/${id}/baselines`),
  takeBaseline: (id: string, name: string, gate: string) => post<unknown>(`/projects/${id}/baselines`, { name, gate }),
  compareBaseline: (id: string, bl: string) => request<unknown>(`/projects/${id}/baselines/${bl}/compare`),
  changes: (id: string) => request<unknown[]>(`/projects/${id}/changes`),
  requestChange: (id: string, title: string, changes: Record<string, unknown>) =>
    post<unknown>(`/projects/${id}/changes`, { title, changes }),
  decideChange: (id: string, change: string, decision: "approve" | "reject") =>
    post<unknown>(`/projects/${id}/changes/${change}/${decision}`, {}),
  inventory: (q: string, category: string) =>
    request<ItemSummary[]>(`/inventory?q=${encodeURIComponent(q)}&category=${encodeURIComponent(category)}`),
  inventoryItem: (itemId: string) => request<InventoryItem>(`/inventory/items/${encodeURIComponent(itemId)}`),
  itemUsage: (itemId: string) => request<{ item: string; version: string; project: string; part: string }[]>(`/inventory/items/${encodeURIComponent(itemId)}/usage`),
  bearingLife: (itemId: string, load_kN: number, rpm: number) =>
    post<{ L10_Mrev: number; L10_hours: number; exponent: number }>(`/inventory/items/${encodeURIComponent(itemId)}/bearing-life`, { load_kN, rpm }),
  installItem: (id: string, item: string, at: { x: number; y: number; z: number },
    mate?: { part: string; port: string; own_port: string }) =>
    post<PartOut>(`/projects/${id}/inventory/install`, { item, at, mate }),
  installedItems: (id: string) =>
    request<{ part: string; name: string; item: string; version: string; ports: ItemPort[] }[]>(`/projects/${id}/inventory/installed`),
  publishPart: (id: string, partId: string) => post<InventoryItem>(`/projects/${id}/parts/${partId}/publish`, {}),
  importStep: (id: string, file: File) =>
    request<PartOut>(`/projects/${id}/import-step?name=${encodeURIComponent(file.name.replace(/\.(step|stp)$/i, "").slice(0, 80) || "Imported part")}`,
      { method: "POST", body: file, headers: { "content-type": "application/octet-stream" } }),
  routeHarness: (body: unknown) => post<unknown>("/routing/harness", body),
  routePipe: (body: unknown) => post<unknown>("/routing/pipe", body),
  addRoute: (id: string, body: unknown) => post<PartOut>(`/projects/${id}/routes`, body),
  addPort: (itemId: string, port: unknown) => post<InventoryItem>(`/inventory/items/${encodeURIComponent(itemId)}/ports`, port),
  installEngine: (id: string, item: string) =>
    post<{ item: string; version: string; name: string; checks: { id: string; label: string; status: string; message: string }[] }>(`/projects/${id}/install-engine`, { item }),
  installedEngine: (id: string) =>
    request<{ item: string; name: string; version: string; latest: string; upgrade_available: boolean; impact: Record<string, number> } | null>(`/projects/${id}/installed-engine`),
  upgradeEngine: (id: string) => post<{ version: string }>(`/projects/${id}/installed-engine/upgrade`, {}),
  enginePerformance: (id: string) => request<{
    engine: string; gears: number[]; top_speed_kmh: number; zero_to_100_s: number | null;
    zero_to_200_s: number | null; cvt_zero_to_100_s: number | null; assumptions: string[];
    trace: { t: number[]; v: number[]; gear: number[]; rpm: number[] } }>(`/projects/${id}/installed-engine/performance`),
  systemChain: (id: string, fn: string) => request<ChainStep[]>(`/projects/${id}/systems/chain/${encodeURIComponent(fn)}`),
  allocate: (id: string, requirement: string, fn: string) =>
    request<Record<string, string>>(`/projects/${id}/systems/allocations`, { method: "PUT", body: JSON.stringify({ requirement, function: fn }) }),
  saveAircraftSpec: (id: string, spec: AircraftSpec) =>
    request<AircraftSpec>(`/projects/${id}/aircraft/spec`, { method: "PUT", body: JSON.stringify(spec) }),
  buildAircraft: (id: string, spec: AircraftSpec) => post<PartOut>(`/projects/${id}/aircraft`, spec),
  topology: (body: TopologyRequest) => post<TopologyResult>("/structures/topology", body),
  topologyCases: () => request<{ cases: Record<string, string> }>("/structures/topology/catalogue"),
  feaCatalogue: () => request<FeaCatalogue>("/structures/catalogue"),
  feaMesh: (body: FeaRequest, part?: { project: string; part: string }) =>
    post<{ mesh: FeaMesh }>(part ? `/projects/${part.project}/parts/${part.part}/structures/mesh` : "/structures/mesh", body),
  runFea: (body: FeaRequest, part?: { project: string; part: string }) =>
    post<FeaResult>(part ? `/projects/${part.project}/parts/${part.part}/structures` : "/structures/run", body),
  surfaceContinuity: (a: NurbsSurface, b: NurbsSurface, combScale: number) =>
    post<ContinuityReport>("/surfaces/continuity", { a, b, comb_scale: combScale }),
  parts: (id: string) => request<PartOut[]>(`/projects/${id}/parts`),
  createPart: (id: string, doc: PartDoc) => post<PartOut>(`/projects/${id}/parts`, doc),
  updatePart: (id: string, part: string, doc: PartDoc) =>
    request<PartOut>(`/projects/${id}/parts/${part}`, { method: "PUT", body: JSON.stringify(doc) }),
  reorderPart: (id: string, part: string, order: string[]) =>
    post<PartOut>(`/projects/${id}/parts/${part}/reorder`, { order }),
  undoPart: (id: string, part: string) => post<PartOut>(`/projects/${id}/parts/${part}/undo`),
  redoPart: (id: string, part: string) => post<PartOut>(`/projects/${id}/parts/${part}/redo`),
  partDrawingUrl: (id: string, part: string) => `${API}/projects/${id}/parts/${part}/drawing.svg`,
  partTableUrl: (id: string, part: string) => `${API}/projects/${id}/parts/${part}/design-table.csv`,
  setPartTable: (id: string, part: string, csv: string) =>
    request<PartOut>(`/projects/${id}/parts/${part}/design-table`,
      { method: "PUT", body: csv, headers: { "content-type": "text/csv" } }),
  deletePart: (id: string, part: string) =>
    request<void>(`/projects/${id}/parts/${part}`, { method: "DELETE" }),
  integration: (id: string) => request<IntegrationReport>(`/projects/${id}/integration`),
};

export interface FourBarPose { theta_deg: number; b: [number, number]; c: [number, number]; p: [number, number]; transmission_deg: number; rocker_deg: number }
export interface FourBarOut { class: string; full_rotation: boolean; assembled_fraction: number; poses: FourBarPose[]; transmission_min_deg?: number; transmission_max_deg?: number; rocker_swing_deg?: number; warnings: string[] }
export interface SliderCrankOut { stroke_mm: number; x_max_mm: number; x_min_mm: number; rod_ratio: number; v_max_m_s: number; a_max_m_s2: number; rows: { theta_deg: number; x_mm: number; v_m_s: number; a_m_s2: number }[] }
export interface SweepReport { part: string; unit: string; positions: number[]; box_min: number[]; box_max: number[]; pairs: { other: string; other_name: string; status: string; distance_mm: number; at: number; exact: boolean }[] }
export interface PfmeaRow { part: string; name: string; station: string; step: string; mode: string; effect: string; cause: string; prevention: string; detection_control: string; severity: number; severity_from: string; occurrence: number; detection: number; rpn: number; priority: string }
export interface PfmeaOut { summary: { rows: number; by_priority: Record<string, number>; linked_to_design: number; stations: Record<string, { high: number; medium: number; low: number; max_rpn: number }> }; rows: PfmeaRow[] }
export interface DraftReport { min_draft_deg: number; area_mm2: { perpendicular: number; drafted: number; insufficient: number }; ok: boolean; faces: { index: number; status: string; min_draft_deg: number; side: string; area_mm2: number }[] }
export interface PartingReport { cavity_faces: number; core_faces: number; wall_faces: number; parting_edges: number; parting_length_mm: number; parting_height_mm: [number, number]; flat: boolean; projected_area_mm2: number; clamp_kn: number; undercuts: { index: number; side: string; area_mm2: number }[]; verdict: string }
