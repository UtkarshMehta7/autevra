"""Electric machines and gas turbines as Mechanical-module products: their breakdowns,
checks, loads, stack-ups and concept geometry (the piston engine lives in ``engine``).

Masses: the machine's mass from its kernel (electric: active envelope; gas turbine: a
statistical thrust-to-weight of 5 for small turbojets, power-to-weight 4 kW/kg for small
turboshafts, stated), allocated to parts by stated shares (level 0). Frames: x along the
shaft, z up (m)."""

from autevra.mech import electric as em
from autevra.mech import turbine as gt
from autevra.modules import Check, Values
from autevra.product import templates as tpl
from autevra.product.breakdown import Node, RolledNode
from autevra.product.loads import LoadAt, LoadCase
from autevra.product.templates import PartTemplate
from autevra.quality import Contributor, Stack

MODULE = "mechanical"
F_CONV, F_CONTAIN, F_COOL, F_CTRL, F_MOUNT = ("convert energy to shaft power", "contain",
                                             "reject heat", "control and monitor",
                                             "mount to the consumer")  # fmt: skip
# id, name, group, process, functions, share, count rule
ELECTRIC = (
    ("stator_core", "Stator lamination stack", "stator", "sheet metal", (F_CONV,), 0.26),
    ("winding", "Stator winding (hairpin)", "stator", "assembly", (F_CONV,), 0.18),
    ("rotor_core", "Rotor lamination stack", "rotor", "sheet metal", (F_CONV,), 0.14),
    ("magnets", "Permanent magnets", "rotor", "inventory", (F_CONV,), 0.06),
    ("motor_shaft", "Rotor shaft", "rotor", "machining", (F_CONV, F_MOUNT), 0.06),
    ("motor_bearing", "Bearing", "rotor", "inventory", (F_CONV,), 0.02),
    ("motor_housing", "Housing with cooling jacket", "structure", "casting", (F_CONTAIN, F_COOL),
     0.16),
    ("end_shield", "End shield", "structure", "casting", (F_CONTAIN,), 0.07),
    ("resolver", "Resolver", "control", "inventory", (F_CTRL,), 0.01),
    ("terminal_box", "Terminal box and busbars", "power", "assembly", (F_CONV,), 0.04),
)  # fmt: skip
TURBINE = (
    ("inlet", "Inlet and bellmouth", "intake", "sheet metal", (F_CONV,), 0.05),
    ("compressor_disc", "Compressor disc with blades", "compressor", "forging", (F_CONV,), 0.18),
    ("compressor_case", "Compressor casing", "compressor", "casting", (F_CONTAIN,), 0.10),
    ("combustor", "Combustor liner", "combustor", "sheet metal", (F_CONV, F_CONTAIN), 0.08),
    ("fuel_nozzle", "Fuel nozzle", "combustor", "machining", (F_CONV,), 0.02),
    ("igniter", "Igniter", "combustor", "inventory", (F_CONV,), 0.005),
    ("turbine_disc", "Turbine disc with blades", "turbine", "forging", (F_CONV,), 0.16),
    ("turbine_case", "Turbine casing", "turbine", "casting", (F_CONTAIN,), 0.08),
    ("nozzle", "Exhaust nozzle", "exhaust", "sheet metal", (F_CONV,), 0.06),
    ("rotor_shaft", "Spool shaft", "rotor", "forging", (F_CONV,), 0.06),
    ("main_bearing_gt", "Main bearing", "rotor", "inventory", (F_CONV,), 0.03),
    ("accessory_gearbox", "Accessory gearbox", "accessories", "casting", (F_CTRL,), 0.10),
    ("fuel_control", "Fuel control unit", "accessories", "inventory", (F_CTRL,), 0.04),
    ("gt_mount", "Engine mount", "mounts", "forging", (F_MOUNT,), 0.035),
)  # fmt: skip
tpl.register(*(PartTemplate(id=i, module=MODULE, name=n, code=f"engine.{g}", process=p,
                            functions=f, max_maturity=0)
               for i, n, g, p, f, _ in (*ELECTRIC, *TURBINE)))  # fmt: skip


def motor_spec(values: Values) -> em.MotorSpec:
    return em.MotorSpec.model_validate({k: v for k, v in values.items()
                                        if k in em.MotorSpec.model_fields})  # fmt: skip


def turbine_spec(values: Values) -> gt.TurbineSpec:
    return gt.TurbineSpec.model_validate({k: v for k, v in values.items()
                                          if k in gt.TurbineSpec.model_fields})  # fmt: skip


