"""A piston engine as a product of the Mechanical module: options, the full part breakdown
(every part allocated from day one) and the checks against the engine model.

Masses: the engine's dry mass comes from the kernel's statistical fit; the reciprocating
parts (pistons, pins, rings, rods) are estimated from the bore (kernel); every other part
is allocated a stated share of the remainder (level 0), so the breakdown always sums to
the engine mass. Frame: x along the crankshaft towards the front, y to the left, z up from
the crank axis (m).
"""

from typing import Any

from autevra.mech import piston as pk
from autevra.modules import Check, Values
from autevra.product import templates as tpl
from autevra.product.breakdown import Node, RolledNode
from autevra.product.options import Configuration, OptionFamily, Options
from autevra.product.templates import PartTemplate

MODULE = "mechanical"
PETROL, DIESEL, TURBO = "fuel == 'Petrol'", "fuel == 'Diesel'", "aspiration == 'Turbocharged'"


def spec_of(values: Values) -> pk.EngineSpec:
    return pk.EngineSpec.model_validate({k: v for k, v in values.items()
                                         if k in pk.EngineSpec.model_fields})  # fmt: skip


def options(values: Values) -> Options:
    return Options(families=[
        OptionFamily(id="fuel", label="Fuel", choices=["Petrol", "Diesel"]),
        OptionFamily(id="aspiration", label="Aspiration", choices=["Natural", "Turbocharged"]),
    ])  # fmt: skip


def current(values: Values) -> dict[str, str]:
    return {"fuel": "Diesel" if values.get("fuel") == "diesel" else "Petrol",
            "aspiration": "Turbocharged" if values.get("turbo") else "Natural"}  # fmt: skip


def configure(values: Values, config: Configuration) -> dict[str, Any]:
    out = dict(values)
    c = {**current(values), **config}
    out["fuel"] = "diesel" if c["fuel"] == "Diesel" else "petrol"
    out["turbo"] = c["aspiration"] == "Turbocharged"
    return out


F_CONVERT, F_CONTAIN = "convert fuel energy to shaft power", "contain combustion pressure"
F_FORCES, F_GAS = "transmit and balance forces", "admit and expel the working fluid"
F_HEAT, F_LUBE, F_CONTROL, F_MOUNT = ("reject heat", "lubricate", "control and monitor",
                                      "mount to the consumer")  # fmt: skip
