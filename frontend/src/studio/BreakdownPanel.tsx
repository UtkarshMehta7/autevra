import { Fragment, useEffect, useMemo, useState, type ReactElement } from "react";
import { api } from "../api/client";
import type { BreakdownNode, ProductEnvelope, ProductOut } from "../api/types";

/** Breakdown workspace: the whole product as systems, subsystems and parts (every part
 * present from day one at level 0), with mass and CG roll-ups, a maturity heat map, the
 * checks against the product model, and a configuration filter over the product's options
 * (backend product/ and modules/). Viewing another configuration never changes the design. */

const LEVEL_SHORT = ["L0", "L1", "L2", "L3", "L4"];

function kg(m: number): string {
  return m >= 100 ? m.toFixed(0) : m >= 10 ? m.toFixed(1) : m.toFixed(2);
}

function MaturityBar({ counts, levels }: { counts: number[]; levels: string[] }) {
  const total = counts.reduce((a, b) => a + b, 0) || 1;
  return (
    <div>
      <div className="mat-bar" role="img" aria-label="Parts per maturity level">
        {counts.map((c, i) => c > 0 && (
          <span key={i} className={`mat-${i}`} style={{ width: `${(100 * c) / total}%` }}
            title={`${levels[i]}: ${c} parts`} />
        ))}
      </div>
      <div className="mat-legend">
        {counts.map((c, i) => (
          <span key={i}><i className={`mat-${i}`} />{levels[i]} <b>{c}</b></span>
        ))}
      </div>
    </div>
  );
}

