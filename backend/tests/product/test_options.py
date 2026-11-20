import pytest

from autevra.product.options import (
    ApplicabilityError,
    OptionFamily,
    OptionRule,
    Options,
    applies,
    parse,
)

OPTS = Options(
    families=[
        OptionFamily(id="pt", label="Powertrain", choices=["ice", "bev"]),
        OptionFamily(id="engine", label="Engine", choices=["i4", "v8"], applies="pt == 'ice'"),
        OptionFamily(id="tow", label="Tow bar", choices=["no", "yes"]),
    ],
    rules=[OptionRule(id="r", when="engine == 'v8'", then="tow == 'no'", message="no tow v8")],
)


def test_applicability_language() -> None:
    c = {"pt": "ice", "engine": "v8", "tow": "no"}
    assert applies("", c)
    assert applies("pt == 'ice' and engine in ('v8', 'v6')", c)
    assert not applies("not (pt == 'ice')", c)
    assert applies("pt != 'bev' or tow == 'yes'", c)
    assert applies("engine not in ('i4',)", c)


@pytest.mark.parametrize("bad", ["__import__('os')", "pt.upper()", "1 + 2", "pt < 'x'",
                                 "lambda: 1", "unknown == 'x'", "x" * 400])  # fmt: skip
def test_applicability_rejects_anything_else(bad: str) -> None:
    with pytest.raises(ApplicabilityError):
        parse(bad, {"pt"})


def test_resolve_drops_inapplicable_families_and_fills_defaults() -> None:
    assert OPTS.resolve({"pt": "bev", "engine": "v8"}) == {"pt": "bev", "tow": "no"}
    assert OPTS.resolve({}) == {"pt": "ice", "engine": "i4", "tow": "no"}
    with pytest.raises(ApplicabilityError):
        OPTS.resolve({"pt": "diesel"})
    with pytest.raises(ApplicabilityError):
        OPTS.resolve({"colour": "red"})


def test_rules_and_enumeration() -> None:
    assert OPTS.violations({"pt": "ice", "engine": "v8", "tow": "yes"}) == ["no tow v8"]
    configs = list(OPTS.enumerate())
    # ice x {i4, v8} x tow, minus v8+tow; bev x tow (engine does not apply)
    assert len(configs) == 3 + 2
    assert {"pt": "ice", "engine": "v8", "tow": "yes"} not in configs
    OPTS.validate_expressions()
