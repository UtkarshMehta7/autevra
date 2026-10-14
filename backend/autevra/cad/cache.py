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

from autevra.cad import kernel

# Builder name -> function(inputs) -> shape, or None when the part is not fitted for these
# inputs (equipment that depends on the configuration). Filled by domain modules and plugins.
BUILDERS: dict[str, Callable[[Mapping[str, float]], kernel.Shape | None]] = {}
DEFAULT_ANGULAR = 0.3  # display mesh angular deflection, rad


def mesh_angular(builder: Callable) -> float:
    """A builder may declare ``mesh_angular`` for a coarser display mesh (a coil spring
    does not need tyre-like smoothness); the B-rep and STEP export are unaffected."""
    return float(getattr(builder, "mesh_angular", DEFAULT_ANGULAR))


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
        self._shapes: OrderedDict[str, kernel.Shape | None] = OrderedDict()
        self._meshes: dict[str, kernel.Mesh] = {}
        self._builder_of: dict[str, str] = {}
        self.max_entries = max_entries
        self.stats = CacheStats()

    def shape(self, builder: str, inputs: Mapping[str, float]) -> tuple[str, kernel.Shape | None]:
        key = geometry_key(builder, inputs)
        if key in self._shapes:
            self._shapes.move_to_end(key)
            self.stats.hits += 1
        else:
            self._shapes[key] = BUILDERS[builder](inputs)
            self._builder_of[key] = builder
            self.stats.builds.append(builder)
            while len(self._shapes) > self.max_entries:
                old, _ = self._shapes.popitem(last=False)
                self._meshes.pop(old, None)
                self._builder_of.pop(old, None)
        return key, self._shapes[key]

    def mesh(self, key: str) -> kernel.Mesh:
        if key not in self._meshes:
            builder = BUILDERS.get(self._builder_of.get(key, ""))
            angular = mesh_angular(builder) if builder else DEFAULT_ANGULAR
            self._meshes[key] = kernel.tessellate(self._shapes[key], angular=angular)
        return self._meshes[key]

    def reset_stats(self) -> None:
        self.stats = CacheStats()
