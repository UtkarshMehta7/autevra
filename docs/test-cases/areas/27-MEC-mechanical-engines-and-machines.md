# MEC — Mechanical: engines and machines

**CATIA-class equivalent:** Machine design extensions (engines, drives, bearings)  
**Autevra workspace:** Engine; Inventory  
**Scope:** Mechanical  
**Cases:** 268 (Have 228, Partial 8, Gap 32)

Piston engines, motors, turbines, bearings and standard parts.

[← Back to the index](../README.md)

## Features

- Piston engine geometry — 126 cases (Have)
- Bearings — 72 cases (Have)
- Power and torque — 30 cases (Have)
- Machine elements to add — 40 cases (Gap)

## Piston engine geometry

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MEC-0001 | Engine bore 72 × stroke 70, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 855.016 cm³; bore/stroke = 1.03; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0002 | Engine bore 72 × stroke 70, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1140.02 cm³; bore/stroke = 1.03; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0003 | Engine bore 72 × stroke 70, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1710.03 cm³; bore/stroke = 1.03; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0004 | Engine bore 72 × stroke 70, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2280.04 cm³; bore/stroke = 1.03; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0005 | Engine bore 72 × stroke 80, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 977.161 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0006 | Engine bore 72 × stroke 80, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1302.88 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0007 | Engine bore 72 × stroke 80, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1954.32 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0008 | Engine bore 72 × stroke 80, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2605.76 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0009 | Engine bore 72 × stroke 86, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1050.45 cm³; bore/stroke = 0.837; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0010 | Engine bore 72 × stroke 86, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1400.6 cm³; bore/stroke = 0.837; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0011 | Engine bore 72 × stroke 86, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2100.9 cm³; bore/stroke = 0.837; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0012 | Engine bore 72 × stroke 86, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2801.19 cm³; bore/stroke = 0.837; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0013 | Engine bore 72 × stroke 90, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1099.31 cm³; bore/stroke = 0.8; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0014 | Engine bore 72 × stroke 90, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1465.74 cm³; bore/stroke = 0.8; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0015 | Engine bore 72 × stroke 90, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2198.61 cm³; bore/stroke = 0.8; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0016 | Engine bore 72 × stroke 90, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2931.48 cm³; bore/stroke = 0.8; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0017 | Engine bore 72 × stroke 100, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1221.45 cm³; bore/stroke = 0.72; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0018 | Engine bore 72 × stroke 100, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1628.6 cm³; bore/stroke = 0.72; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0019 | Engine bore 72 × stroke 100, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2442.9 cm³; bore/stroke = 0.72; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0020 | Engine bore 72 × stroke 100, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3257.2 cm³; bore/stroke = 0.72; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0021 | Engine bore 77 × stroke 70, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 977.891 cm³; bore/stroke = 1.1; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0022 | Engine bore 77 × stroke 70, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1303.86 cm³; bore/stroke = 1.1; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0023 | Engine bore 77 × stroke 70, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1955.78 cm³; bore/stroke = 1.1; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0024 | Engine bore 77 × stroke 70, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2607.71 cm³; bore/stroke = 1.1; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0025 | Engine bore 77 × stroke 80, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1117.59 cm³; bore/stroke = 0.963; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0026 | Engine bore 77 × stroke 80, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1490.12 cm³; bore/stroke = 0.963; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0027 | Engine bore 77 × stroke 80, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2235.18 cm³; bore/stroke = 0.963; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0028 | Engine bore 77 × stroke 80, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2980.24 cm³; bore/stroke = 0.963; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0029 | Engine bore 77 × stroke 86, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1201.41 cm³; bore/stroke = 0.895; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0030 | Engine bore 77 × stroke 86, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1601.88 cm³; bore/stroke = 0.895; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0031 | Engine bore 77 × stroke 86, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2402.82 cm³; bore/stroke = 0.895; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0032 | Engine bore 77 × stroke 86, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3203.76 cm³; bore/stroke = 0.895; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0033 | Engine bore 77 × stroke 90, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1257.29 cm³; bore/stroke = 0.856; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0034 | Engine bore 77 × stroke 90, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1676.39 cm³; bore/stroke = 0.856; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0035 | Engine bore 77 × stroke 90, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2514.58 cm³; bore/stroke = 0.856; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0036 | Engine bore 77 × stroke 90, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3352.77 cm³; bore/stroke = 0.856; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0037 | Engine bore 77 × stroke 100, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1396.99 cm³; bore/stroke = 0.77; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0038 | Engine bore 77 × stroke 100, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1862.65 cm³; bore/stroke = 0.77; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0039 | Engine bore 77 × stroke 100, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2793.98 cm³; bore/stroke = 0.77; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0040 | Engine bore 77 × stroke 100, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3725.3 cm³; bore/stroke = 0.77; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0041 | Engine bore 81 × stroke 70, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1082.13 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0042 | Engine bore 81 × stroke 70, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1442.84 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0043 | Engine bore 81 × stroke 70, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2164.26 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0044 | Engine bore 81 × stroke 70, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2885.68 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0045 | Engine bore 81 × stroke 80, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1236.72 cm³; bore/stroke = 1.01; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0046 | Engine bore 81 × stroke 80, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1648.96 cm³; bore/stroke = 1.01; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0047 | Engine bore 81 × stroke 80, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2473.44 cm³; bore/stroke = 1.01; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0048 | Engine bore 81 × stroke 80, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3297.92 cm³; bore/stroke = 1.01; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0049 | Engine bore 81 × stroke 86, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1329.47 cm³; bore/stroke = 0.942; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0050 | Engine bore 81 × stroke 86, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1772.63 cm³; bore/stroke = 0.942; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0051 | Engine bore 81 × stroke 86, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2658.95 cm³; bore/stroke = 0.942; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0052 | Engine bore 81 × stroke 86, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3545.26 cm³; bore/stroke = 0.942; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0053 | Engine bore 81 × stroke 90, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1391.31 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0054 | Engine bore 81 × stroke 90, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1855.08 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0055 | Engine bore 81 × stroke 90, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2782.62 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0056 | Engine bore 81 × stroke 90, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3710.16 cm³; bore/stroke = 0.9; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0057 | Engine bore 81 × stroke 100, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1545.9 cm³; bore/stroke = 0.81; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0058 | Engine bore 81 × stroke 100, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2061.2 cm³; bore/stroke = 0.81; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0059 | Engine bore 81 × stroke 100, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3091.8 cm³; bore/stroke = 0.81; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0060 | Engine bore 81 × stroke 100, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4122.4 cm³; bore/stroke = 0.81; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0061 | Engine bore 86 × stroke 70, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1219.85 cm³; bore/stroke = 1.23; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0062 | Engine bore 86 × stroke 70, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1626.47 cm³; bore/stroke = 1.23; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0063 | Engine bore 86 × stroke 70, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2439.7 cm³; bore/stroke = 1.23; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0064 | Engine bore 86 × stroke 70, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3252.93 cm³; bore/stroke = 1.23; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0065 | Engine bore 86 × stroke 80, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1394.11 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0066 | Engine bore 86 × stroke 80, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1858.82 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0067 | Engine bore 86 × stroke 80, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2788.23 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0068 | Engine bore 86 × stroke 80, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3717.64 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0069 | Engine bore 86 × stroke 86, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1498.67 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0070 | Engine bore 86 × stroke 86, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1998.23 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0071 | Engine bore 86 × stroke 86, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2997.34 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0072 | Engine bore 86 × stroke 86, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3996.46 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0073 | Engine bore 86 × stroke 90, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1568.38 cm³; bore/stroke = 0.956; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0074 | Engine bore 86 × stroke 90, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2091.17 cm³; bore/stroke = 0.956; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0075 | Engine bore 86 × stroke 90, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3136.75 cm³; bore/stroke = 0.956; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0076 | Engine bore 86 × stroke 90, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4182.34 cm³; bore/stroke = 0.956; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0077 | Engine bore 86 × stroke 100, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1742.64 cm³; bore/stroke = 0.86; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0078 | Engine bore 86 × stroke 100, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2323.52 cm³; bore/stroke = 0.86; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0079 | Engine bore 86 × stroke 100, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3485.28 cm³; bore/stroke = 0.86; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0080 | Engine bore 86 × stroke 100, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4647.04 cm³; bore/stroke = 0.86; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0081 | Engine bore 92 × stroke 70, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1396 cm³; bore/stroke = 1.31; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0082 | Engine bore 92 × stroke 70, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1861.33 cm³; bore/stroke = 1.31; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0083 | Engine bore 92 × stroke 70, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2792 cm³; bore/stroke = 1.31; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0084 | Engine bore 92 × stroke 70, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3722.66 cm³; bore/stroke = 1.31; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0085 | Engine bore 92 × stroke 80, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1595.43 cm³; bore/stroke = 1.15; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0086 | Engine bore 92 × stroke 80, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2127.24 cm³; bore/stroke = 1.15; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0087 | Engine bore 92 × stroke 80, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3190.85 cm³; bore/stroke = 1.15; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0088 | Engine bore 92 × stroke 80, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4254.47 cm³; bore/stroke = 1.15; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0089 | Engine bore 92 × stroke 86, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1715.08 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0090 | Engine bore 92 × stroke 86, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2286.78 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0091 | Engine bore 92 × stroke 86, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3430.17 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0092 | Engine bore 92 × stroke 86, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4573.56 cm³; bore/stroke = 1.07; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0093 | Engine bore 92 × stroke 90, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1794.85 cm³; bore/stroke = 1.02; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0094 | Engine bore 92 × stroke 90, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2393.14 cm³; bore/stroke = 1.02; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0095 | Engine bore 92 × stroke 90, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3589.71 cm³; bore/stroke = 1.02; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0096 | Engine bore 92 × stroke 90, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4786.28 cm³; bore/stroke = 1.02; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0097 | Engine bore 92 × stroke 100, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1994.28 cm³; bore/stroke = 0.92; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0098 | Engine bore 92 × stroke 100, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2659.04 cm³; bore/stroke = 0.92; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0099 | Engine bore 92 × stroke 100, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3988.57 cm³; bore/stroke = 0.92; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0100 | Engine bore 92 × stroke 100, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 5318.09 cm³; bore/stroke = 0.92; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0101 | Engine bore 100 × stroke 70, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1649.34 cm³; bore/stroke = 1.43; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0102 | Engine bore 100 × stroke 70, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2199.11 cm³; bore/stroke = 1.43; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0103 | Engine bore 100 × stroke 70, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3298.67 cm³; bore/stroke = 1.43; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0104 | Engine bore 100 × stroke 70, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4398.23 cm³; bore/stroke = 1.43; mean piston speed at 6000 rpm = 14 m/s. |  |
| MEC-0105 | Engine bore 100 × stroke 80, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 1884.96 cm³; bore/stroke = 1.25; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0106 | Engine bore 100 × stroke 80, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2513.27 cm³; bore/stroke = 1.25; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0107 | Engine bore 100 × stroke 80, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3769.91 cm³; bore/stroke = 1.25; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0108 | Engine bore 100 × stroke 80, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 5026.55 cm³; bore/stroke = 1.25; mean piston speed at 6000 rpm = 16 m/s. |  |
| MEC-0109 | Engine bore 100 × stroke 86, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2026.33 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0110 | Engine bore 100 × stroke 86, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2701.77 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0111 | Engine bore 100 × stroke 86, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4052.65 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0112 | Engine bore 100 × stroke 86, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 5403.54 cm³; bore/stroke = 1.16; mean piston speed at 6000 rpm = 17.2 m/s. |  |
| MEC-0113 | Engine bore 100 × stroke 90, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2120.58 cm³; bore/stroke = 1.11; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0114 | Engine bore 100 × stroke 90, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2827.43 cm³; bore/stroke = 1.11; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0115 | Engine bore 100 × stroke 90, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4241.15 cm³; bore/stroke = 1.11; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0116 | Engine bore 100 × stroke 90, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 5654.87 cm³; bore/stroke = 1.11; mean piston speed at 6000 rpm = 18 m/s. |  |
| MEC-0117 | Engine bore 100 × stroke 100, 3 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 2356.19 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0118 | Engine bore 100 × stroke 100, 4 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 3141.59 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0119 | Engine bore 100 × stroke 100, 6 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 4712.39 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0120 | Engine bore 100 × stroke 100, 8 cyl | Accuracy | P2 | PUT /engine/spec; read the analysis. | Displacement = π/4·B²·S·n = 6283.19 cm³; bore/stroke = 1; mean piston speed at 6000 rpm = 20 m/s. |  |
| MEC-0121 | Compression ratio 8 on 500 cm³ cylinder | Accuracy | P2 | Set CR. | Clearance volume = Vs/(CR−1) = 71.429 cm³; Otto efficiency 1−CR^(1−γ) = 0.5647 (γ=1.4). |  |
| MEC-0122 | Compression ratio 9.5 on 500 cm³ cylinder | Accuracy | P2 | Set CR. | Clearance volume = Vs/(CR−1) = 58.824 cm³; Otto efficiency 1−CR^(1−γ) = 0.5936 (γ=1.4). |  |
| MEC-0123 | Compression ratio 10.5 on 500 cm³ cylinder | Accuracy | P2 | Set CR. | Clearance volume = Vs/(CR−1) = 52.632 cm³; Otto efficiency 1−CR^(1−γ) = 0.6096 (γ=1.4). |  |
| MEC-0124 | Compression ratio 12 on 500 cm³ cylinder | Accuracy | P2 | Set CR. | Clearance volume = Vs/(CR−1) = 45.455 cm³; Otto efficiency 1−CR^(1−γ) = 0.6299 (γ=1.4). |  |
| MEC-0125 | Compression ratio 14 on 500 cm³ cylinder | Accuracy | P2 | Set CR. | Clearance volume = Vs/(CR−1) = 38.462 cm³; Otto efficiency 1−CR^(1−γ) = 0.652 (γ=1.4). |  |
| MEC-0126 | Compression ratio 18 on 500 cm³ cylinder | Accuracy | P2 | Set CR. | Clearance volume = Vs/(CR−1) = 29.412 cm³; Otto efficiency 1−CR^(1−γ) = 0.6853 (γ=1.4). |  |

