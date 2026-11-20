# CLA — NURBS and Class-A analysis

**CATIA-class equivalent:** FreeStyle / Imagine & Shape / ICEM-style Class-A  
**Autevra workspace:** Surfaces (NURBS lab); Styling  
**Scope:** Shared  
**Cases:** 249 (Have 126, Partial 123, Gap 0)

Curve and surface definition checks with exact mathematical expectations, plus shape analyses.

[← Back to the index](../README.md)

## Features

- Curve definition — 112 cases (Have)
- Rational geometry — 14 cases (Have)
- Knot insertion and degree elevation — 51 cases (Partial)
- Shape analysis — 72 cases (Partial)

## Curve definition

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CLA-0001 | Degree 1 with 1 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 2 poles. |  |
| CLA-0002 | Degree 1, 2 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 4; 0 interior knots; ends repeated 2×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0003 | Degree 1, 2 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P1 exactly; C'(0) = 1·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0004 | Degree 1, 2 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0005 | Degree 1, 3 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 5; 1 interior knots; ends repeated 2×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0006 | Degree 1, 3 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P2 exactly; C'(0) = 2·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0007 | Degree 1, 3 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0008 | Degree 1, 5 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 7; 3 interior knots; ends repeated 2×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0009 | Degree 1, 5 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P4 exactly; C'(0) = 4·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0010 | Degree 1, 5 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0011 | Degree 1, 5 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 7; 3 interior knots; ends repeated 2×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0012 | Degree 1, 5 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P4 exactly; C'(0) = 4·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0013 | Degree 1, 5 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0014 | Degree 1, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 22; 18 interior knots; ends repeated 2×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0015 | Degree 1, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 19·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0016 | Degree 1, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0017 | Degree 2 with 2 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 3 poles. |  |
| CLA-0018 | Degree 2, 3 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 6; 0 interior knots; ends repeated 3×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0019 | Degree 2, 3 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P2 exactly; C'(0) = 2·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0020 | Degree 2, 3 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0021 | Degree 2, 4 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 7; 1 interior knots; ends repeated 3×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0022 | Degree 2, 4 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P3 exactly; C'(0) = 4·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0023 | Degree 2, 4 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0024 | Degree 2, 6 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 9; 3 interior knots; ends repeated 3×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0025 | Degree 2, 6 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P5 exactly; C'(0) = 8·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0026 | Degree 2, 6 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0027 | Degree 2, 7 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 10; 4 interior knots; ends repeated 3×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0028 | Degree 2, 7 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P6 exactly; C'(0) = 10·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0029 | Degree 2, 7 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0030 | Degree 2, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 23; 17 interior knots; ends repeated 3×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0031 | Degree 2, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 36·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0032 | Degree 2, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0033 | Degree 3 with 3 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 4 poles. |  |
| CLA-0034 | Degree 3, 4 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 8; 0 interior knots; ends repeated 4×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0035 | Degree 3, 4 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P3 exactly; C'(0) = 3·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0036 | Degree 3, 4 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0037 | Degree 3, 5 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 9; 1 interior knots; ends repeated 4×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0038 | Degree 3, 5 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P4 exactly; C'(0) = 6·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0039 | Degree 3, 5 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0040 | Degree 3, 7 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 11; 3 interior knots; ends repeated 4×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0041 | Degree 3, 7 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P6 exactly; C'(0) = 12·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0042 | Degree 3, 7 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0043 | Degree 3, 9 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 13; 5 interior knots; ends repeated 4×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0044 | Degree 3, 9 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P8 exactly; C'(0) = 18·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0045 | Degree 3, 9 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0046 | Degree 3, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 24; 16 interior knots; ends repeated 4×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0047 | Degree 3, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 51·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0048 | Degree 3, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0049 | Degree 4 with 4 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 5 poles. |  |
| CLA-0050 | Degree 4, 5 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 10; 0 interior knots; ends repeated 5×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0051 | Degree 4, 5 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P4 exactly; C'(0) = 4·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0052 | Degree 4, 5 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0053 | Degree 4, 6 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 11; 1 interior knots; ends repeated 5×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0054 | Degree 4, 6 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P5 exactly; C'(0) = 8·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0055 | Degree 4, 6 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0056 | Degree 4, 8 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 13; 3 interior knots; ends repeated 5×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0057 | Degree 4, 8 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P7 exactly; C'(0) = 16·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0058 | Degree 4, 8 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0059 | Degree 4, 11 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 16; 6 interior knots; ends repeated 5×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0060 | Degree 4, 11 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P10 exactly; C'(0) = 28·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0061 | Degree 4, 11 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0062 | Degree 4, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 25; 15 interior knots; ends repeated 5×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0063 | Degree 4, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 64·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0064 | Degree 4, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0065 | Degree 5 with 5 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 6 poles. |  |
| CLA-0066 | Degree 5, 6 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 12; 0 interior knots; ends repeated 6×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0067 | Degree 5, 6 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P5 exactly; C'(0) = 5·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0068 | Degree 5, 6 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0069 | Degree 5, 7 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 13; 1 interior knots; ends repeated 6×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0070 | Degree 5, 7 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P6 exactly; C'(0) = 10·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0071 | Degree 5, 7 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0072 | Degree 5, 9 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 15; 3 interior knots; ends repeated 6×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0073 | Degree 5, 9 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P8 exactly; C'(0) = 20·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0074 | Degree 5, 9 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0075 | Degree 5, 13 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 19; 7 interior knots; ends repeated 6×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0076 | Degree 5, 13 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P12 exactly; C'(0) = 40·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0077 | Degree 5, 13 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0078 | Degree 5, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 26; 14 interior knots; ends repeated 6×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0079 | Degree 5, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 75·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0080 | Degree 5, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0081 | Degree 6 with 6 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 7 poles. |  |
| CLA-0082 | Degree 6, 7 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 14; 0 interior knots; ends repeated 7×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0083 | Degree 6, 7 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P6 exactly; C'(0) = 6·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0084 | Degree 6, 7 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0085 | Degree 6, 8 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 15; 1 interior knots; ends repeated 7×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0086 | Degree 6, 8 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P7 exactly; C'(0) = 12·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0087 | Degree 6, 8 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0088 | Degree 6, 10 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 17; 3 interior knots; ends repeated 7×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0089 | Degree 6, 10 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P9 exactly; C'(0) = 24·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0090 | Degree 6, 10 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0091 | Degree 6, 15 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 22; 8 interior knots; ends repeated 7×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0092 | Degree 6, 15 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P14 exactly; C'(0) = 54·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0093 | Degree 6, 15 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0094 | Degree 6, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 27; 13 interior knots; ends repeated 7×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0095 | Degree 6, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 84·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0096 | Degree 6, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0097 | Degree 7 with 7 poles | Negative | P2 | Create a clamped uniform B-spline. | Rejected: need at least p+1 = 8 poles. |  |
| CLA-0098 | Degree 7, 8 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 16; 0 interior knots; ends repeated 8×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0099 | Degree 7, 8 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P7 exactly; C'(0) = 7·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0100 | Degree 7, 8 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0101 | Degree 7, 9 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 17; 1 interior knots; ends repeated 8×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0102 | Degree 7, 9 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P8 exactly; C'(0) = 14·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0103 | Degree 7, 9 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0104 | Degree 7, 11 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 19; 3 interior knots; ends repeated 8×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0105 | Degree 7, 11 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P10 exactly; C'(0) = 28·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0106 | Degree 7, 11 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0107 | Degree 7, 17 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 25; 9 interior knots; ends repeated 8×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0108 | Degree 7, 17 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P16 exactly; C'(0) = 70·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0109 | Degree 7, 17 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |
| CLA-0110 | Degree 7, 20 poles: knot vector | Accuracy | P2 | Create a clamped uniform B-spline on [0,1]. | Knot count = n+p+1 = 28; 12 interior knots; ends repeated 8×. | Piegl & Tiller, The NURBS Book, §2 |
| CLA-0111 | Degree 7, 20 poles: end interpolation and tangent | Accuracy | P2 | Evaluate C(0), C(1), C'(0). | C(0)=P0, C(1)=P19 exactly; C'(0) = 91·(P1 − P0) (= p/u_(p+1)). |  |
| CLA-0112 | Degree 7, 20 poles: partition of unity | Accuracy | P2 | Sample 101 parameters; sum the basis functions. | Σ N_i,p(u) = 1 within 1e-12 at every sample; every N ≥ 0. |  |

