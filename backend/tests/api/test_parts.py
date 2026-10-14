import pytest
from fastapi.testclient import TestClient

from autevra.part import build as pb
from autevra.part import features as f

pytestmark = pytest.mark.cad

BRACKET = {
    "name": "Bracket",
    "features": [
        {"id": "plate", "type": "box", "size": [200, 200, 15]},
        {"id": "hole", "type": "cylinder", "op": "cut", "radius": 8, "height": 40,
         "at": {"x": 70}},
        {"id": "holes", "type": "circular_pattern", "count": 4},
        {"id": "round", "type": "fillet", "radius": 2},
    ],
    "at": {"x": 500, "z": 800},
}  # fmt: skip


def _doc(data: dict) -> f.PartDoc:
    return f.PartDoc.model_validate(data)


# --- builder ---


def test_a_bracket_builds_with_four_holes() -> None:
    plain = pb.build_part(_doc({"features": BRACKET["features"][:1]}))
    holed = pb.build_part(_doc({"features": BRACKET["features"][:3]}))
    assert not holed.errors and holed.built == ["plate", "hole", "holes"]
    hole = 3.14159265 * 8**2 * 15
    removed = pb.k.volume(plain.shape) - pb.k.volume(holed.shape)
    assert removed == pytest.approx(4 * hole, rel=1e-3)  # four through holes
    rounded = pb.build_part(_doc(BRACKET))
    assert rounded.built == ["plate", "hole", "holes", "round"]
    assert pb.k.volume(rounded.shape) < pb.k.volume(holed.shape)  # the fillets take a little


@pytest.mark.parametrize(
    "features",
    [
        [{"id": "b", "type": "revolve", "points": [[0, 0], [40, 0], [40, 180], [15, 220],
                                                   [15, 250], [0, 250]]},
         {"id": "s", "type": "shell", "thickness": 2, "open_towards": "+z"}],
        [{"id": "l", "type": "loft", "sections": [
            {"z": 0, "width": 200, "height": 200, "radius": 99},
            {"z": 2000, "width": 2400, "height": 2600, "radius": 1150},
            {"z": 6000, "width": 600, "height": 900, "radius": 290}]}],
        [{"id": "p", "type": "sweep", "path": [[0, 0, 0], [500, 0, 0], [500, 400, 0]],
          "radius": 30, "wall": 3, "bend_radius": 90}],
        [{"id": "e", "type": "extrude", "plane": "xz",
          "points": [[0, 0], [100, 0], [100, 50], [0, 50]], "depth": 40, "symmetric": True},
         {"id": "m", "type": "mirror", "plane": "yz"}],
        [{"id": "d", "type": "revolve", "points": [[30, -20], [300, -8], [300, 8], [30, 20]]},
         {"id": "blade", "type": "box", "size": [80, 6, 40], "at": {"x": 330, "rx": 20}},
         {"id": "blades", "type": "circular_pattern", "count": 24}],
        [{"id": "rail", "type": "box", "size": [1000, 40, 40]},
         {"id": "post", "type": "box", "size": [40, 40, 400], "at": {"x": -480, "z": 220}},
         {"id": "posts", "type": "linear_pattern", "count": 5, "step": [240, 0, 0]}],
    ],
    ids=["bottle", "fuselage", "pipe", "mirrored", "turbine", "frame"],
)  # fmt: skip
def test_parts_from_several_domains_build(features: list[dict]) -> None:
    result = pb.build_part(_doc({"features": features}))
    assert not result.errors, result.errors
    assert result.shape is not None and pb.k.is_valid(result.shape)


def test_a_failing_feature_is_named_and_the_earlier_work_kept() -> None:
    doc = _doc({"features": [
        {"id": "plate", "type": "box", "size": [100, 100, 10]},
        {"id": "too_big", "type": "fillet", "radius": 60},
        {"id": "never", "type": "cylinder", "radius": 5, "height": 5},
    ]})  # fmt: skip
    result = pb.build_part(doc)
    assert [e.feature for e in result.errors] == ["too_big"]
    assert result.built == ["plate"] and result.shape is not None


