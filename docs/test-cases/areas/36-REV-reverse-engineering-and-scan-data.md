# REV — Reverse engineering and scan data

**CATIA-class equivalent:** Digitized Shape Editor / Quick Surface Reconstruction  
**Autevra workspace:** Part Design (imports); Styling (reference)  
**Scope:** Shared  
**Cases:** 114 (Have 0, Partial 0, Gap 114)

Point clouds and meshes to usable geometry.

[← Back to the index](../README.md)

## Features

- Point clouds and meshes — 90 cases (Gap)
- Surface reconstruction — 24 cases (Gap)

## Point clouds and meshes

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| REV-0001 | import: PLY, 10k points | Functional | P2 | Import a 10k-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0002 | decimate 50%: PLY, 10k points | Functional | P2 | Decimate 50% a 10k-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0003 | remove outliers: PLY, 10k points | Functional | P2 | Remove outliers a 10k-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0004 | align to datum (3-2-1): PLY, 10k points | Functional | P2 | Align to datum (3-2-1) a 10k-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0005 | mesh from cloud: PLY, 10k points | Functional | P2 | Mesh from cloud a 10k-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0006 | import: PLY, 1M points | Functional | P2 | Import a 1M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0007 | decimate 50%: PLY, 1M points | Functional | P2 | Decimate 50% a 1M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0008 | remove outliers: PLY, 1M points | Functional | P2 | Remove outliers a 1M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0009 | align to datum (3-2-1): PLY, 1M points | Functional | P2 | Align to datum (3-2-1) a 1M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0010 | mesh from cloud: PLY, 1M points | Functional | P2 | Mesh from cloud a 1M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0011 | import: PLY, 20M points | Performance | P2 | Import a 20M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0012 | decimate 50%: PLY, 20M points | Performance | P2 | Decimate 50% a 20M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0013 | remove outliers: PLY, 20M points | Performance | P2 | Remove outliers a 20M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0014 | align to datum (3-2-1): PLY, 20M points | Performance | P2 | Align to datum (3-2-1) a 20M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0015 | mesh from cloud: PLY, 20M points | Performance | P2 | Mesh from cloud a 20M-point PLY scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0016 | import: STL, 10k points | Functional | P2 | Import a 10k-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0017 | decimate 50%: STL, 10k points | Functional | P2 | Decimate 50% a 10k-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0018 | remove outliers: STL, 10k points | Functional | P2 | Remove outliers a 10k-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0019 | align to datum (3-2-1): STL, 10k points | Functional | P2 | Align to datum (3-2-1) a 10k-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0020 | mesh from cloud: STL, 10k points | Functional | P2 | Mesh from cloud a 10k-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0021 | import: STL, 1M points | Functional | P2 | Import a 1M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0022 | decimate 50%: STL, 1M points | Functional | P2 | Decimate 50% a 1M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0023 | remove outliers: STL, 1M points | Functional | P2 | Remove outliers a 1M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0024 | align to datum (3-2-1): STL, 1M points | Functional | P2 | Align to datum (3-2-1) a 1M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0025 | mesh from cloud: STL, 1M points | Functional | P2 | Mesh from cloud a 1M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0026 | import: STL, 20M points | Performance | P2 | Import a 20M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0027 | decimate 50%: STL, 20M points | Performance | P2 | Decimate 50% a 20M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0028 | remove outliers: STL, 20M points | Performance | P2 | Remove outliers a 20M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0029 | align to datum (3-2-1): STL, 20M points | Performance | P2 | Align to datum (3-2-1) a 20M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0030 | mesh from cloud: STL, 20M points | Performance | P2 | Mesh from cloud a 20M-point STL scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0031 | import: OBJ, 10k points | Functional | P2 | Import a 10k-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0032 | decimate 50%: OBJ, 10k points | Functional | P2 | Decimate 50% a 10k-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0033 | remove outliers: OBJ, 10k points | Functional | P2 | Remove outliers a 10k-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0034 | align to datum (3-2-1): OBJ, 10k points | Functional | P2 | Align to datum (3-2-1) a 10k-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0035 | mesh from cloud: OBJ, 10k points | Functional | P2 | Mesh from cloud a 10k-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0036 | import: OBJ, 1M points | Functional | P2 | Import a 1M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0037 | decimate 50%: OBJ, 1M points | Functional | P2 | Decimate 50% a 1M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0038 | remove outliers: OBJ, 1M points | Functional | P2 | Remove outliers a 1M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0039 | align to datum (3-2-1): OBJ, 1M points | Functional | P2 | Align to datum (3-2-1) a 1M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0040 | mesh from cloud: OBJ, 1M points | Functional | P2 | Mesh from cloud a 1M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0041 | import: OBJ, 20M points | Performance | P2 | Import a 20M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0042 | decimate 50%: OBJ, 20M points | Performance | P2 | Decimate 50% a 20M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0043 | remove outliers: OBJ, 20M points | Performance | P2 | Remove outliers a 20M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0044 | align to datum (3-2-1): OBJ, 20M points | Performance | P2 | Align to datum (3-2-1) a 20M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0045 | mesh from cloud: OBJ, 20M points | Performance | P2 | Mesh from cloud a 20M-point OBJ scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0046 | import: E57, 10k points | Functional | P2 | Import a 10k-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0047 | decimate 50%: E57, 10k points | Functional | P2 | Decimate 50% a 10k-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0048 | remove outliers: E57, 10k points | Functional | P2 | Remove outliers a 10k-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0049 | align to datum (3-2-1): E57, 10k points | Functional | P2 | Align to datum (3-2-1) a 10k-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0050 | mesh from cloud: E57, 10k points | Functional | P2 | Mesh from cloud a 10k-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0051 | import: E57, 1M points | Functional | P2 | Import a 1M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0052 | decimate 50%: E57, 1M points | Functional | P2 | Decimate 50% a 1M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0053 | remove outliers: E57, 1M points | Functional | P2 | Remove outliers a 1M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0054 | align to datum (3-2-1): E57, 1M points | Functional | P2 | Align to datum (3-2-1) a 1M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0055 | mesh from cloud: E57, 1M points | Functional | P2 | Mesh from cloud a 1M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0056 | import: E57, 20M points | Performance | P2 | Import a 20M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0057 | decimate 50%: E57, 20M points | Performance | P2 | Decimate 50% a 20M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0058 | remove outliers: E57, 20M points | Performance | P2 | Remove outliers a 20M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0059 | align to datum (3-2-1): E57, 20M points | Performance | P2 | Align to datum (3-2-1) a 20M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0060 | mesh from cloud: E57, 20M points | Performance | P2 | Mesh from cloud a 20M-point E57 scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0061 | import: XYZ ASCII, 10k points | Functional | P2 | Import a 10k-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0062 | decimate 50%: XYZ ASCII, 10k points | Functional | P2 | Decimate 50% a 10k-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0063 | remove outliers: XYZ ASCII, 10k points | Functional | P2 | Remove outliers a 10k-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0064 | align to datum (3-2-1): XYZ ASCII, 10k points | Functional | P2 | Align to datum (3-2-1) a 10k-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0065 | mesh from cloud: XYZ ASCII, 10k points | Functional | P2 | Mesh from cloud a 10k-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0066 | import: XYZ ASCII, 1M points | Functional | P2 | Import a 1M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0067 | decimate 50%: XYZ ASCII, 1M points | Functional | P2 | Decimate 50% a 1M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0068 | remove outliers: XYZ ASCII, 1M points | Functional | P2 | Remove outliers a 1M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0069 | align to datum (3-2-1): XYZ ASCII, 1M points | Functional | P2 | Align to datum (3-2-1) a 1M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0070 | mesh from cloud: XYZ ASCII, 1M points | Functional | P2 | Mesh from cloud a 1M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0071 | import: XYZ ASCII, 20M points | Performance | P2 | Import a 20M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0072 | decimate 50%: XYZ ASCII, 20M points | Performance | P2 | Decimate 50% a 20M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0073 | remove outliers: XYZ ASCII, 20M points | Performance | P2 | Remove outliers a 20M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0074 | align to datum (3-2-1): XYZ ASCII, 20M points | Performance | P2 | Align to datum (3-2-1) a 20M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0075 | mesh from cloud: XYZ ASCII, 20M points | Performance | P2 | Mesh from cloud a 20M-point XYZ ASCII scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0076 | import: LAS, 10k points | Functional | P2 | Import a 10k-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0077 | decimate 50%: LAS, 10k points | Functional | P2 | Decimate 50% a 10k-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0078 | remove outliers: LAS, 10k points | Functional | P2 | Remove outliers a 10k-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0079 | align to datum (3-2-1): LAS, 10k points | Functional | P2 | Align to datum (3-2-1) a 10k-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0080 | mesh from cloud: LAS, 10k points | Functional | P2 | Mesh from cloud a 10k-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0081 | import: LAS, 1M points | Functional | P2 | Import a 1M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0082 | decimate 50%: LAS, 1M points | Functional | P2 | Decimate 50% a 1M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0083 | remove outliers: LAS, 1M points | Functional | P2 | Remove outliers a 1M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0084 | align to datum (3-2-1): LAS, 1M points | Functional | P2 | Align to datum (3-2-1) a 1M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0085 | mesh from cloud: LAS, 1M points | Functional | P2 | Mesh from cloud a 1M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0086 | import: LAS, 20M points | Performance | P2 | Import a 20M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0087 | decimate 50%: LAS, 20M points | Performance | P2 | Decimate 50% a 20M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0088 | remove outliers: LAS, 20M points | Performance | P2 | Remove outliers a 20M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0089 | align to datum (3-2-1): LAS, 20M points | Performance | P2 | Align to datum (3-2-1) a 20M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |
| REV-0090 | mesh from cloud: LAS, 20M points | Performance | P2 | Mesh from cloud a 20M-point LAS scan. | Completes with progress; point/face counts reported; memory bounded. |  |

