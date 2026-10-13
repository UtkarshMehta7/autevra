# Extending Autevra: plugins

A plugin adds engineering content without editing the core: parameters, derived
values, design rules, CAD builders, components placed by mates, clearance
checks and component tests. Once registered, everything it adds takes part in
the same workflows as the built-in model:

| Added | Where it shows up |
|---|---|
| Parameters (`ParameterDef`) | property editor, API catalogue, parser aliases, LLM prompt, commands, undo/redo, requirements |
| Derived values | queries, requirements, the editor |
| Rules | every command is validated against them; previews report them |
| Builders + components | CAD model, viewport, STEP export, dependency graph (rebuild/move), integration checks |
| Clearances | exact OCCT distance checks in the Integration tab |
| Tests (`TestDefinition`) | test bench, stored runs, requirements, diagnosis, optimisation, live retest |

The worked example is [`autevra/contrib/brake_discs.py`](../backend/autevra/contrib/brake_discs.py):
ventilated discs with caliper envelopes on the four hubs, a rule that the disc
and caliper fit inside the rim, and an analytical disc-heating test.

## 1. Enable a plugin

```bash
AUTEVRA_PLUGINS=autevra.contrib.brake_discs make dev
```

or install a package that declares the entry point group:

```toml
# pyproject.toml of your plugin package
[project.entry-points."autevra.plugins"]
my_plugin = "my_package.plugin:PLUGIN"
```

`GET /api/plugins` lists what is loaded and what each plugin added.

## 2. Write one

```python
from autevra.extensions import Plugin

PLUGIN = Plugin(
    name="my_plugin",
    parameters=(...),        # ParameterDef: id, label, group, unit, default, min, max, aliases
    derived=((DerivedDef(...), compute_fn), ...),
    rules=((Rule(...), check_fn), ...),        # check_fn(values) -> message or None
    builders={"my_part": build_my_part},      # inputs -> kernel shape (local frame)
    components=(ComponentDef(...), ...),       # declares geometry deps, frames, a Mate
    clearances=(Clearance(a, b, minimum_mm, reason, parameters), ...),
    tests=(TestDefinition(...),),
)
```

Rules for a good plugin, all enforced or tested:

- **Declare dependencies.** A component's `inputs` and `interfaces` see only
  the parameters listed in `geometry` and `frames`; reading anything else
  raises, so selective rebuilds stay correct.
- **Mate to existing interfaces** (for example an axle's `hub_left`) instead
  of computing absolute positions.
- **Keep the default design valid.** `register` refuses a plugin whose
  defaults break any rule, and rolls everything back.
- **Label credibility honestly.** A closed-form estimate is
  `ANALYTICAL_ESTIMATE`; a time integration is `NUMERICAL_SIMULATION`; never
  `EXPERIMENTALLY_VALIDATED` without measured data.
- **Do not invent pass/fail limits.** Leave `criteria` empty unless the limit
  comes from the design itself; users add requirements.
- **Use the kernel adapter** (`autevra.cad.kernel`) rather than CadQuery directly.

## 3. Test it

Register in a fixture and unregister afterwards (see `backend/tests/test_extensions.py`):

```python
@pytest.fixture
def plugin():
    extensions.register(PLUGIN)
    yield PLUGIN
    extensions.unregister(PLUGIN.name)
```

`register` checks identifier clashes, builder names, mate interfaces, declared
dependencies and the default design before anything becomes visible.
