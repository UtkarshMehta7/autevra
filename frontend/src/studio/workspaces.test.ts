import { describe, expect, it } from "vitest";
import { WORKSPACES } from "./workspaces";

describe("studio workspaces", () => {
  it("covers the routed workspaces of the brief, once each", () => {
    expect(WORKSPACES.map((w) => w.id)).toEqual([
      "design", "engine", "vessel", "breakdown", "functions", "loads", "production", "reviews", "inventory", "elements", "machining", "routing", "styling", "part-design", "surfaces", "structures", "aircraft", "package", "assembly", "simulation", "ai-engineering", "optimization",
      "requirements",
      "systems", "manufacturing", "digital-engineering",
    ]);
  });
});

describe("engineering modules", () => {
  it("keep their workspaces apart: aircraft tools are not in land vehicles and vice versa", async () => {
    const { MODULES, moduleOf } = await import("./workspaces");
    const land = moduleOf("automotive"), air = moduleOf("aerospace");
    expect(land.workspaces).not.toContain("aircraft");
    expect(air.workspaces).not.toContain("design");
    expect(air.workspaces[0]).toBe("aircraft");
    expect(moduleOf(undefined).id).toBe("automotive");
    expect(MODULES.filter((m) => m.planned).map((m) => m.id)).toEqual([]);
  });
});
