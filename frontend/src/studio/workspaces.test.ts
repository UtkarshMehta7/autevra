import { describe, expect, it } from "vitest";
import { WORKSPACES } from "./workspaces";

describe("studio workspaces", () => {
  it("covers the routed workspaces of the brief, once each", () => {
    expect(WORKSPACES.map((w) => w.id)).toEqual([
      "design", "assembly", "simulation", "ai-engineering", "optimization", "requirements",
      "systems", "manufacturing", "digital-engineering",
    ]);
  });
});
