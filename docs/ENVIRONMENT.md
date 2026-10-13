# Environment inspection and platform compatibility

This file records what was inspected before any code was written, and which
technology choices were **verified** (not assumed) to work on the target
hardware. Re-run the checks when dependency versions change.

## 1. Repository state (inspected 2026-10-13)

- Remote: `github.com/UtkarshMehta7/autevra`
- The repository was empty: no commits, no files, no existing implementation.
- Nothing needed to be migrated or preserved.

## 2. Two different machines

| | Target development machine | Inspection machine used for this phase |
|---|---|---|
| Hardware | Apple Mac M2, 8 GB unified memory, 256 GB SSD | Linux x86_64 cloud container, 4 vCPU, 15 GB RAM |
| OS / arch | macOS, `arm64` | Ubuntu 24.04, `x86_64` |
| Purpose | Daily development | Research, package verification, documentation |

Everything below about the Mac was checked by asking the package indexes
for **macOS arm64 binaries** (`pip download --platform macosx_14_0_arm64`)
and the conda channels for `osx-arm64` builds. This is strong evidence that
the packages install, but it is not the same as running them on the Mac.
The first step of Phase 1 is a smoke test on the Mac itself.

### Tools found in the inspection container

| Tool | Version |
|---|---|
| Python | 3.13.16 (3.12 available through `uv`) |
| uv | 0.11.32 |
| Node.js / npm / pnpm | 22.22.0 / 10.9.4 / 10.28.0 |
| Docker | 29.8.2 (Compose plugin not installed as `docker-compose`) |
| Git | 2.43.0 |
| Ollama, conda | not installed |

### Tools to install on the Mac (when Phase 1 starts)

| Tool | Why | Install |
|---|---|---|
| Homebrew | package manager | https://brew.sh |
| uv | fast Python + virtualenv manager; installs Python 3.12 | `brew install uv` |
| Node.js 22 LTS | frontend toolchain | `brew install node@22` |
| Git | version control | ships with Xcode CLT: `xcode-select --install` |
| Ollama (optional) | local LLM runtime with Metal acceleration | `brew install ollama` |
| Docker Desktop (optional) | packaging checks; not needed for daily dev | https://www.docker.com/products/docker-desktop |
| Miniforge (later, Phase 8) | only for Project Chrono, which ships via conda | `brew install miniforge` |

## 3. Verified compatibility matrix

Legend: ✅ binary available and/or run successfully, ⚠️ works with a caveat, ❌ not available.

### CAD

| Package | macOS arm64 (native) | Linux arm64 (Docker on Mac) | Linux x86_64 (Docker / AWS) | Notes |
|---|---|---|---|---|
| `cadquery==2.8.0` + `cadquery-ocp 7.9.3` | ✅ wheels | ❌ no `cadquery-ocp 7.9.x` wheel | ✅ installed and ran (fillets, STEP export) | full install = **1.7 GB** (VTK 638 MB, casadi 262 MB) |
| `cadquery-ocp 8.0.1` | ✅ | ✅ | ✅ | **incompatible with CadQuery 2.8.0**: `ImportError: TColgp_HArray1OfPnt` (tested) |
| `cadquery-ocp-novtk 8.0.1` | ✅ | ✅ | ✅ | slim OCP build, but same CadQuery 2.8 incompatibility |
| `build123d 0.13.0` | ✅ (pure Python on OCP) | depends on OCP | ✅ | alternative API on the same kernel |
| `gmsh 4.15.2` | ✅ | ✅ | ✅ | meshing for FEA |
| `manifold3d 3.5.4` | ✅ | ✅ | ✅ | fast mesh booleans (not B-rep) |

Measured: `import cadquery` takes about 2.4 s warm (8 s on the first, cold
import), and a filleted box builds in milliseconds.

### Local AI

| Package | macOS arm64 | Notes |
|---|---|---|
| Ollama | ✅ native app, Metal GPU | the GPU is **not** reachable from Docker on macOS, so run it natively |
| `ollama` Python client 0.6.3 | ✅ | thin HTTP client; plain `httpx` works too |
| `llama-cpp-python 0.3.36` | ⚠️ source only | compiles with Metal; needs Xcode CLT and a few minutes |
| llama.cpp `llama-server` | ✅ `brew install llama.cpp` | same engine as Ollama, OpenAI-compatible HTTP API |
| `mlx 0.32.3`, `mlx-lm 0.32.0` | ✅ | Apple-only; fastest on M-series, also supports LoRA fine-tuning |

### Simulation and analysis

| Package | macOS arm64 | Notes |
|---|---|---|
| **Project Chrono / PyChrono** | ✅ conda `projectchrono` channel: 9.0.1 (py3.12, py3.13) | linux-64: 9.0.1; linux-aarch64: 10.0.0. **Not on PyPI** (see warning below) |
| `scikit-fem 12.0.2` | ✅ pure Python | small FEA problems, good for validation |
| `fmpy 0.3.32` | ✅ | run FMI/FMU models (e.g. exported from Modelica) |
| `rainflow 3.2.0` | ✅ | fatigue cycle counting |
| `openseespy 3.8.0.0` | ✅ | structural analysis (frames, beams) |
| `pyvista 0.49.1`, `trimesh 5.1.1` | ✅ | mesh processing / post-processing |

