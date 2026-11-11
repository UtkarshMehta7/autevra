"""Structures workspace API: mesh a part, apply supports and loads, solve K u = F, and
return the results with the numbers behind them (matrix size and sparsity, solver
convergence, equilibrium). Educational solver; see ``autevra.fea.solver``."""

from typing import Annotated, Literal

import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from autevra.api import access
from autevra.api.routes import WorkspaceDep
from autevra.cad import kernel as k
from autevra.fea import mesh as fm
from autevra.fea import simp
from autevra.fea import solver as fs

# Project paths are guarded like the rest of the API (a visitor's own projects only).
router = APIRouter(tags=["structures"], dependencies=[Depends(access.guard_project)])


def _demo(name: str) -> k.Shape:
    if name == "cantilever":
        return k.box((0, 200), (0, 20), (0, 20))
    if name == "bracket":  # an L-bracket with a bolt hole in its foot
        foot = k.box((0, 80), (0, 40), (0, 10))
        wall = k.box((0, 10), (0, 40), (0, 70))
        body = k.fuse(foot, wall)
        return k.cut(body, k.cylinder_z(6, (-1, 11), x=50, y=20))
    if name == "plate-hole":  # tension plate with a central hole (stress concentration)
        return k.cut(k.box((0, 120), (0, 40), (0, 4)), k.cylinder_z(8, (-1, 5), x=60, y=20))
    raise HTTPException(status_code=422, detail=f"unknown demo geometry '{name}'")


DEMOS = {
    "cantilever": "Cantilever beam 200 x 20 x 20 mm",
    "bracket": "L-bracket with a bolt hole",
    "plate-hole": "Plate with a hole in tension (stress concentration)",
}


class MaterialIn(BaseModel):
    name: str = "Structural steel"
    youngs: Annotated[float, Field(gt=0, le=1e7)] | None = None
    poisson: Annotated[float, Field(ge=0, lt=0.5)] | None = None
    density: Annotated[float, Field(gt=0, le=1e5)] | None = None
    yield_strength: Annotated[float, Field(gt=0, le=1e5)] | None = None

    def material(self) -> fs.Material:
        base = fs.MATERIALS.get(self.name, fs.MATERIALS["Structural steel"])
        return fs.Material(
            self.name, self.youngs or base.youngs,
            base.poisson if self.poisson is None else self.poisson,
            self.density or base.density, self.yield_strength or base.yield_strength,
        )  # fmt: skip


# a side of the bounding box, or one of the part's own faces (``face:<index>``)
Region = Annotated[str, Field(pattern=r"^([xyz]-(min|max)|face:\d{1,5})$")]


class LoadIn(BaseModel):
    region: Region
    force: tuple[float, float, float] = (0.0, 0.0, 0.0)
    pressure: float = 0.0


class RunIn(BaseModel):
    demo: str = "cantilever"  # the demo geometry (ignored for a project part)
    element: Literal["tet4", "tet10", "hex8"] = "tet10"
    size: Annotated[float, Field(gt=0.2, le=500)] = 5.0
    material: MaterialIn = MaterialIn()
    supports: list[Region] = Field(default_factory=lambda: ["x-min"])
    loads: list[LoadIn] = Field(
        default_factory=lambda: [LoadIn(region="x-max", force=(0, 0, -1000))]
    )


@router.get("/structures/catalogue")
def catalogue() -> dict:
    return {
        "demos": DEMOS,
        "materials": {n: m.__dict__ for n, m in fs.MATERIALS.items()},
        "regions": list(fs.REGIONS),
    }


def _r(a: np.ndarray, digits: int = 5) -> list:
    return np.round(a, digits).tolist()


@router.post("/structures/run")
def run_demo(body: RunIn) -> dict:
    """Analyse a demo geometry (cantilever, bracket, plate with a hole)."""
    return _analyse(_demo(body.demo), body)


@router.post("/projects/{project_id}/parts/{part_id}/structures")
def run_part(project_id: str, part_id: str, body: RunIn, ws: WorkspaceDep) -> dict:
    """Analyse a Part Design part (in its own frame)."""
    return _analyse(_part_shape(project_id, part_id, ws), body)


@router.post("/structures/mesh")
def mesh_demo(body: RunIn) -> dict:
    """Mesh a demo geometry without solving (to pick faces for supports and loads)."""
    return _mesh_only(_demo(body.demo), body)


@router.post("/projects/{project_id}/parts/{part_id}/structures/mesh")
def mesh_part(project_id: str, part_id: str, body: RunIn, ws: WorkspaceDep) -> dict:
    return _mesh_only(_part_shape(project_id, part_id, ws), body)


def _part_shape(project_id: str, part_id: str, ws: WorkspaceDep) -> k.Shape:
    from autevra.api import model_service

    doc = dict(ws._part_docs(project_id)).get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="no such part")
    _, report = model_service.build_part(doc, ws.cache)
    if report.shape is None:
        raise HTTPException(status_code=422, detail="the part has no solid to analyse")
    return report.shape


def _mesh(shape: k.Shape, body: RunIn) -> fm.Mesh:
    if body.element == "hex8":
        return fm.hex_mesh(shape, body.size)
    mesh = fm.tet_mesh(shape, body.size)
    return fm.to_tet10(mesh) if body.element == "tet10" else mesh


def _mesh_only(shape: k.Shape, body: RunIn) -> dict:
    try:
        mesh = _mesh(shape, body)
    except fm.MeshError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    return {"mesh": {
        "kind": mesh.kind, "nodes": _r(mesh.nodes, 3), "boundary": mesh.boundary.tolist(),
        "boundary_face": [] if mesh.boundary_face is None else mesh.boundary_face.tolist(),
        "faces": mesh.faces, "stats": mesh.stats, "cad_volume": mesh.cad_volume,
    }}  # fmt: skip


