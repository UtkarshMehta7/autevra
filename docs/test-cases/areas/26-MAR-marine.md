# MAR — Marine

**CATIA-class equivalent:** Ship design extensions (hull form, hydrostatics, structure)  
**Autevra workspace:** Vessel; Loads  
**Scope:** Marine  
**Cases:** 188 (Have 164, Partial 0, Gap 24)

Hydrostatics, stability against IMO criteria and resistance.

[← Back to the index](../README.md)

## Features

- Box-barge hydrostatics — 27 cases (Have)
- Ship-shape displacement — 96 cases (Have)
- IMO intact stability — 21 cases (Have)
- Resistance — 20 cases (Have)
- Marine features to add — 24 cases (Gap)

## Box-barge hydrostatics

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAR-0001 | Box barge L=20, B=6, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 184.5 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 2 m; KM = 2.75 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0002 | Box barge L=20, B=6, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 369 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 1 m; KM = 2.5 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0003 | Box barge L=20, B=6, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 615 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 0.6 m; KM = 3.1 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0004 | Box barge L=20, B=10, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 307.5 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 5.556 m; KM = 6.306 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0005 | Box barge L=20, B=10, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 615 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 2.778 m; KM = 4.278 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0006 | Box barge L=20, B=10, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1025 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 1.667 m; KM = 4.167 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0007 | Box barge L=20, B=16, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 492 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 14.22 m; KM = 14.97 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0008 | Box barge L=20, B=16, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 984 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 7.111 m; KM = 8.611 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0009 | Box barge L=20, B=16, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1640 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 4.267 m; KM = 6.767 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0010 | Box barge L=50, B=6, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 461.25 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 2 m; KM = 2.75 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0011 | Box barge L=50, B=6, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 922.5 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 1 m; KM = 2.5 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0012 | Box barge L=50, B=6, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1537.5 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 0.6 m; KM = 3.1 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0013 | Box barge L=50, B=10, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 768.75 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 5.556 m; KM = 6.306 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0014 | Box barge L=50, B=10, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1537.5 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 2.778 m; KM = 4.278 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0015 | Box barge L=50, B=10, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 2562.5 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 1.667 m; KM = 4.167 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0016 | Box barge L=50, B=16, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1230 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 14.22 m; KM = 14.97 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0017 | Box barge L=50, B=16, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 2460 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 7.111 m; KM = 8.611 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0018 | Box barge L=50, B=16, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 4100 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 4.267 m; KM = 6.767 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0019 | Box barge L=100, B=6, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 922.5 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 2 m; KM = 2.75 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0020 | Box barge L=100, B=6, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1845 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 1 m; KM = 2.5 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0021 | Box barge L=100, B=6, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 3075 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 0.6 m; KM = 3.1 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0022 | Box barge L=100, B=10, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 1537.5 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 5.556 m; KM = 6.306 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0023 | Box barge L=100, B=10, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 3075 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 2.778 m; KM = 4.278 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0024 | Box barge L=100, B=10, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 5125 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 1.667 m; KM = 4.167 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0025 | Box barge L=100, B=16, T=1.5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 2460 t (seawater 1.025); KB = 0.75 m; BM = B²/12T = 14.22 m; KM = 14.97 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0026 | Box barge L=100, B=16, T=3 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 4920 t (seawater 1.025); KB = 1.5 m; BM = B²/12T = 7.111 m; KM = 8.611 m; Cb = 1. | Hydrostatics of a rectangular prism |
| MAR-0027 | Box barge L=100, B=16, T=5 | Accuracy | P2 | POST /marine/analyse with a rectangular section. | Δ = 8200 t (seawater 1.025); KB = 2.5 m; BM = B²/12T = 4.267 m; KM = 6.767 m; Cb = 1. | Hydrostatics of a rectangular prism |

