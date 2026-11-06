import { type ReactNode, useEffect, useRef, useState } from "react";

export type Pt = [number, number];

export interface EditableCurve {
  id: string;
  points: Pt[];
  color: string;
  label: string;
}

/**
 * Editor for open curves running from rear to front (x increasing), in model units with
 * v upwards. Drag a point (it stays between its neighbours in x), click "+" to insert one,
 * double-click to delete one (at least three stay). Commits when a drag ends.
 */
export function CurveEditor({ curves, view, onCommit, children, height = 260, onPick }: {
  curves: EditableCurve[];
  view: { x0: number; x1: number; v0: number; v1: number };
  onCommit: (id: string, points: Pt[]) => void;
  children?: ReactNode; // background drawn in model units (v already flipped by the caller)
  height?: number;
  onPick?: (point: Pt) => void; // when set, a click on the background reports a model point
}) {
  const [draft, setDraft] = useState<Record<string, Pt[]>>({});
  const [drag, setDrag] = useState<{ id: string; i: number } | null>(null);
  const svg = useRef<SVGSVGElement>(null);
  useEffect(() => { if (!drag) setDraft({}); }, [curves, drag]);
  const pointsOf = (c: EditableCurve) => draft[c.id] ?? c.points;
  const w = view.x1 - view.x0, h = view.v1 - view.v0;
  const r = Math.max(w, h) * 0.008;

  const toModel = (ev: { clientX: number; clientY: number }): Pt => {
    const rect = svg.current!.getBoundingClientRect();
    const scale = Math.max(w / rect.width, h / rect.height);
    const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
    return [view.x0 + w / 2 + (ev.clientX - cx) * scale, view.v0 + h / 2 - (ev.clientY - cy) * scale];
  };
  const finish = () => {
    if (!drag) return;
    const c = curves.find((k) => k.id === drag.id);
    const pts = draft[drag.id];
    setDrag(null);
    if (c && pts) onCommit(c.id, pts.map(([x, v]) => [Math.round(x), Math.round(v)]));
  };

  return (
    <svg ref={svg} className="curve-editor"
      viewBox={`${view.x0} ${-view.v1} ${w} ${h}`} preserveAspectRatio="xMidYMid meet"
      onPointerMove={(ev) => {
        if (!drag) return;
        const c = curves.find((k) => k.id === drag.id);
        if (!c) return;
        const pts = [...pointsOf(c)];
        const [x, v] = toModel(ev);
        const lo = drag.i > 0 ? pts[drag.i - 1][0] + 5 : -Infinity;
        const hi = drag.i < pts.length - 1 ? pts[drag.i + 1][0] - 5 : Infinity;
        pts[drag.i] = [Math.min(Math.max(x, lo), hi), v];
        setDraft((d) => ({ ...d, [c.id]: pts }));
      }}
      onPointerUp={finish} onPointerLeave={finish}
      onPointerDown={(ev) => { if (onPick && !drag) onPick(toModel(ev)); }}
      style={{ height, cursor: onPick ? "crosshair" : undefined }}>
      {children}
      {curves.map((c) => {
        const pts = pointsOf(c);
        return (
          <g key={c.id}>
            <polyline points={pts.map(([x, v]) => `${x},${-v}`).join(" ")} fill="none" stroke={c.color}
              strokeWidth={2.5} vectorEffect="non-scaling-stroke" />
            {pts.slice(0, -1).map(([x, v], i) => {
              const [nx, nv] = pts[i + 1];
              return (
                <circle key={`m${i}`} cx={(x + nx) / 2} cy={-(v + nv) / 2} r={r * 0.6} className="curve-insert"
                  onPointerDown={(ev) => {
                    ev.stopPropagation();
                    const next = [...pts];
                    next.splice(i + 1, 0, [Math.round((x + nx) / 2), Math.round((v + nv) / 2)]);
                    onCommit(c.id, next);
                  }}><title>Insert a point</title></circle>
              );
            })}
            {pts.map(([x, v], i) => (
              <circle key={`p${i}`} cx={x} cy={-v} r={r} fill={c.color} className="curve-point"
                onPointerDown={(ev) => { ev.stopPropagation(); (ev.target as Element).setPointerCapture?.(ev.pointerId); setDrag({ id: c.id, i }); }}
                onDoubleClick={() => { if (pts.length > 3) onCommit(c.id, pts.filter((_, j) => j !== i)); }}>
                <title>{`${c.label}: x ${Math.round(x)}, ${Math.round(v)} mm (double-click deletes)`}</title>
              </circle>
            ))}
          </g>
        );
      })}
    </svg>
  );
}
