"""CNC turning: profile and reachable envelope, roughing never inside the finish
allowance, grooves programmed wall to wall or refused when too narrow, lathe G-code."""

import math

import pytest
from fastapi.testclient import TestClient

from autevra.cam import turning as tu
from autevra.part.features import PartDoc

pytestmark = pytest.mark.cad

SHAFT = [
    (0, 0),
    (20, 0),
    (20, 40),
    (16, 40),
    (16, 44),
    (20, 44),
    (20, 56),
    (12, 56),
    (12, 80),
    (0, 80),
]


def doc(points=SHAFT) -> PartDoc:  # noqa: ANN001
    return PartDoc.model_validate(
        {"name": "Shaft", "features": [{"id": "r", "type": "revolve", "points": points}]}
    )


def test_profile_envelope_and_bar():
    pl = tu.plan(doc(), tu.TurnIn())
    assert pl["bar"] == 45 and pl["length"] == pytest.approx(80)
    prof = dict(pl["profile"])
    r_at = lambda z: min(prof.items(), key=lambda kv: abs(kv[0] - z))[1]  # noqa: E731
    assert (
        r_at(10) == pytest.approx(20)
        and r_at(42) == pytest.approx(16)
        and r_at(70) == pytest.approx(12)
    )
    ((z0, z1, r_min, r_top),) = pl["grooves"]
    assert (z0, z1, r_min, r_top) == (
        pytest.approx(40, abs=1e-3),
        pytest.approx(44, abs=1e-3),
        16,
        20,
    )
    vol = math.pi * (20**2 * 40 + 16**2 * 4 + 20**2 * 12 + 12**2 * 24)
    assert pl["volume"] == pytest.approx(vol, rel=1e-6)


def test_toolpaths_stay_outside_the_part():
    pl = tu.plan(doc(), tu.TurnIn())
    prof = pl["profile"]
    front = pl["front"]

    def r_part(z: float) -> float:  # the profile radius at the nearest sample
        return min(prof, key=lambda zr: abs(zr[0] - z))[1]

    for op in pl["operations"]:
        allow = 0.3 - 1e-6 if op.name.startswith("Rough") else -1e-6
        if op.name.startswith(("Part off", "Face")):
            continue
        for kind, pts in op.moves:
            if kind == "rapid":
                continue
            for x, z in pts:
                zp = z + front
                if 0 < zp < front:
                    assert x / 2 >= r_part(zp) + allow - 0.01, f"{op.name} at z {zp}: r {x / 2}"


def test_groove_plunges_cover_the_width_and_narrow_grooves_are_refused():
    pl = tu.plan(doc(), tu.TurnIn())
    g = next(op for op in pl["operations"] if op.name.startswith("Groove"))
    centres = sorted({pts[0][1] for kind, pts in g.moves if kind == "feed"})
    assert centres[0] - 1.5 == pytest.approx(-40, abs=1e-3) and centres[-1] + 1.5 == pytest.approx(
        -36, abs=1e-3
    )
    narrow = [(0, 0), (10, 0), (10, 30), (9.05, 30), (9.05, 31.3), (10, 31.3), (10, 50), (0, 50)]
    pn = tu.plan(doc(narrow), tu.TurnIn())
    assert not any(op.name.startswith("Groove") for op in pn["operations"])
    assert any("narrower than the 3 mm" in w for w in pn["warnings"])


def test_refuses_parts_not_about_z():
    box = PartDoc.model_validate(
        {"name": "Box", "features": [{"id": "b", "type": "box", "size": [40, 20, 10]}]}
    )
    with pytest.raises(ValueError, match="revolved about its own Z axis"):
        tu.plan(box, tu.TurnIn())


def test_lathe_gcode():
    pl = tu.plan(doc(), tu.TurnIn())
    prog = tu.gcode(pl["operations"], tu.TurnIn(), "Shaft", pl["vc"])
    lines = prog.splitlines()
    assert lines[0] == "%" and "M30" in lines and "G21 G18 G40 G99" in lines
    assert "G50 S3500" in lines and any(line.startswith("G96 S200") for line in lines)
    assert any("G42" in line for line in lines) and "G40" in lines
    assert all(line.isascii() for line in lines)


def test_api(client: TestClient):
    pid = client.post("/api/projects", json={"name": "Lathe", "domain": "machinery"}).json()["id"]
    part = client.post(
        f"/api/projects/{pid}/parts",
        json={"name": "Shaft", "features": [{"id": "r", "type": "revolve", "points": SHAFT}]},
    ).json()["id"]
    out = client.post(
        f"/api/projects/{pid}/parts/{part}/turning", json={"material": "aluminium 6061-T6"}
    ).json()
    assert out["process"] == "turning" and out["gcode"].startswith("%") and out["operations"]
    assert all(p[1] == 0.0 for op in out["operations"] for path in op["paths"] for p in path)
