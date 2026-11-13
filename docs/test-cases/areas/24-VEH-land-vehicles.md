# VEH — Land vehicles

**CATIA-class equivalent:** Automotive extensions (Body-in-White, Styling, Vehicle Dynamics)  
**Autevra workspace:** Design; Styling; Package; Simulation; Loads  
**Scope:** Land  
**Cases:** 296 (Have 251, Partial 5, Gap 40)

Vehicle templates, styled bodies, packaging and vehicle physics.

[← Back to the index](../README.md)

## Features

- Tyre geometry — 138 cases (Have)
- Templates and styled body — 91 cases (Have)
- Packaging rules — 10 cases (Have)
- Longitudinal performance — 12 cases (Have)
- Ride and handling — 29 cases (Partial)
- Body in white — 16 cases (Gap)

## Tyre geometry

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| VEH-0001 | Tyre 175/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 579.7 mm; rolling circumference ≈ 1821.18 mm. |  |
| VEH-0002 | Tyre 175/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 605.1 mm; rolling circumference ≈ 1900.98 mm. |  |
| VEH-0003 | Tyre 175/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 630.5 mm; rolling circumference ≈ 1980.77 mm. |  |
| VEH-0004 | Tyre 175/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 655.9 mm; rolling circumference ≈ 2060.57 mm. |  |
| VEH-0005 | Tyre 175/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 614.7 mm; rolling circumference ≈ 1931.14 mm. |  |
| VEH-0006 | Tyre 175/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 640.1 mm; rolling circumference ≈ 2010.93 mm. |  |
| VEH-0007 | Tyre 175/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 665.5 mm; rolling circumference ≈ 2090.73 mm. |  |
| VEH-0008 | Tyre 175/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 690.9 mm; rolling circumference ≈ 2170.53 mm. |  |
| VEH-0009 | Tyre 175/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 573.5 mm; rolling circumference ≈ 1801.7 mm. |  |
| VEH-0010 | Tyre 175/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 598.9 mm; rolling circumference ≈ 1881.5 mm. |  |
| VEH-0011 | Tyre 175/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 624.3 mm; rolling circumference ≈ 1961.3 mm. |  |
| VEH-0012 | Tyre 175/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 608.5 mm; rolling circumference ≈ 1911.66 mm. |  |
| VEH-0013 | Tyre 175/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 633.9 mm; rolling circumference ≈ 1991.46 mm. |  |
| VEH-0014 | Tyre 175/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 659.3 mm; rolling circumference ≈ 2071.25 mm. |  |
| VEH-0015 | Tyre 175/70 R14 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 600.6 mm; rolling circumference ≈ 1886.84 mm. |  |
| VEH-0016 | Tyre 185/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 621.5 mm; rolling circumference ≈ 1952.5 mm. |  |
| VEH-0017 | Tyre 195/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 593.7 mm; rolling circumference ≈ 1865.16 mm. |  |
| VEH-0018 | Tyre 195/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 619.1 mm; rolling circumference ≈ 1944.96 mm. |  |
| VEH-0019 | Tyre 195/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 644.5 mm; rolling circumference ≈ 2024.76 mm. |  |
| VEH-0020 | Tyre 195/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 669.9 mm; rolling circumference ≈ 2104.55 mm. |  |
| VEH-0021 | Tyre 195/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 632.7 mm; rolling circumference ≈ 1987.69 mm. |  |
| VEH-0022 | Tyre 195/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 658.1 mm; rolling circumference ≈ 2067.48 mm. |  |
| VEH-0023 | Tyre 195/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 683.5 mm; rolling circumference ≈ 2147.28 mm. |  |
| VEH-0024 | Tyre 195/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 708.9 mm; rolling circumference ≈ 2227.08 mm. |  |
| VEH-0025 | Tyre 195/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 595.5 mm; rolling circumference ≈ 1870.82 mm. |  |
| VEH-0026 | Tyre 195/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 620.9 mm; rolling circumference ≈ 1950.61 mm. |  |
| VEH-0027 | Tyre 195/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 646.3 mm; rolling circumference ≈ 2030.41 mm. |  |
| VEH-0028 | Tyre 195/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 634.5 mm; rolling circumference ≈ 1993.34 mm. |  |
| VEH-0029 | Tyre 195/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 659.9 mm; rolling circumference ≈ 2073.14 mm. |  |
| VEH-0030 | Tyre 195/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 685.3 mm; rolling circumference ≈ 2152.93 mm. |  |
| VEH-0031 | Tyre 205/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 631.9 mm; rolling circumference ≈ 1985.17 mm. |  |
| VEH-0032 | Tyre 215/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 607.7 mm; rolling circumference ≈ 1909.15 mm. |  |
| VEH-0033 | Tyre 215/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 633.1 mm; rolling circumference ≈ 1988.94 mm. |  |
| VEH-0034 | Tyre 215/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 658.5 mm; rolling circumference ≈ 2068.74 mm. |  |
| VEH-0035 | Tyre 215/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 683.9 mm; rolling circumference ≈ 2148.54 mm. |  |
| VEH-0036 | Tyre 215/45 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 625.3 mm; rolling circumference ≈ 1964.44 mm. |  |
| VEH-0037 | Tyre 215/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 650.7 mm; rolling circumference ≈ 2044.23 mm. |  |
| VEH-0038 | Tyre 215/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 676.1 mm; rolling circumference ≈ 2124.03 mm. |  |
| VEH-0039 | Tyre 215/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 701.5 mm; rolling circumference ≈ 2203.83 mm. |  |
| VEH-0040 | Tyre 215/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 726.9 mm; rolling circumference ≈ 2283.62 mm. |  |
| VEH-0041 | Tyre 215/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 617.5 mm; rolling circumference ≈ 1939.93 mm. |  |
| VEH-0042 | Tyre 215/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 642.9 mm; rolling circumference ≈ 2019.73 mm. |  |
| VEH-0043 | Tyre 215/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 668.3 mm; rolling circumference ≈ 2099.53 mm. |  |
| VEH-0044 | Tyre 215/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 660.5 mm; rolling circumference ≈ 2075.02 mm. |  |
| VEH-0045 | Tyre 215/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 685.9 mm; rolling circumference ≈ 2154.82 mm. |  |
| VEH-0046 | Tyre 215/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 711.3 mm; rolling circumference ≈ 2234.61 mm. |  |
| VEH-0047 | Tyre 225/40 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 637.2 mm; rolling circumference ≈ 2001.82 mm. |  |
| VEH-0048 | Tyre 235/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 621.7 mm; rolling circumference ≈ 1953.13 mm. |  |
| VEH-0049 | Tyre 235/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 647.1 mm; rolling circumference ≈ 2032.92 mm. |  |
| VEH-0050 | Tyre 235/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 672.5 mm; rolling circumference ≈ 2112.72 mm. |  |
| VEH-0051 | Tyre 235/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 697.9 mm; rolling circumference ≈ 2192.52 mm. |  |
| VEH-0052 | Tyre 235/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 668.7 mm; rolling circumference ≈ 2100.78 mm. |  |
| VEH-0053 | Tyre 235/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 694.1 mm; rolling circumference ≈ 2180.58 mm. |  |
| VEH-0054 | Tyre 235/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 719.5 mm; rolling circumference ≈ 2260.38 mm. |  |
| VEH-0055 | Tyre 235/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 744.9 mm; rolling circumference ≈ 2340.17 mm. |  |
| VEH-0056 | Tyre 235/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 639.5 mm; rolling circumference ≈ 2009.05 mm. |  |
| VEH-0057 | Tyre 235/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 664.9 mm; rolling circumference ≈ 2088.84 mm. |  |
| VEH-0058 | Tyre 235/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 690.3 mm; rolling circumference ≈ 2168.64 mm. |  |
| VEH-0059 | Tyre 235/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 686.5 mm; rolling circumference ≈ 2156.7 mm. |  |
| VEH-0060 | Tyre 235/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 711.9 mm; rolling circumference ≈ 2236.5 mm. |  |
| VEH-0061 | Tyre 235/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 737.3 mm; rolling circumference ≈ 2316.3 mm. |  |
| VEH-0062 | Tyre 245/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 677.7 mm; rolling circumference ≈ 2129.06 mm. |  |
| VEH-0063 | Tyre 255/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 635.7 mm; rolling circumference ≈ 1997.11 mm. |  |
| VEH-0064 | Tyre 255/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 661.1 mm; rolling circumference ≈ 2076.91 mm. |  |
| VEH-0065 | Tyre 255/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 686.5 mm; rolling circumference ≈ 2156.7 mm. |  |
| VEH-0066 | Tyre 255/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 711.9 mm; rolling circumference ≈ 2236.5 mm. |  |
| VEH-0067 | Tyre 255/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 686.7 mm; rolling circumference ≈ 2157.33 mm. |  |
| VEH-0068 | Tyre 255/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 712.1 mm; rolling circumference ≈ 2237.13 mm. |  |
| VEH-0069 | Tyre 255/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 737.5 mm; rolling circumference ≈ 2316.92 mm. |  |
| VEH-0070 | Tyre 255/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 762.9 mm; rolling circumference ≈ 2396.72 mm. |  |
| VEH-0071 | Tyre 255/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 661.5 mm; rolling circumference ≈ 2078.16 mm. |  |
| VEH-0072 | Tyre 255/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 686.9 mm; rolling circumference ≈ 2157.96 mm. |  |
| VEH-0073 | Tyre 255/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 712.3 mm; rolling circumference ≈ 2237.76 mm. |  |
| VEH-0074 | Tyre 255/55 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 737.7 mm; rolling circumference ≈ 2317.55 mm. |  |
| VEH-0075 | Tyre 255/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 712.5 mm; rolling circumference ≈ 2238.38 mm. |  |
| VEH-0076 | Tyre 255/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 737.9 mm; rolling circumference ≈ 2318.18 mm. |  |
| VEH-0077 | Tyre 255/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 763.3 mm; rolling circumference ≈ 2397.98 mm. |  |
| VEH-0078 | Tyre 265/70 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 802.8 mm; rolling circumference ≈ 2522.07 mm. |  |
| VEH-0079 | Tyre 275/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 649.7 mm; rolling circumference ≈ 2041.09 mm. |  |
| VEH-0080 | Tyre 275/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 675.1 mm; rolling circumference ≈ 2120.89 mm. |  |
| VEH-0081 | Tyre 275/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 700.5 mm; rolling circumference ≈ 2200.69 mm. |  |
| VEH-0082 | Tyre 275/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 725.9 mm; rolling circumference ≈ 2280.48 mm. |  |
| VEH-0083 | Tyre 275/40 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 728 mm; rolling circumference ≈ 2287.08 mm. |  |
| VEH-0084 | Tyre 275/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 704.7 mm; rolling circumference ≈ 2213.88 mm. |  |
| VEH-0085 | Tyre 275/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 730.1 mm; rolling circumference ≈ 2293.68 mm. |  |
| VEH-0086 | Tyre 275/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 755.5 mm; rolling circumference ≈ 2373.47 mm. |  |
| VEH-0087 | Tyre 275/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 780.9 mm; rolling circumference ≈ 2453.27 mm. |  |
| VEH-0088 | Tyre 275/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 683.5 mm; rolling circumference ≈ 2147.28 mm. |  |
| VEH-0089 | Tyre 275/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 708.9 mm; rolling circumference ≈ 2227.08 mm. |  |
| VEH-0090 | Tyre 275/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 734.3 mm; rolling circumference ≈ 2306.87 mm. |  |
| VEH-0091 | Tyre 275/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 738.5 mm; rolling circumference ≈ 2320.07 mm. |  |
| VEH-0092 | Tyre 275/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 763.9 mm; rolling circumference ≈ 2399.86 mm. |  |
| VEH-0093 | Tyre 275/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 789.3 mm; rolling circumference ≈ 2479.66 mm. |  |
| VEH-0094 | Tyre 285/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 732.9 mm; rolling circumference ≈ 2302.47 mm. |  |
| VEH-0095 | Tyre 295/30 R22 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 735.8 mm; rolling circumference ≈ 2311.58 mm. |  |
| VEH-0096 | Tyre 295/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 663.7 mm; rolling circumference ≈ 2085.08 mm. |  |
| VEH-0097 | Tyre 295/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 689.1 mm; rolling circumference ≈ 2164.87 mm. |  |
| VEH-0098 | Tyre 295/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 714.5 mm; rolling circumference ≈ 2244.67 mm. |  |
| VEH-0099 | Tyre 295/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 739.9 mm; rolling circumference ≈ 2324.46 mm. |  |
| VEH-0100 | Tyre 295/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 722.7 mm; rolling circumference ≈ 2270.43 mm. |  |
| VEH-0101 | Tyre 295/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 748.1 mm; rolling circumference ≈ 2350.23 mm. |  |
| VEH-0102 | Tyre 295/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 773.5 mm; rolling circumference ≈ 2430.02 mm. |  |
| VEH-0103 | Tyre 295/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 798.9 mm; rolling circumference ≈ 2509.82 mm. |  |
| VEH-0104 | Tyre 295/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 705.5 mm; rolling circumference ≈ 2216.39 mm. |  |
| VEH-0105 | Tyre 295/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 730.9 mm; rolling circumference ≈ 2296.19 mm. |  |
| VEH-0106 | Tyre 295/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 756.3 mm; rolling circumference ≈ 2375.99 mm. |  |
| VEH-0107 | Tyre 295/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 764.5 mm; rolling circumference ≈ 2401.75 mm. |  |
| VEH-0108 | Tyre 295/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 789.9 mm; rolling circumference ≈ 2481.54 mm. |  |
| VEH-0109 | Tyre 295/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 815.3 mm; rolling circumference ≈ 2561.34 mm. |  |
| VEH-0110 | Tyre 315/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 677.7 mm; rolling circumference ≈ 2129.06 mm. |  |
| VEH-0111 | Tyre 315/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 703.1 mm; rolling circumference ≈ 2208.85 mm. |  |
| VEH-0112 | Tyre 315/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 728.5 mm; rolling circumference ≈ 2288.65 mm. |  |
| VEH-0113 | Tyre 315/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 753.9 mm; rolling circumference ≈ 2368.45 mm. |  |
| VEH-0114 | Tyre 315/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 740.7 mm; rolling circumference ≈ 2326.98 mm. |  |
| VEH-0115 | Tyre 315/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 766.1 mm; rolling circumference ≈ 2406.77 mm. |  |
| VEH-0116 | Tyre 315/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 791.5 mm; rolling circumference ≈ 2486.57 mm. |  |
| VEH-0117 | Tyre 315/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 816.9 mm; rolling circumference ≈ 2566.37 mm. |  |
| VEH-0118 | Tyre 315/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 727.5 mm; rolling circumference ≈ 2285.51 mm. |  |
| VEH-0119 | Tyre 315/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 752.9 mm; rolling circumference ≈ 2365.31 mm. |  |
| VEH-0120 | Tyre 315/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 778.3 mm; rolling circumference ≈ 2445.1 mm. |  |
| VEH-0121 | Tyre 315/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 790.5 mm; rolling circumference ≈ 2483.43 mm. |  |
| VEH-0122 | Tyre 315/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 815.9 mm; rolling circumference ≈ 2563.23 mm. |  |
| VEH-0123 | Tyre 315/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 841.3 mm; rolling circumference ≈ 2643.02 mm. |  |
| VEH-0124 | Tyre 315/70 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 872.8 mm; rolling circumference ≈ 2741.98 mm. |  |
| VEH-0125 | Tyre 335/35 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 691.7 mm; rolling circumference ≈ 2173.04 mm. |  |
| VEH-0126 | Tyre 335/35 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 717.1 mm; rolling circumference ≈ 2252.84 mm. |  |
| VEH-0127 | Tyre 335/35 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 742.5 mm; rolling circumference ≈ 2332.63 mm. |  |
| VEH-0128 | Tyre 335/35 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 767.9 mm; rolling circumference ≈ 2412.43 mm. |  |
| VEH-0129 | Tyre 335/45 R18 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 758.7 mm; rolling circumference ≈ 2383.53 mm. |  |
| VEH-0130 | Tyre 335/45 R19 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 784.1 mm; rolling circumference ≈ 2463.32 mm. |  |
| VEH-0131 | Tyre 335/45 R20 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 809.5 mm; rolling circumference ≈ 2543.12 mm. |  |
| VEH-0132 | Tyre 335/45 R21 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 834.9 mm; rolling circumference ≈ 2622.92 mm. |  |
| VEH-0133 | Tyre 335/55 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 749.5 mm; rolling circumference ≈ 2354.62 mm. |  |
| VEH-0134 | Tyre 335/55 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 774.9 mm; rolling circumference ≈ 2434.42 mm. |  |
| VEH-0135 | Tyre 335/55 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 800.3 mm; rolling circumference ≈ 2514.22 mm. |  |
| VEH-0136 | Tyre 335/65 R15 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 816.5 mm; rolling circumference ≈ 2565.11 mm. |  |
| VEH-0137 | Tyre 335/65 R16 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 841.9 mm; rolling circumference ≈ 2644.91 mm. |  |
| VEH-0138 | Tyre 335/65 R17 | Accuracy | P1 | Set the tyre size; read derived diameter. | Diameter = rim·25.4 + 2·w·AR/100 = 867.3 mm; rolling circumference ≈ 2724.7 mm. |  |

