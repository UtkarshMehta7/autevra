"""Routing of wiring harnesses and pipes along waypoints, with their engineering checks.

Harness (stated rules): each conductor's insulated diameter from its cross-section
(thin-wall automotive cable, d = 1.2 sqrt(4 A / pi) + 0.5 mm); bundle diameter
D = 1.15 sqrt(sum d_i^2) (a packing allowance); minimum bend radius 6 D; voltage drop of a
two-wire circuit dV = 2 I rho L / A with copper rho = 0.0175 ohm mm^2/m, checked against a
limit (default 3 % of the supply).
Pipe: Darcy-Weisbach dp = (f L / D + sum K) rho v^2 / 2 with f = 64 / Re (laminar) or the
Blasius f = 0.316 Re^-0.25 (turbulent, smooth), bend losses K = 0.3 per 90 degrees of turn,
and the bend radius checked against 3 x the outer diameter (a common minimum for bent tube).
Fluids at 20-40 degC: water, diesel, engine oil, hydraulic oil (density, kinematic viscosity).
Geometry: the route's centreline polyline with rounded corners (a Part Design sweep).
"""

import math

import numpy as np
from pydantic import BaseModel, Field

RHO_CU = 0.0175  # ohm mm²/m
FLUIDS = {"water": (998.0, 1.0e-6), "diesel": (830.0, 3.0e-6),
          "engine oil": (870.0, 1.0e-4), "hydraulic oil": (870.0, 4.6e-5)}  # fmt: skip


class Conductor(BaseModel):
    name: str
    area_mm2: float = Field(gt=0, le=150)
    current_a: float = Field(ge=0, le=1000)


class HarnessIn(BaseModel):
    name: str = "Harness"
    points: list[tuple[float, float, float]] = Field(min_length=2, max_length=100)  # mm
    bend_radius: float = Field(60.0, gt=0)
    supply_v: float = Field(12.0, gt=0, le=1000)
    max_drop_pct: float = Field(3.0, gt=0, le=20)
    conductors: list[Conductor] = Field(min_length=1, max_length=200)


class PipeIn(BaseModel):
    name: str = "Pipe"
    points: list[tuple[float, float, float]] = Field(min_length=2, max_length=100)
    bend_radius: float = Field(40.0, gt=0)
    outer_mm: float = Field(12.0, gt=1, le=500)
    wall_mm: float = Field(1.0, gt=0.1, le=50)
    fluid: str = Field("water", pattern="^(water|diesel|engine oil|hydraulic oil)$")
    flow_lpm: float = Field(10.0, gt=0, le=100_000)


def length_and_turns(points: list[tuple[float, float, float]]) -> tuple[float, float]:
    """Centreline length (mm) and total turning (degrees)."""
    p = np.array(points, dtype=float)
    seg = np.diff(p, axis=0)
    length = float(np.linalg.norm(seg, axis=1).sum())
    turn = 0.0
    for a, b in zip(seg[:-1], seg[1:], strict=False):
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na > 0 and nb > 0:
            turn += math.degrees(math.acos(max(-1.0, min(1.0, float(a @ b / (na * nb))))))
    return length, turn


def harness(h: HarnessIn) -> dict:
    length, turn = length_and_turns(h.points)
    diameters = [1.2 * math.sqrt(4 * c.area_mm2 / math.pi) + 0.5 for c in h.conductors]
    bundle = 1.15 * math.sqrt(sum(d * d for d in diameters))
    drops = [{"name": c.name, "drop_v": 2 * c.current_a * RHO_CU * length / 1000 / c.area_mm2,
              "drop_pct": 100 * 2 * c.current_a * RHO_CU * length / 1000 / c.area_mm2 / h.supply_v}
             for c in h.conductors]  # fmt: skip
    worst = max(drops, key=lambda d: d["drop_pct"])
    checks = [
        {"id": "bend", "label": "Bend radius", "status": "pass" if h.bend_radius >= 6 * bundle
         else "fail", "message": f"{h.bend_radius:.0f} mm vs minimum {6 * bundle:.0f} mm "
         f"(6 x the {bundle:.1f} mm bundle)"},
        {"id": "drop", "label": "Voltage drop", "status": "pass" if worst["drop_pct"] <=
         h.max_drop_pct else "fail", "message": f"worst {worst['name']}: {worst['drop_v']:.2f} V "
         f"({worst['drop_pct']:.1f} % of {h.supply_v:g} V; limit {h.max_drop_pct:g} %)"},
    ]  # fmt: skip
    return {"length_mm": length, "turning_deg": turn, "bundle_mm": bundle,
            "conductors": drops, "checks": checks,
            "part": {"name": h.name, "color": [0.05, 0.05, 0.06], "finish": "rubber",
                     "features": [{"id": "route", "name": "Harness", "type": "sweep",
                                   "path": [list(x) for x in h.points],
                                   "radius": bundle / 2,
                                   "bend_radius": h.bend_radius}]}}  # fmt: skip


def pipe(pp: PipeIn) -> dict:
    length, turn = length_and_turns(pp.points)
    rho, nu = FLUIDS[pp.fluid]
    d = (pp.outer_mm - 2 * pp.wall_mm) / 1000
    area = math.pi / 4 * d * d
    v = pp.flow_lpm / 60_000 / area
    re = v * d / nu
    f = 64 / re if re < 2300 else 0.316 * re**-0.25
    k = 0.3 * turn / 90
    dp = (f * length / 1000 / d + k) * rho * v * v / 2
    checks = [
        {"id": "bend", "label": "Bend radius", "status": "pass" if pp.bend_radius >=
         3 * pp.outer_mm else "fail", "message": f"{pp.bend_radius:.0f} mm vs minimum "
         f"{3 * pp.outer_mm:.0f} mm (3 x the outer diameter)"},
        {"id": "velocity", "label": "Flow velocity", "status": "pass" if v <= 3.0 else "warn",
         "message": f"{v:.2f} m/s (keep under about 3 m/s for noise and erosion)"},
    ]  # fmt: skip
    return {"length_mm": length, "turning_deg": turn, "velocity_ms": v, "reynolds": re,
            "friction_factor": f, "bend_k": k, "pressure_drop_kpa": dp / 1000,
            "regime": "laminar" if re < 2300 else "turbulent", "checks": checks,
            "part": {"name": pp.name, "color": [0.72, 0.5, 0.3], "finish": "polished",
                     "features": [{"id": "route", "name": "Pipe", "type": "sweep",
                                   "path": [list(x) for x in pp.points],
                                   "radius": pp.outer_mm / 2, "wall": pp.wall_mm,
                                   "bend_radius": pp.bend_radius}]}}  # fmt: skip
