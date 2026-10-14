"""The half-car test on the design: criteria from the design, templates, sensitivity."""

from fastapi.testclient import TestClient

from autevra.core.parameters import default_values
from autevra.core.templates import TEMPLATES
from autevra.domains.automotive import tests as t
from autevra.engineering import testing as tst


def test_mass_centre_and_inertia_follow_the_design() -> None:
    v = default_values()
    p = t.half_car_params(v)
    assert p.front_to_cg + p.rear_to_cg == v["wheelbase"] / 1000
    front_heavy = t.half_car_params(v | {"front_mass_distribution": 65})
    assert front_heavy.front_to_cg < p.front_to_cg  # the CG moves towards the heavier axle
    heavier = t.half_car_params(v | {"pitch_dynamic_index": 1.2})
    assert heavier.pitch_inertia == 1.2 * p.pitch_inertia


def test_the_test_runs_on_the_default_design_and_every_template() -> None:
    for values in (default_values(), *(tpl.values() for tpl in TEMPLATES.values())):
        record = tst.quick_evaluate("half_car", "vehicle", "hump_75", values)
        assert record is not None


def test_a_longer_wheelbase_pitches_less_over_a_hump(client: TestClient, project: str) -> None:
    def pitch() -> float:
        runs = client.post(f"/api/projects/{project}/tests/run",
                           json={"test_id": "half_car", "target": "vehicle",
                                 "scenario_id": "hump_75"}).json()["runs"]  # fmt: skip
        return runs[0]["metrics"]["peak_pitch_angle"]["value"]

    short = pitch()
    client.post(
        f"/api/projects/{project}/commands",
        json={
            "command": {
                "changes": [
                    {"parameter": "wheelbase", "operation": "increase", "value": 400, "unit": "mm"}
                ]
            }
        },
    )
    assert pitch() < short


def test_instruction_runs_the_half_car(client: TestClient, project: str) -> None:
    reply = client.post(f"/api/projects/{project}/instructions",
                        json={"text": "test the pitch over the hump"}).json()  # fmt: skip
    assert reply["kind"] == "test"
    run = reply["runs"][0]
    assert run["test_id"] == "half_car" and run["scenario_id"] == "hump_75"
    record = client.get(f"/api/projects/{project}/runs/{run['id']}").json()
    assert {c["id"] for c in record["criteria"]} >= {"front_bump_travel", "rear_tyre_contact"}
