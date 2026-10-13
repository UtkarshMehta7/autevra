import type { ComponentStatus, Credibility } from "../api/types";

export const STATUS_LABELS: Record<ComponentStatus, string> = {
  passed_within_model: "Passed within the model",
  failed: "Failed",
  no_criteria: "No criteria defined",
  invalid: "Invalid (numerics or inputs)",
  not_tested: "Not tested",
  stale: "Stale: design changed since the test",
  experimentally_validated: "Experimentally validated",
};

export const STATUS_SHORT: Record<ComponentStatus, string> = {
  passed_within_model: "pass", failed: "fail", no_criteria: "no criteria", invalid: "invalid",
  not_tested: "not tested", stale: "stale", experimentally_validated: "validated",
};

export const CREDIBILITY_LABELS: Record<Credibility, string> = {
  analytical_estimate: "Analytical estimate",
  numerical_simulation: "Numerical simulation (not validated against test data)",
  experimentally_validated: "Experimentally validated",
};

/** Engineering number formatting: 3 significant figures, no exponent for common ranges. */
export function fmt(value: number | null | undefined, unit = ""): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  const abs = Math.abs(value);
  let text: string;
  if (abs === 0) text = "0";
  else if (abs >= 1000) text = Math.round(value).toString();
  else if (abs >= 100) text = value.toFixed(0);
  else if (abs >= 10) text = value.toFixed(1);
  else if (abs >= 1) text = value.toFixed(2);
  else text = value.toFixed(3);
  return unit ? `${text} ${unit}` : text;
}

/** A tidy axis range that contains every value and the given reference lines. */
export function niceExtent(values: number[], extra: number[] = []): [number, number] {
  const all = [...values, ...extra].filter(Number.isFinite);
  if (all.length === 0) return [0, 1];
  let lo = Math.min(...all), hi = Math.max(...all);
  if (lo === hi) { lo -= 1; hi += 1; }
  const pad = (hi - lo) * 0.08;
  return [lo - pad, hi + pad];
}

export function ticks([lo, hi]: [number, number], count = 4): number[] {
  const step0 = (hi - lo) / count;
  const mag = 10 ** Math.floor(Math.log10(step0));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= step0) ?? step0;
  const out: number[] = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(+v.toFixed(10));
  return out;
}

/** Severity order for showing the worst status first. */
export function severity(status: ComponentStatus): number {
  return ["failed", "invalid", "stale", "not_tested", "no_criteria", "passed_within_model",
    "experimentally_validated"].indexOf(status);
}
