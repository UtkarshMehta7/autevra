# GSD — Generative Shape Design

**CATIA-class equivalent:** Generative Shape Design (GSD) / wireframe and surfaces  
**Autevra workspace:** Surfaces; Styling  
**Scope:** Shared  
**Cases:** 156 (Have 45, Partial 111, Gap 0)

Wireframe and surface operations, joins, healing and continuity checks.

[← Back to the index](../README.md)

## Features

- Surface creation — 60 cases (Partial)
- Join and healing — 25 cases (Have)
- Wireframe — 51 cases (Partial)
- Connect checker — 20 cases (Have)

## Surface creation

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| GSD-0001 | Extrude circle r=5 by 10 | Accuracy | P2 | Extrude a circle into an open surface. | Area = 2πrh = 314.159 mm². |  |
| GSD-0002 | Revolve line (r=5, h=10) 360° | Accuracy | P2 | Revolve a line parallel to Z about Z. | Cylindrical surface; area 314.159 mm²; single periodic face. |  |
| GSD-0003 | Extrude circle r=10 by 50 | Accuracy | P2 | Extrude a circle into an open surface. | Area = 2πrh = 3141.59 mm². |  |
| GSD-0004 | Revolve line (r=10, h=50) 360° | Accuracy | P2 | Revolve a line parallel to Z about Z. | Cylindrical surface; area 3141.59 mm²; single periodic face. |  |
| GSD-0005 | Extrude circle r=25 by 100 | Accuracy | P2 | Extrude a circle into an open surface. | Area = 2πrh = 15708 mm². |  |
| GSD-0006 | Revolve line (r=25, h=100) 360° | Accuracy | P2 | Revolve a line parallel to Z about Z. | Cylindrical surface; area 15708 mm²; single periodic face. |  |
| GSD-0007 | Extrude circle r=100 by 1 | Accuracy | P2 | Extrude a circle into an open surface. | Area = 2πrh = 628.319 mm². |  |
| GSD-0008 | Revolve line (r=100, h=1) 360° | Accuracy | P2 | Revolve a line parallel to Z about Z. | Cylindrical surface; area 628.319 mm²; single periodic face. |  |
| GSD-0009 | Sphere surface r=1 | Accuracy | P2 | Revolve a semicircle 360°. | Area 4πr² = 12.5664 mm². |  |
| GSD-0010 | Sphere surface r=10 | Accuracy | P2 | Revolve a semicircle 360°. | Area 4πr² = 1256.64 mm². |  |
| GSD-0011 | Sphere surface r=50 | Accuracy | P2 | Revolve a semicircle 360°. | Area 4πr² = 31415.9 mm². |  |
| GSD-0012 | Sphere surface r=500 | Accuracy | P2 | Revolve a semicircle 360°. | Area 4πr² = 3141593 mm². |  |
| GSD-0013 | sweep (explicit profile) with G0 to supports | Functional | P2 | Build sweep (explicit profile); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0014 | sweep (explicit profile) with G1 to supports | Functional | P2 | Build sweep (explicit profile); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0015 | sweep (explicit profile) with G2 to supports | Functional | P1 | Build sweep (explicit profile); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0016 | sweep (line, two guides) with G0 to supports | Functional | P2 | Build sweep (line, two guides); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0017 | sweep (line, two guides) with G1 to supports | Functional | P2 | Build sweep (line, two guides); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0018 | sweep (line, two guides) with G2 to supports | Functional | P1 | Build sweep (line, two guides); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0019 | sweep (circle, three guides) with G0 to supports | Functional | P2 | Build sweep (circle, three guides); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0020 | sweep (circle, three guides) with G1 to supports | Functional | P2 | Build sweep (circle, three guides); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0021 | sweep (circle, three guides) with G2 to supports | Functional | P1 | Build sweep (circle, three guides); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0022 | sweep (conic) with G0 to supports | Functional | P2 | Build sweep (conic); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0023 | sweep (conic) with G1 to supports | Functional | P2 | Build sweep (conic); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0024 | sweep (conic) with G2 to supports | Functional | P1 | Build sweep (conic); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0025 | fill (3 boundaries) with G0 to supports | Functional | P2 | Build fill (3 boundaries); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0026 | fill (3 boundaries) with G1 to supports | Functional | P2 | Build fill (3 boundaries); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0027 | fill (3 boundaries) with G2 to supports | Functional | P1 | Build fill (3 boundaries); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0028 | fill (4 boundaries) with G0 to supports | Functional | P2 | Build fill (4 boundaries); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0029 | fill (4 boundaries) with G1 to supports | Functional | P2 | Build fill (4 boundaries); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0030 | fill (4 boundaries) with G2 to supports | Functional | P1 | Build fill (4 boundaries); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0031 | fill (5 boundaries) with G0 to supports | Functional | P2 | Build fill (5 boundaries); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0032 | fill (5 boundaries) with G1 to supports | Functional | P2 | Build fill (5 boundaries); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0033 | fill (5 boundaries) with G2 to supports | Functional | P1 | Build fill (5 boundaries); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0034 | fill (6 boundaries) with G0 to supports | Functional | P2 | Build fill (6 boundaries); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0035 | fill (6 boundaries) with G1 to supports | Functional | P2 | Build fill (6 boundaries); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0036 | fill (6 boundaries) with G2 to supports | Functional | P1 | Build fill (6 boundaries); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0037 | multi-section surface with G0 to supports | Functional | P2 | Build multi-section surface; set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0038 | multi-section surface with G1 to supports | Functional | P2 | Build multi-section surface; set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0039 | multi-section surface with G2 to supports | Functional | P1 | Build multi-section surface; set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0040 | blend between two edges with G0 to supports | Functional | P2 | Build blend between two edges; set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0041 | blend between two edges with G1 to supports | Functional | P2 | Build blend between two edges; set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0042 | blend between two edges with G2 to supports | Functional | P1 | Build blend between two edges; set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0043 | offset 2 mm with G0 to supports | Functional | P2 | Build offset 2 mm; set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0044 | offset 2 mm with G1 to supports | Functional | P2 | Build offset 2 mm; set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0045 | offset 2 mm with G2 to supports | Functional | P1 | Build offset 2 mm; set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0046 | offset -2 mm with G0 to supports | Functional | P2 | Build offset -2 mm; set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0047 | offset -2 mm with G1 to supports | Functional | P2 | Build offset -2 mm; set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0048 | offset -2 mm with G2 to supports | Functional | P1 | Build offset -2 mm; set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0049 | variable offset with G0 to supports | Functional | P2 | Build variable offset; set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0050 | variable offset with G1 to supports | Functional | P2 | Build variable offset; set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0051 | variable offset with G2 to supports | Functional | P1 | Build variable offset; set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0052 | extrapolate 10 mm (tangent) with G0 to supports | Functional | P2 | Build extrapolate 10 mm (tangent); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0053 | extrapolate 10 mm (tangent) with G1 to supports | Functional | P2 | Build extrapolate 10 mm (tangent); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0054 | extrapolate 10 mm (tangent) with G2 to supports | Functional | P1 | Build extrapolate 10 mm (tangent); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0055 | extrapolate 10 mm (curvature) with G0 to supports | Functional | P2 | Build extrapolate 10 mm (curvature); set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0056 | extrapolate 10 mm (curvature) with G1 to supports | Functional | P2 | Build extrapolate 10 mm (curvature); set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0057 | extrapolate 10 mm (curvature) with G2 to supports | Functional | P1 | Build extrapolate 10 mm (curvature); set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0058 | ruled surface with G0 to supports | Functional | P2 | Build ruled surface; set boundary continuity G0. | Surface built; connect check meets G0 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0059 | ruled surface with G1 to supports | Functional | P2 | Build ruled surface; set boundary continuity G1. | Surface built; connect check meets G1 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |
| GSD-0060 | ruled surface with G2 to supports | Functional | P1 | Build ruled surface; set boundary continuity G2. | Surface built; connect check meets G2 thresholds (G0 ≤ 0.001 mm, G1 ≤ 0.1°, G2 ≤ 5% curvature). |  |

