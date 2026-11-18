export type WorkspaceId =
  | "design" | "engine" | "vessel" | "breakdown" | "functions" | "loads" | "production" | "reviews" | "inventory" | "elements" | "machining" | "mates" | "library" | "routing" | "styling" | "part-design" | "surfaces" | "structures" | "aircraft" | "package" | "assembly" | "simulation" | "ai-engineering" | "optimization" | "requirements"
  | "systems" | "manufacturing" | "digital-engineering";

export const WORKSPACES: { id: WorkspaceId; label: string; description: string }[] = [
  { id: "design", label: "Design", description: "Specification, parameters and the 3D model" },
  { id: "engine", label: "Engine", description: "Piston engine: bore, stroke, layout and boost; cycle, torque and power, kinematics and balance; built as parts and published to the inventory" },
  { id: "vessel", label: "Vessel", description: "Displacement hull: form coefficients, hydrostatics, GZ curve against the IMO criteria, viscous resistance; built as parts" },
  { id: "breakdown", label: "Breakdown", description: "The whole product as systems and parts: every part from day one, mass and CG roll-ups, maturity heat map, configurations" },
  { id: "functions", label: "Functions", description: "Requirements → functions → logical blocks → parts: function chains, typed flows, interfaces, design FMEA and trace gaps" },
  { id: "loads", label: "Loads", description: "Load cases from the design (road g-cases, V-n and gust, landing, firing), the compliance matrix and the materials database" },
  { id: "production", label: "Production", description: "MBOM by station, process plan, takt and operators, unit cost and CO2, reconciliation, tolerance stack-ups" },
  { id: "reviews", label: "Reviews", description: "Review gates computed from the model, baselines and comparisons, engineering change requests with impact before approval" },
  { id: "inventory", label: "Inventory", description: "Shared library: ISO fasteners, bearings, hollow sections and published parts, with their ports and performance; add to the project" },
  { id: "elements", label: "Machine elements", description: "Shared calculators: bolted joints, fillet welds, fatigue (Goodman, S-N, rainflow), springs and spur gears; gear pairs added as parts" },
  { id: "machining", label: "Machining", description: "CAM for a part: stock, tools and cutting data by material, facing, Z-level roughing, rest machining, finishing, drilling and tapping from Hole features; toolpaths in 3D and ISO G-code" },
  { id: "mates", label: "Assembly design", description: "Constraints between parts: Fix, Coincidence, Contact, Offset, Angle on faces and axes; Update solves them, moves the parts and reports the degrees of freedom left" },
  { id: "library", label: "Library", description: "Design library for every module: save this design as a reusable starting point, start new projects from saved designs" },
  { id: "routing", label: "Routing", description: "Wiring harnesses and pipes along waypoints: bundle size, voltage drop, pressure drop and bend checks; added as parts" },
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

const SHARED: WorkspaceId[] = ["part-design", "mates", "inventory", "elements", "machining", "library", "routing", "surfaces", "structures"];

export const MODULES: ModuleDef[] = [
  { id: "automotive", label: "Land vehicles", noun: "Vehicle", description: "Cars, SUVs, pickups and trucks",
    workspaces: ["design", "breakdown", "functions", "loads", "production", "reviews", "styling", ...SHARED, "package", "assembly", "simulation", "ai-engineering",
      "optimization", "requirements", "systems", "manufacturing", "digital-engineering"] },
  { id: "aerospace", label: "Aircraft", noun: "Aircraft", description: "Fixed-wing aircraft",
    workspaces: ["aircraft", "breakdown", "functions", "loads", "production", "reviews", ...SHARED] },
  { id: "marine", label: "Marine", noun: "Vessel", description: "Displacement vessels: hull, stability, resistance",
    workspaces: ["vessel", "breakdown", "functions", "loads", "production", "reviews", ...SHARED] },
  { id: "machinery", label: "Mechanical", noun: "Engine", description: "Engines category by category (piston engines first)",
    workspaces: ["engine", "breakdown", "functions", "loads", "production", "reviews", ...SHARED] },
];

export function moduleOf(domain: string | undefined): ModuleDef {
  return MODULES.find((m) => m.id === (domain ?? "automotive")) ?? MODULES[0];
}
