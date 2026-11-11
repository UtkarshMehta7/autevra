"""A light aircraft's functional and logical architecture.

The pitch-control chain is modelled end to end (pilot → control column → cables and
pushrods → elevator, with the trim, the stabiliser carrying the hinge loads into the
fuselage, and the airflow loading the surfaces); the other functions are allocated at
system level. Interface values are typical targets for a light aircraft, stated as agreed
values, not measured. FMEA ratings are starting values for review.
"""

from autevra.modules import Values
from autevra.product.systems import Architecture, Block, FailureMode, Flow, Function

FUNCTIONS = [
    Function(id="lift", name="generate lift"),
    Function(id="thrust", name="provide thrust"),
    Function(id="control", name="control attitude and trajectory"),
    Function(id="control_pitch", name="control pitch", parent="control"),
    Function(id="pitch_input", name="transmit the pilot's pitch input", parent="control_pitch"),
    Function(id="pitch_moment", name="generate pitch moment", parent="control_pitch"),
    Function(id="pitch_trim", name="trim pitch", parent="control_pitch"),
    Function(id="control_roll", name="control roll", parent="control"),
    Function(id="control_yaw", name="control yaw", parent="control"),
    Function(id="loads", name="carry structural loads"),
    Function(id="ground", name="support on the ground and absorb landing"),
    Function(id="fuel", name="store and supply fuel"),
    Function(id="power", name="supply electrical power"),
    Function(id="nav", name="navigate and communicate"),
    Function(id="indicate", name="indicate and alert"),
    Function(id="protect", name="protect occupants"),
    Function(id="payload", name="carry payload"),
]  # fmt: skip

BLOCKS = [
    Block(id="pilot", name="Pilot", functions=[], templates=[], external=True),
    Block(id="airflow", name="Airflow", functions=[], templates=[], external=True),
    Block(id="runway", name="Runway", functions=[], templates=[], external=True),
    Block(id="wing", name="Wing", functions=["lift", "loads"],
          templates=["spar", "rib", "wing_skin", "leading_edge", "wing_tip", "flap"]),
    Block(id="fuselage", name="Fuselage", functions=["loads", "protect"],
          templates=["frame", "stringer", "fuselage_skin", "firewall", "cabin_floor", "door",
                     "windscreen", "tail_cone"]),
    Block(id="column", name="Control column", functions=["pitch_input", "control_roll"],
          templates=["control_column"]),
    Block(id="circuit", name="Cables and pushrods",
          functions=["pitch_input", "control_roll", "control_yaw"],
          templates=["control_cables", "pushrods"]),
    Block(id="elevator", name="Elevator", functions=["pitch_moment"], templates=["elevator"]),
    Block(id="stabiliser", name="Horizontal stabiliser", functions=["pitch_moment", "loads"],
          templates=["stabiliser"]),
    Block(id="trim", name="Pitch trim", functions=["pitch_trim"], templates=["trim"]),
    Block(id="ailerons", name="Ailerons", functions=["control_roll"], templates=["aileron"]),
    Block(id="pedals", name="Rudder pedals", functions=["control_yaw"],
          templates=["rudder_pedals"]),
    Block(id="vertical_tail", name="Fin and rudder", functions=["control_yaw", "loads"],
          templates=["fin", "rudder"]),
    Block(id="gear", name="Landing gear", functions=["ground"],
          templates=["main_leg", "main_wheel", "nose_leg", "nose_wheel", "tailwheel",
                     "retraction", "brake_hydraulics"]),
    Block(id="engine", name="Engine installation", functions=["thrust"],
          templates=["engine", "engine_mount", "cowling", "exhaust", "engine_accessories"]),
    Block(id="propeller", name="Propeller", functions=["thrust"], templates=["propeller"]),
    Block(id="fuel_system", name="Fuel system", functions=["fuel"],
          templates=["fuel_tank", "fuel_lines", "fuel_pump", "fuel_gauging"]),
    Block(id="electrical", name="Electrical system", functions=["power"],
          templates=["alternator", "battery", "harness", "electrical_bus"]),
    Block(id="avionics", name="Avionics", functions=["nav", "indicate"],
          templates=["displays", "radios", "pitot_static"]),
    Block(id="cabin", name="Cabin", functions=["protect", "payload"],
          templates=["seat", "restraints", "linings", "baggage"]),
]  # fmt: skip

