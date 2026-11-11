# Autevra platform architecture (target)

Status: **design, November 2026**. This is the architecture the platform grows into; each
milestone below states what exists today and what it adds. [ARCHITECTURE.md](ARCHITECTURE.md)
describes the code as built; this file is the plan it follows.
[PART_CATALOGUE.md](PART_CATALOGUE.md) lists every part each module designs. The
established CAD suites (CATIA and its peers) are used as a reference for the *breadth* of
capability an engineering platform needs; no parity with, or affiliation to, any vendor is
claimed.

## 1. What we are building

One engineering platform where **every product is a module** (land vehicles, aircraft,
marine, engines and machinery, …), **every product is a complete breakdown of parts from
the first minute**, **every module draws on one shared inventory of engineered items**, and
**every number is computed in the open** from the design's own parameters.

The design brief, as an engineer would state it:

1. A module must be complete for its domain: its own product model, part breakdown,
   rules, analyses, workspaces and vocabulary. Modules never mix in one project or view.
2. Every part the product needs exists from day one, as an allocation (envelope, mass,
   CG, interfaces) that matures through concept, engineered, manufacturable and released
   levels. Mass, balance, cost and packaging are always complete.
3. Parts are generators, not drawings: part templates with inputs, rules, interfaces, a
   manufacturing process and the analyses that size them.
4. Anything engineered once is reusable everywhere: an engine designed in the Mechanical
   module is an inventory item a car, an aircraft or a boat can install, with its
   interfaces, mass properties and performance travelling with it.
5. The source of truth is intent, not geometry: parameters, features and command history
   regenerate the geometry, so every design is editable, diff-able and reproducible.
6. Engineering is continuous, not a separate phase: each change re-runs exactly the
   analyses it affects and shows the equations, inputs and convergence behind every result.

## 2. Platform map

```
┌───────────────────────────────── Studio (browser) ─────────────────────────────────┐
│ Module switcher: Land vehicles │ Aircraft │ Marine │ Mechanical │ …                 │
│ Breakdown tree (maturity heat map) │ Module workspaces │ Shared workbenches (scoped)│
│ Inventory browser (search, filter by interface, drag into the design)              │
└──────────────┬─────────────────────────────────────────────────────┬───────────────┘
               │ HTTP / events                                       │
┌──────────────▼──────────────────── Platform services ──────────────▼───────────────┐
│ Projects & products │ Breakdown & maturity │ Part templates │ Inventory & versions  │
│ Interfaces & mating │ Budgets (mass, cost) │ Materials & processes │ Standards       │
│ Commands & history  │ Requirements & trace │ Impact graph   │ Jobs │ AI tools        │
└──────┬───────────────────────┬──────────────────────────┬──────────────────────────┘
┌──────▼───────┐  ┌────────────▼────────────┐  ┌──────────▼──────────────────────────┐
│ Modules      │  │ Shared workbenches      │  │ Engineering kernels                 │
│ land, air,   │  │ (section 5): Sketcher,  │  │ Geometry: OCCT B-rep, NURBS,        │
│ marine,      │  │ Part, Shape, Sheet      │  │  continuity, unfolding, routing     │
│ mechanical,  │  │ metal, Weldment,        │  │ Solvers: FEA, SIMP, sketch GN,      │
│ space, …     │  │ Composites, Assembly,   │  │  lifting line, cycles, multibody,   │
│              │  │ Routing, Tolerancing,   │  │  hydrostatics, laminate theory      │
│              │  │ Drafting, Structures, … │  │ Units, parameters, rules            │
└──────────────┘  └─────────────────────────┘  └─────────────────────────────────────┘
                         Storage: projects, items, versions, files
```

Three kinds of building block, with strict rules between them:

