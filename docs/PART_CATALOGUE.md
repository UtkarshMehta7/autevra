# Autevra part catalogue (target)

Status: **design, November 2026**. Companion to
[PLATFORM_ARCHITECTURE.md](PLATFORM_ARCHITECTURE.md). It lists every part each module must
be able to design, how each part is defined, and how it grows from a placeholder into a
released, manufacturable item. No parity with, or affiliation to, any other vendor is claimed.

## 1. Principles

1. **The whole product exists from day one.** Every part in a module's breakdown is present
   from the first minute of a project, at the lowest maturity (an envelope with mass and
   CG). Mass, balance, packaging and cost are therefore always complete, and parts mature
   independently. Nothing is "not modelled yet"; it is modelled at level 0.
2. **Parts are generators, not drawings.** Each part is a *part template*: a parametric
   generator with typed inputs, design rules, interfaces, a manufacturing process and the
   analyses that size it. A user part is an instance of a template, or a free Part Design
   document when no template fits.
3. **Domain-standard breakdowns.** Each module organises its parts by the breakdown its
   engineers already use: ATA chapters for aircraft, SFI/ESWBS groups for ships, a
   system/subsystem tree for road vehicles, and functional groups for engines and machines.
4. **Skeleton first, then parts.** The module's product model is the skeleton (hardpoints,
   axes, surfaces, zones). Parts read the skeleton through published interfaces, never
   another part's raw faces, so they rebuild robustly when the skeleton changes.
5. **Process-aware geometry.** A part knows how it is made (sheet metal, casting, forging,
   machining, moulding, composite lay-up, extrusion, welding, additive). The process
   decides the features it may use and the checks it must pass, like draft, bend radius,
   ply drop-off or minimum wall.
6. **Shared parts are shared once.** Fasteners, bearings, seals, gears, springs, tyres,
   cables, hoses and profiles are inventory standard parts used by every module. Engines and
   motors are Mechanical-module products installed everywhere.

## 2. Part maturity ladder

Every part instance carries a maturity level. Levels are gates with automatic checks, not
labels.

| Level | Name | What exists | Gate (checked automatically) |
|---|---|---|---|
| **L0** | Allocation | envelope (box or swept volume), mass and CG estimate, interfaces at their skeleton frames | in the breakdown; mass from a statistical or parametric estimate with its source |
| **L1** | Concept | parametric concept geometry from the template; main dimensions driven by the skeleton | no clash with neighbours at the stated clearance; mass within the L0 allocation band |
| **L2** | Engineered | sized by its analyses (loads, stress, stiffness, thermal, flow); material chosen | every sizing analysis passes with its margin; results stored with the version |
| **L3** | Manufacturable | process features (draft, bend reliefs, fillets, ply book, weld preps), tolerances and PMI, drawing | process checks pass; tolerance stack-ups at its interfaces close |
| **L4** | Released | immutable item version in the inventory, where-used tracked | review sign-off; regeneration from source reproduces the geometry hash |

The product's maturity is shown as a heat map over the breakdown, so reviews ask "what is
still L0?" instead of "what is missing?".

## 3. Part template contract

Every template, in every module, implements the same contract:

```
PartTemplate
├── id, module, breakdown code (e.g. ATA 57-10, SFI 1xx, LV body.closures.door)
├── inputs          typed parameters with units, limits and defaults
├── skeleton reads  the published skeleton entities it consumes (hardpoints, axes, zones)
├── interfaces      ports it offers and consumes (mount, shaft, flange, hardpoint, fluid, …)
├── process         sheet metal | casting | forging | machining | moulding | composite |
│                   extrusion | weldment | tube | additive | standard (bought)
├── rules           design rules (knowledge) checked continuously, each with its reference
├── generators      L0 envelope → L1 concept → L2 sized → L3 detailed geometry
├── analyses        the sizing and verification methods, with credibility and limits
├── estimators      mass, cost and CO2e models used before the geometry exists
└── outputs         geometry, mass properties, BOM line, drawing views, inventory item
```

Templates are code plus data. They are unit-tested against closed-form or published
reference cases, the same way the FEA and lifting-line kernels are tested today.

## 4. Shared standard parts (inventory, every module)

