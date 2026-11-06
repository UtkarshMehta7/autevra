export type WorkspaceId =
  | "design" | "styling" | "part-design" | "package" | "assembly" | "simulation" | "ai-engineering" | "optimization" | "requirements"
  | "systems" | "manufacturing" | "digital-engineering";

export const WORKSPACES: { id: WorkspaceId; label: string; description: string }[] = [
  { id: "design", label: "Design", description: "Specification, parameters and the 3D model" },
  { id: "styling", label: "Styling", description: "Draw the body: silhouette, underbody and plan curves of the styled skin" },
  { id: "part-design", label: "Part Design", description: "Your own parts from a feature tree: sketches, revolves, lofts, sweeps, shells, patterns" },
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
