# Autevra feature test-case catalogue

**10,000 test cases** across 40 capability areas, mapping the workbench families of CATIA-class CAD/CAE/PLM suites onto Autevra. Each case either checks something Autevra already does (status **Have** or **Partial**) or specifies a feature still to build (status **Gap**), so the catalogue doubles as a backlog: build the feature, then make its cases pass.

Named products are examples of a category. The catalogue describes capability families, not claims about any vendor's product, and Autevra is not affiliated with any of them.

## Files

| File | Use |
|---|---|
| [`areas/`](areas/) | One readable Markdown file per area, grouped by feature |
| [`AUTEVRA_TEST_CASES.csv`](AUTEVRA_TEST_CASES.csv) | Every case on one row; open in Excel, Numbers or a test-management import |
| `AUTEVRA_TEST_CASES.xlsx` | Same data with a summary sheet and filters (written when `openpyxl` is available) |
| [`generate_catalogue.py`](generate_catalogue.py) | Regenerates every file: `python3 docs/test-cases/generate_catalogue.py` |

## How to read a case

| Column | Meaning |
|---|---|
| ID | `<AREA>-<nnnn>`, stable while the generator is unchanged |
| Type | Functional, Accuracy (closed-form number to match), Boundary, Negative, Regression, Interop, Performance, Usability, Security |
| Priority | P1 core path, P2 normal, P3 edge |
| Autevra status | Have = implemented and tested; Partial = working subset; Gap = to build. Initial estimate from the code and docs/INDUSTRY_FEATURES.md, by feature, so check a case before relying on it |
| Automation | pytest (backend), vitest (frontend), benchmark (timed), manual |
| Expected | Accuracy cases carry the computed value; use the stated tolerance (default 1e-6 relative for exact geometry, ±5% for FEA) |

## Totals

| Status | Cases |
|---|---|
| Have | 5,478 |
| Partial | 1,723 |
| Gap | 2,799 |

| Type | Cases |
|---|---|
| Accuracy | 4,991 |
| Functional | 2,791 |
| Regression | 724 |
| Negative | 613 |
| Interop | 376 |
| Boundary | 256 |
| Performance | 115 |
| Usability | 110 |
| Security | 24 |

| Priority | Cases |
|---|---|
| P1 | 1,341 |
| P2 | 8,646 |
| P3 | 13 |

| Automation | Cases |
|---|---|
| pytest | 9,191 |
| vitest | 592 |
| manual | 170 |
| benchmark | 47 |

## Areas

