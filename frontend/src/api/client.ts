import type {
  Command,
  Comparison,
  ComponentTestStatus,
  IntegrationReport,
  RunRecord,
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
  createProject: (name: string) => post<ProjectState>("/projects", { name }),
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
  runs: (id: string) => request<RunSummary[]>(`/projects/${id}/runs`),
  run: (id: string, run: string) => request<RunRecord>(`/projects/${id}/runs/${run}`),
  compare: (id: string, baseline: string, candidate: string) =>
    request<Comparison>(`/projects/${id}/runs/compare?baseline=${baseline}&candidate=${candidate}`),
  componentStatus: (id: string) => request<ComponentTestStatus[]>(`/projects/${id}/components/status`),
  integration: (id: string) => request<IntegrationReport>(`/projects/${id}/integration`),
};