## Templates and styled body

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| VEH-0139 | hatchback: builds as one valid solid | Regression | P1 | Create a hatchback project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0140 | hatchback: seats fit under roofline | Regression | P2 | Create a hatchback project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0141 | hatchback: wheels inside arches at full bump | Regression | P2 | Create a hatchback project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0142 | hatchback: frame/harness/grille fit the skin | Regression | P2 | Create a hatchback project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0143 | hatchback: glTF export | Regression | P2 | Create a hatchback project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0144 | hatchback: STEP export | Regression | P2 | Create a hatchback project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0145 | hatchback: rebuild < 10 s | Regression | P2 | Create a hatchback project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0146 | sedan: builds as one valid solid | Regression | P1 | Create a sedan project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0147 | sedan: seats fit under roofline | Regression | P2 | Create a sedan project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0148 | sedan: wheels inside arches at full bump | Regression | P2 | Create a sedan project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0149 | sedan: frame/harness/grille fit the skin | Regression | P2 | Create a sedan project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0150 | sedan: glTF export | Regression | P2 | Create a sedan project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0151 | sedan: STEP export | Regression | P2 | Create a sedan project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0152 | sedan: rebuild < 10 s | Regression | P2 | Create a sedan project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0153 | estate: builds as one valid solid | Regression | P1 | Create a estate project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0154 | estate: seats fit under roofline | Regression | P2 | Create a estate project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0155 | estate: wheels inside arches at full bump | Regression | P2 | Create a estate project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0156 | estate: frame/harness/grille fit the skin | Regression | P2 | Create a estate project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0157 | estate: glTF export | Regression | P2 | Create a estate project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0158 | estate: STEP export | Regression | P2 | Create a estate project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0159 | estate: rebuild < 10 s | Regression | P2 | Create a estate project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0160 | coupe: builds as one valid solid | Regression | P1 | Create a coupe project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0161 | coupe: seats fit under roofline | Regression | P2 | Create a coupe project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0162 | coupe: wheels inside arches at full bump | Regression | P2 | Create a coupe project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0163 | coupe: frame/harness/grille fit the skin | Regression | P2 | Create a coupe project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0164 | coupe: glTF export | Regression | P2 | Create a coupe project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0165 | coupe: STEP export | Regression | P2 | Create a coupe project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0166 | coupe: rebuild < 10 s | Regression | P2 | Create a coupe project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0167 | convertible: builds as one valid solid | Regression | P1 | Create a convertible project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0168 | convertible: seats fit under roofline | Regression | P2 | Create a convertible project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0169 | convertible: wheels inside arches at full bump | Regression | P2 | Create a convertible project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0170 | convertible: frame/harness/grille fit the skin | Regression | P2 | Create a convertible project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0171 | convertible: glTF export | Regression | P2 | Create a convertible project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0172 | convertible: STEP export | Regression | P2 | Create a convertible project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0173 | convertible: rebuild < 10 s | Regression | P2 | Create a convertible project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0174 | grand tourer: builds as one valid solid | Regression | P1 | Create a grand tourer project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0175 | grand tourer: seats fit under roofline | Regression | P2 | Create a grand tourer project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0176 | grand tourer: wheels inside arches at full bump | Regression | P2 | Create a grand tourer project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0177 | grand tourer: frame/harness/grille fit the skin | Regression | P2 | Create a grand tourer project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0178 | grand tourer: glTF export | Regression | P2 | Create a grand tourer project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0179 | grand tourer: STEP export | Regression | P2 | Create a grand tourer project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0180 | grand tourer: rebuild < 10 s | Regression | P2 | Create a grand tourer project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0181 | SUV: builds as one valid solid | Regression | P1 | Create a SUV project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0182 | SUV: seats fit under roofline | Regression | P2 | Create a SUV project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0183 | SUV: wheels inside arches at full bump | Regression | P2 | Create a SUV project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0184 | SUV: frame/harness/grille fit the skin | Regression | P2 | Create a SUV project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0185 | SUV: glTF export | Regression | P2 | Create a SUV project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0186 | SUV: STEP export | Regression | P2 | Create a SUV project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0187 | SUV: rebuild < 10 s | Regression | P2 | Create a SUV project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0188 | crossover: builds as one valid solid | Regression | P1 | Create a crossover project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0189 | crossover: seats fit under roofline | Regression | P2 | Create a crossover project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0190 | crossover: wheels inside arches at full bump | Regression | P2 | Create a crossover project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0191 | crossover: frame/harness/grille fit the skin | Regression | P2 | Create a crossover project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0192 | crossover: glTF export | Regression | P2 | Create a crossover project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0193 | crossover: STEP export | Regression | P2 | Create a crossover project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0194 | crossover: rebuild < 10 s | Regression | P2 | Create a crossover project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0195 | pickup: builds as one valid solid | Regression | P1 | Create a pickup project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0196 | pickup: seats fit under roofline | Regression | P2 | Create a pickup project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0197 | pickup: wheels inside arches at full bump | Regression | P2 | Create a pickup project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0198 | pickup: frame/harness/grille fit the skin | Regression | P2 | Create a pickup project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0199 | pickup: glTF export | Regression | P2 | Create a pickup project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0200 | pickup: STEP export | Regression | P2 | Create a pickup project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0201 | pickup: rebuild < 10 s | Regression | P2 | Create a pickup project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0202 | van: builds as one valid solid | Regression | P1 | Create a van project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0203 | van: seats fit under roofline | Regression | P2 | Create a van project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0204 | van: wheels inside arches at full bump | Regression | P2 | Create a van project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0205 | van: frame/harness/grille fit the skin | Regression | P2 | Create a van project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0206 | van: glTF export | Regression | P2 | Create a van project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0207 | van: STEP export | Regression | P2 | Create a van project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0208 | van: rebuild < 10 s | Regression | P2 | Create a van project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0209 | minibus: builds as one valid solid | Regression | P1 | Create a minibus project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0210 | minibus: seats fit under roofline | Regression | P2 | Create a minibus project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0211 | minibus: wheels inside arches at full bump | Regression | P2 | Create a minibus project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0212 | minibus: frame/harness/grille fit the skin | Regression | P2 | Create a minibus project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0213 | minibus: glTF export | Regression | P2 | Create a minibus project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0214 | minibus: STEP export | Regression | P2 | Create a minibus project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0215 | minibus: rebuild < 10 s | Regression | P2 | Create a minibus project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0216 | light truck: builds as one valid solid | Regression | P1 | Create a light truck project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0217 | light truck: seats fit under roofline | Regression | P2 | Create a light truck project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0218 | light truck: wheels inside arches at full bump | Regression | P2 | Create a light truck project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0219 | light truck: frame/harness/grille fit the skin | Regression | P2 | Create a light truck project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0220 | light truck: glTF export | Regression | P2 | Create a light truck project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0221 | light truck: STEP export | Regression | P2 | Create a light truck project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0222 | light truck: rebuild < 10 s | Regression | P2 | Create a light truck project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |
| VEH-0223 | roadster: builds as one valid solid | Regression | P1 | Create a roadster project; check that it builds as one valid solid. | Pass; no OCCT boolean failures logged. |  |
| VEH-0224 | roadster: seats fit under roofline | Regression | P2 | Create a roadster project; check that it seats fit under roofline. | Pass; no OCCT boolean failures logged. |  |
| VEH-0225 | roadster: wheels inside arches at full bump | Regression | P2 | Create a roadster project; check that it wheels inside arches at full bump. | Pass; no OCCT boolean failures logged. |  |
| VEH-0226 | roadster: frame/harness/grille fit the skin | Regression | P2 | Create a roadster project; check that it frame/harness/grille fit the skin. | Pass; no OCCT boolean failures logged. |  |
| VEH-0227 | roadster: glTF export | Regression | P2 | Create a roadster project; check that it glTF export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0228 | roadster: STEP export | Regression | P2 | Create a roadster project; check that it STEP export. | Pass; no OCCT boolean failures logged. |  |
| VEH-0229 | roadster: rebuild < 10 s | Regression | P2 | Create a roadster project; check that it rebuild < 10 s. | Pass; no OCCT boolean failures logged. |  |

