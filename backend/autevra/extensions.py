"""Extension API: add parameters, CAD components, rules, checks and tests as a plugin.

A plugin is one ``Plugin`` object. ``register(plugin)`` adds everything it declares to the
same registries the built-in model uses, so new parameters appear in the editor, the
parser, the LLM prompt and the API; new components are built, placed by their mates,
exported to STEP and checked for clearances; new tests run on the test bench and feed
requirements, diagnosis and optimisation. Nothing in the core is edited.

Plugins are discovered from the ``autevra.plugins`` entry-point group (the standard Python
mechanism, declared in the plugin package's ``pyproject.toml``) and from the
``AUTEVRA_PLUGINS`` setting (comma-separated module paths, each exposing ``PLUGIN``).

``register`` validates before it changes anything: identifiers must be new, components
must reference known builders and mate to existing interfaces, every component must read
only parameters it declares, and the default design must still satisfy every rule.
"""

import importlib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from importlib.metadata import entry_points

from autevra.ai import lexicon
from autevra.assembly import graph
from autevra.assembly import model as vehicle
from autevra.assembly.model import Coincidence, ComponentDef
from autevra.cad import cache
from autevra.core import derived, parameters, rules
from autevra.core.derived import DerivedDef
from autevra.core.parameters import ParameterDef
from autevra.core.rules import Rule
from autevra.engineering import integration, testing
from autevra.engineering.integration import Clearance
from autevra.engineering.testing import TestDefinition

ENTRY_POINT_GROUP = "autevra.plugins"


class PluginError(ValueError):
    pass


@dataclass(frozen=True)
class Plugin:
    name: str
    version: str = "0.1.0"
    description: str = ""
    parameters: Sequence[ParameterDef] = ()
    group_aliases: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    derived: Sequence[tuple[DerivedDef, Callable[[Mapping[str, float]], float]]] = ()
    rules: Sequence[tuple[Rule, Callable[[Mapping[str, float]], str | None]]] = ()
    builders: Mapping[str, Callable] = field(default_factory=dict)
    components: Sequence[ComponentDef] = ()
    coincidences: Sequence[Coincidence] = ()
    load_paths: Sequence[tuple[str, ...]] = ()
    compatible_interfaces: Sequence[tuple[str, str]] = ()
    clearances: Sequence[Clearance] = ()
    tests: Sequence[TestDefinition] = ()
    integration_checks: Sequence[Callable] = ()  # values -> list of integration Checks
    notes: Sequence[str] = ()  # stated limitations of what is checked


LOADED: dict[str, Plugin] = {}


def _check(plugin: Plugin) -> None:
    if plugin.name in LOADED:
        raise PluginError(f"plugin '{plugin.name}' is already registered")
    clashes = (
        [p.id for p in plugin.parameters if p.id in parameters.REGISTRY]
        + [d.id for d, _ in plugin.derived if d.id in derived.DERIVED]
        + [r.id for r, _ in plugin.rules if r.id in {x.id for x in rules.RULES}]
        + [b for b in plugin.builders if b in cache.BUILDERS]
        + [c.id for c in plugin.components if c.id in vehicle.BY_ID]
        + [t.id for t in plugin.tests if t.id in testing.DEFINITIONS]
    )
    if clashes:
        raise PluginError(f"identifiers already in use: {', '.join(clashes)}")
    for c in plugin.components:
        if c.builder is not None and c.builder not in cache.BUILDERS | dict(plugin.builders):
            raise PluginError(f"component '{c.id}' uses unknown builder '{c.builder}'")
        if c.mate is not None:
            parent = vehicle.BY_ID.get(c.mate.parent) or next(
                (x for x in plugin.components if x.id == c.mate.parent), None
            )
            if parent is None or c.mate.parent_interface not in parent.frames:
                raise PluginError(f"component '{c.id}' mates to an unknown interface")


