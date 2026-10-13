"""The vehicle assembly: component definitions, interfaces, mates and coincidences.

Each component declares the parameters its geometry depends on (``geometry``)
and, per interface, the parameters that interface frame depends on (``frames``). Input and
interface functions receive a view of the design that contains **only** the
declared parameters, so an undeclared dependency fails loudly instead of
silently breaking selective rebuilds.
"""

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field

from autevra.assembly import transforms as tf
from autevra.assembly.transforms import Matrix
from autevra.domain import derived as d

Values = Mapping[str, float]

TYRE = ("rim_diameter", "tyre_width", "tyre_aspect_ratio")


class UndeclaredDependencyError(KeyError):
    pass


class DeclaredView(Mapping[str, float]):
    """Read-only view of a parameter set restricted to declared keys."""

    def __init__(self, values: Values, allowed: tuple[str, ...], owner: str) -> None:
        self._values, self._allowed, self._owner = values, frozenset(allowed), owner

    def __getitem__(self, key: str) -> float:
        if key not in self._allowed:
            raise UndeclaredDependencyError(f"{self._owner} reads undeclared parameter '{key}'")
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(k for k in self._values if k in self._allowed)

    def __len__(self) -> int:
        return sum(1 for _ in self)


@dataclass(frozen=True)
class Mate:
    """Places a child so its ``child_interface`` coincides with the parent's interface."""

    parent: str
    parent_interface: str
    child_interface: str


@dataclass(frozen=True)
class ComponentDef:
    id: str
    name: str
    category: str
    builder: str | None  # None for components without geometry (the vehicle root)
    geometry: tuple[str, ...] = ()
    inputs: Callable[[Values], dict[str, float]] = lambda p: {}
    frames: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    interfaces: Callable[[Values], dict[str, Matrix]] = lambda p: {}
    mate: Mate | None = None
    color: tuple[float, float, float] = (0.6, 0.6, 0.6)

    def resolve_inputs(self, values: Values) -> dict[str, float]:
        return self.inputs(DeclaredView(values, self.geometry, self.id))

    def resolve_interfaces(self, values: Values) -> dict[str, Matrix]:
        allowed = tuple({p for deps in self.frames.values() for p in deps})
        return self.interfaces(DeclaredView(values, allowed, self.id))


BODY_GEOMETRY = (
    "wheelbase", "front_overhang", "rear_overhang", "body_width", "overall_height",
    "beltline_height", "ground_clearance", "rail_height", "cabin_length", "roof_length",
    "cabin_offset", "track_front", "track_rear", "arch_clearance", *TYRE,
)  # fmt: skip


def _body_inputs(p: Values) -> dict[str, float]:
    keys = [k for k in BODY_GEOMETRY if k not in TYRE]
    return {k: p[k] for k in keys} | {
        "body_floor": d.body_floor_height(p),
        "tyre_width": p["tyre_width"],
        "tyre_radius": d.tyre_radius(p),
        "arch_radius": d.arch_radius(p),
    }


FRAME_GEOMETRY = (
    "wheelbase", "front_overhang", "rear_overhang", "rail_spacing", "rail_width",
    "rail_height", "rail_wall", "ground_clearance",
)  # fmt: skip


def _wheel_inputs(p: Values) -> dict[str, float]:
    return {
        "tyre_radius": d.tyre_radius(p),
        "rim_radius": d.rim_diameter_mm(p) / 2.0,
        "tyre_width": p["tyre_width"],
    }


def _vehicle_interfaces(p: Values) -> dict[str, Matrix]:
    z = d.tyre_radius(p)  # wheel centre height (unloaded tyre)
    return {
        "origin": tf.identity(),
        "front_axle_mount": tf.translation(0.0, 0.0, z),
        "rear_axle_mount": tf.translation(-p["wheelbase"], 0.0, z),
    }


def _axle_interfaces(track_param: str) -> Callable[[Values], dict[str, Matrix]]:
    def interfaces(p: Values) -> dict[str, Matrix]:
        half = p[track_param] / 2.0
        shock_y = p["rail_spacing"] / 2.0  # dampers stand over the frame rail lines
        return {
            "centre": tf.identity(),
            "hub_left": tf.translation(0.0, half, 0.0),
            # Right hub faces outward along -Y: the wheel is turned 180 degrees about Z.
            "hub_right": tf.compose(tf.translation(0.0, -half, 0.0), tf.rotation_z(180.0)),
            "shock_left": tf.translation(0.0, shock_y, d.AXLE_RADIUS),
            "shock_right": tf.translation(0.0, -shock_y, d.AXLE_RADIUS),
        }

    return interfaces


SHOCK_TOWERS = {  # body interface -> (axle, side)
    "shock_tower_fl": ("front", 1.0),
    "shock_tower_fr": ("front", -1.0),
    "shock_tower_rl": ("rear", 1.0),
    "shock_tower_rr": ("rear", -1.0),
}


def _body_interfaces(p: Values) -> dict[str, Matrix]:
    """Origin plus the upper damper mounts (shock towers) built into the body."""
    out = {"origin": tf.identity()}
    for name, (axle, side) in SHOCK_TOWERS.items():
        x = 0.0 if axle == "front" else -p["wheelbase"]
        out[name] = tf.translation(
            x, side * p["rail_spacing"] / 2.0, p[f"{axle}_shock_mount_height"]
        )
    return out


def _damper_geometry(axle: str) -> tuple[str, ...]:
    return (
        f"{axle}_shock_mount_height", *TYRE, f"{axle}_damper_stroke", "damper_body_diameter",
        "spring_coil_diameter", f"{axle}_spring_rate",
    )  # fmt: skip


