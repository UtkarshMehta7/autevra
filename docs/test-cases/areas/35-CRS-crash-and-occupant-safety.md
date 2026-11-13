# CRS — Crash and occupant safety

**CATIA-class equivalent:** Crash / safety add-ons (explicit FE, occupant models)  
**Autevra workspace:** Loads; Simulation  
**Scope:** Land  
**Cases:** 128 (Have 0, Partial 0, Gap 128)

Energy and deceleration bounds, crush space and the explicit-crash workflow.

[← Back to the index](../README.md)

## Features

- Crush space and deceleration — 80 cases (Gap)
- Crash workflow — 48 cases (Gap)

## Crush space and deceleration

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CRS-0001 | m=1200 kg at 30 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 41.667 kJ; mean deceleration v²/2s = 11.8 g; mean force 138.89 kN. |  |
| CRS-0002 | m=1200 kg at 30 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 41.667 kJ; mean deceleration v²/2s = 7.081 g; mean force 83.333 kN. |  |
| CRS-0003 | m=1200 kg at 30 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 41.667 kJ; mean deceleration v²/2s = 5.058 g; mean force 59.524 kN. |  |
| CRS-0004 | m=1200 kg at 30 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 41.667 kJ; mean deceleration v²/2s = 3.934 g; mean force 46.296 kN. |  |
| CRS-0005 | m=1200 kg at 40 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 74.074 kJ; mean deceleration v²/2s = 20.98 g; mean force 246.91 kN. |  |
| CRS-0006 | m=1200 kg at 40 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 74.074 kJ; mean deceleration v²/2s = 12.59 g; mean force 148.15 kN. |  |
| CRS-0007 | m=1200 kg at 40 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 74.074 kJ; mean deceleration v²/2s = 8.992 g; mean force 105.82 kN. |  |
| CRS-0008 | m=1200 kg at 40 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 74.074 kJ; mean deceleration v²/2s = 6.994 g; mean force 82.305 kN. |  |
| CRS-0009 | m=1200 kg at 50 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 115.74 kJ; mean deceleration v²/2s = 32.78 g; mean force 385.8 kN. |  |
| CRS-0010 | m=1200 kg at 50 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 115.74 kJ; mean deceleration v²/2s = 19.67 g; mean force 231.48 kN. |  |
| CRS-0011 | m=1200 kg at 50 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 115.74 kJ; mean deceleration v²/2s = 14.05 g; mean force 165.34 kN. |  |
| CRS-0012 | m=1200 kg at 50 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 115.74 kJ; mean deceleration v²/2s = 10.93 g; mean force 128.6 kN. |  |
| CRS-0013 | m=1200 kg at 56 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 145.19 kJ; mean deceleration v²/2s = 41.12 g; mean force 483.95 kN. |  |
| CRS-0014 | m=1200 kg at 56 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 145.19 kJ; mean deceleration v²/2s = 24.67 g; mean force 290.37 kN. |  |
| CRS-0015 | m=1200 kg at 56 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 145.19 kJ; mean deceleration v²/2s = 17.62 g; mean force 207.41 kN. |  |
| CRS-0016 | m=1200 kg at 56 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 145.19 kJ; mean deceleration v²/2s = 13.71 g; mean force 161.32 kN. |  |
| CRS-0017 | m=1200 kg at 64 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 189.63 kJ; mean deceleration v²/2s = 53.71 g; mean force 632.1 kN. |  |
| CRS-0018 | m=1200 kg at 64 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 189.63 kJ; mean deceleration v²/2s = 32.23 g; mean force 379.26 kN. |  |
| CRS-0019 | m=1200 kg at 64 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 189.63 kJ; mean deceleration v²/2s = 23.02 g; mean force 270.9 kN. |  |
| CRS-0020 | m=1200 kg at 64 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 189.63 kJ; mean deceleration v²/2s = 17.9 g; mean force 210.7 kN. |  |
| CRS-0021 | m=1600 kg at 30 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 55.556 kJ; mean deceleration v²/2s = 11.8 g; mean force 185.19 kN. |  |
| CRS-0022 | m=1600 kg at 30 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 55.556 kJ; mean deceleration v²/2s = 7.081 g; mean force 111.11 kN. |  |
| CRS-0023 | m=1600 kg at 30 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 55.556 kJ; mean deceleration v²/2s = 5.058 g; mean force 79.365 kN. |  |
| CRS-0024 | m=1600 kg at 30 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 55.556 kJ; mean deceleration v²/2s = 3.934 g; mean force 61.728 kN. |  |
| CRS-0025 | m=1600 kg at 40 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 98.765 kJ; mean deceleration v²/2s = 20.98 g; mean force 329.22 kN. |  |
| CRS-0026 | m=1600 kg at 40 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 98.765 kJ; mean deceleration v²/2s = 12.59 g; mean force 197.53 kN. |  |
| CRS-0027 | m=1600 kg at 40 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 98.765 kJ; mean deceleration v²/2s = 8.992 g; mean force 141.09 kN. |  |
| CRS-0028 | m=1600 kg at 40 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 98.765 kJ; mean deceleration v²/2s = 6.994 g; mean force 109.74 kN. |  |
| CRS-0029 | m=1600 kg at 50 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 154.32 kJ; mean deceleration v²/2s = 32.78 g; mean force 514.4 kN. |  |
| CRS-0030 | m=1600 kg at 50 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 154.32 kJ; mean deceleration v²/2s = 19.67 g; mean force 308.64 kN. |  |
| CRS-0031 | m=1600 kg at 50 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 154.32 kJ; mean deceleration v²/2s = 14.05 g; mean force 220.46 kN. |  |
| CRS-0032 | m=1600 kg at 50 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 154.32 kJ; mean deceleration v²/2s = 10.93 g; mean force 171.47 kN. |  |
| CRS-0033 | m=1600 kg at 56 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 193.58 kJ; mean deceleration v²/2s = 41.12 g; mean force 645.27 kN. |  |
| CRS-0034 | m=1600 kg at 56 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 193.58 kJ; mean deceleration v²/2s = 24.67 g; mean force 387.16 kN. |  |
| CRS-0035 | m=1600 kg at 56 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 193.58 kJ; mean deceleration v²/2s = 17.62 g; mean force 276.54 kN. |  |
| CRS-0036 | m=1600 kg at 56 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 193.58 kJ; mean deceleration v²/2s = 13.71 g; mean force 215.09 kN. |  |
| CRS-0037 | m=1600 kg at 64 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 252.84 kJ; mean deceleration v²/2s = 53.71 g; mean force 842.8 kN. |  |
| CRS-0038 | m=1600 kg at 64 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 252.84 kJ; mean deceleration v²/2s = 32.23 g; mean force 505.68 kN. |  |
| CRS-0039 | m=1600 kg at 64 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 252.84 kJ; mean deceleration v²/2s = 23.02 g; mean force 361.2 kN. |  |
| CRS-0040 | m=1600 kg at 64 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 252.84 kJ; mean deceleration v²/2s = 17.9 g; mean force 280.93 kN. |  |
| CRS-0041 | m=2200 kg at 30 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 76.389 kJ; mean deceleration v²/2s = 11.8 g; mean force 254.63 kN. |  |
| CRS-0042 | m=2200 kg at 30 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 76.389 kJ; mean deceleration v²/2s = 7.081 g; mean force 152.78 kN. |  |
| CRS-0043 | m=2200 kg at 30 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 76.389 kJ; mean deceleration v²/2s = 5.058 g; mean force 109.13 kN. |  |
| CRS-0044 | m=2200 kg at 30 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 76.389 kJ; mean deceleration v²/2s = 3.934 g; mean force 84.877 kN. |  |
| CRS-0045 | m=2200 kg at 40 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 135.8 kJ; mean deceleration v²/2s = 20.98 g; mean force 452.67 kN. |  |
| CRS-0046 | m=2200 kg at 40 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 135.8 kJ; mean deceleration v²/2s = 12.59 g; mean force 271.6 kN. |  |
| CRS-0047 | m=2200 kg at 40 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 135.8 kJ; mean deceleration v²/2s = 8.992 g; mean force 194 kN. |  |
| CRS-0048 | m=2200 kg at 40 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 135.8 kJ; mean deceleration v²/2s = 6.994 g; mean force 150.89 kN. |  |
| CRS-0049 | m=2200 kg at 50 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 212.19 kJ; mean deceleration v²/2s = 32.78 g; mean force 707.3 kN. |  |
| CRS-0050 | m=2200 kg at 50 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 212.19 kJ; mean deceleration v²/2s = 19.67 g; mean force 424.38 kN. |  |
| CRS-0051 | m=2200 kg at 50 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 212.19 kJ; mean deceleration v²/2s = 14.05 g; mean force 303.13 kN. |  |
| CRS-0052 | m=2200 kg at 50 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 212.19 kJ; mean deceleration v²/2s = 10.93 g; mean force 235.77 kN. |  |
| CRS-0053 | m=2200 kg at 56 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 266.17 kJ; mean deceleration v²/2s = 41.12 g; mean force 887.24 kN. |  |
| CRS-0054 | m=2200 kg at 56 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 266.17 kJ; mean deceleration v²/2s = 24.67 g; mean force 532.35 kN. |  |
| CRS-0055 | m=2200 kg at 56 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 266.17 kJ; mean deceleration v²/2s = 17.62 g; mean force 380.25 kN. |  |
| CRS-0056 | m=2200 kg at 56 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 266.17 kJ; mean deceleration v²/2s = 13.71 g; mean force 295.75 kN. |  |
| CRS-0057 | m=2200 kg at 64 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 347.65 kJ; mean deceleration v²/2s = 53.71 g; mean force 1158.8 kN. |  |
| CRS-0058 | m=2200 kg at 64 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 347.65 kJ; mean deceleration v²/2s = 32.23 g; mean force 695.31 kN. |  |
| CRS-0059 | m=2200 kg at 64 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 347.65 kJ; mean deceleration v²/2s = 23.02 g; mean force 496.65 kN. |  |
| CRS-0060 | m=2200 kg at 64 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 347.65 kJ; mean deceleration v²/2s = 17.9 g; mean force 386.28 kN. |  |
| CRS-0061 | m=3000 kg at 30 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 104.17 kJ; mean deceleration v²/2s = 11.8 g; mean force 347.22 kN. |  |
| CRS-0062 | m=3000 kg at 30 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 104.17 kJ; mean deceleration v²/2s = 7.081 g; mean force 208.33 kN. |  |
| CRS-0063 | m=3000 kg at 30 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 104.17 kJ; mean deceleration v²/2s = 5.058 g; mean force 148.81 kN. |  |
| CRS-0064 | m=3000 kg at 30 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 104.17 kJ; mean deceleration v²/2s = 3.934 g; mean force 115.74 kN. |  |
| CRS-0065 | m=3000 kg at 40 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 185.19 kJ; mean deceleration v²/2s = 20.98 g; mean force 617.28 kN. |  |
| CRS-0066 | m=3000 kg at 40 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 185.19 kJ; mean deceleration v²/2s = 12.59 g; mean force 370.37 kN. |  |
| CRS-0067 | m=3000 kg at 40 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 185.19 kJ; mean deceleration v²/2s = 8.992 g; mean force 264.55 kN. |  |
| CRS-0068 | m=3000 kg at 40 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 185.19 kJ; mean deceleration v²/2s = 6.994 g; mean force 205.76 kN. |  |
| CRS-0069 | m=3000 kg at 50 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 289.35 kJ; mean deceleration v²/2s = 32.78 g; mean force 964.51 kN. |  |
| CRS-0070 | m=3000 kg at 50 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 289.35 kJ; mean deceleration v²/2s = 19.67 g; mean force 578.7 kN. |  |
| CRS-0071 | m=3000 kg at 50 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 289.35 kJ; mean deceleration v²/2s = 14.05 g; mean force 413.36 kN. |  |
| CRS-0072 | m=3000 kg at 50 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 289.35 kJ; mean deceleration v²/2s = 10.93 g; mean force 321.5 kN. |  |
| CRS-0073 | m=3000 kg at 56 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 362.96 kJ; mean deceleration v²/2s = 41.12 g; mean force 1209.9 kN. |  |
| CRS-0074 | m=3000 kg at 56 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 362.96 kJ; mean deceleration v²/2s = 24.67 g; mean force 725.93 kN. |  |
| CRS-0075 | m=3000 kg at 56 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 362.96 kJ; mean deceleration v²/2s = 17.62 g; mean force 518.52 kN. |  |
| CRS-0076 | m=3000 kg at 56 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 362.96 kJ; mean deceleration v²/2s = 13.71 g; mean force 403.29 kN. |  |
| CRS-0077 | m=3000 kg at 64 km/h, crush 0.3 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 474.07 kJ; mean deceleration v²/2s = 53.71 g; mean force 1580.2 kN. |  |
| CRS-0078 | m=3000 kg at 64 km/h, crush 0.5 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 474.07 kJ; mean deceleration v²/2s = 32.23 g; mean force 948.15 kN. |  |
| CRS-0079 | m=3000 kg at 64 km/h, crush 0.7 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 474.07 kJ; mean deceleration v²/2s = 23.02 g; mean force 677.25 kN. |  |
| CRS-0080 | m=3000 kg at 64 km/h, crush 0.9 m | Accuracy | P2 | Compute the energy and mean deceleration. | E = ½mv² = 474.07 kJ; mean deceleration v²/2s = 17.9 g; mean force 526.75 kN. |  |

