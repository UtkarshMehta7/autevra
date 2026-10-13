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

- [x] Mac smoke test: `uv` + Python 3.12 + `cadquery==2.8.0` imports and exports a STEP file
- [x] Backend skeleton: FastAPI app, config, health endpoint, pytest, ruff
- [x] Domain: units, parameter registry, derived values, cross-parameter rules
- [x] Command system: typed commands, validation, history, undo/redo
- [x] CAD: kernel adapter; builders for body (with wheel arches and cabin), ladder frame, axles, wheels (tyre + rim)
- [x] Assembly: interfaces + mates, dependency graph, rebuild only affected components (cache by parameter hash)
- [x] Deterministic intent parser (automotive lexicon + units) for set/increase/decrease/scale, undo/redo, queries, clarifications
- [x] API: projects, parameters, model mesh, commands, instructions, undo/redo, history, STEP export
- [x] SQLite persistence via SQLAlchemy + Alembic
- [x] Frontend: Vite + React + TS + three.js viewport, component tree, property editor, AI instruction panel, history
- [x] Docker Compose (backend `linux/amd64`, frontend nginx) and Makefile
- [x] GitHub Actions CI: lint + backend tests + frontend build
- [x] **Acceptance:** "increase the wheelbase by 100 mm" → wheelbase 2800 mm, rear axle and wheels move, body lengthens, STEP export reflects it, undo restores 2700 mm, all covered by automated tests

## Phase 2: Local LLM integration

- [x] LLM client interface with Ollama and llama-server backends (JSON-schema-constrained output)
- [x] Prompt built from the parameter registry; temperature 0
- [x] Escalation policy: parser first, LLM for unresolved text, user confirmation for LLM proposals
- [x] Evaluation dataset (`eval/`) and scoring script; pick the model by score vs memory
- [x] Graceful behaviour when no model is running

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

### 2026-10-13: Phase 2 complete (local LLM fallback)

**Done**
- HTTP client switched from `httpx` to `httpx2` (tests and LLM clients).
- `ai/llm/`: `OllamaClient` (`/api/chat` with a JSON schema in `format`, thinking off) and `LlamaServerClient` (OpenAI-compatible `response_format`), both at temperature 0 with a fixed seed; `DisabledClient` when `AUTEVRA_LLM_PROVIDER=off`. Only local URLs, `trust_env` off, 2 s connect timeout.
- Prompt generated from the parameter registry (id, unit, current value, range, meaning, aliases) and the derived values, with five few-shot examples.
- Escalation policy: deterministic parser → unmodelled automotive concepts (clarify; "make the suspension softer" asks spring rate vs compression vs rebound damping) → automotive scope check → local model → grounding and rule validation → **proposal**. Proposals are never applied until the user confirms them (`POST …/proposals/{id}/confirm`); the service refuses to apply an LLM-sourced command any other way.
- Grounding: every value must be a number the user wrote (digits or number words); "to N" means set, "by N" means relative with the direction taken from the user's verb; scale factors must come from the text; the user's unit overrides the model's.
- Parser hardening found by the evaluation: it no longer guesses when a sentence has words it cannot explain ("slide the cabin 100 mm forward" and "drop the window line by 40 mm" were previously misapplied).
- Evaluation set `eval/instructions.jsonl` (47 items, `rules` and `llm` tiers) and `python -m autevra.ai.evaluate`; the rules tier is 100 % deterministic and checked in CI, and a test ensures the parser never misapplies an `llm`-tier phrase.
- Model choice by score vs memory: `qwen3:1.7b` (82.6 % on the `llm` tier, 1.6 GB RAM); `qwen3:4b` scored the same with twice the errors, time and memory (table in `ENVIRONMENT.md`).
- UI: model status badge, proposal card with Confirm / Reject, and the app is fully usable with no model running (status explains how to start Ollama).
- 229 backend tests and 5 frontend tests pass; ruff and TypeScript clean. Confirm, reject, once-only confirmation and undo of a confirmed proposal checked against the live model through the API.

**Known limitations**
- Proposals live in memory for 15 minutes and do not survive a backend restart.
- "push the rear axle back 10 cm" is ambiguous (wheelbase or rear overhang); both models chose the rear overhang. Shown as a proposal, so nothing changes unless confirmed.
- Small models still confuse related parameters: live, `qwen3:1.7b` read "stretch the gap between front and rear axles by 4 inches" as the rear track. The rule check rejected it (tyres outside the body), but a mapping that happened to pass the rules would reach the user as a wrong proposal; confirmation is the safeguard.
- The `llm` tier is small (23 items); accuracy figures have wide error bars.

