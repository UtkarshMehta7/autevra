import { describe, expect, it } from "vitest";
import type { Sketch } from "../api/types";
import { available } from "./ConstraintSketcher";

const sketch: Sketch = {
  points: [{ id: "o", x: 0, y: 0, fixed: true }, { id: "p1", x: 30, y: 40 }, { id: "c", x: 100, y: 0 }],
  entities: [
    { type: "line", id: "l1", a: "o", b: "p1" },
    { type: "line", id: "l2", a: "o", b: "c" },
    { type: "circle", id: "c1", center: "c", radius: 12 },
  ],
  constraints: [],
};
const kinds = (sel: string[]) => available(sketch, sel).map((o) => o.kind);

describe("constraints offered for a selection", () => {
  it("measures a line's current length, so adding it does not move the sketch", () => {
    expect(kinds(["l1"])).toEqual(["horizontal", "vertical", "length"]);
    expect(available(sketch, ["l1"]).find((o) => o.kind === "length")?.value).toBeCloseTo(50);
  });
  it("offers distances between two points", () => {
    const d = available(sketch, ["o", "p1"]);
    expect(d.map((o) => o.kind)).toEqual(["coincident", "distance", "hdistance", "vdistance"]);
    expect(d[2].value).toBeCloseTo(30);
    expect(d[3].value).toBeCloseTo(40);
  });
  it("measures the angle between two lines counter-clockwise", () => {
    const angle = available(sketch, ["l2", "l1"]).find((o) => o.kind === "angle");
    expect(angle?.value).toBeCloseTo(53.13, 1);
  });
  it("offers radius and diameter for a circle, and tangency with a line", () => {
    expect(available(sketch, ["c1"]).map((o) => [o.kind, o.value])).toEqual([["radius", 12], ["diameter", 24]]);
    expect(kinds(["l1", "c1"])).toEqual(["tangent"]);
  });
  it("offers nothing for a mixed selection it cannot constrain", () => {
    expect(kinds(["o", "p1", "c1"])).toEqual([]);
  });
});
