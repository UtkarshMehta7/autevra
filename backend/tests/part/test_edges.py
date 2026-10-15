import math

import pytest

from autevra.cad import kernel as k
from autevra.part import features as f
from autevra.part.build import build_part

pytestmark = pytest.mark.cad

BOX = {"id": "b", "type": "box", "size": [100, 60, 40]}


def _volume(modifier: dict) -> float:
    result = build_part(f.PartDoc.model_validate({"features": [BOX, {"id": "m", **modifier}]}))
    assert not result.errors, result.errors
    return k.volume(result.shape)


def test_fillet_on_the_vertical_edges_only() -> None:
    removed = 100 * 60 * 40 - _volume({"type": "fillet", "radius": 5, "edges": "|Z"})
    assert removed == pytest.approx(4 * (1 - math.pi / 4) * 5**2 * 40, rel=1e-4)


def test_chamfer_on_the_vertical_edges_only() -> None:
    removed = 100 * 60 * 40 - _volume({"type": "chamfer", "size": 4, "edges": "|Z"})
    assert removed == pytest.approx(4 * 4**2 / 2 * 40, rel=1e-4)


def test_all_edges_remove_more_than_some() -> None:
    every = _volume({"type": "fillet", "radius": 5})
    top = _volume({"type": "fillet", "radius": 5, "edges": ">Z"})
    assert every < top < 100 * 60 * 40


def test_a_selector_matching_nothing_is_reported() -> None:
    features = [{"id": "c", "type": "cylinder"}, {"id": "m", "type": "fillet", "edges": "|X"}]
    doc = f.PartDoc.model_validate({"features": features})
    result = build_part(doc)
    assert result.errors[0].feature == "m" and "no edge matches" in result.errors[0].message


@pytest.mark.parametrize("bad", ["import os", "__class__", "edges; drop"])
def test_selectors_outside_the_grammar_are_rejected(bad: str) -> None:
    with pytest.raises(ValueError):
        f.PartDoc.model_validate({"features": [BOX, {"id": "m", "type": "fillet", "edges": bad}]})
