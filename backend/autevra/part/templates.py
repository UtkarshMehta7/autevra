"""Feature templates ("power copies"): a group of features with published inputs, saved to
a library and inserted into any part.

On insertion the template's features get the instance prefix on their ids, its parameters
become part parameters named ``<prefix>_<name>``, and each published input is either a
value or an expression of the target part's own parameters (``width / 2``). Bindings in
the features are rewritten to the renamed parameters, and an offset moves the inserted
solids.
"""

import ast
import re

from pydantic import BaseModel, ConfigDict, Field

from autevra.part.features import PartDoc

NAME = r"^[A-Za-z_][A-Za-z0-9_]{0,39}$"


class FeatureTemplate(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1, max_length=80)
    description: str = Field("", max_length=400)
    parameters: dict[str, float | str] = Field(default_factory=dict)  # published inputs
    features: list[dict] = Field(min_length=1, max_length=100)


class Insertion(BaseModel):
    template: str  # template id
    prefix: str = Field("t1", pattern=r"^[A-Za-z][A-Za-z0-9_]{0,15}$")
    inputs: dict[str, float | str] = Field(default_factory=dict)  # name -> value or expression
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0)


def _rename(expression: str, names: dict[str, str]) -> str:
    """Rename parameter names in an expression (only whole names, via the syntax tree)."""
    tree = ast.parse(expression.strip().removeprefix("="), mode="eval")

    class Renamer(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.Name:  # noqa: N802
            return ast.Name(id=names.get(node.id, node.id), ctx=node.ctx)

    return ast.unparse(Renamer().visit(tree))


def from_part(
    doc: PartDoc, name: str, feature_ids: list[str], description: str = ""
) -> FeatureTemplate:
    """A template of the chosen features of a part, publishing the parameters they use."""
    chosen = [f for f in doc.features if f.id in set(feature_ids)]
    if not chosen:
        raise ValueError("choose at least one feature")
    used: set[str] = set()
    for f in chosen:
        for expression in f.bindings.values():
            used |= {n.id for n in ast.walk(ast.parse(expression.removeprefix("="), mode="eval"))
                     if isinstance(n, ast.Name)}  # fmt: skip
    params = {k: v for k, v in doc.parameters.items() if k in used}
    # Parameters used by published parameters' own expressions come along too.
    for value in list(params.values()):
        if isinstance(value, str):
            for n in ast.walk(ast.parse(value.removeprefix("="), mode="eval")):
                if isinstance(n, ast.Name) and n.id in doc.parameters:
                    params.setdefault(n.id, doc.parameters[n.id])
    ordered = {k: v for k, v in doc.parameters.items() if k in params}
    return FeatureTemplate(name=name, description=description, parameters=ordered,
                           features=[f.model_dump(mode="json") for f in chosen])  # fmt: skip


def insert(doc: PartDoc, template: FeatureTemplate, how: Insertion) -> PartDoc:
    """The part with the template's features appended (validated)."""
    names = {k: f"{how.prefix}_{k}" for k in template.parameters}
    params = dict(doc.parameters)
    for k, default in template.parameters.items():
        value = how.inputs.get(k, default)
        if isinstance(value, str):
            # An input is an expression of the target part; the template's own default
            # (also when sent back unchanged) refers to the template's renamed parameters.
            given = k in how.inputs and how.inputs[k] != default
            value = value if given else _rename(value, names)
        if names[k] in params:
            raise ValueError(f"the part already has a parameter '{names[k]}'; use another prefix")
        params[names[k]] = value
    existing = {f.id for f in doc.features}
    features = []
    for raw in template.features:
        f = dict(raw)
        f["id"] = f"{how.prefix}_{raw['id']}"
        if f["id"] in existing:
            raise ValueError(f"the part already has a feature '{f['id']}'; use another prefix")
        f["bindings"] = {
            path: _rename(expr, names) for path, expr in raw.get("bindings", {}).items()
        }
        if "at" in f and any(how.offset):
            at = dict(f["at"])
            for axis, d in zip(("x", "y", "z"), how.offset, strict=True):
                at[axis] = at.get(axis, 0.0) + d
            f["at"] = at
        features.append(f)
    data = doc.model_dump(mode="json")
    data["parameters"] = params
    data["features"] = data["features"] + features
    return PartDoc.model_validate(data)


def valid_name(name: str) -> bool:
    return re.match(NAME, name) is not None