## Ship-shape displacement

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAR-0028 | L=30, B=8, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 216 m³; Δ = 221.4 t in seawater; 216 t in fresh water. |  |
| MAR-0029 | L=30, B=8, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 264 m³; Δ = 270.6 t in seawater; 264 t in fresh water. |  |
| MAR-0030 | L=30, B=8, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 336 m³; Δ = 344.4 t in seawater; 336 t in fresh water. |  |
| MAR-0031 | L=30, B=8, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 393.6 m³; Δ = 403.44 t in seawater; 393.6 t in fresh water. |  |
| MAR-0032 | L=30, B=8, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 432 m³; Δ = 442.8 t in seawater; 432 t in fresh water. |  |
| MAR-0033 | L=30, B=8, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 528 m³; Δ = 541.2 t in seawater; 528 t in fresh water. |  |
| MAR-0034 | L=30, B=8, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 672 m³; Δ = 688.8 t in seawater; 672 t in fresh water. |  |
| MAR-0035 | L=30, B=8, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 787.2 m³; Δ = 806.88 t in seawater; 787.2 t in fresh water. |  |
| MAR-0036 | L=30, B=14, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 378 m³; Δ = 387.45 t in seawater; 378 t in fresh water. |  |
| MAR-0037 | L=30, B=14, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 462 m³; Δ = 473.55 t in seawater; 462 t in fresh water. |  |
| MAR-0038 | L=30, B=14, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 588 m³; Δ = 602.7 t in seawater; 588 t in fresh water. |  |
| MAR-0039 | L=30, B=14, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 688.8 m³; Δ = 706.02 t in seawater; 688.8 t in fresh water. |  |
| MAR-0040 | L=30, B=14, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 756 m³; Δ = 774.9 t in seawater; 756 t in fresh water. |  |
| MAR-0041 | L=30, B=14, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 924 m³; Δ = 947.1 t in seawater; 924 t in fresh water. |  |
| MAR-0042 | L=30, B=14, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1176 m³; Δ = 1205.4 t in seawater; 1176 t in fresh water. |  |
| MAR-0043 | L=30, B=14, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1377.6 m³; Δ = 1412.04 t in seawater; 1377.6 t in fresh water. |  |
| MAR-0044 | L=30, B=14, T=8, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1512 m³; Δ = 1549.8 t in seawater; 1512 t in fresh water. |  |
| MAR-0045 | L=30, B=14, T=8, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1848 m³; Δ = 1894.2 t in seawater; 1848 t in fresh water. |  |
| MAR-0046 | L=30, B=14, T=8, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2352 m³; Δ = 2410.8 t in seawater; 2352 t in fresh water. |  |
| MAR-0047 | L=30, B=14, T=8, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2755.2 m³; Δ = 2824.08 t in seawater; 2755.2 t in fresh water. |  |
| MAR-0048 | L=30, B=22, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 594 m³; Δ = 608.85 t in seawater; 594 t in fresh water. |  |
| MAR-0049 | L=30, B=22, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 726 m³; Δ = 744.15 t in seawater; 726 t in fresh water. |  |
| MAR-0050 | L=30, B=22, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 924 m³; Δ = 947.1 t in seawater; 924 t in fresh water. |  |
| MAR-0051 | L=30, B=22, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1082.4 m³; Δ = 1109.46 t in seawater; 1082.4 t in fresh water. |  |
| MAR-0052 | L=30, B=22, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1188 m³; Δ = 1217.7 t in seawater; 1188 t in fresh water. |  |
| MAR-0053 | L=30, B=22, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1452 m³; Δ = 1488.3 t in seawater; 1452 t in fresh water. |  |
| MAR-0054 | L=30, B=22, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1848 m³; Δ = 1894.2 t in seawater; 1848 t in fresh water. |  |
| MAR-0055 | L=30, B=22, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2164.8 m³; Δ = 2218.92 t in seawater; 2164.8 t in fresh water. |  |
| MAR-0056 | L=30, B=22, T=8, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2376 m³; Δ = 2435.4 t in seawater; 2376 t in fresh water. |  |
| MAR-0057 | L=30, B=22, T=8, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2904 m³; Δ = 2976.6 t in seawater; 2904 t in fresh water. |  |
| MAR-0058 | L=30, B=22, T=8, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3696 m³; Δ = 3788.4 t in seawater; 3696 t in fresh water. |  |
| MAR-0059 | L=30, B=22, T=8, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 4329.6 m³; Δ = 4437.84 t in seawater; 4329.6 t in fresh water. |  |
| MAR-0060 | L=80, B=8, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 576 m³; Δ = 590.4 t in seawater; 576 t in fresh water. |  |
| MAR-0061 | L=80, B=8, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 704 m³; Δ = 721.6 t in seawater; 704 t in fresh water. |  |
| MAR-0062 | L=80, B=8, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 896 m³; Δ = 918.4 t in seawater; 896 t in fresh water. |  |
| MAR-0063 | L=80, B=8, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1049.6 m³; Δ = 1075.84 t in seawater; 1049.6 t in fresh water. |  |
| MAR-0064 | L=80, B=8, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1152 m³; Δ = 1180.8 t in seawater; 1152 t in fresh water. |  |
| MAR-0065 | L=80, B=8, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1408 m³; Δ = 1443.2 t in seawater; 1408 t in fresh water. |  |
| MAR-0066 | L=80, B=8, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1792 m³; Δ = 1836.8 t in seawater; 1792 t in fresh water. |  |
| MAR-0067 | L=80, B=8, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2099.2 m³; Δ = 2151.68 t in seawater; 2099.2 t in fresh water. |  |
| MAR-0068 | L=80, B=14, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1008 m³; Δ = 1033.2 t in seawater; 1008 t in fresh water. |  |
| MAR-0069 | L=80, B=14, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1232 m³; Δ = 1262.8 t in seawater; 1232 t in fresh water. |  |
| MAR-0070 | L=80, B=14, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1568 m³; Δ = 1607.2 t in seawater; 1568 t in fresh water. |  |
| MAR-0071 | L=80, B=14, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1836.8 m³; Δ = 1882.72 t in seawater; 1836.8 t in fresh water. |  |
| MAR-0072 | L=80, B=14, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2016 m³; Δ = 2066.4 t in seawater; 2016 t in fresh water. |  |
| MAR-0073 | L=80, B=14, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2464 m³; Δ = 2525.6 t in seawater; 2464 t in fresh water. |  |
| MAR-0074 | L=80, B=14, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3136 m³; Δ = 3214.4 t in seawater; 3136 t in fresh water. |  |
| MAR-0075 | L=80, B=14, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3673.6 m³; Δ = 3765.44 t in seawater; 3673.6 t in fresh water. |  |
| MAR-0076 | L=80, B=14, T=8, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 4032 m³; Δ = 4132.8 t in seawater; 4032 t in fresh water. |  |
| MAR-0077 | L=80, B=14, T=8, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 4928 m³; Δ = 5051.2 t in seawater; 4928 t in fresh water. |  |
| MAR-0078 | L=80, B=14, T=8, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 6272 m³; Δ = 6428.8 t in seawater; 6272 t in fresh water. |  |
| MAR-0079 | L=80, B=14, T=8, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 7347.2 m³; Δ = 7530.88 t in seawater; 7347.2 t in fresh water. |  |
| MAR-0080 | L=80, B=22, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1584 m³; Δ = 1623.6 t in seawater; 1584 t in fresh water. |  |
| MAR-0081 | L=80, B=22, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1936 m³; Δ = 1984.4 t in seawater; 1936 t in fresh water. |  |
| MAR-0082 | L=80, B=22, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2464 m³; Δ = 2525.6 t in seawater; 2464 t in fresh water. |  |
| MAR-0083 | L=80, B=22, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2886.4 m³; Δ = 2958.56 t in seawater; 2886.4 t in fresh water. |  |
| MAR-0084 | L=80, B=22, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3168 m³; Δ = 3247.2 t in seawater; 3168 t in fresh water. |  |
| MAR-0085 | L=80, B=22, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3872 m³; Δ = 3968.8 t in seawater; 3872 t in fresh water. |  |
| MAR-0086 | L=80, B=22, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 4928 m³; Δ = 5051.2 t in seawater; 4928 t in fresh water. |  |
| MAR-0087 | L=80, B=22, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 5772.8 m³; Δ = 5917.12 t in seawater; 5772.8 t in fresh water. |  |
| MAR-0088 | L=80, B=22, T=8, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 6336 m³; Δ = 6494.4 t in seawater; 6336 t in fresh water. |  |
| MAR-0089 | L=80, B=22, T=8, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 7744 m³; Δ = 7937.6 t in seawater; 7744 t in fresh water. |  |
| MAR-0090 | L=80, B=22, T=8, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 9856 m³; Δ = 10102.4 t in seawater; 9856 t in fresh water. |  |
| MAR-0091 | L=80, B=22, T=8, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 11545.6 m³; Δ = 11834.2 t in seawater; 11545.6 t in fresh water. |  |
| MAR-0092 | L=150, B=8, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1080 m³; Δ = 1107 t in seawater; 1080 t in fresh water. |  |
| MAR-0093 | L=150, B=8, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1320 m³; Δ = 1353 t in seawater; 1320 t in fresh water. |  |
| MAR-0094 | L=150, B=8, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1680 m³; Δ = 1722 t in seawater; 1680 t in fresh water. |  |
| MAR-0095 | L=150, B=8, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1968 m³; Δ = 2017.2 t in seawater; 1968 t in fresh water. |  |
| MAR-0096 | L=150, B=8, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2160 m³; Δ = 2214 t in seawater; 2160 t in fresh water. |  |
| MAR-0097 | L=150, B=8, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2640 m³; Δ = 2706 t in seawater; 2640 t in fresh water. |  |
| MAR-0098 | L=150, B=8, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3360 m³; Δ = 3444 t in seawater; 3360 t in fresh water. |  |
| MAR-0099 | L=150, B=8, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3936 m³; Δ = 4034.4 t in seawater; 3936 t in fresh water. |  |
| MAR-0100 | L=150, B=14, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 1890 m³; Δ = 1937.25 t in seawater; 1890 t in fresh water. |  |
| MAR-0101 | L=150, B=14, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2310 m³; Δ = 2367.75 t in seawater; 2310 t in fresh water. |  |
| MAR-0102 | L=150, B=14, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2940 m³; Δ = 3013.5 t in seawater; 2940 t in fresh water. |  |
| MAR-0103 | L=150, B=14, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3444 m³; Δ = 3530.1 t in seawater; 3444 t in fresh water. |  |
| MAR-0104 | L=150, B=14, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3780 m³; Δ = 3874.5 t in seawater; 3780 t in fresh water. |  |
| MAR-0105 | L=150, B=14, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 4620 m³; Δ = 4735.5 t in seawater; 4620 t in fresh water. |  |
| MAR-0106 | L=150, B=14, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 5880 m³; Δ = 6027 t in seawater; 5880 t in fresh water. |  |
| MAR-0107 | L=150, B=14, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 6888 m³; Δ = 7060.2 t in seawater; 6888 t in fresh water. |  |
| MAR-0108 | L=150, B=14, T=8, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 7560 m³; Δ = 7749 t in seawater; 7560 t in fresh water. |  |
| MAR-0109 | L=150, B=14, T=8, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 9240 m³; Δ = 9471 t in seawater; 9240 t in fresh water. |  |
| MAR-0110 | L=150, B=14, T=8, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 11760 m³; Δ = 12054 t in seawater; 11760 t in fresh water. |  |
| MAR-0111 | L=150, B=14, T=8, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 13776 m³; Δ = 14120.4 t in seawater; 13776 t in fresh water. |  |
| MAR-0112 | L=150, B=22, T=2, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 2970 m³; Δ = 3044.25 t in seawater; 2970 t in fresh water. |  |
| MAR-0113 | L=150, B=22, T=2, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 3630 m³; Δ = 3720.75 t in seawater; 3630 t in fresh water. |  |
| MAR-0114 | L=150, B=22, T=2, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 4620 m³; Δ = 4735.5 t in seawater; 4620 t in fresh water. |  |
| MAR-0115 | L=150, B=22, T=2, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 5412 m³; Δ = 5547.3 t in seawater; 5412 t in fresh water. |  |
| MAR-0116 | L=150, B=22, T=4, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 5940 m³; Δ = 6088.5 t in seawater; 5940 t in fresh water. |  |
| MAR-0117 | L=150, B=22, T=4, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 7260 m³; Δ = 7441.5 t in seawater; 7260 t in fresh water. |  |
| MAR-0118 | L=150, B=22, T=4, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 9240 m³; Δ = 9471 t in seawater; 9240 t in fresh water. |  |
| MAR-0119 | L=150, B=22, T=4, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 10824 m³; Δ = 11094.6 t in seawater; 10824 t in fresh water. |  |
| MAR-0120 | L=150, B=22, T=8, Cb=0.45 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 11880 m³; Δ = 12177 t in seawater; 11880 t in fresh water. |  |
| MAR-0121 | L=150, B=22, T=8, Cb=0.55 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 14520 m³; Δ = 14883 t in seawater; 14520 t in fresh water. |  |
| MAR-0122 | L=150, B=22, T=8, Cb=0.7 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 18480 m³; Δ = 18942 t in seawater; 18480 t in fresh water. |  |
| MAR-0123 | L=150, B=22, T=8, Cb=0.82 | Accuracy | P2 | Set the hull form coefficients; read displacement. | ∇ = Cb·L·B·T = 21648 m³; Δ = 22189.2 t in seawater; 21648 t in fresh water. |  |

