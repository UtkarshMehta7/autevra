"""A piston engine's functions, logical blocks, typed flows and design FMEA.

The energy chain is modelled end to end: air and fuel → combustion chambers → pistons and
cranktrain → flywheel (to the consumer), with exhaust gas, heat to the coolant and oil to
the bearings. FMEA ratings are starting values for review."""

from autevra.modules import Values
from autevra.product.systems import Architecture, Block, FailureMode, Flow, Function

PETROL, DIESEL, TURBO = "fuel == 'Petrol'", "fuel == 'Diesel'", "aspiration == 'Turbocharged'"

FUNCTIONS = [
    Function(id="convert", name="convert fuel energy to shaft power"),
    Function(id="charge", name="admit air and fuel", parent="convert"),
    Function(id="ignite", name="ignite the charge", parent="convert"),
    Function(id="expand", name="turn gas pressure into crank torque", parent="convert"),
    Function(id="deliver", name="deliver torque to the consumer", parent="convert"),
    Function(id="contain", name="contain combustion pressure"),
    Function(id="forces", name="transmit and balance forces"),
    Function(id="exhaust", name="expel the exhaust gas"),
    Function(id="time", name="time the valves to the crank"),
    Function(id="heat", name="reject heat"),
    Function(id="lube", name="lubricate"),
    Function(id="control", name="control and monitor"),
    Function(id="mount", name="mount to the consumer"),
]  # fmt: skip

BLOCKS = [
    Block(id="ambient", name="Ambient air", functions=[], templates=[], external=True),
    Block(id="fuel_supply", name="Vehicle fuel supply", functions=[], templates=[],
          external=True),
    Block(id="consumer", name="Gearbox / propeller (consumer)", functions=[], templates=[],
          external=True),
    Block(id="radiator", name="Vehicle radiator", functions=[], templates=[], external=True),
    Block(id="intake", name="Intake system", functions=["charge"],
          templates=["air_box", "throttle", "intake_manifold"]),
    Block(id="turbo", name="Turbocharger and intercooler", functions=["charge", "exhaust"],
          templates=["turbocharger", "intercooler"], applicability=TURBO),
    Block(id="injection", name="Fuel injection", functions=["charge"],
          templates=["injector", "fuel_rail", "hp_pump"]),
    Block(id="ignition", name="Ignition", functions=["ignite"],
          templates=["spark_plug", "coil", "glow_plug"]),
    Block(id="chambers", name="Combustion chambers", functions=["contain", "expand"],
          templates=["head", "head_gasket", "block", "piston", "piston_rings"]),
    Block(id="cranktrain", name="Cranktrain", functions=["expand", "forces"],
          templates=["conrod", "gudgeon_pin", "crankshaft", "main_bearing", "big_end_bearing",
                     "damper", "bedplate"]),
    Block(id="flywheel", name="Flywheel", functions=["deliver"], templates=["flywheel"]),
    Block(id="valvetrain", name="Valvetrain", functions=["charge", "exhaust"],
          templates=["camshaft", "valve", "valve_spring", "follower", "cam_phaser"]),
    Block(id="timing", name="Timing drive", functions=["time"],
          templates=["timing_chain", "front_cover"]),
    Block(id="exhaust_m", name="Exhaust manifold", functions=["exhaust"],
          templates=["exhaust_manifold"]),
    Block(id="lubrication", name="Lubrication", functions=["lube"],
          templates=["oil_pump", "oil_filter", "sump", "cam_cover"]),
    Block(id="cooling", name="Cooling", functions=["heat"], templates=["water_pump",
                                                                         "thermostat"]),
    Block(id="accessories", name="Accessory drive", functions=["control", "forces"],
          templates=["alternator", "starter", "accessory_belt"]),
    Block(id="ecu", name="Engine control", functions=["control"], templates=["ecu"]),
    Block(id="mounts", name="Mounts", functions=["mount"], templates=["engine_mount"]),
]  # fmt: skip

