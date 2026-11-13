# NRG — Electrified powertrain and energy

**CATIA-class equivalent:** Systems / Dymola-class 1D energy modelling  
**Autevra workspace:** Design (powertrain); Simulation  
**Scope:** Land  
**Cases:** 205 (Have 27, Partial 168, Gap 10)

Road load, consumption, battery packs, motors and range.

[← Back to the index](../README.md)

## Features

- Road load and consumption — 144 cases (Partial)
- Battery pack — 24 cases (Partial)
- Motor and drive — 27 cases (Have)
- Charging and thermal — 10 cases (Gap)

## Road load and consumption

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| NRG-0001 | m=1200 kg, 30 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 115.41 N; consumption = 3.562 kWh/100 km; range on 75 kWh usable = 2106 km. |  |
| NRG-0002 | m=1200 kg, 30 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 162.48 N; consumption = 5.015 kWh/100 km; range on 75 kWh usable = 1496 km. |  |
| NRG-0003 | m=1200 kg, 30 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 121.79 N; consumption = 3.759 kWh/100 km; range on 75 kWh usable = 1995 km. |  |
| NRG-0004 | m=1200 kg, 30 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 168.86 N; consumption = 5.212 kWh/100 km; range on 75 kWh usable = 1439 km. |  |
| NRG-0005 | m=1200 kg, 30 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 132.43 N; consumption = 4.087 kWh/100 km; range on 75 kWh usable = 1835 km. |  |
| NRG-0006 | m=1200 kg, 30 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 179.5 N; consumption = 5.54 kWh/100 km; range on 75 kWh usable = 1354 km. |  |
| NRG-0007 | m=1200 kg, 50 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 153.22 N; consumption = 4.729 kWh/100 km; range on 75 kWh usable = 1586 km. |  |
| NRG-0008 | m=1200 kg, 50 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 200.29 N; consumption = 6.182 kWh/100 km; range on 75 kWh usable = 1213 km. |  |
| NRG-0009 | m=1200 kg, 50 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 170.94 N; consumption = 5.276 kWh/100 km; range on 75 kWh usable = 1422 km. |  |
| NRG-0010 | m=1200 kg, 50 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 218.01 N; consumption = 6.729 kWh/100 km; range on 75 kWh usable = 1115 km. |  |
| NRG-0011 | m=1200 kg, 50 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 200.48 N; consumption = 6.188 kWh/100 km; range on 75 kWh usable = 1212 km. |  |
| NRG-0012 | m=1200 kg, 50 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 247.55 N; consumption = 7.641 kWh/100 km; range on 75 kWh usable = 981.6 km. |  |
| NRG-0013 | m=1200 kg, 90 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 285.55 N; consumption = 8.813 kWh/100 km; range on 75 kWh usable = 851 km. |  |
| NRG-0014 | m=1200 kg, 90 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 332.62 N; consumption = 10.27 kWh/100 km; range on 75 kWh usable = 730.6 km. |  |
| NRG-0015 | m=1200 kg, 90 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 342.97 N; consumption = 10.59 kWh/100 km; range on 75 kWh usable = 708.5 km. |  |
| NRG-0016 | m=1200 kg, 90 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 390.04 N; consumption = 12.04 kWh/100 km; range on 75 kWh usable = 623 km. |  |
| NRG-0017 | m=1200 kg, 90 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 438.68 N; consumption = 13.54 kWh/100 km; range on 75 kWh usable = 553.9 km. |  |
| NRG-0018 | m=1200 kg, 90 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 485.75 N; consumption = 14.99 kWh/100 km; range on 75 kWh usable = 500.3 km. |  |
| NRG-0019 | m=1200 kg, 100 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 330.45 N; consumption = 10.2 kWh/100 km; range on 75 kWh usable = 735.4 km. |  |
| NRG-0020 | m=1200 kg, 100 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 377.52 N; consumption = 11.65 kWh/100 km; range on 75 kWh usable = 643.7 km. |  |
| NRG-0021 | m=1200 kg, 100 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 401.34 N; consumption = 12.39 kWh/100 km; range on 75 kWh usable = 605.5 km. |  |
| NRG-0022 | m=1200 kg, 100 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 448.41 N; consumption = 13.84 kWh/100 km; range on 75 kWh usable = 541.9 km. |  |
| NRG-0023 | m=1200 kg, 100 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 519.49 N; consumption = 16.03 kWh/100 km; range on 75 kWh usable = 467.8 km. |  |
| NRG-0024 | m=1200 kg, 100 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 566.56 N; consumption = 17.49 kWh/100 km; range on 75 kWh usable = 428.9 km. |  |
| NRG-0025 | m=1200 kg, 120 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 434.42 N; consumption = 13.41 kWh/100 km; range on 75 kWh usable = 559.4 km. |  |
| NRG-0026 | m=1200 kg, 120 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 481.49 N; consumption = 14.86 kWh/100 km; range on 75 kWh usable = 504.7 km. |  |
| NRG-0027 | m=1200 kg, 120 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 536.5 N; consumption = 16.56 kWh/100 km; range on 75 kWh usable = 452.9 km. |  |
| NRG-0028 | m=1200 kg, 120 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 583.58 N; consumption = 18.01 kWh/100 km; range on 75 kWh usable = 416.4 km. |  |
| NRG-0029 | m=1200 kg, 120 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 706.64 N; consumption = 21.81 kWh/100 km; range on 75 kWh usable = 343.9 km. |  |
| NRG-0030 | m=1200 kg, 120 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 753.72 N; consumption = 23.26 kWh/100 km; range on 75 kWh usable = 322.4 km. |  |
| NRG-0031 | m=1200 kg, 130 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 493.5 N; consumption = 15.23 kWh/100 km; range on 75 kWh usable = 492.4 km. |  |
| NRG-0032 | m=1200 kg, 130 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 540.57 N; consumption = 16.68 kWh/100 km; range on 75 kWh usable = 449.5 km. |  |
| NRG-0033 | m=1200 kg, 130 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 613.3 N; consumption = 18.93 kWh/100 km; range on 75 kWh usable = 396.2 km. |  |
| NRG-0034 | m=1200 kg, 130 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 660.38 N; consumption = 20.38 kWh/100 km; range on 75 kWh usable = 368 km. |  |
| NRG-0035 | m=1200 kg, 130 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 812.98 N; consumption = 25.09 kWh/100 km; range on 75 kWh usable = 298.9 km. |  |
| NRG-0036 | m=1200 kg, 130 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 860.05 N; consumption = 26.54 kWh/100 km; range on 75 kWh usable = 282.5 km. |  |
| NRG-0037 | m=1600 kg, 30 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 146.79 N; consumption = 4.531 kWh/100 km; range on 75 kWh usable = 1655 km. |  |
| NRG-0038 | m=1600 kg, 30 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 209.56 N; consumption = 6.468 kWh/100 km; range on 75 kWh usable = 1160 km. |  |
| NRG-0039 | m=1600 kg, 30 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 153.17 N; consumption = 4.728 kWh/100 km; range on 75 kWh usable = 1586 km. |  |
| NRG-0040 | m=1600 kg, 30 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 215.94 N; consumption = 6.665 kWh/100 km; range on 75 kWh usable = 1125 km. |  |
| NRG-0041 | m=1600 kg, 30 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 163.81 N; consumption = 5.056 kWh/100 km; range on 75 kWh usable = 1483 km. |  |
| NRG-0042 | m=1600 kg, 30 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 226.57 N; consumption = 6.993 kWh/100 km; range on 75 kWh usable = 1073 km. |  |
| NRG-0043 | m=1600 kg, 50 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 184.6 N; consumption = 5.698 kWh/100 km; range on 75 kWh usable = 1316 km. |  |
| NRG-0044 | m=1600 kg, 50 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 247.36 N; consumption = 7.635 kWh/100 km; range on 75 kWh usable = 982.4 km. |  |
| NRG-0045 | m=1600 kg, 50 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 202.32 N; consumption = 6.245 kWh/100 km; range on 75 kWh usable = 1201 km. |  |
| NRG-0046 | m=1600 kg, 50 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 265.09 N; consumption = 8.182 kWh/100 km; range on 75 kWh usable = 916.7 km. |  |
| NRG-0047 | m=1600 kg, 50 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 231.86 N; consumption = 7.156 kWh/100 km; range on 75 kWh usable = 1048 km. |  |
| NRG-0048 | m=1600 kg, 50 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 294.62 N; consumption = 9.093 kWh/100 km; range on 75 kWh usable = 824.8 km. |  |
| NRG-0049 | m=1600 kg, 90 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 316.93 N; consumption = 9.782 kWh/100 km; range on 75 kWh usable = 766.7 km. |  |
| NRG-0050 | m=1600 kg, 90 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 379.69 N; consumption = 11.72 kWh/100 km; range on 75 kWh usable = 640 km. |  |
| NRG-0051 | m=1600 kg, 90 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 374.35 N; consumption = 11.55 kWh/100 km; range on 75 kWh usable = 649.1 km. |  |
| NRG-0052 | m=1600 kg, 90 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 437.12 N; consumption = 13.49 kWh/100 km; range on 75 kWh usable = 555.9 km. |  |
| NRG-0053 | m=1600 kg, 90 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 470.06 N; consumption = 14.51 kWh/100 km; range on 75 kWh usable = 517 km. |  |
| NRG-0054 | m=1600 kg, 90 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 532.82 N; consumption = 16.45 kWh/100 km; range on 75 kWh usable = 456.1 km. |  |
| NRG-0055 | m=1600 kg, 100 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 361.83 N; consumption = 11.17 kWh/100 km; range on 75 kWh usable = 671.6 km. |  |
| NRG-0056 | m=1600 kg, 100 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 424.59 N; consumption = 13.1 kWh/100 km; range on 75 kWh usable = 572.3 km. |  |
| NRG-0057 | m=1600 kg, 100 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 432.72 N; consumption = 13.36 kWh/100 km; range on 75 kWh usable = 561.6 km. |  |
| NRG-0058 | m=1600 kg, 100 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 495.48 N; consumption = 15.29 kWh/100 km; range on 75 kWh usable = 490.4 km. |  |
| NRG-0059 | m=1600 kg, 100 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 550.87 N; consumption = 17 kWh/100 km; range on 75 kWh usable = 441.1 km. |  |
| NRG-0060 | m=1600 kg, 100 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 613.63 N; consumption = 18.94 kWh/100 km; range on 75 kWh usable = 396 km. |  |
| NRG-0061 | m=1600 kg, 120 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 465.8 N; consumption = 14.38 kWh/100 km; range on 75 kWh usable = 521.7 km. |  |
| NRG-0062 | m=1600 kg, 120 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 528.57 N; consumption = 16.31 kWh/100 km; range on 75 kWh usable = 459.7 km. |  |
| NRG-0063 | m=1600 kg, 120 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 567.89 N; consumption = 17.53 kWh/100 km; range on 75 kWh usable = 427.9 km. |  |
| NRG-0064 | m=1600 kg, 120 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 630.65 N; consumption = 19.46 kWh/100 km; range on 75 kWh usable = 385.3 km. |  |
| NRG-0065 | m=1600 kg, 120 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 738.03 N; consumption = 22.78 kWh/100 km; range on 75 kWh usable = 329.3 km. |  |
| NRG-0066 | m=1600 kg, 120 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 800.79 N; consumption = 24.72 kWh/100 km; range on 75 kWh usable = 303.5 km. |  |
| NRG-0067 | m=1600 kg, 130 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 524.88 N; consumption = 16.2 kWh/100 km; range on 75 kWh usable = 463 km. |  |
| NRG-0068 | m=1600 kg, 130 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 587.64 N; consumption = 18.14 kWh/100 km; range on 75 kWh usable = 413.5 km. |  |
| NRG-0069 | m=1600 kg, 130 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 644.69 N; consumption = 19.9 kWh/100 km; range on 75 kWh usable = 376.9 km. |  |
| NRG-0070 | m=1600 kg, 130 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 707.45 N; consumption = 21.83 kWh/100 km; range on 75 kWh usable = 343.5 km. |  |
| NRG-0071 | m=1600 kg, 130 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 844.36 N; consumption = 26.06 kWh/100 km; range on 75 kWh usable = 287.8 km. |  |
| NRG-0072 | m=1600 kg, 130 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 907.12 N; consumption = 28 kWh/100 km; range on 75 kWh usable = 267.9 km. |  |
| NRG-0073 | m=2000 kg, 30 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 178.17 N; consumption = 5.499 kWh/100 km; range on 75 kWh usable = 1364 km. |  |
| NRG-0074 | m=2000 kg, 30 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 256.63 N; consumption = 7.921 kWh/100 km; range on 75 kWh usable = 946.9 km. |  |
| NRG-0075 | m=2000 kg, 30 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 184.55 N; consumption = 5.696 kWh/100 km; range on 75 kWh usable = 1317 km. |  |
| NRG-0076 | m=2000 kg, 30 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 263.01 N; consumption = 8.118 kWh/100 km; range on 75 kWh usable = 923.9 km. |  |
| NRG-0077 | m=2000 kg, 30 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 195.19 N; consumption = 6.024 kWh/100 km; range on 75 kWh usable = 1245 km. |  |
| NRG-0078 | m=2000 kg, 30 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 273.64 N; consumption = 8.446 kWh/100 km; range on 75 kWh usable = 888 km. |  |
| NRG-0079 | m=2000 kg, 50 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 215.98 N; consumption = 6.666 kWh/100 km; range on 75 kWh usable = 1125 km. |  |
| NRG-0080 | m=2000 kg, 50 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 294.44 N; consumption = 9.088 kWh/100 km; range on 75 kWh usable = 825.3 km. |  |
| NRG-0081 | m=2000 kg, 50 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 233.71 N; consumption = 7.213 kWh/100 km; range on 75 kWh usable = 1040 km. |  |
| NRG-0082 | m=2000 kg, 50 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 312.16 N; consumption = 9.635 kWh/100 km; range on 75 kWh usable = 778.5 km. |  |
| NRG-0083 | m=2000 kg, 50 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 263.24 N; consumption = 8.125 kWh/100 km; range on 75 kWh usable = 923.1 km. |  |
| NRG-0084 | m=2000 kg, 50 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 341.7 N; consumption = 10.55 kWh/100 km; range on 75 kWh usable = 711.2 km. |  |
| NRG-0085 | m=2000 kg, 90 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 348.31 N; consumption = 10.75 kWh/100 km; range on 75 kWh usable = 697.6 km. |  |
| NRG-0086 | m=2000 kg, 90 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 426.77 N; consumption = 13.17 kWh/100 km; range on 75 kWh usable = 569.4 km. |  |
| NRG-0087 | m=2000 kg, 90 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 405.73 N; consumption = 12.52 kWh/100 km; range on 75 kWh usable = 598.9 km. |  |
| NRG-0088 | m=2000 kg, 90 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 484.19 N; consumption = 14.94 kWh/100 km; range on 75 kWh usable = 501.9 km. |  |
| NRG-0089 | m=2000 kg, 90 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 501.44 N; consumption = 15.48 kWh/100 km; range on 75 kWh usable = 484.6 km. |  |
| NRG-0090 | m=2000 kg, 90 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 579.89 N; consumption = 17.9 kWh/100 km; range on 75 kWh usable = 419 km. |  |
| NRG-0091 | m=2000 kg, 100 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 393.21 N; consumption = 12.14 kWh/100 km; range on 75 kWh usable = 618 km. |  |
| NRG-0092 | m=2000 kg, 100 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 471.66 N; consumption = 14.56 kWh/100 km; range on 75 kWh usable = 515.2 km. |  |
| NRG-0093 | m=2000 kg, 100 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 464.1 N; consumption = 14.32 kWh/100 km; range on 75 kWh usable = 523.6 km. |  |
| NRG-0094 | m=2000 kg, 100 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 542.55 N; consumption = 16.75 kWh/100 km; range on 75 kWh usable = 447.9 km. |  |
| NRG-0095 | m=2000 kg, 100 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 582.25 N; consumption = 17.97 kWh/100 km; range on 75 kWh usable = 417.3 km. |  |
| NRG-0096 | m=2000 kg, 100 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 660.71 N; consumption = 20.39 kWh/100 km; range on 75 kWh usable = 367.8 km. |  |
| NRG-0097 | m=2000 kg, 120 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 497.18 N; consumption = 15.35 kWh/100 km; range on 75 kWh usable = 488.8 km. |  |
| NRG-0098 | m=2000 kg, 120 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 575.64 N; consumption = 17.77 kWh/100 km; range on 75 kWh usable = 422.1 km. |  |
| NRG-0099 | m=2000 kg, 120 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 599.27 N; consumption = 18.5 kWh/100 km; range on 75 kWh usable = 405.5 km. |  |
| NRG-0100 | m=2000 kg, 120 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 677.72 N; consumption = 20.92 kWh/100 km; range on 75 kWh usable = 358.6 km. |  |
| NRG-0101 | m=2000 kg, 120 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 769.41 N; consumption = 23.75 kWh/100 km; range on 75 kWh usable = 315.8 km. |  |
| NRG-0102 | m=2000 kg, 120 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 847.86 N; consumption = 26.17 kWh/100 km; range on 75 kWh usable = 286.6 km. |  |
| NRG-0103 | m=2000 kg, 130 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 556.26 N; consumption = 17.17 kWh/100 km; range on 75 kWh usable = 436.8 km. |  |
| NRG-0104 | m=2000 kg, 130 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 634.71 N; consumption = 19.59 kWh/100 km; range on 75 kWh usable = 382.8 km. |  |
| NRG-0105 | m=2000 kg, 130 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 676.07 N; consumption = 20.87 kWh/100 km; range on 75 kWh usable = 359.4 km. |  |
| NRG-0106 | m=2000 kg, 130 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 754.52 N; consumption = 23.29 kWh/100 km; range on 75 kWh usable = 322.1 km. |  |
| NRG-0107 | m=2000 kg, 130 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 875.74 N; consumption = 27.03 kWh/100 km; range on 75 kWh usable = 277.5 km. |  |
| NRG-0108 | m=2000 kg, 130 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 954.2 N; consumption = 29.45 kWh/100 km; range on 75 kWh usable = 254.7 km. |  |
| NRG-0109 | m=2500 kg, 30 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 217.4 N; consumption = 6.71 kWh/100 km; range on 75 kWh usable = 1118 km. |  |
| NRG-0110 | m=2500 kg, 30 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 315.47 N; consumption = 9.737 kWh/100 km; range on 75 kWh usable = 770.3 km. |  |
| NRG-0111 | m=2500 kg, 30 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 223.78 N; consumption = 6.907 kWh/100 km; range on 75 kWh usable = 1086 km. |  |
| NRG-0112 | m=2500 kg, 30 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 321.85 N; consumption = 9.934 kWh/100 km; range on 75 kWh usable = 755 km. |  |
| NRG-0113 | m=2500 kg, 30 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 234.41 N; consumption = 7.235 kWh/100 km; range on 75 kWh usable = 1037 km. |  |
| NRG-0114 | m=2500 kg, 30 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 332.48 N; consumption = 10.26 kWh/100 km; range on 75 kWh usable = 730.9 km. |  |
| NRG-0115 | m=2500 kg, 50 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 255.21 N; consumption = 7.877 kWh/100 km; range on 75 kWh usable = 952.2 km. |  |
| NRG-0116 | m=2500 kg, 50 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 353.28 N; consumption = 10.9 kWh/100 km; range on 75 kWh usable = 687.8 km. |  |
| NRG-0117 | m=2500 kg, 50 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 272.93 N; consumption = 8.424 kWh/100 km; range on 75 kWh usable = 890.3 km. |  |
| NRG-0118 | m=2500 kg, 50 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 371 N; consumption = 11.45 kWh/100 km; range on 75 kWh usable = 655 km. |  |
| NRG-0119 | m=2500 kg, 50 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 302.47 N; consumption = 9.335 kWh/100 km; range on 75 kWh usable = 803.4 km. |  |
| NRG-0120 | m=2500 kg, 50 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 400.54 N; consumption = 12.36 kWh/100 km; range on 75 kWh usable = 606.7 km. |  |
| NRG-0121 | m=2500 kg, 90 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 387.54 N; consumption = 11.96 kWh/100 km; range on 75 kWh usable = 627 km. |  |
| NRG-0122 | m=2500 kg, 90 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 485.61 N; consumption = 14.99 kWh/100 km; range on 75 kWh usable = 500.4 km. |  |
| NRG-0123 | m=2500 kg, 90 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 444.96 N; consumption = 13.73 kWh/100 km; range on 75 kWh usable = 546.1 km. |  |
| NRG-0124 | m=2500 kg, 90 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 543.03 N; consumption = 16.76 kWh/100 km; range on 75 kWh usable = 447.5 km. |  |
| NRG-0125 | m=2500 kg, 90 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 540.66 N; consumption = 16.69 kWh/100 km; range on 75 kWh usable = 449.4 km. |  |
| NRG-0126 | m=2500 kg, 90 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 638.73 N; consumption = 19.71 kWh/100 km; range on 75 kWh usable = 380.4 km. |  |
| NRG-0127 | m=2500 kg, 100 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 432.44 N; consumption = 13.35 kWh/100 km; range on 75 kWh usable = 561.9 km. |  |
| NRG-0128 | m=2500 kg, 100 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 530.5 N; consumption = 16.37 kWh/100 km; range on 75 kWh usable = 458.1 km. |  |
| NRG-0129 | m=2500 kg, 100 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 503.33 N; consumption = 15.53 kWh/100 km; range on 75 kWh usable = 482.8 km. |  |
| NRG-0130 | m=2500 kg, 100 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 601.39 N; consumption = 18.56 kWh/100 km; range on 75 kWh usable = 404.1 km. |  |
| NRG-0131 | m=2500 kg, 100 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 621.48 N; consumption = 19.18 kWh/100 km; range on 75 kWh usable = 391 km. |  |
| NRG-0132 | m=2500 kg, 100 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 719.55 N; consumption = 22.21 kWh/100 km; range on 75 kWh usable = 337.7 km. |  |
| NRG-0133 | m=2500 kg, 120 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 536.41 N; consumption = 16.56 kWh/100 km; range on 75 kWh usable = 453 km. |  |
| NRG-0134 | m=2500 kg, 120 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 634.48 N; consumption = 19.58 kWh/100 km; range on 75 kWh usable = 383 km. |  |
| NRG-0135 | m=2500 kg, 120 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 638.49 N; consumption = 19.71 kWh/100 km; range on 75 kWh usable = 380.6 km. |  |
| NRG-0136 | m=2500 kg, 120 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 736.56 N; consumption = 22.73 kWh/100 km; range on 75 kWh usable = 329.9 km. |  |
| NRG-0137 | m=2500 kg, 120 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 808.63 N; consumption = 24.96 kWh/100 km; range on 75 kWh usable = 300.5 km. |  |
| NRG-0138 | m=2500 kg, 120 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 906.7 N; consumption = 27.98 kWh/100 km; range on 75 kWh usable = 268 km. |  |
| NRG-0139 | m=2500 kg, 130 km/h, CdA=0.5, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 595.49 N; consumption = 18.38 kWh/100 km; range on 75 kWh usable = 408.1 km. |  |
| NRG-0140 | m=2500 kg, 130 km/h, CdA=0.5, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 693.55 N; consumption = 21.41 kWh/100 km; range on 75 kWh usable = 350.4 km. |  |
| NRG-0141 | m=2500 kg, 130 km/h, CdA=0.65, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 715.29 N; consumption = 22.08 kWh/100 km; range on 75 kWh usable = 339.7 km. |  |
| NRG-0142 | m=2500 kg, 130 km/h, CdA=0.65, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 813.36 N; consumption = 25.1 kWh/100 km; range on 75 kWh usable = 298.8 km. |  |
| NRG-0143 | m=2500 kg, 130 km/h, CdA=0.9, Crr=0.008 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 914.97 N; consumption = 28.24 kWh/100 km; range on 75 kWh usable = 265.6 km. |  |
| NRG-0144 | m=2500 kg, 130 km/h, CdA=0.9, Crr=0.012 | Accuracy | P2 | Steady-speed energy estimate (η drivetrain 0.9). | F = mgCrr + ½ρCdAv² = 1013 N; consumption = 31.27 kWh/100 km; range on 75 kWh usable = 239.9 km. |  |

