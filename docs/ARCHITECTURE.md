# Proposed architecture

Status: **proposal**. Nothing here is implemented yet. It will be refined as
each phase is built and verified.

## 0. Current architecture (as built)

> Sections 1–7 below are the original planning draft and are kept for reference. This
> section describes the code as it is now.

### Three environments, one model

```
Website  /            ─┐
Workspace /app        ─┼─ React + react-router (frontend/src/site, workspace, studio)
Studio  /studio/:id/:ws┘   one Studio component per project; nine workspaces share its state
        │ HTTP /api
FastAPI (autevra.api) ── wires everything; the only layer that may import a domain directly
```

### Shared core and domain modules

| Layer | Packages | Knows about vehicles? |
|---|---|---|
| Core model | `autevra.core` (units, parameter / derived / rule registries, commands, design state) | no |
| Assembly | `autevra.assembly` (components, mates, coincidences, load paths, dependency graph) | no |
| Geometry | `autevra.cad` (kernel adapter, geometry cache, builder registry) | no |
| Engineering | `autevra.engineering` (tests, integration, diagnosis, optimisation, loop, requirements, trace, ReqIF) | no |
| AI | `autevra.ai` (parser engine, concepts, LLM clients and prompt, language registry) | no |
| Storage | `autevra.storage` | no |
| Extension API | `autevra.extensions` (`Plugin`, `register`, `unregister`, entry points) | no |
| Domain registry | `autevra.domains` (status and capabilities of every domain) | lists them |
| **Automotive domain** | `autevra.domains.automotive` (parameters, derived physics, rules, builders, vehicle, solvers, tests, integration checks, specification, language) | yes |
| Plugins | `autevra.contrib.*`, or packages with the `autevra.plugins` entry point | as needed |

`tests/test_architecture.py` enforces the first seven rows: no core package imports a
domain, and importing the core alone leaves every registry empty (checked in a fresh
interpreter). The automotive domain registers itself through the same `Plugin` interface
as third-party plugins, so a new domain is a new package that does the same.

**Domain interface.** A domain module supplies a `Plugin`:
- parameters, derived values and rules;
- builders, components, coincidences, load paths, interface kinds and clearances;
- integration checks and the limitations it states;
- test definitions, with their solver version, quick runs, limit explanations, default
  optimisation variables and saturation proxies;
- a `Language`.

It also supplies an entry in the domain registry.

**Current limit.** Registries are process-wide, so one installation runs its loaded
domains side by side in one model. Projects already record their domain, and creating
projects in unavailable domains is refused. When a second domain is implemented, the
registries will be keyed by domain so each project sees only its own.

## 1. Guiding decisions

| # | Decision | Reason |
|---|---|---|
| D1 | The **parameter set + command history** is the source of truth; B-rep geometry and meshes are always regenerated from it | Makes every design editable, reproducible, diff-able and undoable |
| D2 | Every change to the design goes through a **typed, validated command** | One path for UI edits, API calls and AI instructions; no unvalidated geometry changes |
| D3 | The **LLM only proposes commands**; it never executes code or touches geometry | Safety, determinism, testability |
| D4 | **Deterministic parser first, LLM second** | Common instructions work instantly with zero RAM; LLM handles the long tail |
| D5 | CAD kernel calls live behind one **adapter module** | CadQuery ↔ build123d ↔ raw OCP swaps stay local (see risk R1 in ENVIRONMENT.md) |
| D6 | Each component builder is a **pure function** `params → solid` that declares the parameters it depends on | Enables dependency tracking, selective rebuild and caching |
| D7 | **ISO 8855** vehicle axes (X forward, Y left, Z up, mm); origin on the ground below the front axle | One unambiguous convention for CAD, assembly and simulation |
| D8 | Heavy or differently-packaged engines (Chrono, FEA, CFD) run as **separate worker processes** | Isolates conda-only and GPL tools, keeps the API light, matches the future async-worker design on AWS |
| D9 | Simulation results carry a **fidelity label** (`estimate`, `verified`, `validated`) | Clear distinction between approximate and validated results |
| D10 | SQLAlchemy + Alembic from day one, storage behind an interface | SQLite → PostgreSQL and local disk → S3 without a rewrite |

## 2. Module overview