## Bearings

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MEC-0127 | ball bearing C=10 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 2083.3 h. | ISO 281 |
| MEC-0128 | roller bearing C=10 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 3562.4 h. | ISO 281 |
| MEC-0129 | ball bearing C=10 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 694.44 h. | ISO 281 |
| MEC-0130 | roller bearing C=10 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 1187.5 h. | ISO 281 |
| MEC-0131 | ball bearing C=10 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 347.22 h. | ISO 281 |
| MEC-0132 | roller bearing C=10 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 593.74 h. | ISO 281 |
| MEC-0133 | ball bearing C=10 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 8 Mrev = 133.33 h. | ISO 281 |
| MEC-0134 | roller bearing C=10 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 10.079 Mrev = 167.99 h. | ISO 281 |
| MEC-0135 | ball bearing C=10 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 8 Mrev = 44.444 h. | ISO 281 |
| MEC-0136 | roller bearing C=10 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 10.079 Mrev = 55.996 h. | ISO 281 |
| MEC-0137 | ball bearing C=10 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 8 Mrev = 22.222 h. | ISO 281 |
| MEC-0138 | roller bearing C=10 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 10.079 Mrev = 27.998 h. | ISO 281 |
| MEC-0139 | ball bearing C=10 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1 Mrev = 16.667 h. | ISO 281 |
| MEC-0140 | roller bearing C=10 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 1 Mrev = 16.667 h. | ISO 281 |
| MEC-0141 | ball bearing C=10 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1 Mrev = 5.5556 h. | ISO 281 |
| MEC-0142 | roller bearing C=10 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 1 Mrev = 5.5556 h. | ISO 281 |
| MEC-0143 | ball bearing C=10 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1 Mrev = 2.7778 h. | ISO 281 |
| MEC-0144 | roller bearing C=10 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 1 Mrev = 2.7778 h. | ISO 281 |
| MEC-0145 | ball bearing C=25 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1953.1 Mrev = 32552 h. | ISO 281 |
| MEC-0146 | roller bearing C=25 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 4532.8 Mrev = 75547 h. | ISO 281 |
| MEC-0147 | ball bearing C=25 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1953.1 Mrev = 10851 h. | ISO 281 |
| MEC-0148 | roller bearing C=25 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 4532.8 Mrev = 25182 h. | ISO 281 |
| MEC-0149 | ball bearing C=25 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1953.1 Mrev = 5425.3 h. | ISO 281 |
| MEC-0150 | roller bearing C=25 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 4532.8 Mrev = 12591 h. | ISO 281 |
| MEC-0151 | ball bearing C=25 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 2083.3 h. | ISO 281 |
| MEC-0152 | roller bearing C=25 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 3562.4 h. | ISO 281 |
| MEC-0153 | ball bearing C=25 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 694.44 h. | ISO 281 |
| MEC-0154 | roller bearing C=25 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 1187.5 h. | ISO 281 |
| MEC-0155 | ball bearing C=25 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 347.22 h. | ISO 281 |
| MEC-0156 | roller bearing C=25 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 593.74 h. | ISO 281 |
| MEC-0157 | ball bearing C=25 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 15.625 Mrev = 260.42 h. | ISO 281 |
| MEC-0158 | roller bearing C=25 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 21.206 Mrev = 353.44 h. | ISO 281 |
| MEC-0159 | ball bearing C=25 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 15.625 Mrev = 86.806 h. | ISO 281 |
| MEC-0160 | roller bearing C=25 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 21.206 Mrev = 117.81 h. | ISO 281 |
| MEC-0161 | ball bearing C=25 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 15.625 Mrev = 43.403 h. | ISO 281 |
| MEC-0162 | roller bearing C=25 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 21.206 Mrev = 58.907 h. | ISO 281 |
| MEC-0163 | ball bearing C=50 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 15625 Mrev = 260417 h. | ISO 281 |
| MEC-0164 | roller bearing C=50 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 45688 Mrev = 761463 h. | ISO 281 |
| MEC-0165 | ball bearing C=50 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 15625 Mrev = 86806 h. | ISO 281 |
| MEC-0166 | roller bearing C=50 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 45688 Mrev = 253821 h. | ISO 281 |
| MEC-0167 | ball bearing C=50 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 15625 Mrev = 43403 h. | ISO 281 |
| MEC-0168 | roller bearing C=50 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 45688 Mrev = 126910 h. | ISO 281 |
| MEC-0169 | ball bearing C=50 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1000 Mrev = 16667 h. | ISO 281 |
| MEC-0170 | roller bearing C=50 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 2154.4 Mrev = 35907 h. | ISO 281 |
| MEC-0171 | ball bearing C=50 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1000 Mrev = 5555.6 h. | ISO 281 |
| MEC-0172 | roller bearing C=50 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 2154.4 Mrev = 11969 h. | ISO 281 |
| MEC-0173 | ball bearing C=50 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1000 Mrev = 2777.8 h. | ISO 281 |
| MEC-0174 | roller bearing C=50 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 2154.4 Mrev = 5984.5 h. | ISO 281 |
| MEC-0175 | ball bearing C=50 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 2083.3 h. | ISO 281 |
| MEC-0176 | roller bearing C=50 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 3562.4 h. | ISO 281 |
| MEC-0177 | ball bearing C=50 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 694.44 h. | ISO 281 |
| MEC-0178 | roller bearing C=50 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 1187.5 h. | ISO 281 |
| MEC-0179 | ball bearing C=50 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125 Mrev = 347.22 h. | ISO 281 |
| MEC-0180 | roller bearing C=50 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 213.75 Mrev = 593.74 h. | ISO 281 |
| MEC-0181 | ball bearing C=100 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125000 Mrev = 2083333 h. | ISO 281 |
| MEC-0182 | roller bearing C=100 kN, P=2 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 460504 Mrev = 7675066 h. | ISO 281 |
| MEC-0183 | ball bearing C=100 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125000 Mrev = 694444 h. | ISO 281 |
| MEC-0184 | roller bearing C=100 kN, P=2 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 460504 Mrev = 2558355 h. | ISO 281 |
| MEC-0185 | ball bearing C=100 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 125000 Mrev = 347222 h. | ISO 281 |
| MEC-0186 | roller bearing C=100 kN, P=2 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 460504 Mrev = 1279178 h. | ISO 281 |
| MEC-0187 | ball bearing C=100 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 8000 Mrev = 133333 h. | ISO 281 |
| MEC-0188 | roller bearing C=100 kN, P=5 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 21715 Mrev = 361922 h. | ISO 281 |
| MEC-0189 | ball bearing C=100 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 8000 Mrev = 44444 h. | ISO 281 |
| MEC-0190 | roller bearing C=100 kN, P=5 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 21715 Mrev = 120641 h. | ISO 281 |
| MEC-0191 | ball bearing C=100 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 8000 Mrev = 22222 h. | ISO 281 |
| MEC-0192 | roller bearing C=100 kN, P=5 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 21715 Mrev = 60320 h. | ISO 281 |
| MEC-0193 | ball bearing C=100 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1000 Mrev = 16667 h. | ISO 281 |
| MEC-0194 | roller bearing C=100 kN, P=10 kN, 1000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 2154.4 Mrev = 35907 h. | ISO 281 |
| MEC-0195 | ball bearing C=100 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1000 Mrev = 5555.6 h. | ISO 281 |
| MEC-0196 | roller bearing C=100 kN, P=10 kN, 3000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 2154.4 Mrev = 11969 h. | ISO 281 |
| MEC-0197 | ball bearing C=100 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3 = 1000 Mrev = 2777.8 h. | ISO 281 |
| MEC-0198 | roller bearing C=100 kN, P=10 kN, 6000 rpm | Accuracy | P2 | POST /inventory/items/{id}/bearing-life. | L10 = (C/P)^3.33 = 2154.4 Mrev = 5984.5 h. | ISO 281 |