| Family | Members | Defined by | Checks |
|---|---|---|---|
| Threaded fasteners | bolts, screws, studs, nuts, washers, inserts, rivets, blind rivets | ISO metric and UNC/UNF series, length series | bolted-joint sizing (VDI 2230 method), thread engagement, clamp-length |
| Pins and keys | dowels, spring pins, clevis pins, parallel and Woodruff keys, splines | ISO series | shear and bearing stress |
| Rolling bearings | deep-groove, angular-contact, taper, cylindrical and needle roller, thrust | bore/OD/width series | ISO 281 basic rating life, speed limit |
| Plain bearings and bushes | sleeve, flanged, spherical plain | series | PV limit |
| Seals | O-rings, lip seals, gaskets, mechanical seals | ISO 3601 and similar sizes | groove fill and squeeze |
| Power transmission | spur, helical, bevel and worm gears; pulleys; belts; chains; sprockets; couplings | module/pitch, teeth, face width | ISO 6336-style bending and contact stress (simplified), ratios |
| Springs | compression, extension, torsion, disc, gas | wire/coil geometry | rate, stress, buckling |
| Profiles | I, H, C, angle, tube, box, extrusions | standard sections | section properties for beam analyses |
| Fluid | pipes, tubes, hoses, fittings, valves, clamps | DN/OD series, pressure class | pressure rating |
| Electrical | connectors, terminals, wires, cable ties, grommets, fuses, relays | gauge and current rating | current, voltage drop |
| Wheels and tyres | tyres, rims, valves | ETRTO size codes | load index, speed rating |
| Raw stock | sheet, plate, bar, billet, honeycomb, prepreg | gauge and grade | material availability |

## 5. Land vehicles module

Breakdown: **vehicle → system → subsystem → part**. The skeleton is the vehicle package
(hard points, axle lines, H-points, wheel envelopes, styling surfaces, sections).
"Today" marks parts the module already generates (mostly at L1).

| System | Subsystems and parts | Process | Sizing analyses |
|---|---|---|---|
| **Body-in-white** | side frame (A/B/C/D pillars, roof rail, sill), floor (front, centre, rear), tunnel, front structure (rails, crush cans, shotgun, shock towers, dash panel, cowl), rear structure (rails, rear panel, wheelhouses), roof panel and bows, crossmembers, bumper beams, subframes (front, rear), cradles | sheet metal (stamped), extrusion, casting (mega-casting option), spot/laser welds, adhesive | torsional and bending stiffness, crash load paths (energy and section force estimates), modal frequencies, weld-spot pitch. *Today: unibody/frame with sills, pillars, rails* |
| **Closures** | doors (outer, inner, intrusion beam, hinges, check strap, latch, window regulator), bonnet, tailgate or boot lid, fuel/charge flap, convertible roof (soft-top linkage or folding hard-top) | sheet metal, hem flange, moulding | hinge-axis kinematics, swing envelope, sag and dent resistance, sealing gap and flush. *Today: closures in the body shell, opening roof* |
| **Exterior** | bumpers and fascias, grilles, wings/fenders, mirrors, sills covers, spoilers and diffusers, badges (user-supplied only), seals, wipers | injection moulding, paint | draft, wall thickness, aero (drag and lift contributions). *Today: styled body, mirrors, grille* |
| **Glazing** | windscreen, side glass (drop glass, fixed), backlight, sunroof | glass forming | curvature limits, vision obscuration, wiper sweep. *Today: glasshouse* |
| **Lighting** | headlamps, tail lamps, DRL, indicators, fog, CHMSL | moulding, optics | photometric zones (simplified), placement rules. *Today: lamp graphics* |
| **Suspension** | knuckles, control arms (upper, lower, trailing), links, springs, dampers, anti-roll bars and drop links, bushes, ball joints, top mounts, subframe mounts | forging, casting, stamping, tube | hardpoint kinematics (camber, toe, roll centre, motion ratio), ride frequency, bushing loads, arm buckling. *Today: double wishbone/strut geometry, dampers, ride model* |
| **Steering** | rack and pinion, column, intermediate shaft, wheel, tie rods, EPS unit | machining, standard | Ackermann, turning circle, steering ratio, column collapse stroke |
| **Brakes** | discs, calipers, pads, master cylinder, booster/brake-by-wire, lines, ABS/ESC unit, parking brake | casting, machining | brake balance, thermal capacity per stop, pedal ratio, fade. *Today: discs, calipers* |
| **Wheels and tyres** | rims (multi-spoke, ten-twin, …), tyres, hubs, wheel bearings, studs/nuts, TPMS | casting/forging, inventory | rim load, offset/ET, tyre load index. *Today: rims, tyres, hubs* |
| **Powertrain (installed)** | engine or motor (from the Mechanical module), mounts, transmission, clutch/torque converter, inverter, reduction gear | inventory | mount loads, NVH isolation frequency, packaging. *Today: powertrain envelope* |
| **Driveline** | driveshafts (half-shafts, propshaft), CV and universal joints, differentials, transfer case, hubs | forging, tube | torsional strength, CV angle range, critical speed |
| **Energy storage** | fuel tank, filler pipe, HV battery (cells, modules, pack enclosure, crash frame, cooling plates), 12 V battery | moulding, sheet metal, extrusion | capacity, range, pack mass, crush protection, cell thermal |
| **Thermal** | radiator, condenser, fans, pumps, hoses, coolant reservoir, intercooler, battery chiller | inventory, tube routing | heat rejection, airflow, pressure drop |
| **Exhaust (ICE)** | manifold (engine), catalytic converter, flex, silencers, tailpipes, hangers | tube bending, sheet | back pressure estimate, hanger loads, clearance to floor |
| **Electrical and electronics** | harness (routes, bundles, branches, connectors), ECUs, fuse boxes, sensors (ADAS radar, camera, lidar, ultrasonic), antennas, chargers and ports | harness routing | bundle diameter, bend radius, current and voltage drop, sensor field of view |
| **Interior** | seats (frame, foam, trim, recliner, tracks), instrument panel (carrier, cross-car beam, skins), console, door trims, headliner, pillar trims, carpet, steering wheel, displays, pedal box, HVAC unit and ducts, restraints (belts, airbags, pretensioners) | moulding, tube, foam, sewing | H-point and seat travel, reach and vision (obscuration, mirror fields), knee clearance, airbag deployment zones. *Today: seats, dash, wheel, console, screens* |

