"""A parametric monohull: form, hydrostatics, large-angle stability and viscous resistance.

Form (x from the aft perpendicular to the forward one, z up from the keel, half-breadths y):
- sections: y = (B/2) f(x) (z/T)^(1/n) below the waterline and wall-sided above it, with
  n = Cm / (1 - Cm), so every section's fullness below the waterline equals the midship
  coefficient Cm;
- waterlines: f(xi) = 1 - |2 xi - 1|^p forward of midships and
  1 - (1 - t) (1 - 2 xi)^p aft of it (t: transom width / beam), with p chosen so the
  prismatic coefficient is exactly Cp; the block coefficient is then Cb = Cp Cm.
Hydrostatics by numerical integration over stations and heights: volume, LCB, KB, the
waterplane (area, LCF, transverse and longitudinal second moments), BM = I_T / V,
BM_L = I_L / V, KM, GM = KM - KG, tonnes per centimetre immersion and the moment to change
trim one centimetre.
Large-angle stability: each section (closed at the deck) is clipped by the inclined
waterline (Sutherland-Hodgman) and the waterline height is found by bisection so the
displaced volume stays constant (free trim neglected); GZ = y_B cos(phi) + (z_B - KG)
sin(phi). Criteria: IMO Intact Stability Code 2008, Part A 2.2 (areas under GZ 0-30°
>= 0.055 m·rad, 0-40° >= 0.090, 30-40° >= 0.030; GZ >= 0.20 m at 30° or more; maximum GZ
at 25° or more; GM0 >= 0.15 m), without downflooding angles or weather criteria.
Resistance (viscous only): ITTC-1957 friction line C_F = 0.075 / (log10 Rn - 2)^2, form
factor by Watanabe k = -0.095 + 25.6 Cb / ((L/B)^2 sqrt(B/T)), wetted surface by
Holtrop's formula (no bulb); wave-making resistance is not modelled yet, so the effective
power is a lower bound, increasingly so above a Froude number of about 0.25.
"""

import math

import numpy as np
from pydantic import BaseModel, Field, model_validator

RHO_SW = 1025.0  # kg/m³
NU_SW = 1.188e-6  # m²/s at 15 °C
G = 9.80665


class HullSpec(BaseModel):
    name: str = "12 m workboat"
    length: float = Field(12.0, gt=2.0, le=400.0)  # waterline length, m
    beam: float = Field(4.0, gt=0.5, le=70.0)
    draft: float = Field(1.0, gt=0.1, le=25.0)
    depth: float = Field(2.0, gt=0.2, le=40.0)  # keel to deck at the side
    cp: float = Field(0.64, ge=0.5, le=0.9)  # prismatic
    cm: float = Field(0.78, ge=0.5, le=0.995)  # midship
    transom: float = Field(0.55, ge=0.0, le=0.95)  # transom width / beam
    kg: float = Field(1.0, gt=0.0, le=40.0)  # centre of gravity above the keel, m
    speed_kn: float = Field(7.0, gt=0.5, le=60.0)
    material: str = "steel"  # steel | aluminium | grp

    @model_validator(mode="after")
    def _form(self) -> "HullSpec":
        if self.depth <= self.draft:
            raise ValueError("the depth must exceed the draft (freeboard)")
        if self.exponent < 0.6:
            raise ValueError("this prismatic is too low for the transom width; raise Cp or "
                             "narrow the transom")  # fmt: skip
        return self

    @property
    def exponent(self) -> float:
        """p making the waterline's prismatic exactly Cp (see the module notes)."""
        return (2 - self.transom) / (2 * (1 - self.cp)) - 1

    @property
    def section_n(self) -> float:
        return self.cm / (1 - self.cm)


def half_breadth_factor(spec: HullSpec, xi: np.ndarray) -> np.ndarray:
    p = spec.exponent
    fwd = 1 - np.abs(2 * xi - 1) ** p
    aft = 1 - (1 - spec.transom) * np.abs(1 - 2 * xi) ** p
    return np.where(xi >= 0.5, fwd, aft)


