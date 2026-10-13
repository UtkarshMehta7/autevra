import type { IntegrationReport } from "../api/types";

const KIND_LABELS: Record<string, string> = {
  clearance: "Clearances (exact, on the CAD solids)",
  travel: "Wheel travel limits",
  coincidence: "Closed mounts",
  load_path: "Load paths",
  interface: "Mates and interfaces",
  connectivity: "Connectivity",
};

export function IntegrationPanel({ report, onRefresh, busy }: {
  report: IntegrationReport | null; onRefresh: () => void; busy: boolean;
}) {
  if (!report) return <p className="hint">Checking the assembly…</p>;
  const kinds = Object.keys(KIND_LABELS).filter((k) => report.checks.some((c) => c.kind === k));
  return (
    <div className="integration">
      <div className="bench-controls">
        <span>{report.counts.pass ?? 0} pass · {report.counts.warning ?? 0} warnings ·{" "}
          {report.counts.fail ?? 0} failures</span>
        <button onClick={onRefresh} disabled={busy}>Re-check</button>
      </div>
      {kinds.map((kind) => {
        const checks = report.checks.filter((c) => c.kind === kind);
        const notable = checks.filter((c) => c.status !== "pass");
        return (
          <details key={kind} open={notable.length > 0}>
            <summary>
              {KIND_LABELS[kind]} <small>({checks.length - notable.length}/{checks.length} pass)</small>
            </summary>
            <ul className="checks">
              {checks.map((c) => (
                <li key={c.id} className={c.status}>
                  <span className={`status-pill ${c.status}`}>{c.status}</span> {c.message}
                  {c.parameters.length > 0 && c.status !== "pass" && (
                    <small className="hint"> · parameters: {c.parameters.join(", ")}</small>
                  )}
                </li>
              ))}
            </ul>
          </details>
        );
      })}
      <p className="hint">Not checked: {report.not_checked.join(" ")}</p>
    </div>
  );
}
