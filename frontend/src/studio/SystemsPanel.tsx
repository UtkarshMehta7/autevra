import { type ReactElement, useEffect, useState } from "react";
import { api } from "../api/client";
import type { SystemGraph } from "../api/types";

/** System architecture from the assembly definition: components, interfaces, relationships. */
export function SystemsPanel({ projectId, version, compact, onSelect }: {
  projectId: string; version: number; compact?: boolean; onSelect: (id: string) => void;
}) {
  const [graph, setGraph] = useState<SystemGraph | null>(null);
  const [kind, setKind] = useState("mounted_to");
  useEffect(() => {
    api.system(projectId).then(setGraph).catch(() => setGraph(null));
  }, [projectId, version]);
  if (!graph) return <p className="hint">Loading the system graph…</p>;
  const children = (parent: string | null) => graph.nodes.filter((n) => n.parent === parent);
  const tree = (id: string | null, depth: number): ReactElement[] => children(id).flatMap((n) => [
    <li key={n.id} style={{ paddingLeft: depth * 14 }}>
      <button className="link" onClick={() => onSelect(n.id)}>{n.name}</button>
      <small className="hint"> {n.category}{n.tests.length ? ` · tests: ${n.tests.join(", ")}` : ""}</small>
      {!compact && n.interfaces.length > 0 && (
        <div className="hint ifaces">{n.interfaces.map((i) =>
          `${i.name} (${i.kind})${i.used_by.length ? ` ← ${i.used_by.join(", ")}` : ""}`).join(" · ")}</div>
      )}
    </li>,
    ...tree(n.id, depth + 1),
  ]);
  const edges = graph.edges.filter((e) => e.kind === kind);
  return (
    <div className={compact ? "systems compact" : "bench wide"}>
      <div className={compact ? "" : "bench-side"}>
        <strong>Assembly tree</strong> <small className="hint">({graph.nodes.length} components; click to select)</small>
        <ul className="tree-list">{tree(null, 0)}</ul>
      </div>
      {!compact && (
        <div className="bench-detail">
          <div className="bench-controls">
            <strong>Relationships</strong>
            <select value={kind} onChange={(e) => setKind(e.target.value)}>
              <option value="mounted_to">mounted to (mates)</option>
              <option value="coincident">closed mounts (coincidences)</option>
              <option value="load_path">load paths</option>
            </select>
            <span className="hint">{edges.length} relationship(s)</span>
          </div>
          <table>
            <thead><tr><th>From</th><th>To</th><th>Detail</th></tr></thead>
            <tbody>{edges.map((e, i) => <tr key={i}><td>{e.source}</td><td>{e.target}</td><td className="hint">{e.detail}</td></tr>)}</tbody>
          </table>
          <p className="hint">Relationships are the assembly's own data (mates, coincidences, load
            paths), validated by the Integration checks. Electrical, fluid and control
            connections are not modelled yet.</p>
        </div>
      )}
    </div>
  );
}
