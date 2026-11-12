"""glTF 2.0 binary (.glb) export of placed parts: a lightweight mesh for viewers, web and
AR, next to the exact STEP export.

One mesh per distinct shape (repeated parts such as wheels share theirs), one node per
part with its placement matrix, and one material per colour. Each B-rep face is
tessellated with its own vertices, so normals are smooth within a face and creased
between faces. glTF is metres and Y-up: a root node scales millimetres to metres and turns
the Z-up project frame to Y-up. The file is written directly (JSON chunk + one binary
buffer); it carries triangles only, not the B-rep.
"""

import json
import struct
from collections.abc import Iterable

import numpy as np

from autevra.cad import kernel as k

# mm, Z-up (x fwd, y left)  ->  m, Y-up: (x, y, z) -> (x, z, -y) / 1000; column-major.
ROOT = [0.001, 0, 0, 0, 0, 0, -0.001, 0, 0, 0.001, 0, 0, 0, 0, 0, 1]


def _normals(v: np.ndarray, tri: np.ndarray) -> np.ndarray:
    """Area-weighted vertex normals."""
    face = np.cross(v[tri[:, 1]] - v[tri[:, 0]], v[tri[:, 2]] - v[tri[:, 0]])
    n = np.zeros_like(v)
    for i in range(3):
        np.add.at(n, tri[:, i], face)
    length = np.linalg.norm(n, axis=1, keepdims=True)
    return np.where(length > 1e-12, n / np.maximum(length, 1e-12), (0.0, 0.0, 1.0))


def glb(parts: Iterable[k.Part], tolerance: float = 0.5, name: str = "model") -> bytes:
    """The parts as one .glb file. ``tolerance`` is the chord deviation of the mesh, mm."""
    blob = bytearray()
    views: list[dict] = []
    accessors: list[dict] = []
    meshes: list[dict] = []
    materials: list[dict] = []
    nodes: list[dict] = [{"name": name, "matrix": ROOT, "children": []}]
    mesh_of: dict[int, int | None] = {}
    material_of: dict[tuple[float, float, float], int] = {}

    def view(data: bytes, target: int) -> int:
        while len(blob) % 4:
            blob.append(0)
        views.append({"buffer": 0, "byteOffset": len(blob), "byteLength": len(data),
                      "target": target})  # fmt: skip
        blob.extend(data)
        return len(views) - 1

    def geometry(shape: k.Shape) -> int | None:
        mesh = k.tessellate(shape, tolerance)
        v = np.asarray(mesh.vertices, dtype=np.float32).reshape(-1, 3)
        tri = np.asarray(mesh.indices, dtype=np.uint32).reshape(-1, 3)
        if len(v) == 0 or len(tri) == 0:
            return None
        n = _normals(v.astype(np.float64), tri).astype(np.float32)
        accessors.append({"bufferView": view(v.tobytes(), 34962), "componentType": 5126,
                          "count": len(v), "type": "VEC3", "min": v.min(axis=0).tolist(),
                          "max": v.max(axis=0).tolist()})  # fmt: skip
        accessors.append({"bufferView": view(n.tobytes(), 34962), "componentType": 5126,
                          "count": len(n), "type": "VEC3"})  # fmt: skip
        accessors.append({"bufferView": view(tri.tobytes(), 34963), "componentType": 5125,
                          "count": int(tri.size), "type": "SCALAR"})  # fmt: skip
        base = len(accessors) - 3
        meshes.append({"primitives": [{"attributes": {"POSITION": base, "NORMAL": base + 1},
                                       "indices": base + 2}]})  # fmt: skip
        return len(meshes) - 1

    for part in parts:
        key = id(part.shape)
        if key not in mesh_of:
            mesh_of[key] = geometry(part.shape)
        source = mesh_of[key]
        if source is None:
            continue
        color = tuple(round(float(c), 4) for c in part.color)
        if color not in material_of:
            materials.append({"pbrMetallicRoughness": {"baseColorFactor": [*color, 1.0],
                                                       "metallicFactor": 0.1,
                                                       "roughnessFactor": 0.6}})  # fmt: skip
            material_of[color] = len(materials) - 1
        # A mesh carries its material, so a shape used in two colours gets a second mesh
        # entry that shares the same accessors.
        wanted = material_of[color]
        prim = meshes[source]["primitives"][0]
        if "material" not in prim:
            prim["material"] = wanted
            mesh = source
        elif prim["material"] == wanted:
            mesh = source
        else:
            meshes.append({"primitives": [{**prim, "material": wanted}]})
            mesh = len(meshes) - 1
        matrix = np.asarray(part.matrix, dtype=float).T.reshape(-1).tolist()  # column-major
        nodes.append({"name": part.name, "mesh": mesh, "matrix": matrix})
        nodes[0]["children"].append(len(nodes) - 1)

    while len(blob) % 4:
        blob.append(0)
    doc: dict = {"asset": {"version": "2.0", "generator": "Autevra"}, "scene": 0,
                 "scenes": [{"nodes": [0]}], "nodes": nodes}  # fmt: skip
    if meshes:
        doc |= {"meshes": meshes, "materials": materials, "accessors": accessors,
                "bufferViews": views, "buffers": [{"byteLength": len(blob)}]}  # fmt: skip
    else:
        del nodes[0]["children"]
    text = json.dumps(doc, separators=(",", ":")).encode()
    text += b" " * (-len(text) % 4)
    chunks = struct.pack("<II", len(text), 0x4E4F534A) + text
    if meshes:
        chunks += struct.pack("<II", len(blob), 0x004E4942) + bytes(blob)
    return struct.pack("<III", 0x46546C67, 2, 12 + len(chunks)) + chunks


def read(data: bytes) -> tuple[dict, bytes]:
    """Split a .glb into its JSON document and binary buffer (for checks and tests)."""
    magic, version, total = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67 or version != 2 or total != len(data):
        raise ValueError("not a glTF 2.0 binary file")
    n, kind = struct.unpack_from("<II", data, 12)
    if kind != 0x4E4F534A:
        raise ValueError("the first chunk is not JSON")
    doc = json.loads(data[20 : 20 + n])
    rest = data[20 + n :]
    return doc, (rest[8 : 8 + struct.unpack_from("<I", rest, 0)[0]] if rest else b"")
