import { useEffect, useRef, useState } from "react";
import type { InstructionResult } from "../api/types";

export interface ChatTurn {
  text: string;
  reply: InstructionResult | { kind: "error"; message: string };
}

interface Props {
  turns: ChatTurn[];
  busy: boolean;
  onSend: (text: string) => void;
}

const EXAMPLES = [
  "increase the wheelbase by 100 mm",
  "set the rims to 18 inch",
  "lower the car by 20 mm",
  "how long is the car?",
];

export function AiPanel({ turns, busy, onSend }: Props) {
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
      <h2>Instructions <small>deterministic parser · LLM off</small></h2>
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
              {t.reply.message}
              {"assumptions" in t.reply && t.reply.assumptions.length > 0 && (
                <div className="assumptions">Assumed: {t.reply.assumptions.join("; ")}</div>
              )}
              {"result" in t.reply && t.reply.result && t.reply.result.changed.length > 0 && (
                <div className="impact">
                  Rebuilt: {t.reply.result.impact.rebuild.join(", ") || "none"} · Moved:{" "}
                  {t.reply.result.impact.move.join(", ") || "none"}
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
