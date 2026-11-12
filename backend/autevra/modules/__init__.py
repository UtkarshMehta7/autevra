"""Engineering modules: one per product domain, kept apart.

A module registers one ``ModuleDef``: its product's options, how a configuration maps to
design values, the 150 % breakdown generated from those values, and the checks that
compare the breakdown's roll-ups with the product model. Modules never import each other;
the platform (``autevra.product``) holds the domain-neutral mechanisms.

Projects name their module through their domain (``automotive`` → land vehicles,
``aerospace`` → aircraft).
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel

from autevra.product.breakdown import Node, RolledNode
from autevra.product.loads import Compliance, LoadCase
from autevra.product.options import Configuration, Options
from autevra.product.systems import Architecture
from autevra.quality import Stack

Values = Mapping[str, Any]


class Check(BaseModel):
    id: str
    label: str
    status: Literal["pass", "warn", "fail"]
    message: str


@dataclass(frozen=True)
class ModuleDef:
    id: str
    domain: str  # the project domain hosting this module
    name: str
    frame: str  # the breakdown's axes, stated for every CG
    options: Callable[[Values], Options]
    current: Callable[[Values], dict[str, str]]  # the design's own configuration
    configure: Callable[[Values, Configuration], dict[str, Any]]  # values of a config
    breakdown: Callable[[Values], Node]  # the 150 % breakdown from (configured) values
    checks: Callable[[Values, RolledNode], list[Check]]
    architecture: Callable[[Values], Architecture] | None = None  # functions, blocks, flows
    loads: Callable[[Values], list[LoadCase]] | None = None  # the module's load cases
    compliance: Callable[[Values], list[Compliance]] | None = None  # regulation clauses
    stations: tuple[tuple[str, str], ...] = ()  # breakdown code prefix -> production station
    station_order: tuple[str, ...] = ()
    stackups: Callable[[Values], list[Stack]] | None = None  # tolerance chains of the design


_MODULES: dict[str, ModuleDef] = {}


def register(module: ModuleDef) -> None:
    _MODULES[module.id] = module


BUILTIN = (
    "autevra.modules.land",
    "autevra.modules.aircraft",
    "autevra.modules.mechanical",
    "autevra.modules.marine",
)


def _load() -> None:
    import importlib

    for name in BUILTIN:  # idempotent: importing registers the module once
        importlib.import_module(name)


def all_modules() -> list[ModuleDef]:
    _load()
    return list(_MODULES.values())


def for_domain(domain: str) -> ModuleDef | None:
    _load()
    return next((m for m in _MODULES.values() if m.domain == domain), None)


def get(module_id: str) -> ModuleDef:
    _load()
    try:
        return _MODULES[module_id]
    except KeyError:
        raise KeyError(f"unknown module '{module_id}'") from None
