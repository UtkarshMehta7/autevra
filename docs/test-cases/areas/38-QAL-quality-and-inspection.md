# QAL — Quality and inspection

**CATIA-class equivalent:** Quality / CMM inspection planning add-ons  
**Autevra workspace:** Production → quality  
**Scope:** Shared  
**Cases:** 92 (Have 0, Partial 64, Gap 28)

Process capability, inspection plans and measurement-system checks.

[← Back to the index](../README.md)

## Features

- Process capability — 64 cases (Partial)
- Inspection planning — 28 cases (Gap)

## Process capability

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| QAL-0001 | Tol ±0.05, σ=0.01, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.667; capable. |  |
| QAL-0002 | Tol ±0.05, σ=0.01, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.25; not capable (Cpk < 1.33). |  |
| QAL-0003 | Tol ±0.05, σ=0.01, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0004 | Tol ±0.05, σ=0.01, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.4167; not capable (Cpk < 1.33). |  |
| QAL-0005 | Tol ±0.05, σ=0.02, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0006 | Tol ±0.05, σ=0.02, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.625; not capable (Cpk < 1.33). |  |
| QAL-0007 | Tol ±0.05, σ=0.02, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.4167; not capable (Cpk < 1.33). |  |
| QAL-0008 | Tol ±0.05, σ=0.02, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.2083; not capable (Cpk < 1.33). |  |
| QAL-0009 | Tol ±0.05, σ=0.05, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.3333; not capable (Cpk < 1.33). |  |
| QAL-0010 | Tol ±0.05, σ=0.05, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.25; not capable (Cpk < 1.33). |  |
| QAL-0011 | Tol ±0.05, σ=0.05, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.1667; not capable (Cpk < 1.33). |  |
| QAL-0012 | Tol ±0.05, σ=0.05, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.08333; not capable (Cpk < 1.33). |  |
| QAL-0013 | Tol ±0.05, σ=0.1, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 0.1667; Cpk = 0.1667; not capable (Cpk < 1.33). |  |
| QAL-0014 | Tol ±0.05, σ=0.1, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 0.1667; Cpk = 0.125; not capable (Cpk < 1.33). |  |
| QAL-0015 | Tol ±0.05, σ=0.1, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 0.1667; Cpk = 0.08333; not capable (Cpk < 1.33). |  |
| QAL-0016 | Tol ±0.05, σ=0.1, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 0.1667; Cpk = 0.04167; not capable (Cpk < 1.33). |  |
| QAL-0017 | Tol ±0.1, σ=0.01, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 3.333; capable. |  |
| QAL-0018 | Tol ±0.1, σ=0.01, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 2.5; capable. |  |
| QAL-0019 | Tol ±0.1, σ=0.01, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 1.667; capable. |  |
| QAL-0020 | Tol ±0.1, σ=0.01, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0021 | Tol ±0.1, σ=0.02, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.667; capable. |  |
| QAL-0022 | Tol ±0.1, σ=0.02, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.25; not capable (Cpk < 1.33). |  |
| QAL-0023 | Tol ±0.1, σ=0.02, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0024 | Tol ±0.1, σ=0.02, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.4167; not capable (Cpk < 1.33). |  |
| QAL-0025 | Tol ±0.1, σ=0.05, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 0.6667; Cpk = 0.6667; not capable (Cpk < 1.33). |  |
| QAL-0026 | Tol ±0.1, σ=0.05, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 0.6667; Cpk = 0.5; not capable (Cpk < 1.33). |  |
| QAL-0027 | Tol ±0.1, σ=0.05, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 0.6667; Cpk = 0.3333; not capable (Cpk < 1.33). |  |
| QAL-0028 | Tol ±0.1, σ=0.05, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 0.6667; Cpk = 0.1667; not capable (Cpk < 1.33). |  |
| QAL-0029 | Tol ±0.1, σ=0.1, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.3333; not capable (Cpk < 1.33). |  |
| QAL-0030 | Tol ±0.1, σ=0.1, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.25; not capable (Cpk < 1.33). |  |
| QAL-0031 | Tol ±0.1, σ=0.1, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.1667; not capable (Cpk < 1.33). |  |
| QAL-0032 | Tol ±0.1, σ=0.1, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 0.3333; Cpk = 0.08333; not capable (Cpk < 1.33). |  |
| QAL-0033 | Tol ±0.25, σ=0.01, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 8.333; capable. |  |
| QAL-0034 | Tol ±0.25, σ=0.01, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 6.25; capable. |  |
| QAL-0035 | Tol ±0.25, σ=0.01, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 4.167; capable. |  |
| QAL-0036 | Tol ±0.25, σ=0.01, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 2.083; capable. |  |
| QAL-0037 | Tol ±0.25, σ=0.02, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 4.167; Cpk = 4.167; capable. |  |
| QAL-0038 | Tol ±0.25, σ=0.02, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 4.167; Cpk = 3.125; capable. |  |
| QAL-0039 | Tol ±0.25, σ=0.02, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 4.167; Cpk = 2.083; capable. |  |
| QAL-0040 | Tol ±0.25, σ=0.02, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 4.167; Cpk = 1.042; not capable (Cpk < 1.33). |  |
| QAL-0041 | Tol ±0.25, σ=0.05, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.667; capable. |  |
| QAL-0042 | Tol ±0.25, σ=0.05, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.25; not capable (Cpk < 1.33). |  |
| QAL-0043 | Tol ±0.25, σ=0.05, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0044 | Tol ±0.25, σ=0.05, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.4167; not capable (Cpk < 1.33). |  |
| QAL-0045 | Tol ±0.25, σ=0.1, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0046 | Tol ±0.25, σ=0.1, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.625; not capable (Cpk < 1.33). |  |
| QAL-0047 | Tol ±0.25, σ=0.1, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.4167; not capable (Cpk < 1.33). |  |
| QAL-0048 | Tol ±0.25, σ=0.1, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 0.8333; Cpk = 0.2083; not capable (Cpk < 1.33). |  |
| QAL-0049 | Tol ±0.5, σ=0.01, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 16.67; Cpk = 16.67; capable. |  |
| QAL-0050 | Tol ±0.5, σ=0.01, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 16.67; Cpk = 12.5; capable. |  |
| QAL-0051 | Tol ±0.5, σ=0.01, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 16.67; Cpk = 8.333; capable. |  |
| QAL-0052 | Tol ±0.5, σ=0.01, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 16.67; Cpk = 4.167; capable. |  |
| QAL-0053 | Tol ±0.5, σ=0.02, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 8.333; capable. |  |
| QAL-0054 | Tol ±0.5, σ=0.02, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 6.25; capable. |  |
| QAL-0055 | Tol ±0.5, σ=0.02, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 4.167; capable. |  |
| QAL-0056 | Tol ±0.5, σ=0.02, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 8.333; Cpk = 2.083; capable. |  |
| QAL-0057 | Tol ±0.5, σ=0.05, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 3.333; capable. |  |
| QAL-0058 | Tol ±0.5, σ=0.05, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 2.5; capable. |  |
| QAL-0059 | Tol ±0.5, σ=0.05, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 1.667; capable. |  |
| QAL-0060 | Tol ±0.5, σ=0.05, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 3.333; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0061 | Tol ±0.5, σ=0.1, mean at 0% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.667; capable. |  |
| QAL-0062 | Tol ±0.5, σ=0.1, mean at 25% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 1.25; not capable (Cpk < 1.33). |  |
| QAL-0063 | Tol ±0.5, σ=0.1, mean at 50% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.8333; not capable (Cpk < 1.33). |  |
| QAL-0064 | Tol ±0.5, σ=0.1, mean at 75% of USL | Accuracy | P2 | Compute capability. | Cp = 1.667; Cpk = 0.4167; not capable (Cpk < 1.33). |  |

