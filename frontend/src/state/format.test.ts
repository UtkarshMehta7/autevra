import { describe, expect, it } from "vitest";
import type { ModelPart } from "../api/types";
import { describeChange, formatValue, groupParts, staleGeometry } from "./format";

const part = (id: string, category: string, geometry: string): ModelPart => ({
  id, name: id, category, geometry, matrix: [], color: [0, 0, 0],
});

describe("format helpers", () => {
  it("formats values", () => {
    expect(formatValue(4600, "mm")).toBe("4600 mm");
    expect(formatValue(656.80000001, "mm")).toBe("656.8 mm");
  });

  it("groups parts in display order", () => {
    const groups = groupParts([part("wheel_fl", "wheel", "w"), part("body", "body", "b"),
      part("front_axle", "axle", "a")]);
    expect(groups.map(([c]) => c)).toEqual(["body", "axle", "wheel"]);
  });

  it("evicts the oldest unused geometry beyond the keep limit", () => {
    const parts = [part("x", "body", "b")];
    expect(staleGeometry(["a", "b", "c"], parts, 0)).toEqual(["a", "c"]);
    expect(staleGeometry(["a", "b", "c"], parts, 1)).toEqual(["a"]);
    expect(staleGeometry(["a", "b", "c"], parts)).toEqual([]);
  });

  it("describes history entries", () => {
    expect(describeChange({ command: { instruction: "lower the car by 20 mm" }, changes: [] }))
      .toBe("lower the car by 20 mm");
    expect(describeChange({ command: {}, changes: [{ parameter: "wheelbase", old: 2700, new: 2800 }] }))
      .toBe("wheelbase: 2700 → 2800");
  });
});
