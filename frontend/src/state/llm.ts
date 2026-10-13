import type { LLMStatus } from "../api/types";

/** Short label for the instruction panel header. */
export function llmLabel(status: LLMStatus | null): string {
  if (!status) return "deterministic parser";
  if (status.provider === "off") return "deterministic parser · LLM off";
  if (status.available) return `parser + local ${status.model}`;
  return `deterministic parser · ${status.model} unavailable`;
}
