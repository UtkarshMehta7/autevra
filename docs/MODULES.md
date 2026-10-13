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