## Packaging rules

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| VEH-0230 | Overall length fo=800, wb=2500, ro=600 | Accuracy | P2 | Set overhangs and wheelbase. | Overall length = 3900 mm. |  |
| VEH-0231 | Overall length fo=900, wb=2700, ro=800 | Accuracy | P2 | Set overhangs and wheelbase. | Overall length = 4400 mm. |  |
| VEH-0232 | Overall length fo=1000, wb=3000, ro=1100 | Accuracy | P2 | Set overhangs and wheelbase. | Overall length = 5100 mm. |  |
| VEH-0233 | Overall length fo=750, wb=2400, ro=500 | Accuracy | P2 | Set overhangs and wheelbase. | Overall length = 3650 mm. |  |
| VEH-0234 | Overall length fo=1100, wb=3600, ro=1300 | Accuracy | P2 | Set overhangs and wheelbase. | Overall length = 6000 mm. |  |
| VEH-0235 | Static stability factor T=1500, hCG=550 | Accuracy | P2 | Read the rollover check. | SSF = T/2h = 1.364. |  |
| VEH-0236 | Static stability factor T=1600, hCG=600 | Accuracy | P2 | Read the rollover check. | SSF = T/2h = 1.333. |  |
| VEH-0237 | Static stability factor T=1550, hCG=750 | Accuracy | P2 | Read the rollover check. | SSF = T/2h = 1.033; flagged (< 1.2). |  |
| VEH-0238 | Static stability factor T=1700, hCG=900 | Accuracy | P2 | Read the rollover check. | SSF = T/2h = 0.9444; flagged (< 1.2). |  |
| VEH-0239 | Static stability factor T=1450, hCG=500 | Accuracy | P2 | Read the rollover check. | SSF = T/2h = 1.45. |  |

