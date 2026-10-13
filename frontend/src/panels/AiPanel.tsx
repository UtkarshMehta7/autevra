import { useEffect, useRef, useState } from "react";
import type { InstructionResult, LLMStatus } from "../api/types";
import { llmLabel } from "../state/llm";

export interface ChatTurn {
  text: string;
  reply: InstructionResult | { kind: "error"; message: string };
  /** For LLM proposals: what the user decided. */
  decision?: "confirmed" | "rejected" | "failed";
}

interface Props {
  turns: ChatTurn[];
  busy: boolean;
  llm: LLMStatus | null;
  onSend: (text: string) => void;
  onDecide: (turn: number, confirm: boolean) => void;
}

const EXAMPLES = [
  "I want an electric SUV with 220 kW, 7 seats and AWD",
  "increase the wheelbase by 100 mm",
  "increase the rear shock absorber damping by 10% and test its response",
  "test the front suspension over a pothole",
  "explain why the suspension travel limit was exceeded",
  "optimise ride comfort on the rear over the hump",
  "fix the rear suspension",
  "make the suspension softer",
  "how long is the car?",
];

export function AiPanel({ turns, busy, llm, onSend, onDecide }: Props) {
  const [text, setText] = useState("");
  const log = useRef<HTMLDivElement>(null);
  useEffect(() => {
    // Block body: in current browsers scrollTo returns a Promise, which must not reach React.
    log.current?.scrollTo(0, log.current.scrollHeight);
  }, [turns]);

  const send = (value: string) => {
    if (!value.trim()) return;
    onSend(value.trim());
    setText("");
  };

  return (
    <section className="panel ai">
      <h2>Instructions <small title={llm?.detail || llm?.url}>{llmLabel(llm)}</small></h2>
      <div className="chat" ref={log}>
        {turns.length === 0 && (
          <div className="hint">
            Try:{" "}
            {EXAMPLES.map((e) => (
              <button key={e} className="chip" onClick={() => send(e)}>{e}</button>
            ))}
          </div>
        )}
        {turns.map((t, i) => (
          <div key={i} className="turn">
            <div className="you">{t.text}</div>
            <div className={`reply ${t.reply.kind}`}>
              {"interpreted_by" in t.reply && t.reply.interpreted_by === "llm" && (
                <span className="badge" title="Interpreted by the local language model">LLM</span>
              )}
              {t.reply.message}
              {t.reply.kind === "proposal" && (
                t.decision ? (
                  <div className="decision">
                    {t.decision === "confirmed" ? "Applied." : t.decision === "rejected"
                      ? "Discarded." : "Could not be applied (it may have expired)."}
                  </div>
                ) : (
                  <div className="decision">
                    <button className="confirm" onClick={() => onDecide(i, true)}>Confirm</button>
                    <button onClick={() => onDecide(i, false)}>Reject</button>
                  </div>
                )
              )}
              {"assumptions" in t.reply && t.reply.assumptions.length > 0 && (
                <div className="assumptions">Assumed: {t.reply.assumptions.join("; ")}</div>
              )}
              {"result" in t.reply && t.reply.result && t.reply.result.changed.length > 0 && (
                <div className="impact">
                  Rebuilt: {t.reply.result.impact.rebuild.join(", ") || "none"} · Moved:{" "}
                  {t.reply.result.impact.move.join(", ") || "none"}
                  {(t.reply.result.impact.retest?.length ?? 0) > 0 &&
                    ` · Tests to rerun: ${t.reply.result.impact.retest!.join(", ")}`}
                </div>
              )}
              {"suggestions" in t.reply && t.reply.suggestions.length > 0 && (
                <div>
                  {t.reply.suggestions.map((s) => (
                    <button key={s} className="chip" onClick={() => send(s)}>{s}</button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={(e) => { e.preventDefault(); send(text); }}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe a change, e.g. increase the wheelbase by 100 mm"
          autoFocus
        />
        <button type="submit" disabled={!text.trim()}>{busy ? "Queue" : "Send"}</button>
      </form>
    </section>
  );
}
