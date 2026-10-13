"""Placement through mates, and the parameter -> component dependency graph."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from autevra.assembly import transforms as tf
from autevra.assembly.model import BY_ID, COMPONENTS, ComponentDef, Values
from autevra.assembly.transforms import Matrix


def ancestors(component: ComponentDef) -> list[ComponentDef]:
    """Parents from the immediate one up to the root."""
    chain, seen = [], {component.id}
    current = component
    while current.mate is not None:
        current = BY_ID[current.mate.parent]
        if current.id in seen:
            raise ValueError(f"mate cycle at '{current.id}'")
        seen.add(current.id)
        chain.append(current)
    return chain


def placement_dependencies(component: ComponentDef) -> frozenset[str]:
    """Parameters that can move ``component``: the interface frames along its mate chain."""
    deps: set[str] = set()
    current = component
    for parent in ancestors(component):
        assert current.mate is not None
        deps |= set(parent.frames[current.mate.parent_interface])
        deps |= set(current.frames[current.mate.child_interface])
        current = parent
    return frozenset(deps)


def place_all(values: Values) -> dict[str, Matrix]:
    """World matrix of every component.

    ``world(child) = world(parent) @ parent_interface @ inverse(child_interface)``
    """
    world: dict[str, Matrix] = {}
    frames = {c.id: c.resolve_interfaces(values) for c in COMPONENTS}

    def place(c: ComponentDef) -> Matrix:
        if c.id in world:
            return world[c.id]
        if c.mate is None:
            world[c.id] = tf.identity()
        else:
            parent = BY_ID[c.mate.parent]
            world[c.id] = tf.compose(
                place(parent),
                frames[parent.id][c.mate.parent_interface],
                tf.inverse(frames[c.id][c.mate.child_interface]),
            )
        return world[c.id]

    for c in COMPONENTS:
        place(c)
    return world


@dataclass(frozen=True)
class Impact:
    """Components affected by a set of changed parameters."""

    rebuild: frozenset[str]  # geometry must be regenerated
    move: frozenset[str]  # placement changes (geometry may be reused)

    @property
    def affected(self) -> frozenset[str]:
        return self.rebuild | self.move


def _index() -> tuple[Mapping[str, frozenset[str]], Mapping[str, frozenset[str]]]:
    geometry: dict[str, set[str]] = {}
    placement: dict[str, set[str]] = {}
    for c in COMPONENTS:
        if c.builder is None:
            continue
        for p in c.geometry:
            geometry.setdefault(p, set()).add(c.id)
        for p in placement_dependencies(c):
            placement.setdefault(p, set()).add(c.id)
    return (
        {k: frozenset(v) for k, v in geometry.items()},
        {k: frozenset(v) for k, v in placement.items()},
    )


GEOMETRY_INDEX: dict[str, frozenset[str]] = {}
PLACEMENT_INDEX: dict[str, frozenset[str]] = {}


def reindex() -> None:
    """Rebuild the parameter -> component indexes in place (after components change)."""
    geometry, placement = _index()
    GEOMETRY_INDEX.clear()
    GEOMETRY_INDEX.update(geometry)
    PLACEMENT_INDEX.clear()
    PLACEMENT_INDEX.update(placement)


reindex()


def impact(changed: Iterable[str]) -> Impact:
    changed = list(changed)
    rebuild = frozenset().union(*(GEOMETRY_INDEX.get(p, frozenset()) for p in changed))
    move = frozenset().union(*(PLACEMENT_INDEX.get(p, frozenset()) for p in changed))
    return Impact(rebuild=rebuild, move=move)
