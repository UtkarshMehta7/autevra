# FEA — Structural analysis (FEA)

**CATIA-class equivalent:** Generative Structural Analysis (GPS/GAS) / SIMULIA  
**Autevra workspace:** Structures; /structures/run  
**Scope:** Shared  
**Cases:** 281 (Have 182, Partial 45, Gap 54)

Linear static, modal, buckling and thermal analysis checked against closed-form solutions.

[← Back to the index](../README.md)

## Features

- Cantilever static (Euler-Bernoulli) — 144 cases (Have)
- Other static benchmarks — 38 cases (Have)
- Modal analysis — 18 cases (Gap)
- Buckling — 12 cases (Gap)
- Thermal — 24 cases (Gap)
- Mesh, solver and results — 45 cases (Partial)

## Cantilever static (Euler-Bernoulli)

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| FEA-0001 | Cantilever steel, L=100, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.19048 mm; σmax = FLc/I = 60 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0002 | Cantilever steel, L=100, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.9048 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0003 | Cantilever steel, L=100, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 9.5238 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0004 | Cantilever steel, L=100, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.095238 mm; σmax = FLc/I = 30 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0005 | Cantilever steel, L=100, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.95238 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0006 | Cantilever steel, L=100, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 4.7619 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0007 | Cantilever steel, L=100, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.02381 mm; σmax = FLc/I = 15 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.1%, widen tolerance). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0008 | Cantilever steel, L=100, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.2381 mm; σmax = FLc/I = 150 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.1%, widen tolerance). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0009 | Cantilever steel, L=100, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.1905 mm; σmax = FLc/I = 750 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.1%, widen tolerance). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0010 | Cantilever steel, L=100, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.0023516 mm; σmax = FLc/I = 2.2222 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7%, widen tolerance). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0011 | Cantilever steel, L=100, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.023516 mm; σmax = FLc/I = 22.222 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7%, widen tolerance). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0012 | Cantilever steel, L=100, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.11758 mm; σmax = FLc/I = 111.11 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7%, widen tolerance). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0013 | Cantilever steel, L=200, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.5238 mm; σmax = FLc/I = 120 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0014 | Cantilever steel, L=200, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 15.238 mm; σmax = FLc/I = 1200 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0015 | Cantilever steel, L=200, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 76.19 mm; σmax = FLc/I = 6000 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0016 | Cantilever steel, L=200, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.7619 mm; σmax = FLc/I = 60 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0017 | Cantilever steel, L=200, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 7.619 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0018 | Cantilever steel, L=200, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 38.095 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0019 | Cantilever steel, L=200, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.19048 mm; σmax = FLc/I = 30 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0020 | Cantilever steel, L=200, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.9048 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0021 | Cantilever steel, L=200, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 9.5238 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0022 | Cantilever steel, L=200, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.018812 mm; σmax = FLc/I = 4.4444 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0023 | Cantilever steel, L=200, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.18812 mm; σmax = FLc/I = 44.444 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0024 | Cantilever steel, L=200, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.94062 mm; σmax = FLc/I = 222.22 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0025 | Cantilever steel, L=500, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 23.81 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0026 | Cantilever steel, L=500, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 238.1 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0027 | Cantilever steel, L=500, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1190.5 mm; σmax = FLc/I = 15000 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0028 | Cantilever steel, L=500, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 11.905 mm; σmax = FLc/I = 150 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0029 | Cantilever steel, L=500, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 119.05 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0030 | Cantilever steel, L=500, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 595.24 mm; σmax = FLc/I = 7500 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0031 | Cantilever steel, L=500, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.9762 mm; σmax = FLc/I = 75 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0032 | Cantilever steel, L=500, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 29.762 mm; σmax = FLc/I = 750 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0033 | Cantilever steel, L=500, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 148.81 mm; σmax = FLc/I = 3750 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0034 | Cantilever steel, L=500, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.29394 mm; σmax = FLc/I = 11.111 MPa at the root (±5%). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0035 | Cantilever steel, L=500, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.9394 mm; σmax = FLc/I = 111.11 MPa at the root (±5%). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0036 | Cantilever steel, L=500, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 14.697 mm; σmax = FLc/I = 555.56 MPa at the root (±5%). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0037 | Cantilever steel, L=1000, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 190.48 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0038 | Cantilever steel, L=1000, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1904.8 mm; σmax = FLc/I = 6000 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0039 | Cantilever steel, L=1000, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 9523.8 mm; σmax = FLc/I = 30000 MPa at the root (±5%). | E=210000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0040 | Cantilever steel, L=1000, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 95.238 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0041 | Cantilever steel, L=1000, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 952.38 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0042 | Cantilever steel, L=1000, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 4761.9 mm; σmax = FLc/I = 15000 MPa at the root (±5%). | E=210000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0043 | Cantilever steel, L=1000, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 23.81 mm; σmax = FLc/I = 150 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0044 | Cantilever steel, L=1000, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 238.1 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0045 | Cantilever steel, L=1000, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1190.5 mm; σmax = FLc/I = 7500 MPa at the root (±5%). | E=210000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0046 | Cantilever steel, L=1000, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.3516 mm; σmax = FLc/I = 22.222 MPa at the root (±5%). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0047 | Cantilever steel, L=1000, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 23.516 mm; σmax = FLc/I = 222.22 MPa at the root (±5%). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0048 | Cantilever steel, L=1000, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 117.58 mm; σmax = FLc/I = 1111.1 MPa at the root (±5%). | E=210000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0049 | Cantilever aluminium 6061, L=100, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.57971 mm; σmax = FLc/I = 60 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0050 | Cantilever aluminium 6061, L=100, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 5.7971 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0051 | Cantilever aluminium 6061, L=100, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 28.986 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0052 | Cantilever aluminium 6061, L=100, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.28986 mm; σmax = FLc/I = 30 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0053 | Cantilever aluminium 6061, L=100, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.8986 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0054 | Cantilever aluminium 6061, L=100, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 14.493 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0055 | Cantilever aluminium 6061, L=100, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.072464 mm; σmax = FLc/I = 15 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.2%, widen tolerance). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0056 | Cantilever aluminium 6061, L=100, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.72464 mm; σmax = FLc/I = 150 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.2%, widen tolerance). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0057 | Cantilever aluminium 6061, L=100, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 3.6232 mm; σmax = FLc/I = 750 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.2%, widen tolerance). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0058 | Cantilever aluminium 6061, L=100, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.0071569 mm; σmax = FLc/I = 2.2222 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7.2%, widen tolerance). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0059 | Cantilever aluminium 6061, L=100, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.071569 mm; σmax = FLc/I = 22.222 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7.2%, widen tolerance). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0060 | Cantilever aluminium 6061, L=100, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.35785 mm; σmax = FLc/I = 111.11 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7.2%, widen tolerance). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0061 | Cantilever aluminium 6061, L=200, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 4.6377 mm; σmax = FLc/I = 120 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0062 | Cantilever aluminium 6061, L=200, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 46.377 mm; σmax = FLc/I = 1200 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0063 | Cantilever aluminium 6061, L=200, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 231.88 mm; σmax = FLc/I = 6000 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0064 | Cantilever aluminium 6061, L=200, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.3188 mm; σmax = FLc/I = 60 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0065 | Cantilever aluminium 6061, L=200, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 23.188 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0066 | Cantilever aluminium 6061, L=200, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 115.94 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0067 | Cantilever aluminium 6061, L=200, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.57971 mm; σmax = FLc/I = 30 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0068 | Cantilever aluminium 6061, L=200, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 5.7971 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0069 | Cantilever aluminium 6061, L=200, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 28.986 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0070 | Cantilever aluminium 6061, L=200, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.057255 mm; σmax = FLc/I = 4.4444 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0071 | Cantilever aluminium 6061, L=200, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.57255 mm; σmax = FLc/I = 44.444 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0072 | Cantilever aluminium 6061, L=200, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.8628 mm; σmax = FLc/I = 222.22 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0073 | Cantilever aluminium 6061, L=500, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 72.464 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0074 | Cantilever aluminium 6061, L=500, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 724.64 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0075 | Cantilever aluminium 6061, L=500, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 3623.2 mm; σmax = FLc/I = 15000 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0076 | Cantilever aluminium 6061, L=500, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 36.232 mm; σmax = FLc/I = 150 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0077 | Cantilever aluminium 6061, L=500, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 362.32 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0078 | Cantilever aluminium 6061, L=500, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1811.6 mm; σmax = FLc/I = 7500 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0079 | Cantilever aluminium 6061, L=500, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 9.058 mm; σmax = FLc/I = 75 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0080 | Cantilever aluminium 6061, L=500, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 90.58 mm; σmax = FLc/I = 750 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0081 | Cantilever aluminium 6061, L=500, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 452.9 mm; σmax = FLc/I = 3750 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0082 | Cantilever aluminium 6061, L=500, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.89461 mm; σmax = FLc/I = 11.111 MPa at the root (±5%). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0083 | Cantilever aluminium 6061, L=500, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 8.9461 mm; σmax = FLc/I = 111.11 MPa at the root (±5%). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0084 | Cantilever aluminium 6061, L=500, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 44.731 mm; σmax = FLc/I = 555.56 MPa at the root (±5%). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0085 | Cantilever aluminium 6061, L=1000, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 579.71 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0086 | Cantilever aluminium 6061, L=1000, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 5797.1 mm; σmax = FLc/I = 6000 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0087 | Cantilever aluminium 6061, L=1000, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 28986 mm; σmax = FLc/I = 30000 MPa at the root (±5%). | E=69000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0088 | Cantilever aluminium 6061, L=1000, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 289.86 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0089 | Cantilever aluminium 6061, L=1000, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2898.6 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0090 | Cantilever aluminium 6061, L=1000, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 14493 mm; σmax = FLc/I = 15000 MPa at the root (±5%). | E=69000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0091 | Cantilever aluminium 6061, L=1000, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 72.464 mm; σmax = FLc/I = 150 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0092 | Cantilever aluminium 6061, L=1000, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 724.64 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0093 | Cantilever aluminium 6061, L=1000, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 3623.2 mm; σmax = FLc/I = 7500 MPa at the root (±5%). | E=69000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0094 | Cantilever aluminium 6061, L=1000, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 7.1569 mm; σmax = FLc/I = 22.222 MPa at the root (±5%). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0095 | Cantilever aluminium 6061, L=1000, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 71.569 mm; σmax = FLc/I = 222.22 MPa at the root (±5%). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0096 | Cantilever aluminium 6061, L=1000, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 357.85 mm; σmax = FLc/I = 1111.1 MPa at the root (±5%). | E=69000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0097 | Cantilever titanium Ti-6Al-4V, L=100, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.35088 mm; σmax = FLc/I = 60 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0098 | Cantilever titanium Ti-6Al-4V, L=100, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 3.5088 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0099 | Cantilever titanium Ti-6Al-4V, L=100, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 17.544 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0100 | Cantilever titanium Ti-6Al-4V, L=100, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.17544 mm; σmax = FLc/I = 30 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0101 | Cantilever titanium Ti-6Al-4V, L=100, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.7544 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0102 | Cantilever titanium Ti-6Al-4V, L=100, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 8.7719 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0103 | Cantilever titanium Ti-6Al-4V, L=100, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.04386 mm; σmax = FLc/I = 15 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.2%, widen tolerance). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0104 | Cantilever titanium Ti-6Al-4V, L=100, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.4386 mm; σmax = FLc/I = 150 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.2%, widen tolerance). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0105 | Cantilever titanium Ti-6Al-4V, L=100, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.193 mm; σmax = FLc/I = 750 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~3.2%, widen tolerance). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0106 | Cantilever titanium Ti-6Al-4V, L=100, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.0043318 mm; σmax = FLc/I = 2.2222 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7.2%, widen tolerance). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0107 | Cantilever titanium Ti-6Al-4V, L=100, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.043318 mm; σmax = FLc/I = 22.222 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7.2%, widen tolerance). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0108 | Cantilever titanium Ti-6Al-4V, L=100, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.21659 mm; σmax = FLc/I = 111.11 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~7.2%, widen tolerance). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0109 | Cantilever titanium Ti-6Al-4V, L=200, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2.807 mm; σmax = FLc/I = 120 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0110 | Cantilever titanium Ti-6Al-4V, L=200, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 28.07 mm; σmax = FLc/I = 1200 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0111 | Cantilever titanium Ti-6Al-4V, L=200, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 140.35 mm; σmax = FLc/I = 6000 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0112 | Cantilever titanium Ti-6Al-4V, L=200, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.4035 mm; σmax = FLc/I = 60 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0113 | Cantilever titanium Ti-6Al-4V, L=200, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 14.035 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0114 | Cantilever titanium Ti-6Al-4V, L=200, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 70.175 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0115 | Cantilever titanium Ti-6Al-4V, L=200, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.35088 mm; σmax = FLc/I = 30 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0116 | Cantilever titanium Ti-6Al-4V, L=200, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 3.5088 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0117 | Cantilever titanium Ti-6Al-4V, L=200, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 17.544 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0118 | Cantilever titanium Ti-6Al-4V, L=200, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.034655 mm; σmax = FLc/I = 4.4444 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0119 | Cantilever titanium Ti-6Al-4V, L=200, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.34655 mm; σmax = FLc/I = 44.444 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0120 | Cantilever titanium Ti-6Al-4V, L=200, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1.7327 mm; σmax = FLc/I = 222.22 MPa at the root (±5%) (L/h < 10: Timoshenko shear adds ~1.8%, widen tolerance). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0121 | Cantilever titanium Ti-6Al-4V, L=500, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 43.86 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0122 | Cantilever titanium Ti-6Al-4V, L=500, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 438.6 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0123 | Cantilever titanium Ti-6Al-4V, L=500, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2193 mm; σmax = FLc/I = 15000 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0124 | Cantilever titanium Ti-6Al-4V, L=500, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 21.93 mm; σmax = FLc/I = 150 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0125 | Cantilever titanium Ti-6Al-4V, L=500, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 219.3 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0126 | Cantilever titanium Ti-6Al-4V, L=500, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1096.5 mm; σmax = FLc/I = 7500 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0127 | Cantilever titanium Ti-6Al-4V, L=500, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 5.4825 mm; σmax = FLc/I = 75 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0128 | Cantilever titanium Ti-6Al-4V, L=500, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 54.825 mm; σmax = FLc/I = 750 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0129 | Cantilever titanium Ti-6Al-4V, L=500, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 274.12 mm; σmax = FLc/I = 3750 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0130 | Cantilever titanium Ti-6Al-4V, L=500, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 0.54148 mm; σmax = FLc/I = 11.111 MPa at the root (±5%). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0131 | Cantilever titanium Ti-6Al-4V, L=500, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 5.4148 mm; σmax = FLc/I = 111.11 MPa at the root (±5%). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0132 | Cantilever titanium Ti-6Al-4V, L=500, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 27.074 mm; σmax = FLc/I = 555.56 MPa at the root (±5%). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0133 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=10×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 350.88 mm; σmax = FLc/I = 600 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0134 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=10×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 3508.8 mm; σmax = FLc/I = 6000 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0135 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=10×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 17544 mm; σmax = FLc/I = 30000 MPa at the root (±5%). | E=114000 MPa, I=833.333 mm⁴; Euler-Bernoulli beam |
| FEA-0136 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=20×10, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 175.44 mm; σmax = FLc/I = 300 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0137 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=20×10, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 1754.4 mm; σmax = FLc/I = 3000 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0138 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=20×10, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 8771.9 mm; σmax = FLc/I = 15000 MPa at the root (±5%). | E=114000 MPa, I=1666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0139 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=10×20, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 43.86 mm; σmax = FLc/I = 150 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0140 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=10×20, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 438.6 mm; σmax = FLc/I = 1500 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0141 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=10×20, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 2193 mm; σmax = FLc/I = 7500 MPa at the root (±5%). | E=114000 MPa, I=6666.67 mm⁴; Euler-Bernoulli beam |
| FEA-0142 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=30×30, F=100 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 4.3318 mm; σmax = FLc/I = 22.222 MPa at the root (±5%). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0143 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=30×30, F=1000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 43.318 mm; σmax = FLc/I = 222.22 MPa at the root (±5%). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |
| FEA-0144 | Cantilever titanium Ti-6Al-4V, L=1000, b×h=30×30, F=5000 N | Accuracy | P1 | Clamp one end; tip load −Z; quadratic tets ≥ 4 through thickness. | Tip δ = FL³/3EI = 216.59 mm; σmax = FLc/I = 1111.1 MPa at the root (±5%). | E=114000 MPa, I=67500 mm⁴; Euler-Bernoulli beam |

