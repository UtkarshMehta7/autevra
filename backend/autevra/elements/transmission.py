"""Stepped transmission for a road vehicle: gear ratios from the vehicle's driving
requirements, then a two-shaft helical transaxle that realises them, with performance.

Ratios (overall i = gearbox i_g x final drive i_f):
- First gear from the larger of the gradeability requirement at full load, at the
  engine's peak torque, i_1 = r_dyn (m g (f_R cos a + sin a)) / (T_max eta), and the launch
  requirement that first gear tops out at about 60 km/h at the redline (creep speed and
  clutch take-up; trailer starts).
- Top gear from the top-speed strategy: "power" puts the top speed (where the power
  available meets the road load) at the power peak; "overdrive" lets the engine run at
  85 % of the power-peak speed at top speed (a quieter, more economical top gear).
- Between them, geometric steps phi = (i_1 / i_n)^(1/(n-1)), or the progressive layout
  (Jante) i_k = i_n phi_1^(n-k) phi_2^((n-k)(n-k-1)/2) with phi_2 = 1.05-1.1, so the higher
  gears sit closer together where the road load rises fastest.

Transaxle (input shaft to output shaft, one helical pair per gear, all on one centre
distance a): normal module m_n per gear from bending and contact stress, tooth sum
z1 + z2 = floor(2 a cos(beta_0) / m_n), pinion z1 = round(z_sum / (1 + i)), and the helix
angle of each pair solved so that pair sits exactly on a: cos(beta) = m_n z_sum / (2 a)
(production practice; no profile shift needed). Centre distance by the empirical
a = 13 T_in^(1/3) mm unless given.

Rating per pair (pinion) after ISO 6336 at the engine's peak torque, as automotive gears
are rated to a load spectrum: bending sigma_F = F_t / (b m_n) Y_FS Y_eps Y_beta K_V against
sigma_FP = sigma_Flim Y_ST Y_NT / S_Fmin, contact
sigma_H = Z_E Z_H Z_eps Z_beta sqrt(K_V F_t (u + 1) / (b d_1 u)) against
sigma_HP = sigma_Hlim Z_NT / S_Hmin, for case-hardened 16MnCr5 (sigma_Flim 500,
sigma_Hlim 1500 MPa). The life factors Y_NT and Z_NT come from the load cycles at full
torque: life distance x the share driven in that gear x the full-load share x the input
shaft revolutions per wheel revolution. Application factor 1 (the peak torque is the
load); K_V 1.05; K_Hbeta, K_Halpha and the size, roughness and lubricant factors are
left at 1. Shaft diameters from torsion, d = (16 T / (pi tau))^(1/3), tau 55 MPa.

Performance: tractive force F = T(n) i eta / r_dyn capped at the driven wheels' grip
with longitudinal load transfer (``traction_limit``), road load
F_R = m g f_R + rho/2 c_d A v^2, rotating-mass factor delta = 1.04 + 0.0025 i^2;
0-100 km/h by time-stepping full load with 0.3 s shifts at the redline; top speed where
the best gear's force meets the road load.
"""

import math
from typing import Literal

from pydantic import BaseModel, Field, model_validator

G = 9.80665
RHO = 1.204
MODULES = (1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 4.5, 5.0)
SIGMA_F_ALLOW = 350.0
SIGMA_H_ALLOW = 1500.0
TAU_SHAFT = 55.0


