"""Land vehicles module: a road vehicle's breakdown by system, with parametric mass
estimates per part and the options of the model range."""

from autevra.modules import ModuleDef, register
from autevra.modules.land import breakdown as bd

MODULE = ModuleDef(
    id="land", domain="automotive", name="Land vehicles",
    frame="x rearward from the front axle, y to the left, z up from the ground; metres",
    options=bd.options, current=bd.current, configure=bd.configure,
    breakdown=bd.breakdown, checks=bd.checks,
)  # fmt: skip
register(MODULE)
