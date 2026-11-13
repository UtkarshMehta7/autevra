# SMD — Sheet Metal Design

**CATIA-class equivalent:** Generative Sheetmetal Design  
**Autevra workspace:** Part Design (SheetMetal feature)  
**Scope:** Shared  
**Cases:** 275 (Have 135, Partial 60, Gap 80)

Walls, flanges, bends, unfolding and flat-pattern accuracy (K-factor bend allowance).

[← Back to the index](../README.md)

## Features

- Bend allowance and flat length — 135 cases (Have)
- Manufacturability rules — 60 cases (Partial)
- Sheet-metal features — 80 cases (Gap)

## Bend allowance and flat length

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SMD-0001 | Bend t=1, R=1, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.04458 mm; flat length = 100 + BA = 101.045 mm. | t=1, R=1, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0002 | Bend t=1, R=1, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.08916 mm; flat length = 100 + BA = 102.089 mm. | t=1, R=1, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0003 | Bend t=1, R=1, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.13374 mm; flat length = 100 + BA = 103.134 mm. | t=1, R=1, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0004 | Bend t=1, R=1, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.13097 mm; flat length = 100 + BA = 101.131 mm. | t=1, R=1, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0005 | Bend t=1, R=1, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.26195 mm; flat length = 100 + BA = 102.262 mm. | t=1, R=1, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0006 | Bend t=1, R=1, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.39292 mm; flat length = 100 + BA = 103.393 mm. | t=1, R=1, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0007 | Bend t=1, R=1, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.1781 mm; flat length = 100 + BA = 101.178 mm. | t=1, R=1, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0008 | Bend t=1, R=1, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.35619 mm; flat length = 100 + BA = 102.356 mm. | t=1, R=1, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0009 | Bend t=1, R=1, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.53429 mm; flat length = 100 + BA = 103.534 mm. | t=1, R=1, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0010 | Bend t=1, R=2, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.82998 mm; flat length = 100 + BA = 101.83 mm. | t=1, R=2, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0011 | Bend t=1, R=2, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.65996 mm; flat length = 100 + BA = 103.66 mm. | t=1, R=2, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0012 | Bend t=1, R=2, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.48993 mm; flat length = 100 + BA = 105.49 mm. | t=1, R=2, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0013 | Bend t=1, R=2, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.91637 mm; flat length = 100 + BA = 101.916 mm. | t=1, R=2, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0014 | Bend t=1, R=2, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.83274 mm; flat length = 100 + BA = 103.833 mm. | t=1, R=2, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0015 | Bend t=1, R=2, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.74911 mm; flat length = 100 + BA = 105.749 mm. | t=1, R=2, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0016 | Bend t=1, R=2, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.9635 mm; flat length = 100 + BA = 101.963 mm. | t=1, R=2, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0017 | Bend t=1, R=2, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.92699 mm; flat length = 100 + BA = 103.927 mm. | t=1, R=2, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0018 | Bend t=1, R=2, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.89049 mm; flat length = 100 + BA = 105.89 mm. | t=1, R=2, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0019 | Bend t=1, R=5, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.18617 mm; flat length = 100 + BA = 104.186 mm. | t=1, R=5, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0020 | Bend t=1, R=5, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.37234 mm; flat length = 100 + BA = 108.372 mm. | t=1, R=5, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0021 | Bend t=1, R=5, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 12.5585 mm; flat length = 100 + BA = 112.559 mm. | t=1, R=5, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0022 | Bend t=1, R=5, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.27257 mm; flat length = 100 + BA = 104.273 mm. | t=1, R=5, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0023 | Bend t=1, R=5, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.54513 mm; flat length = 100 + BA = 108.545 mm. | t=1, R=5, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0024 | Bend t=1, R=5, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 12.8177 mm; flat length = 100 + BA = 112.818 mm. | t=1, R=5, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0025 | Bend t=1, R=5, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.31969 mm; flat length = 100 + BA = 104.32 mm. | t=1, R=5, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0026 | Bend t=1, R=5, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.63938 mm; flat length = 100 + BA = 108.639 mm. | t=1, R=5, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0027 | Bend t=1, R=5, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 12.9591 mm; flat length = 100 + BA = 112.959 mm. | t=1, R=5, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0028 | Bend t=1.5, R=1, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.17417 mm; flat length = 100 + BA = 101.174 mm. | t=1.5, R=1, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0029 | Bend t=1.5, R=1, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.34834 mm; flat length = 100 + BA = 102.348 mm. | t=1.5, R=1, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0030 | Bend t=1.5, R=1, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.52251 mm; flat length = 100 + BA = 103.523 mm. | t=1.5, R=1, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0031 | Bend t=1.5, R=1, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.30376 mm; flat length = 100 + BA = 101.304 mm. | t=1.5, R=1, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0032 | Bend t=1.5, R=1, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.60752 mm; flat length = 100 + BA = 102.608 mm. | t=1.5, R=1, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0033 | Bend t=1.5, R=1, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.91128 mm; flat length = 100 + BA = 103.911 mm. | t=1.5, R=1, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0034 | Bend t=1.5, R=1, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.37445 mm; flat length = 100 + BA = 101.374 mm. | t=1.5, R=1, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0035 | Bend t=1.5, R=1, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.74889 mm; flat length = 100 + BA = 102.749 mm. | t=1.5, R=1, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0036 | Bend t=1.5, R=1, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.12334 mm; flat length = 100 + BA = 104.123 mm. | t=1.5, R=1, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0037 | Bend t=1.5, R=2, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.95957 mm; flat length = 100 + BA = 101.96 mm. | t=1.5, R=2, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0038 | Bend t=1.5, R=2, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.91914 mm; flat length = 100 + BA = 103.919 mm. | t=1.5, R=2, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0039 | Bend t=1.5, R=2, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.87871 mm; flat length = 100 + BA = 105.879 mm. | t=1.5, R=2, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0040 | Bend t=1.5, R=2, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.08916 mm; flat length = 100 + BA = 102.089 mm. | t=1.5, R=2, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0041 | Bend t=1.5, R=2, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.17832 mm; flat length = 100 + BA = 104.178 mm. | t=1.5, R=2, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0042 | Bend t=1.5, R=2, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 6.26748 mm; flat length = 100 + BA = 106.267 mm. | t=1.5, R=2, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0043 | Bend t=1.5, R=2, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.15984 mm; flat length = 100 + BA = 102.16 mm. | t=1.5, R=2, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0044 | Bend t=1.5, R=2, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.31969 mm; flat length = 100 + BA = 104.32 mm. | t=1.5, R=2, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0045 | Bend t=1.5, R=2, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 6.47953 mm; flat length = 100 + BA = 106.48 mm. | t=1.5, R=2, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0046 | Bend t=1.5, R=5, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.31576 mm; flat length = 100 + BA = 104.316 mm. | t=1.5, R=5, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0047 | Bend t=1.5, R=5, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.63153 mm; flat length = 100 + BA = 108.632 mm. | t=1.5, R=5, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0048 | Bend t=1.5, R=5, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 12.9473 mm; flat length = 100 + BA = 112.947 mm. | t=1.5, R=5, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0049 | Bend t=1.5, R=5, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.44535 mm; flat length = 100 + BA = 104.445 mm. | t=1.5, R=5, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0050 | Bend t=1.5, R=5, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.89071 mm; flat length = 100 + BA = 108.891 mm. | t=1.5, R=5, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0051 | Bend t=1.5, R=5, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 13.3361 mm; flat length = 100 + BA = 113.336 mm. | t=1.5, R=5, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0052 | Bend t=1.5, R=5, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.51604 mm; flat length = 100 + BA = 104.516 mm. | t=1.5, R=5, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0053 | Bend t=1.5, R=5, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.03208 mm; flat length = 100 + BA = 109.032 mm. | t=1.5, R=5, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0054 | Bend t=1.5, R=5, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 13.5481 mm; flat length = 100 + BA = 113.548 mm. | t=1.5, R=5, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0055 | Bend t=2, R=1, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.30376 mm; flat length = 100 + BA = 101.304 mm. | t=2, R=1, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0056 | Bend t=2, R=1, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.60752 mm; flat length = 100 + BA = 102.608 mm. | t=2, R=1, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0057 | Bend t=2, R=1, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.91128 mm; flat length = 100 + BA = 103.911 mm. | t=2, R=1, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0058 | Bend t=2, R=1, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.47655 mm; flat length = 100 + BA = 101.477 mm. | t=2, R=1, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0059 | Bend t=2, R=1, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.9531 mm; flat length = 100 + BA = 102.953 mm. | t=2, R=1, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0060 | Bend t=2, R=1, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.42965 mm; flat length = 100 + BA = 104.43 mm. | t=2, R=1, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0061 | Bend t=2, R=1, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.5708 mm; flat length = 100 + BA = 101.571 mm. | t=2, R=1, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0062 | Bend t=2, R=1, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.14159 mm; flat length = 100 + BA = 103.142 mm. | t=2, R=1, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0063 | Bend t=2, R=1, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.71239 mm; flat length = 100 + BA = 104.712 mm. | t=2, R=1, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0064 | Bend t=2, R=2, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.08916 mm; flat length = 100 + BA = 102.089 mm. | t=2, R=2, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0065 | Bend t=2, R=2, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.17832 mm; flat length = 100 + BA = 104.178 mm. | t=2, R=2, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0066 | Bend t=2, R=2, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 6.26748 mm; flat length = 100 + BA = 106.267 mm. | t=2, R=2, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0067 | Bend t=2, R=2, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.26195 mm; flat length = 100 + BA = 102.262 mm. | t=2, R=2, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0068 | Bend t=2, R=2, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.52389 mm; flat length = 100 + BA = 104.524 mm. | t=2, R=2, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0069 | Bend t=2, R=2, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 6.78584 mm; flat length = 100 + BA = 106.786 mm. | t=2, R=2, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0070 | Bend t=2, R=2, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.35619 mm; flat length = 100 + BA = 102.356 mm. | t=2, R=2, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0071 | Bend t=2, R=2, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.71239 mm; flat length = 100 + BA = 104.712 mm. | t=2, R=2, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0072 | Bend t=2, R=2, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 7.06858 mm; flat length = 100 + BA = 107.069 mm. | t=2, R=2, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0073 | Bend t=2, R=5, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.44535 mm; flat length = 100 + BA = 104.445 mm. | t=2, R=5, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0074 | Bend t=2, R=5, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.89071 mm; flat length = 100 + BA = 108.891 mm. | t=2, R=5, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0075 | Bend t=2, R=5, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 13.3361 mm; flat length = 100 + BA = 113.336 mm. | t=2, R=5, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0076 | Bend t=2, R=5, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.61814 mm; flat length = 100 + BA = 104.618 mm. | t=2, R=5, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0077 | Bend t=2, R=5, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.23628 mm; flat length = 100 + BA = 109.236 mm. | t=2, R=5, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0078 | Bend t=2, R=5, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 13.8544 mm; flat length = 100 + BA = 113.854 mm. | t=2, R=5, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0079 | Bend t=2, R=5, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.71239 mm; flat length = 100 + BA = 104.712 mm. | t=2, R=5, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0080 | Bend t=2, R=5, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.42478 mm; flat length = 100 + BA = 109.425 mm. | t=2, R=5, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0081 | Bend t=2, R=5, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 14.1372 mm; flat length = 100 + BA = 114.137 mm. | t=2, R=5, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0082 | Bend t=3, R=1, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.56294 mm; flat length = 100 + BA = 101.563 mm. | t=3, R=1, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0083 | Bend t=3, R=1, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.12588 mm; flat length = 100 + BA = 103.126 mm. | t=3, R=1, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0084 | Bend t=3, R=1, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.68883 mm; flat length = 100 + BA = 104.689 mm. | t=3, R=1, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0085 | Bend t=3, R=1, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.82212 mm; flat length = 100 + BA = 101.822 mm. | t=3, R=1, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0086 | Bend t=3, R=1, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.64425 mm; flat length = 100 + BA = 103.644 mm. | t=3, R=1, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0087 | Bend t=3, R=1, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.46637 mm; flat length = 100 + BA = 105.466 mm. | t=3, R=1, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0088 | Bend t=3, R=1, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.9635 mm; flat length = 100 + BA = 101.963 mm. | t=3, R=1, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0089 | Bend t=3, R=1, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.92699 mm; flat length = 100 + BA = 103.927 mm. | t=3, R=1, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0090 | Bend t=3, R=1, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.89049 mm; flat length = 100 + BA = 105.89 mm. | t=3, R=1, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0091 | Bend t=3, R=2, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.34834 mm; flat length = 100 + BA = 102.348 mm. | t=3, R=2, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0092 | Bend t=3, R=2, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.69668 mm; flat length = 100 + BA = 104.697 mm. | t=3, R=2, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0093 | Bend t=3, R=2, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 7.04502 mm; flat length = 100 + BA = 107.045 mm. | t=3, R=2, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0094 | Bend t=3, R=2, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.60752 mm; flat length = 100 + BA = 102.608 mm. | t=3, R=2, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0095 | Bend t=3, R=2, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.21504 mm; flat length = 100 + BA = 105.215 mm. | t=3, R=2, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0096 | Bend t=3, R=2, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 7.82257 mm; flat length = 100 + BA = 107.823 mm. | t=3, R=2, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0097 | Bend t=3, R=2, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.74889 mm; flat length = 100 + BA = 102.749 mm. | t=3, R=2, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0098 | Bend t=3, R=2, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.49779 mm; flat length = 100 + BA = 105.498 mm. | t=3, R=2, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0099 | Bend t=3, R=2, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.24668 mm; flat length = 100 + BA = 108.247 mm. | t=3, R=2, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0100 | Bend t=3, R=5, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.70453 mm; flat length = 100 + BA = 104.705 mm. | t=3, R=5, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0101 | Bend t=3, R=5, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.40907 mm; flat length = 100 + BA = 109.409 mm. | t=3, R=5, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0102 | Bend t=3, R=5, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 14.1136 mm; flat length = 100 + BA = 114.114 mm. | t=3, R=5, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0103 | Bend t=3, R=5, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.96372 mm; flat length = 100 + BA = 104.964 mm. | t=3, R=5, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0104 | Bend t=3, R=5, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.92743 mm; flat length = 100 + BA = 109.927 mm. | t=3, R=5, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0105 | Bend t=3, R=5, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 14.8911 mm; flat length = 100 + BA = 114.891 mm. | t=3, R=5, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0106 | Bend t=3, R=5, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.10509 mm; flat length = 100 + BA = 105.105 mm. | t=3, R=5, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0107 | Bend t=3, R=5, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 10.2102 mm; flat length = 100 + BA = 110.21 mm. | t=3, R=5, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0108 | Bend t=3, R=5, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 15.3153 mm; flat length = 100 + BA = 115.315 mm. | t=3, R=5, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0109 | Bend t=4, R=1, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 1.82212 mm; flat length = 100 + BA = 101.822 mm. | t=4, R=1, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0110 | Bend t=4, R=1, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.64425 mm; flat length = 100 + BA = 103.644 mm. | t=4, R=1, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0111 | Bend t=4, R=1, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.46637 mm; flat length = 100 + BA = 105.466 mm. | t=4, R=1, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0112 | Bend t=4, R=1, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.1677 mm; flat length = 100 + BA = 102.168 mm. | t=4, R=1, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0113 | Bend t=4, R=1, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.3354 mm; flat length = 100 + BA = 104.335 mm. | t=4, R=1, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0114 | Bend t=4, R=1, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 6.5031 mm; flat length = 100 + BA = 106.503 mm. | t=4, R=1, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0115 | Bend t=4, R=1, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.35619 mm; flat length = 100 + BA = 102.356 mm. | t=4, R=1, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0116 | Bend t=4, R=1, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.71239 mm; flat length = 100 + BA = 104.712 mm. | t=4, R=1, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0117 | Bend t=4, R=1, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 7.06858 mm; flat length = 100 + BA = 107.069 mm. | t=4, R=1, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0118 | Bend t=4, R=2, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.60752 mm; flat length = 100 + BA = 102.608 mm. | t=4, R=2, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0119 | Bend t=4, R=2, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.21504 mm; flat length = 100 + BA = 105.215 mm. | t=4, R=2, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0120 | Bend t=4, R=2, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 7.82257 mm; flat length = 100 + BA = 107.823 mm. | t=4, R=2, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0121 | Bend t=4, R=2, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 2.9531 mm; flat length = 100 + BA = 102.953 mm. | t=4, R=2, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0122 | Bend t=4, R=2, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.90619 mm; flat length = 100 + BA = 105.906 mm. | t=4, R=2, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0123 | Bend t=4, R=2, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 8.85929 mm; flat length = 100 + BA = 108.859 mm. | t=4, R=2, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0124 | Bend t=4, R=2, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 3.14159 mm; flat length = 100 + BA = 103.142 mm. | t=4, R=2, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0125 | Bend t=4, R=2, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 6.28319 mm; flat length = 100 + BA = 106.283 mm. | t=4, R=2, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0126 | Bend t=4, R=2, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.42478 mm; flat length = 100 + BA = 109.425 mm. | t=4, R=2, K=0.5, θ=135; BA = θ(R + K t) |
| SMD-0127 | Bend t=4, R=5, K=0.33, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 4.96372 mm; flat length = 100 + BA = 104.964 mm. | t=4, R=5, K=0.33, θ=45; BA = θ(R + K t) |
| SMD-0128 | Bend t=4, R=5, K=0.33, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 9.92743 mm; flat length = 100 + BA = 109.927 mm. | t=4, R=5, K=0.33, θ=90; BA = θ(R + K t) |
| SMD-0129 | Bend t=4, R=5, K=0.33, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 14.8911 mm; flat length = 100 + BA = 114.891 mm. | t=4, R=5, K=0.33, θ=135; BA = θ(R + K t) |
| SMD-0130 | Bend t=4, R=5, K=0.44, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.30929 mm; flat length = 100 + BA = 105.309 mm. | t=4, R=5, K=0.44, θ=45; BA = θ(R + K t) |
| SMD-0131 | Bend t=4, R=5, K=0.44, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 10.6186 mm; flat length = 100 + BA = 110.619 mm. | t=4, R=5, K=0.44, θ=90; BA = θ(R + K t) |
| SMD-0132 | Bend t=4, R=5, K=0.44, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 15.9279 mm; flat length = 100 + BA = 115.928 mm. | t=4, R=5, K=0.44, θ=135; BA = θ(R + K t) |
| SMD-0133 | Bend t=4, R=5, K=0.5, θ=45° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 5.49779 mm; flat length = 100 + BA = 105.498 mm. | t=4, R=5, K=0.5, θ=45; BA = θ(R + K t) |
| SMD-0134 | Bend t=4, R=5, K=0.5, θ=90° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 10.9956 mm; flat length = 100 + BA = 110.996 mm. | t=4, R=5, K=0.5, θ=90; BA = θ(R + K t) |
| SMD-0135 | Bend t=4, R=5, K=0.5, θ=135° | Accuracy | P1 | Two 50 mm flanges (to tangent) with one bend; unfold. | BA = π·θ/180·(R + K·t) = 16.4934 mm; flat length = 100 + BA = 116.493 mm. | t=4, R=5, K=0.5, θ=135; BA = θ(R + K t) |