## Battery pack

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| NRG-0145 | Pack 96s1p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 50 Ah; 17.28 kWh (3.6 V/cell); cell count 96. |  |
| NRG-0146 | Pack 96s1p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 100 Ah; 34.56 kWh (3.6 V/cell); cell count 96. |  |
| NRG-0147 | Pack 96s2p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 100 Ah; 34.56 kWh (3.6 V/cell); cell count 192. |  |
| NRG-0148 | Pack 96s2p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 200 Ah; 69.12 kWh (3.6 V/cell); cell count 192. |  |
| NRG-0149 | Pack 96s4p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 200 Ah; 69.12 kWh (3.6 V/cell); cell count 384. |  |
| NRG-0150 | Pack 96s4p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 400 Ah; 138.2 kWh (3.6 V/cell); cell count 384. |  |
| NRG-0151 | Pack 96s46p, 3.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 138 Ah; 47.69 kWh (3.6 V/cell); cell count 4416. |  |
| NRG-0152 | Pack 96s46p, 5.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 345.6 V; 230 Ah; 79.49 kWh (3.6 V/cell); cell count 4416. |  |
| NRG-0153 | Pack 108s1p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 50 Ah; 19.44 kWh (3.6 V/cell); cell count 108. |  |
| NRG-0154 | Pack 108s1p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 100 Ah; 38.88 kWh (3.6 V/cell); cell count 108. |  |
| NRG-0155 | Pack 108s2p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 100 Ah; 38.88 kWh (3.6 V/cell); cell count 216. |  |
| NRG-0156 | Pack 108s2p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 200 Ah; 77.76 kWh (3.6 V/cell); cell count 216. |  |
| NRG-0157 | Pack 108s4p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 200 Ah; 77.76 kWh (3.6 V/cell); cell count 432. |  |
| NRG-0158 | Pack 108s4p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 400 Ah; 155.5 kWh (3.6 V/cell); cell count 432. |  |
| NRG-0159 | Pack 108s46p, 3.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 138 Ah; 53.65 kWh (3.6 V/cell); cell count 4968. |  |
| NRG-0160 | Pack 108s46p, 5.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 388.8 V; 230 Ah; 89.42 kWh (3.6 V/cell); cell count 4968. |  |
| NRG-0161 | Pack 192s1p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 50 Ah; 34.56 kWh (3.6 V/cell); cell count 192. |  |
| NRG-0162 | Pack 192s1p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 100 Ah; 69.12 kWh (3.6 V/cell); cell count 192. |  |
| NRG-0163 | Pack 192s2p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 100 Ah; 69.12 kWh (3.6 V/cell); cell count 384. |  |
| NRG-0164 | Pack 192s2p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 200 Ah; 138.2 kWh (3.6 V/cell); cell count 384. |  |
| NRG-0165 | Pack 192s4p, 50.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 200 Ah; 138.2 kWh (3.6 V/cell); cell count 768. |  |
| NRG-0166 | Pack 192s4p, 100.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 400 Ah; 276.5 kWh (3.6 V/cell); cell count 768. |  |
| NRG-0167 | Pack 192s46p, 3.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 138 Ah; 95.39 kWh (3.6 V/cell); cell count 8832. |  |
| NRG-0168 | Pack 192s46p, 5.0 Ah cells | Accuracy | P2 | Configure the pack. | Nominal 691.2 V; 230 Ah; 159 kWh (3.6 V/cell); cell count 8832. |  |

