import { describe, expect, it } from "vitest";
import { clampDock, clampSide, LIMITS } from "./layout";

describe("panel sizes", () => {
  it("collapses a side panel dragged almost shut", () => {
    expect(clampSide(40, "left")).toBe(0);
    expect(clampSide(79, "right")).toBe(0);
  });
  it("keeps a side panel within its limits", () => {
    expect(clampSide(120, "left")).toBe(LIMITS.left.min);
    expect(clampSide(5000, "left")).toBe(LIMITS.left.max);
    expect(clampSide(420.4, "right")).toBe(420);
  });
  it("leaves room for the viewport above the dock", () => {
    expect(clampDock(2000, 900)).toBe(680);
    expect(clampDock(50, 900)).toBe(LIMITS.dock.min);
    expect(clampDock(300, 900)).toBe(300);
  });
});
