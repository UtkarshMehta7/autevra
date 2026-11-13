# JNT — Fasteners, welds and fatigue

**CATIA-class equivalent:** Fastener / Weld Design / joint analysis add-ons  
**Autevra workspace:** Inventory (ISO fasteners); Structures  
**Scope:** Shared  
**Cases:** 284 (Have 0, Partial 90, Gap 194)

Bolt preload and tightening torque, weld throat stresses and fatigue safety factors.

[← Back to the index](../README.md)

## Features

- Bolt preload and torque — 90 cases (Partial)
- Fillet welds — 66 cases (Gap)
- Fatigue (modified Goodman) — 128 cases (Gap)

## Bolt preload and torque

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| JNT-0001 | M3×0.5 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 2.6261 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 0.9454 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0002 | M3×0.5 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 2.6261 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 1.1817 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0003 | M3×0.5 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 2.6261 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 1.5757 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0004 | M3×0.5 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 3.758 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 1.3529 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0005 | M3×0.5 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 3.758 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 1.6911 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0006 | M3×0.5 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 3.758 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 2.2548 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0007 | M3×0.5 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 4.3919 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 1.5811 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0008 | M3×0.5 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 4.3919 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 1.9764 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0009 | M3×0.5 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 5.0308 mm²; Fi = 0.9·Sp·As = 4.3919 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 2.6352 N·m. | d2=2.6752, d3=2.3866; ISO 898-1; T = K F d |
| JNT-0010 | M4×0.7 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 4.5825 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 2.1996 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0011 | M4×0.7 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 4.5825 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 2.7495 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0012 | M4×0.7 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 4.5825 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 3.666 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0013 | M4×0.7 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 6.5577 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 3.1477 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0014 | M4×0.7 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 6.5577 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 3.9346 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0015 | M4×0.7 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 6.5577 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 5.2462 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0016 | M4×0.7 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 7.6638 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 3.6786 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0017 | M4×0.7 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 7.6638 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 4.5983 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0018 | M4×0.7 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 8.7787 mm²; Fi = 0.9·Sp·As = 7.6638 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 6.1311 N·m. | d2=3.5453, d3=3.1412; ISO 898-1; T = K F d |
| JNT-0019 | M5×0.8 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 7.4033 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 4.442 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0020 | M5×0.8 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 7.4033 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 5.5525 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0021 | M5×0.8 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 7.4033 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 7.4033 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0022 | M5×0.8 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 10.594 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 6.3566 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0023 | M5×0.8 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 10.594 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 7.9458 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0024 | M5×0.8 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 10.594 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 10.594 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0025 | M5×0.8 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 12.381 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 7.4288 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0026 | M5×0.8 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 12.381 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 9.286 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0027 | M5×0.8 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 14.183 mm²; Fi = 0.9·Sp·As = 12.381 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 12.381 N·m. | d2=4.4804, d3=4.0185; ISO 898-1; T = K F d |
| JNT-0028 | M6×1.0 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 10.504 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 7.5632 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0029 | M6×1.0 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 10.504 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 9.454 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0030 | M6×1.0 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 10.504 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 12.605 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0031 | M6×1.0 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 15.032 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 10.823 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0032 | M6×1.0 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 15.032 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 13.529 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0033 | M6×1.0 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 15.032 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 18.039 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0034 | M6×1.0 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 17.568 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 12.649 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0035 | M6×1.0 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 17.568 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 15.811 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0036 | M6×1.0 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 20.123 mm²; Fi = 0.9·Sp·As = 17.568 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 21.081 N·m. | d2=5.3505, d3=4.7731; ISO 898-1; T = K F d |
| JNT-0037 | M8×1.25 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 19.11 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 18.345 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0038 | M8×1.25 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 19.11 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 22.932 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0039 | M8×1.25 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 19.11 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 30.575 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0040 | M8×1.25 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 27.347 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 26.253 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0041 | M8×1.25 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 27.347 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 32.816 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0042 | M8×1.25 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 27.347 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 43.755 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0043 | M8×1.25 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 31.959 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 30.681 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0044 | M8×1.25 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 31.959 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 38.351 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0045 | M8×1.25 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 36.609 mm²; Fi = 0.9·Sp·As = 31.959 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 51.135 N·m. | d2=7.1881, d3=6.4664; ISO 898-1; T = K F d |
| JNT-0046 | M10×1.5 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 30.271 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 36.325 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0047 | M10×1.5 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 30.271 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 45.406 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0048 | M10×1.5 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 30.271 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 60.541 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0049 | M10×1.5 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 43.318 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 51.982 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0050 | M10×1.5 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 43.318 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 64.977 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0051 | M10×1.5 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 43.318 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 86.636 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0052 | M10×1.5 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 50.625 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 60.75 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0053 | M10×1.5 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 50.625 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 75.937 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0054 | M10×1.5 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 57.99 mm²; Fi = 0.9·Sp·As = 50.625 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 101.25 N·m. | d2=9.0257, d3=8.1597; ISO 898-1; T = K F d |
| JNT-0055 | M12×1.75 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 43.987 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 63.341 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0056 | M12×1.75 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 43.987 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 79.177 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0057 | M12×1.75 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 43.987 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 105.57 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0058 | M12×1.75 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 62.947 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 90.644 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0059 | M12×1.75 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 62.947 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 113.3 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0060 | M12×1.75 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 62.947 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 151.07 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0061 | M12×1.75 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 73.565 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 105.93 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0062 | M12×1.75 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 73.565 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 132.42 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0063 | M12×1.75 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 84.267 mm²; Fi = 0.9·Sp·As = 73.565 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 176.56 N·m. | d2=10.863, d3=9.853; ISO 898-1; T = K F d |
| JNT-0064 | M16×2.0 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 81.781 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 157.02 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0065 | M16×2.0 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 81.781 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 196.27 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0066 | M16×2.0 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 81.781 kN (Sp=580 MPa); tightening torque T = K·Fi·d = 261.7 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0067 | M16×2.0 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 117.03 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 224.7 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0068 | M16×2.0 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 117.03 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 280.88 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0069 | M16×2.0 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 117.03 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 374.5 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0070 | M16×2.0 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 136.77 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 262.6 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0071 | M16×2.0 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 136.77 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 328.25 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0072 | M16×2.0 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 156.67 mm²; Fi = 0.9·Sp·As = 136.77 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 437.67 N·m. | d2=14.701, d3=13.546; ISO 898-1; T = K F d |
| JNT-0073 | M20×2.5 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 132.19 kN (Sp=600 MPa); tightening torque T = K·Fi·d = 317.25 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0074 | M20×2.5 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 132.19 kN (Sp=600 MPa); tightening torque T = K·Fi·d = 396.57 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0075 | M20×2.5 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 132.19 kN (Sp=600 MPa); tightening torque T = K·Fi·d = 528.76 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0076 | M20×2.5 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 182.86 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 438.87 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0077 | M20×2.5 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 182.86 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 548.58 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0078 | M20×2.5 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 182.86 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 731.45 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0079 | M20×2.5 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 213.71 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 512.89 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0080 | M20×2.5 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 213.71 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 641.12 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0081 | M20×2.5 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 244.79 mm²; Fi = 0.9·Sp·As = 213.71 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 854.82 N·m. | d2=18.376, d3=16.933; ISO 898-1; T = K F d |
| JNT-0082 | M24×3.0 class 8.8, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 190.35 kN (Sp=600 MPa); tightening torque T = K·Fi·d = 548.21 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0083 | M24×3.0 class 8.8, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 190.35 kN (Sp=600 MPa); tightening torque T = K·Fi·d = 685.27 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0084 | M24×3.0 class 8.8, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 190.35 kN (Sp=600 MPa); tightening torque T = K·Fi·d = 913.69 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0085 | M24×3.0 class 10.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 263.32 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 758.36 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0086 | M24×3.0 class 10.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 263.32 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 947.95 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0087 | M24×3.0 class 10.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 263.32 kN (Sp=830 MPa); tightening torque T = K·Fi·d = 1263.9 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0088 | M24×3.0 class 12.9, K=0.12 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 307.74 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 886.28 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0089 | M24×3.0 class 12.9, K=0.15 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 307.74 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 1107.8 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |
| JNT-0090 | M24×3.0 class 12.9, K=0.2 | Accuracy | P2 | Size the bolted joint at 90% of proof load. | As = π/4·((d2+d3)/2)² = 352.5 mm²; Fi = 0.9·Sp·As = 307.74 kN (Sp=970 MPa); tightening torque T = K·Fi·d = 1477.1 N·m. | d2=22.051, d3=20.319; ISO 898-1; T = K F d |

