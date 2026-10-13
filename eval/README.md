# Evaluation sets

`instructions.jsonl`: one instruction per line with the expected outcome on
the **default design**.

| Field | Meaning |
|---|---|
| `tier` | `rules`: the deterministic parser must get it right; `llm`: paraphrases the parser cannot resolve, used to score local models |
| `expect.set` | parameter → expected new value (compared after resolving, ±0.5 in the parameter's unit, so "+4 in" and "set 2801.6 mm" are equal) |
| `expect.query` | parameter or derived IDs the answer must contain |
| `expect.action` | `clarify`, `out_of_scope`, `undo` or `redo` |

Run (from `backend/`):

```bash
uv run python -m autevra.ai.evaluate                                   # parser only
uv run python -m autevra.ai.evaluate --provider ollama --model qwen3:1.7b
```

The `rules` tier is also a unit test (`tests/ai/test_evaluation.py`). Add a
line here whenever a phrasing fails in practice.
