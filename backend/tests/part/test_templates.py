import pytest
from fastapi.testclient import TestClient

from autevra.cad import kernel as k
from autevra.part import features as f
from autevra.part import templates as ft
from autevra.part.build import build_part

pytestmark = pytest.mark.cad

SOURCE = {
    "name": "Plate with a boss",
    "parameters": {"width": 200, "boss_r": 20, "boss_h": "boss_r * 2"},
    "features": [
        {"id": "plate", "type": "box", "bindings": {"size.0": "width", "size.1": "width"},
         "size": [200, 200, 10]},
        {"id": "boss", "type": "cylinder", "at": {"z": 20},
         "bindings": {"radius": "boss_r", "height": "boss_h"}},
        {"id": "hole", "type": "cylinder", "op": "cut", "radius": 6, "height": 200,
         "bindings": {"radius": "boss_r / 3"}},
    ],
}  # fmt: skip


def test_a_template_publishes_the_parameters_its_features_use() -> None:
    template = ft.from_part(f.PartDoc.model_validate(SOURCE), "Boss", ["boss", "hole"])
    assert set(template.parameters) == {"boss_r", "boss_h"}  # width is not used
    assert [x["id"] for x in template.features] == ["boss", "hole"]


def test_inserting_renames_binds_and_offsets() -> None:
    template = ft.from_part(f.PartDoc.model_validate(SOURCE), "Boss", ["boss", "hole"])
    target = f.PartDoc.model_validate({"parameters": {"size": 400}, "features": [
        {"id": "base", "type": "box", "size": [400, 400, 10]}]})  # fmt: skip
    how = ft.Insertion(template="x", prefix="b1", inputs={"boss_r": "size / 20"},
                       offset=(100.0, 0.0, 0.0))  # fmt: skip
    doc = ft.insert(target, template, how)
    assert doc.parameters["b1_boss_r"] == "size / 20"  # driven by the target's parameter
    assert doc.parameters["b1_boss_h"] == "b1_boss_r * 2"  # renamed inside expressions
    boss = next(x for x in doc.features if x.id == "b1_boss")
    assert boss.at.x == 100.0 and boss.bindings == {"radius": "b1_boss_r", "height": "b1_boss_h"}
    result = build_part(doc)
    assert not result.errors and result.built == ["base", "b1_boss", "b1_hole"]
    (x0, _, _), (x1, _, z1) = k.bounds(result.shape)
    assert z1 == pytest.approx(20 + 20)  # boss r = 400/20 = 20, h = 40, centred at z = 20


def test_an_input_sent_back_unchanged_keeps_the_template_meaning() -> None:
    template = ft.from_part(f.PartDoc.model_validate(SOURCE), "Boss", ["boss"])
    how = ft.Insertion(template="x", prefix="c", inputs={"boss_h": "boss_r * 2"})
    doc = ft.insert(f.PartDoc.model_validate(SOURCE), template, how)
    assert doc.parameters["c_boss_h"] == "c_boss_r * 2"


def test_inserting_twice_needs_another_prefix() -> None:
    template = ft.from_part(f.PartDoc.model_validate(SOURCE), "Boss", ["boss"])
    once = ft.insert(
        f.PartDoc.model_validate(SOURCE), template, ft.Insertion(template="x", prefix="a")
    )
    with pytest.raises(ValueError, match="another prefix"):
        ft.insert(once, template, ft.Insertion(template="x", prefix="a"))


def test_template_api(client: TestClient, project: str) -> None:
    part = client.post(f"/api/projects/{project}/parts", json=SOURCE).json()
    body = {"project_id": project, "part_id": part["id"], "name": "Boss",
            "feature_ids": ["boss", "hole"]}  # fmt: skip
    saved = client.post("/api/feature-templates", json=body)
    assert saved.status_code == 201
    tid = saved.json()["id"]
    assert [t["name"] for t in client.get("/api/feature-templates").json()] == ["Boss"]
    out = client.post(f"/api/projects/{project}/parts/{part['id']}/insert-template",
                      json={"template": tid, "prefix": "b2", "offset": [60, 60, 0]})  # fmt: skip
    assert out.status_code == 200
    assert "b2_boss" in out.json()["built"] and not out.json()["errors"]
    bad = client.post(f"/api/projects/{project}/parts/{part['id']}/insert-template",
                      json={"template": "nope", "prefix": "b3"})  # fmt: skip
    assert bad.status_code == 422
    assert client.delete(f"/api/feature-templates/{tid}").status_code == 204
