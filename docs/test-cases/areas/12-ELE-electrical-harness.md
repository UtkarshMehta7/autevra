# ELE — Electrical harness

**CATIA-class equivalent:** Electrical Harness Design / Wire Harness Flattening  
**Autevra workspace:** Routing  
**Scope:** Shared  
**Cases:** 262 (Have 192, Partial 28, Gap 42)

Harness routing, bundles, connectors, voltage drop and bend checks.

[← Back to the index](../README.md)

## Features

- Voltage drop — 192 cases (Have)
- Routing and bundles — 28 cases (Partial)
- Harness design — 42 cases (Gap)

## Voltage drop

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ELE-0001 | 12 V, 5 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (2.87%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0002 | 12 V, 5 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1147 V (0.956%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0003 | 12 V, 5 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.358%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0004 | 12 V, 5 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.01075 V (0.0896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0005 | 12 V, 5 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.688 V (5.73%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0006 | 12 V, 5 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.2293 V (1.91%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0007 | 12 V, 5 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.717%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0008 | 12 V, 5 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.0215 V (0.179%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0009 | 12 V, 5 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (14.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0010 | 12 V, 5 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.5733 V (4.78%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0011 | 12 V, 5 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (1.79%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0012 | 12 V, 5 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.05375 V (0.448%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0013 | 12 V, 5 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 3.44 V (28.7%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0014 | 12 V, 5 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.147 V (9.56%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0015 | 12 V, 5 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (3.58%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0016 | 12 V, 5 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1075 V (0.896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0017 | 12 V, 20 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (11.5%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0018 | 12 V, 20 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.4587 V (3.82%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0019 | 12 V, 20 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.172 V (1.43%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0020 | 12 V, 20 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.358%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0021 | 12 V, 20 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (22.9%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0022 | 12 V, 20 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.9173 V (7.64%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0023 | 12 V, 20 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (2.87%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0024 | 12 V, 20 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.717%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0025 | 12 V, 20 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (57.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0026 | 12 V, 20 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.293 V (19.1%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0027 | 12 V, 20 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.86 V (7.17%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0028 | 12 V, 20 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (1.79%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0029 | 12 V, 20 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (115%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0030 | 12 V, 20 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.587 V (38.2%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0031 | 12 V, 20 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (14.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0032 | 12 V, 20 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (3.58%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0033 | 12 V, 60 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.128 V (34.4%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0034 | 12 V, 60 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (11.5%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0035 | 12 V, 60 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.516 V (4.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0036 | 12 V, 60 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.129 V (1.08%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0037 | 12 V, 60 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 8.256 V (68.8%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0038 | 12 V, 60 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (22.9%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0039 | 12 V, 60 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.032 V (8.6%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0040 | 12 V, 60 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.258 V (2.15%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0041 | 12 V, 60 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 20.64 V (172%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0042 | 12 V, 60 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (57.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0043 | 12 V, 60 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.58 V (21.5%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0044 | 12 V, 60 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.645 V (5.38%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0045 | 12 V, 60 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 41.28 V (344%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0046 | 12 V, 60 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (115%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0047 | 12 V, 60 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 5.16 V (43%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0048 | 12 V, 60 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.29 V (10.8%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0049 | 24 V, 5 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (1.43%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0050 | 24 V, 5 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1147 V (0.478%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0051 | 24 V, 5 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.179%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0052 | 24 V, 5 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.01075 V (0.0448%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0053 | 24 V, 5 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.688 V (2.87%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0054 | 24 V, 5 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.2293 V (0.956%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0055 | 24 V, 5 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.358%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0056 | 24 V, 5 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.0215 V (0.0896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0057 | 24 V, 5 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (7.17%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0058 | 24 V, 5 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.5733 V (2.39%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0059 | 24 V, 5 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (0.896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0060 | 24 V, 5 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.05375 V (0.224%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0061 | 24 V, 5 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 3.44 V (14.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0062 | 24 V, 5 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.147 V (4.78%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0063 | 24 V, 5 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (1.79%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0064 | 24 V, 5 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1075 V (0.448%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0065 | 24 V, 20 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (5.73%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0066 | 24 V, 20 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.4587 V (1.91%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0067 | 24 V, 20 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.172 V (0.717%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0068 | 24 V, 20 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.179%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0069 | 24 V, 20 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (11.5%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0070 | 24 V, 20 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.9173 V (3.82%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0071 | 24 V, 20 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (1.43%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0072 | 24 V, 20 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.358%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0073 | 24 V, 20 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (28.7%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0074 | 24 V, 20 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.293 V (9.56%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0075 | 24 V, 20 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.86 V (3.58%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0076 | 24 V, 20 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (0.896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0077 | 24 V, 20 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (57.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0078 | 24 V, 20 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.587 V (19.1%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0079 | 24 V, 20 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (7.17%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0080 | 24 V, 20 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (1.79%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0081 | 24 V, 60 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.128 V (17.2%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0082 | 24 V, 60 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (5.73%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0083 | 24 V, 60 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.516 V (2.15%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0084 | 24 V, 60 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.129 V (0.538%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0085 | 24 V, 60 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 8.256 V (34.4%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0086 | 24 V, 60 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (11.5%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0087 | 24 V, 60 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.032 V (4.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0088 | 24 V, 60 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.258 V (1.08%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0089 | 24 V, 60 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 20.64 V (86%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0090 | 24 V, 60 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (28.7%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0091 | 24 V, 60 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.58 V (10.8%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0092 | 24 V, 60 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.645 V (2.69%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0093 | 24 V, 60 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 41.28 V (172%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0094 | 24 V, 60 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (57.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0095 | 24 V, 60 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 5.16 V (21.5%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0096 | 24 V, 60 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.29 V (5.38%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0097 | 48 V, 5 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (0.717%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0098 | 48 V, 5 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1147 V (0.239%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0099 | 48 V, 5 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.0896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0100 | 48 V, 5 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.01075 V (0.0224%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0101 | 48 V, 5 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.688 V (1.43%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0102 | 48 V, 5 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.2293 V (0.478%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0103 | 48 V, 5 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.179%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0104 | 48 V, 5 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.0215 V (0.0448%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0105 | 48 V, 5 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (3.58%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0106 | 48 V, 5 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.5733 V (1.19%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0107 | 48 V, 5 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (0.448%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0108 | 48 V, 5 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.05375 V (0.112%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0109 | 48 V, 5 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 3.44 V (7.17%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0110 | 48 V, 5 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.147 V (2.39%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0111 | 48 V, 5 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (0.896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0112 | 48 V, 5 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1075 V (0.224%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0113 | 48 V, 20 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (2.87%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0114 | 48 V, 20 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.4587 V (0.956%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0115 | 48 V, 20 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.172 V (0.358%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0116 | 48 V, 20 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.0896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0117 | 48 V, 20 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (5.73%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0118 | 48 V, 20 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.9173 V (1.91%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0119 | 48 V, 20 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (0.717%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0120 | 48 V, 20 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.179%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0121 | 48 V, 20 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (14.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0122 | 48 V, 20 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.293 V (4.78%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0123 | 48 V, 20 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.86 V (1.79%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0124 | 48 V, 20 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (0.448%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0125 | 48 V, 20 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (28.7%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0126 | 48 V, 20 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.587 V (9.56%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0127 | 48 V, 20 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (3.58%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0128 | 48 V, 20 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (0.896%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0129 | 48 V, 60 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.128 V (8.6%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0130 | 48 V, 60 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (2.87%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0131 | 48 V, 60 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.516 V (1.08%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0132 | 48 V, 60 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.129 V (0.269%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0133 | 48 V, 60 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 8.256 V (17.2%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0134 | 48 V, 60 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (5.73%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0135 | 48 V, 60 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.032 V (2.15%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0136 | 48 V, 60 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.258 V (0.538%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0137 | 48 V, 60 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 20.64 V (43%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0138 | 48 V, 60 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (14.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0139 | 48 V, 60 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.58 V (5.38%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0140 | 48 V, 60 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.645 V (1.34%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0141 | 48 V, 60 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 41.28 V (86%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0142 | 48 V, 60 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (28.7%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0143 | 48 V, 60 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 5.16 V (10.8%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0144 | 48 V, 60 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.29 V (2.69%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0145 | 400 V, 5 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (0.086%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0146 | 400 V, 5 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1147 V (0.0287%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0147 | 400 V, 5 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.0107%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0148 | 400 V, 5 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.01075 V (0.00269%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0149 | 400 V, 5 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.688 V (0.172%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0150 | 400 V, 5 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.2293 V (0.0573%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0151 | 400 V, 5 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.0215%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0152 | 400 V, 5 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.0215 V (0.00537%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0153 | 400 V, 5 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (0.43%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0154 | 400 V, 5 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.5733 V (0.143%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0155 | 400 V, 5 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (0.0537%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0156 | 400 V, 5 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.05375 V (0.0134%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0157 | 400 V, 5 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 3.44 V (0.86%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0158 | 400 V, 5 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.147 V (0.287%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0159 | 400 V, 5 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (0.107%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0160 | 400 V, 5 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.1075 V (0.0269%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0161 | 400 V, 20 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (0.344%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0162 | 400 V, 20 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.4587 V (0.115%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0163 | 400 V, 20 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.172 V (0.043%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0164 | 400 V, 20 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.043 V (0.0107%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0165 | 400 V, 20 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (0.688%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0166 | 400 V, 20 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.9173 V (0.229%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0167 | 400 V, 20 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.344 V (0.086%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0168 | 400 V, 20 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.086 V (0.0215%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0169 | 400 V, 20 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (1.72%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0170 | 400 V, 20 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.293 V (0.573%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0171 | 400 V, 20 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.86 V (0.215%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0172 | 400 V, 20 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.215 V (0.0537%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0173 | 400 V, 20 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (3.44%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0174 | 400 V, 20 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.587 V (1.15%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0175 | 400 V, 20 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.72 V (0.43%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0176 | 400 V, 20 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.43 V (0.107%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0177 | 400 V, 60 A, 1 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 4.128 V (1.03%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0178 | 400 V, 60 A, 1 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.376 V (0.344%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0179 | 400 V, 60 A, 1 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.516 V (0.129%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0180 | 400 V, 60 A, 1 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.129 V (0.0323%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0181 | 400 V, 60 A, 2 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 8.256 V (2.06%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0182 | 400 V, 60 A, 2 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.752 V (0.688%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0183 | 400 V, 60 A, 2 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.032 V (0.258%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0184 | 400 V, 60 A, 2 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.258 V (0.0645%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0185 | 400 V, 60 A, 5 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 20.64 V (5.16%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0186 | 400 V, 60 A, 5 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 6.88 V (1.72%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0187 | 400 V, 60 A, 5 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 2.58 V (0.645%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0188 | 400 V, 60 A, 5 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 0.645 V (0.161%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0189 | 400 V, 60 A, 10 m, 0.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 41.28 V (10.3%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0190 | 400 V, 60 A, 10 m, 1.5 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 13.76 V (3.44%) → FAIL (> 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0191 | 400 V, 60 A, 10 m, 4 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 5.16 V (1.29%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |
| ELE-0192 | 400 V, 60 A, 10 m, 16 mm² Cu | Accuracy | P2 | POST /routing/harness with the circuit. | ΔV = I·2L·ρ/A = 1.29 V (0.323%) → PASS (≤ 3%). | ρCu = 0.0172 Ω·mm²/m (20 °C) |

## Routing and bundles

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ELE-0193 | Bundle of 1 wires Ø1.2 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 1.38 mm (fill factor model); length = polyline length. |  |
| ELE-0194 | Bundle of 1 wires Ø2.0 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 2.3 mm (fill factor model); length = polyline length. |  |
| ELE-0195 | Bundle of 1 wires Ø3.5 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 4.025 mm (fill factor model); length = polyline length. |  |
| ELE-0196 | Bend radius 2× bundle Ø (1 wires) | Boundary | P2 | Insert a bend. | Flag: bend radius below 4× bundle diameter. |  |
| ELE-0197 | Bend radius 4× bundle Ø (1 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0198 | Bend radius 6× bundle Ø (1 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0199 | Bend radius 10× bundle Ø (1 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0200 | Bundle of 5 wires Ø1.2 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 3.086 mm (fill factor model); length = polyline length. |  |
| ELE-0201 | Bundle of 5 wires Ø2.0 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 5.143 mm (fill factor model); length = polyline length. |  |
| ELE-0202 | Bundle of 5 wires Ø3.5 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 9 mm (fill factor model); length = polyline length. |  |
| ELE-0203 | Bend radius 2× bundle Ø (5 wires) | Boundary | P2 | Insert a bend. | Flag: bend radius below 4× bundle diameter. |  |
| ELE-0204 | Bend radius 4× bundle Ø (5 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0205 | Bend radius 6× bundle Ø (5 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0206 | Bend radius 10× bundle Ø (5 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0207 | Bundle of 20 wires Ø1.2 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 6.172 mm (fill factor model); length = polyline length. |  |
| ELE-0208 | Bundle of 20 wires Ø2.0 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 10.29 mm (fill factor model); length = polyline length. |  |
| ELE-0209 | Bundle of 20 wires Ø3.5 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 18 mm (fill factor model); length = polyline length. |  |
| ELE-0210 | Bend radius 2× bundle Ø (20 wires) | Boundary | P2 | Insert a bend. | Flag: bend radius below 4× bundle diameter. |  |
| ELE-0211 | Bend radius 4× bundle Ø (20 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0212 | Bend radius 6× bundle Ø (20 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0213 | Bend radius 10× bundle Ø (20 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0214 | Bundle of 80 wires Ø1.2 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 12.34 mm (fill factor model); length = polyline length. |  |
| ELE-0215 | Bundle of 80 wires Ø2.0 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 20.57 mm (fill factor model); length = polyline length. |  |
| ELE-0216 | Bundle of 80 wires Ø3.5 | Functional | P2 | Route the bundle along 4 waypoints. | Bundle Ø ≈ 1.15·√(n)·d = 36 mm (fill factor model); length = polyline length. |  |
| ELE-0217 | Bend radius 2× bundle Ø (80 wires) | Boundary | P2 | Insert a bend. | Flag: bend radius below 4× bundle diameter. |  |
| ELE-0218 | Bend radius 4× bundle Ø (80 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0219 | Bend radius 6× bundle Ø (80 wires) | Boundary | P2 | Insert a bend. | Pass. |  |
| ELE-0220 | Bend radius 10× bundle Ø (80 wires) | Boundary | P2 | Insert a bend. | Pass. |  |

## Harness design

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ELE-0221 | connector from library — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: connector from library. | Result consistent with the 3D route and wire list. |  |
| ELE-0222 | connector from library — EV 400 V | Functional | P2 | On the EV 400 V harness: connector from library. | Result consistent with the 3D route and wire list. |  |
| ELE-0223 | connector from library — truck 24 V | Functional | P2 | On the truck 24 V harness: connector from library. | Result consistent with the 3D route and wire list. |  |
| ELE-0224 | splice — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: splice. | Result consistent with the 3D route and wire list. |  |
| ELE-0225 | splice — EV 400 V | Functional | P2 | On the EV 400 V harness: splice. | Result consistent with the 3D route and wire list. |  |
| ELE-0226 | splice — truck 24 V | Functional | P2 | On the truck 24 V harness: splice. | Result consistent with the 3D route and wire list. |  |
| ELE-0227 | protective covering (tape) — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: protective covering (tape). | Result consistent with the 3D route and wire list. |  |
| ELE-0228 | protective covering (tape) — EV 400 V | Functional | P2 | On the EV 400 V harness: protective covering (tape). | Result consistent with the 3D route and wire list. |  |
| ELE-0229 | protective covering (tape) — truck 24 V | Functional | P2 | On the truck 24 V harness: protective covering (tape). | Result consistent with the 3D route and wire list. |  |
| ELE-0230 | conduit — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: conduit. | Result consistent with the 3D route and wire list. |  |
| ELE-0231 | conduit — EV 400 V | Functional | P2 | On the EV 400 V harness: conduit. | Result consistent with the 3D route and wire list. |  |
| ELE-0232 | conduit — truck 24 V | Functional | P2 | On the truck 24 V harness: conduit. | Result consistent with the 3D route and wire list. |  |
| ELE-0233 | clip/grommet — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: clip/grommet. | Result consistent with the 3D route and wire list. |  |
| ELE-0234 | clip/grommet — EV 400 V | Functional | P2 | On the EV 400 V harness: clip/grommet. | Result consistent with the 3D route and wire list. |  |
| ELE-0235 | clip/grommet — truck 24 V | Functional | P2 | On the truck 24 V harness: clip/grommet. | Result consistent with the 3D route and wire list. |  |
| ELE-0236 | branch point — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: branch point. | Result consistent with the 3D route and wire list. |  |
| ELE-0237 | branch point — EV 400 V | Functional | P2 | On the EV 400 V harness: branch point. | Result consistent with the 3D route and wire list. |  |
| ELE-0238 | branch point — truck 24 V | Functional | P2 | On the truck 24 V harness: branch point. | Result consistent with the 3D route and wire list. |  |
| ELE-0239 | wire list export — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: wire list export. | Result consistent with the 3D route and wire list. |  |
| ELE-0240 | wire list export — EV 400 V | Functional | P2 | On the EV 400 V harness: wire list export. | Result consistent with the 3D route and wire list. |  |
| ELE-0241 | wire list export — truck 24 V | Functional | P2 | On the truck 24 V harness: wire list export. | Result consistent with the 3D route and wire list. |  |
| ELE-0242 | schematic link — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: schematic link. | Result consistent with the 3D route and wire list. |  |
| ELE-0243 | schematic link — EV 400 V | Functional | P2 | On the EV 400 V harness: schematic link. | Result consistent with the 3D route and wire list. |  |
| ELE-0244 | schematic link — truck 24 V | Functional | P2 | On the truck 24 V harness: schematic link. | Result consistent with the 3D route and wire list. |  |
| ELE-0245 | flatten to formboard — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: flatten to formboard. | Result consistent with the 3D route and wire list. |  |
| ELE-0246 | flatten to formboard — EV 400 V | Functional | P2 | On the EV 400 V harness: flatten to formboard. | Result consistent with the 3D route and wire list. |  |
| ELE-0247 | flatten to formboard — truck 24 V | Functional | P2 | On the truck 24 V harness: flatten to formboard. | Result consistent with the 3D route and wire list. |  |
| ELE-0248 | formboard drawing — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: formboard drawing. | Result consistent with the 3D route and wire list. |  |
| ELE-0249 | formboard drawing — EV 400 V | Functional | P2 | On the EV 400 V harness: formboard drawing. | Result consistent with the 3D route and wire list. |  |
| ELE-0250 | formboard drawing — truck 24 V | Functional | P2 | On the truck 24 V harness: formboard drawing. | Result consistent with the 3D route and wire list. |  |
| ELE-0251 | fuse sizing — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: fuse sizing. | Result consistent with the 3D route and wire list. |  |
| ELE-0252 | fuse sizing — EV 400 V | Functional | P2 | On the EV 400 V harness: fuse sizing. | Result consistent with the 3D route and wire list. |  |
| ELE-0253 | fuse sizing — truck 24 V | Functional | P2 | On the truck 24 V harness: fuse sizing. | Result consistent with the 3D route and wire list. |  |
| ELE-0254 | connector pin-out check — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: connector pin-out check. | Result consistent with the 3D route and wire list. |  |
| ELE-0255 | connector pin-out check — EV 400 V | Functional | P2 | On the EV 400 V harness: connector pin-out check. | Result consistent with the 3D route and wire list. |  |
| ELE-0256 | connector pin-out check — truck 24 V | Functional | P2 | On the truck 24 V harness: connector pin-out check. | Result consistent with the 3D route and wire list. |  |
| ELE-0257 | shielded twisted pair — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: shielded twisted pair. | Result consistent with the 3D route and wire list. |  |
| ELE-0258 | shielded twisted pair — EV 400 V | Functional | P2 | On the EV 400 V harness: shielded twisted pair. | Result consistent with the 3D route and wire list. |  |
| ELE-0259 | shielded twisted pair — truck 24 V | Functional | P2 | On the truck 24 V harness: shielded twisted pair. | Result consistent with the 3D route and wire list. |  |
| ELE-0260 | HV orange cable rules — hatchback 12 V | Functional | P2 | On the hatchback 12 V harness: HV orange cable rules. | Result consistent with the 3D route and wire list. |  |
| ELE-0261 | HV orange cable rules — EV 400 V | Functional | P2 | On the EV 400 V harness: HV orange cable rules. | Result consistent with the 3D route and wire list. |  |
| ELE-0262 | HV orange cable rules — truck 24 V | Functional | P2 | On the truck 24 V harness: HV orange cable rules. | Result consistent with the 3D route and wire list. |  |
