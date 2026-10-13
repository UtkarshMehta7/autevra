# Research: resources, options and possibilities

This document surveys the building blocks available for Autevra, compares
the realistic options in each area, and records a recommendation for each.
Every recommendation is judged against the project constraints:

- **Local-first**: no hosted AI inference; runs on a Mac M2 with 8 GB RAM and 256 GB SSD.
- **Real engineering**: editable B-rep CAD and deterministic, validated calculations rather than pictures.
- **Incremental**: each choice must allow a small working version first.
- **Cloud-ready later**: Docker → AWS ECR/ECS, PostgreSQL, S3, async workers.

Platform verification results (which packages actually install on Apple
Silicon) are in [ENVIRONMENT.md](ENVIRONMENT.md).

---

## 1. CAD kernel and parametric modelling

| Option | What it is | Licence | Strengths | Weaknesses | Fit |
|---|---|---|---|---|---|
| **Open CASCADE Technology (OCCT)** | Industrial B-rep kernel in C++ | LGPL-2.1 + exception | Real solids, booleans, fillets, STEP/IGES, tessellation, distance queries | Low-level API, verbose | Foundation |
| **CadQuery 2.8** (on OCCT via OCP) | Python parametric CAD library | Apache-2.0 | Concise fluent API, sketches, lofts, assemblies, STEP/STL/glTF export, large community | 1.7 GB full install, pins OCP < 8 | **Recommended for Phase 1** |
| **build123d** (on OCCT via OCP) | Newer Python CAD API | Apache-2.0 | Cleaner, more Pythonic, algebra mode, good typing | Smaller ecosystem, API still evolving | Strong alternative; easy switch since same kernel |
| **OCP** directly | Python bindings to OCCT | Apache-2.0 bindings | Full kernel access | Verbose | Use for advanced operations CadQuery lacks (e.g. `BRepExtrema_DistShapeShape`) |
| FreeCAD (as library) | Full CAD application | LGPL-2.1 | Sketcher constraint solver, FEM workbench | Heavy, GUI-centric, hard to embed headless | Not for core |
| OpenSCAD | CSG scripting | GPL-2.0 | Simple | Mesh output, **no B-rep, no STEP** | Rejected |
| Manifold (`manifold3d`) | Fast mesh booleans | Apache-2.0 | Very fast, robust | Mesh only | Useful for quick previews or collision proxies, not as source of truth |
| opencascade.js | OCCT compiled to WebAssembly | LGPL-2.1 | CAD in the browser | Large WASM download, memory-heavy in browser | Later, optional client-side viewing |
| truck (Rust) | Rust B-rep kernel | Apache-2.0 | Modern | Immature | Watch only |

**Recommendation.** Use CadQuery on OCCT as the geometry engine, wrapped by
an Autevra-owned adapter (`cad/kernel.py`) so build123d or raw OCP can
replace it without touching the rest of the system. The source of truth is
**not** the mesh and not even the B-rep: it is the **parameter set plus the
feature/command history**. Geometry is always regenerated from that.

**Exchange formats.** STEP AP214/AP242 for engineering exchange (editable
in FreeCAD, Fusion, SolidWorks, CATIA); glTF/GLB for the web viewer; STL for
3D printing; DXF/SVG 2D drawings (CadQuery + `ezdxf`) later.

**Key CAD techniques we will need**
- Parametric component builders: pure functions `parameters -> solid`.
- Named coordinate frames ("interfaces") on each component for assembly mates.
- Tessellation with tolerance control for the viewport; per-face triangulation keeps sharp edges crisp.
- Shape-to-shape minimum distance (`BRepExtrema_DistShapeShape`) for clearance checks.
- Swept envelopes (e.g. front wheel at several steer angles) for packaging checks.
- Mass properties (volume, centre of mass, inertia) from B-rep → feed simulation.
- Caching geometry by a hash of the parameters each component depends on, so only affected parts are rebuilt.

---

## 2. Local AI for automotive intent understanding

### 2.1 Runtimes

| Runtime | Licence | Apple Silicon | Structured output | Notes | Fit |
|---|---|---|---|---|---|
| **Ollama** | MIT | Native, Metal GPU | JSON-schema `format` parameter | One-command model download, separate process with HTTP API, wraps llama.cpp | **Recommended default** |
| **llama.cpp `llama-server`** | MIT | Native, Metal (`brew install llama.cpp`) | GBNF grammars + JSON schema | Same engine, more control, OpenAI-compatible API | **Supported alternative** |
| llama-cpp-python | MIT | Needs compile | Grammars | In-process; model memory shares the backend's address space | Avoid on 8 GB |
| MLX / mlx-lm | MIT | Apple-only, fastest on M-series | via Outlines | Great for **LoRA fine-tuning** on the Mac | Use for fine-tuning experiments |
| LM Studio | Proprietary freeware | Native | JSON schema | GUI app, handy for model trials | Developer convenience only |