## Other static benchmarks

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| FEA-0145 | Simply supported, centre load, L=200, 20×20, F=500 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 0.029762 mm; σ = FL/4·c/I = 18.75 MPa. |  |
| FEA-0146 | Axial bar L=200, 20×20, F=500 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0011905 mm; σ = 1.25 MPa (uniform). |  |
| FEA-0147 | Simply supported, centre load, L=200, 20×20, F=2000 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 0.11905 mm; σ = FL/4·c/I = 75 MPa. |  |
| FEA-0148 | Axial bar L=200, 20×20, F=2000 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0047619 mm; σ = 5 MPa (uniform). |  |
| FEA-0149 | Simply supported, centre load, L=200, 30×10, F=500 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 0.15873 mm; σ = FL/4·c/I = 50 MPa. |  |
| FEA-0150 | Axial bar L=200, 30×10, F=500 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0015873 mm; σ = 1.6667 MPa (uniform). |  |
| FEA-0151 | Simply supported, centre load, L=200, 30×10, F=2000 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 0.63492 mm; σ = FL/4·c/I = 200 MPa. |  |
| FEA-0152 | Axial bar L=200, 30×10, F=2000 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0063492 mm; σ = 6.6667 MPa (uniform). |  |
| FEA-0153 | Simply supported, centre load, L=400, 20×20, F=500 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 0.2381 mm; σ = FL/4·c/I = 37.5 MPa. |  |
| FEA-0154 | Axial bar L=400, 20×20, F=500 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.002381 mm; σ = 1.25 MPa (uniform). |  |
| FEA-0155 | Simply supported, centre load, L=400, 20×20, F=2000 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 0.95238 mm; σ = FL/4·c/I = 150 MPa. |  |
| FEA-0156 | Axial bar L=400, 20×20, F=2000 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0095238 mm; σ = 5 MPa (uniform). |  |
| FEA-0157 | Simply supported, centre load, L=400, 30×10, F=500 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 1.2698 mm; σ = FL/4·c/I = 100 MPa. |  |
| FEA-0158 | Axial bar L=400, 30×10, F=500 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0031746 mm; σ = 1.6667 MPa (uniform). |  |
| FEA-0159 | Simply supported, centre load, L=400, 30×10, F=2000 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 5.0794 mm; σ = FL/4·c/I = 400 MPa. |  |
| FEA-0160 | Axial bar L=400, 30×10, F=2000 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.012698 mm; σ = 6.6667 MPa (uniform). |  |
| FEA-0161 | Simply supported, centre load, L=1000, 20×20, F=500 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 3.7202 mm; σ = FL/4·c/I = 93.75 MPa. |  |
| FEA-0162 | Axial bar L=1000, 20×20, F=500 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0059524 mm; σ = 1.25 MPa (uniform). |  |
| FEA-0163 | Simply supported, centre load, L=1000, 20×20, F=2000 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 14.881 mm; σ = FL/4·c/I = 375 MPa. |  |
| FEA-0164 | Axial bar L=1000, 20×20, F=2000 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.02381 mm; σ = 5 MPa (uniform). |  |
| FEA-0165 | Simply supported, centre load, L=1000, 30×10, F=500 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 19.841 mm; σ = FL/4·c/I = 250 MPa. |  |
| FEA-0166 | Axial bar L=1000, 30×10, F=500 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.0079365 mm; σ = 1.6667 MPa (uniform). |  |
| FEA-0167 | Simply supported, centre load, L=1000, 30×10, F=2000 | Accuracy | P2 | Pin–roller supports; centre load. | δ = FL³/48EI = 79.365 mm; σ = FL/4·c/I = 1000 MPa. |  |
| FEA-0168 | Axial bar L=1000, 30×10, F=2000 | Accuracy | P2 | Clamp one end; axial tension. | δ = FL/AE = 0.031746 mm; σ = 6.6667 MPa (uniform). |  |
| FEA-0169 | Plate W=50 with hole d/W=0.1, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.729; σmax ≈ 121.29 MPa (±7%). | Heywood |
| FEA-0170 | Plate W=100 with hole d/W=0.1, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.729; σmax ≈ 60.644 MPa (±7%). | Heywood |
| FEA-0171 | Plate W=50 with hole d/W=0.2, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.512; σmax ≈ 125.6 MPa (±7%). | Heywood |
| FEA-0172 | Plate W=100 with hole d/W=0.2, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.512; σmax ≈ 62.8 MPa (±7%). | Heywood |
| FEA-0173 | Plate W=50 with hole d/W=0.3, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.343; σmax ≈ 133.89 MPa (±7%). | Heywood |
| FEA-0174 | Plate W=100 with hole d/W=0.3, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.343; σmax ≈ 66.943 MPa (±7%). | Heywood |
| FEA-0175 | Plate W=50 with hole d/W=0.4, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.216; σmax ≈ 147.73 MPa (±7%). | Heywood |
| FEA-0176 | Plate W=100 with hole d/W=0.4, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.216; σmax ≈ 73.867 MPa (±7%). | Heywood |
| FEA-0177 | Plate W=50 with hole d/W=0.5, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.125; σmax ≈ 170 MPa (±7%). | Heywood |
| FEA-0178 | Plate W=100 with hole d/W=0.5, 10 kN, t=5 | Accuracy | P2 | Tension plate; refine at the hole. | Kt(net) = 2 + (1−d/W)³ = 2.125; σmax ≈ 85 MPa (±7%). | Heywood |
| FEA-0179 | Thick cylinder ri=50, ro=60, p=10 MPa | Accuracy | P2 | Internal pressure, plane strain, quarter symmetry. | Inner hoop σθ = p(ro²+ri²)/(ro²−ri²) = 55.455 MPa; σr = −10 MPa (±3%). | Lamé |
| FEA-0180 | Thick cylinder ri=50, ro=75, p=20 MPa | Accuracy | P2 | Internal pressure, plane strain, quarter symmetry. | Inner hoop σθ = p(ro²+ri²)/(ro²−ri²) = 52 MPa; σr = −20 MPa (±3%). | Lamé |
| FEA-0181 | Thick cylinder ri=50, ro=100, p=50 MPa | Accuracy | P2 | Internal pressure, plane strain, quarter symmetry. | Inner hoop σθ = p(ro²+ri²)/(ro²−ri²) = 83.333 MPa; σr = −50 MPa (±3%). | Lamé |
| FEA-0182 | Thick cylinder ri=20, ro=40, p=100 MPa | Accuracy | P2 | Internal pressure, plane strain, quarter symmetry. | Inner hoop σθ = p(ro²+ri²)/(ro²−ri²) = 166.67 MPa; σr = −100 MPa (±3%). | Lamé |

