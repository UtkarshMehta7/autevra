// Mirrors backend/autevra/api/schemas.py.

export type Operation = "set" | "increase" | "decrease" | "scale";
export type Unit = "mm" | "cm" | "m" | "in" | "deg" | "%";

export interface ParameterDef {
  id: string;
  label: string;
  group: "dimensions" | "cabin" | "wheels" | "steering" | "frame";
  unit: Unit;
  default: number;
  min: number;
  max: number;
  step: number;
  description: string;
}

export interface DerivedValue {
  id: string;
  label: string;
  unit: string;
  value: number;
  controlled_by: string[];
}

export interface ProjectSummary {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectState extends ProjectSummary {
  values: Record<string, number>;
  derived: DerivedValue[];
  can_undo: boolean;
  can_redo: boolean;
  history_length: number;
  cursor: number;
}

export interface Change {
  parameter: string;
  operation: Operation;
  value: number;
  unit?: Unit | null;
}

export interface Command {
  type?: "set_parameters";
  changes: Change[];
  source?: "ui" | "api" | "rules" | "llm";
  instruction?: string | null;
}

export interface HistoryEntry {
  id: string;
  command: Command;
  changes: { parameter: string; old: number; new: number }[];
  created_at: string;
}

export interface Impact {
  rebuild: string[];
  move: string[];
}

export interface CommandResult {
  changed: string[];
  values: Record<string, number>;
  impact: Impact;
  entry: HistoryEntry | null;
  can_undo: boolean;
  can_redo: boolean;
}

export interface Violation {
  rule: string;
  message: string;
  parameters: string[];
}

export interface InstructionResult {
  kind: "command" | "undo" | "redo" | "query" | "clarification" | "rejected" | "proposal"
    | "out_of_scope";
  message: string;
  interpreted_by: "rules" | "llm";
  command: Command | null;
  proposal_id: string | null;
  preview: Record<string, number>;
  result: CommandResult | null;
  suggestions: string[];
  assumptions: string[];
  violations: Violation[];
  answer: Record<string, number>;
}

export interface GeometryData {
  vertices: number[];
  indices: number[];
}

export interface ModelPart {
  id: string;
  name: string;
  category: string;
  geometry: string;
  matrix: number[][];
  color: [number, number, number];
}

export interface ModelPayload {
  units: "mm";
  geometries: Record<string, GeometryData>;
  parts: ModelPart[];
}

export interface LLMStatus {
  provider: string;
  model: string;
  url: string;
  available: boolean;
  detail: string;
  models: string[];
}
