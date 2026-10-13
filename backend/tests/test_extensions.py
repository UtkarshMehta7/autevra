"""The extension API: a plugin adds parameters, CAD, rules, checks and tests, and is removable."""

from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from autevra import extensions
from autevra.assembly.model import BY_ID, ComponentDef, Mate
from autevra.contrib import brake_discs
from autevra.core import parameters, rules
from autevra.engineering import testing

pytestmark = pytest.mark.cad


@pytest.fixture
def plugin() -> Iterator[extensions.Plugin]:
    extensions.register(brake_discs.PLUGIN)
    yield brake_discs.PLUGIN
    extensions.unregister(brake_discs.PLUGIN.name)


def test_plugin_extends_every_registry(plugin: extensions.Plugin) -> None:
    from autevra.ai.rule_parser import parse
    from autevra.assembly import graph

    assert "front_disc_diameter" in parameters.REGISTRY
    assert "brake_heat" in testing.DEFINITIONS and "disc_fl" in BY_ID
    assert graph.impact(["front_disc_diameter"]).rebuild == {"disc_fl", "disc_fr"}
    command = parse("increase the front disc diameter by 10 mm").command
    assert command is not None and command.changes[0].parameter == "front_disc_diameter"
    assert "front_disc_fits_rim" in {v.rule for v in rules.validate(
        parameters.default_values() | {"rim_diameter": 15})}  # fmt: skip


def test_plugin_components_build_place_and_clear_the_wheels(plugin: extensions.Plugin) -> None:
    from autevra.api import model_service
    from autevra.cad.cache import GeometryCache
    from autevra.engineering import integration

    model = model_service.build_model(parameters.default_values(), GeometryCache())
    assert {"disc_fl", "disc_rr"} <= {p.id for p in model.parts}
    checks = [c for c in integration.clearance_checks(model) if c.id.startswith("clearance:disc")]
    assert len(checks) == 4 and all(c.status == "pass" for c in checks)
    assert all(c.measured is not None and c.measured > 3 for c in checks)


def test_plugin_test_runs_with_requirements(plugin: extensions.Plugin) -> None:
    run = testing.run_test("brake_heat", "front", "stop_100", parameters.default_values())
    rise = run.metrics["disc_temperature_rise"]["value"]
    assert 20 < rise < 200 and run.credibility is testing.Credibility.ANALYTICAL_ESTIMATE
    thicker = parameters.default_values() | {"front_disc_thickness": 32}
    bigger = testing.run_test("brake_heat", "front", "stop_100", thicker)
    assert bigger.metrics["disc_temperature_rise"]["value"] < rise  # more iron, less heating


def test_unregister_restores_the_core_model() -> None:
    before = (len(parameters.REGISTRY), len(BY_ID), len(rules.RULES), set(testing.DEFINITIONS))
    extensions.register(brake_discs.PLUGIN)
    extensions.unregister(brake_discs.PLUGIN.name)
    after = (len(parameters.REGISTRY), len(BY_ID), len(rules.RULES), set(testing.DEFINITIONS))
    assert after == before


def test_invalid_plugins_are_refused_and_leave_nothing_behind() -> None:
    before = len(parameters.REGISTRY)
    bad_mate = replace(brake_discs.PLUGIN, name="bad_mate", components=(ComponentDef(
        id="ghost", name="Ghost", category="x", builder="brake_disc",
        mate=Mate("front_axle", "no_such_interface", "hub")),))  # fmt: skip
    with pytest.raises(extensions.PluginError, match="unknown interface"):
        extensions.register(bad_mate)
    clash = replace(
        brake_discs.PLUGIN, name="clash", parameters=(parameters.REGISTRY["wheelbase"],)
    )
    with pytest.raises(extensions.PluginError, match="already in use"):
        extensions.register(clash)
    breaks = replace(brake_discs.PLUGIN, name="breaks", parameters=(
        brake_discs.PARAMETERS[0].model_copy(update={"default": 440}),
    ) + brake_discs.PARAMETERS[1:])  # fmt: skip
    with pytest.raises(extensions.PluginError, match="default design breaks"):
        extensions.register(breaks)
    assert len(parameters.REGISTRY) == before and "breaks" not in extensions.LOADED


def test_plugins_load_from_settings(tmp_path: Path) -> None:
    from autevra.config import Settings
    from autevra.main import create_app

    settings = Settings(data_dir=tmp_path, llm_provider="off", plugin_entry_points=False,
                        plugins="autevra.contrib.brake_discs")  # fmt: skip
    try:
        with TestClient(create_app(settings)) as client:
            assert [p["name"] for p in client.get("/api/plugins").json()] == ["brake_discs"]
            ids = [p["id"] for p in client.get("/api/parameters").json()["parameters"]]
            assert "rear_disc_thickness" in ids
            assert any(t["id"] == "brake_heat" for t in client.get("/api/tests").json())
    finally:
        extensions.unregister("brake_discs")
