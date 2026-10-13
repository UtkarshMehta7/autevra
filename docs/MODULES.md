# How the modules work

This file explains each implemented backend module. It grows with each step;
[ARCHITECTURE.md](ARCHITECTURE.md) holds the overall design.

## `autevra.domain` — the engineering core (imports nothing else from Autevra)

### `units`
Three dimensions, each with a base unit: length (mm), angle (deg), ratio (%).
`convert(value, from_unit, to_unit)` goes through the base unit and refuses
cross-dimension conversions. `parse_unit` accepts spellings such as
`millimetres`, `"`, `°` and `percent`.

### `parameters`
`REGISTRY` maps each parameter ID to a frozen `ParameterDef` (label, group,
unit, default, min, max, step, description, language aliases and
increase/decrease words). It is the single list of editable parameters;
commands, the parser, the API and the future LLM schema all derive from it.
`GROUP_ALIASES` lets one word address several parameters ("track" → front
and rear track).

### `derived`
Read-only values computed from parameters, for example
`overall_length = front_overhang + wheelbase + rear_overhang` and
`tyre_diameter = rim × 25.4 + 2 × width × aspect / 100`. Each entry in
`DERIVED` lists the parameters that control it, so a request such as "make
it longer" can be answered with a clarification.

### `rules`
`validate(values)` returns every violation for a complete parameter set:
registry bounds first, then the cross-parameter rules (tyres inside body
width, arch top below the beltline, overhangs contain the arches, roof ≤
cabin, cabin inside the body, minimum cabin and body depth, rail wall less
than half the section, frame rails clear the tyres). Each violation names the
rule and the parameters involved.

### `commands`
A `SetParameters` command holds one or more `Change`s
(`parameter`, `operation`, `value`, optional `unit`) plus its `source`
(`ui`, `api`, `rules`, `llm`) and the original instruction. `resolve` turns
the changes into absolute values in each parameter's unit:

