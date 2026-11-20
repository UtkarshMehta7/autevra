# MFG — Manufacturing engineering and CAM

**CATIA-class equivalent:** DELMIA process planning / Prismatic Machining / NC  
**Autevra workspace:** Production; Manufacturing  
**Scope:** Shared  
**Cases:** 364 (Have 248, Partial 0, Gap 116)

Process plans, line balancing, cost/CO2, machining data and NC output.

[← Back to the index](../README.md)

## Features

- Takt and line balance — 212 cases (Have)
- Machining data — 32 cases (Gap)
- NC operations — 60 cases (Gap)
- Process planning, cost and CO2 — 36 cases (Have)
- Additive manufacturing — 24 cases (Gap)

## Takt and line balance

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MFG-0001 | Takt: 7.5 h available, 100 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 270 s. |  |
| MFG-0002 | Takt: 7.5 h available, 240 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 112.5 s. |  |
| MFG-0003 | Takt: 7.5 h available, 480 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 56.25 s. |  |
| MFG-0004 | Takt: 7.5 h available, 960 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 28.125 s. |  |
| MFG-0005 | Takt: 15 h available, 100 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 540 s. |  |
| MFG-0006 | Takt: 15 h available, 240 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 225 s. |  |
| MFG-0007 | Takt: 15 h available, 480 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 112.5 s. |  |
| MFG-0008 | Takt: 15 h available, 960 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 56.25 s. |  |
| MFG-0009 | Takt: 22.5 h available, 100 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 810 s. |  |
| MFG-0010 | Takt: 22.5 h available, 240 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 337.5 s. |  |
| MFG-0011 | Takt: 22.5 h available, 480 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 168.75 s. |  |
| MFG-0012 | Takt: 22.5 h available, 960 units/day | Accuracy | P2 | Set shift time and demand. | Takt = 84.375 s. |  |
| MFG-0013 | Line balance #01: 10 tasks, takt 114.3 s | Accuracy | P2 | Balance stations. | Σt = 683.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [60.8, 42.6, 87.4, 53.8, 68.4, 46.5, 69.1, 80.3, 86.1, 88.4] |
| MFG-0014 | Line balance #02: 12 tasks, takt 140.7 s | Accuracy | P2 | Balance stations. | Σt = 498.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [23.1, 89.5, 31.1, 25.6, 81.9, 13.2, 47.3, 56.6, 70.4, 23.0, 19.9, 17.0] |
| MFG-0015 | Line balance #03: 9 tasks, takt 107.2 s | Accuracy | P2 | Balance stations. | Σt = 391.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [20.1, 58.6, 26.5, 57.3, 58.0, 13.6, 39.3, 78.5, 39.9] |
| MFG-0016 | Line balance #04: 10 tasks, takt 134.4 s | Accuracy | P2 | Balance stations. | Σt = 560.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [45.4, 57.1, 75.6, 63.0, 38.8, 68.4, 89.6, 49.5, 27.4, 45.6] |
| MFG-0017 | Line balance #05: 9 tasks, takt 158.1 s | Accuracy | P2 | Balance stations. | Σt = 403.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [45.2, 79.2, 77.6, 21.2, 58.9, 41.1, 15.5, 27.6, 37.3] |
| MFG-0018 | Line balance #06: 10 tasks, takt 131.5 s | Accuracy | P2 | Balance stations. | Σt = 522.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [80.5, 49.3, 83.3, 45.0, 31.3, 28.8, 44.5, 72.4, 74.8, 12.7] |
| MFG-0019 | Line balance #07: 6 tasks, takt 99.0 s | Accuracy | P2 | Balance stations. | Σt = 245.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [23.7, 73.3, 74.8, 26.4, 18.3, 28.6] |
| MFG-0020 | Line balance #08: 11 tasks, takt 125.2 s | Accuracy | P2 | Balance stations. | Σt = 594.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [27.4, 43.5, 69.7, 24.9, 65.8, 87.1, 22.0, 75.4, 83.7, 63.8, 31.2] |
| MFG-0021 | Line balance #09: 7 tasks, takt 167.1 s | Accuracy | P2 | Balance stations. | Σt = 260.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [48.0, 83.8, 22.3, 15.5, 15.1, 60.1, 15.5] |
| MFG-0022 | Line balance #10: 6 tasks, takt 70.0 s | Accuracy | P2 | Balance stations. | Σt = 264.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [32.0, 56.8, 29.3, 57.6, 20.8, 68.4] |
| MFG-0023 | Line balance #11: 7 tasks, takt 152.9 s | Accuracy | P2 | Balance stations. | Σt = 396.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [81.2, 65.7, 71.7, 16.4, 56.8, 29.7, 75.2] |
| MFG-0024 | Line balance #12: 4 tasks, takt 108.2 s | Accuracy | P2 | Balance stations. | Σt = 212 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [32.9, 21.7, 84.0, 73.4] |
| MFG-0025 | Line balance #13: 12 tasks, takt 142.4 s | Accuracy | P2 | Balance stations. | Σt = 796.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [71.9, 49.4, 59.5, 58.0, 18.3, 83.5, 57.5, 74.7, 77.6, 77.9, 87.9, 79.9] |
| MFG-0026 | Line balance #14: 8 tasks, takt 96.5 s | Accuracy | P2 | Balance stations. | Σt = 361.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [63.7, 79.9, 45.3, 22.1, 34.3, 15.0, 77.4, 23.6] |
| MFG-0027 | Line balance #15: 11 tasks, takt 128.1 s | Accuracy | P2 | Balance stations. | Σt = 403.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [52.1, 32.8, 34.3, 27.6, 14.2, 44.8, 17.0, 71.9, 17.7, 39.5, 51.3] |
| MFG-0028 | Line balance #16: 10 tasks, takt 140.9 s | Accuracy | P2 | Balance stations. | Σt = 466.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [63.1, 69.2, 23.0, 28.9, 21.1, 16.7, 87.3, 28.3, 75.7, 52.9] |
| MFG-0029 | Line balance #17: 6 tasks, takt 66.2 s | Accuracy | P2 | Balance stations. | Σt = 236.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [61.1, 60.1, 28.2, 13.9, 34.1, 39.2] |
| MFG-0030 | Line balance #18: 8 tasks, takt 129.6 s | Accuracy | P2 | Balance stations. | Σt = 339.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [12.6, 22.4, 23.5, 45.2, 58.3, 58.6, 82.0, 36.8] |
| MFG-0031 | Line balance #19: 8 tasks, takt 89.5 s | Accuracy | P2 | Balance stations. | Σt = 460.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [71.8, 49.3, 66.6, 78.9, 22.3, 79.3, 21.6, 70.3] |
| MFG-0032 | Line balance #20: 12 tasks, takt 115.0 s | Accuracy | P2 | Balance stations. | Σt = 511.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [85.3, 84.6, 19.4, 24.3, 18.8, 10.9, 62.2, 31.4, 34.2, 25.6, 82.7, 32.4] |
| MFG-0033 | Line balance #21: 11 tasks, takt 156.6 s | Accuracy | P2 | Balance stations. | Σt = 386.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [31.5, 44.7, 19.8, 15.7, 10.5, 23.1, 53.9, 60.1, 15.0, 30.3, 81.6] |
| MFG-0034 | Line balance #22: 9 tasks, takt 93.3 s | Accuracy | P2 | Balance stations. | Σt = 461.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [51.8, 87.1, 78.7, 72.9, 21.1, 14.6, 46.8, 32.1, 56.4] |
| MFG-0035 | Line balance #23: 8 tasks, takt 94.3 s | Accuracy | P2 | Balance stations. | Σt = 351.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [32.4, 50.7, 56.3, 78.2, 34.5, 52.5, 23.9, 22.7] |
| MFG-0036 | Line balance #24: 8 tasks, takt 116.3 s | Accuracy | P2 | Balance stations. | Σt = 277.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [30.2, 37.8, 22.5, 41.5, 52.0, 16.5, 65.5, 11.8] |
| MFG-0037 | Line balance #25: 8 tasks, takt 112.7 s | Accuracy | P2 | Balance stations. | Σt = 344.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [72.3, 45.1, 44.9, 43.1, 27.6, 47.3, 34.4, 29.8] |
| MFG-0038 | Line balance #26: 11 tasks, takt 126.6 s | Accuracy | P2 | Balance stations. | Σt = 511 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [83.7, 21.7, 88.6, 52.1, 31.6, 51.1, 63.9, 37.8, 12.4, 17.0, 51.1] |
| MFG-0039 | Line balance #27: 11 tasks, takt 91.9 s | Accuracy | P2 | Balance stations. | Σt = 517.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [18.5, 43.4, 82.7, 70.2, 55.6, 11.0, 47.8, 81.0, 68.7, 25.9, 12.8] |
| MFG-0040 | Line balance #28: 7 tasks, takt 127.2 s | Accuracy | P2 | Balance stations. | Σt = 345 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [88.8, 19.5, 63.5, 61.2, 16.3, 45.6, 50.1] |
| MFG-0041 | Line balance #29: 9 tasks, takt 103.2 s | Accuracy | P2 | Balance stations. | Σt = 400.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [26.5, 42.2, 42.8, 23.6, 52.4, 57.4, 46.6, 87.6, 21.0] |
| MFG-0042 | Line balance #30: 11 tasks, takt 161.5 s | Accuracy | P2 | Balance stations. | Σt = 557 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [87.3, 32.5, 42.3, 53.3, 51.2, 55.6, 68.5, 29.5, 15.4, 38.8, 82.6] |
| MFG-0043 | Line balance #31: 10 tasks, takt 78.9 s | Accuracy | P2 | Balance stations. | Σt = 522.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [78.1, 37.1, 52.0, 36.8, 77.1, 55.4, 18.4, 46.0, 45.9, 75.8] |
| MFG-0044 | Line balance #32: 12 tasks, takt 103.7 s | Accuracy | P2 | Balance stations. | Σt = 590.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [45.4, 79.2, 50.5, 62.6, 45.5, 71.2, 21.9, 23.2, 85.2, 39.1, 32.2, 34.2] |
| MFG-0045 | Line balance #33: 4 tasks, takt 142.5 s | Accuracy | P2 | Balance stations. | Σt = 199.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [29.3, 63.3, 87.4, 19.8] |
| MFG-0046 | Line balance #34: 11 tasks, takt 159.9 s | Accuracy | P2 | Balance stations. | Σt = 496.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [13.7, 61.7, 74.5, 48.8, 10.6, 72.5, 88.9, 32.8, 15.6, 40.4, 37.4] |
| MFG-0047 | Line balance #35: 9 tasks, takt 142.0 s | Accuracy | P2 | Balance stations. | Σt = 389.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [19.6, 16.1, 50.1, 26.7, 60.6, 34.0, 74.2, 30.5, 77.9] |
| MFG-0048 | Line balance #36: 11 tasks, takt 153.9 s | Accuracy | P2 | Balance stations. | Σt = 440 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [68.5, 61.2, 20.5, 15.5, 19.0, 39.7, 24.4, 83.4, 33.4, 58.8, 15.6] |
| MFG-0049 | Line balance #37: 12 tasks, takt 126.5 s | Accuracy | P2 | Balance stations. | Σt = 689.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [67.8, 85.3, 82.6, 80.3, 77.1, 75.9, 21.7, 24.0, 11.4, 89.6, 51.9, 21.6] |
| MFG-0050 | Line balance #38: 7 tasks, takt 87.9 s | Accuracy | P2 | Balance stations. | Σt = 299.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [38.7, 11.3, 41.5, 86.7, 69.7, 32.7, 19.2] |
| MFG-0051 | Line balance #39: 4 tasks, takt 142.0 s | Accuracy | P2 | Balance stations. | Σt = 230 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [14.6, 75.0, 52.6, 87.8] |
| MFG-0052 | Line balance #40: 10 tasks, takt 83.5 s | Accuracy | P2 | Balance stations. | Σt = 453.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [64.6, 69.1, 36.7, 32.3, 12.0, 37.5, 58.4, 64.2, 21.0, 58.1] |
| MFG-0053 | Line balance #41: 8 tasks, takt 126.8 s | Accuracy | P2 | Balance stations. | Σt = 402.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [75.8, 26.8, 86.0, 57.1, 53.0, 72.5, 19.5, 12.0] |
| MFG-0054 | Line balance #42: 9 tasks, takt 109.8 s | Accuracy | P2 | Balance stations. | Σt = 543.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [46.5, 74.3, 58.3, 37.3, 66.0, 57.6, 81.9, 73.8, 47.4] |
| MFG-0055 | Line balance #43: 7 tasks, takt 139.1 s | Accuracy | P2 | Balance stations. | Σt = 310.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [52.5, 72.0, 23.2, 32.1, 33.1, 63.7, 33.8] |
| MFG-0056 | Line balance #44: 6 tasks, takt 137.0 s | Accuracy | P2 | Balance stations. | Σt = 329.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [47.0, 63.1, 31.8, 33.2, 86.8, 67.4] |
| MFG-0057 | Line balance #45: 5 tasks, takt 151.8 s | Accuracy | P2 | Balance stations. | Σt = 195.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [34.8, 23.2, 83.9, 11.7, 41.5] |
| MFG-0058 | Line balance #46: 7 tasks, takt 69.1 s | Accuracy | P2 | Balance stations. | Σt = 267.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [14.3, 38.0, 25.3, 25.1, 56.7, 50.2, 58.1] |
| MFG-0059 | Line balance #47: 7 tasks, takt 119.4 s | Accuracy | P2 | Balance stations. | Σt = 340.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [15.4, 44.1, 31.9, 87.9, 43.2, 58.9, 59.5] |
| MFG-0060 | Line balance #48: 11 tasks, takt 136.0 s | Accuracy | P2 | Balance stations. | Σt = 606.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [88.3, 17.4, 33.9, 80.0, 68.7, 75.9, 15.2, 82.2, 78.3, 16.4, 49.8] |
| MFG-0061 | Line balance #49: 12 tasks, takt 102.8 s | Accuracy | P2 | Balance stations. | Σt = 532.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [66.1, 23.9, 81.6, 79.7, 19.8, 24.8, 42.7, 13.3, 59.3, 11.6, 76.6, 33.0] |
| MFG-0062 | Line balance #50: 10 tasks, takt 127.3 s | Accuracy | P2 | Balance stations. | Σt = 379.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [39.0, 14.3, 61.6, 25.4, 84.7, 10.7, 60.8, 24.9, 15.5, 42.7] |
| MFG-0063 | Line balance #51: 4 tasks, takt 76.3 s | Accuracy | P2 | Balance stations. | Σt = 127.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [42.4, 31.1, 14.1, 39.8] |
| MFG-0064 | Line balance #52: 9 tasks, takt 161.7 s | Accuracy | P2 | Balance stations. | Σt = 523.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [85.7, 79.6, 17.0, 64.9, 84.3, 66.8, 38.7, 66.0, 20.9] |
| MFG-0065 | Line balance #53: 10 tasks, takt 103.6 s | Accuracy | P2 | Balance stations. | Σt = 635.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [81.3, 61.1, 52.2, 51.4, 77.2, 75.9, 86.8, 43.0, 75.4, 30.9] |
| MFG-0066 | Line balance #54: 9 tasks, takt 91.2 s | Accuracy | P2 | Balance stations. | Σt = 508 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [71.8, 15.9, 86.6, 51.2, 65.1, 17.5, 75.3, 88.9, 35.7] |
| MFG-0067 | Line balance #55: 9 tasks, takt 120.0 s | Accuracy | P2 | Balance stations. | Σt = 539.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [82.8, 79.9, 60.9, 78.5, 34.8, 22.7, 73.4, 25.7, 81.1] |
| MFG-0068 | Line balance #56: 7 tasks, takt 115.6 s | Accuracy | P2 | Balance stations. | Σt = 426 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [80.2, 32.6, 25.1, 74.5, 57.8, 69.6, 86.2] |
| MFG-0069 | Line balance #57: 12 tasks, takt 106.0 s | Accuracy | P2 | Balance stations. | Σt = 523.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [11.4, 59.5, 20.7, 86.3, 59.8, 32.0, 38.5, 19.1, 36.2, 85.5, 29.4, 45.2] |
| MFG-0070 | Line balance #58: 6 tasks, takt 106.8 s | Accuracy | P2 | Balance stations. | Σt = 280.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [20.1, 76.0, 35.1, 49.9, 38.5, 60.7] |
| MFG-0071 | Line balance #59: 5 tasks, takt 102.1 s | Accuracy | P2 | Balance stations. | Σt = 231 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [65.3, 35.8, 10.8, 75.9, 43.2] |
| MFG-0072 | Line balance #60: 6 tasks, takt 96.3 s | Accuracy | P2 | Balance stations. | Σt = 408.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [69.0, 62.0, 81.2, 87.4, 80.4, 28.8] |
| MFG-0073 | Line balance #61: 10 tasks, takt 109.9 s | Accuracy | P2 | Balance stations. | Σt = 402.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [12.5, 39.4, 37.3, 24.6, 42.3, 63.3, 58.0, 32.0, 20.1, 73.3] |
| MFG-0074 | Line balance #62: 12 tasks, takt 133.8 s | Accuracy | P2 | Balance stations. | Σt = 598.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [84.0, 50.0, 55.2, 82.6, 25.6, 24.9, 76.3, 24.9, 20.8, 54.0, 36.8, 63.8] |
| MFG-0075 | Line balance #63: 10 tasks, takt 104.7 s | Accuracy | P2 | Balance stations. | Σt = 391.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [18.2, 62.6, 64.5, 48.8, 43.8, 10.7, 14.2, 25.3, 20.2, 83.5] |
| MFG-0076 | Line balance #64: 11 tasks, takt 131.7 s | Accuracy | P2 | Balance stations. | Σt = 586.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [46.0, 31.6, 85.9, 72.3, 79.0, 30.3, 82.0, 11.7, 45.3, 72.6, 30.0] |
| MFG-0077 | Line balance #65: 11 tasks, takt 135.2 s | Accuracy | P2 | Balance stations. | Σt = 609.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [43.4, 23.3, 86.4, 72.1, 53.9, 79.8, 53.6, 81.5, 72.4, 12.2, 30.6] |
| MFG-0078 | Line balance #66: 9 tasks, takt 156.2 s | Accuracy | P2 | Balance stations. | Σt = 478.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [39.5, 31.5, 62.1, 56.7, 61.5, 36.0, 83.2, 87.7, 20.4] |
| MFG-0079 | Line balance #67: 6 tasks, takt 118.7 s | Accuracy | P2 | Balance stations. | Σt = 304.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [30.5, 47.8, 20.8, 77.0, 54.4, 73.8] |
| MFG-0080 | Line balance #68: 6 tasks, takt 81.0 s | Accuracy | P2 | Balance stations. | Σt = 238.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [62.7, 59.6, 22.7, 42.2, 37.9, 13.5] |
| MFG-0081 | Line balance #69: 11 tasks, takt 148.2 s | Accuracy | P2 | Balance stations. | Σt = 503.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [29.9, 56.7, 50.0, 48.1, 76.4, 44.4, 23.2, 75.9, 10.4, 55.0, 33.2] |
| MFG-0082 | Line balance #70: 10 tasks, takt 81.7 s | Accuracy | P2 | Balance stations. | Σt = 519.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [40.4, 35.5, 31.0, 47.5, 69.4, 71.6, 63.4, 38.5, 66.6, 55.3] |
| MFG-0083 | Line balance #71: 5 tasks, takt 95.0 s | Accuracy | P2 | Balance stations. | Σt = 268.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [82.9, 22.1, 49.3, 56.4, 58.1] |
| MFG-0084 | Line balance #72: 6 tasks, takt 87.6 s | Accuracy | P2 | Balance stations. | Σt = 264.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [47.4, 20.0, 44.8, 80.1, 34.0, 38.5] |
| MFG-0085 | Line balance #73: 9 tasks, takt 118.1 s | Accuracy | P2 | Balance stations. | Σt = 441.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [12.2, 13.2, 66.7, 12.3, 42.1, 78.7, 86.6, 61.1, 69.0] |
| MFG-0086 | Line balance #74: 7 tasks, takt 149.9 s | Accuracy | P2 | Balance stations. | Σt = 426.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [83.9, 74.0, 85.6, 41.0, 31.8, 26.1, 84.1] |
| MFG-0087 | Line balance #75: 7 tasks, takt 159.2 s | Accuracy | P2 | Balance stations. | Σt = 303.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [87.7, 37.7, 21.1, 54.6, 46.8, 33.6, 21.9] |
| MFG-0088 | Line balance #76: 10 tasks, takt 112.9 s | Accuracy | P2 | Balance stations. | Σt = 420.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [24.8, 56.1, 55.6, 17.1, 53.2, 64.6, 42.3, 24.5, 42.1, 39.8] |
| MFG-0089 | Line balance #77: 6 tasks, takt 111.3 s | Accuracy | P2 | Balance stations. | Σt = 209 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [32.0, 20.3, 19.8, 46.4, 58.8, 31.7] |
| MFG-0090 | Line balance #78: 8 tasks, takt 109.5 s | Accuracy | P2 | Balance stations. | Σt = 418.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [60.6, 59.3, 84.4, 69.6, 43.9, 18.9, 70.0, 11.9] |
| MFG-0091 | Line balance #79: 9 tasks, takt 85.5 s | Accuracy | P2 | Balance stations. | Σt = 546.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [74.1, 30.6, 64.5, 81.3, 69.3, 28.5, 63.3, 52.4, 82.4] |
| MFG-0092 | Line balance #80: 9 tasks, takt 100.7 s | Accuracy | P2 | Balance stations. | Σt = 476.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [69.0, 29.8, 42.8, 11.6, 85.3, 68.4, 56.9, 38.7, 74.1] |
| MFG-0093 | Line balance #81: 12 tasks, takt 78.6 s | Accuracy | P2 | Balance stations. | Σt = 521.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [22.1, 41.0, 69.7, 53.0, 43.3, 25.9, 12.8, 61.9, 58.0, 38.2, 47.0, 48.3] |
| MFG-0094 | Line balance #82: 5 tasks, takt 84.4 s | Accuracy | P2 | Balance stations. | Σt = 151.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [17.2, 75.2, 22.1, 16.2, 21.2] |
| MFG-0095 | Line balance #83: 4 tasks, takt 115.2 s | Accuracy | P2 | Balance stations. | Σt = 287.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [82.7, 71.4, 48.9, 84.7] |
| MFG-0096 | Line balance #84: 8 tasks, takt 108.9 s | Accuracy | P2 | Balance stations. | Σt = 317.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [76.4, 21.7, 51.9, 54.8, 25.7, 33.9, 28.0, 25.2] |
| MFG-0097 | Line balance #85: 11 tasks, takt 161.5 s | Accuracy | P2 | Balance stations. | Σt = 486.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [16.3, 48.5, 45.9, 10.5, 65.4, 22.7, 62.6, 49.2, 51.0, 82.0, 32.3] |
| MFG-0098 | Line balance #86: 8 tasks, takt 176.6 s | Accuracy | P2 | Balance stations. | Σt = 502.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [37.0, 30.6, 85.0, 84.6, 81.1, 63.5, 30.5, 90.0] |
| MFG-0099 | Line balance #87: 10 tasks, takt 131.3 s | Accuracy | P2 | Balance stations. | Σt = 559.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [50.7, 49.7, 53.6, 68.6, 82.8, 50.7, 52.2, 14.9, 85.7, 51.0] |
| MFG-0100 | Line balance #88: 8 tasks, takt 92.9 s | Accuracy | P2 | Balance stations. | Σt = 360.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [45.4, 12.7, 54.0, 85.2, 45.3, 40.1, 64.9, 12.7] |
| MFG-0101 | Line balance #89: 10 tasks, takt 120.8 s | Accuracy | P2 | Balance stations. | Σt = 547.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [71.3, 86.1, 19.6, 41.6, 86.8, 57.0, 48.8, 87.0, 29.8, 19.3] |
| MFG-0102 | Line balance #90: 11 tasks, takt 157.7 s | Accuracy | P2 | Balance stations. | Σt = 527.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [10.1, 26.8, 35.1, 84.6, 77.0, 59.1, 27.9, 76.3, 43.4, 32.4, 54.4] |
| MFG-0103 | Line balance #91: 11 tasks, takt 124.9 s | Accuracy | P2 | Balance stations. | Σt = 604.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [81.2, 58.3, 80.1, 31.1, 49.9, 31.0, 51.4, 59.1, 24.3, 73.9, 64.2] |
| MFG-0104 | Line balance #92: 5 tasks, takt 163.3 s | Accuracy | P2 | Balance stations. | Σt = 271.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [44.8, 82.0, 29.3, 77.7, 37.3] |
| MFG-0105 | Line balance #93: 11 tasks, takt 107.8 s | Accuracy | P2 | Balance stations. | Σt = 609.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [75.2, 69.2, 37.4, 69.5, 41.7, 30.8, 10.4, 75.0, 71.8, 75.3, 52.8] |
| MFG-0106 | Line balance #94: 11 tasks, takt 100.3 s | Accuracy | P2 | Balance stations. | Σt = 619.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [84.3, 17.4, 89.1, 25.6, 76.4, 33.8, 71.3, 19.0, 56.3, 66.1, 80.2] |
| MFG-0107 | Line balance #95: 5 tasks, takt 121.6 s | Accuracy | P2 | Balance stations. | Σt = 177.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [22.5, 68.5, 16.3, 51.8, 18.8] |
| MFG-0108 | Line balance #96: 7 tasks, takt 126.0 s | Accuracy | P2 | Balance stations. | Σt = 329.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [26.0, 21.3, 74.1, 52.8, 30.3, 51.9, 73.5] |
| MFG-0109 | Line balance #97: 5 tasks, takt 168.3 s | Accuracy | P2 | Balance stations. | Σt = 353.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [68.2, 87.6, 55.6, 69.1, 72.7] |
| MFG-0110 | Line balance #98: 6 tasks, takt 167.9 s | Accuracy | P2 | Balance stations. | Σt = 278 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [21.1, 39.7, 43.3, 85.8, 68.8, 19.3] |
| MFG-0111 | Line balance #99: 6 tasks, takt 79.1 s | Accuracy | P2 | Balance stations. | Σt = 292.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [35.5, 52.0, 32.3, 67.1, 40.7, 64.7] |
| MFG-0112 | Line balance #100: 9 tasks, takt 93.6 s | Accuracy | P2 | Balance stations. | Σt = 513.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [83.9, 19.1, 71.1, 88.6, 13.1, 56.0, 69.1, 42.2, 70.2] |
| MFG-0113 | Line balance #101: 8 tasks, takt 106.0 s | Accuracy | P2 | Balance stations. | Σt = 372.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [21.1, 82.7, 42.2, 12.0, 70.9, 24.4, 34.9, 84.4] |
| MFG-0114 | Line balance #102: 11 tasks, takt 133.3 s | Accuracy | P2 | Balance stations. | Σt = 392.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [23.6, 16.0, 71.9, 36.7, 22.7, 36.9, 46.7, 31.2, 24.8, 38.3, 44.0] |
| MFG-0115 | Line balance #103: 4 tasks, takt 105.5 s | Accuracy | P2 | Balance stations. | Σt = 231.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [53.6, 15.1, 75.9, 87.3] |
| MFG-0116 | Line balance #104: 9 tasks, takt 87.7 s | Accuracy | P2 | Balance stations. | Σt = 375.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [44.1, 25.0, 60.6, 38.1, 13.8, 82.1, 19.4, 30.7, 61.8] |
| MFG-0117 | Line balance #105: 6 tasks, takt 85.0 s | Accuracy | P2 | Balance stations. | Σt = 315.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [68.5, 79.7, 36.8, 14.6, 66.4, 49.3] |
| MFG-0118 | Line balance #106: 9 tasks, takt 169.6 s | Accuracy | P2 | Balance stations. | Σt = 488.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [39.1, 77.4, 27.4, 20.5, 88.1, 77.3, 54.7, 43.8, 59.9] |
| MFG-0119 | Line balance #107: 8 tasks, takt 115.6 s | Accuracy | P2 | Balance stations. | Σt = 405.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [81.7, 25.2, 44.3, 85.1, 12.6, 54.8, 83.2, 18.6] |
| MFG-0120 | Line balance #108: 9 tasks, takt 138.3 s | Accuracy | P2 | Balance stations. | Σt = 525.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [29.9, 88.9, 36.5, 30.4, 73.9, 88.1, 88.5, 26.7, 62.7] |
| MFG-0121 | Line balance #109: 12 tasks, takt 123.8 s | Accuracy | P2 | Balance stations. | Σt = 669.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [58.1, 59.4, 44.4, 34.7, 55.7, 36.6, 56.2, 64.6, 72.0, 65.4, 73.9, 48.8] |
| MFG-0122 | Line balance #110: 4 tasks, takt 124.6 s | Accuracy | P2 | Balance stations. | Σt = 226.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [40.2, 57.8, 87.1, 41.4] |
| MFG-0123 | Line balance #111: 12 tasks, takt 144.5 s | Accuracy | P2 | Balance stations. | Σt = 567.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [59.9, 23.7, 17.2, 68.9, 60.3, 10.4, 51.7, 65.4, 25.3, 46.0, 65.3, 73.3] |
| MFG-0124 | Line balance #112: 6 tasks, takt 138.6 s | Accuracy | P2 | Balance stations. | Σt = 269.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [33.7, 24.4, 70.1, 71.2, 29.3, 40.5] |
| MFG-0125 | Line balance #113: 8 tasks, takt 98.1 s | Accuracy | P2 | Balance stations. | Σt = 439.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [11.3, 32.4, 46.0, 76.7, 83.8, 81.6, 27.3, 80.4] |
| MFG-0126 | Line balance #114: 10 tasks, takt 138.1 s | Accuracy | P2 | Balance stations. | Σt = 524.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [36.4, 59.1, 13.1, 63.7, 78.6, 72.4, 50.4, 83.7, 45.4, 21.8] |
| MFG-0127 | Line balance #115: 5 tasks, takt 150.7 s | Accuracy | P2 | Balance stations. | Σt = 253.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [81.9, 17.9, 50.3, 74.8, 28.7] |
| MFG-0128 | Line balance #116: 12 tasks, takt 163.4 s | Accuracy | P2 | Balance stations. | Σt = 627.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [42.3, 65.4, 38.1, 12.6, 79.6, 28.6, 83.8, 56.0, 40.8, 84.2, 63.4, 32.3] |
| MFG-0129 | Line balance #117: 10 tasks, takt 123.9 s | Accuracy | P2 | Balance stations. | Σt = 557.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [65.1, 69.6, 45.2, 67.2, 78.5, 43.3, 26.4, 31.7, 40.6, 89.9] |
| MFG-0130 | Line balance #118: 4 tasks, takt 85.2 s | Accuracy | P2 | Balance stations. | Σt = 163 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [34.9, 35.9, 73.4, 18.8] |
| MFG-0131 | Line balance #119: 5 tasks, takt 96.7 s | Accuracy | P2 | Balance stations. | Σt = 255.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [62.4, 71.5, 26.9, 39.1, 55.4] |
| MFG-0132 | Line balance #120: 12 tasks, takt 90.1 s | Accuracy | P2 | Balance stations. | Σt = 578.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [48.6, 26.9, 88.6, 87.9, 23.4, 56.9, 49.7, 12.8, 40.7, 62.1, 10.9, 69.8] |
| MFG-0133 | Line balance #121: 9 tasks, takt 129.1 s | Accuracy | P2 | Balance stations. | Σt = 555.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [77.9, 58.9, 53.4, 86.1, 43.9, 36.1, 80.4, 75.5, 43.6] |
| MFG-0134 | Line balance #122: 12 tasks, takt 85.1 s | Accuracy | P2 | Balance stations. | Σt = 661.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 8; efficiency = Σt/(n·takt) reported. | tasks [62.3, 31.5, 47.1, 75.8, 70.4, 67.8, 48.2, 53.7, 36.9, 54.1, 37.0, 76.9] |
| MFG-0135 | Line balance #123: 4 tasks, takt 84.3 s | Accuracy | P2 | Balance stations. | Σt = 163.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [56.5, 13.6, 46.0, 47.8] |
| MFG-0136 | Line balance #124: 9 tasks, takt 143.0 s | Accuracy | P2 | Balance stations. | Σt = 372.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [15.1, 80.3, 10.1, 56.2, 21.0, 27.7, 44.5, 31.4, 86.3] |
| MFG-0137 | Line balance #125: 4 tasks, takt 153.0 s | Accuracy | P2 | Balance stations. | Σt = 220.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [39.3, 88.7, 78.8, 13.9] |
| MFG-0138 | Line balance #126: 4 tasks, takt 94.6 s | Accuracy | P2 | Balance stations. | Σt = 198.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [35.9, 62.0, 67.2, 33.4] |
| MFG-0139 | Line balance #127: 5 tasks, takt 126.5 s | Accuracy | P2 | Balance stations. | Σt = 352.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [87.2, 69.7, 28.6, 89.9, 77.1] |
| MFG-0140 | Line balance #128: 9 tasks, takt 84.3 s | Accuracy | P2 | Balance stations. | Σt = 394.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [70.6, 11.9, 55.6, 31.5, 60.8, 39.3, 27.0, 67.2, 30.8] |
| MFG-0141 | Line balance #129: 6 tasks, takt 172.9 s | Accuracy | P2 | Balance stations. | Σt = 318.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [12.2, 87.3, 69.8, 69.1, 51.3, 28.9] |
| MFG-0142 | Line balance #130: 12 tasks, takt 140.4 s | Accuracy | P2 | Balance stations. | Σt = 580.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [71.4, 13.2, 57.8, 56.1, 15.6, 79.6, 15.3, 15.6, 40.0, 70.2, 63.0, 82.3] |
| MFG-0143 | Line balance #131: 4 tasks, takt 122.2 s | Accuracy | P2 | Balance stations. | Σt = 171.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [43.0, 30.2, 10.4, 87.5] |
| MFG-0144 | Line balance #132: 4 tasks, takt 152.4 s | Accuracy | P2 | Balance stations. | Σt = 214.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [56.8, 23.8, 86.4, 47.7] |
| MFG-0145 | Line balance #133: 10 tasks, takt 132.2 s | Accuracy | P2 | Balance stations. | Σt = 525.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [25.2, 56.7, 30.1, 12.5, 57.1, 86.6, 62.6, 89.0, 63.0, 43.1] |
| MFG-0146 | Line balance #134: 4 tasks, takt 55.3 s | Accuracy | P2 | Balance stations. | Σt = 125 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [27.1, 53.2, 18.9, 25.8] |
| MFG-0147 | Line balance #135: 4 tasks, takt 164.2 s | Accuracy | P2 | Balance stations. | Σt = 302.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [89.6, 87.1, 70.5, 55.1] |
| MFG-0148 | Line balance #136: 6 tasks, takt 96.0 s | Accuracy | P2 | Balance stations. | Σt = 343.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [29.5, 15.4, 82.0, 67.2, 67.6, 82.0] |
| MFG-0149 | Line balance #137: 7 tasks, takt 140.5 s | Accuracy | P2 | Balance stations. | Σt = 330.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [11.3, 73.3, 46.4, 80.1, 27.7, 54.4, 37.7] |
| MFG-0150 | Line balance #138: 11 tasks, takt 103.8 s | Accuracy | P2 | Balance stations. | Σt = 597.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [52.7, 73.0, 36.1, 65.8, 78.1, 41.7, 44.6, 89.6, 46.7, 26.0, 43.5] |
| MFG-0151 | Line balance #139: 6 tasks, takt 75.6 s | Accuracy | P2 | Balance stations. | Σt = 153.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [24.0, 22.6, 26.8, 43.2, 19.7, 17.5] |
| MFG-0152 | Line balance #140: 6 tasks, takt 141.6 s | Accuracy | P2 | Balance stations. | Σt = 356.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [46.7, 24.6, 79.3, 60.7, 70.7, 74.5] |
| MFG-0153 | Line balance #141: 5 tasks, takt 106.2 s | Accuracy | P2 | Balance stations. | Σt = 250.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [77.7, 16.4, 67.7, 32.9, 56.1] |
| MFG-0154 | Line balance #142: 12 tasks, takt 146.7 s | Accuracy | P2 | Balance stations. | Σt = 554.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [25.8, 42.0, 12.2, 43.0, 58.1, 52.0, 73.9, 79.7, 11.4, 75.5, 57.7, 23.1] |
| MFG-0155 | Line balance #143: 5 tasks, takt 105.3 s | Accuracy | P2 | Balance stations. | Σt = 236.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [30.2, 62.2, 26.6, 46.4, 71.3] |
| MFG-0156 | Line balance #144: 9 tasks, takt 129.8 s | Accuracy | P2 | Balance stations. | Σt = 464.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [66.5, 87.8, 78.2, 37.7, 73.3, 12.1, 12.0, 75.2, 21.7] |
| MFG-0157 | Line balance #145: 10 tasks, takt 124.1 s | Accuracy | P2 | Balance stations. | Σt = 399.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [15.9, 50.2, 23.6, 66.0, 47.6, 16.5, 62.8, 32.5, 20.6, 63.4] |
| MFG-0158 | Line balance #146: 12 tasks, takt 140.6 s | Accuracy | P2 | Balance stations. | Σt = 742.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [84.6, 48.0, 61.1, 66.5, 58.7, 59.8, 75.8, 53.8, 79.2, 65.0, 42.7, 47.1] |
| MFG-0159 | Line balance #147: 7 tasks, takt 102.3 s | Accuracy | P2 | Balance stations. | Σt = 275.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [30.8, 20.2, 29.6, 72.9, 77.2, 27.4, 17.4] |
| MFG-0160 | Line balance #148: 6 tasks, takt 115.4 s | Accuracy | P2 | Balance stations. | Σt = 404.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [69.7, 57.1, 84.3, 37.9, 82.6, 73.0] |
| MFG-0161 | Line balance #149: 11 tasks, takt 168.2 s | Accuracy | P2 | Balance stations. | Σt = 627 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [78.0, 68.5, 43.1, 85.7, 40.2, 86.6, 47.8, 44.0, 38.1, 76.7, 18.3] |
| MFG-0162 | Line balance #150: 8 tasks, takt 123.3 s | Accuracy | P2 | Balance stations. | Σt = 486.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [75.8, 73.8, 59.7, 29.7, 60.7, 62.8, 46.0, 78.3] |
| MFG-0163 | Line balance #151: 6 tasks, takt 147.1 s | Accuracy | P2 | Balance stations. | Σt = 333.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [81.0, 77.5, 41.0, 72.7, 49.4, 11.9] |
| MFG-0164 | Line balance #152: 6 tasks, takt 120.5 s | Accuracy | P2 | Balance stations. | Σt = 321.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [80.5, 78.7, 51.2, 43.3, 44.1, 23.3] |
| MFG-0165 | Line balance #153: 12 tasks, takt 89.3 s | Accuracy | P2 | Balance stations. | Σt = 582.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 7; efficiency = Σt/(n·takt) reported. | tasks [10.3, 17.2, 52.4, 24.7, 11.5, 86.6, 73.1, 83.4, 78.6, 64.8, 57.4, 22.5] |
| MFG-0166 | Line balance #154: 11 tasks, takt 111.2 s | Accuracy | P2 | Balance stations. | Σt = 423.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [45.4, 25.9, 66.3, 11.4, 25.7, 15.8, 63.6, 77.9, 27.1, 48.1, 16.0] |
| MFG-0167 | Line balance #155: 5 tasks, takt 127.4 s | Accuracy | P2 | Balance stations. | Σt = 310.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [80.4, 51.9, 64.9, 79.2, 34.3] |
| MFG-0168 | Line balance #156: 5 tasks, takt 113.7 s | Accuracy | P2 | Balance stations. | Σt = 314.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [29.0, 86.1, 63.6, 46.4, 89.2] |
| MFG-0169 | Line balance #157: 7 tasks, takt 106.7 s | Accuracy | P2 | Balance stations. | Σt = 320.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [27.3, 49.0, 44.3, 58.7, 10.1, 58.1, 72.6] |
| MFG-0170 | Line balance #158: 4 tasks, takt 125.3 s | Accuracy | P2 | Balance stations. | Σt = 209.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [79.5, 39.4, 54.6, 36.0] |
| MFG-0171 | Line balance #159: 12 tasks, takt 153.8 s | Accuracy | P2 | Balance stations. | Σt = 659.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [51.0, 86.8, 46.5, 19.1, 29.0, 84.0, 70.7, 52.8, 11.3, 56.3, 80.1, 71.5] |
| MFG-0172 | Line balance #160: 4 tasks, takt 111.9 s | Accuracy | P2 | Balance stations. | Σt = 167.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [13.5, 77.2, 15.9, 60.7] |
| MFG-0173 | Line balance #161: 12 tasks, takt 142.9 s | Accuracy | P2 | Balance stations. | Σt = 561.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [29.5, 16.6, 58.8, 50.8, 58.7, 14.2, 44.1, 69.6, 70.1, 23.1, 73.1, 53.1] |
| MFG-0174 | Line balance #162: 11 tasks, takt 133.0 s | Accuracy | P2 | Balance stations. | Σt = 530.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [78.9, 67.5, 10.3, 16.9, 81.7, 52.4, 20.4, 50.9, 45.9, 69.0, 36.4] |
| MFG-0175 | Line balance #163: 9 tasks, takt 166.2 s | Accuracy | P2 | Balance stations. | Σt = 501.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [64.9, 36.7, 36.5, 16.7, 26.4, 86.5, 84.0, 63.3, 86.2] |
| MFG-0176 | Line balance #164: 9 tasks, takt 123.3 s | Accuracy | P2 | Balance stations. | Σt = 416.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [41.3, 45.0, 12.1, 44.3, 17.2, 53.5, 80.4, 81.4, 41.3] |
| MFG-0177 | Line balance #165: 11 tasks, takt 177.7 s | Accuracy | P2 | Balance stations. | Σt = 530.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [38.7, 28.3, 82.7, 57.0, 12.1, 37.2, 76.9, 12.4, 33.8, 61.7, 89.7] |
| MFG-0178 | Line balance #166: 8 tasks, takt 96.0 s | Accuracy | P2 | Balance stations. | Σt = 469.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [26.2, 56.9, 89.8, 33.4, 74.8, 87.7, 21.2, 79.2] |
| MFG-0179 | Line balance #167: 10 tasks, takt 133.4 s | Accuracy | P2 | Balance stations. | Σt = 470.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [15.3, 13.6, 49.7, 69.1, 56.6, 72.1, 35.9, 61.1, 60.5, 37.0] |
| MFG-0180 | Line balance #168: 12 tasks, takt 118.8 s | Accuracy | P2 | Balance stations. | Σt = 579.2 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [88.8, 67.0, 43.4, 40.4, 57.0, 74.7, 23.1, 17.7, 20.1, 41.3, 24.7, 81.0] |
| MFG-0181 | Line balance #169: 8 tasks, takt 93.8 s | Accuracy | P2 | Balance stations. | Σt = 463.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [63.3, 66.3, 24.4, 70.6, 47.2, 88.5, 53.7, 49.6] |
| MFG-0182 | Line balance #170: 11 tasks, takt 121.5 s | Accuracy | P2 | Balance stations. | Σt = 485.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [76.7, 57.0, 37.7, 14.8, 40.8, 17.3, 28.6, 77.3, 23.8, 61.2, 50.6] |
| MFG-0183 | Line balance #171: 7 tasks, takt 115.6 s | Accuracy | P2 | Balance stations. | Σt = 348.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [56.0, 85.5, 48.7, 48.3, 71.1, 21.8, 17.0] |
| MFG-0184 | Line balance #172: 6 tasks, takt 112.7 s | Accuracy | P2 | Balance stations. | Σt = 348.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [49.8, 18.2, 68.4, 86.7, 57.3, 68.5] |
| MFG-0185 | Line balance #173: 4 tasks, takt 120.3 s | Accuracy | P2 | Balance stations. | Σt = 179.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [30.0, 82.6, 28.1, 39.2] |
| MFG-0186 | Line balance #174: 9 tasks, takt 121.7 s | Accuracy | P2 | Balance stations. | Σt = 424.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [47.1, 34.2, 60.8, 23.2, 44.9, 50.3, 46.6, 56.2, 61.4] |
| MFG-0187 | Line balance #175: 11 tasks, takt 132.7 s | Accuracy | P2 | Balance stations. | Σt = 663.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 6; efficiency = Σt/(n·takt) reported. | tasks [73.5, 19.8, 57.3, 72.4, 44.1, 66.8, 70.8, 48.4, 45.5, 85.4, 79.6] |
| MFG-0188 | Line balance #176: 9 tasks, takt 113.1 s | Accuracy | P2 | Balance stations. | Σt = 473 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [30.3, 57.2, 73.6, 79.4, 21.6, 71.6, 31.8, 84.7, 22.8] |
| MFG-0189 | Line balance #177: 5 tasks, takt 158.9 s | Accuracy | P2 | Balance stations. | Σt = 204.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [19.7, 36.3, 20.0, 43.8, 85.0] |
| MFG-0190 | Line balance #178: 6 tasks, takt 122.6 s | Accuracy | P2 | Balance stations. | Σt = 242.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [73.3, 48.1, 10.6, 11.3, 87.7, 11.3] |
| MFG-0191 | Line balance #179: 6 tasks, takt 116.6 s | Accuracy | P2 | Balance stations. | Σt = 399.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [84.3, 55.0, 56.9, 72.3, 64.4, 66.4] |
| MFG-0192 | Line balance #180: 4 tasks, takt 99.4 s | Accuracy | P2 | Balance stations. | Σt = 232.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [31.1, 68.2, 87.4, 45.7] |
| MFG-0193 | Line balance #181: 6 tasks, takt 100.3 s | Accuracy | P2 | Balance stations. | Σt = 283.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [56.6, 41.6, 41.2, 61.9, 66.4, 15.7] |
| MFG-0194 | Line balance #182: 4 tasks, takt 76.9 s | Accuracy | P2 | Balance stations. | Σt = 157.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [62.4, 46.9, 36.8, 11.6] |
| MFG-0195 | Line balance #183: 10 tasks, takt 130.8 s | Accuracy | P2 | Balance stations. | Σt = 491.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [22.2, 35.4, 51.7, 63.0, 59.4, 88.1, 84.1, 12.0, 63.8, 11.4] |
| MFG-0196 | Line balance #184: 9 tasks, takt 127.1 s | Accuracy | P2 | Balance stations. | Σt = 395.9 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [19.8, 53.6, 15.7, 30.6, 84.3, 88.9, 40.7, 33.3, 29.0] |
| MFG-0197 | Line balance #185: 10 tasks, takt 164.5 s | Accuracy | P2 | Balance stations. | Σt = 488 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [23.1, 38.9, 38.6, 13.1, 16.7, 86.7, 68.4, 69.2, 71.8, 61.5] |
| MFG-0198 | Line balance #186: 7 tasks, takt 178.7 s | Accuracy | P2 | Balance stations. | Σt = 419.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [36.0, 89.7, 87.6, 58.6, 57.1, 52.8, 37.6] |
| MFG-0199 | Line balance #187: 12 tasks, takt 129.9 s | Accuracy | P2 | Balance stations. | Σt = 485.8 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [27.1, 75.3, 37.6, 13.4, 33.5, 69.2, 32.4, 39.4, 54.3, 28.2, 26.7, 48.7] |
| MFG-0200 | Line balance #188: 11 tasks, takt 105.0 s | Accuracy | P2 | Balance stations. | Σt = 404.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [76.1, 15.7, 53.7, 32.7, 20.2, 14.1, 59.0, 24.3, 48.6, 21.7, 38.6] |
| MFG-0201 | Line balance #189: 7 tasks, takt 138.7 s | Accuracy | P2 | Balance stations. | Σt = 309.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [68.5, 17.3, 21.3, 86.0, 22.4, 62.4, 31.7] |
| MFG-0202 | Line balance #190: 6 tasks, takt 124.2 s | Accuracy | P2 | Balance stations. | Σt = 347.1 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [79.2, 55.1, 39.4, 82.6, 14.7, 76.1] |
| MFG-0203 | Line balance #191: 10 tasks, takt 155.0 s | Accuracy | P2 | Balance stations. | Σt = 508.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [48.6, 83.2, 53.8, 49.0, 80.1, 75.9, 42.8, 28.1, 13.9, 32.9] |
| MFG-0204 | Line balance #192: 12 tasks, takt 117.2 s | Accuracy | P2 | Balance stations. | Σt = 533.6 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [34.6, 57.2, 34.9, 53.7, 42.8, 41.0, 70.5, 21.5, 27.7, 48.2, 57.6, 43.9] |
| MFG-0205 | Line balance #193: 9 tasks, takt 175.7 s | Accuracy | P2 | Balance stations. | Σt = 525 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [85.1, 74.5, 56.0, 88.9, 17.7, 67.1, 25.3, 85.1, 25.3] |
| MFG-0206 | Line balance #194: 9 tasks, takt 80.4 s | Accuracy | P2 | Balance stations. | Σt = 317 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [30.1, 34.0, 16.6, 44.3, 62.4, 20.3, 25.4, 30.0, 53.9] |
| MFG-0207 | Line balance #195: 8 tasks, takt 100.2 s | Accuracy | P2 | Balance stations. | Σt = 497.7 s; theoretical minimum stations = ⌈Σt/takt⌉ = 5; efficiency = Σt/(n·takt) reported. | tasks [84.8, 58.4, 78.3, 13.3, 46.4, 88.9, 37.8, 89.8] |
| MFG-0208 | Line balance #196: 11 tasks, takt 139.9 s | Accuracy | P2 | Balance stations. | Σt = 541.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 4; efficiency = Σt/(n·takt) reported. | tasks [22.1, 44.0, 84.7, 77.6, 53.9, 36.6, 49.8, 86.2, 43.0, 25.3, 18.1] |
| MFG-0209 | Line balance #197: 5 tasks, takt 136.8 s | Accuracy | P2 | Balance stations. | Σt = 257.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [26.0, 34.0, 50.8, 84.5, 62.2] |
| MFG-0210 | Line balance #198: 5 tasks, takt 144.8 s | Accuracy | P2 | Balance stations. | Σt = 238.5 s; theoretical minimum stations = ⌈Σt/takt⌉ = 2; efficiency = Σt/(n·takt) reported. | tasks [40.2, 43.1, 44.1, 31.0, 80.1] |
| MFG-0211 | Line balance #199: 7 tasks, takt 139.9 s | Accuracy | P2 | Balance stations. | Σt = 340.3 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [23.7, 65.5, 72.9, 80.3, 53.3, 28.5, 16.1] |
| MFG-0212 | Line balance #200: 5 tasks, takt 130.3 s | Accuracy | P2 | Balance stations. | Σt = 264.4 s; theoretical minimum stations = ⌈Σt/takt⌉ = 3; efficiency = Σt/(n·takt) reported. | tasks [44.5, 59.2, 79.4, 42.6, 38.7] |

