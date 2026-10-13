# Autevra

**Intent-based AI engineering platform for automotive design and simulation.**

Describe what you want in plain language, and Autevra designs, modifies,
integrates and tests **real, editable 3D CAD components** of a vehicle.
It is not an image generator and not a generic chatbot: every instruction
becomes a validated engineering operation on parametric geometry.

> "Increase the wheelbase by 100 mm."
> "Increase the rear shock absorber damping by 10% and test its response."
> "Explain why the suspension travel limit was exceeded."
> "Optimise ride comfort on the rear over the hump." / "Fix the rear suspension."

---

## Status

**Phases 1–5 are implemented.**

- **Parametric vehicle.** Body with wheel wells and cabin, hollow ladder frame, beam axles, wheels and four coil-over dampers, in real CadQuery/Open CASCADE geometry. It is edited through typed, validated commands from the property editor, the API or plain English, with undo/redo, persistence and STEP export.
- **Local language model (optional).** A local model proposes changes the deterministic parser cannot resolve, and every proposal needs confirmation.
- **Engineering workflow.** One complete loop on the suspension:
  - edit a spring rate or damper coefficient;
  - see which tests that makes stale;
  - run the verified quarter-car test bench (step, road hump, pothole);
  - compare with the previous revision;
  - diagnose a failure from measured sensitivities;
  - optimise within bounds, or let the engineering loop fix and retest.
  
  Nothing changes until you accept, and every result says whether it is an analytical estimate or a numerical simulation. Nothing is presented as validated without test data.

- **Specification interview.** Describe the vehicle ("an electric SUV, 220 kW, 7 seats, AWD"). Autevra:
  - asks only the questions that apply;
  - flags physically impossible targets and implausible values, with the basis for each;
  - generates a rule-checked starting design that you preview and apply.
- **Traceability.**
  - Requirements, stated in plain English or imported from ReqIF, are linked to the parameters, components and test runs that prove them.
  - Each requirement shows whether it is verified, failed or stale.
  - "What if I …" previews a change's impact on geometry, tests and requirements before anything is applied.

See [docs/ROADMAP.md](docs/ROADMAP.md) for progress, known limitations and what is next.

| Document | Contents |
|---|---|
| [docs/RESEARCH.md](docs/RESEARCH.md) | Resources, options and recommendations for CAD, local AI, simulation, frontend, backend, deployment, plus product possibilities and reference material |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Proposed modules, data model, NL pipeline, repository layout, path to AWS |
| [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) | Environment inspection, verified Apple Silicon compatibility matrix, risks and memory budget |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phased implementation plan and progress log (completed and remaining work) |
| [docs/MODULES.md](docs/MODULES.md) | How each implemented module works |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development workflow, branch and commit conventions |

## Core capabilities (✅ available, the rest planned)

1. ✅ **Automotive AI, fully local**: a deterministic automotive command parser plus an optional small quantised LLM (Ollama or llama.cpp). No hosted AI APIs.
2. **Specification interview**: adaptive questions on vehicle type, powertrain, power, torque, dimensions, drivetrain, materials, suspension, budget and use, with conflict detection.
3. ✅ **Real parametric CAD**: B-rep geometry on Open CASCADE (via CadQuery), exportable to STEP.
4. ✅ **Natural-language editing**: instructions become validated commands with feature history, undo and redo.
5. ✅ **Component integration**: a connected assembly with interfaces, coordinate frames, dependencies and clearance checks; only affected components are rebuilt.
6. **Engineering simulation**: ✅ quarter-car ride (step, hump, pothole) with verified numerics; next half-car and full vehicle, braking, cornering, powertrain and tyres; later structural, thermal, fatigue, aero and crash.
7. ✅ **Simulation automation**: describe a test in words, run it, compare against requirements, diagnose failures, optimise and iterate, with results labelled as analytical estimate, numerical simulation or experimentally validated.
8. **3D workspace**: viewport, component tree, property editor, AI panel, spec forms, simulation controls, telemetry and reports.

## Principles

- Real, editable CAD geometry over visual demos.
- The LLM only **proposes** typed commands; deterministic code validates and executes them. No arbitrary code execution.
- Deterministic engineering calculations wherever possible, verified against analytical or reference results.
- Modular: AI interpretation, CAD, assembly, simulation and visualisation are separate modules.
- Lightweight enough for a Mac M2 with 8 GB RAM; Docker-ready; designed for AWS later without a rewrite.
- Small, verifiable steps with a working application at every stage.

## Planned technology stack

