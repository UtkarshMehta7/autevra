# ELM — Springs, gears and sections

**CATIA-class equivalent:** Machine Design / structural section libraries  
**Autevra workspace:** Inventory; Structures  
**Scope:** Shared  
**Cases:** 336 (Have 128, Partial 96, Gap 112)

Helical springs, spur gear geometry and section properties from the hollow-section catalogue.

[← Back to the index](../README.md)

## Features

- Helical compression springs — 96 cases (Partial)
- Spur gear geometry — 112 cases (Gap)
- Section properties — 128 cases (Have)

## Helical compression springs

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ELM-0001 | Spring d=0.5, D=10, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.15488 N/mm; index 20. | EN 13906-1 |
| ELM-0002 | Spring d=0.5, D=10, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.10326 N/mm; index 20. | EN 13906-1 |
| ELM-0003 | Spring d=0.5, D=10, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.061953 N/mm; index 20. | EN 13906-1 |
| ELM-0004 | Spring d=0.5, D=10, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.041302 N/mm; index 20. | EN 13906-1 |
| ELM-0005 | Spring d=0.5, D=20, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0006 | Spring d=0.5, D=20, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0007 | Spring d=0.5, D=20, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0008 | Spring d=0.5, D=20, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0009 | Spring d=0.5, D=40, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0010 | Spring d=0.5, D=40, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0011 | Spring d=0.5, D=40, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0012 | Spring d=0.5, D=40, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0013 | Spring d=0.5, D=80, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 160 outside 4–20 (EN 13906). |  |
| ELM-0014 | Spring d=0.5, D=80, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 160 outside 4–20 (EN 13906). |  |
| ELM-0015 | Spring d=0.5, D=80, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 160 outside 4–20 (EN 13906). |  |
| ELM-0016 | Spring d=0.5, D=80, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 160 outside 4–20 (EN 13906). |  |
| ELM-0017 | Spring d=1, D=10, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 2.4781 N/mm; index 10. | EN 13906-1 |
| ELM-0018 | Spring d=1, D=10, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 1.6521 N/mm; index 10. | EN 13906-1 |
| ELM-0019 | Spring d=1, D=10, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.99125 N/mm; index 10. | EN 13906-1 |
| ELM-0020 | Spring d=1, D=10, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.66083 N/mm; index 10. | EN 13906-1 |
| ELM-0021 | Spring d=1, D=20, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.30977 N/mm; index 20. | EN 13906-1 |
| ELM-0022 | Spring d=1, D=20, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.20651 N/mm; index 20. | EN 13906-1 |
| ELM-0023 | Spring d=1, D=20, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.12391 N/mm; index 20. | EN 13906-1 |
| ELM-0024 | Spring d=1, D=20, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.082604 N/mm; index 20. | EN 13906-1 |
| ELM-0025 | Spring d=1, D=40, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0026 | Spring d=1, D=40, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0027 | Spring d=1, D=40, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0028 | Spring d=1, D=40, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0029 | Spring d=1, D=80, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0030 | Spring d=1, D=80, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0031 | Spring d=1, D=80, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0032 | Spring d=1, D=80, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 80 outside 4–20 (EN 13906). |  |
| ELM-0033 | Spring d=2, D=10, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 39.65 N/mm; index 5. | EN 13906-1 |
| ELM-0034 | Spring d=2, D=10, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 26.433 N/mm; index 5. | EN 13906-1 |
| ELM-0035 | Spring d=2, D=10, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 15.86 N/mm; index 5. | EN 13906-1 |
| ELM-0036 | Spring d=2, D=10, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 10.573 N/mm; index 5. | EN 13906-1 |
| ELM-0037 | Spring d=2, D=20, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 4.9562 N/mm; index 10. | EN 13906-1 |
| ELM-0038 | Spring d=2, D=20, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 3.3042 N/mm; index 10. | EN 13906-1 |
| ELM-0039 | Spring d=2, D=20, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 1.9825 N/mm; index 10. | EN 13906-1 |
| ELM-0040 | Spring d=2, D=20, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 1.3217 N/mm; index 10. | EN 13906-1 |
| ELM-0041 | Spring d=2, D=40, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.61953 N/mm; index 20. | EN 13906-1 |
| ELM-0042 | Spring d=2, D=40, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.41302 N/mm; index 20. | EN 13906-1 |
| ELM-0043 | Spring d=2, D=40, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.24781 N/mm; index 20. | EN 13906-1 |
| ELM-0044 | Spring d=2, D=40, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.16521 N/mm; index 20. | EN 13906-1 |
| ELM-0045 | Spring d=2, D=80, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0046 | Spring d=2, D=80, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0047 | Spring d=2, D=80, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0048 | Spring d=2, D=80, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 40 outside 4–20 (EN 13906). |  |
| ELM-0049 | Spring d=3, D=10, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 3.33 outside 4–20 (EN 13906). |  |
| ELM-0050 | Spring d=3, D=10, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 3.33 outside 4–20 (EN 13906). |  |
| ELM-0051 | Spring d=3, D=10, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 3.33 outside 4–20 (EN 13906). |  |
| ELM-0052 | Spring d=3, D=10, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 3.33 outside 4–20 (EN 13906). |  |
| ELM-0053 | Spring d=3, D=20, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 25.091 N/mm; index 6.67. | EN 13906-1 |
| ELM-0054 | Spring d=3, D=20, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 16.727 N/mm; index 6.67. | EN 13906-1 |
| ELM-0055 | Spring d=3, D=20, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 10.036 N/mm; index 6.67. | EN 13906-1 |
| ELM-0056 | Spring d=3, D=20, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 6.6909 N/mm; index 6.67. | EN 13906-1 |
| ELM-0057 | Spring d=3, D=40, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 3.1364 N/mm; index 13.3. | EN 13906-1 |
| ELM-0058 | Spring d=3, D=40, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 2.0909 N/mm; index 13.3. | EN 13906-1 |
| ELM-0059 | Spring d=3, D=40, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 1.2546 N/mm; index 13.3. | EN 13906-1 |
| ELM-0060 | Spring d=3, D=40, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.83637 N/mm; index 13.3. | EN 13906-1 |
| ELM-0061 | Spring d=3, D=80, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 26.7 outside 4–20 (EN 13906). |  |
| ELM-0062 | Spring d=3, D=80, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 26.7 outside 4–20 (EN 13906). |  |
| ELM-0063 | Spring d=3, D=80, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 26.7 outside 4–20 (EN 13906). |  |
| ELM-0064 | Spring d=3, D=80, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 26.7 outside 4–20 (EN 13906). |  |
| ELM-0065 | Spring d=4, D=10, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0066 | Spring d=4, D=10, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0067 | Spring d=4, D=10, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0068 | Spring d=4, D=10, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0069 | Spring d=4, D=20, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 79.3 N/mm; index 5. | EN 13906-1 |
| ELM-0070 | Spring d=4, D=20, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 52.867 N/mm; index 5. | EN 13906-1 |
| ELM-0071 | Spring d=4, D=20, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 31.72 N/mm; index 5. | EN 13906-1 |
| ELM-0072 | Spring d=4, D=20, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 21.147 N/mm; index 5. | EN 13906-1 |
| ELM-0073 | Spring d=4, D=40, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 9.9125 N/mm; index 10. | EN 13906-1 |
| ELM-0074 | Spring d=4, D=40, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 6.6083 N/mm; index 10. | EN 13906-1 |
| ELM-0075 | Spring d=4, D=40, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 3.965 N/mm; index 10. | EN 13906-1 |
| ELM-0076 | Spring d=4, D=40, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 2.6433 N/mm; index 10. | EN 13906-1 |
| ELM-0077 | Spring d=4, D=80, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 1.2391 N/mm; index 20. | EN 13906-1 |
| ELM-0078 | Spring d=4, D=80, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.82604 N/mm; index 20. | EN 13906-1 |
| ELM-0079 | Spring d=4, D=80, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.49562 N/mm; index 20. | EN 13906-1 |
| ELM-0080 | Spring d=4, D=80, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 0.33042 N/mm; index 20. | EN 13906-1 |
| ELM-0081 | Spring d=8, D=10, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 1.25 outside 4–20 (EN 13906). |  |
| ELM-0082 | Spring d=8, D=10, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 1.25 outside 4–20 (EN 13906). |  |
| ELM-0083 | Spring d=8, D=10, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 1.25 outside 4–20 (EN 13906). |  |
| ELM-0084 | Spring d=8, D=10, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 1.25 outside 4–20 (EN 13906). |  |
| ELM-0085 | Spring d=8, D=20, n=4 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0086 | Spring d=8, D=20, n=6 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0087 | Spring d=8, D=20, n=10 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0088 | Spring d=8, D=20, n=15 | Boundary | P2 | Design the spring. | Rejected/warned: spring index D/d = 2.5 outside 4–20 (EN 13906). |  |
| ELM-0089 | Spring d=8, D=40, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 158.6 N/mm; index 5. | EN 13906-1 |
| ELM-0090 | Spring d=8, D=40, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 105.73 N/mm; index 5. | EN 13906-1 |
| ELM-0091 | Spring d=8, D=40, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 63.44 N/mm; index 5. | EN 13906-1 |
| ELM-0092 | Spring d=8, D=40, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 42.293 N/mm; index 5. | EN 13906-1 |
| ELM-0093 | Spring d=8, D=80, n=4 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 19.825 N/mm; index 10. | EN 13906-1 |
| ELM-0094 | Spring d=8, D=80, n=6 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 13.217 N/mm; index 10. | EN 13906-1 |
| ELM-0095 | Spring d=8, D=80, n=10 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 7.93 N/mm; index 10. | EN 13906-1 |
| ELM-0096 | Spring d=8, D=80, n=15 | Accuracy | P2 | Design the spring (G = 79.3 GPa). | k = Gd⁴/(8D³n) = 5.2867 N/mm; index 10. | EN 13906-1 |

