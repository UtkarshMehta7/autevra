import pytest

from autevra.cad import kernel as k
from autevra.domains.automotive import suspension as s

pytestmark = pytest.mark.cad


@pytest.mark.parametrize(("axle", "index"), [(a, i) for a in (0, 1) for i in range(4)])
def test_every_type_builds_one_linkage_per_side(axle: int, index: int) -> None:
    p = {"track": 1560.0, "suspension": float(index), "axle": float(axle), "rail_spacing": 800.0}
    shape = s.build_suspension(p)
    rigid = s.kind(p) in ("beam", "twist_beam")  # one piece across the car
    assert k.is_valid(shape) and k.solid_count(shape) == (1 if rigid else 2)
    (_, y0, _), (_, y1, _) = k.bounds(shape)
    assert y1 <= 1560 / 2 and y0 >= -1560 / 2  # inside the wheel centre planes


def test_independent_types_have_more_links_than_a_strut() -> None:
    base = {"track": 1560.0, "axle": 0.0, "rail_spacing": 800.0}
    faces = {
        i: len(s.build_suspension(base | {"suspension": float(i)}).Faces()) for i in range(1, 4)
    }
    assert faces[1] < faces[2] and faces[1] < faces[3]  # MacPherson is the simplest linkage
