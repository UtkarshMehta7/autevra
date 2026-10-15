import pytest
from fastapi.testclient import TestClient

from autevra.cad import kernel as k
from autevra.part import features as f
from autevra.part import tables
from autevra.part.build import build_part

pytestmark = pytest.mark.cad

PLATE = {
    "name": "Plate",
    "parameters": {"width": 200, "thickness": 10, "hole": "width / 25"},
    "features": [
        {"id": "plate", "type": "box",
         "bindings": {"size.0": "width", "size.1": "width", "size.2": "thickness"}},
        {"id": "hole", "type": "cylinder", "op": "cut", "height": 50,
         "bindings": {"radius": "hole"}},
    ],
}  # fmt: skip
TABLE = {
    "columns": ["width", "thickness"],
    "active": "L",
    "rows": [{"name": "S", "values": [100, 6]}, {"name": "L", "values": [400, 20]}],
}


def test_the_active_row_drives_the_part() -> None:
    doc = f.PartDoc.model_validate(PLATE | {"design_table": TABLE})
    assert doc.effective_parameters() == {"width": 400, "thickness": 20, "hole": "width / 25"}
    (x0, _, z0), (x1, _, z1) = k.bounds(build_part(doc).shape)
    assert (x1 - x0, z1 - z0) == (pytest.approx(400), pytest.approx(20))
    small = doc.model_copy(
        update={"design_table": doc.design_table.model_copy(update={"active": "S"})}
    )
    (x0, _, _), (x1, _, _) = k.bounds(build_part(small).shape)
    assert x1 - x0 == pytest.approx(100)


@pytest.mark.parametrize(
    "table",
    [{"columns": ["width"], "rows": [{"name": "S", "values": [1, 2]}]},  # wrong length
     {"columns": ["width", "width"], "rows": []},  # duplicate column
     {"columns": ["width"], "rows": [{"name": "S", "values": [1]}], "active": "M"},
     {"columns": ["depth"], "rows": []}],  # not a parameter
)  # fmt: skip
def test_inconsistent_tables_are_rejected(table: dict) -> None:
    with pytest.raises(ValueError):
        f.PartDoc.model_validate(PLATE | {"design_table": table})


def test_csv_round_trip_and_errors() -> None:
    table = f.DesignTable.model_validate(TABLE)
    text = tables.to_csv(table)
    assert text.splitlines() == ["variant,width,thickness", "S,100,6", "L,400,20"]
    assert tables.from_csv(text, active="L") == table
    cases = (("", "empty"), ("size,width\nS,1", "first column"),
             ("variant,width\nS,1,2", "line 2"), ("variant,width\nS,big", "numbers"))  # fmt: skip
    for bad, message in cases:
        with pytest.raises(ValueError, match=message):
            tables.from_csv(bad)


def test_design_table_api(client: TestClient, project: str) -> None:
    base = f"/api/projects/{project}/parts"
    part = client.post(base, json=PLATE).json()
    assert client.get(f"{base}/{part['id']}/design-table.csv").status_code == 404
    csv_text = "variant,width,thickness,depth\nS,100,6,5\nM,250,12,8\n"
    out = client.put(f"{base}/{part['id']}/design-table", content=csv_text).json()
    doc = out["document"]
    assert doc["design_table"]["columns"] == ["width", "thickness", "depth"]
    assert doc["parameters"]["depth"] == 5  # a new column becomes a parameter
    doc["design_table"]["active"] = "M"
    active = client.put(f"{base}/{part['id']}", json=doc).json()
    assert active["bounds"][1][0] - active["bounds"][0][0] == pytest.approx(250)
    exported = client.get(f"{base}/{part['id']}/design-table.csv")
    assert exported.headers["content-type"].startswith("text/csv")
    assert exported.text.splitlines()[2] == "M,250,12,8"
    bad = client.put(f"{base}/{part['id']}/design-table", content="variant,width\nS,x\n")
    assert bad.status_code == 422 and "numbers" in bad.json()["detail"]
