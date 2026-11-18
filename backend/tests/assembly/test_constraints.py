"""Assembly constraints: face signatures, re-matching after edits, the solver's poses,
degrees of freedom and conflicts, and the API that moves parts."""

import math

import numpy as np
import pytest
from fastapi.testclient import TestClient

from autevra.assembly import constraints as ac
from autevra.part.build import build_part, placement_matrix
from autevra.part.features import PartDoc, Placement

pytestmark = pytest.mark.cad

BLOCK = {
    "name": "Block",
    "features": [
        {"id": "b", "type": "box", "size": [80, 60, 30], "at": {"z": 15}},
        {
            "id": "h",
            "type": "hole",
            "diameter": 10,
            "through": True,
            "at": {"x": 20, "y": 10, "z": 30},
        },
    ],
}
PIN = {
    "name": "Pin",
    "at": {"x": 200, "y": -50, "z": 40, "rx": 30, "ry": 10, "rz": 45},
    "features": [
        {"id": "shank", "type": "cylinder", "radius": 5, "height": 50, "at": {"z": -25}},
        {"id": "head", "type": "cylinder", "radius": 9, "height": 6, "at": {"z": 3}},
    ],
}


def _setup(docs: dict) -> tuple[dict, dict, dict]:
    shapes = {k: build_part(PartDoc.model_validate(v)).shape for k, v in docs.items()}
    sigs = {k: ac.face_signatures(s) for k, s in shapes.items()}
    pl = {k: placement_matrix(PartDoc.model_validate(v).at) for k, v in docs.items()}
    cen = {}
    for k, s in shapes.items():
        c = s.BoundingBox().center
        cen[k] = (pl[k] @ np.array([c.x, c.y, c.z, 1.0]))[:3]
    return pl, sigs, cen


def _face(sigs, kind, radius=None, normal=None):  # noqa: ANN001, ANN202
    for i, s in enumerate(sigs):
        if (
            s.kind == kind
            and (radius is None or abs(s.radius - radius) < 1e-6)
            and (normal is None or np.allclose(s.direction, normal))
        ):
            return i
    raise AssertionError("face not found")


def _pin_constraints(sigs) -> list[ac.Constraint]:  # noqa: ANN001
    hole = _face(sigs["block"], "cylinder", 5)
    top = _face(sigs["block"], "plane", normal=(0, 0, 1))
    shank = _face(sigs["pin"], "cylinder", 5)
    under = next(
        i
        for i, s in enumerate(sigs["pin"])
        if s.kind == "plane" and s.direction[2] < -0.99 and abs(s.centre[2]) < 1e-6
    )
    return [
        ac.Constraint(id="fix", kind="fix", part="block"),
        ac.Constraint(
            id="axis",
            kind="coincidence",
            a=ac.FaceRef(part="block", face=hole),
            b=ac.FaceRef(part="pin", face=shank),
        ),
        ac.Constraint(
            id="seat",
            kind="contact",
            a=ac.FaceRef(part="block", face=top),
            b=ac.FaceRef(part="pin", face=under),
        ),
    ]


def test_pin_drops_into_the_hole_with_one_rotation_left():
    pl, sigs, cen = _setup({"block": BLOCK, "pin": PIN})
    out = ac.solve(_pin_constraints(sigs), pl, sigs, cen)
    m = out["placements"]["pin"]
    assert np.allclose(m[:3, 3], [20, 10, 30], atol=1e-6)
    assert np.allclose(m[:3, :3] @ [0, 0, 1], [0, 0, 1], atol=1e-8)
    assert out["dof_by_part"] == {"pin": 1, "block": 0} and out["dof"] == 1
    assert not out["conflicts"] and all(s["ok"] for s in out["status"])
    assert np.allclose(out["placements"]["block"], pl["block"])  # the fixed part never moves


def test_conflict_is_reported():
    pl, sigs, cen = _setup({"block": BLOCK, "pin": PIN})
    cons = _pin_constraints(sigs)
    cons.append(ac.Constraint(id="gap", kind="offset", value=5, a=cons[2].a, b=cons[2].b))
    assert set(ac.solve(cons, pl, sigs, cen)["conflicts"]) == {"seat", "gap"}


