import { useCallback, useEffect, useState } from "react";

/** Sizes of the studio panels, in CSS pixels; a side panel at 0 is collapsed. */
export interface Layout {
  left: number;
  right: number;
  dock: number;
  focus: boolean; // the viewport takes the whole window below the header
}

const KEY = "autevra.layout";
export const DEFAULT_LAYOUT: Layout = { left: 240, right: 360, dock: 360, focus: false };
export const LIMITS = {
  left: { min: 160, max: 640 },
  right: { min: 240, max: 760 },
  dock: { min: 140 }, // the maximum leaves room for the viewport (see clampDock)
};
const COLLAPSE_BELOW = 80; // dragging a side panel narrower than this collapses it

/** The dock height kept between its minimum and the window height less room for the
 * header and a usable viewport. */
export function clampDock(px: number, windowHeight: number): number {
  return Math.round(Math.min(Math.max(px, LIMITS.dock.min), Math.max(windowHeight - 220, LIMITS.dock.min)));
}

/** A side panel width after a drag: collapsed when dragged almost shut, otherwise kept
 * within its limits. */
export function clampSide(px: number, side: "left" | "right"): number {
  if (px < COLLAPSE_BELOW) return 0;
  const { min, max } = LIMITS[side];
  return Math.round(Math.min(Math.max(px, min), max));
}

function load(): Layout {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return DEFAULT_LAYOUT;
    const saved = JSON.parse(raw) as Partial<Layout>;
    const num = (v: unknown, d: number) => (typeof v === "number" && Number.isFinite(v) ? v : d);
    return {
      left: num(saved.left, DEFAULT_LAYOUT.left),
      right: num(saved.right, DEFAULT_LAYOUT.right),
      dock: num(saved.dock, DEFAULT_LAYOUT.dock),
      focus: false, // always start with the panels visible
    };
  } catch {
    return DEFAULT_LAYOUT;
  }
}

/** Panel sizes that persist in this browser. */
export function useLayout() {
  const [layout, setLayout] = useState<Layout>(load);
  // Width a side panel had before it was collapsed, to restore it.
  const [restore, setRestore] = useState({ left: DEFAULT_LAYOUT.left, right: DEFAULT_LAYOUT.right });

  useEffect(() => {
    try {
      localStorage.setItem(KEY, JSON.stringify({ ...layout, focus: false }));
    } catch {
      /* storage unavailable: sizes last for this visit only */
    }
  }, [layout]);

  const set = useCallback((patch: Partial<Layout>) => setLayout((l) => ({ ...l, ...patch })), []);
  const toggleSide = useCallback((side: "left" | "right") => {
    setLayout((l) => {
      if (l[side] > 0) {
        setRestore((r) => ({ ...r, [side]: l[side] }));
        return { ...l, [side]: 0 };
      }
      return { ...l, [side]: restore[side] || DEFAULT_LAYOUT[side] };
    });
  }, [restore]);
  const reset = useCallback(() => setLayout(DEFAULT_LAYOUT), []);
  return { layout, set, toggleSide, reset };
}