## Join and healing

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| GSD-0061 | Join two patches, gap 0.0005 mm, tolerance 0.001 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.0005, tol=0.001 |
| GSD-0062 | Join two patches, gap 0.0005 mm, tolerance 0.01 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.0005, tol=0.01 |
| GSD-0063 | Join two patches, gap 0.0005 mm, tolerance 0.1 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.0005, tol=0.1 |
| GSD-0064 | Join two patches, gap 0.005 mm, tolerance 0.001 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.005 > tolerance 0.001; offending edge highlighted. | gap=0.005, tol=0.001 |
| GSD-0065 | Join two patches, gap 0.005 mm, tolerance 0.01 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.005, tol=0.01 |
| GSD-0066 | Join two patches, gap 0.005 mm, tolerance 0.1 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.005, tol=0.1 |
| GSD-0067 | Join two patches, gap 0.02 mm, tolerance 0.001 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.02 > tolerance 0.001; offending edge highlighted. | gap=0.02, tol=0.001 |
| GSD-0068 | Join two patches, gap 0.02 mm, tolerance 0.01 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.02 > tolerance 0.01; offending edge highlighted. | gap=0.02, tol=0.01 |
| GSD-0069 | Join two patches, gap 0.02 mm, tolerance 0.1 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.02, tol=0.1 |
| GSD-0070 | Join two patches, gap 0.05 mm, tolerance 0.001 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.05 > tolerance 0.001; offending edge highlighted. | gap=0.05, tol=0.001 |
| GSD-0071 | Join two patches, gap 0.05 mm, tolerance 0.01 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.05 > tolerance 0.01; offending edge highlighted. | gap=0.05, tol=0.01 |
| GSD-0072 | Join two patches, gap 0.05 mm, tolerance 0.1 mm | Boundary | P2 | Join two adjacent surfaces. | One joined shell; free edges = boundary only. | gap=0.05, tol=0.1 |
| GSD-0073 | Join two patches, gap 0.5 mm, tolerance 0.001 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.5 > tolerance 0.001; offending edge highlighted. | gap=0.5, tol=0.001 |
| GSD-0074 | Join two patches, gap 0.5 mm, tolerance 0.01 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.5 > tolerance 0.01; offending edge highlighted. | gap=0.5, tol=0.01 |
| GSD-0075 | Join two patches, gap 0.5 mm, tolerance 0.1 mm | Boundary | P2 | Join two adjacent surfaces. | Join refuses: gap 0.5 > tolerance 0.1; offending edge highlighted. | gap=0.5, tol=0.1 |
| GSD-0076 | Healing: heal 20 patches with 0.01 mm gaps | Functional | P2 | Run: heal 20 patches with 0.01 mm gaps. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0077 | Healing: heal a sliver face | Functional | P2 | Run: heal a sliver face. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0078 | Healing: remove duplicate faces | Functional | P2 | Run: remove duplicate faces. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0079 | Healing: flip inconsistent normals | Functional | P2 | Run: flip inconsistent normals. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0080 | Healing: close a shell into a solid | Functional | P2 | Run: close a shell into a solid. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0081 | Healing: split by plane | Functional | P2 | Run: split by plane. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0082 | Healing: trim two surfaces | Functional | P2 | Run: trim two surfaces. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0083 | Healing: untrim a face | Functional | P2 | Run: untrim a face. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0084 | Healing: disassemble a join | Functional | P2 | Run: disassemble a join. | Topology valid (BRepCheck OK); counts before/after reported. |  |
| GSD-0085 | Healing: near (extract nearest sub-element) | Functional | P2 | Run: near (extract nearest sub-element). | Topology valid (BRepCheck OK); counts before/after reported. |  |