def test_offset_and_angle_between_plates():
    plate = {"name": "Plate", "features": [{"id": "p", "type": "box", "size": [100, 100, 10]}]}
    other = {**plate, "at": {"x": 30, "y": 300, "z": 50, "rx": 20, "ry": 40}}
    pl, sigs, cen = _setup({"a": plate, "b": other})
    up = _face(sigs["a"], "plane", normal=(0, 0, 1))
    down = _face(sigs["b"], "plane", normal=(0, 0, -1))
    side_a = _face(sigs["a"], "plane", normal=(1, 0, 0))
    side_b = _face(sigs["b"], "plane", normal=(1, 0, 0))
    cons = [
        ac.Constraint(id="f", kind="fix", part="a"),
        ac.Constraint(
            id="o",
            kind="offset",
            value=12.5,
            a=ac.FaceRef(part="a", face=up),
            b=ac.FaceRef(part="b", face=down),
        ),
        ac.Constraint(
            id="ang",
            kind="angle",
            value=30,
            a=ac.FaceRef(part="a", face=side_a),
            b=ac.FaceRef(part="b", face=side_b),
        ),
    ]
    out = ac.solve(cons, pl, sigs, cen)
    assert not out["conflicts"]
    m = out["placements"]["b"]
    bottom_of_b = (m @ np.array([0, 0, -5, 1.0]))[2]
    assert bottom_of_b == pytest.approx(5 + 12.5, abs=1e-6)  # a's top at z 5, then the gap
    xb = m[:3, :3] @ [1, 0, 0]
    assert math.degrees(math.acos(np.clip(xb[0], -1, 1))) == pytest.approx(30, abs=1e-6)
    assert out["dof_by_part"]["b"] == 2  # slides in the plane: 3 - the angle about z = 2


def test_rematch_after_an_edit_moves_the_face_index():
    pl, sigs, cen = _setup({"block": BLOCK, "pin": PIN})
    hole = _face(sigs["block"], "cylinder", 5)
    ref = ac.FaceRef(part="block", face=hole, sig=sigs["block"][hole])
    edited = {
        **BLOCK,
        "features": [*BLOCK["features"], {"id": "c", "type": "chamfer", "size": 1, "edges": ">Z"}],
    }
    new = ac.face_signatures(build_part(PartDoc.model_validate(edited)).shape)
    index, moved = ac.resolve(ref, new)
    assert new[index].kind == "cylinder" and new[index].radius == pytest.approx(5)
    assert moved == (index != hole)


def test_euler_round_trip():
    for at in (Placement(rx=30, ry=10, rz=45), Placement(rx=-170, ry=80, rz=5), Placement(ry=90)):
        m = placement_matrix(at)
        rx, ry, rz = ac.euler_xyz(m)
        assert np.allclose(placement_matrix(Placement(rx=rx, ry=ry, rz=rz)), m, atol=1e-9)


def test_api_moves_the_part(client: TestClient):
    pid = client.post("/api/projects", json={"name": "Mates", "domain": "machinery"}).json()["id"]
    block = client.post(f"/api/projects/{pid}/parts", json=BLOCK).json()["id"]
    pin = client.post(f"/api/projects/{pid}/parts", json=PIN).json()["id"]
    faces = {p: client.get(f"/api/projects/{pid}/mates/faces/{p}").json() for p in (block, pin)}
    assert all(f["outline"] for f in faces[block])
    hole = next(f["index"] for f in faces[block] if f["kind"] == "cylinder")
    top = next(f["index"] for f in faces[block] if f["label"] == "plane +Z")
    shank = next(f["index"] for f in faces[pin] if f["label"] == "cylinder ⌀10")
    under = next(
        f["index"]
        for f in faces[pin]
        if f["label"] == "plane −Z" and abs(f["sig"]["centre"][2]) < 1e-6
    )
    body = {
        "constraints": [
            {"id": "f", "kind": "fix", "part": block},
            {
                "id": "a",
                "kind": "coincidence",
                "a": {"part": block, "face": hole},
                "b": {"part": pin, "face": shank},
            },
            {
                "id": "c",
                "kind": "contact",
                "a": {"part": block, "face": top},
                "b": {"part": pin, "face": under},
            },
        ]
    }
    saved = client.put(f"/api/projects/{pid}/mates", json=body).json()
    assert saved["constraints"][1]["a"]["sig"]["kind"] == "cylinder"
    out = client.post(f"/api/projects/{pid}/mates/solve").json()
    assert out["applied"] and out["moved"] == [pin] and out["dof"] == 1
    at = next(p for p in client.get(f"/api/projects/{pid}/parts").json() if p["id"] == pin)[
        "document"
    ]["at"]
    assert (at["x"], at["y"], at["z"]) == pytest.approx((20, 10, 30), abs=1e-5)
    bad = {
        "constraints": [
            {
                "id": "x",
                "kind": "contact",
                "a": {"part": block, "face": 0},
                "b": {"part": block, "face": 1},
            }
        ]
    }
    client.put(f"/api/projects/{pid}/mates", json=bad)
    assert client.post(f"/api/projects/{pid}/mates/solve").status_code == 422