## Rational geometry

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CLA-0113 | Exact quarter circle r=1 | Accuracy | P2 | Quadratic NURBS, poles (r,0),(r,r),(0,r), weights 1, √2/2, 1. | Radius error < 1e-12·r over 1001 samples. |  |
| CLA-0114 | Full circle r=1 (9 poles) | Accuracy | P2 | Degree 2, 9 poles, knots 0,0,0,¼,¼,½,½,¾,¾,1,1,1. | Closed; perimeter 2πr = 6.283185 within 1e-9 rel. |  |
| CLA-0115 | Exact quarter circle r=10 | Accuracy | P2 | Quadratic NURBS, poles (r,0),(r,r),(0,r), weights 1, √2/2, 1. | Radius error < 1e-12·r over 1001 samples. |  |
| CLA-0116 | Full circle r=10 (9 poles) | Accuracy | P2 | Degree 2, 9 poles, knots 0,0,0,¼,¼,½,½,¾,¾,1,1,1. | Closed; perimeter 2πr = 62.83185 within 1e-9 rel. |  |
| CLA-0117 | Exact quarter circle r=123.4 | Accuracy | P2 | Quadratic NURBS, poles (r,0),(r,r),(0,r), weights 1, √2/2, 1. | Radius error < 1e-12·r over 1001 samples. |  |
| CLA-0118 | Full circle r=123.4 (9 poles) | Accuracy | P2 | Degree 2, 9 poles, knots 0,0,0,¼,¼,½,½,¾,¾,1,1,1. | Closed; perimeter 2πr = 775.3451 within 1e-9 rel. |  |
| CLA-0119 | Exact quarter circle r=1000 | Accuracy | P2 | Quadratic NURBS, poles (r,0),(r,r),(0,r), weights 1, √2/2, 1. | Radius error < 1e-12·r over 1001 samples. |  |
| CLA-0120 | Full circle r=1000 (9 poles) | Accuracy | P2 | Degree 2, 9 poles, knots 0,0,0,¼,¼,½,½,¾,¾,1,1,1. | Closed; perimeter 2πr = 6283.185 within 1e-9 rel. |  |
| CLA-0121 | Pole weight 0 | Boundary | P2 | Set the middle pole weight. | Rejected: weights must be > 0. |  |
| CLA-0122 | Pole weight -1 | Boundary | P2 | Set the middle pole weight. | Rejected: weights must be > 0. |  |
| CLA-0123 | Pole weight 1e-09 | Boundary | P2 | Set the middle pole weight. | Curve pulled towards/away from the pole; still in convex hull. |  |
| CLA-0124 | Pole weight 0.5 | Boundary | P2 | Set the middle pole weight. | Curve pulled towards/away from the pole; still in convex hull. |  |
| CLA-0125 | Pole weight 2 | Boundary | P2 | Set the middle pole weight. | Curve pulled towards/away from the pole; still in convex hull. |  |
| CLA-0126 | Pole weight 100 | Boundary | P2 | Set the middle pole weight. | Curve pulled towards/away from the pole; still in convex hull. |  |

