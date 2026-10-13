import type {
  Command,
  CommandResult,
  HistoryEntry,
  InstructionResult,
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
  undo: (id: string) => post<CommandResult>(`/projects/${id}/undo`),
  redo: (id: string) => post<CommandResult>(`/projects/${id}/redo`),
  history: (id: string) => request<{ entries: HistoryEntry[]; cursor: number }>(`/projects/${id}/history`),
  model: (id: string, known: Iterable<string>) =>
    request<ModelPayload>(`/projects/${id}/model?known=${encodeURIComponent([...known].join(","))}`),
  stepUrl: (id: string) => `/api/projects/${id}/export.step`,
};