## Inspection planning

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| QAL-0065 | CMM program from PMI — bracket | Functional | P2 | Run CMM program from PMI on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0066 | CMM program from PMI — housing | Functional | P2 | Run CMM program from PMI on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0067 | CMM program from PMI — turbine blade | Functional | P2 | Run CMM program from PMI on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0068 | CMM program from PMI — body panel | Functional | P2 | Run CMM program from PMI on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0069 | probe path collision check — bracket | Functional | P2 | Run probe path collision check on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0070 | probe path collision check — housing | Functional | P2 | Run probe path collision check on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0071 | probe path collision check — turbine blade | Functional | P2 | Run probe path collision check on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0072 | probe path collision check — body panel | Functional | P2 | Run probe path collision check on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0073 | feature-based inspection (holes) — bracket | Functional | P2 | Run feature-based inspection (holes) on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0074 | feature-based inspection (holes) — housing | Functional | P2 | Run feature-based inspection (holes) on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0075 | feature-based inspection (holes) — turbine blade | Functional | P2 | Run feature-based inspection (holes) on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0076 | feature-based inspection (holes) — body panel | Functional | P2 | Run feature-based inspection (holes) on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0077 | first-article report (AS9102) — bracket | Functional | P2 | Run first-article report (AS9102) on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0078 | first-article report (AS9102) — housing | Functional | P2 | Run first-article report (AS9102) on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0079 | first-article report (AS9102) — turbine blade | Functional | P2 | Run first-article report (AS9102) on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0080 | first-article report (AS9102) — body panel | Functional | P2 | Run first-article report (AS9102) on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0081 | gauge R&R study — bracket | Functional | P2 | Run gauge R&R study on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0082 | gauge R&R study — housing | Functional | P2 | Run gauge R&R study on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0083 | gauge R&R study — turbine blade | Functional | P2 | Run gauge R&R study on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0084 | gauge R&R study — body panel | Functional | P2 | Run gauge R&R study on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0085 | SPC chart from imports — bracket | Functional | P2 | Run SPC chart from imports on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0086 | SPC chart from imports — housing | Functional | P2 | Run SPC chart from imports on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0087 | SPC chart from imports — turbine blade | Functional | P2 | Run SPC chart from imports on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0088 | SPC chart from imports — body panel | Functional | P2 | Run SPC chart from imports on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0089 | deviation colour map — bracket | Functional | P2 | Run deviation colour map on the bracket. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0090 | deviation colour map — housing | Functional | P2 | Run deviation colour map on the housing. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0091 | deviation colour map — turbine blade | Functional | P2 | Run deviation colour map on the turbine blade. | Plan/report generated, linked to the tolerances that drive it. |  |
| QAL-0092 | deviation colour map — body panel | Functional | P2 | Run deviation colour map on the body panel. | Plan/report generated, linked to the tolerances that drive it. |  |
