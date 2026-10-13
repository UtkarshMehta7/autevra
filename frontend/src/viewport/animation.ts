import * as THREE from "three";

/** Solver output played back in the viewport. Every pose comes from a computed sample. */
export type Animation =
  | {
      kind: "quarter_car";
      label: string;
      axle: "front" | "rear";
      wheelbase: number; // mm
      t: number[]; // s
      body: number[]; // mm, sprung mass from equilibrium
      wheel: number[]; // mm, unsprung mass from equilibrium
      road: number[]; // mm
      exaggeration: number;
    }
  | {
      kind: "longitudinal";
      label: string;
      tyreRadius: number; // mm
      t: number[];
      distance: number[]; // m
      speed: number[]; // km/h
    };

export interface Frame {
  index: number;
  time: number;
  readout: string;
}

const CORNERS = { front: ["fl", "fr"], rear: ["rl", "rr"] } as const;

/** Sample index for a playback time (loops over the run). */
export function frameIndex(t: number[], elapsed: number): number {
  const end = t[t.length - 1] || 1;
  const time = elapsed % end;
  let lo = 0, hi = t.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (t[mid] < time) lo = mid + 1; else hi = mid;
  }
  return lo;
}

/**
 * Extra transforms (pre-multiplied onto each part's assembly matrix) for one frame.
 * Quarter car: the simulated axle's wheels and axle follow the wheel motion; the sprung
 * parts pitch about the other (not simulated, held) axle so that the body moves by the
 * computed body motion at the simulated axle; the dampers stretch between the two.
 */
export function framePoses(
  anim: Animation, index: number, base: Map<string, THREE.Matrix4>,
  damperLength: (id: string) => number,
): Map<string, THREE.Matrix4> {
  const out = new Map<string, THREE.Matrix4>();
  if (anim.kind === "longitudinal") {
    const angle = (anim.distance[index] * 1000) / anim.tyreRadius;
    for (const c of ["fl", "fr", "rl", "rr"]) {
      const id = `wheel_${c}`;
      const m = base.get(id);
      if (m) out.set(id, m.clone().multiply(new THREE.Matrix4().makeRotationY(angle)));
    }
    return out;
  }
  const k = anim.exaggeration;
  const body = anim.body[index] * k, wheel = anim.wheel[index] * k;
  const xAxle = anim.axle === "front" ? 0 : -anim.wheelbase;
  const xPivot = anim.axle === "front" ? -anim.wheelbase : 0;
  const lever = xAxle - xPivot;
  const phi = -Math.asin(Math.max(-1, Math.min(1, body / lever)));
  const pitch = new THREE.Matrix4().makeTranslation(xPivot, 0, 0)
    .multiply(new THREE.Matrix4().makeRotationY(phi))
    .multiply(new THREE.Matrix4().makeTranslation(-xPivot, 0, 0));
  const lift = new THREE.Matrix4().makeTranslation(0, 0, wheel);
  for (const [id, m] of base) {
    if (id === `${anim.axle}_axle` || CORNERS[anim.axle].some((c) => id === `wheel_${c}`)) {
      out.set(id, lift.clone().multiply(m));
    } else if (CORNERS[anim.axle].some((c) => id === `damper_${c}`)) {
      const length = damperLength(id);
      const stretch = length > 0 ? (length + body - wheel) / length : 1;
      out.set(id, lift.clone().multiply(m).multiply(new THREE.Matrix4().makeScale(1, 1, stretch)));
    } else if (id.startsWith("wheel_") || id.endsWith("_axle") || id.startsWith("damper_")) {
      out.set(id, m.clone()); // the other axle is held (it was not simulated)
    } else {
      out.set(id, pitch.clone().multiply(m)); // sprung: body, frame
    }
  }
  return out;
}

export function readout(anim: Animation, index: number): string {
  const t = anim.t[index].toFixed(2);
  if (anim.kind === "longitudinal") {
    return `${anim.label} · t ${t} s · ${anim.speed[index].toFixed(1)} km/h · ${anim.distance[index].toFixed(1)} m`;
  }
  const f = (v: number) => `${v >= 0 ? "+" : ""}${v.toFixed(1)} mm`;
  return `${anim.label} · t ${t} s · road ${f(anim.road[index])} · wheel ${f(anim.wheel[index])} · body ${f(anim.body[index])}`
    + (anim.exaggeration !== 1 ? ` · motion ×${anim.exaggeration}` : "")
    + " · other axle held (not simulated)";
}
