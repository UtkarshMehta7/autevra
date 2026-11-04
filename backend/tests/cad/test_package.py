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
