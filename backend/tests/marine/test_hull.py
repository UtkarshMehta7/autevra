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


def test_holtrop_wave_resistance_matches_the_published_example() -> None:
    # Holtrop and Mennen's worked example: L 205 m, B 32 m, T 10 m, 37 500 m3, Cp 0.5833,
    # Cm 0.98, Cwp 0.75, lcb -0.75 %, bulb 20 m2 centred 4 m up, transom 16 m2, at 25 knots.
    r = h.holtrop_wave(205, 32, 10, 37500, 0.5833, 0.98, 0.75, -0.75, 16.0, 25 * 0.5144,
                       bulb_area=20, bulb_height=4)  # fmt: skip
    assert r["froude"] == pytest.approx(0.2868, abs=2e-4)
    assert r["c1"] == pytest.approx(1.398, abs=1e-3)
    assert r["c2"] == pytest.approx(0.7595, abs=1e-4)
    assert r["c5"] == pytest.approx(0.9592, abs=1e-4)
    assert r["m1"] == pytest.approx(-2.1274, abs=1e-4)
    assert r["lambda"] == pytest.approx(0.6513, abs=1e-4)
    assert r["half_entrance_deg"] == pytest.approx(12.08, abs=0.01)
    assert r["rw_n"] == pytest.approx(557.11e3, rel=0.01)


def test_total_resistance_adds_wave_making_and_is_continuous() -> None:
    s = h.HullSpec()
    r = h.resistance(s, 8)
    parts = (r["viscous_resistance_n"] + r["wave_resistance_n"] + r["transom_resistance_n"]
             + r["correlation_resistance_n"])  # fmt: skip
    assert r["total_resistance_n"] == pytest.approx(parts)
    assert r["effective_power_kw"] == pytest.approx(r["total_resistance_n"] * r["speed_ms"] / 1e3)
    assert r["effective_power_kw"] > r["effective_power_kw_lower_bound"]
    # wave-making is negligible when slow and takes over towards hull speed
    slow, fast = h.resistance(s, 3), h.resistance(s, 10)
    assert slow["wave_resistance_n"] < 0.05 * slow["viscous_resistance_n"]
    assert fast["wave_resistance_n"] > fast["viscous_resistance_n"]
    # no jump where the method changes formula (Fn 0.4 and 0.55)
    for fn in (0.4, 0.55):
        v = fn * (h.G * s.length) ** 0.5 / 0.514444
        a, b = h.resistance(s, v - 1e-4), h.resistance(s, v + 1e-4)
        assert a["wave_resistance_n"] == pytest.approx(b["wave_resistance_n"], rel=1e-3)


def test_lcb_closed_form_matches_the_integrated_hydrostatics() -> None:
    for s in (h.HullSpec(), h.HullSpec(cp=0.7, transom=0.2), h.HullSpec(transom=0.0)):
        numeric = 100 * (h.hydrostatics(s)["lcb_m"] / s.length - 0.5)
        assert h.lcb_percent(s) == pytest.approx(numeric, abs=0.01)
