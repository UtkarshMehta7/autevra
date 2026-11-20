# OPT — Optimisation and topology

**CATIA-class equivalent:** Product Engineering Optimizer / Tosca-class topology  
**Autevra workspace:** Structures → topology; Optimization  
**Scope:** Shared  
**Cases:** 137 (Have 87, Partial 0, Gap 50)

SIMP topology optimisation and parametric optimisation/DOE.

[← Back to the index](../README.md)

## Features

- SIMP topology — 72 cases (Have)
- Topology constraints — 30 cases (Gap)
- Parametric optimisation / DOE — 35 cases (Have)

## SIMP topology

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| OPT-0001 | MBB vf=0.3, p=1, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0002 | MBB vf=0.3, p=1, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0003 | MBB vf=0.3, p=1, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0004 | MBB vf=0.3, p=1, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0005 | MBB vf=0.3, p=1, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0006 | MBB vf=0.3, p=1, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0007 | MBB vf=0.3, p=2, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0008 | MBB vf=0.3, p=2, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0009 | MBB vf=0.3, p=2, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0010 | MBB vf=0.3, p=2, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0011 | MBB vf=0.3, p=2, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0012 | MBB vf=0.3, p=2, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0013 | MBB vf=0.3, p=3, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0014 | MBB vf=0.3, p=3, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0015 | MBB vf=0.3, p=3, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0016 | MBB vf=0.3, p=3, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0017 | MBB vf=0.3, p=3, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0018 | MBB vf=0.3, p=3, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0019 | MBB vf=0.3, p=4, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0020 | MBB vf=0.3, p=4, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0021 | MBB vf=0.3, p=4, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0022 | MBB vf=0.3, p=4, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0023 | MBB vf=0.3, p=4, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0024 | MBB vf=0.3, p=4, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.3 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0025 | MBB vf=0.4, p=1, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0026 | MBB vf=0.4, p=1, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0027 | MBB vf=0.4, p=1, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0028 | MBB vf=0.4, p=1, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0029 | MBB vf=0.4, p=1, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0030 | MBB vf=0.4, p=1, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0031 | MBB vf=0.4, p=2, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0032 | MBB vf=0.4, p=2, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0033 | MBB vf=0.4, p=2, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0034 | MBB vf=0.4, p=2, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0035 | MBB vf=0.4, p=2, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0036 | MBB vf=0.4, p=2, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0037 | MBB vf=0.4, p=3, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0038 | MBB vf=0.4, p=3, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0039 | MBB vf=0.4, p=3, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0040 | MBB vf=0.4, p=3, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0041 | MBB vf=0.4, p=3, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0042 | MBB vf=0.4, p=3, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0043 | MBB vf=0.4, p=4, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0044 | MBB vf=0.4, p=4, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0045 | MBB vf=0.4, p=4, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0046 | MBB vf=0.4, p=4, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0047 | MBB vf=0.4, p=4, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0048 | MBB vf=0.4, p=4, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.4 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0049 | MBB vf=0.5, p=1, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0050 | MBB vf=0.5, p=1, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0051 | MBB vf=0.5, p=1, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0052 | MBB vf=0.5, p=1, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0053 | MBB vf=0.5, p=1, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0054 | MBB vf=0.5, p=1, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; p=1 gives grey (no 0/1) result as expected; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0055 | MBB vf=0.5, p=2, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0056 | MBB vf=0.5, p=2, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0057 | MBB vf=0.5, p=2, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0058 | MBB vf=0.5, p=2, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0059 | MBB vf=0.5, p=2, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0060 | MBB vf=0.5, p=2, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0061 | MBB vf=0.5, p=3, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0062 | MBB vf=0.5, p=3, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0063 | MBB vf=0.5, p=3, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0064 | MBB vf=0.5, p=3, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0065 | MBB vf=0.5, p=3, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0066 | MBB vf=0.5, p=3, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0067 | MBB vf=0.5, p=4, rmin=1.5, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0068 | MBB vf=0.5, p=4, rmin=1.5, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0069 | MBB vf=0.5, p=4, rmin=2.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0070 | MBB vf=0.5, p=4, rmin=2.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0071 | MBB vf=0.5, p=4, rmin=3.0, 60×20 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |
| OPT-0072 | MBB vf=0.5, p=4, rmin=3.0, 120×40 | Accuracy | P2 | POST /structures/topology on the MBB half-beam. | Volume fraction = 0.5 ± 0.1%; compliance monotone after 20 iterations; near 0/1 design; seeded run reproducible. | Sigmund 2001, 99-line code |