## Knot insertion and degree elevation

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CLA-0127 | Insert knot u=0.1 ×1 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0128 | Insert knot u=0.1 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0129 | Insert knot u=0.1 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0130 | Insert knot u=0.1 ×3 on degree 2 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 2. |  |
| CLA-0131 | Insert knot u=0.25 ×1 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0132 | Insert knot u=0.25 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0133 | Insert knot u=0.25 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0134 | Insert knot u=0.25 ×3 on degree 2 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 2. |  |
| CLA-0135 | Insert knot u=0.5 ×1 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0136 | Insert knot u=0.5 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0137 | Insert knot u=0.5 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0138 | Insert knot u=0.5 ×3 on degree 2 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 2. |  |
| CLA-0139 | Insert knot u=0.9 ×1 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0140 | Insert knot u=0.9 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0141 | Insert knot u=0.9 ×2 on degree 2 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0142 | Insert knot u=0.9 ×3 on degree 2 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 2. |  |
| CLA-0143 | Degree elevate 2→3 | Accuracy | P2 | Elevate the degree. | Shape unchanged (< 1e-12); continuity preserved. |  |
| CLA-0144 | Insert knot u=0.1 ×1 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0145 | Insert knot u=0.1 ×2 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0146 | Insert knot u=0.1 ×3 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +3. |  |
| CLA-0147 | Insert knot u=0.1 ×4 on degree 3 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 3. |  |
| CLA-0148 | Insert knot u=0.25 ×1 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0149 | Insert knot u=0.25 ×2 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0150 | Insert knot u=0.25 ×3 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +3. |  |
| CLA-0151 | Insert knot u=0.25 ×4 on degree 3 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 3. |  |
| CLA-0152 | Insert knot u=0.5 ×1 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0153 | Insert knot u=0.5 ×2 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0154 | Insert knot u=0.5 ×3 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +3. |  |
| CLA-0155 | Insert knot u=0.5 ×4 on degree 3 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 3. |  |
| CLA-0156 | Insert knot u=0.9 ×1 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0157 | Insert knot u=0.9 ×2 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0158 | Insert knot u=0.9 ×3 on degree 3 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +3. |  |
| CLA-0159 | Insert knot u=0.9 ×4 on degree 3 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 3. |  |
| CLA-0160 | Degree elevate 3→4 | Accuracy | P2 | Elevate the degree. | Shape unchanged (< 1e-12); continuity preserved. |  |
| CLA-0161 | Insert knot u=0.1 ×1 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0162 | Insert knot u=0.1 ×2 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0163 | Insert knot u=0.1 ×5 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +5. |  |
| CLA-0164 | Insert knot u=0.1 ×6 on degree 5 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 5. |  |
| CLA-0165 | Insert knot u=0.25 ×1 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0166 | Insert knot u=0.25 ×2 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0167 | Insert knot u=0.25 ×5 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +5. |  |
| CLA-0168 | Insert knot u=0.25 ×6 on degree 5 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 5. |  |
| CLA-0169 | Insert knot u=0.5 ×1 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0170 | Insert knot u=0.5 ×2 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0171 | Insert knot u=0.5 ×5 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +5. |  |
| CLA-0172 | Insert knot u=0.5 ×6 on degree 5 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 5. |  |
| CLA-0173 | Insert knot u=0.9 ×1 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +1. |  |
| CLA-0174 | Insert knot u=0.9 ×2 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +2. |  |
| CLA-0175 | Insert knot u=0.9 ×5 on degree 5 | Accuracy | P2 | Insert knot (Boehm). | Shape unchanged (max deviation < 1e-12); pole count +5. |  |
| CLA-0176 | Insert knot u=0.9 ×6 on degree 5 | Negative | P2 | Insert knot (Boehm). | Rejected: multiplicity cannot exceed degree 5. |  |
| CLA-0177 | Degree elevate 5→6 | Accuracy | P2 | Elevate the degree. | Shape unchanged (< 1e-12); continuity preserved. |  |

