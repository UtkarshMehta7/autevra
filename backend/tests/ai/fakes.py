"""A scripted stand-in for a local LLM runtime."""

from typing import Any

from autevra.ai.llm.clients import LLMStatus, LLMUnavailableError


class FakeLLM:
    provider = "fake"
    model = "fake-1b"

    def __init__(self, *answers: dict[str, Any] | Exception) -> None:
        self.answers = list(answers)
        self.calls: list[list[dict[str, str]]] = []

    def status(self) -> LLMStatus:
        return LLMStatus(self.provider, self.model, "fake://", True)

    def complete_json(self, messages, schema) -> dict[str, Any]:  # type: ignore[no-untyped-def]
        self.calls.append(messages)
        if not self.answers:
            raise LLMUnavailableError("no scripted answer")
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer


def proposal(*changes: tuple[str, str, float, str | None]) -> dict[str, Any]:
    return {
        "action": "set_parameters",
        "changes": [
            {"parameter": p, "operation": o, "value": v, "unit": u} for p, o, v, u in changes
        ],
        "query": [],
        "question": "",
    }
