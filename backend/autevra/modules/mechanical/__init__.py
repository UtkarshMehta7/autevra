"""Mechanical module: engines category by category (piston, electric machine, gas
turbine), designed as products and published to the shared inventory. A project's
``category`` value selects the product model."""

from autevra.modules import ModuleDef, Values, register
from autevra.modules.mechanical import engine as bd
from autevra.modules.mechanical import loads, machines, systems
from autevra.product.options import OptionFamily, Options
from autevra.product.systems import Architecture, Block, Flow, Function


def _cat(values: Values) -> str:
    return str(values.get("category", "piston"))


def options(values: Values) -> Options:
    cat = _cat(values)
    if cat == "electric":
        return Options(families=[OptionFamily(id="cooling", label="Cooling",
                                              choices=["Water jacket", "Oil spray"],
                                              affects_mass=False)])  # fmt: skip
    if cat == "turbine":
        return Options(families=[OptionFamily(id="kind", label="Type",
                                              choices=["Turbojet", "Turboshaft"])])  # fmt: skip
    return bd.options(values)


def current(values: Values) -> dict[str, str]:
    cat = _cat(values)
    if cat == "electric":
        return {"cooling": str(values.get("cooling", "Water jacket"))}
    if cat == "turbine":
        return {"kind": "Turboshaft" if values.get("kind") == "turboshaft" else "Turbojet"}
    return bd.current(values)


def configure(values: Values, config: dict) -> dict:  # type: ignore[type-arg]
    cat = _cat(values)
    if cat == "electric":
        return {**values, **config}
    if cat == "turbine":
        kind = {**current(values), **config}["kind"]
        return {**values, "kind": "turboshaft" if kind == "Turboshaft" else "turbojet"}
    return bd.configure(values, config)


def _by(piston, electric, turbine):  # type: ignore[no-untyped-def]
    def pick(values, *rest):  # type: ignore[no-untyped-def]
        fn = {"electric": electric, "turbine": turbine}.get(_cat(values), piston)
        return fn(values, *rest)

    return pick


def _simple(functions: list[tuple[str, str]], blocks: list[tuple[str, str, list[str], list[str]]],
            flows: list[tuple[str, str, str, str, str]]) -> Architecture:  # fmt: skip
    return Architecture(
        functions=[Function(id=i, name=n) for i, n in functions],
        blocks=[Block(id=i, name=n, functions=f, templates=t, external=not f)
                for i, n, f, t in blocks],
        flows=[Flow(id=i, kind=k, source=a, target=b, item=item)  # type: ignore[arg-type]
               for i, k, a, b, item in flows])  # fmt: skip


ELECTRIC_ARCH = _simple(
    [("convert", "convert electrical power to shaft torque"), ("contain", "contain"),
     ("cool", "reject heat"), ("control", "control and monitor"), ("mount", "mount")],
    [("inverter", "Inverter (consumer)", [], []), ("consumer", "Driven load", [], []),
     ("coolant", "Coolant circuit", [], []),
     ("stator", "Stator", ["convert"], ["stator_core", "winding"]),
     ("rotor", "Rotor", ["convert", "mount"], ["rotor_core", "magnets", "motor_shaft",
                                              "motor_bearing"]),
     ("structure", "Housing", ["contain", "cool"], ["motor_housing", "end_shield"]),
     ("sensing", "Position sensing", ["control"], ["resolver"]),
     ("terminals", "Terminals", ["convert"], ["terminal_box"])],
    [("ac", "electrical_power", "inverter", "terminals", "three-phase AC"),
     ("phases", "electrical_power", "terminals", "stator", "phase currents"),
     ("airgap", "mechanical", "stator", "rotor", "electromagnetic torque"),
     ("output", "mechanical", "rotor", "consumer", "shaft torque and speed"),
     ("position", "signal", "sensing", "inverter", "rotor position"),
     ("losses", "thermal", "structure", "coolant", "copper and iron losses")])  # fmt: skip
TURBINE_ARCH = _simple(
    [("convert", "convert fuel energy to thrust or shaft power"), ("contain", "contain"),
     ("control", "control and monitor"), ("mount", "mount")],
    [("ambient", "Ambient air", [], []), ("fuel_supply", "Fuel supply", [], []),
     ("intake", "Intake", ["convert"], ["inlet"]),
     ("compressor", "Compressor", ["convert", "contain"], ["compressor_disc", "compressor_case"]),
     ("combustor", "Combustor", ["convert", "contain"], ["combustor", "fuel_nozzle", "igniter"]),
     ("turbine", "Turbine", ["convert", "contain"], ["turbine_disc", "turbine_case"]),
     ("exhaust", "Exhaust", ["convert"], ["nozzle"]),
     ("spool", "Spool and bearings", ["convert"], ["rotor_shaft", "main_bearing_gt"]),
     ("controls", "Accessories and fuel control", ["control"],
      ["accessory_gearbox", "fuel_control"]),
     ("mounts", "Mounts", ["mount"], ["gt_mount"])],
    [("air", "fluid", "ambient", "intake", "air"),
     ("to_compressor", "fluid", "intake", "compressor", "air"),
     ("compressed", "fluid", "compressor", "combustor", "compressed air"),
     ("fuel", "fluid", "fuel_supply", "controls", "fuel"),
     ("metered", "fluid", "controls", "combustor", "metered fuel"),
     ("hot_gas", "fluid", "combustor", "turbine", "hot gas"),
     ("exhaust_gas", "fluid", "turbine", "exhaust", "exhaust gas"),
     ("shaft_work", "mechanical", "turbine", "spool", "turbine work"),
     ("drive", "mechanical", "spool", "compressor", "compressor drive")])  # fmt: skip

MODULE = ModuleDef(
    id="mechanical", domain="machinery", name="Mechanical",
    frame="x along the crankshaft or rotor to the front, y to the left, z up from the axis; m",
    options=options, current=current, configure=configure,
    breakdown=_by(bd.breakdown, machines.electric_breakdown, machines.turbine_breakdown),
    checks=_by(bd.checks, machines.electric_checks, machines.turbine_checks),
    architecture=_by(systems.architecture, lambda v: ELECTRIC_ARCH, lambda v: TURBINE_ARCH),
    loads=_by(loads.cases, machines.electric_loads, machines.turbine_loads),
    compliance=_by(loads.compliance, lambda v: [], lambda v: []),
    stations=loads.STATIONS + (("engine.stator", "Stator line"), ("engine.rotor", "Rotor line"),
                               ("engine.compressor", "Rotating module"),
                               ("engine.turbine", "Rotating module"),
                               ("engine.combustor", "Hot section")),
    station_order=loads.ORDER[:-1] + ("Stator line", "Rotor line", "Rotating module",
                                      "Hot section", loads.ORDER[-1]),
    stackups=_by(loads.stackups, machines.electric_stack, machines.turbine_stack),
)  # fmt: skip
register(MODULE)
