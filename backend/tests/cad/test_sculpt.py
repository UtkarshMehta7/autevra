import pytest

from autevra.ai.rule_parser import Kind, parse
from autevra.assembly.model import BY_ID
from autevra.cad import kernel as k
from autevra.core.parameters import REGISTRY, default_values
from autevra.core.rules import validate
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import exterior as e
from autevra.domains.automotive import sculpt, spec

pytestmark = pytest.mark.cad


def _inputs(v: dict[str, float]) -> dict[str, float]:
    return BY_ID["body"].resolve_inputs(v)


def _style(name: str) -> float:
    return float(b.BODY_STYLES.index(name))


def test_the_plan_is_full_width_around_the_arches_and_narrower_at_the_ends() -> None:
    p = _inputs(default_values())
    rear, front = -(p["wheelbase"] + p["rear_overhang"]), p["front_overhang"]
    half_w = p["body_width"] / 2
    for x in (sculpt.ARCH_ZONE, 0.0, -p["wheelbase"], -p["wheelbase"] - sculpt.ARCH_ZONE):
        assert sculpt.width_at(p, x, (rear, front)) == pytest.approx(half_w)
    assert sculpt.width_at(p, front, (rear, front)) == pytest.approx(half_w * 0.72)
    assert sculpt.width_at(p, rear, (rear, front)) == pytest.approx(half_w * 0.82)
    waist = sculpt.width_at(p, -p["wheelbase"] / 2, (rear, front))
    assert waist == pytest.approx(half_w - p["haunch"])


@pytest.mark.parametrize(
    ("control", "low", "high"),
    [("haunch", 0.0, 80.0), ("nose_taper", 50.0, 100.0), ("sill_tuck", 0.0, 150.0),
     ("body_roundness", 0.0, 100.0)],
)  # fmt: skip
def test_shape_controls_change_the_body_but_not_its_extents(
    control: str, low: float, high: float
) -> None:
    shapes = []
    for value in (low, high):
        body = b.build_body(_inputs(default_values() | {control: value}))
        assert k.is_valid(body) and k.solid_count(body) == 1
        shapes.append(body)
    flat = [[c for corner in k.bounds(s) for c in corner] for s in shapes]
    assert flat[0] == pytest.approx(flat[1], abs=0.01)  # same design extents
    assert k.volume(shapes[0]) != pytest.approx(k.volume(shapes[1]), rel=1e-3)


def test_more_tumblehome_draws_the_roof_in() -> None:
    v = default_values()
    widths = [b.roof_half_width(_inputs(v | {"tumblehome": t})) for t in (60.0, 200.0)]
    assert widths[1] == pytest.approx(widths[0] - 140.0)


@pytest.mark.parametrize("style", ["estate", "crossover", "mpv", "roadster", "supercar"])
def test_new_styles_build_with_the_design_extents(style: str) -> None:
    p = _inputs(default_values() | {"body_style": _style(style)})
    body = b.build_body(p)
    assert k.is_valid(body) and k.solid_count(body) == 1
    (x0, y0, _), (x1, y1, z1) = k.bounds(body)
    assert x0 == pytest.approx(-(p["wheelbase"] + p["rear_overhang"]), abs=1)
    assert x1 == pytest.approx(p["front_overhang"], abs=1)
    assert y1 - y0 == pytest.approx(p["body_width"], abs=0.01)
    assert z1 == pytest.approx(p["overall_height"], abs=1)


def test_an_estate_carries_its_roof_further_back_than_a_crossover() -> None:
    v = default_values()
    estate = b.body_layout(_inputs(v | {"body_style": _style("estate")}))
    crossover = b.body_layout(_inputs(v | {"body_style": _style("crossover")}))
    assert estate.roof[0] < crossover.roof[0]


def test_a_supercar_has_a_lower_nose_and_a_longer_screen_than_a_coupe() -> None:
    v = default_values() | spec.TEMPLATES["supercar"]
    coupe = b.body_layout(_inputs(v | {"body_style": _style("coupe")}))
    supercar = b.body_layout(_inputs(v | {"body_style": _style("supercar")}))
    # Both noses stay at least 40 mm above the front arch, so "lower" can be equal there.
    assert supercar.profile[3][1] <= coupe.profile[3][1]
    assert supercar.glass[1] - supercar.roof[1] > coupe.glass[1] - coupe.roof[1]
    assert supercar.glass[0] < coupe.glass[0] or supercar.roof[0] != coupe.roof[0]


def test_a_roadster_is_open_with_only_a_windscreen() -> None:
    v = default_values() | {"body_style": _style("roadster")}
    layout = b.body_layout(_inputs(v))
    assert layout.open
    glass = b.build_glass(BY_ID["glass"].resolve_inputs(v))
    (gx0, _, _), _ = k.bounds(glass)
    assert gx0 >= layout.roof[1] - b.PILLAR - 2  # nothing behind the windscreen header
    for option, value in (("roof_rails", 1.0), ("rear_spoiler", 1.0), ("roof_type", 1.0)):
        assert any(r.rule == "roof_options_need_a_roof" for r in validate(v | {option: value}))
    assert e.build_roof_rails(BY_ID["roof_rails"].resolve_inputs(v | {"roof_rails": 1.0})) is None


@pytest.mark.parametrize("template", ["estate", "crossover", "mpv", "roadster", "supercar"])
def test_new_templates_obey_the_rules(template: str) -> None:
    v = default_values() | spec.TEMPLATES[template]
    assert not validate(v)
    assert b.body_style(v) == b.BODY_STYLES[int(v["body_style"])]


@pytest.mark.parametrize(
    ("text", "style"),
    [("make it a roadster", "Roadster"), ("make it a convertible", "Roadster"),
     ("make it a supercar", "Supercar"), ("make it an estate", "Estate"),
     ("make it a station wagon", "Estate"), ("make it a crossover", "Crossover"),
     ("make it an mpv", "MPV"), ("make it a minivan", "MPV")],
)  # fmt: skip
def test_style_phrases(text: str, style: str) -> None:
    result = parse(text)
    assert result.kind is Kind.COMMAND, (text, result.question)
    assert result.command is not None
    (change,) = result.command.changes
    assert REGISTRY["body_style"].options[int(change.value)] == style
