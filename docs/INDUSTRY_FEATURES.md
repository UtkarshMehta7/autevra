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
| Sketch-based features (pads, pockets, revolves, fillets) authored by the user | partial | Part Design feature tree: extrude, revolve, loft, sweep, shell, fillet, mirror, patterns, add/cut/intersect; sketches are point lists, no interactive sketcher |
| Surface design: lofts, sweeps, fills, continuity control | partial | Smooth lofts for the glasshouse; no user-driven surfaces or G2 control |
| Class-A styling surfaces (highlight lines, zebra and curvature analysis) | partial | Zebra highlight-line display; no curvature combs or continuity checks yet |
| Knowledge-based engineering (rules, formulas, checks bound to the model) | **have** | Design rules, derived values, packaging checks with stated limits |
| Templates and catalogues of standard designs | **have** | Thirteen vehicle templates; twelve body styles; chassis, powertrain and trim choices |
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
| Body styles and packaging | **have** | Twelve sculpted body styles with shape controls, cabin packaging, headroom, seat-row rule |
| Chassis architectures | **have** | Ladder frame, unibody, skateboard |
| Suspension types (MacPherson, double wishbone, multi-link, twist beam) | **have** | Per axle, linkage geometry; ride models treat each as a vertical corner |
| Wheel and rim design | **have** | Six rim designs, six finishes; tyre size drives the ride models |
| Exterior options (roof, rails, spoilers, mirrors, towing) | **have** | Panoramic roof, sunroof, rails, crossbars, roof spoiler, boot lip, wing, mirrors or cameras, tow bar |
| Powertrain packaging (engine, transmission, e-motors, battery) | **have** | Envelopes per configuration; no detailed components |
| Electrical: harness routing, connectors, schematics | partial | Main harness trunk, HV cables, ECUs; no schematics or connector library |
| Thermal systems (cooling circuits) | partial | Cooling module envelope only |
| Interior: seats, instrument panel, trim levels | **have** | Representative envelopes, trims, colours, driving side |
| Ergonomics with human models (reach, vision, H-point) | partial | Seated-height allowance for headroom; no manikin, reach or vision study |
| Lighting design (signatures, photometry) | partial | Four head and three tail lamp signatures as flush envelopes; no photometry |

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

1. ✅ **Suspension types** with their own geometry (MacPherson strut, double wishbone, multi-link, twist beam, beam axle), selectable per axle, with unsprung-mass defaults.
2. ✅ **Wheel designs and lamp signatures**: spoke patterns and rim finishes; LED strip, matrix, round and split lamps; light bar or separate rear clusters.
3. **Body options and shaping controls**: ✅ panoramic roof, roof rails, rear spoiler, mirrors, tow bar; next: bonnet height, screen rake, tumblehome and sill tuck as parameters.
4. **Ergonomics**: a seated manikin from percentile dimensions, eye points, reach envelopes and vision checks.
5. **Electrical schematics and harness routing** by zone, with connectors and a bill of materials.
6. **Clearance matrix** between all equipment and body parts.
7. **Structural analysis** via an external solver (beam model of the frame first).
8. **Freeform surfaces and surface quality analysis** (zebra, curvature).
9. **PLM basics**: accounts, a parts list and bill of materials, release states.

## Where the flexibility of the established tools comes from

Research notes (October 2026) from public training outlines, user-community posts and
vendor material. Treat them as how the capabilities are generally described, not as a
feature-by-feature account of any product.

