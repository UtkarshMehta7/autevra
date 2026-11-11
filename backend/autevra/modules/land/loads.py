"""Road load cases at the four tyre contact patches, and the compliance rows they support.

Quasi-static "g-cases" in the form chassis engineers commonly start from (each company's
own values differ; these are stated, typical ones): vertical bump 3 g; braking 1 g with
1 g vertical; cornering 1 g lateral; pothole on one front wheel 4 g vertical with 2.5 g
longitudinal. Axle loads from the static weight split, with longitudinal and lateral
load transfer through the CG height (m a h / L and m a h / track). Frame: x rearward from
the front axle, y to the left, z up; forces on the vehicle at the contact patches (N).

Braking compliance (UN ECE R13-H, Type-0 test): stopping distance from 100 km/h of at
most 0.1 v + 0.0060 v² (v in km/h) = 70 m, computed with the longitudinal model on a dry
road (friction 0.9), including a 0.15 s brake build-up.
"""

from autevra.domains.automotive import tests as vt
from autevra.domains.automotive.sim import longitudinal as lon
from autevra.modules import Values
from autevra.product.loads import Compliance, LoadAt, LoadCase

G = 9.80665
DRIVER = 75.0


def _num(values: Values) -> dict[str, float]:
    return {k: float(v) for k, v in values.items() if isinstance(v, int | float)}


def cases(values: Values) -> list[LoadCase]:
    p = _num(values)
    m = p["vehicle_mass"]  # test condition (kerb plus load)
    f = p["front_mass_distribution"] / 100
    h, wb = p["cg_height"] / 1000, p["wheelbase"] / 1000
    tf, tr = p["track_front"] / 1000, p["track_rear"] / 1000
    static = {"FL": m * G * f / 2, "FR": m * G * f / 2,
              "RL": m * G * (1 - f) / 2, "RR": m * G * (1 - f) / 2}  # fmt: skip

    def case(cid: str, name: str, factors: dict[str, float],
             corners: dict[str, tuple[float, float, float]]) -> LoadCase:  # fmt: skip
        loads = [LoadAt(location=f"contact patch {k}", fx=round(fx), fy=round(fy), fz=round(fz))
                 for k, (fx, fy, fz) in corners.items()]  # fmt: skip
        peak = max(abs(x.fz) for x in loads)
        return LoadCase(id=cid, name=name, kind="limit", factors=factors,
                        method="quasi-static g-case (typical values), load transfer through "
                        "the CG height", loads=loads, results={"peak_fz_n": peak})  # fmt: skip

    bump = case(
        "bump",
        "Vertical bump, 3 g",
        {"vertical_g": 3.0},
        {k: (0.0, 0.0, 3 * v) for k, v in static.items()},
    )
    transfer = m * G * 1.0 * h / wb / 2  # per corner, to the front
    brake = case("braking", "Braking 1 g", {"longitudinal_g": 1.0, "vertical_g": 1.0},
                 {k: ((v + (transfer if k[0] == "F" else -transfer)) * 1.0, 0.0,
                      v + (transfer if k[0] == "F" else -transfer))
                  for k, v in static.items()})  # fmt: skip
    lat = {"F": m * G * f * h / tf, "R": m * G * (1 - f) * h / tr}  # axle transfer, 1 g
    corner = case("cornering", "Cornering 1 g (left turn)", {"lateral_g": 1.0},
                  {k: (0.0, v + (lat[k[0]] / 2 if k[1] == "R" else -lat[k[0]] / 2),
                       v + (lat[k[0]] / 2 if k[1] == "R" else -lat[k[0]] / 2))
                   for k, v in static.items()})  # fmt: skip
    pothole = case(
        "pothole",
        "Pothole, front left (4 g vertical, 2.5 g longitudinal)",
        {"vertical_g": 4.0, "longitudinal_g": 2.5},
        {"FL": (2.5 * static["FL"], 0.0, 4 * static["FL"])},
    )
    return [bump, brake, corner, pothole]


def stopping_distance(values: Values) -> float:
    params = vt.longitudinal_params(_num(values))
    run = lon.simulate(params, lon.Manoeuvre(kind="brake", friction=0.9, v_end=100 / 3.6))
    return float(run.metrics.get("stopping_distance") or 0.0)


def compliance(values: Values) -> list[Compliance]:
    limit = 0.1 * 100 + 0.0060 * 100**2
    dist = stopping_distance(values)
    return [
        Compliance(clause="UN ECE R13-H, Annex 3 (Type-0)", requirement="stopping distance from "
                   f"100 km/h at most {limit:.0f} m", means="analysis",
                   evidence=f"{dist:.1f} m with friction 0.9 and 0.15 s build-up (test needed "
                   "for approval)", status="shown" if 0 < dist <= limit else "not shown"),
        Compliance(clause="UN ECE R79", requirement="steering equipment", means="test",
                   evidence="steering system not yet detailed", status="open"),
        Compliance(clause="UN ECE R94 / R95", requirement="frontal and lateral collision "
                   "occupant protection", means="test", evidence="crash load paths at "
                   "concept level only; crash analysis planned", status="open"),
        Compliance(clause="UN ECE R17", requirement="seat and anchorage strength",
                   means="test", evidence="seat structure not yet detailed", status="open"),
        Compliance(clause="UN ECE R48", requirement="installation of lighting devices",
                   means="inspection", evidence="lamp positions exist; photometric zones "
                   "not yet checked", status="open"),
    ]  # fmt: skip
