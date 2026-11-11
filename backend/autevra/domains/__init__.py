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
    from autevra.assembly.model import COMPONENTS
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
    ("space", "Space systems and propulsion", "Spacecraft structures and propulsion.",
     ["mass and delta-v budgets", "propulsion sizing"]),
    ("robotics", "Robotics", "Manipulators and mobile robots.",
     ["kinematic chains and joints", "reach and payload checks"]),
    ("manufacturing", "Advanced manufacturing", "Manufacturing processes and planning.",
     ["manufacturability checks", "process plans"]),
)  # fmt: skip


BUILTIN = ("autevra.domains.automotive",)


def load_builtin() -> None:
    """Register the built-in domain modules (idempotent)."""
    import importlib

    for module in BUILTIN:
        importlib.import_module(module)


def _aerospace() -> DomainDef:
    from autevra import __version__

    return DomainDef(
        id="aerospace", name="Aircraft",
        description="Fixed-wing aircraft: a parametric light aircraft (fuselage, NACA wing and "
        "tails, propeller, landing gear) with lifting-line aerodynamics, drag build-up, "
        "stability and performance; Part Design, surfaces and structures for its parts.",
        status="experimental", version=__version__,
        component_library=["fuselage", "wing", "horizontal tail", "fin", "propeller",
                           "landing gear"],
        operations=["parametric aircraft", "build as a Part Design part", "Part Design",
                    "structures (FEA, topology optimisation)", "drawings"],
        simulations=["lifting-line theory (Glauert)", "component drag build-up (Raymer)",
                     "static stability (neutral point)", "Breguet range and endurance"],
        formats=["STEP AP214 export", "SVG drawings"],
        dependencies=["cadquery 2.8 / OCCT 7.9"],
        roadmap=["control surfaces and hinges", "engine nacelles and turbofans",
                 "mass and balance build-up", "V-n diagram and structural loads"],
        evidence="covered by tests/aero (closed-form lifting-line checks) and the workspace",
    )  # fmt: skip


def _machinery() -> DomainDef:
    from autevra import __version__

    return DomainDef(
        id="machinery", name="Mechanical",
        description="Engines designed category by category, starting with piston engines "
        "(inline, V and opposed; petrol and diesel; natural and turbocharged): cycle, torque "
        "and power, kinematics, balance, mass, the full part breakdown and concept geometry, "
        "published to the shared inventory.",
        status="experimental", version=__version__,
        component_library=["piston engines"],
        operations=["parametric engine", "build as parts", "publish to the inventory",
                    "Part Design", "structures (FEA)"],
        simulations=["air-standard Otto and Diesel cycles", "BMEP torque and power curves",
                     "slider-crank kinematics", "primary and secondary balance"],
        formats=["STEP AP214 export"],
        dependencies=["cadquery 2.8 / OCCT 7.9"],
        roadmap=["electric machines", "gas turbines", "gearboxes and mechanisms"],
        evidence="covered by tests/mech (balance against textbook results) and the workspace",
    )  # fmt: skip


def _marine() -> DomainDef:
    from autevra import __version__

    return DomainDef(
        id="marine", name="Marine",
        description="Small displacement vessels: parametric hull form, hydrostatics, the GZ "
        "curve against the IMO intact stability criteria, viscous resistance, the SFI-style "
        "breakdown, architecture, loads and production.",
        status="experimental", version=__version__, component_library=["displacement hulls"],
        operations=["parametric hull", "build as parts", "Part Design"],
        simulations=["hydrostatics", "large-angle stability (GZ) and IMO IS Code criteria",
                     "ITTC-1957 friction with form factor"],
        formats=["STEP AP214 export"], dependencies=["cadquery 2.8 / OCCT 7.9"],
        roadmap=["wave-making resistance (Holtrop-Mennen)", "planing hulls (Savitsky)",
                 "ISO 12215 scantlings", "weather criterion"],
        evidence="covered by tests/marine (box-barge and GM checks) and the workspace",
    )  # fmt: skip


def registry() -> list[DomainDef]:
    planned = [
        DomainDef(id=i, name=n, description=d, status="unavailable", roadmap=r,
                  evidence="not implemented: roadmap only")
        for i, n, d, r in _PLANNED
    ]  # fmt: skip
    return [_automotive(), _aerospace(), _machinery(), _marine(), *planned]


def get(domain_id: str) -> DomainDef | None:
    return next((d for d in registry() if d.id == domain_id), None)


def can_host_projects(domain_id: str) -> bool:
    d = get(domain_id)
    return d is not None and d.status in ("available", "experimental")