## Modal analysis

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| FEA-0183 | Cantilever modal steel, L=200, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 208.88 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0184 | Cantilever modal steel, L=200, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 104.44 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0185 | Cantilever modal steel, L=500, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 33.421 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0186 | Cantilever modal steel, L=500, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 16.71 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0187 | Cantilever modal steel, L=1000, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 8.3551 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0188 | Cantilever modal steel, L=1000, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 4.1776 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0189 | Cantilever modal aluminium 6061, L=200, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 204.16 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0190 | Cantilever modal aluminium 6061, L=200, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 102.08 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0191 | Cantilever modal aluminium 6061, L=500, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 32.665 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0192 | Cantilever modal aluminium 6061, L=500, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 16.332 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0193 | Cantilever modal aluminium 6061, L=1000, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 8.1662 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0194 | Cantilever modal aluminium 6061, L=1000, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 4.0831 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0195 | Cantilever modal titanium Ti-6Al-4V, L=200, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 204.87 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0196 | Cantilever modal titanium Ti-6Al-4V, L=200, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 102.43 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0197 | Cantilever modal titanium Ti-6Al-4V, L=500, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 32.778 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0198 | Cantilever modal titanium Ti-6Al-4V, L=500, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 16.389 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0199 | Cantilever modal titanium Ti-6Al-4V, L=1000, 10×10 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 8.1946 Hz (±3%); f2/f1 ≈ 6.27. |  |
| FEA-0200 | Cantilever modal titanium Ti-6Al-4V, L=1000, 20×5 | Accuracy | P2 | Modal: first 6 modes. | f1 = (1.8751²/2π)·√(EI/ρAL⁴) = 4.0973 Hz (±3%); f2/f1 ≈ 6.27. |  |

