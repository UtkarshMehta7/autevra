"""Aircraft module: a fixed-wing light aircraft's breakdown by ATA chapter, with group
masses from Raymer's general-aviation weight equations and the options of the type."""

from autevra.modules import ModuleDef, register
from autevra.modules.aircraft import breakdown as bd
from autevra.modules.aircraft import loads, systems

MODULE = ModuleDef(
    id="aircraft", domain="aerospace", name="Aircraft",
    frame="x aft of the nose, y to the left, z up from the fuselage datum; metres",
    options=bd.options, current=bd.current, configure=bd.configure,
    breakdown=bd.breakdown, checks=bd.checks, architecture=systems.architecture,
    loads=loads.cases, compliance=loads.compliance,
)  # fmt: skip
register(MODULE)