```
                    ┌──────────────────────────── Frontend (React + TS + three.js) ───────────────────────────┐
                    │ Viewport │ Component tree │ Property editor │ AI panel │ Spec forms │ History │ Sim/Telemetry │
                    └─────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                              │ REST (JSON / GLB)  + WebSocket (telemetry, later)
┌─────────────────────────────────────────── Backend API (FastAPI) ─────────────────────────────────────────────┐
│                                                                                                                │
│  ai/                    domain/                   cad/                  assembly/            simulation/       │
│  ├ lexicon              ├ units                   ├ kernel (adapter)    ├ interfaces/mates   ├ scenarios       │
│  ├ rule_parser  ──────▶ ├ parameters (registry)◀──├ components/*        ├ dependency graph   ├ models/*        │
│  ├ llm (Ollama/         ├ rules (validation)      ├ builder + cache     ├ clearance          ├ requirements    │
│  │   llama-server)      ├ commands + history      ├ tessellate          └ mass properties    └ fidelity        │
│  └ interpreter ───────▶ └ spec (interview)        └ export (STEP/GLB)                                          │
│                                                                                                                │
│  storage/ (SQLAlchemy: projects, designs, history, results)      jobs/ (sequential queue → worker processes)   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
          │ HTTP localhost                                               │ job queue
   ┌──────┴───────┐                                           ┌──────────┴───────────┐
   │ Ollama /     │  (native on Mac, Metal GPU)               │ Simulation workers   │ (custom models in-process first;
   │ llama-server │                                           │ Chrono (conda), FEA  │  Chrono/FEA/CFD as separate envs)
   └──────────────┘                                           └──────────────────────┘
```

Dependency rule: `domain` depends on nothing else in Autevra. `ai` depends on
`domain` only (it produces commands, never geometry). `cad` and `assembly`
depend on `domain`. `api` wires everything together. `simulation` reads
the design and derived mass properties but never mutates them.

## 3. Proposed repository layout

```
autevra/
├── README.md
├── docs/                      # research, architecture, roadmap, environment, workflow
├── backend/
│   ├── pyproject.toml         # uv-managed, Python 3.12
│   ├── Dockerfile             # linux/amd64 (see ENVIRONMENT.md R1)
│   ├── autevra/
│   │   ├── main.py            # FastAPI app factory
│   │   ├── config.py          # settings from environment variables
│   │   ├── api/               # routes + request/response schemas
│   │   ├── domain/            # units, parameter registry, rules, commands, history, spec
│   │   ├── cad/               # kernel adapter, component builders, cache, tessellation, export
│   │   ├── assembly/          # interfaces, mates, dependency graph, clearance, mass props
│   │   ├── ai/                # lexicon, rule parser, LLM clients, interpreter, prompts
│   │   ├── simulation/        # scenarios, models, requirements, fidelity (Phase 6+)
│   │   ├── jobs/              # sequential job queue (Phase 6+)
│   │   └── storage/           # SQLAlchemy models, repositories, file storage interface
│   ├── migrations/            # Alembic
│   └── tests/
├── frontend/
│   ├── package.json           # Vite + React + TypeScript + three
│   ├── Dockerfile             # build → nginx
│   └── src/
│       ├── api/               # typed API client
│       ├── viewport/          # three.js scene, picking, highlighting
│       ├── panels/            # tree, properties, AI, history, checks, simulation
│       └── state/
├── workers/                   # (later) chrono/, fea/ — separate environments
├── eval/                      # (Phase 2) NL instruction → expected command datasets
├── docker-compose.yml
└── Makefile                   # one-line commands: setup, dev, test, lint, docker
```

## 4. Core data model (draft)

**Parameter definition** (registry entry): `id`, `label`, `group`, `unit`,
`default`, `min`, `max`, `step`, `description`, `aliases` (for language),
`increase_words` / `decrease_words` (e.g. "wider" → body width up).

**Derived value**: read-only, computed deterministically from parameters
(e.g. overall length = front overhang + wheelbase + rear overhang; tyre
diameter = rim × 25.4 + 2 × width × aspect ratio). Requests to edit a
derived value produce a clarification that names the controlling inputs.

**Command** (examples):

```json
{ "type": "set_parameters",
  "changes": [ { "parameter": "wheelbase", "operation": "increase", "value": 100, "unit": "mm" } ],
  "source": "rules", "instruction": "increase the wheelbase by 100 mm" }
```

