"""Mechanical module: engines (piston engines first; electric machines and gas turbines
next), designed as products and published to the shared inventory."""

from autevra.modules import ModuleDef, register
from autevra.modules.mechanical import engine as bd
from autevra.modules.mechanical import systems

MODULE = ModuleDef(
    id="mechanical", domain="machinery", name="Mechanical",
    frame="x along the crankshaft to the front, y to the left, z up from the crank axis; metres",
    options=bd.options, current=bd.current, configure=bd.configure,
    breakdown=bd.breakdown, checks=bd.checks, architecture=systems.architecture,
)  # fmt: skip
register(MODULE)
