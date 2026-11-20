"""Marine module: small displacement vessels (workboats, motor yachts): hull form,
hydrostatics, intact stability against the IMO criteria, viscous resistance, the SFI-style
breakdown, architecture, loads and production."""

from autevra.modules import ModuleDef, register
from autevra.modules.marine import loads, systems
from autevra.modules.marine import vessel as bd

MODULE = ModuleDef(
    id="marine", domain="marine", name="Marine",
    frame="x forward from the aft perpendicular, y to port, z up from the keel; metres",
    options=bd.options, current=bd.current, configure=bd.configure,
    breakdown=bd.breakdown, checks=bd.checks, architecture=systems.architecture,
    loads=loads.cases, compliance=loads.compliance, stations=loads.STATIONS,
    station_order=loads.ORDER, stackups=loads.stackups,
)  # fmt: skip
register(MODULE)