**Why a separate model process (Ollama or llama-server) rather than in-process:**
it keeps 1–2.5 GB of model weights out of the CAD backend, can be stopped
when not needed, is GPU-accelerated on the Mac while containers are not,
and is a stable HTTP contract that also works on a Linux server later.

### 2.2 Candidate small models (quantised Q4_K_M sizes are approximate)

| Model family | Sizes worth testing | Approx. RAM (Q4) | Licence | Notes |
|---|---|---|---|---|
| Qwen2.5-Instruct | 0.5B, 1.5B, 3B | 0.4 / 1.0 / 2.0 GB | Apache-2.0 (3B: Qwen research licence) | Strong JSON and tool-call behaviour for size |
| Qwen3 | 0.6B, 1.7B, 4B | 0.5 / 1.2 / 2.6 GB | Apache-2.0 | Has a "thinking" mode; disable for latency |
| Llama 3.2 Instruct | 1B, 3B | 0.8 / 2.0 GB | Llama community licence | Good general instruction following |
| Phi-3.5-mini / Phi-4-mini | 3.8B | ~2.4 GB | MIT | Good reasoning for size |
| Gemma 3 | 1B, 4B | 0.8 / 2.6 GB | Gemma terms | Good multilingual |
| SmolLM2 | 360M, 1.7B | 0.3 / 1.1 GB | Apache-2.0 | Very small, weaker reasoning |

Newer small models appear often. The choice will be made by an **evaluation
harness** (instruction → expected command JSON, scored automatically), not
by reputation. Start with a ~1.5B model and move up only if the scores
justify the memory.

### 2.3 How the AI is used safely

The LLM never executes code and never touches geometry. It only **translates
language into a typed command proposal** that the deterministic system then
validates:

```
user text
  → deterministic automotive parser (regex/grammar + automotive lexicon + units)
      ├─ confident? → typed Command
      └─ not confident → local LLM with JSON-schema-constrained output → typed Command proposal
  → validation (parameter exists, unit conversion, min/max, cross-parameter rules)
  → user confirmation for LLM-derived proposals
  → command executor (records history, enables undo/redo)
  → CAD rebuild of only the affected components
```

Techniques and resources:
- **Constrained decoding**: Ollama `format` (JSON schema), llama.cpp GBNF grammars, Outlines, XGrammar. These guarantee syntactically valid output.
- **Schema from the registry**: the allowed parameter IDs, units and ranges come from the vehicle parameter registry, so the model cannot invent parameters.
- **Few-shot prompts** with automotive examples, temperature 0 for determinism.
- **Retrieval (RAG)** for engineering knowledge later: small local embedding model (e.g. `nomic-embed-text`, `bge-small`), stored in `sqlite-vec` now and `pgvector` later.
- **Fine-tuning (optional, later)**: LoRA with `mlx-lm` on the Mac using a synthetic dataset generated from the parameter registry (thousands of phrasings → command JSON). This is how the model becomes "automotive-specialised" without a big model.
- **Evaluation set**: a versioned file of instructions with expected commands, including tricky ones ("lower the car", "make it longer", "17s to 18s", "track", unit mix-ups). Every model or prompt change must keep or improve the score.

### 2.4 Intelligent specification interview

| Approach | Description | Fit |
|---|---|---|
| **Rule-driven question graph** | Questions are nodes with conditions ("if drivetrain = AWD ask torque split"). Answers fill a typed `VehicleSpec`. | **Core**: deterministic and testable |
| **Constraint/conflict checker** | Rules over the spec ("0–100 km/h in 4 s with 80 kW and 2,000 kg is not physically plausible" via power-to-weight and traction limits) | **Core** |
| LLM phrasing layer | The LLM rewords questions and extracts answers from free text into the typed spec | Optional, on top |
| Constraint solvers (OR-Tools CP-SAT, `python-constraint`) | Find feasible parameter combinations or explain infeasibility | Later, for "suggest a fix" |

Specification domains to cover: vehicle class (hatchback, sedan, SUV,
pickup, sports car, LCV), intended use, seating, dimensions, mass target,
powertrain (ICE / hybrid / BEV), engine layout and displacement, power,
torque, transmission, drivetrain (FWD/RWD/AWD), top speed and acceleration
targets, range or fuel economy, suspension type, brakes, tyres, materials,
budget and production volume, regulatory market.