## Fillet welds

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| JNT-0091 | Fillet weld leg 3, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.121 mm; τ = F/(a·L) = 94.282 MPa. |  |
| JNT-0092 | Fillet weld leg 3, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.121 mm; τ = F/(a·L) = 471.41 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0093 | Fillet weld leg 3, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.121 mm; τ = F/(a·L) = 47.141 MPa. |  |
| JNT-0094 | Fillet weld leg 3, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.121 mm; τ = F/(a·L) = 235.7 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0095 | Fillet weld leg 3, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.121 mm; τ = F/(a·L) = 23.57 MPa. |  |
| JNT-0096 | Fillet weld leg 3, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.121 mm; τ = F/(a·L) = 117.85 MPa. |  |
| JNT-0097 | Fillet weld leg 4, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.828 mm; τ = F/(a·L) = 70.711 MPa. |  |
| JNT-0098 | Fillet weld leg 4, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.828 mm; τ = F/(a·L) = 353.56 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0099 | Fillet weld leg 4, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.828 mm; τ = F/(a·L) = 35.356 MPa. |  |
| JNT-0100 | Fillet weld leg 4, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.828 mm; τ = F/(a·L) = 176.78 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0101 | Fillet weld leg 4, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.828 mm; τ = F/(a·L) = 17.678 MPa. |  |
| JNT-0102 | Fillet weld leg 4, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 2.828 mm; τ = F/(a·L) = 88.389 MPa. |  |
| JNT-0103 | Fillet weld leg 5, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 3.535 mm; τ = F/(a·L) = 56.569 MPa. |  |
| JNT-0104 | Fillet weld leg 5, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 3.535 mm; τ = F/(a·L) = 282.85 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0105 | Fillet weld leg 5, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 3.535 mm; τ = F/(a·L) = 28.285 MPa. |  |
| JNT-0106 | Fillet weld leg 5, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 3.535 mm; τ = F/(a·L) = 141.42 MPa. |  |
| JNT-0107 | Fillet weld leg 5, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 3.535 mm; τ = F/(a·L) = 14.142 MPa. |  |
| JNT-0108 | Fillet weld leg 5, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 3.535 mm; τ = F/(a·L) = 70.711 MPa. |  |
| JNT-0109 | Fillet weld leg 6, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 4.243 mm; τ = F/(a·L) = 47.141 MPa. |  |
| JNT-0110 | Fillet weld leg 6, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 4.243 mm; τ = F/(a·L) = 235.7 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0111 | Fillet weld leg 6, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 4.243 mm; τ = F/(a·L) = 23.57 MPa. |  |
| JNT-0112 | Fillet weld leg 6, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 4.243 mm; τ = F/(a·L) = 117.85 MPa. |  |
| JNT-0113 | Fillet weld leg 6, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 4.243 mm; τ = F/(a·L) = 11.785 MPa. |  |
| JNT-0114 | Fillet weld leg 6, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 4.243 mm; τ = F/(a·L) = 58.926 MPa. |  |
| JNT-0115 | Fillet weld leg 8, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 5.657 mm; τ = F/(a·L) = 35.356 MPa. |  |
| JNT-0116 | Fillet weld leg 8, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 5.657 mm; τ = F/(a·L) = 176.78 MPa; exceeds 150 MPa allowable (flag). |  |
| JNT-0117 | Fillet weld leg 8, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 5.657 mm; τ = F/(a·L) = 17.678 MPa. |  |
| JNT-0118 | Fillet weld leg 8, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 5.657 mm; τ = F/(a·L) = 88.389 MPa. |  |
| JNT-0119 | Fillet weld leg 8, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 5.657 mm; τ = F/(a·L) = 8.8389 MPa. |  |
| JNT-0120 | Fillet weld leg 8, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 5.657 mm; τ = F/(a·L) = 44.195 MPa. |  |
| JNT-0121 | Fillet weld leg 10, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 7.071 mm; τ = F/(a·L) = 28.285 MPa. |  |
| JNT-0122 | Fillet weld leg 10, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 7.071 mm; τ = F/(a·L) = 141.42 MPa. |  |
| JNT-0123 | Fillet weld leg 10, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 7.071 mm; τ = F/(a·L) = 14.142 MPa. |  |
| JNT-0124 | Fillet weld leg 10, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 7.071 mm; τ = F/(a·L) = 70.711 MPa. |  |
| JNT-0125 | Fillet weld leg 10, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 7.071 mm; τ = F/(a·L) = 7.0711 MPa. |  |
| JNT-0126 | Fillet weld leg 10, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 7.071 mm; τ = F/(a·L) = 35.356 MPa. |  |
| JNT-0127 | Fillet weld leg 12, length 50, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 8.485 mm; τ = F/(a·L) = 23.57 MPa. |  |
| JNT-0128 | Fillet weld leg 12, length 50, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 8.485 mm; τ = F/(a·L) = 117.85 MPa. |  |
| JNT-0129 | Fillet weld leg 12, length 100, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 8.485 mm; τ = F/(a·L) = 11.785 MPa. |  |
| JNT-0130 | Fillet weld leg 12, length 100, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 8.485 mm; τ = F/(a·L) = 58.926 MPa. |  |
| JNT-0131 | Fillet weld leg 12, length 200, shear 10 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 8.485 mm; τ = F/(a·L) = 5.8926 MPa. |  |
| JNT-0132 | Fillet weld leg 12, length 200, shear 50 kN | Accuracy | P2 | Check a longitudinal fillet weld. | Throat a = 0.707·z = 8.485 mm; τ = F/(a·L) = 29.463 MPa. |  |
| JNT-0133 | fillet weld: create from edges | Functional | P2 | Create from edges for a fillet weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0134 | fillet weld: weld symbol on drawing | Functional | P2 | Weld symbol on drawing for a fillet weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0135 | fillet weld: weld bead mass in BOM | Functional | P2 | Weld bead mass in bom for a fillet weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0136 | fillet weld: weld in FEA as tie | Functional | P2 | Weld in fea as tie for a fillet weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0137 | butt (full penetration) weld: create from edges | Functional | P2 | Create from edges for a butt (full penetration) weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0138 | butt (full penetration) weld: weld symbol on drawing | Functional | P2 | Weld symbol on drawing for a butt (full penetration) weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0139 | butt (full penetration) weld: weld bead mass in BOM | Functional | P2 | Weld bead mass in bom for a butt (full penetration) weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0140 | butt (full penetration) weld: weld in FEA as tie | Functional | P2 | Weld in fea as tie for a butt (full penetration) weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0141 | plug weld: create from edges | Functional | P2 | Create from edges for a plug weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0142 | plug weld: weld symbol on drawing | Functional | P2 | Weld symbol on drawing for a plug weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0143 | plug weld: weld bead mass in BOM | Functional | P2 | Weld bead mass in bom for a plug weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0144 | plug weld: weld in FEA as tie | Functional | P2 | Weld in fea as tie for a plug weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0145 | spot weld: create from edges | Functional | P2 | Create from edges for a spot weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0146 | spot weld: weld symbol on drawing | Functional | P2 | Weld symbol on drawing for a spot weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0147 | spot weld: weld bead mass in BOM | Functional | P2 | Weld bead mass in bom for a spot weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0148 | spot weld: weld in FEA as tie | Functional | P2 | Weld in fea as tie for a spot weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0149 | seam weld: create from edges | Functional | P2 | Create from edges for a seam weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0150 | seam weld: weld symbol on drawing | Functional | P2 | Weld symbol on drawing for a seam weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0151 | seam weld: weld bead mass in BOM | Functional | P2 | Weld bead mass in bom for a seam weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0152 | seam weld: weld in FEA as tie | Functional | P2 | Weld in fea as tie for a seam weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0153 | stitch fillet 50-100 weld: create from edges | Functional | P2 | Create from edges for a stitch fillet 50-100 weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0154 | stitch fillet 50-100 weld: weld symbol on drawing | Functional | P2 | Weld symbol on drawing for a stitch fillet 50-100 weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0155 | stitch fillet 50-100 weld: weld bead mass in BOM | Functional | P2 | Weld bead mass in bom for a stitch fillet 50-100 weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |
| JNT-0156 | stitch fillet 50-100 weld: weld in FEA as tie | Functional | P2 | Weld in fea as tie for a stitch fillet 50-100 weld. | Weld stored with type, size and length; appears in drawing/BOM/FEA. |  |