export function BreakdownPanel({ projectId, version }: { projectId: string; version?: number }) {
  const [out, setOut] = useState<ProductOut | null>(null);
  const [override, setOverride] = useState<Record<string, string>>({});
  const [open, setOpen] = useState<Set<string>>(new Set());
  const [selected, setSelected] = useState<string | null>(null);
  const [envelope, setEnvelope] = useState<ProductEnvelope | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let live = true;
    api.product(projectId, override)
      .then((r) => {
        if (!live) return;
        setOut(r); setError(null);
        setOpen((prev) => (prev.size ? prev : new Set([r.breakdown.id])));
      })
      .catch((e) => live && setError(e instanceof Error ? e.message : String(e)));
    return () => { live = false; };
  }, [projectId, override, version]);
  useEffect(() => setEnvelope(null), [projectId, version]);

  const byId = useMemo(() => {
    const map = new Map<string, BreakdownNode>();
    const walk = (n: BreakdownNode) => { map.set(n.id, n); n.children.forEach(walk); };
    if (out) walk(out.breakdown);
    return map;
  }, [out]);

  if (!out) return <div className="bench wide">{error ?? "Loading the breakdown…"}</div>;
  const root = out.breakdown;
  const budget = root.budget ?? 0;
  const pick = selected ? byId.get(selected) : undefined;
  const changed = Object.keys(out.configuration).some((k) => out.configuration[k] !== out.design_configuration[k]);
  const toggle = (id: string) => setOpen((s) => { const n = new Set(s); if (n.has(id)) n.delete(id); else n.add(id); return n; });
  const expandAll = (on: boolean) => setOpen(on ? new Set([...byId.values()].filter((n) => n.children.length).map((n) => n.id)) : new Set([root.id]));
  const loadEnvelope = async () => {
    setBusy(true);
    try { setEnvelope(await api.productEnvelope(projectId)); } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    setBusy(false);
  };

  const rows: ReactElement[] = [];
  const emit = (n: BreakdownNode, depth: number) => {
    const isOpen = open.has(n.id);
    const over = n.rollup.over_budget[0] === n.id;
    rows.push(
      <tr key={n.id} className={`bd-${n.kind}${selected === n.id ? " selected" : ""}`} onClick={() => setSelected(n.id)}>
        <td style={{ paddingLeft: 6 + depth * 14 }}>
          {n.children.length ? (
            <button className="bd-twist" onClick={(e) => { e.stopPropagation(); toggle(n.id); }}
              aria-label={isOpen ? "Collapse" : "Expand"}>{isOpen ? "▾" : "▸"}</button>
          ) : <span className="bd-twist" />}
          {n.name}
          {n.applicability && <span className="bd-tag" title={`Only where ${n.applicability}`}>variant</span>}
          {n.geometry && <span className="bd-tag geo" title={`Geometry: ${n.geometry}`}>3D</span>}
        </td>
        <td className="muted">{n.code}</td>
        <td className="num">{n.kind === "part" ? n.instances : n.rollup.instances}</td>
        <td className={`num${over ? " bad" : ""}`}>{kg(n.rollup.mass)}</td>
        <td className="num muted">{n.rollup.cg[0].toFixed(2)}</td>
        <td><span className={`mat-chip mat-${n.kind === "part" ? n.maturity : n.rollup.min_maturity}`}>
          {LEVEL_SHORT[n.kind === "part" ? n.maturity : n.rollup.min_maturity]}</span></td>
        <td className="muted bd-source">{n.kind === "part" || !n.children.length ? n.mass_source : ""}</td>
      </tr>,
    );
    if (isOpen) n.children.forEach((c) => emit(c, depth + 1));
  };
  emit(root, 0);

  return (
    <div className="bench wide breakdown">
      <div className="bench-side">
        <h3>{root.name}</h3>
        <p className="muted small">{out.module_name} module · {out.templates} part templates · frame: {out.frame}</p>
        <div className="bd-summary">
          <div><span className="muted">Mass</span><b>{kg(root.rollup.mass)} kg</b>
            {budget > 0 && <span className="muted"> of {kg(budget)} kg budget</span>}</div>
          <div><span className="muted">CG (x, z)</span><b>{root.rollup.cg[0].toFixed(2)} m, {root.rollup.cg[2].toFixed(2)} m</b></div>
          <div><span className="muted">Parts</span><b>{root.rollup.parts}</b><span className="muted"> types, {root.rollup.instances} physical</span></div>
        </div>
        <h4>Maturity</h4>
        <MaturityBar counts={root.rollup.maturity} levels={out.levels} />
        <h4>Checks against the product model</h4>
        <div className="bd-checks">
          {out.checks.map((c) => (
            <div key={c.id} className={`check ${c.status}`}><span className="badge">{c.status}</span><b>{c.label}</b><br />{c.message}</div>
          ))}
          {root.rollup.over_budget.length > 0 && (
            <div className="check fail"><span className="badge">fail</span><b>Budget</b><br />Over budget: {root.rollup.over_budget.join(", ")}</div>
          )}
        </div>
        <h4>Configuration {changed && <button className="link" onClick={() => setOverride({})}>back to the design's</button>}</h4>
        <p className="muted small">Viewing a variant never changes the design; the parameters do.</p>
        <div className="bd-options">
          {out.families.map((f) => {
            const value = out.configuration[f.id];
            const own = out.design_configuration[f.id];
            return (
              <label key={f.id} title={f.description || (f.applies ? `Applies where ${f.applies}` : "")}>
                <span>{f.label}</span>
                <select value={value ?? ""} disabled={value === undefined}
                  onChange={(e) => setOverride({ ...override, [f.id]: e.target.value })}>
                  {value === undefined && <option value="">not applicable</option>}
                  {f.choices.map((c) => <option key={c} value={c}>{c}{c === own ? " (design)" : ""}</option>)}
                </select>
              </label>
            );
          })}
        </div>
        {out.violations.map((v) => <div key={v} className="check fail"><span className="badge">rule</span>{v}</div>)}
        <h4>Variants</h4>
        <button onClick={loadEnvelope} disabled={busy}>{busy ? "Computing…" : "Mass envelope over every variant"}</button>
        {envelope && (
          <p className="small">
            {envelope.configurations} valid configurations: {kg(envelope.mass_min)}–{kg(envelope.mass_max)} kg,
            CG x {envelope.cg_x_min.toFixed(2)}–{envelope.cg_x_max.toFixed(2)} m.<br />
            <span className="muted">Heaviest: {Object.values(envelope.heaviest).join(", ")}</span>
          </p>
        )}
        {error && <p className="error">{error}</p>}
      </div>
      <div className="bench-detail">
        <div className="bench-controls">
          <button onClick={() => expandAll(true)}>Expand all</button>
          <button onClick={() => expandAll(false)}>Collapse</button>
          <span className="muted small">Every part exists from day one: L0 is an allocation (mass, CG, interfaces); parts mature to L4 released.</span>
        </div>
        {pick && (
          <div className="bd-detail">
            <b>{pick.name}</b> <span className="muted">{pick.code}{pick.template ? ` · template ${pick.template}` : ""}{pick.process ? ` · ${pick.process}` : ""}</span>
            <div className="small">
              {pick.basis && <Fragment>Mass: {kg(pick.rollup.mass)} kg ({pick.mass_source}: {pick.basis})<br /></Fragment>}
              {pick.functions.length > 0 && <Fragment>Functions: {pick.functions.join(", ")}<br /></Fragment>}
              {pick.applicability && <Fragment>Applies where: <code>{pick.applicability}</code><br /></Fragment>}
              {pick.geometry && <Fragment>Geometry: generated today (component <code>{pick.geometry}</code>)<br /></Fragment>}
              CG: {pick.rollup.cg.map((v) => v.toFixed(2)).join(", ")} m
            </div>
          </div>
        )}
        <table className="bd-table">
          <thead><tr><th>Item</th><th>Code</th><th className="num">Qty</th><th className="num">Mass kg</th><th className="num">CG x m</th><th>Level</th><th>Mass from</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
  );
}
