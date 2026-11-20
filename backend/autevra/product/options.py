"""Options, option rules and configurations (one product, many variants).

An option family is a named choice (``powertrain``: Combustion | Hybrid | Battery
electric). A configuration picks one choice per family. Families may themselves apply
only in some configurations (an engine choice only where there is an engine), and rules
state which combinations are valid. Breakdown nodes carry an *applicability* expression
over the options, so one "150 %" breakdown serves every variant.

Applicability expressions are a small safe language, checked before evaluation (no
Python ``eval``): option ids, quoted choice labels, ``==``, ``!=``, ``in``, ``not in``,
tuples, ``and``, ``or``, ``not`` and parentheses, e.g.
``powertrain != 'Battery electric' and tow_bar == 'Fitted'``.
"""

import ast
import itertools
from collections.abc import Iterator, Mapping

from pydantic import BaseModel, Field

MAX_LENGTH = 300

Configuration = Mapping[str, str]


class ApplicabilityError(ValueError):
    pass


class OptionFamily(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    label: str
    choices: list[str] = Field(min_length=1)
    applies: str = ""  # applicability of the family itself ("" = always)
    affects_mass: bool = True  # whether choices change the mass roll-up
    description: str = ""


class OptionRule(BaseModel):
    """``when`` → ``then`` must hold: a configuration where ``when`` is true and ``then`` is
    false is invalid."""

    id: str
    when: str
    then: str
    message: str


def _check(node: ast.AST, names: set[str]) -> None:
    match node:
        case ast.Expression(body=body):
            _check(body, names)
        case ast.BoolOp(values=values):
            for v in values:
                _check(v, names)
        case ast.UnaryOp(op=ast.Not(), operand=x):
            _check(x, names)
        case ast.Compare(left=left, ops=ops, comparators=comps):
            if not all(isinstance(o, ast.Eq | ast.NotEq | ast.In | ast.NotIn) for o in ops):
                raise ApplicabilityError("only ==, !=, in and not in compare options")
            for x in (left, *comps):
                _check(x, names)
        case ast.Tuple(elts=elts) | ast.List(elts=elts):
            for x in elts:
                _check(x, names)
        case ast.Constant(value=v) if isinstance(v, str):
            pass
        case ast.Name(id=name):
            if name not in names:
                raise ApplicabilityError(f"unknown option '{name}'")
        case _:
            raise ApplicabilityError(f"not allowed in an applicability expression: "
                                     f"{type(node).__name__}")  # fmt: skip


def parse(text: str, names: set[str]) -> ast.Expression:
    if len(text) > MAX_LENGTH:
        raise ApplicabilityError(f"expression longer than {MAX_LENGTH} characters")
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError:
        raise ApplicabilityError(f"cannot read '{text}'") from None
    _check(tree, names)
    return tree


def _ev(node: ast.AST, config: Configuration) -> object:
    match node:
        case ast.Expression(body=body):
            return _ev(body, config)
        case ast.BoolOp(op=ast.And(), values=values):
            return all(_ev(v, config) for v in values)
        case ast.BoolOp(op=ast.Or(), values=values):
            return any(_ev(v, config) for v in values)
        case ast.UnaryOp(op=ast.Not(), operand=x):
            return not _ev(x, config)
        case ast.Compare(left=left, ops=ops, comparators=comps):
            a = _ev(left, config)
            for op, c in zip(ops, comps, strict=True):
                b = _ev(c, config)
                ok = {ast.Eq: a == b, ast.NotEq: a != b}.get(type(op))
                if ok is None:
                    ok = (a in b) if isinstance(op, ast.In) else (a not in b)  # type: ignore[operator]
                if not ok:
                    return False
                a = b
            return True
        case ast.Tuple(elts=elts) | ast.List(elts=elts):
            return tuple(_ev(x, config) for x in elts)
        case ast.Constant(value=v):
            return v
        case ast.Name(id=name):
            return config.get(name)  # an inapplicable family has no choice (None)
    raise ApplicabilityError(type(node).__name__)  # unreachable after _check


def applies(text: str, config: Configuration, names: set[str] | None = None) -> bool:
    """Whether an applicability expression holds in a configuration ("" always holds)."""
    if not text.strip():
        return True
    return bool(_ev(parse(text, set(config) if names is None else names), config))


class Options(BaseModel):
    """A product's option families and rules."""

    families: list[OptionFamily] = []
    rules: list[OptionRule] = []

    def names(self) -> set[str]:
        return {f.id for f in self.families}

    def resolve(self, config: Configuration) -> dict[str, str]:
        """A complete configuration: unknown keys and invalid choices rejected, families
        that do not apply removed, missing applicable families set to their first choice."""
        by_id = {f.id: f for f in self.families}
        for key, choice in config.items():
            if key not in by_id:
                raise ApplicabilityError(f"unknown option '{key}'")
            if choice not in by_id[key].choices:
                raise ApplicabilityError(f"'{choice}' is not a choice of {by_id[key].label}")
        out: dict[str, str] = {}
        names = self.names()
        for f in self.families:  # in order: a family may depend on earlier ones
            if applies(f.applies, out, names):
                out[f.id] = config.get(f.id, f.choices[0])
        return out

    def violations(self, config: Configuration) -> list[str]:
        names = self.names()
        return [
            r.message
            for r in self.rules
            if applies(r.when, config, names) and not applies(r.then, config, names)
        ]

    def validate_expressions(self) -> None:
        names = self.names()
        for f in self.families:
            if f.applies:
                parse(f.applies, names)
        for r in self.rules:
            parse(r.when, names)
            parse(r.then, names)

    def enumerate(self, only_mass: bool = False) -> Iterator[dict[str, str]]:
        """Every valid configuration (families not affecting mass held at their first
        choice when ``only_mass``)."""
        fams = [f for f in self.families if f.affects_mass or not only_mass]
        seen: set[tuple] = set()
        for combo in itertools.product(*(f.choices for f in fams)):
            config = self.resolve(dict(zip((f.id for f in fams), combo, strict=True)))
            key = tuple(sorted(config.items()))
            if key in seen or self.violations(config):
                continue
            seen.add(key)
            yield config