| Layer | Choice |
|---|---|
| Frontend | React + TypeScript + Vite + three.js |
| Backend | Python 3.12 + FastAPI + Pydantic |
| CAD | Open CASCADE Technology via CadQuery 2.8 (behind an adapter) |
| Local AI | Deterministic parser + Ollama or llama.cpp `llama-server` with a ~1.5B–4B quantised model |
| Simulation | Custom verified models (NumPy/SciPy) first, Project Chrono later |
| Database | SQLite via SQLAlchemy + Alembic, PostgreSQL later |
| Packaging | Git, pytest, GitHub Actions, Docker Compose; later AWS ECR/ECS, S3, PostgreSQL, async workers |

See [docs/RESEARCH.md](docs/RESEARCH.md) for the alternatives considered and why.

## Getting started (Mac M2)

Prerequisites: `xcode-select --install`, then `brew install uv node@22`.

```bash
git clone https://github.com/UtkarshMehta7/autevra.git ~/Downloads/autevra
cd ~/Downloads/autevra
make setup        # backend venv via uv (~1.3 GB, CadQuery + OCCT) and frontend npm packages
make dev          # backend on http://127.0.0.1:8000, workspace on http://localhost:5173
```

Open http://localhost:5173 and try "increase the wheelbase by 100 mm",
"set the rims to 18 inch and lower the car by 20 mm", "make it longer",
"how long is the car?" or "undo". For the engineering workflow, try
"increase the rear shock absorber damping by 10% and test its response",
"explain why the suspension travel limit was exceeded", "fix the rear
suspension", "require the ground clearance to be at least 150 mm", "what if I
lower the car by 20 mm?", "verify the requirements", "I want an electric SUV
with 220 kW, 7 seats and AWD", or use the Specification, Test bench,
Integration, Optimise & loop and Requirements tabs under the viewport. The first start after installing can take a
minute or two while macOS scans the new native libraries; later starts take seconds.

| Command | What it does |
|---|---|
| `make setup` | install backend (`uv sync`) and frontend (`npm ci`) dependencies |
| `make dev` | run the backend (auto-reload) and the Vite dev server together |
| `make backend` / `make frontend` | run one of them |
| `make test` | backend `pytest` (includes the acceptance test) and frontend `vitest` |
| `make lint` | `ruff check`, `ruff format --check` and the TypeScript check |
| `make format` | apply ruff formatting and fixes |
| `make docker` / `make docker-up` | build / run the Compose stack (UI on http://localhost:8080) |

Data (SQLite database and STEP exports) lives in `backend/data/` by default;
set `AUTEVRA_DATA_DIR` or `AUTEVRA_DATABASE_URL` to change it. The API is
documented interactively at http://127.0.0.1:8000/docs.

### Optional: local language model

The deterministic parser handles common phrasing with no model at all. For
other phrasing, Autevra can ask a small local model, which only **proposes**
a change; you confirm or reject it in the instruction panel.

```bash
brew install ollama
ollama serve                 # or: brew services start ollama
ollama pull qwen3:1.7b       # default model, about 1.4 GB on disk, about 1.6 GB RAM
```

| Variable | Default | Meaning |
|---|---|---|
| `AUTEVRA_LLM_PROVIDER` | `ollama` | `ollama`, `llama_server` or `off` |
| `AUTEVRA_LLM_URL` | `http://127.0.0.1:11434` | runtime URL (`http://127.0.0.1:8080` for `llama-server`) |
| `AUTEVRA_LLM_MODEL` | `qwen3:1.7b` | model name |

If the runtime is not running, the app behaves exactly as with the LLM off.
Measure a model with `cd backend && uv run python -m autevra.ai.evaluate
--provider ollama --model <name>` (see [eval/README.md](eval/README.md)). Docker Desktop is optional too: daily
development runs natively, and the backend image targets `linux/amd64` (see
[docs/ENVIRONMENT.md](docs/ENVIRONMENT.md)).

## Repository layout

```
autevra/
├── backend/            FastAPI app (uv, Python 3.12)
│   ├── autevra/
│   │   ├── domain/     units, parameter registry, derived values, rules, commands, history
│   │   ├── cad/        kernel adapter (only CadQuery importer), component builders, geometry cache
│   │   ├── assembly/   transforms, interfaces and mates, dependency graph
│   │   ├── ai/         lexicon and deterministic intent parser
│   │   ├── storage/    SQLAlchemy models, repository, migrations runner
│   │   └── api/        routes, schemas, workspace service, model building
│   ├── migrations/     Alembic
│   └── tests/
├── frontend/           React + TypeScript + Vite + three.js workspace
├── eval/               instruction → expected outcome evaluation set
├── docs/               research, architecture, modules, environment, roadmap
├── docker-compose.yml  backend (linux/amd64) + nginx frontend
└── Makefile            setup, dev, test, lint, docker
```

`eval/` holds the natural-language → command evaluation set. Planned later:
`workers/` (Chrono, FEA in separate environments).

## Author

Utkarsh Mehta

## License

Not yet chosen. All rights reserved until a licence is added.