class EngineCurve(BaseModel):
    idle_rpm: float = Field(800.0, ge=300.0, le=3000.0)
    peak_torque_Nm: float = Field(320.0, gt=10.0, le=5000.0)  # noqa: N815
    torque_from_rpm: float = Field(1800.0, gt=500.0)
    torque_to_rpm: float = Field(4000.0, gt=500.0)
    peak_power_kW: float = Field(150.0, gt=5.0, le=2000.0)  # noqa: N815
    power_rpm: float = Field(5800.0, gt=1000.0)
    redline_rpm: float = Field(6500.0, gt=1000.0)

    @model_validator(mode="after")
    def _order(self) -> "EngineCurve":
        if (
            not self.idle_rpm
            < self.torque_from_rpm
            <= self.torque_to_rpm
            < self.power_rpm
            <= self.redline_rpm
        ):
            raise ValueError(
                "engine speeds must rise: idle < torque plateau <= power peak <= redline"
            )
        plateau_power = self.peak_torque_Nm * self.torque_to_rpm * math.pi / 30.0 / 1000.0
        if plateau_power > self.peak_power_kW * 1.0001:
            raise ValueError(
                f"peak torque to {self.torque_to_rpm:g} rpm already gives {plateau_power:.0f} kW, "
                f"above the {self.peak_power_kW:g} kW peak power"
            )
        return self

    def torque(self, rpm: float) -> float:
        """Full-load torque: rising from 60 % at idle to the plateau, flat, then falling to
        the power peak (T = P / omega there), and on to the redline at 92 % of that."""
        t_max = self.peak_torque_Nm
        t_p = self.peak_power_kW * 1000.0 / (self.power_rpm * math.pi / 30.0)
        if rpm <= self.idle_rpm:
            return 0.6 * t_max
        if rpm < self.torque_from_rpm:
            return t_max * (
                0.6 + 0.4 * (rpm - self.idle_rpm) / (self.torque_from_rpm - self.idle_rpm)
            )
        if rpm <= self.torque_to_rpm:
            return t_max
        if rpm <= self.power_rpm:
            return t_max + (t_p - t_max) * (rpm - self.torque_to_rpm) / (
                self.power_rpm - self.torque_to_rpm
            )
        if rpm <= self.redline_rpm:
            span = max(self.redline_rpm - self.power_rpm, 1.0)
            return t_p * (1.0 - 0.08 * (rpm - self.power_rpm) / span)
        return 0.0


class TransmissionIn(BaseModel):
    mass_kg: float = Field(1600.0, gt=100.0, le=60_000.0)
    tyre_radius_m: float = Field(0.32, gt=0.15, le=1.0)  # dynamic rolling radius
    drag_area_m2: float = Field(0.70, gt=0.05, le=15.0)  # c_d x A
    rolling_resistance: float = Field(0.012, gt=0.003, le=0.05)
    driveline_efficiency: float = Field(0.92, gt=0.5, le=1.0)
    driven_axle_share: float = Field(0.58, gt=0.2, le=1.0)  # static load on the driven axle
    drive: Literal["front", "rear", "all"] = "front"
    cg_height_m: float = Field(0.55, gt=0.1, le=3.0)
    wheelbase_m: float = Field(2.7, gt=1.0, le=10.0)
    grip: float = Field(1.0, gt=0.2, le=1.6)
    engine: EngineCurve = EngineCurve()
    gears: int = Field(6, ge=3, le=10)
    gradeability: float = Field(35.0, gt=5.0, le=80.0)  # % slope in first at full load
    top_strategy: Literal["power", "overdrive"] = "overdrive"
    progression: Literal["geometric", "progressive"] = "progressive"
    phi2: float = Field(1.07, ge=1.0, le=1.2)
    top_gearbox_ratio: float = Field(0.80, gt=0.4, le=1.5)  # sets the final drive
    centre_distance: float | None = Field(None, gt=30.0, le=400.0)
    face_width: float = Field(18.0, gt=5.0, le=200.0)
    helix_deg: float = Field(25.0, ge=0.0, le=40.0)
    pressure_angle: float = Field(20.0, ge=14.5, le=25.0)
    first_gear_top_kmh: float = Field(60.0, gt=15.0, le=200.0)  # launch: 1st at the redline
    life_km: float = Field(250_000.0, gt=1_000.0, le=3_000_000.0)
    full_load_share: float = Field(0.05, gt=0.0, le=1.0)  # of the distance at peak torque


def road_load(t: TransmissionIn, v: float, grade: float = 0.0) -> float:
    a = math.atan(grade / 100.0)
    return (
        t.mass_kg * G * (t.rolling_resistance * math.cos(a) + math.sin(a))
        + 0.5 * RHO * t.drag_area_m2 * v * v
    )


def _speed(rpm: float, i: float, r: float) -> float:
    return rpm * math.pi / 30.0 * r / i  # m/s