## Longitudinal performance

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| VEH-0240 | Traction-limited 0–100: μ=0.8, driven-axle share 0.5 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 7.081 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0241 | Traction-limited 0–100: μ=0.8, driven-axle share 0.6 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 5.901 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0242 | Traction-limited 0–100: μ=0.8, driven-axle share 1.0 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 3.541 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0243 | Traction-limited 0–100: μ=0.9, driven-axle share 0.5 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 6.295 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0244 | Traction-limited 0–100: μ=0.9, driven-axle share 0.6 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 5.245 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0245 | Traction-limited 0–100: μ=0.9, driven-axle share 1.0 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 3.147 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0246 | Traction-limited 0–100: μ=1.0, driven-axle share 0.5 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 5.665 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0247 | Traction-limited 0–100: μ=1.0, driven-axle share 0.6 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 4.721 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0248 | Traction-limited 0–100: μ=1.0, driven-axle share 1.0 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 2.833 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0249 | Traction-limited 0–100: μ=1.1, driven-axle share 0.5 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 5.15 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0250 | Traction-limited 0–100: μ=1.1, driven-axle share 0.6 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 4.292 s (no load transfer); targets below are flagged as conflicts. |  |
| VEH-0251 | Traction-limited 0–100: μ=1.1, driven-axle share 1.0 | Accuracy | P2 | Spec interview acceleration bound. | t ≥ v/(μ·g·share) = 2.575 s (no load transfer); targets below are flagged as conflicts. |  |

