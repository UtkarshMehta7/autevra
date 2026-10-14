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

## Phase 3: Suspension, test bench and the engineering loop ✅

Goal: one complete, verifiable engineering workflow on a real, editable component (the first
milestone of the engineering brief). Order changed from the earlier plan on request: the
specification interview moves to Phase 5.

- [x] Suspension and mass as parameters with mass, stiffness and damping units
- [x] Coil-over dampers in the CAD assembly; spring wire diameter follows the rate
- [x] Whole-vehicle integration checks: interfaces, connectivity, closed mounts, load paths, travel limits, exact OCCT clearances
- [x] Quarter-car solver behind a solver interface, verified against closed-form results
- [x] Component test framework: definitions, criteria, credibility labels, stored runs with design revisions, staleness, user requirements
- [x] Evidence-based diagnosis from measured sensitivities, with rule-checked fixes
- [x] Bounded, seeded optimisation (single objective or Pareto) on the real solver, approval required
- [x] Engineering loop: test → diagnose → fix → retest, bounded and traceable
- [x] Test bench, integration and optimisation panels in the workspace
- [x] **Acceptance:** "Increase the rear shock absorber damping by 10% and test its response" changes the dynamic model only, reruns the rear tests, compares with the previous revision and keeps undo; automated tests cover NL → command → simulation → evaluation → history

## Phase 4: Traceability core ✅

- [x] Requirements as first-class records linked to parameters, tests, runs and verdicts
- [x] Impact report of any change on requirements and evidence (before applying it)
- [x] ReqIF import and export
- [x] Evidence structure ready for ISO 26262 / ASPICE work products (no compliance claims)

## Phase 5: Specification interview and conflict detection ✅

- [x] Typed `VehicleSpec` (class, use, powertrain, drivetrain, power, battery, mass, seats, 0–100 target, ride character, wheel size); torque, materials and budget deferred
- [x] Adaptive question graph with conditions
- [x] Physics-based plausibility and conflict rules (traction- and power-limited acceleration bound, battery mass share, cabin share; packaging through the design rules)
- [x] Spec → initial parameter set generation; provisional targets the user approves
- [x] Interview UI (forms + chat)

## Phase 6: Fidelity ladder and validation

- [ ] Half-car (pitch) and 14-DOF vehicle (roll, pitch, heave, four corners)
- [ ] Magic Formula (Pacejka) tyres; bicycle model for steady-state cornering and step steer
- [ ] ISO 8608 random road profiles; tyre enveloping for short obstacles
- [ ] Validation module: import measured data, correlation metrics, then "experimentally validated"
- [ ] Credibility assessment following NASA-STD-7009A / ASME V&V 40 ideas
- [ ] Project Chrono adapter after a license, arm64 and memory evaluation (conda worker, separate process)

## Phase 7: Uncertainty and robustness

- [ ] Sensitivities on every key result (generalising the diagnosis perturbations)
- [ ] Monte Carlo over tolerances, mass and load variation; confidence bands in reports

## Phase 8: Electrified powertrain and energy

- [ ] Battery, e-motor, inverter and thermal models; packaging envelopes in CAD
- [x] Longitudinal: acceleration 0–100 km/h, braking 100–0 km/h (dry and wet)
- [ ] Energy over WLTP-style cycles
- [ ] Range, charging and thermal-limit tests as first-class component tests

## Phase 9: Component library and integration depth

- [ ] Suspension: double wishbone, MacPherson strut (hardpoints as parameters); travel and steering sweep envelopes
- [ ] Brakes: disc, caliper envelope; steering: rack and pinion, tie rods (Ackermann geometry)
- [ ] Mass properties from CAD (materials, CoG, inertia)
- [x] Plugin SDK (components, interfaces, rules, clearances, tests); example brake-disc plugin

## Phase 10: Interoperability

- [ ] STEP AP242 with PMI; FMI 3.0 / SSP co-simulation; SysML v2 export; OpenSCENARIO / OpenDRIVE scenarios

