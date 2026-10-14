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
      kind: "half_car";
      label: string;
      wheelbase: number; // mm
      cgX: number; // mm, x of the sprung-mass centre (front axle at 0, rear at -wheelbase)
      t: number[];
      heave: number[]; // mm
      pitch: number[]; // deg, ISO 8855: positive nose down
      frontAxle: number[]; // mm
      rearAxle: number[]; // mm
      road: number[]; // mm under the front wheels
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
  if (anim.kind === "half_car") return halfCarPoses(anim, index, base, damperLength);
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

/**
 * Half car: the sprung parts heave and pitch about the sprung-mass centre, each axle and its
 * wheels follow that axle's computed motion, and the dampers stretch between the two.
 */
function halfCarPoses(
  anim: Extract<Animation, { kind: "half_car" }>, index: number,
  base: Map<string, THREE.Matrix4>, damperLength: (id: string) => number,
): Map<string, THREE.Matrix4> {
  const out = new Map<string, THREE.Matrix4>();
  const k = anim.exaggeration;
  const heave = anim.heave[index] * k;
  const theta = THREE.MathUtils.degToRad(anim.pitch[index] * k);
  const axleZ = { front: anim.frontAxle[index] * k, rear: anim.rearAxle[index] * k };
  const a = -anim.cgX, b = anim.cgX + anim.wheelbase;
  const bodyAt = { front: heave - a * theta, rear: heave + b * theta };
  const sprung = new THREE.Matrix4().makeTranslation(anim.cgX, 0, heave)
    .multiply(new THREE.Matrix4().makeRotationY(theta)) // +Y rotation: nose down
    .multiply(new THREE.Matrix4().makeTranslation(-anim.cgX, 0, 0));
  for (const [id, m] of base) {
    const axle = (["front", "rear"] as const).find((x) => id === `${x}_axle`
      || CORNERS[x].some((c) => id === `wheel_${c}` || id === `damper_${c}`));
    if (!axle) {
      out.set(id, sprung.clone().multiply(m)); // body, glazing, lamps, frame
      continue;
    }
    const lift = new THREE.Matrix4().makeTranslation(0, 0, axleZ[axle]);
    if (id.startsWith("damper_")) {
      const length = damperLength(id);
      const stretch = length > 0 ? (length + bodyAt[axle] - axleZ[axle]) / length : 1;
      out.set(id, lift.multiply(m.clone()).multiply(new THREE.Matrix4().makeScale(1, 1, stretch)));
    } else {
      out.set(id, lift.multiply(m.clone()));
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
  if (anim.kind === "half_car") {
    const p = anim.pitch[index];
    return `${anim.label} · t ${t} s · heave ${f(anim.heave[index])} · pitch ${p >= 0 ? "+" : ""}${p.toFixed(2)}° (+ nose down)`
      + (anim.exaggeration !== 1 ? ` · motion ×${anim.exaggeration}` : "");
  }
  return `${anim.label} · t ${t} s · road ${f(anim.road[index])} · wheel ${f(anim.wheel[index])} · body ${f(anim.body[index])}`
    + (anim.exaggeration !== 1 ? ` · motion ×${anim.exaggeration}` : "")
    + " · other axle held (not simulated)";
}
