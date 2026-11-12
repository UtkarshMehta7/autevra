"""Starting specifications for the Aircraft workspace.

The transport preset uses the published external dimensions, masses and thrust of the
Boeing 777-300ER (span 64.8 m, length 73.9 m, fuselage 6.2 m, reference wing area
436.8 m2, 351 534 kg maximum take-off mass, 145 538 kg of fuel, two engines of 513 kN,
Mach 0.84 at 35 000 ft). The wing is the trapezoid with that span and area (the real
planform has an inboard trailing-edge extension), tail positions and the centre of gravity
are estimates, and the engine consumption is a typical cruise value for its class.
"""

from autevra.aero.aircraft import AircraftSpec

PRESETS: dict[str, AircraftSpec] = {
    "Light aircraft (piston single)": AircraftSpec(),
    "Boeing 777-300ER (twin-jet transport)": AircraftSpec(
        name="Boeing 777-300ER study",
        propulsion="turbofan",
        engines=2,
        thrust_kn=513.0,
        bypass_ratio=9.0,
        tsfc=15.6,
        nacelle_diameter=3.9,
        nacelle_length=7.3,
        engine_span_fraction=0.31,
        wing_span=64.8,
        wing_root_chord=11.73,
        wing_tip_chord=1.75,
        wing_sweep=34.5,
        wing_dihedral=6.0,
        wing_twist=-3.0,
        wing_naca="2411",
        wing_x=24.5,
        high_wing=False,
        cl_max_section=1.6,
        fuselage_length=73.9,
        fuselage_width=6.2,
        fuselage_height=6.2,
        htail_span=21.5,
        htail_root_chord=7.0,
        htail_tip_chord=2.4,
        htail_x=64.5,
        fin_height=9.2,
        fin_root_chord=8.2,
        fin_tip_chord=3.3,
        fin_sweep=46.0,
        fin_x=62.0,
        mtow=351_534.0,
        fuel_mass=145_538.0,
        x_cg=36.0,
        fixed_gear=False,
        tricycle=True,
        cruise_speed=249.2,
        cruise_altitude=10_668.0,
    ),  # fmt: skip
}