## Machining data

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MFG-0213 | Mill Ø6 z=2 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 15915 rpm; vf = fz·z·n = 1591.5 mm/min (fz=0.05). |  |
| MFG-0214 | Mill Ø6 z=4 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 15915 rpm; vf = fz·z·n = 3183.1 mm/min (fz=0.05). |  |
| MFG-0215 | Mill Ø10 z=2 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 9549.3 rpm; vf = fz·z·n = 954.93 mm/min (fz=0.05). |  |
| MFG-0216 | Mill Ø10 z=4 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 9549.3 rpm; vf = fz·z·n = 1909.9 mm/min (fz=0.05). |  |
| MFG-0217 | Mill Ø16 z=2 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 5968.3 rpm; vf = fz·z·n = 1193.7 mm/min (fz=0.1). |  |
| MFG-0218 | Mill Ø16 z=4 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 5968.3 rpm; vf = fz·z·n = 2387.3 mm/min (fz=0.1). |  |
| MFG-0219 | Mill Ø25 z=2 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 3819.7 rpm; vf = fz·z·n = 763.94 mm/min (fz=0.1). |  |
| MFG-0220 | Mill Ø25 z=4 in aluminium (Vc=300) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 3819.7 rpm; vf = fz·z·n = 1527.9 mm/min (fz=0.1). |  |
| MFG-0221 | Mill Ø6 z=2 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 6366.2 rpm; vf = fz·z·n = 636.62 mm/min (fz=0.05). |  |
| MFG-0222 | Mill Ø6 z=4 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 6366.2 rpm; vf = fz·z·n = 1273.2 mm/min (fz=0.05). |  |
| MFG-0223 | Mill Ø10 z=2 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 3819.7 rpm; vf = fz·z·n = 381.97 mm/min (fz=0.05). |  |
| MFG-0224 | Mill Ø10 z=4 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 3819.7 rpm; vf = fz·z·n = 763.94 mm/min (fz=0.05). |  |
| MFG-0225 | Mill Ø16 z=2 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 2387.3 rpm; vf = fz·z·n = 477.46 mm/min (fz=0.1). |  |
| MFG-0226 | Mill Ø16 z=4 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 2387.3 rpm; vf = fz·z·n = 954.93 mm/min (fz=0.1). |  |
| MFG-0227 | Mill Ø25 z=2 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1527.9 rpm; vf = fz·z·n = 305.58 mm/min (fz=0.1). |  |
| MFG-0228 | Mill Ø25 z=4 in steel (Vc=120) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1527.9 rpm; vf = fz·z·n = 611.15 mm/min (fz=0.1). |  |
| MFG-0229 | Mill Ø6 z=2 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 4244.1 rpm; vf = fz·z·n = 424.41 mm/min (fz=0.05). |  |
| MFG-0230 | Mill Ø6 z=4 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 4244.1 rpm; vf = fz·z·n = 848.83 mm/min (fz=0.05). |  |
| MFG-0231 | Mill Ø10 z=2 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 2546.5 rpm; vf = fz·z·n = 254.65 mm/min (fz=0.05). |  |
| MFG-0232 | Mill Ø10 z=4 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 2546.5 rpm; vf = fz·z·n = 509.3 mm/min (fz=0.05). |  |
| MFG-0233 | Mill Ø16 z=2 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1591.5 rpm; vf = fz·z·n = 318.31 mm/min (fz=0.1). |  |
| MFG-0234 | Mill Ø16 z=4 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1591.5 rpm; vf = fz·z·n = 636.62 mm/min (fz=0.1). |  |
| MFG-0235 | Mill Ø25 z=2 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1018.6 rpm; vf = fz·z·n = 203.72 mm/min (fz=0.1). |  |
| MFG-0236 | Mill Ø25 z=4 in stainless (Vc=80) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1018.6 rpm; vf = fz·z·n = 407.44 mm/min (fz=0.1). |  |
| MFG-0237 | Mill Ø6 z=2 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 2652.6 rpm; vf = fz·z·n = 265.26 mm/min (fz=0.05). |  |
| MFG-0238 | Mill Ø6 z=4 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 2652.6 rpm; vf = fz·z·n = 530.52 mm/min (fz=0.05). |  |
| MFG-0239 | Mill Ø10 z=2 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1591.5 rpm; vf = fz·z·n = 159.15 mm/min (fz=0.05). |  |
| MFG-0240 | Mill Ø10 z=4 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 1591.5 rpm; vf = fz·z·n = 318.31 mm/min (fz=0.05). |  |
| MFG-0241 | Mill Ø16 z=2 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 994.72 rpm; vf = fz·z·n = 198.94 mm/min (fz=0.1). |  |
| MFG-0242 | Mill Ø16 z=4 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 994.72 rpm; vf = fz·z·n = 397.89 mm/min (fz=0.1). |  |
| MFG-0243 | Mill Ø25 z=2 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 636.62 rpm; vf = fz·z·n = 127.32 mm/min (fz=0.1). |  |
| MFG-0244 | Mill Ø25 z=4 in titanium (Vc=50) | Accuracy | P2 | Compute speeds/feeds. | n = 1000·Vc/(πD) = 636.62 rpm; vf = fz·z·n = 254.65 mm/min (fz=0.1). |  |

