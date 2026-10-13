import { describe, expect, it } from "vitest";
import { llmLabel } from "./llm";

const status = (provider: string, available: boolean) => ({
  provider, available, model: "qwen2.5:1.5b", url: "", detail: "", models: [],
});

describe("llmLabel", () => {
  it("describes each state", () => {
    expect(llmLabel(null)).toBe("deterministic parser");
    expect(llmLabel(status("off", false))).toBe("deterministic parser · LLM off");
    expect(llmLabel(status("ollama", true))).toBe("parser + local qwen2.5:1.5b");
    expect(llmLabel(status("ollama", false))).toBe("deterministic parser · qwen2.5:1.5b unavailable");
  });
});
