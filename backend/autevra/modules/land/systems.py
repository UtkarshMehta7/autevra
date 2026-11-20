"""A road vehicle's functional and logical architecture: what it must do, the logical
blocks that do it, the typed flows between them, and design FMEA rows.

The braking chain is modelled end to end (driver → pedal → modulator ↔ controller →
calipers → discs → wheels → road, with wheel-speed sensing, 12 V supply and heat to the
air); the other functions are allocated at system level. Interface values are typical
targets for a passenger car, stated as agreed values in the interface rows, not measured.
FMEA ratings are typical starting values for review.
"""

from autevra.modules import Values
from autevra.product.systems import Architecture, Block, FailureMode, Flow, Function

ICE = "powertrain != 'Battery electric'"
ELECTRIFIED = "powertrain != 'Combustion'"

FUNCTIONS = [
    Function(id="carry", name="carry occupants and cargo"),
    Function(id="protect", name="protect occupants and road users"),
    Function(id="propel", name="propel"),
    Function(id="energy", name="store and supply energy"),
    Function(id="decelerate", name="decelerate and hold"),
    Function(id="brake_command", name="sense the driver's braking demand", parent="decelerate"),
    Function(id="brake_pressure", name="generate and modulate brake pressure",
             parent="decelerate"),
    Function(id="friction", name="generate friction torque at the wheels", parent="decelerate"),
    Function(id="wheel_slip", name="keep the wheels rolling (anti-lock, stability)",
             parent="decelerate"),
    Function(id="road_force", name="transfer braking force to the road", parent="decelerate"),
    Function(id="brake_heat", name="reject braking heat", parent="decelerate"),
    Function(id="steer", name="steer"),
    Function(id="ride", name="support and isolate from the road"),
    Function(id="heat", name="manage heat"),
    Function(id="vision", name="provide vision and visibility"),
    Function(id="comfort", name="provide comfort and climate"),
    Function(id="hmi", name="inform and control"),
    Function(id="sense", name="sense the environment"),
]  # fmt: skip