1. **A general feature modeller under every domain.** Users compose sketches, pads,
   pockets, revolves, sweeps, multi-section (lofted) surfaces, fills, blends, offsets and
   shells into any shape. Domain workbenches sit on that one model. This, not a catalogue
   of templates, is why the same tool designs a car body, a wing, a mouse or a die.
   Surfacing courses list multi-section surfaces with guides and spines, adaptive sweeps,
   laws, fills and healing as core topics
   ([TECHNIA GSD course](https://learning.technia.com/w/uk/courses/361-catiav5-surfacing-gsd-training/2403)).
2. **Several shape paradigms on one model.**
   - Subdivision "virtual clay" for finding a form fast: a control mesh is deformed locally
     or globally, and the result converts to exact surfaces
     ([3DEXPERIENCE community: Imagine & Shape](https://3dswym.3dexperience.3ds.com/wiki/catia-user-community/catia-imagine-shape-2-ima_QxNAfthmSVe2EA3V2_gz8A)).
   - Parametric NURBS for the engineered shape; designers report moving between the two
     ([concept modelling post](https://3dswym.3dexperience.3ds.com/post/catia-creative-design-styling-user-community/concept-modeling-with-subdiv-virtual-clay-modeling-for-design-creativity_1405)).
   - Class-A tools for the final reflective surfaces, with G2/G3 continuity
     ([Hawk Ridge Systems](https://hawkridgesys.com/blog/why-catia-surfacing-drives-precision-in-automotive-design)).
3. **Knowledge-based engineering.**
   - Parameters, formulas, rules and checks bound to the geometry.
   - Design tables that drive variants from a spreadsheet.
   - Reusable templates (power copies and user-defined features) with published inputs, so
     a proven feature is dropped into a new context and re-fitted
     ([power copies tutorial](https://www.staff.city.ac.uk/~ra600/ME2105/Catia%20course/CATIA%20Tutorials/wfsug_C2/wfsugat0201.htm),
     [KBE course outline](https://www.goengineer.com/training/catia-v5-knowledge-based-engineering)).
4. **Surface quality analysis.**
   - Connection checks (G0, G1, G2 between faces).
   - Curvature combs, porcupine analysis and highlight (zebra) lines
     ([GrabCAD tutorial](https://cad.grabcad.com/tutorials/how-make-class-a-surface-analysis-in-catia),
     [Alias help on curvature continuity](https://help.autodesk.com/cloudhelp/2014/ENU/Alias/files/GUID-9DD73E22-A5EF-4952-BB84-2CEE2109993C.htm)).
5. **Associativity.** A skeleton or master model drives the parts, so a change ripples
   through the assembly. Autevra already does this with declared dependencies and impact
   analysis.

## What Autevra takes from it

| Lesson | Autevra step | Status |
|---|---|---|
| One general shape engine for every domain | Plan-law sections lofted and trimmed by a profile; the automotive body is the first user. Measured: smooth multi-section B-spline lofts are too slow on the hosted tier, so they wait for the Part Design workbench | partial |
| Shape controls instead of fixed designs | Haunch, nose and tail width, sill tuck, roundness and tumblehome as parameters on every body style | **have** |
| A general feature modeller | Part Design workbench: user-authored feature tree (extrude, revolve, loft, sweep, shell, fillet, mirror, patterns) on OCCT, with per-part undo | **have** (v1) |
| Reusable templates with published inputs | Starting-point parts with parameters and formulas (a first form of power copies); instantiating a feature template into an existing part is next | partial |
| Design tables | Variant tables that drive parameters, exportable as CSV | planned |
| Surface quality analysis | Zebra (highlight-line) display mode; curvature next | partial |
| Subdivision form finding | Editable control sections, then a control mesh, converted to exact surfaces | planned |

## Domains beyond road vehicles (plan)

Autevra's core (parameters, commands, assemblies, rules, impact analysis, tests,
requirements) is domain-neutral, and domains plug in as modules like the automotive one.
On top of the shared shape engine and the Part Design workbench:

1. **Aerospace**
   - Fuselage from sections; wings and tail surfaces from NACA four-digit aerofoils (a
     published formula).
   - Engine nacelle and a simplified turbofan.
   - Landing gear linkage and control-surface hinges.
2. **Consumer products and organic shapes**: freeform lofts, sweeps and shells for handheld
   products, bottles, bellows and bicycle frames (tube sweeps along a path).
3. **Tooling**: mould cavities (a part subtracted from a block, with draft and parting
   plane), sheet-metal flanges and bends, and simple stamping dies.
4. **Plant and factory equipment**: piping routed along paths with standard bends,
   conveyors from repeated modules, and robot arms as kinematic chains.

Each domain will state its limits as the automotive module does: representative geometry,
no claim of certification, analysis only where a verified solver runs.
