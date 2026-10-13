"""Whole-vehicle integration checks: is the assembly a connected, consistent system?

Structural checks (no CAD needed):
- every mate names interfaces that exist and are of compatible kinds;
- every component is connected to the vehicle root;
- closed loops (coincidences, e.g. damper upper eye on the body shock tower) meet;
- every declared load path is joined by mates or coincidences.

Geometric checks use exact OCCT distances between the placed solids for the pairs
listed in ``CLEARANCES``. The body is a solid envelope, so parts packaged inside it (axles,
dampers) are not checked against it; that is a stated limitation, not a pass.
"""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum

import numpy as np

from autevra.assembly import graph
from autevra.assembly.vehicle import BY_ID, COINCIDENCES, COMPONENTS, LOAD_PATHS
from autevra.cad import kernel
from autevra.domain import derived as d

Values = Mapping[str, float]


class Status(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass(frozen=True)
class Check:
    id: str
    kind: str  # interface | connectivity | coincidence | load_path | clearance | travel
    status: Status
    message: str
    components: tuple[str, ...] = ()
    parameters: tuple[str, ...] = ()
    measured: float | None = None
    limit: float | None = None
    unit: str = ""


# Interface kinds that may be mated (parent kind, child kind).
COMPATIBLE = set({  # extensible
    ("origin", "origin"), ("axle_mount", "centre"), ("hub", "hub"), ("shock", "lower_eye"),
    ("shock_tower", "upper_eye"),
})  # fmt: skip


def interface_kind(name: str) -> str:
    name = re.sub(r"^(front|rear)_", "", name)
    return re.sub(r"_(left|right|fl|fr|rl|rr)$", "", name)


@dataclass(frozen=True)
class Clearance:
    a: str
    b: str
    minimum: float  # mm
    reason: str
    parameters: tuple[str, ...] = ()


_TYRE = ("rim_diameter", "tyre_width", "tyre_aspect_ratio")
CLEARANCES: list[Clearance] = list(
    item
    for c, axle in (("fl", "front"), ("fr", "front"), ("rl", "rear"), ("rr", "rear"))
    for item in (
        Clearance(f"wheel_{c}", "body", 5.0, "tyre must not touch the body at ride height",
                  ("arch_clearance", *_TYRE)),
        Clearance(f"wheel_{c}", "frame", 30.0, "frame rail clearance to the tyre",
                  ("rail_spacing", "rail_width", f"track_{axle}", "tyre_width")),
        Clearance(f"wheel_{c}", f"damper_{c}", 20.0, "coil-over clearance to the tyre",
                  ("spring_coil_diameter", f"{axle}_spring_rate", "rail_spacing",
                   f"track_{axle}", "tyre_width")),
        Clearance(f"damper_{c}", "frame", 5.0, "coil-over clearance to the frame",
                  ("rail_spacing", "rail_height", "ground_clearance")),
    )
)  # fmt: skip


def _world_point(world: Mapping[str, np.ndarray], values: Values, cid: str, iface: str):
    frame = BY_ID[cid].resolve_interfaces(values)[iface]
    return (np.asarray(world[cid]) @ np.asarray(frame))[:3, 3]


def structural_checks(values: Values) -> list[Check]:
    out: list[Check] = []
    frames = {c.id: c.resolve_interfaces(values) for c in COMPONENTS}
    for c in COMPONENTS:
        if c.mate is None:
            continue
        parent = BY_ID.get(c.mate.parent)
        missing = (
            parent is None
            or c.mate.parent_interface not in frames[parent.id]
            or c.mate.child_interface not in frames[c.id]
        )
        if missing:
            out.append(Check(f"mate:{c.id}", "interface", Status.FAIL,
                             f"{c.name} is mated to an interface that does not exist",
                             (c.id, c.mate.parent)))  # fmt: skip
            continue
        kinds = (interface_kind(c.mate.parent_interface), interface_kind(c.mate.child_interface))
        ok = kinds in COMPATIBLE
        out.append(Check(
            f"mate:{c.id}", "interface", Status.PASS if ok else Status.FAIL,
            f"{c.name} {c.mate.child_interface} → {parent.name} {c.mate.parent_interface}"
            + ("" if ok else f": incompatible interface kinds {kinds[1]} and {kinds[0]}"),
            (c.id, parent.id),
        ))  # fmt: skip

    for c in COMPONENTS:
        try:
            chain = graph.ancestors(c)
            rooted = (chain[-1] if chain else c).mate is None
        except (KeyError, ValueError):
            rooted = False
        if not rooted:
            out.append(Check(f"connected:{c.id}", "connectivity", Status.FAIL,
                             f"{c.name} is not connected to the vehicle", (c.id,)))  # fmt: skip
    if all(ch.kind != "connectivity" for ch in out):
        message = f"all {len(COMPONENTS)} components are connected to the vehicle"
        out.append(Check("connected", "connectivity", Status.PASS, message))

    world = graph.place_all(values)
    for co in COINCIDENCES:
        gap = float(np.linalg.norm(
            _world_point(world, values, *co.a) - _world_point(world, values, *co.b)
        ))  # fmt: skip
        ok = gap <= co.tolerance
        out.append(Check(
            f"coincident:{co.a[0]}.{co.a[1]}", "coincidence", Status.PASS if ok else Status.FAIL,
            f"{BY_ID[co.a[0]].name} {co.a[1]} {'meets' if ok else 'misses'} "
            f"{BY_ID[co.b[0]].name} {co.b[1]} (gap {gap:.3f} mm)",
            (co.a[0], co.b[0]), measured=round(gap, 6), limit=co.tolerance, unit="mm",
        ))  # fmt: skip

    joined = {(c.id, c.mate.parent) for c in COMPONENTS if c.mate} | {
        (co.a[0], co.b[0]) for co in COINCIDENCES
    }
    for path in LOAD_PATHS:
        breaks = [
            (x, y) for x, y in zip(path, path[1:], strict=False)
            if (x, y) not in joined and (y, x) not in joined
        ]  # fmt: skip
        out.append(Check(
            f"load_path:{path[0]}", "load_path", Status.FAIL if breaks else Status.PASS,
            " → ".join(BY_ID[x].name for x in path)
            + (f": no connection between {breaks[0][0]} and {breaks[0][1]}" if breaks else ""),
            path,
        ))  # fmt: skip
    return out


def travel_checks(values: Values) -> list[Check]:
    """Warnings when the packaging, not the suspension, sets the usable wheel travel."""
    out = []
    for a in d.AXLES:
        limits = d.travel_limits(values, a)
        for kinds, label, name in (
            (d.BUMP_LIMITS, "bump", "bump_stop"), (d.REBOUND_LIMITS, "rebound", "droop")
        ):  # fmt: skip
            governing = min(kinds, key=lambda k: limits[k][0])
            value, param = limits[governing]
            design = limits[name][0]
            if governing == name:
                message = f"{a} {label} travel {value:.1f} mm is set by the suspension"
                out.append(Check(
                    f"travel:{a}_{label}", "travel", Status.PASS, message,
                    parameters=(param,), measured=round(value, 3), unit="mm",
                ))  # fmt: skip
                continue
            out.append(Check(
                f"travel:{a}_{label}", "travel", Status.WARNING,
                f"{a} {label} travel is limited to {value:.1f} mm by the "
                f"{governing.replace('_', ' ')} ({param}), below the {design:.0f} mm "
                f"{name.replace('_', ' ')} travel",
                parameters=(param, limits[name][1]), measured=round(value, 3), limit=design,
                unit="mm",
            ))  # fmt: skip
    return out


@dataclass
class ClearanceCache:
    """Exact distances are ~0.05–0.2 s each; cache by geometry key and placement."""

    entries: dict[tuple, float] = field(default_factory=dict)
    max_entries: int = 512

    def get(self, key: tuple, compute) -> float:  # type: ignore[no-untyped-def]
        if key not in self.entries:
            if len(self.entries) >= self.max_entries:
                self.entries.pop(next(iter(self.entries)))
            self.entries[key] = compute()
        return self.entries[key]


def clearance_checks(model, cache: ClearanceCache | None = None) -> list[Check]:  # type: ignore[no-untyped-def]
    """``model`` is a built vehicle model (parts with geometry keys, matrices and shapes)."""
    cache = cache or ClearanceCache()
    parts = {p.id: p for p in model.parts}
    out = []
    for cl in CLEARANCES:
        a, b = parts[cl.a], parts[cl.b]
        key = (a.geometry, str(a.matrix), b.geometry, str(b.matrix))
        dist = cache.get(key, lambda a=a, b=b: kernel.min_distance(
            model.shapes[a.geometry], np.array(a.matrix), model.shapes[b.geometry],
            np.array(b.matrix),
        ))  # fmt: skip
        ok = dist >= cl.minimum
        out.append(Check(
            f"clearance:{cl.a}:{cl.b}", "clearance", Status.PASS if ok else Status.FAIL,
            f"{BY_ID[cl.a].name} to {BY_ID[cl.b].name}: {dist:.1f} mm "
            f"({'≥' if ok else 'below'} {cl.minimum:g} mm, {cl.reason})",
            (cl.a, cl.b), cl.parameters, round(dist, 3), cl.minimum, "mm",
        ))  # fmt: skip
    return out


NOT_CHECKED = (
    "Parts packaged inside the body envelope (axles, dampers) are not checked against the body: "
    "the body is a solid envelope, not a shell.",
    "Clearances are static (ride height, straight ahead); wheel travel and steering sweeps are "
    "covered by the suspension tests and a later steering sweep check.",
)
