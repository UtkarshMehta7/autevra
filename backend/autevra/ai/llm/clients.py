"""HTTP clients for local LLM runtimes (no hosted inference, ever).

Both runtimes run natively on the Mac (Metal GPU) and are reached over
localhost, or ``host.docker.internal`` from a container.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Protocol

import httpx2

Messages = list[dict[str, str]]


class LLMUnavailableError(RuntimeError):
    """The runtime is not reachable, or the model is not installed."""


class LLMResponseError(RuntimeError):
    """The runtime answered, but not with a usable JSON object."""


@dataclass(frozen=True)
class LLMStatus:
    provider: str
    model: str
    url: str
    available: bool
    detail: str = ""
    models: list[str] = field(default_factory=list)


class LLMClient(Protocol):
    provider: str
    model: str

    def status(self) -> LLMStatus: ...

    def complete_json(self, messages: Messages, schema: dict[str, Any]) -> dict[str, Any]: ...


def _http(url: str, timeout: float, transport: httpx2.BaseTransport | None) -> httpx2.Client:
    # Connect fast (the runtime is local); allow longer for generation.
    return httpx2.Client(
        base_url=url,
        timeout=httpx2.Timeout(timeout, connect=2.0),
        trust_env=False,
        transport=transport,
    )


def _decode(content: str) -> dict[str, Any]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMResponseError(f"model returned invalid JSON: {exc}") from None
    if not isinstance(data, dict):
        raise LLMResponseError("model returned JSON that is not an object")
    return data


class OllamaClient:
    """Ollama ``/api/chat`` with a JSON-schema ``format`` (constrained decoding)."""

    provider = "ollama"

    def __init__(
        self,
        url: str,
        model: str,
        timeout: float = 60.0,
        keep_alive: str = "5m",
        transport: httpx2.BaseTransport | None = None,
    ) -> None:
        self.url, self.model, self.keep_alive = url.rstrip("/"), model, keep_alive
        self._http = _http(self.url, timeout, transport)

    def status(self) -> LLMStatus:
        try:
            response = self._http.get("/api/tags")
            response.raise_for_status()
        except httpx2.HTTPError as exc:
            return LLMStatus(self.provider, self.model, self.url, False, f"unreachable: {exc}")
        models = [m["name"] for m in response.json().get("models", [])]
        installed = self.model in models or f"{self.model}:latest" in models
        detail = (
            "" if installed else f"model '{self.model}' is not pulled (ollama pull {self.model})"
        )
        return LLMStatus(self.provider, self.model, self.url, installed, detail, models)

    def complete_json(self, messages: Messages, schema: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self.model,
            "messages": messages,
            "format": schema,
            "stream": False,
            "think": False,
            "keep_alive": self.keep_alive,
            "options": {"temperature": 0, "seed": 0, "num_ctx": 4096, "num_predict": 300},
        }
        try:
            response = self._http.post("/api/chat", json=body)
        except httpx2.HTTPError as exc:
            raise LLMUnavailableError(f"Ollama unreachable at {self.url}: {exc}") from None
        if response.status_code == 400 and "think" in response.text:
            body.pop("think")  # older Ollama or a model without a thinking switch
            response = self._http.post("/api/chat", json=body)
        if response.status_code == 404:
            raise LLMUnavailableError(f"model '{self.model}' is not available in Ollama")
        if response.status_code >= 400:
            raise LLMResponseError(f"Ollama error {response.status_code}: {response.text[:200]}")
        return _decode(response.json().get("message", {}).get("content", ""))


class LlamaServerClient:
    """llama.cpp ``llama-server`` OpenAI-compatible chat API with ``response_format``."""

    provider = "llama_server"

    def __init__(
        self,
        url: str,
        model: str,
        timeout: float = 60.0,
        transport: httpx2.BaseTransport | None = None,
    ) -> None:
        self.url, self.model = url.rstrip("/"), model
        self._http = _http(self.url, timeout, transport)

    def status(self) -> LLMStatus:
        try:
            response = self._http.get("/health")
            response.raise_for_status()
        except httpx2.HTTPError as exc:
            return LLMStatus(self.provider, self.model, self.url, False, f"unreachable: {exc}")
        return LLMStatus(self.provider, self.model, self.url, True)

    def complete_json(self, messages: Messages, schema: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "seed": 0,
            "max_tokens": 300,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "autevra_command", "schema": schema},
            },
        }
        try:
            response = self._http.post("/v1/chat/completions", json=body)
        except httpx2.HTTPError as exc:
            raise LLMUnavailableError(f"llama-server unreachable at {self.url}: {exc}") from None
        if response.status_code >= 400:
            raise LLMResponseError(
                f"llama-server error {response.status_code}: {response.text[:200]}"
            )
        choices = response.json().get("choices") or [{}]
        return _decode(choices[0].get("message", {}).get("content", ""))


class DisabledClient:
    """Used when the LLM is switched off. The app is fully usable without it."""

    provider = "off"
    model = ""

    def status(self) -> LLMStatus:
        return LLMStatus(self.provider, "", "", False, "LLM disabled (AUTEVRA_LLM_PROVIDER=off)")

    def complete_json(self, messages: Messages, schema: dict[str, Any]) -> dict[str, Any]:
        raise LLMUnavailableError("LLM disabled")


def make_client(provider: str, url: str, model: str, timeout: float = 60.0) -> LLMClient:
    match provider:
        case "ollama":
            return OllamaClient(url, model, timeout)
        case "llama_server":
            return LlamaServerClient(url, model, timeout)
        case "off" | "":
            return DisabledClient()
    raise ValueError(f"unknown LLM provider '{provider}' (use ollama, llama_server or off)")
