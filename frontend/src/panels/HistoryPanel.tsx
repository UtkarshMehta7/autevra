import type { HistoryEntry } from "../api/types";
import { describeChange } from "../state/format";

interface Props {
  entries: HistoryEntry[];
  cursor: number;
}

export function HistoryPanel({ entries, cursor }: Props) {
  return (
    <section className="panel">
      <h2>History</h2>
      <ol className="history">
        <li className={cursor === 0 ? "current" : ""}>Initial design</li>
        {entries.map((e, i) => (
          <li key={e.id} className={`${i + 1 === cursor ? "current" : ""}${
            i + 1 > cursor ? " undone" : ""}`}>
            {e.command.source === "llm" ? (
              <span className="source ai" title={`Proposed by the AI${e.command.model ? ` (${e.command.model})` : ""} from: “${e.command.instruction ?? ""}”, then validated and applied like any edit`}>
                AI{e.command.model ? ` · ${e.command.model}` : ""}
              </span>
            ) : <span className="source">{e.command.source}</span>} {describeChange(e)}
          </li>
        ))}
      </ol>
    </section>
  );
}
