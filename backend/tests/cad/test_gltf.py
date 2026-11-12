"""glTF binary export: structure, shared meshes, units and frame."""

import cadquery as cq
import numpy as np
import pytest

from autevra.cad import gltf
from autevra.cad import kernel as k


def _at(x: float) -> np.ndarray:
    m = np.eye(4)
    m[0, 3] = x
    return m


@pytest.mark.cad
def test_glb_structure_instances_and_bounds() -> None:
    box = cq.Workplane().box(1000, 400, 200).val()
    ball = cq.Workplane().sphere(100).val()
    parts = [k.Part("body", box, _at(0), (0.2, 0.4, 0.6)),
             k.Part("wheel_l", ball, _at(500), (0.1, 0.1, 0.1)),
             k.Part("wheel_r", ball, _at(-500), (0.1, 0.1, 0.1)),
             k.Part("marker", ball, _at(0), (1.0, 0.0, 0.0))]  # fmt: skip
    data = gltf.glb(parts, name="demo")
    doc, blob = gltf.read(data)
    assert doc["asset"]["version"] == "2.0" and len(data) % 4 == 0
    assert len(doc["buffers"]) == 1 and doc["buffers"][0]["byteLength"] == len(blob)
    nodes = {n["name"]: n for n in doc["nodes"]}
    assert doc["nodes"][0]["children"] == [1, 2, 3, 4]
    # the two wheels share one mesh; the red marker shares its accessors, not its material
    assert nodes["wheel_l"]["mesh"] == nodes["wheel_r"]["mesh"] != nodes["marker"]["mesh"]
    wheel = doc["meshes"][nodes["wheel_l"]["mesh"]]["primitives"][0]
    marker = doc["meshes"][nodes["marker"]["mesh"]]["primitives"][0]
    assert wheel["attributes"] == marker["attributes"] and wheel["material"] != marker["material"]
    assert len(doc["materials"]) == 3
    assert nodes["wheel_l"]["matrix"][12:15] == [500.0, 0.0, 0.0]  # column-major translation
    # body accessor: bounds in mm, 12 triangles, unit normals
    prim = doc["meshes"][nodes["body"]["mesh"]]["primitives"][0]
    pos, nor, idx = (doc["accessors"][prim["attributes"]["POSITION"]],
                     doc["accessors"][prim["attributes"]["NORMAL"]],
                     doc["accessors"][prim["indices"]])  # fmt: skip
    assert pos["min"] == [-500.0, -200.0, -100.0] and pos["max"] == [500.0, 200.0, 100.0]
    assert idx["count"] == 36
    view = doc["bufferViews"][nor["bufferView"]]
    normals = np.frombuffer(blob, np.float32, nor["count"] * 3, view["byteOffset"])
    normals = normals.reshape(-1, 3)
    assert np.linalg.norm(normals, axis=1) == pytest.approx(1.0, abs=1e-5)
    assert np.abs(normals).max(axis=1) == pytest.approx(1.0, abs=1e-5)  # box faces: axis normals
    iview = doc["bufferViews"][idx["bufferView"]]
    tri = np.frombuffer(blob, np.uint32, idx["count"], iview["byteOffset"])
    assert tri.max() < pos["count"] and all(v["byteOffset"] % 4 == 0 for v in doc["bufferViews"])


def test_root_turns_mm_z_up_into_m_y_up() -> None:
    root = np.array(gltf.ROOT).reshape(4, 4).T  # column-major -> matrix
    assert root @ np.array([1000.0, 0, 0, 1]) == pytest.approx([1, 0, 0, 1])  # forward stays x
    assert root @ np.array([0, 0, 1000.0, 1]) == pytest.approx([0, 1, 0, 1])  # up becomes +y
    assert root @ np.array([0, 1000.0, 0, 1]) == pytest.approx([0, 0, -1, 1])
    assert np.linalg.det(root[:3, :3]) > 0  # a rotation and scale, not a mirror


def test_empty_export_is_still_a_valid_file() -> None:
    doc, blob = gltf.read(gltf.glb([]))
    assert doc["scenes"] == [{"nodes": [0]}] and blob == b"" and "meshes" not in doc
    with pytest.raises(ValueError):
        gltf.read(b"not a glb file....")
