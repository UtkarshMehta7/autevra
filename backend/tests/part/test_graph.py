"""The feature dependency graph, incremental rebuild and reorder guard."""

import pytest

from autevra.part import build, graph
from autevra.part import expressions as ex
from autevra.part import features as f

pytestmark = pytest.mark.cad


def _doc(width: float = 200.0, hole: float = 10.0) -> f.PartDoc:
    return f.PartDoc.model_validate({
        "name": "Plate",
        "parameters": {"width": width, "hole": hole, "pitch": "width / 2 - 2 * hole"},
        "features": [
            {"id": "plate", "type": "box", "size": [200, 100, 10],
             "bindings": {"size.0": "width"}},
            {"id": "bore", "type": "cylinder", "op": "cut", "radius": 10, "height": 30,
             "bindings": {"radius": "hole"}, "at": {"x": 40}},
            {"id": "row", "type": "linear_pattern", "count": 3, "step": [40, 0, 0],
             "bindings": {"step.0": "pitch"}},
            {"id": "round", "type": "fillet", "radius": 2, "edges": "|Z"},
        ],
    })  # fmt: skip


def test_expression_names_skip_functions_and_pi() -> None:
    assert ex.names("sqrt(width) * pi + hole / 2") == {"width", "hole"}
    assert ex.names("not ( valid") == set()


def test_the_graph_links_parameters_bindings_body_and_patterns() -> None:
    g = graph.dependency_graph(_doc())
    edges = {(e["from"], e["to"], e["kind"]) for e in g["edges"]}
    assert ("param:width", "param:pitch", "expression") in edges
    assert ("param:hole", "param:pitch", "expression") in edges
    assert ("param:width", "feature:plate", "binding") in edges
    assert ("param:pitch", "feature:row", "binding") in edges
    assert ("feature:plate", "feature:bore", "body") in edges
    assert ("feature:bore", "feature:row", "repeats") in edges
    assert ("feature:row", "feature:round", "body") in edges
    assert g["levels"]["feature:round"] > g["levels"]["feature:row"] > g["levels"]["param:pitch"]


def test_downstream_of_a_feature_is_what_rebuilds() -> None:
    assert graph.downstream(_doc(), "bore") == ["bore", "row", "round"]
    assert graph.downstream(_doc(), "round") == ["round"]


def test_an_edit_rebuilds_only_downstream_features() -> None:
    first = build.build_part(_doc())
    assert not first.errors and first.built == ["plate", "bore", "row", "round"]
    again = build.build_part(_doc())
    assert again.reused == ["plate", "bore", "row", "round"]  # nothing changed
    doc = _doc()
    rounder = doc.features[3].model_copy(update={"radius": 3.0})
    edited = doc.model_copy(update={"features": [*doc.features[:3], rounder]})
    out = build.build_part(edited)
    assert out.reused == ["plate", "bore", "row"] and list(out.feature_ms) == ["round"]
    # a parameter change rebuilds from the first feature that reads it
    assert build.build_part(_doc(width=210.0)).reused == []
    assert build.build_part(_doc(hole=8.0)).reused == ["plate"]


def test_reorders_that_break_a_dependency_are_refused() -> None:
    doc = _doc()
    assert graph.reorder_problem(doc, ["plate", "bore", "row", "round"]) is None
    assert graph.reorder_problem(doc, ["plate", "row", "bore", "round"]) is None  # repeats plate
    assert "after a solid" in graph.reorder_problem(doc, ["round", "plate", "bore", "row"])
    assert "after one" in graph.reorder_problem(doc, ["row", "plate", "bore", "round"])
    assert "needs a body" in graph.reorder_problem(doc, ["bore", "plate", "row", "round"])
    assert "every feature" in graph.reorder_problem(doc, ["plate", "bore"])