## Power and torque

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MEC-0199 | Torque 50 N·m at 1000 rpm | Accuracy | P2 | Read power. | P = T·ω = 5.236 kW. |  |
| MEC-0200 | Torque 50 N·m at 2000 rpm | Accuracy | P2 | Read power. | P = T·ω = 10.472 kW. |  |
| MEC-0201 | Torque 50 N·m at 3000 rpm | Accuracy | P2 | Read power. | P = T·ω = 15.708 kW. |  |
| MEC-0202 | Torque 50 N·m at 4500 rpm | Accuracy | P2 | Read power. | P = T·ω = 23.562 kW. |  |
| MEC-0203 | Torque 50 N·m at 6000 rpm | Accuracy | P2 | Read power. | P = T·ω = 31.416 kW. |  |
| MEC-0204 | Torque 100 N·m at 1000 rpm | Accuracy | P2 | Read power. | P = T·ω = 10.472 kW. |  |
| MEC-0205 | Torque 100 N·m at 2000 rpm | Accuracy | P2 | Read power. | P = T·ω = 20.944 kW. |  |
| MEC-0206 | Torque 100 N·m at 3000 rpm | Accuracy | P2 | Read power. | P = T·ω = 31.416 kW. |  |
| MEC-0207 | Torque 100 N·m at 4500 rpm | Accuracy | P2 | Read power. | P = T·ω = 47.124 kW. |  |
| MEC-0208 | Torque 100 N·m at 6000 rpm | Accuracy | P2 | Read power. | P = T·ω = 62.832 kW. |  |
| MEC-0209 | Torque 250 N·m at 1000 rpm | Accuracy | P2 | Read power. | P = T·ω = 26.18 kW. |  |
| MEC-0210 | Torque 250 N·m at 2000 rpm | Accuracy | P2 | Read power. | P = T·ω = 52.36 kW. |  |
| MEC-0211 | Torque 250 N·m at 3000 rpm | Accuracy | P2 | Read power. | P = T·ω = 78.54 kW. |  |
| MEC-0212 | Torque 250 N·m at 4500 rpm | Accuracy | P2 | Read power. | P = T·ω = 117.81 kW. |  |
| MEC-0213 | Torque 250 N·m at 6000 rpm | Accuracy | P2 | Read power. | P = T·ω = 157.08 kW. |  |
| MEC-0214 | Torque 400 N·m at 1000 rpm | Accuracy | P2 | Read power. | P = T·ω = 41.888 kW. |  |
| MEC-0215 | Torque 400 N·m at 2000 rpm | Accuracy | P2 | Read power. | P = T·ω = 83.776 kW. |  |
| MEC-0216 | Torque 400 N·m at 3000 rpm | Accuracy | P2 | Read power. | P = T·ω = 125.66 kW. |  |
| MEC-0217 | Torque 400 N·m at 4500 rpm | Accuracy | P2 | Read power. | P = T·ω = 188.5 kW. |  |
| MEC-0218 | Torque 400 N·m at 6000 rpm | Accuracy | P2 | Read power. | P = T·ω = 251.33 kW. |  |
| MEC-0219 | Torque 800 N·m at 1000 rpm | Accuracy | P2 | Read power. | P = T·ω = 83.776 kW. |  |
| MEC-0220 | Torque 800 N·m at 2000 rpm | Accuracy | P2 | Read power. | P = T·ω = 167.55 kW. |  |
| MEC-0221 | Torque 800 N·m at 3000 rpm | Accuracy | P2 | Read power. | P = T·ω = 251.33 kW. |  |
| MEC-0222 | Torque 800 N·m at 4500 rpm | Accuracy | P2 | Read power. | P = T·ω = 376.99 kW. |  |
| MEC-0223 | Torque 800 N·m at 6000 rpm | Accuracy | P2 | Read power. | P = T·ω = 502.65 kW. |  |
| MEC-0224 | Torque 1500 N·m at 1000 rpm | Accuracy | P2 | Read power. | P = T·ω = 157.08 kW. |  |
| MEC-0225 | Torque 1500 N·m at 2000 rpm | Accuracy | P2 | Read power. | P = T·ω = 314.16 kW. |  |
| MEC-0226 | Torque 1500 N·m at 3000 rpm | Accuracy | P2 | Read power. | P = T·ω = 471.24 kW. |  |
| MEC-0227 | Torque 1500 N·m at 4500 rpm | Accuracy | P2 | Read power. | P = T·ω = 706.86 kW. |  |
| MEC-0228 | Torque 1500 N·m at 6000 rpm | Accuracy | P2 | Read power. | P = T·ω = 942.48 kW. |  |

