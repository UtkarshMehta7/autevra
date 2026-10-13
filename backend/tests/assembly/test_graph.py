import numpy as np
import pytest

from autevra.assembly import graph
from autevra.assembly import transforms as tf
from autevra.assembly.vehicle import BY_ID, COMPONENTS, DeclaredView, UndeclaredDependencyError
from autevra.domain import derived as d
from autevra.domain.parameters import REGISTRY, default_values


def _position(world: dict, cid: str) -> tuple[float, float, float]:
    return tuple(round(float(v), 6) for v in world[cid][:3, 3])


def test_wheels_placed_by_mates_at_hubs() -> None:
    p = default_values()
    world = graph.place_all(p)
    z = d.tyre_radius(p)
    assert _position(world, "wheel_fl") == pytest.approx((0, 780, z))
    assert _position(world, "wheel_fr") == pytest.approx((0, -780, z))
    assert _position(world, "wheel_rl") == pytest.approx((-2700, 780, z))
    assert _position(world, "wheel_rr") == pytest.approx((-2700, -780, z))
    assert _position(world, "rear_axle") == pytest.approx((-2700, 0, z))


def test_right_wheels_face_outwards() -> None:
    world = graph.place_all(default_values())
    outboard = np.array([0, 1, 0, 0])  # wheel local +Y is its outer face
    assert (world["wheel_fl"] @ outboard)[1] == pytest.approx(1)
    assert (world["wheel_fr"] @ outboard)[1] == pytest.approx(-1)


def test_wheelbase_moves_only_the_rear_axle_group() -> None:
    p = default_values()
    before = graph.place_all(p)
    after = graph.place_all(p | {"wheelbase": 2800})
    moved = {c for c in before if not np.allclose(before[c], after[c])}
    assert moved == {"rear_axle", "wheel_rl", "wheel_rr"}
    delta = after["wheel_rl"][:3, 3] - before["wheel_rl"][:3, 3]
    assert delta == pytest.approx([-100, 0, 0])


def test_impact_of_wheelbase() -> None:
    impact = graph.impact(["wheelbase"])
    assert impact.rebuild == {"body", "frame"}
    assert impact.move == {"rear_axle", "wheel_rl", "wheel_rr"}


def test_impact_of_rim_rebuilds_wheels_and_body_and_moves_axles() -> None:
    impact = graph.impact(["rim_diameter"])
    assert impact.rebuild == {"body", "wheel_fl", "wheel_fr", "wheel_rl", "wheel_rr"}
    assert {"front_axle", "rear_axle"} <= impact.move


def test_impact_of_front_track() -> None:
    impact = graph.impact(["track_front"])
    assert impact.rebuild == {"body", "front_axle"}
    assert impact.move == {"wheel_fl", "wheel_fr"}


def test_frame_spacing_touches_only_the_frame() -> None:
    assert graph.impact(["rail_spacing"]).affected == {"frame"}


def test_every_parameter_affects_some_component() -> None:
    unused = [pid for pid in REGISTRY if not graph.impact([pid]).affected]
    # Steering lock is used by the Phase 4 steering sweep, not by Phase 1 geometry.
    assert unused == ["max_steer_angle"]


def test_declared_dependencies_are_complete() -> None:
    # Resolving inputs and interfaces through DeclaredView raises on any undeclared read.
    p = default_values()
    for c in COMPONENTS:
        c.resolve_inputs(p)
        c.resolve_interfaces(p)


def test_declared_view_rejects_undeclared_reads() -> None:
    view = DeclaredView(default_values(), ("wheelbase",), "test")
    assert view["wheelbase"] == 2700
    with pytest.raises(UndeclaredDependencyError):
        view["body_width"]


def test_mates_reference_existing_interfaces() -> None:
    p = default_values()
    for c in COMPONENTS:
        assert set(c.frames) == set(c.resolve_interfaces(p)), c.id
        if c.mate:
            assert c.mate.parent_interface in BY_ID[c.mate.parent].resolve_interfaces(p)
            assert c.mate.child_interface in c.resolve_interfaces(p)


def test_inverse_round_trip() -> None:
    m = tf.compose(tf.translation(10, -20, 30), tf.rotation_z(33))
    assert tf.compose(m, tf.inverse(m)) == pytest.approx(np.eye(4))
