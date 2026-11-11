# Autevra platform architecture (target)

Status: **design, November 2026**. This is the architecture the platform grows into; each
milestone below states what exists today and what it adds. [ARCHITECTURE.md](ARCHITECTURE.md)
describes the code as built; this file is the plan it follows.
[PART_CATALOGUE.md](PART_CATALOGUE.md) lists every part each module designs. The
established CAD/PLM suites (CATIA and its peers) are used as a reference for the *breadth*
an engineering platform needs; no parity with, or affiliation to, any vendor is claimed.

## 1. What we are building

One engineering platform where **every product is a module** (land vehicles, aircraft,
marine, engines and machinery, …), engineered through **one connected model**:

```
 Requirements ─► Functions ─► Logical architecture ─► Physical parts ─► Manufacturing
 (needs, regs,   (what it     (systems and the       (breakdown of     (MBOM, process
  budgets)        must do)     flows between them)    part templates)   plan, quality)
        ▲             │               │                     │                 │
        └──── verification: analyses, loads, safety, simulation, inspection ◄─┘
          configurations (variants, options, effectivity) apply to every layer
```

The design brief, as a team of vehicle, systems, aerospace and manufacturing engineers
would state it:

1. **Modules are complete and separate.** Each has its own product model, breakdown,
   rules, analyses, workspaces and vocabulary. Modules never mix in one project or view.
2. **Function before form.** Every part exists because a function needs it; every
   function traces to a requirement; every requirement to a need or a regulation clause.
3. **The whole product exists from day one.** Every part starts as an allocation
   (envelope, mass, CG, interfaces) and matures through concept, engineered,
   manufacturable and released levels. Mass, balance, cost and packaging are always complete.
4. **One model, many configurations.** Variants, options and markets are rules over one
   product (a "150 %" model), never copies of it.
5. **Parts are generators, sized by traced loads.** Part templates carry inputs, rules,
   interfaces, a manufacturing process and analyses; their loads come from named load
   cases, and their strength from stated material allowables.
6. **Designed to be built.** The manufacturing view (MBOM, assembly sequence, joints,
   inspection) is developed alongside the design, not after it.
7. **Reuse is live and typed.** Engines, standard parts and platforms are versioned
   inventory items installed by mating interfaces, with where-used and impact before upgrade.
8. **Intent is the source of truth.** Parameters, features and command history
   regenerate geometry; every design is editable, diff-able, branchable and reproducible.
9. **Glass-box engineering.** Each change re-runs exactly the analyses it affects and
   shows the method, inputs, convergence and credibility of every result.

## 2. Platform map

```
┌─────────────────────────────────── Studio (browser) ───────────────────────────────────┐
│ Module switcher │ Requirements · Functions · Logical · Physical · Manufacturing views    │
│ Breakdown tree (maturity heat map, configuration filter) │ Workspaces │ Workbenches     │
│ Inventory browser │ Reviews and change requests │ Branches and comparisons              │
└──────────────┬──────────────────────────────────────────────────────────┬──────────────┘
               │ HTTP / events                                            │
┌──────────────▼────────────────────── Platform services ─────────────────▼──────────────┐
│ Projects, branches, merges │ Commands & history │ Configurations & effectivity          │
│ Requirements & regulations │ Functions & logical│ Breakdown & maturity │ Budgets          │
│ Part templates │ Inventory │ Interfaces & flows │ Load cases │ Materials & allowables   │
│ Safety (FMEA, FTA) │ Manufacturing (MBOM, BOP, joints, quality) │ Change (ECR/ECO)      │
│ Impact graph │ Job queue & workers │ Geometry store (by hash) │ Access control │ AI    │
└──────┬─────────────────────────┬──────────────────────────────┬────────────────────────┘
┌──────▼───────┐  ┌──────────────▼────────────┐  ┌───────────────▼─────────────────────┐
│ Modules      │  │ Shared workbenches        │  │ Engineering kernels                 │
│ land, air,   │  │ (section 6): Sketcher,    │  │ Geometry: OCCT B-rep, NURBS,        │
│ marine,      │  │ Part, Shape, Sheet metal, │  │  naming, unfolding, routing, LOD    │
│ mechanical,  │  │ Weldment, Composites,     │  │ Solvers: FEA, SIMP, sketch, lifting │
│ space, …     │  │ Assembly, DMU, Routing,   │  │  line, cycles, multibody, hydro-    │
│              │  │ PMI, Drafting, Structures,│  │  statics, laminate theory, ODE/     │
│              │  │ Manufacturing, …          │  │  system simulation, reliability     │
└──────────────┘  └───────────────────────────┘  └─────────────────────────────────────┘
                     Storage: event log, SQL, content-addressed geometry, files
```

Three kinds of building block, with strict rules between them:

| Block | Owns | May depend on | Examples |
|---|---|---|---|
| **Kernel** | mathematics and geometry, no product knowledge | nothing above it | `cad`, `geometry`, `fea`, `aero.lifting_line`, `part` |
| **Workbench** | a domain-neutral way of working | kernels, services | Part Design, Sheet metal, Structures, Drafting |
| **Module** | a product domain: product model, breakdown, templates, functions, load cases, rules, analyses, workspaces, language | kernels, workbenches, services, the inventory | Land vehicles, Aircraft, Mechanical |

A module never imports another module. Modules meet **only through the inventory and
typed interfaces** (section 8).

