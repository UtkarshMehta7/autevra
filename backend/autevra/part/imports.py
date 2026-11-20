"""The import store: STEP files kept by their SHA-256 so imported parts stay reproducible.

The store's folder is set once at start-up (``configure``); imported B-reps are cached per
file. A STEP file is accepted only if it parses into at least one solid."""

import hashlib
from functools import lru_cache
from pathlib import Path

import cadquery as cq

_ROOT: list[Path] = [Path("data") / "imports"]
MAX_BYTES = 50 * 1024 * 1024


def configure(root: Path) -> None:
    _ROOT[0] = Path(root)
    _ROOT[0].mkdir(parents=True, exist_ok=True)
    shape.cache_clear()


def path(sha: str) -> Path:
    return _ROOT[0] / f"{sha}.step"


def store(data: bytes) -> tuple[str, int]:
    """Keep a STEP file; returns (sha256, number of solids). Raises ValueError if the bytes
    are not a STEP file with at least one solid."""
    if len(data) > MAX_BYTES:
        raise ValueError("STEP files are limited to 50 MB")
    if b"ISO-10303-21" not in data[:200]:
        raise ValueError("not a STEP (ISO 10303-21) file")
    sha = hashlib.sha256(data).hexdigest()
    target = path(sha)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(data)
    try:
        solids = len(shape(sha).Solids())
    except Exception as exc:  # noqa: BLE001 (OCCT raises assorted errors on bad files)
        target.unlink(missing_ok=True)
        shape.cache_clear()
        raise ValueError(f"cannot read the STEP file: {exc}") from None
    if solids == 0:
        target.unlink(missing_ok=True)
        shape.cache_clear()
        raise ValueError("the STEP file contains no solids")
    return sha, solids


@lru_cache(maxsize=64)
def shape(sha: str) -> cq.Shape:
    p = path(sha)
    if not p.exists():
        raise ValueError(f"imported file {sha[:12]} is not in the import store")
    vals = cq.importers.importStep(str(p)).vals()
    return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)