FLOWS = [
    # pitch-control chain
    Flow(id="stick_force", kind="mechanical", source="pilot", target="column",
         item="stick force and travel",
         attributes={"stick force per g": "≥ 4.5 lbf/g target (light aircraft practice)"}),
    Flow(id="column_motion", kind="mechanical", source="column", target="circuit",
         item="control displacement"),
    Flow(id="elevator_drive", kind="mechanical", source="circuit", target="elevator",
         item="elevator deflection", attributes={"range": "+25° / -20°"}),
    Flow(id="trim_tab", kind="mechanical", source="trim", target="elevator",
         item="trim deflection"),
    Flow(id="elevator_air", kind="mechanical", source="airflow", target="elevator",
         item="aerodynamic load"),
    Flow(id="hinge_moment", kind="mechanical", source="elevator", target="stabiliser",
         item="hinge loads"),
    Flow(id="tail_loads", kind="mechanical", source="stabiliser", target="fuselage",
         item="tail loads at the attachment"),
    # other systems
    Flow(id="wing_air", kind="mechanical", source="airflow", target="wing", item="lift and drag"),
    Flow(id="wing_loads", kind="mechanical", source="wing", target="fuselage",
         item="wing attachment loads"),
    Flow(id="fuel_flow", kind="fluid", source="fuel_system", target="engine", item="fuel flow",
         attributes={"medium": "avgas 100LL"}),
    Flow(id="shaft_power", kind="mechanical", source="engine", target="propeller",
         item="shaft power"),
    Flow(id="thrust_out", kind="mechanical", source="propeller", target="airflow", item="thrust"),
    Flow(id="alternator_drive", kind="mechanical", source="engine", target="electrical",
         item="alternator drive"),
    Flow(id="avionics_power", kind="electrical_power", source="electrical", target="avionics",
         item="14 V / 28 V bus"),
    Flow(id="flight_data", kind="signal", source="avionics", target="pilot",
         item="flight and engine data"),
    Flow(id="engine_heat", kind="thermal", source="engine", target="airflow",
         item="cooling air heat"),
    Flow(id="landing_loads", kind="mechanical", source="runway", target="gear",
         item="landing and ground loads"),
    Flow(id="gear_loads", kind="mechanical", source="gear", target="fuselage",
         item="gear attachment loads"),
    Flow(id="roll_drive", kind="mechanical", source="circuit", target="ailerons",
         item="aileron deflection"),
    Flow(id="yaw_input", kind="mechanical", source="pilot", target="pedals", item="pedal force"),
    Flow(id="rudder_drive", kind="mechanical", source="pedals", target="vertical_tail",
         item="rudder deflection"),
]  # fmt: skip

FAILURE_MODES = [
    FailureMode(id="circuit_disconnect", function="pitch_input", block="circuit",
                mode="cable or pushrod disconnection", effect="loss of elevator control",
                severity=10, occurrence=2, detection=6,
                action="duplicate inspection after maintenance; safety-wired fasteners"),
    FailureMode(id="elevator_flutter", function="pitch_moment", block="elevator",
                mode="flutter", effect="structural failure of the tail", severity=10,
                occurrence=2, detection=7,
                action="mass balance; flutter clearance analysis (planned)"),
    FailureMode(id="trim_runaway", function="pitch_trim", block="trim",
                mode="trim jammed at full deflection", effect="high stick forces",
                severity=7, occurrence=2, detection=3, action="trim within pilot override"),
    FailureMode(id="power_loss", function="thrust", block="engine", mode="engine power loss",
                effect="forced landing", severity=9, occurrence=3, detection=3,
                action="fuel management; carburettor heat; glide procedures"),
    FailureMode(id="fuel_contamination", function="fuel", block="fuel_system",
                mode="water in fuel", effect="engine stoppage", severity=8, occurrence=3,
                detection=4, action="sump drains checked before flight"),
    FailureMode(id="alternator_failure", function="power", block="electrical",
                mode="alternator failure", effect="battery-only endurance", severity=5,
                occurrence=4, detection=2),
    FailureMode(id="nose_gear_collapse", function="ground", block="gear",
                mode="nose gear collapse", effect="prop strike, airframe damage", severity=7,
                occurrence=2, detection=4, action="landing load case sizing (planned)"),
]  # fmt: skip

ARCHITECTURE = Architecture(functions=FUNCTIONS, blocks=BLOCKS, flows=FLOWS,
                            failure_modes=FAILURE_MODES)  # fmt: skip


def architecture(values: Values) -> Architecture:
    return ARCHITECTURE
