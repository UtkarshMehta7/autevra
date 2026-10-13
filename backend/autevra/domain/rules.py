"""Cross-parameter rules: physical and packaging consistency checks.

Bounds on single parameters live in the registry. These rules relate several
parameters. Geometric checks that need real CAD (e.g. the steered tyre
sweeping past the frame) come in Phase 4; ``frame_clears_tyres`` is the
static, straight-ahead version.
"""

from collections.abc import Callable

from pydantic import BaseModel, ConfigDict

from autevra.domain import derived as d
from autevra.domain.derived import Values
from autevra.domain.parameters import REGISTRY


class Violation(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule: str
    message: str
    parameters: tuple[str, ...]


class Rule(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    description: str
    parameters: tuple[str, ...]


_RuleFn = Callable[[Values], str | None]
_RULES: list[tuple[Rule, _RuleFn]] = []


def _rule(rule_id: str, description: str, *parameters: str) -> Callable[[_RuleFn], _RuleFn]:
    def register(fn: _RuleFn) -> _RuleFn:
        _RULES.append((Rule(id=rule_id, description=description, parameters=parameters), fn))
        return fn

    return register


def _mm(x: float) -> str:
    return f"{x:.1f} mm"


@_rule(
    "tyres_within_body",
    "Tyres must fit inside the body width.",
    "body_width",
    "track_front",
    "track_rear",
    "tyre_width",
)
def _tyres_within_body(p: Values) -> str | None:
    over = d.overall_width_at_tyres(p)
    if over > p["body_width"]:
        return f"width over tyres {_mm(over)} exceeds body width {_mm(p['body_width'])}"
    return None


@_rule(
    "arch_below_beltline",
    "The wheel arch top must stay below the beltline.",
    "beltline_height",
    "rim_diameter",
    "tyre_width",
    "tyre_aspect_ratio",
    "arch_clearance",
)
def _arch_below_beltline(p: Values) -> str | None:
    top = d.arch_top_height(p)
    if top >= p["beltline_height"]:
        return f"wheel arch top {_mm(top)} is not below the beltline {_mm(p['beltline_height'])}"
    return None


@_rule(
    "front_overhang_contains_arch",
    "The front overhang must contain the front wheel arch.",
    "front_overhang",
    "rim_diameter",
    "tyre_width",
    "tyre_aspect_ratio",
    "arch_clearance",
)
def _front_overhang_contains_arch(p: Values) -> str | None:
    r = d.arch_radius(p)
    if p["front_overhang"] < r:
        return f"front overhang {_mm(p['front_overhang'])} is shorter than the arch radius {_mm(r)}"
    return None


@_rule(
    "rear_overhang_contains_arch",
    "The rear overhang must contain the rear wheel arch.",
    "rear_overhang",
    "rim_diameter",
    "tyre_width",
    "tyre_aspect_ratio",
    "arch_clearance",
)
def _rear_overhang_contains_arch(p: Values) -> str | None:
    r = d.arch_radius(p)
    if p["rear_overhang"] < r:
        return f"rear overhang {_mm(p['rear_overhang'])} is shorter than the arch radius {_mm(r)}"
    return None


@_rule(
    "arches_do_not_overlap",
    "Front and rear wheel arches must not overlap.",
    "wheelbase",
    "rim_diameter",
    "tyre_width",
    "tyre_aspect_ratio",
    "arch_clearance",
)
def _arches_do_not_overlap(p: Values) -> str | None:
    r = d.arch_radius(p)
    if p["wheelbase"] < 2 * r + 100:
        return f"wheelbase {_mm(p['wheelbase'])} leaves under 100 mm between the wheel arches"
    return None


@_rule(
    "roof_within_cabin", "Roof length must not exceed cabin length.", "roof_length", "cabin_length"
)
def _roof_within_cabin(p: Values) -> str | None:
    if p["roof_length"] > p["cabin_length"]:
        return f"roof length {_mm(p['roof_length'])} exceeds cabin length {_mm(p['cabin_length'])}"
    return None


@_rule(
    "cabin_within_body",
    "The cabin must lie within the body length.",
    "cabin_length",
    "cabin_offset",
    "wheelbase",
    "front_overhang",
    "rear_overhang",
)
def _cabin_within_body(p: Values) -> str | None:
    body_rear, body_front = d.body_x_range(p)
    cab_rear, cab_front = d.cabin_x_range(p)
    if cab_rear < body_rear or cab_front > body_front:
        return "the cabin extends beyond the front or rear of the body"
    return None


@_rule(
    "cabin_has_height",
    "The roof must be at least 250 mm above the beltline.",
    "overall_height",
    "beltline_height",
)
def _cabin_has_height(p: Values) -> str | None:
    gap = p["overall_height"] - p["beltline_height"]
    if gap < 250:
        return f"only {_mm(gap)} between the beltline and the roof (minimum 250 mm)"
    return None


@_rule(
    "body_has_depth",
    "The lower body must be at least 200 mm deep.",
    "beltline_height",
    "ground_clearance",
    "rail_height",
)
def _body_has_depth(p: Values) -> str | None:
    depth = p["beltline_height"] - d.body_floor_height(p)
    if depth < 200:
        return f"lower body is only {_mm(depth)} deep (minimum 200 mm)"
    return None


@_rule(
    "rail_wall_fits_section",
    "Rail wall thickness must be under half the rail section.",
    "rail_wall",
    "rail_width",
    "rail_height",
)
def _rail_wall_fits_section(p: Values) -> str | None:
    limit = min(p["rail_width"], p["rail_height"]) / 2.0
    if p["rail_wall"] >= limit:
        return f"rail wall {_mm(p['rail_wall'])} must be less than {_mm(limit)}"
    return None


@_rule(
    "frame_clears_tyres",
    "Frame rails must clear the inner tyre faces (straight ahead).",
    "rail_spacing",
    "rail_width",
    "track_front",
    "track_rear",
    "tyre_width",
)
def _frame_clears_tyres(p: Values) -> str | None:
    rail_outer = (p["rail_spacing"] + p["rail_width"]) / 2.0
    tyre_inner = (min(p["track_front"], p["track_rear"]) - p["tyre_width"]) / 2.0
    gap = tyre_inner - rail_outer
    if gap < 30:
        return f"frame rails are only {_mm(gap)} from the inner tyre face (minimum 30 mm)"
    return None


def _suspension_rules(a: str) -> None:
    A = a.capitalize()  # noqa: N806
    mount = (f"{a}_shock_mount_height", f"{a}_damper_stroke", "rim_diameter", "tyre_width",
             "tyre_aspect_ratio")  # fmt: skip

    @_rule(
        f"{a}_damper_fits_mounts",
        f"{A} dampers must fit between their mounts (within their length range).",
        *mount,
    )
    def _fits(p: Values) -> str | None:
        length = d.damper_installed_length(p, a)
        lo, hi = d.damper_min_length(p, a), d.damper_max_length(p, a)
        if not lo <= length <= hi:
            return (
                f"{a} damper length between mounts {_mm(length)} is outside its range "
                f"{_mm(lo)}–{_mm(hi)}"
            )
        return None

    @_rule(
        f"{a}_stroke_covers_travel",
        f"{A} damper stroke must cover bump plus rebound travel.",
        f"{a}_damper_stroke",
        f"{a}_bump_travel",
        f"{a}_rebound_travel",
    )
    def _stroke(p: Values) -> str | None:
        travel = p[f"{a}_bump_travel"] + p[f"{a}_rebound_travel"]
        if p[f"{a}_damper_stroke"] < travel:
            return (
                f"{a} damper stroke {_mm(p[f'{a}_damper_stroke'])} is shorter than bump plus "
                f"rebound travel {_mm(travel)}"
            )
        return None

    @_rule(
        f"{a}_shock_mount_inside_body",
        f"{A} upper damper mounts must sit at least 50 mm below the beltline.",
        f"{a}_shock_mount_height",
        "beltline_height",
    )
    def _inside(p: Values) -> str | None:
        limit = p["beltline_height"] - 50.0
        if p[f"{a}_shock_mount_height"] > limit:
            return (
                f"{a} upper damper mount {_mm(p[f'{a}_shock_mount_height'])} is above "
                f"{_mm(limit)} (50 mm below the beltline)"
            )
        return None

    @_rule(
        f"{a}_springs_clear_tyres",
        f"{A} coil springs must clear the inner tyre faces by 20 mm.",
        "spring_coil_diameter",
        f"{a}_spring_rate",
        "rail_spacing",
        f"track_{a}",
        "tyre_width",
    )
    def _clear(p: Values) -> str | None:
        spring_outer = p["rail_spacing"] / 2.0 + d.spring_outer_diameter(p, a) / 2.0
        gap = (p[f"track_{a}"] - p["tyre_width"]) / 2.0 - spring_outer
        if gap < 20:
            return f"{a} coil springs are only {_mm(gap)} from the inner tyre face (minimum 20 mm)"
        return None

    @_rule(
        f"{a}_spring_index",
        f"{A} spring index (coil / wire diameter) must be 4–12.",
        "spring_coil_diameter",
        f"{a}_spring_rate",
    )
    def _index(p: Values) -> str | None:
        index = p["spring_coil_diameter"] / d.spring_wire_diameter(p, a)
        if not 4.0 <= index <= 12.0:
            return (
                f"{a} spring index {index:.1f} is outside 4–12: the coil is impractical to "
                "manufacture; change the coil diameter"
            )
        return None

    @_rule(
        f"{a}_spring_clears_coil_bind",
        f"{A} springs must not reach solid length at full bump travel.",
        *mount,
        f"{a}_spring_rate",
        "spring_coil_diameter",
        f"{a}_bump_travel",
        "arch_clearance",
    )
    def _bind(p: Values) -> str | None:
        squeezed = d.spring_installed_length(p, a) - d.available_bump_travel(p, a)
        solid = d.spring_solid_length(p, a)
        if squeezed < solid:
            return (
                f"{a} springs compress to {_mm(squeezed)} at full bump, below their solid "
                f"length {_mm(solid)} (coil bind)"
            )
        return None

    @_rule(
        f"{a}_positive_sprung_mass",
        f"{A} sprung corner mass must be positive.",
        "vehicle_mass",
        "front_mass_distribution",
        f"{a}_unsprung_mass",
    )
    def _sprung(p: Values) -> str | None:
        m = d.sprung_corner_mass(p, a)
        if m <= 0:
            return (
                f"{a} sprung corner mass is {m:.1f} kg: the unsprung mass exceeds the corner load"
            )
        return None


for _axle in d.AXLES:
    _suspension_rules(_axle)


RULES: tuple[Rule, ...] = tuple(r for r, _ in _RULES)


def check_bounds(p: Values) -> list[Violation]:
    out = []
    for pid, value in p.items():
        spec = REGISTRY[pid]
        if not spec.min <= value <= spec.max:
            out.append(
                Violation(
                    rule="bounds",
                    message=(
                        f"{spec.label} {value:g} {spec.unit} is outside "
                        f"{spec.min:g}–{spec.max:g} {spec.unit}"
                    ),
                    parameters=(pid,),
                )
            )
    return out


def check_rules(p: Values) -> list[Violation]:
    out = []
    for rule, fn in _RULES:
        message = fn(p)
        if message is not None:
            out.append(Violation(rule=rule.id, message=message, parameters=rule.parameters))
    return out


def validate(p: Values) -> list[Violation]:
    """All violations for a complete parameter set: bounds first, then rules."""
    missing = set(REGISTRY) - set(p)
    if missing:
        raise KeyError(f"missing parameters: {sorted(missing)}")
    return check_bounds(p) + check_rules(p)
