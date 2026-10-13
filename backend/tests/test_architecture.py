"""Layering: the shared core must not depend on any engineering domain."""

import ast
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "autevra"
CORE = ("core", "assembly", "cad", "engineering", "storage", "sim")


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.add(node.module)
            out |= {f"{node.module}.{a.name}" for a in node.names}
    return out


@pytest.mark.parametrize("package", CORE)
def test_core_packages_do_not_import_domains(package: str) -> None:
    offenders = {
        str(f.relative_to(PACKAGE)): sorted(
            i for i in _imports(f) if i.startswith("autevra.domains")
        )
        for f in (PACKAGE / package).rglob("*.py")
    }
    assert {k: v for k, v in offenders.items() if v} == {}


def test_core_package_imports_nothing_else_from_autevra() -> None:
    for f in (PACKAGE / "core").rglob("*.py"):
        bad = [
            i for i in _imports(f) if i.startswith("autevra.") and not i.startswith("autevra.core")
        ]
        assert bad == [], f


def test_core_registries_start_empty() -> None:
    """Run in a fresh interpreter: importing the core alone registers no engineering content."""
    import subprocess
    import sys

    code = ("from autevra.core import parameters, rules, derived; "
            "from autevra.assembly import model; from autevra.engineering import testing; "
            "print(len(parameters.REGISTRY), len(rules.RULES), len(derived.DERIVED), "
            "len(model.COMPONENTS), len(testing.DEFINITIONS))")  # fmt: skip
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.split() == ["0", "0", "0", "0", "0"]
