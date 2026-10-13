"""Builds the vehicle model from a parameter set: assembly placement + cached CAD."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from autevra.assembly import graph
from autevra.assembly import transforms as tf
from autevra.assembly.vehicle import COMPONENTS
from autevra.cad import kernel
from autevra.cad.cache import GeometryCache


@dataclass(frozen=True)
class PlacedPart:
    id: str
    name: str
    category: str
    geometry: str  # geometry key; parts with equal keys share one mesh
    matrix: list[list[float]]
    color: tuple[float, float, float]


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
        shapes[key] = shape
        parts.append(PlacedPart(
            id=c.id, name=c.name, category=c.category, geometry=key,
            matrix=tf.to_list(world[c.id]), color=c.color,
        ))  # fmt: skip
    return VehicleModel(parts=parts, shapes=shapes)


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
            }
            for p in model.parts
        ],  # fmt: skip
    }


def export_step(model: VehicleModel, path: Path) -> Path:
    return kernel.export_step(
        [kernel.Part(p.id, model.shapes[p.geometry], p.matrix, p.color) for p in model.parts],
        path,
    )
