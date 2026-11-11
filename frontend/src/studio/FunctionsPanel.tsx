import { useEffect, useMemo, useState, type ReactElement } from "react";
import { api } from "../api/client";
import type { ChainStep, FlowKind, SysFunction, SystemsOut } from "../api/types";

/** Functions workspace: requirements → functions → logical blocks → parts. A function's
 * chain shows the blocks that perform it in flow order, the typed flows between them and
 * the parts that realise each block; interface rows, design FMEA and the allocation gaps
 * between the layers sit beside it (backend product/systems.py). */

const KIND_LABEL: Record<FlowKind, string> = {
  mechanical: "mechanical", electrical_power: "electrical power", signal: "signal", fluid: "fluid", thermal: "thermal",
};
const LEVELS = ["L0", "L1", "L2", "L3", "L4"];

function ChainDiagram({ steps }: { steps: ChainStep[] }) {
  const w = 150, h = 54, gap = 46, pad = 10;
  const width = pad * 2 + steps.length * w + (steps.length - 1) * gap;
  const x = (i: number) => pad + i * (w + gap);
  const index = new Map(steps.map((s, i) => [s.block, i]));
  const arrows = steps.flatMap((s, i) => s.flows_out.map((f) => ({ f, from: i, to: index.get(f.target) ?? -1 })))
    .filter((a) => a.to >= 0);
  return (
    <svg className="chain" viewBox={`0 0 ${width} ${h + 2 * pad + 70}`} width={width} role="img" aria-label="Function chain">
      <defs>
        {(["mechanical", "electrical_power", "signal", "fluid", "thermal"] as FlowKind[]).map((k) => (
          <marker key={k} id={`arr-${k}`} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className={`flow-${k}`} />
          </marker>
        ))}
      </defs>
      {arrows.map(({ f, from, to }, k) => {
        const y = pad + h / 2;
        if (to === from + 1) {
          return (
            <g key={f.id}>
              <line x1={x(from) + w} y1={y} x2={x(to)} y2={y} className={`flow-line flow-${f.kind}`} markerEnd={`url(#arr-${f.kind})`} />
              <title>{`${f.item} (${KIND_LABEL[f.kind]})`}</title>
            </g>
          );
        }
        // longer or backward flows arc below the boxes
        const x1 = x(from) + w / 2, x2 = x(to) + w / 2, depth = 18 + (k % 4) * 12;
        return (
          <g key={f.id}>
            <path d={`M${x1},${pad + h} C${x1},${pad + h + depth * 2} ${x2},${pad + h + depth * 2} ${x2},${pad + h}`}
              className={`flow-line flow-${f.kind}`} fill="none" markerEnd={`url(#arr-${f.kind})`} />
            <title>{`${f.item} (${KIND_LABEL[f.kind]})`}</title>
          </g>
        );
      })}
      {steps.map((s, i) => (
        <g key={s.block} transform={`translate(${x(i)},${pad})`}>
          <rect width={w} height={h} rx={6} className={s.external ? "blk ext" : "blk"} />
          <text x={w / 2} y={22} textAnchor="middle" className="blk-name">{s.name.length > 24 ? `${s.name.slice(0, 23)}…` : s.name}</text>
          <text x={w / 2} y={40} textAnchor="middle" className="blk-sub">
            {s.external ? "outside the product" : `${s.parts.length} part type${s.parts.length === 1 ? "" : "s"}`}
          </text>
        </g>
      ))}
    </svg>
  );
}

