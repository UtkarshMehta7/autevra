"""Feature definitions: typed, validated, JSON round-trippable (all lengths in mm, angles
in degrees, the part frame is ISO 8855 like the vehicle: X forward, Y left, Z up)."""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Length = Annotated[float, Field(gt=0.0, le=50_000.0)]
Coord = Annotated[float, Field(ge=-50_000.0, le=50_000.0)]
Point2 = tuple[Coord, Coord]
Point3 = tuple[Coord, Coord, Coord]


class Op(StrEnum):
    ADD = "add"
    CUT = "cut"
    INTERSECT = "intersect"


class Axis(StrEnum):
    X = "x"
    Y = "y"
    Z = "z"


class Plane(StrEnum):
    XY = "xy"
    XZ = "xz"
    YZ = "yz"


class Placement(BaseModel):
    """Where a feature sits: a translation, then rotations about X, Y and Z (degrees)."""

    model_config = ConfigDict(frozen=True)

    x: Coord = 0.0
    y: Coord = 0.0
    z: Coord = 0.0
    rx: float = Field(0.0, ge=-360.0, le=360.0)
    ry: float = Field(0.0, ge=-360.0, le=360.0)
    rz: float = Field(0.0, ge=-360.0, le=360.0)


Expression = Annotated[str, Field(min_length=1, max_length=200)]
BindingPath = Annotated[str, Field(pattern=r"^[a-z_]+(\.[a-z_0-9]+)*$", max_length=60)]