| Operation | Meaning |
|---|---|
| `set` | the value (converted to the parameter's unit) becomes the new value |
| `increase` / `decrease` | add or subtract; `%` on a non-ratio parameter means relative (+5 % → × 1.05), on a ratio parameter it means percentage points |
| `scale` | multiply by a unitless factor |

Changes apply in order, so two changes to one parameter compound.

### `design`
`DesignState` holds the current values, the history and a cursor. `apply`
resolves a command, validates the **whole** resulting parameter set and
either rejects it (`CommandRejectedError` with the violations, state untouched)
or records a `HistoryEntry` with the exact old and new value of each changed
parameter. `undo` and `redo` restore those recorded values, so they are exact
even after relative changes. A new command discards the redo branch.
`replay()` recomputes the values from defaults plus applied history; tests
assert it always equals the current values.

## `autevra.cad` — geometry

### `kernel`
The only module that imports CadQuery/OCP. It exposes primitive solids
(boxes, Y/X cylinders, rings, open rectangular tubes, ruled lofts), booleans
with validity checks, fillets, tight bounding boxes, volume, tessellation to
flat vertex/index arrays, and STEP export of named, placed, coloured parts.

### `components`
Pure builders `inputs → solid`, each in its own local frame:

| Builder | Inputs | Geometry |
|---|---|---|
| `build_body` | overhangs, wheelbase, width, heights, cabin, tracks, tyre and arch sizes | box lower body from floor to beltline with four wheel wells cut around the wheels, fused with a ruled-loft cabin from beltline to roof |
| `build_frame` | overhangs, wheelbase, rail spacing and section, ground clearance | two open hollow rectangular rails and five hollow cross members, fused into one solid |
| `build_axle` | track | beam axle along Y ending 60 mm inboard of each wheel plane |
| `build_wheel` | tyre radius, rim radius, tyre width | filleted tyre ring, rim barrel and a five-hole disc with a hub bore |

### `cache`
`GeometryCache` builds a shape only when (builder, inputs) hashes to a new
key; a bounded LRU (64 entries) keeps memory low, and each key is tessellated
once.

## `autevra.assembly` — placement and dependencies (imports only `domain`)

### `transforms`
Plain NumPy 4×4 rigid transforms: identity, translation, rotation about Z,
composition and inverse.

### `vehicle`
The Phase 1 vehicle as data. Each `ComponentDef` names its builder, declares
the parameters its **geometry** depends on, declares per **interface** (named
coordinate frame) the parameters that frame depends on, and has one `Mate`
to a parent:

```
vehicle ─origin──────────── body, frame
        ─front_axle_mount── front_axle ─hub_left── wheel_fl
        │                              ─hub_right─ wheel_fr (turned 180° about Z)
        ─rear_axle_mount─── rear_axle  ─hub_left── wheel_rl
                                       ─hub_right─ wheel_rr
```

Input and interface functions only see a `DeclaredView` of the design, which
raises `UndeclaredDependencyError` if they read a parameter they did not
declare, so the dependency graph cannot silently go stale.

### `graph`
`place_all(values)` computes each world matrix as
`world(parent) · parent_interface · inverse(child_interface)`.
`impact(changed)` returns the components whose geometry must be rebuilt and
those that only move. For the wheelbase: rebuild body and frame; move the rear
axle and rear wheels.

## `autevra.ai` — language → commands (imports only `domain`)

### `lexicon`
Builds one alias table from the registry (aliases, labels, IDs), the group
aliases and the derived values, and refuses ambiguous aliases. It also holds
the increase/decrease/set verbs, comparatives ("wider" → body width up,
"longer" → overall length) and adjectives ("1.9 m wide").

### `rule_parser`
`parse(text)` returns an `Interpretation`: a `command`, `undo`, `redo`, a
`query` (parameter or derived IDs), or a `clarification` with suggestions.
Steps: normalise (case, `tire` → `tyre`, `18s` → `18`, `18 inch wheels` →
rims, `the car` → `it`); detect undo/redo and questions; split compound
requests on "and", commas, "then"; per clause match the longest alias, detect
the operation ("to <number>" means set), extract the quantity and unit (bare
numbers use the parameter's unit and are reported as assumptions); later
clauses without a verb inherit the previous operation. Derived targets,
missing amounts and unknown words produce clarifying questions (with
`difflib` suggestions for typos). The parser never applies anything itself.

## `autevra.storage` — persistence

- `models`: `projects` (current values as JSON, history cursor) and
  `history_entries` (one row per command, ordered by `seq`, including the
  undone redo branch).
- `database`: engine creation (SQLite foreign keys on), sessions, and
  `migrate(url)`, which runs Alembic to `head` on app start.
- `repository`: `ProjectRepository.load/save` convert between rows and
  `DesignState`; `save` keeps the unchanged prefix of the history and
  rewrites only the rest.

Swapping to PostgreSQL later means changing `AUTEVRA_DATABASE_URL`; the models
and migrations are dialect-neutral (`render_as_batch` for SQLite ALTERs).

## `autevra.api` — HTTP and wiring

- `service.Workspace` is the only place where parser, commands, persistence
  and CAD meet. Mutations and CAD builds run under one lock (sequential, low
  memory). Instructions from the deterministic parser are applied directly;
  rule violations come back as `kind: "rejected"` with the violations.
- `model_service` builds the model (placement from `assembly`, shapes from the
  CAD cache), produces the mesh payload (de-duplicated geometries plus one
  4×4 matrix per part), and exports STEP with one named, placed part per
  component.
- `routes` (all under `/api`):

| Method and path | Purpose |
|---|---|
| `GET /parameters` | registry and derived-value definitions |
| `GET/POST /projects`, `GET/PATCH/DELETE /projects/{id}` | projects (state includes values, derived values, undo/redo availability) |
| `POST /projects/{id}/commands` | apply a typed `SetParameters` command; 422 with violations if rejected |
| `POST /projects/{id}/instructions` | plain-English instruction → command / query / clarification / undo / redo |
| `POST /projects/{id}/undo`, `/redo` | step through history |
| `GET /projects/{id}/history` | entries and cursor |
| `GET /projects/{id}/model?known=k1,k2` | meshes and transforms, skipping geometry keys the client already has |
| `GET /projects/{id}/export.step` | STEP AP214 assembly file |

| `GET /tests` | component test catalogue: scenarios, criteria, inputs, metrics, assumptions |
| `POST /projects/{id}/tests/run` | run a test (`target` front, rear or all; one scenario or all); stored and compared with the previous revision |
| `GET /projects/{id}/runs`, `/runs/{run}`, `/runs/compare?baseline=&candidate=` | run summaries (with `current`), full records, comparisons |
| `GET /projects/{id}/runs/{run}/diagnosis` | evidence-based diagnosis of a run |
| `GET /projects/{id}/components/status` | per component: passed, failed, stale, not tested, … |
| `GET/POST/DELETE /projects/{id}/requirements` | user criteria that join test verdicts |
| `GET /projects/{id}/integration` | assembly checks |
| `POST /projects/{id}/optimize`, `POST /projects/{id}/loop` | optimisation study, engineering loop |
| `GET /projects/{id}/studies`, `/loops`; `POST /studies/{s}/accept`, `/reject`, `/choose/{i}` | decisions on proposals (accept applies one undoable command) |

## `autevra.sim` — solvers (imports nothing from Autevra)

`quarter_car`: one corner as two masses. Linear spring, two-rate damper (bump
in compression, rebound in extension), point-contact tyre that can lift off
but not pull. States are displacements from static equilibrium; fixed-step
RK4, then a rerun at half the step measures convergence (`numerics`). Road
inputs: half-cosine step, cosine bump and pothole at constant speed. Metrics:
peak and RMS body acceleration, bump and rebound travel, tyre load ratio and
time off the road, settling time, step overshoot. `ASSUMPTIONS` travel with
every result. Verified in `tests/sim` against the exact linear solution
(matrix exponential), the characteristic equation and static equilibrium.

## `autevra.engineering` — tests, integration, diagnosis, optimisation, loop

- `integration`: structural checks (mate interfaces and kinds, connectivity,
  coincidences such as damper upper eye on the shock tower, load paths
  wheel → axle → damper → body), travel checks (which limit governs: bump
  stop, wheel arch or damper length), and exact clearances between placed
  solids (`kernel.min_distance`, cached). Not checked, and said so: parts
  inside the body envelope.
- `testing`: `TestDefinition` (solver, inputs read, scenarios, criteria with
  fixed limits or limits taken from derived values, credibility), `run_test`
  → `RunRecord` (revision with a hash of only the inputs this test reads, so
  results go stale exactly when they should), `evaluate`, `compare`,
  `tests_affected`, `quick_evaluate` for perturbation studies. Statuses:
  passed within the model, failed, no criteria, invalid; components can also
  be stale or not tested. Nothing is marked experimentally validated
  automatically.
- `diagnosis`: for each failed criterion, the limit source, ±10 % re-simulation
  of every input, ranked effects with side effects, smallest rule-checked fix
  up to ±30 %. A saturated tyre-contact margin is probed through time off the
  road. Effects are labelled as measured in the model, not root causes.
- `optimize`: `Study` (variables with bounds, one or two objectives, scenarios,
  budget, seed) → seeded Latin hypercube + compass search; rule screening
  before simulation; feasibility = all criteria pass in all scenarios;
  worst-case objectives; Pareto set for two objectives; full re-verification
  of the proposal.
- `loop`: `Goal` → iterations of full test runs, diagnosis and the smallest
  admissible fix, until all pass, no admissible fix exists, or the limit;
  optional final optimisation. Candidate designs stay in the record until
  accepted.

## Frontend (`frontend/src`)

- `api/` — typed client mirroring the backend schemas.
- `viewport/Viewport.tsx` — plain three.js with ISO 8855 axes (`camera.up =
  Z`), orbit controls, a ground grid in the XY plane, click picking, x-ray body,
  and highlighting of selected and just-affected parts. Geometry is cached by
  key and shared across parts (four wheels, one buffer); unused geometry stays
  in a 16-entry LRU so undo/redo reuse it.
- `panels/` — component tree, property editor (one `set` command per edit,
  source `ui`), instruction panel (shows assumptions, impact, clickable
  suggestions), history (undone entries struck through).
- `panels/TestBench.tsx`, `LineChart.tsx`, `DiagnosisView.tsx` — test runs,
  criteria with margins, solver traces (SVG, real samples only) with limits
  and the previous revision, comparisons, diagnosis with Apply.
- `panels/IntegrationPanel.tsx`, `panels/StudiesPanel.tsx` — assembly checks;
  optimisation and loop set-up, candidate scatter, Pareto choice, accept or
  reject.
- `App.tsx` — runs all actions through one sequential queue, so instructions
  typed during a rebuild are applied in order; then refetches project,
  history and model.

## Phase 2: local LLM fallback

### `autevra.ai.concepts`
Automotive concepts behind vague requests. Suspension is modelled (Phase 3)
but "make the suspension softer" is ambiguous, so it gets a question with
runnable suggestions; brakes, engine, transmission, steering system and
appearance are not modelled yet. A request
about one of them gets a specific, deterministic answer instead of a guess:
"make the suspension softer" asks whether that means spring rate, bump
damping or rebound damping. `is_automotive(text)` is a conservative scope check: text with no
automotive vocabulary, design verbs or numbers is declined without calling
any model.

### `autevra.ai.interpreter`
The single entry point for instruction text. Escalation policy:

1. The rule parser runs first. Its commands, queries and its clarifying
   questions about derived values or missing amounts are final.
2. If the parser found no target (`Reason.NO_TARGET`), an unmodelled concept
   gets its deterministic question, and off-topic text is declined.
3. Only then is the local LLM asked, with a registry-derived JSON schema.
4. The answer is validated: Pydantic shape, registry IDs, unit dimensions,
   positive scale factors, then **grounding** against the user's words:
   - every value must be a number the user wrote (digits or number words);
     scale factors must be such a number, follow from a percentage, or come
     from "double"/"halve";
   - "to N" makes the operation absolute; "by N" relative, with the direction
     taken from the user's verb (no verb → ask);
   - a bare amount without relative wording ("I want 18 inch alloys") is
     absolute;
   - the unit written next to the number overrides the model's unit.
5. A valid result becomes a `PROPOSAL` (never a command). Undo/redo from the
   model become suggestions. If the model is off, unreachable or returns
   garbage, the parser's own question is returned with a note.

The parser also refuses to guess on its own: when it would have to guess the
operation or fall back to a "make it lower" shortcut, every remaining word must
be understood. "Slide the cabin 100 mm forward" or "drop the window line by
40 mm" therefore escalate instead of changing the cabin length or the ground
clearance.

### `autevra.ai.llm`
- `schema.proposal_schema()` — JSON schema with enums from the registry
  (`action`, `changes[{parameter, operation, value, unit}]`, `query`,
  `question`), used for constrained decoding.
- `prompt.messages(text, values)` — system prompt with the rules, a table of
  every parameter (unit, current value, range, description, aliases), the
  derived values, and five few-shot examples; temperature 0.
- `clients` — `OllamaClient` (`/api/chat` with `format`, `think: false`,
  retried without `think` for runtimes that reject it), `LlamaServerClient`
  (`/v1/chat/completions` with `response_format`), `DisabledClient`, and
  `make_client`. Connect timeout 2 s, so a stopped runtime fails fast.

### `autevra.ai.evaluate`
Scores interpretation on `eval/instructions.jsonl` (see `eval/README.md`).
Outcomes: `PASS`; `MISS` (a question, a decline, or a change validation would
refuse anyway); `WRONG` (a valid-looking wrong change that only the user's
confirmation would stop, counted as `wrong_but_valid`).

### API additions
| Method and path | Purpose |
|---|---|
| `POST /projects/{id}/instructions` | may now return `kind: "proposal"` (with `proposal_id` and `preview`) or `"out_of_scope"`; `interpreted_by` is `rules` or `llm` |
| `POST /projects/{id}/proposals/{pid}/confirm` | apply the proposal through the normal validated command path (history source `llm`) |
| `POST /projects/{id}/proposals/{pid}/reject` | discard it |
| `GET /llm` | provider, model, availability and installed models |

Proposals live in memory for 15 minutes, can be used once, belong to one
project, and are re-validated against the design when confirmed. A proposal
that already breaks a design rule is returned as `rejected` straight away.

### Frontend
The instruction panel header shows the LLM state (polled every 30 s). LLM
replies carry an `LLM` badge; proposals show **Confirm** and **Reject**, and
nothing changes in the model until Confirm.