| Block | Owns | May depend on | Examples |
|---|---|---|---|
| **Kernel** | mathematics and geometry, no product knowledge | nothing above it | `cad`, `geometry`, `fea`, `aero.lifting_line`, `part` |
| **Workbench** | a domain-neutral way of working on parts | kernels, services | Part Design, Shape, Sheet metal, Structures, Drafting |
| **Module** | a product domain: product model, breakdown, part templates, rules, analyses, workspaces, language | kernels, workbenches, services, the inventory | Land vehicles, Aircraft, Mechanical |

A module never imports another module. Modules meet **only through the inventory and
typed interfaces** (section 6), which keeps them separate yet able to share work.

## 3. Modules

Each module is a package (`autevra.modules.<id>`) registering one `ModuleDef`:

- **product model**: the parametric product (a vehicle, an aircraft, a hull, an engine)
  as parameters, derived values and rules. It owns the **skeleton**: the published
  hardpoints, axes, reference surfaces, stations and zones that parts read;
- **breakdown**: the product's part tree in the domain's own standard (section 4);
- **part templates**: the generators for every part in the breakdown;
- **workspaces**: its own studio tabs, plus the shared workbenches it enables;
- **analyses**: product-level tests and solvers with stated credibility and limits;
- **interfaces it offers and consumes** (e.g. a vehicle consumes a `powertrain.mount`);
- **language**: the vocabulary its command parser and AI tools understand;
- **templates**: starting points (a hatchback, a trainer aircraft, a planing hull).

Registries (parameters, rules, tests, builders, templates) are keyed by module, so a
project only ever sees its own module's definitions. Today they are process-wide; keying
them is milestone M1.

### 3.1 Module catalogue

| Module | Product families | Breakdown standard | First analyses | Status |
|---|---|---|---|---|
| **Land vehicles** | cars (all body styles), SUVs, pickups; then motorcycles, trucks, buses, trailers | system → subsystem → part | packaging, ride and pitch, longitudinal performance, clearances | available |
| **Aircraft** | fixed-wing (light, trainer, UAV, glider); then rotorcraft, eVTOL | ATA chapters | lifting line, drag build-up, stability, Breguet performance | experimental |
| **Mechanical: engines** | piston SI/CI, rotary, electric, gas turbine, rocket | functional groups | cycles, torque and power, balance, mass | planned (next) |
| **Mechanical: machinery** | gearboxes, mechanisms, robot arms, frames, pressure equipment, conveyors, tooling | functional groups | kinematics, gear and shaft sizing, bearing life | planned |
| **Marine** | displacement and planing hulls, catamarans, sailing yachts | SFI/ESWBS groups | hydrostatics, GZ stability, Holtrop resistance, powering | planned |
| **Space** | launchers and spacecraft structures | stage → subsystem | mass and delta-v budgets, tank sizing | later |

### 3.2 Engines, category by category

Engines are designed in the Mechanical module as **products in their own right** and
published to the inventory, from where vehicles, aircraft and boats install them.

| Category | Variants | Parametric definition | Analyses (open methods) | Outputs to the inventory |
|---|---|---|---|---|
| **Piston, spark ignition** | inline, V, boxer, W; 1–16 cylinders | bore, stroke, cylinders, layout, bank angle, compression ratio, rpm limits | displacement, Otto cycle with real-gas correction, BMEP-based torque and power curves, firing order, primary/secondary balance, mass estimate | envelope, mounts, crank axis, flywheel interface, torque curve, fuel map, mass and CG |
| **Piston, compression ignition** | inline, V; automotive to marine | as above, plus injection and boost | Diesel / dual cycle, turbo-matching estimate | as above |
| **Rotary (Wankel)** | 1–4 rotors | generating radius, eccentricity, width | chamber volume, cycle | as above |
| **Electric machines** | PMSM, induction, axial flux | stack length, diameter, poles, winding, cooling | torque constant, efficiency map, continuous vs. peak, thermal estimate | shaft interface, power and efficiency maps, voltage class |
| **Gas turbines** | turbojet, turbofan, turboprop, turboshaft | pressure ratios, bypass ratio, turbine entry temperature, spool layout | Brayton cycle with component efficiencies, thrust and SFC, station table | thrust or shaft-power maps, envelope, mounts |
| **Rocket engines** | liquid, solid | chamber pressure, expansion ratio, propellants | ideal nozzle flow, Isp, thrust | thrust, Isp, mass |

