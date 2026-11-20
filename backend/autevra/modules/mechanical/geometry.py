"""Concept geometry of a piston engine (level 1), as coloured Part Design parts in mm:
crankcase and cylinder banks (inline, V or opposed), heads and cam covers, sump, intake
plenum and runners, exhaust manifolds, flywheel, front pulley and (turbocharged) the turbo.

Frame: the crankshaft along X (front +X, flywheel at -X), Z up from the crank axis.
Banks are tilted about the crank axis by half the bank angle (opposed: 90°).
Dimensions follow the engine's own bore, stroke and rod: bore pitch 1.2 B, deck height
S/2 + l + 0.55 B (crank radius, rod length and piston compression height).
"""

import math

from autevra.mech import piston as pk


def _tilted(z: float, angle: float, y: float = 0.0) -> dict[str, float]:
    """Placement of a point at (y, z) in a bank frame tilted by ``angle`` (deg) about X."""
    a = math.radians(angle)
    return {"y": y * math.cos(a) - z * math.sin(a), "z": y * math.sin(a) + z * math.cos(a),
            "rx": angle}  # fmt: skip


def parts(spec: pk.EngineSpec) -> list[dict]:
    b, s = spec.bore, spec.stroke
    n = spec.cylinders
    banks = (
        [0.0]
        if spec.layout == "inline"
        else ([-spec.bank_angle / 2, spec.bank_angle / 2] if spec.layout == "V" else [-90.0, 90.0])
    )
    per_bank = n // len(banks)
    pitch = 1.2 * b
    length = per_bank * pitch + 0.35 * b
    rod = spec.rod_ratio * s
    deck = s / 2 + rod + 0.55 * b
    width = 1.45 * b
    head_h, cover_h = 0.95 * b, 0.32 * b
    block, heads, covers, intake, exhaust = [], [], [], [], []
    # crankcase around the crank axis
    case_w = (
        width
        if spec.layout == "inline"
        else (2 * deck * math.sin(math.radians(min(spec.bank_angle, 120) / 2)) + 0.6 * b)
    )
    block.append(
        {
            "id": "crankcase",
            "name": "Crankcase",
            "type": "box",
            "size": [length, case_w, 0.9 * s + 0.4 * b],
            "at": {"z": -0.05 * s},
        }
    )
    for k, angle in enumerate(banks):
        tag = f"_{k}" if len(banks) > 1 else ""
        stagger = 0.25 * pitch * (1 if k else -1) if len(banks) > 1 else 0.0
        block.append(
            {
                "id": f"bank{tag}",
                "name": f"Cylinder bank{tag}",
                "type": "box",
                "size": [length, width, deck - 0.2 * s],
                "at": {"x": stagger, **_tilted(0.1 * s + (deck - 0.2 * s) / 2, angle)},
            }
        )
        heads.append(
            {
                "id": f"head{tag}",
                "name": f"Cylinder head{tag}",
                "type": "box",
                "size": [length, 1.25 * width, head_h],
                "at": {"x": stagger, **_tilted(deck + head_h / 2, angle)},
            }
        )
        covers.append(
            {
                "id": f"cover{tag}",
                "name": f"Cam cover{tag}",
                "type": "box",
                "size": [length * 0.96, 1.1 * width, cover_h],
                "at": {"x": stagger, **_tilted(deck + head_h + cover_h / 2, angle)},
            }
        )
        # exhaust: one primary pipe per cylinder on the outer side, into a collector
        side = -1.0 if (spec.layout == "inline" or angle > 0) else 1.0  # outboard of the bank
        for i in range(per_bank):
            x = stagger + (i - (per_bank - 1) / 2) * pitch
            exhaust.append({"id": f"primary{tag}_{i}", "name": "Primary pipe", "type": "cylinder",
                            "radius": 0.2 * b, "height": 0.75 * width, "axis": "y",
                            "at": {"x": x, **_tilted(deck + 0.45 * head_h,
                                                     angle, side * 0.9 * width)}})  # fmt: skip
        exhaust.append({"id": f"collector{tag}", "name": "Collector", "type": "cylinder",
                        "radius": 0.24 * b, "height": length * 0.95, "axis": "x",
                        "at": {"x": stagger, **_tilted(deck + 0.3 * head_h, angle,
                                                       side * 1.3 * width)}})  # fmt: skip
        if spec.layout == "inline":  # runners on the other side, plenum along the block
            for i in range(per_bank):
                x = (i - (per_bank - 1) / 2) * pitch
                intake.append(
                    {
                        "id": f"runner_{i}",
                        "name": "Runner",
                        "type": "cylinder",
                        "radius": 0.17 * b,
                        "height": 0.9 * width,
                        "axis": "y",
                        "at": {"x": x, "y": 1.0 * width, "z": deck + 0.5 * head_h},
                    }
                )
            intake.append(
                {
                    "id": "plenum",
                    "name": "Plenum",
                    "type": "cylinder",
                    "radius": 0.42 * b,
                    "height": length * 0.9,
                    "axis": "x",
                    "at": {"y": 1.55 * width, "z": deck + 0.35 * head_h},
                }
            )
    if spec.layout != "inline":  # plenum in the vee (on top for an opposed engine)
        top = deck * (math.cos(math.radians(spec.bank_angle / 2)) if spec.layout == "V"
                      else 0.0) + 0.9 * head_h  # fmt: skip
        intake.append({"id": "plenum", "name": "Plenum", "type": "loft", "sections": [
            {"z": 0, "width": 0.9 * width, "height": 0.7 * b, "radius": 0.2 * b},
            {"z": length * 0.9, "width": 0.9 * width, "height": 0.7 * b, "radius": 0.2 * b}],
            "at": {"x": length * 0.45, "z": top, "ry": -90}})  # fmt: skip
    sump_h = 0.7 * s + 0.6 * b
    sump = [{"id": "sump", "name": "Sump", "type": "loft", "sections": [
        {"z": 0, "width": case_w * 0.95, "height": sump_h, "radius": 0.12 * b},
        {"z": length * 0.95, "width": case_w * 0.95, "height": sump_h * 0.85,
         "radius": 0.12 * b}],
        "at": {"x": length * 0.475, "z": -0.5 * s - 0.2 * b - sump_h / 2, "ry": -90}}]  # fmt: skip
    flywheel = [{"id": "flywheel", "name": "Flywheel", "type": "cylinder", "radius": 1.6 * b,
                 "height": 0.32 * b, "axis": "x", "at": {"x": -(length / 2 + 0.2 * b)}},
                {"id": "ring", "name": "Starter ring", "type": "cylinder", "radius": 1.66 * b,
                 "height": 0.18 * b, "axis": "x",
                 "at": {"x": -(length / 2 + 0.2 * b)}}]  # fmt: skip
    pulley = [{"id": "damper", "name": "Damper pulley", "type": "cylinder", "radius": 0.9 * b,
               "height": 0.35 * b, "axis": "x", "at": {"x": length / 2 + 0.25 * b}}]  # fmt: skip
    docs = [
        {
            "name": f"{spec.name}: block",
            "color": [0.66, 0.68, 0.70],
            "finish": "metal",
            "features": block,
        },
        {
            "name": f"{spec.name}: cylinder heads",
            "color": [0.55, 0.57, 0.59],
            "finish": "metal",
            "features": heads,
        },
        {
            "name": f"{spec.name}: cam covers",
            "color": [0.62, 0.06, 0.06],
            "finish": "paint",
            "features": covers,
        },
        {
            "name": f"{spec.name}: intake",
            "color": [0.08, 0.08, 0.09],
            "finish": "paint_matte",
            "features": intake,
        },
        {
            "name": f"{spec.name}: exhaust",
            "color": [0.45, 0.33, 0.25],
            "finish": "metal",
            "features": exhaust,
        },
        {
            "name": f"{spec.name}: sump",
            "color": [0.1, 0.1, 0.11],
            "finish": "paint_matte",
            "features": sump,
        },
        {
            "name": f"{spec.name}: flywheel",
            "color": [0.72, 0.73, 0.75],
            "finish": "polished",
            "features": flywheel,
        },
        {
            "name": f"{spec.name}: front pulley",
            "color": [0.2, 0.2, 0.22],
            "finish": "metal",
            "features": pulley,
        },
    ]
    if spec.turbo:
        x = length / 2 - 0.3 * b
        side = -1.0
        docs.append({"name": f"{spec.name}: turbocharger", "color": [0.7, 0.71, 0.73],
                     "finish": "polished", "features": [
            {"id": "turbine", "name": "Turbine housing", "type": "sphere", "radius": 0.75 * b,
             "at": {"x": x, "y": side * 1.9 * width, "z": deck * 0.55}},
            {"id": "compressor", "name": "Compressor housing", "type": "cylinder",
             "radius": 0.8 * b, "height": 0.6 * b, "axis": "x",
             "at": {"x": x + 0.9 * b, "y": side * 1.9 * width, "z": deck * 0.55}}]})  # fmt: skip
    return docs
