import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { Styling } from "../api/types";
import { CurveEditor, type Pt } from "./CurveEditor";

const LABELS = { top: "Silhouette (top line)", bottom: "Underbody", plan: "Plan (half width)" };

/** Draw the styled body's guide curves: side silhouette, underbody and plan width. */
export function StylingPanel({ projectId, version, onModelChanged }: {
  projectId: string; version: number; onModelChanged: () => void;
}) {
  const [styling, setStyling] = useState<Styling | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    api.styling(projectId).then(setStyling).catch((e) => setError(String(e.message ?? e)));
  }, [projectId, version]);

  const run = useCallback(async (action: () => Promise<Styling>) => {
    setBusy(true);
    setError(null);
    try {
      setStyling(await action());
      onModelChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }, [onModelChanged]);

  if (!styling) return <div className="bench"><p className="hint">{error ?? "Loading the styling curves…"}</p></div>;
  const { curves, custom, reference: ref } = styling;
  const own = (overrides: Partial<Record<"top" | "bottom" | "plan", Pt[] | null>>) => {
    const doc: Record<string, Pt[]> = {};
    for (const name of ["top", "bottom", "plan"] as const) {
      const value = name in overrides ? overrides[name] : custom[name] ? curves[name] : null;
      if (value) doc[name] = value;
    }
    return doc;
  };
  const save = (id: string, points: Pt[]) => run(() => api.setStyling(projectId, own({ [id]: points })));
  const reset = (id: "top" | "bottom" | "plan") => run(() => api.setStyling(projectId, own({ [id]: null })));

  const side = { x0: ref.rear - 300, x1: ref.front + 300, v0: -150, v1: ref.overall_height + 250 };
  const plan = { x0: ref.rear - 300, x1: ref.front + 300, v0: -ref.half_width - 150, v1: ref.half_width + 150 };
  const wheels = [0, -ref.wheelbase].map((x) => (
    <circle key={x} cx={x} cy={-ref.tyre_radius} r={ref.tyre_radius} className="ref-wheel" />
  ));
  return (
    <div className="bench wide styling">
      <div className="bench-side">
        <strong>Body styling</strong>
        <p className="hint">Drag the control points to shape the styled body; “+” inserts a point,
          double-click deletes one. The skin is rebuilt through your curves; the length, width and
          height parameters still bound it (dashed lines).</p>
        {(["top", "bottom", "plan"] as const).map((id) => (
          <div key={id} className="binding">
            <span>{LABELS[id]}: <em>{custom[id] ? "your curve" : "from the style"}</em></span>
            {custom[id] && <button disabled={busy} onClick={() => reset(id)}>Reset</button>}
          </div>
        ))}
        <div className="binding">
          <button disabled={busy || !styling.can_undo} onClick={() => run(() => api.undoStyling(projectId))}>Undo</button>
          <button disabled={busy || !styling.can_redo} onClick={() => run(() => api.redoStyling(projectId))}>Redo</button>
          <button disabled={busy || !(custom.top || custom.bottom || custom.plan)}
            onClick={() => run(() => api.setStyling(projectId, {}))}>Reset all to the style</button>
        </div>
        {busy && <p className="hint">Rebuilding the skin…</p>}
        {error && <div className="error">{error}</div>}
        <p className="hint">Surface must be “Styled freeform” (Body shaping) for the curves to apply.</p>
      </div>
      <div className="bench-detail">
        <strong>Side view</strong>
        <CurveEditor view={side} onCommit={save} curves={[
          { id: "top", points: curves.top, color: "#7fb2ff", label: LABELS.top },
          { id: "bottom", points: curves.bottom, color: "#f0b44c", label: LABELS.bottom },
        ]}>
          <line x1={side.x0} x2={side.x1} y1={0} y2={0} className="ref-ground" />
          <line x1={ref.rear} x2={ref.front} y1={-ref.overall_height} y2={-ref.overall_height} className="ref-limit" />
          <line x1={ref.rear} x2={ref.rear} y1={0} y2={-ref.overall_height} className="ref-limit" />
          <line x1={ref.front} x2={ref.front} y1={0} y2={-ref.overall_height} className="ref-limit" />
          <line x1={ref.glass[0]} x2={ref.glass[1]} y1={-ref.beltline} y2={-ref.beltline} className="ref-belt" />
          {wheels}
        </CurveEditor>
        <strong>Plan view (left half)</strong>
        <CurveEditor view={plan} height={200} onCommit={save} curves={[
          { id: "plan", points: curves.plan, color: "#8fd694", label: LABELS.plan },
        ]}>
          <polyline points={curves.plan.map(([x, y]) => `${x},${y}`).join(" ")} className="ref-mirror" />
          <line x1={plan.x0} x2={plan.x1} y1={0} y2={0} className="ref-ground" />
          <line x1={ref.rear} x2={ref.front} y1={-ref.half_width} y2={-ref.half_width} className="ref-limit" />
          {[0, -ref.wheelbase].map((x) => <line key={x} x1={x} x2={x} y1={-ref.half_width} y2={ref.half_width} className="ref-belt" />)}
        </CurveEditor>
      </div>
    </div>
  );
}