Execution resolves each change to an absolute value, validates bounds and
cross-parameter rules, and records a **history entry** with old and new
values so undo/redo is exact.

**Component**: `id`, `name`, `category`, builder function, declared
parameter dependencies, **interfaces** (named coordinate frames such as
`hub_left`, `axle_mount`), and a material for mass properties and rendering.

**Mate**: `(parent component, parent interface) ↔ (child component, child interface)`.
The child's placement = parent placement × parent interface frame × inverse(child interface frame).

### Draft initial parameter set (Phase 1)

| Group | Parameter | Unit | Default | Range |
|---|---|---|---|---|
| Dimensions | Wheelbase | mm | 2700 | 2000–3600 |
| | Front overhang | mm | 900 | 500–1400 |
| | Rear overhang | mm | 1000 | 500–1500 |
| | Body width | mm | 1820 | 1500–2200 |
| | Overall height | mm | 1450 | 1100–2100 |
| | Beltline height | mm | 960 | 700–1400 |
| | Ground clearance | mm | 160 | 90–350 |
| Cabin | Cabin length (at beltline) | mm | 2500 | 1200–4200 |
| | Roof length | mm | 1500 | 600–3800 |
| | Cabin fore/aft offset | mm | -150 | -900–900 |
| Wheels & tyres | Front / rear track | mm | 1560 | 1200–1900 |
| | Rim diameter | in | 17 | 13–22 |
| | Tyre width | mm | 225 | 145–335 |
| | Tyre aspect ratio | % | 50 | 25–80 |
| | Wheel arch clearance | mm | 35 | 15–120 |
| Steering | Max steer angle | deg | 35 | 20–45 |
| Chassis frame | Rail spacing (centre-to-centre) | mm | 900 | 600–1300 |
| | Rail section width × height | mm | 70 × 110 | 40–150 × 60–250 |
| | Rail wall thickness | mm | 4 | 2–10 |

Example cross-parameter rules: tyres must fit inside the body width;
wheel arch top must stay below the beltline; front overhang must contain
the front arch; roof length ≤ cabin length; rail wall thickness < half the
rail section; steered front tyre must clear the frame rails (checked
geometrically at sampled steer angles).

## 5. Natural-language pipeline in detail

1. **Normalise**: lower-case, unify units (`mm`, `cm`, `m`, `inch`, `"`, `%`, `deg`), split compound requests on "and" / commas.
2. **Match parameters** with the longest alias first ("front track" before "track"); group aliases ("track" → front and rear).
3. **Detect the operation**: increase/raise/extend/widen/lengthen, decrease/reduce/lower/shorten/narrow, set ("to", "make it"), scale ("by 10 %").
4. **Extract quantities** and convert to the parameter's unit; flag assumed units for bare numbers.
5. **Special phrases**: "lower the car" → ground clearance; "make it longer" → clarification (length is derived); "undo", "redo", "what is the wheelbase?".
6. **Confidence**: if every clause resolved cleanly, emit a command; otherwise escalate to the local LLM (if enabled) with the registry-derived JSON schema; otherwise ask a clarifying question with suggestions (fuzzy matching).
7. **Validate and execute** through the command system; return affected components, warnings and rebuild time.

## 6. Simulation architecture (Phase 6+)

- `ScenarioSpec` (typed): scenario type, initial conditions, environment (μ, road profile), duration, requirements.
- Model registry: each scenario maps to one or more models with a declared fidelity.
- Inputs from the design: mass, CoG height and position, wheelbase, track, tyre radius, inertia from CAD mass properties, plus spec values (power, torque, gear ratios, brake sizes).
- Outputs: time-series telemetry plus scalar metrics, compared with requirements.
- Every model ships with **verification tests** against closed-form solutions before it is exposed in the UI.

## 7. Path to AWS

| Local | AWS |
|---|---|
| Uvicorn process | ECS Fargate service from an ECR image |
| SQLite file | RDS PostgreSQL (same SQLAlchemy models, Alembic migrations) |
| `data/` folder | S3 bucket (same storage interface) |
| In-process sequential job queue | SQS + ECS worker tasks (same job interface) |
| Ollama on the Mac | Ollama/llama-server on an EC2 instance or ECS task in the VPC, still self-hosted (no hosted inference API) |
| `.env` file | SSM Parameter Store / Secrets Manager |
