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
  source?: "ui" | "api" | "rules" | "llm" | "optimizer" | "spec";
  instruction?: string | null;
  model?: string | null; // the language model behind an AI-originated change
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
  op?: "add" | "cut" | "intersect"; bindings?: Record<string, string>; [field: string]: unknown };

export interface Placement { x?: number; y?: number; z?: number; rx?: number; ry?: number; rz?: number }

export interface FeatureTemplate {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, number | string>;
  features: PartFeature[];
}

export interface Styling {
  curves: { top: [number, number][]; bottom: [number, number][]; plan: [number, number][] };
  custom: { top: boolean; bottom: boolean; plan: boolean };
  reference: { rear: number; front: number; wheelbase: number; tyre_radius: number;
    overall_height: number; half_width: number; beltline: number; glass: number[]; roof: number[] };
  can_undo: boolean;
  can_redo: boolean;
}

export interface PackageValue { id: string; label: string; value: number; unit: string; note: string }

export interface BomLine {
  item: string;
  category: string;
  quantity: number;
  size: [number, number, number];
  volume: number;
  source: string;
  parts: string[];
}

export interface DesignTable {
  columns: string[];
  rows: { name: string; values: number[] }[];
  active?: string | null;
}

export interface PartDoc {
  name: string;
  parameters?: Record<string, number | string>;
  design_table?: DesignTable | null;
  features: PartFeature[];
  at?: Placement;
  color?: [number, number, number];
  finish?: string;
}

/** B-rep topology after a feature (backend cad/topology.py). */
export interface Topology {
  vertices: number; edges: number; loops: number; faces: number; shells: number; solids: number;
  rings: number; euler: number; genus: number; balanced: boolean;
  free_edges: number; nonmanifold_edges: number; degenerate_edges: number; seam_edges: number;
  watertight: boolean; valid: boolean;
  surfaces: Record<string, number>; curves: Record<string, number>;
  area: number; volume: number;
}

/** Where a boolean's tool met the body (the curves the boolean is computed along). */
export interface BooleanSection {
  op: "add" | "cut" | "intersect"; tools: number; curves: number; length: number;
  polylines: [number, number, number][][];
}

export interface PartOut {
  id: string;
  document: PartDoc;
  can_undo: boolean;
  can_redo: boolean;
  built: string[];
  errors: { feature: string; message: string }[];
  info?: Record<string, Record<string, number>>;
  topology?: Record<string, Topology | { error: string }>; // per feature, after it
  sections?: Record<string, BooleanSection>; // per boolean feature on an existing body
  reused?: string[]; // features taken from the prefix cache in the last build
  feature_ms?: Record<string, number>; // ms per rebuilt feature
  graph?: PartGraph;
  volume: number | null;
  bounds: [[number, number, number], [number, number, number]] | null;
}

/** A constrained 2D sketch (see backend autevra/part/sketch.py). */
export interface SketchPoint { id: string; x: number; y: number; fixed?: boolean }
export type SketchEntity =
  | { type: "line"; id: string; a: string; b: string; construction?: boolean }
  | { type: "circle"; id: string; center: string; radius: number; construction?: boolean }
  | { type: "arc"; id: string; center: string; start: string; end: string; construction?: boolean };
export interface SketchConstraint { kind: string; refs: string[]; value?: number | null }
export interface Sketch { points: SketchPoint[]; entities: SketchEntity[]; constraints: SketchConstraint[] }
export interface SketchSolve {
  sketch: Sketch;
  ok: boolean;
  dof: number;
  redundant: number;
  conflicting: number[];
  fixed_points: string[];
  fixed_entities: string[];
  residual: number;
  // Inspection (backend part/sketch.py): the system F(x) = 0 and the convergence history.
  method?: string;
  unknowns?: number;
  equations?: { index: number | null; kind: string; text: string; rows: number; residual: number }[];
  rank?: number;
  iterations?: { step: number; cost: number; max_residual: number; damping: number; step_norm: number; accepted: boolean }[];
  converged?: boolean;
}

/** A NURBS surface (backend geometry/nurbs.py): control grid [u][v] of (x, y, z), weights. */
export interface NurbsSurface {
  degree_u: number;
  degree_v: number;
  control: [number, number, number][][];
  weights?: number[][];
  knots_u?: number[];
  knots_v?: number[];
}

export interface NurbsEvaluation {
  surface: Required<NurbsSurface>;
  grid: { u: number[]; v: number[]; points: [number, number, number][]; normals: [number, number, number][];
    gaussian: number[]; mean: number[]; triangles: number[] };
  basis_u: { t: number[]; functions: number[][] };
  basis_v: { t: number[]; functions: number[][] };
  domain: [[number, number], [number, number]];
  support: { u: [number, number]; v: [number, number]; point: [number, number, number]; weight: number } | null;
}

export interface ContinuityReport {
  report: { samples: number; gap: number; angle: number; curvature_a: number[]; curvature_b: number[];
    curvature_jump: number; rate_jump: number; level: "none" | "G0" | "G1" | "G2" | "G3"; explanation: string };
  tolerances: { g0: number; g1_deg: number; g2_rel: number; g3_rel: number };
  combs: { points: [number, number, number][]; tips: [number, number, number][]; curvature: number[] }[];
}

