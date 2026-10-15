import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.cad


def test_bom_groups_identical_parts(client: TestClient, project: str) -> None:
    lines = client.get(f"/api/projects/{project}/bom").json()
    by_item = {line["item"]: line for line in lines}
    assert by_item["Wheel"]["quantity"] == 4  # four corners share one tyre geometry
    assert by_item["Rim"]["quantity"] == 4
    assert by_item["Body"]["quantity"] == 1 and by_item["Body"]["source"] == "parametric"
    assert sum(line["quantity"] for line in lines) == len(
        client.get(f"/api/projects/{project}/model").json()["parts"]
    )  # every placed part is on one line
    assert all(line["volume"] > 0 and min(line["size"]) > 0 for line in lines)


def test_bom_includes_part_design_parts_and_exports_csv(client: TestClient, project: str) -> None:
    part = {"name": "Bracket", "features": [{"id": "p", "type": "box", "size": [200, 100, 10]}]}
    client.post(f"/api/projects/{project}/parts", json=part)
    lines = client.get(f"/api/projects/{project}/bom").json()
    bracket = next(line for line in lines if line["item"] == "Bracket")
    assert bracket["source"] == "Part Design" and bracket["size"] == [200, 100, 10]
    assert bracket["volume"] == pytest.approx(200 * 100 * 10)
    csv_text = client.get(f"/api/projects/{project}/bom.csv").text.splitlines()
    assert csv_text[0].startswith("item,category,quantity,length_mm")
    assert any(
        row.startswith("Bracket,custom,1,200.0,100.0,10.0,200.0,Part Design") for row in csv_text
    )