## Crash workflow

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CRS-0081 | full-width frontal 56 km/h: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for full-width frontal 56 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0082 | full-width frontal 56 km/h: explicit run | Functional | P2 | explicit run for full-width frontal 56 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0083 | full-width frontal 56 km/h: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for full-width frontal 56 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0084 | full-width frontal 56 km/h: intrusion report | Functional | P2 | intrusion report for full-width frontal 56 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0085 | full-width frontal 56 km/h: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for full-width frontal 56 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0086 | full-width frontal 56 km/h: compare with previous revision | Functional | P2 | compare with previous revision for full-width frontal 56 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0087 | ODB 40% 64 km/h: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for ODB 40% 64 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0088 | ODB 40% 64 km/h: explicit run | Functional | P2 | explicit run for ODB 40% 64 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0089 | ODB 40% 64 km/h: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for ODB 40% 64 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0090 | ODB 40% 64 km/h: intrusion report | Functional | P2 | intrusion report for ODB 40% 64 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0091 | ODB 40% 64 km/h: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for ODB 40% 64 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0092 | ODB 40% 64 km/h: compare with previous revision | Functional | P2 | compare with previous revision for ODB 40% 64 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0093 | small overlap: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for small overlap. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0094 | small overlap: explicit run | Functional | P2 | explicit run for small overlap. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0095 | small overlap: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for small overlap. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0096 | small overlap: intrusion report | Functional | P2 | intrusion report for small overlap. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0097 | small overlap: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for small overlap. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0098 | small overlap: compare with previous revision | Functional | P2 | compare with previous revision for small overlap. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0099 | side MDB 50 km/h: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for side MDB 50 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0100 | side MDB 50 km/h: explicit run | Functional | P2 | explicit run for side MDB 50 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0101 | side MDB 50 km/h: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for side MDB 50 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0102 | side MDB 50 km/h: intrusion report | Functional | P2 | intrusion report for side MDB 50 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0103 | side MDB 50 km/h: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for side MDB 50 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0104 | side MDB 50 km/h: compare with previous revision | Functional | P2 | compare with previous revision for side MDB 50 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0105 | side pole 32 km/h: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for side pole 32 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0106 | side pole 32 km/h: explicit run | Functional | P2 | explicit run for side pole 32 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0107 | side pole 32 km/h: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for side pole 32 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0108 | side pole 32 km/h: intrusion report | Functional | P2 | intrusion report for side pole 32 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0109 | side pole 32 km/h: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for side pole 32 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0110 | side pole 32 km/h: compare with previous revision | Functional | P2 | compare with previous revision for side pole 32 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0111 | rear 80 km/h: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for rear 80 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0112 | rear 80 km/h: explicit run | Functional | P2 | explicit run for rear 80 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0113 | rear 80 km/h: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for rear 80 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0114 | rear 80 km/h: intrusion report | Functional | P2 | intrusion report for rear 80 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0115 | rear 80 km/h: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for rear 80 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0116 | rear 80 km/h: compare with previous revision | Functional | P2 | compare with previous revision for rear 80 km/h. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0117 | roof crush 3×weight: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for roof crush 3×weight. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0118 | roof crush 3×weight: explicit run | Functional | P2 | explicit run for roof crush 3×weight. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0119 | roof crush 3×weight: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for roof crush 3×weight. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0120 | roof crush 3×weight: intrusion report | Functional | P2 | intrusion report for roof crush 3×weight. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0121 | roof crush 3×weight: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for roof crush 3×weight. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0122 | roof crush 3×weight: compare with previous revision | Functional | P2 | compare with previous revision for roof crush 3×weight. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0123 | pedestrian head impact: model set-up (mass, contacts) | Functional | P2 | model set-up (mass, contacts) for pedestrian head impact. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0124 | pedestrian head impact: explicit run | Functional | P2 | explicit run for pedestrian head impact. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0125 | pedestrian head impact: energy balance (hourglass < 5%) | Functional | P2 | energy balance (hourglass < 5%) for pedestrian head impact. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0126 | pedestrian head impact: intrusion report | Functional | P2 | intrusion report for pedestrian head impact. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0127 | pedestrian head impact: pulse (accel vs time) | Functional | P2 | pulse (accel vs time) for pedestrian head impact. | Output stored with run, solver, inputs and credibility label. |  |
| CRS-0128 | pedestrian head impact: compare with previous revision | Functional | P2 | compare with previous revision for pedestrian head impact. | Output stored with run, solver, inputs and credibility label. |  |
