# CFD — Flow and thermal

**CATIA-class equivalent:** Fluid / thermal add-ons (STAR-CCM+/Fluent-class, SIMULIA Flow)  
**Autevra workspace:** Simulation; Aircraft; Loads  
**Scope:** Shared  
**Cases:** 278 (Have 0, Partial 140, Gap 138)

Road-load drag, boundary layers, heat transfer and CFD workflow.

[← Back to the index](../README.md)

## Features

- Drag force and power — 140 cases (Partial)
- Flat-plate boundary layer — 25 cases (Gap)
- Heat transfer — 57 cases (Gap)
- CFD workflow — 56 cases (Gap)

## Drag force and power

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CFD-0001 | Cd=0.2, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 47.261 N; power = F·v = 0.6564 kW (ρ = 1.225). |  |
| CFD-0002 | Cd=0.2, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 120.99 N; power = F·v = 2.6886 kW (ρ = 1.225). |  |
| CFD-0003 | Cd=0.2, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 189.04 N; power = F·v = 5.2512 kW (ρ = 1.225). |  |
| CFD-0004 | Cd=0.2, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 319.48 N; power = F·v = 11.537 kW (ρ = 1.225). |  |
| CFD-0005 | Cd=0.2, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 756.17 N; power = F·v = 42.01 kW (ρ = 1.225). |  |
| CFD-0006 | Cd=0.2, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 56.713 N; power = F·v = 0.78768 kW (ρ = 1.225). |  |
| CFD-0007 | Cd=0.2, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 145.19 N; power = F·v = 3.2263 kW (ρ = 1.225). |  |
| CFD-0008 | Cd=0.2, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 226.85 N; power = F·v = 6.3014 kW (ρ = 1.225). |  |
| CFD-0009 | Cd=0.2, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 383.38 N; power = F·v = 13.844 kW (ρ = 1.225). |  |
| CFD-0010 | Cd=0.2, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 907.41 N; power = F·v = 50.412 kW (ρ = 1.225). |  |
| CFD-0011 | Cd=0.2, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 66.165 N; power = F·v = 0.91896 kW (ρ = 1.225). |  |
| CFD-0012 | Cd=0.2, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 169.38 N; power = F·v = 3.7641 kW (ρ = 1.225). |  |
| CFD-0013 | Cd=0.2, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 264.66 N; power = F·v = 7.3517 kW (ρ = 1.225). |  |
| CFD-0014 | Cd=0.2, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 447.28 N; power = F·v = 16.152 kW (ρ = 1.225). |  |
| CFD-0015 | Cd=0.2, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1058.6 N; power = F·v = 58.813 kW (ρ = 1.225). |  |
| CFD-0016 | Cd=0.2, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 80.343 N; power = F·v = 1.1159 kW (ρ = 1.225). |  |
| CFD-0017 | Cd=0.2, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 205.68 N; power = F·v = 4.5706 kW (ρ = 1.225). |  |
| CFD-0018 | Cd=0.2, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 321.37 N; power = F·v = 8.927 kW (ρ = 1.225). |  |
| CFD-0019 | Cd=0.2, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 543.12 N; power = F·v = 19.613 kW (ρ = 1.225). |  |
| CFD-0020 | Cd=0.2, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1285.5 N; power = F·v = 71.416 kW (ρ = 1.225). |  |
| CFD-0021 | Cd=0.24, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 56.713 N; power = F·v = 0.78768 kW (ρ = 1.225). |  |
| CFD-0022 | Cd=0.24, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 145.19 N; power = F·v = 3.2263 kW (ρ = 1.225). |  |
| CFD-0023 | Cd=0.24, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 226.85 N; power = F·v = 6.3014 kW (ρ = 1.225). |  |
| CFD-0024 | Cd=0.24, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 383.38 N; power = F·v = 13.844 kW (ρ = 1.225). |  |
| CFD-0025 | Cd=0.24, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 907.41 N; power = F·v = 50.412 kW (ρ = 1.225). |  |
| CFD-0026 | Cd=0.24, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 68.056 N; power = F·v = 0.94522 kW (ρ = 1.225). |  |
| CFD-0027 | Cd=0.24, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 174.22 N; power = F·v = 3.8716 kW (ρ = 1.225). |  |
| CFD-0028 | Cd=0.24, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 272.22 N; power = F·v = 7.5617 kW (ρ = 1.225). |  |
| CFD-0029 | Cd=0.24, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 460.06 N; power = F·v = 16.613 kW (ρ = 1.225). |  |
| CFD-0030 | Cd=0.24, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1088.9 N; power = F·v = 60.494 kW (ρ = 1.225). |  |
| CFD-0031 | Cd=0.24, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 79.398 N; power = F·v = 1.1028 kW (ρ = 1.225). |  |
| CFD-0032 | Cd=0.24, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 203.26 N; power = F·v = 4.5169 kW (ρ = 1.225). |  |
| CFD-0033 | Cd=0.24, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 317.59 N; power = F·v = 8.822 kW (ρ = 1.225). |  |
| CFD-0034 | Cd=0.24, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 536.73 N; power = F·v = 19.382 kW (ρ = 1.225). |  |
| CFD-0035 | Cd=0.24, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1270.4 N; power = F·v = 70.576 kW (ρ = 1.225). |  |
| CFD-0036 | Cd=0.24, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 96.412 N; power = F·v = 1.3391 kW (ρ = 1.225). |  |
| CFD-0037 | Cd=0.24, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 246.81 N; power = F·v = 5.4848 kW (ρ = 1.225). |  |
| CFD-0038 | Cd=0.24, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 385.65 N; power = F·v = 10.712 kW (ρ = 1.225). |  |
| CFD-0039 | Cd=0.24, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 651.75 N; power = F·v = 23.535 kW (ρ = 1.225). |  |
| CFD-0040 | Cd=0.24, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1542.6 N; power = F·v = 85.7 kW (ρ = 1.225). |  |
| CFD-0041 | Cd=0.28, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 66.165 N; power = F·v = 0.91896 kW (ρ = 1.225). |  |
| CFD-0042 | Cd=0.28, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 169.38 N; power = F·v = 3.7641 kW (ρ = 1.225). |  |
| CFD-0043 | Cd=0.28, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 264.66 N; power = F·v = 7.3517 kW (ρ = 1.225). |  |
| CFD-0044 | Cd=0.28, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 447.28 N; power = F·v = 16.152 kW (ρ = 1.225). |  |
| CFD-0045 | Cd=0.28, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1058.6 N; power = F·v = 58.813 kW (ρ = 1.225). |  |
| CFD-0046 | Cd=0.28, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 79.398 N; power = F·v = 1.1028 kW (ρ = 1.225). |  |
| CFD-0047 | Cd=0.28, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 203.26 N; power = F·v = 4.5169 kW (ρ = 1.225). |  |
| CFD-0048 | Cd=0.28, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 317.59 N; power = F·v = 8.822 kW (ρ = 1.225). |  |
| CFD-0049 | Cd=0.28, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 536.73 N; power = F·v = 19.382 kW (ρ = 1.225). |  |
| CFD-0050 | Cd=0.28, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1270.4 N; power = F·v = 70.576 kW (ρ = 1.225). |  |
| CFD-0051 | Cd=0.28, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 92.631 N; power = F·v = 1.2865 kW (ρ = 1.225). |  |
| CFD-0052 | Cd=0.28, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 237.14 N; power = F·v = 5.2697 kW (ρ = 1.225). |  |
| CFD-0053 | Cd=0.28, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 370.52 N; power = F·v = 10.292 kW (ρ = 1.225). |  |
| CFD-0054 | Cd=0.28, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 626.19 N; power = F·v = 22.612 kW (ρ = 1.225). |  |
| CFD-0055 | Cd=0.28, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1482.1 N; power = F·v = 82.339 kW (ρ = 1.225). |  |
| CFD-0056 | Cd=0.28, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 112.48 N; power = F·v = 1.5622 kW (ρ = 1.225). |  |
| CFD-0057 | Cd=0.28, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 287.95 N; power = F·v = 6.3989 kW (ρ = 1.225). |  |
| CFD-0058 | Cd=0.28, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 449.92 N; power = F·v = 12.498 kW (ρ = 1.225). |  |
| CFD-0059 | Cd=0.28, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 760.37 N; power = F·v = 27.458 kW (ρ = 1.225). |  |
| CFD-0060 | Cd=0.28, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1799.7 N; power = F·v = 99.983 kW (ρ = 1.225). |  |
| CFD-0061 | Cd=0.32, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 75.617 N; power = F·v = 1.0502 kW (ρ = 1.225). |  |
| CFD-0062 | Cd=0.32, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 193.58 N; power = F·v = 4.3018 kW (ρ = 1.225). |  |
| CFD-0063 | Cd=0.32, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 302.47 N; power = F·v = 8.4019 kW (ρ = 1.225). |  |
| CFD-0064 | Cd=0.32, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 511.17 N; power = F·v = 18.459 kW (ρ = 1.225). |  |
| CFD-0065 | Cd=0.32, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1209.9 N; power = F·v = 67.215 kW (ρ = 1.225). |  |
| CFD-0066 | Cd=0.32, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 90.741 N; power = F·v = 1.2603 kW (ρ = 1.225). |  |
| CFD-0067 | Cd=0.32, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 232.3 N; power = F·v = 5.1621 kW (ρ = 1.225). |  |
| CFD-0068 | Cd=0.32, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 362.96 N; power = F·v = 10.082 kW (ρ = 1.225). |  |
| CFD-0069 | Cd=0.32, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 613.41 N; power = F·v = 22.151 kW (ρ = 1.225). |  |
| CFD-0070 | Cd=0.32, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1451.9 N; power = F·v = 80.658 kW (ρ = 1.225). |  |
| CFD-0071 | Cd=0.32, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 105.86 N; power = F·v = 1.4703 kW (ρ = 1.225). |  |
| CFD-0072 | Cd=0.32, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 271.01 N; power = F·v = 6.0225 kW (ρ = 1.225). |  |
| CFD-0073 | Cd=0.32, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 423.46 N; power = F·v = 11.763 kW (ρ = 1.225). |  |
| CFD-0074 | Cd=0.32, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 715.64 N; power = F·v = 25.843 kW (ρ = 1.225). |  |
| CFD-0075 | Cd=0.32, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1693.8 N; power = F·v = 94.102 kW (ρ = 1.225). |  |
| CFD-0076 | Cd=0.32, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 128.55 N; power = F·v = 1.7854 kW (ρ = 1.225). |  |
| CFD-0077 | Cd=0.32, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 329.09 N; power = F·v = 7.313 kW (ρ = 1.225). |  |
| CFD-0078 | Cd=0.32, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 514.2 N; power = F·v = 14.283 kW (ρ = 1.225). |  |
| CFD-0079 | Cd=0.32, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 868.99 N; power = F·v = 31.38 kW (ρ = 1.225). |  |
| CFD-0080 | Cd=0.32, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2056.8 N; power = F·v = 114.27 kW (ρ = 1.225). |  |
| CFD-0081 | Cd=0.38, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 89.796 N; power = F·v = 1.2472 kW (ρ = 1.225). |  |
| CFD-0082 | Cd=0.38, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 229.88 N; power = F·v = 5.1084 kW (ρ = 1.225). |  |
| CFD-0083 | Cd=0.38, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 359.18 N; power = F·v = 9.9773 kW (ρ = 1.225). |  |
| CFD-0084 | Cd=0.38, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 607.02 N; power = F·v = 21.92 kW (ρ = 1.225). |  |
| CFD-0085 | Cd=0.38, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1436.7 N; power = F·v = 79.818 kW (ρ = 1.225). |  |
| CFD-0086 | Cd=0.38, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 107.75 N; power = F·v = 1.4966 kW (ρ = 1.225). |  |
| CFD-0087 | Cd=0.38, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 275.85 N; power = F·v = 6.13 kW (ρ = 1.225). |  |
| CFD-0088 | Cd=0.38, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 431.02 N; power = F·v = 11.973 kW (ρ = 1.225). |  |
| CFD-0089 | Cd=0.38, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 728.42 N; power = F·v = 26.304 kW (ρ = 1.225). |  |
| CFD-0090 | Cd=0.38, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1724.1 N; power = F·v = 95.782 kW (ρ = 1.225). |  |
| CFD-0091 | Cd=0.38, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 125.71 N; power = F·v = 1.746 kW (ρ = 1.225). |  |
| CFD-0092 | Cd=0.38, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 321.83 N; power = F·v = 7.1517 kW (ρ = 1.225). |  |
| CFD-0093 | Cd=0.38, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 502.85 N; power = F·v = 13.968 kW (ρ = 1.225). |  |
| CFD-0094 | Cd=0.38, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 849.82 N; power = F·v = 30.688 kW (ρ = 1.225). |  |
| CFD-0095 | Cd=0.38, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2011.4 N; power = F·v = 111.75 kW (ρ = 1.225). |  |
| CFD-0096 | Cd=0.38, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 152.65 N; power = F·v = 2.1202 kW (ρ = 1.225). |  |
| CFD-0097 | Cd=0.38, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 390.79 N; power = F·v = 8.6842 kW (ρ = 1.225). |  |
| CFD-0098 | Cd=0.38, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 610.61 N; power = F·v = 16.961 kW (ρ = 1.225). |  |
| CFD-0099 | Cd=0.38, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1031.9 N; power = F·v = 37.264 kW (ρ = 1.225). |  |
| CFD-0100 | Cd=0.38, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2442.4 N; power = F·v = 135.69 kW (ρ = 1.225). |  |
| CFD-0101 | Cd=0.45, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 106.34 N; power = F·v = 1.4769 kW (ρ = 1.225). |  |
| CFD-0102 | Cd=0.45, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 272.22 N; power = F·v = 6.0494 kW (ρ = 1.225). |  |
| CFD-0103 | Cd=0.45, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 425.35 N; power = F·v = 11.815 kW (ρ = 1.225). |  |
| CFD-0104 | Cd=0.45, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 718.84 N; power = F·v = 25.958 kW (ρ = 1.225). |  |
| CFD-0105 | Cd=0.45, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1701.4 N; power = F·v = 94.522 kW (ρ = 1.225). |  |
| CFD-0106 | Cd=0.45, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 127.6 N; power = F·v = 1.7723 kW (ρ = 1.225). |  |
| CFD-0107 | Cd=0.45, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 326.67 N; power = F·v = 7.2593 kW (ρ = 1.225). |  |
| CFD-0108 | Cd=0.45, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 510.42 N; power = F·v = 14.178 kW (ρ = 1.225). |  |
| CFD-0109 | Cd=0.45, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 862.6 N; power = F·v = 31.15 kW (ρ = 1.225). |  |
| CFD-0110 | Cd=0.45, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2041.7 N; power = F·v = 113.43 kW (ρ = 1.225). |  |
| CFD-0111 | Cd=0.45, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 148.87 N; power = F·v = 2.0677 kW (ρ = 1.225). |  |
| CFD-0112 | Cd=0.45, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 381.11 N; power = F·v = 8.4691 kW (ρ = 1.225). |  |
| CFD-0113 | Cd=0.45, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 595.49 N; power = F·v = 16.541 kW (ρ = 1.225). |  |
| CFD-0114 | Cd=0.45, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1006.4 N; power = F·v = 36.341 kW (ρ = 1.225). |  |
| CFD-0115 | Cd=0.45, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2381.9 N; power = F·v = 132.33 kW (ρ = 1.225). |  |
| CFD-0116 | Cd=0.45, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 180.77 N; power = F·v = 2.5107 kW (ρ = 1.225). |  |
| CFD-0117 | Cd=0.45, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 462.78 N; power = F·v = 10.284 kW (ρ = 1.225). |  |
| CFD-0118 | Cd=0.45, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 723.09 N; power = F·v = 20.086 kW (ρ = 1.225). |  |
| CFD-0119 | Cd=0.45, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1222 N; power = F·v = 44.129 kW (ρ = 1.225). |  |
| CFD-0120 | Cd=0.45, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2892.4 N; power = F·v = 160.69 kW (ρ = 1.225). |  |
| CFD-0121 | Cd=0.55, A=2.0 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 129.97 N; power = F·v = 1.8051 kW (ρ = 1.225). |  |
| CFD-0122 | Cd=0.55, A=2.0 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 332.72 N; power = F·v = 7.3937 kW (ρ = 1.225). |  |
| CFD-0123 | Cd=0.55, A=2.0 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 519.87 N; power = F·v = 14.441 kW (ρ = 1.225). |  |
| CFD-0124 | Cd=0.55, A=2.0 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 878.58 N; power = F·v = 31.726 kW (ρ = 1.225). |  |
| CFD-0125 | Cd=0.55, A=2.0 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2079.5 N; power = F·v = 115.53 kW (ρ = 1.225). |  |
| CFD-0126 | Cd=0.55, A=2.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 155.96 N; power = F·v = 2.1661 kW (ρ = 1.225). |  |
| CFD-0127 | Cd=0.55, A=2.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 399.26 N; power = F·v = 8.8724 kW (ρ = 1.225). |  |
| CFD-0128 | Cd=0.55, A=2.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 623.84 N; power = F·v = 17.329 kW (ρ = 1.225). |  |
| CFD-0129 | Cd=0.55, A=2.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1054.3 N; power = F·v = 38.072 kW (ρ = 1.225). |  |
| CFD-0130 | Cd=0.55, A=2.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2495.4 N; power = F·v = 138.63 kW (ρ = 1.225). |  |
| CFD-0131 | Cd=0.55, A=2.8 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 181.95 N; power = F·v = 2.5271 kW (ρ = 1.225). |  |
| CFD-0132 | Cd=0.55, A=2.8 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 465.8 N; power = F·v = 10.351 kW (ρ = 1.225). |  |
| CFD-0133 | Cd=0.55, A=2.8 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 727.82 N; power = F·v = 20.217 kW (ρ = 1.225). |  |
| CFD-0134 | Cd=0.55, A=2.8 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1230 N; power = F·v = 44.417 kW (ρ = 1.225). |  |
| CFD-0135 | Cd=0.55, A=2.8 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 2911.3 N; power = F·v = 161.74 kW (ρ = 1.225). |  |
| CFD-0136 | Cd=0.55, A=3.4 m², 50 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 220.94 N; power = F·v = 3.0687 kW (ρ = 1.225). |  |
| CFD-0137 | Cd=0.55, A=3.4 m², 80 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 565.62 N; power = F·v = 12.569 kW (ρ = 1.225). |  |
| CFD-0138 | Cd=0.55, A=3.4 m², 100 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 883.78 N; power = F·v = 24.549 kW (ρ = 1.225). |  |
| CFD-0139 | Cd=0.55, A=3.4 m², 130 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 1493.6 N; power = F·v = 53.935 kW (ρ = 1.225). |  |
| CFD-0140 | Cd=0.55, A=3.4 m², 200 km/h | Accuracy | P2 | Read the road-load aero drag. | F = ½ρv²CdA = 3535.1 N; power = F·v = 196.39 kW (ρ = 1.225). |  |