/** Linear static FEA run (backend api/structures.py, fea/). */
export interface FeaRequest {
  demo?: string;
  element: "tet4" | "tet10" | "hex8";
  size: number;
  material: { name: string; youngs?: number; poisson?: number; density?: number; yield_strength?: number };
  supports: string[];
  loads: { region: string; force: [number, number, number]; pressure: number }[];
}

export interface FeaFace { id: number; type: string; area: number; centre: [number, number, number]; normal: [number, number, number] }

export interface FeaMesh {
  kind: "tet4" | "tet10" | "hex8"; nodes: [number, number, number][]; boundary: [number, number, number][];
  boundary_face: number[]; faces: FeaFace[];
  stats: { nodes: number; elements: number; size: number; volume_ratio: number; quality_min: number;
    quality_mean: number; slivers: number; method: string };
  cad_volume: number;
}

export interface FeaResult {
  mesh: FeaMesh;
  fields: { displacement: [number, number, number][]; magnitude: number[]; von_mises: number[];
    principal_1: number[]; strain_eq: number[] };
  supports: number[];
  loaded: Record<string, number[]>;
  material: { name: string; youngs: number; poisson: number; density: number; yield_strength: number };
  stats: { dofs: number; free_dofs: number; fixed_dofs: number; k_shape: [number, number]; k_nnz: number;
    k_density: number; k_memory_mb: number; element_matrix: [number, number]; cg_iterations: number;
    cg_converged: boolean; cg_residuals: number[]; cg_final_residual: number; direct_difference: number | null;
    time_assemble: number; time_solve: number; applied_force: [number, number, number];
    reaction_force: [number, number, number]; equilibrium_error: number; compliance: number;
    max_displacement: number; max_von_mises: number; max_principal: number; min_principal: number;
    factor_of_safety: number | null; mass_kg: number; method: string };
  assumptions: string[];
}

export interface FeaCatalogue {
  demos: Record<string, string>;
  materials: Record<string, { name: string; youngs: number; poisson: number; density: number; yield_strength: number }>;
  regions: string[];
}

/** SIMP topology optimisation (backend fea/simp.py). */
export interface TopologyRequest {
  case: "mbb" | "cantilever" | "bridge" | "bracket";
  nx: number; ny: number; nz: number; volfrac: number; penal: number; rmin: number; max_iter: number;
}

export interface TopologyResult {
  shape: number[];
  description: string;
  density: number[];
  snapshots: number[][];
  snapshot_iters: number[];
  history: { iter: number; compliance: number; volume: number; change: number; grey: number; lambda: number }[];
  stats: { elements: number; dofs: number; free_dofs: number; k_nnz_per_element: number; iterations: number;
    converged: boolean; final_change: number; final_compliance: number; initial_compliance: number;
    volume_fraction: number; grey_fraction: number; filter_neighbours: number; time_solve: number;
    time_total: number; solver: string };
  equations: string[];
}

/** A part's dependency graph (backend part/graph.py). */
export interface PartGraph {
  nodes: { id: string; kind: "parameter" | "feature"; label: string; type?: string; suppressed?: boolean; value?: number | string }[];
  edges: { from: string; to: string; kind: "expression" | "binding" | "body" | "repeats"; field?: string }[];
  levels: Record<string, number>;
}

/** Parametric aircraft (backend aero/aircraft.py). */
export interface AircraftSpec {
  name: string;
  wing_span: number; wing_root_chord: number; wing_tip_chord: number; wing_sweep: number; wing_dihedral: number;
  wing_twist: number; wing_naca: string; wing_x: number; high_wing: boolean; cl_max_section: number;
  fuselage_length: number; fuselage_width: number; fuselage_height: number;
  htail_span: number; htail_root_chord: number; htail_tip_chord: number; htail_x: number; t_tail: boolean;
  fin_height: number; fin_root_chord: number; fin_tip_chord: number; fin_sweep: number; fin_x: number;
  power_kw: number; prop_diameter: number; prop_efficiency: number; bsfc: number; mtow: number; fuel_mass: number;
  x_cg: number; fixed_gear: boolean; tricycle: boolean; cruise_speed: number; cruise_altitude: number;
}

export interface AircraftAnalysis {
  atmosphere: { T: number; p: number; rho: number; mu: number; a: number; sigma: number; altitude: number; mach: number; q: number };
  geometry: { wing_area: number; aspect_ratio: number; taper: number; mac: number; mac_x: number; mac_y: number;
    htail_area: number; fin_area: number; tail_arm: number; fin_arm: number; wetted_area: number };
  aero: { wing_lift_slope: number; tail_lift_slope: number; downwash_gradient: number; oswald_e: number; span_efficiency: number;
    cl_cruise: number; alpha_cruise: number; cd0: number; cd_cruise: number; l_over_d: number; ld_max: number; v_ld_max: number;
    zero_lift_angle: number; gear_cd0: number; span_y: number[]; span_cl: number[]; polar: { cl: number; cd: number }[];
    components: { name: string; re: number; cf: number; ff: number; q: number; s_wet: number; cd0: number }[] };
  stability: { x_ac_wing: number; x_ac_tail: number; x_np: number; x_cg: number; static_margin: number; v_h: number; v_v: number; eta: number };
  performance: { wing_loading: number; power_loading: number; drag: number; power_required: number; power_available: number;
    v_stall: number; cl_max: number; range_km: number; endurance_h: number };
  checks: { name: string; value: number; range: [number, number]; unit: string; status: "pass" | "warn" | "fail"; why: string }[];
  assumptions: string[];
}

