"""Bill of materials: the project's parts grouped into lines (identical parts counted).

Parts with the same geometry and category form one line with a quantity; the corner or
side words of their names ("front left", "rear right") are dropped from the line name.
Volumes are of the modelled solids. No mass is given: several parts are modelled as solid
envelopes (the body is not a sheet-metal shell), so volume times a density would mislead.
"""

import csv
import io
import re
from dataclasses import dataclass

from autevra.api.model_service import VehicleModel
from autevra.cad import kernel

_SIDES = re.compile(r"\b(front|rear)?\s*(left|right)\b|\b(front|rear)\b", re.IGNORECASE)


@dataclass(frozen=True)
class BomLine:
    item: str
    category: str
    quantity: int
    size: tuple[float, float, float]  # bounding box of one part, mm
    volume: float  # of one part, mm^3
    source: str  # "parametric" or "Part Design"
    parts: tuple[str, ...]  # part ids


def _base_name(names: list[str]) -> str:
    if len(names) == 1:
        return names[0]
    stripped = {re.sub(r"\s+", " ", _SIDES.sub("", n)).strip() for n in names}
    return stripped.pop() if len(stripped) == 1 else names[0]


def bill_of_materials(model: VehicleModel) -> list[BomLine]:
    groups: dict[tuple[str, str], list] = {}
    for part in model.parts:
        groups.setdefault((part.geometry, part.category), []).append(part)
    lines = []
    for (key, category), parts in groups.items():
        shape = model.shapes[key]
        (x0, y0, z0), (x1, y1, z1) = kernel.bounds(shape)
        lines.append(BomLine(
            item=_base_name([p.name for p in parts]), category=category,
            quantity=len(parts), size=(round(x1 - x0, 1), round(y1 - y0, 1), round(z1 - z0, 1)),
            volume=kernel.volume(shape),
            source="Part Design" if category == "custom" else "parametric",
            parts=tuple(p.id for p in parts),
        ))  # fmt: skip
    return sorted(lines, key=lambda line: (line.source, line.category, line.item))


def to_csv(lines: list[BomLine]) -> str:
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["item", "category", "quantity", "length_mm", "width_mm", "height_mm",
                "volume_cm3", "source"])  # fmt: skip
    for line in lines:
        w.writerow([line.item, line.category, line.quantity, *line.size,
                    f"{line.volume / 1e3:.1f}", line.source])  # fmt: skip
    return out.getvalue()
