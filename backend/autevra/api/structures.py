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


Region = Literal["x-min", "x-max", "y-min", "y-max", "z-min", "z-max"]


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
    from autevra.api import model_service

    doc = dict(ws._part_docs(project_id)).get(part_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="no such part")
    _, report = model_service.build_part(doc, ws.cache)
    if report.shape is None:
        raise HTTPException(status_code=422, detail="the part has no solid to analyse")
    return _analyse(report.shape, body)


def _analyse(shape: k.Shape, body: RunIn) -> dict:
    """Mesh, assemble, solve and post-process; every number in the reply is computed."""
    try:
        if body.element == "hex8":
            mesh = fm.hex_mesh(shape, body.size)
        else:
            mesh = fm.tet_mesh(shape, body.size)
            if body.element == "tet10":
                mesh = fm.to_tet10(mesh)
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