**Next**
- Phase 3: specification interview and conflict detection.
- From the engineering brief: the quarter-car model is the first simulator to build (Phase 6 item, with closed-form verification and fidelity labels: estimated / simulated / validated / certified).

### 2026-10-13: Phase 1 complete (steps 5–9)

**Done**
- Assembly: 4×4 transforms; components declare geometry dependencies and per-interface frame dependencies, enforced by a view that raises on undeclared reads; wheels are mated to axle hubs and axles to vehicle mounts; dependency graph splits affected components into *rebuild* and *move*.
- Geometry cache keyed by a hash of (builder, inputs): the four wheels share one solid and mesh; a wheelbase change rebuilds only the body and frame.
- Deterministic intent parser: aliases from the registry, units, compound requests, group aliases ("track"), "lower the car", "make it 1.9 m wide", "18 inch wheels", undo/redo, queries, and clarifying questions for derived values ("make it longer"), missing amounts and typos.
- API: projects, catalogue, commands (422 with violations), instructions, undo/redo, history, de-duplicated meshes with 4×4 transforms (`?known=` skips geometry the client already has), STEP export. SQLite via SQLAlchemy 2 with an Alembic migration applied on start.
- Frontend: three.js viewport (Z-up, picking, x-ray body, change highlight), component tree, property editor with derived values, instruction panel with suggestions and a sequential action queue, history; client-side geometry LRU so undo/redo download nothing.
- Docker Compose (backend `linux/amd64`, nginx frontend), Makefile, GitHub Actions CI (lint, tests, frontend build, image build).
- **Acceptance test passes** (`backend/tests/api/test_api.py::test_acceptance_increase_wheelbase_by_100_mm`), and the flow was checked by hand in Chrome on the Mac.
- 163 backend tests and 4 frontend tests pass; ruff and TypeScript clean.

**Not verified locally**
- Docker images: Docker is not installed on the Mac. CI builds them successfully on x86_64; running the stack (`make docker-up`) is untested until Docker Desktop is installed.

**Remaining / follow-ups**
- ~~Switch the test client from `httpx` to `httpx2`~~ done: `httpx2` is now the backend's HTTP client (tests and, from Phase 2, the LLM clients); deprecation warnings are no longer filtered.
- Phase 2: local LLM fallback for text the parser cannot resolve, with confirmation of LLM proposals and an evaluation set.
- Phase 4 items already prepared for: `max_steer_angle` is in the registry but unused until the steering sweep clearance check.

### 2026-10-13: Phase 1 steps 1–4 (backend, domain, commands, CAD builders)

**Done**
- Mac smoke test passed natively on arm64: `uv` 0.12.19, Python 3.12.14, `cadquery 2.8.0` with `cadquery-ocp 7.9.3.1.1`; a filleted box exports to STEP and re-imports with the same volume.
- Backend skeleton (`backend/`): FastAPI app factory, settings, `/api/health`, pytest, ruff.
- Domain: units (mm, cm, m, in, %, deg), 21-parameter registry from the architecture draft, derived values (overall length, tyre geometry, arch heights), 11 cross-parameter rules.
- Command system: `set` / `increase` / `decrease` / `scale`, unit conversion, relative `%`, atomic validation, history with exact undo and redo, replay check, JSON round trip.
- CAD: kernel adapter (`cad/kernel.py`, the only module that imports CadQuery) and builders for the body (lower body, wheel wells, lofted cabin), hollow ladder frame, beam axles and wheels (filleted tyre, rim barrel, spoked disc). Each builds in under 0.1 s.
- 71 tests pass; ruff clean.

**Remaining in Phase 1**
- Interfaces, mates, dependency graph and geometry cache (wheels placed by mates).
- Deterministic intent parser.
- API, SQLite persistence (SQLAlchemy + Alembic), STEP export endpoint.
- Frontend workspace; Docker Compose, Makefile, CI; acceptance test.

**Notes**
- Two rules (`rail_wall_fits_section`, `arches_do_not_overlap`) cannot fire within today's registry bounds; they guard against wider bounds later and are tested directly.

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
