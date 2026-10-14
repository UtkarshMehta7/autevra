import { useEffect, useState } from "react";
import type { LLMStatus } from "../api/types";
import { llmLabel } from "../state/llm";
import { type ChatTurn, EXAMPLES, TurnView } from "./AiPanel";

interface Props {
  turns: ChatTurn[];
  busy: boolean;
  llm: LLMStatus | null;
  onSend: (text: string) => void;
  onDecide: (turn: number, confirm: boolean) => void;
}

const MORE_EXAMPLES = [
  "make it a pickup", "paint it racing red", "make the interior premium",
  "make it electric", "give it a v8", "test the pitch over the hump",
];

/**
 * One-line command input in the studio header (like a CAD power-input line): plain-English
 * instructions are parsed deterministically; the reply shows under the bar and earlier
 * turns are a click away. A proposal from the optional local model still needs Confirm.
 */
export function CommandBar({ turns, busy, llm, onSend, onDecide }: Props) {
  const [text, setText] = useState("");
  const [open, setOpen] = useState(false); // reply / history popover
  const [history, setHistory] = useState(false);
  useEffect(() => { if (turns.length) setOpen(true); }, [turns.length]);
  const send = (value: string) => {
    if (!value.trim()) return;
    onSend(value.trim());
    setText("");
  };
  const last = turns.length - 1;
  const pending = turns.some((t) => t.reply.kind === "proposal" && !t.decision);
  return (
    <div className="command-bar">
      <form onSubmit={(e) => { e.preventDefault(); send(text); }}>
        <input value={text} onChange={(e) => setText(e.target.value)} list="command-examples"
          placeholder="Command: e.g. make it a pickup · paint it red · test the pitch over the hump"
          aria-label="Command" onFocus={() => turns.length && setOpen(true)} />
        <datalist id="command-examples">
          {[...MORE_EXAMPLES, ...EXAMPLES].map((e) => <option key={e} value={e} />)}
        </datalist>
        <button type="submit" disabled={!text.trim()}>{busy ? "Queue" : "Run"}</button>
      </form>
      <small className="command-status" title={llm?.detail || llm?.url}>{llmLabel(llm)}</small>
      {turns.length > 0 && (
        <button className={`subtle${pending ? " attention" : ""}`} onClick={() => setOpen(!open)}
          title="Show the last reply and the history">{pending ? "Confirm…" : `Replies (${turns.length})`}</button>
      )}
      {open && turns.length > 0 && (
        <div className="command-popover chat" role="dialog" aria-label="Command replies">
          <div className="popover-actions">
            <button className="subtle" onClick={() => setHistory(!history)}>
              {history ? "Latest only" : `History (${turns.length})`}</button>
            <button className="subtle" onClick={() => setOpen(false)} aria-label="Close">✕</button>
          </div>
          {(history ? turns.map((t, i) => [t, i] as const) : [[turns[last], last] as const]).map(([t, i]) => (
            <TurnView key={i} t={t} i={i} onDecide={onDecide} send={send} />
          ))}
        </div>
      )}
    </div>
  );
}