## Flat-plate boundary layer

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CFD-0141 | Plate L=0.1 m in air at 1 m/s | Accuracy | P2 | Compute skin friction. | Re = 6849; laminar (Blasius): CF = 0.01605. |  |
| CFD-0142 | Plate L=0.1 m in air at 5 m/s | Accuracy | P2 | Compute skin friction. | Re = 34247; laminar (Blasius): CF = 0.007176. |  |
| CFD-0143 | Plate L=0.1 m in air at 10 m/s | Accuracy | P2 | Compute skin friction. | Re = 68493; laminar (Blasius): CF = 0.005074. |  |
| CFD-0144 | Plate L=0.1 m in air at 30 m/s | Accuracy | P2 | Compute skin friction. | Re = 205479; laminar (Blasius): CF = 0.00293. |  |
| CFD-0145 | Plate L=0.1 m in air at 60 m/s | Accuracy | P2 | Compute skin friction. | Re = 410959; laminar (Blasius): CF = 0.002072. |  |
| CFD-0146 | Plate L=0.5 m in air at 1 m/s | Accuracy | P2 | Compute skin friction. | Re = 34247; laminar (Blasius): CF = 0.007176. |  |
| CFD-0147 | Plate L=0.5 m in air at 5 m/s | Accuracy | P2 | Compute skin friction. | Re = 171233; laminar (Blasius): CF = 0.003209. |  |
| CFD-0148 | Plate L=0.5 m in air at 10 m/s | Accuracy | P2 | Compute skin friction. | Re = 342466; laminar (Blasius): CF = 0.002269. |  |
| CFD-0149 | Plate L=0.5 m in air at 30 m/s | Accuracy | P2 | Compute skin friction. | Re = 1027397; turbulent (1/7 power): CF = 0.004644. |  |
| CFD-0150 | Plate L=0.5 m in air at 60 m/s | Accuracy | P2 | Compute skin friction. | Re = 2054795; turbulent (1/7 power): CF = 0.004043. |  |
| CFD-0151 | Plate L=1 m in air at 1 m/s | Accuracy | P2 | Compute skin friction. | Re = 68493; laminar (Blasius): CF = 0.005074. |  |
| CFD-0152 | Plate L=1 m in air at 5 m/s | Accuracy | P2 | Compute skin friction. | Re = 342466; laminar (Blasius): CF = 0.002269. |  |
| CFD-0153 | Plate L=1 m in air at 10 m/s | Accuracy | P2 | Compute skin friction. | Re = 684932; turbulent (1/7 power): CF = 0.005036. |  |
| CFD-0154 | Plate L=1 m in air at 30 m/s | Accuracy | P2 | Compute skin friction. | Re = 2054795; turbulent (1/7 power): CF = 0.004043. |  |
| CFD-0155 | Plate L=1 m in air at 60 m/s | Accuracy | P2 | Compute skin friction. | Re = 4109589; turbulent (1/7 power): CF = 0.003519. |  |
| CFD-0156 | Plate L=2 m in air at 1 m/s | Accuracy | P2 | Compute skin friction. | Re = 136986; laminar (Blasius): CF = 0.003588. |  |
| CFD-0157 | Plate L=2 m in air at 5 m/s | Accuracy | P2 | Compute skin friction. | Re = 684932; turbulent (1/7 power): CF = 0.005036. |  |
| CFD-0158 | Plate L=2 m in air at 10 m/s | Accuracy | P2 | Compute skin friction. | Re = 1369863; turbulent (1/7 power): CF = 0.004384. |  |
| CFD-0159 | Plate L=2 m in air at 30 m/s | Accuracy | P2 | Compute skin friction. | Re = 4109589; turbulent (1/7 power): CF = 0.003519. |  |
| CFD-0160 | Plate L=2 m in air at 60 m/s | Accuracy | P2 | Compute skin friction. | Re = 8219178; turbulent (1/7 power): CF = 0.003064. |  |
| CFD-0161 | Plate L=5 m in air at 1 m/s | Accuracy | P2 | Compute skin friction. | Re = 342466; laminar (Blasius): CF = 0.002269. |  |
| CFD-0162 | Plate L=5 m in air at 5 m/s | Accuracy | P2 | Compute skin friction. | Re = 1712329; turbulent (1/7 power): CF = 0.004193. |  |
| CFD-0163 | Plate L=5 m in air at 10 m/s | Accuracy | P2 | Compute skin friction. | Re = 3424658; turbulent (1/7 power): CF = 0.00365. |  |
| CFD-0164 | Plate L=5 m in air at 30 m/s | Accuracy | P2 | Compute skin friction. | Re = 10273973; turbulent (1/7 power): CF = 0.00293. |  |
| CFD-0165 | Plate L=5 m in air at 60 m/s | Accuracy | P2 | Compute skin friction. | Re = 20547945; turbulent (1/7 power): CF = 0.002551. |  |