## Shape analysis

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CLA-0178 | curvature comb on plane | Accuracy | P2 | Run curvature comb on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0179 | curvature comb on cylinder r=50 | Accuracy | P2 | Run curvature comb on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0180 | curvature comb on sphere r=50 | Accuracy | P2 | Run curvature comb on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0181 | curvature comb on G1 blend | Functional | P2 | Run curvature comb on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0182 | curvature comb on G2 blend | Functional | P2 | Run curvature comb on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0183 | curvature comb on Class-A bonnet patch | Functional | P2 | Run curvature comb on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0184 | porcupine on plane | Accuracy | P2 | Run porcupine on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0185 | porcupine on cylinder r=50 | Accuracy | P2 | Run porcupine on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0186 | porcupine on sphere r=50 | Accuracy | P2 | Run porcupine on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0187 | porcupine on G1 blend | Functional | P2 | Run porcupine on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0188 | porcupine on G2 blend | Functional | P2 | Run porcupine on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0189 | porcupine on Class-A bonnet patch | Functional | P2 | Run porcupine on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0190 | zebra stripes on plane | Accuracy | P2 | Run zebra stripes on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0191 | zebra stripes on cylinder r=50 | Accuracy | P2 | Run zebra stripes on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0192 | zebra stripes on sphere r=50 | Accuracy | P2 | Run zebra stripes on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0193 | zebra stripes on G1 blend | Functional | P2 | Run zebra stripes on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0194 | zebra stripes on G2 blend | Functional | P2 | Run zebra stripes on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0195 | zebra stripes on Class-A bonnet patch | Functional | P2 | Run zebra stripes on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0196 | reflection lines on plane | Accuracy | P2 | Run reflection lines on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0197 | reflection lines on cylinder r=50 | Accuracy | P2 | Run reflection lines on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0198 | reflection lines on sphere r=50 | Accuracy | P2 | Run reflection lines on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0199 | reflection lines on G1 blend | Functional | P2 | Run reflection lines on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0200 | reflection lines on G2 blend | Functional | P2 | Run reflection lines on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0201 | reflection lines on Class-A bonnet patch | Functional | P2 | Run reflection lines on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0202 | highlight lines on plane | Accuracy | P2 | Run highlight lines on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0203 | highlight lines on cylinder r=50 | Accuracy | P2 | Run highlight lines on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0204 | highlight lines on sphere r=50 | Accuracy | P2 | Run highlight lines on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0205 | highlight lines on G1 blend | Functional | P2 | Run highlight lines on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0206 | highlight lines on G2 blend | Functional | P2 | Run highlight lines on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0207 | highlight lines on Class-A bonnet patch | Functional | P2 | Run highlight lines on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0208 | isophotes on plane | Accuracy | P2 | Run isophotes on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0209 | isophotes on cylinder r=50 | Accuracy | P2 | Run isophotes on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0210 | isophotes on sphere r=50 | Accuracy | P2 | Run isophotes on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0211 | isophotes on G1 blend | Functional | P2 | Run isophotes on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0212 | isophotes on G2 blend | Functional | P2 | Run isophotes on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0213 | isophotes on Class-A bonnet patch | Functional | P2 | Run isophotes on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0214 | Gaussian curvature map on plane | Accuracy | P2 | Run Gaussian curvature map on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0215 | Gaussian curvature map on cylinder r=50 | Accuracy | P2 | Run Gaussian curvature map on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0216 | Gaussian curvature map on sphere r=50 | Accuracy | P2 | Run Gaussian curvature map on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0217 | Gaussian curvature map on G1 blend | Functional | P2 | Run Gaussian curvature map on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0218 | Gaussian curvature map on G2 blend | Functional | P2 | Run Gaussian curvature map on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0219 | Gaussian curvature map on Class-A bonnet patch | Functional | P2 | Run Gaussian curvature map on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0220 | mean curvature map on plane | Accuracy | P2 | Run mean curvature map on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0221 | mean curvature map on cylinder r=50 | Accuracy | P2 | Run mean curvature map on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0222 | mean curvature map on sphere r=50 | Accuracy | P2 | Run mean curvature map on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0223 | mean curvature map on G1 blend | Functional | P2 | Run mean curvature map on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0224 | mean curvature map on G2 blend | Functional | P2 | Run mean curvature map on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0225 | mean curvature map on Class-A bonnet patch | Functional | P2 | Run mean curvature map on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0226 | draft angle map on plane | Accuracy | P2 | Run draft angle map on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0227 | draft angle map on cylinder r=50 | Accuracy | P2 | Run draft angle map on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0228 | draft angle map on sphere r=50 | Accuracy | P2 | Run draft angle map on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0229 | draft angle map on G1 blend | Functional | P2 | Run draft angle map on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0230 | draft angle map on G2 blend | Functional | P2 | Run draft angle map on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0231 | draft angle map on Class-A bonnet patch | Functional | P2 | Run draft angle map on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0232 | distance to reference on plane | Accuracy | P2 | Run distance to reference on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0233 | distance to reference on cylinder r=50 | Accuracy | P2 | Run distance to reference on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0234 | distance to reference on sphere r=50 | Accuracy | P2 | Run distance to reference on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0235 | distance to reference on G1 blend | Functional | P2 | Run distance to reference on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0236 | distance to reference on G2 blend | Functional | P2 | Run distance to reference on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0237 | distance to reference on Class-A bonnet patch | Functional | P2 | Run distance to reference on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0238 | inflection points on plane | Accuracy | P2 | Run inflection points on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0239 | inflection points on cylinder r=50 | Accuracy | P2 | Run inflection points on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0240 | inflection points on sphere r=50 | Accuracy | P2 | Run inflection points on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0241 | inflection points on G1 blend | Functional | P2 | Run inflection points on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0242 | inflection points on G2 blend | Functional | P2 | Run inflection points on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0243 | inflection points on Class-A bonnet patch | Functional | P2 | Run inflection points on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
| CLA-0244 | curvature min/max report on plane | Accuracy | P2 | Run curvature min/max report on a plane. | Display correct: zero everywhere / straight stripes. |  |
| CLA-0245 | curvature min/max report on cylinder r=50 | Accuracy | P2 | Run curvature min/max report on a cylinder r=50. | Display correct: k=0.02 1/mm in one direction. |  |
| CLA-0246 | curvature min/max report on sphere r=50 | Accuracy | P2 | Run curvature min/max report on a sphere r=50. | Display correct: K=4e-4 1/mm², uniform. |  |
| CLA-0247 | curvature min/max report on G1 blend | Functional | P2 | Run curvature min/max report on a G1 blend. | Display correct: curvature jump visible at the seam. |  |
| CLA-0248 | curvature min/max report on G2 blend | Functional | P2 | Run curvature min/max report on a G2 blend. | Display correct: continuous curvature across the seam. |  |
| CLA-0249 | curvature min/max report on Class-A bonnet patch | Functional | P2 | Run curvature min/max report on a Class-A bonnet patch. | Display correct: no inflections, smooth flow. |  |
