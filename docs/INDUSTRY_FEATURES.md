# Industry feature survey and upgrade plan

What the established vehicle-engineering tools offer, by capability family, and where
Autevra stands. The tools are named as examples of a category (Dassault Systèmes CATIA,
Siemens NX, PTC Creo, Dassault Systèmes SolidWorks, Autodesk Alias and VRED, ICEM Surf,
Siemens Capital and Zuken E3 for electrical, RAMSIS and Siemens Jack for ergonomics, MSC
Adams and CarSim for vehicle dynamics, Abaqus, Ansys and Nastran for structures, Simcenter
STAR-CCM+ and Ansys Fluent for flow, Teamcenter and ENOVIA for data management). The
descriptions are of capability families as generally documented, not feature-by-feature
claims about any product or version. Autevra is not affiliated with, and does not claim
parity with, any of them.

Status: **have** (implemented and tested), **partial** (a working subset), **planned**.

## 1. Geometry and design

| Capability (typical in the category) | Autevra | Notes |
|---|---|---|
| Parametric solid modelling (features, history, parameters) | **have** | Parameters drive B-rep builders (CadQuery / Open CASCADE); typed commands with undo and redo |
| Sketch-based features (pads, pockets, revolves, fillets) authored by the user | planned | Builders are authored in code; no interactive sketcher |
| Surface design: lofts, sweeps, fills, continuity control | partial | Smooth lofts for the glasshouse; no user-driven surfaces or G2 control |
| Class-A styling surfaces (highlight lines, zebra and curvature analysis) | planned | Needs freeform surfaces first |
| Knowledge-based engineering (rules, formulas, checks bound to the model) | **have** | Design rules, derived values, packaging checks with stated limits |
| Templates and catalogues of standard designs | **have** | Eight vehicle templates; body styles; chassis, powertrain and trim choices |
| Design tables and variants | partial | Choice parameters and templates; no tabular configuration manager |
| Sheet metal, composites, castings | planned | |
| 2D drawings with dimensions and GD&T | planned | |
| Neutral exchange (STEP, IGES, JT) | partial | STEP AP214 export with names and colours; no import workflow or JT |

## 2. Assembly and digital mock-up

| Capability | Autevra | Notes |
|---|---|---|
| Assemblies with constraints and interfaces | **have** | Mates on named interfaces, coincidences, load paths, integration checks |
| Change impact (what rebuilds and moves) | **have** | Declared dependencies per component; impact preview before applying |
| Clearance and interference checks | partial | Exact OCCT distances for listed pairs; not every pair |
| Section views, measurement, hide and isolate | **have** | Section plane X/Y/Z, point-to-point measure, isolate (not capped) |
| Display modes and standard views | **have** | Shaded, edges, wireframe; iso and six orthographic views; perspective or ortho |
| Kinematics (mechanism motion, suspension travel envelopes) | partial | Solver output played back (quarter car, half car); no mechanism solver |
| Large-assembly performance (lightweight representations) | partial | Cached geometry, de-duplicated meshes, gzip; no LOD |

## 3. Vehicle systems

| Capability | Autevra | Notes |
|---|---|---|
| Body styles and packaging | **have** | Seven body styles, cabin packaging, headroom, seat-row rule |
| Chassis architectures | **have** | Ladder frame, unibody, skateboard |
| Suspension types (MacPherson, double wishbone, multi-link, twist beam) | planned | Beam axles with coil-over dampers today |
| Powertrain packaging (engine, transmission, e-motors, battery) | **have** | Envelopes per configuration; no detailed components |
| Electrical: harness routing, connectors, schematics | partial | Main harness trunk, HV cables, ECUs; no schematics or connector library |
| Thermal systems (cooling circuits) | partial | Cooling module envelope only |
| Interior: seats, instrument panel, trim levels | **have** | Representative envelopes, trims, colours, driving side |
| Ergonomics with human models (reach, vision, H-point) | partial | Seated-height allowance for headroom; no manikin, reach or vision study |
| Lighting design (signatures, photometry) | partial | LED strip and light bar envelopes; no photometry |

## 4. Simulation and analysis

| Capability | Autevra | Notes |
|---|---|---|
| Ride and handling (multibody vehicle dynamics) | partial | Quarter car and half car, verified; no roll, handling or full multibody |
| Longitudinal performance (acceleration, braking) | **have** | Traction, load transfer, drag, rolling resistance |
| Structural FEA (stiffness, strength, modes) | planned | GPL solvers would run as separate executables |
| CFD (drag, cooling, HVAC) | planned | Drag coefficient is a typical per-class value today |
| Crash and occupant safety | planned | |
| Energy and range | partial | Steady-speed estimate with stated assumptions |
| Design of experiments and optimisation | **have** | Latin hypercube plus compass search, Pareto sets |
| Verification evidence (credibility labels, convergence) | **have** | Every run records solver, inputs, numerics and credibility |

## 5. Data, process and collaboration

| Capability | Autevra | Notes |
|---|---|---|
| Requirements linked to design and tests (traceability) | **have** | Requirements, trace matrix, ReqIF 1.2 import and export |
| Revisions and history | **have** | Command history, run revisions, staleness |
| PLM: parts, BOM, workflows, access control | planned | Per-browser workspaces only; no accounts or BOM |
| Multi-user collaboration and review | planned | |
| Scripting and automation API | **have** | REST API, plugin API with entry points |
| Visualisation and rendering (materials, environments) | partial | Physically based materials, studio environment; no ray tracing |

## Upgrade plan (from the gaps, in order of value)

1. **Suspension types** with their own geometry (MacPherson strut, double wishbone, multi-link, twist beam, beam axle), selectable per axle, with unsprung-mass defaults.
2. **Wheel designs and lamp signatures**: spoke patterns and rim finishes; LED strip, matrix, round and split lamps; light bar or separate rear clusters.
3. **Body options and shaping controls**: panoramic roof, roof rails, rear spoiler, mirrors, tow bar; bonnet height, screen rake, tumblehome and sill tuck as parameters.
4. **Ergonomics**: a seated manikin from percentile dimensions, eye points, reach envelopes and vision checks.
5. **Electrical schematics and harness routing** by zone, with connectors and a bill of materials.
6. **Clearance matrix** between all equipment and body parts.
7. **Structural analysis** via an external solver (beam model of the frame first).
8. **Freeform surfaces and surface quality analysis** (zebra, curvature).
9. **PLM basics**: accounts, a parts list and bill of materials, release states.