## IMO intact stability

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAR-0124 | GM0 = 0.05 m | Boundary | P2 | Run the stability check. | Fail: GM0 < 0.15 m. | IMO IS Code 2008 §2.2 |
| MAR-0125 | GM0 = 0.1 m | Boundary | P2 | Run the stability check. | Fail: GM0 < 0.15 m. | IMO IS Code 2008 §2.2 |
| MAR-0126 | GM0 = 0.15 m | Boundary | P2 | Run the stability check. | Pass (GM0 ≥ 0.15 m). | IMO IS Code 2008 §2.2 |
| MAR-0127 | GM0 = 0.2 m | Boundary | P2 | Run the stability check. | Pass (GM0 ≥ 0.15 m). | IMO IS Code 2008 §2.2 |
| MAR-0128 | GM0 = 0.5 m | Boundary | P2 | Run the stability check. | Pass (GM0 ≥ 0.15 m). | IMO IS Code 2008 §2.2 |
| MAR-0129 | GM0 = 1.0 m | Boundary | P2 | Run the stability check. | Pass (GM0 ≥ 0.15 m). | IMO IS Code 2008 §2.2 |
| MAR-0130 | GZ area 0–30° = 0.0495 m·rad | Boundary | P2 | Run the stability check. | Fail: below 0.055 m·rad. | IMO IS Code 2008 §2.2 |
| MAR-0131 | GZ area 0–30° = 0.055 m·rad | Boundary | P2 | Run the stability check. | Pass. | IMO IS Code 2008 §2.2 |
| MAR-0132 | GZ area 0–30° = 0.0605 m·rad | Boundary | P2 | Run the stability check. | Pass. | IMO IS Code 2008 §2.2 |
| MAR-0133 | GZ area 0–40° = 0.081 m·rad | Boundary | P2 | Run the stability check. | Fail: below 0.09 m·rad. | IMO IS Code 2008 §2.2 |
| MAR-0134 | GZ area 0–40° = 0.09 m·rad | Boundary | P2 | Run the stability check. | Pass. | IMO IS Code 2008 §2.2 |
| MAR-0135 | GZ area 0–40° = 0.099 m·rad | Boundary | P2 | Run the stability check. | Pass. | IMO IS Code 2008 §2.2 |
| MAR-0136 | GZ area 30–40° = 0.027 m·rad | Boundary | P2 | Run the stability check. | Fail: below 0.03 m·rad. | IMO IS Code 2008 §2.2 |
| MAR-0137 | GZ area 30–40° = 0.03 m·rad | Boundary | P2 | Run the stability check. | Pass. | IMO IS Code 2008 §2.2 |
| MAR-0138 | GZ area 30–40° = 0.033 m·rad | Boundary | P2 | Run the stability check. | Pass. | IMO IS Code 2008 §2.2 |
| MAR-0139 | GZ at 30° = 0.15 m | Boundary | P2 | Run the stability check. | Fail: GZ(30°) < 0.20 m. |  |
| MAR-0140 | GZ at 30° = 0.2 m | Boundary | P2 | Run the stability check. | Pass. |  |
| MAR-0141 | GZ at 30° = 0.25 m | Boundary | P2 | Run the stability check. | Pass. |  |
| MAR-0142 | Angle of max GZ = 20° | Boundary | P2 | Run the stability check. | Fail: must be ≥ 25°. |  |
| MAR-0143 | Angle of max GZ = 25° | Boundary | P2 | Run the stability check. | Pass. |  |
| MAR-0144 | Angle of max GZ = 30° | Boundary | P2 | Run the stability check. | Pass. |  |

