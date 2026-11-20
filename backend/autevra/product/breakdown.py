"""Product breakdown: product → system → subsystem → part, with maturity, mass and CG.

A module generates its product's *150 %* breakdown from the design values: every node a
variant could need, each with an applicability expression over the options. ``configure``
keeps the nodes of one configuration; ``rollup`` sums mass, CG, maturity and budgets up the
tree.

Mass of a part comes from one of three sources, always stated:

- ``allocated``: a share of its parent's budget (level 0 before any part estimate exists);
- ``estimated``: a parametric estimate from the part template, with its basis;
- ``computed``: from geometry and material (levels 2 and up).

Frame: the module states its axes (e.g. x rearward from the front axle, z up from the
ground for a road vehicle); all CG positions in one breakdown use that frame, in metres.
"""

from collections.abc import Iterator
from typing import Literal

from pydantic import BaseModel, Field

from autevra.product.options import Configuration, applies

Kind = Literal["product", "system", "subsystem", "part"]
MassSource = Literal["allocated", "estimated", "computed"]
LEVELS = ("L0 Allocation", "L1 Concept", "L2 Engineered", "L3 Manufacturable", "L4 Released")


class Node(BaseModel):
    id: str  # unique path id within the product: "body.closures.door_fl"
    name: str
    kind: Kind = "part"
    code: str = ""  # breakdown code in the module's standard (ATA 57-10, …)
    template: str = ""  # part template id (parts only)
    process: str = ""
    functions: list[str] = []
    applicability: str = ""  # over the product's options ("" = every configuration)
    instances: int = Field(1, ge=1)  # repeated identical parts (ribs, frames, rods)
    maturity: int = Field(0, ge=0, le=4)  # parts; systems report the minimum below them
    mass: float = Field(0.0, ge=0.0)  # kg, all instances together
    mass_source: MassSource = "allocated"
    basis: str = ""  # how the mass was obtained
    budget: float | None = None  # kg, the allocation this node must stay within
    cg: tuple[float, float, float] = (0.0, 0.0, 0.0)  # m, module frame
    envelope: tuple[float, float, float] = (0.0, 0.0, 0.0)  # m, one instance
    geometry: str = ""  # link to the generated geometry (component or part id), if any
    children: list["Node"] = []

    def walk(self) -> Iterator["Node"]:
        yield self
        for c in self.children:
            yield from c.walk()


class Rollup(BaseModel):
    mass: float
    cg: tuple[float, float, float]
    parts: int  # part nodes
    instances: int  # physical parts (instances counted)
    maturity: list[int]  # part-instance count per level L0..L4
    min_maturity: int
    over_budget: list[str]  # node ids whose roll-up exceeds their budget


class RolledNode(BaseModel):
    id: str
    name: str
    kind: Kind
    code: str
    template: str
    process: str
    functions: list[str]
    applicability: str
    instances: int
    maturity: int
    mass: float
    mass_source: MassSource
    basis: str
    budget: float | None
    cg: tuple[float, float, float]
    envelope: tuple[float, float, float]
    geometry: str
    rollup: Rollup
    children: list["RolledNode"]


def configure(node: Node, config: Configuration, names: set[str]) -> Node | None:
    """The node with only the descendants that apply in ``config`` (None if it does not)."""
    if not applies(node.applicability, config, names):
        return None
    kids = [c for c in (configure(k, config, names) for k in node.children) if c is not None]
    return node.model_copy(update={"children": kids})


def rollup(node: Node) -> RolledNode:
    if not node.children:
        mass = node.mass
        r = Rollup(mass=mass, cg=node.cg, parts=1 if node.kind == "part" else 0,
                   instances=node.instances if node.kind == "part" else 0,
                   maturity=[node.instances if (node.kind == "part" and i == node.maturity)
                             else 0 for i in range(5)],
                   min_maturity=node.maturity, over_budget=[])  # fmt: skip
        kids: list[RolledNode] = []
    else:
        kids = [rollup(c) for c in node.children]
        mass = sum(k.rollup.mass for k in kids)
        cg = tuple(sum(k.rollup.mass * k.rollup.cg[i] for k in kids) / mass if mass > 0
                   else 0.0 for i in range(3))  # fmt: skip
        r = Rollup(mass=mass, cg=cg,  # type: ignore[arg-type]
                   parts=sum(k.rollup.parts for k in kids),
                   instances=sum(k.rollup.instances for k in kids),
                   maturity=[sum(k.rollup.maturity[i] for k in kids) for i in range(5)],
                   min_maturity=min(k.rollup.min_maturity for k in kids),
                   over_budget=[x for k in kids for x in k.rollup.over_budget])  # fmt: skip
    if node.budget is not None and r.mass > node.budget * 1.0001:
        r.over_budget.insert(0, node.id)
    data = node.model_dump(exclude={"children"})
    if node.children:
        data["maturity"] = r.min_maturity
    return RolledNode(**data, rollup=r, children=kids)


def check_ids(node: Node) -> None:
    """Node ids must be unique within a breakdown."""
    seen: set[str] = set()
    for n in node.walk():
        if n.id in seen:
            raise ValueError(f"duplicate breakdown id '{n.id}'")
        seen.add(n.id)
