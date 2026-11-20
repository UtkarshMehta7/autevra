"""A small displacement vessel (workboat, motor yacht): options, the breakdown by SFI-style
groups (100 hull, 200 propulsion, 300 electrical, 400 navigation, 500 auxiliary, 600
outfit) and its checks.

Masses: the displacement comes from the hull's hydrostatics; the lightship is a stated
fraction of it for small craft by hull material (steel 0.60, aluminium 0.50, GRP 0.52;
statistical, about 15 %), split into the groups and parts by stated shares (level 0
allocations); the rest is deadweight (fuel, water, crew and payload). Frame: x forward
from the aft perpendicular, y to port, z up from the keel (m).
"""

from typing import Any

from autevra.marine import hull as hk
from autevra.modules import Check, Values
from autevra.product import templates as tpl
from autevra.product.breakdown import Node, RolledNode
from autevra.product.options import Configuration, OptionFamily, Options
from autevra.product.templates import PartTemplate

MODULE = "marine"
LIGHTSHIP = {"steel": 0.60, "aluminium": 0.50, "grp": 0.52}
MATERIALS = {"Steel": "steel", "Aluminium": "aluminium", "GRP": "grp"}
GROUP_SHARE = {"100": 0.42, "200": 0.18, "300": 0.05, "400": 0.02, "500": 0.08, "600": 0.25}
GROUPS = {"100": "Hull structure", "200": "Propulsion", "300": "Electrical plant",
          "400": "Navigation and command", "500": "Auxiliary systems",
          "600": "Outfit and furnishing"}  # fmt: skip


def spec_of(values: Values) -> hk.HullSpec:
    return hk.HullSpec.model_validate({k: v for k, v in values.items()
                                       if k in hk.HullSpec.model_fields})  # fmt: skip


def options(values: Values) -> Options:
    return Options(families=[
        OptionFamily(id="material", label="Hull material", choices=list(MATERIALS)),
        OptionFamily(id="propulsion", label="Propulsion", choices=["Single shaft", "Twin shaft"]),
        OptionFamily(id="thruster", label="Bow thruster", choices=["None", "Fitted"]),
    ])  # fmt: skip


def current(values: Values) -> dict[str, str]:
    mat = next((k for k, v in MATERIALS.items() if v == values.get("material")), "Steel")
    return {"material": mat,
            "propulsion": "Twin shaft" if values.get("twin_shaft") else "Single shaft",
            "thruster": "Fitted" if values.get("bow_thruster") else "None"}  # fmt: skip


def configure(values: Values, config: Configuration) -> dict[str, Any]:
    c = {**current(values), **config}
    return {**values, "material": MATERIALS[c["material"]],
            "twin_shaft": c["propulsion"] == "Twin shaft",
            "bow_thruster": c["thruster"] == "Fitted"}  # fmt: skip


TWIN, SINGLE = "propulsion == 'Twin shaft'", "propulsion == 'Single shaft'"
# id, name, group, process, functions, share of the group, instances rule
_T: tuple[tuple[str, str, str, str, tuple[str, ...], float], ...] = (
    ("shell", "Shell plating (bottom and sides)", "100", "sheet metal",
     ("provide buoyancy", "resist sea loads"), 0.40),
    ("frame", "Transverse frame", "100", "weldment", ("resist sea loads",), 0.20),
    ("longitudinal", "Longitudinals and stringers", "100", "extrusion", ("resist sea loads",),
     0.10),
    ("bulkhead", "Watertight bulkhead", "100", "sheet metal",
     ("provide buoyancy", "resist sea loads"), 0.10),
    ("deck", "Deck and beams", "100", "sheet metal", ("resist sea loads",), 0.12),
    ("deckhouse", "Deckhouse", "100", "sheet metal", ("accommodate crew",), 0.08),
    ("main_engine", "Main engine (Mechanical module item)", "200", "inventory", ("propel",),
     0.55),
    ("gearbox", "Marine gearbox", "200", "inventory", ("propel",), 0.12),
    ("shaft_line", "Shaft line (shaft, couplings, bearings)", "200", "machining", ("propel",),
     0.10),
    ("propeller", "Propeller", "200", "casting", ("propel",), 0.05),
    ("stern_tube", "Stern tube and seal", "200", "machining", ("propel",), 0.05),
    ("engine_bed", "Engine bed", "200", "weldment", ("propel",), 0.08),
    ("marine_exhaust", "Wet exhaust", "200", "tube", ("propel",), 0.05),
    ("generator", "Generator set", "300", "inventory", ("supply power",), 0.40),
    ("batteries", "Battery banks", "300", "inventory", ("supply power",), 0.30),
    ("switchboard", "Switchboard", "300", "assembly", ("supply power",), 0.10),
    ("cabling", "Cabling", "300", "assembly", ("supply power",), 0.20),
    ("helm", "Helm console", "400", "moulding", ("navigate",), 0.30),
    ("radar", "Radar and antennas", "400", "inventory", ("navigate",), 0.20),
    ("nav_lights", "Navigation lights", "400", "inventory", ("navigate",), 0.10),
    ("mast", "Mast", "400", "tube", ("navigate",), 0.40),
    ("fuel_tank", "Fuel tank", "500", "weldment", ("handle fluids",), 0.30),
    ("water_tank", "Fresh-water tank", "500", "moulding", ("handle fluids",), 0.15),
    ("bilge", "Bilge pumps and piping", "500", "tube", ("handle fluids",), 0.15),
    ("steering", "Steering gear and rudder", "500", "weldment", ("manoeuvre",), 0.25),
    ("thruster", "Bow thruster", "500", "inventory", ("manoeuvre",), 0.0),
    ("fire", "Fire detection and extinguishing", "500", "inventory", ("handle fluids",), 0.15),
    ("hatches", "Hatches and doors", "600", "sheet metal", ("accommodate crew",), 0.15),
    ("windows", "Windows", "600", "glass", ("accommodate crew",), 0.10),
    ("railings", "Railings", "600", "tube", ("moor and anchor",), 0.15),
    ("mooring", "Cleats and bollards", "600", "casting", ("moor and anchor",), 0.10),
    ("anchor", "Anchor, chain and windlass", "600", "inventory", ("moor and anchor",), 0.20),
    ("interior", "Seating and interior", "600", "moulding", ("accommodate crew",), 0.30),
)  # fmt: skip
GEOMETRY = {"shell": "hull", "deck": "hull", "deckhouse": "deckhouse", "mast": "mast",
            "propeller": "propeller", "steering": "rudder"}  # fmt: skip
