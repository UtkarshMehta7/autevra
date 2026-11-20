"""The dependency graph (a DAG) behind a Part Design feature tree.

Nodes are the part's parameters and its features. Edges say what each one reads:

- ``expression``: a parameter whose expression uses another parameter;
- ``binding``: a feature field bound to an expression of parameters;
- ``body``: a feature that adds to, cuts from or modifies the body built by the features
  before it (it reads that body);
- ``repeats``: a pattern that copies the solid feature before it.

The tree is built in order, so every edge points from an earlier node to a later one; a
reorder is refused when it would put a feature before something it reads. Editing a
feature invalidates exactly the features downstream of it in this graph; the builder
reuses every result before it (see ``autevra.part.build``).
"""

from autevra.part import expressions as ex
from autevra.part import features as f

PATTERNS = ("linear_pattern", "circular_pattern")


def dependency_graph(doc: f.PartDoc) -> dict:
    nodes: list[dict] = []
    edges: list[dict] = []
    params = doc.effective_parameters()
    for name, value in params.items():
        nodes.append({"id": f"param:{name}", "kind": "parameter", "label": name,
                      "value": value})  # fmt: skip
        if isinstance(value, str):
            for used in sorted(ex.names(value) & set(params)):
                edges.append({"from": f"param:{used}", "to": f"param:{name}",
                              "kind": "expression"})  # fmt: skip
    body_from: str | None = None  # the last feature that produced the body
    last_solid: str | None = None
    for feat in doc.features:
        node = f"feature:{feat.id}"
        nodes.append({"id": node, "kind": "feature", "label": feat.name or feat.id,
                      "type": feat.type, "suppressed": feat.suppressed})  # fmt: skip
        for path, expression in feat.bindings.items():
            for used in sorted(ex.names(expression) & set(params)):
                edges.append({"from": f"param:{used}", "to": node, "kind": "binding",
                              "field": path})  # fmt: skip
        if feat.suppressed:
            continue
        if body_from is not None:
            edges.append({"from": f"feature:{body_from}", "to": node, "kind": "body"})
        if feat.type in PATTERNS and last_solid is not None:
            edges.append({"from": f"feature:{last_solid}", "to": node, "kind": "repeats"})
        if feat.type in f.SOLID_TYPES:
            last_solid = feat.id
        body_from = feat.id
    return {"nodes": nodes, "edges": edges, "levels": _levels(nodes, edges)}


def _levels(nodes: list[dict], edges: list[dict]) -> dict[str, int]:
    """Longest-path layer of every node (sources at 0), for drawing the DAG in columns."""
    level = {n["id"]: 0 for n in nodes}
    order = {n["id"]: i for i, n in enumerate(nodes)}
    for e in sorted(edges, key=lambda e: order[e["to"]]):  # edges point forward in order
        level[e["to"]] = max(level[e["to"]], level[e["from"]] + 1)
    return level


def downstream(doc: f.PartDoc, feature_id: str) -> list[str]:
    """Features that must rebuild when ``feature_id`` changes (itself first)."""
    g = dependency_graph(doc)
    out, stack = [], [f"feature:{feature_id}"]
    seen = set(stack)
    children: dict[str, list[str]] = {}
    for e in g["edges"]:
        children.setdefault(e["from"], []).append(e["to"])
    while stack:
        n = stack.pop()
        out.append(n)
        for c in children.get(n, []):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    order = [n["id"] for n in g["nodes"]]
    return [n.split(":", 1)[1] for n in sorted(out, key=order.index) if n.startswith("feature:")]


def reorder_problem(doc: f.PartDoc, order: list[str]) -> str | None:
    """Why the features cannot be built in ``order`` (None when they can)."""
    if sorted(order) != sorted(feat.id for feat in doc.features):
        return "the new order must list every feature once"
    by_id = {feat.id: feat for feat in doc.features}
    seen_solid = False
    for i, fid in enumerate(order):
        feat = by_id[fid]
        if feat.suppressed:
            continue
        if feat.type in PATTERNS and not seen_solid:
            return f"'{feat.name or fid}' repeats a solid, so it must come after one"
        if feat.type not in f.SOLID_TYPES and feat.type not in PATTERNS and not seen_solid:
            return f"'{feat.name or fid}' modifies the body, so it must come after a solid"
        if i == 0 and getattr(feat, "op", f.Op.ADD) != f.Op.ADD:
            return f"'{feat.name or fid}' cuts or intersects, so it needs a body before it"
        seen_solid = seen_solid or feat.type in f.SOLID_TYPES
    return None