def _damper_inputs(axle: str) -> Callable[[Values], dict[str, float]]:
    def inputs(p: Values) -> dict[str, float]:
        return {
            "length": d.damper_installed_length(p, axle),
            "stroke": p[f"{axle}_damper_stroke"],
            "body_diameter": p["damper_body_diameter"],
            "coil_diameter": p["spring_coil_diameter"],
            "wire_diameter": round(d.spring_wire_diameter(p, axle), 3),
        }

    return inputs


def _damper_interfaces(axle: str) -> Callable[[Values], dict[str, Matrix]]:
    def interfaces(p: Values) -> dict[str, Matrix]:
        return {
            "lower_eye": tf.identity(),
            "upper_eye": tf.translation(0.0, 0.0, d.damper_installed_length(p, axle)),
        }

    return interfaces


def _hub(p: Values) -> dict[str, Matrix]:
    return {"hub": tf.identity()}


_BODY_COLOR = (0.62, 0.70, 0.80)
_FRAME_COLOR = (0.30, 0.32, 0.36)
_AXLE_COLOR = (0.45, 0.45, 0.48)
_WHEEL_COLOR = (0.12, 0.12, 0.13)
_DAMPER_COLOR = (0.85, 0.55, 0.12)


@dataclass(frozen=True)
class Coincidence:
    """Two interfaces that must coincide in world space (a closed loop the mates do not set).

    The dampers are placed by their lower eye; their upper eye must meet the body's shock
    tower. ``integration.check`` verifies it for every design.
    """

    a: tuple[str, str]  # (component, interface)
    b: tuple[str, str]
    tolerance: float = 0.01  # mm


def _wheel(cid: str, name: str, axle: str, side: str) -> ComponentDef:
    return ComponentDef(
        id=cid, name=name, category="wheel", builder="wheel",
        geometry=TYRE, inputs=_wheel_inputs,
        frames={"hub": ()}, interfaces=_hub,
        mate=Mate(axle, f"hub_{side}", "hub"), color=_WHEEL_COLOR,
    )  # fmt: skip


def _damper(cid: str, name: str, axle: str, side: str) -> ComponentDef:
    upper = (f"{axle}_shock_mount_height", *TYRE)
    return ComponentDef(
        id=cid, name=name, category="suspension", builder="damper",
        geometry=_damper_geometry(axle), inputs=_damper_inputs(axle),
        frames={"lower_eye": (), "upper_eye": upper}, interfaces=_damper_interfaces(axle),
        mate=Mate(f"{axle}_axle", f"shock_{side}", "lower_eye"), color=_DAMPER_COLOR,
    )  # fmt: skip


def _axle(cid: str, name: str, track: str, mount: str) -> ComponentDef:
    return ComponentDef(
        id=cid, name=name, category="axle", builder="axle",
        geometry=(track,), inputs=lambda p: {"track": p[track]},
        frames={"centre": (), "hub_left": (track,), "hub_right": (track,),
                "shock_left": ("rail_spacing",), "shock_right": ("rail_spacing",)},
        interfaces=_axle_interfaces(track),
        mate=Mate("vehicle", mount, "centre"), color=_AXLE_COLOR,
    )  # fmt: skip


COMPONENTS: list[ComponentDef] = [
    ComponentDef(
        id="vehicle", name="Vehicle", category="assembly", builder=None,
        frames={"origin": (), "front_axle_mount": TYRE,
                "rear_axle_mount": ("wheelbase", *TYRE)},
        interfaces=_vehicle_interfaces,
    ),
    ComponentDef(
        id="body", name="Body", category="body", builder="body",
        geometry=BODY_GEOMETRY, inputs=_body_inputs,
        frames={"origin": (),
                **{name: ("wheelbase", "rail_spacing", f"{axle}_shock_mount_height")
                   for name, (axle, _) in SHOCK_TOWERS.items()}},
        interfaces=_body_interfaces,
        mate=Mate("vehicle", "origin", "origin"), color=_BODY_COLOR,
    ),
    ComponentDef(
        id="frame", name="Ladder frame", category="chassis", builder="frame",
        geometry=FRAME_GEOMETRY, inputs=lambda p: {k: p[k] for k in FRAME_GEOMETRY},
        frames={"origin": ()}, interfaces=lambda p: {"origin": tf.identity()},
        mate=Mate("vehicle", "origin", "origin"), color=_FRAME_COLOR,
    ),
    _axle("front_axle", "Front axle", "track_front", "front_axle_mount"),
    _axle("rear_axle", "Rear axle", "track_rear", "rear_axle_mount"),
    _wheel("wheel_fl", "Wheel front left", "front_axle", "left"),
    _wheel("wheel_fr", "Wheel front right", "front_axle", "right"),
    _wheel("wheel_rl", "Wheel rear left", "rear_axle", "left"),
    _wheel("wheel_rr", "Wheel rear right", "rear_axle", "right"),
    _damper("damper_fl", "Damper front left", "front", "left"),
    _damper("damper_fr", "Damper front right", "front", "right"),
    _damper("damper_rl", "Damper rear left", "rear", "left"),
    _damper("damper_rr", "Damper rear right", "rear", "right"),
]  # fmt: skip

BY_ID: dict[str, ComponentDef] = {c.id: c for c in COMPONENTS}  # extensible

COINCIDENCES: list[Coincidence] = [
    Coincidence((f"damper_{tower[-2:]}", "upper_eye"), ("body", tower)) for tower in SHOCK_TOWERS
]

# Vertical load paths from the road to the body. Each consecutive pair must be joined by a
# mate or a coincidence; ``integration.check`` verifies this against the definitions above.
LOAD_PATHS: list[tuple[str, ...]] = [
    (f"wheel_{c}", f"{'front' if c[0] == 'f' else 'rear'}_axle", f"damper_{c}", "body")
    for c in ("fl", "fr", "rl", "rr")
]
