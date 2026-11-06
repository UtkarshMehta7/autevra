import math
import xml.etree.ElementTree as ET

import pytest
from fastapi.testclient import TestClient

from autevra.core import derived
from autevra.core.parameters import default_values
from autevra.domains.automotive import package as pk
from autevra.domains.automotive import spec

pytestmark = pytest.mark.cad


def _angles(**changes: float) -> dict[str, float]:
    return pk.clearance_angles(default_values() | spec.TEMPLATES["suv"] | changes)


def test_tangent_angle_matches_geometry() -> None:
    r, centre = 300.0, (0.0, 300.0)
    for point in ((900.0, 250.0), (1400.0, 600.0), (600.0, 150.0)):
        angle = pk._tangent_angle(point, centre, r)
        assert angle is not None and 0 < angle < 90
        # The line through the point at that angle touches the tyre: distance r from the
        # centre, with the tyre above it (the ground side).
        a = math.radians(angle)
        nx, nz = math.sin(a), -math.cos(a)  # unit normal of a line rising towards the front
        dist = (centre[0] - point[0]) * nx + (centre[1] - point[1]) * nz
        assert abs(dist) == pytest.approx(r, rel=1e-9)
    assert pk._tangent_angle((900.0, 0.0), centre, r) == pytest.approx(
        0.0, abs=1e-9
    )  # on the ground
    assert pk._tangent_angle((0.0, 100.0), centre, r) is None  # inside the tyre


def test_clearance_angles_respond_like_a_vehicle() -> None:
    base = _angles()
    assert _angles(ground_clearance=base_gc() + 60)["approach_angle"] > base["approach_angle"]
    assert _angles(front_overhang=1100)["approach_angle"] < base["approach_angle"]
    assert _angles(rear_overhang=1200)["departure_angle"] < base["departure_angle"]
    raised = {"ground_clearance": 280.0}  # a high departure line, which the tow ball limits
    with_bar = _angles(tow_bar=1, **raised)["departure_angle"]
    assert with_bar < _angles(tow_bar=0, **raised)["departure_angle"]
    assert _angles(wheelbase=3200)["breakover_angle"] < base["breakover_angle"]


def base_gc() -> float:
    return (default_values() | spec.TEMPLATES["suv"])["ground_clearance"]


def test_an_suv_clears_more_than_a_sedan_and_a_supercar_least() -> None:
    def approach(cls: str) -> float:
        return pk.clearance_angles(default_values() | spec.TEMPLATES[cls])["approach_angle"]

    assert approach("suv") > approach("sedan") > approach("supercar")


def test_package_values_are_derived_values_for_requirements_and_queries() -> None:
    v = default_values()
    for key in ("approach_angle", "departure_angle", "breakover_angle", "h_point_height"):
        assert key in derived.DERIVED
        assert derived.compute(key, v) > 0


def test_the_drawing_is_valid_svg_with_three_views() -> None:
    svg = pk.drawing_svg(default_values() | spec.TEMPLATES["pickup"], title="Test")
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg")
    text = " ".join(t.text or "" for t in root.iter() if t.tag.endswith("text"))
    for label in ("SIDE VIEW", "TOP VIEW", "FRONT VIEW", "approach"):
        assert label in text
    wheelbase = f"{spec.TEMPLATES['pickup']['wheelbase']:.0f}"
    assert wheelbase in text


def test_package_endpoints(client: TestClient, project: str) -> None:
    values = client.get(f"/api/projects/{project}/package").json()
    ids = {v["id"] for v in values}
    assert {"approach_angle", "departure_angle", "breakover_angle", "wheelbase"} <= ids
    svg = client.get(f"/api/projects/{project}/package.svg")
    assert svg.headers["content-type"].startswith("image/svg+xml")
    ET.fromstring(svg.text)


def _seating(cls: str, **changes: float) -> dict[str, float]:
    return pk.seating(default_values() | spec.TEMPLATES[cls] | changes)


@pytest.mark.parametrize("cls", sorted(spec.TEMPLATES))
def test_every_template_seats_a_large_adult_under_the_roof(cls: str) -> None:
    # The integration check warns below 25 mm; low cars use low, reclined sports seats.
    assert _seating(cls)["headroom"] >= 25.0


def test_seating_allowances_are_parameters() -> None:
    base = _seating("sedan")
    lower = _seating("sedan", seat_height=200)
    assert lower["h_point_z"] == pytest.approx(base["h_point_z"] - 80.0)
    assert lower["headroom"] == pytest.approx(base["headroom"] + 80.0)
    # A steeper recline lowers the head: the gain follows the cosine of the backrest angle.
    reclined = _seating("sedan", seat_recline=32)
    gain = 715.0 * (1 - math.cos(math.radians(32)) / math.cos(math.radians(22)))
    assert reclined["headroom"] == pytest.approx(base["headroom"] + gain)
    # The dashboard zone moves the front seats rearward.
    deeper = _seating("sedan", dash_zone=450)
    assert deeper["h_point_x"] == pytest.approx(base["h_point_x"] - 100.0)


def test_row_pitch_drives_the_seat_rows_rule() -> None:
    from autevra.domains.automotive import rules

    p = default_values() | spec.TEMPLATES["city_car"]
    assert rules._seat_rows_fit(p) is None
    tight = rules._seat_rows_fit(p | {"row_pitch": 1100, "dash_zone": 700})
    assert tight is not None and "2 seat rows need" in tight