tpl.register(*(PartTemplate(id=i, module=MODULE, name=n, code=f"SFI {g}", process=p,
                            functions=f, max_maturity=1 if i in GEOMETRY else 0)
               for i, n, g, p, f, _ in _T))  # fmt: skip


def breakdown(values: Values) -> Node:
    s = spec_of(values)
    hs = hk.hydrostatics(s)
    disp = hs["displacement_t"] * 1000  # kg
    mat = str(values.get("material", s.material))
    light = LIGHTSHIP.get(mat, 0.6) * disp
    twin = bool(values.get("twin_shaft"))
    thruster = bool(values.get("bow_thruster"))
    frames = max(round(s.length / 0.5), 6)
    counts = {"frame": frames, "bulkhead": 3 if s.length < 20 else 5,
              "main_engine": 2 if twin else 1, "propeller": 2 if twin else 1,
              "shaft_line": 2 if twin else 1, "stern_tube": 2 if twin else 1,
              "gearbox": 2 if twin else 1, "nav_lights": 4, "mooring": 6}  # fmt: skip
    cg = {"100": (0.48 * s.length, 0.0, 0.55 * s.depth),
          "200": (0.3 * s.length, 0.0, 0.35 * s.draft),
          "300": (0.4 * s.length, 0.0, 0.5 * s.draft),
          "400": (0.55 * s.length, 0.0, s.depth + 1.2),
          "500": (0.4 * s.length, 0.0, 0.4 * s.draft),
          "600": (0.5 * s.length, 0.0, s.depth)}  # fmt: skip
    groups: dict[str, list[Node]] = {}
    for tid, name, g, process, funcs, share in _T:
        mass = light * GROUP_SHARE[g] * share
        basis = f"{share:.0%} of SFI {g} ({GROUP_SHARE[g]:.0%} of a {mat} lightship)"
        app = ""
        if tid == "thruster":
            mass, basis, app = 0.004 * disp, "0.4 % of displacement", "thruster == 'Fitted'"
        groups.setdefault(g, []).append(Node(
            id=tid, name=name, kind="part", code=f"SFI {g}", template=tid, process=process,
            functions=list(funcs), applicability=app, instances=counts.get(tid, 1),
            maturity=1 if tid in GEOMETRY else 0, mass=mass, mass_source="allocated",
            basis=basis, cg=cg[g], geometry=GEOMETRY.get(tid, "")))  # fmt: skip
    del thruster
    children = [Node(id=f"sfi{g}", name=GROUPS[g], kind="system", code=f"SFI {g}",
                     children=parts) for g, parts in groups.items()]  # fmt: skip
    dead = max(disp - light - (0.004 * disp if values.get("bow_thruster") else 0.0), 0.0)
    children.append(Node(id="deadweight", name="Deadweight (fuel, water, crew, payload)",
                         kind="system", code="deadweight", mass=dead, mass_source="estimated",
                         basis="displacement less lightship", cg=(0.45 * s.length, 0.0,
                                                                   0.6 * s.depth)))  # fmt: skip
    return Node(id="vessel", name=s.name, kind="product", code="vessel",
                budget=disp * 1.0001, children=children)  # fmt: skip


def checks(values: Values, root: RolledNode) -> list[Check]:
    s = spec_of(values)
    crit = hk.imo_criteria(s)
    failed = [c["criterion"] for c in crit if not c["pass"]]
    res = hk.resistance(s)
    out = [
        Check(id="stability", label="Intact stability (IMO IS Code)",
              status="pass" if not failed else "fail",
              message="all six general criteria met" if not failed else
              "not met: " + ", ".join(failed)),
        Check(id="froude", label="Speed regime", status="pass" if res["froude"] <= 0.45 else "warn",
              message=f"Froude number {res['froude']:.2f}, wave-making "
              f"{100 * res['wave_resistance_n'] / res['total_resistance_n']:.0f} % of the "
              "resistance: " + ("displacement regime" if res["froude"] <= 0.45 else
                                "beyond the range the resistance method supports well")),
        Check(id="freeboard", label="Freeboard", status="pass" if s.depth - s.draft >= 0.08 *
              s.length ** 0.5 * 2 else "warn", message=f"{s.depth - s.draft:.2f} m"),
    ]  # fmt: skip
    del root
    return out
