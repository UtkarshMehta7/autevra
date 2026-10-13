import pytest

from autevra.domain.parameters import default_values
from autevra.domain.rules import RULES, check_rules, validate


def _violated(changes: dict[str, float]) -> set[str]:
    p = default_values() | changes
    return {v.rule for v in validate(p)}


@pytest.mark.parametrize(
    ("changes", "rule"),
    [
        ({"body_width": 1700}, "tyres_within_body"),
        (
            {"rim_diameter": 22, "tyre_aspect_ratio": 80, "beltline_height": 800},
            "arch_below_beltline",
        ),
        (
            {
                "front_overhang": 500,
                "rim_diameter": 22,
                "tyre_width": 335,
                "tyre_aspect_ratio": 80,
                "beltline_height": 1400,
                "overall_height": 2100,
                "body_width": 2200,
            },
            "front_overhang_contains_arch",
        ),
        (
            {
                "rear_overhang": 500,
                "rim_diameter": 22,
                "tyre_width": 335,
                "tyre_aspect_ratio": 80,
                "beltline_height": 1400,
                "overall_height": 2100,
                "body_width": 2200,
            },
            "rear_overhang_contains_arch",
        ),
        ({"roof_length": 2600}, "roof_within_cabin"),
        ({"cabin_offset": 900, "cabin_length": 4000, "roof_length": 1500}, "cabin_within_body"),
        ({"overall_height": 1150, "beltline_height": 960}, "cabin_has_height"),
        ({"beltline_height": 700, "ground_clearance": 350, "rail_height": 250}, "body_has_depth"),
        ({"rail_spacing": 1300}, "frame_clears_tyres"),
    ],
)
def test_rule_detects_violation(changes: dict[str, float], rule: str) -> None:
    assert rule in _violated(changes)


def test_every_rule_has_a_violation_test() -> None:
    tested = {
        "tyres_within_body",
        "arch_below_beltline",
        "front_overhang_contains_arch",
        "rear_overhang_contains_arch",
        "roof_within_cabin",
        "cabin_within_body",
        "cabin_has_height",
        "body_has_depth",
        "rail_wall_fits_section",
        "frame_clears_tyres",
        "arches_do_not_overlap",
    }
    assert {r.id for r in RULES} == tested


def test_guard_rules_outside_current_bounds() -> None:
    # With today's registry bounds these two rules cannot fire; they guard wider bounds later.
    p = default_values()
    assert "rail_wall_fits_section" in {
        v.rule for v in check_rules(p | {"rail_wall": 40, "rail_width": 70})
    }
    assert "arches_do_not_overlap" in {v.rule for v in check_rules(p | {"wheelbase": 800})}


def test_bounds_violation() -> None:
    violations = validate(default_values() | {"wheelbase": 5000})
    assert violations[0].rule == "bounds"
    assert violations[0].parameters == ("wheelbase",)


def test_validate_requires_complete_set() -> None:
    p = default_values()
    del p["wheelbase"]
    with pytest.raises(KeyError):
        validate(p)