def traction_limit(t: TransmissionIn) -> float:
    """Most tractive force the driven wheels transmit at full grip, with the longitudinal
    load transfer m a h / L under acceleration (rotating inertia neglected): rear drive
    gains load, F = mu m g s / (1 - mu h / L); front drive loses it, F = mu m g s / (1 + mu h / L);
    all-wheel drive F = mu m g (s: static share on the driven axle)."""
    w = t.mass_kg * G
    k = t.grip * t.cg_height_m / t.wheelbase_m
    if t.drive == "all":
        return t.grip * w
    if t.drive == "rear":
        return t.grip * w * t.driven_axle_share / max(1.0 - k, 0.2)
    return t.grip * w * t.driven_axle_share / (1.0 + k)


def ratios(t: TransmissionIn) -> tuple[list[float], float, float]:
    """Overall ratios (first to top), the top speed and the final drive."""
    e = t.engine
    grade = math.atan(t.gradeability / 100.0)
    need = t.mass_kg * G * (t.rolling_resistance * math.cos(grade) + math.sin(grade))
    i1_grade = need * t.tyre_radius_m / (e.peak_torque_Nm * t.driveline_efficiency)
    i1_launch = e.redline_rpm * math.pi / 30.0 * t.tyre_radius_m / (t.first_gear_top_kmh / 3.6)
    i1 = max(i1_grade, i1_launch)
    # top speed: power available at the wheels = road load power (bisection on v)
    p_w = e.peak_power_kW * 1000.0 * t.driveline_efficiency
    lo, hi = 1.0, 150.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if road_load(t, mid) * mid < p_w else (lo, mid)
    v_max = lo
    rpm_top = e.power_rpm if t.top_strategy == "power" else 0.85 * e.power_rpm
    i_top = rpm_top * math.pi / 30.0 * t.tyre_radius_m / v_max
    n = t.gears
    if i1 <= i_top * 1.2:
        i1 = i_top * 1.2 ** (n - 1)  # gradeability is easy: keep a sensible spread
    if t.progression == "geometric":
        phi = (i1 / i_top) ** (1.0 / (n - 1))
        out = [i_top * phi ** (n - 1 - k) for k in range(n)]
    else:
        m = n - 1
        phi1 = (i1 / i_top / t.phi2 ** (m * (m - 1) / 2.0)) ** (1.0 / m)
        if phi1 < 1.0:
            phi1 = (i1 / i_top) ** (1.0 / m)
            out = [i_top * phi1 ** (m - k) for k in range(n)]
        else:
            out = [
                i_top * phi1 ** (m - k) * t.phi2 ** ((m - k) * (m - k - 1) / 2.0) for k in range(n)
            ]
    final = i_top / t.top_gearbox_ratio
    return out, v_max, final


def usage_shares(n: int) -> list[float]:
    """Share of the distance driven in each gear (first to top): the higher gears carry most
    of it. A heuristic spectrum after Naunheimer et al., Automotive Transmissions."""
    w = [0.15 * 2.2**k for k in range(n)]
    total = sum(w)
    return [x / total for x in w]


def y_fs(zv: float) -> float:
    """Combined tooth form and stress correction factor of ISO 6336-3 for an unshifted
    tooth on the ISO 53 A rack (fit to the published curve, z_v 12-200)."""
    return 3.75 + 12.5 / zv


def life_factors(cycles: float) -> tuple[float, float]:
    """ISO 6336 life factors for case-hardened steel: Y_NT from 2.5 at 1e3 to 1 at 3e6
    load cycles, Z_NT from 1.6 at 1e5 to 1 at 5e7 (log-linear, static limits held)."""
    y = min(max((3e6 / max(cycles, 1.0)) ** (math.log(2.5) / math.log(3e3)), 1.0), 2.5)
    z = min(max((5e7 / max(cycles, 1.0)) ** (math.log(1.6) / math.log(500.0)), 1.0), 1.6)
    return y, z


SIGMA_F_LIM = 500.0  # 16MnCr5 case-hardened, MQ (ISO 6336-5)
SIGMA_H_LIM = 1500.0
Y_ST = 2.0
S_F_MIN = 1.3
S_H_MIN = 1.0
K_V = 1.05  # quality 6 ground gears at road speeds (dynamic factor, typical)