Every engine is a full part breakdown (block, crank, rods, pistons, head, valvetrain, …
for piston engines; stator, rotor, housing, inverter for motors; see the catalogue,
section 8). Engines share a common **engine interface**, so a consumer does not care which
category it installs: mount points, output shaft (axis, spline/flange, speed range),
envelope, mass properties, and a performance map.

## 4. Parts: breakdown, templates and maturity

This is the core of "design every part". Full lists are in
[PART_CATALOGUE.md](PART_CATALOGUE.md); the mechanism is here.

### 4.1 Breakdown

Each product is a tree: product → system → subsystem → part (→ feature). Nodes carry a
**breakdown code** in the domain's own standard (ATA 57-10 wing spar, SFI 1xx hull
structure, `body.closures.door.inner`). The tree is generated by the module's product
model from its parameters: a four-door saloon has four door assemblies, a 6-cylinder
engine six connecting rods, a 40-frame fuselage forty frames. Changing the parameter
adds or removes parts, each with its allocation.

### 4.2 Part templates

A part template is a generator with a fixed contract (catalogue, section 3): inputs,
**skeleton reads**, interfaces, manufacturing process, rules, generators per maturity
level, analyses, estimators (mass, cost, CO2e) and outputs. Today's Part Design feature
templates ("power copies"), design tables and presets are the seed of this: a template is
a power copy promoted to a module-aware, tested, process-aware generator.

Robust references, by design: a part reads only **published skeleton entities and
interface frames**, which have stable names, never raw faces or edges of another part.
This avoids the topological-naming failures that break feature trees in history-based
CAD when upstream geometry changes.

### 4.3 Maturity ladder

| Level | Meaning | Gate |
|---|---|---|
| L0 Allocation | envelope, mass and CG estimate, interfaces | in the breakdown, estimate source stated |
| L1 Concept | parametric geometry from the template, driven by the skeleton | no clash at the stated clearance; mass within allocation |
| L2 Engineered | sized by its analyses, material chosen | all sizing analyses pass with margin |
| L3 Manufacturable | process features, tolerances, PMI, drawing | process checks pass; stack-ups close |
| L4 Released | immutable inventory item version | review sign-off; reproducible geometry hash |

### 4.4 Budgets flow down, actuals roll up

Requirements set product budgets (mass, cost, power, volume, CO2e). The module allocates
them down the breakdown; every part's estimate or computed value rolls back up. An
overrun at any node is flagged where it happens, with the parts that caused it, instead
of being discovered at the weigh-in.

## 5. Workbenches

The established suites organise their tools into workbenches grouped by discipline:
mechanical design, shape, analysis and simulation, equipment and systems, digital
mock-up, knowledgeware and machining. Autevra covers the same disciplines with
**shared, module-scoped workbenches**. Each one acts only on the current module's parts
and adds what a browser-native, intent-first platform makes possible.