## Motor and drive

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| NRG-0169 | Motor 150 N·m at 4000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 62.832 kW; wheel torque = 1091.2 N·m (η 0.97); wheel speed 533.33 rpm. |  |
| NRG-0170 | Motor 150 N·m at 4000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 62.832 kW; wheel torque = 1309.5 N·m (η 0.97); wheel speed 444.44 rpm. |  |
| NRG-0171 | Motor 150 N·m at 4000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 62.832 kW; wheel torque = 1600.5 N·m (η 0.97); wheel speed 363.64 rpm. |  |
| NRG-0172 | Motor 150 N·m at 8000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 125.66 kW; wheel torque = 1091.2 N·m (η 0.97); wheel speed 1066.7 rpm. |  |
| NRG-0173 | Motor 150 N·m at 8000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 125.66 kW; wheel torque = 1309.5 N·m (η 0.97); wheel speed 888.89 rpm. |  |
| NRG-0174 | Motor 150 N·m at 8000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 125.66 kW; wheel torque = 1600.5 N·m (η 0.97); wheel speed 727.27 rpm. |  |
| NRG-0175 | Motor 150 N·m at 12000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 188.5 kW; wheel torque = 1091.2 N·m (η 0.97); wheel speed 1600 rpm. |  |
| NRG-0176 | Motor 150 N·m at 12000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 188.5 kW; wheel torque = 1309.5 N·m (η 0.97); wheel speed 1333.3 rpm. |  |
| NRG-0177 | Motor 150 N·m at 12000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 188.5 kW; wheel torque = 1600.5 N·m (η 0.97); wheel speed 1090.9 rpm. |  |
| NRG-0178 | Motor 300 N·m at 4000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 125.66 kW; wheel torque = 2182.5 N·m (η 0.97); wheel speed 533.33 rpm. |  |
| NRG-0179 | Motor 300 N·m at 4000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 125.66 kW; wheel torque = 2619 N·m (η 0.97); wheel speed 444.44 rpm. |  |
| NRG-0180 | Motor 300 N·m at 4000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 125.66 kW; wheel torque = 3201 N·m (η 0.97); wheel speed 363.64 rpm. |  |
| NRG-0181 | Motor 300 N·m at 8000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 251.33 kW; wheel torque = 2182.5 N·m (η 0.97); wheel speed 1066.7 rpm. |  |
| NRG-0182 | Motor 300 N·m at 8000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 251.33 kW; wheel torque = 2619 N·m (η 0.97); wheel speed 888.89 rpm. |  |
| NRG-0183 | Motor 300 N·m at 8000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 251.33 kW; wheel torque = 3201 N·m (η 0.97); wheel speed 727.27 rpm. |  |
| NRG-0184 | Motor 300 N·m at 12000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 376.99 kW; wheel torque = 2182.5 N·m (η 0.97); wheel speed 1600 rpm. |  |
| NRG-0185 | Motor 300 N·m at 12000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 376.99 kW; wheel torque = 2619 N·m (η 0.97); wheel speed 1333.3 rpm. |  |
| NRG-0186 | Motor 300 N·m at 12000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 376.99 kW; wheel torque = 3201 N·m (η 0.97); wheel speed 1090.9 rpm. |  |
| NRG-0187 | Motor 450 N·m at 4000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 188.5 kW; wheel torque = 3273.8 N·m (η 0.97); wheel speed 533.33 rpm. |  |
| NRG-0188 | Motor 450 N·m at 4000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 188.5 kW; wheel torque = 3928.5 N·m (η 0.97); wheel speed 444.44 rpm. |  |
| NRG-0189 | Motor 450 N·m at 4000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 188.5 kW; wheel torque = 4801.5 N·m (η 0.97); wheel speed 363.64 rpm. |  |
| NRG-0190 | Motor 450 N·m at 8000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 376.99 kW; wheel torque = 3273.8 N·m (η 0.97); wheel speed 1066.7 rpm. |  |
| NRG-0191 | Motor 450 N·m at 8000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 376.99 kW; wheel torque = 3928.5 N·m (η 0.97); wheel speed 888.89 rpm. |  |
| NRG-0192 | Motor 450 N·m at 8000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 376.99 kW; wheel torque = 4801.5 N·m (η 0.97); wheel speed 727.27 rpm. |  |
| NRG-0193 | Motor 450 N·m at 12000 rpm, ratio 7.5 | Accuracy | P2 | Read motor/wheel figures. | P = 565.49 kW; wheel torque = 3273.8 N·m (η 0.97); wheel speed 1600 rpm. |  |
| NRG-0194 | Motor 450 N·m at 12000 rpm, ratio 9.0 | Accuracy | P2 | Read motor/wheel figures. | P = 565.49 kW; wheel torque = 3928.5 N·m (η 0.97); wheel speed 1333.3 rpm. |  |
| NRG-0195 | Motor 450 N·m at 12000 rpm, ratio 11.0 | Accuracy | P2 | Read motor/wheel figures. | P = 565.49 kW; wheel torque = 4801.5 N·m (η 0.97); wheel speed 1090.9 rpm. |  |

## Charging and thermal

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| NRG-0196 | Charge 10→80% at 7.4 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 425.7 min; taper modelled above 80%. |  |
| NRG-0197 | Charge 20→100% at 7.4 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 364.9 min; taper modelled above 80%. |  |
| NRG-0198 | Charge 10→80% at 11 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 286.4 min; taper modelled above 80%. |  |
| NRG-0199 | Charge 20→100% at 11 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 245.5 min; taper modelled above 80%. |  |
| NRG-0200 | Charge 10→80% at 50 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 63 min; taper modelled above 80%. |  |
| NRG-0201 | Charge 20→100% at 50 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 54 min; taper modelled above 80%. |  |
| NRG-0202 | Charge 10→80% at 150 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 21 min; taper modelled above 80%. |  |
| NRG-0203 | Charge 20→100% at 150 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 18 min; taper modelled above 80%. |  |
| NRG-0204 | Charge 10→80% at 350 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 9 min; taper modelled above 80%. |  |
| NRG-0205 | Charge 20→100% at 350 kW (75 kWh) | Accuracy | P2 | Estimate charge time with taper above 80%. | Constant-power portion = 7.714 min; taper modelled above 80%. |  |