export function FunctionsPanel({ projectId, version }: { projectId: string; version?: number }) {
  const [out, setOut] = useState<SystemsOut | null>(null);
  const [fn, setFn] = useState<string | null>(null);
  const [steps, setSteps] = useState<ChainStep[] | null>(null);
  const [tab, setTab] = useState<"chain" | "icd" | "fmea">("chain");
  const [error, setError] = useState<string | null>(null);

  const load = () => api.systems(projectId).then((r) => { setOut(r); setError(null); })
    .catch((e) => setError(e instanceof Error ? e.message : String(e)));
  useEffect(() => { load(); }, [projectId, version]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!out) return;
    const first = fn ?? out.functions.find((f) => f.id === "decelerate" || f.id === "control_pitch")?.id ?? out.functions[0]?.id;
    if (!first) return;
    if (first !== fn) setFn(first);
    api.systemChain(projectId, first).then(setSteps).catch((e) => setError(String(e.message ?? e)));
  }, [out, fn, projectId]);

  const performers = useMemo(() => {
    const m = new Map<string, number>();
    out?.blocks.forEach((b) => b.functions.forEach((f) => m.set(f, (m.get(f) ?? 0) + 1)));
    return m;
  }, [out]);

  if (!out) return <div className="bench wide">{error ?? "Loading the architecture…"}</div>;
  const children = (pid: string) => out.functions.filter((f) => f.parent === pid);
  const fails = out.issues.filter((i) => i.severity === "fail");
  const warns = out.issues.filter((i) => i.severity === "warn");
  const name = (bid: string) => out.blocks.find((b) => b.id === bid)?.name ?? bid;
  const fnName = (fid: string) => out.functions.find((f) => f.id === fid)?.name ?? fid;

  const tree = (f: SysFunction, depth: number): ReactElement => {
    const kids = children(f.id);
    const n = performers.get(f.id) ?? 0;
    const ok = n > 0 || kids.length > 0;
    return (
      <div key={f.id}>
        <button className={`fn-row${fn === f.id ? " active" : ""}`} style={{ paddingLeft: 6 + depth * 14 }} onClick={() => setFn(f.id)}>
          <span className={ok ? "dot good" : "dot bad"} />{f.name}
          <span className="muted small"> {kids.length ? "" : `${n} block${n === 1 ? "" : "s"}`}{f.requirements.length ? ` · ${f.requirements.join(", ")}` : ""}</span>
        </button>
        {kids.map((k) => tree(k, depth + 1))}
      </div>
    );
  };

  return (
    <div className="bench wide functions">
      <div className="bench-side">
        <h4>Functions</h4>
        <div className="fn-tree">{out.functions.filter((f) => !f.parent).map((f) => tree(f, 0))}</div>
        <h4>Trace</h4>
        {fails.length === 0 && warns.length === 0 && <div className="check pass"><span className="badge">pass</span>Every function performed, every block realised by parts, every requirement allocated.</div>}
        {[...fails, ...warns].map((i) => (
          <div key={`${i.kind}-${i.subject}`} className={`check ${i.severity}`}><span className="badge">{i.kind.replace(/_/g, " ")}</span>{i.message}</div>
        ))}
        <h4>Requirements → functions</h4>
        {out.requirements.length === 0 && <p className="muted small">No requirements in this project yet (Requirements workspace, or ReqIF import).</p>}
        {out.requirements.map((r) => (
          <label key={r.key} className="req-alloc" title={r.text}>
            <span><b>{r.key}</b> <span className="muted">{r.text}</span></span>
            <select value={r.function} onChange={(e) => api.allocate(projectId, r.key, e.target.value).then(load)}>
              <option value="">not allocated</option>
              {out.functions.map((f) => <option key={f.id} value={f.id}>{f.parent ? "  " : ""}{f.name}</option>)}
            </select>
          </label>
        ))}
        {error && <p className="error">{error}</p>}
      </div>
      <div className="bench-detail">
        <div className="bench-controls">
          <button className={tab === "chain" ? "active" : ""} onClick={() => setTab("chain")}>Function chain</button>
          <button className={tab === "icd" ? "active" : ""} onClick={() => setTab("icd")}>Interfaces ({out.icd.length})</button>
          <button className={tab === "fmea" ? "active" : ""} onClick={() => setTab("fmea")}>Design FMEA ({out.failure_modes.length})</button>
          <span className="legend">
            {(Object.keys(KIND_LABEL) as FlowKind[]).map((k) => <span key={k}><i className={`flow-${k}`} />{KIND_LABEL[k]}</span>)}
          </span>
        </div>
        {tab === "chain" && fn && (
          <div>
            <h3 className="fn-title">{fnName(fn)}</h3>
            {steps && steps.length > 0 ? (
              <>
                <div className="chain-wrap"><ChainDiagram steps={steps} /></div>
                <table className="bd-table">
                  <thead><tr><th>Block</th><th>Flows out</th><th>Parts (mass, level)</th></tr></thead>
                  <tbody>
                    {steps.map((s) => (
                      <tr key={s.block}>
                        <td><b>{s.name}</b>{s.external && <span className="bd-tag">outside</span>}</td>
                        <td>{s.flows_out.map((f) => <div key={f.id}><i className={`kind-dot flow-${f.kind}`} />{f.item} → {name(f.target)}</div>)}</td>
                        <td>{s.parts.map((p) => <div key={p.id}>{p.name}{p.instances > 1 ? ` ×${p.instances}` : ""} <span className="muted">{p.mass.toFixed(1)} kg</span> <span className={`mat-chip mat-${p.maturity}`}>{LEVELS[p.maturity]}</span></div>)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </>
            ) : <p className="muted">No block performs this function yet.</p>}
          </div>
        )}
        {tab === "icd" && (
          <table className="bd-table">
            <thead><tr><th>From</th><th>To</th><th>Kind</th><th>Item</th><th>Agreed values</th></tr></thead>
            <tbody>{out.icd.map((r) => (
              <tr key={r.flow}><td>{r.source}</td><td>{r.target}</td><td><i className={`kind-dot flow-${r.kind}`} />{KIND_LABEL[r.kind]}</td><td>{r.item}</td>
                <td className="muted">{Object.entries(r.attributes).map(([k, v]) => `${k}: ${v}`).join(" · ")}</td></tr>
            ))}</tbody>
          </table>
        )}
        {tab === "fmea" && (
          <>
            <p className="muted small">Ratings are review starting values. Priority is a stated simplification (high: severity 9–10 with occurrence ≥ 4 or detection ≥ 7, or RPN ≥ 200), not the AIAG-VDA table.</p>
            <table className="bd-table">
              <thead><tr><th>Function</th><th>Block</th><th>Failure mode</th><th>Effect</th><th className="num">S</th><th className="num">O</th><th className="num">D</th><th className="num">RPN</th><th>Priority</th><th>Action</th></tr></thead>
              <tbody>{out.failure_modes.map((m) => (
                <tr key={m.id}><td>{fnName(m.function)}</td><td>{name(m.block)}</td><td>{m.mode}</td><td className="muted">{m.effect}</td>
                  <td className="num">{m.severity}</td><td className="num">{m.occurrence}</td><td className="num">{m.detection}</td><td className="num">{m.rpn}</td>
                  <td><span className={`prio ${m.priority}`}>{m.priority}</span></td><td className="muted">{m.action || "—"}</td></tr>
              ))}</tbody>
            </table>
          </>
        )}
      </div>
    </div>
  );
}
