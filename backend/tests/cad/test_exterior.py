import pytest

from autevra.ai.rule_parser import Kind, parse
from autevra.assembly.model import BY_ID
from autevra.cad import kernel as k
from autevra.core.parameters import REGISTRY, default_values
from autevra.core.rules import validate
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import derived as d
from autevra.domains.automotive import exterior as e
from autevra.domains.automotive import spec

pytestmark = pytest.mark.cad

OPTIONS = (("mirrors", "mirror_type"), ("roof_rails", "roof_rails"),
           ("spoiler", "rear_spoiler"), ("tow_bar", "tow_bar"))  # fmt: skip


def _build(cid: str, v: dict[str, float]) -> k.Shape | None:
    return getattr(e, f"build_{cid}")(BY_ID[cid].resolve_inputs(v))


@pytest.mark.parametrize("template", sorted(spec.TEMPLATES))
def test_every_option_builds_on_every_template(template: str) -> None:
    v = default_values() | spec.TEMPLATES[template]
    assert not validate(v)  # the template's own options obey the rules
    for cid, option in OPTIONS:
        for i in range(len(REGISTRY[option].options)):
            shape = _build(cid, v | {option: float(i)})
            if shape is None:
                assert i == 0 or cid == "spoiler"  # off, or a boot spoiler without a boot
                continue
            per_side = cid in ("mirrors", "roof_rails") and k.solid_count(shape) == 2
            assert k.is_valid(shape) and (k.solid_count(shape) == 1 or per_side), (cid, i)


def test_a_boot_spoiler_needs_a_boot() -> None:
    suv = default_values() | spec.TEMPLATES["suv"] | {"rear_spoiler": 3.0}
    assert _build("spoiler", suv) is None
    assert any(r.rule == "boot_spoiler_needs_a_boot" for r in validate(suv))
    sedan = default_values() | spec.TEMPLATES["sedan"] | {"rear_spoiler": 3.0}
    assert _build("spoiler", sedan) is not None and not validate(sedan)


@pytest.mark.parametrize("template", ["sedan", "suv", "box_truck"])
def test_roof_openings_keep_the_extents_and_remove_roof_panel(template: str) -> None:
    v = default_values() | spec.TEMPLATES[template]
    volume, bounds = {}, {}
    for i, kind in enumerate(e.ROOF_TYPES):
        body = b.build_body(BY_ID["body"].resolve_inputs(v | {"roof_type": float(i)}))
        assert k.is_valid(body) and k.solid_count(body) == 1
        volume[kind] = k.volume(body)
        bounds[kind] = [c for corner in k.bounds(body) for c in corner]
    assert volume["panoramic"] < volume["sunroof"] < volume["solid"]
    assert bounds["panoramic"] == pytest.approx(bounds["solid"], abs=0.01)


@pytest.mark.parametrize("mirror", [0.0, 1.0])
def test_mirrors_reach_the_width_over_mirrors(mirror: float) -> None:
    v = default_values() | {"mirror_type": mirror}
    (_, y0, _), (_, y1, _) = k.bounds(_build("mirrors", v))
    assert y1 - y0 == pytest.approx(d.compute("width_over_mirrors", v), abs=0.01)
    assert y1 > v["body_width"] / 2  # beyond the body side


def test_camera_pods_are_narrower_than_mirrors() -> None:
    v = default_values()
    widths = [d.compute("width_over_mirrors", v | {"mirror_type": m}) for m in (0.0, 1.0)]
    assert widths[1] < widths[0]


@pytest.mark.parametrize("template", ["sedan", "pickup", "box_truck"])
def test_the_tow_ball_sits_near_400_mm(template: str) -> None:
    v = default_values() | spec.TEMPLATES[template] | {"tow_bar": 1.0}
    (x0, _, _), (_, _, z1) = k.bounds(_build("tow_bar", v))
    assert z1 - 25 == pytest.approx(e.BALL_HEIGHT, abs=15)  # ball centre
    assert x0 < -(v["wheelbase"] + v["rear_overhang"])  # behind the body


def test_roof_rails_stand_on_the_roof() -> None:
    v = default_values() | spec.TEMPLATES["suv"] | {"roof_rails": 2.0}
    layout = b.body_layout(BY_ID["body"].resolve_inputs(v))
    (x0, _, z0), (x1, _, z1) = k.bounds(_build("roof_rails", v))
    assert z0 < layout.roof_z < z1 <= layout.roof_z + 80
    assert layout.roof[0] <= x0 and x1 <= layout.roof[1]


@pytest.mark.parametrize(
    ("text", "parameter", "option"),
    [
        ("fit a panoramic roof", "roof_type", "Panoramic glass"),
        ("fit a sunroof", "roof_type", "Sunroof"),
        ("remove the sunroof", "roof_type", "Solid"),
        ("fit roof rails", "roof_rails", "Rails"),
        ("fit a roof rack", "roof_rails", "Rails with crossbars"),
        ("remove the roof rails", "roof_rails", "None"),
        ("fit a wing", "rear_spoiler", "Wing"),
        ("fit a boot lip spoiler", "rear_spoiler", "Boot lip"),
        ("remove the spoiler", "rear_spoiler", "None"),
        ("fit camera mirrors", "mirror_type", "Camera"),
        ("fit a tow bar", "tow_bar", "Fitted"),
        ("remove the tow bar", "tow_bar", "None"),
    ],
)
def test_option_phrases(text: str, parameter: str, option: str) -> None:
    result = parse(text)
    assert result.kind is Kind.COMMAND, (text, result.question)
    assert result.command is not None
    (change,) = result.command.changes
    assert change.parameter == parameter
    assert REGISTRY[parameter].options[int(change.value)] == option


def test_roof_length_phrases_still_mean_the_roof_length() -> None:
    result = parse("increase the roof by 100 mm")
    assert result.command is not None
    assert result.command.changes[0].parameter == "roof_length"
