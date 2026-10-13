"""Geometry cache keyed by a hash of (builder, inputs).

Identical inputs give identical geometry, so the four wheels share one entry
and an unchanged component is never rebuilt. The cache is a bounded LRU to
keep memory low on an 8 GB machine.
"""

import hashlib
import json
from collections import OrderedDict
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from autevra.cad import components, kernel

BUILDERS: Mapping[str, Callable[[Mapping[str, float]], kernel.Shape]] = {
    "body": components.build_body,
    "frame": components.build_frame,
    "axle": components.build_axle,
    "wheel": components.build_wheel,
}


def geometry_key(builder: str, inputs: Mapping[str, float]) -> str:
    payload = json.dumps(
        {"builder": builder, "inputs": {k: round(float(v), 6) for k, v in sorted(inputs.items())}},
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class CacheStats:
    hits: int = 0
    builds: list[str] = field(default_factory=list)  # builder names, in build order


class GeometryCache:
    def __init__(self, max_entries: int = 64) -> None:
        self._shapes: OrderedDict[str, kernel.Shape] = OrderedDict()
        self._meshes: dict[str, kernel.Mesh] = {}
        self.max_entries = max_entries
        self.stats = CacheStats()

    def shape(self, builder: str, inputs: Mapping[str, float]) -> tuple[str, kernel.Shape]:
        key = geometry_key(builder, inputs)
        if key in self._shapes:
            self._shapes.move_to_end(key)
            self.stats.hits += 1
        else:
            self._shapes[key] = BUILDERS[builder](inputs)
            self.stats.builds.append(builder)
            while len(self._shapes) > self.max_entries:
                old, _ = self._shapes.popitem(last=False)
                self._meshes.pop(old, None)
        return key, self._shapes[key]

    def mesh(self, key: str) -> kernel.Mesh:
        if key not in self._meshes:
            self._meshes[key] = kernel.tessellate(self._shapes[key])
        return self._meshes[key]

    def reset_stats(self) -> None:
        self.stats = CacheStats()
