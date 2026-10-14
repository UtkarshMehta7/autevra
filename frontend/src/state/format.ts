import type { ModelPart } from "../api/types";

export function formatValue(value: number, unit: string): string {
  const rounded = Math.round(value * 1000) / 1000;
  return `${rounded} ${unit}`;
}

export const CATEGORY_LABELS: Record<string, string> = {
  body: "Body",
  exterior: "Exterior options",
  chassis: "Chassis",
  axle: "Axles",
  wheel: "Wheels",
  suspension: "Suspension",
  brakes: "Brakes",
  interior: "Interior",
  powertrain: "Powertrain",
  electrical: "Electrical",
  custom: "Part Design",
};

/** Parts grouped by category, in a stable display order. */
export function groupParts(parts: ModelPart[]): [string, ModelPart[]][] {
  const order = Object.keys(CATEGORY_LABELS);
  const groups = new Map<string, ModelPart[]>();
  for (const part of parts) {
    groups.set(part.category, [...(groups.get(part.category) ?? []), part]);
  }
  return [...groups.entries()].sort(([a], [b]) => {
    const ia = order.indexOf(a), ib = order.indexOf(b);
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
  });
}

/**
 * Geometry keys to evict after a model update. Unused geometry is kept (oldest
 * evicted first, ``cached`` is in insertion order) so undo/redo can reuse it.
 */
export function staleGeometry(cached: Iterable<string>, parts: ModelPart[], keep = 16): string[] {
  const used = new Set(parts.map((p) => p.geometry));
  const unused = [...cached].filter((key) => !used.has(key));
  return unused.slice(0, Math.max(0, unused.length - keep));
}

export function describeChange(entry: {
  command: { instruction?: string | null };
  changes: { parameter: string; old: number; new: number }[];
}): string {
  if (entry.command.instruction) return entry.command.instruction;
  return entry.changes.map((c) => `${c.parameter}: ${c.old} → ${c.new}`).join(", ");
}
