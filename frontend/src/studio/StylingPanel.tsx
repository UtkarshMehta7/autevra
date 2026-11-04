import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { Styling } from "../api/types";
import { type Blueprint, BlueprintControls, BlueprintImage, loadBlueprint } from "./Blueprint";
import { CurveEditor, type Pt } from "./CurveEditor";

/**
 * Align a blueprint on two picked points: ``a`` (front) and ``b`` (rear), picked on the
 * image as placed now, must land on the model points ``ta`` and ``tb`` (same height).
 */
function align(bp: Blueprint, a: Pt, b: Pt, ta: Pt, tb: Pt): Blueprint {
  const frac = ([x, v]: Pt): Pt => {
    const f = (x - bp.x) / bp.width;
    return [bp.flip ? 1 - f : f, (bp.v - v) / (bp.width * bp.aspect)];
  };
  const [fa, ga] = frac(a), [fb, gb] = frac(b);
  const sa = bp.flip ? 1 - fa : fa, sb = bp.flip ? 1 - fb : fb; // image fraction -> x order
  if (Math.abs(sa - sb) < 1e-6) return bp;
  const width = (ta[0] - tb[0]) / (sa - sb);
  const x = ta[0] - sa * width;
  const v = (ta[1] + tb[1]) / 2 + ((ga + gb) / 2) * width * bp.aspect;
  return { ...bp, width: Math.abs(width), x: width > 0 ? x : x + width, v };
}

const LABELS = { top: "Silhouette (top line)", bottom: "Underbody", plan: "Plan (half width)" };

/** Draw the styled body's guide curves: side silhouette, underbody and plan width. */
export function StylingPanel({ projectId, version, onModelChanged }: {
  projectId: string; version: number; onModelChanged: () => void;
}) {
  const [styling, setStyling] = useState<Styling | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [blueprints, setBlueprints] = useState<Record<string, Blueprint | null>>(() => ({
    side: loadBlueprint(projectId, "side"), plan: loadBlueprint(projectId, "plan"),
  }));
  const [picking, setPicking] = useState<{ view: string; first: Pt | null } | null>(null);
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
  const placed = (view: string, bp: Blueprint | null): Blueprint | null => {
    if (!bp || bp.width > 0) return bp;
    const width = ref.front - ref.rear; // first placement: the image spans the car's length
    return { ...bp, x: ref.rear, width, v: view === "side" ? width * bp.aspect : (width * bp.aspect) / 2 };
  };
  const setBp = (view: string, bp: Blueprint | null) => setBlueprints((all) => ({ ...all, [view]: placed(view, bp) }));
  const pick = (view: string) => (pt: Pt) => {
    if (!picking || picking.view !== view) return;
    if (!picking.first) { setPicking({ view, first: pt }); return; }
    const bp = blueprints[view];
    if (bp) {
      const target: [Pt, Pt] = view === "side"
        ? [[0, ref.tyre_radius], [-ref.wheelbase, ref.tyre_radius]] : [[0, 0], [-ref.wheelbase, 0]];
      setBp(view, align(bp, picking.first, pt, target[0], target[1]));
    }
    setPicking(null);
  };
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
        <BlueprintControls project={projectId} view="side" label="side" bp={blueprints.side}
          onChange={(bp) => setBp("side", bp)} picking={picking?.view === "side"}
          onPickStart={() => setPicking({ view: "side", first: null })} />
        <CurveEditor view={side} onCommit={save} onPick={picking?.view === "side" ? pick("side") : undefined} curves={[
          { id: "top", points: curves.top, color: "#7fb2ff", label: LABELS.top },
          { id: "bottom", points: curves.bottom, color: "#f0b44c", label: LABELS.bottom },
        ]}>
          {blueprints.side && <BlueprintImage bp={blueprints.side} />}
          <line x1={side.x0} x2={side.x1} y1={0} y2={0} className="ref-ground" />
          <line x1={ref.rear} x2={ref.front} y1={-ref.overall_height} y2={-ref.overall_height} className="ref-limit" />
          <line x1={ref.rear} x2={ref.rear} y1={0} y2={-ref.overall_height} className="ref-limit" />
          <line x1={ref.front} x2={ref.front} y1={0} y2={-ref.overall_height} className="ref-limit" />
          <line x1={ref.glass[0]} x2={ref.glass[1]} y1={-ref.beltline} y2={-ref.beltline} className="ref-belt" />
          {wheels}
        </CurveEditor>
        <strong>Plan view (left half)</strong>
        <BlueprintControls project={projectId} view="plan" label="top" bp={blueprints.plan}
          onChange={(bp) => setBp("plan", bp)} picking={picking?.view === "plan"}
          onPickStart={() => setPicking({ view: "plan", first: null })} />
        <CurveEditor view={plan} height={200} onCommit={save} onPick={picking?.view === "plan" ? pick("plan") : undefined} curves={[
          { id: "plan", points: curves.plan, color: "#8fd694", label: LABELS.plan },
        ]}>
          {blueprints.plan && <BlueprintImage bp={blueprints.plan} />}
          <polyline points={curves.plan.map(([x, y]: [number, number]) => `${x},${y}`).join(" ")} className="ref-mirror" />
          <line x1={plan.x0} x2={plan.x1} y1={0} y2={0} className="ref-ground" />
          <line x1={ref.rear} x2={ref.front} y1={-ref.half_width} y2={-ref.half_width} className="ref-limit" />
          {[0, -ref.wheelbase].map((x) => <line key={x} x1={x} x2={x} y1={-ref.half_width} y2={ref.half_width} className="ref-belt" />)}
        </CurveEditor>
      </div>
    </div>
  );
}
