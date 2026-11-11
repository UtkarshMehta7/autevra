# Autevra platform architecture (target)

Status: **design, November 2026**. This is the architecture the platform grows into; each
milestone below states what exists today and what it adds. [ARCHITECTURE.md](ARCHITECTURE.md)
describes the code as built; this file is the plan it follows. No parity with, or
affiliation to, any other vendor is claimed.

## 1. What we are building

One engineering platform where **every product is a module** (land vehicles, aircraft,
marine, engines and machinery, …), **every module draws on one shared inventory of
engineered items** (parts, assemblies, engines, standard components), and **every number
is computed in the open** from the design's own parameters.

The design brief, as an engineer would state it:

1. A module must be complete for its domain: its own product model, rules, analyses,
   workspaces and vocabulary. Modules never mix in one project or one view.
2. Anything engineered once is reusable everywhere: an engine designed in the Mechanical
   module is an inventory item a car, an aircraft or a boat can install, with its
   interfaces, mass properties and performance travelling with it.
3. The source of truth is intent, not geometry: parameters, features and command history
   regenerate the geometry, so every design is editable, diff-able and reproducible.
4. Engineering is continuous, not a separate phase: each change re-runs exactly the
   analyses it affects and shows the equations, inputs and convergence behind every result.

## 2. Platform map

```
┌───────────────────────────── Studio (browser) ─────────────────────────────┐
│  Module switcher: Land vehicles │ Aircraft │ Marine │ Mechanical │ …       │
│  Module workspaces (the module's own)   +   Shared workbenches (scoped)    │
│  Inventory browser (search, filter by interface, drag into the design)     │
└───────────────┬───────────────────────────────────────────────┬────────────┘
                │ HTTP / events                                 │
┌───────────────▼────────────── Platform services ──────────────▼────────────┐
│ Projects & products │ Inventory & versions │ Interfaces & mating │ Jobs     │
│ Commands & history  │ Requirements & trace │ Impact graph        │ AI tools │
└───────┬─────────────────────┬─────────────────────┬────────────────────────┘
┌───────▼──────┐  ┌───────────▼──────────┐  ┌────────▼────────────────────────┐
│ Modules      │  │ Shared workbenches   │  │ Engineering kernels             │
│ (domain      │  │ Part Design (feature │  │ Geometry: OCCT B-rep, NURBS,    │
│  packs)      │  │  DAG), Sketcher,     │  │  continuity, topology           │
│ land, air,   │  │ Surfaces, Structures │  │ Solvers: FEA, SIMP, sketch GN,  │
│ marine,      │  │ (FEA, topology opt), │  │  lifting line, cycles, dynamics │
│ mechanical,  │  │ Drafting, Assembly   │  │ Units, parameters, rules        │
│ …            │  │                      │  │                                 │
└──────────────┘  └──────────────────────┘  └─────────────────────────────────┘
                              Storage: projects, items, versions, files
```

Three kinds of building block, with strict rules between them:

| Block | Owns | May depend on | Examples |
|---|---|---|---|
| **Kernel** | mathematics and geometry, no product knowledge | nothing above it | `cad`, `geometry`, `fea`, `aero.lifting_line`, `part` |
| **Workbench** | a domain-neutral way of working on parts | kernels, services | Part Design, Surfaces, Structures, Drafting |
| **Module** | a product domain: product model, rules, analyses, workspaces, language | kernels, workbenches, services, the inventory | Land vehicles, Aircraft, Mechanical |

A module never imports another module. Modules meet **only through the inventory and
typed interfaces** (section 4), which is what keeps them separate yet able to share work.

## 3. Modules

Each module is a package (`autevra.modules.<id>`) registering one `ModuleDef`:

- **product model**: the parametric product (a vehicle, an aircraft, a hull, an engine)
  as parameters, derived values and rules, generating its geometry and its bill of
  materials;
- **workspaces**: its own studio tabs (plus the shared workbenches it enables);
- **analyses**: tests and solvers with stated credibility and limits;
- **interfaces it offers and consumes** (e.g. a vehicle consumes a `powertrain.mount`);
- **language**: the vocabulary its command parser and AI tools understand;
- **templates**: starting points (a hatchback, a trainer aircraft, a planing hull).

Registries (parameters, rules, tests, builders) are keyed by module, so a project only
ever sees its own module's definitions. Today they are process-wide; keying them is
milestone M1.

### 3.1 Module catalogue