## Spur gear geometry

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ELM-0097 | Gear pair m=1, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 12, d2 = 20 mm; centre distance 16 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0098 | Gear pair m=1, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 12, d2 = 40 mm; centre distance 26 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0099 | Gear pair m=1, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 12, d2 = 60 mm; centre distance 36 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0100 | Gear pair m=1, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 12, d2 = 100 mm; centre distance 56 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0101 | Gear pair m=1, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 17, d2 = 20 mm; centre distance 18.5 mm; ratio 1.176. | ISO 21771 |
| ELM-0102 | Gear pair m=1, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 17, d2 = 40 mm; centre distance 28.5 mm; ratio 2.353. | ISO 21771 |
| ELM-0103 | Gear pair m=1, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 17, d2 = 60 mm; centre distance 38.5 mm; ratio 3.529. | ISO 21771 |
| ELM-0104 | Gear pair m=1, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 17, d2 = 100 mm; centre distance 58.5 mm; ratio 5.882. | ISO 21771 |
| ELM-0105 | Gear pair m=1, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 20, d2 = 20 mm; centre distance 20 mm; ratio 1. | ISO 21771 |
| ELM-0106 | Gear pair m=1, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 20, d2 = 40 mm; centre distance 30 mm; ratio 2. | ISO 21771 |
| ELM-0107 | Gear pair m=1, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 20, d2 = 60 mm; centre distance 40 mm; ratio 3. | ISO 21771 |
| ELM-0108 | Gear pair m=1, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 20, d2 = 100 mm; centre distance 60 mm; ratio 5. | ISO 21771 |
| ELM-0109 | Gear pair m=1, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 20 mm; centre distance 25 mm; ratio 0.6667. | ISO 21771 |
| ELM-0110 | Gear pair m=1, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 40 mm; centre distance 35 mm; ratio 1.333. | ISO 21771 |
| ELM-0111 | Gear pair m=1, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 60 mm; centre distance 45 mm; ratio 2. | ISO 21771 |
| ELM-0112 | Gear pair m=1, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 100 mm; centre distance 65 mm; ratio 3.333. | ISO 21771 |
| ELM-0113 | Gear pair m=1.5, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 18, d2 = 30 mm; centre distance 24 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0114 | Gear pair m=1.5, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 18, d2 = 60 mm; centre distance 39 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0115 | Gear pair m=1.5, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 18, d2 = 90 mm; centre distance 54 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0116 | Gear pair m=1.5, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 18, d2 = 150 mm; centre distance 84 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0117 | Gear pair m=1.5, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 25.5, d2 = 30 mm; centre distance 27.75 mm; ratio 1.176. | ISO 21771 |
| ELM-0118 | Gear pair m=1.5, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 25.5, d2 = 60 mm; centre distance 42.75 mm; ratio 2.353. | ISO 21771 |
| ELM-0119 | Gear pair m=1.5, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 25.5, d2 = 90 mm; centre distance 57.75 mm; ratio 3.529. | ISO 21771 |
| ELM-0120 | Gear pair m=1.5, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 25.5, d2 = 150 mm; centre distance 87.75 mm; ratio 5.882. | ISO 21771 |
| ELM-0121 | Gear pair m=1.5, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 30 mm; centre distance 30 mm; ratio 1. | ISO 21771 |
| ELM-0122 | Gear pair m=1.5, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 60 mm; centre distance 45 mm; ratio 2. | ISO 21771 |
| ELM-0123 | Gear pair m=1.5, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 90 mm; centre distance 60 mm; ratio 3. | ISO 21771 |
| ELM-0124 | Gear pair m=1.5, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 30, d2 = 150 mm; centre distance 90 mm; ratio 5. | ISO 21771 |
| ELM-0125 | Gear pair m=1.5, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 45, d2 = 30 mm; centre distance 37.5 mm; ratio 0.6667. | ISO 21771 |
| ELM-0126 | Gear pair m=1.5, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 45, d2 = 60 mm; centre distance 52.5 mm; ratio 1.333. | ISO 21771 |
| ELM-0127 | Gear pair m=1.5, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 45, d2 = 90 mm; centre distance 67.5 mm; ratio 2. | ISO 21771 |
| ELM-0128 | Gear pair m=1.5, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 45, d2 = 150 mm; centre distance 97.5 mm; ratio 3.333. | ISO 21771 |
| ELM-0129 | Gear pair m=2, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 24, d2 = 40 mm; centre distance 32 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0130 | Gear pair m=2, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 24, d2 = 80 mm; centre distance 52 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0131 | Gear pair m=2, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 24, d2 = 120 mm; centre distance 72 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0132 | Gear pair m=2, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 24, d2 = 200 mm; centre distance 112 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0133 | Gear pair m=2, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 34, d2 = 40 mm; centre distance 37 mm; ratio 1.176. | ISO 21771 |
| ELM-0134 | Gear pair m=2, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 34, d2 = 80 mm; centre distance 57 mm; ratio 2.353. | ISO 21771 |
| ELM-0135 | Gear pair m=2, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 34, d2 = 120 mm; centre distance 77 mm; ratio 3.529. | ISO 21771 |
| ELM-0136 | Gear pair m=2, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 34, d2 = 200 mm; centre distance 117 mm; ratio 5.882. | ISO 21771 |
| ELM-0137 | Gear pair m=2, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 40, d2 = 40 mm; centre distance 40 mm; ratio 1. | ISO 21771 |
| ELM-0138 | Gear pair m=2, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 40, d2 = 80 mm; centre distance 60 mm; ratio 2. | ISO 21771 |
| ELM-0139 | Gear pair m=2, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 40, d2 = 120 mm; centre distance 80 mm; ratio 3. | ISO 21771 |
| ELM-0140 | Gear pair m=2, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 40, d2 = 200 mm; centre distance 120 mm; ratio 5. | ISO 21771 |
| ELM-0141 | Gear pair m=2, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 40 mm; centre distance 50 mm; ratio 0.6667. | ISO 21771 |
| ELM-0142 | Gear pair m=2, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 80 mm; centre distance 70 mm; ratio 1.333. | ISO 21771 |
| ELM-0143 | Gear pair m=2, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 120 mm; centre distance 90 mm; ratio 2. | ISO 21771 |
| ELM-0144 | Gear pair m=2, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 200 mm; centre distance 130 mm; ratio 3.333. | ISO 21771 |
| ELM-0145 | Gear pair m=3, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 36, d2 = 60 mm; centre distance 48 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0146 | Gear pair m=3, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 36, d2 = 120 mm; centre distance 78 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0147 | Gear pair m=3, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 36, d2 = 180 mm; centre distance 108 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0148 | Gear pair m=3, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 36, d2 = 300 mm; centre distance 168 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0149 | Gear pair m=3, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 51, d2 = 60 mm; centre distance 55.5 mm; ratio 1.176. | ISO 21771 |
| ELM-0150 | Gear pair m=3, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 51, d2 = 120 mm; centre distance 85.5 mm; ratio 2.353. | ISO 21771 |
| ELM-0151 | Gear pair m=3, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 51, d2 = 180 mm; centre distance 115.5 mm; ratio 3.529. | ISO 21771 |
| ELM-0152 | Gear pair m=3, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 51, d2 = 300 mm; centre distance 175.5 mm; ratio 5.882. | ISO 21771 |
| ELM-0153 | Gear pair m=3, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 60 mm; centre distance 60 mm; ratio 1. | ISO 21771 |
| ELM-0154 | Gear pair m=3, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 120 mm; centre distance 90 mm; ratio 2. | ISO 21771 |
| ELM-0155 | Gear pair m=3, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 180 mm; centre distance 120 mm; ratio 3. | ISO 21771 |
| ELM-0156 | Gear pair m=3, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 300 mm; centre distance 180 mm; ratio 5. | ISO 21771 |
| ELM-0157 | Gear pair m=3, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 90, d2 = 60 mm; centre distance 75 mm; ratio 0.6667. | ISO 21771 |
| ELM-0158 | Gear pair m=3, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 90, d2 = 120 mm; centre distance 105 mm; ratio 1.333. | ISO 21771 |
| ELM-0159 | Gear pair m=3, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 90, d2 = 180 mm; centre distance 135 mm; ratio 2. | ISO 21771 |
| ELM-0160 | Gear pair m=3, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 90, d2 = 300 mm; centre distance 195 mm; ratio 3.333. | ISO 21771 |
| ELM-0161 | Gear pair m=4, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 48, d2 = 80 mm; centre distance 64 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0162 | Gear pair m=4, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 48, d2 = 160 mm; centre distance 104 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0163 | Gear pair m=4, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 48, d2 = 240 mm; centre distance 144 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0164 | Gear pair m=4, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 48, d2 = 400 mm; centre distance 224 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0165 | Gear pair m=4, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 68, d2 = 80 mm; centre distance 74 mm; ratio 1.176. | ISO 21771 |
| ELM-0166 | Gear pair m=4, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 68, d2 = 160 mm; centre distance 114 mm; ratio 2.353. | ISO 21771 |
| ELM-0167 | Gear pair m=4, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 68, d2 = 240 mm; centre distance 154 mm; ratio 3.529. | ISO 21771 |
| ELM-0168 | Gear pair m=4, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 68, d2 = 400 mm; centre distance 234 mm; ratio 5.882. | ISO 21771 |
| ELM-0169 | Gear pair m=4, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 80, d2 = 80 mm; centre distance 80 mm; ratio 1. | ISO 21771 |
| ELM-0170 | Gear pair m=4, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 80, d2 = 160 mm; centre distance 120 mm; ratio 2. | ISO 21771 |
| ELM-0171 | Gear pair m=4, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 80, d2 = 240 mm; centre distance 160 mm; ratio 3. | ISO 21771 |
| ELM-0172 | Gear pair m=4, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 80, d2 = 400 mm; centre distance 240 mm; ratio 5. | ISO 21771 |
| ELM-0173 | Gear pair m=4, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 120, d2 = 80 mm; centre distance 100 mm; ratio 0.6667. | ISO 21771 |
| ELM-0174 | Gear pair m=4, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 120, d2 = 160 mm; centre distance 140 mm; ratio 1.333. | ISO 21771 |
| ELM-0175 | Gear pair m=4, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 120, d2 = 240 mm; centre distance 180 mm; ratio 2. | ISO 21771 |
| ELM-0176 | Gear pair m=4, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 120, d2 = 400 mm; centre distance 260 mm; ratio 3.333. | ISO 21771 |
| ELM-0177 | Gear pair m=5, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 100 mm; centre distance 80 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0178 | Gear pair m=5, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 200 mm; centre distance 130 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0179 | Gear pair m=5, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 300 mm; centre distance 180 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0180 | Gear pair m=5, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 60, d2 = 500 mm; centre distance 280 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0181 | Gear pair m=5, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 85, d2 = 100 mm; centre distance 92.5 mm; ratio 1.176. | ISO 21771 |
| ELM-0182 | Gear pair m=5, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 85, d2 = 200 mm; centre distance 142.5 mm; ratio 2.353. | ISO 21771 |
| ELM-0183 | Gear pair m=5, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 85, d2 = 300 mm; centre distance 192.5 mm; ratio 3.529. | ISO 21771 |
| ELM-0184 | Gear pair m=5, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 85, d2 = 500 mm; centre distance 292.5 mm; ratio 5.882. | ISO 21771 |
| ELM-0185 | Gear pair m=5, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 100, d2 = 100 mm; centre distance 100 mm; ratio 1. | ISO 21771 |
| ELM-0186 | Gear pair m=5, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 100, d2 = 200 mm; centre distance 150 mm; ratio 2. | ISO 21771 |
| ELM-0187 | Gear pair m=5, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 100, d2 = 300 mm; centre distance 200 mm; ratio 3. | ISO 21771 |
| ELM-0188 | Gear pair m=5, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 100, d2 = 500 mm; centre distance 300 mm; ratio 5. | ISO 21771 |
| ELM-0189 | Gear pair m=5, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 150, d2 = 100 mm; centre distance 125 mm; ratio 0.6667. | ISO 21771 |
| ELM-0190 | Gear pair m=5, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 150, d2 = 200 mm; centre distance 175 mm; ratio 1.333. | ISO 21771 |
| ELM-0191 | Gear pair m=5, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 150, d2 = 300 mm; centre distance 225 mm; ratio 2. | ISO 21771 |
| ELM-0192 | Gear pair m=5, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 150, d2 = 500 mm; centre distance 325 mm; ratio 3.333. | ISO 21771 |
| ELM-0193 | Gear pair m=8, z1=12, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 96, d2 = 160 mm; centre distance 128 mm; ratio 1.667; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0194 | Gear pair m=8, z1=12, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 96, d2 = 320 mm; centre distance 208 mm; ratio 3.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0195 | Gear pair m=8, z1=12, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 96, d2 = 480 mm; centre distance 288 mm; ratio 5; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0196 | Gear pair m=8, z1=12, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 96, d2 = 800 mm; centre distance 448 mm; ratio 8.333; undercut warning (z < 17, needs profile shift). | ISO 21771 |
| ELM-0197 | Gear pair m=8, z1=17, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 136, d2 = 160 mm; centre distance 148 mm; ratio 1.176. | ISO 21771 |
| ELM-0198 | Gear pair m=8, z1=17, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 136, d2 = 320 mm; centre distance 228 mm; ratio 2.353. | ISO 21771 |
| ELM-0199 | Gear pair m=8, z1=17, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 136, d2 = 480 mm; centre distance 308 mm; ratio 3.529. | ISO 21771 |
| ELM-0200 | Gear pair m=8, z1=17, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 136, d2 = 800 mm; centre distance 468 mm; ratio 5.882. | ISO 21771 |
| ELM-0201 | Gear pair m=8, z1=20, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 160, d2 = 160 mm; centre distance 160 mm; ratio 1. | ISO 21771 |
| ELM-0202 | Gear pair m=8, z1=20, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 160, d2 = 320 mm; centre distance 240 mm; ratio 2. | ISO 21771 |
| ELM-0203 | Gear pair m=8, z1=20, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 160, d2 = 480 mm; centre distance 320 mm; ratio 3. | ISO 21771 |
| ELM-0204 | Gear pair m=8, z1=20, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 160, d2 = 800 mm; centre distance 480 mm; ratio 5. | ISO 21771 |
| ELM-0205 | Gear pair m=8, z1=30, z2=20 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 240, d2 = 160 mm; centre distance 200 mm; ratio 0.6667. | ISO 21771 |
| ELM-0206 | Gear pair m=8, z1=30, z2=40 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 240, d2 = 320 mm; centre distance 280 mm; ratio 1.333. | ISO 21771 |
| ELM-0207 | Gear pair m=8, z1=30, z2=60 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 240, d2 = 480 mm; centre distance 360 mm; ratio 2. | ISO 21771 |
| ELM-0208 | Gear pair m=8, z1=30, z2=100 | Accuracy | P2 | Create the gear pair (α = 20°, no shift). | d1 = 240, d2 = 800 mm; centre distance 520 mm; ratio 3.333. | ISO 21771 |

