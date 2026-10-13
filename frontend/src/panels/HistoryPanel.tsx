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
            <span className="source">{e.command.source}</span> {describeChange(e)}
          </li>
        ))}
      </ol>
    </section>
  );
}