## Ride and handling

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| VEH-0252 | Quarter-car k=20000 N/m, sprung 300 kg | Accuracy | P2 | Run the quarter-car test. | Body natural frequency ≈ √(k/m)/2π = 1.299 Hz (tyre-compliance ignored). |  |
| VEH-0253 | Quarter-car k=25000 N/m, sprung 350 kg | Accuracy | P2 | Run the quarter-car test. | Body natural frequency ≈ √(k/m)/2π = 1.345 Hz (tyre-compliance ignored). |  |
| VEH-0254 | Quarter-car k=30000 N/m, sprung 400 kg | Accuracy | P2 | Run the quarter-car test. | Body natural frequency ≈ √(k/m)/2π = 1.378 Hz (tyre-compliance ignored). |  |
| VEH-0255 | Quarter-car k=40000 N/m, sprung 500 kg | Accuracy | P2 | Run the quarter-car test. | Body natural frequency ≈ √(k/m)/2π = 1.424 Hz (tyre-compliance ignored). |  |
| VEH-0256 | Quarter-car k=60000 N/m, sprung 700 kg | Accuracy | P2 | Run the quarter-car test. | Body natural frequency ≈ √(k/m)/2π = 1.473 Hz (tyre-compliance ignored). |  |
| VEH-0257 | steady-state cornering (understeer gradient) — hatchback | Functional | P2 | Run steady-state cornering (understeer gradient). | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0258 | steady-state cornering (understeer gradient) — SUV | Functional | P2 | Run steady-state cornering (understeer gradient). | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0259 | steady-state cornering (understeer gradient) — pickup | Functional | P2 | Run steady-state cornering (understeer gradient). | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0260 | step steer — hatchback | Functional | P2 | Run step steer. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0261 | step steer — SUV | Functional | P2 | Run step steer. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0262 | step steer — pickup | Functional | P2 | Run step steer. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0263 | sine-with-dwell — hatchback | Functional | P2 | Run sine-with-dwell. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0264 | sine-with-dwell — SUV | Functional | P2 | Run sine-with-dwell. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0265 | sine-with-dwell — pickup | Functional | P2 | Run sine-with-dwell. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0266 | ISO lane change — hatchback | Functional | P2 | Run ISO lane change. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0267 | ISO lane change — SUV | Functional | P2 | Run ISO lane change. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0268 | ISO lane change — pickup | Functional | P2 | Run ISO lane change. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0269 | roll gradient — hatchback | Functional | P2 | Run roll gradient. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0270 | roll gradient — SUV | Functional | P2 | Run roll gradient. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0271 | roll gradient — pickup | Functional | P2 | Run roll gradient. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0272 | brake-in-turn — hatchback | Functional | P2 | Run brake-in-turn. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0273 | brake-in-turn — SUV | Functional | P2 | Run brake-in-turn. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0274 | brake-in-turn — pickup | Functional | P2 | Run brake-in-turn. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0275 | kinematics & compliance (bump steer) — hatchback | Functional | P2 | Run kinematics & compliance (bump steer). | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0276 | kinematics & compliance (bump steer) — SUV | Functional | P2 | Run kinematics & compliance (bump steer). | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0277 | kinematics & compliance (bump steer) — pickup | Functional | P2 | Run kinematics & compliance (bump steer). | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0278 | full multibody 14-DOF — hatchback | Functional | P2 | Run full multibody 14-DOF. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0279 | full multibody 14-DOF — SUV | Functional | P2 | Run full multibody 14-DOF. | Response metrics with credibility label; compared with the previous revision. |  |
| VEH-0280 | full multibody 14-DOF — pickup | Functional | P2 | Run full multibody 14-DOF. | Response metrics with credibility label; compared with the previous revision. |  |

