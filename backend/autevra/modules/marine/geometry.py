"""Concept geometry of the vessel (level 1), coloured parts in mm: the hull as a loft of
rounded sections following the hull form's deck-edge half-breadths (bilge radius from the
midship coefficient: r = sqrt((1 - Cm) B T / (2 (1 - pi/4)))), deckhouse with a window
band, mast, propeller(s) and rudder. Frame: x forward from the aft perpendicular, z up
from the keel."""

import math

import numpy as np

from autevra.marine import hull as hk


def parts(spec: hk.HullSpec, twin: bool = False) -> list[dict]:
    mm = 1000.0
    lng, b, t, d = spec.length * mm, spec.beam * mm, spec.draft * mm, spec.depth * mm
    bilge = math.sqrt(max(1 - spec.cm, 1e-4) * b * t / (2 * (1 - math.pi / 4)))
    sections = []
    for xi in np.linspace(0, 1, 13):
        w = max(2 * float(hk.half_breadth_factor(spec, np.array([xi]))[0]) * b / 2, 0.04 * b)
        r = max(min(bilge, w / 2 - 1, d / 2 - 1), 0.0)
        sections.append({"z": float(xi) * lng, "width": w, "height": d, "radius": r})
    hull = {"name": f"{spec.name}: hull", "color": [0.08, 0.13, 0.27], "finish": "paint",
            "features": [{"id": "hull", "name": "Hull", "type": "loft", "sections": sections,
                          "at": {"z": d / 2, "ry": 90}}]}  # fmt: skip
    house_l, house_w, house_h = 0.32 * lng, 0.72 * b, 0.9 * d
    house = {"name": f"{spec.name}: deckhouse", "color": [0.93, 0.94, 0.95], "finish": "paint",
             "features": [{"id": "deckhouse", "name": "Deckhouse", "type": "box",
                           "size": [house_l, house_w, house_h],
                           "at": {"x": 0.55 * lng, "z": d + house_h / 2}}]}  # fmt: skip
    windows = {"name": f"{spec.name}: windows", "color": [0.05, 0.08, 0.12], "finish": "glass",
               "features": [{"id": "windows", "name": "Window band", "type": "box",
                             "size": [house_l * 1.01, house_w * 1.01, 0.3 * house_h],
                             "at": {"x": 0.55 * lng, "z": d + 0.68 * house_h}}]}  # fmt: skip
    mast = {"name": f"{spec.name}: mast", "color": [0.8, 0.81, 0.83], "finish": "metal",
            "features": [{"id": "mast", "name": "Mast", "type": "cylinder", "radius": 40,
                          "height": 1.2 * d, "at": {"x": 0.5 * lng,
                                                    "z": d + house_h + 0.6 * d}}]}  # fmt: skip
    ys = [-0.22 * b, 0.22 * b] if twin else [0.0]
    prop_r = 0.35 * t
    props = {"name": f"{spec.name}: propellers", "color": [0.72, 0.52, 0.26], "finish": "polished",
             "features": [{"id": f"prop{i}", "name": "Propeller", "type": "cylinder",
                           "radius": prop_r, "height": 0.25 * prop_r, "axis": "x",
                           "at": {"x": 0.06 * lng, "y": y, "z": 0.45 * t}}
                          for i, y in enumerate(ys)]}  # fmt: skip
    rudder = {"name": f"{spec.name}: rudder", "color": [0.55, 0.1, 0.08], "finish": "paint",
              "features": [{"id": f"rudder{i}", "name": "Rudder", "type": "box",
                            "size": [0.06 * lng, 0.04 * prop_r * 4, 1.1 * t],
                            "at": {"x": 0.015 * lng, "y": y, "z": 0.5 * t}}
                           for i, y in enumerate(ys)]}  # fmt: skip
    return [hull, house, windows, mast, props, rudder]