| Discipline | Autevra workbench | Today | Target | What we do differently |
|---|---|---|---|---|
| Sketching | **Sketcher** | constraint solver (Gauss–Newton) | full constraint set, construction geometry, sketch-on-face | degrees of freedom shown live; conflicting constraints named, not just "over-constrained" |
| Solid features | **Part Design** | 17 feature types, feature DAG, incremental rebuild, power copies, design tables | holes (standard), ribs, draft, thread, boolean bodies, multi-body | visible dependency graph; rebuild time per feature; reorder checked before it breaks |
| Surfaces | **Shape** | NURBS, styling curves, styled body | G1/G2/G3 blends, fillet surfaces, curvature combs, zebra and highlight lines, class-A checks | continuity checks as rules that run on every edit |
| Sheet metal | **Sheet metal** | channel feature | walls, flanges, hems, bend reliefs, K-factor unfold, flat pattern DXF | bend allowance and minimum flange checked against the material |
| Structures from profiles | **Weldment** | conveyor and bicycle presets | profiles along a skeleton, end treatments, weld beads, cut lists | beam FEA directly on the skeleton, before solids exist |
| Composites | **Composites** | — | plies, zones, stacking, drape (kinematic), ply book, laminate stiffness (classical laminate theory) | laminate properties feed Structures automatically |
| Moulds and dies | **Tooling** | mould-half preset | draft analysis, parting line, core/cavity split, shrinkage | draft is a continuous rule on moulded parts, not a final check |
| Assembly | **Assembly** | interface frames and mates in the land-vehicle model | interface mating for any item, sub-assemblies, flexible assemblies, exploded views, BOM | ports snap by type (shaft to shaft, bolt pattern to bolt pattern) with compatibility checks, not face-picked constraints |
| Digital mock-up | **DMU** | clearance and packaging checks | kinematics and mechanism simulation, swept envelopes, clash and clearance matrix, service and removal paths | suspension travel, door swing and gear retraction come from the product model, not hand-built mechanisms |
| Systems routing | **Routing** | pipe-run preset | harness, tubing, piping and duct routing along skeleton paths; bundles, bend rules, clamps | bundle diameter, voltage drop and pressure drop update as the route changes |
| Tolerancing and annotation | **PMI** | — | GD&T on 3D, datum schemes, 1D/3D stack-ups (worst case and statistical) | stack-ups at interfaces are part of the L3 gate |
| Drafting | **Drafting** | A3 third-angle views, hidden lines, dimensions | sections, details, BOM tables, balloons, views generated from PMI | drawings regenerate from the model; never edited by hand |
| Knowledge | **Rules and optimisation** | rules, requirements, traceability, optimiser, power copies | part templates, budgets, design studies (sweeps, Pareto fronts) | the platform's core rather than an add-on |
| Structural analysis | **Structures** | linear FEA (TET4/TET10/HEX8), SIMP topology optimisation, B-rep face loads | shells and beams, modal, buckling, thermal, fatigue estimate, assembly contact | runs inside the design session; mesh and convergence shown |
| Fluids and aero | **Aero / Hydro** | lifting line, drag build-up | panel method, hull resistance, propeller BEM | module-specific; results feed the product model |
| Machining | **Manufacturing** | — | process plans, 2.5-axis toolpaths, stock and cycle-time estimates | cost estimators in templates use the same process plan |
| Reverse engineering | **Scan** | — | mesh/point-cloud import, fit surfaces | later |
| Visualisation | **Render** | PBR materials, environments | turntables, configurators | configurator options are product parameters |

Honest gaps against mature systems remain: class-A surfacing depth, very large assembly
performance, enterprise PLM and certification-grade solvers. These are on the roadmap,
and every result states its credibility and limits.

## 6. The shared inventory

The inventory is the platform's library of engineered items, shared across modules and
projects. It replaces "copy a STEP file around" with **live, versioned, typed reuse**.

### 6.1 What an item is

```
Item (versioned, e.g. "I4 2.0 turbo petrol" v1.3.0, released)
├── definition       parametric source: a module product spec, a part template instance,
│                    a Part Design document, or an imported B-rep (STEP)
├── geometry         regenerated B-rep + display mesh, cached by definition hash
├── interfaces       typed ports: mount points, shafts, flanges, electrical, fluid, bolt
│                    patterns — each with a frame (position + orientation) and attributes
├── properties       mass, CG, inertia tensor, material, cost, CO2e
├── performance      maps the item publishes (torque curve, thrust map, efficiency map)
├── maturity         L0–L4 and the evidence for its gate
├── provenance       who/what made it, from which project and version, licence
└── usage            where-used: every project and assembly that installs it
```

Kinds of item: **standard parts** (catalogue section 4: fasteners, bearings, seals,
gears, springs, profiles, tyres), **module products** (an engine, a wheel, a seat, a
wing), **user parts** (from Part Design or a template), and **imported parts** (STEP, with
interfaces added by picking faces).