## NC operations

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MFG-0245 | facing: toolpath generation | Functional | P2 | toolpath generation for facing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0246 | facing: gouge check | Functional | P2 | gouge check for facing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0247 | facing: collision with holder | Functional | P2 | collision with holder for facing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0248 | facing: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for facing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0249 | facing: cycle time estimate | Functional | P2 | cycle time estimate for facing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0250 | 2.5D pocket: toolpath generation | Functional | P2 | toolpath generation for 2.5D pocket on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0251 | 2.5D pocket: gouge check | Functional | P2 | gouge check for 2.5D pocket on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0252 | 2.5D pocket: collision with holder | Functional | P2 | collision with holder for 2.5D pocket on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0253 | 2.5D pocket: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for 2.5D pocket on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0254 | 2.5D pocket: cycle time estimate | Functional | P2 | cycle time estimate for 2.5D pocket on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0255 | contour: toolpath generation | Functional | P2 | toolpath generation for contour on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0256 | contour: gouge check | Functional | P2 | gouge check for contour on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0257 | contour: collision with holder | Functional | P2 | collision with holder for contour on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0258 | contour: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for contour on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0259 | contour: cycle time estimate | Functional | P2 | cycle time estimate for contour on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0260 | drilling (peck): toolpath generation | Functional | P2 | toolpath generation for drilling (peck) on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0261 | drilling (peck): gouge check | Functional | P2 | gouge check for drilling (peck) on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0262 | drilling (peck): collision with holder | Functional | P2 | collision with holder for drilling (peck) on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0263 | drilling (peck): G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for drilling (peck) on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0264 | drilling (peck): cycle time estimate | Functional | P2 | cycle time estimate for drilling (peck) on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0265 | tapping: toolpath generation | Functional | P2 | toolpath generation for tapping on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0266 | tapping: gouge check | Functional | P2 | gouge check for tapping on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0267 | tapping: collision with holder | Functional | P2 | collision with holder for tapping on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0268 | tapping: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for tapping on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0269 | tapping: cycle time estimate | Functional | P2 | cycle time estimate for tapping on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0270 | chamfer: toolpath generation | Functional | P2 | toolpath generation for chamfer on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0271 | chamfer: gouge check | Functional | P2 | gouge check for chamfer on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0272 | chamfer: collision with holder | Functional | P2 | collision with holder for chamfer on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0273 | chamfer: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for chamfer on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0274 | chamfer: cycle time estimate | Functional | P2 | cycle time estimate for chamfer on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0275 | 3-axis roughing: toolpath generation | Functional | P2 | toolpath generation for 3-axis roughing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0276 | 3-axis roughing: gouge check | Functional | P2 | gouge check for 3-axis roughing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0277 | 3-axis roughing: collision with holder | Functional | P2 | collision with holder for 3-axis roughing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0278 | 3-axis roughing: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for 3-axis roughing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0279 | 3-axis roughing: cycle time estimate | Functional | P2 | cycle time estimate for 3-axis roughing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0280 | 3-axis finishing: toolpath generation | Functional | P2 | toolpath generation for 3-axis finishing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0281 | 3-axis finishing: gouge check | Functional | P2 | gouge check for 3-axis finishing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0282 | 3-axis finishing: collision with holder | Functional | P2 | collision with holder for 3-axis finishing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0283 | 3-axis finishing: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for 3-axis finishing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0284 | 3-axis finishing: cycle time estimate | Functional | P2 | cycle time estimate for 3-axis finishing on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0285 | rest machining: toolpath generation | Functional | P2 | toolpath generation for rest machining on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0286 | rest machining: gouge check | Functional | P2 | gouge check for rest machining on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0287 | rest machining: collision with holder | Functional | P2 | collision with holder for rest machining on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0288 | rest machining: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for rest machining on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0289 | rest machining: cycle time estimate | Functional | P2 | cycle time estimate for rest machining on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0290 | 5-axis swarf: toolpath generation | Functional | P2 | toolpath generation for 5-axis swarf on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0291 | 5-axis swarf: gouge check | Functional | P2 | gouge check for 5-axis swarf on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0292 | 5-axis swarf: collision with holder | Functional | P2 | collision with holder for 5-axis swarf on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0293 | 5-axis swarf: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for 5-axis swarf on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0294 | 5-axis swarf: cycle time estimate | Functional | P2 | cycle time estimate for 5-axis swarf on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0295 | turning OD: toolpath generation | Functional | P2 | toolpath generation for turning OD on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0296 | turning OD: gouge check | Functional | P2 | gouge check for turning OD on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0297 | turning OD: collision with holder | Functional | P2 | collision with holder for turning OD on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0298 | turning OD: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for turning OD on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0299 | turning OD: cycle time estimate | Functional | P2 | cycle time estimate for turning OD on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0300 | turning bore: toolpath generation | Functional | P2 | toolpath generation for turning bore on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0301 | turning bore: gouge check | Functional | P2 | gouge check for turning bore on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0302 | turning bore: collision with holder | Functional | P2 | collision with holder for turning bore on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0303 | turning bore: G-code post (Fanuc) | Functional | P2 | G-code post (Fanuc) for turning bore on the housing. | Path valid; no gouges; post-processed code simulates. |  |
| MFG-0304 | turning bore: cycle time estimate | Functional | P2 | cycle time estimate for turning bore on the housing. | Path valid; no gouges; post-processed code simulates. |  |