---

## 3. Vehicle assembly, constraints and integration

| Need | Options | Recommendation |
|---|---|---|
| Component placement | CadQuery `Assembly` constraints (uses casadi solver); custom mate graph | Own lightweight **mate graph** (parent interface frame ↔ child interface frame), exported to `cq.Assembly` for STEP. Deterministic and easy to explain. |
| Dependency tracking | Hand-written maps; general DAG library (`networkx`) | Parameter → component dependency declared by each builder; a small DAG computes "affected components" for every command. |
| Clearance / interference | OCCT `BRepExtrema_DistShapeShape`; BVH mesh distance (`trimesh`, `three-mesh-bvh`) | OCCT exact distance on simplified envelopes (tyre as cylinder) for accuracy; mesh BVH for interactive previews. |
| Kinematic envelopes | Sample positions (steer angles, suspension travel) and union the shapes | Start with discrete sampling; document the sampling resolution. |
| Mass properties | OCCT `GProp` with density per material | Use for weight estimates, centre of gravity, inertia → simulation inputs. |

Vehicle coordinate convention: **ISO 8855** (X forward, Y left, Z up, mm),
origin on the ground below the front axle centre.

---

## 4. Engineering simulation

### 4.1 Vehicle dynamics and multibody

| Option | Licence | Install on Mac | What it offers | Fit |
|---|---|---|---|---|
| **Custom validated models (NumPy/SciPy)** | ours | pip | Point-mass longitudinal, quarter-car, linear/non-linear bicycle model, Pacejka tyre, powertrain maps | **First**: fast, transparent, testable against closed-form results |
| **Project Chrono / Chrono::Vehicle** | BSD-3 | conda `projectchrono` (osx-arm64 9.0.1) | Full multibody vehicles: double wishbone, MacPherson, multilink, solid axle; Pacejka, TMeasy, Fiala tyres; powertrain, driveline; deformable terrain; FEA module | **Recommended high-fidelity engine**, run as a separate conda worker |
| MuJoCo | Apache-2.0 | pip wheels | Fast general rigid-body physics | Possible, not vehicle-specific |
| PyBullet | zlib | pip | Simple rigid body + vehicle raycast | Toy-level for vehicle dynamics |
| OpenModelica + Modelica libraries | OSMC-PL / GPL | installer | Equation-based models (powertrain, thermal, electrical); FMU export | Good for powertrain/thermal later via FMI (`fmpy`) |
| CommonRoad vehicle models | BSD-3 | pip | Published kinematic/single-track/multi-body reference models | **Reference/validation source** |

**Validation references for the custom models** (closed-form or textbook):

| Scenario | Model | Reference check |
|---|---|---|
| Emergency braking 100 → 0 km/h | Point mass with friction, load transfer | Stopping distance `v²/(2μg)` = 39.3 m at μ = 1.0, plus reaction/build-up time |
| Acceleration 0–100 km/h | Longitudinal model with power/traction limit, aero and rolling drag, gear shifts | Traction-limited bound `t ≥ v/(μg·weight fraction on driven axle)`; constant-power analytical solution |
| Steady-state cornering | Linear bicycle model | Understeer gradient, yaw-rate gain, critical/characteristic speed (Gillespie, Milliken) |
| Step steer / lane change | Bicycle model with Pacejka tyres | ISO 7401 metrics; ISO 3888 double-lane-change course |
| Suspension, shock absorber | Quarter-car 2-DOF | Analytical natural frequencies (body ~1–1.5 Hz, wheel hop ~10–12 Hz), damping ratio |
| Potholes / uneven roads | Quarter-car or half-car with road input | ISO 8608 road classes A–H (PSD), half-sine pothole/bump |
| Engine performance | Torque map + gear ratios + final drive | Power = torque × ω check; wheel force vs traction limit |
| Tyre forces | Pacejka Magic Formula | Published coefficient sets; curve shape checks |

### 4.2 Structural, thermal, fatigue, aerodynamics, crash

