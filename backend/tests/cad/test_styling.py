import pytest

from autevra.ai.rule_parser import Kind, parse
from autevra.assembly.model import BY_ID
from autevra.cad import kernel as k
from autevra.core.parameters import REGISTRY, default_values
from autevra.domains.automotive import builders as b
from autevra.domains.automotive import styling as s
from autevra.domains.automotive import vehicle

pytestmark = pytest.mark.cad


def test_the_parameters_offer_every_design_in_builder_order() -> None:
    assert len(REGISTRY["wheel_design"].options) == len(s.WHEEL_DESIGNS)
    assert len(REGISTRY["head_lamp_style"].options) == len(s.HEAD_LAMP_STYLES)
    assert len(REGISTRY["tail_lamp_style"].options) == len(s.TAIL_LAMP_STYLES)
    assert len(REGISTRY["rim_finish"].options) == len(vehicle.RIM_FINISHES)


@pytest.mark.parametrize("design", range(len(s.WHEEL_DESIGNS)))
def test_every_rim_is_one_solid_inside_the_tyre(design: int) -> None:
    v = default_values() | {"wheel_design": float(design)}
    rim_inputs = BY_ID["rim_fl"].resolve_inputs(v)
    rim = s.build_rim(rim_inputs)
    assert k.is_valid(rim) and k.solid_count(rim) == 1
    (x0, y0, _), (x1, y1, _) = k.bounds(rim)
    half = rim_inputs["tyre_width"] / 2
    assert x1 - x0 == pytest.approx(2 * rim_inputs["rim_radius"], abs=0.5)  # seats in the tyre
    assert y0 >= -half and y1 <= half + 15  # a steel hub cap may stand a little proud
    tyre = b.build_wheel(BY_ID["wheel_fl"].resolve_inputs(v))
    assert k.volume(k.intersect(tyre, rim)) == pytest.approx(0, abs=1)  # no overlap


def test_open_designs_are_lighter_than_closed_discs() -> None:
    v = default_values()
    volume = {
        d: k.volume(s.build_rim(BY_ID["rim_fl"].resolve_inputs(v | {"wheel_design": float(i)})))
        for i, d in enumerate(s.WHEEL_DESIGNS)
    }
    assert max(volume[d] for d in ("five_spoke", "multi_spoke", "twin_spoke")) < volume["aero"]


@pytest.mark.parametrize(
    ("head", "tail"), [(h, t) for h in range(len(s.HEAD_LAMP_STYLES)) for t in (0, 1, 2)]
)
def test_lamps_sit_flush_in_the_body(head: int, tail: int) -> None:
    v = default_values() | {"head_lamp_style": float(head), "tail_lamp_style": float(tail)}
    inputs = BY_ID["body"].resolve_inputs(v)
    body = b.build_body(inputs)
    lamps = k.fuse(b.build_head_lamps(inputs), b.build_tail_lamps(inputs))
    assert k.is_valid(body) and k.solid_count(body) == 1
    flat = [c for corner in k.bounds(body) for c in corner]
    assert [c for corner in k.bounds(k.fuse(body, lamps)) for c in corner] == pytest.approx(
        flat, abs=0.01
    )  # flush: the lamps do not change the extents
    assert k.volume(k.intersect(body, lamps)) == pytest.approx(0, abs=1)  # in their recesses


def test_rim_finish_changes_appearance_without_a_rebuild() -> None:
    v = default_values()
    rim = BY_ID["rim_fl"]
    assert "rim_finish" not in rim.geometry
    finishes = {rim.resolve_appearance(v | {"rim_finish": float(i)}) for i in range(6)}
    assert len(finishes) == 6


@pytest.mark.parametrize(
    ("text", "parameter", "option"),
    [
        ("fit mesh wheels", "wheel_design", "Mesh"),
        ("fit it with aero wheels", "wheel_design", "Aero disc"),
        ("change the wheel design to twin spoke", "wheel_design", "Twin-spoke"),
        ("make the rims gloss black", "rim_finish", "Gloss black"),
        ("make the wheels bronze", "rim_finish", "Bronze"),
        ("fit diamond cut alloys", "rim_finish", "Diamond cut"),
        ("fit matrix led headlights", "head_lamp_style", "Matrix LED"),
        ("fit round headlamps", "head_lamp_style", "Round"),
        ("fit a light bar tail lamps", "tail_lamp_style", "Light bar"),
        ("make the tail lights vertical", "tail_lamp_style", "Vertical"),
    ],
)
def test_styling_phrases_set_the_choice(text: str, parameter: str, option: str) -> None:
    result = parse(text)
    assert result.kind is Kind.COMMAND, (text, result.question)
    assert result.command is not None
    (change,) = result.command.changes
    assert change.parameter == parameter
    assert REGISTRY[parameter].options[int(change.value)] == option


@pytest.mark.parametrize(
    ("text", "parameter"),
    [("make it bronze", "paint_colour"), ("make it black", "paint_colour"),
     ("make the rims 1 inch bigger", "rim_diameter")],
)  # fmt: skip
def test_vehicle_phrases_are_not_taken_by_part_choices(text: str, parameter: str) -> None:
    result = parse(text)
    assert result.command is not None
    assert result.command.changes[0].parameter == parameter