## Body in white

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| VEH-0281 | BIW spot weld points — sedan | Functional | P2 | Run spot weld points. | Results per panel/joint; exportable. |  |
| VEH-0282 | BIW spot weld points — SUV | Functional | P2 | Run spot weld points. | Results per panel/joint; exportable. |  |
| VEH-0283 | BIW weld flange check — sedan | Functional | P2 | Run weld flange check. | Results per panel/joint; exportable. |  |
| VEH-0284 | BIW weld flange check — SUV | Functional | P2 | Run weld flange check. | Results per panel/joint; exportable. |  |
| VEH-0285 | BIW panel thickness map — sedan | Functional | P2 | Run panel thickness map. | Results per panel/joint; exportable. |  |
| VEH-0286 | BIW panel thickness map — SUV | Functional | P2 | Run panel thickness map. | Results per panel/joint; exportable. |  |
| VEH-0287 | BIW BIW torsional stiffness — sedan | Functional | P2 | Run BIW torsional stiffness. | Results per panel/joint; exportable. |  |
| VEH-0288 | BIW BIW torsional stiffness — SUV | Functional | P2 | Run BIW torsional stiffness. | Results per panel/joint; exportable. |  |
| VEH-0289 | BIW crash load path check — sedan | Functional | P2 | Run crash load path check. | Results per panel/joint; exportable. |  |
| VEH-0290 | BIW crash load path check — SUV | Functional | P2 | Run crash load path check. | Results per panel/joint; exportable. |  |
| VEH-0291 | BIW joint stiffness — sedan | Functional | P2 | Run joint stiffness. | Results per panel/joint; exportable. |  |
| VEH-0292 | BIW joint stiffness — SUV | Functional | P2 | Run joint stiffness. | Results per panel/joint; exportable. |  |
| VEH-0293 | BIW sealer lines — sedan | Functional | P2 | Run sealer lines. | Results per panel/joint; exportable. |  |
| VEH-0294 | BIW sealer lines — SUV | Functional | P2 | Run sealer lines. | Results per panel/joint; exportable. |  |
| VEH-0295 | BIW hemming flange — sedan | Functional | P2 | Run hemming flange. | Results per panel/joint; exportable. |  |
| VEH-0296 | BIW hemming flange — SUV | Functional | P2 | Run hemming flange. | Results per panel/joint; exportable. |  |