## Section properties

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ELM-0209 | RHS 40×40×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 304 mm²; Ixx = (BH³ − bh³)/12 = 73365 mm⁴; Zxx = 3668.3 mm³. |  |
| ELM-0210 | RHS 40×40×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 444 mm²; Ixx = (BH³ − bh³)/12 = 101972 mm⁴; Zxx = 5098.6 mm³. |  |
| ELM-0211 | RHS 40×40×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 700 mm²; Ixx = (BH³ − bh³)/12 = 145833 mm⁴; Zxx = 7291.7 mm³. |  |
| ELM-0212 | RHS 40×40×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1024 mm²; Ixx = (BH³ − bh³)/12 = 185685 mm⁴; Zxx = 9284.3 mm³. |  |
| ELM-0213 | RHS 40×60×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 384 mm²; Ixx = (BH³ − bh³)/12 = 193152 mm⁴; Zxx = 6438.4 mm³. |  |
| ELM-0214 | RHS 40×60×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 564 mm²; Ixx = (BH³ − bh³)/12 = 273852 mm⁴; Zxx = 9128.4 mm³. |  |
| ELM-0215 | RHS 40×60×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 900 mm²; Ixx = (BH³ − bh³)/12 = 407500 mm⁴; Zxx = 13583 mm³. |  |
| ELM-0216 | RHS 40×60×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1344 mm²; Ixx = (BH³ − bh³)/12 = 549632 mm⁴; Zxx = 18321 mm³. |  |
| ELM-0217 | RHS 40×100×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 544 mm²; Ixx = (BH³ − bh³)/12 = 679125 mm⁴; Zxx = 13583 mm³. |  |
| ELM-0218 | RHS 40×100×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 804 mm²; Ixx = (BH³ − bh³)/12 = 980012 mm⁴; Zxx = 19600 mm³. |  |
| ELM-0219 | RHS 40×100×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1300 mm²; Ixx = (BH³ − bh³)/12 = 1510833 mm⁴; Zxx = 30217 mm³. |  |
| ELM-0220 | RHS 40×100×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1984 mm²; Ixx = (BH³ − bh³)/12 = 2147925 mm⁴; Zxx = 42959 mm³. |  |
| ELM-0221 | RHS 40×150×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 744 mm²; Ixx = (BH³ − bh³)/12 = 1913592 mm⁴; Zxx = 25515 mm³. |  |
| ELM-0222 | RHS 40×150×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1104 mm²; Ixx = (BH³ − bh³)/12 = 2789712 mm⁴; Zxx = 37196 mm³. |  |
| ELM-0223 | RHS 40×150×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1800 mm²; Ixx = (BH³ − bh³)/12 = 4390000 mm⁴; Zxx = 58533 mm³. |  |
| ELM-0224 | RHS 40×150×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2784 mm²; Ixx = (BH³ − bh³)/12 = 6437792 mm⁴; Zxx = 85837 mm³. |  |
| ELM-0225 | RHS 40×200×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 944 mm²; Ixx = (BH³ − bh³)/12 = 4078059 mm⁴; Zxx = 40781 mm³. |  |
| ELM-0226 | RHS 40×200×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1404 mm²; Ixx = (BH³ − bh³)/12 = 5979412 mm⁴; Zxx = 59794 mm³. |  |
| ELM-0227 | RHS 40×200×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2300 mm²; Ixx = (BH³ − bh³)/12 = 9519167 mm⁴; Zxx = 95192 mm³. |  |
| ELM-0228 | RHS 40×200×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3584 mm²; Ixx = (BH³ − bh³)/12 = 14207659 mm⁴; Zxx = 142077 mm³. |  |
| ELM-0229 | RHS 60×40×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 384 mm²; Ixx = (BH³ − bh³)/12 = 102272 mm⁴; Zxx = 5113.6 mm³. |  |
| ELM-0230 | RHS 60×40×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 564 mm²; Ixx = (BH³ − bh³)/12 = 143132 mm⁴; Zxx = 7156.6 mm³. |  |
| ELM-0231 | RHS 60×40×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 900 mm²; Ixx = (BH³ − bh³)/12 = 207500 mm⁴; Zxx = 10375 mm³. |  |
| ELM-0232 | RHS 60×40×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1344 mm²; Ixx = (BH³ − bh³)/12 = 269312 mm⁴; Zxx = 13466 mm³. |  |
| ELM-0233 | RHS 60×60×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 464 mm²; Ixx = (BH³ − bh³)/12 = 260459 mm⁴; Zxx = 8682 mm³. |  |
| ELM-0234 | RHS 60×60×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 684 mm²; Ixx = (BH³ − bh³)/12 = 371412 mm⁴; Zxx = 12380 mm³. |  |
| ELM-0235 | RHS 60×60×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1100 mm²; Ixx = (BH³ − bh³)/12 = 559167 mm⁴; Zxx = 18639 mm³. |  |
| ELM-0236 | RHS 60×60×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1664 mm²; Ixx = (BH³ − bh³)/12 = 767659 mm⁴; Zxx = 25589 mm³. |  |
| ELM-0237 | RHS 60×100×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 624 mm²; Ixx = (BH³ − bh³)/12 = 871232 mm⁴; Zxx = 17425 mm³. |  |
| ELM-0238 | RHS 60×100×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 924 mm²; Ixx = (BH³ − bh³)/12 = 1262372 mm⁴; Zxx = 25247 mm³. |  |
| ELM-0239 | RHS 60×100×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1500 mm²; Ixx = (BH³ − bh³)/12 = 1962500 mm⁴; Zxx = 39250 mm³. |  |
| ELM-0240 | RHS 60×100×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2304 mm²; Ixx = (BH³ − bh³)/12 = 2826752 mm⁴; Zxx = 56535 mm³. |  |
| ELM-0241 | RHS 60×150×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 824 mm²; Ixx = (BH³ − bh³)/12 = 2351699 mm⁴; Zxx = 31356 mm³. |  |
| ELM-0242 | RHS 60×150×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1224 mm²; Ixx = (BH³ − bh³)/12 = 3438072 mm⁴; Zxx = 45841 mm³. |  |
| ELM-0243 | RHS 60×150×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2000 mm²; Ixx = (BH³ − bh³)/12 = 5441667 mm⁴; Zxx = 72556 mm³. |  |
| ELM-0244 | RHS 60×150×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3104 mm²; Ixx = (BH³ − bh³)/12 = 8052619 mm⁴; Zxx = 107368 mm³. |  |
| ELM-0245 | RHS 60×200×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1024 mm²; Ixx = (BH³ − bh³)/12 = 4862165 mm⁴; Zxx = 48622 mm³. |  |
| ELM-0246 | RHS 60×200×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1524 mm²; Ixx = (BH³ − bh³)/12 = 7143772 mm⁴; Zxx = 71438 mm³. |  |
| ELM-0247 | RHS 60×200×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2500 mm²; Ixx = (BH³ − bh³)/12 = 11420833 mm⁴; Zxx = 114208 mm³. |  |
| ELM-0248 | RHS 60×200×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3904 mm²; Ixx = (BH³ − bh³)/12 = 17158485 mm⁴; Zxx = 171585 mm³. |  |
| ELM-0249 | RHS 80×40×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 464 mm²; Ixx = (BH³ − bh³)/12 = 131179 mm⁴; Zxx = 6558.9 mm³. |  |
| ELM-0250 | RHS 80×40×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 684 mm²; Ixx = (BH³ − bh³)/12 = 184292 mm⁴; Zxx = 9214.6 mm³. |  |
| ELM-0251 | RHS 80×40×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1100 mm²; Ixx = (BH³ − bh³)/12 = 269167 mm⁴; Zxx = 13458 mm³. |  |
| ELM-0252 | RHS 80×40×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1664 mm²; Ixx = (BH³ − bh³)/12 = 352939 mm⁴; Zxx = 17647 mm³. |  |
| ELM-0253 | RHS 80×60×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 544 mm²; Ixx = (BH³ − bh³)/12 = 327765 mm⁴; Zxx = 10926 mm³. |  |
| ELM-0254 | RHS 80×60×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 804 mm²; Ixx = (BH³ − bh³)/12 = 468972 mm⁴; Zxx = 15632 mm³. |  |
| ELM-0255 | RHS 80×60×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1300 mm²; Ixx = (BH³ − bh³)/12 = 710833 mm⁴; Zxx = 23694 mm³. |  |
| ELM-0256 | RHS 80×60×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1984 mm²; Ixx = (BH³ − bh³)/12 = 985685 mm⁴; Zxx = 32856 mm³. |  |
| ELM-0257 | RHS 80×100×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 704 mm²; Ixx = (BH³ − bh³)/12 = 1063339 mm⁴; Zxx = 21267 mm³. |  |
| ELM-0258 | RHS 80×100×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1044 mm²; Ixx = (BH³ − bh³)/12 = 1544732 mm⁴; Zxx = 30895 mm³. |  |
| ELM-0259 | RHS 80×100×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1700 mm²; Ixx = (BH³ − bh³)/12 = 2414167 mm⁴; Zxx = 48283 mm³. |  |
| ELM-0260 | RHS 80×100×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2624 mm²; Ixx = (BH³ − bh³)/12 = 3505579 mm⁴; Zxx = 70112 mm³. |  |
| ELM-0261 | RHS 80×150×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 904 mm²; Ixx = (BH³ − bh³)/12 = 2789805 mm⁴; Zxx = 37197 mm³. |  |
| ELM-0262 | RHS 80×150×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1344 mm²; Ixx = (BH³ − bh³)/12 = 4086432 mm⁴; Zxx = 54486 mm³. |  |
| ELM-0263 | RHS 80×150×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2200 mm²; Ixx = (BH³ − bh³)/12 = 6493333 mm⁴; Zxx = 86578 mm³. |  |
| ELM-0264 | RHS 80×150×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3424 mm²; Ixx = (BH³ − bh³)/12 = 9667445 mm⁴; Zxx = 128899 mm³. |  |
| ELM-0265 | RHS 80×200×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1104 mm²; Ixx = (BH³ − bh³)/12 = 5646272 mm⁴; Zxx = 56463 mm³. |  |
| ELM-0266 | RHS 80×200×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1644 mm²; Ixx = (BH³ − bh³)/12 = 8308132 mm⁴; Zxx = 83081 mm³. |  |
| ELM-0267 | RHS 80×200×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2700 mm²; Ixx = (BH³ − bh³)/12 = 13322500 mm⁴; Zxx = 133225 mm³. |  |
| ELM-0268 | RHS 80×200×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 4224 mm²; Ixx = (BH³ − bh³)/12 = 20109312 mm⁴; Zxx = 201093 mm³. |  |
| ELM-0269 | RHS 100×40×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 544 mm²; Ixx = (BH³ − bh³)/12 = 160085 mm⁴; Zxx = 8004.3 mm³. |  |
| ELM-0270 | RHS 100×40×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 804 mm²; Ixx = (BH³ − bh³)/12 = 225452 mm⁴; Zxx = 11273 mm³. |  |
| ELM-0271 | RHS 100×40×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1300 mm²; Ixx = (BH³ − bh³)/12 = 330833 mm⁴; Zxx = 16542 mm³. |  |
| ELM-0272 | RHS 100×40×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1984 mm²; Ixx = (BH³ − bh³)/12 = 436565 mm⁴; Zxx = 21828 mm³. |  |
| ELM-0273 | RHS 100×60×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 624 mm²; Ixx = (BH³ − bh³)/12 = 395072 mm⁴; Zxx = 13169 mm³. |  |
| ELM-0274 | RHS 100×60×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 924 mm²; Ixx = (BH³ − bh³)/12 = 566532 mm⁴; Zxx = 18884 mm³. |  |
| ELM-0275 | RHS 100×60×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1500 mm²; Ixx = (BH³ − bh³)/12 = 862500 mm⁴; Zxx = 28750 mm³. |  |
| ELM-0276 | RHS 100×60×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2304 mm²; Ixx = (BH³ − bh³)/12 = 1203712 mm⁴; Zxx = 40124 mm³. |  |
| ELM-0277 | RHS 100×100×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 784 mm²; Ixx = (BH³ − bh³)/12 = 1255445 mm⁴; Zxx = 25109 mm³. |  |
| ELM-0278 | RHS 100×100×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1164 mm²; Ixx = (BH³ − bh³)/12 = 1827092 mm⁴; Zxx = 36542 mm³. |  |
| ELM-0279 | RHS 100×100×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1900 mm²; Ixx = (BH³ − bh³)/12 = 2865833 mm⁴; Zxx = 57317 mm³. |  |
| ELM-0280 | RHS 100×100×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2944 mm²; Ixx = (BH³ − bh³)/12 = 4184405 mm⁴; Zxx = 83688 mm³. |  |
| ELM-0281 | RHS 100×150×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 984 mm²; Ixx = (BH³ − bh³)/12 = 3227912 mm⁴; Zxx = 43039 mm³. |  |
| ELM-0282 | RHS 100×150×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1464 mm²; Ixx = (BH³ − bh³)/12 = 4734792 mm⁴; Zxx = 63131 mm³. |  |
| ELM-0283 | RHS 100×150×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2400 mm²; Ixx = (BH³ − bh³)/12 = 7545000 mm⁴; Zxx = 100600 mm³. |  |
| ELM-0284 | RHS 100×150×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3744 mm²; Ixx = (BH³ − bh³)/12 = 11282272 mm⁴; Zxx = 150430 mm³. |  |
| ELM-0285 | RHS 100×200×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1184 mm²; Ixx = (BH³ − bh³)/12 = 6430379 mm⁴; Zxx = 64304 mm³. |  |
| ELM-0286 | RHS 100×200×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1764 mm²; Ixx = (BH³ − bh³)/12 = 9472492 mm⁴; Zxx = 94725 mm³. |  |
| ELM-0287 | RHS 100×200×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2900 mm²; Ixx = (BH³ − bh³)/12 = 15224167 mm⁴; Zxx = 152242 mm³. |  |
| ELM-0288 | RHS 100×200×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 4544 mm²; Ixx = (BH³ − bh³)/12 = 23060139 mm⁴; Zxx = 230601 mm³. |  |
| ELM-0289 | RHS 150×40×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 744 mm²; Ixx = (BH³ − bh³)/12 = 232352 mm⁴; Zxx = 11618 mm³. |  |
| ELM-0290 | RHS 150×40×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1104 mm²; Ixx = (BH³ − bh³)/12 = 328352 mm⁴; Zxx = 16418 mm³. |  |
| ELM-0291 | RHS 150×40×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1800 mm²; Ixx = (BH³ − bh³)/12 = 485000 mm⁴; Zxx = 24250 mm³. |  |
| ELM-0292 | RHS 150×40×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2784 mm²; Ixx = (BH³ − bh³)/12 = 645632 mm⁴; Zxx = 32282 mm³. |  |
| ELM-0293 | RHS 150×60×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 824 mm²; Ixx = (BH³ − bh³)/12 = 563339 mm⁴; Zxx = 18778 mm³. |  |
| ELM-0294 | RHS 150×60×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1224 mm²; Ixx = (BH³ − bh³)/12 = 810432 mm⁴; Zxx = 27014 mm³. |  |
| ELM-0295 | RHS 150×60×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2000 mm²; Ixx = (BH³ − bh³)/12 = 1241667 mm⁴; Zxx = 41389 mm³. |  |
| ELM-0296 | RHS 150×60×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3104 mm²; Ixx = (BH³ − bh³)/12 = 1748779 mm⁴; Zxx = 58293 mm³. |  |
| ELM-0297 | RHS 150×100×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 984 mm²; Ixx = (BH³ − bh³)/12 = 1735712 mm⁴; Zxx = 34714 mm³. |  |
| ELM-0298 | RHS 150×100×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1464 mm²; Ixx = (BH³ − bh³)/12 = 2532992 mm⁴; Zxx = 50660 mm³. |  |
| ELM-0299 | RHS 150×100×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2400 mm²; Ixx = (BH³ − bh³)/12 = 3995000 mm⁴; Zxx = 79900 mm³. |  |
| ELM-0300 | RHS 150×100×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3744 mm²; Ixx = (BH³ − bh³)/12 = 5881472 mm⁴; Zxx = 117629 mm³. |  |
| ELM-0301 | RHS 150×150×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1184 mm²; Ixx = (BH³ − bh³)/12 = 4323179 mm⁴; Zxx = 57642 mm³. |  |
| ELM-0302 | RHS 150×150×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1764 mm²; Ixx = (BH³ − bh³)/12 = 6355692 mm⁴; Zxx = 84743 mm³. |  |
| ELM-0303 | RHS 150×150×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2900 mm²; Ixx = (BH³ − bh³)/12 = 10174167 mm⁴; Zxx = 135656 mm³. |  |
| ELM-0304 | RHS 150×150×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 4544 mm²; Ixx = (BH³ − bh³)/12 = 15319339 mm⁴; Zxx = 204258 mm³. |  |
| ELM-0305 | RHS 150×200×2 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 1384 mm²; Ixx = (BH³ − bh³)/12 = 8390645 mm⁴; Zxx = 83906 mm³. |  |
| ELM-0306 | RHS 150×200×3 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 2064 mm²; Ixx = (BH³ − bh³)/12 = 12383392 mm⁴; Zxx = 123834 mm³. |  |
| ELM-0307 | RHS 150×200×5 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 3400 mm²; Ixx = (BH³ − bh³)/12 = 19978333 mm⁴; Zxx = 199783 mm³. |  |
| ELM-0308 | RHS 150×200×8 | Accuracy | P2 | Read the hollow-section catalogue entry (sharp corners). | A = 5344 mm²; Ixx = (BH³ − bh³)/12 = 30437205 mm⁴; Zxx = 304372 mm³. |  |
| ELM-0309 | CHS Ø20×2 | Accuracy | P2 | Read the circular hollow section. | A = 113.1 mm²; I = π/64·(D⁴ − d⁴) = 4637 mm⁴; J = 9274 mm⁴. |  |
| ELM-0310 | CHS Ø20×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 168.89 mm²; I = π/64·(D⁴ − d⁴) = 6174.7 mm⁴; J = 12349 mm⁴. |  |
| ELM-0311 | CHS Ø20×5 | Accuracy | P2 | Read the circular hollow section. | A = 235.62 mm²; I = π/64·(D⁴ − d⁴) = 7363.1 mm⁴; J = 14726 mm⁴. |  |
| ELM-0312 | CHS Ø20×8 | Accuracy | P2 | Read the circular hollow section. | A = 301.59 mm²; I = π/64·(D⁴ − d⁴) = 7841.4 mm⁴; J = 15683 mm⁴. |  |
| ELM-0313 | CHS Ø33.7×2 | Accuracy | P2 | Read the circular hollow section. | A = 199.18 mm²; I = π/64·(D⁴ − d⁴) = 25118 mm⁴; J = 50237 mm⁴. |  |
| ELM-0314 | CHS Ø33.7×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 306.62 mm²; I = π/64·(D⁴ − d⁴) = 36047 mm⁴; J = 72093 mm⁴. |  |
| ELM-0315 | CHS Ø33.7×5 | Accuracy | P2 | Read the circular hollow section. | A = 450.82 mm²; I = π/64·(D⁴ − d⁴) = 47826 mm⁴; J = 95651 mm⁴. |  |
| ELM-0316 | CHS Ø33.7×8 | Accuracy | P2 | Read the circular hollow section. | A = 645.91 mm²; I = π/64·(D⁴ − d⁴) = 58495 mm⁴; J = 116989 mm⁴. |  |
| ELM-0317 | CHS Ø48.3×2 | Accuracy | P2 | Read the circular hollow section. | A = 290.91 mm²; I = π/64·(D⁴ − d⁴) = 78098 mm⁴; J = 156197 mm⁴. |  |
| ELM-0318 | CHS Ø48.3×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 453.39 mm²; I = π/64·(D⁴ − d⁴) = 115857 mm⁴; J = 231713 mm⁴. |  |
| ELM-0319 | CHS Ø48.3×5 | Accuracy | P2 | Read the circular hollow section. | A = 680.15 mm²; I = π/64·(D⁴ − d⁴) = 161527 mm⁴; J = 323055 mm⁴. |  |
| ELM-0320 | CHS Ø48.3×8 | Accuracy | P2 | Read the circular hollow section. | A = 1012.8 mm²; I = π/64·(D⁴ − d⁴) = 213723 mm⁴; J = 427445 mm⁴. |  |
| ELM-0321 | CHS Ø60.3×2 | Accuracy | P2 | Read the circular hollow section. | A = 366.31 mm²; I = π/64·(D⁴ − d⁴) = 155814 mm⁴; J = 311628 mm⁴. |  |
| ELM-0322 | CHS Ø60.3×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 574.03 mm²; I = π/64·(D⁴ − d⁴) = 234682 mm⁴; J = 469364 mm⁴. |  |
| ELM-0323 | CHS Ø60.3×5 | Accuracy | P2 | Read the circular hollow section. | A = 868.65 mm²; I = π/64·(D⁴ − d⁴) = 334766 mm⁴; J = 669532 mm⁴. |  |
| ELM-0324 | CHS Ø60.3×8 | Accuracy | P2 | Read the circular hollow section. | A = 1314.4 mm²; I = π/64·(D⁴ − d⁴) = 459938 mm⁴; J = 919876 mm⁴. |  |
| ELM-0325 | CHS Ø88.9×2 | Accuracy | P2 | Read the circular hollow section. | A = 546.01 mm²; I = π/64·(D⁴ − d⁴) = 515679 mm⁴; J = 1031357 mm⁴. |  |
| ELM-0326 | CHS Ø88.9×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 861.55 mm²; I = π/64·(D⁴ − d⁴) = 792059 mm⁴; J = 1584118 mm⁴. |  |
| ELM-0327 | CHS Ø88.9×5 | Accuracy | P2 | Read the circular hollow section. | A = 1317.9 mm²; I = π/64·(D⁴ − d⁴) = 1163739 mm⁴; J = 2327477 mm⁴. |  |
| ELM-0328 | CHS Ø88.9×8 | Accuracy | P2 | Read the circular hollow section. | A = 2033.2 mm²; I = π/64·(D⁴ − d⁴) = 1679661 mm⁴; J = 3359322 mm⁴. |  |
| ELM-0329 | CHS Ø114.3×2 | Accuracy | P2 | Read the circular hollow section. | A = 705.6 mm²; I = π/64·(D⁴ − d⁴) = 1112671 mm⁴; J = 2225343 mm⁴. |  |
| ELM-0330 | CHS Ø114.3×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 1116.9 mm²; I = π/64·(D⁴ − d⁴) = 1724695 mm⁴; J = 3449389 mm⁴. |  |
| ELM-0331 | CHS Ø114.3×5 | Accuracy | P2 | Read the circular hollow section. | A = 1716.9 mm²; I = π/64·(D⁴ − d⁴) = 2569202 mm⁴; J = 5138404 mm⁴. |  |
| ELM-0332 | CHS Ø114.3×8 | Accuracy | P2 | Read the circular hollow section. | A = 2671.6 mm²; I = π/64·(D⁴ − d⁴) = 3794919 mm⁴; J = 7589838 mm⁴. |  |
| ELM-0333 | CHS Ø168.3×2 | Accuracy | P2 | Read the circular hollow section. | A = 1044.9 mm²; I = π/64·(D⁴ − d⁴) = 3612680 mm⁴; J = 7225359 mm⁴. |  |
| ELM-0334 | CHS Ø168.3×3.2 | Accuracy | P2 | Read the circular hollow section. | A = 1659.8 mm²; I = π/64·(D⁴ − d⁴) = 5657365 mm⁴; J = 11314730 mm⁴. |  |
| ELM-0335 | CHS Ø168.3×5 | Accuracy | P2 | Read the circular hollow section. | A = 2565.1 mm²; I = π/64·(D⁴ − d⁴) = 8558456 mm⁴; J = 17116911 mm⁴. |  |
| ELM-0336 | CHS Ø168.3×8 | Accuracy | P2 | Read the circular hollow section. | A = 4028.8 mm²; I = π/64·(D⁴ − d⁴) = 12972712 mm⁴; J = 25945424 mm⁴. |  |
