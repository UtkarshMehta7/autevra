import numpy as np
import pytest

from autevra.assembly import graph
from autevra.assembly import transforms as tf
from autevra.assembly.model import BY_ID, COMPONENTS, DeclaredView, UndeclaredDependencyError
from autevra.core.parameters import REGISTRY, default_values
from autevra.domains.automotive import derived as d


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
    assert moved == {"rear_axle", "wheel_rl", "wheel_rr", "rim_rl", "rim_rr", "damper_rl",
                     "damper_rr"}  # fmt: skip
    for cid in ("wheel_rl", "damper_rr"):
        assert after[cid][:3, 3] - before[cid][:3, 3] == pytest.approx([-100, 0, 0])


EQUIPMENT = {
    "engine", "gearbox", "fuel_tank", "exhaust", "radiator", "traction_battery", "front_motor",
    "rear_motor", "inverters", "charger", "charge_port", "hv_cables", "battery_12v", "ecus",
    "harness",
}  # fmt: skip
INTERIOR = {"seats", "dashboard", "display", "steering_wheel", "console"}
EXTERIOR = {"mirrors", "roof_rails", "spoiler", "tow_bar"}  # greenhouse options and spoiler


def test_impact_of_wheelbase() -> None:
    impact = graph.impact(["wheelbase"])
    assert (
        impact.rebuild
        == {"body", "frame", "glass", "head_lamps", "tail_lamps"} | INTERIOR | EQUIPMENT | EXTERIOR
    )
    assert impact.move == {"damper_rl", "damper_rr", "rear_axle", "wheel_rl", "wheel_rr",
                           "rim_rl", "rim_rr"}  # fmt: skip
    assert not {"wheel_fl", "front_axle"} & (impact.rebuild | impact.move)  # the front stays


def test_impact_of_rim_rebuilds_wheels_and_body_and_moves_axles() -> None:
    impact = graph.impact(["rim_diameter"])
    wheels = {f"{part}_{c}" for part in ("wheel", "rim") for c in ("fl", "fr", "rl", "rr")}
    dampers = {"damper_fl", "damper_fr", "damper_rl", "damper_rr"}
    # dampers: length between mounts; equipment: placed from the wheel-centre height
    # the spoiler sits on the body's side profile, which clears the arches
    assert (
        impact.rebuild
        == {"body", "head_lamps", "tail_lamps", "spoiler"} | wheels | dampers | EQUIPMENT
    )
    assert not INTERIOR & impact.rebuild  # the cabin does not follow the wheels
    assert {"front_axle", "rear_axle"} <= impact.move


def test_impact_of_front_track() -> None:
    impact = graph.impact(["track_front"])
    assert impact.rebuild == {"body", "head_lamps", "tail_lamps", "spoiler", "front_axle"}
    assert impact.move == {"wheel_fl", "wheel_fr", "rim_fl", "rim_fr"}


def test_frame_spacing_rebuilds_the_frame_and_moves_the_dampers() -> None:
    impact = graph.impact(["rail_spacing"])
    # Conservative: on a ladder frame the floor battery sits between the rails, so the floor
    # height (and every body-mounted part) is declared to depend on the rail spacing.
    assert {"frame", "front_axle", "rear_axle"} <= impact.rebuild  # suspension pivots follow
    assert not {"wheel_fl", "wheel_rr"} & impact.rebuild
    assert impact.move == {"damper_fl", "damper_fr", "damper_rl", "damper_rr"}


# Parameters with no geometry: suspension dynamics and mass feed the simulation model
# (tests/engineering checks that each one is a test input); steering lock is for the
# later steering sweep.
NO_GEOMETRY = {
    "max_steer_angle", "vehicle_mass", "front_mass_distribution", "tyre_vertical_stiffness",
    "peak_power", "drivetrain_efficiency", "drag_coefficient",
    "rolling_resistance", "cg_height", "pitch_dynamic_index", "paint_colour", "paint_finish",
    "interior_colour", "rim_finish",
    *(f"{a}_{n}" for a in ("front", "rear")
      for n in ("damping_bump", "damping_rebound", "unsprung_mass", "bump_travel",
                "rebound_travel")),
}  # fmt: skip


def test_every_parameter_affects_some_component() -> None:
    unused = {pid for pid in REGISTRY if not graph.impact([pid]).affected}
    assert unused == NO_GEOMETRY


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


def test_dampers_stand_on_the_axle_under_the_shock_towers() -> None:
    p = default_values()
    world = graph.place_all(p)
    lower = np.asarray(world["damper_rl"])[:3, 3]
    assert lower == pytest.approx(
        [-p["wheelbase"], p["rail_spacing"] / 2, d.lower_shock_mount_height(p)]
    )


def test_damping_changes_no_geometry_but_spring_rate_rebuilds_its_axle_dampers() -> None:
    assert graph.impact(["rear_damping_bump"]).affected == frozenset()
    assert graph.impact(["rear_spring_rate"]).rebuild == {"damper_rl", "damper_rr"}


def test_wheel_size_rebuilds_dampers_and_moves_them() -> None:
    impact = graph.impact(["rim_diameter"])
    assert {"damper_fl", "damper_fr", "damper_rl", "damper_rr"} <= impact.rebuild
