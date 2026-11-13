# IOX — Data exchange

**CATIA-class equivalent:** STEP/IGES interfaces, 3D XML, CATIA V5↔V6 migration  
**Autevra workspace:** Manufacturing (exports); /import-step  
**Scope:** Shared  
**Cases:** 390 (Have 50, Partial 39, Gap 301)

Import, export and round trips for neutral formats, with unit, naming and accuracy checks.

[← Back to the index](../README.md)

## Features

- Export — 224 cases (Have)
- Import — 112 cases (Partial)
- Round trip — 30 cases (Partial)
- Data formats (non-geometry) — 24 cases (Have)

## Export

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| IOX-0001 | Export STEP AP214: single solid | Interop | P1 | Build single solid; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0002 | Export STEP AP214: multi-body part | Interop | P1 | Build multi-body part; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0003 | Export STEP AP214: assembly (10 parts, names, colours) | Interop | P1 | Build assembly (10 parts, names, colours); export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0004 | Export STEP AP214: surface-only model | Interop | P1 | Build surface-only model; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0005 | Export STEP AP214: wireframe | Interop | P1 | Build wireframe; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0006 | Export STEP AP214: model in inches | Interop | P1 | Build model in inches; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0007 | Export STEP AP214: part with 1 µm features | Interop | P1 | Build part with 1 µm features; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0008 | Export STEP AP214: 1,000-part assembly | Interop | P1 | Build 1,000-part assembly; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0009 | Export STEP AP214: empty project | Interop | P1 | Build empty project; export STEP AP214. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0010 | Export STEP AP214: non-ASCII part names (Größe, 部品) | Interop | P1 | Build non-ASCII part names (Größe, 部品); export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0011 | Export STEP AP214: part with a 0.001 mm sliver face | Interop | P1 | Build part with a 0.001 mm sliver face; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0012 | Export STEP AP214: part 100 m long | Interop | P1 | Build part 100 m long; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0013 | Export STEP AP214: assembly with instanced parts | Interop | P1 | Build assembly with instanced parts; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0014 | Export STEP AP214: model with a cosmetic thread | Interop | P1 | Build model with a cosmetic thread; export STEP AP214. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0015 | Export STEP AP242: single solid | Interop | P1 | Build single solid; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0016 | Export STEP AP242: multi-body part | Interop | P1 | Build multi-body part; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0017 | Export STEP AP242: assembly (10 parts, names, colours) | Interop | P1 | Build assembly (10 parts, names, colours); export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0018 | Export STEP AP242: surface-only model | Interop | P1 | Build surface-only model; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0019 | Export STEP AP242: wireframe | Interop | P1 | Build wireframe; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0020 | Export STEP AP242: model in inches | Interop | P1 | Build model in inches; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0021 | Export STEP AP242: part with 1 µm features | Interop | P1 | Build part with 1 µm features; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0022 | Export STEP AP242: 1,000-part assembly | Interop | P1 | Build 1,000-part assembly; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0023 | Export STEP AP242: empty project | Interop | P1 | Build empty project; export STEP AP242. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0024 | Export STEP AP242: non-ASCII part names (Größe, 部品) | Interop | P1 | Build non-ASCII part names (Größe, 部品); export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0025 | Export STEP AP242: part with a 0.001 mm sliver face | Interop | P1 | Build part with a 0.001 mm sliver face; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0026 | Export STEP AP242: part 100 m long | Interop | P1 | Build part 100 m long; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0027 | Export STEP AP242: assembly with instanced parts | Interop | P1 | Build assembly with instanced parts; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0028 | Export STEP AP242: model with a cosmetic thread | Interop | P1 | Build model with a cosmetic thread; export STEP AP242. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0029 | Export STEP AP203: single solid | Interop | P2 | Build single solid; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0030 | Export STEP AP203: multi-body part | Interop | P2 | Build multi-body part; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0031 | Export STEP AP203: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0032 | Export STEP AP203: surface-only model | Interop | P2 | Build surface-only model; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0033 | Export STEP AP203: wireframe | Interop | P2 | Build wireframe; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0034 | Export STEP AP203: model in inches | Interop | P2 | Build model in inches; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0035 | Export STEP AP203: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0036 | Export STEP AP203: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0037 | Export STEP AP203: empty project | Interop | P2 | Build empty project; export STEP AP203. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0038 | Export STEP AP203: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0039 | Export STEP AP203: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0040 | Export STEP AP203: part 100 m long | Interop | P2 | Build part 100 m long; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0041 | Export STEP AP203: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0042 | Export STEP AP203: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export STEP AP203. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0043 | Export IGES 5.3: single solid | Interop | P2 | Build single solid; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0044 | Export IGES 5.3: multi-body part | Interop | P2 | Build multi-body part; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0045 | Export IGES 5.3: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0046 | Export IGES 5.3: surface-only model | Interop | P2 | Build surface-only model; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0047 | Export IGES 5.3: wireframe | Interop | P2 | Build wireframe; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0048 | Export IGES 5.3: model in inches | Interop | P2 | Build model in inches; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0049 | Export IGES 5.3: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0050 | Export IGES 5.3: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0051 | Export IGES 5.3: empty project | Interop | P2 | Build empty project; export IGES 5.3. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0052 | Export IGES 5.3: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0053 | Export IGES 5.3: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0054 | Export IGES 5.3: part 100 m long | Interop | P2 | Build part 100 m long; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0055 | Export IGES 5.3: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0056 | Export IGES 5.3: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export IGES 5.3. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0057 | Export STL (binary): single solid | Interop | P2 | Build single solid; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0058 | Export STL (binary): multi-body part | Interop | P2 | Build multi-body part; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0059 | Export STL (binary): assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0060 | Export STL (binary): surface-only model | Interop | P2 | Build surface-only model; export STL (binary). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0061 | Export STL (binary): wireframe | Interop | P2 | Build wireframe; export STL (binary). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0062 | Export STL (binary): model in inches | Interop | P2 | Build model in inches; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0063 | Export STL (binary): part with 1 µm features | Interop | P2 | Build part with 1 µm features; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0064 | Export STL (binary): 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0065 | Export STL (binary): empty project | Interop | P2 | Build empty project; export STL (binary). | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0066 | Export STL (binary): non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0067 | Export STL (binary): part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0068 | Export STL (binary): part 100 m long | Interop | P2 | Build part 100 m long; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0069 | Export STL (binary): assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0070 | Export STL (binary): model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export STL (binary). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0071 | Export STL (ASCII): single solid | Interop | P2 | Build single solid; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0072 | Export STL (ASCII): multi-body part | Interop | P2 | Build multi-body part; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0073 | Export STL (ASCII): assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0074 | Export STL (ASCII): surface-only model | Interop | P2 | Build surface-only model; export STL (ASCII). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0075 | Export STL (ASCII): wireframe | Interop | P2 | Build wireframe; export STL (ASCII). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0076 | Export STL (ASCII): model in inches | Interop | P2 | Build model in inches; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0077 | Export STL (ASCII): part with 1 µm features | Interop | P2 | Build part with 1 µm features; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0078 | Export STL (ASCII): 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0079 | Export STL (ASCII): empty project | Interop | P2 | Build empty project; export STL (ASCII). | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0080 | Export STL (ASCII): non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0081 | Export STL (ASCII): part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0082 | Export STL (ASCII): part 100 m long | Interop | P2 | Build part 100 m long; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0083 | Export STL (ASCII): assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0084 | Export STL (ASCII): model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export STL (ASCII). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0085 | Export OBJ: single solid | Interop | P2 | Build single solid; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0086 | Export OBJ: multi-body part | Interop | P2 | Build multi-body part; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0087 | Export OBJ: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0088 | Export OBJ: surface-only model | Interop | P2 | Build surface-only model; export OBJ. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0089 | Export OBJ: wireframe | Interop | P2 | Build wireframe; export OBJ. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0090 | Export OBJ: model in inches | Interop | P2 | Build model in inches; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0091 | Export OBJ: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0092 | Export OBJ: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0093 | Export OBJ: empty project | Interop | P2 | Build empty project; export OBJ. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0094 | Export OBJ: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0095 | Export OBJ: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0096 | Export OBJ: part 100 m long | Interop | P2 | Build part 100 m long; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0097 | Export OBJ: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0098 | Export OBJ: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export OBJ. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0099 | Export glTF 2.0 (.glb): single solid | Interop | P2 | Build single solid; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0100 | Export glTF 2.0 (.glb): multi-body part | Interop | P2 | Build multi-body part; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0101 | Export glTF 2.0 (.glb): assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0102 | Export glTF 2.0 (.glb): surface-only model | Interop | P2 | Build surface-only model; export glTF 2.0 (.glb). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0103 | Export glTF 2.0 (.glb): wireframe | Interop | P2 | Build wireframe; export glTF 2.0 (.glb). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0104 | Export glTF 2.0 (.glb): model in inches | Interop | P2 | Build model in inches; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0105 | Export glTF 2.0 (.glb): part with 1 µm features | Interop | P2 | Build part with 1 µm features; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0106 | Export glTF 2.0 (.glb): 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0107 | Export glTF 2.0 (.glb): empty project | Interop | P2 | Build empty project; export glTF 2.0 (.glb). | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0108 | Export glTF 2.0 (.glb): non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0109 | Export glTF 2.0 (.glb): part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0110 | Export glTF 2.0 (.glb): part 100 m long | Interop | P2 | Build part 100 m long; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0111 | Export glTF 2.0 (.glb): assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0112 | Export glTF 2.0 (.glb): model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export glTF 2.0 (.glb). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0113 | Export 3MF: single solid | Interop | P2 | Build single solid; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0114 | Export 3MF: multi-body part | Interop | P2 | Build multi-body part; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0115 | Export 3MF: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0116 | Export 3MF: surface-only model | Interop | P2 | Build surface-only model; export 3MF. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0117 | Export 3MF: wireframe | Interop | P2 | Build wireframe; export 3MF. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0118 | Export 3MF: model in inches | Interop | P2 | Build model in inches; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0119 | Export 3MF: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0120 | Export 3MF: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0121 | Export 3MF: empty project | Interop | P2 | Build empty project; export 3MF. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0122 | Export 3MF: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0123 | Export 3MF: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0124 | Export 3MF: part 100 m long | Interop | P2 | Build part 100 m long; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0125 | Export 3MF: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0126 | Export 3MF: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export 3MF. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0127 | Export Parasolid x_t: single solid | Interop | P2 | Build single solid; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0128 | Export Parasolid x_t: multi-body part | Interop | P2 | Build multi-body part; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0129 | Export Parasolid x_t: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0130 | Export Parasolid x_t: surface-only model | Interop | P2 | Build surface-only model; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0131 | Export Parasolid x_t: wireframe | Interop | P2 | Build wireframe; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0132 | Export Parasolid x_t: model in inches | Interop | P2 | Build model in inches; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0133 | Export Parasolid x_t: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0134 | Export Parasolid x_t: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0135 | Export Parasolid x_t: empty project | Interop | P2 | Build empty project; export Parasolid x_t. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0136 | Export Parasolid x_t: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0137 | Export Parasolid x_t: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0138 | Export Parasolid x_t: part 100 m long | Interop | P2 | Build part 100 m long; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0139 | Export Parasolid x_t: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0140 | Export Parasolid x_t: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export Parasolid x_t. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0141 | Export JT: single solid | Interop | P2 | Build single solid; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0142 | Export JT: multi-body part | Interop | P2 | Build multi-body part; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0143 | Export JT: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0144 | Export JT: surface-only model | Interop | P2 | Build surface-only model; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0145 | Export JT: wireframe | Interop | P2 | Build wireframe; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0146 | Export JT: model in inches | Interop | P2 | Build model in inches; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0147 | Export JT: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0148 | Export JT: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0149 | Export JT: empty project | Interop | P2 | Build empty project; export JT. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0150 | Export JT: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0151 | Export JT: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0152 | Export JT: part 100 m long | Interop | P2 | Build part 100 m long; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0153 | Export JT: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0154 | Export JT: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export JT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0155 | Export ACIS SAT: single solid | Interop | P2 | Build single solid; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0156 | Export ACIS SAT: multi-body part | Interop | P2 | Build multi-body part; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0157 | Export ACIS SAT: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0158 | Export ACIS SAT: surface-only model | Interop | P2 | Build surface-only model; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0159 | Export ACIS SAT: wireframe | Interop | P2 | Build wireframe; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0160 | Export ACIS SAT: model in inches | Interop | P2 | Build model in inches; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0161 | Export ACIS SAT: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0162 | Export ACIS SAT: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0163 | Export ACIS SAT: empty project | Interop | P2 | Build empty project; export ACIS SAT. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0164 | Export ACIS SAT: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0165 | Export ACIS SAT: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0166 | Export ACIS SAT: part 100 m long | Interop | P2 | Build part 100 m long; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0167 | Export ACIS SAT: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0168 | Export ACIS SAT: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export ACIS SAT. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0169 | Export DXF: single solid | Interop | P2 | Build single solid; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0170 | Export DXF: multi-body part | Interop | P2 | Build multi-body part; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0171 | Export DXF: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0172 | Export DXF: surface-only model | Interop | P2 | Build surface-only model; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0173 | Export DXF: wireframe | Interop | P2 | Build wireframe; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0174 | Export DXF: model in inches | Interop | P2 | Build model in inches; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0175 | Export DXF: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0176 | Export DXF: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0177 | Export DXF: empty project | Interop | P2 | Build empty project; export DXF. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0178 | Export DXF: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0179 | Export DXF: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0180 | Export DXF: part 100 m long | Interop | P2 | Build part 100 m long; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0181 | Export DXF: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0182 | Export DXF: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export DXF. | Re-imports in a reference reader with identical topology counts and volume (1e-6 rel); names/colours kept. |  |
| IOX-0183 | Export VRML: single solid | Interop | P2 | Build single solid; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0184 | Export VRML: multi-body part | Interop | P2 | Build multi-body part; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0185 | Export VRML: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0186 | Export VRML: surface-only model | Interop | P2 | Build surface-only model; export VRML. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0187 | Export VRML: wireframe | Interop | P2 | Build wireframe; export VRML. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0188 | Export VRML: model in inches | Interop | P2 | Build model in inches; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0189 | Export VRML: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0190 | Export VRML: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0191 | Export VRML: empty project | Interop | P2 | Build empty project; export VRML. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0192 | Export VRML: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0193 | Export VRML: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0194 | Export VRML: part 100 m long | Interop | P2 | Build part 100 m long; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0195 | Export VRML: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0196 | Export VRML: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export VRML. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0197 | Export PLY: single solid | Interop | P2 | Build single solid; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0198 | Export PLY: multi-body part | Interop | P2 | Build multi-body part; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0199 | Export PLY: assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0200 | Export PLY: surface-only model | Interop | P2 | Build surface-only model; export PLY. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0201 | Export PLY: wireframe | Interop | P2 | Build wireframe; export PLY. | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0202 | Export PLY: model in inches | Interop | P2 | Build model in inches; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0203 | Export PLY: part with 1 µm features | Interop | P2 | Build part with 1 µm features; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0204 | Export PLY: 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0205 | Export PLY: empty project | Interop | P2 | Build empty project; export PLY. | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0206 | Export PLY: non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0207 | Export PLY: part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0208 | Export PLY: part 100 m long | Interop | P2 | Build part 100 m long; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0209 | Export PLY: assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0210 | Export PLY: model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export PLY. | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0211 | Export USD (.usdz): single solid | Interop | P2 | Build single solid; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0212 | Export USD (.usdz): multi-body part | Interop | P2 | Build multi-body part; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0213 | Export USD (.usdz): assembly (10 parts, names, colours) | Interop | P2 | Build assembly (10 parts, names, colours); export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0214 | Export USD (.usdz): surface-only model | Interop | P2 | Build surface-only model; export USD (.usdz). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0215 | Export USD (.usdz): wireframe | Interop | P2 | Build wireframe; export USD (.usdz). | Surfaces tessellated; wireframe skipped with a warning. |  |
| IOX-0216 | Export USD (.usdz): model in inches | Interop | P2 | Build model in inches; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0217 | Export USD (.usdz): part with 1 µm features | Interop | P2 | Build part with 1 µm features; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0218 | Export USD (.usdz): 1,000-part assembly | Interop | P2 | Build 1,000-part assembly; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0219 | Export USD (.usdz): empty project | Interop | P2 | Build empty project; export USD (.usdz). | Valid empty file or a clear 'nothing to export' message; no crash. |  |
| IOX-0220 | Export USD (.usdz): non-ASCII part names (Größe, 部品) | Interop | P2 | Build non-ASCII part names (Größe, 部品); export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0221 | Export USD (.usdz): part with a 0.001 mm sliver face | Interop | P2 | Build part with a 0.001 mm sliver face; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0222 | Export USD (.usdz): part 100 m long | Interop | P2 | Build part 100 m long; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0223 | Export USD (.usdz): assembly with instanced parts | Interop | P2 | Build assembly with instanced parts; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |
| IOX-0224 | Export USD (.usdz): model with a cosmetic thread | Interop | P2 | Build model with a cosmetic thread; export USD (.usdz). | Watertight mesh per solid; chord tolerance honoured; units stated (glTF: metres, Y-up). |  |