## Wireframe

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| GSD-0086 | Wireframe point on curve at 0.5: build | Functional | P2 | Create point on curve at 0.5; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0087 | Wireframe point on curve at 0.5: edit input | Functional | P2 | Create point on curve at 0.5; then edit input. | Element updates associatively. |  |
| GSD-0088 | Wireframe point on curve at 0.5: delete input | Functional | P2 | Create point on curve at 0.5; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0089 | Wireframe point at intersection: build | Functional | P2 | Create point at intersection; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0090 | Wireframe point at intersection: edit input | Functional | P2 | Create point at intersection; then edit input. | Element updates associatively. |  |
| GSD-0091 | Wireframe point at intersection: delete input | Functional | P2 | Create point at intersection; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0092 | Wireframe line tangent to curve: build | Functional | P2 | Create line tangent to curve; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0093 | Wireframe line tangent to curve: edit input | Functional | P2 | Create line tangent to curve; then edit input. | Element updates associatively. |  |
| GSD-0094 | Wireframe line tangent to curve: delete input | Functional | P2 | Create line tangent to curve; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0095 | Wireframe line normal to surface: build | Functional | P2 | Create line normal to surface; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0096 | Wireframe line normal to surface: edit input | Functional | P2 | Create line normal to surface; then edit input. | Element updates associatively. |  |
| GSD-0097 | Wireframe line normal to surface: delete input | Functional | P2 | Create line normal to surface; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0098 | Wireframe plane through 3 points: build | Functional | P2 | Create plane through 3 points; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0099 | Wireframe plane through 3 points: edit input | Functional | P2 | Create plane through 3 points; then edit input. | Element updates associatively. |  |
| GSD-0100 | Wireframe plane through 3 points: delete input | Functional | P2 | Create plane through 3 points; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0101 | Wireframe plane offset 20: build | Functional | P2 | Create plane offset 20; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0102 | Wireframe plane offset 20: edit input | Functional | P2 | Create plane offset 20; then edit input. | Element updates associatively. |  |
| GSD-0103 | Wireframe plane offset 20: delete input | Functional | P2 | Create plane offset 20; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0104 | Wireframe plane at angle 30°: build | Functional | P2 | Create plane at angle 30°; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0105 | Wireframe plane at angle 30°: edit input | Functional | P2 | Create plane at angle 30°; then edit input. | Element updates associatively. |  |
| GSD-0106 | Wireframe plane at angle 30°: delete input | Functional | P2 | Create plane at angle 30°; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0107 | Wireframe projection of curve on surface: build | Functional | P2 | Create projection of curve on surface; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0108 | Wireframe projection of curve on surface: edit input | Functional | P2 | Create projection of curve on surface; then edit input. | Element updates associatively. |  |
| GSD-0109 | Wireframe projection of curve on surface: delete input | Functional | P2 | Create projection of curve on surface; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0110 | Wireframe intersection curve of two surfaces: build | Functional | P2 | Create intersection curve of two surfaces; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0111 | Wireframe intersection curve of two surfaces: edit input | Functional | P2 | Create intersection curve of two surfaces; then edit input. | Element updates associatively. |  |
| GSD-0112 | Wireframe intersection curve of two surfaces: delete input | Functional | P2 | Create intersection curve of two surfaces; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0113 | Wireframe parallel curve on surface 5 mm: build | Functional | P2 | Create parallel curve on surface 5 mm; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0114 | Wireframe parallel curve on surface 5 mm: edit input | Functional | P2 | Create parallel curve on surface 5 mm; then edit input. | Element updates associatively. |  |
| GSD-0115 | Wireframe parallel curve on surface 5 mm: delete input | Functional | P2 | Create parallel curve on surface 5 mm; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0116 | Wireframe helix pitch 5, height 50: build | Functional | P2 | Create helix pitch 5, height 50; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0117 | Wireframe helix pitch 5, height 50: edit input | Functional | P2 | Create helix pitch 5, height 50; then edit input. | Element updates associatively. |  |
| GSD-0118 | Wireframe helix pitch 5, height 50: delete input | Functional | P2 | Create helix pitch 5, height 50; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0119 | Wireframe spiral: build | Functional | P2 | Create spiral; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0120 | Wireframe spiral: edit input | Functional | P2 | Create spiral; then edit input. | Element updates associatively. |  |
| GSD-0121 | Wireframe spiral: delete input | Functional | P2 | Create spiral; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0122 | Wireframe corner r=5: build | Functional | P2 | Create corner r=5; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0123 | Wireframe corner r=5: edit input | Functional | P2 | Create corner r=5; then edit input. | Element updates associatively. |  |
| GSD-0124 | Wireframe corner r=5: delete input | Functional | P2 | Create corner r=5; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0125 | Wireframe connect curve (G2): build | Functional | P2 | Create connect curve (G2); then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0126 | Wireframe connect curve (G2): edit input | Functional | P2 | Create connect curve (G2); then edit input. | Element updates associatively. |  |
| GSD-0127 | Wireframe connect curve (G2): delete input | Functional | P2 | Create connect curve (G2); then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0128 | Wireframe 3D polyline: build | Functional | P2 | Create 3D polyline; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0129 | Wireframe 3D polyline: edit input | Functional | P2 | Create 3D polyline; then edit input. | Element updates associatively. |  |
| GSD-0130 | Wireframe 3D polyline: delete input | Functional | P2 | Create 3D polyline; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0131 | Wireframe boundary of a face: build | Functional | P2 | Create boundary of a face; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0132 | Wireframe boundary of a face: edit input | Functional | P2 | Create boundary of a face; then edit input. | Element updates associatively. |  |
| GSD-0133 | Wireframe boundary of a face: delete input | Functional | P2 | Create boundary of a face; then delete input. | Asks to delete dependents or isolate (datum). |  |
| GSD-0134 | Wireframe extract edge: build | Functional | P2 | Create extract edge; then build. | Element valid and positioned correctly (±1e-6 mm). |  |
| GSD-0135 | Wireframe extract edge: edit input | Functional | P2 | Create extract edge; then edit input. | Element updates associatively. |  |
| GSD-0136 | Wireframe extract edge: delete input | Functional | P2 | Create extract edge; then delete input. | Asks to delete dependents or isolate (datum). |  |