## Heat transfer

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CFD-0166 | Wall k=0.04 W/mK, t=2 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 200 W/m². |  |
| CFD-0167 | Wall k=0.04 W/mK, t=2 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 1000 W/m². |  |
| CFD-0168 | Wall k=0.04 W/mK, t=2 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 2000 W/m². |  |
| CFD-0169 | Wall k=0.04 W/mK, t=10 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 40 W/m². |  |
| CFD-0170 | Wall k=0.04 W/mK, t=10 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 200 W/m². |  |
| CFD-0171 | Wall k=0.04 W/mK, t=10 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 400 W/m². |  |
| CFD-0172 | Wall k=0.04 W/mK, t=50 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 8 W/m². |  |
| CFD-0173 | Wall k=0.04 W/mK, t=50 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 40 W/m². |  |
| CFD-0174 | Wall k=0.04 W/mK, t=50 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 80 W/m². |  |
| CFD-0175 | Wall k=0.8 W/mK, t=2 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 4000 W/m². |  |
| CFD-0176 | Wall k=0.8 W/mK, t=2 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 20000 W/m². |  |
| CFD-0177 | Wall k=0.8 W/mK, t=2 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 40000 W/m². |  |
| CFD-0178 | Wall k=0.8 W/mK, t=10 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 800 W/m². |  |
| CFD-0179 | Wall k=0.8 W/mK, t=10 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 4000 W/m². |  |
| CFD-0180 | Wall k=0.8 W/mK, t=10 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 8000 W/m². |  |
| CFD-0181 | Wall k=0.8 W/mK, t=50 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 160 W/m². |  |
| CFD-0182 | Wall k=0.8 W/mK, t=50 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 800 W/m². |  |
| CFD-0183 | Wall k=0.8 W/mK, t=50 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 1600 W/m². |  |
| CFD-0184 | Wall k=16 W/mK, t=2 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 80000 W/m². |  |
| CFD-0185 | Wall k=16 W/mK, t=2 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 400000 W/m². |  |
| CFD-0186 | Wall k=16 W/mK, t=2 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 800000 W/m². |  |
| CFD-0187 | Wall k=16 W/mK, t=10 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 16000 W/m². |  |
| CFD-0188 | Wall k=16 W/mK, t=10 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 80000 W/m². |  |
| CFD-0189 | Wall k=16 W/mK, t=10 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 160000 W/m². |  |
| CFD-0190 | Wall k=16 W/mK, t=50 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 3200 W/m². |  |
| CFD-0191 | Wall k=16 W/mK, t=50 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 16000 W/m². |  |
| CFD-0192 | Wall k=16 W/mK, t=50 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 32000 W/m². |  |
| CFD-0193 | Wall k=50 W/mK, t=2 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 250000 W/m². |  |
| CFD-0194 | Wall k=50 W/mK, t=2 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 1250000 W/m². |  |
| CFD-0195 | Wall k=50 W/mK, t=2 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 2500000 W/m². |  |
| CFD-0196 | Wall k=50 W/mK, t=10 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 50000 W/m². |  |
| CFD-0197 | Wall k=50 W/mK, t=10 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 250000 W/m². |  |
| CFD-0198 | Wall k=50 W/mK, t=10 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 500000 W/m². |  |
| CFD-0199 | Wall k=50 W/mK, t=50 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 10000 W/m². |  |
| CFD-0200 | Wall k=50 W/mK, t=50 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 50000 W/m². |  |
| CFD-0201 | Wall k=50 W/mK, t=50 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 100000 W/m². |  |
| CFD-0202 | Wall k=205 W/mK, t=2 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 1025000 W/m². |  |
| CFD-0203 | Wall k=205 W/mK, t=2 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 5125000 W/m². |  |
| CFD-0204 | Wall k=205 W/mK, t=2 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 10250000 W/m². |  |
| CFD-0205 | Wall k=205 W/mK, t=10 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 205000 W/m². |  |
| CFD-0206 | Wall k=205 W/mK, t=10 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 1025000 W/m². |  |
| CFD-0207 | Wall k=205 W/mK, t=10 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 2050000 W/m². |  |
| CFD-0208 | Wall k=205 W/mK, t=50 mm, ΔT=10 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 41000 W/m². |  |
| CFD-0209 | Wall k=205 W/mK, t=50 mm, ΔT=50 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 205000 W/m². |  |
| CFD-0210 | Wall k=205 W/mK, t=50 mm, ΔT=100 K | Accuracy | P2 | 1D steady conduction. | q = kΔT/t = 410000 W/m². |  |
| CFD-0211 | Radiation ε=0.1, surface 350 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 43.214 W/m². |  |
| CFD-0212 | Radiation ε=0.1, surface 500 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 312.52 W/m². |  |
| CFD-0213 | Radiation ε=0.1, surface 800 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 2280.7 W/m². |  |
| CFD-0214 | Radiation ε=0.1, surface 1200 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 11716 W/m². |  |
| CFD-0215 | Radiation ε=0.5, surface 350 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 216.07 W/m². |  |
| CFD-0216 | Radiation ε=0.5, surface 500 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 1562.6 W/m². |  |
| CFD-0217 | Radiation ε=0.5, surface 800 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 11404 W/m². |  |
| CFD-0218 | Radiation ε=0.5, surface 1200 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 58581 W/m². |  |
| CFD-0219 | Radiation ε=0.9, surface 350 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 388.93 W/m². |  |
| CFD-0220 | Radiation ε=0.9, surface 500 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 2812.7 W/m². |  |
| CFD-0221 | Radiation ε=0.9, surface 800 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 20526 W/m². |  |
| CFD-0222 | Radiation ε=0.9, surface 1200 K to 293 K | Accuracy | P2 | Grey-body radiation to surroundings. | q = εσ(T⁴ − T∞⁴) = 105446 W/m². |  |

