"""Hull form, hydrostatics and stability against closed-form results."""

import math

import pytest

from autevra.marine import hull as h


def test_form_coefficients_are_exact() -> None:
    s = h.HullSpec(cp=0.7, cm=0.9, transom=0.5)
    hs = h.hydrostatics(s)
    assert hs["cb"] == pytest.approx(0.7 * 0.9, rel=2e-3)
    assert hs["midship_area_m2"] == pytest.approx(0.9 * s.beam * s.draft, rel=2e-3)


def test_box_barge_limit() -> None:
    """Nearly full sections and waterlines tend to a box: KB = T/2, BM = B^2 / (12 T)."""
    s = h.HullSpec(length=40, beam=10, draft=2, depth=4, cp=0.9, cm=0.995, transom=0.95,
                   kg=2.0)  # fmt: skip
    hs = h.hydrostatics(s)
    assert hs["kb_m"] == pytest.approx(1.0, rel=0.03)
    # transverse I of the waterplane over the volume: within 15 % of the box value
    assert hs["bm_m"] == pytest.approx(10**2 / (12 * 2), rel=0.15)


def test_gz_starts_with_the_metacentric_height() -> None:
    s = h.HullSpec()
    gm = h.hydrostatics(s)["gm_m"]
    gz5 = next(p["gz_m"] for p in h.gz_curve(s, [5.0]))
    assert gz5 == pytest.approx(gm * math.sin(math.radians(5)), rel=0.08)
    assert h.gz_curve(s, [0.0])[0]["gz_m"] == pytest.approx(0.0, abs=1e-3)


def test_raising_kg_fails_the_imo_criteria() -> None:
    assert all(r["pass"] for r in h.imo_criteria(h.HullSpec()))
    tender = h.imo_criteria(h.HullSpec(kg=1.45))
    assert not all(r["pass"] for r in tender)


def test_friction_line_and_resistance_scale_with_speed() -> None:
    s = h.HullSpec()
    r6, r8 = h.resistance(s, 6), h.resistance(s, 8)
    rn = r6["reynolds"]
    assert r6["cf"] == pytest.approx(0.075 / (math.log10(rn) - 2) ** 2)
    assert r8["viscous_resistance_n"] > r6["viscous_resistance_n"] * (8 / 6) ** 1.8


def test_invalid_hulls() -> None:
    with pytest.raises(ValueError):
        h.HullSpec(depth=0.9, draft=1.0)
    with pytest.raises(ValueError):
        h.HullSpec(cp=0.5, transom=0.95)
