"""Permanent-magnet synchronous machines: torque from air-gap shear stress, torque-speed
envelope, an efficiency map from a stated loss model, and mass.

Method (concept sizing, stated):
- torque from the tangential air-gap shear stress sigma acting on the rotor surface:
  T = sigma (pi D_r L) (D_r / 2) = (pi / 2) sigma D_r^2 L, with peak and continuous stresses
  (liquid-cooled automotive machines about 50-60 kPa peak, 25-35 kPa continuous);
- envelope: peak torque up to the base speed, then constant power (field weakening) to the
  maximum speed;
- losses (a loss split calibrated to 96 % efficiency at the rated point, stated): copper
  2.5 % of rated power at continuous torque, scaling with torque squared; iron 1.2 % at base
  speed, scaling with speed^1.5; mechanical (bearings, windage) 0.5 % at the maximum speed,
  scaling with speed squared;
- mass: active parts at 5,000 kg per m^3 of the stator envelope (laminations, copper,
  magnets), times 1.6 for housing, shaft, end shields and cooling.
Limits: no electromagnetic field solution, no voltage or current limits, no thermal model;
use it to size and compare, not to rate a machine.
"""

import math

import numpy as np
from pydantic import BaseModel, Field, model_validator


class MotorSpec(BaseModel):
    name: str = "PMSM 150 kW"
    stator_diameter: float = Field(220.0, gt=40.0, le=1500.0)  # mm, outer
    stack_length: float = Field(150.0, gt=10.0, le=1500.0)  # mm
    rotor_ratio: float = Field(0.65, ge=0.4, le=0.85)  # rotor / stator diameter
    poles: int = Field(8, ge=2, le=48)
    shear_peak_kpa: float = Field(55.0, gt=5.0, le=120.0)
    shear_continuous_kpa: float = Field(30.0, gt=2.0, le=80.0)
    base_rpm: float = Field(5000.0, gt=100.0, le=40_000.0)
    max_rpm: float = Field(16_000.0, gt=200.0, le=60_000.0)
    voltage: float = Field(400.0, gt=12.0, le=1500.0)  # DC link, V

    @model_validator(mode="after")
    def _ok(self) -> "MotorSpec":
        if self.poles % 2:
            raise ValueError("pole count must be even")
        if self.max_rpm <= self.base_rpm:
            raise ValueError("the maximum speed must exceed the base speed")
        if self.shear_continuous_kpa > self.shear_peak_kpa:
            raise ValueError("continuous shear stress cannot exceed the peak")
        return self


def torque(spec: MotorSpec, shear_kpa: float) -> float:
    dr = spec.rotor_ratio * spec.stator_diameter / 1000
    return math.pi / 2 * shear_kpa * 1e3 * dr * dr * spec.stack_length / 1000


def envelope_torque(spec: MotorSpec, rpm: float, peak: bool = True) -> float:
    t = torque(spec, spec.shear_peak_kpa if peak else spec.shear_continuous_kpa)
    if rpm > spec.max_rpm:
        return 0.0
    return t if rpm <= spec.base_rpm else t * spec.base_rpm / rpm


def losses_w(spec: MotorSpec, rpm: float, t: float) -> float:
    t_cont = torque(spec, spec.shear_continuous_kpa)
    rated = t_cont * spec.base_rpm * 2 * math.pi / 60
    cu = 0.025 * rated * (t / t_cont) ** 2
    fe = 0.012 * rated * (rpm / spec.base_rpm) ** 1.5
    mech = 0.005 * rated * (rpm / spec.max_rpm) ** 2
    return cu + fe + mech


def efficiency(spec: MotorSpec, rpm: float, t: float) -> float:
    p = t * rpm * 2 * math.pi / 60
    return p / (p + losses_w(spec, rpm, t)) if p > 0 else 0.0


def mass_kg(spec: MotorSpec) -> float:
    v = math.pi / 4 * (spec.stator_diameter / 1000) ** 2 * spec.stack_length / 1000
    return 5000.0 * v * 1.6


def analyse(spec: MotorSpec) -> dict:
    t_peak = torque(spec, spec.shear_peak_kpa)
    t_cont = torque(spec, spec.shear_continuous_kpa)
    w_base = spec.base_rpm * 2 * math.pi / 60
    rpms = np.linspace(spec.max_rpm / 40, spec.max_rpm, 40)
    curve = [{"rpm": float(n), "torque_nm": envelope_torque(spec, n),
              "continuous_nm": envelope_torque(spec, n, peak=False),
              "power_kw": envelope_torque(spec, n) * n * 2 * math.pi / 60 / 1000}
             for n in rpms]  # fmt: skip
    grid_n = np.linspace(spec.max_rpm / 20, spec.max_rpm, 20)
    grid_t = np.linspace(t_peak / 20, t_peak, 20)
    eff = [[round(efficiency(spec, float(n), float(t)), 4) if t <= envelope_torque(spec, n)
            else None for n in grid_n] for t in grid_t]  # fmt: skip
    best = max((e, n, t) for row, t in zip(eff, grid_t, strict=True)
               for e, n in zip(row, grid_n, strict=True) if e is not None)  # fmt: skip
    mass = mass_kg(spec)
    peak_kw = t_peak * w_base / 1000
    tip = spec.rotor_ratio * spec.stator_diameter / 2000 * spec.max_rpm * 2 * math.pi / 60
    checks = [
        {"id": "tip_speed", "label": "Rotor surface speed", "status": "pass" if tip <= 120 else
         "warn" if tip <= 160 else "fail",
         "message": f"{tip:.0f} m/s at {spec.max_rpm:.0f} rpm (embedded-magnet rotors usually "
         "stay under 120-160 m/s without a sleeve)"},
        {"id": "frequency", "label": "Electrical frequency", "status": "pass" if
         spec.max_rpm * spec.poles / 120 <= 1200 else "warn",
         "message": f"{spec.max_rpm * spec.poles / 120:.0f} Hz at maximum speed (iron losses "
         "and inverter switching grow above about 1 kHz)"},
        {"id": "power_density", "label": "Power density", "status": "pass" if
         peak_kw / mass <= 8 else "warn",
         "message": f"{peak_kw / mass:.1f} kW/kg peak (automotive machines about 2-6)"},
    ]  # fmt: skip
    return {"peak_torque_nm": t_peak, "continuous_torque_nm": t_cont,
            "peak_power_kw": peak_kw, "continuous_power_kw": t_cont * w_base / 1000,
            "mass_kg": mass, "power_density_kw_per_kg": peak_kw / mass,
            "peak_efficiency": best[0], "peak_efficiency_at": {"rpm": float(best[1]),
                                                               "torque_nm": float(best[2])},
            "curve": curve, "efficiency_map": {"rpm": grid_n.tolist(),
                                               "torque_nm": grid_t.tolist(), "eta": eff},
            "checks": checks}  # fmt: skip