## 3. Modules

Each module is a package (`autevra.modules.<id>`) registering one `ModuleDef`:

- **product model**: parameters, derived values and rules; owns the **skeleton**
  (published hardpoints, axes, reference surfaces, stations, zones);
- **function library**: the functions its products perform ("decelerate vehicle",
  "generate lift", "provide buoyancy") and their standard decomposition;
- **breakdown and part templates** (section 5 and the catalogue);
- **load-case library**: the load cases its domain sizes against (section 9.1);
- **regulation library**: references to the clauses its products must show compliance
  with (section 9.2);
- **analyses, workspaces, interfaces offered and consumed, language, templates**.

Registries (parameters, rules, tests, builders, templates, functions, load cases) are
keyed by module. Today they are process-wide; keying them is milestone M1.

### 3.1 Module catalogue

| Module | Product families | Breakdown standard | Regulation families (referenced) | Status |
|---|---|---|---|---|
| **Land vehicles** | cars, SUVs, pickups; motorcycles, trucks, buses, trailers | system → subsystem → part | UN ECE regulations, FMVSS, Euro NCAP protocols, ISO 26262 | available |
| **Aircraft** | fixed-wing (light, trainer, UAV, glider); rotorcraft, eVTOL | ATA chapters | CS-23 / 14 CFR Part 23, CS-VLA, ARP4754A / ARP4761 | experimental |
| **Mechanical: engines** | piston SI/CI, rotary, electric, gas turbine, rocket | functional groups | emissions and installation requirements of the consumer | planned (next) |
| **Mechanical: machinery** | gearboxes, mechanisms, robots, frames, pressure equipment, conveyors, tooling | functional groups | ISO 12100, ISO 13849, pressure-equipment codes | planned |
| **Marine** | displacement and planing hulls, catamarans, sailing yachts | SFI/ESWBS groups | ISO 12215 (small-craft scantlings), ISO 12217 (stability), class rules | planned |
| **Space** | launchers and spacecraft structures | stage → subsystem | ECSS standards | later |

Regulations are stored as **clause references plus our own requirement wording**, never
the copyrighted text; users attach their licensed copies.

### 3.2 Engines, category by category

Engines are **products of the Mechanical module**, published to the inventory and
installed by vehicles, aircraft and boats through a common **engine interface** (mounts,
output shaft, envelope, mass properties, performance map, fluid and electrical ports).

| Category | Variants | Parametric definition | Analyses (open methods) |
|---|---|---|---|
| **Piston, spark ignition** | inline, V, boxer, W; 1–16 cylinders | bore, stroke, cylinders, layout, bank angle, compression ratio, rpm limits | Otto cycle with real-gas correction, BMEP torque and power, firing order, balance, mass |
| **Piston, compression ignition** | inline, V | as above, plus injection and boost | Diesel / dual cycle, turbo matching |
| **Rotary (Wankel)** | 1–4 rotors | generating radius, eccentricity, width | chamber volume, cycle |
| **Electric machines** | PMSM, induction, axial flux | stack, diameter, poles, winding, cooling | torque constant, efficiency map, thermal |
| **Gas turbines** | turbojet, turbofan, turboprop, turboshaft | pressure ratios, bypass ratio, TET, spools | Brayton cycle, thrust and SFC, station table |
| **Rocket engines** | liquid, solid | chamber pressure, expansion ratio, propellants | ideal nozzle flow, Isp, thrust |

Each engine is a full part breakdown (catalogue section 8).

## 4. Systems engineering: requirements → functions → logical → physical

The part tree alone cannot answer "what performs braking, through which parts, and what
happens if one fails?". Four linked layers can.

| Layer | Contains | Example (land vehicle) | Example (aircraft) |
|---|---|---|---|
| **Requirements** | needs, regulation clauses, budgets, performance targets; ReqIF import/export (exists today) | stop from 100 km/h in under 36 m | stall speed ≤ 45 kn (CS-23 reference) |
| **Functions** | what the product must do, decomposed | decelerate vehicle → generate friction torque, modulate, keep wheels rolling | control pitch → generate pitch moment, transmit pilot input |
| **Logical architecture** | systems as blocks and the **flows** between them | pedal → brake controller → hydraulic unit → caliper | stick → cables → elevator; trim tab |
| **Physical** | the breakdown of part templates that realise each logical block | pedal box, master cylinder, ESC unit, lines, calipers, discs | stick, pulleys, cables, horns, elevator spars and ribs |

**Flows** are typed and carried on interfaces: mechanical (force, torque, motion),
**electrical power**, **signal and data** (bus, rate, latency), **fluid** (medium,
pressure, flow), **thermal** (heat load). Every flow crossing a system boundary appears in
an **interface control document** generated from the model, with both owners, the agreed
values and the verification of each.

Allocation and trace are links, checked continuously:
every requirement is allocated to a function; every function to a logical block; every
logical block to physical parts; and every requirement has a verification (analysis, test,
inspection or review) with a status. Gaps appear in the review dashboards (section 11).

**Budgets** flow down this tree and actuals roll up: mass, cost, CO2e, volume, electrical
power, heat rejection, data bandwidth. An overrun is flagged at the node that caused it.

## 5. Parts: breakdown, templates, maturity, references

Full lists are in [PART_CATALOGUE.md](PART_CATALOGUE.md); the mechanism is here.

### 5.1 Breakdown

