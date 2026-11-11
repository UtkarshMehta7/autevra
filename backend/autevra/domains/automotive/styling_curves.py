"""Styling curves: designer-drawn guide curves for the styled body, edited in the studio.

A project may override any of the styled skin's guide curves with its own control points
(vehicle frame, mm): the side silhouette's top line and underbody line (x, z), and the
plan's half width (x, y). Curves not given are derived from the body style as before. The
design's length, width and height still clip the skin, so the engineering dimensions and
the drawn shape stay consistent.

The curves reach the body, glazing, lamp and seat builders as flat numeric inputs, so
they take part in geometry caching like any other input.
"""

from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator

CURVES = ("top", "bottom", "plan")
PREFIX = "styling_"
# Builders whose geometry follows the styled skin.
STYLED_BUILDERS = ("body", "glass", "head_lamps", "tail_lamps", "seats")

Point = tuple[float, float]


class StylingDoc(BaseModel):
    model_config = ConfigDict(frozen=True)

    top: list[Point] | None = Field(None, min_length=3, max_length=60)
    bottom: list[Point] | None = Field(None, min_length=3, max_length=60)
    plan: list[Point] | None = Field(None, min_length=3, max_length=60)

    @model_validator(mode="after")
    def _increasing(self) -> "StylingDoc":
        for name in CURVES:
            pts = getattr(self, name)
            if pts is None:
                continue
            xs = [x for x, _ in pts]
            if any(b <= a for a, b in zip(xs, xs[1:], strict=False)):
                raise ValueError(f"{name} curve points must run from rear to front (x increasing)")
            if name == "plan" and any(y <= 0.0 for _, y in pts):
                raise ValueError("plan half widths must be positive")
        return self


def to_inputs(doc: StylingDoc | None) -> dict[str, float]:
    """Flatten the curves into numeric builder inputs."""
    out: dict[str, float] = {}
    if doc is None:
        return out
    for name in CURVES:
        pts = getattr(doc, name)
        if pts is None:
            continue
        for i, (x, v) in enumerate(pts):
            out[f"{PREFIX}{name}_x{i}"] = float(x)
            out[f"{PREFIX}{name}_v{i}"] = float(v)
    return out


def effective(body_inputs: Mapping[str, float], doc: StylingDoc | None) -> dict:
    """The curves the skin uses (the project's own, or the style's sampled as control
    points) and reference geometry for an editor."""
    from autevra.domains.automotive import builders as b
    from autevra.domains.automotive import styled

    p = dict(body_inputs) | to_inputs(doc)
    layout = b.body_layout(p)
    g = styled.guides(p, layout)
    n = 16
    xs = [g.rear + (g.front - g.rear) * i / n for i in range(n + 1)]

    def sample(f):  # type: ignore[no-untyped-def]
        return [(round(x, 1), round(f(x), 1)) for x in xs]

    curves = {
        "top": doc.top if doc and doc.top else sample(g.top),
        "bottom": doc.bottom if doc and doc.bottom else sample(g.bottom),
        "plan": doc.plan if doc and doc.plan else sample(g.width),
    }
    return {
        "curves": {k_: [list(pt) for pt in v] for k_, v in curves.items()},
        "custom": {name: bool(doc and getattr(doc, name)) for name in CURVES},
        "reference": {
            "rear": g.rear, "front": g.front, "wheelbase": p["wheelbase"],
            "tyre_radius": p["tyre_radius"], "overall_height": p["overall_height"],
            "half_width": p["body_width"] / 2.0, "beltline": p["beltline_height"],
            "glass": list(layout.glass), "roof": list(layout.roof),
        },
    }  # fmt: skip


def from_inputs(p: Mapping[str, float], name: str) -> list[Point] | None:
    pts = []
    i = 0
    while f"{PREFIX}{name}_x{i}" in p:
        pts.append((p[f"{PREFIX}{name}_x{i}"], p[f"{PREFIX}{name}_v{i}"]))
        i += 1
    return pts or None