Families: car body styles (today), then motorcycles (frame, swingarm, fork, tank),
trucks and buses (ladder frame, cab, axles, body), trailers. Each adds templates, never
mixes with another family's product model.

## 6. Aircraft module

Breakdown: **ATA iSpec 2200 chapters** (the numbering aircraft engineers use). The skeleton is
the aircraft geometry: reference wing, fuselage stations (FS), buttock (BL) and waterlines
(WL), wing stations, hinge lines, and engine and gear hardpoints.

| ATA | System | Parts | Process | Sizing analyses |
|---|---|---|---|---|
| 53 | **Fuselage** | frames (station), bulkheads (pressure, firewall), stringers, skins, longerons, floor beams and panels, keel beam, doors and surrounds, windows, cockpit canopy, tail cone, fairings | sheet metal, machined, composite | shear flow and bending (idealised section), pressure hoop stress, frame spacing vs. panel buckling, crash ditching loads |
| 57 | **Wings** | front and rear spars, ribs (nose, main, trailing), skins, stringers, leading edge, wing tip, fuel bays, attachment fittings, carry-through | machined, sheet, composite | lift distribution (lifting line, *today*), spar bending and shear, skin buckling, torsion box stiffness, flutter estimate |
| 55 | **Stabilisers** | horizontal and vertical tails: spars, ribs, skins, fittings | as wings | tail volume and stability (*today*), loads |
| 27 | **Flight controls** | ailerons, elevators, rudder, flaps, slats, spoilers, tabs; hinges, horns, pushrods, cables, pulleys, bellcranks, stick and pedals, actuators | machined, sheet, cable | hinge moments, control-circuit stiffness and friction, mass balance, deflection envelopes |
| 32 | **Landing gear** | main and nose legs (spring steel, oleo), trunnions, axles, wheels, tyres, brakes, retraction actuators, doors | forging, machining | tip-back and turnover angles, ground clearance, oleo stroke and energy absorption, leg loads |
| 28 | **Fuel** | tanks (integral, bladder), vents, pumps, lines, selectors, gauging | composite, tube | capacity vs. range (Breguet, *today*), CG shift with fuel burn |
| 29 / 36 | **Hydraulic and pneumatic** | reservoirs, pumps, actuators, lines | tube | flow, pressure drop |
| 24 | **Electrical** | generator/alternator, battery, buses, harness, circuit breakers | harness | load analysis |
| 21 / 30 | **Environmental and ice protection** | ducts, heat exchangers, de-ice boots | tube | heat balance |
| 22 / 31 / 34 | **Avionics** | displays, autopilot servos, antennas, pitot-static, sensors | inventory | placement, field of view |
| 25 | **Cabin and equipment** | seats, harnesses, floor, linings, baggage | moulding | 9 g / 16 g seat load cases (simplified) |
| 54 / 71 | **Nacelles and engine mounts** | cowlings, mount truss, firewall, engine attach | tube weldment, composite | mount loads, vibration isolation |
| 61 | **Propellers** | blades, hub, spinner, governor | machined, composite | blade-element momentum, efficiency vs. advance ratio, tip Mach |
| 72–80 | **Powerplant (installed)** | piston, turboprop, turbofan or electric motor from the Mechanical module | inventory | power lapse with altitude (*today*), installed thrust |

