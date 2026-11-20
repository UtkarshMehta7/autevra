"""Cutting tools and cutting data.

Starting values for solid carbide end mills and drills as tool makers' catalogues give
them (typical, not optimised for a given machine): cutting speed Vc (m/min), feed per
tooth fz = k_fz * D (mm), roughing depth of cut ap = k_ap * D, stepover ae = 0.4 D, and the
specific cutting force kc (N/mm2) for the power estimate. Spindle speed
n = 1000 Vc / (pi D), table feed vf = n z fz, cutting power Pc = ap ae vf kc / 6e7 (kW).
Drills: feed per revolution f = k_f * d; taps: feed = n * pitch (rigid tapping).
"""

import math
from dataclasses import dataclass
from typing import Literal

MaterialName = Literal[
    "aluminium 6061-T6", "steel C45", "stainless 304", "cast iron GG25", "POM (acetal)"
]


@dataclass(frozen=True)
class CuttingData:
    vc_mill: float  # m/min
    k_fz: float  # fz = k_fz * D, mm/tooth
    k_ap: float  # roughing ap = k_ap * D
    flutes: int
    kc: float  # N/mm2
    vc_drill: float
    k_f_drill: float  # f = k * d, mm/rev
    vc_tap: float
    density: float  # kg/m3


MATERIALS: dict[str, CuttingData] = {
    "aluminium 6061-T6": CuttingData(300.0, 0.010, 0.5, 3, 800.0, 120.0, 0.020, 20.0, 2700.0),
    "steel C45": CuttingData(150.0, 0.006, 0.25, 4, 2000.0, 80.0, 0.015, 10.0, 7850.0),
    "stainless 304": CuttingData(90.0, 0.004, 0.2, 4, 2500.0, 50.0, 0.010, 6.0, 8000.0),
    "cast iron GG25": CuttingData(120.0, 0.006, 0.3, 4, 1150.0, 90.0, 0.020, 12.0, 7200.0),
    "POM (acetal)": CuttingData(250.0, 0.012, 0.6, 2, 300.0, 100.0, 0.025, 15.0, 1410.0),
}
END_MILLS = (3.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0)


@dataclass(frozen=True)
class Tool:
    number: int
    kind: Literal["end mill", "spot drill", "drill", "tap"]
    diameter: float
    flutes: int = 2
    pitch: float = 0.0  # taps
    point_angle: float = 0.0  # drills and spot drills, degrees

    @property
    def label(self) -> str:
        if self.kind == "tap":
            return f"T{self.number} tap M{self.diameter:g}×{self.pitch:g}"
        if self.kind == "end mill":
            return f"T{self.number} end mill ⌀{self.diameter:g} {self.flutes}F carbide"
        return f"T{self.number} {self.kind} ⌀{self.diameter:g} {self.point_angle:g}°"


@dataclass(frozen=True)
class Speeds:
    rpm: float
    feed: float  # mm/min
    plunge: float  # mm/min
    ap: float  # mm
    ae: float  # mm
    capped: bool  # the spindle limit lowered the speed


def mill_speeds(tool: Tool, mat: CuttingData, max_rpm: float) -> Speeds:
    n = 1000.0 * mat.vc_mill / (math.pi * tool.diameter)
    capped = n > max_rpm
    n = min(n, max_rpm)
    vf = n * tool.flutes * mat.k_fz * tool.diameter
    return Speeds(n, vf, 0.5 * vf, mat.k_ap * tool.diameter, 0.4 * tool.diameter, capped)


def drill_speeds(tool: Tool, mat: CuttingData, max_rpm: float) -> Speeds:
    if tool.kind == "tap":
        n = min(1000.0 * mat.vc_tap / (math.pi * tool.diameter), max_rpm, 1500.0)
        return Speeds(n, n * tool.pitch, n * tool.pitch, 0.0, 0.0, False)
    n = 1000.0 * mat.vc_drill / (math.pi * tool.diameter)
    capped = n > max_rpm
    n = min(n, max_rpm)
    f = mat.k_f_drill * tool.diameter * (0.5 if tool.kind == "spot drill" else 1.0)
    return Speeds(n, n * f, n * f, 0.0, 0.0, capped)


def power_kw(ap: float, ae: float, vf: float, kc: float) -> float:
    return ap * ae * vf * kc / 6.0e7