## Topology constraints

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| OPT-0073 | symmetry plane on bracket | Functional | P2 | Optimise the bracket with symmetry plane. | Constraint visibly respected; report lists it. |  |
| OPT-0074 | symmetry plane on control arm | Functional | P2 | Optimise the control arm with symmetry plane. | Constraint visibly respected; report lists it. |  |
| OPT-0075 | symmetry plane on wing rib | Functional | P2 | Optimise the wing rib with symmetry plane. | Constraint visibly respected; report lists it. |  |
| OPT-0076 | extrusion direction on bracket | Functional | P2 | Optimise the bracket with extrusion direction. | Constraint visibly respected; report lists it. |  |
| OPT-0077 | extrusion direction on control arm | Functional | P2 | Optimise the control arm with extrusion direction. | Constraint visibly respected; report lists it. |  |
| OPT-0078 | extrusion direction on wing rib | Functional | P2 | Optimise the wing rib with extrusion direction. | Constraint visibly respected; report lists it. |  |
| OPT-0079 | draw direction (casting) on bracket | Functional | P2 | Optimise the bracket with draw direction (casting). | Constraint visibly respected; report lists it. |  |
| OPT-0080 | draw direction (casting) on control arm | Functional | P2 | Optimise the control arm with draw direction (casting). | Constraint visibly respected; report lists it. |  |
| OPT-0081 | draw direction (casting) on wing rib | Functional | P2 | Optimise the wing rib with draw direction (casting). | Constraint visibly respected; report lists it. |  |
| OPT-0082 | min member size on bracket | Functional | P2 | Optimise the bracket with min member size. | Constraint visibly respected; report lists it. |  |
| OPT-0083 | min member size on control arm | Functional | P2 | Optimise the control arm with min member size. | Constraint visibly respected; report lists it. |  |
| OPT-0084 | min member size on wing rib | Functional | P2 | Optimise the wing rib with min member size. | Constraint visibly respected; report lists it. |  |
| OPT-0085 | max member size on bracket | Functional | P2 | Optimise the bracket with max member size. | Constraint visibly respected; report lists it. |  |
| OPT-0086 | max member size on control arm | Functional | P2 | Optimise the control arm with max member size. | Constraint visibly respected; report lists it. |  |
| OPT-0087 | max member size on wing rib | Functional | P2 | Optimise the wing rib with max member size. | Constraint visibly respected; report lists it. |  |
| OPT-0088 | frozen regions on bracket | Functional | P2 | Optimise the bracket with frozen regions. | Constraint visibly respected; report lists it. |  |
| OPT-0089 | frozen regions on control arm | Functional | P2 | Optimise the control arm with frozen regions. | Constraint visibly respected; report lists it. |  |
| OPT-0090 | frozen regions on wing rib | Functional | P2 | Optimise the wing rib with frozen regions. | Constraint visibly respected; report lists it. |  |
| OPT-0091 | multiple load cases on bracket | Functional | P2 | Optimise the bracket with multiple load cases. | Constraint visibly respected; report lists it. |  |
| OPT-0092 | multiple load cases on control arm | Functional | P2 | Optimise the control arm with multiple load cases. | Constraint visibly respected; report lists it. |  |
| OPT-0093 | multiple load cases on wing rib | Functional | P2 | Optimise the wing rib with multiple load cases. | Constraint visibly respected; report lists it. |  |
| OPT-0094 | stress constraint on bracket | Functional | P2 | Optimise the bracket with stress constraint. | Constraint visibly respected; report lists it. |  |
| OPT-0095 | stress constraint on control arm | Functional | P2 | Optimise the control arm with stress constraint. | Constraint visibly respected; report lists it. |  |
| OPT-0096 | stress constraint on wing rib | Functional | P2 | Optimise the wing rib with stress constraint. | Constraint visibly respected; report lists it. |  |
| OPT-0097 | frequency target on bracket | Functional | P2 | Optimise the bracket with frequency target. | Constraint visibly respected; report lists it. |  |
| OPT-0098 | frequency target on control arm | Functional | P2 | Optimise the control arm with frequency target. | Constraint visibly respected; report lists it. |  |
| OPT-0099 | frequency target on wing rib | Functional | P2 | Optimise the wing rib with frequency target. | Constraint visibly respected; report lists it. |  |
| OPT-0100 | overhang angle 45° (AM) on bracket | Functional | P2 | Optimise the bracket with overhang angle 45° (AM). | Constraint visibly respected; report lists it. |  |
| OPT-0101 | overhang angle 45° (AM) on control arm | Functional | P2 | Optimise the control arm with overhang angle 45° (AM). | Constraint visibly respected; report lists it. |  |
| OPT-0102 | overhang angle 45° (AM) on wing rib | Functional | P2 | Optimise the wing rib with overhang angle 45° (AM). | Constraint visibly respected; report lists it. |  |