## Fatigue (modified Goodman)

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| JNT-0157 | Su=400, Se=140, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.8. | Modified Goodman |
| JNT-0158 | Su=400, Se=140, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.647. | Modified Goodman |
| JNT-0159 | Su=400, Se=140, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.167; marginal (< 1.5). | Modified Goodman |
| JNT-0160 | Su=400, Se=140, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.9032 → FAIL (n < 1). | Modified Goodman |
| JNT-0161 | Su=400, Se=140, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.4; marginal (< 1.5). | Modified Goodman |
| JNT-0162 | Su=400, Se=140, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.037; marginal (< 1.5). | Modified Goodman |
| JNT-0163 | Su=400, Se=140, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8235 → FAIL (n < 1). | Modified Goodman |
| JNT-0164 | Su=400, Se=140, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.6829 → FAIL (n < 1). | Modified Goodman |
| JNT-0165 | Su=400, Se=140, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.9333 → FAIL (n < 1). | Modified Goodman |
| JNT-0166 | Su=400, Se=140, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.7568 → FAIL (n < 1). | Modified Goodman |
| JNT-0167 | Su=400, Se=140, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.6364 → FAIL (n < 1). | Modified Goodman |
| JNT-0168 | Su=400, Se=140, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.549 → FAIL (n < 1). | Modified Goodman |
| JNT-0169 | Su=400, Se=140, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.56 → FAIL (n < 1). | Modified Goodman |
| JNT-0170 | Su=400, Se=140, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.4912 → FAIL (n < 1). | Modified Goodman |
| JNT-0171 | Su=400, Se=140, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.4375 → FAIL (n < 1). | Modified Goodman |
| JNT-0172 | Su=400, Se=140, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.3944 → FAIL (n < 1). | Modified Goodman |
| JNT-0173 | Su=400, Se=200, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4. | Modified Goodman |
| JNT-0174 | Su=400, Se=200, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0175 | Su=400, Se=200, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.333; marginal (< 1.5). | Modified Goodman |
| JNT-0176 | Su=400, Se=200, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1; marginal (< 1.5). | Modified Goodman |
| JNT-0177 | Su=400, Se=200, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0178 | Su=400, Se=200, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.333; marginal (< 1.5). | Modified Goodman |
| JNT-0179 | Su=400, Se=200, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1; marginal (< 1.5). | Modified Goodman |
| JNT-0180 | Su=400, Se=200, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8 → FAIL (n < 1). | Modified Goodman |
| JNT-0181 | Su=400, Se=200, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.333; marginal (< 1.5). | Modified Goodman |
| JNT-0182 | Su=400, Se=200, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1; marginal (< 1.5). | Modified Goodman |
| JNT-0183 | Su=400, Se=200, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8 → FAIL (n < 1). | Modified Goodman |
| JNT-0184 | Su=400, Se=200, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.6667 → FAIL (n < 1). | Modified Goodman |
| JNT-0185 | Su=400, Se=200, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8 → FAIL (n < 1). | Modified Goodman |
| JNT-0186 | Su=400, Se=200, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.6667 → FAIL (n < 1). | Modified Goodman |
| JNT-0187 | Su=400, Se=200, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.5714 → FAIL (n < 1). | Modified Goodman |
| JNT-0188 | Su=400, Se=200, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.5 → FAIL (n < 1). | Modified Goodman |
| JNT-0189 | Su=600, Se=210, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4.2. | Modified Goodman |
| JNT-0190 | Su=600, Se=210, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.471. | Modified Goodman |
| JNT-0191 | Su=600, Se=210, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.75. | Modified Goodman |
| JNT-0192 | Su=600, Se=210, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.355; marginal (< 1.5). | Modified Goodman |
| JNT-0193 | Su=600, Se=210, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.1. | Modified Goodman |
| JNT-0194 | Su=600, Se=210, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.556. | Modified Goodman |
| JNT-0195 | Su=600, Se=210, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.235; marginal (< 1.5). | Modified Goodman |
| JNT-0196 | Su=600, Se=210, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.024; marginal (< 1.5). | Modified Goodman |
| JNT-0197 | Su=600, Se=210, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.4; marginal (< 1.5). | Modified Goodman |
| JNT-0198 | Su=600, Se=210, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.135; marginal (< 1.5). | Modified Goodman |
| JNT-0199 | Su=600, Se=210, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.9545 → FAIL (n < 1). | Modified Goodman |
| JNT-0200 | Su=600, Se=210, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8235 → FAIL (n < 1). | Modified Goodman |
| JNT-0201 | Su=600, Se=210, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.84 → FAIL (n < 1). | Modified Goodman |
| JNT-0202 | Su=600, Se=210, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.7368 → FAIL (n < 1). | Modified Goodman |
| JNT-0203 | Su=600, Se=210, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.6562 → FAIL (n < 1). | Modified Goodman |
| JNT-0204 | Su=600, Se=210, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.5915 → FAIL (n < 1). | Modified Goodman |
| JNT-0205 | Su=600, Se=300, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 6. | Modified Goodman |
| JNT-0206 | Su=600, Se=300, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0207 | Su=600, Se=300, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0208 | Su=600, Se=300, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.5. | Modified Goodman |
| JNT-0209 | Su=600, Se=300, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0210 | Su=600, Se=300, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0211 | Su=600, Se=300, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.5. | Modified Goodman |
| JNT-0212 | Su=600, Se=300, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.2; marginal (< 1.5). | Modified Goodman |
| JNT-0213 | Su=600, Se=300, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0214 | Su=600, Se=300, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.5. | Modified Goodman |
| JNT-0215 | Su=600, Se=300, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.2; marginal (< 1.5). | Modified Goodman |
| JNT-0216 | Su=600, Se=300, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1; marginal (< 1.5). | Modified Goodman |
| JNT-0217 | Su=600, Se=300, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.2; marginal (< 1.5). | Modified Goodman |
| JNT-0218 | Su=600, Se=300, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1; marginal (< 1.5). | Modified Goodman |
| JNT-0219 | Su=600, Se=300, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8571 → FAIL (n < 1). | Modified Goodman |
| JNT-0220 | Su=600, Se=300, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.75 → FAIL (n < 1). | Modified Goodman |
| JNT-0221 | Su=900, Se=315, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 6.3. | Modified Goodman |
| JNT-0222 | Su=900, Se=315, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3.706. | Modified Goodman |
| JNT-0223 | Su=900, Se=315, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.625. | Modified Goodman |
| JNT-0224 | Su=900, Se=315, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.032. | Modified Goodman |
| JNT-0225 | Su=900, Se=315, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3.15. | Modified Goodman |
| JNT-0226 | Su=900, Se=315, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.333. | Modified Goodman |
| JNT-0227 | Su=900, Se=315, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.853. | Modified Goodman |
| JNT-0228 | Su=900, Se=315, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.537. | Modified Goodman |
| JNT-0229 | Su=900, Se=315, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.1. | Modified Goodman |
| JNT-0230 | Su=900, Se=315, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.703. | Modified Goodman |
| JNT-0231 | Su=900, Se=315, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.432; marginal (< 1.5). | Modified Goodman |
| JNT-0232 | Su=900, Se=315, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.235; marginal (< 1.5). | Modified Goodman |
| JNT-0233 | Su=900, Se=315, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.26; marginal (< 1.5). | Modified Goodman |
| JNT-0234 | Su=900, Se=315, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.105; marginal (< 1.5). | Modified Goodman |
| JNT-0235 | Su=900, Se=315, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.9844 → FAIL (n < 1). | Modified Goodman |
| JNT-0236 | Su=900, Se=315, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 0.8873 → FAIL (n < 1). | Modified Goodman |
| JNT-0237 | Su=900, Se=450, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 9. | Modified Goodman |
| JNT-0238 | Su=900, Se=450, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4.5. | Modified Goodman |
| JNT-0239 | Su=900, Se=450, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0240 | Su=900, Se=450, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.25. | Modified Goodman |
| JNT-0241 | Su=900, Se=450, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4.5. | Modified Goodman |
| JNT-0242 | Su=900, Se=450, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0243 | Su=900, Se=450, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.25. | Modified Goodman |
| JNT-0244 | Su=900, Se=450, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.8. | Modified Goodman |
| JNT-0245 | Su=900, Se=450, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0246 | Su=900, Se=450, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.25. | Modified Goodman |
| JNT-0247 | Su=900, Se=450, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.8. | Modified Goodman |
| JNT-0248 | Su=900, Se=450, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.5. | Modified Goodman |
| JNT-0249 | Su=900, Se=450, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.8. | Modified Goodman |
| JNT-0250 | Su=900, Se=450, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.5; marginal (< 1.5). | Modified Goodman |
| JNT-0251 | Su=900, Se=450, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.286; marginal (< 1.5). | Modified Goodman |
| JNT-0252 | Su=900, Se=450, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.125; marginal (< 1.5). | Modified Goodman |
| JNT-0253 | Su=1200, Se=420, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 8.4. | Modified Goodman |
| JNT-0254 | Su=1200, Se=420, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4.941. | Modified Goodman |
| JNT-0255 | Su=1200, Se=420, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3.5. | Modified Goodman |
| JNT-0256 | Su=1200, Se=420, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.71. | Modified Goodman |
| JNT-0257 | Su=1200, Se=420, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4.2. | Modified Goodman |
| JNT-0258 | Su=1200, Se=420, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3.111. | Modified Goodman |
| JNT-0259 | Su=1200, Se=420, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.471. | Modified Goodman |
| JNT-0260 | Su=1200, Se=420, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.049. | Modified Goodman |
| JNT-0261 | Su=1200, Se=420, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.8. | Modified Goodman |
| JNT-0262 | Su=1200, Se=420, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.27. | Modified Goodman |
| JNT-0263 | Su=1200, Se=420, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.909. | Modified Goodman |
| JNT-0264 | Su=1200, Se=420, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.647. | Modified Goodman |
| JNT-0265 | Su=1200, Se=420, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.68. | Modified Goodman |
| JNT-0266 | Su=1200, Se=420, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.474; marginal (< 1.5). | Modified Goodman |
| JNT-0267 | Su=1200, Se=420, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.312; marginal (< 1.5). | Modified Goodman |
| JNT-0268 | Su=1200, Se=420, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.183; marginal (< 1.5). | Modified Goodman |
| JNT-0269 | Su=1200, Se=600, σa=50, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 12. | Modified Goodman |
| JNT-0270 | Su=1200, Se=600, σa=50, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 6. | Modified Goodman |
| JNT-0271 | Su=1200, Se=600, σa=50, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4. | Modified Goodman |
| JNT-0272 | Su=1200, Se=600, σa=50, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0273 | Su=1200, Se=600, σa=100, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 6. | Modified Goodman |
| JNT-0274 | Su=1200, Se=600, σa=100, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4. | Modified Goodman |
| JNT-0275 | Su=1200, Se=600, σa=100, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0276 | Su=1200, Se=600, σa=100, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.4. | Modified Goodman |
| JNT-0277 | Su=1200, Se=600, σa=150, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 4. | Modified Goodman |
| JNT-0278 | Su=1200, Se=600, σa=150, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 3. | Modified Goodman |
| JNT-0279 | Su=1200, Se=600, σa=150, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.4. | Modified Goodman |
| JNT-0280 | Su=1200, Se=600, σa=150, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0281 | Su=1200, Se=600, σa=250, σm=0 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2.4. | Modified Goodman |
| JNT-0282 | Su=1200, Se=600, σa=250, σm=100 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 2. | Modified Goodman |
| JNT-0283 | Su=1200, Se=600, σa=250, σm=200 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.714. | Modified Goodman |
| JNT-0284 | Su=1200, Se=600, σa=250, σm=300 MPa | Accuracy | P2 | Run a fatigue check. | Goodman safety factor n = 1/(σa/Se + σm/Su) = 1.5; marginal (< 1.5). | Modified Goodman |
