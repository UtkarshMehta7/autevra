import { useEffect, useState } from "react";
import { api } from "../api/client";

/** Loads workspace (every module): the module's load cases computed from the design, the
 * aircraft V-n envelope, the compliance matrix (regulation clause references with our own
 * wording, means, evidence and status) and the materials database with the basis of each
 * value (backend product/loads.py, modules/<id>/loads.py, materials.py). */

interface LoadAt { location: string; fx: number; fy: number; fz: number; mx: number; my: number; mz: number }
interface Case { id: string; name: string; kind: string; method: string; factors: Record<string, number>; loads: LoadAt[]; results: Record<string, number> }
interface Row { clause: string; requirement: string; means: string; evidence: string; status: "shown" | "not shown" | "open" }
interface Envelope { n_pos: number; n_neg: number; vs: number; va: number; vc: number; vd: number; gust_vc: number[]; gust_vd: number[]; stall_line: [number, number][]; category: string }
interface Material { id: string; name: string; family: string; density: number; youngs_modulus_gpa: number; yield_mpa: number; ultimate_mpa: number; basis: string; source: string; fatigue_mpa: number }

const KN = 1.943844;
const fmt = (v: number) => (Math.abs(v) >= 1000 ? `${(v / 1000).toFixed(1)} k` : v.toFixed(Math.abs(v) >= 10 ? 0 : 2));