## Manufacturability rules

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SMD-0136 | mild steel DC01: t=1, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0137 | mild steel DC01: t=1, R=1 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0138 | mild steel DC01: t=1, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0139 | mild steel DC01: t=1, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0140 | mild steel DC01: t=1, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0141 | mild steel DC01: t=2, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 0.5·t = 1 mm for mild steel DC01. |  |
| SMD-0142 | mild steel DC01: t=2, R=1 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0143 | mild steel DC01: t=2, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0144 | mild steel DC01: t=2, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0145 | mild steel DC01: t=2, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0146 | mild steel DC01: t=3, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 0.5·t = 1.5 mm for mild steel DC01. |  |
| SMD-0147 | mild steel DC01: t=3, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 0.5·t = 1.5 mm for mild steel DC01. |  |
| SMD-0148 | mild steel DC01: t=3, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0149 | mild steel DC01: t=3, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0150 | mild steel DC01: t=3, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0151 | stainless 304: t=1, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 1 mm for stainless 304. |  |
| SMD-0152 | stainless 304: t=1, R=1 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0153 | stainless 304: t=1, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0154 | stainless 304: t=1, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0155 | stainless 304: t=1, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0156 | stainless 304: t=2, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 2 mm for stainless 304. |  |
| SMD-0157 | stainless 304: t=2, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 2 mm for stainless 304. |  |
| SMD-0158 | stainless 304: t=2, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0159 | stainless 304: t=2, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0160 | stainless 304: t=2, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0161 | stainless 304: t=3, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 3 mm for stainless 304. |  |
| SMD-0162 | stainless 304: t=3, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 3 mm for stainless 304. |  |
| SMD-0163 | stainless 304: t=3, R=2 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 3 mm for stainless 304. |  |
| SMD-0164 | stainless 304: t=3, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0165 | stainless 304: t=3, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0166 | Al 5052-H32: t=1, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 1 mm for Al 5052-H32. |  |
| SMD-0167 | Al 5052-H32: t=1, R=1 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0168 | Al 5052-H32: t=1, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0169 | Al 5052-H32: t=1, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0170 | Al 5052-H32: t=1, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0171 | Al 5052-H32: t=2, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 2 mm for Al 5052-H32. |  |
| SMD-0172 | Al 5052-H32: t=2, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 2 mm for Al 5052-H32. |  |
| SMD-0173 | Al 5052-H32: t=2, R=2 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0174 | Al 5052-H32: t=2, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0175 | Al 5052-H32: t=2, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0176 | Al 5052-H32: t=3, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 3 mm for Al 5052-H32. |  |
| SMD-0177 | Al 5052-H32: t=3, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 3 mm for Al 5052-H32. |  |
| SMD-0178 | Al 5052-H32: t=3, R=2 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 1.0·t = 3 mm for Al 5052-H32. |  |
| SMD-0179 | Al 5052-H32: t=3, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0180 | Al 5052-H32: t=3, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0181 | Al 6061-T6: t=1, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 2.5 mm for Al 6061-T6. |  |
| SMD-0182 | Al 6061-T6: t=1, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 2.5 mm for Al 6061-T6. |  |
| SMD-0183 | Al 6061-T6: t=1, R=2 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 2.5 mm for Al 6061-T6. |  |
| SMD-0184 | Al 6061-T6: t=1, R=4 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0185 | Al 6061-T6: t=1, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0186 | Al 6061-T6: t=2, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 5 mm for Al 6061-T6. |  |
| SMD-0187 | Al 6061-T6: t=2, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 5 mm for Al 6061-T6. |  |
| SMD-0188 | Al 6061-T6: t=2, R=2 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 5 mm for Al 6061-T6. |  |
| SMD-0189 | Al 6061-T6: t=2, R=4 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 5 mm for Al 6061-T6. |  |
| SMD-0190 | Al 6061-T6: t=2, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |
| SMD-0191 | Al 6061-T6: t=3, R=0.5 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 7.5 mm for Al 6061-T6. |  |
| SMD-0192 | Al 6061-T6: t=3, R=1 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 7.5 mm for Al 6061-T6. |  |
| SMD-0193 | Al 6061-T6: t=3, R=2 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 7.5 mm for Al 6061-T6. |  |
| SMD-0194 | Al 6061-T6: t=3, R=4 | Boundary | P2 | Check minimum inside bend radius. | Flag: R < 2.5·t = 7.5 mm for Al 6061-T6. |  |
| SMD-0195 | Al 6061-T6: t=3, R=8 | Boundary | P2 | Check minimum inside bend radius. | Pass. |  |