## Buckling

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| FEA-0201 | Euler buckling fixed-free, L=300, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 9595.4 N (K=2.0, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0202 | Euler buckling fixed-free, L=600, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 2398.9 N (K=2.0, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0203 | Euler buckling fixed-free, L=1000, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 863.59 N (K=2.0, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0204 | Euler buckling pinned-pinned, L=300, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 38382 N (K=1.0, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0205 | Euler buckling pinned-pinned, L=600, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 9595.4 N (K=1.0, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0206 | Euler buckling pinned-pinned, L=1000, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 3454.4 N (K=1.0, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0207 | Euler buckling fixed-pinned, L=300, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 78330 N (K=0.7, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0208 | Euler buckling fixed-pinned, L=600, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 19583 N (K=0.7, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0209 | Euler buckling fixed-pinned, L=1000, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 7049.7 N (K=0.7, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0210 | Euler buckling fixed-fixed, L=300, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 153527 N (K=0.5, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0211 | Euler buckling fixed-fixed, L=600, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 38382 N (K=0.5, weak axis I=1666.7 mm⁴) ±3%. |  |
| FEA-0212 | Euler buckling fixed-fixed, L=1000, 20×10 steel | Accuracy | P2 | Linear buckling, first mode. | Pcr = π²EI/(KL)² = 13817 N (K=0.5, weak axis I=1666.7 mm⁴) ±3%. |  |

## Thermal

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| FEA-0213 | Free bar 1000 mm steel, ΔT=10 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 0.12 mm; stress ≈ 0. |  |
| FEA-0214 | Clamped bar steel, ΔT=10 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -25.2 MPa. |  |
| FEA-0215 | Free bar 1000 mm steel, ΔT=50 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 0.6 mm; stress ≈ 0. |  |
| FEA-0216 | Clamped bar steel, ΔT=50 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -126 MPa. |  |
| FEA-0217 | Free bar 1000 mm steel, ΔT=100 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 1.2 mm; stress ≈ 0. |  |
| FEA-0218 | Clamped bar steel, ΔT=100 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -252 MPa. |  |
| FEA-0219 | Free bar 1000 mm steel, ΔT=200 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 2.4 mm; stress ≈ 0. |  |
| FEA-0220 | Clamped bar steel, ΔT=200 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -504 MPa. |  |
| FEA-0221 | Free bar 1000 mm aluminium 6061, ΔT=10 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 0.23 mm; stress ≈ 0. |  |
| FEA-0222 | Clamped bar aluminium 6061, ΔT=10 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -15.87 MPa. |  |
| FEA-0223 | Free bar 1000 mm aluminium 6061, ΔT=50 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 1.15 mm; stress ≈ 0. |  |
| FEA-0224 | Clamped bar aluminium 6061, ΔT=50 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -79.35 MPa. |  |
| FEA-0225 | Free bar 1000 mm aluminium 6061, ΔT=100 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 2.3 mm; stress ≈ 0. |  |
| FEA-0226 | Clamped bar aluminium 6061, ΔT=100 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -158.7 MPa. |  |
| FEA-0227 | Free bar 1000 mm aluminium 6061, ΔT=200 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 4.6 mm; stress ≈ 0. |  |
| FEA-0228 | Clamped bar aluminium 6061, ΔT=200 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -317.4 MPa. |  |
| FEA-0229 | Free bar 1000 mm titanium Ti-6Al-4V, ΔT=10 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 0.086 mm; stress ≈ 0. |  |
| FEA-0230 | Clamped bar titanium Ti-6Al-4V, ΔT=10 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -9.804 MPa. |  |
| FEA-0231 | Free bar 1000 mm titanium Ti-6Al-4V, ΔT=50 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 0.43 mm; stress ≈ 0. |  |
| FEA-0232 | Clamped bar titanium Ti-6Al-4V, ΔT=50 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -49.02 MPa. |  |
| FEA-0233 | Free bar 1000 mm titanium Ti-6Al-4V, ΔT=100 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 0.86 mm; stress ≈ 0. |  |
| FEA-0234 | Clamped bar titanium Ti-6Al-4V, ΔT=100 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -98.04 MPa. |  |
| FEA-0235 | Free bar 1000 mm titanium Ti-6Al-4V, ΔT=200 K | Accuracy | P2 | Uniform temperature rise; free expansion. | ΔL = αΔT·L = 1.72 mm; stress ≈ 0. |  |
| FEA-0236 | Clamped bar titanium Ti-6Al-4V, ΔT=200 K | Accuracy | P2 | Both ends fixed; uniform temperature rise. | σ = −EαΔT = -196.08 MPa. |  |

## Mesh, solver and results

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| FEA-0237 | patch test (constant strain) (bracket) | Regression | P2 | Run patch test (constant strain) on the bracket. | Exact constant stress in every element. |  |
| FEA-0238 | patch test (constant strain) (beam) | Regression | P2 | Run patch test (constant strain) on the beam. | Exact constant stress in every element. |  |
| FEA-0239 | patch test (constant strain) (plate) | Regression | P2 | Run patch test (constant strain) on the plate. | Exact constant stress in every element. |  |
| FEA-0240 | rigid-body check (no BCs) (bracket) | Regression | P2 | Run rigid-body check (no BCs) on the bracket. | Solver reports singular stiffness, 6 zero modes. |  |
| FEA-0241 | rigid-body check (no BCs) (beam) | Regression | P2 | Run rigid-body check (no BCs) on the beam. | Solver reports singular stiffness, 6 zero modes. |  |
| FEA-0242 | rigid-body check (no BCs) (plate) | Regression | P2 | Run rigid-body check (no BCs) on the plate. | Solver reports singular stiffness, 6 zero modes. |  |
| FEA-0243 | mesh convergence h, h/2, h/4 (bracket) | Regression | P2 | Run mesh convergence h, h/2, h/4 on the bracket. | Energy norm converges monotonically; rate reported. |  |
| FEA-0244 | mesh convergence h, h/2, h/4 (beam) | Regression | P2 | Run mesh convergence h, h/2, h/4 on the beam. | Energy norm converges monotonically; rate reported. |  |
| FEA-0245 | mesh convergence h, h/2, h/4 (plate) | Regression | P2 | Run mesh convergence h, h/2, h/4 on the plate. | Energy norm converges monotonically; rate reported. |  |
| FEA-0246 | symmetry BC on half model (bracket) | Regression | P2 | Run symmetry BC on half model on the bracket. | Same result as full model within 0.5%. |  |
| FEA-0247 | symmetry BC on half model (beam) | Regression | P2 | Run symmetry BC on half model on the beam. | Same result as full model within 0.5%. |  |
| FEA-0248 | symmetry BC on half model (plate) | Regression | P2 | Run symmetry BC on half model on the plate. | Same result as full model within 0.5%. |  |
| FEA-0249 | unit change N/mm vs kN/m (bracket) | Regression | P2 | Run unit change N/mm vs kN/m on the bracket. | Identical results after conversion. |  |
| FEA-0250 | unit change N/mm vs kN/m (beam) | Regression | P2 | Run unit change N/mm vs kN/m on the beam. | Identical results after conversion. |  |
| FEA-0251 | unit change N/mm vs kN/m (plate) | Regression | P2 | Run unit change N/mm vs kN/m on the plate. | Identical results after conversion. |  |
| FEA-0252 | tet linear vs tet quadratic (bracket) | Regression | P2 | Run tet linear vs tet quadratic on the bracket. | Quadratic within 2% at coarse mesh; linear stiffer. |  |
| FEA-0253 | tet linear vs tet quadratic (beam) | Regression | P2 | Run tet linear vs tet quadratic on the beam. | Quadratic within 2% at coarse mesh; linear stiffer. |  |
| FEA-0254 | tet linear vs tet quadratic (plate) | Regression | P2 | Run tet linear vs tet quadratic on the plate. | Quadratic within 2% at coarse mesh; linear stiffer. |  |
| FEA-0255 | voxel mesh vs tet mesh (bracket) | Regression | P2 | Run voxel mesh vs tet mesh on the bracket. | Agree within 5% for a block. |  |
| FEA-0256 | voxel mesh vs tet mesh (beam) | Regression | P2 | Run voxel mesh vs tet mesh on the beam. | Agree within 5% for a block. |  |
| FEA-0257 | voxel mesh vs tet mesh (plate) | Regression | P2 | Run voxel mesh vs tet mesh on the plate. | Agree within 5% for a block. |  |
| FEA-0258 | 1M DOF model (bracket) | Regression | P2 | Run 1M DOF model on the bracket. | Solves < 60 s with CG; memory < 4 GB. |  |
| FEA-0259 | 1M DOF model (beam) | Regression | P2 | Run 1M DOF model on the beam. | Solves < 60 s with CG; memory < 4 GB. |  |
| FEA-0260 | 1M DOF model (plate) | Regression | P2 | Run 1M DOF model on the plate. | Solves < 60 s with CG; memory < 4 GB. |  |
| FEA-0261 | bad mesh (sliver) (bracket) | Regression | P2 | Run bad mesh (sliver) on the bracket. | Quality warning with element ids. |  |
| FEA-0262 | bad mesh (sliver) (beam) | Regression | P2 | Run bad mesh (sliver) on the beam. | Quality warning with element ids. |  |
| FEA-0263 | bad mesh (sliver) (plate) | Regression | P2 | Run bad mesh (sliver) on the plate. | Quality warning with element ids. |  |
| FEA-0264 | pressure on curved face (bracket) | Regression | P2 | Run pressure on curved face on the bracket. | Resultant force equals p·projected area. |  |
| FEA-0265 | pressure on curved face (beam) | Regression | P2 | Run pressure on curved face on the beam. | Resultant force equals p·projected area. |  |
| FEA-0266 | pressure on curved face (plate) | Regression | P2 | Run pressure on curved face on the plate. | Resultant force equals p·projected area. |  |
| FEA-0267 | bolt pretension (bracket) | Regression | P2 | Run bolt pretension on the bracket. | Preload reached within 1%. |  |
| FEA-0268 | bolt pretension (beam) | Regression | P2 | Run bolt pretension on the beam. | Preload reached within 1%. |  |
| FEA-0269 | bolt pretension (plate) | Regression | P2 | Run bolt pretension on the plate. | Preload reached within 1%. |  |
| FEA-0270 | contact (frictionless) (bracket) | Regression | P2 | Run contact (frictionless) on the bracket. | Gap closes; no penetration > 1e-3 mm. |  |
| FEA-0271 | contact (frictionless) (beam) | Regression | P2 | Run contact (frictionless) on the beam. | Gap closes; no penetration > 1e-3 mm. |  |
| FEA-0272 | contact (frictionless) (plate) | Regression | P2 | Run contact (frictionless) on the plate. | Gap closes; no penetration > 1e-3 mm. |  |
| FEA-0273 | factor of safety plot (bracket) | Regression | P2 | Run factor of safety plot on the bracket. | FoS = yield / von Mises; min reported. |  |
| FEA-0274 | factor of safety plot (beam) | Regression | P2 | Run factor of safety plot on the beam. | FoS = yield / von Mises; min reported. |  |
| FEA-0275 | factor of safety plot (plate) | Regression | P2 | Run factor of safety plot on the plate. | FoS = yield / von Mises; min reported. |  |
| FEA-0276 | result probe at node (bracket) | Regression | P2 | Run result probe at node on the bracket. | Matches tabular export. |  |
| FEA-0277 | result probe at node (beam) | Regression | P2 | Run result probe at node on the beam. | Matches tabular export. |  |
| FEA-0278 | result probe at node (plate) | Regression | P2 | Run result probe at node on the plate. | Matches tabular export. |  |
| FEA-0279 | CG solver tolerance 1e-8 vs 1e-12 (bracket) | Regression | P2 | Run CG solver tolerance 1e-8 vs 1e-12 on the bracket. | Displacement differs < 1e-6 rel. |  |
| FEA-0280 | CG solver tolerance 1e-8 vs 1e-12 (beam) | Regression | P2 | Run CG solver tolerance 1e-8 vs 1e-12 on the beam. | Displacement differs < 1e-6 rel. |  |
| FEA-0281 | CG solver tolerance 1e-8 vs 1e-12 (plate) | Regression | P2 | Run CG solver tolerance 1e-8 vs 1e-12 on the plate. | Displacement differs < 1e-6 rel. |  |
