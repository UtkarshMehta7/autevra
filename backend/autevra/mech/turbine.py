"""Gas-turbine cycle, station by station: single-spool turbojet or turboshaft (free power
turbine) at a flight condition.

Method (stated): ISA ambient; ram compression with inlet pressure recovery; compressor
with isentropic efficiency; burner energy balance for the fuel-air ratio
f = (cp_h T4 - cp T3) / (eta_b LHV - cp_h T4) with a pressure loss; turbine driving the
compressor (mechanical efficiency); then either a nozzle expanding fully to ambient
(turbojet: specific thrust (1 + f) V9 - V0, TSFC = f / specific thrust) or a free power
turbine expanding to ambient (turboshaft: specific power). Air cp 1,005 J/kg K with
gamma 1.4; combustion gas cp 1,148 with gamma 1.333; kerosene LHV 43 MJ/kg.
Limits: constant specific heats per stream, no cooling-air bleed or turbine cooling, no
off-design matching (each point is a design point).
"""

import math

from pydantic import BaseModel, Field

from autevra.aero.aircraft import isa


class TurbineSpec(BaseModel):
    name: str = "Turbojet"
    kind: str = Field("turbojet", pattern="^(turbojet|turboshaft)$")
    pressure_ratio: float = Field(12.0, ge=1.5, le=60.0)
    tit_k: float = Field(1400.0, ge=900.0, le=2100.0)  # turbine entry temperature
    mass_flow: float = Field(20.0, gt=0.1, le=1500.0)  # kg/s
    eta_c: float = Field(0.85, ge=0.5, le=1.0)
    eta_t: float = Field(0.88, ge=0.5, le=1.0)
    eta_b: float = Field(0.99, ge=0.8, le=1.0)
    eta_n: float = Field(0.97, ge=0.8, le=1.0)
    eta_m: float = Field(0.99, ge=0.9, le=1.0)
    burner_loss: float = Field(0.04, ge=0.0, le=0.15)
    inlet_recovery: float = Field(0.98, ge=0.8, le=1.0)
    mach: float = Field(0.0, ge=0.0, le=2.5)
    altitude: float = Field(0.0, ge=0.0, le=11_000.0)
    cp: float = 1005.0
    gamma: float = 1.4
    cp_h: float = 1148.0
    gamma_h: float = 1.333
    lhv: float = 43e6


def cycle(s: TurbineSpec) -> dict:
    air = isa(s.altitude)
    t0, p0 = air["T"], air["p"]
    v0 = s.mach * air["a"]
    g, gh = s.gamma, s.gamma_h
    t2 = t0 * (1 + (g - 1) / 2 * s.mach**2)
    p2 = p0 * (t2 / t0) ** (g / (g - 1)) * s.inlet_recovery
    t3 = t2 * (1 + (s.pressure_ratio ** ((g - 1) / g) - 1) / s.eta_c)
    p3 = p2 * s.pressure_ratio
    t4 = s.tit_k
    f = (s.cp_h * t4 - s.cp * t3) / (s.eta_b * s.lhv - s.cp_h * t4)
    if f <= 0:
        raise ValueError("the turbine entry temperature is below the compressor exit")
    p4 = p3 * (1 - s.burner_loss)
    w_c = s.cp * (t3 - t2)
    t5 = t4 - w_c / (s.cp_h * (1 + f) * s.eta_m)
    p5 = p4 * (1 - (t4 - t5) / (s.eta_t * t4)) ** (gh / (gh - 1))
    stations = {"0": (t0, p0), "2": (t2, p2), "3": (t3, p3), "4": (t4, p4), "5": (t5, p5)}
    out: dict = {"fuel_air_ratio": f, "compressor_work_kj_per_kg": w_c / 1000,
                 "stations": {k: {"T_K": round(t, 1), "p_kPa": round(p / 1000, 2)}
                              for k, (t, p) in stations.items()}}  # fmt: skip
    expansion = 1 - (p0 / p5) ** ((gh - 1) / gh)
    if expansion <= 0:
        raise ValueError("no pressure left to expand after the turbine")
    if s.kind == "turbojet":
        v9 = math.sqrt(2 * s.eta_n * s.cp_h * t5 * expansion)
        spec_thrust = (1 + f) * v9 - v0
        thrust = spec_thrust * s.mass_flow
        out.update(
            exit_velocity=v9,
            specific_thrust=spec_thrust,
            thrust_kn=thrust / 1000,
            tsfc_g_per_kn_s=f / spec_thrust * 1e6 if spec_thrust > 0 else math.inf,
            thermal_efficiency=((1 + f) * v9**2 - v0**2) / 2 / (f * s.lhv),
        )
    else:
        w_shaft = s.eta_t * (1 + f) * s.cp_h * t5 * expansion * s.eta_m
        power = w_shaft * s.mass_flow
        out.update(
            specific_power_kj_per_kg=w_shaft / 1000,
            shaft_power_kw=power / 1000,
            sfc_g_per_kwh=f * s.mass_flow / (power / 1000) * 3.6e6,
            thermal_efficiency=w_shaft / (f * s.lhv),
        )
    return out


def ideal_brayton_efficiency(pressure_ratio: float, gamma: float = 1.4) -> float:
    return 1 - pressure_ratio ** (-(gamma - 1) / gamma)
