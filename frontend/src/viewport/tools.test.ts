import * as THREE from "three";
import { describe, expect, it } from "vitest";
import { VIEWS, framing, measure, sectionPlane } from "./tools";

const box = new THREE.Box3(new THREE.Vector3(-3700, -910, 0), new THREE.Vector3(900, 910, 1450));

describe("CAD view tools", () => {
  it("frames the model from each standard view along the right axis", () => {
    const front = framing(box, "front", 35, 1.6);
    const c = box.getCenter(new THREE.Vector3());
    expect(front.position.y).toBeCloseTo(c.y);
    expect(front.position.x).toBeGreaterThan(box.max.x); // in front of the nose (+X)
    const top = framing(box, "top", 35, 1.6);
    expect(top.position.z).toBeGreaterThan(box.max.z);
    expect(top.up.x).toBe(1); // nose up on screen in plan view
    expect(VIEWS.left.dir.y).toBe(1); // ISO 8855: +Y is the vehicle's left
  });

  it("places the section plane at a share of the model extent", () => {
    const plane = sectionPlane(box, "x", 0.5);
    const mid = (box.min.x + box.max.x) / 2;
    expect(plane.distanceToPoint(new THREE.Vector3(mid - 10, 0, 0))).toBeGreaterThan(0); // kept
    expect(plane.distanceToPoint(new THREE.Vector3(mid + 10, 0, 0))).toBeLessThan(0); // cut away
  });

  it("measures distance and its components", () => {
    const m = measure(new THREE.Vector3(0, 0, 0), new THREE.Vector3(300, -400, 0));
    expect(m.distance).toBeCloseTo(500);
    expect([m.dx, m.dy, m.dz]).toEqual([300, 400, 0]);
  });
});
