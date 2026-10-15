import { type ReactElement, useEffect, useMemo, useRef, useState } from "react";

type Pt = [number, number];

/** Grid step (mm) giving about 8–20 lines across the view. */
function gridStep(span: number): number {
  const steps = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000];
  return steps.find((s) => span / s <= 20) ?? 10000;
}

/**
 * A small 2D sketcher for a closed profile: drag a point to move it (snapped to the grid),
 * click a "+" handle to insert a point on an edge, double-click a point to delete it.
 * Changes are committed when a drag ends. ``axis`` draws the revolve axis (u = 0) and
 * keeps points on its positive side.
 */
export function Sketcher({ points, onCommit, axis = false, labels = ["u", "v"] }: {
  points: Pt[]; onCommit: (points: Pt[]) => void; axis?: boolean; labels?: [string, string];
}) {
  const [draft, setDraft] = useState<Pt[]>(points);
  const [drag, setDrag] = useState<number | null>(null);
  const svg = useRef<SVGSVGElement>(null);
  useEffect(() => { if (drag === null) setDraft(points); }, [points, drag]);

  // View box fitted to the committed points (stable while dragging), with a margin.
  const view = useMemo(() => {
    const us = points.map((p) => p[0]).concat(axis ? [0] : []);
    const vs = points.map((p) => p[1]);
    const [u0, u1, v0, v1] = [Math.min(...us), Math.max(...us), Math.min(...vs), Math.max(...vs)];
    const span = Math.max(u1 - u0, v1 - v0, 10);
    const m = span * 0.2;
    return { u0: u0 - m, v0: v0 - m, w: u1 - u0 + 2 * m, h: v1 - v0 + 2 * m, step: gridStep(span) };
  }, [points, axis]);
  const snap = (x: number) => Math.round(x / (view.step / 2)) * (view.step / 2);

  const toModel = (ev: { clientX: number; clientY: number }): Pt => {
    const rect = svg.current!.getBoundingClientRect();
    const scale = Math.max(view.w / rect.width, view.h / rect.height);
    const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
    const u = view.u0 + view.w / 2 + (ev.clientX - cx) * scale;
    const v = view.v0 + view.h / 2 - (ev.clientY - cy) * scale; // v up
    return [axis ? Math.max(0, snap(u)) : snap(u), snap(v)];
  };

  const r = Math.max(view.w, view.h) * 0.012; // handle radius in model units
  const lines: ReactElement[] = [];
  for (let u = Math.ceil(view.u0 / view.step) * view.step; u <= view.u0 + view.w; u += view.step) {
    lines.push(<line key={`u${u}`} x1={u} x2={u} y1={-view.v0 - view.h} y2={-view.v0} className="grid" />);
  }
  for (let v = Math.ceil(view.v0 / view.step) * view.step; v <= view.v0 + view.h; v += view.step) {
    lines.push(<line key={`v${v}`} x1={view.u0} x2={view.u0 + view.w} y1={-v} y2={-v} className="grid" />);
  }

  return (
    <div className="sketcher">
      <svg ref={svg} viewBox={`${view.u0} ${-view.v0 - view.h} ${view.w} ${view.h}`}
        preserveAspectRatio="xMidYMid meet"
        onPointerMove={(ev) => {
          if (drag === null) return;
          const p = toModel(ev);
          setDraft((d) => d.map((q, i) => (i === drag ? p : q)));
        }}
        onPointerUp={() => { if (drag !== null) { setDrag(null); onCommit(draft); } }}
        onPointerLeave={() => { if (drag !== null) { setDrag(null); onCommit(draft); } }}>
        {lines}
        {axis && <line x1={0} x2={0} y1={-view.v0 - view.h} y2={-view.v0} className="axis" />}
        <polygon points={draft.map(([u, v]) => `${u},${-v}`).join(" ")} className="profile" />
        {draft.map(([u, v], i) => {
          const [nu, nv] = draft[(i + 1) % draft.length];
          return (
            <g key={`m${i}`} className="insert" onPointerDown={(ev) => {
              ev.stopPropagation();
              const next = [...draft];
              next.splice(i + 1, 0, [snap((u + nu) / 2), snap((v + nv) / 2)]);
              onCommit(next);
            }}>
              <circle cx={(u + nu) / 2} cy={-(v + nv) / 2} r={r * 0.8} />
              <text x={(u + nu) / 2} y={-(v + nv) / 2} fontSize={r * 1.6} textAnchor="middle" dominantBaseline="central">+</text>
            </g>
          );
        })}
        {draft.map(([u, v], i) => (
          <circle key={`p${i}`} cx={u} cy={-v} r={r} className={`point ${drag === i ? "active" : ""}`}
            onPointerDown={(ev) => { ev.stopPropagation(); (ev.target as Element).setPointerCapture?.(ev.pointerId); setDrag(i); }}
            onDoubleClick={() => { if (draft.length > 3) onCommit(draft.filter((_, j) => j !== i)); }}>
            <title>{`${labels[0]} ${u}, ${labels[1]} ${v} (double-click to delete)`}</title>
          </circle>
        ))}
      </svg>
      <span className="hint">Drag points (snap {view.step / 2} mm) · “+” inserts · double-click deletes · grid {view.step} mm
        {axis && " · the vertical line is the revolve axis"}</span>
    </div>
  );
}