def _geometry(t: TransmissionIn, mn: float, z1: int, z2: int, a: float, b: float) -> dict | None:
    z_sum = z1 + z2
    cos_b = mn * z_sum / (2.0 * a)
    if not 0.7 < cos_b <= 1.0:
        return None
    beta = math.acos(cos_b)
    alpha_n = math.radians(t.pressure_angle)
    alpha_t = math.atan(math.tan(alpha_n) / cos_b)
    mt = mn / cos_b
    d1, d2 = z1 * mt, z2 * mt
    da1, da2 = d1 + 2 * mn, d2 + 2 * mn
    db1, db2 = d1 * math.cos(alpha_t), d2 * math.cos(alpha_t)
    pbt = math.pi * mt * math.cos(alpha_t)
    eps_a = (
        math.sqrt(da1**2 - db1**2) / 2 + math.sqrt(da2**2 - db2**2) / 2 - a * math.sin(alpha_t)
    ) / pbt
    eps_b = b * math.sin(beta) / (math.pi * mn)
    return {
        "face_width": b,
        "module": mn,
        "z1": z1,
        "z2": z2,
        "ratio": z2 / z1,
        "helix_deg": math.degrees(beta),
        "beta": beta,
        "alpha_t": alpha_t,
        "d1": d1,
        "d2": d2,
        "da1": da1,
        "da2": da2,
        "contact_ratio": eps_a,
        "overlap_ratio": eps_b,
    }


def _rate(t: TransmissionIn, g: dict, torque: float, rpm: float, cycles: float) -> dict:
    """ISO 6336-style bending and contact rating of the pinion at a torque, with life
    factors for the given load cycles (K_A = 1: the torque is already the peak)."""
    b, mn, beta, alpha_t = g["face_width"], g["module"], g["beta"], g["alpha_t"]
    ft = 2000.0 * torque / g["d1"]
    beta_b = math.atan(math.tan(beta) * math.cos(alpha_t))
    eps_an = g["contact_ratio"] / math.cos(beta_b) ** 2
    y_eps = 0.25 + 0.75 / eps_an
    y_beta = max(1.0 - min(g["overlap_ratio"], 1.0) * math.degrees(beta) / 120.0, 0.75)
    zv = g["z1"] / (math.cos(beta_b) ** 2 * math.cos(beta))
    sigma_f = ft / (b * mn) * y_fs(zv) * y_eps * y_beta * K_V
    zh = math.sqrt(2.0 * math.cos(beta_b) / (math.cos(alpha_t) ** 2 * math.tan(alpha_t)))
    eb = g["overlap_ratio"]
    ea = g["contact_ratio"]
    z_eps = math.sqrt(1.0 / ea) if eb >= 1.0 else math.sqrt((4 - ea) / 3 * (1 - eb) + eb / ea)
    u = g["ratio"]
    sigma_h = (
        189.8
        * zh
        * z_eps
        * math.sqrt(math.cos(beta))
        * math.sqrt(K_V * ft * (u + 1) / (b * g["d1"] * u))
    )
    ynt, znt = life_factors(cycles)
    sfp = SIGMA_F_LIM * Y_ST * ynt / S_F_MIN
    shp = SIGMA_H_LIM * znt / S_H_MIN
    return {
        "tangential_N": ft,
        "axial_N": ft * math.tan(beta),
        "radial_N": ft * math.tan(alpha_t),
        "pitch_speed": math.pi * g["d1"] / 1000.0 * rpm / 60.0,
        "sigma_F": sigma_f,
        "sigma_H": sigma_h,
        "sigma_FP": sfp,
        "sigma_HP": shp,
        "SF": S_F_MIN * sfp / sigma_f,
        "SH": S_H_MIN * shp / sigma_h,
        "Y_FS": y_fs(zv),
        "Y_eps": y_eps,
        "Y_beta": y_beta,
        "Z_H": zh,
        "Z_eps": z_eps,
        "Y_NT": ynt,
        "Z_NT": znt,
        "load_cycles": cycles,
    }