Each product is a tree: product → system → subsystem → part (→ feature), each node with a
breakdown code in the domain's own standard (ATA 57-10, SFI 1xx,
`body.closures.door.inner`). The tree is generated from the product's parameters: a
6-cylinder engine has six connecting rods, a 40-frame fuselage forty frames.
**Repeated parts are instances of one template with per-instance transforms and
inputs**, which is also what keeps large products fast (section 13).

### 5.2 Part templates

A part template is a tested generator with a fixed contract (catalogue, section 3):
inputs, skeleton reads, interfaces and flows, functions realised, manufacturing process,
joints, rules, load cases consumed, materials and allowables, failure modes, generators
per maturity level, analyses and estimators. Today's feature templates ("power copies"),
design tables and presets are the seed.

### 5.3 Maturity ladder

| Level | Meaning | Gate |
|---|---|---|
| L0 Allocation | envelope, mass and CG estimate, interfaces, function link | in the breakdown, estimate source stated |
| L1 Concept | parametric geometry from the template, driven by the skeleton | no clash at the stated clearance; mass within allocation |
| L2 Engineered | sized by its analyses against traced load cases and allowables | every sizing analysis passes with margin; failure modes rated |
| L3 Manufacturable | process features, joints, tolerances and PMI, drawing, MBOM placement | process and DFM checks pass; stack-ups close; inspection characteristics defined |
| L4 Released | immutable item version in a baseline | review sign-off; reproducible geometry hash |

### 5.4 References that survive change

- **Between parts**: a part reads only **published skeleton entities and interface
  frames**, which have stable names. Upstream topology changes cannot break it.
- **Inside a part**: features that pick topology (fillet these edges, sketch on this face)
  store **generated names** built from the creating feature and the element's role
  (`pad3/side(sketch-line-2)`, `hole1/rim`), traced through the kernel's modelling
  history. If a name no longer resolves, a geometric re-match (position, normal,
  adjacency) is scored; a confident match is applied and reported, an ambiguous one stops
  the rebuild at that feature and asks. Feature templates prefer *semantic selectors*
  ("all edges of the pocket floor", "the face mating to `mount_1`") over picked elements.

This reduces, but does not eliminate, the topological naming problem; the rebuild report
always lists which references were re-matched.

## 6. Workbenches

The established suites organise their tools into disciplines: mechanical design, shape,
analysis and simulation, equipment and systems, digital mock-up, knowledgeware,
manufacturing and systems engineering. Autevra covers the same disciplines with
**shared, module-scoped workbenches**.

| Discipline | Autevra workbench | Today | Target | What we do differently |
|---|---|---|---|---|
| Systems engineering | **Systems** | requirements, trace, ReqIF | functions, logical blocks and flows, ICDs, allocation matrices | trace and allocation gaps are live checks, not a report |
| Sketching | **Sketcher** | constraint solver (Gauss–Newton) | full constraint set, construction geometry | DOF shown live; conflicting constraints named |
| Solid features | **Part Design** | 17 feature types, DAG, incremental rebuild, power copies, design tables | standard holes, ribs, draft, threads, multi-body, generated naming | dependency graph visible; rebuild time per feature |
| Surfaces | **Shape** | NURBS, styling curves, styled body | G1–G3 blends, curvature combs, zebra, class-A checks | continuity checks run on every edit |
| Sheet metal | **Sheet metal** | channel feature | flanges, hems, reliefs, K-factor unfold, flat patterns | bend limits checked against the material |
| Profiles and frames | **Weldment** | conveyor, bicycle presets | profiles along a skeleton, end cuts, cut lists | beam FEA on the skeleton before solids |
| Composites | **Composites** | — | plies, zones, stacking, drape, ply book, laminate theory | laminate properties feed Structures automatically |
| Moulds and dies | **Tooling** | mould-half preset | draft, parting line, core/cavity, shrinkage | draft is a continuous rule on moulded parts |
| Joining | **Joints** | — | spot and seam welds, rivets, bolts, adhesive as objects | joint checks and FEA connectors from the same objects |
| Assembly | **Assembly** | interface frames and mates (land vehicles) | interface mating for any item, flexible sub-assemblies, exploded views | ports snap by type with compatibility checks |
| Digital mock-up | **DMU** | clearance and packaging checks | mechanisms, swept envelopes, clash matrix, service paths | travel, swing and retraction come from the product model |
| Systems routing | **Routing** | pipe-run preset | harness, tube, pipe and duct routing; bundles, clamps | bundle size, voltage drop, pressure drop live |
| Tolerancing | **PMI** | — | GD&T on 3D, datums, 1D/3D stack-ups (worst case, statistical) | stack-ups are part of the L3 gate |
| Drafting | **Drafting** | A3 third-angle views, hidden lines, dimensions | sections, details, BOM tables, balloons, views from PMI | regenerated from the model, never hand-edited |
| Knowledge | **Rules and studies** | rules, optimiser, power copies | templates, budgets, design studies (sweeps, Pareto fronts) | the platform's core rather than an add-on |
| Structures | **Structures** | linear FEA (TET4/TET10/HEX8), SIMP, B-rep face loads | shells, beams, modal, buckling, thermal, fatigue, contact | runs in the design session; mesh and convergence shown |
| Fluids and aero | **Aero / Hydro** | lifting line, drag build-up | panel method, hull resistance, propeller BEM | results feed the product model |
| System simulation | **Behaviour** | longitudinal and ride models (land vehicles) | block models, drive cycles, missions, FMI import/export | parameters come straight from the parts and maps |
| Safety | **Safety** | — | FMEA (design and process), fault trees, safety goals | failure modes live on functions and parts |
| Manufacturing | **Manufacturing** | — | MBOM, process plans, stations, cycle time, cost, 2.5-axis toolpaths | MBOM reconciled with the design on every change |
| Quality | **Quality** | — | inspection plans, control plans, CMM export from PMI | characteristics come from the PMI, not retyped |
| Reverse engineering | **Scan** | — | mesh/point-cloud import, surface fitting | later |
| Visualisation | **Render** | PBR materials, environments | turntables, configurators | configurator options are configuration rules |

