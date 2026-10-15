import time

import pytest
from fastapi.testclient import TestClient

from autevra.cad import kernel as k
from autevra.part.build import build_part
from autevra.part.presets import presets

pytestmark = pytest.mark.cad

DOMAINS = ("aerospace", "consumer product", "tooling", "plant", "machinery", "propulsion")


def test_presets_cover_several_domains() -> None:
    names = " ".join(presets()).lower()
    assert all(domain in names for domain in DOMAINS)


@pytest.mark.parametrize("name", sorted(presets()))
def test_every_preset_builds_as_one_solid_quickly(name: str) -> None:
    started = time.perf_counter()
    result = build_part(presets()[name])
    assert not result.errors, result.errors
    assert result.shape is not None and k.is_valid(result.shape)
    assert k.solid_count(result.shape) == 1
    assert time.perf_counter() - started < 5.0  # the hosted instance has 0.1 CPU


def test_presets_are_served(client: TestClient) -> None:
    body = client.get("/api/part-presets").json()
    assert set(body) == set(presets())
    assert body["Mounting bracket"]["parameters"]["width"] == 200