| Domain | Lightweight first step | Open-source high-fidelity option | Licence | Mac notes |
|---|---|---|---|---|
| Meshing | — | **gmsh** (pip wheels), Netgen | GPL / LGPL | gmsh ✅ arm64 wheel |
| Structural (static, modal) | Beam/frame models (`openseespy`), hand calcs for rails | **CalculiX**, **FEniCSx**, scikit-fem, Code_Aster, Elmer | GPL / LGPL / BSD / GPL / GPL | scikit-fem ✅ pip; FEniCSx via conda; CalculiX via Homebrew/conda; Code_Aster via Docker |
| Thermal | Lumped thermal network (brake disc temperature rise, cooling) | Elmer, FEniCSx | GPL / LGPL | — |
| Fatigue | Rainflow counting (`rainflow`), S-N curves (Basquin), Miner's rule, FKM guideline | — | MIT | ✅ |
| Aerodynamics | Drag `F = ½ρ·Cd·A·v²` with Cd estimate and frontal area from CAD | **OpenFOAM**, SU2; lattice-Boltzmann (e.g. XLB) | GPL / LGPL / Apache | OpenFOAM heavy: Docker or cloud; coarse meshes only on 8 GB |
| Crash | Lumped mass-spring (Kamal) frontal model, energy and pulse checks | **OpenRadioss** | AGPL-3.0 | Docker or cloud; long runtimes |

**Aerodynamic validation references:** Ahmed body (classic bluff body with
published drag vs slant angle), DrivAer (TU Munich open realistic car
geometry with wind-tunnel data).

**Licensing note (not legal advice):** GPL/AGPL solvers should run as
**separate executables** that Autevra calls with input files, never linked
into Autevra's code. This keeps licence options open if Autevra is ever
commercialised. AGPL (OpenRadioss) needs particular care when offered as a
network service.

### 4.3 Honesty about fidelity

Every simulation result will carry a **fidelity label**:

| Label | Meaning |
|---|---|
| `estimate` | Simplified model, verified against analytical results, not correlated to test data |
| `verified` | Model code verified against closed-form solutions and reference implementations |
| `validated` | Correlated against physical test data for a comparable vehicle (requires real data) |

No result is presented as `validated` without real reference data.

---

## 5. Simulation automation from natural language

Possible pipeline:

1. User: "Run an emergency stop from 100 km/h on wet asphalt and check it stops within 45 m."
2. The parser/LLM maps this to a typed `ScenarioSpec` (scenario = `braking`, v0 = 100 km/h, μ = wet asphalt preset 0.5–0.7, requirement = distance ≤ 45 m).
3. Validation of the scenario against the scenario schema and vehicle state.
4. A job is queued (sequential worker on the Mac) and runs the right solver (custom model, Chrono later).
5. Telemetry is stored (Parquet or SQLite now, S3 later) and streamed to the UI.
6. Results are compared with requirements → pass/fail with margins.
7. A rule-based advisor suggests changes ("increase front brake disc diameter", "use higher-μ tyre compound", "shift weight rearward") and can turn them into CAD commands for the user to approve.

Scenario standards to model progressively: ISO 21994 (stopping distance
with ABS), ISO 4138 (steady-state circular driving), ISO 3888-1/-2 (lane
change), ISO 7401 (transient response), ISO 8608 (road profiles), WLTP
drive cycle (energy/fuel).

---

## 6. 3D workspace (frontend)

| Area | Options | Recommendation |
|---|---|---|
| Framework | React + TypeScript, Vue, Svelte | **React + TypeScript** (as specified) |
| Build | Vite, Next.js | **Vite**: fast, no server rendering needed |
| 3D | plain three.js, react-three-fiber + drei, Babylon.js | **three.js**, with react-three-fiber optional. Plain three.js has fewer dependencies; R3F is more ergonomic for complex scenes. |
| Picking / BVH | `three-mesh-bvh` | for large assemblies |
| Telemetry plots | uPlot (fast time series), ECharts, Plotly | **uPlot** for live telemetry, ECharts for reports |
| Layout | CSS grid, `react-resizable-panels`, dockview | start with CSS grid, add resizable panels later |
| State | React state, Zustand, Redux Toolkit | **Zustand** when state grows (small, simple) |
| Geometry transfer | JSON triangle arrays, glTF/GLB, Draco compression | JSON first, GLB once assemblies grow; geometry de-duplicated by content hash (four wheels share one mesh) |
| In-browser STEP | `occt-import-js` | optional STEP viewer |
| UI testing | Playwright, Vitest | both |

Workspace panels: vehicle viewport, component tree, property editor,
AI instruction/chat panel, specification interview forms, command history
with undo/redo, clearance/validation results, simulation controls,
telemetry charts, engineering report view.

---

## 7. Backend, data and deployment

