import { useEffect, useState } from "react";
import type { PartOut, Topology } from "../api/types";
import { setOverlay } from "../viewport/overlay";

/** Topology inspection for one Part Design feature: what the B-rep is made of after the
 * feature (and how that changed), the Euler-Poincare check, watertightness, the kinds of
 * surface and curve, and for a boolean the section curves the kernel computed it along
 * (drawable in the 3D view). The numbers come from the kernel (backend cad/topology.py). */

const ROWS: [keyof Topology, string, string][] = [
  ["vertices", "V", "Vertices"],
  ["edges", "E", "Edges"],
  ["loops", "L", "Loops (wires)"],
  ["faces", "F", "Faces"],
  ["shells", "S", "Shells"],
  ["solids", "", "Solids"],
];

export function TopologyInspector({ part, featureId }: { part: PartOut; featureId: string }) {
  const [show, setShow] = useState(true);
  const order = part.built;
  const at = order.indexOf(featureId);
  const after = part.topology?.[featureId];
  const prior = at > 0 ? part.topology?.[order[at - 1]] : undefined;
  const before = prior && !("error" in prior) ? (prior as Topology) : undefined;
  const section = part.sections?.[featureId];

  useEffect(() => {
    if (show && section?.polylines?.length) {
      setOverlay({ partId: `part_${part.id}`, polylines: section.polylines, color: 0xffc94a });
    } else {
      setOverlay(null);
    }
    return () => setOverlay(null);
  }, [show, section, part.id]);

  if (at < 0 || !after) return <p className="hint">Not built: no topology to inspect.</p>;
  if ("error" in after) return <p className="bad-text">Inspection failed: {String(after.error)}</p>;
  const t = after as Topology;
  const delta = (k: keyof Topology) => (before ? (t[k] as number) - (before[k] as number) : null);
  const sign = (d: number | null) => (d == null ? "" : d > 0 ? `+${d}` : d < 0 ? `${d}` : "0");
  const genus = Number.isInteger(t.genus) ? t.genus : t.genus.toFixed(2);

  return (
    <div className="inspector" aria-label="Topology inspection">
      <table className="mini">
        <thead><tr><th>Entity</th><th>Before</th><th>After</th><th>Δ</th></tr></thead>
        <tbody>
          {ROWS.map(([k, sym, label]) => (
            <tr key={k}>
              <td>{label}{sym && <span className="muted"> {sym}</span>}</td>
              <td>{before ? String(before[k]) : "—"}</td>
              <td>{String(t[k])}</td>
              <td className={(delta(k) ?? 0) !== 0 ? "changed" : ""}>{sign(delta(k))}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="math" title="Euler-Poincaré formula for a closed manifold solid">
        <div>V − E + F − (L − F) = 2(S − G)</div>
        <div>
          {t.vertices} − {t.edges} + {t.faces} − {t.rings} = {t.euler} = 2({t.shells} − G)
          {"  ⇒  "}G = {genus}
        </div>
        <div className={t.balanced ? "good-text" : "bad-text"}>
          {t.balanced
            ? `Balanced: ${t.genus === 0 ? "no through-holes" : `${t.genus} through-hole${t.genus === 1 ? "" : "s"}`} (genus ${genus})`
            : "Does not balance: the boundary is not a closed manifold"}
        </div>
        {(t.seam_edges > 0 || t.degenerate_edges > 0) && (
          <div className="muted">{t.seam_edges} seam edge(s) counted twice by their face;
            {" "}{t.degenerate_edges} degenerate edge(s) (poles) left out of V and E.</div>
        )}
      </div>
      <div className="checks">
        <span className={t.watertight ? "good-text" : "bad-text"}>
          {t.watertight ? "Watertight" : "Not watertight"}
        </span>
        {" · "}free edges {t.free_edges} · non-manifold edges {t.nonmanifold_edges}
        {" · "}<span className={t.valid ? "good-text" : "bad-text"}>{t.valid ? "kernel check passed" : "kernel check failed"}</span>
      </div>
      <div className="muted">
        Surfaces: {Object.entries(t.surfaces).map(([k, n]) => `${n} ${k}`).join(", ") || "none"}
        <br />Curves: {Object.entries(t.curves).map(([k, n]) => `${n} ${k}`).join(", ") || "none"}
        <br />Area {(t.area / 100).toFixed(1)} cm² · volume {(t.volume / 1000).toFixed(1)} cm³
      </div>
      {section && "curves" in section && (
        <div className="section-info">
          <strong>Boolean {section.op}</strong>: the tool{section.tools > 1 ? `s (${section.tools})` : ""} met
          {" "}the body along {section.curves} curve{section.curves === 1 ? "" : "s"},
          {" "}{section.length.toFixed(1)} mm in all. The kernel splits both boundaries there and keeps the
          {" "}{section.op === "add" ? "faces outside the other solid (union)" : section.op === "cut" ? "body's faces outside the tool and the tool's faces inside the body (subtraction)" : "faces inside both (intersection)"}.
          <label className="toggle">
            <input type="checkbox" checked={show} onChange={(e) => setShow(e.target.checked)} />
            Show the section curves in 3D
          </label>
        </div>
      )}
    </div>
  );
}