## Connect checker

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| GSD-0137 | Connect check distance (G0): joined fillet | Functional | P2 | Run the checker on a joined fillet. | Max deviation reported and compared with 0.001 mm; colour map and worst point shown. |  |
| GSD-0138 | Connect check distance (G0): tangent blend | Functional | P2 | Run the checker on a tangent blend. | Max deviation reported and compared with 0.001 mm; colour map and worst point shown. |  |
| GSD-0139 | Connect check distance (G0): curvature blend | Functional | P2 | Run the checker on a curvature blend. | Max deviation reported and compared with 0.001 mm; colour map and worst point shown. |  |
| GSD-0140 | Connect check distance (G0): mismatched patches | Functional | P2 | Run the checker on a mismatched patches. | Max deviation reported and compared with 0.001 mm; colour map and worst point shown. |  |
| GSD-0141 | Connect check distance (G0): trimmed edge | Functional | P2 | Run the checker on a trimmed edge. | Max deviation reported and compared with 0.001 mm; colour map and worst point shown. |  |
| GSD-0142 | Connect check tangency (G1): joined fillet | Functional | P2 | Run the checker on a joined fillet. | Max deviation reported and compared with 0.1°; colour map and worst point shown. |  |
| GSD-0143 | Connect check tangency (G1): tangent blend | Functional | P2 | Run the checker on a tangent blend. | Max deviation reported and compared with 0.1°; colour map and worst point shown. |  |
| GSD-0144 | Connect check tangency (G1): curvature blend | Functional | P2 | Run the checker on a curvature blend. | Max deviation reported and compared with 0.1°; colour map and worst point shown. |  |
| GSD-0145 | Connect check tangency (G1): mismatched patches | Functional | P2 | Run the checker on a mismatched patches. | Max deviation reported and compared with 0.1°; colour map and worst point shown. |  |
| GSD-0146 | Connect check tangency (G1): trimmed edge | Functional | P2 | Run the checker on a trimmed edge. | Max deviation reported and compared with 0.1°; colour map and worst point shown. |  |
| GSD-0147 | Connect check curvature (G2): joined fillet | Functional | P2 | Run the checker on a joined fillet. | Max deviation reported and compared with 5%; colour map and worst point shown. |  |
| GSD-0148 | Connect check curvature (G2): tangent blend | Functional | P2 | Run the checker on a tangent blend. | Max deviation reported and compared with 5%; colour map and worst point shown. |  |
| GSD-0149 | Connect check curvature (G2): curvature blend | Functional | P2 | Run the checker on a curvature blend. | Max deviation reported and compared with 5%; colour map and worst point shown. |  |
| GSD-0150 | Connect check curvature (G2): mismatched patches | Functional | P2 | Run the checker on a mismatched patches. | Max deviation reported and compared with 5%; colour map and worst point shown. |  |
| GSD-0151 | Connect check curvature (G2): trimmed edge | Functional | P2 | Run the checker on a trimmed edge. | Max deviation reported and compared with 5%; colour map and worst point shown. |  |
| GSD-0152 | Connect check curvature rate (G3): joined fillet | Functional | P2 | Run the checker on a joined fillet. | Max deviation reported and compared with 10%; colour map and worst point shown. |  |
| GSD-0153 | Connect check curvature rate (G3): tangent blend | Functional | P2 | Run the checker on a tangent blend. | Max deviation reported and compared with 10%; colour map and worst point shown. |  |
| GSD-0154 | Connect check curvature rate (G3): curvature blend | Functional | P2 | Run the checker on a curvature blend. | Max deviation reported and compared with 10%; colour map and worst point shown. |  |
| GSD-0155 | Connect check curvature rate (G3): mismatched patches | Functional | P2 | Run the checker on a mismatched patches. | Max deviation reported and compared with 10%; colour map and worst point shown. |  |
| GSD-0156 | Connect check curvature rate (G3): trimmed edge | Functional | P2 | Run the checker on a trimmed edge. | Max deviation reported and compared with 10%; colour map and worst point shown. |  |