def register(plugin: Plugin) -> Plugin:
    """Add a plugin to the live registries (validated first; rolled back on failure)."""
    _check(plugin)
    LOADED[plugin.name] = plugin
    try:
        for p in plugin.parameters:
            parameters.REGISTRY[p.id] = p
        parameters.GROUP_ALIASES.update(plugin.group_aliases)
        for d, fn in plugin.derived:
            derived._DERIVED[d.id] = (d, fn)
            derived.DERIVED[d.id] = d
        for r, fn in plugin.rules:
            rules._RULES.append((r, fn))
            rules.RULES.append(r)
        cache.BUILDERS.update(plugin.builders)
        for c in plugin.components:
            vehicle.COMPONENTS.append(c)
            vehicle.BY_ID[c.id] = c
        vehicle.COINCIDENCES.extend(plugin.coincidences)
        vehicle.LOAD_PATHS.extend(plugin.load_paths)
        integration.COMPATIBLE.update(plugin.compatible_interfaces)
        integration.CLEARANCES.extend(plugin.clearances)
        integration.DOMAIN_CHECKS.extend(plugin.integration_checks)
        integration.NOT_CHECKED.extend(plugin.notes)
        for t in plugin.tests:
            testing.DEFINITIONS[t.id] = t
        graph.reindex()
        lexicon.rebuild()
        _verify()
    except Exception:
        unregister(plugin.name)
        raise
    return plugin


def _verify() -> None:
    values = parameters.default_values()
    if not values:
        return
    for c in vehicle.COMPONENTS:  # raises UndeclaredDependencyError on undeclared reads
        c.resolve_inputs(values)
        c.resolve_interfaces(values)
    violations = rules.validate(values)
    if violations:
        raise PluginError("the default design breaks: " + "; ".join(v.message for v in violations))


def unregister(name: str) -> None:
    """Remove everything a plugin added."""
    plugin = LOADED.pop(name, None)
    if plugin is None:
        return
    for p in plugin.parameters:
        parameters.REGISTRY.pop(p.id, None)
    for alias in plugin.group_aliases:
        parameters.GROUP_ALIASES.pop(alias, None)
    for d, _ in plugin.derived:
        derived._DERIVED.pop(d.id, None)
        derived.DERIVED.pop(d.id, None)
    ids = {r.id for r, _ in plugin.rules}
    rules._RULES[:] = [x for x in rules._RULES if x[0].id not in ids]
    rules.RULES[:] = [r for r in rules.RULES if r.id not in ids]
    for b in plugin.builders:
        cache.BUILDERS.pop(b, None)
    cids = {c.id for c in plugin.components}
    vehicle.COMPONENTS[:] = [c for c in vehicle.COMPONENTS if c.id not in cids]
    for cid in cids:
        vehicle.BY_ID.pop(cid, None)
    vehicle.COINCIDENCES[:] = [x for x in vehicle.COINCIDENCES if x not in plugin.coincidences]
    vehicle.LOAD_PATHS[:] = [x for x in vehicle.LOAD_PATHS if x not in plugin.load_paths]
    integration.COMPATIBLE.difference_update(plugin.compatible_interfaces)
    integration.CLEARANCES[:] = [x for x in integration.CLEARANCES if x not in plugin.clearances]
    integration.DOMAIN_CHECKS[:] = [
        x for x in integration.DOMAIN_CHECKS if x not in plugin.integration_checks
    ]
    integration.NOT_CHECKED[:] = [x for x in integration.NOT_CHECKED if x not in plugin.notes]
    for t in plugin.tests:
        testing.DEFINITIONS.pop(t.id, None)
    graph.reindex()
    lexicon.rebuild()


def load(modules: Sequence[str] = (), use_entry_points: bool = True) -> list[str]:
    """Register plugins from module paths (each exposing ``PLUGIN``) and entry points."""
    found: list[Plugin] = []
    for path in modules:
        found.append(importlib.import_module(path).PLUGIN)
    if use_entry_points:
        for ep in entry_points(group=ENTRY_POINT_GROUP):
            obj = ep.load()
            found.append(obj if isinstance(obj, Plugin) else obj.PLUGIN)
    names = []
    for plugin in found:
        if plugin.name not in LOADED:
            register(plugin)
            names.append(plugin.name)
    return names
