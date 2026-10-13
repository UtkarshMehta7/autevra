import type { HistoryEntry, LoopResult, RequirementRow, RunSummary, StudyResult } from "../api/types";

/** The digital thread: every revision with the runs, studies and evidence attached to it. */
export function DigitalPanel({ history, runs, studies, loops, requirements, onOpenRun }: {
  history: { entries: HistoryEntry[]; cursor: number };
  runs: RunSummary[]; studies: StudyResult[]; loops: LoopResult[];
  requirements: RequirementRow[]; onOpenRun: (id: string) => void;
}) {
  const revisions = [{ index: 0, label: "Initial design", source: "", when: "" },
    ...history.entries.map((e, i) => ({ index: i + 1, label: e.command.instruction ?? "edit",
      source: e.command.source ?? "", when: e.created_at }))];
  const verified = requirements.filter((r) => r.verification.status === "verified").length;
  return (
    <div className="bench wide">
      <div className="bench-side">
        <p><strong>{history.entries.length}</strong> change(s), current revision <strong>{history.cursor}</strong></p>
        <p><strong>{runs.length}</strong> stored test run(s) · <strong>{studies.length}</strong> optimisation(s) ·{" "}
          <strong>{loops.length}</strong> engineering loop(s)</p>
        <p><strong>{verified}</strong> of {requirements.length} requirement(s) verified on the current revision</p>
        <p className="hint">Every run records the exact design revision and a hash of the inputs it
          read, so results go stale exactly when their inputs change.</p>
      </div>
      <div className="bench-detail">
        <table>
          <thead><tr><th>Rev</th><th>Change</th><th>Source</th><th>Runs on this revision</th></tr></thead>
          <tbody>
            {revisions.map((r) => {
              const here = runs.filter((x) => x.history_cursor === r.index);
              return (
                <tr key={r.index} className={r.index === history.cursor ? "selected-row" : r.index > history.cursor ? "undone" : ""}>
                  <td>{r.index}</td>
                  <td>{r.label}{r.when && <small className="hint"> · {new Date(r.when).toLocaleString()}</small>}</td>
                  <td>{r.source && <span className="source">{r.source}</span>}</td>
                  <td>{here.map((x) => (
                    <button key={x.id} className={`status-pill ${x.current ? x.status : "stale"}`}
                      onClick={() => onOpenRun(x.id)} title={x.test_name}>
                      {x.target} · {x.scenario_label}
                    </button>
                  ))}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
