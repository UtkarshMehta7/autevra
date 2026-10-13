import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import type { Command, Comparison, Diagnosis, RunRecord, RunSummary, TestDefinition } from "../api/types";
import { CREDIBILITY_LABELS, fmt, STATUS_LABELS, STATUS_SHORT } from "../state/engineering";
import { DiagnosisView } from "./DiagnosisView";
import { LineChart, type Series } from "./LineChart";

interface Props {
  projectId: string;
  definitions: TestDefinition[];
  runs: RunSummary[];
  comparisons: Comparison[];
  selected: string | null;
  busy: boolean;
  /** Corner of the component selected in the tree, if any. */
  focusTarget: string | null;
  onSelect: (runId: string) => void;
  onRun: (testId: string, target: string, scenarioId: string | null) => void;
  onApply: (command: Command) => void;
  /** A diagnosis already computed (e.g. by an instruction) for the selected run. */
  diagnosis: Diagnosis | null;
}

const BLUE = "#4f8fe6", GREY = "#8b96a3", AMBER = "#e0a33a", GREEN = "#5cbf8a";

function TraceCharts({ run, baseline }: { run: RunRecord; baseline: RunRecord | null }) {
  const tr = run.trace, bt = baseline?.trace;
  if (!tr.t?.length) return <p className="hint">This test has no time history (closed-form result).</p>;
  const limit = (id: string) => run.criteria.find((c) => c.id === id)?.limit;
  const bump = limit("bump_travel"), rebound = limit("rebound_travel");
  const withBase = (label: string, key: string, color: string): Series[] => [
    { label, values: tr[key], color },
    ...(bt?.[key] ? [{ label: "before", values: bt[key], color: GREY, dashed: true }] : []),
  ];
  return (
    <div className="charts">
      <LineChart title="Wheel travel, + compression" unit="mm" t={tr.t} baselineT={bt?.t}
        series={withBase("travel", "travel_mm", BLUE)}
        limits={[
          ...(bump !== undefined ? [{ value: bump, label: `bump limit ${fmt(bump)}` }] : []),
          ...(rebound !== undefined ? [{ value: -rebound, label: `rebound limit ${fmt(rebound)}` }] : []),
        ]} />
      <LineChart title="Body and road height" unit="mm" t={tr.t} baselineT={bt?.t}
        series={[{ label: "road", values: tr.road_mm, color: AMBER },
          ...withBase("body", "body_mm", BLUE)]} />
      <LineChart title="Body acceleration" unit="m/s²" t={tr.t} baselineT={bt?.t}
        series={withBase("body", "body_acc", BLUE)} />
      <LineChart title="Tyre load / static load" unit="–" t={tr.t} baselineT={bt?.t}
        series={withBase("tyre", "tyre_load_ratio", GREEN)}
        limits={[{ value: 0, label: "lift-off" }]} />
    </div>
  );
}

