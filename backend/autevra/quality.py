"""Quality: one-dimensional tolerance stack-ups and process capability.

A stack is a chain of contributors, each with a nominal, a symmetric or asymmetric
tolerance and a direction (+1 or -1) along the measured gap. Results:
- nominal gap = sum(direction x nominal);
- worst case: every contributor at its limit, gap range = nominal +- sum(tolerance);
- statistical (root sum of squares): each tolerance taken as +-3 sigma of a centred normal
  distribution, sigma_gap = sqrt(sum((t_i / 3)^2)), range = nominal +- 3 sigma_gap;
- against the gap's specification limits: the worst-case verdict, the RSS process
  capability Cpk = min(USL - mean, mean - LSL) / (3 sigma) and the expected fraction
  outside the limits (normal distribution).
Asymmetric tolerances are re-centred (mean shifted to the middle of the band) before both
methods. Limits: 1D chains only; no geometric (GD&T) form or orientation contributions.
"""

import math

from pydantic import BaseModel, Field, model_validator


class Contributor(BaseModel):
    name: str
    nominal: float
    plus: float = Field(ge=0)
    minus: float = Field(ge=0)
    direction: int = Field(1)

    @model_validator(mode="after")
    def _dir(self) -> "Contributor":
        if self.direction not in (1, -1):
            raise ValueError("direction is +1 or -1")
        return self

    @property
    def centre(self) -> float:
        return self.nominal + (self.plus - self.minus) / 2

    @property
    def half_band(self) -> float:
        return (self.plus + self.minus) / 2


class Stack(BaseModel):
    name: str
    contributors: list[Contributor] = Field(min_length=1)
    lsl: float | None = None  # lower specification limit of the gap
    usl: float | None = None


def _phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def analyse(stack: Stack) -> dict:
    nominal = sum(c.direction * c.nominal for c in stack.contributors)
    mean = sum(c.direction * c.centre for c in stack.contributors)
    wc = sum(c.half_band for c in stack.contributors)
    sigma = math.sqrt(sum((c.half_band / 3) ** 2 for c in stack.contributors))
    out = {"nominal": nominal, "mean": mean, "worst_case": [mean - wc, mean + wc],
           "rss": [mean - 3 * sigma, mean + 3 * sigma], "sigma": sigma,
           "contributions": {c.name: (c.half_band / 3) ** 2 / sigma**2 if sigma else 0.0
                             for c in stack.contributors}}  # fmt: skip
    if stack.lsl is not None or stack.usl is not None:
        lo = stack.lsl if stack.lsl is not None else -math.inf
        hi = stack.usl if stack.usl is not None else math.inf
        out["worst_case_ok"] = lo <= mean - wc and mean + wc <= hi
        if sigma > 0:
            cpk = min((hi - mean) / (3 * sigma), (mean - lo) / (3 * sigma))
            out["cpk"] = cpk
            out["ppm_out"] = 1e6 * ((1 - _phi((hi - mean) / sigma)) + _phi((lo - mean) / sigma))
    return out