## Parametric optimisation / DOE

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| OPT-0103 | Latin hypercube on Rosenbrock 2D | Functional | P2 | Run Latin hypercube, seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0104 | Latin hypercube on spring mass/stiffness | Functional | P2 | Run Latin hypercube, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0105 | Latin hypercube on damper rate vs comfort | Functional | P2 | Run Latin hypercube, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0106 | Latin hypercube on beam mass vs deflection | Functional | P2 | Run Latin hypercube, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0107 | Latin hypercube on wing span vs range | Functional | P2 | Run Latin hypercube, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0108 | full factorial on Rosenbrock 2D | Functional | P2 | Run full factorial, seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0109 | full factorial on spring mass/stiffness | Functional | P2 | Run full factorial, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0110 | full factorial on damper rate vs comfort | Functional | P2 | Run full factorial, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0111 | full factorial on beam mass vs deflection | Functional | P2 | Run full factorial, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0112 | full factorial on wing span vs range | Functional | P2 | Run full factorial, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0113 | compass search on Rosenbrock 2D | Functional | P2 | Run compass search, seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0114 | compass search on spring mass/stiffness | Functional | P2 | Run compass search, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0115 | compass search on damper rate vs comfort | Functional | P2 | Run compass search, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0116 | compass search on beam mass vs deflection | Functional | P2 | Run compass search, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0117 | compass search on wing span vs range | Functional | P2 | Run compass search, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0118 | Nelder-Mead on Rosenbrock 2D | Functional | P2 | Run Nelder-Mead, seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0119 | Nelder-Mead on spring mass/stiffness | Functional | P2 | Run Nelder-Mead, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0120 | Nelder-Mead on damper rate vs comfort | Functional | P2 | Run Nelder-Mead, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0121 | Nelder-Mead on beam mass vs deflection | Functional | P2 | Run Nelder-Mead, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0122 | Nelder-Mead on wing span vs range | Functional | P2 | Run Nelder-Mead, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0123 | NSGA-II Pareto on Rosenbrock 2D | Functional | P2 | Run NSGA-II Pareto, seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0124 | NSGA-II Pareto on spring mass/stiffness | Functional | P2 | Run NSGA-II Pareto, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0125 | NSGA-II Pareto on damper rate vs comfort | Functional | P2 | Run NSGA-II Pareto, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0126 | NSGA-II Pareto on beam mass vs deflection | Functional | P2 | Run NSGA-II Pareto, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0127 | NSGA-II Pareto on wing span vs range | Functional | P2 | Run NSGA-II Pareto, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0128 | gradient (finite differences) on Rosenbrock 2D | Functional | P2 | Run gradient (finite differences), seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0129 | gradient (finite differences) on spring mass/stiffness | Functional | P2 | Run gradient (finite differences), seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0130 | gradient (finite differences) on damper rate vs comfort | Functional | P2 | Run gradient (finite differences), seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0131 | gradient (finite differences) on beam mass vs deflection | Functional | P2 | Run gradient (finite differences), seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0132 | gradient (finite differences) on wing span vs range | Functional | P2 | Run gradient (finite differences), seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0133 | response surface on Rosenbrock 2D | Functional | P2 | Run response surface, seed 42, bounded. | Converges to (1,1) within 1e-3; history stored. |  |
| OPT-0134 | response surface on spring mass/stiffness | Functional | P2 | Run response surface, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0135 | response surface on damper rate vs comfort | Functional | P2 | Run response surface, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0136 | response surface on beam mass vs deflection | Functional | P2 | Run response surface, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
| OPT-0137 | response surface on wing span vs range | Functional | P2 | Run response surface, seed 42, bounded. | Feasible optimum within bounds; approval required before apply; history stored. |  |
