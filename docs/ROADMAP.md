# Roadmap and progress record

Each phase ends with a **working, tested application** and an updated
"Progress log" entry at the bottom of this file. A phase starts only when
the phases it depends on are complete.

Legend: `[x]` done, `[ ]` to do.

---

## Phase 0: Discovery and planning ✅

- [x] Inspect the repository (empty) and the development environment
- [x] Verify Apple Silicon availability of the key packages (CAD, local AI, simulation, frontend)
- [x] Identify compatibility risks and mitigations ([ENVIRONMENT.md](ENVIRONMENT.md))
- [x] Survey resources, options and product possibilities ([RESEARCH.md](RESEARCH.md))
- [x] Propose architecture and repository layout ([ARCHITECTURE.md](ARCHITECTURE.md))
- [x] Write this phased plan
- [x] Repository hygiene: README, `.gitignore`, `.gitattributes`, `.editorconfig`, issue/PR templates, contributing guide

## Phase 1: Foundation prototype (smallest working version)

Goal: change a **real** CAD parameter of a simple vehicle through natural language.

- [ ] Mac smoke test: `uv` + Python 3.12 + `cadquery==2.8.0` imports and exports a STEP file
- [ ] Backend skeleton: FastAPI app, config, health endpoint, pytest, ruff
- [ ] Domain: units, parameter registry, derived values, cross-parameter rules
- [ ] Command system: typed commands, validation, history, undo/redo
- [ ] CAD: kernel adapter; builders for body (with wheel arches and cabin), ladder frame, axles, wheels (tyre + rim)
- [ ] Assembly: interfaces + mates, dependency graph, rebuild only affected components (cache by parameter hash)
- [ ] Deterministic intent parser (automotive lexicon + units) for set/increase/decrease/scale, undo/redo, queries, clarifications
- [ ] API: projects, parameters, model mesh, commands, instructions, undo/redo, history, STEP export
- [ ] SQLite persistence via SQLAlchemy + Alembic
- [ ] Frontend: Vite + React + TS + three.js viewport, component tree, property editor, AI instruction panel, history
- [ ] Docker Compose (backend `linux/amd64`, frontend nginx) and Makefile
- [ ] GitHub Actions CI: lint + backend tests + frontend build
- [ ] **Acceptance:** "increase the wheelbase by 100 mm" → wheelbase 2800 mm, rear axle and wheels move, body lengthens, STEP export reflects it, undo restores 2700 mm, all covered by automated tests

## Phase 2: Local LLM integration

- [ ] LLM client interface with Ollama and llama-server backends (JSON-schema-constrained output)
- [ ] Prompt built from the parameter registry; temperature 0
- [ ] Escalation policy: parser first, LLM for unresolved text, user confirmation for LLM proposals
- [ ] Evaluation dataset (`eval/`) and scoring script; pick the model by score vs memory
- [ ] Graceful behaviour when no model is running

## Phase 3: Specification interview and conflict detection

- [ ] Typed `VehicleSpec` (class, use, powertrain, power, torque, mass, drivetrain, dimensions, materials, suspension, budget)
- [ ] Adaptive question graph with conditions
- [ ] Physics-based plausibility and conflict rules (power-to-weight vs acceleration, traction limits, packaging)
- [ ] Spec → initial parameter set generation
- [ ] Interview UI (forms + chat)

## Phase 4: Integration depth

- [ ] Geometric clearance checks (OCCT exact distance on envelopes)
- [ ] Steering sweep envelope for front wheels; suspension travel envelopes
- [ ] Mass properties from CAD (materials, CoG, inertia)
- [ ] Impact report for each command: affected components, changed interfaces, failed checks

## Phase 5: Component library expansion

- [ ] Suspension: double wishbone, MacPherson strut (hardpoints as parameters)
- [ ] Shock absorber / spring (geometry + damping and spring-rate parameters)
- [ ] Brakes: disc, caliper envelope
- [ ] Steering: rack and pinion, tie rods (Ackermann geometry)
- [ ] Powertrain: engine block envelope, piston, connecting rod, crankshaft; gearbox envelope
- [ ] NL editing for component-level parameters ("redesign the shock absorber for softer damping")

## Phase 6: Simulation v1 (custom, verified models)

- [ ] Job queue (sequential) and telemetry storage
- [ ] Longitudinal: acceleration 0–100 km/h, emergency braking 100–0 km/h
- [ ] Quarter-car / half-car: potholes, bumps, ISO 8608 roads
- [ ] Bicycle model with Pacejka tyres: steady-state cornering, step steer
- [ ] Powertrain: torque map, gears, final drive
- [ ] Verification tests against closed-form results; fidelity labels
- [ ] Telemetry charts and result reports in the UI

## Phase 7: Natural-language simulation automation

- [ ] NL → `ScenarioSpec` → run → compare with requirements
- [ ] Rule-based engineering suggestions turned into proposed CAD commands

## Phase 8: High-fidelity multibody (Project Chrono)

- [ ] Conda-based Chrono worker (separate environment)
- [ ] Map Autevra design → Chrono::Vehicle templates
- [ ] Cross-check against the Phase 6 models

## Phase 9: Structural, thermal and fatigue

- [ ] gmsh meshing of components
- [ ] Static/modal FEA (CalculiX or FEniCSx/scikit-fem) for frame rails and suspension arms
- [ ] Lumped thermal models (brakes), then 3D thermal
- [ ] Fatigue from simulated load histories (rainflow + S-N + Miner)

## Phase 10: Aerodynamics and crash

- [ ] Drag estimate from CAD frontal area and Cd, then coarse CFD (OpenFOAM, offline/cloud)
- [ ] Lumped crash model, then OpenRadioss (offline/cloud)

## Phase 11: Cloud deployment

- [ ] PostgreSQL, S3 storage, async workers (SQS + ECS)
- [ ] Image build and push to ECR in CI; ECS task definitions
- [ ] Authentication and multi-user projects

---

## Progress log

### 2026-10-13: Phase 0 complete

**Done**
- Inspected the repository: empty, no prior implementation.
- Inspected the toolchain available for planning (Python 3.13/3.12 via uv, Node 22, Docker, Git).
- Verified on package indexes that CadQuery/OCP, gmsh, MLX, scikit-fem, fmpy and others have macOS arm64 binaries; verified PyChrono conda builds for osx-arm64.
- Installed and ran CadQuery 2.8 (x86_64): fillets and STEP export work; full install measured at 1.7 GB.
- Found and documented risks: CadQuery 2.8 incompatible with OCP 8 (tested); no Linux arm64 OCP 7.9 wheels; `pychrono` PyPI name collision; Docker on macOS has no GPU access.
- Wrote research, architecture, environment and roadmap documents plus repository hygiene files.

**Not done / open**
- No application code yet (by decision: research first).
- Local LLM not tested yet (model hosts were unreachable from the planning environment); to be tested on the Mac in Phase 2.
- Licence for the project not chosen yet.

**Next**
- Phase 1, starting with the Mac smoke test.