| Module | Product families | First analyses | Status |
|---|---|---|---|
| **Land vehicles** | cars (all body styles), SUVs, pickups; then motorcycles, trucks, buses, trailers | packaging, ride and pitch, longitudinal performance, clearances | available |
| **Aircraft** | fixed-wing (light, trainer, UAV); then rotorcraft, eVTOL | lifting line, drag build-up, stability, Breguet performance | experimental |
| **Mechanical: engines** | category-wise, see 3.2 | thermodynamic cycle, torque and power curves, balance, mass | planned (next) |
| **Marine** | displacement and planing hulls, catamarans; propulsion | hydrostatics, stability (GZ curve), resistance (Holtrop), powering | planned |
| **Mechanical: machinery** | mechanisms, gearboxes, drives, robot arms | kinematics, gear sizing, bearing life | planned |
| **Space** | launchers and spacecraft structures | mass and delta-v budgets, rocket sizing | planned |
| **Tooling and plant** | moulds, dies, piping, conveyors | draft and parting, flow routing | planned |

### 3.2 Engines, category by category

Engines are designed in the Mechanical module as **products in their own right** and
published to the inventory, from where vehicles, aircraft and boats install them.

| Category | Variants | Parametric definition | Analyses (open methods) | Outputs to the inventory |
|---|---|---|---|---|
| **Piston, spark ignition** | inline, V, boxer, W; 1–16 cylinders | bore, stroke, cylinders, layout, bank angle, compression ratio, rpm limits | displacement, Otto cycle with real-gas correction, BMEP-based torque and power curves, firing order, primary/secondary balance forces and couples, mass estimate | envelope, mounts, crank axis, flywheel interface, torque curve, fuel map, mass and CG |
| **Piston, compression ignition** | inline, V; automotive to marine | as above, plus injection and boost | Diesel / dual cycle, turbo-matching estimate | as above |
| **Rotary (Wankel)** | 1–4 rotors | generating radius, eccentricity, width | chamber volume, cycle | as above |
| **Electric machines** | PMSM, induction, axial flux | stack length, diameter, poles, winding, cooling | torque constant, efficiency map, continuous vs peak, thermal estimate | shaft interface, power and efficiency maps, voltage class |
| **Gas turbines** | turbojet, turbofan, turboprop, turboshaft | pressure ratios, bypass ratio, turbine entry temperature, spool layout | Brayton cycle with component efficiencies, thrust and SFC, station table | thrust or shaft-power maps, envelope, mounts |
| **Rocket engines** | liquid, solid | chamber pressure, expansion ratio, propellants | ideal nozzle flow, Isp, thrust | thrust, Isp, mass |

Engines share a common **engine interface** so a consumer does not care which category
it installs: mount points, output shaft (axis, spline/flange, speed range), envelope,
mass properties, and a performance map (torque or thrust versus speed and throttle).

## 4. The shared inventory

The inventory is the platform's library of engineered items, shared across modules and
projects. It replaces "copy a STEP file around" with **live, versioned, typed reuse**.

### 4.1 What an item is

```
Item (versioned, e.g. "I4 2.0 turbo petrol" v1.3.0, released)
├── definition       parametric source: a module product spec, a Part Design document,
│                    or an imported B-rep (STEP) with no parameters
├── geometry         regenerated B-rep + display mesh, cached by definition hash
├── interfaces       typed ports: mount points, shafts, flanges, electrical, fluid, bolt
│                    patterns — each with a frame (position + orientation) and attributes
├── properties       mass, CG, inertia tensor, material, cost
├── performance      maps the item publishes (torque curve, thrust map, efficiency map)
├── provenance       who/what made it, from which project and version, licence
└── usage            where-used: every project and assembly that installs it
```

Kinds of item: **standard parts** (ISO fasteners, bearings, seals, tyres, profiles),
**module products** (an engine, a wheel, a seat, a wing), **user parts** (from Part
Design), and **imported parts** (STEP, with interfaces added by picking faces).

### 4.2 Using an item in any module

1. **Find** it in the inventory browser by category, text, or by the interface it must
   fit ("an engine with a flywheel interface, 150–200 kW, under 180 kg").
2. **Place** it by **mating interfaces**, not coordinates: its `flywheel` port snaps to the
   vehicle's `gearbox.input`; its `mount` ports to the frame's mount brackets.
3. **Check** compatibility automatically: shaft sizes and speed ranges, power required
   versus offered, envelope clearance against the surrounding parts, mass budget.
4. **Stay linked**: the installed item references a version. A new engine version shows
   the impact on every consumer (mass, CG, performance, clearance) before upgrading;
   upgrades are explicit commands in the consumer's history.
5. **Override locally** without forking: a placement, a colour or a configuration
   (design-table row) is a local setting; changing the geometry means a new item version.

### 4.3 Interfaces are the contract

Interfaces are defined in a platform registry (`interfaces`) with kinds and attributes:
`mechanical.mount` (bolt pattern, load rating), `mechanical.shaft` (diameter, spline,
speed range), `power.output` (map reference), `electrical.hv` (voltage class),
`fluid.port` (diameter, medium), `structure.hardpoint` (loads). Modules declare which
kinds they offer and consume; the platform does the snapping, frames and checks. This
already exists inside the land-vehicle model (frames, mates, interface kinds); the
inventory lifts it to the platform.