def test_cut_first_and_modifier_first_are_reported() -> None:
    cut_first = pb.build_part(_doc({"features": [
        {"id": "c", "type": "box", "op": "cut", "size": [10, 10, 10]}]}))  # fmt: skip
    assert cut_first.errors[0].message == "the first solid must add material"
    shell_first = pb.build_part(_doc({"features": [{"id": "s", "type": "shell"}]}))
    assert shell_first.errors[0].message == "add a solid before this modifier"


def test_suppressed_features_are_skipped() -> None:
    feats = [dict(BRACKET["features"][0]), dict(BRACKET["features"][1], suppressed=True)]
    result = pb.build_part(_doc({"features": feats}))
    assert result.built == ["plate"]


@pytest.mark.parametrize(
    "bad",
    [
        {"features": [{"id": "a", "type": "box"}, {"id": "a", "type": "box"}]},  # duplicate id
        {"features": [{"id": "r", "type": "revolve", "points": [[-1, 0], [5, 0], [5, 5]]}]},
        {"features": [{"id": "l", "type": "loft", "sections": [
            {"z": 10, "width": 5, "height": 5}, {"z": 0, "width": 5, "height": 5}]}]},
        {"features": [{"id": "s", "type": "sweep", "path": [[0, 0, 0], [1, 0, 0]],
                       "radius": 5, "wall": 5}]},
        {"features": [{"id": "x", "type": "teapot"}]},
    ],
)  # fmt: skip
def test_invalid_documents_are_rejected(bad: dict) -> None:
    with pytest.raises(ValueError):
        _doc(bad)


# --- API ---


def test_parts_crud_undo_and_model(client: TestClient, project: str) -> None:
    base = f"/api/projects/{project}/parts"
    created = client.post(base, json=BRACKET)
    assert created.status_code == 201
    part = created.json()
    assert part["built"] == ["plate", "hole", "holes", "round"] and not part["errors"]
    assert part["volume"] > 0 and not part["can_undo"]

    model = client.get(f"/api/projects/{project}/model").json()
    placed = [p for p in model["parts"] if p["category"] == "custom"]
    assert [p["name"] for p in placed] == ["Bracket"]
    assert placed[0]["matrix"][0][3] == 500 and placed[0]["matrix"][2][3] == 800

    edited = dict(BRACKET, features=BRACKET["features"][:2], name="Bracket, one hole")
    updated = client.put(f"{base}/{part['id']}", json=edited).json()
    assert updated["built"] == ["plate", "hole"] and updated["can_undo"]
    undone = client.post(f"{base}/{part['id']}/undo").json()
    assert undone["document"]["name"] == "Bracket" and undone["can_redo"]
    redone = client.post(f"{base}/{part['id']}/redo").json()
    assert redone["document"]["name"] == "Bracket, one hole"
    assert client.post(f"{base}/{part['id']}/redo").status_code == 409  # nothing left

    assert [p["id"] for p in client.get(base).json()] == [part["id"]]
    assert client.delete(f"{base}/{part['id']}").status_code == 204
    assert client.get(base).json() == []
    assert client.put(f"{base}/{part['id']}", json=BRACKET).status_code == 404


def test_parts_are_in_the_step_export(client: TestClient, project: str, tmp_path) -> None:
    client.post(f"/api/projects/{project}/parts", json=BRACKET)
    step = client.get(f"/api/projects/{project}/export.step")
    assert step.status_code == 200 and b"part_" in step.content


def test_a_bad_document_is_a_422(client: TestClient, project: str) -> None:
    bad = {"features": [{"id": "x", "type": "box", "size": [0, 1, 1]}]}
    assert client.post(f"/api/projects/{project}/parts", json=bad).status_code == 422


def test_the_feature_catalogue_lists_every_type(client: TestClient) -> None:
    body = client.get("/api/part-features").json()
    assert set(body["types"]) == set(f.FEATURE_TYPES)
    assert "features" in body["schema"]["properties"]
