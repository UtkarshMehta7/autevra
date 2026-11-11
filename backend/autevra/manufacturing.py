"""Manufacturing view (platform service): the MBOM by station, a process plan with
indicative times and costs, line balance at a takt time, material cost and CO2, and the
reconciliation of the MBOM against the design breakdown (EBOM).

Indicative process data (stated, concept level; a real plan uses the plant's own rates):
per instance, time = setup + rate x mass (minutes), at a machine rate (EUR/h) plus labour
at 40 EUR/h; material bought = mass x buy-to-fly (scrap and offcut) at the material's
indicative price; bought-out items (standard, inventory, glass) are priced per kg by
category and only fitted. Fitting at assembly: 0.4 min + 0.02 min/kg per instance.
"""

import math

from pydantic import BaseModel

from autevra import materials
from autevra.product.breakdown import Node

LABOUR = 40.0  # EUR/h
# process -> (setup min, min per kg, machine EUR/h, buy-to-fly, default material, bought-out)
PROCESS: dict[str, tuple[float, float, float, float, str, bool]] = {
    "sheet metal": (0.4, 0.010, 250.0, 1.45, "dp600", False),
    "casting": (3.5, 0.45, 120.0, 1.15, "a356_t6", False),
    "forging": (4.0, 0.40, 150.0, 1.35, "42crmo4", False),
    "machining": (3.0, 0.50, 80.0, 1.6, "42crmo4", False),
    "moulding": (0.8, 0.05, 70.0, 1.05, "pa66_gf30", False),
    "extrusion": (0.5, 0.05, 60.0, 1.15, "6061_t6", False),
    "weldment": (5.0, 0.40, 60.0, 1.20, "s355", False),
    "composite": (30.0, 6.0, 50.0, 1.35, "cfrp_qi", False),
    "tube": (1.0, 0.20, 50.0, 1.10, "s355", False),
    "additive": (60.0, 20.0, 90.0, 1.10, "ti6al4v", False),
    "assembly": (4.0, 0.20, 0.0, 1.0, "", True),
    "glass": (0.0, 0.0, 0.0, 1.0, "", True),
    "standard": (0.0, 0.0, 0.0, 1.0, "", True),
    "inventory": (0.0, 0.0, 0.0, 1.0, "", True),
}
BOUGHT_EUR_PER_KG = {"assembly": 12.0, "glass": 6.0, "standard": 8.0, "inventory": 20.0}


class Operation(BaseModel):
    part: str
    name: str
    process: str
    station: str
    instances: int
    make_min: float  # fabrication time, all instances (0 for bought-out)
    fit_min: float  # assembly time at the station
    material: str
    material_kg: float
    cost_eur: float
    co2_kg: float
    bought_out: bool


class Station(BaseModel):
    name: str
    operations: int
    work_min: float  # fitting work content
    operators: int  # at the takt time
    make_min: float  # fabrication feeding this station


class Plan(BaseModel):
    stations: list[Station]
    operations: list[Operation]
    takt_s: float
    total_cost_eur: float
    total_co2_kg: float
    material_cost_eur: float
    labour_and_machine_eur: float
    reconciliation: list[str]  # problems; empty when every EBOM part is used once


def plan(root: Node, station_of: dict[str, str], order: list[str], takt_s: float = 60.0,
         default_station: str = "Final assembly") -> Plan:  # fmt: skip
    """Process plan for a configured breakdown. ``station_of`` maps breakdown codes (or
    code prefixes) to stations, longest prefix first."""

    def station(code: str) -> str:
        best = max((p for p in station_of if code.startswith(p)), key=len, default=None)
        return station_of[best] if best else default_station

    ops: list[Operation] = []
    for n in root.walk():
        if n.kind != "part" or n.mass <= 0:
            continue
        setup, rate, machine, btf, mat_id, bought = PROCESS.get(n.process, PROCESS["assembly"])
        each = n.mass / n.instances
        make = 0.0 if bought else n.instances * (setup + rate * each)
        fit = n.instances * (0.4 + 0.02 * each)
        if bought:
            mat_name, kg = "bought-out", n.mass
            cost = n.mass * BOUGHT_EUR_PER_KG.get(n.process, 15.0)
            co2 = n.mass * 5.0  # generic purchased-part footprint (estimate)
        else:
            mat = materials.get(mat_id)
            mat_name, kg = mat.id, n.mass * btf
            cost = kg * mat.cost_eur_per_kg + make / 60 * (machine + LABOUR)
            co2 = kg * mat.co2_kg_per_kg
        cost += fit / 60 * LABOUR
        ops.append(Operation(part=n.id, name=n.name, process=n.process, station=station(n.code),
                             instances=n.instances, make_min=round(make, 2),
                             fit_min=round(fit, 2), material=mat_name,
                             material_kg=round(kg, 3), cost_eur=round(cost, 2),
                             co2_kg=round(co2, 2), bought_out=bought))  # fmt: skip
    names = list(dict.fromkeys([*order, *(o.station for o in ops)]))
    stations = []
    for s in names:
        mine = [o for o in ops if o.station == s]
        if not mine:
            continue
        work = sum(o.fit_min for o in mine)
        stations.append(Station(name=s, operations=len(mine), work_min=round(work, 2),
                                operators=max(1, math.ceil(work * 60 / takt_s)),
                                make_min=round(sum(o.make_min for o in mine), 2)))  # fmt: skip
    # reconciliation: every part of the EBOM consumed exactly once
    ebom = [n.id for n in root.walk() if n.kind == "part" and n.mass > 0]
    used = [o.part for o in ops]
    problems = [f"part '{p}' appears {used.count(p)} times in the MBOM" for p in
                set(used) if used.count(p) != 1]  # fmt: skip
    problems += [f"part '{p}' is not in the MBOM" for p in ebom if p not in used]
    material = sum(o.material_kg * materials.get(o.material).cost_eur_per_kg for o in ops
                   if not o.bought_out)  # fmt: skip
    total = sum(o.cost_eur for o in ops)
    return Plan(stations=stations, operations=ops, takt_s=takt_s, total_cost_eur=round(total, 2),
                total_co2_kg=round(sum(o.co2_kg for o in ops), 1),
                material_cost_eur=round(material, 2),
                labour_and_machine_eur=round(total - material, 2),
                reconciliation=problems)  # fmt: skip
