import { useState } from "react";
import type { LLMStatus } from "../api/types";
import type { ChatTurn } from "../panels/AiPanel";
import { llmLabel } from "../state/llm";

/** Operations the instruction pipeline supports today, each with an example that runs. */
const OPERATIONS: [string, string, string][] = [
  ["update parameter", "increase the wheelbase by 100 mm", "deterministic parser"],
  ["impact preview", "what if I set the rims to 20 inch?", "deterministic parser"],
  ["run simulation", "test the rear suspension over a pothole", "deterministic parser"],
  ["diagnose failure", "explain why the suspension travel limit was exceeded", "deterministic parser"],
  ["optimise parameters", "optimise ride comfort on the rear over the hump", "deterministic parser"],
  ["engineering loop", "fix the rear suspension", "deterministic parser"],
  ["create requirement", "require the ground clearance to be at least 150 mm", "deterministic parser"],
  ["specification", "I want an electric SUV with 220 kW, 7 seats and AWD", "deterministic parser"],
  ["undo operation", "undo", "deterministic parser"],
  ["unresolved text", "stretch the gap between the axles a little, say 4 inches", "local LLM proposal, needs confirmation"],
];
const NOT_YET = ["create component", "move component", "connect components", "create constraint",
  "generate engineering report"];

export function AiEngineeringPanel({ turns, llm, onSend }: {
  turns: ChatTurn[]; llm: LLMStatus | null; onSend: (text: string) => void;
}) {
  const [filter, setFilter] = useState("");
  const log = turns.filter((t) => !filter || t.reply.kind === filter);
  return (
    <div className="bench wide">
      <div className="bench-side">
        <p><strong>Language model:</strong> {llmLabel(llm)}</p>
        <p className="hint">The parser handles everything it can. A local model ({llm?.model ?? "none"})
          only proposes changes for text the parser cannot resolve, and each proposal needs your
          confirmation. Every operation is validated by the design rules before it is applied.</p>
        <table>
          <thead><tr><th>Operation</th><th>Try</th></tr></thead>
          <tbody>
            {OPERATIONS.map(([op, example, how]) => (
              <tr key={op}><td>{op}<br /><small className="hint">{how}</small></td>
                <td><button className="chip" onClick={() => onSend(example)}>{example}</button></td></tr>
            ))}
          </tbody>
        </table>
        <p className="hint">Not available yet: {NOT_YET.join(", ")}.</p>
      </div>
      <div className="bench-detail">
        <div className="bench-controls">
          <strong>Operation log (this session)</strong>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="">all kinds</option>
            {[...new Set(turns.map((t) => t.reply.kind))].map((k) => <option key={k}>{k}</option>)}
          </select>
        </div>
        {log.length === 0 && <p className="hint">No instructions yet in this session.</p>}
        <ol className="oplog">
          {log.map((t, i) => (
            <li key={i}>
              <span className={`status-pill ${t.reply.kind === "rejected" || t.reply.kind === "error" ? "failed" : t.reply.kind === "proposal" ? "warning" : "pass"}`}>{t.reply.kind}</span>
              <strong>{t.text}</strong>
              <div className="hint">{t.reply.message}</div>
              {"command" in t.reply && t.reply.command && (
                <code className="op">{t.reply.command.changes.map((c) =>
                  `${c.operation} ${c.parameter} ${c.value}${c.unit ? " " + c.unit : ""}`).join("; ")}</code>
              )}
              {t.decision && <div className="hint">Decision: {t.decision}</div>}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