## Resistance

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAR-0145 | L=20 m at 5 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.1837; Re = 43303367; Cf = 0.075/(log Re − 2)² = 0.002361. | ITTC-57 |
| MAR-0146 | L=20 m at 10 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.3673; Re = 86606734; Cf = 0.075/(log Re − 2)² = 0.002127. | ITTC-57 |
| MAR-0147 | L=20 m at 15 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.551; Re = 129910101; Cf = 0.075/(log Re − 2)² = 0.002007; Fn > 0.45: outside Holtrop range, warn. | ITTC-57 |
| MAR-0148 | L=20 m at 20 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.7347; Re = 173213468; Cf = 0.075/(log Re − 2)² = 0.001927; Fn > 0.45: outside Holtrop range, warn. | ITTC-57 |
| MAR-0149 | L=20 m at 25 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.9183; Re = 216516835; Cf = 0.075/(log Re − 2)² = 0.001869; Fn > 0.45: outside Holtrop range, warn. | ITTC-57 |
| MAR-0150 | L=50 m at 5 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.1162; Re = 108258418; Cf = 0.075/(log Re − 2)² = 0.00206. | ITTC-57 |
| MAR-0151 | L=50 m at 10 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.2323; Re = 216516835; Cf = 0.075/(log Re − 2)² = 0.001869. | ITTC-57 |
| MAR-0152 | L=50 m at 15 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.3485; Re = 324775253; Cf = 0.075/(log Re − 2)² = 0.001769. | ITTC-57 |
| MAR-0153 | L=50 m at 20 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.4646; Re = 433033670; Cf = 0.075/(log Re − 2)² = 0.001703; Fn > 0.45: outside Holtrop range, warn. | ITTC-57 |
| MAR-0154 | L=50 m at 25 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.5808; Re = 541292088; Cf = 0.075/(log Re − 2)² = 0.001654; Fn > 0.45: outside Holtrop range, warn. | ITTC-57 |
| MAR-0155 | L=100 m at 5 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.08214; Re = 216516835; Cf = 0.075/(log Re − 2)² = 0.001869. | ITTC-57 |
| MAR-0156 | L=100 m at 10 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.1643; Re = 433033670; Cf = 0.075/(log Re − 2)² = 0.001703. | ITTC-57 |
| MAR-0157 | L=100 m at 15 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.2464; Re = 649550505; Cf = 0.075/(log Re − 2)² = 0.001616. | ITTC-57 |
| MAR-0158 | L=100 m at 20 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.3286; Re = 866067340; Cf = 0.075/(log Re − 2)² = 0.001558. | ITTC-57 |
| MAR-0159 | L=100 m at 25 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.4107; Re = 1.083e+09; Cf = 0.075/(log Re − 2)² = 0.001516. | ITTC-57 |
| MAR-0160 | L=200 m at 5 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.05808; Re = 433033670; Cf = 0.075/(log Re − 2)² = 0.001703. | ITTC-57 |
| MAR-0161 | L=200 m at 10 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.1162; Re = 866067340; Cf = 0.075/(log Re − 2)² = 0.001558. | ITTC-57 |
| MAR-0162 | L=200 m at 15 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.1742; Re = 1.299e+09; Cf = 0.075/(log Re − 2)² = 0.001482. | ITTC-57 |
| MAR-0163 | L=200 m at 20 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.2323; Re = 1.732e+09; Cf = 0.075/(log Re − 2)² = 0.001431. | ITTC-57 |
| MAR-0164 | L=200 m at 25 kn | Accuracy | P2 | Compute Froude number and ITTC-57 friction. | Fn = 0.2904; Re = 2.165e+09; Cf = 0.075/(log Re − 2)² = 0.001394. | ITTC-57 |

