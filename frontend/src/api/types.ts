// Mirrors backend/autevra/api/schemas.py.

export type Operation = "set" | "increase" | "decrease" | "scale";
export type Unit =
  | "mm" | "cm" | "m" | "in" | "deg" | "%"
  | "kg" | "lb" | "N/mm" | "N/m" | "kN/m" | "lbf/in" | "N·s/m" | "N·s/mm" | "kN·s/m"
  | "kW" | "hp" | "PS" | "";

export interface ParameterDef {
  id: string;
  label: string;
  group: string; // built-in groups plus any added by plugins
  unit: Unit;
  default: number;
  min: number;
  max: number;
  step: number;
  description: string;
  options?: string[]; // a choice: the value is the index of one of these labels
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
  domain?: string;
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
  /** "test_id:target" pairs whose results the change makes stale. */
  retest?: string[];
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
    | "out_of_scope" | "test" | "diagnosis" | "optimization" | "loop" | "preview" | "requirement"
    | "verification" | "spec";
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
  runs?: RunSummary[];
  comparisons?: Comparison[];
  diagnosis?: Diagnosis | null;
  studies?: StudyResult[];
  loops?: LoopResult[];
  impact_preview?: ImpactPreview | null;
  requirements?: RequirementRow[];
  spec?: SpecState | null;
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
  finish?: string; // paint | glass | lamp | rubber | metal
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

// --- Engineering: component tests, runs and integration (backend/autevra/engineering) ---

export type RunStatus = "passed_within_model" | "failed" | "no_criteria" | "invalid";
export type ComponentStatus = RunStatus | "not_tested" | "stale" | "experimentally_validated";
export type Credibility = "analytical_estimate" | "numerical_simulation" | "experimentally_validated";

export interface Scenario {
  id: string;
  label: string;
  road: string;
  height_mm: number;
  length_m: number;
  speed_kmh: number;
  duration_s: number;
  note: string;
}

export interface MetricInfo { label: string; unit: string; lower_is_better: boolean }

export interface TestDefinition {
  id: string;
  name: string;
  description: string;
  solver: string;
  credibility: Credibility;
  targets: string[];
  components: Record<string, string[]>;
  inputs: Record<string, string[]>;
  scenarios: Scenario[];
  criteria: { id: string; label: string; metric: string; comparator: string; unit: string;
    limit: number | null; limit_from: string | null; source: string }[];
  metrics: Record<string, MetricInfo>;
  assumptions: string[];
}

export interface CriterionResult {
  id: string;
  label: string;
  metric: string;
  comparator: string;
  limit: number;
  unit: string;
  measured: number | null;
  passed: boolean | null;
  source: string;
  limit_parameters: string[];
  margin: number | null;
}

export interface RunSummary {
  id: string;
  test_id: string;
  test_name: string;
  target: string;
  scenario_id: string;
  scenario_label: string;
  status: RunStatus;
  credibility: Credibility;
  created_at: string;
  history_cursor: number;
  current: boolean;
  failed: string[];
  warnings: string[];
}

export interface RunRecord {
  id: string;
  test_id: string;
  test_name: string;
  target: string;
  scenario: Scenario;
  revision: { values_hash: string; inputs_hash: string; history_cursor: number;
    entry_id: string | null };
  inputs: Record<string, { value: number; unit: string; label: string }>;
  solver: { id: string; version: string; method: string };
  config: Record<string, unknown>;
  numerics: Record<string, number | boolean>;
  metrics: Record<string, MetricInfo & { value: number | null }>;
  criteria: CriterionResult[];
  status: RunStatus;
  credibility: Credibility;
  assumptions: string[];
  warnings: string[];
  trace: Record<string, number[]>;
  created_at: string;
}

export interface MetricDelta {
  metric: string;
  label: string;
  unit: string;
  before: number | null;
  after: number | null;
  change: number | null;
  percent: number | null;
  verdict: "better" | "worse" | "unchanged" | "n/a";
}

export interface Comparison {
  baseline: string;
  candidate: string;
  same_test: boolean;
  changed_inputs: Record<string, { before: number; after: number; unit: string }>;
  metrics: MetricDelta[];
  criteria: { id: string; label: string; before: boolean | null; after: boolean | null;
    measured_before: number | null; measured_after: number | null; limit: number;
    unit: string }[];
  summary: string;
}

export interface TestRunResponse { runs: RunRecord[]; comparisons: Comparison[] }

export interface ComponentTestStatus {
  component: string;
  status: ComponentStatus;
  tests: { test_id: string; test_name: string; target: string; scenario_id: string;
    scenario_label: string; status: ComponentStatus; run_id: string | null }[];
}

export interface IntegrationCheck {
  id: string;
  kind: string;
  status: "pass" | "fail" | "warning";
  message: string;
  components: string[];
  parameters: string[];
  measured: number | null;
  limit: number | null;
  unit: string;
}

export interface IntegrationReport {
  checks: IntegrationCheck[];
  counts: Record<string, number>;
  not_checked: string[];
}

export interface Effect {
  parameter: string;
  label: string;
  unit: string;
  value: number;
  margin_up: number | null;
  margin_down: number | null;
  better_direction: "increase" | "decrease" | null;
  evidence: "confirmed_in_model" | "possible" | "none";
  side_effects: string[];
}

export interface Fix {
  parameter: string;
  label: string;
  operation: string;
  from_value: number;
  to_value: number;
  unit: string;
  step_percent: number;
  margin_after: number;
  breaks: string[];
  rule_violations: string[];
  command: Command;
}

export interface Finding {
  criterion: string;
  label: string;
  status: "failed" | "tightest_margin";
  measured: number | null;
  limit: number;
  unit: string;
  margin: number | null;
  limit_source: string;
  governing_parameter: string | null;
  effects: Effect[];
  fixes: Fix[];
  explanation: string;
}

export interface Diagnosis {
  run_id: string;
  test_id: string;
  target: string;
  scenario_id: string;
  scenario_label: string;
  design_revision: number;
  current: boolean;
  status: string;
  findings: Finding[];
  evidence: Record<string, unknown>;
  recommendation: string;
  caveats: string[];
}

export interface Variable { parameter: string; lower: number; upper: number }
export interface Objective { metric: string; sense: "minimize" | "maximize" }

export interface Study {
  test_id: string;
  target: string;
  scenarios: string[];
  objectives: Objective[];
  variables: Variable[];
  budget: number;
  seed?: number;
}

export interface Candidate {
  index: number;
  phase: "baseline" | "sample" | "refine";
  values: Record<string, number>;
  rule_violations: string[];
  simulated: boolean;
  feasible: boolean;
  objectives: Record<string, number>;
  failed: string[];
}

export interface StudyResult {
  id: string;
  created_at: string;
  study: Study;
  method: string;
  baseline: Candidate;
  candidates: Candidate[];
  best: Candidate | null;
  pareto: number[];
  verified: { scenario: string; status: string; converged: boolean;
    metrics: Record<string, number> }[];
  improvement: Record<string, number>;
  command: Command | null;
  evaluations: number;
  status: "proposed" | "accepted" | "rejected" | "no_feasible_design";
  blocking: string | null;
  notes: string[];
}

export interface LoopResult {
  id: string;
  created_at: string;
  goal: { test_id: string; target: string; scenarios: string[] | null;
    objective: Objective | null; max_iterations: number };
  iterations: { index: number; changes: Record<string, { from: number; to: number; unit: string }>;
    runs: { scenario: string; status: string; converged: boolean; failed: string[] }[];
    diagnosis: string | null; decision: string }[];
  outcome: "all_pass" | "needs_decision" | "iteration_limit" | "already_passing";
  optimization: StudyResult | null;
  command: Command | null;
  status: "proposed" | "accepted" | "rejected" | "nothing_to_apply";
  notes: string[];
}

export type Comparator = "<=" | "<" | ">=" | ">";

export interface Requirement {
  id: string;
  key: string;
  title: string;
  text: string;
  rationale: string;
  kind: "performance" | "design" | "text";
  verification: "test" | "analysis" | "inspection";
  priority: "must" | "should" | "may";
  parent: string | null;
  approved: boolean;
  source: string;
  created_at: string;
  test_id: string | null;
  target: string;
  scenario_id: string;
  metric: string | null;
  quantity: string | null;
  comparator: Comparator;
  limit: number;
  unit: string;
  note: string;
}

export interface RequirementEvidence {
  kind: string;
  status: "pass" | "fail" | "stale" | "missing";
  detail: string;
  run_id: string | null;
  measured: number | null;
  limit: number | null;
  unit: string;
  design_revision: number | null;
}

export interface RequirementRow {
  requirement: Requirement;
  verification: { requirement: string; key: string; status: string;
    evidence: RequirementEvidence[]; summary: string };
  parameters: string[];
  components: string[];
  cases: string[];
}

export interface ImpactPreview {
  valid: boolean;
  violations: Violation[];
  changes: { id: string; label: string; unit: string; before: number; after: number }[];
  derived: { id: string; label: string; unit: string; before: number; after: number }[];
  rebuild: string[];
  move: string[];
  retest: string[];
  requirements: { key: string; title: string; before: string; after: string; detail: string }[];
  warnings_added: string[];
  warnings_cleared: string[];
  summary: string;
}

export interface SpecQuestion {
  id: string;
  prompt: string;
  kind: "choice" | "number";
  options: string[];
  option_labels: string[];
  unit: string;
  minimum: number | null;
  maximum: number | null;
  optional: boolean;
  help: string;
}

export interface SpecCheck {
  id: string;
  severity: "conflict" | "warning" | "info";
  message: string;
  basis: string;
  answers: string[];
  parameters: string[];
  estimate: Record<string, number>;
}

export interface SpecState {
  spec: { answers: Record<string, { value: string | number; source: "user" | "default"; note: string }> };
  questions: SpecQuestion[];
  applicable: string[];
  next: SpecQuestion | null;
  checks: SpecCheck[];
  missing: string[];
}

export interface SpecDesign {
  values: Record<string, number>;
  sources: Record<string, string>;
  violations: Violation[];
  checks: SpecCheck[];
  requirements: Record<string, unknown>[];
  missing: string[];
  command: Command | null;
  preview: ImpactPreview | null;
}

export interface SystemGraph {
  nodes: { id: string; name: string; category: string; builder: string | null; parent: string | null;
    interfaces: { name: string; kind: string; used_by: string[] }[]; parameters: string[];
    tests: string[] }[];
  edges: { kind: string; source: string; target: string; detail: string }[];
}

export interface RuleStatus {
  id: string;
  description: string;
  parameters: string[];
  passed: boolean;
  message: string | null;
}

export interface DomainDef {
  id: string;
  name: string;
  description: string;
  status: "available" | "experimental" | "in_development" | "unavailable";
  component_library: string[];
  operations: string[];
  simulations: string[];
  formats: string[];
  dependencies: string[];
  version: string;
  roadmap: string[];
  evidence: string;
}

export interface RunIndexItem extends RunSummary {
  project_id: string;
  project_name: string;
}

export interface DesignTemplate {
  id: string;
  label: string;
  description: string;
}

/** A Part Design feature (see backend autevra/part/features.py): typed by ``type``. */
export type PartFeature = { id: string; type: string; name?: string; suppressed?: boolean;
  op?: "add" | "cut" | "intersect"; [field: string]: unknown };

export interface Placement { x?: number; y?: number; z?: number; rx?: number; ry?: number; rz?: number }

export interface PartDoc {
  name: string;
  features: PartFeature[];
  at?: Placement;
  color?: [number, number, number];
  finish?: string;
}

export interface PartOut {
  id: string;
  document: PartDoc;
  can_undo: boolean;
  can_redo: boolean;
  built: string[];
  errors: { feature: string; message: string }[];
  volume: number | null;
  bounds: [[number, number, number], [number, number, number]] | null;
}
