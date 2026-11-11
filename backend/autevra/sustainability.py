"""Life-cycle assessment (climate change, kg CO2e), structured as ISO 14040/14044 stages:
production, use and end of life, with every factor stated and adjustable.

- production: the manufacturing plan's materials (buy-to-fly masses x the material's
  cradle-to-gate factor) and purchased parts (5 kg CO2e/kg, generic);
- use: the module's own energy per unit of service (per km, per flight hour, per running
  hour) x the energy's intensity x the service life;
- end of life: a credit for recycled metals, mass x recycled fraction x (primary - secondary
  footprint): steel 85 % (1.9 -> 0.6), aluminium 75 % (8.5 -> 0.6).
Intensity factors (defaults, stated): petrol 2.31 kg/L, diesel 2.68 kg/L (3.2 kg/kg),
avgas 3.1 kg/kg, grid electricity 0.30 kg/kWh (adjustable). These are indicative; a
certified LCA uses licensed datasets.
"""

from pydantic import BaseModel, Field

from autevra.manufacturing import Plan

RECYCLE = {"steel": (0.85, 1.9, 0.6), "aluminium": (0.75, 8.5, 0.6)}  # rate, primary, secondary
FAMILY = {"s235": "steel", "s355": "steel", "dp600": "steel", "42crmo4": "steel",
          "gjs500": "steel", "6061_t6": "aluminium", "2024_t3": "aluminium",
          "7075_t6": "aluminium", "a356_t6": "aluminium"}  # fmt: skip


class UsePhase(BaseModel):
    unit: str  # "km", "flight hour", "running hour"
    energy_per_unit_kwh: float
    carrier: str  # "electricity", "petrol", "diesel", "avgas"
    co2_per_unit_kg: float
    life_units: float
    basis: str


class Assessment(BaseModel):
    production_kg: float
    use_kg: float
    end_of_life_kg: float  # negative: a credit
    total_kg: float
    use: UsePhase | None
    shares: dict[str, float]
    notes: list[str] = Field(default_factory=list)


def end_of_life_credit(plan: Plan) -> float:
    credit = 0.0
    for op in plan.operations:
        fam = FAMILY.get(op.material)
        if fam and not op.bought_out:
            rate, primary, secondary = RECYCLE[fam]
            finished = op.material_kg  # bought mass; offcuts recycled at the plant as well
            credit += finished * rate * (primary - secondary)
    return -credit


def assess(plan: Plan, use: UsePhase | None) -> Assessment:
    production = plan.total_co2_kg
    use_kg = use.co2_per_unit_kg * use.life_units if use else 0.0
    eol = end_of_life_credit(plan)
    total = production + use_kg + eol
    gross = production + use_kg
    return Assessment(
        production_kg=round(production, 1),
        use_kg=round(use_kg, 1),
        end_of_life_kg=round(eol, 1),
        total_kg=round(total, 1),
        use=use,
        shares={
            "production": production / gross if gross else 0.0,
            "use": use_kg / gross if gross else 0.0,
        },
        notes=["indicative factors; a certified LCA uses licensed datasets"],
    )
