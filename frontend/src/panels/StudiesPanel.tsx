import { useEffect, useState } from "react";
import type {
  Candidate, LoopResult, ParameterDef, StudyResult, TestDefinition, Variable,
} from "../api/types";
import { fmt } from "../state/engineering";

interface Props {
  definition: TestDefinition | undefined;
  parameters: ParameterDef[];
  values: Record<string, number>;
  studies: StudyResult[];
  loops: LoopResult[];
  busy: boolean;
  onOptimize: (target: string, scenarios: string[], metric: string, sense: "minimize" | "maximize",
    second: string | null, variables: Variable[], budget: number) => void;
  onLoop: (target: string, scenarios: string[], metric: string | null) => void;
  onDecide: (studyId: string, accept: boolean) => void;
  onChoose: (studyId: string, index: number) => void;
}

const ADJUSTABLE = ["spring_rate", "damping_bump", "damping_rebound", "unsprung_mass"];

function Scatter({ result }: { result: StudyResult }) {
  const [m1, m2] = result.study.objectives.map((o) => o.metric);
  const pts = result.candidates.filter((c) => c.simulated);
  if (pts.length === 0) return null;
  const xs = pts.map((c) => (m2 ? c.objectives[m2] : c.index));
  const ys = pts.map((c) => c.objectives[m1]);
  const [x0, x1] = [Math.min(...xs), Math.max(...xs)], [y0, y1] = [Math.min(...ys), Math.max(...ys)];
  const W = 360, H = 170, P = 34;
  const sx = (v: number) => P + ((v - x0) / (x1 - x0 || 1)) * (W - P - 8);
  const sy = (v: number) => 10 + (1 - (v - y0) / (y1 - y0 || 1)) * (H - 10 - P);
  const pareto = new Set(result.pareto);
  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="candidates">
      <text x={P} y={H - 8} className="tick">{m2 ?? "candidate"} {m2 ? `${fmt(x0)}–${fmt(x1)}` : ""}</text>
      <text x={4} y={12} className="tick">{m1} {fmt(y0)}–{fmt(y1)}</text>
      {pts.map((c) => (
        <circle key={c.index} cx={sx(m2 ? c.objectives[m2] : c.index)} cy={sy(c.objectives[m1])}
          r={c.index === result.best?.index || pareto.has(c.index) ? 4 : 2.5}
          className={c.phase === "baseline" ? "pt-base" : c.index === result.best?.index ? "pt-best"
            : pareto.has(c.index) ? "pt-front" : c.feasible ? "pt-ok" : "pt-bad"}>
          <title>{Object.entries(c.values).map(([k, v]) => `${k} ${v}`).join(", ")}
            {c.feasible ? "" : ` · infeasible: ${c.failed[0] ?? ""}`}</title>
        </circle>
      ))}
    </svg>
  );
}