export function TestBench({
  projectId, definitions, runs, comparisons, selected, busy, focusTarget, onSelect, onRun,
  onApply, diagnosis: given,
}: Props) {
  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [diagnosing, setDiagnosing] = useState(false);
  useEffect(() => {
    setDiagnosis(given && given.run_id === selected ? given : null);
  }, [given, selected]);
  const diagnose = () => {
    if (!selected) return;
    setDiagnosing(true);
    api.diagnosis(projectId, selected).then(setDiagnosis).finally(() => setDiagnosing(false));
  };
  const [testId, setTestId] = useState("quarter_car");
  const [target, setTarget] = useState("rear");
  const [scenario, setScenario] = useState<string>("");
  const [run, setRun] = useState<RunRecord | null>(null);
  const [baseline, setBaseline] = useState<RunRecord | null>(null);
  const [comparison, setComparison] = useState<Comparison | null>(null);
  const [baselineChoice, setBaselineChoice] = useState<string>("");
  const definition = definitions.find((d) => d.id === testId);
  useEffect(() => {
    if (focusTarget) setTarget(focusTarget);
  }, [focusTarget]);

  useEffect(() => {
    if (!selected) { setRun(null); return; }
    let live = true;
    api.run(projectId, selected).then((r) => { if (live) setRun(r); }).catch(() => setRun(null));
    return () => { live = false; };
  }, [projectId, selected]);

  // Same test, target and scenario on other revisions: candidates for "compare with".
  const peers = useMemo(() => runs.filter((r) => run && r.id !== run.id && r.test_id === run.test_id
    && r.target === run.target && r.scenario_id === run.scenario.id), [runs, run]);

  useEffect(() => {
    if (!run) { setComparison(null); setBaseline(null); return; }
    const auto = comparisons.find((c) => c.candidate === run.id);
    const baseId = baselineChoice || auto?.baseline || "";
    if (!baseId) { setComparison(null); setBaseline(null); return; }
    let live = true;
    Promise.all([
      auto && auto.baseline === baseId ? Promise.resolve(auto) : api.compare(projectId, baseId, run.id),
      api.run(projectId, baseId),
    ]).then(([c, b]) => { if (live) { setComparison(c); setBaseline(b); } })
      .catch(() => { if (live) { setComparison(null); setBaseline(null); } });
    return () => { live = false; };
  }, [projectId, run, comparisons, baselineChoice]);

  useEffect(() => setBaselineChoice(""), [selected]);

  return (
    <div className="bench">
      <div className="bench-side">
        <div className="bench-controls">
          <select value={testId} onChange={(e) => { setTestId(e.target.value); setScenario(""); }}>
            {definitions.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
          </select>
          <select value={target} onChange={(e) => setTarget(e.target.value)}>
            {definition?.targets.map((t) => <option key={t} value={t}>{t} corner</option>)}
            <option value="all">both</option>
          </select>
          <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
            <option value="">all scenarios</option>
            {definition?.scenarios.map((s) => <option key={s.id} value={s.id}>{s.label}</option>)}
          </select>
          <button className="primary" disabled={busy}
            onClick={() => onRun(testId, target, scenario || null)}>Run</button>
        </div>
        {definition && <p className="hint">{definition.description}</p>}
        <ul className="runs">
          {runs.length === 0 && <li className="hint">No runs yet.</li>}
          {runs.map((r) => (
            <li key={r.id}>
              <button className={`run-item${r.id === selected ? " selected" : ""}`}
                onClick={() => onSelect(r.id)} title={STATUS_LABELS[r.status]}>
                <span className={`status-pill ${r.current ? r.status : "stale"}`}>
                  {r.current ? STATUS_SHORT[r.status] : "stale"}
                </span>
                {r.target} · {r.scenario_label}
                <small> rev {r.history_cursor}</small>
              </button>
            </li>
          ))}
        </ul>
      </div>
      <div className="bench-detail">
        {!run && <p className="hint">Run a test or pick a run to see its evidence.</p>}
        {run && (
          <>
            <div className="run-head">
              <strong>{run.test_name}, {run.target} corner, {run.scenario.label}</strong>
              <span className={`status-pill ${run.status}`}>{STATUS_LABELS[run.status]}</span>
              <span className="hint">{CREDIBILITY_LABELS[run.credibility]}</span>
            </div>
            <div className="hint">
              {run.solver.id} {run.solver.version} ({run.solver.method}) · design revision{" "}
              {run.revision.history_cursor} ({run.revision.values_hash}) ·{" "}
              {run.numerics.converged ? "converged" : "NOT converged"}
              {run.numerics.max_relative_change_at_half_step !== undefined &&
                ` (Δ at half step ${fmt(Number(run.numerics.max_relative_change_at_half_step) * 100)} %)`}
              {" · "}{run.scenario.note}
            </div>
            {run.warnings.length > 0 && <div className="warnings">{run.warnings.join(" · ")}</div>}
            <div className="bench-controls">
              <button onClick={diagnose} disabled={diagnosing}>
                {diagnosing ? "Diagnosing…" : run.status === "failed" ? "Diagnose failure" : "Find tightest margin"}
              </button>
              {diagnosis && <button onClick={() => setDiagnosis(null)}>Hide diagnosis</button>}
            </div>
            {diagnosis && <DiagnosisView diagnosis={diagnosis} busy={busy} onApply={onApply} />}
            <table className="criteria">
              <thead><tr><th>Criterion</th><th>Measured</th><th>Limit</th><th>Margin</th><th /></tr></thead>
              <tbody>
                {run.criteria.length === 0 && (
                  <tr><td colSpan={5} className="hint">No criteria: results are reported without a verdict.</td></tr>
                )}
                {run.criteria.map((c) => (
                  <tr key={c.id} className={c.passed ? "ok" : "bad"}>
                    <td title={c.limit_parameters.length ? `limit from ${c.limit_parameters.join(", ")}` : c.source}>
                      {c.label}{c.source === "user" && <span className="source">requirement</span>}
                    </td>
                    <td>{fmt(c.measured, c.unit)}</td>
                    <td>{c.comparator} {fmt(c.limit, c.unit)}</td>
                    <td>{fmt(c.margin, c.unit)}</td>
                    <td>{c.passed ? "pass" : "fail"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="compare-bar">
              Compare with{" "}
              <select value={baselineChoice || comparison?.baseline || ""}
                onChange={(e) => setBaselineChoice(e.target.value)}>
                <option value="">—</option>
                {peers.map((p) => <option key={p.id} value={p.id}>revision {p.history_cursor} ({STATUS_SHORT[p.status]})</option>)}
              </select>
              {comparison && <span className="hint"> {comparison.summary}</span>}
            </div>
            {comparison && Object.keys(comparison.changed_inputs).length > 0 && (
              <div className="hint">Changed: {Object.entries(comparison.changed_inputs).map(([p, v]) =>
                `${p} ${fmt(v.before)} → ${fmt(v.after)} ${v.unit}`).join("; ")}</div>
            )}
            <TraceCharts run={run} baseline={baseline} />
            <table className="metrics">
              <thead><tr><th>Metric</th><th>{comparison ? "Before" : ""}</th><th>Value</th><th>{comparison ? "Change" : ""}</th></tr></thead>
              <tbody>
                {Object.entries(run.metrics).map(([id, m]) => {
                  const d = comparison?.metrics.find((x) => x.metric === id);
                  return (
                    <tr key={id} className={d?.verdict ?? ""}>
                      <td>{m.label}</td>
                      <td>{d ? fmt(d.before, m.unit) : ""}</td>
                      <td>{fmt(m.value, m.unit)}</td>
                      <td>{d && d.percent !== null ? `${d.percent > 0 ? "+" : ""}${fmt(d.percent)} % ${d.verdict}` : ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <details>
              <summary>Model assumptions and inputs</summary>
              <ul>{run.assumptions.map((a) => <li key={a}>{a}</li>)}</ul>
              <ul className="inputs">
                {Object.entries(run.inputs).map(([p, v]) => <li key={p}>{v.label}: {fmt(v.value, v.unit)}</li>)}
              </ul>
            </details>
          </>
        )}
      </div>
    </div>
  );
}