def _pair(
    t: TransmissionIn,
    i_g: float,
    a: float,
    torque_in: float,
    rpm_in: float,
    cycles: float,
    taken: set[tuple[int, int]],
) -> dict:
    """Smallest standard normal module whose pair passes, with the tooth numbers nearest the
    target ratio (helix angle 15-35 deg, solved to sit on the centre distance). A gear that
    fails at the nominal face width is widened (x1.25, then x1.5), as first and reverse
    gears are in production boxes. With nothing passing, the least-stressed option within
    3 % of the ratio is returned, flagged."""
    best_fail, best_score = None, math.inf
    for widen in (1.0, 1.25, 1.5):
        b = t.face_width * widen
        for mn in MODULES:
            nominal = 2.0 * a * math.cos(math.radians(t.helix_deg)) / mn
            options = []
            for z_sum in range(math.floor(nominal) - 3, math.floor(nominal) + 2):
                for z1 in range(max(round(z_sum / (1 + i_g)) - 1, 1), round(z_sum / (1 + i_g)) + 2):
                    z2 = z_sum - z1
                    if z1 < 12 or z2 < 12 or (z1, z2) in taken:
                        continue
                    g = _geometry(t, mn, z1, z2, a, b)
                    if g is None or not 15.0 <= g["helix_deg"] <= 35.0:
                        continue
                    err = abs(z2 / z1 - i_g) / i_g
                    options.append((err + 0.002 * abs(g["helix_deg"] - t.helix_deg) / 10, err, g))
            if not options:
                continue
            _, err, g = min(options, key=lambda o: o[0])
            r = _rate(t, g, torque_in, rpm_in, cycles)
            out = {**g, **r}
            out.pop("beta")
            out.pop("alpha_t")
            load = max(r["sigma_F"] / r["sigma_FP"], r["sigma_H"] / r["sigma_HP"])
            if load <= 1.0 and err <= 0.03:
                return out
            score = load + (10.0 if err > 0.03 else 0.0) + 0.01 * widen
            if score < best_score:
                best_fail, best_score = out, score
    if best_fail is None:
        raise ValueError(f"no standard module fits a {i_g:.2f} ratio on a {a:g} mm centre distance")
    best_fail["overloaded"] = True
    return best_fail


