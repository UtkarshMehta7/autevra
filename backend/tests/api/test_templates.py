import pytest
from fastapi.testclient import TestClient

from autevra.core.parameters import REGISTRY
from autevra.core.rules import validate
from autevra.core.templates import TEMPLATES

STYLE = {o: i for i, o in enumerate(REGISTRY["body_style"].options)}


def test_every_vehicle_class_is_a_template(client: TestClient) -> None:
    listed = client.get("/api/templates").json()
    ids = [t["id"] for t in listed]
    assert ids == ["city_car", "hatchback", "sedan", "suv", "pickup", "sports_car", "van",
                   "box_truck"]  # fmt: skip
    assert all(t["label"] and t["description"] for t in listed)


@pytest.mark.parametrize("template", sorted(TEMPLATES))
def test_templates_are_complete_rule_checked_designs(template: str) -> None:
    values = TEMPLATES[template].values()
    assert set(values) == set(REGISTRY)
    assert validate(values) == []


@pytest.mark.parametrize(
    ("template", "style"),
    [("pickup", "Pickup"), ("box_truck", "Box truck"), ("van", "Van"), ("sports_car", "Coupe"),
     ("suv", "SUV"), ("city_car", "Hatchback"), ("sedan", "Sedan")],
)  # fmt: skip
def test_a_project_starts_from_the_template_design(
    client: TestClient, template: str, style: str
) -> None:
    created = client.post("/api/projects", json={"name": "T", "template": template})
    assert created.status_code == 201
    values = created.json()["values"]
    assert values == TEMPLATES[template].values()
    assert values["body_style"] == STYLE[style]
    assert created.json()["can_undo"] is False  # the template is the initial design


def test_an_unknown_template_is_refused(client: TestClient) -> None:
    reply = client.post("/api/projects", json={"name": "T", "template": "tank"})
    assert reply.status_code == 409 and "unknown template" in reply.json()["detail"]


def test_road_loads_follow_the_class_and_say_they_are_typical() -> None:
    from autevra.domains.automotive.spec import VehicleSpec, generate

    drag = {t: TEMPLATES[t].values()["drag_coefficient"] for t in TEMPLATES}
    assert drag["box_truck"] > drag["pickup"] > drag["suv"] > drag["sedan"]
    spec = VehicleSpec()
    spec.set("vehicle_class", "box_truck", source="default")
    assert "not measured" in generate(spec).sources["drag_coefficient"]