### 6.2 Using an item in any module

1. **Find** it by category, text, or by the interface it must fit ("an engine with a
   flywheel interface, 150–200 kW, under 180 kg").
2. **Place** it by **mating interfaces**, not coordinates: its `flywheel` port snaps to the
   vehicle's `gearbox.input`; its `mount` ports to the frame's mount brackets.
3. **Check** compatibility automatically: shaft sizes and speed ranges, power required
   versus offered, envelope clearance, mass budget.
4. **Stay linked**: the installed item references a version. A new version shows its
   impact on every consumer (mass, CG, performance, clearance) before upgrading; upgrades
   are explicit commands in the consumer's history.
5. **Override locally** without forking: a placement, a colour or a configuration
   (design-table row) is a local setting; changing the geometry means a new item version.

### 6.3 Interfaces are the contract

Interfaces are defined in a platform registry with kinds and attributes:
`mechanical.mount` (bolt pattern, load rating), `mechanical.shaft` (diameter, spline,
speed range), `power.output` (map reference), `electrical.hv` (voltage class),
`fluid.port` (diameter, medium), `structure.hardpoint` (loads), `route.path` (harness or
pipe waypoints). Modules declare which kinds they offer and consume; the platform does
the snapping, frames and checks. This exists today inside the land-vehicle model (frames,
mates, interface kinds); the inventory lifts it to the platform.

## 7. The workflow

The workflow is the same in every module; only the product model, breakdown and analyses
differ. It is concurrent: parts mature in parallel under budgets, with review gates
computed from the model rather than assembled by hand.

```
 Intent ──► Concept ──────► Architecture ──────► Detail ────────► Verify ─────► Release
   │          │                 │                    │               │             │
 require-   template +       skeleton frozen      part templates   module +       item versions
 ments,     parameters;      enough to work;      L1 → L3 in the   FEA, DMU,      to the
 budgets    whole breakdown  inventory items      process work-    tolerance,     inventory;
 (traced)   at L0; instant   mated by interface;  benches; budgets reports        drawings,
            analyses         budgets allocated    roll up live                    STEP, BOM
   ▼          ▼                 ▼                    ▼               ▼             ▼
          Concept review      Preliminary review   Critical review  Verification   Release
          (all L0, require-   (critical parts L2,  (all parts L3,   (all analyses  (all L4)
          ments covered)      budgets closed)      stack-ups close) pass)
       ◄────────────── impact graph re-runs only what each change affects ──────────────►
```

What makes it different from the established workflow:

| Established CAD practice | Autevra |
|---|---|
| The product is complete only when the last part is modelled | The whole breakdown exists at L0 from the first minute; mass, CG and cost are always complete |
| Geometry first; analysis later, in another tool, by another team | Analyses run on every change, inside the session, with equations and convergence shown (glass box) |
| Reviews prepared by hand from slides and spreadsheets | Review gates computed from maturity, budgets and requirement coverage |
| Feature trees break when upstream faces change | Parts read named skeleton entities and interface frames only |
| Product knowledge in people's heads and spreadsheets | Rules, templates, budgets and requirements live in the model and are checked continuously |
| Reuse by copying files; links break, versions drift | Versioned inventory items with typed interfaces, where-used and impact-before-upgrade |
| Menus and dialogs | Commands (typed or natural language) that are validated, previewed for impact and undoable |
| Desktop installs and licence servers | Browser-native; the same model on any machine |
| History is a file | Every change is a command in a diff-able history; design branches and comparisons |

## 8. Data model

```
Organisation ─┬─ Project (module, owner) ── Product (module's parametric product)
              │      ├── history (commands)    ├── skeleton (published entities)
              │      ├── requirements, budgets ├── breakdown ── PartInstance
              │      └── runs, studies, reviews│     (template@version, code, maturity,
              │                                │      inputs, allocation, owner)
              │                                └── installed items (item@version + mates)
              ├─ Template registry ── PartTemplate (module, code pattern, contract)
              ├─ Materials & processes ── Material, Process (rules, cost model)
              └─ Inventory ── Item ── ItemVersion (definition, interfaces, properties,
                                                   performance, maturity, geometry hash)
                                └── usage (project, product, installation)
```

- A project belongs to exactly one module (`domain` today).
- Item versions are immutable once released; a working version can change.
- Geometry is never the source of truth: it is regenerated from the definition and
  cached by hash (the cache exists today for vehicle components and parts).

## 9. Technical architecture

| Layer | Responsibility | Today | Target |
|---|---|---|---|
| Kernels | geometry, solvers | OCCT via CadQuery, NURBS, FEA, SIMP, sketch solver, lifting line, HLR drawings | + sheet unfolding, laminate theory and drape, routing, involute gears, multibody kinematics, Brayton/Otto cycles, hydrostatics, tolerance stack-ups |
| Workbenches | domain-neutral tools | Part Design (DAG, incremental rebuild), Shape, Structures, Drafting | section 5 |
| Modules | products | land vehicles (`domains/automotive`), aircraft (`aero`) | `modules/<id>` packages with breakdowns, templates and module-keyed registries |
| Services | projects, commands, impact, requirements, AI | per project, process-wide registries | breakdown and maturity, template registry, budgets, inventory, materials and processes, job queue |
| Storage | SQL + files | projects, parts, stylings, runs | + part instances, items, item versions, usage, templates, materials |
| Studio | React | module switcher, scoped workspaces | + breakdown tree with maturity heat map, inventory browser, interface snapping, review dashboards |

Rules enforced by tests (extending `tests/test_architecture.py`): kernels import no
module; modules import no other module; a project's API calls only reach its own module;
every template passes its reference cases.

## 10. Milestones

| # | Milestone | Delivers | Proof |
|---|---|---|---|
| M0 | **Modules kept apart** (done) | module switcher; aircraft projects without a car; scoped workspaces | tests: no mixing |
| M1 | **Module-keyed registries, breakdown, L0** | `autevra.modules.<id>` layout; template contract; breakdown + L0 allocation for land vehicles and aircraft; maturity heat map | every product complete at L0; mass and CG roll-ups match the product model |
| M2 | **Inventory core + first standard parts** | items, versions, interfaces, where-used; fasteners, bearings, profiles; publish a part and install it elsewhere by mating | API + studio round trip; ISO 281 and bolt checks against hand calculation |
| M3 | **Piston engines** | Mechanical module; full engine breakdown at L0; block, crank, rods, pistons, head, cam at L1–L2; cycle, torque curve, balance | closed-form cycle and balance checks; known engines within stated error |
| M4 | **Install engines across modules** | vehicle powertrain and aircraft engine from the inventory; compatibility checks | performance follows the engine version |
| M5 | **Manufacturing workbenches** | sheet metal unfold, weldments, draft and parting, PMI and stack-ups; L3 gate | unfold lengths vs. bend-allowance tables; stack-up examples |
| M6 | **Aircraft structure** | ATA 53/55/57 templates (frames, stringers, spars, ribs, skins) at L1–L2; control surfaces, gear | beam and buckling checks against textbook cases |
| M7 | **Marine module** | hull form, hydrostatics, GZ, Holtrop; hull structure and shaft-line templates; installs inventory engines | hydrostatic tables against hand calculation |
| M8 | **Electric machines and gas turbines** | PMSM/induction parts and maps; Brayton turbojet/turbofan/turboprop with stage parts | textbook cycle examples |
| M9 | **Assembly, DMU and routing** | multi-item assemblies, mechanisms, swept envelopes, harness and pipe routing, BOM across the breakdown | mechanism and clearance cases |
| M10 | **Composites, tooling, STEP** | plies and laminate stiffness, mould splits, STEP import with picked interfaces | laminate theory examples; STEP round trip |

Each milestone ends green (tests, lint, live check in the studio) and is committed
locally; pushes happen at milestone boundaries.