def design(t: TransmissionIn) -> dict:
    e = t.engine
    overall, v_max, final = ratios(t)
    gbox = [i / final for i in overall]
    a = t.centre_distance or round(2.0 * 13.0 * e.peak_torque_Nm ** (1.0 / 3.0)) / 2.0
    warnings: list[str] = []
    pairs = []
    shares = usage_shares(len(gbox))
    wheel_revs = t.life_km * 1000.0 / (2.0 * math.pi * t.tyre_radius_m)
    taken: set[tuple[int, int]] = set()
    for k, ig in enumerate(gbox):
        cycles = wheel_revs * shares[k] * t.full_load_share * overall[k]
        p = _pair(t, ig, a, e.peak_torque_Nm, e.torque_to_rpm, cycles, taken)
        taken.add((p["z1"], p["z2"]))
        p["usage_share"] = shares[k]
        p["target"] = ig
        p["error_pct"] = 100.0 * (p["ratio"] - ig) / ig
        pairs.append(p)
        if p.get("overloaded"):
            warnings.append(
                f"Gear {k + 1}: no standard module passes at a = {a:g} mm and "
                f"b = {1.5 * t.face_width:g} mm "
                f"(σF {p['sigma_F']:.0f} of {p['sigma_FP']:.0f}, σH {p['sigma_H']:.0f} of "
                f"{p['sigma_HP']:.0f} MPa): widen the gears or the centre distance."
            )
    actual = [p["ratio"] * final for p in pairs]
    r = t.tyre_radius_m
    eta = t.driveline_efficiency
    grip_n = traction_limit(t)
    gears_out = []
    for k, (i, p) in enumerate(zip(actual, pairs, strict=True)):
        v_red = _speed(e.redline_rpm, i, r)
        f_max = e.peak_torque_Nm * i * eta / r
        f_use = min(f_max, grip_n)
        sin_g = max(
            min((f_use - t.mass_kg * G * t.rolling_resistance) / (t.mass_kg * G), 1.0), -1.0
        )
        gears_out.append(
            {
                "gear": k + 1,
                "gearbox_ratio": p["ratio"],
                "overall": i,
                "step": actual[k - 1] / i if k else None,
                "v_redline_kmh": 3.6 * v_red,
                "max_force_N": f_max,
                "grip_limited": f_max > grip_n,
                "gradeability_pct": 100.0 * math.tan(math.asin(sin_g)) if sin_g > 0 else 0.0,
                "pair": p,
            }
        )
    if gears_out[0]["grip_limited"]:
        warnings.append(
            "First gear can exceed the driven axle's grip "
            f"({grip_n / 1000:.1f} kN at μ {t.grip:g}): "
            "launch is traction limited."
        )
    steps = [g["step"] for g in gears_out[1:]]
    if steps and max(steps) > 1.8:
        warnings.append(
            f"Largest step {max(steps):.2f} > 1.8: the engine drops far below its torque "
            "plateau on upshifts."
        )

    # traction diagram and performance
    def force(i: float, v: float) -> float:
        rpm = v / r * i * 30.0 / math.pi
        if rpm > e.redline_rpm:
            return 0.0
        return min(e.torque(max(rpm, e.idle_rpm)) * i * eta / r, grip_n)

    v_top = 0.0
    curves = []
    for i in actual:
        pts = []
        v_lo, v_hi = _speed(e.idle_rpm, i, r), _speed(e.redline_rpm, i, r)
        for j in range(41):
            v = v_lo + (v_hi - v_lo) * j / 40
            pts.append([3.6 * v, force(i, v)])
            if force(i, v) >= road_load(t, v):
                v_top = max(v_top, v)
        curves.append(pts)
    road = [
        [3.6 * v, road_load(t, v)]
        for v in (k * 2.0 for k in range(0, int(max(v_top, v_max) / 2.0) + 4))
    ]
    # 0-100 km/h: full load, shift at the redline (0.3 s with no drive), clutch slip below idle
    v, time_s, gear, shift_left, t100 = 0.0, 0.0, 0, 0.0, None
    dt = 0.01
    while time_s < 60.0:
        i = actual[gear]
        delta = 1.04 + 0.0025 * i * i
        shifting = shift_left > 0
        drive = 0.0 if shifting else force(i, v)
        if gear == 0 and v < _speed(e.torque_from_rpm, i, r):
            drive = min(e.peak_torque_Nm * 0.9 * i * eta / r, grip_n)  # launch on the clutch
        acc = (drive - road_load(t, v)) / (delta * t.mass_kg)
        v += acc * dt
        time_s += dt
        shift_left = max(shift_left - dt, 0.0)
        if t100 is None and v >= 100 / 3.6:
            t100 = time_s
            break
        if v >= _speed(e.redline_rpm, i, r) * 0.999 and gear < len(actual) - 1:
            gear += 1
            shift_left = 0.3
        if acc <= 0 and not shifting:
            break  # cannot reach 100 km/h
    in_top_rpm_100 = (100 / 3.6) / r * actual[-1] * 30.0 / math.pi
    torque_out = e.peak_torque_Nm * gbox[0] * eta
    return {
        "centre_distance": a,
        "final_drive": final,
        "gears": gears_out,
        "spread": actual[0] / actual[-1],
        "v_max_kmh": 3.6 * v_top,
        "v_max_power_kmh": 3.6 * v_max,
        "zero_to_100_s": t100,
        "rpm_at_100_top": in_top_rpm_100,
        "traction": curves,
        "road_load": road,
        "grip_limit_N": grip_n,
        "input_shaft_mm": (16.0 * e.peak_torque_Nm * 1000.0 / (math.pi * TAU_SHAFT)) ** (1 / 3),
        "output_shaft_mm": (16.0 * torque_out * 1000.0 / (math.pi * TAU_SHAFT)) ** (1 / 3),
        "torque_curve": [
            [rpm, e.torque(rpm)] for rpm in range(int(e.idle_rpm), int(e.redline_rpm) + 1, 100)
        ],
        "warnings": warnings,
    }