## Machine elements to add

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MEC-0229 | spur gear (ISO 6336 bending): size | Functional | P2 | Size a spur gear (ISO 6336 bending). | Calculation shown with standard reference; part generated. |  |
| MEC-0230 | spur gear (ISO 6336 bending): check capacity | Functional | P2 | Check capacity a spur gear (ISO 6336 bending). | Calculation shown with standard reference; part generated. |  |
| MEC-0231 | spur gear (ISO 6336 bending): generate 3D part | Functional | P2 | Generate 3d part a spur gear (ISO 6336 bending). | Calculation shown with standard reference; part generated. |  |
| MEC-0232 | spur gear (ISO 6336 bending): add to inventory with ports | Functional | P2 | Add to inventory with ports a spur gear (ISO 6336 bending). | Calculation shown with standard reference; part generated. |  |
| MEC-0233 | helical gear: size | Functional | P2 | Size a helical gear. | Calculation shown with standard reference; part generated. |  |
| MEC-0234 | helical gear: check capacity | Functional | P2 | Check capacity a helical gear. | Calculation shown with standard reference; part generated. |  |
| MEC-0235 | helical gear: generate 3D part | Functional | P2 | Generate 3d part a helical gear. | Calculation shown with standard reference; part generated. |  |
| MEC-0236 | helical gear: add to inventory with ports | Functional | P2 | Add to inventory with ports a helical gear. | Calculation shown with standard reference; part generated. |  |
| MEC-0237 | shaft fatigue (Goodman): size | Functional | P2 | Size a shaft fatigue (Goodman). | Calculation shown with standard reference; part generated. |  |
| MEC-0238 | shaft fatigue (Goodman): check capacity | Functional | P2 | Check capacity a shaft fatigue (Goodman). | Calculation shown with standard reference; part generated. |  |
| MEC-0239 | shaft fatigue (Goodman): generate 3D part | Functional | P2 | Generate 3d part a shaft fatigue (Goodman). | Calculation shown with standard reference; part generated. |  |
| MEC-0240 | shaft fatigue (Goodman): add to inventory with ports | Functional | P2 | Add to inventory with ports a shaft fatigue (Goodman). | Calculation shown with standard reference; part generated. |  |
| MEC-0241 | key/spline: size | Functional | P2 | Size a key/spline. | Calculation shown with standard reference; part generated. |  |
| MEC-0242 | key/spline: check capacity | Functional | P2 | Check capacity a key/spline. | Calculation shown with standard reference; part generated. |  |
| MEC-0243 | key/spline: generate 3D part | Functional | P2 | Generate 3d part a key/spline. | Calculation shown with standard reference; part generated. |  |
| MEC-0244 | key/spline: add to inventory with ports | Functional | P2 | Add to inventory with ports a key/spline. | Calculation shown with standard reference; part generated. |  |
| MEC-0245 | bolted joint (VDI 2230): size | Functional | P2 | Size a bolted joint (VDI 2230). | Calculation shown with standard reference; part generated. |  |
| MEC-0246 | bolted joint (VDI 2230): check capacity | Functional | P2 | Check capacity a bolted joint (VDI 2230). | Calculation shown with standard reference; part generated. |  |
| MEC-0247 | bolted joint (VDI 2230): generate 3D part | Functional | P2 | Generate 3d part a bolted joint (VDI 2230). | Calculation shown with standard reference; part generated. |  |
| MEC-0248 | bolted joint (VDI 2230): add to inventory with ports | Functional | P2 | Add to inventory with ports a bolted joint (VDI 2230). | Calculation shown with standard reference; part generated. |  |
| MEC-0249 | spring (EN 13906): size | Functional | P2 | Size a spring (EN 13906). | Calculation shown with standard reference; part generated. |  |
| MEC-0250 | spring (EN 13906): check capacity | Functional | P2 | Check capacity a spring (EN 13906). | Calculation shown with standard reference; part generated. |  |
| MEC-0251 | spring (EN 13906): generate 3D part | Functional | P2 | Generate 3d part a spring (EN 13906). | Calculation shown with standard reference; part generated. |  |
| MEC-0252 | spring (EN 13906): add to inventory with ports | Functional | P2 | Add to inventory with ports a spring (EN 13906). | Calculation shown with standard reference; part generated. |  |
| MEC-0253 | belt drive: size | Functional | P2 | Size a belt drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0254 | belt drive: check capacity | Functional | P2 | Check capacity a belt drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0255 | belt drive: generate 3D part | Functional | P2 | Generate 3d part a belt drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0256 | belt drive: add to inventory with ports | Functional | P2 | Add to inventory with ports a belt drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0257 | chain drive: size | Functional | P2 | Size a chain drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0258 | chain drive: check capacity | Functional | P2 | Check capacity a chain drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0259 | chain drive: generate 3D part | Functional | P2 | Generate 3d part a chain drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0260 | chain drive: add to inventory with ports | Functional | P2 | Add to inventory with ports a chain drive. | Calculation shown with standard reference; part generated. |  |
| MEC-0261 | clutch: size | Functional | P2 | Size a clutch. | Calculation shown with standard reference; part generated. |  |
| MEC-0262 | clutch: check capacity | Functional | P2 | Check capacity a clutch. | Calculation shown with standard reference; part generated. |  |
| MEC-0263 | clutch: generate 3D part | Functional | P2 | Generate 3d part a clutch. | Calculation shown with standard reference; part generated. |  |
| MEC-0264 | clutch: add to inventory with ports | Functional | P2 | Add to inventory with ports a clutch. | Calculation shown with standard reference; part generated. |  |
| MEC-0265 | brake disc thermal: size | Functional | P2 | Size a brake disc thermal. | Calculation shown with standard reference; part generated. |  |
| MEC-0266 | brake disc thermal: check capacity | Functional | P2 | Check capacity a brake disc thermal. | Calculation shown with standard reference; part generated. |  |
| MEC-0267 | brake disc thermal: generate 3D part | Functional | P2 | Generate 3d part a brake disc thermal. | Calculation shown with standard reference; part generated. |  |
| MEC-0268 | brake disc thermal: add to inventory with ports | Functional | P2 | Add to inventory with ports a brake disc thermal. | Calculation shown with standard reference; part generated. |  |