Families: fixed-wing light and trainer (today), UAVs, gliders, then rotorcraft (rotor
blades, hub, swashplate, gearbox, tail rotor) and eVTOL (lift rotors, booms, battery bays).

## 7. Marine module

Breakdown: **SFI/ESWBS-style groups** (100 hull structure, 200 propulsion, 300 electric,
400 command and navigation, 500 auxiliary, 600 outfit). The skeleton is the hull form with
frame stations, decks, bulkhead positions and the shaft line.

| Group | System | Parts | Process | Sizing analyses |
|---|---|---|---|---|
| 100 | **Hull structure** | shell plating (bottom, side, bilge, transom), keel and keelson, frames (transverse), longitudinals and stiffeners, floors, girders, bulkheads (watertight, collision), decks and deck beams, superstructure, engine bed foundations, chines, stem and stern frames | welded plate, aluminium, FRP lay-up | scantlings (rule-based plate thickness and section modulus), longitudinal strength (still-water and wave bending), hydrostatic pressure on panels |
| 200 | **Propulsion** | engines (Mechanical module), gearbox, shaft line (shafts, couplings, bearings, stern tube, seals), propeller (blades, hub), waterjet, pods and outboards | inventory, machining, casting | propeller sizing (Bp-δ or B-series charts), shaft diameter (torsion and whirl), alignment |
| 300 | **Electric plant** | generators, switchboards, batteries, cable trays, shore power | inventory | load balance |
| 400 | **Navigation and command** | helm, consoles, mast, radar, antennas, lights | moulding, tube | visibility arcs, light placement |
| 500 | **Auxiliary systems** | fuel, fresh water, bilge, ballast, fire, HVAC, steering gear; tanks and piping | piping routing | tank capacities and free surface, pump heads |
| 500 | **Manoeuvring** | rudders and stocks, thrusters, fins and stabilisers, keels (ballast keel, centreboard) | casting, composite | rudder force and torque, keel righting moment |
| 600 | **Outfit and furnishing** | hatches, doors, windows and portlights, railings, cleats and bollards, anchors and chain, ladders, seating, cabins | standard, sheet | anchor and mooring loads |

Hull-level analyses (module, not part): hydrostatics and Bonjean curves, GZ righting-arm
curve and stability criteria, Holtrop–Mennen resistance, powering, seakeeping (strip
theory, later).

Families: displacement monohulls, planing craft (Savitsky method), catamarans, sailing
yachts (sail plan, rig: mast, boom, standing rigging).

## 8. Mechanical module: engines, category by category

Each engine category is a product with its own template set. Parts below are generated
from the engine's own parameters (bore, stroke, cylinders, layout, …), so an engine
designed at L0 has every part allocated with mass from the start.

### 8.1 Piston engines (spark and compression ignition)

| Group | Parts | Process | Sizing |
|---|---|---|---|
| **Structure** | cylinder block (deck, bores, water jacket, main bearing bulkheads), bedplate or main caps, cylinder liners, cylinder head (ports, combustion chamber, valve seats and guides), head gasket, oil sump, front cover, rear seal carrier | casting, machining | bore spacing, bulkhead load from peak firing pressure, head bolt clamp |
| **Cranktrain** | crankshaft (journals, pins, webs, counterweights), connecting rods (small end, shank, big end, cap, bolts), pistons (crown, ring lands, skirt, pin bosses), piston rings, gudgeon pins, main and big-end bearings, flywheel or flexplate, torsional damper, balance shafts | forging, casting, machining | slider-crank kinematics and gas plus inertia forces, rod buckling, crank fillet stress (simplified), bearing loads and oil-film estimate, primary and secondary balance, firing order |
| **Valvetrain** | camshafts (lobes from a lift profile), valves (intake, exhaust), springs, retainers, collets, followers, rocker arms, lash adjusters, cam phasers | forging, machining, spring | lift, velocity and acceleration of the cam profile, spring force vs. valve-float speed, valve area vs. bore |
| **Timing drive** | chain or belt, sprockets/pulleys, tensioners, guides | standard | drive ratio, tension |
| **Induction** | intake manifold (runners, plenum), throttle body, air filter box, turbocharger or supercharger, intercooler, wastegate | moulding, casting | runner tuning length, boost and compressor-map matching |
| **Exhaust** | exhaust manifold or header, turbine housing, heat shields | casting, tube | back pressure, thermal expansion |
| **Fuel and ignition** | injectors, fuel rail, high-pressure pump, spark plugs, coils, glow plugs | standard | injector flow vs. power |
| **Lubrication** | oil pump, pickup, filter, cooler, galleries, jets | casting, machining | flow and pressure |
| **Cooling** | water pump, thermostat housing, jackets, hoses | casting | heat rejection share |
| **Accessories and mounts** | alternator, starter, A/C compressor, accessory belt, engine mounts and brackets | standard, casting | belt wrap, mount loads |

