import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";

/** Reviews workspace (every module): review gates computed from the model, baselines with
 * comparison against the current design, and engineering change requests whose impact is
 * computed before approval; an approved change applies through the design's own path
 * (backend api/change.py). */

interface Gate { gate: string; passed: boolean; criteria: { criterion: string; met: boolean; detail: string }[] }
interface Baseline { id: string; name: string; gate: string; created_at: string; mass_kg: number }
interface Impact { values: Record<string, [unknown, unknown]>; mass_kg: number; cg_x_m: number; unit_cost_eur: number; co2_kg: number; checks: Record<string, [string, string]>; compliance: Record<string, [string, string]> }
interface ChangeReq { id: string; title: string; reason: string; changes: Record<string, unknown>; status: string; impact: Impact; eco?: string }

function ImpactView({ i }: { i: Impact }) {
  const sign = (v: number, unit: string, d = 1) => `${v > 0 ? "+" : ""}${v.toFixed(d)} ${unit}`;
  return (
    <div className="impact small">
      {Object.entries(i.values).map(([k, [a, b]]) => <span key={k}>{k}: {String(a)} → <b>{String(b)}</b></span>)}
      <span>mass <b>{sign(i.mass_kg, "kg")}</b></span><span>CG x <b>{sign(i.cg_x_m * 1000, "mm", 0)}</b></span>
      <span>unit cost <b>{sign(i.unit_cost_eur, "€", 0)}</b></span><span>CO₂ <b>{sign(i.co2_kg, "kg", 0)}</b></span>
      {Object.entries(i.checks).map(([k, [a, b]]) => <span key={k} className={b === "fail" ? "bad" : ""}>check {k}: {a} → {b}</span>)}
      {Object.entries(i.compliance).map(([k, [a, b]]) => <span key={k}>{k}: {a} → {b}</span>)}
    </div>
  );
}

export function ReviewsPanel({ projectId, version, onModelChanged }: { projectId: string; version?: number; onModelChanged: () => void }) {
  const [gates, setGates] = useState<Gate[]>([]);
  const [baselines, setBaselines] = useState<Baseline[]>([]);
  const [changes, setChanges] = useState<ChangeReq[]>([]);
  const [diff, setDiff] = useState<(Impact & { baseline: string }) | null>(null);
  const [form, setForm] = useState({ title: "", key: "", value: "" });
  const [blName, setBlName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const load = useCallback(() => {
    api.reviews(projectId).then((g) => setGates(g as Gate[])).catch((e) => setError(String(e.message ?? e)));
    api.baselines(projectId).then((b) => setBaselines(b as Baseline[])).catch(() => undefined);
    api.changes(projectId).then((c) => setChanges(c as ChangeReq[])).catch(() => undefined);
  }, [projectId]);
  useEffect(() => { load(); }, [load, version]);
  const act = async (f: () => Promise<unknown>) => {
    try { await f(); setError(null); load(); } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
  };
  const parsed = () => (form.value === "true" || form.value === "false" ? form.value === "true"
    : Number.isNaN(Number(form.value)) ? form.value : Number(form.value));
  return (
    <div className="reviews">
      <div className="gates">
        {gates.map((g) => (
          <div key={g.gate} className={`gate ${g.passed ? "ok" : ""}`}>
            <b>{g.passed ? "✓" : "○"} {g.gate}</b>
            {g.criteria.map((c) => (
              <div key={c.criterion} className={`crit ${c.met ? "met" : "unmet"}`} title={c.detail}>
                {c.met ? "✓" : "✗"} {c.criterion}<span className="muted"> — {c.detail}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
      <div className="rev-grid">
        <section>
          <h4>Baselines</h4>
          <div className="row">
            <input placeholder="name, e.g. Concept freeze" value={blName} onChange={(e) => setBlName(e.target.value)} />
            <button disabled={!blName.trim()} onClick={() => act(async () => {
              const passed = gates.filter((g) => g.passed);  // the latest gate the design has passed
              await api.takeBaseline(projectId, blName.trim(), passed.length ? passed[passed.length - 1].gate : "none");
              setBlName("");
            })}>Take baseline</button>
          </div>
          {baselines.map((b) => (
            <div key={b.id} className="bl">
              <b>{b.id}</b> {b.name} <span className="muted small">{b.gate !== "none" ? b.gate + " · " : ""}{new Date(b.created_at).toLocaleString()} · {b.mass_kg.toFixed(0)} kg</span>
              <button onClick={() => act(async () => setDiff((await api.compareBaseline(projectId, b.id)) as never))}>Compare with now</button>
            </div>
          ))}
          {diff && <div className="diff"><b>Since {diff.baseline}</b><ImpactView i={diff} /></div>}
        </section>
        <section>
          <h4>Engineering change requests</h4>
          <div className="row">
            <input placeholder="title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            <input placeholder="value, e.g. wheelbase" value={form.key} onChange={(e) => setForm({ ...form, key: e.target.value })} />
            <input placeholder="new value" value={form.value} onChange={(e) => setForm({ ...form, value: e.target.value })} />
            <button disabled={!form.title || !form.key || form.value === ""} onClick={() => act(async () => {
              await api.requestChange(projectId, form.title, { [form.key]: parsed() });
              setForm({ title: "", key: "", value: "" });
            })}>Raise ECR (impact first)</button>
          </div>
          {[...changes].reverse().map((c) => (
            <div key={c.id} className={`ecr ${c.status}`}>
              <b>{c.id}</b> {c.title} <span className={`status ${c.status === "approved" ? "shown" : c.status === "rejected" ? "not-shown" : "open"}`}>{c.status}{c.eco ? ` as ${c.eco}` : ""}</span>
              <ImpactView i={c.impact} />
              {c.status === "open" && (
                <div className="row">
                  <button onClick={() => act(async () => { await api.decideChange(projectId, c.id, "approve"); onModelChanged(); })}>Approve (ECO)</button>
                  <button onClick={() => act(() => api.decideChange(projectId, c.id, "reject"))}>Reject</button>
                </div>
              )}
            </div>
          ))}
        </section>
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