# id, name, group code, process, functions, has level-1 geometry today, share of remainder
_T: tuple[tuple[str, str, str, str, tuple[str, ...], bool, float], ...] = (
    ("block", "Cylinder block", "structure", "casting", (F_CONTAIN, F_FORCES), True, 0.30),
    ("bedplate", "Bedplate / main bearing caps", "structure", "casting", (F_FORCES,), False,
     0.04),
    ("head", "Cylinder head", "structure", "casting", (F_CONTAIN, F_GAS), True, 0.15),
    ("head_gasket", "Head gasket", "structure", "standard", (F_CONTAIN,), False, 0.005),
    ("cam_cover", "Cam cover", "structure", "moulding", (F_LUBE,), True, 0.015),
    ("sump", "Oil sump", "structure", "sheet metal", (F_LUBE,), True, 0.03),
    ("front_cover", "Front (timing) cover", "structure", "casting", (F_LUBE,), False, 0.02),
    ("crankshaft", "Crankshaft", "cranktrain", "forging", (F_CONVERT, F_FORCES), False, 0.12),
    ("conrod", "Connecting rod", "cranktrain", "forging", (F_FORCES,), False, 0.0),
    ("piston", "Piston", "cranktrain", "casting", (F_CONVERT, F_CONTAIN), False, 0.0),
    ("piston_rings", "Piston ring set", "cranktrain", "standard", (F_CONTAIN,), False, 0.0),
    ("gudgeon_pin", "Gudgeon pin", "cranktrain", "machining", (F_FORCES,), False, 0.0),
    ("main_bearing", "Main bearing shells", "cranktrain", "standard", (F_FORCES, F_LUBE),
     False, 0.006),
    ("big_end_bearing", "Big-end bearing shells", "cranktrain", "standard",
     (F_FORCES, F_LUBE), False, 0.004),
    ("flywheel", "Flywheel", "cranktrain", "casting", (F_CONVERT, F_MOUNT), True, 0.07),
    ("damper", "Torsional damper and pulley", "cranktrain", "casting", (F_FORCES,), True,
     0.012),
    ("camshaft", "Camshaft", "valvetrain", "forging", (F_GAS,), False, 0.03),
    ("valve", "Valve", "valvetrain", "forging", (F_GAS,), False, 0.012),
    ("valve_spring", "Valve spring", "valvetrain", "standard", (F_GAS,), False, 0.008),
    ("follower", "Follower and lash adjuster", "valvetrain", "machining", (F_GAS,), False,
     0.008),
    ("cam_phaser", "Cam phaser", "valvetrain", "assembly", (F_GAS, F_CONTROL), False, 0.006),
    ("timing_chain", "Timing chain, sprockets and tensioner", "timing", "standard", (F_GAS,),
     False, 0.02),
    ("intake_manifold", "Intake manifold", "induction", "moulding", (F_GAS,), True, 0.035),
    ("throttle", "Throttle body", "induction", "assembly", (F_GAS, F_CONTROL), False, 0.005),
    ("air_box", "Air filter box", "induction", "moulding", (F_GAS,), False, 0.015),
    ("turbocharger", "Turbocharger", "induction", "inventory", (F_GAS, F_CONVERT), True, 0.0),
    ("intercooler", "Intercooler", "induction", "assembly", (F_GAS, F_HEAT), False, 0.0),
    ("exhaust_manifold", "Exhaust manifold", "exhaust", "casting", (F_GAS, F_HEAT), True,
     0.045),
    ("injector", "Fuel injector", "fuel", "inventory", (F_CONVERT,), False, 0.004),
    ("fuel_rail", "Fuel rail", "fuel", "tube", (F_CONVERT,), False, 0.006),
    ("hp_pump", "High-pressure fuel pump", "fuel", "inventory", (F_CONVERT,), False, 0.012),
    ("spark_plug", "Spark plug", "ignition", "inventory", (F_CONVERT,), False, 0.002),
    ("coil", "Ignition coil", "ignition", "inventory", (F_CONVERT, F_CONTROL), False, 0.006),
    ("glow_plug", "Glow plug", "ignition", "inventory", (F_CONVERT,), False, 0.002),
    ("oil_pump", "Oil pump and pickup", "lubrication", "casting", (F_LUBE,), False, 0.015),
    ("oil_filter", "Oil filter", "lubrication", "inventory", (F_LUBE,), False, 0.005),
    ("water_pump", "Water pump", "cooling", "casting", (F_HEAT,), False, 0.015),
    ("thermostat", "Thermostat housing", "cooling", "moulding", (F_HEAT,), False, 0.005),
    ("alternator", "Alternator", "accessories", "inventory", (F_CONTROL,), False, 0.04),
    ("starter", "Starter motor", "accessories", "inventory", (F_CONVERT,), False, 0.03),
    ("accessory_belt", "Accessory belt and tensioner", "accessories", "standard",
     (F_FORCES,), False, 0.008),
    ("engine_mount", "Engine mount bracket", "mounts", "casting", (F_MOUNT,), False, 0.03),
    ("ecu", "Engine control unit and sensors", "control", "inventory", (F_CONTROL,), False,
     0.012),
)  # fmt: skip
GROUPS = {"structure": "Structure", "cranktrain": "Cranktrain", "valvetrain": "Valvetrain",
          "timing": "Timing drive", "induction": "Induction", "exhaust": "Exhaust",
          "fuel": "Fuel injection", "ignition": "Ignition", "lubrication": "Lubrication",
          "cooling": "Cooling", "accessories": "Accessories", "mounts": "Mounts",
          "control": "Control"}  # fmt: skip
GEOMETRY = {t[0] for t in _T if t[5]}
tpl.register(*(PartTemplate(id=i, module=MODULE, name=n, code=f"engine.{g}", process=p,
                            functions=f, max_maturity=1 if geo else 0)
               for i, n, g, p, f, geo, _ in _T))  # fmt: skip
SHARE = {t[0]: t[6] for t in _T}