## Sheet-metal features

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SMD-0196 | wall on edge: build | Functional | P2 | Create wall on edge; build. | Valid solid; thickness constant. |  |
| SMD-0197 | wall on edge: unfold | Functional | P2 | Create wall on edge; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0198 | wall on edge: refold | Functional | P2 | Create wall on edge; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0199 | wall on edge: flat-pattern DXF | Functional | P2 | Create wall on edge; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0200 | flange: build | Functional | P2 | Create flange; build. | Valid solid; thickness constant. |  |
| SMD-0201 | flange: unfold | Functional | P2 | Create flange; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0202 | flange: refold | Functional | P2 | Create flange; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0203 | flange: flat-pattern DXF | Functional | P2 | Create flange; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0204 | hem (closed): build | Functional | P2 | Create hem (closed); build. | Valid solid; thickness constant. |  |
| SMD-0205 | hem (closed): unfold | Functional | P2 | Create hem (closed); unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0206 | hem (closed): refold | Functional | P2 | Create hem (closed); refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0207 | hem (closed): flat-pattern DXF | Functional | P2 | Create hem (closed); flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0208 | hem (open 1 mm): build | Functional | P2 | Create hem (open 1 mm); build. | Valid solid; thickness constant. |  |
| SMD-0209 | hem (open 1 mm): unfold | Functional | P2 | Create hem (open 1 mm); unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0210 | hem (open 1 mm): refold | Functional | P2 | Create hem (open 1 mm); refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0211 | hem (open 1 mm): flat-pattern DXF | Functional | P2 | Create hem (open 1 mm); flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0212 | tear-drop: build | Functional | P2 | Create tear-drop; build. | Valid solid; thickness constant. |  |
| SMD-0213 | tear-drop: unfold | Functional | P2 | Create tear-drop; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0214 | tear-drop: refold | Functional | P2 | Create tear-drop; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0215 | tear-drop: flat-pattern DXF | Functional | P2 | Create tear-drop; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0216 | swept flange: build | Functional | P2 | Create swept flange; build. | Valid solid; thickness constant. |  |
| SMD-0217 | swept flange: unfold | Functional | P2 | Create swept flange; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0218 | swept flange: refold | Functional | P2 | Create swept flange; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0219 | swept flange: flat-pattern DXF | Functional | P2 | Create swept flange; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0220 | jog: build | Functional | P2 | Create jog; build. | Valid solid; thickness constant. |  |
| SMD-0221 | jog: unfold | Functional | P2 | Create jog; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0222 | jog: refold | Functional | P2 | Create jog; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0223 | jog: flat-pattern DXF | Functional | P2 | Create jog; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0224 | bend from flat: build | Functional | P2 | Create bend from flat; build. | Valid solid; thickness constant. |  |
| SMD-0225 | bend from flat: unfold | Functional | P2 | Create bend from flat; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0226 | bend from flat: refold | Functional | P2 | Create bend from flat; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0227 | bend from flat: flat-pattern DXF | Functional | P2 | Create bend from flat; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0228 | corner relief (round): build | Functional | P2 | Create corner relief (round); build. | Valid solid; thickness constant. |  |
| SMD-0229 | corner relief (round): unfold | Functional | P2 | Create corner relief (round); unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0230 | corner relief (round): refold | Functional | P2 | Create corner relief (round); refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0231 | corner relief (round): flat-pattern DXF | Functional | P2 | Create corner relief (round); flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0232 | corner relief (square): build | Functional | P2 | Create corner relief (square); build. | Valid solid; thickness constant. |  |
| SMD-0233 | corner relief (square): unfold | Functional | P2 | Create corner relief (square); unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0234 | corner relief (square): refold | Functional | P2 | Create corner relief (square); refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0235 | corner relief (square): flat-pattern DXF | Functional | P2 | Create corner relief (square); flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0236 | bend relief (obround): build | Functional | P2 | Create bend relief (obround); build. | Valid solid; thickness constant. |  |
| SMD-0237 | bend relief (obround): unfold | Functional | P2 | Create bend relief (obround); unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0238 | bend relief (obround): refold | Functional | P2 | Create bend relief (obround); refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0239 | bend relief (obround): flat-pattern DXF | Functional | P2 | Create bend relief (obround); flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0240 | cut-out across bend: build | Functional | P2 | Create cut-out across bend; build. | Valid solid; thickness constant. |  |
| SMD-0241 | cut-out across bend: unfold | Functional | P2 | Create cut-out across bend; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0242 | cut-out across bend: refold | Functional | P2 | Create cut-out across bend; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0243 | cut-out across bend: flat-pattern DXF | Functional | P2 | Create cut-out across bend; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0244 | louver: build | Functional | P2 | Create louver; build. | Valid solid; thickness constant. |  |
| SMD-0245 | louver: unfold | Functional | P2 | Create louver; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0246 | louver: refold | Functional | P2 | Create louver; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0247 | louver: flat-pattern DXF | Functional | P2 | Create louver; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0248 | bead: build | Functional | P2 | Create bead; build. | Valid solid; thickness constant. |  |
| SMD-0249 | bead: unfold | Functional | P2 | Create bead; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0250 | bead: refold | Functional | P2 | Create bead; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0251 | bead: flat-pattern DXF | Functional | P2 | Create bead; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0252 | bridge: build | Functional | P2 | Create bridge; build. | Valid solid; thickness constant. |  |
| SMD-0253 | bridge: unfold | Functional | P2 | Create bridge; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0254 | bridge: refold | Functional | P2 | Create bridge; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0255 | bridge: flat-pattern DXF | Functional | P2 | Create bridge; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0256 | extruded hole: build | Functional | P2 | Create extruded hole; build. | Valid solid; thickness constant. |  |
| SMD-0257 | extruded hole: unfold | Functional | P2 | Create extruded hole; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0258 | extruded hole: refold | Functional | P2 | Create extruded hole; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0259 | extruded hole: flat-pattern DXF | Functional | P2 | Create extruded hole; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0260 | curve stamp: build | Functional | P2 | Create curve stamp; build. | Valid solid; thickness constant. |  |
| SMD-0261 | curve stamp: unfold | Functional | P2 | Create curve stamp; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0262 | curve stamp: refold | Functional | P2 | Create curve stamp; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0263 | curve stamp: flat-pattern DXF | Functional | P2 | Create curve stamp; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0264 | dimple: build | Functional | P2 | Create dimple; build. | Valid solid; thickness constant. |  |
| SMD-0265 | dimple: unfold | Functional | P2 | Create dimple; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0266 | dimple: refold | Functional | P2 | Create dimple; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0267 | dimple: flat-pattern DXF | Functional | P2 | Create dimple; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0268 | cross-break: build | Functional | P2 | Create cross-break; build. | Valid solid; thickness constant. |  |
| SMD-0269 | cross-break: unfold | Functional | P2 | Create cross-break; unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0270 | cross-break: refold | Functional | P2 | Create cross-break; refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0271 | cross-break: flat-pattern DXF | Functional | P2 | Create cross-break; flat-pattern DXF. | Outline + bend lines on separate layers. |  |
| SMD-0272 | rolled wall (cone): build | Functional | P2 | Create rolled wall (cone); build. | Valid solid; thickness constant. |  |
| SMD-0273 | rolled wall (cone): unfold | Functional | P2 | Create rolled wall (cone); unfold. | Flat pattern with no overlaps; area conserved (neutral fibre). |  |
| SMD-0274 | rolled wall (cone): refold | Functional | P2 | Create rolled wall (cone); refold. | Identical to original (< 1e-6 mm). |  |
| SMD-0275 | rolled wall (cone): flat-pattern DXF | Functional | P2 | Create rolled wall (cone); flat-pattern DXF. | Outline + bend lines on separate layers. |  |
