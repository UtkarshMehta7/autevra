import { describe, expect, it } from "vitest";
import { fmt, niceExtent, severity, ticks } from "./engineering";

describe("engineering formatting", () => {
  it("formats with sensible precision", () => {
    expect(fmt(42.7366, "mm")).toBe("42.7 mm");
    expect(fmt(0.44187)).toBe("0.442");
    expect(fmt(5.297, "m/s²")).toBe("5.30 m/s²");
    expect(fmt(2860, "N·s/m")).toBe("2860 N·s/m");
    expect(fmt(null)).toBe("—");
  });

  it("builds an extent that includes limit lines", () => {
    const [lo, hi] = niceExtent([-5, 20], [35]);
    expect(lo).toBeLessThan(-5);
    expect(hi).toBeGreaterThan(35);
  });

  it("chooses round tick steps", () => {
    expect(ticks([0, 40])).toEqual([0, 10, 20, 30, 40]);
  });

  it("orders failures first", () => {
    expect(severity("failed")).toBeLessThan(severity("stale"));
    expect(severity("stale")).toBeLessThan(severity("passed_within_model"));
  });
});