| Area | Phase-1 choice | Later (cloud) |
|---|---|---|
| API | FastAPI + Pydantic v2 + Uvicorn | same, behind an ALB on ECS |
| Database | SQLite via SQLAlchemy 2.0 | PostgreSQL (RDS) via the same SQLAlchemy models; **Alembic** migrations from day one |
| File storage | local `data/` directory behind a storage interface | S3 (same interface) |
| Jobs | in-process **sequential** queue (one simulation at a time) | Redis + RQ/Arq, or SQS + ECS worker tasks |
| Containers | Docker Compose (backend `linux/amd64`, frontend nginx) | ECR images, ECS Fargate services; Graviton arm64 once CAD wheels allow |
| CI | GitHub Actions: lint, tests, build | + image build & push to ECR |
| Observability | structured logging | CloudWatch, OpenTelemetry |

---

## 8. Product possibilities (beyond the core vision)

Ideas that the architecture should not block, ranked roughly by value and feasibility:

1. **Design variants and comparison**: branch a design, change parameters, compare geometry, mass and simulation results side by side.
2. **Design-of-experiments and optimisation**: sweep wheelbase/track/spring rates, find Pareto fronts (SciPy, Optuna, `pymoo`).
3. **Mass and cost estimation**: material densities × volumes; simple cost models per material and process.
4. **Bill of materials and STEP/2D drawing export**: hand-off to manufacturing or other CAD tools.
5. **Requirement traceability**: each requirement links to the parameters, components and tests that satisfy it.
6. **Regulation and packaging checks**: ground clearance, approach/departure angles, turning circle, overhang limits, visibility zones.
7. **Component library**: standard parts (bearings, fasteners, tyres by ETRTO size) with real dimensions.
8. **EV-specific modules**: battery pack packaging, motor/inverter placement, range estimation on WLTP.
9. **Motorsport / Formula Student mode**: FSAE-style rules checks, lap-time simulation (point-mass lap sim).
10. **Education mode**: explain each calculation step and equation; useful for students and training.
11. **Collaboration**: share designs, comments on components, review workflows (needs the cloud phase).
12. **Plugin system**: third-party component builders and simulation scenarios behind the same validated command interface.

---

## 9. Learning and reference resources

**CAD and geometry**
- Open CASCADE Technology documentation: https://dev.opencascade.org/doc/overview/html/
- CadQuery documentation: https://cadquery.readthedocs.io/
- build123d documentation: https://build123d.readthedocs.io/
- OCP bindings: https://github.com/CadQuery/OCP

**Local AI**
- Ollama: https://ollama.com and API docs at https://github.com/ollama/ollama/blob/main/docs/api.md
- llama.cpp: https://github.com/ggml-org/llama.cpp (grammars: `grammars/README.md`)
- MLX and mlx-lm (LoRA fine-tuning): https://github.com/ml-explore/mlx, https://github.com/ml-explore/mlx-lm
- Outlines (structured generation): https://github.com/dottxt-ai/outlines

**Simulation**
- Project Chrono and Chrono::Vehicle: https://projectchrono.org, https://api.projectchrono.org/manual_vehicle.html
- PyChrono install (conda): https://api.projectchrono.org/pychrono_installation.html
- CommonRoad vehicle models: https://gitlab.lrz.de/tum-cps/commonroad-vehicle-models
- gmsh: https://gmsh.info; CalculiX: http://www.calculix.de; FEniCSx: https://fenicsproject.org
- OpenFOAM: https://www.openfoam.com; OpenRadioss: https://openradioss.org
- DrivAer model: https://www.epc.ed.tum.de/en/aer/research-groups/automotive/drivaer/

**Books (vehicle engineering)**
- T. Gillespie, *Fundamentals of Vehicle Dynamics*
- W. Milliken & D. Milliken, *Race Car Vehicle Dynamics*
- H. Pacejka, *Tire and Vehicle Dynamics*
- B. Heißing & M. Ersoy, *Chassis Handbook*
- G. Genta & L. Morello, *The Automotive Chassis*
- R. Stone & J. Ball, *Automotive Engineering Fundamentals*
- J. Heywood, *Internal Combustion Engine Fundamentals*

**Standards (paid, cite by number)**: ISO 8855 (vehicle axes), ISO 21994,
ISO 4138, ISO 3888, ISO 7401, ISO 8608, ETRTO tyre standards, UN ECE
regulations, FMVSS.

**Public data useful for validation**
- US EPA Test Car List data (test weights, road-load coefficients A/B/C): https://www.epa.gov/compliance-and-fuel-economy-data/data-cars-used-testing-fuel-economy
- Published manufacturer specifications (dimensions, power, 0–100 times) for sanity checks.
