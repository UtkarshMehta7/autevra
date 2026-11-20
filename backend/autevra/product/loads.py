"""Load cases and compliance rows (domain-neutral).

A load case is computed by a module from its product model and distributed to named
locations (interfaces, hardpoints, components), so a part's sizing records which case
governed it. A compliance row ties a regulation clause (a reference plus our own wording,
never the regulation's text) to a requirement, its means of compliance, the evidence and a
status."""

from typing import Literal

from pydantic import BaseModel


class LoadAt(BaseModel):
    """Forces (N) and moments (N·m) at one location, in the module's frame."""

    location: str
    fx: float = 0.0
    fy: float = 0.0
    fz: float = 0.0
    mx: float = 0.0
    my: float = 0.0
    mz: float = 0.0


class LoadCase(BaseModel):
    id: str
    name: str
    kind: Literal["limit", "ultimate", "fatigue", "operating"] = "limit"
    method: str  # how it was derived, with its source
    factors: dict[str, float] = {}  # load factors in g or the case's own parameters
    loads: list[LoadAt] = []
    results: dict[str, float] = {}  # summary values (e.g. root bending moment)


class Compliance(BaseModel):
    clause: str  # reference only, e.g. "CS-23 Amdt 4, 23.337"
    requirement: str  # our wording of what must be shown
    means: Literal["analysis", "test", "inspection", "similarity"]
    evidence: str  # the analysis result or what is still needed
    status: Literal["shown", "not shown", "open"]
