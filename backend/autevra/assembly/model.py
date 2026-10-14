"""Assembly model: components, interfaces, mates and closed-loop constraints.

Domain-agnostic. Each component declares the parameters its geometry depends on
(``geometry``) and, per interface, the parameters that interface frame depends on
(``frames``). Input and interface functions receive a view of the design that contains
**only** the declared parameters, so an undeclared dependency fails loudly instead of
silently breaking selective rebuilds. Domain modules and plugins register components
through ``autevra.extensions``.
"""

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field

from autevra.assembly.transforms import Matrix

Values = Mapping[str, float]


class UndeclaredDependencyError(KeyError):
    pass


class DeclaredView(Mapping[str, float]):
    """Read-only view of a parameter set restricted to declared keys."""

    def __init__(self, values: Values, allowed: tuple[str, ...], owner: str) -> None:
        self._values, self._allowed, self._owner = values, frozenset(allowed), owner

    def __getitem__(self, key: str) -> float:
        if key not in self._allowed:
            raise UndeclaredDependencyError(f"{self._owner} reads undeclared parameter '{key}'")
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(k for k in self._values if k in self._allowed)

    def __len__(self) -> int:
        return sum(1 for _ in self)


@dataclass(frozen=True)
class Mate:
    """Places a child so its ``child_interface`` coincides with the parent's interface."""

    parent: str
    parent_interface: str
    child_interface: str


@dataclass(frozen=True)
class ComponentDef:
    id: str
    name: str
    category: str
    builder: str | None  # None for components without geometry (the vehicle root)
    geometry: tuple[str, ...] = ()
    inputs: Callable[[Values], dict[str, float]] = lambda p: {}
    frames: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    interfaces: Callable[[Values], dict[str, Matrix]] = lambda p: {}
    mate: Mate | None = None
    color: tuple[float, float, float] = (0.6, 0.6, 0.6)
    finish: str = "paint"  # display material: paint | glass | lamp | rubber | metal

    def resolve_inputs(self, values: Values) -> dict[str, float]:
        return self.inputs(DeclaredView(values, self.geometry, self.id))

    def resolve_interfaces(self, values: Values) -> dict[str, Matrix]:
        allowed = tuple({p for deps in self.frames.values() for p in deps})
        return self.interfaces(DeclaredView(values, allowed, self.id))


@dataclass(frozen=True)
class Coincidence:
    """Two interfaces that must coincide in world space (a closed loop the mates do not set).

    The dampers are placed by their lower eye; their upper eye must meet the body's shock
    tower. ``integration.check`` verifies it for every design.
    """

    a: tuple[str, str]  # (component, interface)
    b: tuple[str, str]
    tolerance: float = 0.01  # mm


# Registries (filled by domain modules and plugins).
COMPONENTS: list[ComponentDef] = []
BY_ID: dict[str, ComponentDef] = {}
COINCIDENCES: list[Coincidence] = []
# Load paths: chains of components that must be joined by mates or coincidences.
LOAD_PATHS: list[tuple[str, ...]] = []
