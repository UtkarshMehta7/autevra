import json

import httpx2
import pytest

from autevra.ai.llm.clients import (
    DisabledClient,
    LlamaServerClient,
    LLMResponseError,
    LLMUnavailableError,
    OllamaClient,
    make_client,
)

MESSAGES = [{"role": "user", "content": "hello"}]
SCHEMA = {"type": "object"}


def _ollama(handler) -> OllamaClient:  # type: ignore[no-untyped-def]
    return OllamaClient(
        "http://ollama.test", "qwen2.5:1.5b", transport=httpx2.MockTransport(handler)
    )


def test_ollama_request_is_schema_constrained_and_deterministic() -> None:
    seen = {}

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen["path"] = request.url.path
        seen["body"] = json.loads(request.content)
        return httpx2.Response(200, json={"message": {"content": '{"action": "undo"}'}})

    assert _ollama(handler).complete_json(MESSAGES, SCHEMA) == {"action": "undo"}
    body = seen["body"]
    assert seen["path"] == "/api/chat"
    assert body["format"] == SCHEMA
    assert body["stream"] is False
    assert body["options"]["temperature"] == 0
    assert body["model"] == "qwen2.5:1.5b"


def test_ollama_retries_without_think_flag() -> None:
    bodies = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        bodies.append(json.loads(request.content))
        if "think" in bodies[-1]:
            return httpx2.Response(400, json={"error": "model does not support think"})
        return httpx2.Response(200, json={"message": {"content": "{}"}})

    assert _ollama(handler).complete_json(MESSAGES, SCHEMA) == {}
    assert "think" not in bodies[-1]


@pytest.mark.parametrize(
    ("response", "error"),
    [
        (httpx2.Response(404, json={"error": "model not found"}), LLMUnavailableError),
        (httpx2.Response(500, text="boom"), LLMResponseError),
        (httpx2.Response(200, json={"message": {"content": "not json"}}), LLMResponseError),
        (httpx2.Response(200, json={"message": {"content": "[1, 2]"}}), LLMResponseError),
    ],
)
def test_ollama_errors(response: httpx2.Response, error: type[Exception]) -> None:
    with pytest.raises(error):
        _ollama(lambda _r: response).complete_json(MESSAGES, SCHEMA)


def test_ollama_unreachable() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("connection refused", request=request)

    client = _ollama(handler)
    with pytest.raises(LLMUnavailableError):
        client.complete_json(MESSAGES, SCHEMA)
    assert client.status().available is False


def test_ollama_status_reports_missing_model() -> None:
    def handler(_r: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"models": [{"name": "llama3.2:1b"}]})

    status = _ollama(handler).status()
    assert status.available is False
    assert "ollama pull qwen2.5:1.5b" in status.detail
    assert status.models == ["llama3.2:1b"]


def test_llama_server_uses_response_format() -> None:
    seen = {}

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen["path"] = request.url.path
        seen["body"] = json.loads(request.content)
        return httpx2.Response(200, json={"choices": [{"message": {"content": '{"a": 1}'}}]})

    client = LlamaServerClient(
        "http://llama.test", "local", transport=httpx2.MockTransport(handler)
    )
    assert client.complete_json(MESSAGES, SCHEMA) == {"a": 1}
    assert seen["path"] == "/v1/chat/completions"
    assert seen["body"]["response_format"]["json_schema"]["schema"] == SCHEMA
    assert seen["body"]["temperature"] == 0


def test_disabled_client_and_factory() -> None:
    assert isinstance(make_client("off", "", ""), DisabledClient)
    with pytest.raises(LLMUnavailableError):
        DisabledClient().complete_json(MESSAGES, SCHEMA)
    with pytest.raises(ValueError):
        make_client("openai", "", "")