## Surface reconstruction

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| REV-0091 | fit plane with noise σ=0.0 mm | Accuracy | P2 | Run fit plane on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0092 | fit plane with noise σ=0.05 mm | Accuracy | P2 | Run fit plane on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0093 | fit plane with noise σ=0.2 mm | Accuracy | P2 | Run fit plane on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0094 | fit cylinder with noise σ=0.0 mm | Accuracy | P2 | Run fit cylinder on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0095 | fit cylinder with noise σ=0.05 mm | Accuracy | P2 | Run fit cylinder on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0096 | fit cylinder with noise σ=0.2 mm | Accuracy | P2 | Run fit cylinder on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0097 | fit sphere with noise σ=0.0 mm | Accuracy | P2 | Run fit sphere on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0098 | fit sphere with noise σ=0.05 mm | Accuracy | P2 | Run fit sphere on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0099 | fit sphere with noise σ=0.2 mm | Accuracy | P2 | Run fit sphere on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0100 | fit cone with noise σ=0.0 mm | Accuracy | P2 | Run fit cone on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0101 | fit cone with noise σ=0.05 mm | Accuracy | P2 | Run fit cone on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0102 | fit cone with noise σ=0.2 mm | Accuracy | P2 | Run fit cone on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0103 | auto-surface (NURBS patches) with noise σ=0.0 mm | Accuracy | P2 | Run auto-surface (NURBS patches) on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0104 | auto-surface (NURBS patches) with noise σ=0.05 mm | Accuracy | P2 | Run auto-surface (NURBS patches) on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0105 | auto-surface (NURBS patches) with noise σ=0.2 mm | Accuracy | P2 | Run auto-surface (NURBS patches) on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0106 | feature lines with noise σ=0.0 mm | Accuracy | P2 | Run feature lines on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0107 | feature lines with noise σ=0.05 mm | Accuracy | P2 | Run feature lines on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0108 | feature lines with noise σ=0.2 mm | Accuracy | P2 | Run feature lines on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0109 | deviation map scan vs CAD with noise σ=0.0 mm | Accuracy | P2 | Run deviation map scan vs CAD on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0110 | deviation map scan vs CAD with noise σ=0.05 mm | Accuracy | P2 | Run deviation map scan vs CAD on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0111 | deviation map scan vs CAD with noise σ=0.2 mm | Accuracy | P2 | Run deviation map scan vs CAD on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0112 | section curves from mesh with noise σ=0.0 mm | Accuracy | P2 | Run section curves from mesh on a synthetic scan. | Exact parameters recovered (< 1e-6). |  |
| REV-0113 | section curves from mesh with noise σ=0.05 mm | Accuracy | P2 | Run section curves from mesh on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
| REV-0114 | section curves from mesh with noise σ=0.2 mm | Accuracy | P2 | Run section curves from mesh on a synthetic scan. | Fitted parameters within 3σ of truth; deviation histogram reported. |  |