def turbine_mass(s: gt.TurbineSpec) -> float:
    out = gt.cycle(s)
    if s.kind == "turbojet":
        return out["thrust_kn"] * 1000 / 9.80665 / 5.0
    return out["shaft_power_kw"] / 4.0


def _tree(name: str, rows: tuple, total: float, counts: dict[str, int], basis: str) -> Node:
    groups: dict[str, list[Node]] = {}
    norm = sum(r[5] for r in rows)
    for tid, pname, g, process, funcs, share in rows:
        groups.setdefault(g, []).append(Node(
            id=tid, name=pname, kind="part", code=f"engine.{g}", template=tid, process=process,
            functions=list(funcs), instances=counts.get(tid, 1), mass=total * share / norm,
            mass_source="allocated", basis=f"{share / norm:.1%} of {basis}"))  # fmt: skip
    children = [Node(id=f"g_{g}", name=g.title(), kind="system", code=f"engine.{g}",
                     children=parts) for g, parts in groups.items()]  # fmt: skip
    return Node(id="engine", name=name, kind="product", code="engine", budget=total * 1.0001,
                children=children)  # fmt: skip


def electric_breakdown(values: Values) -> Node:
    s = motor_spec(values)
    return _tree(s.name, ELECTRIC, em.mass_kg(s), {"motor_bearing": 2, "end_shield": 2,
                                                   "magnets": s.poles * 2},
                 "the machine mass (active envelope x 1.6)")  # fmt: skip


