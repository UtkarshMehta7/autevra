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
Resistance: viscous by the ITTC-1957 friction line C_F = 0.075 / (log10 Rn - 2)^2 with
Watanabe's form factor k = -0.095 + 25.6 Cb / ((L/B)^2 sqrt(B/T)) and Holtrop's wetted
surface; wave-making, immersed-transom and model-ship correlation resistance by Holtrop
and Mennen's statistical method (1982, revised 1984), a regression on model tests of
displacement ships. It is an estimate for conventional forms at Froude numbers up to about
0.45 (above 0.55 the method's high-speed formula is used, with less support in its data);
it does not cover planing. The hull form here has no bulb and its transom is immersed over
the full section, which the method penalises (c5 and the transom term).
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


def holtrop_wave(length: float, beam: float, draft: float, volume: float, cp: float,
                 cm: float, cwp: float, lcb_pct: float, transom_area: float, speed: float,
                 bulb_area: float = 0.0, bulb_height: float = 0.0) -> dict:  # fmt: skip
    """Wave-making resistance by Holtrop and Mennen (1984), N.

    ``lcb_pct`` is the centre of buoyancy forward of midships in percent of the length;
    ``bulb_area`` and ``bulb_height`` (transverse bulb area and the height of its centre
    above the keel) are zero for a hull without a bulb.
    """
    lw, b, t = length, beam, draft
    fn = speed / math.sqrt(G * lw)
    lr = lw * (1 - cp + 0.06 * cp * lcb_pct / (4 * cp - 1))  # length of the run
    ie = 1 + 89 * math.exp(-((lw / b) ** 0.80856) * (1 - cwp) ** 0.30484
                           * (1 - cp - 0.0225 * lcb_pct) ** 0.6367 * (lr / b) ** 0.34574
                           * (100 * volume / lw**3) ** 0.16302)  # fmt: skip
    ratio = b / lw
    c7 = (0.229577 * ratio ** (1 / 3) if ratio < 0.11 else ratio if ratio <= 0.25
          else 0.5 - 0.0625 / ratio)  # fmt: skip
    c1 = 2223105 * c7**3.78613 * (t / b) ** 1.07961 * (90 - ie) ** -1.37565
    c3 = (0.56 * bulb_area**1.5 / (b * t * (0.31 * math.sqrt(bulb_area) + t - bulb_height))
          if bulb_area > 0 else 0.0)  # fmt: skip
    c2 = math.exp(-1.89 * math.sqrt(c3))
    c5 = 1 - 0.8 * transom_area / (b * t * cm)
    c16 = (8.07981 * cp - 13.8673 * cp**2 + 6.984388 * cp**3 if cp < 0.8
           else 1.73014 - 0.7067 * cp)  # fmt: skip
    m1 = 0.0140407 * lw / t - 1.75254 * volume ** (1 / 3) / lw - 4.79323 * b / lw - c16
    slender = lw**3 / volume
    c15 = (-1.69385 if slender < 512 else 0.0 if slender > 1726.91
           else -1.69385 + (lw / volume ** (1 / 3) - 8) / 2.36)  # fmt: skip
    lam = 1.446 * cp - (0.03 * lw / b if lw / b < 12 else 0.36)
    weight = volume * RHO_SW * G

    def low(f: float) -> float:  # Fn <= 0.4
        m4 = c15 * 0.4 * math.exp(-0.034 * f**-3.29)
        return c1 * c2 * c5 * weight * math.exp(m1 * f**-0.9 + m4 * math.cos(lam * f**-2))

    def high(f: float) -> float:  # Fn >= 0.55
        c17 = 6919.3 * cm**-1.3346 * (volume / lw**3) ** 2.00977 * (lw / b - 2) ** 1.40692
        m3 = -7.2035 * (b / lw) ** 0.326869 * (t / b) ** 0.605375
        m4 = c15 * 0.4 * math.exp(-0.034 * f**-3.29)
        return c17 * c2 * c5 * weight * math.exp(m3 * f**-0.9 + m4 * math.cos(lam * f**-2))

    if fn <= 0.4:
        rw = low(fn)
    elif fn >= 0.55:
        rw = high(fn)
    else:
        rw = low(0.4) + (10 * fn - 4) * (high(0.55) - low(0.4)) / 1.5
    return {"rw_n": rw, "froude": fn, "half_entrance_deg": ie, "c1": c1, "c2": c2, "c5": c5,
            "m1": m1, "lambda": lam, "run_length_m": lr}  # fmt: skip


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
    # Wave-making, immersed transom and correlation allowance (Holtrop and Mennen).
    volume = cb * lw * b * t
    cwp = 1 - (2 - spec.transom) / (2 * (spec.exponent + 1))
    at = spec.transom * b * t * spec.cm  # the aft section is immersed over its full depth
    wave = holtrop_wave(lw, b, t, volume, spec.cp, spec.cm, cwp, lcb_percent(spec), at, v)
    rtr = 0.0
    if at > 0:
        fnt = v / math.sqrt(2 * G * at / (b + b * cwp))
        rtr = 0.5 * RHO_SW * v * v * at * (0.2 * (1 - 0.2 * fnt) if fnt < 5 else 0.0)
    ca = 0.006 * (lw + 100) ** -0.16 - 0.00205
    ra = 0.5 * RHO_SW * v * v * s * ca
    total = rv + wave["rw_n"] + rtr + ra
    return {"speed_ms": v, "froude": fn, "reynolds": rn, "cf": cf, "form_factor": 1 + k,
            "wetted_surface_m2": s, "viscous_resistance_n": rv,
            "wave_resistance_n": wave["rw_n"], "transom_resistance_n": rtr,
            "correlation_resistance_n": ra, "total_resistance_n": total,
            "half_entrance_deg": wave["half_entrance_deg"],
            "effective_power_kw": total * v / 1000,
            "delivered_power_kw": total * v / 1000 / 0.6,
            "effective_power_kw_lower_bound": rv * v / 1000,
            "delivered_power_kw_lower_bound": rv * v / 1000 / 0.6}  # fmt: skip


def lcb_percent(spec: HullSpec) -> float:
    """Centre of buoyancy forward of midships, percent of the length (closed form: every
    section has the same fullness, so the volume is distributed like the waterline)."""
    p, tr = spec.exponent, spec.transom
    # integral of f and of f * (xi - 1/2) over each half, with u = |2 xi - 1|
    fore_a, aft_a = 0.5 * (1 - 1 / (p + 1)), 0.5 * (1 - (1 - tr) / (p + 1))
    fore_m = 0.25 * (0.5 - 1 / (p + 2))
    aft_m = -0.25 * (0.5 - (1 - tr) / (p + 2))
    return 100.0 * (fore_m + aft_m) / (fore_a + aft_a)