## Process planning, cost and CO2

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MFG-0305 | MBOM by station — car | Functional | P2 | Generate MBOM by station for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0306 | MBOM by station — aircraft | Functional | P2 | Generate MBOM by station for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0307 | MBOM by station — vessel | Functional | P2 | Generate MBOM by station for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0308 | MBOM by station — engine | Functional | P2 | Generate MBOM by station for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0309 | process plan generation — car | Functional | P2 | Generate process plan generation for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0310 | process plan generation — aircraft | Functional | P2 | Generate process plan generation for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0311 | process plan generation — vessel | Functional | P2 | Generate process plan generation for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0312 | process plan generation — engine | Functional | P2 | Generate process plan generation for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0313 | operator count — car | Functional | P2 | Generate operator count for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0314 | operator count — aircraft | Functional | P2 | Generate operator count for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0315 | operator count — vessel | Functional | P2 | Generate operator count for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0316 | operator count — engine | Functional | P2 | Generate operator count for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0317 | unit cost roll-up — car | Functional | P2 | Generate unit cost roll-up for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0318 | unit cost roll-up — aircraft | Functional | P2 | Generate unit cost roll-up for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0319 | unit cost roll-up — vessel | Functional | P2 | Generate unit cost roll-up for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0320 | unit cost roll-up — engine | Functional | P2 | Generate unit cost roll-up for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0321 | CO2 per unit — car | Functional | P2 | Generate CO2 per unit for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0322 | CO2 per unit — aircraft | Functional | P2 | Generate CO2 per unit for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0323 | CO2 per unit — vessel | Functional | P2 | Generate CO2 per unit for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0324 | CO2 per unit — engine | Functional | P2 | Generate CO2 per unit for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0325 | EBOM↔MBOM reconciliation — car | Functional | P2 | Generate EBOM↔MBOM reconciliation for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0326 | EBOM↔MBOM reconciliation — aircraft | Functional | P2 | Generate EBOM↔MBOM reconciliation for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0327 | EBOM↔MBOM reconciliation — vessel | Functional | P2 | Generate EBOM↔MBOM reconciliation for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0328 | EBOM↔MBOM reconciliation — engine | Functional | P2 | Generate EBOM↔MBOM reconciliation for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0329 | make vs buy — car | Functional | P2 | Generate make vs buy for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0330 | make vs buy — aircraft | Functional | P2 | Generate make vs buy for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0331 | make vs buy — vessel | Functional | P2 | Generate make vs buy for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0332 | make vs buy — engine | Functional | P2 | Generate make vs buy for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0333 | capacity check — car | Functional | P2 | Generate capacity check for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0334 | capacity check — aircraft | Functional | P2 | Generate capacity check for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0335 | capacity check — vessel | Functional | P2 | Generate capacity check for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0336 | capacity check — engine | Functional | P2 | Generate capacity check for the engine. | Figures consistent with the BOM and plan. |  |
| MFG-0337 | PFMEA generation — car | Functional | P2 | Generate PFMEA generation for the car. | Figures consistent with the BOM and plan. |  |
| MFG-0338 | PFMEA generation — aircraft | Functional | P2 | Generate PFMEA generation for the aircraft. | Figures consistent with the BOM and plan. |  |
| MFG-0339 | PFMEA generation — vessel | Functional | P2 | Generate PFMEA generation for the vessel. | Figures consistent with the BOM and plan. |  |
| MFG-0340 | PFMEA generation — engine | Functional | P2 | Generate PFMEA generation for the engine. | Figures consistent with the BOM and plan. |  |