> **⚠️ Package-name collision:** `pip install pychrono` installs an unrelated
> 10 KB "timing utilities" package (version 1.1.0, by a different author),
> **not** Project Chrono. The real PyChrono must come from conda:
> `conda install -c projectchrono -c conda-forge pychrono`. Never add
> `pychrono` to a pip requirements file.

### Frontend (npm, current versions)

| Package | Version | Use |
|---|---|---|
| `three` | 0.186.1 | 3D rendering |
| `@react-three/fiber` / `@react-three/drei` | 9.8.1 / 10.7.9 | React bindings + helpers (optional) |
| `three-mesh-bvh` | 0.9.16 | fast picking/raycasting on large meshes |
| `react` | 19.3.0 | UI |
| `vite` | 8.3.4 | dev server / bundler |
| `typescript` | 7.0.2 | type checking |
| `uplot` | 1.6.32 | high-rate telemetry plots |
| `echarts` | 6.1.0 | report charts |
| `occt-import-js` | 0.0.23 | view STEP files directly in the browser (WASM) |

## 3a. Verified on the Mac (2026-10-13)

| Item | Result |
|---|---|
| Machine | Apple M2, 8 GB, macOS 27.0 (arm64), ~28 GB free disk |
| uv / Python | uv 0.12.19; Python 3.12.14 (Homebrew) used by the venv |
| Node.js / npm | 22.23.2 / 10.9.8 |
| Docker, Ollama | **not installed**; Docker is only needed for packaging checks, Ollama for Phase 2 |
| `cadquery 2.8.0` + `cadquery-ocp 7.9.3.1.1` | ✅ native arm64 wheels; build, fillet, STEP export and re-import pass |
| Backend venv size | 1.3 GB (`backend/.venv`) |
| First test run | ~2.5 min: macOS scans the newly installed native libraries on first load; later runs take ~4 s |
| FastAPI 0.143, Pydantic 2.14, SQLAlchemy 2.1, Alembic 1.20, Uvicorn 0.54, pytest 9.1, ruff 0.17 | ✅ pure Python or arm64 wheels |
| `httpx 0.28` (test client) | ✅; Starlette 1.8 prefers `httpx2` (pure-Python wheel) and warns about `httpx` |

Gotcha: if `import autevra` fails in tests after the first `uv sync`, run
`uv sync --reinstall-package autevra` to rewrite the editable-install `.pth` file.

## 4. Apple Silicon compatibility risks

| # | Risk | Impact | Mitigation |
|---|---|---|---|
| R1 | CadQuery 2.8 needs `cadquery-ocp < 8.0`, and 7.9.x has **no Linux arm64 wheel** | A native-arm64 Docker image of the CAD backend cannot be built today | Run the backend **natively** on the Mac for development (lighter anyway). Build the Docker image for `linux/amd64`: it runs on the Mac through Docker Desktop's Rosetta emulation and matches AWS Fargate x86_64. Move to arm64/Graviton when CadQuery supports OCP 8. Keep all kernel calls behind one adapter module so the switch is local. |
| R2 | Docker on macOS has **no GPU passthrough** | LLM in a container would run CPU-only and slowly | Run Ollama or llama-server natively; containers reach it at `host.docker.internal:11434`. |
| R3 | 8 GB unified memory shared by OS, browser, IDE, backend, LLM | Swapping, slow UI | Memory budget below; LLM optional and loaded on demand; sequential simulation jobs; no LLM model above ~4B parameters. |
| R4 | Project Chrono is **conda-only** | Cannot share the uv/pip environment | Run Chrono as a separate **simulation worker** process in its own conda env, talking to the API through a job queue. The core app never imports it. |
| R5 | PyPI name collision for `pychrono` | Silent wrong install | Documented above; enforced in requirements review. |
| R6 | CadQuery full install is 1.7 GB per venv | 256 GB SSD fills with duplicate venvs/images | One venv per project; prune Docker images (`docker system prune`); later evaluate a slim install without VTK. |
| R7 | `llama-cpp-python` needs a native compile | Fragile setup | Prefer Ollama or `brew install llama.cpp` (pre-built). |
| R8 | Heavy solvers (OpenFOAM, Code_Aster, OpenRadioss) have no native macOS arm64 builds or need Docker | Long runtimes, large images | Defer to later phases; prefer simplified validated models first; run heavy solvers as optional containerised workers or in the cloud. |
| R9 | Rosetta-emulated amd64 containers are slower | Slower Docker-based tests | Docker only for packaging/integration checks; daily dev native. |

## 5. Memory budget on an 8 GB M2 (estimates)

| Component | Approx. RAM |
|---|---|
| macOS + browser + editor | 3.0–4.0 GB |
| FastAPI backend with OCCT, simple vehicle | 0.3–0.6 GB |
| Vite dev server | 0.2–0.3 GB |
| LLM, 1.5B parameters, Q4 quantised | ~1.0–1.3 GB |
| LLM, 3–4B parameters, Q4 quantised | ~2.2–2.8 GB |
| Simulation worker (custom models) | 0.1–0.3 GB |

**Conclusion:** a 1.5B–2B model fits comfortably, a 3–4B model fits if the
browser is kept lean, and 7B+ models do not fit alongside the rest of the
stack. The deterministic command parser needs no model at all, so the
platform remains fully usable when the LLM is switched off.

## 6. Network notes for the inspection container

The cloud container's network policy blocked `ollama.com`,
`registry.ollama.ai` and `huggingface.co`, so no model weights were
downloaded or run there. PyPI, npm, GitHub and the conda channels were
reachable. Live LLM tests will run on the Mac.