class _Feature(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(min_length=1, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    name: str = Field("", max_length=80)
    suppressed: bool = False  # kept in the tree, skipped in the build
    # Field path ("radius", "size.0", "at.x", "sections.1.width") -> expression of the
    # part's parameters ("width / 2 - 30"); evaluated before the build.
    bindings: dict[BindingPath, Expression] = Field(default_factory=dict, max_length=50)


class _Solid(_Feature):
    op: Op = Op.ADD
    at: Placement = Placement()


class Box(_Solid):
    """Box centred on its placement."""

    type: Literal["box"] = "box"
    size: tuple[Length, Length, Length] = (100.0, 100.0, 100.0)


class Cylinder(_Solid):
    """Cylinder centred on its placement, along an axis."""

    type: Literal["cylinder"] = "cylinder"
    radius: Length = 50.0
    height: Length = 100.0
    axis: Axis = Axis.Z


class Sphere(_Solid):
    type: Literal["sphere"] = "sphere"
    radius: Length = 50.0


class Extrude(_Solid):
    """A closed polygon sketched in a plane, extruded along the plane normal (symmetric
    about the sketch plane when ``symmetric``)."""

    type: Literal["extrude"] = "extrude"
    plane: Plane = Plane.XY
    points: list[Point2] = Field(min_length=3, max_length=500)
    depth: Length = 100.0
    symmetric: bool = False


class Revolve(_Solid):
    """A closed profile (radius, height) revolved about the Z axis of its placement."""

    type: Literal["revolve"] = "revolve"
    points: list[Point2] = Field(min_length=3, max_length=500)  # (r >= 0, z)
    angle: float = Field(360.0, gt=0.0, le=360.0)

    @model_validator(mode="after")
    def _radius_non_negative(self) -> "Revolve":
        if any(r < 0.0 for r, _ in self.points):
            raise ValueError("revolve profile radii must be zero or positive")
        return self


class Section(BaseModel):
    """A rounded rectangle at a station along the loft axis (Z of the placement)."""

    model_config = ConfigDict(frozen=True)

    z: Coord
    width: Length
    height: Length
    radius: float = Field(0.0, ge=0.0, le=25_000.0)  # corner radius (0 = sharp)


class Loft(_Solid):
    """A smooth or ruled solid through rounded-rectangle sections (fuselages, ducts,
    bottles, handles)."""

    type: Literal["loft"] = "loft"
    sections: list[Section] = Field(min_length=2, max_length=40)
    ruled: bool = False

    @model_validator(mode="after")
    def _ordered(self) -> "Loft":
        zs = [s.z for s in self.sections]
        if any(b <= a for a, b in zip(zs, zs[1:], strict=False)):
            raise ValueError("loft sections must be in increasing z")
        return self


class Sweep(_Solid):
    """A round tube swept along a polyline path with rounded corners (pipes, frames,
    handrails, cable runs)."""

    type: Literal["sweep"] = "sweep"
    path: list[Point3] = Field(min_length=2, max_length=200)
    radius: Length = 20.0
    wall: float = Field(0.0, ge=0.0)  # 0 = solid bar, otherwise a tube of this wall
    bend_radius: float = Field(0.0, ge=0.0)  # corner rounding of the path

    @model_validator(mode="after")
    def _wall_fits(self) -> "Sweep":
        if self.wall >= self.radius:
            raise ValueError("tube wall must be thinner than the radius")
        return self


class Shell(_Feature):
    """Hollow the result so far to a wall thickness (open where faces are removed: the
    faces whose outward normal points along ``open_towards``)."""

    type: Literal["shell"] = "shell"
    thickness: Length = 3.0
    open_towards: Literal["none", "+x", "-x", "+y", "-y", "+z", "-z"] = "none"


# Edge selection: CadQuery's selector grammar, e.g. "|Z" (parallel to Z), ">Z" (topmost),
# "<X" (rearmost), "#Z" (perpendicular to Z), combined with and / or / not and brackets.
EdgeSelector = Annotated[
    str,
    Field(
        max_length=80,
        pattern=r"^[<>|#%+\-XYZxyz0-9\[\]().,\s]*(?:(?:and|or|not|exc)[<>|#%+\-XYZxyz0-9\[\]().,\s]*)*$",
    ),
]


class Fillet(_Feature):
    """Round edges of the result so far: every edge, or those picked by ``edges``."""

    type: Literal["fillet"] = "fillet"
    radius: Length = 5.0
    edges: EdgeSelector = ""  # empty: every edge


class Chamfer(_Feature):
    """Bevel edges of the result so far by ``size`` (equal legs): every edge, or those
    picked by ``edges``."""

    type: Literal["chamfer"] = "chamfer"
    size: Length = 2.0
    edges: EdgeSelector = ""


class Mirror(_Feature):
    """Add the mirror image of the result so far across a plane through the origin."""

    type: Literal["mirror"] = "mirror"
    plane: Plane = Plane.XZ


class LinearPattern(_Feature):
    """Repeat the solid feature before it (adding or cutting like it) ``count`` times along
    a step vector, the original included."""

    type: Literal["linear_pattern"] = "linear_pattern"
    count: int = Field(2, ge=2, le=200)
    step: Point3 = (100.0, 0.0, 0.0)


class CircularPattern(_Feature):
    """Repeat the solid feature before it ``count`` times about an axis through the part
    origin, the original included."""

    type: Literal["circular_pattern"] = "circular_pattern"
    count: int = Field(6, ge=2, le=360)
    axis: Axis = Axis.Z
    angle: float = Field(360.0, gt=0.0, le=360.0)  # total angle covered


class Wing(_Solid):
    """A wing or tail surface from NACA four-digit aerofoil sections (the published
    four-digit thickness and camber equations), lofted from the root (at the placement,
    chord running aft along -X) to the tip (along +Y), with leading-edge sweep, dihedral and
    tip twist (washout, about the quarter chord). ``both_sides`` mirrors it across XZ."""

    type: Literal["wing"] = "wing"
    naca: str = Field("2412", pattern=r"^\d{4}$")
    root_chord: Length = 1600.0
    tip_chord: Length = 800.0
    span: Length = 5000.0  # root to tip (one side)
    sweep: float = Field(5.0, ge=-60.0, le=70.0)  # leading edge, degrees
    dihedral: float = Field(3.0, ge=-30.0, le=30.0)
    twist: float = Field(-2.0, ge=-15.0, le=15.0)  # tip incidence relative to the root
    both_sides: bool = True

    @model_validator(mode="after")
    def _thickness(self) -> "Wing":
        if int(self.naca[2:]) == 0:
            raise ValueError("NACA thickness (last two digits) must be above zero")
        if int(self.naca[0]) > 0 and int(self.naca[1]) == 0:
            raise ValueError("a cambered NACA section needs a camber position (second digit)")
        return self


Feature = Annotated[
    Box
    | Cylinder
    | Sphere
    | Extrude
    | Revolve
    | Loft
    | Sweep
    | Wing
    | Shell
    | Fillet
    | Chamfer
    | Mirror
    | LinearPattern
    | CircularPattern,
    Field(discriminator="type"),
]
SOLID_TYPES = ("box", "cylinder", "sphere", "extrude", "revolve", "loft", "sweep", "wing")
FEATURE_TYPES = (*SOLID_TYPES, "shell", "fillet", "chamfer", "mirror", "linear_pattern",
                 "circular_pattern")  # fmt: skip


ParamName = Annotated[str, Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]{0,39}$")]


class Variant(BaseModel):
    """One row of a design table: a named set of parameter values."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1, max_length=40)
    values: list[float] = Field(max_length=50)


class DesignTable(BaseModel):
    """Named variants of a part: columns are parameters, rows are variants. The active row
    overrides those parameters (the others keep their own values or expressions)."""

    model_config = ConfigDict(frozen=True)

    columns: list[ParamName] = Field(min_length=1, max_length=50)
    rows: list[Variant] = Field(default_factory=list, max_length=500)
    active: str | None = None

    @model_validator(mode="after")
    def _consistent(self) -> "DesignTable":
        if len(set(self.columns)) != len(self.columns):
            raise ValueError("design table columns must be unique")
        names = [r.name for r in self.rows]
        if len(set(names)) != len(names):
            raise ValueError("design table row names must be unique")
        for row in self.rows:
            if len(row.values) != len(self.columns):
                raise ValueError(f"row '{row.name}' needs {len(self.columns)} values")
        if self.active is not None and self.active not in names:
            raise ValueError(f"the active row '{self.active}' is not in the table")
        return self

    def active_values(self) -> dict[str, float]:
        row = next((r for r in self.rows if r.name == self.active), None)
        return dict(zip(self.columns, row.values, strict=True)) if row else {}


class PartDoc(BaseModel):
    """A user-authored part: its feature tree, its appearance and where it sits in the
    project (vehicle) frame."""

    model_config = ConfigDict(frozen=True)

    name: str = Field("Part", min_length=1, max_length=80)
    # Named parameters: numbers, or expressions of the parameters before them.
    parameters: dict[ParamName, float | Expression] = Field(default_factory=dict, max_length=100)
    design_table: DesignTable | None = None
    features: list[Feature] = Field(default_factory=list, max_length=200)
    at: Placement = Placement()
    color: tuple[float, float, float] = (0.62, 0.66, 0.72)
    finish: str = Field("metal", max_length=30)

    @model_validator(mode="after")
    def _unique_ids(self) -> "PartDoc":
        ids = [f.id for f in self.features]
        if len(ids) != len(set(ids)):
            raise ValueError("feature ids must be unique within a part")
        if self.design_table is not None:
            missing = [c for c in self.design_table.columns if c not in self.parameters]
            if missing:
                raise ValueError(f"design table columns are not parameters: {missing}")
        return self

    def effective_parameters(self) -> dict[str, float | str]:
        """Parameters with the active design-table row applied."""
        table = self.design_table.active_values() if self.design_table else {}
        return {name: table.get(name, value) for name, value in self.parameters.items()}
