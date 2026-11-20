"""Piston-engine load cases: peak gas force, reciprocating inertia, and the connecting rod
and main bearing loads they produce; the rod shank sized on its material's minimum yield.

Peak cylinder pressures are typical values (stated): naturally aspirated petrol 75 bar,
turbocharged petrol 120 bar, diesel 180 bar. Gas force F = p_max pi/4 B^2. Inertia force of
the reciprocating mass m r w^2 (1 + lambda) at top dead centre. The rod sees compression at
firing TDC (gas force less inertia at the peak-torque speed) and tension at exhaust TDC
(inertia at the rev limit). Shank area at 1.5 x the compression on 42CrMo4 minimum yield
(buckling of a stocky I-section rod is not checked here)."""

import math

from autevra import materials
from autevra.mech import piston as pk
from autevra.modules import Values
from autevra.product.loads import Compliance, LoadAt, LoadCase
from autevra.quality import Contributor, Stack


def _spec(values: Values) -> pk.EngineSpec:
    return pk.EngineSpec.model_validate({k: v for k, v in values.items()
                                         if k in pk.EngineSpec.model_fields})  # fmt: skip


def peak_pressure_bar(spec: pk.EngineSpec) -> float:
    return 180.0 if spec.fuel == "diesel" else (120.0 if spec.turbo else 75.0)


def cases(values: Values) -> list[LoadCase]:
    s = _spec(values)
    area = math.pi / 4 * (s.bore / 1000) ** 2
    gas = peak_pressure_bar(s) * 1e5 * area
    m = pk.reciprocating_mass_kg(s)
    r = s.stroke / 2000
    lam = 1 / (2 * s.rod_ratio)

    def inertia(rpm: float) -> float:
        w = rpm * 2 * math.pi / 60
        return m * r * w * w * (1 + lam)

    comp = gas - inertia(s.rpm_peak_torque)
    tension = inertia(s.rpm_max)
    steel = materials.get("42crmo4")
    shank = 1.5 * comp / (steel.yield_mpa * 1e6) * 1e6  # mm²
    return [
        LoadCase(id="firing", name="Firing at peak pressure (peak-torque speed)", kind="limit",
                 factors={"p_max_bar": peak_pressure_bar(s), "rpm": s.rpm_peak_torque},
                 method="typical peak cylinder pressure; inertia m r w^2 (1 + lambda)",
                 loads=[LoadAt(location="piston crown", fz=round(-gas)),
                        LoadAt(location="connecting rod (compression)", fz=round(-comp)),
                        LoadAt(location="main bearings (shared)", fz=round(-gas))],
                 results={"gas_force_n": round(gas), "rod_compression_n": round(comp),
                          "rod_shank_area_mm2": round(shank, 1)}),
        LoadCase(id="overspeed", name="Exhaust TDC at the rev limit", kind="limit",
                 factors={"rpm": s.rpm_max},
                 method="reciprocating inertia m r w^2 (1 + lambda)",
                 loads=[LoadAt(location="connecting rod (tension)", fz=round(tension)),
                        LoadAt(location="rod bolts (tension)", fz=round(tension))],
                 results={"rod_tension_n": round(tension)}),
    ]  # fmt: skip


def compliance(values: Values) -> list[Compliance]:
    return [
        Compliance(
            clause="Emissions (e.g. Euro 6 / EPA Tier 3)",
            requirement="exhaust emission limits of the target market",
            means="test",
            evidence="no combustion or after-treatment model yet",
            status="open",
        )
    ]


STATIONS = (("engine.structure", "Short block"), ("engine.cranktrain", "Short block"),
            ("engine.valvetrain", "Cylinder head sub-assembly"),
            ("engine.timing", "Long block"), ("engine.lubrication", "Long block"),
            ("engine.cooling", "Long block"))  # fmt: skip
ORDER = ("Short block", "Cylinder head sub-assembly", "Long block", "Dress and test")


def stackups(values: Values) -> list[Stack]:
    """Piston-to-deck clearance at TDC from the engine's own geometry: deck height less
    crank radius, rod length and piston compression height (typical machining tolerances).
    The concept geometry puts the crown 0.3 mm below the deck."""
    s = _spec(values)
    ch = 0.55 * s.bore
    rod = s.rod_ratio * s.stroke
    deck = s.stroke / 2 + rod + ch + 0.3
    return [Stack(name="Piston-to-deck clearance at TDC", lsl=0.05, usl=0.6, contributors=[
        Contributor(name="block deck height", nominal=round(deck, 3), plus=0.05, minus=0.05),
        Contributor(name="crank throw (radius)", nominal=s.stroke / 2, plus=0.03, minus=0.03,
                    direction=-1),
        Contributor(name="connecting rod length", nominal=round(rod, 3), plus=0.04, minus=0.04,
                    direction=-1),
        Contributor(name="piston compression height", nominal=round(ch, 3), plus=0.03,
                    minus=0.03, direction=-1),
    ])]  # fmt: skip
