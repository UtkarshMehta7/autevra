"""Materials and allowables (platform service, every module).

Each material states where its strength values come from:
- ``minimum``: the minimum values guaranteed by the material standard named in ``source``
  (e.g. EN 10025-2 for structural steels, EN 485-2 for aluminium sheet, ASTM B265 for
  titanium sheet). These are the values a design check should use;
- ``typical``: representative values for concept work, labelled so (results using them
  are concept-level).
Fatigue: an endurance (steels) or a long-life fatigue strength (aluminium, at about 5 x
10^8 cycles, which has no true endurance limit), estimated from the ultimate strength
by the usual ratios (0.5 Rm for steels below 1,400 MPa, 0.35 Rm for aluminium alloys,
0.5 Rm for titanium); these are estimates for concept sizing, not test data.
Values in SI: density kg/m³, moduli GPa, strengths MPa.
"""

from typing import Literal

from pydantic import BaseModel


class Material(BaseModel):
    id: str
    name: str
    family: Literal["steel", "aluminium", "titanium", "magnesium", "composite", "polymer",
                    "cast iron"]  # fmt: skip
    density: float
    youngs_modulus_gpa: float
    poisson: float
    yield_mpa: float  # Rp0.2 (composites: none, first-ply failure not modelled here)
    ultimate_mpa: float
    elongation_pct: float
    basis: Literal["minimum", "typical"]
    source: str
    fatigue_mpa: float  # endurance or long-life strength (estimate, see module notes)
    cost_eur_per_kg: float = 0.0  # indicative raw-material price, for estimators
    co2_kg_per_kg: float = 0.0  # indicative cradle-to-gate footprint (primary material)
    notes: str = ""


def _m(id_: str, name: str, family: str, rho: float, e: float, nu: float, fy: float, fu: float,
       el: float, basis: str, source: str, fat: float, cost: float = 0.0, co2: float = 0.0,
       notes: str = "") -> Material:  # fmt: skip
    return Material(id=id_, name=name, family=family, density=rho, youngs_modulus_gpa=e,  # type: ignore[arg-type]
                    poisson=nu, yield_mpa=fy, ultimate_mpa=fu, elongation_pct=el,
                    basis=basis, source=source, fatigue_mpa=fat,  # type: ignore[arg-type]
                    cost_eur_per_kg=cost, co2_kg_per_kg=co2, notes=notes)  # fmt: skip


MATERIALS: dict[str, Material] = {m.id: m for m in [
    _m("s235", "Structural steel S235JR", "steel", 7850, 210, 0.3, 235, 360, 26, "minimum",
       "EN 10025-2 (t <= 16 mm)", 180, 0.8, 1.9),
    _m("s355", "Structural steel S355J2", "steel", 7850, 210, 0.3, 355, 470, 22, "minimum",
       "EN 10025-2 (t <= 16 mm)", 235, 0.9, 1.9),
    _m("dp600", "Dual-phase steel DP600 (automotive sheet)", "steel", 7850, 210, 0.3, 330, 590,
       20, "minimum", "EN 10338 HCT590X", 295, 1.0, 2.1),
    _m("42crmo4", "Alloy steel 42CrMo4, quenched and tempered", "steel", 7850, 210, 0.3, 750,
       1000, 11, "minimum", "EN ISO 683-2 (16 < d <= 40 mm)", 500, 1.6, 2.4),
    _m("6061_t6", "Aluminium EN AW-6061-T6 (extrusion)", "aluminium", 2700, 69, 0.33, 240, 260,
       8, "minimum", "EN 755-2", 91, 3.5, 8.5),
    _m("2024_t3", "Aluminium EN AW-2024-T3 (sheet)", "aluminium", 2780, 73, 0.33, 290, 435, 12,
       "minimum", "EN 485-2 (0.4-1.5 mm)", 152, 5.0, 9.0),
    _m("7075_t6", "Aluminium EN AW-7075-T6 (sheet)", "aluminium", 2810, 72, 0.33, 460, 540, 7,
       "minimum", "EN 485-2 (1.5-3 mm)", 189, 6.0, 9.5),
    _m("a356_t6", "Cast aluminium A356-T6 (AlSi7Mg0.3)", "aluminium", 2680, 72, 0.33, 200, 250,
       3, "typical", "typical permanent-mould T6 values (see EN 1706 for minima)", 75, 3.0,
       8.0),
    _m("ti6al4v", "Titanium Ti-6Al-4V (grade 5, annealed sheet)", "titanium", 4430, 114, 0.34,
       828, 895, 10, "minimum", "ASTM B265 grade 5", 448, 25.0, 35.0),
    _m("gjs500", "Ductile iron EN-GJS-500-7", "cast iron", 7100, 169, 0.275, 320, 500, 7,
       "minimum", "EN 1563", 224, 1.2, 1.8),
    _m("az91", "Magnesium AZ91D (die cast)", "magnesium", 1810, 45, 0.35, 150, 230, 3,
       "typical", "typical die-cast values", 70, 4.0, 24.0),
    _m("cfrp_qi", "Carbon/epoxy, quasi-isotropic laminate", "composite", 1550, 50, 0.3, 0, 600,
       1.2, "typical", "typical autoclave T300-class quasi-isotropic laminate", 240, 30.0, 25.0,
       "in-plane laminate values; ply-level design needs classical laminate theory"),
    _m("gfrp_qi", "Glass/epoxy, quasi-isotropic laminate", "composite", 1900, 18, 0.3, 0, 280,
       2.0, "typical", "typical hand lay-up E-glass quasi-isotropic laminate", 85, 4.0, 4.5),
    _m("pa66_gf30", "PA66 GF30 (dry as moulded)", "polymer", 1360, 9.5, 0.35, 0, 180, 3,
       "typical", "typical datasheet values, dry", 45, 4.5, 7.5,
       "conditioned (moist) strength is about 30 % lower"),
]}  # fmt: skip


def get(material_id: str) -> Material:
    try:
        return MATERIALS[material_id]
    except KeyError:
        raise KeyError(f"unknown material '{material_id}'") from None


def margin_of_safety(stress_mpa: float, material: Material, factor: float = 1.5,
                     ultimate: bool = False) -> float:  # fmt: skip
    """MS = allowable / (factor x stress) - 1 on yield (or ultimate when there is no yield,
    as for composites, or when ``ultimate``); positive means the part holds."""
    allowable = material.ultimate_mpa if ultimate or material.yield_mpa <= 0 else \
        material.yield_mpa  # fmt: skip
    return allowable / (factor * stress_mpa) - 1.0 if stress_mpa > 0 else float("inf")
