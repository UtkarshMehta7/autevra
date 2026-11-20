import type { PartGraph } from "../api/types";

const EDGE_COLOURS: Record<string, string> = {
  expression: "#8a7bd1", binding: "#c9a227", body: "#6fa8ff", repeats: "#58c08a",
};

/** The part's dependency DAG in columns by depth: parameters feed expressions and bound
 * fields, each feature reads the body before it, and patterns repeat a solid. With a
 * feature selected, what it reads (upstream) and what rebuilds after it (downstream) are
 * highlighted. */
export function DependencyGraph({ graph, selected, onSelect }: {
  graph: PartGraph; selected: string | null; onSelect: (featureId: string) => void;
}) {
  const columns = new Map<number, string[]>();
  for (const n of graph.nodes) {
    const lv = graph.levels[n.id] ?? 0;
    columns.set(lv, [...(columns.get(lv) ?? []), n.id]);
  }
  const depth = Math.max(0, ...columns.keys()) + 1;
  const rows = Math.max(1, ...[...columns.values()].map((c) => c.length));
  const CW = 118, RH = 30, W = depth * CW + 10, H = rows * RH + 12;
  const pos = new Map<string, [number, number]>();
  for (const [lv, ids] of columns) ids.forEach((id, i) => pos.set(id, [8 + lv * CW, 8 + i * RH + (rows - ids.length) * RH / 2]));

  const focus = selected ? `feature:${selected}` : null;
  const up = new Set<string>(), down = new Set<string>();
  if (focus) {
    const walk = (start: string, next: (id: string) => string[], into: Set<string>) => {
      const stack = [start];
      while (stack.length) for (const n of next(stack.pop()!)) if (!into.has(n)) { into.add(n); stack.push(n); }
    };
    walk(focus, (id) => graph.edges.filter((e) => e.to === id).map((e) => e.from), up);
    walk(focus, (id) => graph.edges.filter((e) => e.from === id).map((e) => e.to), down);
  }
  const tone = (id: string) => (!focus ? "" : id === focus ? "focus" : up.has(id) ? "up" : down.has(id) ? "down" : "dim");

  return (
    <div className="dag">
      <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H} role="img" aria-label="Feature dependency graph">
        <defs>
          {Object.entries(EDGE_COLOURS).map(([k, c]) => (
            <marker key={k} id={`arrow-${k}`} viewBox="0 0 6 6" refX="6" refY="3" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M0,0 L6,3 L0,6 z" fill={c} />
            </marker>
          ))}
        </defs>
        {graph.edges.map((e, i) => {
          const [x0, y0] = pos.get(e.from)!, [x1, y1] = pos.get(e.to)!;
          const a = x0 + 104, b = y0 + 11, c = x1, d = y1 + 11;
          const on = !focus || ((up.has(e.from) || e.from === focus) && (up.has(e.to) || e.to === focus))
            || ((down.has(e.to)) && (down.has(e.from) || e.from === focus));
          return (
            <path key={i} d={`M${a},${b} C${a + 22},${b} ${c - 22},${d} ${c},${d}`} fill="none"
              stroke={EDGE_COLOURS[e.kind]} strokeWidth={on ? 1.6 : 0.8} strokeOpacity={on ? 0.95 : 0.25}
              markerEnd={`url(#arrow-${e.kind})`}><title>{`${e.kind}${e.field ? ` (${e.field})` : ""}`}</title></path>
          );
        })}
        {graph.nodes.map((n) => {
          const [x, y] = pos.get(n.id)!;
          const feature = n.kind === "feature";
          return (
            <g key={n.id} className={`dag-node ${n.kind} ${tone(n.id)} ${n.suppressed ? "suppressed" : ""}`}
              transform={`translate(${x},${y})`} onClick={() => feature && onSelect(n.id.slice(8))}
              style={{ cursor: feature ? "pointer" : "default" }}>
              <rect width={104} height={22} rx={feature ? 4 : 11} />
              <text x={52} y={14.5} textAnchor="middle">{n.label.length > 15 ? `${n.label.slice(0, 14)}…` : n.label}</text>
              <title>{feature ? `${n.type}: ${n.label}` : `${n.label} = ${n.value}`}</title>
            </g>
          );
        })}
      </svg>
      <div className="dag-legend">
        {Object.entries(EDGE_COLOURS).map(([k, c]) => <span key={k}><i style={{ background: c }} />{k}</span>)}
        {focus && <span className="muted">· amber: what it reads · green: what rebuilds after it</span>}
      </div>
    </div>
  );
}
