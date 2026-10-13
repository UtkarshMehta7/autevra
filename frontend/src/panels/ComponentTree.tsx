import type { ComponentStatus, ModelPart } from "../api/types";
import { STATUS_LABELS } from "../state/engineering";
import { CATEGORY_LABELS, groupParts } from "../state/format";

interface Props {
  parts: ModelPart[];
  selected: string | null;
  highlighted: string[];
  /** Component test status, for components that have tests. */
  statuses: Record<string, ComponentStatus>;
  onSelect: (id: string) => void;
}

export function ComponentTree({ parts, selected, highlighted, statuses, onSelect }: Props) {
  return (
    <section className="panel">
      <h2>Components</h2>
      {groupParts(parts).map(([category, items]) => (
        <div key={category} className="tree-group">
          <div className="tree-category">{CATEGORY_LABELS[category] ?? category}</div>
          {items.map((p) => (
            <button
              key={p.id}
              className={`tree-item${p.id === selected ? " selected" : ""}${
                highlighted.includes(p.id) ? " changed" : ""}`}
              onClick={() => onSelect(p.id)}
              title={statuses[p.id] ? STATUS_LABELS[statuses[p.id]] : `geometry ${p.geometry}`}
            >
              {statuses[p.id] && <span className={`dot ${statuses[p.id]}`} />}
              {p.name}
            </button>
          ))}
        </div>
      ))}
    </section>
  );
}
