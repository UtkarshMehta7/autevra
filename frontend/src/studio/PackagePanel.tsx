import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { PackageValue } from "../api/types";
import { DownloadLink } from "../DownloadLink";

/** Package drawing (side, top and front views) and the package dimensions, live. */
export function PackagePanel({ projectId, version }: { projectId: string; version: number }) {
  const [values, setValues] = useState<PackageValue[] | null>(null);
  const [svg, setSvg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    setError(null);
    api.package(projectId).then(setValues).catch((e) => setError(String(e.message ?? e)));
    api.packageSvg(projectId).then(setSvg).catch((e) => setError(String(e.message ?? e)));
  }, [projectId, version]);
  return (
    <div className="bench wide package">
      <div className="bench-side">
        <strong>Package</strong>
        {error && <div className="error">{error}</div>}
        {!values && !error && <p className="hint">Measuring…</p>}
        {values && (
          <table className="package-values">
            <tbody>
              {values.map((v) => (
                <tr key={v.id} title={v.note}>
                  <td>{v.label}</td>
                  <td className="num">{v.value.toFixed(v.unit === "deg" ? 1 : 0)}</td>
                  <td>{v.unit === "deg" ? "°" : v.unit}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <DownloadLink className="button" href={api.packageSvgUrl(projectId)}>Package drawing (SVG)</DownloadLink>
        <p className="hint">Unladen, tyres unloaded. Clearance angles are tangent to the tyres and
          clear every low point of the body, frame and tow bar. Ask in the command bar, e.g.
          “what is the approach angle?”, or set a requirement: “the approach angle shall be at
          least 20 deg”.</p>
      </div>
      <div className="bench-detail">
        {svg ? <div className="drawing" dangerouslySetInnerHTML={{ __html: svg }} /> : <p className="hint">Drawing…</p>}
      </div>
    </div>
  );
}