| # | Area | CATIA-class equivalent | Autevra workspace | Scope | Cases | Have | Partial | Gap |
|---|---|---|---|---|---|---|---|---|
| 1 | [SKT Sketcher](areas/01-SKT-sketcher.md) | Sketcher | Part Design → Sketcher; /sketch/solve | Shared | 319 | 0 | 244 | 75 |
| 2 | [PRT Part Design](areas/02-PRT-part-design.md) | Part Design | Part Design | Shared | 366 | 127 | 119 | 120 |
| 3 | [GSD Generative Shape Design](areas/03-GSD-generative-shape-design.md) | Generative Shape Design (GSD) / wireframe and surfaces | Surfaces; Styling | Shared | 156 | 45 | 111 | 0 |
| 4 | [CLA NURBS and Class-A analysis](areas/04-CLA-nurbs-and-class-a-analysis.md) | FreeStyle / Imagine & Shape / ICEM-style Class-A | Surfaces (NURBS lab); Styling | Shared | 249 | 126 | 123 | 0 |
| 5 | [ASM Assembly Design](areas/05-ASM-assembly-design.md) | Assembly Design / Product Structure | Assembly; Inventory; Breakdown | Shared | 216 | 82 | 134 | 0 |
| 6 | [DMU DMU Space Analysis and Kinematics](areas/06-DMU-dmu-space-analysis-and-kinematics.md) | DMU Space Analysis / DMU Kinematics / Fitting | Assembly; Production (mechanisms) | Shared | 134 | 21 | 51 | 62 |
| 7 | [DRW Drafting and GD&T](areas/07-DRW-drafting-and-gd-t.md) | Generative Drafting / Functional Tolerancing & Annotation (FT&A) | Part Design → drawing.svg | Shared | 319 | 31 | 1 | 287 |
| 8 | [TOL Tolerance analysis](areas/08-TOL-tolerance-analysis.md) | 3D tolerance stack-up (e.g. 3DCS-class add-ons) | Production → stack-ups | Shared | 712 | 668 | 12 | 32 |
| 9 | [SMD Sheet Metal Design](areas/09-SMD-sheet-metal-design.md) | Generative Sheetmetal Design | Part Design (SheetMetal feature) | Shared | 275 | 135 | 60 | 80 |
| 10 | [CMP Composites Design](areas/10-CMP-composites-design.md) | Composites Design / Composites Engineering | Loads → materials; /composites/laminate | Shared | 129 | 74 | 0 | 55 |
| 11 | [MLD Mold and Tooling](areas/11-MLD-mold-and-tooling.md) | Core & Cavity Design / Mold Tooling Design | Production → tooling check | Shared | 104 | 36 | 0 | 68 |
| 12 | [ELE Electrical harness](areas/12-ELE-electrical-harness.md) | Electrical Harness Design / Wire Harness Flattening | Routing | Shared | 262 | 192 | 28 | 42 |
| 13 | [PIP Piping and tubing](areas/13-PIP-piping-and-tubing.md) | Piping & Tubing Design / Fluid Systems | Routing | Shared | 131 | 75 | 24 | 32 |
| 14 | [FEA Structural analysis (FEA)](areas/14-FEA-structural-analysis-fea.md) | Generative Structural Analysis (GPS/GAS) / SIMULIA | Structures; /structures/run | Shared | 281 | 182 | 45 | 54 |
| 15 | [OPT Optimisation and topology](areas/15-OPT-optimisation-and-topology.md) | Product Engineering Optimizer / Tosca-class topology | Structures → topology; Optimization | Shared | 137 | 87 | 0 | 50 |
| 16 | [KBE Knowledgeware](areas/16-KBE-knowledgeware.md) | Knowledge Advisor / Knowledge Expert / Product Knowledge Template | Design parameters; Part Design expressions; design tables | Shared | 164 | 120 | 0 | 44 |
| 17 | [MAS Materials and mass properties](areas/17-MAS-materials-and-mass-properties.md) | Materials library / Measure Inertia / Weight Engineering | Breakdown (mass roll-up); Loads (materials) | Shared | 108 | 100 | 0 | 8 |
| 18 | [IOX Data exchange](areas/18-IOX-data-exchange.md) | STEP/IGES interfaces, 3D XML, CATIA V5↔V6 migration | Manufacturing (exports); /import-step | Shared | 390 | 50 | 39 | 301 |
| 19 | [VIZ Visualisation and rendering](areas/19-VIZ-visualisation-and-rendering.md) | Real Time Rendering / Photo Studio / 3DEXCITE | Viewport (all workspaces) | Shared | 155 | 84 | 9 | 62 |
| 20 | [PLM PLM, lifecycle and change](areas/20-PLM-plm-lifecycle-and-change.md) | ENOVIA / 3DEXPERIENCE collaboration | Reviews; Digital thread; Breakdown | Shared | 208 | 36 | 12 | 160 |
| 21 | [SYS Requirements and systems engineering](areas/21-SYS-requirements-and-systems-engineering.md) | Requirements / RFLP (CATIA Systems) / Magic-class MBSE | Requirements; Functions; Systems | Shared | 154 | 146 | 0 | 8 |
| 22 | [MFG Manufacturing engineering and CAM](areas/22-MFG-manufacturing-engineering-and-cam.md) | DELMIA process planning / Prismatic Machining / NC | Production; Manufacturing | Shared | 364 | 248 | 0 | 116 |
| 23 | [ERG Human ergonomics](areas/23-ERG-human-ergonomics.md) | Human Builder / Human Posture Analysis (RAMSIS/Jack-class) | Package | Land | 82 | 6 | 0 | 76 |
| 24 | [VEH Land vehicles](areas/24-VEH-land-vehicles.md) | Automotive extensions (Body-in-White, Styling, Vehicle Dynamics) | Design; Styling; Package; Simulation; Loads | Land | 296 | 251 | 5 | 40 |
| 25 | [AIR Aircraft](areas/25-AIR-aircraft.md) | Aerospace extensions (aircraft conceptual design, wing design, structures) | Aircraft; Loads | Air | 303 | 267 | 6 | 30 |
| 26 | [MAR Marine](areas/26-MAR-marine.md) | Ship design extensions (hull form, hydrostatics, structure) | Vessel; Loads | Marine | 188 | 164 | 0 | 24 |
| 27 | [MEC Mechanical: engines and machines](areas/27-MEC-mechanical-engines-and-machines.md) | Machine design extensions (engines, drives, bearings) | Engine; Inventory | Mechanical | 268 | 228 | 8 | 32 |
| 28 | [AI AI and natural language](areas/28-AI-ai-and-natural-language.md) | (No CATIA equivalent: Autevra differentiator) / CATIA Assistant-class | AI engineering; command bar | Shared | 709 | 650 | 0 | 59 |
| 29 | [API API, scripting and extensibility](areas/29-API-api-scripting-and-extensibility.md) | CAA / VBA / EKL automation | REST API; plugins | Shared | 503 | 479 | 0 | 24 |
| 30 | [PLT Platform, UX and non-functional](areas/30-PLT-platform-ux-and-non-functional.md) | V5/3DEXPERIENCE platform behaviour | Studio shell; desktop app | Shared | 220 | 54 | 56 | 110 |
| 31 | [JNT Fasteners, welds and fatigue](areas/31-JNT-fasteners-welds-and-fatigue.md) | Fastener / Weld Design / joint analysis add-ons | Inventory (ISO fasteners); Structures | Shared | 284 | 0 | 90 | 194 |
| 32 | [CFD Flow and thermal](areas/32-CFD-flow-and-thermal.md) | Fluid / thermal add-ons (STAR-CCM+/Fluent-class, SIMULIA Flow) | Simulation; Aircraft; Loads | Shared | 278 | 0 | 140 | 138 |
| 33 | [NRG Electrified powertrain and energy](areas/33-NRG-electrified-powertrain-and-energy.md) | Systems / Dymola-class 1D energy modelling | Design (powertrain); Simulation | Land | 205 | 27 | 168 | 10 |
| 34 | [ELM Springs, gears and sections](areas/34-ELM-springs-gears-and-sections.md) | Machine Design / structural section libraries | Inventory; Structures | Shared | 336 | 128 | 96 | 112 |
| 35 | [CRS Crash and occupant safety](areas/35-CRS-crash-and-occupant-safety.md) | Crash / safety add-ons (explicit FE, occupant models) | Loads; Simulation | Land | 128 | 0 | 0 | 128 |
| 36 | [REV Reverse engineering and scan data](areas/36-REV-reverse-engineering-and-scan-data.md) | Digitized Shape Editor / Quick Surface Reconstruction | Part Design (imports); Styling (reference) | Shared | 114 | 0 | 0 | 114 |
| 37 | [LCA Sustainability and cost](areas/37-LCA-sustainability-and-cost.md) | Sustainable design / cost estimation add-ons | Production (cost, CO2); /lca | Shared | 104 | 80 | 0 | 24 |
| 38 | [QAL Quality and inspection](areas/38-QAL-quality-and-inspection.md) | Quality / CMM inspection planning add-ons | Production → quality | Shared | 92 | 0 | 64 | 28 |
| 39 | [VDY Vehicle dynamics checks](areas/39-VDY-vehicle-dynamics-checks.md) | Vehicle dynamics add-ons (CarSim/Adams Car-class) | Simulation; Loads | Land | 107 | 29 | 78 | 0 |
| 40 | [SMK Smoke tests by module, template and workspace](areas/40-SMK-smoke-tests-by-module-template-and-workspace.md) | (release gate) | All workspaces | Shared | 450 | 450 | 0 | 0 |

