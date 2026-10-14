import json
import math
from pathlib import Path

import pytest

from autevra.cad import kernel as k
from autevra.part import features as f
from autevra.part.build import build_part, naca4

pytestmark = pytest.mark.cad


def _wing(**fields: object) -> k.Shape:
    doc = f.PartDoc.model_validate({"features": [{"id": "w", "type": "wing", **fields}]})
    result = build_part(doc)
    assert not result.errors, result.errors
    return result.shape


def test_naca_0012_is_twelve_percent_thick_near_thirty_percent_chord() -> None:
    pts = naca4("0012", n=200)
    upper = [(x, z) for x, z in pts if z >= 0]
    x_max, z_max = max(upper, key=lambda p: p[1])
    assert 2 * z_max == pytest.approx(0.12, abs=2e-4)  # published thickness, 12 % of chord
    assert x_max == pytest.approx(0.30, abs=0.01)
    assert all(abs(z + w) < 1e-12 for (_, z), (_, w) in zip(pts, reversed(pts), strict=True))


def test_naca_2412_camber_line_peaks_at_two_percent_at_forty_percent() -> None:
    pts = naca4("2412", n=200)
    n = len(pts) // 2
    upper, lower = list(reversed(pts[: n + 1])), pts[n:]
    mid = [((u[0] + w[0]) / 2, (u[1] + w[1]) / 2) for u, w in zip(upper, lower, strict=True)]
    x_peak, z_peak = max(mid, key=lambda p: p[1])
    assert z_peak == pytest.approx(0.02, abs=5e-4) and x_peak == pytest.approx(0.4, abs=0.02)


def test_wing_extents_follow_span_sweep_and_dihedral() -> None:
    span, sweep, dihedral, root = 5000.0, 20.0, 5.0, 1600.0
    (x0, y0, _), (x1, y1, z1) = k.bounds(_wing(span=span, sweep=sweep, dihedral=dihedral,
                                                 root_chord=root, twist=0.0))  # fmt: skip
    assert (y0, y1) == (pytest.approx(-span, abs=1), pytest.approx(span, abs=1))
    assert x1 == pytest.approx(0.0, abs=1)  # the root leading edge is the forward point
    tip_le = -span * math.tan(math.radians(sweep))
    assert x0 == pytest.approx(min(-root, tip_le - 800.0), abs=2)
    assert z1 > span * math.tan(math.radians(dihedral))  # the tip rises by the dihedral


def test_one_sided_wing_and_mirror_symmetry() -> None:
    both, one = _wing(both_sides=True), _wing(both_sides=False)
    assert k.volume(both) == pytest.approx(2 * k.volume(one), rel=1e-3)
    assert k.bounds(one)[0][1] == pytest.approx(0.0, abs=1)


@pytest.mark.parametrize("bad", ["0000", "2012", "12a4", "24123"])
def test_invalid_naca_codes_are_rejected(bad: str) -> None:
    with pytest.raises(ValueError):
        f.PartDoc.model_validate({"features": [{"id": "w", "type": "wing", "naca": bad}]})


def test_a_light_aircraft_builds_from_features() -> None:
    doc = f.PartDoc.model_validate(
        json.loads(Path(__file__).with_name("light_aircraft.json").read_text())
    )
    result = build_part(doc)
    assert not result.errors and result.built == ["fuselage", "wing", "tailplane", "fin"]
    assert k.solid_count(result.shape) == 1
    (_, y0, _), (_, y1, z1) = k.bounds(result.shape)
    assert y1 - y0 == pytest.approx(9000, abs=1) and z1 == pytest.approx(1550, abs=5)