function VnDiagram({ e }: { e: Envelope }) {
  const w = 460, h = 240, pad = 36;
  const vMax = e.vd * 1.08, nMax = Math.max(e.n_pos, e.gust_vc[0]) + 0.6, nMin = Math.min(e.n_neg, e.gust_vc[1]) - 0.6;
  const x = (v: number) => pad + (v / vMax) * (w - 2 * pad);
  const y = (n: number) => pad + ((nMax - n) / (nMax - nMin)) * (h - 2 * pad);
  const pos = [...e.stall_line.map(([v, n]) => [v, n]), [e.va, e.n_pos], [e.vd, e.n_pos], [e.vd, 0]];
  const negV = e.vs * Math.sqrt(-e.n_neg);
  const neg: number[][] = [];
  for (let v = e.vs; v <= negV; v += (negV - e.vs) / 12) neg.push([v, -((v / e.vs) ** 2)]); // same |C_L,max| (simplified)
  neg.push([negV, e.n_neg], [e.vc, e.n_neg], [e.vd, 0]);
  const line = (pts: number[][]) => pts.map(([v, n], i) => `${i ? "L" : "M"}${x(v).toFixed(1)},${y(n).toFixed(1)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="vn" role="img" aria-label="V-n diagram">
      <line x1={pad} y1={y(0)} x2={w - pad} y2={y(0)} className="axis" />
      <line x1={pad} y1={pad} x2={pad} y2={h - pad} className="axis" />
      {[nMin, 0, 1, e.n_pos].map((n) => <text key={n} x={pad - 4} y={y(n) + 3} textAnchor="end">{n.toFixed(1)}</text>)}
      {[e.vs, e.va, e.vc, e.vd].map((v, i) => (
        <g key={i}><line x1={x(v)} y1={y(0) - 3} x2={x(v)} y2={y(0) + 3} className="axis" />
          <text x={x(v)} y={h - pad + 14} textAnchor="middle">{["V_S", "V_A", "V_C", "V_D"][i]} {(v * KN).toFixed(0)}</text></g>
      ))}
      <path d={line(pos)} className="env" />
      <path d={line(neg)} className="env" />
      {[[e.vc, e.gust_vc], [e.vd, e.gust_vd]].map(([v, g], i) => (
        <g key={i}>
          <line x1={x(0)} y1={y(1)} x2={x(v as number)} y2={y((g as number[])[0])} className="gust" />
          <line x1={x(0)} y1={y(1)} x2={x(v as number)} y2={y((g as number[])[1])} className="gust" />
        </g>
      ))}
      <text x={w - pad} y={pad - 8} textAnchor="end">{e.category} category · speeds in kn (EAS) · dashed: gust lines</text>
    </svg>
  );
}

export function LoadsPanel({ projectId, version }: { projectId: string; version?: number }) {
  const [out, setOut] = useState<{ module: string; cases: Case[]; compliance: Row[]; envelope?: Envelope } | null>(null);
  const [mats, setMats] = useState<Material[]>([]);
  const [tab, setTab] = useState<"cases" | "compliance" | "materials">("cases");
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api.projectLoads(projectId).then((r) => { setOut(r as never); setError(null); })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)));
    api.materials().then((m) => setMats(m as never)).catch(() => undefined);
  }, [projectId, version]);
  if (!out) return <div className="bench wide">{error ?? "Computing the load cases…"}</div>;
  const shown = out.compliance.filter((r) => r.status === "shown").length;
  return (
    <div className="loads">
      <div className="bench-controls">
        <button className={tab === "cases" ? "active" : ""} onClick={() => setTab("cases")}>Load cases ({out.cases.length})</button>
        <button className={tab === "compliance" ? "active" : ""} onClick={() => setTab("compliance")}>Compliance ({shown}/{out.compliance.length} shown)</button>
        <button className={tab === "materials" ? "active" : ""} onClick={() => setTab("materials")}>Materials ({mats.length})</button>
      </div>
      {tab === "cases" && (
        <div className="loads-grid">
          {out.envelope && <section><h4>Flight envelope (V-n)</h4><VnDiagram e={out.envelope} /></section>}
          <section>
            {out.cases.map((c) => (
              <div key={c.id} className="case">
                <b>{c.name}</b> <span className="muted small">{c.kind} · {Object.entries(c.factors).map(([k, v]) => `${k} ${v}`).join(", ")}</span>
                <div className="muted small">{c.method}</div>
                <table><tbody>
                  {c.loads.map((l, i) => (
                    <tr key={i}><td>{l.location}</td>
                      <td className="num">{l.fx ? `Fx ${fmt(l.fx)}N` : ""}</td><td className="num">{l.fy ? `Fy ${fmt(l.fy)}N` : ""}</td>
                      <td className="num">{l.fz ? `Fz ${fmt(l.fz)}N` : ""}</td><td className="num">{l.mx ? `Mx ${fmt(l.mx)}N·m` : ""}</td></tr>
                  ))}
                </tbody></table>
                {Object.keys(c.results).length > 0 && (
                  <div className="small">{Object.entries(c.results).map(([k, v]) => <span key={k} className="res">{k.replace(/_/g, " ")}: <b>{fmt(v)}</b></span>)}</div>
                )}
              </div>
            ))}
          </section>
        </div>
      )}
      {tab === "compliance" && (
        <>
          <p className="muted small">Clause references with our own wording of what must be shown. Autevra supports compliance work; it does not certify.</p>
          <table className="bd-table"><thead><tr><th>Clause</th><th>Requirement</th><th>Means</th><th>Evidence</th><th>Status</th></tr></thead>
            <tbody>{out.compliance.map((r) => (
              <tr key={r.clause}><td>{r.clause}</td><td>{r.requirement}</td><td>{r.means}</td><td className="muted">{r.evidence}</td>
                <td><span className={`status ${r.status.replace(" ", "-")}`}>{r.status}</span></td></tr>
            ))}</tbody></table>
        </>
      )}
      {tab === "materials" && (
        <table className="bd-table"><thead><tr><th>Material</th><th className="num">ρ kg/m³</th><th className="num">E GPa</th><th className="num">Rp0.2 MPa</th><th className="num">Rm MPa</th><th className="num">fatigue MPa</th><th>Basis</th><th>Source</th></tr></thead>
          <tbody>{mats.map((m) => (
            <tr key={m.id}><td>{m.name}</td><td className="num">{m.density}</td><td className="num">{m.youngs_modulus_gpa}</td>
              <td className="num">{m.yield_mpa || "—"}</td><td className="num">{m.ultimate_mpa}</td><td className="num">{m.fatigue_mpa}</td>
              <td><span className={`status ${m.basis === "minimum" ? "shown" : "open"}`}>{m.basis}</span></td><td className="muted">{m.source}</td></tr>
          ))}</tbody></table>
      )}
    </div>
  );
}
