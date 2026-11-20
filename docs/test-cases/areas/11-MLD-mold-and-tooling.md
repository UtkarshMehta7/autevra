# MLD — Mold and Tooling

**CATIA-class equivalent:** Core & Cavity Design / Mold Tooling Design  
**Autevra workspace:** Production → tooling check  
**Scope:** Shared  
**Cases:** 104 (Have 36, Partial 0, Gap 68)

Draft and undercut analysis, parting, shrinkage and mold components.

[← Back to the index](../README.md)

## Features

- Draft analysis — 24 cases (Have)
- Parting and undercuts — 36 cases (Have)
- Shrinkage — 24 cases (Gap)
- Mold components — 20 cases (Gap)

## Draft analysis

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MLD-0001 | Face at -2° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face red: undercut (negative draft). |  |
| MLD-0002 | Face at -2° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face red: undercut (negative draft). |  |
| MLD-0003 | Face at -2° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face red: undercut (negative draft). |  |
| MLD-0004 | Face at 0° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0° < 0.5°. |  |
| MLD-0005 | Face at 0° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0° < 1°. |  |
| MLD-0006 | Face at 0° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0° < 2°. |  |
| MLD-0007 | Face at 0.25° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0.25° < 0.5°. |  |
| MLD-0008 | Face at 0.25° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0.25° < 1°. |  |
| MLD-0009 | Face at 0.25° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0.25° < 2°. |  |
| MLD-0010 | Face at 0.5° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0011 | Face at 0.5° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0.5° < 1°. |  |
| MLD-0012 | Face at 0.5° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 0.5° < 2°. |  |
| MLD-0013 | Face at 1° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0014 | Face at 1° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0015 | Face at 1° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 1° < 2°. |  |
| MLD-0016 | Face at 1.5° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0017 | Face at 1.5° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0018 | Face at 1.5° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face yellow: 1.5° < 2°. |  |
| MLD-0019 | Face at 3° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0020 | Face at 3° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0021 | Face at 3° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0022 | Face at 5° draft, required 0.5° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0023 | Face at 5° draft, required 1° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |
| MLD-0024 | Face at 5° draft, required 2° | Boundary | P2 | GET /parts/{id}/draft with pull direction +Z. | Face green (enough draft). |  |

## Parting and undercuts

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MLD-0025 | parting line for cup | Functional | P2 | Run parting line. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0026 | core/cavity split for cup | Functional | P2 | Run core/cavity split. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0027 | undercut detection for cup | Functional | P2 | Run undercut detection. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0028 | slider proposal for cup | Functional | P2 | Run slider proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0029 | lifter proposal for cup | Functional | P2 | Run lifter proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0030 | shut-off surfaces for cup | Functional | P2 | Run shut-off surfaces. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0031 | parting line for box with snap hook | Functional | P2 | Run parting line. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0032 | core/cavity split for box with snap hook | Functional | P2 | Run core/cavity split. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0033 | undercut detection for box with snap hook | Functional | P2 | Run undercut detection. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0034 | slider proposal for box with snap hook | Functional | P2 | Run slider proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0035 | lifter proposal for box with snap hook | Functional | P2 | Run lifter proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0036 | shut-off surfaces for box with snap hook | Functional | P2 | Run shut-off surfaces. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0037 | parting line for threaded cap | Functional | P2 | Run parting line. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0038 | core/cavity split for threaded cap | Functional | P2 | Run core/cavity split. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0039 | undercut detection for threaded cap | Functional | P2 | Run undercut detection. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0040 | slider proposal for threaded cap | Functional | P2 | Run slider proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0041 | lifter proposal for threaded cap | Functional | P2 | Run lifter proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0042 | shut-off surfaces for threaded cap | Functional | P2 | Run shut-off surfaces. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0043 | parting line for bracket with side hole | Functional | P2 | Run parting line. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0044 | core/cavity split for bracket with side hole | Functional | P2 | Run core/cavity split. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0045 | undercut detection for bracket with side hole | Functional | P2 | Run undercut detection. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0046 | slider proposal for bracket with side hole | Functional | P2 | Run slider proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0047 | lifter proposal for bracket with side hole | Functional | P2 | Run lifter proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0048 | shut-off surfaces for bracket with side hole | Functional | P2 | Run shut-off surfaces. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0049 | parting line for housing with bosses | Functional | P2 | Run parting line. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0050 | core/cavity split for housing with bosses | Functional | P2 | Run core/cavity split. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0051 | undercut detection for housing with bosses | Functional | P2 | Run undercut detection. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0052 | slider proposal for housing with bosses | Functional | P2 | Run slider proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0053 | lifter proposal for housing with bosses | Functional | P2 | Run lifter proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0054 | shut-off surfaces for housing with bosses | Functional | P2 | Run shut-off surfaces. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0055 | parting line for lens with flange | Functional | P2 | Run parting line. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0056 | core/cavity split for lens with flange | Functional | P2 | Run core/cavity split. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0057 | undercut detection for lens with flange | Functional | P2 | Run undercut detection. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0058 | slider proposal for lens with flange | Functional | P2 | Run slider proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0059 | lifter proposal for lens with flange | Functional | P2 | Run lifter proposal. | Faces classified core/cavity/undercut; split surfaces watertight. |  |
| MLD-0060 | shut-off surfaces for lens with flange | Functional | P2 | Run shut-off surfaces. | Faces classified core/cavity/undercut; split surfaces watertight. |  |

