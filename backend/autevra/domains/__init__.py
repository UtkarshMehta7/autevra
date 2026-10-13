"""Engineering domain registry.

A domain declares what it actually implements: component library, engineering operations,
simulations, exchange formats and dependencies. Statuses are evidence-based:

- ``available``: implemented, tested and usable end to end;
- ``experimental``: usable, partially tested;
- ``in_development``: work started, not usable yet;
- ``unavailable``: on the roadmap only.

Only available or experimental domains can host projects. The automotive lists are
computed from the live registries, so plugins that add components or tests show up here.
"""

from typing import Literal

from pydantic import BaseModel

Status = Literal["available", "experimental", "in_development", "unavailable"]


class DomainDef(BaseModel):
    id: str
    name: str
    description: str
    status: Status
    component_library: list[str] = []
    operations: list[str] = []
    simulations: list[str] = []
    formats: list[str] = []
    dependencies: list[str] = []
    version: str = "0"
    roadmap: list[str] = []
    evidence: str = ""


def _automotive() -> DomainDef:
    from autevra import __version__
    from autevra.assembly.vehicle import COMPONENTS
    from autevra.engineering.testing import DEFINITIONS

    categories = sorted({c.category for c in COMPONENTS if c.builder})
    return DomainDef(
        id="automotive", name="Automotive",
        description="Road vehicles on a ladder-frame template: body, frame, beam axles, "
        "wheels, coil-over dampers (plus plugin components), with suspension, longitudinal "
        "performance and packaging analysis.",
        status="available", version=__version__,
        component_library=categories,
        operations=["set / increase / decrease / scale parameters", "undo / redo",
                    "impact preview", "run tests", "diagnose failures", "optimise",
                    "engineering loop", "requirements", "specification interview"],
        simulations=[f"{t.name} ({t.credibility.value.replace('_', ' ')})"
                     for t in DEFINITIONS.values()],
        formats=["STEP AP214 export", "ReqIF 1.2 import/export"],
        dependencies=["cadquery 2.8 / OCCT 7.9"],
        roadmap=["half-car and full-vehicle dynamics", "Magic Formula tyres", "steering and "
                 "brakes library", "electrified powertrain energy"],
        evidence="covered by the backend test suite and checked in the workspace",
    )  # fmt: skip


_PLANNED: tuple[tuple[str, str, str, list[str]], ...] = (
    ("motorcycles", "Motorcycles and personal mobility",
     "Two-wheelers, scooters and micromobility.", ["frame and fork geometry", "rider model"]),
    ("commercial", "Commercial transportation", "Trucks, buses and trailers.",
     ["multi-axle templates", "payload and axle-load checks"]),
    ("aerospace", "Aerospace and aviation", "Airframes, wings and aircraft systems.",
     ["parametric wing and fuselage", "aerodynamic and structural estimates"]),
    ("space", "Space systems and propulsion", "Spacecraft structures and propulsion.",
     ["mass and delta-v budgets", "propulsion sizing"]),
    ("marine", "Marine engineering", "Hulls and marine propulsion.",
     ["hull form parameters", "hydrostatics"]),
    ("robotics", "Robotics", "Manipulators and mobile robots.",
     ["kinematic chains and joints", "reach and payload checks"]),
    ("machinery", "Industrial machinery", "Machines, mechanisms and drives.",
     ["mechanism templates", "drive sizing"]),
    ("manufacturing", "Advanced manufacturing", "Manufacturing processes and planning.",
     ["manufacturability checks", "process plans"]),
)  # fmt: skip


def registry() -> list[DomainDef]:
    planned = [
        DomainDef(id=i, name=n, description=d, status="unavailable", roadmap=r,
                  evidence="not implemented: roadmap only")
        for i, n, d, r in _PLANNED
    ]  # fmt: skip
    return [_automotive(), *planned]


def get(domain_id: str) -> DomainDef | None:
    return next((d for d in registry() if d.id == domain_id), None)


def can_host_projects(domain_id: str) -> bool:
    d = get(domain_id)
    return d is not None and d.status in ("available", "experimental")