## Phase 11: Lifecycle, cost and regulation

- [ ] Mass, cost and ISO 14040-style carbon estimates per design variant
- [ ] Checkable UNECE clauses as rules, reported as model-level consistency (never homologation)

## Phase 12: Design branches and signed results

- [ ] Branchable, content-addressed design history (diff, merge, revert); reproducible signed results
- [ ] Surrogate models trained only on Autevra's own verified runs, always re-verified by a solver

## Phase 13: Structural, thermal, fatigue, aero and crash (offline or cloud)

- [ ] gmsh meshing; static/modal FEA (CalculiX or FEniCSx/scikit-fem); lumped then 3D thermal; fatigue (rainflow, S-N, Miner)
- [ ] Drag from frontal area and Cd, then coarse CFD (OpenFOAM); lumped crash, then OpenRadioss

## Phase 14: Cloud deployment

- [x] PostgreSQL support (psycopg 3; suite runs on SQLite and Postgres in CI)
- [x] Hosted demo shape: static frontend (Netlify), container API on Render's free plan (`$PORT`), Neon Postgres ([DEPLOYMENT.md](DEPLOYMENT.md)); CI checks the backend within 512 MB
- [ ] Per-visitor workspaces and rate limits for the public demo (next, before sharing widely)
- [ ] S3 storage, async workers (SQS + ECS)
- [ ] Image build and push to ECR in CI; ECS task definitions
- [ ] Authentication and multi-user projects

---

## Progress log

### 2026-10-14: body styles and visitor workspaces

