import type {
  Command,
  Comparison,
  ComponentTestStatus,
  Diagnosis,
  ImpactPreview,
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

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...init,
    headers: { "content-type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : response.statusText;
    throw new ApiError(detail, response.status, body.violations ?? []);
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

const post = <T>(path: string, body?: unknown) =>
  request<T>(path, { method: "POST", body: body === undefined ? undefined : JSON.stringify(body) });

export const api = {
  catalogue: () => request<{ parameters: ParameterDef[]; derived: DerivedValue[] }>("/parameters"),
  listProjects: () => request<ProjectSummary[]>("/projects"),
  createProject: (name: string, domain = "automotive") =>
    post<ProjectState>("/projects", { name, domain }),
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
  stepUrl: (id: string) => `/api/projects/${id}/export.step`,
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
  reqifUrl: (id: string) => `/api/projects/${id}/requirements.reqif`,
  preview: (id: string, command: Command) => post<ImpactPreview>(`/projects/${id}/preview`, { command }),
  spec: (id: string) => request<SpecState>(`/projects/${id}/spec`),
  specAnswer: (id: string, question: string, value: string | number | null) =>
    post<SpecState>(`/projects/${id}/spec/answers`, { question, value }),
  specText: (id: string, text: string) => post<SpecState>(`/projects/${id}/spec/text`, { text }),
  specReset: (id: string) => request<SpecState>(`/projects/${id}/spec`, { method: "DELETE" }),
  specDesign: (id: string) => post<SpecDesign>(`/projects/${id}/spec/design`),
  specApply: (id: string) => post<{ result: CommandResult; requirements: string[] }>(`/projects/${id}/spec/apply`),
  integration: (id: string) => request<IntegrationReport>(`/projects/${id}/integration`),
};