BLOCKS = [
    Block(id="driver", name="Driver", functions=[], templates=[], external=True),
    Block(id="road", name="Road", functions=[], templates=[], external=True),
    Block(id="air", name="Ambient air", functions=[], templates=[], external=True),
    Block(id="body", name="Body structure",
          functions=["carry", "protect"],
          templates=["side_frame", "floor", "front_structure", "rear_structure", "roof_panel",
                     "crossmember", "bumper_beam", "ladder_frame", "skateboard",
                     "front_subframe", "rear_subframe"]),
    Block(id="closures", name="Closures", functions=["carry", "protect"],
          templates=["front_door", "rear_door", "bonnet", "tailgate", "boot_lid",
                     "cargo_doors"]),
    Block(id="exterior", name="Exterior trim and aero", functions=["protect", "carry"],
          templates=["bumper_fascia", "grille", "fender", "roof_spoiler", "boot_lip",
                     "rear_wing", "roof_rail", "crossbar", "tow_bar"]),
    Block(id="glazing", name="Glazing and mirrors", functions=["vision", "comfort"],
          templates=["windscreen", "side_glass", "backlight", "panoramic_roof", "sunroof",
                     "door_mirror", "camera_mirror"]),
    Block(id="lighting", name="Lighting", functions=["vision"],
          templates=["head_lamp", "tail_lamp"]),
    Block(id="pedal", name="Brake pedal", functions=["brake_command"], templates=["brake_pedal"]),
    Block(id="wheel_speed", name="Wheel speed sensing", functions=["wheel_slip"],
          templates=["wheel_speed_sensor"]),
    Block(id="esc", name="Brake controller (ABS/ESC)", functions=["wheel_slip", "brake_pressure"],
          templates=["ecus"]),
    Block(id="modulator", name="Hydraulic modulator and master cylinder",
          functions=["brake_pressure"], templates=["brake_hydraulics"]),
    Block(id="calipers", name="Calipers", functions=["friction"], templates=["caliper"]),
    Block(id="discs", name="Brake discs", functions=["friction", "brake_heat"],
          templates=["brake_disc"]),
    Block(id="wheels", name="Wheels and tyres", functions=["road_force", "ride"],
          templates=["rim", "tyre"]),
    Block(id="suspension", name="Suspension", functions=["ride"],
          templates=["suspension_corner", "beam_axle", "damper", "anti_roll_bar"]),
    Block(id="steering", name="Steering", functions=["steer"],
          templates=["steering_rack", "steering_column", "steering_wheel"]),
    Block(id="propulsion", name="Propulsion unit", functions=["propel"],
          templates=["engine", "transmission", "motor", "inverter", "reduction_gear",
                     "engine_mounts"]),
    Block(id="driveline", name="Driveline", functions=["propel"],
          templates=["half_shaft", "propshaft", "rear_differential"]),
    Block(id="traction_storage", name="Traction battery", functions=["energy"],
          templates=["traction_battery", "hv_cables", "charger"], applicability=ELECTRIFIED),
    Block(id="fuel_storage", name="Fuel storage", functions=["energy"],
          templates=["fuel_tank", "fuel"], applicability=ICE),
    Block(id="exhaust", name="Exhaust", functions=["propel"], templates=["exhaust"],
          applicability=ICE),
    Block(id="lv_power", name="12 V supply and harness", functions=["energy"],
          templates=["battery_12v", "harness"]),
    Block(id="cooling", name="Cooling", functions=["heat"],
          templates=["radiator", "battery_thermal"]),
    Block(id="hvac", name="HVAC", functions=["comfort", "heat"], templates=["hvac"]),
    Block(id="cabin", name="Seats and trim", functions=["comfort", "carry"],
          templates=["front_seat", "rear_seat_row", "door_trim", "headliner", "carpet",
                     "console"]),
    Block(id="restraints", name="Restraints", functions=["protect"], templates=["restraints"]),
    Block(id="hmi", name="Cockpit and displays", functions=["hmi"],
          templates=["instrument_panel", "display", "steering_wheel"]),
    Block(id="sensing", name="Environment sensing", functions=["sense"],
          templates=["adas_sensors"]),
]  # fmt: skip

