"""Engineering calculations for standard parts, each from a published method.

- Rolling bearing basic rating life (ISO 281): L10 = (C / P)^p million revolutions, p = 3
  for ball bearings, 10/3 for roller bearings; L10h = 10^6 L10 / (60 n) hours. Equivalent
  dynamic load for radial ball bearings P = X Fr + Y Fa, taken here as P = Fr when
  Fa / Fr <= e (pure or light axial load; the X/Y table is not applied).
- Threaded fasteners (ISO 898-1, ISO 724): tensile stress area
  As = pi/4 (d - 0.9382 P)^2; strength from the property class (Rm, Rp0.2, proof stress
  Sp). Assembly preload taken at 70 % of the yield load (a common design rule), and the
  tightening torque T = K F d with a nut factor K = 0.2 (dry steel, typical; lubrication
  lowers it). The full VDI 2230 procedure (joint stiffness, embedding, load factor) is not
  applied.
- Hollow sections: exact area, second moment and elastic section modulus of square (SHS)
  and circular (CHS) sections with sharp corners (corner radii of EN 10219 ignored).
"""

import math

STEEL = 7850.0  # kg/m3

# property class -> (Rm, Rp0.2, proof stress Sp) in MPa (ISO 898-1, d <= 16 mm for 8.8)
PROPERTY_CLASSES: dict[str, tuple[float, float, float]] = {
    "8.8": (800.0, 640.0, 580.0),
    "10.9": (1040.0, 940.0, 830.0),
    "12.9": (1220.0, 1100.0, 970.0),
}


def stress_area(d: float, pitch: float) -> float:
    """Tensile stress area of a metric thread, mm² (ISO 898-1)."""
    return math.pi / 4.0 * (d - 0.9382 * pitch) ** 2


def bolt_capacity(d: float, pitch: float, grade: str = "8.8", nut_factor: float = 0.2,
                  utilisation: float = 0.7) -> dict[str, float]:  # fmt: skip
    """Stress area, proof and yield loads, design preload and tightening torque."""
    rm, rp, sp = PROPERTY_CLASSES[grade]
    if grade == "8.8" and d > 16:
        rm, rp, sp = 830.0, 660.0, 600.0  # ISO 898-1 values for d > 16 mm
    a_s = stress_area(d, pitch)
    preload = utilisation * rp * a_s
    return {"stress_area_mm2": a_s, "proof_load_kN": sp * a_s / 1e3,
            "yield_load_kN": rp * a_s / 1e3, "ultimate_load_kN": rm * a_s / 1e3,
            "preload_kN": preload / 1e3, "torque_Nm": nut_factor * preload * d / 1e3}  # fmt: skip


def bearing_life(c_kn: float, load_kn: float, rpm: float, roller: bool = False) -> dict[str, float]:
    """ISO 281 basic rating life (90 % reliability) for an equivalent dynamic load."""
    if load_kn <= 0 or rpm <= 0:
        raise ValueError("load and speed must be positive")
    p = 10.0 / 3.0 if roller else 3.0
    l10 = (c_kn / load_kn) ** p  # million revolutions
    return {"L10_Mrev": l10, "L10_hours": l10 * 1e6 / (60.0 * rpm), "exponent": p}


def shs(b: float, t: float) -> dict[str, float]:
    """Square hollow section b x b x t (mm), sharp corners."""
    if not 0 < 2 * t < b:
        raise ValueError("wall thickness must be under half the width")
    bi = b - 2 * t
    area = b * b - bi * bi
    inertia = (b**4 - bi**4) / 12.0
    return {"area_mm2": area, "I_mm4": inertia, "W_mm3": inertia / (b / 2),
            "mass_kg_per_m": area * 1e-6 * STEEL}  # fmt: skip


def chs(d: float, t: float) -> dict[str, float]:
    """Circular hollow section of outside diameter d and wall t (mm)."""
    if not 0 < 2 * t < d:
        raise ValueError("wall thickness must be under half the diameter")
    di = d - 2 * t
    area = math.pi / 4 * (d * d - di * di)
    inertia = math.pi / 64 * (d**4 - di**4)
    return {"area_mm2": area, "I_mm4": inertia, "W_mm3": inertia / (d / 2),
            "mass_kg_per_m": area * 1e-6 * STEEL}  # fmt: skip