function StudyView({ result, busy, onDecide, onChoose }: {
  result: StudyResult; busy: boolean; onDecide: Props["onDecide"]; onChoose: Props["onChoose"];
}) {
  const m = result.study.objectives[0].metric;
  const best: Candidate | null = result.best;
  return (
    <div className="study">
      <div className="run-head">
        <strong>{result.study.target} corner · {result.study.objectives.map((o) => `${o.sense} ${o.metric}`).join(" & ")}</strong>
        <span className={`status-pill ${result.status === "proposed" ? "pass" : result.status === "no_feasible_design" ? "failed" : ""}`}>
          {result.status.replace(/_/g, " ")}</span>
      </div>
      <div className="hint">{result.method} · {result.evaluations} simulated of {result.candidates.length} candidates · scenarios {result.study.scenarios.join(", ")}</div>
      {result.blocking && <div className="warnings">Blocking: {result.blocking}</div>}
      <Scatter result={result} />
      {best && (
        <table>
          <thead><tr><th /><th>Baseline</th><th>Proposed</th></tr></thead>
          <tbody>
            {Object.keys(best.values).map((p) => (
              <tr key={p}><td>{p}</td><td>{fmt(result.baseline.values[p])}</td><td>{fmt(best.values[p])}</td></tr>
            ))}
            <tr className="better"><td>worst-case {m}</td><td>{fmt(result.baseline.objectives[m])}</td>
              <td>{fmt(best.objectives[m])} ({fmt((result.improvement[m] / result.baseline.objectives[m]) * 100)} %)</td></tr>
          </tbody>
        </table>
      )}
      {result.verified.length > 0 && (
        <div className="hint">Verified with full runs: {result.verified.map((v) =>
          `${v.scenario} ${v.status.replace(/_/g, " ")}${v.converged ? "" : " (not converged)"}`).join("; ")}</div>
      )}
      {!best && result.pareto.length > 0 && (
        <ul className="fixes">
          {result.pareto.map((i) => {
            const c = result.candidates[i];
            return (
              <li key={i}>{Object.entries(c.objectives).map(([k, v]) => `${k} ${fmt(v)}`).join(" · ")}{" "}
                <button disabled={busy} onClick={() => onChoose(result.id, i)}>Choose</button></li>
            );
          })}
        </ul>
      )}
      <ul className="notes">{result.notes.map((n) => <li key={n}>{n}</li>)}</ul>
      {result.status === "proposed" && result.command && (
        <div className="decision">
          <button className="confirm" disabled={busy} onClick={() => onDecide(result.id, true)}>Accept design</button>
          <button disabled={busy} onClick={() => onDecide(result.id, false)}>Reject</button>
        </div>
      )}
    </div>
  );
}

function LoopView({ result, busy, onDecide }: { result: LoopResult; busy: boolean; onDecide: Props["onDecide"] }) {
  const last = result.iterations[result.iterations.length - 1];
  const changes = last ? Object.entries(last.changes) : [];
  return (
    <div className="study">
      <div className="run-head">
        <strong>Engineering loop · {result.goal.target} corner</strong>
        <span className={`status-pill ${result.outcome === "all_pass" || result.outcome === "already_passing" ? "pass" : "warning"}`}>
          {result.outcome.replace(/_/g, " ")}</span>
        <span className="hint">{result.status.replace(/_/g, " ")}</span>
      </div>
      <ol className="iterations">
        {result.iterations.map((it) => (
          <li key={it.index}>
            {it.runs.map((r) => (
              <span key={r.scenario} className={`status-pill ${r.status}`} title={r.failed.join(", ")}>{r.scenario}</span>
            ))}
            <div>{it.decision}</div>
            {it.diagnosis && <details><summary>evidence</summary><p className="hint">{it.diagnosis}</p></details>}
          </li>
        ))}
      </ol>
      {result.optimization && <StudyView result={result.optimization} busy onDecide={onDecide} onChoose={() => {}} />}
      {result.command && (
        <div className="hint">Proposed change: {result.command.changes.map((c) => `${c.parameter} → ${fmt(c.value)}`).join(", ")}
          {changes.length === 0 ? "" : ""}</div>
      )}
      {result.status === "proposed" && result.command && (
        <div className="decision">
          <button className="confirm" disabled={busy} onClick={() => onDecide(result.id, true)}>Accept design</button>
          <button disabled={busy} onClick={() => onDecide(result.id, false)}>Reject</button>
        </div>
      )}
    </div>
  );
}

