"""Fault trees generated from the logical architecture, quantified with generic failure
rates.

The top event "loss of F" is an OR over the blocks performing F or any of its sub-functions
(a series model: no redundancy credit unless a block is marked as duplicated), and a
block's failure is an OR over the failure of its parts' instances. For rare events the OR
rates add: lambda_top = sum(lambda_i). Probability over an exposure time t:
P = 1 - exp(-lambda t).

Generic part failure rates by process, per 10^6 hours (indicative ballparks of the kind
found in published reliability handbooks; a real assessment uses component data):
structure-like processes (sheet metal, extrusion, weldment, glass) 0.05; castings and
forgings 0.2; machined parts 0.5; moulded parts 0.3; tubes and hoses 1.0; assemblies 3.0;
bought-in standard parts 1.0; bought-in equipment (inventory) 10.
"""

import math

from pydantic import BaseModel

from autevra.product.breakdown import Node
from autevra.product.systems import Architecture

RATE_PER_1E6_H = {"sheet metal": 0.05, "extrusion": 0.05, "weldment": 0.05, "glass": 0.05,
                  "composite": 0.05, "casting": 0.2, "forging": 0.2, "machining": 0.5,
                  "moulding": 0.3, "tube": 1.0, "assembly": 3.0, "standard": 1.0,
                  "inventory": 10.0, "additive": 0.5}  # fmt: skip


class Basic(BaseModel):
    part: str
    name: str
    instances: int
    rate_per_h: float


class Gate(BaseModel):
    block: str
    name: str
    rate_per_h: float
    basics: list[Basic]
    importance: float  # share of the top event's rate


class FaultTree(BaseModel):
    function: str
    top_event: str
    rate_per_h: float
    probability: float  # over the exposure time
    exposure_h: float
    gates: list[Gate]


def fault_tree(arch: Architecture, root: Node, function: str, exposure_h: float = 1.0
               ) -> FaultTree:  # fmt: skip
    funcs = {f.id: f for f in arch.functions}
    if function not in funcs:
        raise KeyError(f"no function '{function}'")
    sub, grew = {function}, True
    while grew:
        more = {f.id for f in arch.functions if f.parent in sub} - sub
        grew = bool(more)
        sub |= more
    parts = [n for n in root.walk() if n.kind == "part"]
    gates = []
    for b in arch.blocks:
        if b.external or not set(b.functions) & sub:
            continue
        basics = [Basic(part=p.id, name=p.name, instances=p.instances,
                        rate_per_h=p.instances * RATE_PER_1E6_H.get(p.process, 1.0) * 1e-6)
                  for p in parts if p.template in b.templates]  # fmt: skip
        gates.append(Gate(block=b.id, name=b.name, basics=basics, importance=0.0,
                          rate_per_h=sum(x.rate_per_h for x in basics)))  # fmt: skip
    top = sum(g.rate_per_h for g in gates)
    for g in gates:
        g.importance = g.rate_per_h / top if top else 0.0
    gates.sort(key=lambda g: g.rate_per_h, reverse=True)
    return FaultTree(function=function, top_event=f"loss of {funcs[function].name}",
                     rate_per_h=top, probability=1 - math.exp(-top * exposure_h),
                     exposure_h=exposure_h, gates=gates)  # fmt: skip


# targets per hour by severity, stated: CS-23 Class I aeroplanes (AC 23.1309-1E) and the
# ISO 26262 random-hardware-failure metric for road vehicles
TARGETS = {
    "aircraft": {"catastrophic": 1e-6, "hazardous": 1e-5, "major": 1e-4, "minor": 1e-3},
    "land": {"catastrophic": 1e-8, "hazardous": 1e-7, "major": 1e-7, "minor": 1e-6},
}


def severity_class(severity: int) -> str:
    return ("catastrophic" if severity >= 10 else "hazardous" if severity >= 9 else
            "major" if severity >= 7 else "minor")  # fmt: skip