- **Body styles.** A `body_style` choice parameter (sedan, hatchback, SUV, coupe, pickup, van, box truck) drives a different body construction instead of one three-box shape for every vehicle: two-box roofs that run to the tailgate, an upright SUV, a fastback coupe, a pickup cab with an open bed, a one-box van with a short nose, and a box truck with a cab and a separate cargo box. `body_layout` gives the proportions (tested without CAD); every style builds one valid solid with the design's extents on every class template.
- Choice parameters: `ParameterDef.options`; a dropdown in the property editor; the deterministic parser sets them ("make it a pickup", "change the body style to SUV", "turn it into a lorry") with synonyms from the domain language; they are left out of the LLM prompt.
- The specification interview picks the style from the vehicle class and gains a **box truck** class (template, travel and unsprung masses).
- **Visitor workspaces and rate limits** (PR #16): see `DEPLOYMENT.md`, "Public safety defaults".
- Checked in Chrome on the local studio: sedan, pickup, box truck, van and hatchback render as distinct bodies from plain-English instructions.

- **Glazing.** Window openings (side glass, windscreen, rear screen) are cut into the greenhouse, leaving the pillars and roof; a separate tinted `glass` component fills them from inside. It depends only on the greenhouse parameters, so a wheel or track change does not rebuild it.

- **Start from a template.** `GET /api/templates` lists one starting design per vehicle class (city car to box truck), each the design the specification interview generates for that class (body style, proportions, wheels, springs, dampers; rule-checked). Projects can be created from one (`template` in `POST /api/projects`), from the Projects page or the Models page. Templates are a core registry filled through the plugin API.

- **Lamps.** Head lamps and tail lamps are their own components, flush in recesses on the front and rear faces of every body style (low on the cargo box of a box truck), so the vehicle extents and the STEP bounding box are unchanged.

- **Road loads per class.** Each template sets a typical drag coefficient, rolling resistance and centre-of-gravity height for its class (a box truck at Cd 0.60, a sedan at 0.28); the specification marks them "typical, not measured". The longitudinal test therefore differs by class.
- **Warm-up.** Hosted instances build the default geometry at startup (`AUTEVRA_WARM_UP`).
- Checked on the live site (Chrome): a new project in a browser workspace, "make it a pickup" rebuilt body and glazing in 6.3 s on the free instance; the first model took 34 s.

- **Coupe as a real fastback**: full roof and a long, shallow rear screen (the first version had a short roof that read as a box on a deck; caught on the renders).
- **Website**: a home-page gallery of the eight templates and a new studio hero, all renders of this build.

- **Faster meshes.** CadQuery's `Shape.tessellate` walks OCCT arrays through Python iterators (about 5 ms per face, even for a two-triangle face); `kernel.tessellate` uses indexed access and a face explorer and returns identical meshes (tested against CadQuery). Mesh extraction for the default vehicle fell from about 2.3 s to under 0.6 s on the Mac (body 493 → 8 ms, frame 330 → 4 ms, damper 193 → 42 ms once meshed), which matters most on the 0.1 CPU hosted instance.
- **Smaller downloads.** Builders can declare a coarser display mesh (`mesh_angular`); the coil dampers use 0.5 rad (3x fewer triangles, 5x faster meshing; B-rep and STEP unchanged), and responses are gzip-compressed. The default model's transfer fell from 1.53 MB to 158 KB.

- **Materials.** Components declare a display finish (paint, glass, lamp, rubber, metal); the viewport renders each with a physically based material under a neutral studio environment, so glass reflects, lamps glow, tyres read as rubber and the chassis as metal. Display only: the CAD and STEP are unchanged.

**Known limitations**
- Shapes are still faceted (ruled lofts and prisms); no curved surfaces, doors or mirrors.
- A van's greenhouse and a box truck's cargo box are sized from the overall dimensions, not from the cabin parameters.

### 2026-10-14: hosted demo live

- Live: <https://autevra.netlify.app> (Netlify) with the API at <https://autevra.onrender.com> (Render free web service, Docker) and Postgres on Neon. Both hosts deploy `main` on merge.
- Checked on the live services: backend health, CORS for the Netlify origin, projects, domains, parameters and LLM status (off) over the API; the Netlify bundle targets the Render API.
- Fixes found while deploying:
  - `AUTEVRA_CORS_ORIGINS` accepts one URL, a comma-separated list or JSON; a plain URL had crashed startup.
  - The Netlify build sets `VITE_API_URL`; without it the site fetched `index.html` from `/api` and showed a JSON parse error.
  - A non-JSON answer is now reported as a wrong API address.
  - The "make dev" hint appears only on localhost.
- Hugging Face Docker Spaces now require a paid plan, so Render's free instance hosts the backend; CI runs a full visitor session under its 512 MB limit on every pull request.

**Known limitations**
- No accounts or per-visitor workspaces: every visitor shares the projects. Next milestone.
- Free tiers: the backend sleeps after 15 minutes idle (about a minute to wake) and has 0.1 CPU, so studies are slow.
- Not yet exercised by hand on the live site: creating a project and working in the studio.

### 2026-10-14: deployment readiness

- Postgres: `psycopg[binary]` 3.3.6 (arm64 and x86_64 wheels); `postgres://` and `postgresql://` URLs are rewritten for the driver; pooled connections are pre-pinged (Neon closes idle ones); `%` in URLs is escaped for Alembic.
- `AUTEVRA_TEST_DATABASE_URL` runs the whole suite against Postgres, each test on an empty schema; a new CI job does this on `postgres:17`. 424 tests pass on SQLite and on local Postgres 17.
- The backend image listens on `$PORT` with proxy headers; `render.yaml` blueprint; `netlify.toml` (build, SPA fallback, immutable asset caching); the frontend takes `VITE_API_URL` at build time.
- Measured backend memory: 472 MB after import and 545 MB after a model build on the Mac; in the linux/amd64 container 295 MiB at peak through a full session, so Render's free 512 MB instance fits (13.7 minutes for the session at 0.1 CPU). Hugging Face Docker Spaces turned out to need a paid plan.
- Re-measured the `llm` tier: 78.3 % on main and the branch alike (see `ENVIRONMENT.md`).

**Known limitations**
- No accounts or per-visitor isolation: a hosted instance is a shared demo.
- Not yet deployed: the hosting accounts (Netlify, Neon, a container host) are the owner's to create.

### 2026-10-14: shared engineering core and the automotive domain module

**Done**
- `autevra.domain` renamed `autevra.core`. The core, assembly, CAD, engineering, AI and storage packages now hold mechanisms and empty registries only.
- Everything about road vehicles lives in `autevra.domains.automotive`:
  - parameters, derived physics, rules, builders, the vehicle assembly;
  - the quarter-car and longitudinal solvers and the test definitions;
  - clearances, wheel-travel checks, the specification interview;
  - the language: vocabulary, test and requirement phrases, concepts, prompt framing.
  
  It registers itself through the plugin API, like any plugin.
- New hooks replace every place where generic code special-cased the car: test-definition solver version, quick runs, limit explanations, default optimisation variables and saturation proxies; plugin integration checks, notes and languages.
- Architecture tests: no core package imports a domain; the core alone registers nothing; the parser alone knows no vehicle words.
- Behaviour unchanged: 419 backend tests pass (all earlier tests plus the architecture checks), and the live pipeline was spot-checked through the API.
- Layering documented in [ARCHITECTURE.md](ARCHITECTURE.md) §0.

**Known limitations**
- Registries are process-wide; per-project domain contexts come with the second domain.

### 2026-10-14: three environments, routed studio and the domain registry

**Done**
- Routing (`react-router` 8.4): public website at `/`, user workspace at `/app`, engineering studio at `/studio/:projectId/:workspace`. Direct links and refresh work in development (Vite) and in Docker (nginx falls back to `index.html`).
- The existing studio is preserved intact. Its dock tabs are now nine routed workspaces that share one component, one project state and one mounted viewport:
  - design, assembly, simulation, AI engineering, optimisation and requirements;
  - new: systems (assembly tree, interfaces and their users, mates, coincidences, load paths), manufacturing (STEP and ReqIF outputs, the manufacturability rules with live status; drawings, tolerances, CAM marked not available) and digital thread (revisions with the runs made on each).
- Website pages:
  - home, platform (and CAD, simulation, autonomous engineering);
  - domains and per-domain pages read from the live registry;
  - solutions, pricing (proposed tiers; no payment system, stated), docs, about (no invented history or partners);
  - contact (stored locally; the reply says no e-mail is sent).
  - Screenshots are of this build.
- Workspace pages: dashboard, projects (create, open, rename, duplicate, delete with confirmation), models (templates, tests, plugins), domains (projects only in available domains), simulation history across projects, files (STEP and ReqIF per project; uploads stated as unsupported), settings (local model, plugins; no accounts in this build).
- Backend:
  - domain registry: automotive available, with lists computed from the live registries; eight domains roadmap-only;
  - projects record their domain (additive migration);
  - project duplication, the system graph, rule status, a cross-project run index and the contact store.
- The studio code is loaded lazily: the website bundle is 298 kB (93 kB gzip) without three.js.
- 409 backend tests and 14 frontend tests pass. Every route was checked by hand in Chrome.

**Known limitations**
- ~~The core still contains the automotive model~~: done in the next entry.
- No authentication; the workspace is single-user and local.

### 2026-10-14: longitudinal test, car-shaped body, live simulation, plugin API

**Done**
- Longitudinal performance test: 0–100 km/h and 100–0 km/h (dry, wet), with:
  - a traction limit per driven axle with load transfer, for any torque split;
  - a power limit with a rotating-mass factor, drag and rolling resistance;
  - braking build-up.
  
  Verified against the energy balance, the traction formula and v²/(2μg). The specification's 0–100 target is now a verifiable requirement.
- New parameters: peak power, front drive share, drivetrain efficiency, drag coefficient, rolling resistance, CG height. Derived frontal area and power-to-weight. Power and dimensionless units.
- Body: side profile (bumper, nose, hood to the cowl, rear deck) with a rounded plan view and a tapered greenhouse; proportions follow the parameters; valid across random valid designs.
- Live simulation: tests already run are rerun after every change (`POST /tests/retest`). Runs play back in the 3D view from the solver traces: quarter-car corner motion and longitudinal wheel spin.
- Spec generation centres the dampers, sizes the arch gap and uses class unsprung masses. Every class passes the step and road hump except the light city car's rear with soft damping (brief lift-off on the kerb step).
- Plugin API (`autevra.extensions`, entry-point group `autevra.plugins`, `AUTEVRA_PLUGINS`). Example: brake discs with caliper envelopes, a rim-fit rule, exact caliper-to-rim clearance and an analytical disc-heating test. See [EXTENDING.md](EXTENDING.md).
- 404 backend tests and 13 frontend tests pass.

### 2026-10-13: Phase 5 complete (specification interview)

**Done**
- `VehicleSpec` with a source on every answer (you, or a labelled class-typical default); adaptive questions (battery capacity only for electric vehicles); validated ranges; optional questions can be skipped.
- Free text fills the specification deterministically, with unit conversion: "an electric SUV, 300 hp, 2.3 t, 0-100 in 6.5 s, 7 seats, AWD, 20 inch wheels, 90 kWh".
- Conflict checks:
  - the 0–100 km/h lower bound is traction-limited (μ 1.0, driven-axle static load), then constant power at 90 % efficiency, with no drag, rolling resistance or shifting. A target faster than the bound is a conflict. Example: 150 kW and 2.2 t gives a 6.8 s bound, so 6 s is impossible. A slower target is only "not ruled out".
  - battery mass share at an assumed 160 Wh/kg pack density;
  - cabin share of the body length (seven seats in a city car).
- Generation: class templates (all seven pass every design rule); springs sized for target ride frequencies with the tyre in series (rear 10 % above front); dampers from damping ratios; electric layouts move mass rearwards. The result is shown as an impact preview and applied only on request, as one undoable `spec` command. The proposed requirements (ride frequency band, off-road ground clearance, the 0–100 target as text) are added unapproved.
- UI: Specification tab with the question flow, answers with their source, checks with their basis, the generated design with the reason for each value, and Apply. Checked by hand in Chrome.
- 379 backend tests and 9 frontend tests pass.

**Known limitations**
- The acceleration check is a bound, not a simulation: meeting a target is never claimed until a longitudinal test exists.
- Templates are proportion starting points, not data from real vehicles; torque, top speed, range, materials and budget are not captured yet.

**Next**
- Longitudinal performance test (acceleration and braking) so the 0–100 target can be verified by simulation, then the validation module and the half-car.

### 2026-10-13: Phase 4 complete (traceability core)

**Done**
- Requirement records: key (REQ-001…), statement (generated when not given), rationale, priority, parent, approval, source, verification method. Three kinds:
  - **performance**: a limit on a test metric, verified only by current test runs;
  - **design**: a limit on a parameter or derived value, with unit conversion (15 cm is stored as 150 mm), verified by deterministic analysis;
  - **text**: no machine-checkable form, verified manually.
- Verification from evidence: verified, failed, stale (the design or the requirement changed since the run), not verified, not approved, manual. Each item of evidence names the run, scenario, measured value, limit, credibility and design revision.
- Trace matrix: requirement → parameters that can change it → components they build or place → test cases → evidence.
- Impact preview (`POST /preview`, "what if I …"). Without applying anything it reports:
  - changed values and derived values;
  - rule violations;
  - components rebuilt or moved, and tests to rerun;
  - packaging warnings added or cleared;
  - each requirement's status before and after.
  
  Example: 20-inch rims rebuild 9 components and move 10. The usable bump travel becomes limited by damper compression (28.5 mm) instead of the arch, and REQ-002 needs re-verification.
- "Verify the requirements" runs the missing or stale test cases, then reports.
- ReqIF 1.2 export and import. Exports round-trip exactly, including the hierarchy. Objects from other tools become text requirements (XHTML text read), re-import updates by key, and DOCTYPE/entity declarations and files over 5 MB are rejected.
- Parser: requirement statements; the comparator is taken from the words just before the number. Engineering units in commands (kg, lb, N/mm, kN/m, lbf/in, N·s/m, kN·s/m) are now converted. Previously a "kN/m" was read as the parameter's own unit, which was correct only by coincidence.
- UI: Requirements tab with add form (all three kinds), status, evidence, trace, approve/delete, Verify all, ReqIF import and export. Checked by hand in Chrome.
- 363 backend tests and 9 frontend tests pass; ruff and TypeScript clean.

**Known limitations**
- ReqIF text is written as a plain string attribute; some tools expect XHTML for `ReqIF.Text`.
- Requirements cannot yet span two corners with different limits, or ranges ("between 1.0 and 1.5 Hz"): add two requirements.
- No change history per requirement yet (edits overwrite); that comes with design branches (Phase 12).
- Requirements apply to the quarter-car metrics; vehicle-level metrics follow the fidelity ladder.

**Next**
- Phase 5: specification interview and conflict detection.

### 2026-10-13: Phase 3 complete (suspension, test bench, diagnosis, optimisation, loop)

**Done**
- Suspension and mass parameters (42 in total) with mass, stiffness and damping units; mixing dimensions is rejected.
- Derived values: sprung corner mass, ride frequency (spring and tyre in series), damping ratios, spring wire diameter from the rate, damper installed length, usable travel and the limit that governs it.
- Rules: damper fits its mounts, stroke covers the travel, mounts inside the body, springs clear the tyres, spring index, coil bind, positive sprung mass.
- CAD: four coil-over dampers (swept helical coil) mated to the axles; their upper eyes must meet the body's shock towers.
- Integration checks: interfaces and their kinds, connectivity, closed mounts, load paths, travel limits set by packaging, exact OCCT clearances. Default design: 39 pass, 2 warnings (the 35 mm arch gap, not the 60 mm bump stop, limits bump travel).
- Quarter-car solver: two-rate damper, tyre lift-off, RK4 with a half-step convergence check. Verified to under a micrometre against the exact linear solution and against the characteristic equation; about 40 ms per run.
- Component tests: quarter-car ride test (25 mm step, 75 mm road hump, 50 mm pothole) and an analytical ride-modes test with no default criteria; each run is stored with solver identity, inputs, design revision, numerics and credibility, and compared with the previous revision.
- Diagnosis: governing limit, measured effects of every input (±10 % re-simulation), smallest rule-checked fix. Example: rear hump bump travel 42.7 mm against 35 mm; the arch governs; +30 % arch clearance fixes it in the model, confirmed by a full rerun.
- Optimisation: seeded Latin hypercube plus compass search, rule screening before simulation, worst case over scenarios, Pareto set for two objectives, full re-verification, accept or reject. Example: rear RMS body acceleration −22 % with every criterion kept.
- Engineering loop: test → diagnose → fix → retest; on the default design it fixes the hump and stops at the pothole, which needs an engineering decision.
- UI: test bench (criteria, solver traces with limits and the previous revision, comparisons, diagnosis with Apply), integration panel, optimisation and loop panel, component test status in the tree. Checked by hand in Chrome.
- 332 backend tests and 9 frontend tests pass; ruff and TypeScript clean.

**Known limitations**
- Pothole: the point-contact tyre without enveloping makes short obstacles severe; the tyre leaves the road for every candidate, so pothole studies are infeasible by design of the model. Tyre enveloping is in Phase 6.
- Quarter-car only: no roll or pitch, so requests mentioning roll report it as not checked.
- Spring-rate changes assume the ride height is kept (preload or free length adjusted); static sag is not modelled.
- Spring stress is not checked yet: the allowable stress depends on material and presetting data to be sourced.
- The body is a solid envelope; parts inside it are not clearance-checked against it.
- LLM proposals do not trigger tests; ask for the test after confirming.

**Next**
- Phase 4: traceability core (requirements linked to parameters, tests, runs and verdicts; ReqIF).

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
