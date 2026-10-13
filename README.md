# Autevra

**Intent-based AI engineering platform for automotive design and simulation.**

Describe what you want in plain language, and Autevra designs, modifies,
integrates and tests **real, editable 3D CAD components** of a vehicle.
It is not an image generator and not a generic chatbot: every instruction
becomes a validated engineering operation on parametric geometry.

> "Increase the wheelbase by 100 mm."
> "Set the rims to 18 inch and check the front wheels still clear the frame at full lock."
> "Run an emergency stop from 100 km/h and tell me if it stops within 40 m."

---

## Status

**Phase 1 (foundation prototype) is implemented.** A parametric vehicle
(body with wheel wells and cabin, hollow ladder frame, axles, wheels) is
edited through typed, validated commands from the property editor, the API or
plain-English instructions, with undo/redo, persistence and STEP export.
"Increase the wheelbase by 100 mm" moves the rear axle and wheels back,
lengthens the body and frame, and is reflected in the STEP file; undo restores
it. See [docs/ROADMAP.md](docs/ROADMAP.md) for progress and what is next.

| Document | Contents |
|---|---|
| [docs/RESEARCH.md](docs/RESEARCH.md) | Resources, options and recommendations for CAD, local AI, simulation, frontend, backend, deployment, plus product possibilities and reference material |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Proposed modules, data model, NL pipeline, repository layout, path to AWS |
| [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) | Environment inspection, verified Apple Silicon compatibility matrix, risks and memory budget |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phased implementation plan and progress log (completed and remaining work) |
| [docs/MODULES.md](docs/MODULES.md) | How each implemented module works |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development workflow, branch and commit conventions |

## Core capabilities (planned)

1. **Automotive AI, fully local**: a deterministic automotive command parser plus an optional small quantised LLM (Ollama or llama.cpp). No hosted AI APIs.
2. **Specification interview**: adaptive questions on vehicle type, powertrain, power, torque, dimensions, drivetrain, materials, suspension, budget and use, with conflict detection.
3. **Real parametric CAD**: B-rep geometry on Open CASCADE (via CadQuery), exportable to STEP.
4. **Natural-language editing**: instructions become validated commands with feature history, undo and redo.
5. **Component integration**: a connected assembly with interfaces, coordinate frames, dependencies and clearance checks; only affected components are rebuilt.
6. **Engineering simulation**: acceleration, braking, cornering, steering, suspension, potholes, powertrain, tyres; later structural, thermal, fatigue, aero and crash.
7. **Simulation automation**: describe a test in words, run it, compare against requirements, get suggested design changes, with results clearly labelled `estimate`, `verified` or `validated`.
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
"how long is the car?" or "undo". The first start after installing can take a
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

Optional, for Phase 2: `brew install ollama && ollama pull qwen2.5:1.5b`
(about 1 GB). The app does not need it. Docker Desktop is optional too: daily
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
├── docs/               research, architecture, modules, environment, roadmap
├── docker-compose.yml  backend (linux/amd64) + nginx frontend
└── Makefile            setup, dev, test, lint, docker
```

Planned later: `workers/` (Chrono, FEA in separate environments) and `eval/`
(natural-language → command evaluation sets, Phase 2).

## Author

Utkarsh Mehta

## License

Not yet chosen. All rights reserved until a licence is added.
