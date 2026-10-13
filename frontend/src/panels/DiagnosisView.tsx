import type { Command, Diagnosis } from "../api/types";
import { fmt } from "../state/engineering";

interface Props {
  diagnosis: Diagnosis;
  busy: boolean;
  onApply: (command: Command) => void;
}

const EVIDENCE: Record<string, string> = {
  confirmed_in_model: "measured", possible: "small", none: "no effect",
};

/** Findings with their evidence. Effects come from re-simulation, not from the language model. */
export function DiagnosisView({ diagnosis, busy, onApply }: Props) {
  return (
    <div className="diagnosis">
      {!diagnosis.current && (
        <div className="warnings">This run is from an earlier design; rerun the test before acting.</div>
      )}
      {diagnosis.findings.map((f) => (
        <div key={f.criterion} className="finding">
          <p><span className={`status-pill ${f.status === "failed" ? "failed" : "warning"}`}>
            {f.status === "failed" ? "failed" : "tightest margin"}</span>{f.explanation}</p>
          <table>
            <thead><tr><th>Parameter</th><th>Now</th><th>+10 %</th><th>−10 %</th><th>Evidence</th><th>Side effects</th></tr></thead>
            <tbody>
              {f.effects.filter((e) => e.evidence !== "none").slice(0, 8).map((e) => (
                <tr key={e.parameter} className={e.parameter === f.governing_parameter ? "governing" : ""}>
                  <td title={e.parameter}>{e.label}{e.parameter === f.governing_parameter && <span className="source">sets the limit</span>}</td>
                  <td>{fmt(e.value, e.unit)}</td>
                  <td className={(e.margin_up ?? 0) > 0 ? "better" : (e.margin_up ?? 0) < 0 ? "worse" : ""}>{fmt(e.margin_up)}</td>
                  <td className={(e.margin_down ?? 0) > 0 ? "better" : (e.margin_down ?? 0) < 0 ? "worse" : ""}>{fmt(e.margin_down)}</td>
                  <td>{EVIDENCE[e.evidence]}</td>
                  <td>{e.side_effects.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {f.fixes.length > 0 && (
            <ul className="fixes">
              {f.fixes.map((x) => (
                <li key={x.parameter}>
                  {x.operation} {x.label.toLowerCase()} {fmt(x.from_value, x.unit)} → {fmt(x.to_value, x.unit)} ({x.step_percent} %),
                  margin after {fmt(x.margin_after, f.unit)}
                  {x.breaks.length > 0 && <span className="bad-text"> · breaks {x.breaks.join(", ")}</span>}
                  {x.rule_violations.length > 0 && <span className="bad-text"> · rule: {x.rule_violations[0]}</span>}
                  {" "}
                  <button disabled={busy || x.rule_violations.length > 0} onClick={() => onApply(x.command)}>
                    Apply
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
      <p className="hint">{diagnosis.recommendation} Evidence: {String(diagnosis.evidence.perturbation_runs)} re-simulations, {String(diagnosis.evidence.step)}.</p>
      <details><summary>Caveats</summary><ul>{diagnosis.caveats.map((c) => <li key={c}>{c}</li>)}</ul></details>
    </div>
  );
}
