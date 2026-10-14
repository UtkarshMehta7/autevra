import pytest

from autevra.core.parameters import default_values
from autevra.core.rules import RULES, check_rules, validate


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
        ({"cg_height": 1000}, "cg_within_body"),
        ({"seat_rows": 3}, "seat_rows_fit"),
        ({"powertrain_type": 2, "battery_capacity": 90}, "battery_under_floor"),
        ({"body_style": 2, "rear_spoiler": 3}, "boot_spoiler_needs_a_boot"),
        ({"body_style": 10, "roof_rails": 1}, "roof_options_need_a_roof"),
        ({"front_shock_mount_height": 1000, "beltline_height": 1300, "overall_height": 1800},
         "front_damper_fits_mounts"),
        ({"rear_shock_mount_height": 560}, "rear_damper_fits_mounts"),
        ({"front_bump_travel": 100}, "front_stroke_covers_travel"),
        ({"rear_rebound_travel": 100}, "rear_stroke_covers_travel"),
        ({"beltline_height": 700}, "front_shock_mount_inside_body"),
        ({"beltline_height": 700}, "rear_shock_mount_inside_body"),
        ({"rail_spacing": 1260}, "front_springs_clear_tyres"),
        ({"rail_spacing": 1260}, "rear_springs_clear_tyres"),
        ({"front_spring_rate": 5}, "front_spring_index"),
        ({"rear_spring_rate": 5}, "rear_spring_index"),
        ({"front_spring_rate": 150, "spring_coil_diameter": 200}, "front_spring_clears_coil_bind"),
        ({"rear_spring_rate": 150, "spring_coil_diameter": 200}, "rear_spring_clears_coil_bind"),
        ({"vehicle_mass": 600, "front_mass_distribution": 30, "front_unsprung_mass": 150},
         "front_positive_sprung_mass"),
        ({"vehicle_mass": 600, "front_mass_distribution": 70, "rear_unsprung_mass": 150},
         "rear_positive_sprung_mass"),
    ],
)  # fmt: skip
def test_rule_detects_violation(changes: dict[str, float], rule: str) -> None:
    assert rule in _violated(changes)


def test_every_rule_has_a_violation_test() -> None:
    tested = {
        "tyres_within_body",
        "seat_rows_fit",
        "battery_under_floor",
        "boot_spoiler_needs_a_boot",
        "roof_options_need_a_roof",
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
        "cg_within_body",
        *(
            f"{axle}_{rule}"
            for axle in ("front", "rear")
            for rule in ("damper_fits_mounts", "stroke_covers_travel", "shock_mount_inside_body",
                         "springs_clear_tyres", "spring_index", "spring_clears_coil_bind",
                         "positive_sprung_mass")
        ),
    }  # fmt: skip
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
