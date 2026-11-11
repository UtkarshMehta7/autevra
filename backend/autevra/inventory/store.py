"""Published items and where-used, kept as JSON files in the data folder (local-first;
the same records move to the database when the inventory is shared by a team).

data/inventory/items/<id>/<version>.json   one immutable file per released version
data/inventory/usage.json                  installations: item, version, project, part
"""

import json
import re
from pathlib import Path

from autevra.inventory.model import Item
from autevra.inventory.standard import catalogue

_SAFE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,80}$")


class InventoryError(ValueError):
    pass


class Inventory:
    def __init__(self, root: Path) -> None:
        self.root = Path(root) / "inventory"
        (self.root / "items").mkdir(parents=True, exist_ok=True)

    # --- items ---------------------------------------------------------------------------
    def _versions(self, item_id: str) -> list[str]:
        folder = self.root / "items" / item_id
        if not folder.is_dir():
            return []
        versions = [p.stem for p in folder.glob("*.json")]
        return sorted(versions, key=lambda v: tuple(int(x) for x in v.split(".")))

    def published(self) -> list[Item]:
        out = []
        for folder in sorted((self.root / "items").iterdir()):
            versions = self._versions(folder.name)
            if versions:
                out.append(self.get(folder.name, versions[-1]))
        return out

    def all(self) -> list[Item]:
        return [*catalogue().values(), *self.published()]

    def get(self, item_id: str, version: str | None = None) -> Item:
        standard = catalogue().get(item_id)
        if standard is not None:
            return standard
        if not _SAFE.match(item_id):
            raise InventoryError(f"no item '{item_id}'")
        versions = self._versions(item_id)
        if not versions or (version is not None and version not in versions):
            raise InventoryError(f"no item '{item_id}'" + (f" version {version}" if version
                                                          else ""))  # fmt: skip
        path = self.root / "items" / item_id / f"{version or versions[-1]}.json"
        return Item.model_validate_json(path.read_text())

    def publish(self, item: Item) -> Item:
        """Release a new version (major.minor.patch, minor bumped) of a user item."""
        if item.id in catalogue():
            raise InventoryError("standard items cannot be overwritten")
        if not _SAFE.match(item.id):
            raise InventoryError(f"invalid item id '{item.id}'")
        versions = self._versions(item.id)
        major, minor, _ = (int(x) for x in (versions[-1] if versions else "1.-1.0").split("."))
        released = item.model_copy(update={"version": f"{major}.{minor + 1}.0",
                                           "status": "released"})  # fmt: skip
        folder = self.root / "items" / item.id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{released.version}.json").write_text(released.model_dump_json(indent=1))
        return released

    # --- where-used ----------------------------------------------------------------------
    def _usage_path(self) -> Path:
        return self.root / "usage.json"

    def usage(self, item_id: str | None = None) -> list[dict[str, str]]:
        path = self._usage_path()
        rows = json.loads(path.read_text()) if path.exists() else []
        return [r for r in rows if item_id is None or r["item"] == item_id]

    def record(self, item: Item, project: str, part: str) -> None:
        rows = self.usage()
        rows.append({"item": item.id, "version": item.version, "project": project,
                     "part": part})  # fmt: skip
        self._usage_path().write_text(json.dumps(rows, indent=1))
