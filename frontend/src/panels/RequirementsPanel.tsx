import { Fragment, useMemo, useState } from "react";
import type {
  Comparator, DerivedValue, ParameterDef, Requirement, RequirementRow, TestDefinition,
} from "../api/types";
import { fmt } from "../state/engineering";

interface Props {
  rows: RequirementRow[];
  parameters: ParameterDef[];
  derived: DerivedValue[];
  test: TestDefinition | undefined;
  reqifUrl: string;
  busy: boolean;
  onAdd: (body: Partial<Requirement>) => void;
  onUpdate: (id: string, body: Partial<Requirement>) => void;
  onDelete: (id: string) => void;
  onVerify: () => void;
  onImport: (xml: string) => void;
}

const STATUS_CLASS: Record<string, string> = {
  verified: "passed_within_model", failed: "failed", stale: "stale", not_verified: "",
  not_approved: "", manual: "",
};

export function RequirementsPanel({ rows, parameters, derived, test, reqifUrl, busy, onAdd, onUpdate, onDelete, onVerify, onImport }: Props) {
  const [kind, setKind] = useState<Requirement["kind"]>("design");
  const [quantity, setQuantity] = useState("ground_clearance");
  const [metric, setMetric] = useState("peak_body_acceleration");
  const [target, setTarget] = useState("*");
  const [scenario, setScenario] = useState("*");
  const [comparator, setComparator] = useState<Comparator>(">=");
  const [limit, setLimit] = useState("150");
  const [text, setText] = useState("");
  const [priority, setPriority] = useState<Requirement["priority"]>("must");
  const [open, setOpen] = useState<string | null>(null);

  const quantities = useMemo(() => [
    ...parameters.map((p) => ({ id: p.id, label: p.label, unit: p.unit as string })),
    ...derived.map((d) => ({ id: d.id, label: `${d.label} (derived)`, unit: d.unit })),
  ], [parameters, derived]);
  const unit = kind === "design" ? quantities.find((q) => q.id === quantity)?.unit ?? ""
    : kind === "performance" ? test?.metrics[metric]?.unit ?? "" : "";
  const counts = rows.reduce<Record<string, number>>((acc, r) => {
    acc[r.verification.status] = (acc[r.verification.status] ?? 0) + 1;
    return acc;
  }, {});

  const add = () => {
    const base = { kind, priority, comparator, limit: Number(limit) };
    if (kind === "design") onAdd({ ...base, quantity, unit });
    else if (kind === "performance") onAdd({ ...base, test_id: "quarter_car", metric, target, scenario_id: scenario });
    else onAdd({ kind, priority, text, verification: "inspection" });
  };

  const importFile = (file: File | undefined) => {
    if (file) file.text().then(onImport);
  };

  return (
    <div className="bench wide">
      <div className="bench-side">
        <div className="bench-controls">
          <select value={kind} onChange={(e) => setKind(e.target.value as Requirement["kind"])}>
            <option value="design">design (analysis)</option>
            <option value="performance">performance (test)</option>
            <option value="text">text (manual)</option>
          </select>
          <select value={priority} onChange={(e) => setPriority(e.target.value as Requirement["priority"])}>
            <option value="must">must</option><option value="should">should</option><option value="may">may</option>
          </select>
        </div>
        {kind === "design" && (
          <div className="bench-controls">
            <select value={quantity} onChange={(e) => setQuantity(e.target.value)}>
              {quantities.map((q) => <option key={q.id} value={q.id}>{q.label}</option>)}
            </select>
          </div>
        )}
        {kind === "performance" && test && (
          <div className="bench-controls">
            <select value={metric} onChange={(e) => setMetric(e.target.value)}>
              {Object.entries(test.metrics).map(([id, m]) => <option key={id} value={id}>{m.label}</option>)}
            </select>
            <select value={target} onChange={(e) => setTarget(e.target.value)}>
              <option value="*">each corner</option>
              {test.targets.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
            <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
              <option value="*">every scenario</option>
              {test.scenarios.map((s) => <option key={s.id} value={s.id}>{s.label}</option>)}
            </select>
          </div>
        )}
        {kind === "text" ? (
          <textarea className="statement" value={text} placeholder="The requirement statement"
            onChange={(e) => setText(e.target.value)} />
        ) : (
          <div className="bench-controls">
            <select value={comparator} onChange={(e) => setComparator(e.target.value as Comparator)}>
              <option value=">=">at least</option><option value="<=">at most</option>
              <option value=">">above</option><option value="<">below</option>
            </select>
            <input className="narrow" type="number" value={limit} onChange={(e) => setLimit(e.target.value)} />
            <span>{unit}</span>
          </div>
        )}
        <div className="bench-controls">
          <button className="primary" disabled={busy || (kind === "text" && !text.trim())} onClick={add}>Add requirement</button>
          <button disabled={busy || rows.length === 0} onClick={onVerify} title="Runs the tests that are missing or stale">Verify all</button>
        </div>
        <div className="bench-controls">
          <a className="button" href={reqifUrl}>Export ReqIF</a>
          <label className="button">Import ReqIF
            <input type="file" accept=".reqif,.xml" hidden onChange={(e) => importFile(e.target.files?.[0])} />
          </label>
        </div>
        <p className="hint">
          {(Object.entries(counts).map(([k, n]) => `${n} ${k.replace(/_/g, " ")}`).join(" · ") || "No requirements yet") + ". "}
          Statuses describe the model; they are evidence, not a compliance claim.
        </p>
      </div>
      <div className="bench-detail">
        <table className="requirements">
          <thead><tr><th>Key</th><th>Requirement</th><th>Verified by</th><th>Status</th><th /></tr></thead>
          <tbody>
            {rows.map((r) => (
              <Fragment key={r.requirement.id}>
                <tr className="req-row" onClick={() => setOpen(open === r.requirement.id ? null : r.requirement.id)}>
                  <td>{r.requirement.key}<br /><small className="hint">{r.requirement.priority}</small></td>
                  <td>{r.requirement.text}{r.requirement.source === "reqif" && <span className="source">ReqIF</span>}</td>
                  <td>{r.requirement.verification}</td>
                  <td><span className={`status-pill ${STATUS_CLASS[r.verification.status] ?? ""}`}>{r.verification.status.replace(/_/g, " ")}</span></td>
                  <td>
                    <button onClick={(e) => { e.stopPropagation(); onUpdate(r.requirement.id, { approved: !r.requirement.approved }); }}
                      disabled={busy}>{r.requirement.approved ? "Unapprove" : "Approve"}</button>
                    <button onClick={(e) => { e.stopPropagation(); onDelete(r.requirement.id); }} disabled={busy}>Delete</button>
                  </td>
                </tr>
                {open === r.requirement.id && (
                  <tr className="trace"><td colSpan={5}>
                    <div><strong>Evidence</strong> — {r.verification.summary}</div>
                    <ul>{r.verification.evidence.map((e, i) => (
                      <li key={i}><span className={`status-pill ${e.status === "pass" ? "pass" : e.status === "fail" ? "fail" : "stale"}`}>{e.status}</span>
                        {e.detail}{e.measured !== null && e.limit !== null ? ` (limit ${fmt(e.limit, e.unit)})` : ""}
                        {e.design_revision !== null ? ` · revision ${e.design_revision}` : ""}</li>
                    ))}</ul>
                    <div><strong>Parameters</strong>: {r.parameters.join(", ") || "—"}</div>
                    <div><strong>Components</strong>: {r.components.join(", ") || "—"}</div>
                    <div><strong>Test cases</strong>: {r.cases.join(", ") || "—"}</div>
                  </td></tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
