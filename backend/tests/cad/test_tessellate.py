import pytest

from autevra.cad import kernel as k

pytestmark = pytest.mark.cad


@pytest.mark.parametrize(
    "shape",
    [
        k.box((0, 10), (0, 20), (0, 30)),
        k.cylinder_y(50, (-20, 20)),
        k.cut(k.box((0, 100), (0, 100), (0, 100)), k.cylinder_y(30, (-1, 101), x=50, z=50)),
    ],
    ids=["box", "cylinder", "box-with-hole"],
)
def test_tessellate_matches_cadquery(shape: k.Shape) -> None:
    mesh = k.tessellate(shape)
    vertices, triangles = shape.tessellate(0.5, 0.3)
    assert mesh.indices == [i for t in triangles for i in t]
    assert mesh.vertices == pytest.approx([c for v in vertices for c in (v.x, v.y, v.z)])
