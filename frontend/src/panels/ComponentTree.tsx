import type { ModelPart } from "../api/types";
import { CATEGORY_LABELS, groupParts } from "../state/format";

interface Props {
  parts: ModelPart[];
  selected: string | null;
  highlighted: string[];
  onSelect: (id: string) => void;
}

export function ComponentTree({ parts, selected, highlighted, onSelect }: Props) {
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
              title={`geometry ${p.geometry}`}
            >
              {p.name}
            </button>
          ))}
        </div>
      ))}
    </section>
  );
}
