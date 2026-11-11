"""Systems layer: functions → logical blocks → physical parts, typed flows between blocks,
interface control rows, allocation and trace checks, and design FMEA rows.

- A **function** is what the product must do ("decelerate the vehicle"); functions form a
  tree and may reference requirement keys.
- A **block** is a logical system element ("hydraulic modulator") that performs functions
  and is realised by part templates of the module's breakdown.
- A **flow** is something that crosses from one block to another, typed: mechanical
  (force, torque, motion), electrical power, signal, fluid or thermal.
- A **failure mode** sits on a function and a block, rated for severity, occurrence and
  detection (1-10 each).

Nothing here knows a domain: modules supply the architecture (``autevra.modules``).
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from autevra.product.breakdown import Node
from autevra.product.options import Configuration, applies

FlowKind = Literal["mechanical", "electrical_power", "signal", "fluid", "thermal"]
FLOW_KINDS: tuple[str, ...] = ("mechanical", "electrical_power", "signal", "fluid", "thermal")


class Function(BaseModel):
    id: str
    name: str
    parent: str = ""
    requirements: list[str] = []  # requirement keys or references traced to this function


class Block(BaseModel):
    id: str
    name: str
    functions: list[str]
    templates: list[str]  # part templates of the module realising this block
    applicability: str = ""  # over the product's options
    external: bool = False  # outside the product (driver, road, air): no parts expected


class Flow(BaseModel):
    id: str
    kind: FlowKind
    source: str
    target: str
    item: str  # what flows: "brake pressure", "wheel speed", "hinge moment"
    attributes: dict[str, str] = {}  # agreed values for the interface control document
    applicability: str = ""


class FailureMode(BaseModel):
    id: str
    function: str
    block: str
    mode: str
    effect: str
    severity: int = Field(ge=1, le=10)
    occurrence: int = Field(ge=1, le=10)
    detection: int = Field(ge=1, le=10)
    action: str = ""

    @property
    def rpn(self) -> int:
        return self.severity * self.occurrence * self.detection

    @property
    def priority(self) -> Literal["high", "medium", "low"]:
        """Simplified action priority (a stated simplification, not the AIAG-VDA table):
        high when severity is 9-10 with occurrence 4+ or detection 7+, or RPN 200+;
        medium when severity is 7+ or RPN 100+; otherwise low."""
        s, o, d = self.severity, self.occurrence, self.detection
        if (s >= 9 and (o >= 4 or d >= 7)) or self.rpn >= 200:
            return "high"
        if s >= 7 or self.rpn >= 100:
            return "medium"
        return "low"


class Architecture(BaseModel):
    functions: list[Function]
    blocks: list[Block]
    flows: list[Flow]
    failure_modes: list[FailureMode] = []

    @model_validator(mode="after")
    def _consistent(self) -> "Architecture":
        fids = [f.id for f in self.functions]
        bids = [b.id for b in self.blocks]
        for ids, what in ((fids, "function"), (bids, "block"),
                          ([f.id for f in self.flows], "flow"),
                          ([m.id for m in self.failure_modes], "failure mode")):  # fmt: skip
            dup = {i for i in ids if ids.count(i) > 1}
            if dup:
                raise ValueError(f"duplicate {what} ids: {sorted(dup)}")
        fset, bset = set(fids), set(bids)
        for f in self.functions:
            if f.parent and f.parent not in fset:
                raise ValueError(f"function '{f.id}': unknown parent '{f.parent}'")
        for b in self.blocks:
            bad = [x for x in b.functions if x not in fset]
            if bad:
                raise ValueError(f"block '{b.id}': unknown functions {bad}")
        for fl in self.flows:
            for end in (fl.source, fl.target):
                if end not in bset:
                    raise ValueError(f"flow '{fl.id}': unknown block '{end}'")
        for m in self.failure_modes:
            if m.function not in fset or m.block not in bset:
                raise ValueError(f"failure mode '{m.id}': unknown function or block")
        return self

    def configured(self, config: Configuration, names: set[str]) -> "Architecture":
        """The blocks and flows that exist in one configuration."""
        blocks = [b for b in self.blocks if applies(b.applicability, config, names)]
        ids = {b.id for b in blocks}
        flows = [f for f in self.flows if applies(f.applicability, config, names)
                 and f.source in ids and f.target in ids]  # fmt: skip
        modes = [m for m in self.failure_modes if m.block in ids]
        return Architecture(functions=self.functions, blocks=blocks, flows=flows,
                            failure_modes=modes)  # fmt: skip


class TraceIssue(BaseModel):
    kind: Literal["unallocated_function", "unrealised_block", "orphan_part",
                  "unmitigated_failure", "unallocated_requirement"]  # fmt: skip
    subject: str
    message: str
    severity: Literal["fail", "warn"]


class ChainStep(BaseModel):
    block: str
    name: str
    external: bool
    parts: list[dict]  # {id, name, mass, maturity, instances}
    flows_out: list[Flow]


def _leaves(node: Node) -> list[Node]:
    return [n for n in node.walk() if n.kind == "part"]


def trace(arch: Architecture, breakdown: Node,
          requirements: list[str] | None = None) -> list[TraceIssue]:  # fmt: skip
    """Allocation gaps between the layers, for one configured breakdown."""
    issues: list[TraceIssue] = []
    parts = _leaves(breakdown)
    present = {p.template for p in parts}
    children = {f.parent for f in arch.functions if f.parent}
    performed = {fid for b in arch.blocks for fid in b.functions}
    names = {f.id: f.name for f in arch.functions}
    for f in arch.functions:
        if f.id not in children and f.id not in performed:
            issues.append(TraceIssue(kind="unallocated_function", subject=f.id, severity="fail",
                                     message=f"no block performs '{f.name}'"))  # fmt: skip
    for b in arch.blocks:
        if not b.external and not (set(b.templates) & present):
            issues.append(TraceIssue(kind="unrealised_block", subject=b.id, severity="fail",
                                     message=f"no part in this configuration realises "
                                     f"'{b.name}'"))  # fmt: skip
    realised = {t for b in arch.blocks for t in b.templates}
    for p in parts:
        if p.template and p.template not in realised:
            issues.append(TraceIssue(kind="orphan_part", subject=p.id, severity="warn",
                                     message=f"'{p.name}' realises no logical block"))  # fmt: skip
    for m in arch.failure_modes:
        if m.priority == "high" and not m.action:
            issues.append(
                TraceIssue(
                    kind="unmitigated_failure",
                    subject=m.id,
                    severity="fail",
                    message=f"high-priority failure '{m.mode}' of "
                    f"{names.get(m.function, m.function)} has no action",
                )
            )
    if requirements:
        traced = {r for f in arch.functions for r in f.requirements}
        for r in requirements:
            if r not in traced:
                issues.append(TraceIssue(kind="unallocated_requirement", subject=r,
                                         severity="warn",
                                         message=f"requirement {r} is not allocated to a "
                                         "function"))  # fmt: skip
    return issues


def chain(arch: Architecture, function: str, breakdown: Node) -> list[ChainStep]:
    """The blocks that perform a function (or any of its sub-functions), ordered along their
    flows, each with the parts that realise it in the configured breakdown."""
    sub = {function}
    grew = True
    while grew:
        more = {f.id for f in arch.functions if f.parent in sub} - sub
        grew = bool(more)
        sub |= more
    blocks = [b for b in arch.blocks if set(b.functions) & sub]
    ids = {b.id for b in blocks}
    # the outside world the chain starts from or acts on (driver, road, air)
    ends = {f.source for f in arch.flows if f.target in ids} | {
        f.target for f in arch.flows if f.source in ids
    }
    outside = [b for b in arch.blocks if b.external and b.id in ends and b.id not in ids]
    blocks = outside + blocks  # inputs from outside lead the order
    ids = {b.id for b in blocks}
    sinks = {b.id for b in outside if any(f.source in ids and f.target == b.id
                                          for f in arch.flows)}  # fmt: skip
    flows = [f for f in arch.flows if f.source in ids and f.target in ids]
    ordering = [f for f in flows if f.source not in sinks]  # what the chain acts on comes last
    # order: Kahn's algorithm on the flows inside the chain (cycles keep definition order)
    incoming = {b.id: 0 for b in blocks}
    for f in ordering:
        incoming[f.target] += 1
    order: list[str] = []
    ready = [b.id for b in blocks if incoming[b.id] == 0]
    while ready:
        bid = ready.pop(0)
        order.append(bid)
        for f in ordering:
            if f.source == bid:
                incoming[f.target] -= 1
                if incoming[f.target] == 0:
                    ready.append(f.target)
    order += [b.id for b in blocks if b.id not in order]
    by_id = {b.id: b for b in blocks}
    parts = _leaves(breakdown)
    steps = []
    for bid in order:
        b = by_id[bid]
        mine = [{"id": p.id, "name": p.name, "mass": p.mass, "maturity": p.maturity,
                 "instances": p.instances} for p in parts if p.template in b.templates]  # fmt: skip
        steps.append(ChainStep(block=bid, name=b.name, external=b.external, parts=mine,
                               flows_out=[f for f in flows if f.source == bid]))  # fmt: skip
    return steps


class IcdRow(BaseModel):
    flow: str
    kind: FlowKind
    source: str
    target: str
    item: str
    attributes: dict[str, str]


def icd(arch: Architecture) -> list[IcdRow]:
    """Interface control rows: every flow between two blocks, with its agreed values."""
    names = {b.id: b.name for b in arch.blocks}
    return [IcdRow(flow=f.id, kind=f.kind, source=names[f.source], target=names[f.target],
                   item=f.item, attributes=f.attributes) for f in arch.flows]  # fmt: skip
