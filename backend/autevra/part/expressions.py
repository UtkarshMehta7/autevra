"""Safe arithmetic expressions for part parameters and feature bindings.

Only numbers, parameter names, + - * / ** %, unary signs, parentheses and a few math
functions are allowed; anything else (attribute access, calls to other names, comparisons,
strings) is rejected before evaluation. No Python ``eval``.
"""

import ast
import math
from collections.abc import Mapping

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": lambda d: math.sin(math.radians(d)),
    "cos": lambda d: math.cos(math.radians(d)),
    "tan": lambda d: math.tan(math.radians(d)),
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
    "pi": None,
}  # fmt: skip  (trigonometry in degrees, like every angle in a part)
_BINARY = {
    ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a**b, ast.Mod: lambda a, b: a % b,
}  # fmt: skip
MAX_LENGTH = 200


class ExpressionError(ValueError):
    pass


def evaluate(text: str, names: Mapping[str, float]) -> float:
    """Value of ``text`` with the given parameter values."""
    if len(text) > MAX_LENGTH:
        raise ExpressionError(f"expression longer than {MAX_LENGTH} characters")
    try:
        tree = ast.parse(text.strip().removeprefix("="), mode="eval")
    except SyntaxError:
        raise ExpressionError(f"cannot read '{text}'") from None

    def ev(node: ast.AST) -> float:
        match node:
            case ast.Expression(body=body):
                return ev(body)
            case ast.Constant(value=v) if isinstance(v, int | float) and not isinstance(v, bool):
                return float(v)
            case ast.Name(id="pi"):
                return math.pi
            case ast.Name(id=name):
                if name not in names:
                    raise ExpressionError(f"unknown parameter '{name}'")
                return float(names[name])
            case ast.UnaryOp(op=ast.USub(), operand=x):
                return -ev(x)
            case ast.UnaryOp(op=ast.UAdd(), operand=x):
                return ev(x)
            case ast.BinOp(left=a, op=op, right=b) if type(op) in _BINARY:
                left, right = ev(a), ev(b)
                if isinstance(op, ast.Pow) and abs(right) > 16:
                    raise ExpressionError("exponent too large")
                return _BINARY[type(op)](left, right)
            case ast.Call(func=ast.Name(id=fn), args=args, keywords=[]) if FUNCTIONS.get(fn):
                return float(FUNCTIONS[fn](*(ev(a) for a in args)))
        raise ExpressionError(f"'{ast.unparse(node)}' is not allowed in an expression")

    try:
        value = ev(tree)
    except ZeroDivisionError:
        raise ExpressionError(f"division by zero in '{text}'") from None
    except (TypeError, ValueError, OverflowError) as exc:
        if isinstance(exc, ExpressionError):
            raise
        raise ExpressionError(f"cannot evaluate '{text}': {exc}") from None
    if not math.isfinite(value):
        raise ExpressionError(f"'{text}' is not a finite number")
    return value


def resolve_parameters(params: Mapping[str, str | float]) -> dict[str, float]:
    """Parameter values: numbers, or expressions of parameters defined before them."""
    out: dict[str, float] = {}
    for name, value in params.items():
        out[name] = float(value) if isinstance(value, int | float) else evaluate(value, out)
    return out
