import { useEffect, useState } from "react";
import type { ParameterDef, SpecDesign, SpecQuestion, SpecState } from "../api/types";
import { fmt } from "../state/engineering";

interface Props {
  state: SpecState | null;
  design: SpecDesign | null;
  parameters: ParameterDef[];
  values: Record<string, number>;
  busy: boolean;
  onAnswer: (question: string, value: string | number | null) => void;
  onText: (text: string) => void;
  onReset: () => void;
  onDesign: () => void;
  onApply: () => void;
}

function QuestionInput({ q, current, busy, onAnswer }: {
  q: SpecQuestion; current: string | number | undefined; busy: boolean;
  onAnswer: Props["onAnswer"];
}) {
  const [num, setNum] = useState(current !== undefined && current !== "skip" ? String(current) : "");
  useEffect(() => setNum(current !== undefined && current !== "skip" ? String(current) : ""), [current, q.id]);
  return (
    <div className="question">
      <div><strong>{q.prompt}</strong> {q.help && <span className="hint">{q.help}</span>}</div>
      {q.kind === "choice" ? (
        <div className="choices">
          {q.options.map((o, i) => (
            <button key={o} className={`chip${current === o ? " picked" : ""}`} disabled={busy}
              onClick={() => onAnswer(q.id, o)}>{q.option_labels[i]}</button>
          ))}
        </div>
      ) : (
        <form className="bench-controls" onSubmit={(e) => { e.preventDefault(); if (num) onAnswer(q.id, Number(num)); }}>
          <input className="narrow" type="number" value={num} min={q.minimum ?? undefined}
            max={q.maximum ?? undefined} onChange={(e) => setNum(e.target.value)} />
          <span>{q.unit}</span>
          <button type="submit" disabled={busy || !num}>Set</button>
        </form>
      )}
      {q.optional && <button className="chip" disabled={busy} onClick={() => onAnswer(q.id, null)}>Skip (use class-typical)</button>}
    </div>
  );
}

export function SpecPanel({ state, design, parameters, values, busy, onAnswer, onText, onReset, onDesign, onApply }: Props) {
  const [text, setText] = useState("");
  const [editing, setEditing] = useState<string | null>(null);
  if (!state) return <p className="hint">Loading the specification…</p>;
  const answers = state.spec.answers;
  const shown = state.questions.filter((q) => state.applicable.includes(q.id));
  const editQ = state.questions.find((q) => q.id === editing) ?? state.next;
  const conflicts = (design?.checks ?? state.checks).filter((c) => c.severity === "conflict");
  const label = (id: string) => parameters.find((p) => p.id === id);

  return (
    <div className="bench wide">
      <div className="bench-side">
        <form className="bench-controls" onSubmit={(e) => { e.preventDefault(); if (text.trim()) { onText(text); setText(""); } }}>
          <input className="grow" value={text} onChange={(e) => setText(e.target.value)}
            placeholder="Describe it, e.g. an electric SUV, 220 kW, 7 seats, AWD" />
          <button type="submit" disabled={busy || !text.trim()}>Fill in</button>
        </form>
        {editQ ? (
          <QuestionInput q={editQ} current={answers[editQ.id]?.value} busy={busy}
            onAnswer={(qid, v) => { onAnswer(qid, v); setEditing(null); }} />
        ) : <p className="hint">All questions answered.</p>}
        <table className="answers">
          <tbody>
            {shown.map((q) => {
              const a = answers[q.id];
              return (
                <tr key={q.id} className={editQ?.id === q.id ? "selected-row" : ""} onClick={() => setEditing(q.id)}>
                  <td>{q.prompt}</td>
                  <td>{a ? (a.value === "skip" ? "class-typical" : `${q.kind === "choice" ? q.option_labels[q.options.indexOf(String(a.value))] ?? a.value : fmt(Number(a.value))} ${q.kind === "number" && a.value !== "skip" ? q.unit : ""}`) : <span className="hint">—</span>}</td>
                  <td>{a && <span className="source">{a.source === "user" ? "you" : "default"}</span>}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="bench-controls">
          <button className="primary" disabled={busy || !answers.vehicle_class} onClick={onDesign}>Generate design</button>
          <button disabled={busy} onClick={onReset}>Reset</button>
        </div>
      </div>
      <div className="bench-detail">
        <ul className="checks">
          {(design?.checks ?? state.checks).map((c) => (
            <li key={c.id} title={`basis: ${c.basis}`}>
              <span className={`status-pill ${c.severity === "conflict" ? "failed" : c.severity === "warning" ? "warning" : ""}`}>{c.severity}</span>
              {c.message} <small className="hint">(basis: {c.basis})</small>
            </li>
          ))}
        </ul>
        {state.missing.length > 0 && <p className="hint">Still to answer: {state.missing.join(", ")}</p>}
        {design && (
          <>
            <div className="run-head">
              <strong>Generated design</strong>
              {design.preview && <span className="hint">{design.preview.summary}</span>}
            </div>
            {design.violations.length > 0 && (
              <div className="warnings">Rule violations: {design.violations.map((v) => v.message).join("; ")}</div>
            )}
            <table>
              <thead><tr><th>Parameter</th><th>Now</th><th>Proposed</th><th>Why</th></tr></thead>
              <tbody>
                {(design.command?.changes ?? []).map((c) => {
                  const def = label(c.parameter);
                  return (
                    <tr key={c.parameter}>
                      <td>{def?.label ?? c.parameter}</td>
                      <td>{fmt(values[c.parameter], def?.unit)}</td>
                      <td>{fmt(c.value, def?.unit)}</td>
                      <td className="hint">{design.sources[c.parameter] ?? ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {design.requirements.length > 0 && (
              <p className="hint">Also proposes {design.requirements.length} requirement(s), added unapproved for you to review.</p>
            )}
            <div className="decision">
              <button className="confirm" disabled={busy || conflicts.length > 0 || state.missing.length > 0 || !design.command}
                onClick={onApply}>Apply design</button>
              {conflicts.length > 0 && <span className="bad-text">Resolve the conflicts first.</span>}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
