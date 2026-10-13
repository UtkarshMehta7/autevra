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

**Phase 0 (research and planning) is complete.** There is no application
code yet. The repository holds the research, architecture, compatibility
findings and phased plan that the implementation will follow.

| Document | Contents |
|---|---|
| [docs/RESEARCH.md](docs/RESEARCH.md) | Resources, options and recommendations for CAD, local AI, simulation, frontend, backend, deployment, plus product possibilities and reference material |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Proposed modules, data model, NL pipeline, repository layout, path to AWS |
| [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) | Environment inspection, verified Apple Silicon compatibility matrix, risks and memory budget |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phased implementation plan and progress log (completed and remaining work) |
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

The application code arrives in Phase 1. To prepare the machine now:

```bash
# Developer tools
xcode-select --install                 # Git and compilers
brew install uv node@22                # Python manager and Node.js 22

# Get the repository
git clone https://github.com/UtkarshMehta7/autevra.git ~/Downloads/autevra
cd ~/Downloads/autevra

# Optional: local LLM runtime (native, uses the Metal GPU)
brew install ollama
ollama pull qwen2.5:1.5b               # about 1 GB download
```

Docker Desktop is optional for daily development. See
[docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for why the backend runs natively
on the Mac and why its container image targets `linux/amd64` for now.

## Repository layout (planned)

```
autevra/
├── backend/      FastAPI app: domain, cad, assembly, ai, simulation, storage
├── frontend/     React + three.js workspace
├── workers/      separate-environment solvers (Chrono, FEA) — later
├── eval/         natural-language → command evaluation sets — Phase 2
└── docs/         research, architecture, environment, roadmap
```

## Author

Utkarsh Mehta

## License

Not yet chosen. All rights reserved until a licence is added.
