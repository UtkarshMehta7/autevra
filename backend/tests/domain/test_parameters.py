from autevra.core import parameters
from autevra.core.parameters import GROUP_ALIASES, REGISTRY
from autevra.core.rules import validate


def test_registry_matches_architecture_draft() -> None:
    v = parameters.default_values()
    assert v["wheelbase"] == 2700
    assert v["front_overhang"] == 900
    assert v["rear_overhang"] == 1000
    assert v["rim_diameter"] == 17
    assert v["rail_width"] == 70 and v["rail_height"] == 110
    assert len(REGISTRY) == 77


def test_defaults_lie_within_bounds() -> None:
    for spec in REGISTRY.values():
        assert spec.min <= spec.default <= spec.max, spec.id


def test_default_design_is_valid() -> None:
    assert validate(parameters.default_values()) == []


def test_aliases_are_unique_across_parameters() -> None:
    seen: dict[str, str] = {}
    for spec in REGISTRY.values():
        for alias in spec.aliases:
            assert alias not in seen, f"'{alias}' used by {seen.get(alias)} and {spec.id}"
            seen[alias] = spec.id
    for alias, ids in GROUP_ALIASES.items():
        assert alias not in seen
        assert all(i in REGISTRY for i in ids)
