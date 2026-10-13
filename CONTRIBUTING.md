# Development workflow

Autevra is developed incrementally. Each change should leave the
application in a working, tested state.

## Branches

- `main`: always working and releasable.
- Feature branches: `phase-<n>/<short-topic>`, e.g. `phase-1/command-history`.
- Merge into `main` through a pull request once checks pass.

## Commits

- One logical change per commit, present-tense summary under 72 characters,
  e.g. `Add undo/redo to the command history`.
- Mention the roadmap phase in the body when useful.
- Never commit model weights, generated CAD/simulation outputs, `.env`
  files or databases (see `.gitignore`).

## Definition of done for every change

1. Tests written or updated, and passing.
2. Lint passes.
3. The app still starts and the changed feature was checked by hand.
4. [docs/ROADMAP.md](docs/ROADMAP.md) checkboxes and progress log updated.
5. Any new dependency checked for macOS arm64 support and recorded in
   [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).

## Engineering rules

- All design changes go through typed, validated commands; nothing edits geometry directly.
- AI components only propose commands; they never execute code.
- Simulation models need verification tests against closed-form or reference results before they are shown in the UI, and every result carries a fidelity label.
- Keep the Mac memory budget in mind (8 GB): sequential jobs, small models, lazy loading.
- Do not `pip install pychrono`. That PyPI name belongs to an unrelated package. Use the conda `projectchrono` channel (see ENVIRONMENT.md).

## Commands

Commands for setup, running and testing will be added here in Phase 1
(`make setup`, `make dev`, `make test`, `make docker`).