def turbine_breakdown(values: Values) -> Node:
    s = turbine_spec(values)
    stages = max(1, round(s.pressure_ratio**0.5 / 1.4))  # rough axial stage count
    return _tree(s.name, TURBINE, turbine_mass(s), {"compressor_disc": stages,
                                                    "turbine_disc": max(1, stages // 3),
                                                    "fuel_nozzle": 8, "igniter": 2,
                                                    "main_bearing_gt": 3, "gt_mount": 3},
                 "the engine mass (statistical thrust- or power-to-weight)")  # fmt: skip


def electric_checks(values: Values, root: RolledNode) -> list[Check]:
    out = em.analyse(motor_spec(values))
    return [Check(id="mass", label="Mass", status="pass",
                  message=f"{root.rollup.mass:.1f} kg (active envelope estimate)"),
            *[Check(**c) for c in out["checks"]]]  # fmt: skip


def turbine_checks(values: Values, root: RolledNode) -> list[Check]:
    s = turbine_spec(values)
    out = gt.cycle(s)
    t4 = s.tit_k
    return [Check(id="mass", label="Mass", status="pass", message=f"{root.rollup.mass:.0f} kg "
                  "(statistical)"),
            Check(id="tit", label="Turbine entry temperature",
                  status="pass" if t4 <= 1400 else "warn" if t4 <= 1700 else "fail",
                  message=f"{t4:.0f} K (uncooled blades about 1,400 K; above that blade "
                  "cooling and thermal barrier coatings are needed)"),
            Check(id="efficiency", label="Thermal efficiency", status="pass",
                  message=f"{out['thermal_efficiency']:.1%}")]  # fmt: skip


def electric_loads(values: Values) -> list[LoadCase]:
    s = motor_spec(values)
    t = em.torque(s, s.shear_peak_kpa)
    span = s.stator_diameter / 1000 * 1.2
    return [LoadCase(id="peak_torque", name="Peak torque reaction", kind="limit",
                     factors={"torque_nm": round(t, 1)}, method="peak torque reacted by two "
                     "mounts across the housing", results={"mount_force_n": t / span},
                     loads=[LoadAt(location="mount (each)", fz=round(t / span))])]  # fmt: skip


def turbine_loads(values: Values) -> list[LoadCase]:
    s = turbine_spec(values)
    out = gt.cycle(s)
    thrust = out.get("thrust_kn", 0.0) * 1000
    return [LoadCase(id="thrust", name="Thrust at the mounts", kind="limit",
                     factors={"thrust_kn": round(thrust / 1000, 2)}, method="cycle thrust "
                     "reacted at the thrust mount", results={"thrust_n": thrust},
                     loads=[LoadAt(location="thrust mount", fx=round(thrust))])]  # fmt: skip


def electric_stack(values: Values) -> list[Stack]:
    """Air gap between rotor and stator (radial)."""
    s = motor_spec(values)
    gap = 0.7 if s.stator_diameter < 300 else 1.0
    bore = s.rotor_ratio * s.stator_diameter / 2 + gap
    return [Stack(name="Radial air gap", lsl=0.4, usl=1.2, contributors=[
        Contributor(name="stator bore radius", nominal=round(bore, 3), plus=0.03, minus=0.03),
        Contributor(name="rotor radius", nominal=round(bore - gap, 3), plus=0.02, minus=0.02,
                    direction=-1),
        Contributor(name="bearing clearance and eccentricity", nominal=0.0, plus=0.05,
                    minus=0.05),
    ])]  # fmt: skip


def turbine_stack(values: Values) -> list[Stack]:
    """Compressor blade tip clearance (cold build)."""
    return [Stack(name="Compressor tip clearance", lsl=0.2, usl=0.8, contributors=[
        Contributor(name="casing bore radius", nominal=150.5, plus=0.05, minus=0.05),
        Contributor(name="disc rim radius", nominal=100.0, plus=0.03, minus=0.03, direction=-1),
        Contributor(name="blade height", nominal=50.0, plus=0.05, minus=0.05, direction=-1),
        Contributor(name="bearing radial play", nominal=0.0, plus=0.03, minus=0.03),
    ])]  # fmt: skip


def electric_parts(s: em.MotorSpec) -> list[dict]:
    d, length = s.stator_diameter, s.stack_length
    housing = d * 1.15
    return [
        {"name": f"{s.name}: housing", "color": [0.62, 0.64, 0.67], "finish": "metal",
         "features": [{"id": "housing", "name": "Housing", "type": "cylinder",
                       "radius": housing / 2, "height": length * 1.35, "axis": "x"},
                      {"id": "fins", "name": "Cooling ribs", "type": "cylinder",
                       "radius": housing / 2 + 6, "height": length * 0.9, "axis": "x"}]},
        {"name": f"{s.name}: end shields", "color": [0.3, 0.31, 0.33], "finish": "metal",
         "features": [{"id": f"shield{i}", "name": "End shield", "type": "cylinder",
                       "radius": housing / 2 * 0.95, "height": 12, "axis": "x",
                       "at": {"x": sx * (length * 0.675 + 6)}} for i, sx in enumerate((-1, 1))]},
        {"name": f"{s.name}: shaft", "color": [0.75, 0.76, 0.78], "finish": "polished",
         "features": [{"id": "shaft", "name": "Shaft", "type": "cylinder", "radius": d * 0.08,
                       "height": length * 2.0, "axis": "x"}]},
        {"name": f"{s.name}: terminal box", "color": [0.1, 0.1, 0.11], "finish": "paint_matte",
         "features": [{"id": "box", "name": "Terminal box", "type": "box",
                       "size": [length * 0.5, d * 0.35, d * 0.18],
                       "at": {"z": housing / 2 + d * 0.06}}]},
    ]  # fmt: skip


def turbine_parts(s: gt.TurbineSpec) -> list[dict]:
    r = 60 + 22 * s.mass_flow**0.5  # mm, inlet radius scaling with the flow
    length = 6.0 * r
    secs = lambda pts: [{"z": z * length, "width": 2 * w * r, "height": 2 * w * r,  # noqa: E731
                         "radius": w * r - 1} for z, w in pts]  # fmt: skip
    return [
        {"name": f"{s.name}: casing", "color": [0.7, 0.71, 0.73], "finish": "polished",
         "features": [{"id": "casing", "name": "Casing", "type": "loft", "at": {"ry": 90},
                       "sections": secs([(0, 1.12), (0.08, 1.0), (0.35, 0.82), (0.5, 0.95),
                                         (0.68, 0.9), (0.85, 0.72), (1.0, 0.6)])}]},
        {"name": f"{s.name}: spinner", "color": [0.2, 0.2, 0.22], "finish": "metal",
         "features": [{"id": "spinner", "name": "Spinner", "type": "sphere", "radius": 0.3 * r,
                       "at": {"x": 0.04 * length}}]},
        {"name": f"{s.name}: accessory gearbox", "color": [0.25, 0.26, 0.28], "finish": "metal",
         "features": [{"id": "agb", "name": "Accessory gearbox", "type": "box",
                       "size": [0.25 * length, 0.6 * r, 0.35 * r],
                       "at": {"x": 0.32 * length, "z": -0.95 * r}}]},
    ]  # fmt: skip
