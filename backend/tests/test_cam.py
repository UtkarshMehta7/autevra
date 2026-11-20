"""2.5-axis CAM: cutting data, gouge-free toolpaths, rest machining, hole cycles, process
order and the G-code program."""

import math
import re

import pytest
from fastapi.testclient import TestClient
from shapely import Point

from autevra.cam import gcode, milling
from autevra.cam import tooling as tl
from autevra.part.features import PartDoc

BLOCK = {"id": "block", "type": "box", "size": [80, 60, 30], "at": {"z": 15}}
POCKET = {
    "id": "pocket",
    "type": "box",
    "op": "cut",
    "size": [30, 24, 10],
    "at": {"x": -15, "z": 25},
}
STEP = {"id": "step", "type": "box", "op": "cut", "size": [30, 70, 12], "at": {"x": 30, "z": 30}}


def doc(*features: dict) -> PartDoc:
    return PartDoc.model_validate({"name": "Test", "features": [BLOCK, *features]})


def test_cutting_data_formulas():
    mat = tl.MATERIALS["aluminium 6061-T6"]
    tool = tl.Tool(1, "end mill", 10.0, 3)
    sp = tl.mill_speeds(tool, mat, 60_000)
    n = 1000 * 300 / (math.pi * 10)
    assert sp.rpm == pytest.approx(n)
    assert sp.feed == pytest.approx(n * 3 * 0.010 * 10)
    assert not sp.capped
    capped = tl.mill_speeds(tool, mat, 5000)
    assert capped.rpm == 5000 and capped.capped
    tap = tl.drill_speeds(tl.Tool(2, "tap", 8.0, pitch=1.25), mat, 12_000)
    assert tap.feed == pytest.approx(tap.rpm * 1.25)  # rigid tapping: one pitch per revolution
    assert tl.power_kw(5, 4, 1000, 800) == pytest.approx(5 * 4 * 1000 * 800 / 6e7)


def _feed_points(op: milling.Operation):
    for m in op.moves:
        if m.kind != "rapid":
            yield from m.pts


def test_no_gouge_and_stock_respected():
    d = doc(POCKET, STEP)
    plan = milling.plan(d, milling.CamIn())
    built = milling.build_part(d).shape
    x0, y0, zb, x1, y1, zt = plan["setup"].stock
    assert zt == pytest.approx(31) and zb == pytest.approx(-3)
    for op in plan["operations"]:
        if op.cycle or op.tool.kind != "end mill" or op.name.startswith("Counterbore"):
            continue
        r = op.tool.diameter / 2
        leave = 0.3 if op.name.startswith(("Rough", "Rest")) else 0.0
        cache: dict[float, object] = {}
        for x, y, z in _feed_points(op):
            assert z >= -1e-6, "never below the part bottom (the skin holds the part)"
            if op.name.startswith("Face"):
                assert z >= 30 - 1e-6
                continue
            if z >= 30 - 1e-6:  # above the part: air (plunges start 1 mm above the last level)
                continue
            key = round(z, 3)
            if key not in cache:
                cache[key] = milling.section(built, z + milling.EPS, 0.01)
            dist = cache[key].distance(Point(x, y))
            assert dist >= r + leave - 0.05, (
                f"{op.name}: tool centre {dist:.3f} mm from the part at z {z}"
            )


def test_floors_are_levels_and_volumes():
    plan = milling.plan(doc(POCKET, STEP), milling.CamIn())
    assert 20.0 in [round(z, 6) for z in plan["levels"]]  # pocket floor
    assert 24.0 in [round(z, 6) for z in plan["levels"]]  # step floor
    part_vol = 80 * 60 * 30 - 30 * 24 * 10 - 25 * 60 * 6  # the step overhangs the block end
    assert plan["removed_volume"] == pytest.approx(plan["stock_volume"] - part_vol, rel=1e-6)
    assert plan["mass_kg"] == pytest.approx(part_vol * 1e-9 * 2700, rel=1e-6)


def test_rest_machining_and_corner_radius_note():
    slot = {
        "id": "slot",
        "type": "slot",
        "length": 30,
        "width": 6,
        "depth": 5,
        "at": {"x": -15, "y": -22, "z": 30},
    }
    plan = milling.plan(doc(slot), milling.CamIn(rough_tool=20))
    names = [op.name for op in plan["operations"]]
    assert any(n.startswith("Rest machining") for n in names)
    finish = next(op for op in plan["operations"] if op.name.startswith("Finish"))
    assert finish.tool.diameter == 4.0  # a 6 mm slot needs a tool under 6
    assert any("R2" in n for n in plan["notes"])