def _analyse(shape: k.Shape, body: RunIn) -> dict:
    """Mesh, assemble, solve and post-process; every number in the reply is computed."""
    try:
        mesh = _mesh(shape, body)
        material = body.material.material()
        loads = [fs.Load(load.region, load.force, load.pressure) for load in body.loads]
        result = fs.solve(mesh, material, list(body.supports), loads)
    except (fm.MeshError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    disp_mag = np.linalg.norm(result.displacement, axis=1)
    supported = np.unique(np.concatenate([fs.region_nodes(mesh, r) for r in body.supports]))
    loaded = {load.region: fs.region_nodes(mesh, load.region).tolist() for load in body.loads}
    nodal_principal = np.zeros(len(mesh.nodes))
    weight = np.zeros(len(mesh.nodes))
    per = mesh.elements.shape[1]
    np.add.at(nodal_principal, mesh.elements.ravel(), np.repeat(result.principal[:, 0], per))
    np.add.at(weight, mesh.elements.ravel(), per * 0 + 1.0)
    nodal_principal /= np.maximum(weight, 1)
    nodal_strain = np.zeros(len(mesh.nodes))
    np.add.at(nodal_strain, mesh.elements.ravel(), np.repeat(result.strain_eq, per))
    nodal_strain /= np.maximum(weight, 1)
    m = material
    return {
        "mesh": {
            "kind": mesh.kind, "nodes": _r(mesh.nodes, 3), "boundary": mesh.boundary.tolist(),
            "boundary_face": [] if mesh.boundary_face is None else mesh.boundary_face.tolist(),
            "faces": mesh.faces,
            "stats": mesh.stats, "cad_volume": mesh.cad_volume,
            "elements_preview": mesh.elements[: min(len(mesh.elements), 4000)].tolist(),
        },
        "fields": {
            "displacement": _r(result.displacement, 6), "magnitude": _r(disp_mag, 6),
            "von_mises": _r(result.nodal_vm, 4), "principal_1": _r(nodal_principal, 4),
            "strain_eq": _r(nodal_strain, 8),
        },
        "supports": supported.tolist(),
        "loaded": loaded,
        "material": m.__dict__,
        "stats": result.stats,
        "assumptions": [
            "Linear elastic, isotropic, small strain, static (no contact, plasticity, "
            "buckling or dynamics).",
            "TET4: constant-strain tetrahedra, stiff in bending (refine the mesh); TET10: "
            "quadratic tetrahedra (linear strain, straight sides), accurate in bending; "
            "HEX8: trilinear voxels with full 2x2x2 integration (slight shear locking), "
            "stair-stepped boundaries.",
            "Stresses are element values averaged to the nodes for display; peaks depend on "
            "the mesh.",
            "Supports fix every degree of freedom of the nodes on a bounding-box face; loads are "
            "spread over that face by area.",
            "An educational solver checked against closed-form answers (bar, cantilever); not a "
            "substitute for a validated FEA code (CalculiX, Abaqus, ANSYS) on real designs.",
        ],
    }  # fmt: skip


# --- Topology optimisation (SIMP) ---


class TopologyIn(BaseModel):
    case: Literal["mbb", "cantilever", "bridge", "bracket"] = "mbb"
    nx: Annotated[int, Field(ge=4, le=200)] = 60
    ny: Annotated[int, Field(ge=2, le=100)] = 20
    nz: Annotated[int, Field(ge=0, le=40)] = 0  # 0: a 2D (plane stress) problem
    volfrac: Annotated[float, Field(gt=0.05, lt=0.95)] = 0.5
    penal: Annotated[float, Field(ge=1.0, le=5.0)] = 3.0
    rmin: Annotated[float, Field(ge=1.0, le=6.0)] = 1.5
    max_iter: Annotated[int, Field(ge=1, le=300)] = 120


@router.get("/structures/topology/catalogue")
def topology_catalogue() -> dict:
    return {"cases": simp.PRESETS}


@router.post("/structures/topology")
def topology(body: TopologyIn) -> dict:
    """Minimum-compliance topology by SIMP on a grid domain; returns the density history."""
    shape = (body.nx, body.ny) if body.nz == 0 else (body.nx, body.ny, body.nz)
    try:
        problem = simp.preset(body.case, shape)
        result = simp.optimise(problem, body.volfrac, body.penal, body.rmin, body.max_iter,
                               snapshot_every=max(1, body.max_iter // 40))  # fmt: skip
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    return {
        "shape": list(shape),
        "description": problem.description,
        "density": _r(result.density, 3),
        "snapshots": [_r(s, 2) for s in result.snapshots],
        "snapshot_iters": result.snapshot_iters,
        "history": result.history,
        "stats": result.stats,
        "equations": [
            "E(x_e) = E_min + x_e^p (E_0 - E_min)",
            "min c(x) = F^T u = sum_e E(x_e) u_e^T k_0 u_e",
            "s.t. K(x) u = F,  sum_e x_e = f N,  x_min <= x_e <= 1",
            "dc/dx_e = -p x_e^(p-1) (E_0 - E_min) u_e^T k_0 u_e",
            "filter: dc_e <- sum_f H_ef x_f dc_f / (x_e sum_f H_ef),  H_ef = max(0, r_min - d_ef)",
            "OC: x_e <- clamp(x_e sqrt(-dc_e / lambda), x_e - m, x_e + m), lambda by bisection",
        ],
    }
