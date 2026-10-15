import * as THREE from "three";
import { describe, expect, it } from "vitest";
import { curvatureColors, curvatureEstimate } from "./tools";

describe("curvature estimate", () => {
  it("is zero on a flat plate and higher on a small sphere than a large one", () => {
    const flat = curvatureEstimate(new THREE.PlaneGeometry(1000, 1000, 10, 10));
    expect(Math.max(...flat)).toBeCloseTo(0, 6);
    const small = curvatureEstimate(new THREE.SphereGeometry(10, 32, 16));
    const large = curvatureEstimate(new THREE.SphereGeometry(1000, 32, 16));
    const median = (a: Float32Array) => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];
    expect(median(small)).toBeGreaterThan(median(large) * 50);
    // About 1/r for a sphere tessellated this finely (an estimate, within a factor of two).
    expect(median(large)).toBeGreaterThan(0.5 / 1000);
    expect(median(large)).toBeLessThan(2 / 1000);
  });

  it("maps flat to blue and tight curves to red", () => {
    const [r0, , b0, r1, , b1] = curvatureColors(new Float32Array([0, 1]));
    expect(b0).toBeGreaterThan(r0);
    expect(r1).toBeGreaterThan(b1);
  });
});