def half_breadth(spec: HullSpec, xi: np.ndarray, z: np.ndarray) -> np.ndarray:
    """y(x, z) on a grid (xi along, z up)."""
    f = half_breadth_factor(spec, xi)[:, None]
    shape = np.clip(z / spec.draft, 0, 1)[None, :] ** (1 / spec.section_n)
    return spec.beam / 2 * f * shape


def _grids(spec: HullSpec, nx: int = 101, nz: int = 200) -> tuple[np.ndarray, np.ndarray]:
    return np.linspace(0, 1, nx), np.linspace(0, spec.depth, nz)


def hydrostatics(spec: HullSpec, draft: float | None = None) -> dict:
    d = spec.draft if draft is None else draft
    xi = np.linspace(0, 1, 201)
    z = np.linspace(0, d, 400)
    y = half_breadth(spec, xi, z)
    x = xi * spec.length
    areas = np.trapezoid(2 * y, z, axis=1)  # section areas
    moments_z = np.trapezoid(2 * y * z[None, :], z, axis=1)
    vol = float(np.trapezoid(areas, x))
    lcb = float(np.trapezoid(areas * x, x) / vol)
    kb = float(np.trapezoid(moments_z, x) / vol)
    yw = half_breadth(spec, xi, np.array([d]))[:, 0]
    aw = float(np.trapezoid(2 * yw, x))
    lcf = float(np.trapezoid(2 * yw * x, x) / aw)
    it = float(np.trapezoid(2 / 3 * yw**3, x))
    il = float(np.trapezoid(2 * yw * (x - lcf) ** 2, x))
    bm, bml = it / vol, il / vol
    km = kb + bm
    disp = vol * RHO_SW
    return {"draft": d, "volume_m3": vol, "displacement_t": disp / 1000, "lcb_m": lcb,
            "kb_m": kb, "bm_m": bm, "km_m": km, "gm_m": km - spec.kg, "bml_m": bml,
            "waterplane_m2": aw, "lcf_m": lcf, "tpc_t": aw * RHO_SW / 100 / 1000,
            "mct_tm": disp / 1000 * (kb + bml - spec.kg) / (100 * spec.length),
            "cb": vol / (spec.length * spec.beam * d), "midship_area_m2": float(areas.max()),
            "section_areas": areas.tolist(), "stations": x.tolist()}  # fmt: skip


def _section_polygon(spec: HullSpec, xi: float, nz: int = 24) -> list[tuple[float, float]]:
    z = np.linspace(0, spec.depth, nz)
    y = half_breadth(spec, np.array([xi]), z)[0]
    right = list(zip(y, z, strict=True))
    left = [(-yy, zz) for yy, zz in reversed(right)]
    return right + left  # closed at the deck by the last/first points


def _clip(poly: list[tuple[float, float]], s: float, c: float, h: float) -> list:
    """Part of a polygon with z cos(phi) - y sin(phi) <= h (c = cos, s = sin)."""

    def inside(p: tuple[float, float]) -> bool:
        return p[1] * c - p[0] * s <= h

    out = []
    for i, cur in enumerate(poly):
        prev = poly[i - 1]
        if inside(cur):
            if not inside(prev):
                out.append(_cross(prev, cur, s, c, h))
            out.append(cur)
        elif inside(prev):
            out.append(_cross(prev, cur, s, c, h))
    return out


def _cross(a: tuple[float, float], b: tuple[float, float], s: float, c: float, h: float):  # type: ignore[no-untyped-def]
    fa, fb = a[1] * c - a[0] * s - h, b[1] * c - b[0] * s - h
    t = fa / (fa - fb)
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def _area_centroid(poly: list) -> tuple[float, float, float]:
    if len(poly) < 3:
        return 0.0, 0.0, 0.0
    a = cy = cz = 0.0
    for i, (y1, z1) in enumerate(poly):
        y0, z0 = poly[i - 1]
        cross = y0 * z1 - y1 * z0
        a += cross
        cy += (y0 + y1) * cross
        cz += (z0 + z1) * cross
    a /= 2
    if abs(a) < 1e-12:
        return 0.0, 0.0, 0.0
    return abs(a), cy / (6 * a), cz / (6 * a)