FLOWS = [
    # braking chain
    Flow(id="pedal_force", kind="mechanical", source="driver", target="pedal",
         item="pedal force and travel", attributes={"force": "0-500 N", "travel": "≤ 120 mm"}),
    Flow(id="master_pressure", kind="fluid", source="pedal", target="modulator",
         item="master-cylinder pressure", attributes={"max": "160 bar", "medium": "DOT 4"}),
    Flow(id="wheel_speeds", kind="signal", source="wheel_speed", target="esc",
         item="wheel speeds", attributes={"rate": "100 Hz", "channels": "4"}),
    Flow(id="valve_commands", kind="signal", source="esc", target="modulator",
         item="valve and pump commands", attributes={"cycle": "≤ 10 ms"}),
    Flow(id="esc_power", kind="electrical_power", source="lv_power", target="esc",
         item="12 V supply", attributes={"voltage": "9-16 V", "peak": "40 A (pump)"}),
    Flow(id="caliper_pressure", kind="fluid", source="modulator", target="calipers",
         item="caliper pressure", attributes={"circuits": "2 (diagonal)", "max": "160 bar"}),
    Flow(id="clamp_force", kind="mechanical", source="calipers", target="discs",
         item="pad clamp force"),
    Flow(id="brake_torque", kind="mechanical", source="discs", target="wheels",
         item="brake torque"),
    Flow(id="braking_force", kind="mechanical", source="wheels", target="road",
         item="tyre braking force", attributes={"peak": "≈ 1 g on dry asphalt"}),
    Flow(id="brake_heat", kind="thermal", source="discs", target="air", item="braking heat"),
    # propulsion
    Flow(id="fuel_feed", kind="fluid", source="fuel_storage", target="propulsion",
         item="fuel", applicability=ICE),
    Flow(id="hv_power", kind="electrical_power", source="traction_storage",
         target="propulsion", item="high-voltage DC", applicability=ELECTRIFIED),
    Flow(id="drive_torque", kind="mechanical", source="propulsion", target="driveline",
         item="drive torque"),
    Flow(id="wheel_torque", kind="mechanical", source="driveline", target="wheels",
         item="wheel torque"),
    Flow(id="exhaust_gas", kind="fluid", source="propulsion", target="exhaust",
         item="exhaust gas", applicability=ICE),
    Flow(id="powertrain_heat", kind="thermal", source="propulsion", target="cooling",
         item="powertrain heat"),
    Flow(id="heat_rejection", kind="thermal", source="cooling", target="air",
         item="heat rejection"),
    # steering and ride
    Flow(id="steering_input", kind="mechanical", source="driver", target="steering",
         item="steering torque and angle"),
    Flow(id="steer_angle", kind="mechanical", source="steering", target="wheels",
         item="road-wheel steer angle"),
    Flow(id="road_loads", kind="mechanical", source="road", target="wheels",
         item="road loads"),
    Flow(id="wheel_loads", kind="mechanical", source="wheels", target="suspension",
         item="wheel loads"),
    Flow(id="body_loads", kind="mechanical", source="suspension", target="body",
         item="suspension loads at hardpoints"),
    # information
    Flow(id="sensor_data", kind="signal", source="sensing", target="esc",
         item="object list", attributes={"bus": "CAN FD"}),
    Flow(id="driver_info", kind="signal", source="esc", target="hmi",
         item="warnings and status"),
    Flow(id="cabin_air", kind="thermal", source="hvac", target="cabin", item="conditioned air"),
]  # fmt: skip

FAILURE_MODES = [
    FailureMode(id="pressure_loss", function="brake_pressure", block="modulator",
                mode="loss of hydraulic pressure (leak)", effect="braking lost on one circuit",
                severity=10, occurrence=2, detection=4,
                action="dual diagonal circuits; low-fluid warning"),
    FailureMode(id="pad_wear", function="friction", block="calipers", mode="pads worn out",
                effect="longer stopping distance, disc damage", severity=8, occurrence=4,
                detection=3, action="wear indicator and service interval"),
    FailureMode(id="wheel_speed_lost", function="wheel_slip", block="wheel_speed",
                mode="wheel speed signal lost", effect="ABS/ESC unavailable; base braking "
                "remains", severity=7, occurrence=3, detection=2,
                action="plausibility check and warning lamp"),
    FailureMode(id="disc_fade", function="brake_heat", block="discs",
                mode="disc overheating (fade)", effect="reduced braking on long descents",
                severity=8, occurrence=3, detection=5,
                action="disc thermal capacity check (planned analysis)"),
    FailureMode(id="assist_loss", function="steer", block="steering",
                mode="loss of power assist", effect="high steering effort",
                severity=8, occurrence=2, detection=2, action="manual steering retained"),
    FailureMode(id="thermal_runaway", function="energy", block="traction_storage",
                mode="cell thermal runaway", effect="fire risk", severity=10, occurrence=2,
                detection=5, action="cell monitoring, venting and isolation"),
    FailureMode(id="propulsion_loss", function="propel", block="propulsion",
                mode="loss of propulsion", effect="vehicle stops", severity=6, occurrence=3,
                detection=3),
]  # fmt: skip

ARCHITECTURE = Architecture(functions=FUNCTIONS, blocks=BLOCKS, flows=FLOWS,
                            failure_modes=FAILURE_MODES)  # fmt: skip


def architecture(values: Values) -> Architecture:
    return ARCHITECTURE
