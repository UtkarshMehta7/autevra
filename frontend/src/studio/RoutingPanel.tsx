import { useEffect, useState } from "react";
import { api } from "../api/client";

/** Routing workspace (every module): a wiring harness or a pipe along waypoints, with its
 * checks (bundle size, voltage drop, bend radius; pressure drop, velocity) computed live,
 * then added to the project as a swept part (backend routing.py). */

type Kind = "harness" | "pipe";
const DEFAULT_POINTS = "0, 0, 400\n800, 0, 400\n800, 500, 400\n1400, 500, 200";

function parse(text: string): [number, number, number][] {
  return text.split("\n").map((l) => l.split(",").map((v) => Number(v.trim())))
    .filter((p) => p.length === 3 && p.every((v) => Number.isFinite(v))) as [number, number, number][];
}

export function RoutingPanel({ projectId, onModelChanged }: { projectId: string; onModelChanged: () => void }) {
  const [kind, setKind] = useState<Kind>("harness");
  const [points, setPoints] = useState(DEFAULT_POINTS);
  const [name, setName] = useState("Battery cable");
  const [bend, setBend] = useState(60);
  const [supply, setSupply] = useState(12);
  const [wires, setWires] = useState("Starter feed, 25, 150\nFuse box, 6, 40\nSensors, 0.5, 1");
  const [pipe, setPipe] = useState({ outer_mm: 12, wall_mm: 1, fluid: "water", flow_lpm: 10 });
  const [out, setOut] = useState<Record<string, unknown> | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  const body = () => kind === "harness"
    ? { name, points: parse(points), bend_radius: bend, supply_v: supply,
        conductors: wires.split("\n").map((l) => l.split(",")).filter((c) => c.length === 3)
          .map(([n, a, i]) => ({ name: n.trim(), area_mm2: Number(a), current_a: Number(i) })) }
    : { name, points: parse(points), bend_radius: bend, ...pipe };
  useEffect(() => {
    const t = window.setTimeout(() => {
      (kind === "harness" ? api.routeHarness(body()) : api.routePipe(body()))
        .then((r) => { setOut(r as Record<string, unknown>); setMsg(null); })
        .catch((e) => setMsg(e instanceof Error ? e.message : String(e)));
    }, 250);
    return () => window.clearTimeout(t);
  }, [kind, points, name, bend, supply, wires, pipe]); // eslint-disable-line react-hooks/exhaustive-deps

  const checks = (out?.checks ?? []) as { id: string; label: string; status: string; message: string }[];
  return (
    <div className="bench wide engine routing">
      <div className="bench-side">
        <div className="row3">
          {(["harness", "pipe"] as Kind[]).map((k) => (
            <button key={k} className={kind === k ? "primary" : ""} onClick={() => { setKind(k); setName(k === "harness" ? "Battery cable" : "Coolant pipe"); setBend(k === "harness" ? 60 : 40); }}>
              {k === "harness" ? "Wiring harness" : "Pipe / tube"}</button>
          ))}
        </div>
        <label className="row">name <input value={name} onChange={(e) => setName(e.target.value)} /></label>
        <label>Waypoints (x, y, z in mm, one per line)<textarea rows={5} value={points} onChange={(e) => setPoints(e.target.value)} /></label>
        <div className="fields">
          <label><span>bend radius</span><input type="number" value={bend} onChange={(e) => setBend(Number(e.target.value))} /><span className="muted">mm</span></label>
          {kind === "harness" ? (
            <label><span>supply</span><input type="number" value={supply} onChange={(e) => setSupply(Number(e.target.value))} /><span className="muted">V</span></label>
          ) : (
            <>
              <label><span>outer diameter</span><input type="number" value={pipe.outer_mm} onChange={(e) => setPipe({ ...pipe, outer_mm: Number(e.target.value) })} /><span className="muted">mm</span></label>
              <label><span>wall</span><input type="number" step={0.1} value={pipe.wall_mm} onChange={(e) => setPipe({ ...pipe, wall_mm: Number(e.target.value) })} /><span className="muted">mm</span></label>
              <label><span>flow</span><input type="number" value={pipe.flow_lpm} onChange={(e) => setPipe({ ...pipe, flow_lpm: Number(e.target.value) })} /><span className="muted">L/min</span></label>
              <label><span>fluid</span><select value={pipe.fluid} onChange={(e) => setPipe({ ...pipe, fluid: e.target.value })}>
                {["water", "diesel", "engine oil", "hydraulic oil"].map((f) => <option key={f}>{f}</option>)}</select><span /></label>
            </>
          )}
        </div>
        {kind === "harness" && <label>Conductors (name, mm², A — one per line)<textarea rows={4} value={wires} onChange={(e) => setWires(e.target.value)} /></label>}
        <div className="buttons">
          <button className="primary" onClick={async () => {
            try {
              await api.addRoute(projectId, { [kind]: body() });
              onModelChanged(); setMsg("Added to the project as a swept part.");
            } catch (e) { setMsg(e instanceof Error ? e.message : String(e)); }
          }}>Add to project</button>
        </div>
        {msg && <p className="small">{msg}</p>}
      </div>
      <div className="bench-detail">
        {out && (
          <>
            <div className="figures">
              <div><b>{Number(out.length_mm).toFixed(0)} mm</b><span>length ({Number(out.turning_deg).toFixed(0)}° of turns)</span></div>
              {kind === "harness" ? <div><b>{Number(out.bundle_mm).toFixed(1)} mm</b><span>bundle diameter</span></div> : (
                <>
                  <div><b>{Number(out.pressure_drop_kpa).toFixed(2)} kPa</b><span>pressure drop ({String(out.regime)})</span></div>
                  <div><b>{Number(out.velocity_ms).toFixed(2)} m/s</b><span>Re {Number(out.reynolds).toFixed(0)}</span></div>
                </>
              )}
            </div>
            {checks.map((c) => <div key={c.id} className={`check ${c.status}`}><span className="badge">{c.status}</span><b>{c.label}</b>: {c.message}</div>)}
            {kind === "harness" && (
              <table><thead><tr><th>conductor</th><th className="num">drop V</th><th className="num">%</th></tr></thead>
                <tbody>{(out.conductors as { name: string; drop_v: number; drop_pct: number }[]).map((c) => (
                  <tr key={c.name}><td>{c.name}</td><td className="num">{c.drop_v.toFixed(3)}</td><td className="num">{c.drop_pct.toFixed(2)}</td></tr>))}</tbody></table>
            )}
            <p className="muted small">Stated rules: bundle 1.15 √Σd², bend ≥ 6 × bundle; two-wire copper drop; Darcy–Weisbach with Blasius or laminar friction and 0.3 per 90° of bend.</p>
          </>
        )}
      </div>
    </div>
  );
}