## 5. The workflow

The workflow is the same in every module; only the product model and analyses differ.

```
 Intent ──► Concept ──► Architecture ──► Detail ──► Verify ──► Release
  │           │             │              │           │          │
 requirements template +   inventory      Part Design  module     item version
 + natural    parameters   items mated    features,    analyses   to the inventory,
 language     (instant     by interface   surfaces,    + FEA,     STEP/drawings,
 (traced)     analyses)    (checks run)   drawings     reports    where-used updated
       ◄──────────── impact graph re-runs only what each change affects ────────────►
```

What makes it better than the established workflow:

| Established CAD practice | Autevra |
|---|---|
| Geometry first; analysis later, in another tool, by another team | Analyses run on every change, inside the design session, with their equations and convergence shown (glass box) |
| Product knowledge in people's heads and spreadsheets | Rules, derived values and requirements live in the model and are checked continuously |
| Reuse by copying files; links break, versions drift | Versioned inventory items with typed interfaces, where-used and impact-before-upgrade |
| Menus and dialogs | Commands (typed or natural language) that are validated, previewed for impact and undoable |
| Desktop installs and licence servers | Browser-native; the same model on any machine |
| Hidden feature dependencies | The feature DAG is visible: what each feature reads, what rebuilds after it |
| History is a file | Every design change is a command in a diff-able history; branches and comparisons of designs |

Honest gaps against mature systems: class-A surfacing, large-assembly performance,
PLM at enterprise scale, certification-grade solvers. These are on the roadmap, and
results always state their credibility and limits.

## 6. Data model

```
Organisation ─┬─ Project (module, owner) ── Product (module's parametric product)
              │      ├── history (commands)   ├── local parts (Part Design)
              │      ├── requirements          └── installed items (item@version + mates)
              │      └── runs, studies
              └─ Inventory ── Item ── ItemVersion (definition, interfaces, properties,
                                                   performance, geometry hash, status)
                                └── usage (project, product, installation)
```

- A project belongs to exactly one module (`domain` today).
- Item versions are immutable once released; a working version can change.
- Geometry is never the source of truth: it is regenerated from the definition and
  cached by hash (the cache exists today for vehicle components and parts).

## 7. Technical architecture

| Layer | Responsibility | Today | Target |
|---|---|---|---|
| Kernels | geometry, solvers | OCCT via CadQuery, NURBS, FEA, SIMP, sketch solver, lifting line | + Brayton/Otto cycles, hydrostatics, multibody kinematics |
| Workbenches | domain-neutral tools | Part Design (DAG, incremental rebuild), Surfaces, Structures, drawings | + Assembly workbench (interface mating), Inventory browser |
| Modules | products | land vehicles (in `domains/automotive`), aircraft (`aero`) | `modules/<id>` packages with module-keyed registries |
| Services | projects, commands, impact, requirements, AI | per project, process-wide registries | module-scoped registries; inventory service; job queue for long analyses |
| Storage | SQL + files | projects, parts, stylings, runs | + items, item_versions, usage, interface registry |
| Studio | React | module switcher, scoped workspaces | + inventory browser, interface snapping, where-used views |

Rules enforced by tests (extending `tests/test_architecture.py`): kernels import no
module; modules import no other module; a project's API calls only reach its own module.

## 8. Milestones

| # | Milestone | Delivers | Proof |
|---|---|---|---|
| M0 | **Modules kept apart** (done) | module switcher; aircraft projects without a car; module-scoped workspaces | tests: no mixing |
| M1 | **Module-keyed registries** | `autevra.modules.<id>` layout; registries per module; aircraft becomes a full module (parameters, rules, history, commands) | architecture tests |
| M2 | **Inventory core** | items, versions, interfaces, where-used; publish a Part Design part; install it in another project by mating interfaces | API + studio round trip |
| M3 | **Engines: piston (SI and CI)** | Mechanical module, engine product model, cycle, torque/power curve, balance; publish to the inventory | closed-form cycle checks, known engines within stated error |
| M4 | **Install engines across modules** | land vehicle powertrain from an inventory engine; aircraft propeller engine from the inventory; compatibility checks | performance follows the engine version |
| M5 | **Engines: electric and gas turbine** | PMSM/induction maps; Brayton turbojet/turbofan/turboprop | textbook cycle examples |
| M6 | **Marine module** | hull form, hydrostatics, GZ stability, Holtrop resistance; installs inventory engines | hydrostatic tables against hand calculation |
| M7 | **Standard parts and STEP import** | ISO fasteners, bearings, tyres; imported parts with picked interfaces | round trip STEP |
| M8 | **Assembly workbench** | multi-item assemblies, interference, exploded views, BOM across modules | — |

Each milestone ends green (tests, lint, live check in the studio) and is committed
locally; pushes happen at milestone boundaries.