## 7. Configurations, platforms and change

### 7.1 One product, many configurations

- **Options** are typed codes (`drive=rhd`, `engine=i4_2.0t`, `roof=soft_top`,
  `market=eu`), grouped into families with **rules** (requires, excludes, defaults).
- Every breakdown node, part instance, parameter value, requirement and load case may
  carry an **applicability** expression over options. The product is a "150 %" model;
  a **configuration** is a valid option set, and the studio, analyses, BOMs and drawings
  are always viewed through one.
- Analyses run per configuration, or across all valid configurations for **envelope
  checks** (worst-case mass, CG range, clearance).
- **Effectivity** (from serial number, build date or lot) states when a change applies to
  production.

### 7.2 Platforms

A **platform** is a module-level shared product: a skeleton subset (hardpoints with
allowed ranges) plus the parts it owns (a floor and front structure, a wing box, an engine
family's block). Products derive from a platform and may move hardpoints only within its
ranges. A **commonality** index per product shows how much is shared; a platform change
shows its impact on every derived product before release.

### 7.3 Baselines and change

- A **baseline** is a frozen, named snapshot of every layer for one configuration set,
  taken at each review gate.
- After a baseline, changes go through an **engineering change request** (ECR): the impact
  graph lists every affected requirement, part, analysis, configuration, MBOM line and
  consumer project; the **change order** (ECO) is the approved command batch, merged with
  its effectivity.
- Designers explore on **branches**; merging replays commands with conflict detection at
  parameter and feature level (section 13).

## 8. The shared inventory

The inventory is the platform's library of engineered items: **live, versioned, typed
reuse** instead of copied files.

```
Item (versioned, e.g. "I4 2.0 turbo petrol" v1.3.0, released)
├── definition       module product spec, template instance, Part Design document or STEP
├── geometry         B-rep + display LODs, content-addressed by definition hash
├── interfaces       typed ports with frames: mounts, shafts, flanges, electrical, fluid,
│                    signal, thermal, bolt patterns
├── configurations   its own options (e.g. engine calibration) exposed to consumers
├── properties       mass, CG, inertia, materials, cost, CO2e
├── performance      maps it publishes (torque, thrust, efficiency) and behaviour models
├── safety           failure modes and rates it exports to consumers' FMEA and fault trees
├── maturity         L0–L4 and gate evidence
├── provenance       origin project and version, licence
└── usage            where-used across projects and configurations
```

Kinds: **standard parts** (catalogue section 4), **module products** (engines, wheels,
seats, wings), **platforms**, **user parts**, **imported parts** (STEP, with interfaces
added by picking faces).

Using an item: **find** by category, text or required interface; **place** by mating
interfaces; **check** compatibility (shaft, speed range, power, flows, envelope, mass);
**stay linked** to a version with impact-before-upgrade; **override locally** (placement,
option choice) without forking.

Interfaces are defined in a platform registry: `mechanical.mount`, `mechanical.shaft`,
`power.output`, `electrical.power`, `signal.bus`, `fluid.port`, `thermal.port`,
`structure.hardpoint`, `route.path`. Interface frames and mates exist today inside the
land-vehicle model; the inventory lifts them to the platform.

## 9. Loads, regulations and materials

### 9.1 Load cases are data

Parts are sized against **named load cases**, never against numbers typed into a part.

| Module | Load-case library (method level stated per case) |
|---|---|
| Land vehicles | quasi-static road cases (vertical bump, braking, cornering, pothole, kerb strike, towing), durability spectra, crash pulses and section-force targets, jacking, door slam |
| Aircraft | manoeuvre and gust envelope (V-n diagram), landing and ground handling, control surface loads, engine mount, pressurisation, emergency landing |
| Marine | slamming pressure, still-water and wave bending, hydrostatic panel pressure, rig loads, grounding |
| Engines | peak firing pressure, inertia at maximum speed, overspeed burst, thermal cycles |
| Machinery | rated torque and overload, start-up, emergency stop, fatigue spectra |

A load case is computed by the module from the product model (mass, CG, speeds, geometry)
and **distributed to interfaces**: hardpoint forces and moments, pressure fields, shaft
torques. Each part's sizing records which cases governed it, so changing the product's
mass re-sizes exactly the parts that depend on it.

### 9.2 Regulations

Each regulation clause the product must meet becomes a requirement (with a clause
reference and our own wording), allocated and verified like any other. A **compliance
matrix** per baseline lists clause, requirement, means of compliance (analysis, test,
inspection, similarity), evidence and status. Autevra supports compliance work; it does
not certify.

### 9.3 Materials and allowables

The materials database stores, per material and process: properties with temperature
dependence, **typical** values and, where published, **design allowables** (statistically
based, e.g. A- and B-basis), fatigue curves, joint allowables, cost and CO2e. Every
sizing result states which kind of value it used; results using typical values are
labelled concept-level.

## 10. Safety, reliability and behaviour

- **FMEA**: failure modes live on functions (design FMEA) and on manufacturing operations
  (process FMEA), rated by severity, occurrence and detection (action priority), with
  actions tracked to closure.
- **Fault trees** are generated from the logical architecture (a function fails if its
  blocks fail through their flows) and quantified with failure rates from parts and
  inventory items.
- **Safety goals** per domain method are references, not certifications: hazard analysis
  and integrity levels (ISO 26262), aircraft safety assessment (ARP4761), machinery
  performance levels (ISO 13849).
- **System simulation** (the Behaviour workbench): block models of energy, thermal,
  hydraulic and control systems take their parameters from parts and performance maps:
  vehicle drive cycles and range, aircraft missions, engine warm-up, battery thermal.
  Models export and import as FMUs (FMI) to work with other tools.

## 11. The workflow

The same in every module; only the content differs. It is concurrent: design,
analysis, safety and manufacturing work in parallel on one model, and review gates are
computed from it.

```
 Intent ──► Concept ─────► Architecture ─────► Detail ──────────► Verify ──────► Release
   │          │                │                    │                 │              │
 needs,     functions,       logical blocks       templates L1→L3;  analyses per   L4 items,
 regulation product at L0;   and flows; ICDs;     joints, PMI;      configuration; baseline,
 clauses,   platform choice; inventory mated;     MBOM and process  compliance     drawings,
 budgets,   options and      load cases;          plan; FMEA; DMU;  matrix; fault  STEP, MBOM,
 options    configurations   budgets allocated    behaviour models  trees; stacks  inspection
   ▼          ▼                ▼                    ▼                 ▼              ▼
         Concept review     Preliminary review   Critical review    Verification   Release
         all L0; functions  critical parts L2;   all L3; MBOM       all checks     baseline;
         allocated; budget  ICDs agreed; loads   reconciled; FMEA   pass for every ECR/ECO
         feasible           traced; baseline 1   actions closed     configuration  from here
       ◄──────────── impact graph re-runs only what each change affects ─────────────►
```

Each gate is a **dashboard computed from the model**: maturity per breakdown node,
requirement coverage and verification status, budget margins, open FMEA actions,
unresolved ICD items, MBOM reconciliation, and configuration coverage.

What makes it different from the established workflow:

| Established practice | Autevra |
|---|---|
| The product is complete only when the last part is modelled | Whole breakdown at L0 from the first minute; mass, CG, cost always complete |
| Systems models, CAD, CAE, safety and manufacturing in separate tools, linked by hand | One connected model; trace, loads, safety and MBOM update on every change |
| Variants as copied models | One 150 % model with option rules and effectivity |
| Analysis later, by another team | Analyses run on every change, glass box, with credibility stated |
| Reviews prepared by hand | Gates computed from maturity, trace, budgets, safety and MBOM status |
| Feature trees break when upstream faces change | Skeleton and interface references between parts; generated names inside parts |
| Reuse by copying files | Versioned inventory with typed interfaces, where-used, impact-before-upgrade |
| Menus and dialogs | Validated, previewed, undoable commands, typed or in natural language |
| Desktop installs and licence servers | Browser-native |
| History is a file | Every change a command; branches, merges, comparisons, baselines |

## 12. Manufacturing

### 12.1 EBOM → MBOM → process plan

- The **EBOM** is the physical breakdown (section 5).
- The **MBOM** restructures it the way the product is built: kits, sub-assemblies,
  phantom levels, bought-out items, consumables (sealant, adhesive, paint). It is
  generated from rules (process and assembly order) and edited by commands.
- **Reconciliation** is a continuous check: per configuration, every EBOM part is consumed
  exactly once in the MBOM; mismatches block the critical review.
- The **process plan** (bill of process) lists operations at stations with resources,
  tools, fixtures, standard times and the parts and joints each operation consumes. It
  yields cycle time, line balance and the process cost the templates' estimators use.

### 12.2 Joints are objects

Spot welds, seam welds, rivets, bolts, clinches and adhesive beads are first-class objects
linking parts, with process parameters. The same objects drive joint checks (bolt
clamping, weld throat, rivet pitch), FEA connectors in Structures, operations in the
process plan, and inspection characteristics.

### 12.3 Design for manufacture and assembly

Process rules from each template (draft, minimum radius, wall, bend, ply drop-off,
tool access) run as continuous checks. An assembly-efficiency score (part count, handling
and insertion difficulty, fastener count) is computed per sub-assembly.

### 12.4 Quality

Inspection characteristics are generated from PMI (each toleranced feature and joint),
collected into an inspection plan and a control plan, and exported for CMM programming.
Measured results imported later close the loop against the stack-ups.

## 13. Scale and collaboration

| Concern | Approach |
|---|---|
| Large products (thousands of parts) | instancing of repeated parts; L0 envelopes until opened; display LODs per item; geometry loaded per breakdown subtree on demand; spatial index for clash and picking |
| Slow, single-threaded kernel | content-addressed geometry store (by definition hash) shared by all projects; a job queue with worker processes running B-rep builds, meshing and solvers in parallel; incremental rebuild (exists today for parts) |
| Long analyses | queued jobs with progress, cancel and cached results keyed by inputs |
| Many engineers | per-node ownership in the breakdown; edits as commands on branches; merges replay commands with conflict detection; live presence and comments; access control per project, module and item |
| Audit and reproducibility | an append-only event log of commands; any baseline regenerates bit-for-bit from its log and kernel version |

Performance targets (measured by a benchmark suite in CI, on a stated reference machine;
a regression fails the build):

| Interaction | Target |
|---|---|
| parameter edit → derived values, rules and budgets updated | < 100 ms |
| parameter edit → affected geometry rebuilt and displayed (cached neighbours) | < 1 s for a part, < 3 s for a vehicle |
| open a 5,000-instance product at L0/L1 with display LODs | < 5 s |
| clash check, 5,000 instances | < 10 s |
| configuration switch (re-filter breakdown, BOM, roll-ups) | < 500 ms |
| merge of two branches of 1,000 commands each | < 2 s |
| linear static FEA, 100k DOF | < 30 s, as a background job |


## 14. Data exchange and supplier collaboration

| Need | Approach |
|---|---|
| Neutral CAD exchange | STEP AP242 export and import with product structure and semantic PMI; AP214 and IGES read; STL/3MF and glTF for visualisation and printing |
| Lightweight visualisation | glTF (and JT where a partner requires it) with display LODs |
| Drawings | SVG and PDF (today: SVG), DXF for flat patterns and profiles |
| Requirements | ReqIF import/export (exists today) |
| Behaviour models | FMI 2.0/3.0 FMUs, import and export |
| Supplier packages | an **interface-only item**: envelope, interfaces, mass properties, performance maps and keep-out zones, with no internal geometry or parameters; suppliers return full or simplified items that are checked against the same interfaces |
| Round trip | an imported supplier part keeps its provenance and version; a newer delivery shows its impact before replacing the old one |

Exchange is tested by round trips: export, re-import, compare geometry (volume, area,
centroid within tolerance) and structure.

## 15. Security, intellectual property and export control

- **Classification labels** on projects, items, versions and files: e.g. public,
  internal, confidential, export-controlled (with the jurisdiction and classification,
  such as ITAR or EAR categories, entered by the customer's export officer).
- **Access rules** combine role, project membership, organisation and labels; an
  export-controlled item is visible only to users whose attributes (nationality or
  licence, location) the organisation has cleared. Rules are enforced in the service
  layer and in every export path (files, API, AI context).
- **IP protection** for suppliers and partners: interface-only items (section 14),
  watermarked exports, revocable shares with expiry.
- **Audit**: every read of a labelled item, export, share and permission change is
  recorded in the append-only log.
- **AI and data**: labelled content never leaves the deployment to an external model;
  the local model path (exists today) is the default for restricted projects.
- Autevra provides the mechanisms; compliance with export law remains the customer's
  responsibility.

## 16. Lifecycle after release

The design is one view of the product; after release the platform tracks the others.

| View | Contents | Example |
|---|---|---|
| **As designed** | baselines and configurations (sections 7, 11) | aircraft type design, configuration B |
| **As planned** | MBOM and process plan per plant (section 12) | build plan for line 2 |
| **As built** | per serial number: the configuration, actual part serials and lots, deviations and concessions, measured inspection results | aircraft serial 0042 |
| **As maintained** | per serial: maintenance programme tasks (from the design: inspection intervals derived from fatigue and damage-tolerance analyses), repairs, modifications embodied, life-limited part tracking | landing gear leg at 6,200 of 10,000 cycles |
| **Digital twin** | as-maintained state plus operating data (loads, cycles, temperatures) re-running the design's own analyses to update remaining life | fatigue life consumed by the measured load spectrum |

A design change (ECO) states its retrofit applicability to serials in service, so the
fleet impact is part of the change's impact analysis.

## 17. Test data and model correlation

- **Test plans** are generated from requirements whose verification method is test.
- **Test results** (measured channels, test conditions, the test article's as-built
  configuration) are imported and linked to the analyses that predicted them.
- **Correlation** reports prediction vs. measurement per quantity (stiffness, frequency,
  strain, drag, range) with error metrics; persistent bias is fed back as model
  calibration factors, each with its source.
- An analysis's credibility level (section 22) rises from "checked against reference
  cases" to "validated" only through correlated test data.

## 18. Sustainability

- **Life-cycle assessment** per product and configuration, following the ISO 14040/14044
  structure: materials (from the materials database), manufacturing (from the process
  plan's energy and scrap), use phase (from behaviour simulation: drive cycles, missions,
  duty cycles), and end of life (recyclability by material and joint type).
- CO2e and other impact categories are **budgets** like mass and cost (section 4), with
  estimates at L0 and computed values from L2.
- Design for disassembly: joints record whether they are reversible, and a disassembly
  score is computed per sub-assembly.
- Datasets for emission factors are cited with source and version; users may load licensed
  databases.

## 19. AI: roles and guardrails

AI accelerates engineering; it never signs it off.

| AI may | AI may not |
|---|---|
| translate natural language into typed commands (exists today), always previewed and validated before applying | apply a command without the same validation as a manual edit |
| draft requirements, function decompositions, breakdowns, FMEA rows and test plans for review | approve a review gate, a release, a baseline or a change order |
| suggest templates, materials, inventory items and parameter values, with the reason | change safety ratings, allowables or regulation mappings without a named human owner |
| explain any result: method, inputs, assumptions and limits | present an estimate as a validated result |
| search the inventory and the project history | read or send labelled content outside the permitted deployment (section 15) |

Every AI-originated change is marked as such in the history, with the prompt and the
model used, and is reviewable and reversible like any command. The rule-based parser
remains the fallback when no model is available (exists today).

## 20. Desktop applications (macOS and Windows)

Autevra ships as a browser application today and is built so the same code becomes a
native desktop application on macOS (Apple silicon and Intel) and Windows without a
rewrite.

```
┌──────────── Native shell (Tauri 2) ─────────────┐
│ window, menus, file dialogs, auto-update,       │
│ code signing / notarisation, installer          │
│  ┌─ system web view (WKWebView / WebView2) ───┐ │
│  │  the same React studio (built bundle)      │ │
│  └───────────────▲────────────────────────────┘ │
│                  │ http://127.0.0.1:<free port> │
│  ┌───────────────┴────────────────────────────┐ │
│  │ sidecar: Python backend + OCCT, frozen by  │ │
│  │ PyInstaller per OS/arch (autevra.desktop)  │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
   data: ~/Library/Application Support/Autevra  |  %APPDATA%\Autevra
```

- **One process, one origin.** `python -m autevra.desktop --static <dist>` (exists today)
  starts the backend on a free localhost port, serves the built studio and the API from
  the same origin (no CORS), stores data in the OS's per-user folder, and prints
  `AUTEVRA_READY <url>` for the shell.
- **Why Tauri over Electron:** the system web view keeps the installer small (the
  bundled Python and OCCT dominate its size either way) and the shell's Rust side is
  minimal; Electron remains the fallback if a web-view difference blocks us (WebGL
  behaviour is the one to watch).
- **Local-first.** Projects, the inventory and geometry caches live on disk (SQLite);
  the local language model is optional. The same backend can still be hosted for
  teams, so desktop and web share one code base and one data format.

Rules that keep this cheap, checked in review and by tests where possible:

1. The studio calls a relative `/api` (or a configured base URL); never a fixed host.
2. No runtime CDN: fonts, scripts and icons are bundled.
3. Files through `pathlib` and configured folders only; no POSIX-only paths, no shell
   commands, no symlinks assumed; file names safe on Windows (no `:` `?` `*` `<` `>` `|`).
4. Every dependency must have wheels or binaries for macOS arm64/x86_64 and Windows
   x86_64 (OCCT via `cadquery-ocp` does).
5. Long work runs in the backend's job queue, never in the UI thread, so a native window
   stays responsive.
6. Native features (open/save dialogs, menus, drag and drop of STEP files) go through one
   small studio adapter with a browser implementation, so the web build keeps working.
7. CI builds and tests on macOS and Windows runners before the first desktop release.

## 21. Data model

```
Organisation
├─ Project (module, owner, members, roles)
│   ├─ Branches ── command log (events) ── Baselines
│   ├─ Requirements (needs, regulation clauses, budgets) ── Verifications
│   ├─ Options, rules, Configurations, Effectivities
│   ├─ Functions ── LogicalBlocks ── Flows ── ICDs
│   ├─ Product ── Skeleton
│   │     └─ Breakdown ── PartInstance (template@version, code, maturity, inputs,
│   │                       applicability, allocation, owner) ── Joints
│   ├─ LoadCases ── interface loads
│   ├─ Safety: FailureModes, FMEA rows, FaultTrees
│   ├─ Manufacturing: MBOM ── Operations ── Stations, Resources ── InspectionPlan
│   ├─ Runs, studies, reviews, ECRs, ECOs
│   └─ Installed items (item@version, options, mates)
├─ Platforms (skeleton ranges, owned parts, derived products)
├─ Template registry ── PartTemplate (module, code pattern, contract, reference cases)
├─ Materials & processes ── Material, Allowable, Process (rules, rates)
└─ Inventory ── Item ── ItemVersion ── usage (project, configuration, installation)
```

Rules: a project belongs to exactly one module; released item versions and baselines are
immutable; geometry is never the source of truth.

## 22. Technical architecture

| Layer | Today | Target |
|---|---|---|
| Kernels | OCCT via CadQuery, NURBS, FEA, SIMP, sketch solver, lifting line, HLR drawings | + generated naming, unfolding, laminate theory and drape, routing, involute gears, multibody, cycles, hydrostatics, stack-ups, ODE system simulation, reliability (FTA) |
| Workbenches | Part Design, Shape, Structures, Drafting | section 6 |
| Modules | land vehicles (`domains/automotive`), aircraft (`aero`) | `modules/<id>` with breakdowns, templates, functions, load cases, regulation references |
| Services | per project, process-wide registries, requirements and trace | module-scoped registries; configurations, change, safety, manufacturing, inventory, job queue, access control |
| Storage | SQL + files | + event log, content-addressed geometry store, items, baselines |
| Studio | module switcher, scoped workspaces | + systems views, breakdown heat map, configuration filter, inventory, review dashboards, branches |

Rules enforced by tests (extending `tests/test_architecture.py`): kernels import no
module; modules import no other module; a project's API calls reach only its own module;
every template passes its reference cases; every analysis declares its credibility level
(estimate, concept method, checked against reference cases, validated against test data).

## 23. Delivery strategy

The catalogue is about a thousand templates; the order matters more than the count.

1. **Vertical slices.** Every milestone delivers one path end to end (requirement →
   function → part → load → analysis → MBOM → review), not one layer across everything.
2. **Breadth at L0, depth where it pays.** All products complete at L0 early; templates
   go to L2/L3 in order of mass, cost and risk share (the 20 % of parts that carry 80 %
   of mass and cost first).
3. **Templates as data where possible.** Families that differ only in dimensions and
   rules are data on a shared generator; only genuinely new geometry is new code.
4. **Reference cases first.** A template or analysis is accepted only with its closed-form
   or published reference cases passing; credibility is stated, never implied.
5. **Foundations before features.** Module registries, configurations and the systems
   layer come first (M1–M2) because retrofitting them later is the expensive mistake.

**Build, integrate or leave out.** A small team cannot write every solver; the platform
owns the model, the workflow and the glass-box methods, and integrates the rest.

| Build (our core) | Integrate (behind our interfaces) | Not doing (for now) |
|---|---|---|
| product models, breakdowns, templates, configurations, systems layer, inventory, workflow, reviews, change | geometry kernel (OCCT), meshing, explicit crash and CFD solvers (OpenRadioss, OpenFOAM class) as background jobs, FMI simulation runtimes, CAM post-processors | certification-grade solver qualification, enterprise ERP/MES, class-A surfacing parity with dedicated studio tools, plant layout and robotics offline programming |
| concept and sizing methods with reference cases (cycles, lifting line, hydrostatics, beam and plate sizing, linear FEA, SIMP) | material and emission-factor datasets (licensed by the user) | |

**Scope per milestone.** Each milestone is sized for a few weeks of focused work by a small
team: one vertical slice, its reference cases, its studio views, and its performance
targets measured. A milestone that grows beyond that is split, not stretched.

## 24. Milestones

| # | Milestone | Delivers | Proof |
|---|---|---|---|
| M0 | **Modules kept apart** (done) | module switcher; aircraft projects without a car | tests: no mixing |
| M1 | **Foundations** (mostly done, Nov 2026: product core, land and aircraft breakdowns, configurations, Breakdown workspace, AI model recorded, land tools guarded per module; the vehicle parameter and rule registries still move under `modules/land` when a second module needs the command system) | `autevra.modules.<id>`, module-keyed registries; template contract; breakdown at L0 for land vehicles and aircraft; options, rules and configurations on the breakdown; maturity heat map; AI changes marked in history (section 19) | every product complete at L0 per configuration; roll-ups match the product model |
| M2 | **Systems layer** | functions, logical blocks, typed flows, ICDs, allocation and trace checks, budgets beyond mass; design FMEA rows on functions | a braking and a pitch-control chain traced end to end |
| M3 | **Inventory, standard parts, scale base** | items, versions, interfaces, where-used; fasteners, bearings, profiles; content-addressed geometry store and job queue; performance benchmark suite in CI | install round trip; ISO 281 and bolt checks against hand calculation; section 13 targets measured |
| M4 | **Piston engines** | Mechanical module; full engine breakdown; key parts L1–L2 against firing and inertia load cases | cycle and balance checks; known engines within stated error |
| M5 | **Install across modules + behaviour** | engines in vehicles and aircraft; drive-cycle and mission simulation from installed maps | performance follows the engine version |
| M6 | **Loads, regulations, materials** | load-case libraries (road cases, V-n and gust, landing); clause references and compliance matrix; allowables database | load cases against worked textbook examples |
| M7 | **Manufacturing and quality** | sheet metal, weldments, joints, PMI and stack-ups; MBOM with reconciliation; process plan; inspection plan; L3 gate | unfold lengths vs. tables; stack-up examples; MBOM reconciliation tests |
| M8 | **Aircraft structure** | ATA 53/55/57 templates at L1–L2 against V-n loads; control surfaces; gear | beam and buckling reference cases |
| M9 | **Change, baselines, collaboration** | baselines at gates, ECR/ECO with impact, branches and merges, ownership and access control, platforms and commonality | merge-conflict and baseline-reproduction tests |
| M10 | **Marine module** | hull form, hydrostatics, GZ, Holtrop, scantlings, shaft line | hydrostatic tables against hand calculation |
| M11 | **Electric machines and gas turbines** | motor and turbine breakdowns and maps | textbook cycle examples |
| M12 | **DMU, routing, safety depth** | mechanisms, swept envelopes, harness and pipe routing, fault trees, process FMEA | mechanism, clearance and fault-tree reference cases |
| M13 | **Composites, tooling, exchange, sustainability** | plies and laminate theory, mould splits; STEP AP242 import/export with PMI, glTF, supplier interface-only items; life-cycle assessment | laminate examples; STEP round trip within tolerance; LCA of a reference product |
| D1 | **Desktop preview** (alongside any milestone) | Tauri shell + PyInstaller sidecar, macOS and Windows installers, native file dialogs, CI on both | installers open, build a car and an aircraft, and save to the user data folder on both systems |
| M14 | **Lifecycle, test correlation, security** | as-built and as-maintained views per serial, life-limited parts, digital-twin life update; test import and correlation; classification labels and export-control access rules | correlation reports on a reference test; access-rule tests on every export path |

Each milestone ends green (tests, lint, live check in the studio) and is committed
locally; pushes happen at milestone boundaries.
