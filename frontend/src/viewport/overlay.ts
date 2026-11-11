/** Inspection overlays drawn in the 3D view over a part (for example the section curves a
 * boolean was computed along). Panels publish an overlay; the viewport draws it in the
 * part's own frame, on top of the shaded model. */
export type Polyline = [number, number, number][];

export interface Overlay {
  partId: string; // the placed part (e.g. "part_<id>") whose frame the points are in
  polylines: Polyline[];
  color?: number;
}

let current: Overlay | null = null;
const listeners = new Set<(o: Overlay | null) => void>();

export function setOverlay(next: Overlay | null): void {
  current = next;
  for (const l of listeners) l(next);
}

export function currentOverlay(): Overlay | null {
  return current;
}

export function onOverlay(listener: (o: Overlay | null) => void): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}