def breakdown(values: Values) -> Node:
    spec = spec_of(values)
    n = spec.cylinders
    banks = 1 if spec.layout == "inline" else 2
    mains = (n + 1) if spec.layout == "inline" else (n // 2 + 1)
    total = pk.mass_kg(spec)
    m_rec = pk.reciprocating_mass_kg(spec)
    vd = pk.displacement_l(spec)
    pitch = 1.2 * spec.bore / 1000
    length = (n / banks) * pitch
    deck = (spec.stroke / 2 + spec.rod_ratio * spec.stroke + 0.55 * spec.bore) / 1000
    # estimated parts: (template, mass of all instances, instances, basis, applicability)
    est = {
        "piston": (0.55 * m_rec * n, n, "0.55 x reciprocating mass (bore-cubed fit)", ""),
        "gudgeon_pin": (0.12 * m_rec * n, n, "0.12 x reciprocating mass", ""),
        "piston_rings": (0.06 * m_rec * n, n, "0.06 x reciprocating mass per set", ""),
        "conrod": (0.81 * m_rec * n, n, "rod mass 0.81 x reciprocating mass (a third of "
                   "the rod counted as reciprocating)", ""),
        "turbocharger": (4.0 + 2.5 * vd, 1, "4 kg + 2.5 kg per litre", TURBO),
        "intercooler": (3.0 + 1.0 * vd, 1, "3 kg + 1 kg per litre", TURBO),
    }  # fmt: skip
    counts = {"head": banks, "head_gasket": banks, "cam_cover": banks,
              "exhaust_manifold": banks, "camshaft": 2 * banks, "valve": 4 * n,
              "valve_spring": 4 * n, "follower": 4 * n, "cam_phaser": 2 * banks,
              "main_bearing": mains, "big_end_bearing": n, "injector": n,
              "fuel_rail": banks, "spark_plug": n, "coil": n, "glow_plug": n,
              "engine_mount": 3}  # fmt: skip
    applic = {"spark_plug": PETROL, "coil": PETROL, "throttle": PETROL, "glow_plug": DIESEL,
              "cam_phaser": PETROL}  # fmt: skip
    own = {"fuel": "Diesel" if spec.fuel == "diesel" else "Petrol",
           "aspiration": "Turbocharged" if spec.turbo else "Natural"}  # fmt: skip

    def applies(expr: str) -> bool:
        from autevra.product.options import applies as ok

        return ok(expr, own, {"fuel", "aspiration"})

    fixed = sum(m for m, _, _, a in est.values() if applies(a))
    shares = {k: v for k, v in SHARE.items() if v > 0 and applies(applic.get(k, ""))}
    rest = max(total - fixed, 0.0)
    norm = sum(shares.values())
    cg_of = {"structure": (0.0, 0.0, 0.3 * deck), "cranktrain": (0.0, 0.0, 0.0),
             "valvetrain": (0.0, 0.0, deck + 0.04), "timing": (length / 2 + 0.03, 0.0, 0.5 * deck),
             "induction": (0.0, 0.25, 0.8 * deck), "exhaust": (0.0, -0.25, 0.7 * deck),
             "fuel": (0.0, 0.12, deck), "ignition": (0.0, 0.0, deck + 0.05),
             "lubrication": (0.0, 0.0, -0.12), "cooling": (length / 2 + 0.05, 0.0, 0.4 * deck),
             "accessories": (length / 2, 0.15, 0.3 * deck), "mounts": (0.0, 0.0, 0.2 * deck),
             "control": (0.0, 0.3, deck)}  # fmt: skip
    systems: dict[str, list[Node]] = {}
    for tid, name, group, process, funcs, geo, _share in _T:
        if tid in est:
            mass, inst, basis, app = est[tid]
            source = "estimated"
        else:
            app = applic.get(tid, "")
            inst = counts.get(tid, 1)
            share = shares.get(tid, SHARE[tid]) / norm if norm else 0.0
            mass, basis, source = rest * share, f"{share:.1%} of the remaining dry mass", \
                "allocated"  # fmt: skip
        node = Node(id=tid, name=name, kind="part", code=f"engine.{group}", template=tid,
                    process=process, functions=list(funcs), applicability=app,
                    instances=inst, maturity=1 if geo else 0, mass=max(mass, 0.0),
                    mass_source=source, basis=basis, cg=cg_of[group],
                    geometry=tid if geo else "")  # fmt: skip
        if tid == "flywheel":
            node.cg = (-(length / 2 + 0.04), 0.0, 0.0)
        systems.setdefault(group, []).append(node)
    children = [Node(id=f"g_{g}", name=GROUPS[g], kind="system", code=f"engine.{g}",
                     children=parts) for g, parts in systems.items()]  # fmt: skip
    return Node(id="engine", name=spec.name, kind="product", code="engine",
                budget=total * 1.0001, children=children)  # fmt: skip


def checks(values: Values, root: RolledNode) -> list[Check]:
    spec = spec_of(values)
    out = pk.analyse(spec)
    rows = [Check(id=c["id"], label=c["label"], status=c["status"], message=c["message"])
            for c in out["checks"]]  # fmt: skip
    rows.insert(0, Check(id="mass", label="Dry mass", status="pass",
                         message=f"{root.rollup.mass:.0f} kg: statistical fit (about 20 %) for "
                         f"a {out['displacement_l']:.1f} L {spec.cylinders}-cylinder "
                         f"{spec.fuel}{' turbo' if spec.turbo else ''} engine"))  # fmt: skip
    return rows