## Marine features to add

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAR-0165 | hull fairing (NURBS) — workboat | Functional | P2 | Run hull fairing (NURBS). | Result with method and limits. |  |
| MAR-0166 | hull fairing (NURBS) — ferry | Functional | P2 | Run hull fairing (NURBS). | Result with method and limits. |  |
| MAR-0167 | hull fairing (NURBS) — tanker | Functional | P2 | Run hull fairing (NURBS). | Result with method and limits. |  |
| MAR-0168 | damaged stability — workboat | Functional | P2 | Run damaged stability. | Result with method and limits. |  |
| MAR-0169 | damaged stability — ferry | Functional | P2 | Run damaged stability. | Result with method and limits. |  |
| MAR-0170 | damaged stability — tanker | Functional | P2 | Run damaged stability. | Result with method and limits. |  |
| MAR-0171 | tank sounding tables — workboat | Functional | P2 | Run tank sounding tables. | Result with method and limits. |  |
| MAR-0172 | tank sounding tables — ferry | Functional | P2 | Run tank sounding tables. | Result with method and limits. |  |
| MAR-0173 | tank sounding tables — tanker | Functional | P2 | Run tank sounding tables. | Result with method and limits. |  |
| MAR-0174 | longitudinal strength — workboat | Functional | P2 | Run longitudinal strength. | Result with method and limits. |  |
| MAR-0175 | longitudinal strength — ferry | Functional | P2 | Run longitudinal strength. | Result with method and limits. |  |
| MAR-0176 | longitudinal strength — tanker | Functional | P2 | Run longitudinal strength. | Result with method and limits. |  |
| MAR-0177 | seakeeping RAOs — workboat | Functional | P2 | Run seakeeping RAOs. | Result with method and limits. |  |
| MAR-0178 | seakeeping RAOs — ferry | Functional | P2 | Run seakeeping RAOs. | Result with method and limits. |  |
| MAR-0179 | seakeeping RAOs — tanker | Functional | P2 | Run seakeeping RAOs. | Result with method and limits. |  |
| MAR-0180 | propeller selection (B-series) — workboat | Functional | P2 | Run propeller selection (B-series). | Result with method and limits. |  |
| MAR-0181 | propeller selection (B-series) — ferry | Functional | P2 | Run propeller selection (B-series). | Result with method and limits. |  |
| MAR-0182 | propeller selection (B-series) — tanker | Functional | P2 | Run propeller selection (B-series). | Result with method and limits. |  |
| MAR-0183 | plate nesting — workboat | Functional | P2 | Run plate nesting. | Result with method and limits. |  |
| MAR-0184 | plate nesting — ferry | Functional | P2 | Run plate nesting. | Result with method and limits. |  |
| MAR-0185 | plate nesting — tanker | Functional | P2 | Run plate nesting. | Result with method and limits. |  |
| MAR-0186 | weather criterion — workboat | Functional | P2 | Run weather criterion. | Result with method and limits. |  |
| MAR-0187 | weather criterion — ferry | Functional | P2 | Run weather criterion. | Result with method and limits. |  |
| MAR-0188 | weather criterion — tanker | Functional | P2 | Run weather criterion. | Result with method and limits. |  |
