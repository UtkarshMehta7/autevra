import * as THREE from "three";
import { describe, expect, it } from "vitest";
import { type Animation, frameIndex, framePoses } from "./animation";

const base = new Map<string, THREE.Matrix4>([
  ["body", new THREE.Matrix4()],
  ["rear_axle", new THREE.Matrix4().makeTranslation(-2700, 0, 330)],
  ["wheel_rl", new THREE.Matrix4().makeTranslation(-2700, 780, 330)],
  ["damper_rl", new THREE.Matrix4().makeTranslation(-2700, 450, 365)],
  ["wheel_fl", new THREE.Matrix4().makeTranslation(0, 780, 330)],
]);
const anim: Animation = {
  kind: "quarter_car", label: "rear", axle: "rear", wheelbase: 2700,
  t: [0, 0.1, 0.2], body: [0, 10, 20], wheel: [0, 30, 5], road: [0, 25, 0], exaggeration: 1,
};

const z = (m: THREE.Matrix4, p = new THREE.Vector3()) => p.applyMatrix4(m).z;

describe("quarter-car playback", () => {
  it("finds the sample for a time and loops", () => {
    expect(frameIndex(anim.t, 0.1)).toBe(1);
    expect(frameIndex(anim.t, 0.3)).toBe(1); // 0.3 mod 0.2
  });

  it("moves the simulated wheel by the wheel motion and holds the other axle", () => {
    const poses = framePoses(anim, 1, base, () => 300);
    expect(z(poses.get("wheel_rl")!) - 330).toBeCloseTo(30);
    expect(z(poses.get("wheel_fl")!)).toBeCloseTo(330);
  });

  it("pitches the body so it moves by the body motion over the simulated axle", () => {
    const poses = framePoses(anim, 1, base, () => 300);
    const overAxle = z(poses.get("body")!, new THREE.Vector3(-2700, 0, 0));
    const overPivot = z(poses.get("body")!, new THREE.Vector3(0, 0, 0));
    expect(overAxle).toBeCloseTo(10, 1);
    expect(overPivot).toBeCloseTo(0, 6);
  });

  it("stretches the damper by body minus wheel motion", () => {
    const poses = framePoses(anim, 1, base, () => 300);
    const top = z(poses.get("damper_rl")!, new THREE.Vector3(0, 0, 300));
    const bottom = z(poses.get("damper_rl")!, new THREE.Vector3(0, 0, 0));
    expect(top - bottom).toBeCloseTo(300 + 10 - 30);
  });
});