def gz_curve(spec: HullSpec, angles: list[float] | None = None) -> list[dict[str, float]]:
    angles = angles or [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80]
    target = hydrostatics(spec)["volume_m3"]
    xis = np.linspace(0, 1, 25)
    dx = spec.length / (len(xis) - 1)
    polys = [_section_polygon(spec, float(xi)) for xi in xis]
    weights = np.full(len(xis), dx)
    weights[[0, -1]] = dx / 2
    out = []
    for deg in angles:
        phi = math.radians(deg)
        s, c = math.sin(phi), math.cos(phi)

        def immersed(h: float, s: float = s, c: float = c) -> tuple[float, float, float]:
            v = my = mz = 0.0
            for w, poly in zip(weights, polys, strict=True):
                a, cy, cz = _area_centroid(_clip(poly, s, c, h))
                v += w * a
                my += w * a * cy
                mz += w * a * cz
            return v, my, mz

        lo, hi = -spec.beam - spec.depth, spec.beam + spec.depth
        for _ in range(36):
            mid = (lo + hi) / 2
            if immersed(mid)[0] < target:
                lo = mid
            else:
                hi = mid
        v, my, mz = immersed((lo + hi) / 2)
        yb, zb = my / v, mz / v
        gz = yb * c + (zb - spec.kg) * s
        out.append({"angle": float(deg), "gz_m": float(gz)})
    return out


def imo_criteria(spec: HullSpec, curve: list[dict[str, float]] | None = None) -> list[dict]:
    curve = curve or gz_curve(spec, [float(a) for a in range(0, 81, 5)])
    ang = np.array([p["angle"] for p in curve])
    gz = np.array([p["gz_m"] for p in curve])
    rad = np.radians(ang)

    def area(a0: float, a1: float) -> float:
        m = (ang >= a0) & (ang <= a1)
        return float(np.trapezoid(gz[m], rad[m]))

    gz30 = float(np.interp(30, ang, gz))
    peak = float(ang[int(np.argmax(gz))])
    gm = hydrostatics(spec)["gm_m"]

    def row(label: str, value: float, limit: float, unit: str) -> dict:
        return {"criterion": label, "value": value, "limit": limit, "unit": unit,
                "pass": value >= limit}  # fmt: skip

    return [row("area under GZ 0-30°", area(0, 30), 0.055, "m·rad"),
            row("area under GZ 0-40°", area(0, 40), 0.090, "m·rad"),
            row("area under GZ 30-40°", area(30, 40), 0.030, "m·rad"),
            row("GZ at 30° or more", max(gz30, float(gz[ang >= 30].max())), 0.20, "m"),
            row("angle of maximum GZ", peak, 25.0, "°"),
            row("initial GM", gm, 0.15, "m")]  # fmt: skip


def wetted_surface(spec: HullSpec) -> float:
    """Holtrop and Mennen's wetted-surface formula (no bulbous bow)."""
    lw, b, t = spec.length, spec.beam, spec.draft
    cb, cm = spec.cp * spec.cm, spec.cm
    cwp = 1 - (2 - spec.transom) / (2 * (spec.exponent + 1))  # waterplane coefficient
    return lw * (2 * t + b) * math.sqrt(cm) * (0.453 + 0.4425 * cb - 0.2862 * cm
                                             - 0.003467 * b / t + 0.3696 * cwp)  # fmt: skip


def resistance(spec: HullSpec, speed_kn: float | None = None) -> dict:
    v = (speed_kn or spec.speed_kn) * 0.514444
    lw, b, t = spec.length, spec.beam, spec.draft
    cb = spec.cp * spec.cm
    rn = v * lw / NU_SW
    cf = 0.075 / (math.log10(rn) - 2) ** 2
    k = -0.095 + 25.6 * cb / ((lw / b) ** 2 * math.sqrt(b / t))
    s = wetted_surface(spec)
    rv = 0.5 * RHO_SW * v * v * s * cf * (1 + k)
    fn = v / math.sqrt(G * lw)
    return {"speed_ms": v, "froude": fn, "reynolds": rn, "cf": cf, "form_factor": 1 + k,
            "wetted_surface_m2": s, "viscous_resistance_n": rv,
            "effective_power_kw_lower_bound": rv * v / 1000,
            "delivered_power_kw_lower_bound": rv * v / 1000 / 0.6}  # fmt: skip
