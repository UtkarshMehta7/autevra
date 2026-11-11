import type { SketchSolve } from "../api/types";

/** The sketch solver's working, as a mathematical console: the nonlinear system F(x) = 0
 * the constraints form, the Jacobian rank and what follows from it (degrees of freedom,
 * redundancy), every equation with its residual, and the convergence history of the damped
 * Gauss-Newton iterations (backend part/sketch.py). */
export function SolverConsole({ status }: { status: SketchSolve | null }) {
  if (!status || status.equations == null) return null;
  const m = status.equations.reduce((n, e) => n + e.rows, 0);
  const n = status.unknowns ?? 0;
  const r = status.rank ?? 0;
  const steps = status.iterations ?? [];
  return (
    <details className="solver-console" open>
      <summary>Solver console</summary>
      <div className="math">
        <div>F(x) = 0 — {n} unknown{n === 1 ? "" : "s"} (free point coordinates, circle radii), {m} equation{m === 1 ? "" : "s"}</div>
        <div>J = ∂F/∂x is {m} × {n}, rank {r}</div>
        <div>DOF = n − rank = {n} − {r} = <b>{status.dof}</b>{"   "}redundant = m − rank = {m} − {r} = <b>{status.redundant}</b></div>
        <div className={status.ok ? "good-text" : "bad-text"}>
          {status.ok ? "Every equation met" : "Conflict: some equations cannot be met together"}
          {" "}· max |Fᵢ| = {status.residual.toExponential(2)}
          {" "}· {steps.length} iteration{steps.length === 1 ? "" : "s"}
        </div>
      </div>
      {status.method && <p className="hint">{status.method}</p>}
      {steps.length > 0 && <Convergence steps={steps} />}
      <table className="mini equations">
        <thead><tr><th>#</th><th>Equation</th><th>rows</th><th>residual</th></tr></thead>
        <tbody>
          {status.equations.map((e, i) => (
            <tr key={i} className={e.residual > 1e-4 ? "conflict" : ""}>
              <td>{e.index == null ? "arc" : e.index + 1}</td>
              <td className="eq">{e.text}</td>
              <td>{e.rows}</td>
              <td className={e.residual > 1e-4 ? "bad-text" : "good-text"}>{e.residual.toExponential(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  );
}

function Convergence({ steps }: { steps: NonNullable<SketchSolve["iterations"]> }) {
  const W = 300, H = 90, L = 34, B = 16;
  const ys = steps.map((s) => Math.log10(Math.max(s.max_residual, 1e-16)));
  const lo = Math.min(...ys, -12), hi = Math.max(...ys, 0);
  const x = (i: number) => L + (i / Math.max(steps.length - 1, 1)) * (W - L - 6);
  const y = (v: number) => 6 + (1 - (v - lo) / Math.max(hi - lo, 1e-9)) * (H - B - 6);
  const accepted = steps.map((s, i) => [s, i] as const).filter(([s]) => s.accepted);
  return (
    <svg className="chart convergence" viewBox={`0 0 ${W} ${H}`} role="img"
      aria-label="Convergence: log10 of the largest residual per iteration">
      <text x={L} y={10} className="chart-title">log₁₀ max |Fᵢ| per iteration</text>
      {[hi, (hi + lo) / 2, lo].map((v) => (
        <g key={v}>
          <line x1={L} x2={W - 4} y1={y(v)} y2={y(v)} className="grid" />
          <text x={L - 4} y={y(v) + 3} textAnchor="end" className="tick">{v.toFixed(0)}</text>
        </g>
      ))}
      <path d={accepted.map(([, i], k) => `${k ? "L" : "M"}${x(i).toFixed(1)},${y(ys[i]).toFixed(1)}`).join("")}
        className="series" />
      {steps.map((s, i) => (
        <circle key={i} cx={x(i)} cy={y(ys[i])} r={2.4} className={s.accepted ? "pt" : "pt rejected"}>
          <title>step {s.step}: max |F| {s.max_residual.toExponential(2)}, λ {s.damping.toExponential(1)}, |Δx| {s.step_norm.toExponential(2)}{s.accepted ? "" : " (rejected)"}</title>
        </circle>
      ))}
      <text x={W - 4} y={H - 3} textAnchor="end" className="tick">iteration {steps.length}</text>
    </svg>
  );
}