/** Product structure (backend product/ and modules/): one module's breakdown with
 * maturity, mass and CG roll-ups for one configuration. */
export interface Rollup {
  mass: number; cg: [number, number, number]; parts: number; instances: number;
  maturity: number[]; min_maturity: number; over_budget: string[];
}
export interface BreakdownNode {
  id: string; name: string; kind: "product" | "system" | "subsystem" | "part"; code: string;
  template: string; process: string; functions: string[]; applicability: string; instances: number;
  maturity: number; mass: number; mass_source: "allocated" | "estimated" | "computed"; basis: string;
  budget: number | null; cg: [number, number, number]; envelope: [number, number, number];
  geometry: string; rollup: Rollup; children: BreakdownNode[];
}
export interface OptionFamily { id: string; label: string; choices: string[]; applies: string; affects_mass: boolean; description: string }
export interface OptionRule { id: string; when: string; then: string; message: string }
export interface ProductCheck { id: string; label: string; status: "pass" | "warn" | "fail"; message: string }
export interface ProductOut {
  module: string; module_name: string; frame: string; levels: string[];
  families: OptionFamily[]; rules: OptionRule[];
  design_configuration: Record<string, string>; configuration: Record<string, string>;
  violations: string[]; breakdown: BreakdownNode; checks: ProductCheck[]; templates: number;
}
export interface ProductEnvelope {
  configurations: number; mass_min: number; mass_max: number;
  lightest: Record<string, string>; heaviest: Record<string, string>; cg_x_min: number; cg_x_max: number;
}

/** Systems layer (backend product/systems.py): functions → logical blocks → parts. */
export type FlowKind = "mechanical" | "electrical_power" | "signal" | "fluid" | "thermal";
export interface SysFunction { id: string; name: string; parent: string; requirements: string[] }
export interface SysBlock { id: string; name: string; functions: string[]; templates: string[]; applicability: string; external: boolean }
export interface SysFlow { id: string; kind: FlowKind; source: string; target: string; item: string; attributes: Record<string, string>; applicability: string }
export interface IcdRow { flow: string; kind: FlowKind; source: string; target: string; item: string; attributes: Record<string, string> }
export interface FailureRow { id: string; function: string; block: string; mode: string; effect: string; severity: number; occurrence: number; detection: number; rpn: number; priority: "high" | "medium" | "low"; action: string }
export interface TraceIssue { kind: string; subject: string; message: string; severity: "fail" | "warn" }
export interface SystemsOut {
  module: string; configuration: Record<string, string>; functions: SysFunction[]; blocks: SysBlock[];
  flows: SysFlow[]; icd: IcdRow[]; failure_modes: FailureRow[]; issues: TraceIssue[];
  requirements: { key: string; text: string; function: string }[]; allocations: Record<string, string>;
}
export interface ChainStep { block: string; name: string; external: boolean; parts: { id: string; name: string; mass: number; maturity: number; instances: number }[]; flows_out: SysFlow[] }

/** Shared inventory (backend inventory/). */
export interface ItemSummary { id: string; version: string; kind: string; family: string; category: string; name: string; standard: string; mass_kg: number | null }
export interface ItemPort { name: string; kind: string; at: Record<string, number>; attributes: Record<string, number | string> }
export interface InventoryItem extends ItemSummary {
  status: string; parameters: Record<string, number | string>; properties: Record<string, number | string>;
  performance: Record<string, number>; ports: ItemPort[]; notes: string[]; provenance: string;
}

/** Mechanical module: piston engines (backend mech/piston.py). */
export interface EngineSpec {
  name: string; fuel: "petrol" | "diesel"; layout: "inline" | "V" | "boxer"; cylinders: number;
  bank_angle: number; flat_plane: boolean; bore: number; stroke: number; rod_ratio: number;
  compression_ratio: number; turbo: boolean; bmep_max: number; rpm_peak_torque: number;
  rpm_max: number; rpm_idle: number;
}
export interface EngineAnalysis {
  displacement_l: number; firing_order: string; peak_torque_nm: number; peak_torque_rpm: number; torque_band_rpm: [number, number];
  peak_power_kw: number; peak_power_rpm: number; specific_power_kw_per_l: number;
  mean_piston_speed_ms: number; efficiency: { air_standard: number; fuel_air_approx: number };
  kinematics: Record<string, number>; balance: Record<string, number>; balance_n: Record<string, number>;
  mass_kg: number; curve: { rpm: number; torque_nm: number; power_kw: number; bmep_bar: number }[];
  checks: { id: string; label: string; status: "pass" | "warn" | "fail"; message: string }[];
}
