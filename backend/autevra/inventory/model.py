"""Inventory items: versioned engineering items with typed ports, properties, performance
and a regenerable definition (a Part Design document)."""

from typing import Any, Literal

from pydantic import BaseModel, Field

PortKind = Literal["mechanical.shaft", "mechanical.bore", "mechanical.seat", "mechanical.thread",
                   "mechanical.end", "mechanical.mount"]  # fmt: skip


class Port(BaseModel):
    """A typed interface with a frame (mm, degrees) in the item's own coordinates."""

    name: str
    kind: PortKind
    at: dict[str, float] = {}  # x, y, z, rx, ry, rz
    attributes: dict[str, float | str] = {}


class Item(BaseModel):
    id: str  # stable across versions: "iso4762-m10x40"
    version: str = "1.0.0"
    kind: Literal["standard", "part", "product"] = "standard"
    family: str  # "Socket head cap screw"
    category: str  # "Fasteners", "Bearings", "Profiles"
    name: str
    standard: str = ""  # "ISO 4762", "ISO 15 (boundary dimensions)"
    status: Literal["working", "released"] = "released"
    parameters: dict[str, float | str] = {}
    properties: dict[str, float | str] = {}  # mass_kg, material, ...
    performance: dict[str, float] = {}
    maps: dict[str, list[dict[str, float]]] = {}  # published curves (e.g. torque vs speed)
    ports: list[Port] = []
    definition: dict[str, Any] = Field(default_factory=dict)  # Part Design document
    notes: list[str] = []  # stated sources and limits
    provenance: str = "Autevra standard library"


class ItemSummary(BaseModel):
    id: str
    version: str
    kind: str
    family: str
    category: str
    name: str
    standard: str
    mass_kg: float | None


def summary(item: Item) -> ItemSummary:
    mass = item.properties.get("mass_kg")
    return ItemSummary(id=item.id, version=item.version, kind=item.kind, family=item.family,
                       category=item.category, name=item.name, standard=item.standard,
                       mass_kg=float(mass) if isinstance(mass, int | float) else None)  # fmt: skip
