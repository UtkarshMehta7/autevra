"""A vessel's functions, logical blocks, typed flows and design FMEA. The propulsion chain
is modelled end to end: fuel → main engine → gearbox → shaft line → propeller → water."""

from autevra.modules import Values
from autevra.product.systems import Architecture, Block, FailureMode, Flow, Function

THRUSTER = "thruster == 'Fitted'"

FUNCTIONS = [
    Function(id="buoyancy", name="provide buoyancy"),
    Function(id="stability", name="remain stable"),
    Function(id="sea_loads", name="resist sea loads"),
    Function(id="propel", name="propel"),
    Function(id="manoeuvre", name="manoeuvre"),
    Function(id="power", name="supply power"),
    Function(id="fluids", name="handle fluids (fuel, water, bilge)"),
    Function(id="navigate", name="navigate"),
    Function(id="moor", name="moor and anchor"),
    Function(id="accommodate", name="accommodate crew and passengers"),
]  # fmt: skip

BLOCKS = [
    Block(id="sea", name="Sea", functions=[], templates=[], external=True),
    Block(id="crew", name="Crew", functions=[], templates=[], external=True),
    Block(id="hull", name="Hull", functions=["buoyancy", "stability", "sea_loads"],
          templates=["shell", "frame", "longitudinal", "bulkhead", "deck"]),
    Block(id="engine", name="Main engine", functions=["propel"],
          templates=["main_engine", "engine_bed", "marine_exhaust"]),
    Block(id="gearbox", name="Gearbox", functions=["propel"], templates=["gearbox"]),
    Block(id="shaft", name="Shaft line", functions=["propel"],
          templates=["shaft_line", "stern_tube"]),
    Block(id="propeller", name="Propeller", functions=["propel"], templates=["propeller"]),
    Block(id="steering", name="Steering and rudder", functions=["manoeuvre"],
          templates=["steering"]),
    Block(id="thruster", name="Bow thruster", functions=["manoeuvre"], templates=["thruster"],
          applicability=THRUSTER),
    Block(id="electrical", name="Electrical plant", functions=["power"],
          templates=["generator", "batteries", "switchboard", "cabling"]),
    Block(id="tanks", name="Tanks and piping", functions=["fluids"],
          templates=["fuel_tank", "water_tank", "bilge", "fire"]),
    Block(id="bridge", name="Bridge and navigation", functions=["navigate"],
          templates=["helm", "radar", "nav_lights", "mast"]),
    Block(id="deck_gear", name="Deck gear", functions=["moor"],
          templates=["anchor", "mooring", "railings"]),
    Block(id="accommodation", name="Accommodation", functions=["accommodate"],
          templates=["deckhouse", "hatches", "windows", "interior"]),
]  # fmt: skip

FLOWS = [
    Flow(id="fuel", kind="fluid", source="tanks", target="engine", item="diesel fuel"),
    Flow(id="engine_torque", kind="mechanical", source="engine", target="gearbox",
         item="engine torque"),
    Flow(id="reduced", kind="mechanical", source="gearbox", target="shaft",
         item="reduced shaft speed and torque", attributes={"reduction": "about 2-3:1"}),
    Flow(id="shaft_torque", kind="mechanical", source="shaft", target="propeller",
         item="shaft torque"),
    Flow(id="thrust", kind="mechanical", source="propeller", target="sea", item="thrust"),
    Flow(id="thrust_bearing", kind="mechanical", source="shaft", target="hull",
         item="thrust into the hull"),
    Flow(id="sea_loads", kind="mechanical", source="sea", target="hull",
         item="hydrostatic and wave loads"),
    Flow(id="helm", kind="signal", source="crew", target="bridge", item="helm and throttle"),
    Flow(id="steer", kind="signal", source="bridge", target="steering", item="rudder order"),
    Flow(id="thruster_order", kind="signal", source="bridge", target="thruster",
         item="thruster order", applicability=THRUSTER),
    Flow(id="rudder_force", kind="mechanical", source="steering", target="sea",
         item="rudder force"),
    Flow(id="power", kind="electrical_power", source="electrical", target="bridge",
         item="12/24 V supply"),
    Flow(id="heat", kind="thermal", source="engine", target="sea",
         item="raw-water cooling"),
]  # fmt: skip

FAILURE_MODES = [
    FailureMode(id="flooding", function="buoyancy", block="hull", mode="hull breach",
                effect="flooding, loss of buoyancy", severity=10, occurrence=2, detection=3,
                action="watertight bulkheads; bilge alarms"),
    FailureMode(id="engine_loss", function="propel", block="engine", mode="engine failure",
                effect="loss of propulsion near a lee shore", severity=8, occurrence=3,
                detection=3, action="twin shaft option; anchor ready"),
    FailureMode(id="shaft_seal", function="propel", block="shaft", mode="stern seal leak",
                effect="water ingress", severity=7, occurrence=3, detection=3,
                action="bilge alarm; dripless seal inspection"),
    FailureMode(id="steering_loss", function="manoeuvre", block="steering",
                mode="steering failure", effect="loss of course control", severity=8,
                occurrence=2, detection=2, action="emergency tiller"),
]  # fmt: skip

ARCHITECTURE = Architecture(functions=FUNCTIONS, blocks=BLOCKS, flows=FLOWS,
                            failure_modes=FAILURE_MODES)  # fmt: skip


def architecture(values: Values) -> Architecture:
    return ARCHITECTURE
