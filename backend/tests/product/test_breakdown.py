import pytest

from autevra.product import templates
from autevra.product.breakdown import Node, check_ids, configure, rollup
from autevra.product.templates import PartTemplate


def _tree() -> Node:
    return Node(id="p", name="P", kind="product", budget=100.0, children=[
        Node(id="s", name="S", kind="system", children=[
            Node(id="a", name="A", mass=30.0, cg=(1.0, 0, 0), instances=2, maturity=1),
            Node(id="b", name="B", mass=10.0, cg=(5.0, 0, 0), applicability="x == 'b'"),
        ]),
        Node(id="c", name="C", mass=60.0, cg=(0.0, 0, 2.0), applicability="x == 'c'"),
    ])  # fmt: skip


def test_configure_and_rollup() -> None:
    t = configure(_tree(), {"x": "b"}, {"x"})
    r = rollup(t)
    assert r.rollup.mass == pytest.approx(40.0)
    assert r.rollup.cg[0] == pytest.approx((30 * 1 + 10 * 5) / 40)
    assert r.rollup.parts == 2 and r.rollup.instances == 3
    assert r.rollup.maturity == [1, 2, 0, 0, 0] and r.rollup.min_maturity == 0
    assert r.children[0].maturity == 0  # a system reports its least mature part
    assert r.rollup.over_budget == []


def test_over_budget_is_reported_where_it_happens() -> None:
    r = rollup(configure(_tree(), {"x": "c"}, {"x"}))
    assert r.rollup.mass == pytest.approx(90.0)
    tree = _tree()
    tree.children[1].mass = 80.0
    r = rollup(configure(tree, {"x": "c"}, {"x"}))
    assert r.rollup.over_budget == ["p"]


def test_ids_must_be_unique() -> None:
    t = _tree()
    t.children.append(Node(id="a", name="dup"))
    with pytest.raises(ValueError, match="duplicate"):
        check_ids(t)


def test_templates_are_keyed_by_module() -> None:
    templates.register(PartTemplate(id="t_x", module="mod_a", name="X", code="1",
                                    process="casting"))  # fmt: skip
    assert "t_x" in templates.of("mod_a") and "t_x" not in templates.of("mod_b")
    with pytest.raises(KeyError):
        templates.get("mod_b", "t_x")
    with pytest.raises(ValueError, match="process"):
        PartTemplate(id="t_y", module="mod_a", name="Y", code="1", process="magic")