FLOWS = [
    Flow(id="air_in", kind="fluid", source="ambient", target="intake", item="fresh air"),
    Flow(id="boost", kind="fluid", source="turbo", target="intake", item="boost air",
         attributes={"pressure": "up to about 2.5 bar absolute"}, applicability=TURBO),
    Flow(id="charge_air", kind="fluid", source="intake", target="chambers", item="charge air"),
    Flow(id="fuel_in", kind="fluid", source="fuel_supply", target="injection", item="fuel",
         attributes={"rail pressure": "200-350 bar petrol DI, up to 2,500 bar diesel"}),
    Flow(id="fuel_spray", kind="fluid", source="injection", target="chambers",
         item="injected fuel"),
    Flow(id="spark", kind="electrical_power", source="ignition", target="chambers",
         item="spark / glow heat"),
    Flow(id="gas_force", kind="mechanical", source="chambers", target="cranktrain",
         item="gas force on the pistons"),
    Flow(id="crank_torque", kind="mechanical", source="cranktrain", target="flywheel",
         item="crank torque"),
    Flow(id="output", kind="mechanical", source="flywheel", target="consumer",
         item="output torque and speed"),
    Flow(id="cam_drive", kind="mechanical", source="cranktrain", target="timing",
         item="crank rotation"),
    Flow(id="valve_drive", kind="mechanical", source="timing", target="valvetrain",
         item="cam rotation (half crank speed)"),
    Flow(id="valve_events", kind="mechanical", source="valvetrain", target="chambers",
         item="valve lift"),
    Flow(id="exhaust_gas", kind="fluid", source="chambers", target="exhaust_m",
         item="exhaust gas"),
    Flow(id="turbine_gas", kind="fluid", source="exhaust_m", target="turbo",
         item="exhaust to the turbine", applicability=TURBO),
    Flow(id="coolant_heat", kind="thermal", source="chambers", target="cooling",
         item="heat to the coolant"),
    Flow(id="to_radiator", kind="thermal", source="cooling", target="radiator",
         item="hot coolant"),
    Flow(id="oil", kind="fluid", source="lubrication", target="cranktrain",
         item="pressurised oil", attributes={"pressure": "about 1-5 bar"}),
    Flow(id="oil_valvetrain", kind="fluid", source="lubrication", target="valvetrain",
         item="oil to the cams"),
    Flow(id="accessory_drive", kind="mechanical", source="cranktrain", target="accessories",
         item="belt drive"),
    Flow(id="ecu_injection", kind="signal", source="ecu", target="injection",
         item="injection timing and quantity"),
    Flow(id="ecu_ignition", kind="signal", source="ecu", target="ignition",
         item="ignition timing"),
    Flow(id="ecu_power", kind="electrical_power", source="accessories", target="ecu",
         item="12 V supply"),
    Flow(id="mount_loads", kind="mechanical", source="cranktrain", target="mounts",
         item="reaction torque and free forces"),
]  # fmt: skip

FAILURE_MODES = [
    FailureMode(id="oil_starvation", function="lube", block="lubrication",
                mode="oil starvation", effect="bearing seizure, engine destroyed",
                severity=10, occurrence=2, detection=4,
                action="oil pressure warning; pickup sized for cornering"),
    FailureMode(id="overheating", function="heat", block="cooling", mode="coolant loss",
                effect="head gasket failure", severity=8, occurrence=3, detection=3,
                action="coolant temperature warning and limp mode"),
    FailureMode(id="knock", function="contain", block="chambers",
                mode="knock (detonation)", effect="piston and ring damage", severity=8,
                occurrence=3, detection=4, action="knock sensors and ignition retard"),
    FailureMode(id="chain_stretch", function="time", block="timing",
                mode="timing chain stretch", effect="valve timing error, valve-piston contact",
                severity=9, occurrence=2, detection=5,
                action="cam/crank correlation monitoring"),
    FailureMode(id="ring_wear", function="contain", block="chambers", mode="ring wear",
                effect="oil consumption, lower compression", severity=5, occurrence=4,
                detection=5),
    FailureMode(id="turbo_bearing", function="charge", block="turbo",
                mode="turbo bearing failure", effect="loss of boost, oil in intake",
                severity=7, occurrence=3, detection=4,
                action="oil feed and cool-down strategy"),
]  # fmt: skip

ARCHITECTURE = Architecture(functions=FUNCTIONS, blocks=BLOCKS, flows=FLOWS,
                            failure_modes=FAILURE_MODES)  # fmt: skip


def architecture(values: Values) -> Architecture:
    return ARCHITECTURE
