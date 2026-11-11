import { describe, expect, it } from "vitest";
import { creasedAngleNormals } from "./normals";

/** A unit cylinder (radius 1, axis z) of n facets, each quad split along a diagonal that
 * alternates from facet to facet, as a ruled loft's tessellation can. */
function cylinder(n: number) {
  const v: number[] = [], idx: number[] = [];
  for (let i = 0; i < n; i++) {
    const a = (2 * Math.PI * i) / n;
    v.push(Math.cos(a), Math.sin(a), 0, Math.cos(a), Math.sin(a), 1);
  }
  for (let i = 0; i < n; i++) {
    const a0 = 2 * i, a1 = 2 * i + 1, b0 = 2 * ((i + 1) % n), b1 = b0 + 1;
    if (i % 2) idx.push(a0, b0, b1, a0, b1, a1);
    else idx.push(a0, b0, a1, a1, b0, b1);
  }
  return { v, idx };
}

describe("angle-weighted creased normals", () => {
  it("are radial on a cylinder whatever the diagonal of each quad", () => {
    const { v, idx } = cylinder(24);
    const g = creasedAngleNormals(v, idx, Math.PI / 6);
    const pos = g.getAttribute("position"), nor = g.getAttribute("normal");
    let worst = 0;
    for (let i = 0; i < pos.count; i++) {
      const r = Math.hypot(pos.getX(i), pos.getY(i));
      const dot = (pos.getX(i) * nor.getX(i) + pos.getY(i) * nor.getY(i)) / r;
      worst = Math.max(worst, Math.acos(Math.min(1, dot)));
    }
    expect(worst).toBeLessThan(1e-3); // radians
  });

  it("keep a 90 degree edge crisp", () => {
    // two faces of a cube corner: z = 0 (normal -z after winding) and x = 0
    const v = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1];
    const idx = [0, 2, 1, 0, 3, 2, 0, 4, 5, 0, 5, 3];
    const g = creasedAngleNormals(v, idx, Math.PI / 6);
    const nor = g.getAttribute("normal");
    for (let c = 0; c < 6; c++) expect(Math.abs(nor.getZ(c))).toBeCloseTo(1, 6);
    for (let c = 6; c < 12; c++) expect(Math.abs(nor.getX(c))).toBeCloseTo(1, 6);
  });
});