## Import

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| IOX-0225 | Import STEP AP214: clean solid | Interop | P2 | Import a clean solid (STEP AP214). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0226 | Import STEP AP214: assembly | Interop | P2 | Import a assembly (STEP AP214). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0227 | Import STEP AP214: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (STEP AP214). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0228 | Import STEP AP214: corrupted file | Negative | P2 | Import a corrupted file (STEP AP214). | Rejected with parse position; project untouched. |  |
| IOX-0229 | Import STEP AP214: inch file | Interop | P2 | Import a inch file (STEP AP214). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0230 | Import STEP AP214: 500 MB file | Performance | P2 | Import a 500 MB file (STEP AP214). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0231 | Import STEP AP214: file from another vendor | Interop | P2 | Import a file from another vendor (STEP AP214). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0232 | Import STEP AP242: clean solid | Interop | P2 | Import a clean solid (STEP AP242). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0233 | Import STEP AP242: assembly | Interop | P2 | Import a assembly (STEP AP242). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0234 | Import STEP AP242: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (STEP AP242). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0235 | Import STEP AP242: corrupted file | Negative | P2 | Import a corrupted file (STEP AP242). | Rejected with parse position; project untouched. |  |
| IOX-0236 | Import STEP AP242: inch file | Interop | P2 | Import a inch file (STEP AP242). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0237 | Import STEP AP242: 500 MB file | Performance | P2 | Import a 500 MB file (STEP AP242). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0238 | Import STEP AP242: file from another vendor | Interop | P2 | Import a file from another vendor (STEP AP242). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0239 | Import STEP AP203: clean solid | Interop | P2 | Import a clean solid (STEP AP203). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0240 | Import STEP AP203: assembly | Interop | P2 | Import a assembly (STEP AP203). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0241 | Import STEP AP203: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (STEP AP203). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0242 | Import STEP AP203: corrupted file | Negative | P2 | Import a corrupted file (STEP AP203). | Rejected with parse position; project untouched. |  |
| IOX-0243 | Import STEP AP203: inch file | Interop | P2 | Import a inch file (STEP AP203). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0244 | Import STEP AP203: 500 MB file | Performance | P2 | Import a 500 MB file (STEP AP203). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0245 | Import STEP AP203: file from another vendor | Interop | P2 | Import a file from another vendor (STEP AP203). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0246 | Import IGES 5.3: clean solid | Interop | P2 | Import a clean solid (IGES 5.3). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0247 | Import IGES 5.3: assembly | Interop | P2 | Import a assembly (IGES 5.3). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0248 | Import IGES 5.3: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (IGES 5.3). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0249 | Import IGES 5.3: corrupted file | Negative | P2 | Import a corrupted file (IGES 5.3). | Rejected with parse position; project untouched. |  |
| IOX-0250 | Import IGES 5.3: inch file | Interop | P2 | Import a inch file (IGES 5.3). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0251 | Import IGES 5.3: 500 MB file | Performance | P2 | Import a 500 MB file (IGES 5.3). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0252 | Import IGES 5.3: file from another vendor | Interop | P2 | Import a file from another vendor (IGES 5.3). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0253 | Import STL (binary): clean solid | Interop | P2 | Import a clean solid (STL (binary)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0254 | Import STL (binary): assembly | Interop | P2 | Import a assembly (STL (binary)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0255 | Import STL (binary): file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (STL (binary)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0256 | Import STL (binary): corrupted file | Negative | P2 | Import a corrupted file (STL (binary)). | Rejected with parse position; project untouched. |  |
| IOX-0257 | Import STL (binary): inch file | Interop | P2 | Import a inch file (STL (binary)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0258 | Import STL (binary): 500 MB file | Performance | P2 | Import a 500 MB file (STL (binary)). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0259 | Import STL (binary): file from another vendor | Interop | P2 | Import a file from another vendor (STL (binary)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0260 | Import STL (ASCII): clean solid | Interop | P2 | Import a clean solid (STL (ASCII)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0261 | Import STL (ASCII): assembly | Interop | P2 | Import a assembly (STL (ASCII)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0262 | Import STL (ASCII): file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (STL (ASCII)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0263 | Import STL (ASCII): corrupted file | Negative | P2 | Import a corrupted file (STL (ASCII)). | Rejected with parse position; project untouched. |  |
| IOX-0264 | Import STL (ASCII): inch file | Interop | P2 | Import a inch file (STL (ASCII)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0265 | Import STL (ASCII): 500 MB file | Performance | P2 | Import a 500 MB file (STL (ASCII)). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0266 | Import STL (ASCII): file from another vendor | Interop | P2 | Import a file from another vendor (STL (ASCII)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0267 | Import OBJ: clean solid | Interop | P2 | Import a clean solid (OBJ). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0268 | Import OBJ: assembly | Interop | P2 | Import a assembly (OBJ). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0269 | Import OBJ: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (OBJ). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0270 | Import OBJ: corrupted file | Negative | P2 | Import a corrupted file (OBJ). | Rejected with parse position; project untouched. |  |
| IOX-0271 | Import OBJ: inch file | Interop | P2 | Import a inch file (OBJ). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0272 | Import OBJ: 500 MB file | Performance | P2 | Import a 500 MB file (OBJ). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0273 | Import OBJ: file from another vendor | Interop | P2 | Import a file from another vendor (OBJ). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0274 | Import glTF 2.0 (.glb): clean solid | Interop | P2 | Import a clean solid (glTF 2.0 (.glb)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0275 | Import glTF 2.0 (.glb): assembly | Interop | P2 | Import a assembly (glTF 2.0 (.glb)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0276 | Import glTF 2.0 (.glb): file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (glTF 2.0 (.glb)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0277 | Import glTF 2.0 (.glb): corrupted file | Negative | P2 | Import a corrupted file (glTF 2.0 (.glb)). | Rejected with parse position; project untouched. |  |
| IOX-0278 | Import glTF 2.0 (.glb): inch file | Interop | P2 | Import a inch file (glTF 2.0 (.glb)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0279 | Import glTF 2.0 (.glb): 500 MB file | Performance | P2 | Import a 500 MB file (glTF 2.0 (.glb)). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0280 | Import glTF 2.0 (.glb): file from another vendor | Interop | P2 | Import a file from another vendor (glTF 2.0 (.glb)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0281 | Import 3MF: clean solid | Interop | P2 | Import a clean solid (3MF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0282 | Import 3MF: assembly | Interop | P2 | Import a assembly (3MF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0283 | Import 3MF: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (3MF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0284 | Import 3MF: corrupted file | Negative | P2 | Import a corrupted file (3MF). | Rejected with parse position; project untouched. |  |
| IOX-0285 | Import 3MF: inch file | Interop | P2 | Import a inch file (3MF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0286 | Import 3MF: 500 MB file | Performance | P2 | Import a 500 MB file (3MF). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0287 | Import 3MF: file from another vendor | Interop | P2 | Import a file from another vendor (3MF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0288 | Import Parasolid x_t: clean solid | Interop | P2 | Import a clean solid (Parasolid x_t). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0289 | Import Parasolid x_t: assembly | Interop | P2 | Import a assembly (Parasolid x_t). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0290 | Import Parasolid x_t: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (Parasolid x_t). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0291 | Import Parasolid x_t: corrupted file | Negative | P2 | Import a corrupted file (Parasolid x_t). | Rejected with parse position; project untouched. |  |
| IOX-0292 | Import Parasolid x_t: inch file | Interop | P2 | Import a inch file (Parasolid x_t). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0293 | Import Parasolid x_t: 500 MB file | Performance | P2 | Import a 500 MB file (Parasolid x_t). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0294 | Import Parasolid x_t: file from another vendor | Interop | P2 | Import a file from another vendor (Parasolid x_t). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0295 | Import JT: clean solid | Interop | P2 | Import a clean solid (JT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0296 | Import JT: assembly | Interop | P2 | Import a assembly (JT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0297 | Import JT: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (JT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0298 | Import JT: corrupted file | Negative | P2 | Import a corrupted file (JT). | Rejected with parse position; project untouched. |  |
| IOX-0299 | Import JT: inch file | Interop | P2 | Import a inch file (JT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0300 | Import JT: 500 MB file | Performance | P2 | Import a 500 MB file (JT). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0301 | Import JT: file from another vendor | Interop | P2 | Import a file from another vendor (JT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0302 | Import ACIS SAT: clean solid | Interop | P2 | Import a clean solid (ACIS SAT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0303 | Import ACIS SAT: assembly | Interop | P2 | Import a assembly (ACIS SAT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0304 | Import ACIS SAT: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (ACIS SAT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0305 | Import ACIS SAT: corrupted file | Negative | P2 | Import a corrupted file (ACIS SAT). | Rejected with parse position; project untouched. |  |
| IOX-0306 | Import ACIS SAT: inch file | Interop | P2 | Import a inch file (ACIS SAT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0307 | Import ACIS SAT: 500 MB file | Performance | P2 | Import a 500 MB file (ACIS SAT). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0308 | Import ACIS SAT: file from another vendor | Interop | P2 | Import a file from another vendor (ACIS SAT). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0309 | Import DXF: clean solid | Interop | P2 | Import a clean solid (DXF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0310 | Import DXF: assembly | Interop | P2 | Import a assembly (DXF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0311 | Import DXF: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (DXF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0312 | Import DXF: corrupted file | Negative | P2 | Import a corrupted file (DXF). | Rejected with parse position; project untouched. |  |
| IOX-0313 | Import DXF: inch file | Interop | P2 | Import a inch file (DXF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0314 | Import DXF: 500 MB file | Performance | P2 | Import a 500 MB file (DXF). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0315 | Import DXF: file from another vendor | Interop | P2 | Import a file from another vendor (DXF). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0316 | Import VRML: clean solid | Interop | P2 | Import a clean solid (VRML). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0317 | Import VRML: assembly | Interop | P2 | Import a assembly (VRML). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0318 | Import VRML: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (VRML). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0319 | Import VRML: corrupted file | Negative | P2 | Import a corrupted file (VRML). | Rejected with parse position; project untouched. |  |
| IOX-0320 | Import VRML: inch file | Interop | P2 | Import a inch file (VRML). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0321 | Import VRML: 500 MB file | Performance | P2 | Import a 500 MB file (VRML). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0322 | Import VRML: file from another vendor | Interop | P2 | Import a file from another vendor (VRML). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0323 | Import PLY: clean solid | Interop | P2 | Import a clean solid (PLY). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0324 | Import PLY: assembly | Interop | P2 | Import a assembly (PLY). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0325 | Import PLY: file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (PLY). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0326 | Import PLY: corrupted file | Negative | P2 | Import a corrupted file (PLY). | Rejected with parse position; project untouched. |  |
| IOX-0327 | Import PLY: inch file | Interop | P2 | Import a inch file (PLY). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0328 | Import PLY: 500 MB file | Performance | P2 | Import a 500 MB file (PLY). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0329 | Import PLY: file from another vendor | Interop | P2 | Import a file from another vendor (PLY). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0330 | Import USD (.usdz): clean solid | Interop | P2 | Import a clean solid (USD (.usdz)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0331 | Import USD (.usdz): assembly | Interop | P2 | Import a assembly (USD (.usdz)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0332 | Import USD (.usdz): file with gaps 0.05 mm | Interop | P2 | Import a file with gaps 0.05 mm (USD (.usdz)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0333 | Import USD (.usdz): corrupted file | Negative | P2 | Import a corrupted file (USD (.usdz)). | Rejected with parse position; project untouched. |  |
| IOX-0334 | Import USD (.usdz): inch file | Interop | P2 | Import a inch file (USD (.usdz)). | Imported; units converted to mm; healing report; geometry usable by features. |  |
| IOX-0335 | Import USD (.usdz): 500 MB file | Performance | P2 | Import a 500 MB file (USD (.usdz)). | Streams with progress; cancellable; memory < 3× file size. |  |
| IOX-0336 | Import USD (.usdz): file from another vendor | Interop | P2 | Import a file from another vendor (USD (.usdz)). | Imported; units converted to mm; healing report; geometry usable by features. |  |

## Round trip

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| IOX-0337 | Round trip STEP AP214: bracket | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0338 | Round trip STEP AP214: flange | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0339 | Round trip STEP AP214: loft body | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0340 | Round trip STEP AP214: sheet-metal clip | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0341 | Round trip STEP AP214: car body skin | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0342 | Round trip STEP AP214: turbofan nacelle | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0343 | Round trip STEP AP242: bracket | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0344 | Round trip STEP AP242: flange | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0345 | Round trip STEP AP242: loft body | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0346 | Round trip STEP AP242: sheet-metal clip | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0347 | Round trip STEP AP242: car body skin | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0348 | Round trip STEP AP242: turbofan nacelle | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0349 | Round trip IGES 5.3: bracket | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0350 | Round trip IGES 5.3: flange | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0351 | Round trip IGES 5.3: loft body | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0352 | Round trip IGES 5.3: sheet-metal clip | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0353 | Round trip IGES 5.3: car body skin | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0354 | Round trip IGES 5.3: turbofan nacelle | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0355 | Round trip Parasolid x_t: bracket | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0356 | Round trip Parasolid x_t: flange | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0357 | Round trip Parasolid x_t: loft body | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0358 | Round trip Parasolid x_t: sheet-metal clip | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0359 | Round trip Parasolid x_t: car body skin | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0360 | Round trip Parasolid x_t: turbofan nacelle | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0361 | Round trip JT: bracket | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0362 | Round trip JT: flange | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0363 | Round trip JT: loft body | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0364 | Round trip JT: sheet-metal clip | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0365 | Round trip JT: car body skin | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |
| IOX-0366 | Round trip JT: turbofan nacelle | Interop | P2 | Export, import, compare. | Hausdorff distance < 1e-4 mm; volume within 1e-6 rel; face count equal. |  |

## Data formats (non-geometry)

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| IOX-0367 | ReqIF 1.2: export | Interop | P2 | Export ReqIF 1.2. | Content identical after round trip. |  |
| IOX-0368 | ReqIF 1.2: import | Interop | P2 | Import ReqIF 1.2. | Content identical after round trip. |  |
| IOX-0369 | ReqIF 1.2: round trip | Interop | P2 | Round trip ReqIF 1.2. | Content identical after round trip. |  |
| IOX-0370 | ReqIF 1.2: malformed input | Negative | P2 | Malformed input ReqIF 1.2. | Rejected with a validation message. |  |
| IOX-0371 | BOM CSV: export | Interop | P2 | Export BOM CSV. | Content identical after round trip. |  |
| IOX-0372 | BOM CSV: import | Interop | P2 | Import BOM CSV. | Content identical after round trip. |  |
| IOX-0373 | BOM CSV: round trip | Interop | P2 | Round trip BOM CSV. | Content identical after round trip. |  |
| IOX-0374 | BOM CSV: malformed input | Negative | P2 | Malformed input BOM CSV. | Rejected with a validation message. |  |
| IOX-0375 | design table CSV: export | Interop | P2 | Export design table CSV. | Content identical after round trip. |  |
| IOX-0376 | design table CSV: import | Interop | P2 | Import design table CSV. | Content identical after round trip. |  |
| IOX-0377 | design table CSV: round trip | Interop | P2 | Round trip design table CSV. | Content identical after round trip. |  |
| IOX-0378 | design table CSV: malformed input | Negative | P2 | Malformed input design table CSV. | Rejected with a validation message. |  |
| IOX-0379 | project JSON: export | Interop | P2 | Export project JSON. | Content identical after round trip. |  |
| IOX-0380 | project JSON: import | Interop | P2 | Import project JSON. | Content identical after round trip. |  |
| IOX-0381 | project JSON: round trip | Interop | P2 | Round trip project JSON. | Content identical after round trip. |  |
| IOX-0382 | project JSON: malformed input | Negative | P2 | Malformed input project JSON. | Rejected with a validation message. |  |
| IOX-0383 | FMEA CSV: export | Interop | P2 | Export FMEA CSV. | Content identical after round trip. |  |
| IOX-0384 | FMEA CSV: import | Interop | P2 | Import FMEA CSV. | Content identical after round trip. |  |
| IOX-0385 | FMEA CSV: round trip | Interop | P2 | Round trip FMEA CSV. | Content identical after round trip. |  |
| IOX-0386 | FMEA CSV: malformed input | Negative | P2 | Malformed input FMEA CSV. | Rejected with a validation message. |  |
| IOX-0387 | drawing SVG: export | Interop | P2 | Export drawing SVG. | Content identical after round trip. |  |
| IOX-0388 | drawing SVG: import | Interop | P2 | Import drawing SVG. | Content identical after round trip. |  |
| IOX-0389 | drawing SVG: round trip | Interop | P2 | Round trip drawing SVG. | Content identical after round trip. |  |
| IOX-0390 | drawing SVG: malformed input | Negative | P2 | Malformed input drawing SVG. | Rejected with a validation message. |  |
