"""Builds the vehicle model from a parameter set: assembly placement + cached CAD."""

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from autevra.assembly import graph
from autevra.assembly import transforms as tf
from autevra.assembly.model import COMPONENTS
from autevra.cad import kernel
from autevra.cad.cache import GeometryCache
from autevra.part import build as part_build
from autevra.part.features import PartDoc


@dataclass(frozen=True)
class PlacedPart:
    id: str
    name: str
    category: str
    geometry: str  # geometry key; parts with equal keys share one mesh
    matrix: list[list[float]]
    color: tuple[float, float, float]
    finish: str = "paint"


@dataclass(frozen=True)
class VehicleModel:
    parts: list[PlacedPart]
    shapes: dict[str, kernel.Shape]


def build_model(values: Mapping[str, float], cache: GeometryCache) -> VehicleModel:
    world = graph.place_all(values)
    parts, shapes = [], {}
    for c in COMPONENTS:
        if c.builder is None:
            continue
        key, shape = cache.shape(c.builder, c.resolve_inputs(values))
        if shape is None:  # not fitted in this configuration
            continue
        shapes[key] = shape
        color, finish = c.resolve_appearance(values)
        parts.append(PlacedPart(
            id=c.id, name=c.name, category=c.category, geometry=key,
            matrix=tf.to_list(world[c.id]), color=color, finish=finish,
        ))  # fmt: skip
    return VehicleModel(parts=parts, shapes=shapes)


def part_key(doc: PartDoc) -> str:
    """Geometry key of a Part Design part: a hash of its features (appearance and
    placement excluded, so moving or repainting a part does not rebuild it)."""
    import hashlib

    text = json.dumps([f.model_dump(mode="json") for f in doc.features], sort_keys=True)
    return "part:" + hashlib.sha256(text.encode()).hexdigest()[:20]


_REPORTS: dict[str, part_build.BuildResult] = {}  # build reports by geometry key
_REPORT_LIMIT = 256


def build_part(doc: PartDoc, cache: GeometryCache) -> tuple[str, part_build.BuildResult]:
    """The part's shape (cached by its feature hash) and its build report."""
    key = part_key(doc)

    def run() -> kernel.Shape | None:
        report = part_build.build_part(doc)
        _REPORTS[key] = report
        while len(_REPORTS) > _REPORT_LIMIT:
            _REPORTS.pop(next(iter(_REPORTS)))
        return report.shape

    shape = cache.custom(key, run)
    report = _REPORTS.get(key)
    if report is None or report.shape is not shape:  # evicted: build the report again
        report = part_build.build_part(doc)
        _REPORTS[key] = report
    return key, report


def add_parts(model: VehicleModel, parts: Iterable[tuple[str, PartDoc]],
              cache: GeometryCache) -> VehicleModel:  # fmt: skip
    """The model with the project's Part Design parts placed in it."""
    placed, shapes = list(model.parts), dict(model.shapes)
    for part_id, doc in parts:
        key, result = build_part(doc, cache)
        if result.shape is None:
            continue  # nothing built yet (empty tree or the first feature fails)
        shapes[key] = result.shape
        placed.append(PlacedPart(
            id=f"part_{part_id}", name=doc.name, category="custom", geometry=key,
            matrix=tf.to_list(part_build.placement_matrix(doc.at)), color=doc.color,
            finish=doc.finish,
        ))  # fmt: skip
    return VehicleModel(parts=placed, shapes=shapes)


def mesh_payload(model: VehicleModel, cache: GeometryCache, skip: Iterable[str] = ()) -> dict:
    """JSON-ready model: de-duplicated meshes plus one 4x4 transform per part.

    Geometry keys listed in ``skip`` (already held by the client) are left out.
    """
    skip = set(skip)
    return {
        "units": "mm",
        "axes": "ISO 8855 (X forward, Y left, Z up)",
        "geometries": {
            key: {"vertices": [round(v, 3) for v in mesh.vertices], "indices": mesh.indices}
            for key in model.shapes
            if key not in skip
            for mesh in [cache.mesh(key)]
        },
        "parts": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "geometry": p.geometry,
                "matrix": p.matrix,
                "color": p.color,
                "finish": p.finish,
            }
            for p in model.parts
        ],  # fmt: skip
    }


def export_step(model: VehicleModel, path: Path) -> Path:
    return kernel.export_step(
        [kernel.Part(p.id, model.shapes[p.geometry], p.matrix, p.color) for p in model.parts],
        path,
    )
