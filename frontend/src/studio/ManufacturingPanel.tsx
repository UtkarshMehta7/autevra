import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { RuleStatus } from "../api/types";
import { DownloadLink } from "../DownloadLink";

// Design rules that express manufacturability or assembly feasibility.
const MANUFACTURING_RULES = /spring_index|coil_bind|rail_wall|damper_fits|disc_fits|stroke_covers/;

export function ManufacturingPanel({ projectId, version, stepUrl, reqifUrl }: {
  projectId: string; version: number; stepUrl: string; reqifUrl: string;
}) {
  const [rules, setRules] = useState<RuleStatus[] | null>(null);
  useEffect(() => {
    api.rules(projectId).then(setRules).catch(() => setRules(null));
  }, [projectId, version]);
  const relevant = (rules ?? []).filter((r) => MANUFACTURING_RULES.test(r.id));
  return (
    <div className="bench wide">
      <div className="bench-side">
        <strong>Outputs</strong>
        <ul className="plain">
          <li><DownloadLink className="button" href={stepUrl}>STEP AP214 assembly</DownloadLink> <span className="hint">named, coloured, placed solids</span></li>
          <li><DownloadLink className="button" href={reqifUrl}>ReqIF requirements</DownloadLink></li>
        </ul>
        <p className="hint"><strong>Not available yet:</strong> 2D drawings, tolerances and PMI,
          sheet-metal flat patterns, cost estimation, process planning and CAM. They are on the
          roadmap; nothing here simulates them.</p>
      </div>
      <div className="bench-detail">
        <strong>Manufacturability and fit checks</strong>
        {!rules && <p className="hint">Loading…</p>}
        <ul className="checks">
          {relevant.map((r) => (
            <li key={r.id}>
              <span className={`status-pill ${r.passed ? "pass" : "fail"}`}>{r.passed ? "pass" : "fail"}</span>
              {r.description}{r.message && <span className="bad-text"> — {r.message}</span>}
            </li>
          ))}
        </ul>
        <p className="hint">These are the design rules that concern making and fitting parts
          (spring index and coil bind, rail wall thickness, damper and disc fit). All rules are
          enforced on every change.</p>
      </div>
    </div>
  );
}