## Largest gaps (features to build, by case count)

| Area | Feature | Status | Cases |
|---|---|---|---|
| IOX | Export | Gap | 172 |
| NRG | Road load and consumption | Partial | 144 |
| CFD | Drag force and power | Partial | 140 |
| JNT | Fatigue (modified Goodman) | Gap | 128 |
| SKT | Geometric and dimensional constraints | Partial | 126 |
| PRT | Hole wizard (ISO metric) | Gap | 120 |
| PLM | Access control | Gap | 112 |
| ELM | Spur gear geometry | Gap | 112 |
| IOX | Import | Gap | 105 |
| DRW | Views | Gap | 104 |
| ELM | Helical compression springs | Partial | 96 |
| JNT | Bolt preload and torque | Partial | 90 |
| REV | Point clouds and meshes | Gap | 90 |
| ASM | Assembly constraints | Partial | 80 |
| SMD | Sheet-metal features | Gap | 80 |
| CRS | Crush space and deceleration | Gap | 80 |
| SKT | Sketch operations | Gap | 75 |
| CLA | Shape analysis | Partial | 72 |
| DRW | Dimensions | Gap | 71 |
| PRT | Pad / Pocket | Partial | 66 |
| PLT | Desktop app (Tauri + Python sidecar) | Gap | 66 |
| JNT | Fillet welds | Gap | 66 |
| QAL | Process capability | Partial | 64 |
| GSD | Surface creation | Partial | 60 |
| SMD | Manufacturability rules | Partial | 60 |
| MFG | NC operations | Gap | 60 |
| ERG | Manikins and posture | Gap | 60 |
| CFD | Heat transfer | Gap | 57 |
| DRW | Geometric tolerances (ISO 1101) | Gap | 56 |
| CFD | CFD workflow | Gap | 56 |
| ASM | Product structure | Partial | 54 |
| VDY | Lateral load transfer | Partial | 54 |
| GSD | Wireframe | Partial | 51 |
| CLA | Knot insertion and degree elevation | Partial | 51 |
| SKT | Profile validation | Partial | 48 |
| CRS | Crash workflow | Gap | 48 |
| FEA | Mesh, solver and results | Partial | 45 |
| PRT | Feature tree management | Partial | 42 |
| ELE | Harness design | Gap | 42 |
| DMU | Mechanisms | Gap | 40 |

## Using it

1. Pick a Gap feature, read its cases, build the feature until they pass.
2. Turn Accuracy cases into parametrised pytest tests: the expected numbers are already computed.
3. When a feature lands, change its status in `generate_catalogue.py` (`C.feat(..., "Have")`) and regenerate.
4. Add cases by editing the area function; IDs renumber within the area, so cite IDs together with the title.

Generated 10,232 candidate cases, trimmed evenly to 10,000 (P1 cases kept first).
