"""Starting-point parts from several domains (``presets.json``), each a valid part document
that builds; the studio offers them under "New part"."""

import json
from functools import cache
from pathlib import Path

from autevra.part.features import PartDoc

PRESETS_FILE = Path(__file__).with_name("presets.json")


@cache
def presets() -> dict[str, PartDoc]:
    data = json.loads(PRESETS_FILE.read_text())
    return {name: PartDoc.model_validate(doc) for name, doc in data.items()}