## Shrinkage

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MLD-0061 | Shrinkage ABS on 10 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 10×(1+0.005) = 10.05 mm. |  |
| MLD-0062 | Shrinkage ABS on 50 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 50×(1+0.005) = 50.25 mm. |  |
| MLD-0063 | Shrinkage ABS on 100 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 100×(1+0.005) = 100.5 mm. |  |
| MLD-0064 | Shrinkage ABS on 250 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 250×(1+0.005) = 251.25 mm. |  |
| MLD-0065 | Shrinkage PP on 10 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 10×(1+0.015) = 10.15 mm. |  |
| MLD-0066 | Shrinkage PP on 50 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 50×(1+0.015) = 50.75 mm. |  |
| MLD-0067 | Shrinkage PP on 100 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 100×(1+0.015) = 101.5 mm. |  |
| MLD-0068 | Shrinkage PP on 250 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 250×(1+0.015) = 253.75 mm. |  |
| MLD-0069 | Shrinkage PA66 on 10 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 10×(1+0.015) = 10.15 mm. |  |
| MLD-0070 | Shrinkage PA66 on 50 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 50×(1+0.015) = 50.75 mm. |  |
| MLD-0071 | Shrinkage PA66 on 100 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 100×(1+0.015) = 101.5 mm. |  |
| MLD-0072 | Shrinkage PA66 on 250 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 250×(1+0.015) = 253.75 mm. |  |
| MLD-0073 | Shrinkage PC on 10 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 10×(1+0.006) = 10.06 mm. |  |
| MLD-0074 | Shrinkage PC on 50 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 50×(1+0.006) = 50.3 mm. |  |
| MLD-0075 | Shrinkage PC on 100 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 100×(1+0.006) = 100.6 mm. |  |
| MLD-0076 | Shrinkage PC on 250 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 250×(1+0.006) = 251.5 mm. |  |
| MLD-0077 | Shrinkage POM on 10 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 10×(1+0.02) = 10.2 mm. |  |
| MLD-0078 | Shrinkage POM on 50 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 50×(1+0.02) = 51 mm. |  |
| MLD-0079 | Shrinkage POM on 100 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 100×(1+0.02) = 102 mm. |  |
| MLD-0080 | Shrinkage POM on 250 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 250×(1+0.02) = 255 mm. |  |
| MLD-0081 | Shrinkage PBT GF30 on 10 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 10×(1+0.004) = 10.04 mm. |  |
| MLD-0082 | Shrinkage PBT GF30 on 50 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 50×(1+0.004) = 50.2 mm. |  |
| MLD-0083 | Shrinkage PBT GF30 on 100 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 100×(1+0.004) = 100.4 mm. |  |
| MLD-0084 | Shrinkage PBT GF30 on 250 mm | Accuracy | P2 | Apply isotropic shrinkage to the cavity. | Cavity dimension = 250×(1+0.004) = 251 mm. |  |

## Mold components

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MLD-0085 | mold base (standard plates): insert | Functional | P2 | insert for mold base (standard plates). | Placed from catalogue; clashes reported. |  |
| MLD-0086 | mold base (standard plates): clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for mold base (standard plates). | Placed from catalogue; clashes reported. |  |
| MLD-0087 | sprue bushing: insert | Functional | P2 | insert for sprue bushing. | Placed from catalogue; clashes reported. |  |
| MLD-0088 | sprue bushing: clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for sprue bushing. | Placed from catalogue; clashes reported. |  |
| MLD-0089 | runner (round Ø6): insert | Functional | P2 | insert for runner (round Ø6). | Placed from catalogue; clashes reported. |  |
| MLD-0090 | runner (round Ø6): clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for runner (round Ø6). | Placed from catalogue; clashes reported. |  |
| MLD-0091 | gate (edge): insert | Functional | P2 | insert for gate (edge). | Placed from catalogue; clashes reported. |  |
| MLD-0092 | gate (edge): clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for gate (edge). | Placed from catalogue; clashes reported. |  |
| MLD-0093 | gate (pin): insert | Functional | P2 | insert for gate (pin). | Placed from catalogue; clashes reported. |  |
| MLD-0094 | gate (pin): clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for gate (pin). | Placed from catalogue; clashes reported. |  |
| MLD-0095 | ejector pins ×8: insert | Functional | P2 | insert for ejector pins ×8. | Placed from catalogue; clashes reported. |  |
| MLD-0096 | ejector pins ×8: clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for ejector pins ×8. | Placed from catalogue; clashes reported. |  |
| MLD-0097 | cooling channels Ø8: insert | Functional | P2 | insert for cooling channels Ø8. | Placed from catalogue; clashes reported. |  |
| MLD-0098 | cooling channels Ø8: clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for cooling channels Ø8. | Placed from catalogue; clashes reported. |  |
| MLD-0099 | baffles: insert | Functional | P2 | insert for baffles. | Placed from catalogue; clashes reported. |  |
| MLD-0100 | baffles: clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for baffles. | Placed from catalogue; clashes reported. |  |
| MLD-0101 | guide pins: insert | Functional | P2 | insert for guide pins. | Placed from catalogue; clashes reported. |  |
| MLD-0102 | guide pins: clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for guide pins. | Placed from catalogue; clashes reported. |  |
| MLD-0103 | locating ring: insert | Functional | P2 | insert for locating ring. | Placed from catalogue; clashes reported. |  |
| MLD-0104 | locating ring: clearance to cavity ≥ 2×Ø | Functional | P2 | clearance to cavity ≥ 2×Ø for locating ring. | Placed from catalogue; clashes reported. |  |