Rotary (Wankel): housing (trochoid from generating radius and eccentricity), side
housings, rotor, apex and side seals, eccentric shaft, stationary gear.

### 8.2 Electric machines

| Group | Parts | Sizing |
|---|---|---|
| Stator | laminations (slot geometry), windings (hairpin, distributed, concentrated), end windings, slot liners | slot fill, current density, copper loss |
| Rotor | laminations, magnets (surface or interior V/flux barrier) or cage bars and end rings, shaft, balance rings | torque constant, magnet retention at max speed, rotor burst margin |
| Structure | housing, end shields, cooling jacket or oil spray, bearings, resolver/encoder, terminal box | thermal network estimate, bearing life |
| Power electronics | inverter (modules, DC-link capacitor, busbars, cooling plate, gate driver) | losses and efficiency map |

### 8.3 Gas turbines

| Group | Parts | Sizing |
|---|---|---|
| Intake and fan | inlet, spinner, fan blades and disc, OGVs | mass flow, tip speed |
| Compressor | rotor discs and blades per stage, stator vanes, casings, bleed valves, variable vanes | stage loading and pressure ratio (velocity triangles), disc burst margin (FEA, *today*) |
| Combustor | liner, dome, swirlers, fuel nozzles, igniters, casing | residence time, pressure loss |
| Turbine | NGVs, blades (cooled), discs, seals, casings | stage work, creep and blade-root stress |
| Exhaust | nozzle, mixer, thrust reverser | thrust and SFC (Brayton cycle) |
| Shafts and bearings | spools, bearings, seals, accessory gearbox | critical speeds, bearing loads |

### 8.4 Rocket engines

Thrust chamber (injector plate, chamber, throat, regenerative cooling channels), nozzle
(bell contour by the Rao method), turbopump (pump impeller, turbine, shaft), gas generator,
valves, gimbal mount; solid motor case, grain geometry and nozzle. Sizing: ideal rocket
equations, Isp, chamber pressure vs. mass.

## 9. Mechanical module: machinery

| Family | Parts | Sizing |
|---|---|---|
| Gearboxes | gears (involute, generated from module and teeth), shafts, bearings, housing (split, cast), seals, breathers, oil level | ratio and torque per stage, gear stress, shaft deflection and critical speed, bearing life |
| Mechanisms and linkages | links, joints, cams and followers, Geneva drives, slider-cranks | kinematics and dynamics (multibody), Grashof condition |
| Robot arms | base, links, joints (motor + reducer from the inventory), end effector flange | reach envelope, joint torques, deflection |
| Frames and structures | weldments from profiles, gussets, base plates, anchor bolts | beam/frame FEA, weld throat sizing |
| Pressure equipment | vessels (shell, heads, nozzles, flanges, supports) | wall thickness by the boiler and pressure-vessel code method (simplified) |
| Conveyors and handling | frames, rollers, belts, drives, idlers | belt tension, drive power |
| Tooling | mould halves, cores and cavities, ejector layout, dies, jigs and fixtures | draft and parting line, shrinkage, clamp force |

## 10. Space module (later)

Launcher stages (tanks with domes and skirts, interstages, thrust structure, fairing),
spacecraft bus (panels, honeycomb sandwich, deployables), mechanisms. Sizing: tank wall
thickness and buckling, rocket equation, mass budget.

## 11. How many templates

| Module | First release (L1 generators) | Full catalogue |
|---|---|---|
| Shared standard parts | ~40 families | ~120 families |
| Land vehicles | ~60 (today 41 generators, 57 component instances) | ~250 |
| Aircraft | ~40 | ~180 |
| Marine | ~35 | ~150 |
| Mechanical: engines | ~45 (piston) | ~200 across categories |
| Mechanical: machinery | ~30 | ~120 |

The template SDK (section 3) and the maturity ladder (section 2) are what make these
numbers possible: each new template is a small generator plus tests, and every product is
complete at L0 before the first template is detailed.