## Additive manufacturing

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MFG-0341 | overhang > 45° for FDM | Functional | P2 | Run AM check overhang > 45°. | Regions flagged with values; report exportable. |  |
| MFG-0342 | overhang > 45° for SLA | Functional | P2 | Run AM check overhang > 45°. | Regions flagged with values; report exportable. |  |
| MFG-0343 | overhang > 45° for SLS | Functional | P2 | Run AM check overhang > 45°. | Regions flagged with values; report exportable. |  |
| MFG-0344 | overhang > 45° for metal LPBF | Functional | P2 | Run AM check overhang > 45°. | Regions flagged with values; report exportable. |  |
| MFG-0345 | min wall 0.8 mm for FDM | Functional | P2 | Run AM check min wall 0.8 mm. | Regions flagged with values; report exportable. |  |
| MFG-0346 | min wall 0.8 mm for SLA | Functional | P2 | Run AM check min wall 0.8 mm. | Regions flagged with values; report exportable. |  |
| MFG-0347 | min wall 0.8 mm for SLS | Functional | P2 | Run AM check min wall 0.8 mm. | Regions flagged with values; report exportable. |  |
| MFG-0348 | min wall 0.8 mm for metal LPBF | Functional | P2 | Run AM check min wall 0.8 mm. | Regions flagged with values; report exportable. |  |
| MFG-0349 | trapped powder for FDM | Functional | P2 | Run AM check trapped powder. | Regions flagged with values; report exportable. |  |
| MFG-0350 | trapped powder for SLA | Functional | P2 | Run AM check trapped powder. | Regions flagged with values; report exportable. |  |
| MFG-0351 | trapped powder for SLS | Functional | P2 | Run AM check trapped powder. | Regions flagged with values; report exportable. |  |
| MFG-0352 | trapped powder for metal LPBF | Functional | P2 | Run AM check trapped powder. | Regions flagged with values; report exportable. |  |
| MFG-0353 | support volume for FDM | Functional | P2 | Run AM check support volume. | Regions flagged with values; report exportable. |  |
| MFG-0354 | support volume for SLA | Functional | P2 | Run AM check support volume. | Regions flagged with values; report exportable. |  |
| MFG-0355 | support volume for SLS | Functional | P2 | Run AM check support volume. | Regions flagged with values; report exportable. |  |
| MFG-0356 | support volume for metal LPBF | Functional | P2 | Run AM check support volume. | Regions flagged with values; report exportable. |  |
| MFG-0357 | build orientation for FDM | Functional | P2 | Run AM check build orientation. | Regions flagged with values; report exportable. |  |
| MFG-0358 | build orientation for SLA | Functional | P2 | Run AM check build orientation. | Regions flagged with values; report exportable. |  |
| MFG-0359 | build orientation for SLS | Functional | P2 | Run AM check build orientation. | Regions flagged with values; report exportable. |  |
| MFG-0360 | build orientation for metal LPBF | Functional | P2 | Run AM check build orientation. | Regions flagged with values; report exportable. |  |
| MFG-0361 | slice to 3MF for FDM | Functional | P2 | Run AM check slice to 3MF. | Regions flagged with values; report exportable. |  |
| MFG-0362 | slice to 3MF for SLA | Functional | P2 | Run AM check slice to 3MF. | Regions flagged with values; report exportable. |  |
| MFG-0363 | slice to 3MF for SLS | Functional | P2 | Run AM check slice to 3MF. | Regions flagged with values; report exportable. |  |
| MFG-0364 | slice to 3MF for metal LPBF | Functional | P2 | Run AM check slice to 3MF. | Regions flagged with values; report exportable. |  |