## CFD workflow

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CFD-0223 | hatchback: wrap/clean surface | Functional | P2 | wrap/clean surface for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0224 | hatchback: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0225 | hatchback: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0226 | hatchback: k-ω SST steady | Functional | P2 | k-ω SST steady for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0227 | hatchback: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0228 | hatchback: Cd/Cl report | Functional | P2 | Cd/Cl report for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0229 | hatchback: pressure map on model | Functional | P2 | pressure map on model for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0230 | hatchback: mesh independence | Functional | P2 | mesh independence for the hatchback. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0231 | SUV: wrap/clean surface | Functional | P2 | wrap/clean surface for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0232 | SUV: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0233 | SUV: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0234 | SUV: k-ω SST steady | Functional | P2 | k-ω SST steady for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0235 | SUV: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0236 | SUV: Cd/Cl report | Functional | P2 | Cd/Cl report for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0237 | SUV: pressure map on model | Functional | P2 | pressure map on model for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0238 | SUV: mesh independence | Functional | P2 | mesh independence for the SUV. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0239 | trainer wing: wrap/clean surface | Functional | P2 | wrap/clean surface for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0240 | trainer wing: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0241 | trainer wing: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0242 | trainer wing: k-ω SST steady | Functional | P2 | k-ω SST steady for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0243 | trainer wing: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0244 | trainer wing: Cd/Cl report | Functional | P2 | Cd/Cl report for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0245 | trainer wing: pressure map on model | Functional | P2 | pressure map on model for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0246 | trainer wing: mesh independence | Functional | P2 | mesh independence for the trainer wing. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0247 | nacelle: wrap/clean surface | Functional | P2 | wrap/clean surface for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0248 | nacelle: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0249 | nacelle: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0250 | nacelle: k-ω SST steady | Functional | P2 | k-ω SST steady for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0251 | nacelle: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0252 | nacelle: Cd/Cl report | Functional | P2 | Cd/Cl report for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0253 | nacelle: pressure map on model | Functional | P2 | pressure map on model for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0254 | nacelle: mesh independence | Functional | P2 | mesh independence for the nacelle. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0255 | radiator duct: wrap/clean surface | Functional | P2 | wrap/clean surface for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0256 | radiator duct: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0257 | radiator duct: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0258 | radiator duct: k-ω SST steady | Functional | P2 | k-ω SST steady for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0259 | radiator duct: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0260 | radiator duct: Cd/Cl report | Functional | P2 | Cd/Cl report for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0261 | radiator duct: pressure map on model | Functional | P2 | pressure map on model for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0262 | radiator duct: mesh independence | Functional | P2 | mesh independence for the radiator duct. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0263 | brake disc: wrap/clean surface | Functional | P2 | wrap/clean surface for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0264 | brake disc: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0265 | brake disc: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0266 | brake disc: k-ω SST steady | Functional | P2 | k-ω SST steady for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0267 | brake disc: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0268 | brake disc: Cd/Cl report | Functional | P2 | Cd/Cl report for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0269 | brake disc: pressure map on model | Functional | P2 | pressure map on model for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0270 | brake disc: mesh independence | Functional | P2 | mesh independence for the brake disc. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0271 | battery cooling plate: wrap/clean surface | Functional | P2 | wrap/clean surface for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0272 | battery cooling plate: polyhedral mesh 5M cells | Functional | P2 | polyhedral mesh 5M cells for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0273 | battery cooling plate: prism layers y+≈1 | Functional | P2 | prism layers y+≈1 for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0274 | battery cooling plate: k-ω SST steady | Functional | P2 | k-ω SST steady for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0275 | battery cooling plate: convergence (residuals 1e-4, forces ±0.5%) | Functional | P2 | convergence (residuals 1e-4, forces ±0.5%) for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0276 | battery cooling plate: Cd/Cl report | Functional | P2 | Cd/Cl report for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0277 | battery cooling plate: pressure map on model | Functional | P2 | pressure map on model for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
| CFD-0278 | battery cooling plate: mesh independence | Functional | P2 | mesh independence for the battery cooling plate. | Step completes; settings and results stored with the run; credibility label set. |  |