def test_unreachable_material_is_reported():
    slot = {"id": "slot", "type": "slot", "length": 30, "width": 2.5, "depth": 5, "at": {"z": 30}}
    plan = milling.plan(doc(slot), milling.CamIn())
    assert any("no end mill" in w for w in plan["warnings"])
    assert plan["rest_area"] > 10


def test_hole_cycles_order_and_entry():
    holes = [
        {
            "id": "h1",
            "type": "hole",
            "kind": "counterbore",
            "size": "M6",
            "through": True,
            "at": {"x": -30, "y": 20, "z": 30},
        },
        {
            "id": "h2",
            "type": "hole",
            "kind": "tapped",
            "size": "M8",
            "depth": 15,
            "at": {"x": 30, "y": 0, "z": 18},
        },  # below the step floor (z 24)
        {
            "id": "h3",
            "type": "hole",
            "diameter": 5,
            "depth": 8,
            "at": {"x": -30, "y": -20, "z": 30},
        },
    ]
    plan = milling.plan(doc(STEP, *holes), milling.CamIn())
    ops = plan["operations"]
    order = [op.name.split(" ")[0] for op in ops]
    first = {k: order.index(k) for k in ("Rough", "Spot", "Drill", "Counterbore", "Rigid")}
    assert first["Rough"] < first["Spot"] < first["Drill"] < first["Counterbore"] < first["Rigid"]
    cycles = {op.name: op.cycle for op in ops if op.cycle}
    deep = cycles["Drill ⌀6.6 peck (h1)"]
    assert deep["code"] == "G83" and deep["peck"] == pytest.approx(6.6)
    shallow = next(c for n, c in cycles.items() if "(h3)" in n)
    assert shallow["code"] == "G81"
    assert shallow["depth"] == pytest.approx(8 + 0.3 * 5)  # drill point allowance
    tap = next(c for n, c in cycles.items() if n.startswith("Rigid"))
    assert tap["points"][0][2] == pytest.approx(24.0)  # drilled from the material top
    assert any("h2 starts 6.0 mm below" in w for w in plan["warnings"])


def test_gcode_program():
    plan = milling.plan(
        doc(
            POCKET,
            {
                "id": "h",
                "type": "hole",
                "kind": "tapped",
                "size": "M6",
                "depth": 12,
                "at": {"x": 25, "y": 15, "z": 30},
            },
        ),
        milling.CamIn(),
    )
    prog = gcode.post(plan["operations"], plan["setup"], title="Test (⌀)")
    lines = prog.splitlines()
    assert lines[0] == "%" and lines[-1] == "%" and "M30" in lines
    assert all(line.isascii() for line in lines)
    assert "G21 G17 G90 G94 G40 G49 G80" in lines
    tool_calls = [line for line in lines if re.fullmatch(r"T\d+ M6", line)]
    assert len(tool_calls) == len({op.tool.number for op in plan["operations"]})
    assert any(line.startswith("M29 S") for line in lines)
    tap = next(line for line in lines if " G84 " in line)
    assert " Z-11 " in tap  # thread 12 - 2 P = 10 deep from z 30 -> z 20; stock top 31 is Z0
    zs = [float(m.group(1)) for line in lines if (m := re.search(r"Z(-?\d+(?:\.\d+)?)", line))]
    assert min(zs) >= -(31 + 3) - 1e-6  # never below the stock bottom
    # no duplicated consecutive positions
    moves = [line for line in lines if line.startswith(("G0 ", "G1 "))]
    assert all(
        a.split(" F")[0][3:] != b.split(" F")[0][3:] for a, b in zip(moves, moves[1:], strict=False)
    )


def test_api(client: TestClient):
    pid = client.post("/api/projects", json={"name": "Cam", "domain": "machinery"}).json()["id"]
    part = client.post(
        f"/api/projects/{pid}/parts", json={"name": "Block", "features": [BLOCK, POCKET]}
    ).json()
    out = client.post(
        f"/api/projects/{pid}/parts/{part['id']}/cam", json={"material": "steel C45"}
    ).json()
    assert out["operations"] and out["gcode"].startswith("%")
    assert all(len(p) <= 401 for op in out["operations"] for p in op["paths"])
    assert client.post(f"/api/projects/{pid}/parts/nope/cam", json={}).status_code == 404
