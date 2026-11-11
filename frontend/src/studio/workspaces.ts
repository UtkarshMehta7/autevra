export type WorkspaceId =
  | "design" | "breakdown" | "functions" | "styling" | "part-design" | "surfaces" | "structures" | "aircraft" | "package" | "assembly" | "simulation" | "ai-engineering" | "optimization" | "requirements"
  | "systems" | "manufacturing" | "digital-engineering";

export const WORKSPACES: { id: WorkspaceId; label: string; description: string }[] = [
  { id: "design", label: "Design", description: "Specification, parameters and the 3D model" },
  { id: "breakdown", label: "Breakdown", description: "The whole product as systems and parts: every part from day one, mass and CG roll-ups, maturity heat map, configurations" },
  { id: "functions", label: "Functions", description: "Requirements → functions → logical blocks → parts: function chains, typed flows, interfaces, design FMEA and trace gaps" },
  { id: "styling", label: "Styling", description: "Draw the body: silhouette, underbody and plan curves of the styled skin" },
  { id: "part-design", label: "Part Design", description: "Your own parts from a feature tree: sketches, revolves, lofts, sweeps, shells, patterns" },
  { id: "surfaces", label: "Surfaces", description: "NURBS surface lab: control points, weights, knots and basis functions; curvature; G0–G3 continuity" },
  { id: "structures", label: "Structures", description: "Linear static FEA: tetrahedral or voxel mesh, sparse K u = F, conjugate gradients, von Mises stress and factor of safety" },
  { id: "aircraft", label: "Aircraft", description: "Parametric aircraft: lifting-line aerodynamics, drag build-up, neutral point and static margin, performance; built as a part" },
  { id: "package", label: "Package", description: "Package drawing, clearance angles, H-point and the main dimensions" },
  { id: "assembly", label: "Assembly", description: "Interfaces, mounts, clearances and integration checks" },
  { id: "simulation", label: "Simulation", description: "Component tests, results and comparisons" },
  { id: "ai-engineering", label: "AI engineering", description: "Instructions, proposals and the operation log" },
  { id: "optimization", label: "Optimization", description: "Bounded studies and the engineering loop" },
  { id: "requirements", label: "Requirements", description: "Requirements, evidence and ReqIF" },
  { id: "systems", label: "Systems", description: "System architecture: components and relationships" },
  { id: "manufacturing", label: "Manufacturing", description: "Exports and manufacturability checks" },
  { id: "digital-engineering", label: "Digital thread", description: "Revisions, runs and studies over time" },
];

/** Engineering modules: each project belongs to one, and the studio shows only that
 * module's workspaces (domains are kept apart; shared tools act on the module's parts). */
export interface ModuleDef { id: string; label: string; noun: string; workspaces: WorkspaceId[]; planned?: boolean; description: string }

const SHARED: WorkspaceId[] = ["part-design", "surfaces", "structures"];

export const MODULES: ModuleDef[] = [
  { id: "automotive", label: "Land vehicles", noun: "Vehicle", description: "Cars, SUVs, pickups and trucks",
    workspaces: ["design", "breakdown", "functions", "styling", ...SHARED, "package", "assembly", "simulation", "ai-engineering",
      "optimization", "requirements", "systems", "manufacturing", "digital-engineering"] },
  { id: "aerospace", label: "Aircraft", noun: "Aircraft", description: "Fixed-wing aircraft",
    workspaces: ["aircraft", "breakdown", "functions", ...SHARED] },
  { id: "marine", label: "Marine", noun: "Vessel", description: "Hulls and marine propulsion (planned)", workspaces: [], planned: true },
  { id: "machinery", label: "Mechanical", noun: "Machine", description: "Engines, machinery and mechanisms (planned)", workspaces: [], planned: true },
];

export function moduleOf(domain: string | undefined): ModuleDef {
  return MODULES.find((m) => m.id === (domain ?? "automotive")) ?? MODULES[0];
}
