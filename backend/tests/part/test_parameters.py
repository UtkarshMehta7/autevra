import pytest

from autevra.cad import kernel as k
from autevra.part import expressions as ex
from autevra.part import features as f
from autevra.part.build import build_part

pytestmark = pytest.mark.cad


@pytest.mark.parametrize(
    ("text", "value"),
    [("width / 2 - 30", 70.0), ("=2 * width", 400.0), ("-(width) + 5", -195.0),
     ("sqrt(width * 2)", 20.0), ("max(width, 300)", 300.0), ("cos(60) * 10", 5.0),
     ("width % 7", 4.0), ("2 ** 3", 8.0), ("round(pi * 100)", 314.0)],
)  # fmt: skip
def test_expressions_evaluate(text: str, value: float) -> None:
    assert ex.evaluate(text, {"width": 200.0}) == pytest.approx(value)


@pytest.mark.parametrize(
    "text",
    ["__import__('os').system('true')", "width.real", "open('x')", "lambda: 1", "'a' * 3",
     "[1, 2]", "width if 1 else 2", "1 < 2", "nope + 1", "1 / 0", "2 ** 400", "x" * 300],
)  # fmt: skip
def test_unsafe_or_bad_expressions_are_rejected(text: str) -> None:
    with pytest.raises(ex.ExpressionError):
        ex.evaluate(text, {"width": 200.0})


def test_parameters_may_use_earlier_parameters() -> None:
    values = ex.resolve_parameters(
        {"width": 200, "hole": "width / 25", "pitch": "width/2 - 2*hole"}
    )
    assert values == {"width": 200.0, "hole": 8.0, "pitch": 84.0}
    with pytest.raises(ex.ExpressionError):
        ex.resolve_parameters({"a": "b + 1", "b": 2})  # only earlier parameters


def _plate(width: float) -> f.PartDoc:
    return f.PartDoc.model_validate({
        "parameters": {"width": width, "thickness": 12, "hole": "width / 25"},
        "features": [
            {"id": "plate", "type": "box",
             "bindings": {"size.0": "width", "size.1": "width", "size.2": "thickness"}},
            {"id": "hole", "type": "cylinder", "op": "cut", "height": 50,
             "bindings": {"radius": "hole", "at.x": "width / 2 - 3 * hole"}},
            {"id": "holes", "type": "circular_pattern", "count": 4},
        ],
    })  # fmt: skip


def test_changing_one_parameter_refits_the_whole_part() -> None:
    small, large = build_part(_plate(200)), build_part(_plate(400))
    assert not small.errors and not large.errors
    (x0, _, _), (x1, _, z1) = k.bounds(large.shape)
    assert x1 - x0 == pytest.approx(400) and z1 == pytest.approx(6)
    for width, result in ((200, small), (400, large)):
        hole = width / 25
        expected = width * width * 12 - 4 * 3.14159265 * hole**2 * 12
        assert k.volume(result.shape) == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize(
    ("bindings", "message"),
    [({"radius": "nope"}, "unknown parameter 'nope'"),
     ({"colour": "1"}, "'colour' is not a numeric field"),
     ({"radius": "-5"}, "radius")],
)  # fmt: skip
def test_binding_errors_name_the_feature(bindings: dict, message: str) -> None:
    doc = f.PartDoc.model_validate({"parameters": {"w": 10}, "features": [
        {"id": "base", "type": "box"},
        {"id": "pin", "type": "cylinder", "bindings": bindings}]})  # fmt: skip
    result = build_part(doc)
    assert result.errors[0].feature == "pin" and message in result.errors[0].message
    assert result.built == ["base"]


def test_a_bad_parameter_is_reported_before_any_feature() -> None:
    doc = f.PartDoc.model_validate({"parameters": {"w": "1 / 0"},
                                    "features": [{"id": "b", "type": "box"}]})  # fmt: skip
    result = build_part(doc)
    assert result.errors[0].feature == "parameters" and result.shape is None
