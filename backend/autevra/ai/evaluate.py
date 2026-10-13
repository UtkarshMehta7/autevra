"""Score instruction interpretation against ``eval/instructions.jsonl``.

Usage (from ``backend/``)::

    uv run python -m autevra.ai.evaluate [--provider ollama --model qwen3:1.7b]
"""

import argparse
import json
import time
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

from autevra.ai.interpreter import interpret
from autevra.ai.llm.clients import LLMClient, make_client
from autevra.ai.rule_parser import Interpretation, Kind
from autevra.core.commands import CommandError, resolve
from autevra.core.parameters import default_values
from autevra.core.rules import validate

DATASET = Path(__file__).resolve().parents[3] / "eval" / "instructions.jsonl"
TOLERANCE = 0.5


@dataclass
class Case:
    tier: str
    text: str
    expect: dict


@dataclass
class Outcome:
    tier: str
    text: str
    passed: bool
    got: str
    interpreted_by: str
    seconds: float

    @property
    def unsafe(self) -> bool:
        """A wrong, valid-looking change: only the user's confirmation would stop it."""
        return not self.passed and self.got.startswith("set ")


def load(path: Path = DATASET) -> list[Case]:
    lines = path.read_text().splitlines()
    return [Case(**json.loads(line)) for line in lines if line.strip()]


def _describe(result: Interpretation, values: dict[str, float]) -> tuple[str, dict]:
    match result.kind:
        case Kind.COMMAND | Kind.PROPOSAL:
            assert result.command is not None
            try:
                changed = resolve(result.command, values)
            except CommandError as exc:
                return "invalid", {"error": str(exc)}
            violations = validate(values | changed)
            if violations:
                # Wrong, but the validation layer would have refused it: safe.
                return "rejected", {"rule": violations[0].rule} | changed
            return "set", changed
        case Kind.QUERY:
            return "query", {"ids": list(result.query)}
        case Kind.CLARIFICATION:
            return "clarify", {}
        case Kind.OUT_OF_SCOPE:
            return "out_of_scope", {}
        case Kind.UNDO | Kind.REDO:
            return result.kind.value, {}
    return result.kind.value, {}  # pragma: no cover


def check(case: Case, result: Interpretation) -> tuple[bool, str]:
    values = default_values()
    action, detail = _describe(result, values)
    got = f"{action} {json.dumps(detail)}" if detail else action
    expect = case.expect
    if "set" in expect:
        ok = (
            action == "set"
            and set(detail) == set(expect["set"])
            and all(abs(detail[k] - v) <= TOLERANCE for k, v in expect["set"].items())
        )
    elif "query" in expect:
        ok = action == "query" and set(expect["query"]) <= set(detail.get("ids", []))
    else:
        ok = action == expect["action"]
    return ok, got


def run(cases: Iterable[Case], llm: LLMClient | None = None) -> list[Outcome]:
    outcomes = []
    for case in cases:
        start = time.perf_counter()
        result = interpret(case.text, default_values(), llm)
        seconds = time.perf_counter() - start
        ok, got = check(case, result)
        outcomes.append(Outcome(case.tier, case.text, ok, got, result.interpreted_by, seconds))
    return outcomes


def summary(outcomes: list[Outcome]) -> dict:
    out: dict = {}
    for tier in sorted({o.tier for o in outcomes}):
        rows = [o for o in outcomes if o.tier == tier]
        llm_rows = [o for o in rows if o.interpreted_by == "llm"]
        out[tier] = {
            "passed": sum(o.passed for o in rows),
            "total": len(rows),
            "accuracy": round(sum(o.passed for o in rows) / len(rows), 3),
            "wrong_but_valid": sum(o.unsafe for o in rows),
            "llm_calls": len(llm_rows),
            "mean_llm_seconds": round(sum(o.seconds for o in llm_rows) / len(llm_rows), 2)
            if llm_rows
            else 0.0,
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--provider", default="off", help="off | ollama | llama_server")
    parser.add_argument("--url", default="http://127.0.0.1:11434")
    parser.add_argument("--model", default="qwen3:1.7b")
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--tier", default=None, help="only run this tier")
    parser.add_argument("--json", type=Path, default=None, help="write full results here")
    args = parser.parse_args()

    llm = make_client(args.provider, args.url, args.model, timeout=120)
    if args.provider != "off":
        status = llm.status()
        if not status.available:
            raise SystemExit(f"LLM not available: {status.detail}")
    cases = [c for c in load(args.dataset) if args.tier in (None, c.tier)]
    outcomes = run(cases, llm)
    for o in outcomes:
        mark = "PASS" if o.passed else ("WRONG" if o.unsafe else "MISS")
        print(
            f"{mark} [{o.tier:5}] [{o.interpreted_by:5}] {o.seconds:5.2f}s  {o.text}  ->  {o.got}"
        )
    result = {
        "provider": args.provider,
        "model": args.model if args.provider != "off" else "",
        "summary": summary(outcomes),
    }
    print(json.dumps(result, indent=2))
    if args.json:
        args.json.write_text(
            json.dumps(result | {"outcomes": [asdict(o) for o in outcomes]}, indent=2)
        )


if __name__ == "__main__":
    main()