export function StudiesPanel({ definition, parameters, values, studies, loops, busy, onOptimize, onLoop, onDecide, onChoose }: Props) {
  const [target, setTarget] = useState("rear");
  const [scenarios, setScenarios] = useState<string[]>(["step_25", "hump_75"]);
  const [metric, setMetric] = useState("rms_body_acceleration");
  const [sense, setSense] = useState<"minimize" | "maximize">("minimize");
  const [second, setSecond] = useState("");
  const [budget, setBudget] = useState(60);
  const [variables, setVariables] = useState<Variable[]>([]);
  const [shown, setShown] = useState<string | null>(null);

  useEffect(() => {
    // ±30 % around the current design, within each parameter's bounds.
    setVariables(ADJUSTABLE.slice(0, 3).map((s) => {
      const id = `${target}_${s}`;
      const def = parameters.find((p) => p.id === id);
      const v = values[id] ?? 0;
      return { parameter: id, lower: Math.max(def?.min ?? 0, +(v * 0.7).toFixed(3)),
        upper: Math.min(def?.max ?? v * 2, +(v * 1.3).toFixed(3)) };
    }));
  }, [target, parameters, values]);

  const items = [
    ...studies.map((s) => ({ id: s.id, at: s.created_at, kind: "study" as const, s })),
    ...loops.map((l) => ({ id: l.id, at: l.created_at, kind: "loop" as const, l })),
  ].sort((a, b) => b.at.localeCompare(a.at));
  const current = items.find((i) => i.id === shown) ?? items[0];
  if (!definition) return null;
  const metrics = Object.entries(definition.metrics);

  return (
    <div className="bench wide">
      <div className="bench-side">
        <div className="bench-controls">
          <select value={target} onChange={(e) => setTarget(e.target.value)}>
            {definition.targets.map((t) => <option key={t} value={t}>{t} corner</option>)}
          </select>
          <label>budget <input type="number" min={5} max={400} value={budget} className="narrow"
            onChange={(e) => setBudget(Number(e.target.value))} /></label>
        </div>
        <div className="bench-controls">
          {definition.scenarios.map((s) => (
            <label key={s.id} className="toggle">
              <input type="checkbox" checked={scenarios.includes(s.id)} onChange={(e) =>
                setScenarios(e.target.checked ? [...scenarios, s.id] : scenarios.filter((x) => x !== s.id))} />
              {s.label}
            </label>
          ))}
        </div>
        <div className="bench-controls">
          <select value={sense} onChange={(e) => setSense(e.target.value as "minimize" | "maximize")}>
            <option value="minimize">minimise</option><option value="maximize">maximise</option>
          </select>
          <select value={metric} onChange={(e) => setMetric(e.target.value)}>
            {metrics.map(([id, m]) => <option key={id} value={id}>{m.label}</option>)}
          </select>
          <select value={second} onChange={(e) => setSecond(e.target.value)} title="second objective (Pareto)">
            <option value="">single objective</option>
            {metrics.filter(([id]) => id !== metric).map(([id, m]) => <option key={id} value={id}>and minimise {m.label}</option>)}
          </select>
        </div>
        <table className="vars">
          <tbody>
            {variables.map((v, i) => (
              <tr key={v.parameter}>
                <td>{v.parameter}</td>
                {(["lower", "upper"] as const).map((k) => (
                  <td key={k}><input type="number" className="narrow" value={v[k]} onChange={(e) =>
                    setVariables(variables.map((x, j) => (j === i ? { ...x, [k]: Number(e.target.value) } : x)))} /></td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <div className="bench-controls">
          <button className="primary" disabled={busy || scenarios.length === 0}
            onClick={() => onOptimize(target, scenarios, metric, sense, second || null, variables, budget)}>Optimise</button>
          <button disabled={busy || scenarios.length === 0}
            onClick={() => onLoop(target, scenarios, null)}>Run engineering loop</button>
        </div>
        <p className="hint">Constraints are every test criterion and approved requirement in each chosen scenario. Nothing changes until you accept.</p>
        <ul className="runs">
          {items.map((i) => (
            <li key={i.id}>
              <button className={`run-item${current?.id === i.id ? " selected" : ""}`} onClick={() => setShown(i.id)}>
                {i.kind === "study"
                  ? `${i.s.study.target} · optimise ${i.s.study.objectives[0].metric} · ${i.s.status.replace(/_/g, " ")}`
                  : `${i.l.goal.target} · loop · ${i.l.outcome.replace(/_/g, " ")}`}
              </button>
            </li>
          ))}
        </ul>
      </div>
      <div className="bench-detail">
        {!current && <p className="hint">Run an optimisation or the engineering loop.</p>}
        {current?.kind === "study" && <StudyView result={current.s} busy={busy} onDecide={onDecide} onChoose={onChoose} />}
        {current?.kind === "loop" && <LoopView result={current.l} busy={busy} onDecide={onDecide} />}
      </div>
    </div>
  );
}
