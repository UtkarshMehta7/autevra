# PRT — Part Design

**CATIA-class equivalent:** Part Design  
**Autevra workspace:** Part Design  
**Scope:** Shared  
**Cases:** 366 (Have 127, Partial 119, Gap 120)

Feature-based solids: pads, pockets, revolves, holes, dress-up features, patterns and booleans.

[← Back to the index](../README.md)

## Features

- Pad / Pocket — 66 cases (Partial)
- Shaft / Groove (revolve) — 17 cases (Have)
- Hole wizard (ISO metric) — 120 cases (Gap)
- Fillet — 20 cases (Have)
- Chamfer — 7 cases (Have)
- Shell — 9 cases (Have)
- Draft — 11 cases (Partial)
- Booleans — 30 cases (Have)
- Patterns and mirror — 22 cases (Have)
- Feature tree management — 42 cases (Partial)
- Loft / Sweep / Rib — 22 cases (Have)

## Pad / Pocket

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0001 | Pad rectangle 40×20 by 0.1 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 0.1 mm. | Valid closed solid; volume 80 mm³ (±1e-6 rel); bbox Z = 0.1 mm. | profile area 800 mm² |
| PRT-0002 | Pad rectangle 40×20 by 1 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 1 mm. | Valid closed solid; volume 800 mm³ (±1e-6 rel); bbox Z = 1 mm. | profile area 800 mm² |
| PRT-0003 | Pad rectangle 40×20 by 5 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 5 mm. | Valid closed solid; volume 4000 mm³ (±1e-6 rel); bbox Z = 5 mm. | profile area 800 mm² |
| PRT-0004 | Pad rectangle 40×20 by 10 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 10 mm. | Valid closed solid; volume 8000 mm³ (±1e-6 rel); bbox Z = 10 mm. | profile area 800 mm² |
| PRT-0005 | Pad rectangle 40×20 by 50 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 50 mm. | Valid closed solid; volume 40000 mm³ (±1e-6 rel); bbox Z = 50 mm. | profile area 800 mm² |
| PRT-0006 | Pad rectangle 40×20 by 100 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 100 mm. | Valid closed solid; volume 80000 mm³ (±1e-6 rel); bbox Z = 100 mm. | profile area 800 mm² |
| PRT-0007 | Pad rectangle 40×20 by 250 mm | Functional | P1 | Sketch rectangle 40×20 on XY; Pad, dimension limit 250 mm. | Valid closed solid; volume 200000 mm³ (±1e-6 rel); bbox Z = 250 mm. | profile area 800 mm² |
| PRT-0008 | Pad circle Ø20 by 0.1 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 0.1 mm. | Valid closed solid; volume 31.4159 mm³ (±1e-6 rel); bbox Z = 0.1 mm. | profile area 314.159 mm² |
| PRT-0009 | Pad circle Ø20 by 1 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 1 mm. | Valid closed solid; volume 314.159 mm³ (±1e-6 rel); bbox Z = 1 mm. | profile area 314.159 mm² |
| PRT-0010 | Pad circle Ø20 by 5 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 5 mm. | Valid closed solid; volume 1570.8 mm³ (±1e-6 rel); bbox Z = 5 mm. | profile area 314.159 mm² |
| PRT-0011 | Pad circle Ø20 by 10 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 10 mm. | Valid closed solid; volume 3141.59 mm³ (±1e-6 rel); bbox Z = 10 mm. | profile area 314.159 mm² |
| PRT-0012 | Pad circle Ø20 by 50 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 50 mm. | Valid closed solid; volume 15708 mm³ (±1e-6 rel); bbox Z = 50 mm. | profile area 314.159 mm² |
| PRT-0013 | Pad circle Ø20 by 100 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 100 mm. | Valid closed solid; volume 31415.9 mm³ (±1e-6 rel); bbox Z = 100 mm. | profile area 314.159 mm² |
| PRT-0014 | Pad circle Ø20 by 250 mm | Functional | P1 | Sketch circle Ø20 on XY; Pad, dimension limit 250 mm. | Valid closed solid; volume 78539.8 mm³ (±1e-6 rel); bbox Z = 250 mm. | profile area 314.159 mm² |
| PRT-0015 | Pad hexagon AF 20 by 0.1 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 0.1 mm. | Valid closed solid; volume 34.641 mm³ (±1e-6 rel); bbox Z = 0.1 mm. | profile area 346.41 mm² |
| PRT-0016 | Pad hexagon AF 20 by 1 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 1 mm. | Valid closed solid; volume 346.41 mm³ (±1e-6 rel); bbox Z = 1 mm. | profile area 346.41 mm² |
| PRT-0017 | Pad hexagon AF 20 by 5 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 5 mm. | Valid closed solid; volume 1732.05 mm³ (±1e-6 rel); bbox Z = 5 mm. | profile area 346.41 mm² |
| PRT-0018 | Pad hexagon AF 20 by 10 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 10 mm. | Valid closed solid; volume 3464.1 mm³ (±1e-6 rel); bbox Z = 10 mm. | profile area 346.41 mm² |
| PRT-0019 | Pad hexagon AF 20 by 50 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 50 mm. | Valid closed solid; volume 17320.5 mm³ (±1e-6 rel); bbox Z = 50 mm. | profile area 346.41 mm² |
| PRT-0020 | Pad hexagon AF 20 by 100 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 100 mm. | Valid closed solid; volume 34641 mm³ (±1e-6 rel); bbox Z = 100 mm. | profile area 346.41 mm² |
| PRT-0021 | Pad hexagon AF 20 by 250 mm | Functional | P1 | Sketch hexagon AF 20 on XY; Pad, dimension limit 250 mm. | Valid closed solid; volume 86602.5 mm³ (±1e-6 rel); bbox Z = 250 mm. | profile area 346.41 mm² |
| PRT-0022 | Pad slot 40×10 by 0.1 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 0.1 mm. | Valid closed solid; volume 37.854 mm³ (±1e-6 rel); bbox Z = 0.1 mm. | profile area 378.54 mm² |
| PRT-0023 | Pad slot 40×10 by 1 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 1 mm. | Valid closed solid; volume 378.54 mm³ (±1e-6 rel); bbox Z = 1 mm. | profile area 378.54 mm² |
| PRT-0024 | Pad slot 40×10 by 5 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 5 mm. | Valid closed solid; volume 1892.7 mm³ (±1e-6 rel); bbox Z = 5 mm. | profile area 378.54 mm² |
| PRT-0025 | Pad slot 40×10 by 10 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 10 mm. | Valid closed solid; volume 3785.4 mm³ (±1e-6 rel); bbox Z = 10 mm. | profile area 378.54 mm² |
| PRT-0026 | Pad slot 40×10 by 50 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 50 mm. | Valid closed solid; volume 18927 mm³ (±1e-6 rel); bbox Z = 50 mm. | profile area 378.54 mm² |
| PRT-0027 | Pad slot 40×10 by 100 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 100 mm. | Valid closed solid; volume 37854 mm³ (±1e-6 rel); bbox Z = 100 mm. | profile area 378.54 mm² |
| PRT-0028 | Pad slot 40×10 by 250 mm | Functional | P1 | Sketch slot 40×10 on XY; Pad, dimension limit 250 mm. | Valid closed solid; volume 94635 mm³ (±1e-6 rel); bbox Z = 250 mm. | profile area 378.54 mm² |
| PRT-0029 | Pad triangle 30-40-50 by 0.1 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 0.1 mm. | Valid closed solid; volume 60 mm³ (±1e-6 rel); bbox Z = 0.1 mm. | profile area 600 mm² |
| PRT-0030 | Pad triangle 30-40-50 by 1 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 1 mm. | Valid closed solid; volume 600 mm³ (±1e-6 rel); bbox Z = 1 mm. | profile area 600 mm² |
| PRT-0031 | Pad triangle 30-40-50 by 5 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 5 mm. | Valid closed solid; volume 3000 mm³ (±1e-6 rel); bbox Z = 5 mm. | profile area 600 mm² |
| PRT-0032 | Pad triangle 30-40-50 by 10 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 10 mm. | Valid closed solid; volume 6000 mm³ (±1e-6 rel); bbox Z = 10 mm. | profile area 600 mm² |
| PRT-0033 | Pad triangle 30-40-50 by 50 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 50 mm. | Valid closed solid; volume 30000 mm³ (±1e-6 rel); bbox Z = 50 mm. | profile area 600 mm² |
| PRT-0034 | Pad triangle 30-40-50 by 100 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 100 mm. | Valid closed solid; volume 60000 mm³ (±1e-6 rel); bbox Z = 100 mm. | profile area 600 mm² |
| PRT-0035 | Pad triangle 30-40-50 by 250 mm | Functional | P1 | Sketch triangle 30-40-50 on XY; Pad, dimension limit 250 mm. | Valid closed solid; volume 150000 mm³ (±1e-6 rel); bbox Z = 250 mm. | profile area 600 mm² |
| PRT-0036 | Pad ring Ø40/Ø20 by 0.1 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 0.1 mm. | Valid closed solid; volume 94.2478 mm³ (±1e-6 rel); bbox Z = 0.1 mm. | profile area 942.478 mm² |
| PRT-0037 | Pad ring Ø40/Ø20 by 1 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 1 mm. | Valid closed solid; volume 942.478 mm³ (±1e-6 rel); bbox Z = 1 mm. | profile area 942.478 mm² |
| PRT-0038 | Pad ring Ø40/Ø20 by 5 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 5 mm. | Valid closed solid; volume 4712.39 mm³ (±1e-6 rel); bbox Z = 5 mm. | profile area 942.478 mm² |
| PRT-0039 | Pad ring Ø40/Ø20 by 10 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 10 mm. | Valid closed solid; volume 9424.78 mm³ (±1e-6 rel); bbox Z = 10 mm. | profile area 942.478 mm² |
| PRT-0040 | Pad ring Ø40/Ø20 by 50 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 50 mm. | Valid closed solid; volume 47123.9 mm³ (±1e-6 rel); bbox Z = 50 mm. | profile area 942.478 mm² |
| PRT-0041 | Pad ring Ø40/Ø20 by 100 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 100 mm. | Valid closed solid; volume 94247.8 mm³ (±1e-6 rel); bbox Z = 100 mm. | profile area 942.478 mm² |
| PRT-0042 | Pad ring Ø40/Ø20 by 250 mm | Functional | P1 | Sketch ring Ø40/Ø20 on XY; Pad, dimension limit 250 mm. | Valid closed solid; volume 235619 mm³ (±1e-6 rel); bbox Z = 250 mm. | profile area 942.478 mm² |
| PRT-0043 | Pad: limit 'Up to next' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Up to next'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0044 | Pocket: limit 'Up to next' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Up to next'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0045 | Pad: limit 'Up to last' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Up to last'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0046 | Pocket: limit 'Up to last' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Up to last'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0047 | Pad: limit 'Up to plane' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Up to plane'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0048 | Pocket: limit 'Up to plane' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Up to plane'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0049 | Pad: limit 'Up to surface' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Up to surface'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0050 | Pocket: limit 'Up to surface' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Up to surface'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0051 | Pad: limit 'Mirrored extent' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Mirrored extent'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0052 | Pocket: limit 'Mirrored extent' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Mirrored extent'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0053 | Pad: limit 'Two limits (10/-5)' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Two limits (10/-5)'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0054 | Pocket: limit 'Two limits (10/-5)' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Two limits (10/-5)'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0055 | Pad: limit 'Thick pad (2 mm wall)' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Thick pad (2 mm wall)'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0056 | Pocket: limit 'Thick pad (2 mm wall)' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Thick pad (2 mm wall)'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0057 | Pad: limit 'Along custom direction 30°' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Along custom direction 30°'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0058 | Pocket: limit 'Along custom direction 30°' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Along custom direction 30°'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0059 | Pad: limit 'Reverse direction' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Reverse direction'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0060 | Pocket: limit 'Reverse direction' | Functional | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Reverse direction'. | Feature builds; result volume matches a hand-computed reference within 1e-6 relative. |  |
| PRT-0061 | Pad: limit 'Depth 0 (reject)' | Negative | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Depth 0 (reject)'. | Rejected with a clear limit error; tree unchanged. |  |
| PRT-0062 | Pocket: limit 'Depth 0 (reject)' | Negative | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Depth 0 (reject)'. | Rejected with a clear limit error; tree unchanged. |  |
| PRT-0063 | Pad: limit 'Negative depth -10' | Negative | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Negative depth -10'. | Rejected with a clear limit error; tree unchanged. |  |
| PRT-0064 | Pocket: limit 'Negative depth -10' | Negative | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Negative depth -10'. | Rejected with a clear limit error; tree unchanged. |  |
| PRT-0065 | Pad: limit 'Up to a face that does not intersect (reject)' | Negative | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pad with 'Up to a face that does not intersect (reject)'. | Rejected with a clear limit error; tree unchanged. |  |
| PRT-0066 | Pocket: limit 'Up to a face that does not intersect (reject)' | Negative | P2 | Base block 100×60×40; sketch rectangle 20×20 on top face; Pocket with 'Up to a face that does not intersect (reject)'. | Rejected with a clear limit error; tree unchanged. |  |

## Shaft / Groove (revolve)

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0067 | Shaft 10×20 profile, -10° | Boundary | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Rejected: angle must be in (0, 360]. | A=200.0 mm², R̄=30.0 mm, θ=-10°; Pappus' centroid theorem |
| PRT-0068 | Shaft 10×20 profile, 0° | Boundary | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Rejected: angle must be in (0, 360]. | A=200.0 mm², R̄=30.0 mm, θ=0°; Pappus' centroid theorem |
| PRT-0069 | Shaft 10×20 profile, 0.5° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 52.3599 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=0.5°; Pappus' centroid theorem |
| PRT-0070 | Shaft 10×20 profile, 1° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 104.72 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=1°; Pappus' centroid theorem |
| PRT-0071 | Shaft 10×20 profile, 45° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 4712.39 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=45°; Pappus' centroid theorem |
| PRT-0072 | Shaft 10×20 profile, 90° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 9424.78 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=90°; Pappus' centroid theorem |
| PRT-0073 | Shaft 10×20 profile, 180° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 18849.6 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=180°; Pappus' centroid theorem |
| PRT-0074 | Shaft 10×20 profile, 270° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 28274.3 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=270°; Pappus' centroid theorem |
| PRT-0075 | Shaft 10×20 profile, 359.9° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 37688.6 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=359.9°; Pappus' centroid theorem |
| PRT-0076 | Shaft 10×20 profile, 360° | Accuracy | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Volume = 2π·R̄·A·θ/360 = 37699.1 mm³ (Pappus, ±1e-6 rel). | A=200.0 mm², R̄=30.0 mm, θ=360°; Pappus' centroid theorem |
| PRT-0077 | Shaft 10×20 profile, 361° | Boundary | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Rejected: angle must be in (0, 360]. | A=200.0 mm², R̄=30.0 mm, θ=361°; Pappus' centroid theorem |
| PRT-0078 | Shaft 10×20 profile, 720° | Boundary | P2 | Sketch rectangle 10 (radial) × 20 centred 30 mm from the Z axis; Shaft about Z. | Rejected: angle must be in (0, 360]. | A=200.0 mm², R̄=30.0 mm, θ=720°; Pappus' centroid theorem |
| PRT-0079 | Revolve: profile crossing the axis | Functional | P2 | Set up profile crossing the axis; revolve 360°. | Rejected: self-intersecting revolve |  |
| PRT-0080 | Revolve: profile edge on the axis | Functional | P2 | Set up profile edge on the axis; revolve 360°. | Builds a solid with no inner hole |  |
| PRT-0081 | Revolve: axis = sketch construction line | Functional | P2 | Set up axis = sketch construction line; revolve 360°. | Accepted; axis reference stored |  |
| PRT-0082 | Revolve: axis = model edge | Functional | P2 | Set up axis = model edge; revolve 360°. | Accepted; follows the edge on rebuild |  |
| PRT-0083 | Revolve: groove 90° into a cylinder Ø50 | Functional | P2 | Set up groove 90° into a cylinder Ø50; revolve 360°. | Material removed equals the swept volume |  |

## Hole wizard (ISO metric)

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0084 | M3 tapped, blind 2×d | Functional | P2 | Place hole M3 tapped on a 60 mm plate; blind 2×d. | Drill Ø2.5 mm (= d − P = 3 − 0.5); cosmetic thread M3×0.5; thread depth 2×d=6 mm. | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0085 | M3 tapped, through all | Functional | P2 | Place hole M3 tapped on a 60 mm plate; through all. | Drill Ø2.5 mm (= d − P = 3 − 0.5); cosmetic thread M3×0.5; thread depth 2×d=6 mm. | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0086 | M3 tapped, up to next face | Functional | P2 | Place hole M3 tapped on a 60 mm plate; up to next face. | Drill Ø2.5 mm (= d − P = 3 − 0.5); cosmetic thread M3×0.5; thread depth 2×d=6 mm. | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0087 | M3 clearance (medium), blind 2×d | Functional | P2 | Place hole M3 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø3.4 mm (ISO 273 medium). | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0088 | M3 clearance (medium), through all | Functional | P2 | Place hole M3 clearance (medium) on a 60 mm plate; through all. | Hole Ø3.4 mm (ISO 273 medium). | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0089 | M3 clearance (medium), up to next face | Functional | P2 | Place hole M3 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø3.4 mm (ISO 273 medium). | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0090 | M3 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M3 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø3.4 mm; counterbore Ø ≥ 5.5 mm (head dk) and depth ≥ 3 mm (head k). | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0091 | M3 counterbored for ISO 4762, through all | Functional | P2 | Place hole M3 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø3.4 mm; counterbore Ø ≥ 5.5 mm (head dk) and depth ≥ 3 mm (head k). | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0092 | M3 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M3 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø3.4 mm; counterbore Ø ≥ 5.5 mm (head dk) and depth ≥ 3 mm (head k). | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0093 | M3 countersunk for ISO 10642, blind 2×d | Functional | P2 | Place hole M3 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø3.4 mm; 90° countersink to Ø6.72 mm. | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0094 | M3 countersunk for ISO 10642, through all | Functional | P2 | Place hole M3 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø3.4 mm; 90° countersink to Ø6.72 mm. | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0095 | M3 countersunk for ISO 10642, up to next face | Functional | P2 | Place hole M3 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø3.4 mm; 90° countersink to Ø6.72 mm. | M3: P=0.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0096 | M4 tapped, blind 2×d | Functional | P2 | Place hole M4 tapped on a 60 mm plate; blind 2×d. | Drill Ø3.3 mm (= d − P = 4 − 0.7); cosmetic thread M4×0.7; thread depth 2×d=8 mm. | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0097 | M4 tapped, through all | Functional | P2 | Place hole M4 tapped on a 60 mm plate; through all. | Drill Ø3.3 mm (= d − P = 4 − 0.7); cosmetic thread M4×0.7; thread depth 2×d=8 mm. | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0098 | M4 tapped, up to next face | Functional | P2 | Place hole M4 tapped on a 60 mm plate; up to next face. | Drill Ø3.3 mm (= d − P = 4 − 0.7); cosmetic thread M4×0.7; thread depth 2×d=8 mm. | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0099 | M4 clearance (medium), blind 2×d | Functional | P2 | Place hole M4 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø4.5 mm (ISO 273 medium). | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0100 | M4 clearance (medium), through all | Functional | P2 | Place hole M4 clearance (medium) on a 60 mm plate; through all. | Hole Ø4.5 mm (ISO 273 medium). | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0101 | M4 clearance (medium), up to next face | Functional | P2 | Place hole M4 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø4.5 mm (ISO 273 medium). | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0102 | M4 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M4 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø4.5 mm; counterbore Ø ≥ 7.0 mm (head dk) and depth ≥ 4 mm (head k). | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0103 | M4 counterbored for ISO 4762, through all | Functional | P2 | Place hole M4 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø4.5 mm; counterbore Ø ≥ 7.0 mm (head dk) and depth ≥ 4 mm (head k). | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0104 | M4 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M4 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø4.5 mm; counterbore Ø ≥ 7.0 mm (head dk) and depth ≥ 4 mm (head k). | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0105 | M4 countersunk for ISO 10642, blind 2×d | Functional | P2 | Place hole M4 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø4.5 mm; 90° countersink to Ø8.96 mm. | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0106 | M4 countersunk for ISO 10642, through all | Functional | P2 | Place hole M4 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø4.5 mm; 90° countersink to Ø8.96 mm. | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0107 | M4 countersunk for ISO 10642, up to next face | Functional | P2 | Place hole M4 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø4.5 mm; 90° countersink to Ø8.96 mm. | M4: P=0.7; ISO 261 / 273 / 4762 / 10642 |
| PRT-0108 | M5 tapped, blind 2×d | Functional | P2 | Place hole M5 tapped on a 60 mm plate; blind 2×d. | Drill Ø4.2 mm (= d − P = 5 − 0.8); cosmetic thread M5×0.8; thread depth 2×d=10 mm. | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0109 | M5 tapped, through all | Functional | P2 | Place hole M5 tapped on a 60 mm plate; through all. | Drill Ø4.2 mm (= d − P = 5 − 0.8); cosmetic thread M5×0.8; thread depth 2×d=10 mm. | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0110 | M5 tapped, up to next face | Functional | P2 | Place hole M5 tapped on a 60 mm plate; up to next face. | Drill Ø4.2 mm (= d − P = 5 − 0.8); cosmetic thread M5×0.8; thread depth 2×d=10 mm. | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0111 | M5 clearance (medium), blind 2×d | Functional | P2 | Place hole M5 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø5.5 mm (ISO 273 medium). | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0112 | M5 clearance (medium), through all | Functional | P2 | Place hole M5 clearance (medium) on a 60 mm plate; through all. | Hole Ø5.5 mm (ISO 273 medium). | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0113 | M5 clearance (medium), up to next face | Functional | P2 | Place hole M5 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø5.5 mm (ISO 273 medium). | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0114 | M5 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M5 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø5.5 mm; counterbore Ø ≥ 8.5 mm (head dk) and depth ≥ 5 mm (head k). | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0115 | M5 counterbored for ISO 4762, through all | Functional | P2 | Place hole M5 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø5.5 mm; counterbore Ø ≥ 8.5 mm (head dk) and depth ≥ 5 mm (head k). | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0116 | M5 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M5 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø5.5 mm; counterbore Ø ≥ 8.5 mm (head dk) and depth ≥ 5 mm (head k). | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0117 | M5 countersunk for ISO 10642, blind 2×d | Functional | P2 | Place hole M5 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø5.5 mm; 90° countersink to Ø11.2 mm. | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0118 | M5 countersunk for ISO 10642, through all | Functional | P2 | Place hole M5 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø5.5 mm; 90° countersink to Ø11.2 mm. | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0119 | M5 countersunk for ISO 10642, up to next face | Functional | P2 | Place hole M5 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø5.5 mm; 90° countersink to Ø11.2 mm. | M5: P=0.8; ISO 261 / 273 / 4762 / 10642 |
| PRT-0120 | M6 tapped, blind 2×d | Functional | P1 | Place hole M6 tapped on a 60 mm plate; blind 2×d. | Drill Ø5.0 mm (= d − P = 6 − 1.0); cosmetic thread M6×1.0; thread depth 2×d=12 mm. | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0121 | M6 tapped, through all | Functional | P1 | Place hole M6 tapped on a 60 mm plate; through all. | Drill Ø5.0 mm (= d − P = 6 − 1.0); cosmetic thread M6×1.0; thread depth 2×d=12 mm. | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0122 | M6 tapped, up to next face | Functional | P1 | Place hole M6 tapped on a 60 mm plate; up to next face. | Drill Ø5.0 mm (= d − P = 6 − 1.0); cosmetic thread M6×1.0; thread depth 2×d=12 mm. | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0123 | M6 clearance (medium), blind 2×d | Functional | P1 | Place hole M6 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø6.6 mm (ISO 273 medium). | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0124 | M6 clearance (medium), through all | Functional | P1 | Place hole M6 clearance (medium) on a 60 mm plate; through all. | Hole Ø6.6 mm (ISO 273 medium). | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0125 | M6 clearance (medium), up to next face | Functional | P1 | Place hole M6 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø6.6 mm (ISO 273 medium). | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0126 | M6 counterbored for ISO 4762, blind 2×d | Functional | P1 | Place hole M6 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø6.6 mm; counterbore Ø ≥ 10.0 mm (head dk) and depth ≥ 6 mm (head k). | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0127 | M6 counterbored for ISO 4762, through all | Functional | P1 | Place hole M6 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø6.6 mm; counterbore Ø ≥ 10.0 mm (head dk) and depth ≥ 6 mm (head k). | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0128 | M6 counterbored for ISO 4762, up to next face | Functional | P1 | Place hole M6 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø6.6 mm; counterbore Ø ≥ 10.0 mm (head dk) and depth ≥ 6 mm (head k). | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0129 | M6 countersunk for ISO 10642, blind 2×d | Functional | P1 | Place hole M6 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø6.6 mm; 90° countersink to Ø13.44 mm. | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0130 | M6 countersunk for ISO 10642, through all | Functional | P1 | Place hole M6 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø6.6 mm; 90° countersink to Ø13.44 mm. | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0131 | M6 countersunk for ISO 10642, up to next face | Functional | P1 | Place hole M6 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø6.6 mm; 90° countersink to Ø13.44 mm. | M6: P=1.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0132 | M8 tapped, blind 2×d | Functional | P1 | Place hole M8 tapped on a 60 mm plate; blind 2×d. | Drill Ø6.8 mm (= d − P = 8 − 1.25); cosmetic thread M8×1.25; thread depth 2×d=16 mm. | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0133 | M8 tapped, through all | Functional | P1 | Place hole M8 tapped on a 60 mm plate; through all. | Drill Ø6.8 mm (= d − P = 8 − 1.25); cosmetic thread M8×1.25; thread depth 2×d=16 mm. | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0134 | M8 tapped, up to next face | Functional | P1 | Place hole M8 tapped on a 60 mm plate; up to next face. | Drill Ø6.8 mm (= d − P = 8 − 1.25); cosmetic thread M8×1.25; thread depth 2×d=16 mm. | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0135 | M8 clearance (medium), blind 2×d | Functional | P1 | Place hole M8 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø9.0 mm (ISO 273 medium). | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0136 | M8 clearance (medium), through all | Functional | P1 | Place hole M8 clearance (medium) on a 60 mm plate; through all. | Hole Ø9.0 mm (ISO 273 medium). | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0137 | M8 clearance (medium), up to next face | Functional | P1 | Place hole M8 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø9.0 mm (ISO 273 medium). | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0138 | M8 counterbored for ISO 4762, blind 2×d | Functional | P1 | Place hole M8 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø9.0 mm; counterbore Ø ≥ 13.0 mm (head dk) and depth ≥ 8 mm (head k). | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0139 | M8 counterbored for ISO 4762, through all | Functional | P1 | Place hole M8 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø9.0 mm; counterbore Ø ≥ 13.0 mm (head dk) and depth ≥ 8 mm (head k). | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0140 | M8 counterbored for ISO 4762, up to next face | Functional | P1 | Place hole M8 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø9.0 mm; counterbore Ø ≥ 13.0 mm (head dk) and depth ≥ 8 mm (head k). | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0141 | M8 countersunk for ISO 10642, blind 2×d | Functional | P1 | Place hole M8 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø9.0 mm; 90° countersink to Ø17.92 mm. | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0142 | M8 countersunk for ISO 10642, through all | Functional | P1 | Place hole M8 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø9.0 mm; 90° countersink to Ø17.92 mm. | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0143 | M8 countersunk for ISO 10642, up to next face | Functional | P1 | Place hole M8 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø9.0 mm; 90° countersink to Ø17.92 mm. | M8: P=1.25; ISO 261 / 273 / 4762 / 10642 |
| PRT-0144 | M10 tapped, blind 2×d | Functional | P1 | Place hole M10 tapped on a 60 mm plate; blind 2×d. | Drill Ø8.5 mm (= d − P = 10 − 1.5); cosmetic thread M10×1.5; thread depth 2×d=20 mm. | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0145 | M10 tapped, through all | Functional | P1 | Place hole M10 tapped on a 60 mm plate; through all. | Drill Ø8.5 mm (= d − P = 10 − 1.5); cosmetic thread M10×1.5; thread depth 2×d=20 mm. | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0146 | M10 tapped, up to next face | Functional | P1 | Place hole M10 tapped on a 60 mm plate; up to next face. | Drill Ø8.5 mm (= d − P = 10 − 1.5); cosmetic thread M10×1.5; thread depth 2×d=20 mm. | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0147 | M10 clearance (medium), blind 2×d | Functional | P1 | Place hole M10 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø11.0 mm (ISO 273 medium). | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0148 | M10 clearance (medium), through all | Functional | P1 | Place hole M10 clearance (medium) on a 60 mm plate; through all. | Hole Ø11.0 mm (ISO 273 medium). | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0149 | M10 clearance (medium), up to next face | Functional | P1 | Place hole M10 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø11.0 mm (ISO 273 medium). | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0150 | M10 counterbored for ISO 4762, blind 2×d | Functional | P1 | Place hole M10 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø11.0 mm; counterbore Ø ≥ 16.0 mm (head dk) and depth ≥ 10 mm (head k). | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0151 | M10 counterbored for ISO 4762, through all | Functional | P1 | Place hole M10 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø11.0 mm; counterbore Ø ≥ 16.0 mm (head dk) and depth ≥ 10 mm (head k). | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0152 | M10 counterbored for ISO 4762, up to next face | Functional | P1 | Place hole M10 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø11.0 mm; counterbore Ø ≥ 16.0 mm (head dk) and depth ≥ 10 mm (head k). | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0153 | M10 countersunk for ISO 10642, blind 2×d | Functional | P1 | Place hole M10 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø11.0 mm; 90° countersink to Ø22.4 mm. | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0154 | M10 countersunk for ISO 10642, through all | Functional | P1 | Place hole M10 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø11.0 mm; 90° countersink to Ø22.4 mm. | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0155 | M10 countersunk for ISO 10642, up to next face | Functional | P1 | Place hole M10 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø11.0 mm; 90° countersink to Ø22.4 mm. | M10: P=1.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0156 | M12 tapped, blind 2×d | Functional | P2 | Place hole M12 tapped on a 60 mm plate; blind 2×d. | Drill Ø10.2 mm (= d − P = 12 − 1.75); cosmetic thread M12×1.75; thread depth 2×d=24 mm. | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0157 | M12 tapped, through all | Functional | P2 | Place hole M12 tapped on a 60 mm plate; through all. | Drill Ø10.2 mm (= d − P = 12 − 1.75); cosmetic thread M12×1.75; thread depth 2×d=24 mm. | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0158 | M12 tapped, up to next face | Functional | P2 | Place hole M12 tapped on a 60 mm plate; up to next face. | Drill Ø10.2 mm (= d − P = 12 − 1.75); cosmetic thread M12×1.75; thread depth 2×d=24 mm. | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0159 | M12 clearance (medium), blind 2×d | Functional | P2 | Place hole M12 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø13.5 mm (ISO 273 medium). | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0160 | M12 clearance (medium), through all | Functional | P2 | Place hole M12 clearance (medium) on a 60 mm plate; through all. | Hole Ø13.5 mm (ISO 273 medium). | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0161 | M12 clearance (medium), up to next face | Functional | P2 | Place hole M12 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø13.5 mm (ISO 273 medium). | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0162 | M12 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M12 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø13.5 mm; counterbore Ø ≥ 18.0 mm (head dk) and depth ≥ 12 mm (head k). | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0163 | M12 counterbored for ISO 4762, through all | Functional | P2 | Place hole M12 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø13.5 mm; counterbore Ø ≥ 18.0 mm (head dk) and depth ≥ 12 mm (head k). | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0164 | M12 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M12 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø13.5 mm; counterbore Ø ≥ 18.0 mm (head dk) and depth ≥ 12 mm (head k). | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0165 | M12 countersunk for ISO 10642, blind 2×d | Functional | P2 | Place hole M12 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø13.5 mm; 90° countersink to Ø26.88 mm. | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0166 | M12 countersunk for ISO 10642, through all | Functional | P2 | Place hole M12 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø13.5 mm; 90° countersink to Ø26.88 mm. | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0167 | M12 countersunk for ISO 10642, up to next face | Functional | P2 | Place hole M12 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø13.5 mm; 90° countersink to Ø26.88 mm. | M12: P=1.75; ISO 261 / 273 / 4762 / 10642 |
| PRT-0168 | M16 tapped, blind 2×d | Functional | P2 | Place hole M16 tapped on a 60 mm plate; blind 2×d. | Drill Ø14.0 mm (= d − P = 16 − 2.0); cosmetic thread M16×2.0; thread depth 2×d=32 mm. | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0169 | M16 tapped, through all | Functional | P2 | Place hole M16 tapped on a 60 mm plate; through all. | Drill Ø14.0 mm (= d − P = 16 − 2.0); cosmetic thread M16×2.0; thread depth 2×d=32 mm. | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0170 | M16 tapped, up to next face | Functional | P2 | Place hole M16 tapped on a 60 mm plate; up to next face. | Drill Ø14.0 mm (= d − P = 16 − 2.0); cosmetic thread M16×2.0; thread depth 2×d=32 mm. | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0171 | M16 clearance (medium), blind 2×d | Functional | P2 | Place hole M16 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø17.5 mm (ISO 273 medium). | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0172 | M16 clearance (medium), through all | Functional | P2 | Place hole M16 clearance (medium) on a 60 mm plate; through all. | Hole Ø17.5 mm (ISO 273 medium). | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0173 | M16 clearance (medium), up to next face | Functional | P2 | Place hole M16 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø17.5 mm (ISO 273 medium). | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0174 | M16 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M16 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø17.5 mm; counterbore Ø ≥ 24.0 mm (head dk) and depth ≥ 16 mm (head k). | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0175 | M16 counterbored for ISO 4762, through all | Functional | P2 | Place hole M16 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø17.5 mm; counterbore Ø ≥ 24.0 mm (head dk) and depth ≥ 16 mm (head k). | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0176 | M16 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M16 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø17.5 mm; counterbore Ø ≥ 24.0 mm (head dk) and depth ≥ 16 mm (head k). | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0177 | M16 countersunk for ISO 10642, blind 2×d | Functional | P2 | Place hole M16 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø17.5 mm; 90° countersink to Ø33.6 mm. | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0178 | M16 countersunk for ISO 10642, through all | Functional | P2 | Place hole M16 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø17.5 mm; 90° countersink to Ø33.6 mm. | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0179 | M16 countersunk for ISO 10642, up to next face | Functional | P2 | Place hole M16 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø17.5 mm; 90° countersink to Ø33.6 mm. | M16: P=2.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0180 | M20 tapped, blind 2×d | Functional | P2 | Place hole M20 tapped on a 60 mm plate; blind 2×d. | Drill Ø17.5 mm (= d − P = 20 − 2.5); cosmetic thread M20×2.5; thread depth 2×d=40 mm. | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0181 | M20 tapped, through all | Functional | P2 | Place hole M20 tapped on a 60 mm plate; through all. | Drill Ø17.5 mm (= d − P = 20 − 2.5); cosmetic thread M20×2.5; thread depth 2×d=40 mm. | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0182 | M20 tapped, up to next face | Functional | P2 | Place hole M20 tapped on a 60 mm plate; up to next face. | Drill Ø17.5 mm (= d − P = 20 − 2.5); cosmetic thread M20×2.5; thread depth 2×d=40 mm. | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0183 | M20 clearance (medium), blind 2×d | Functional | P2 | Place hole M20 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø22.0 mm (ISO 273 medium). | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0184 | M20 clearance (medium), through all | Functional | P2 | Place hole M20 clearance (medium) on a 60 mm plate; through all. | Hole Ø22.0 mm (ISO 273 medium). | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0185 | M20 clearance (medium), up to next face | Functional | P2 | Place hole M20 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø22.0 mm (ISO 273 medium). | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0186 | M20 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M20 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø22.0 mm; counterbore Ø ≥ 30.0 mm (head dk) and depth ≥ 20 mm (head k). | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0187 | M20 counterbored for ISO 4762, through all | Functional | P2 | Place hole M20 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø22.0 mm; counterbore Ø ≥ 30.0 mm (head dk) and depth ≥ 20 mm (head k). | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0188 | M20 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M20 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø22.0 mm; counterbore Ø ≥ 30.0 mm (head dk) and depth ≥ 20 mm (head k). | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0189 | M20 countersunk for ISO 10642, blind 2×d | Functional | P2 | Place hole M20 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Hole Ø22.0 mm; 90° countersink to Ø40.32 mm. | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0190 | M20 countersunk for ISO 10642, through all | Functional | P2 | Place hole M20 countersunk for ISO 10642 on a 60 mm plate; through all. | Hole Ø22.0 mm; 90° countersink to Ø40.32 mm. | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0191 | M20 countersunk for ISO 10642, up to next face | Functional | P2 | Place hole M20 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Hole Ø22.0 mm; 90° countersink to Ø40.32 mm. | M20: P=2.5; ISO 261 / 273 / 4762 / 10642 |
| PRT-0192 | M24 tapped, blind 2×d | Functional | P2 | Place hole M24 tapped on a 60 mm plate; blind 2×d. | Drill Ø21.0 mm (= d − P = 24 − 3.0); cosmetic thread M24×3.0; thread depth 2×d=48 mm. | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0193 | M24 tapped, through all | Functional | P2 | Place hole M24 tapped on a 60 mm plate; through all. | Drill Ø21.0 mm (= d − P = 24 − 3.0); cosmetic thread M24×3.0; thread depth 2×d=48 mm. | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0194 | M24 tapped, up to next face | Functional | P2 | Place hole M24 tapped on a 60 mm plate; up to next face. | Drill Ø21.0 mm (= d − P = 24 − 3.0); cosmetic thread M24×3.0; thread depth 2×d=48 mm. | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0195 | M24 clearance (medium), blind 2×d | Functional | P2 | Place hole M24 clearance (medium) on a 60 mm plate; blind 2×d. | Hole Ø26.0 mm (ISO 273 medium). | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0196 | M24 clearance (medium), through all | Functional | P2 | Place hole M24 clearance (medium) on a 60 mm plate; through all. | Hole Ø26.0 mm (ISO 273 medium). | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0197 | M24 clearance (medium), up to next face | Functional | P2 | Place hole M24 clearance (medium) on a 60 mm plate; up to next face. | Hole Ø26.0 mm (ISO 273 medium). | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0198 | M24 counterbored for ISO 4762, blind 2×d | Functional | P2 | Place hole M24 counterbored for ISO 4762 on a 60 mm plate; blind 2×d. | Hole Ø26.0 mm; counterbore Ø ≥ 36.0 mm (head dk) and depth ≥ 24 mm (head k). | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0199 | M24 counterbored for ISO 4762, through all | Functional | P2 | Place hole M24 counterbored for ISO 4762 on a 60 mm plate; through all. | Hole Ø26.0 mm; counterbore Ø ≥ 36.0 mm (head dk) and depth ≥ 24 mm (head k). | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0200 | M24 counterbored for ISO 4762, up to next face | Functional | P2 | Place hole M24 counterbored for ISO 4762 on a 60 mm plate; up to next face. | Hole Ø26.0 mm; counterbore Ø ≥ 36.0 mm (head dk) and depth ≥ 24 mm (head k). | M24: P=3.0; ISO 261 / 273 / 4762 / 10642 |
| PRT-0201 | M24 countersunk for ISO 10642, blind 2×d | Negative | P2 | Place hole M24 countersunk for ISO 10642 on a 60 mm plate; blind 2×d. | Not offered: ISO 10642 has no M24 size (message). |  |
| PRT-0202 | M24 countersunk for ISO 10642, through all | Negative | P2 | Place hole M24 countersunk for ISO 10642 on a 60 mm plate; through all. | Not offered: ISO 10642 has no M24 size (message). |  |
| PRT-0203 | M24 countersunk for ISO 10642, up to next face | Negative | P2 | Place hole M24 countersunk for ISO 10642 on a 60 mm plate; up to next face. | Not offered: ISO 10642 has no M24 size (message). |  |

## Fillet

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0204 | Constant fillet r=0.01 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 0.00107301 mm³. | r=0.01, L=50.0 |
| PRT-0205 | Constant fillet r=0.5 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 2.68252 mm³. | r=0.5, L=50.0 |
| PRT-0206 | Constant fillet r=1 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 10.7301 mm³. | r=1, L=50.0 |
| PRT-0207 | Constant fillet r=2 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 42.9204 mm³. | r=2, L=50.0 |
| PRT-0208 | Constant fillet r=5 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 268.252 mm³. | r=5, L=50.0 |
| PRT-0209 | Constant fillet r=8 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 686.726 mm³. | r=8, L=50.0 |
| PRT-0210 | Constant fillet r=9.99 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 1070.86 mm³. | r=9.99, L=50.0 |
| PRT-0211 | Constant fillet r=10 on a 10 mm plate edge | Accuracy | P1 | Block 50×40×10; fillet the 50 mm top edge. | Volume drops by (1−π/4)·r²·L = 1073.01 mm³. | r=10, L=50.0 |
| PRT-0212 | Constant fillet r=10.01 on a 10 mm plate edge | Negative | P1 | Block 50×40×10; fillet the 50 mm top edge. | Fillet fails cleanly: radius exceeds the 10 mm adjacent face; tree shows the error; no crash. | r=10.01, L=50.0 |
| PRT-0213 | Constant fillet r=15 on a 10 mm plate edge | Negative | P1 | Block 50×40×10; fillet the 50 mm top edge. | Fillet fails cleanly: radius exceeds the 10 mm adjacent face; tree shows the error; no crash. | r=15, L=50.0 |
| PRT-0214 | Fillet: variable radius 2→6 | Functional | P2 | Apply variable radius 2→6 on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0215 | Fillet: face-face | Functional | P2 | Apply face-face on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0216 | Fillet: tritangent | Functional | P2 | Apply tritangent on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0217 | Fillet: edge chain (tangent propagation) | Functional | P2 | Apply edge chain (tangent propagation) on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0218 | Fillet: all edges of a box | Functional | P2 | Apply all edges of a box on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0219 | Fillet: fillet across a boolean seam | Functional | P2 | Apply fillet across a boolean seam on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0220 | Fillet: fillet a revolve seam | Functional | P2 | Apply fillet a revolve seam on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0221 | Fillet: fillet on a sheet-metal bend | Functional | P2 | Apply fillet on a sheet-metal bend on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0222 | Fillet: fillet after shell | Functional | P2 | Apply fillet after shell on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |
| PRT-0223 | Fillet: setback vertex blend | Functional | P2 | Apply setback vertex blend on a representative part. | Valid solid; G1 across the fillet boundaries (angle < 0.01°); rebuild stable after a parameter edit. |  |

## Chamfer

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0224 | Chamfer 0.5×0.5 on a 10 mm plate edge | Accuracy | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Volume drops by ½·d1·d2·L = 6.25 mm³. |  |
| PRT-0225 | Chamfer 1×1 on a 10 mm plate edge | Accuracy | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Volume drops by ½·d1·d2·L = 25 mm³. |  |
| PRT-0226 | Chamfer 2×2 on a 10 mm plate edge | Accuracy | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Volume drops by ½·d1·d2·L = 100 mm³. |  |
| PRT-0227 | Chamfer 3×1 on a 10 mm plate edge | Accuracy | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Volume drops by ½·d1·d2·L = 75 mm³. |  |
| PRT-0228 | Chamfer 5×5 on a 10 mm plate edge | Accuracy | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Volume drops by ½·d1·d2·L = 625 mm³. |  |
| PRT-0229 | Chamfer 10×10 on a 10 mm plate edge | Accuracy | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Volume drops by ½·d1·d2·L = 2500 mm³. |  |
| PRT-0230 | Chamfer 11×1 on a 10 mm plate edge | Negative | P2 | Block 50×40×10; chamfer the 50 mm top edge. | Rejected: chamfer leg exceeds the face. |  |

## Shell

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0231 | Shell box 100×60×40, t=0.5, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 9280.5 mm³. | t=0.5 |
| PRT-0232 | Shell box 100×60×40, t=1, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 18324 mm³. | t=1 |
| PRT-0233 | Shell box 100×60×40, t=2, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 35712 mm³. | t=2 |
| PRT-0234 | Shell box 100×60×40, t=5, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 82500 mm³. | t=5 |
| PRT-0235 | Shell box 100×60×40, t=10, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 144000 mm³. | t=10 |
| PRT-0236 | Shell box 100×60×40, t=19.9, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 215558 mm³. | t=19.9 |
| PRT-0237 | Shell box 100×60×40, t=29.9, top face removed | Accuracy | P2 | Shell inward with the top face open. | Volume = 240000 − (100−2t)(60−2t)(40−t) = 239919 mm³. | t=29.9 |
| PRT-0238 | Shell box 100×60×40, t=30, top face removed | Negative | P2 | Shell inward with the top face open. | Shell fails: walls meet (2t ≥ 60); error names the thickness. | t=30 |
| PRT-0239 | Shell box 100×60×40, t=40, top face removed | Negative | P2 | Shell inward with the top face open. | Shell fails: walls meet (2t ≥ 60); error names the thickness. | t=40 |

## Draft

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0240 | Draft -3° on 4 side faces | Boundary | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Rejected: draft angle must be in (0°, 90°). |  |
| PRT-0241 | Draft 0° on 4 side faces | Boundary | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Rejected: draft angle must be in (0°, 90°). |  |
| PRT-0242 | Draft 0.5° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 0.5°; top face shrinks by 2·40·tan(0.5°) = 0.69815 mm per side pair. |  |
| PRT-0243 | Draft 1° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 1°; top face shrinks by 2·40·tan(1°) = 1.3964 mm per side pair. |  |
| PRT-0244 | Draft 2° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 2°; top face shrinks by 2·40·tan(2°) = 2.7937 mm per side pair. |  |
| PRT-0245 | Draft 3° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 3°; top face shrinks by 2·40·tan(3°) = 4.1926 mm per side pair. |  |
| PRT-0246 | Draft 5° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 5°; top face shrinks by 2·40·tan(5°) = 6.9991 mm per side pair. |  |
| PRT-0247 | Draft 10° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 10°; top face shrinks by 2·40·tan(10°) = 14.106 mm per side pair. |  |
| PRT-0248 | Draft 45° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 45°; top face shrinks by 2·40·tan(45°) = 80 mm per side pair. |  |
| PRT-0249 | Draft 89° on 4 side faces | Accuracy | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Side faces inclined 89°; top face shrinks by 2·40·tan(89°) = 4583.2 mm per side pair. |  |
| PRT-0250 | Draft 90° on 4 side faces | Boundary | P2 | Block 100×60×40; neutral plane = base; pull Z+. | Rejected: draft angle must be in (0°, 90°). |  |

## Booleans

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0251 | Union of two 100 mm cubes offset (0,0,0) | Accuracy | P2 | Create two cubes; union. | Volume 1000000 mm³ | overlap 1000000 mm³ |
| PRT-0252 | Subtract of two 100 mm cubes offset (0,0,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 0 mm³ | overlap 1000000 mm³ |
| PRT-0253 | Intersect of two 100 mm cubes offset (0,0,0) | Accuracy | P2 | Create two cubes; intersect. | Volume 1000000 mm³ | overlap 1000000 mm³ |
| PRT-0254 | Union of two 100 mm cubes offset (50,0,0) | Accuracy | P1 | Create two cubes; union. | Volume 1500000 mm³ | overlap 500000 mm³ |
| PRT-0255 | Subtract of two 100 mm cubes offset (50,0,0) | Accuracy | P1 | Create two cubes; subtract. | Volume 500000 mm³ | overlap 500000 mm³ |
| PRT-0256 | Intersect of two 100 mm cubes offset (50,0,0) | Accuracy | P1 | Create two cubes; intersect. | Volume 500000 mm³ | overlap 500000 mm³ |
| PRT-0257 | Union of two 100 mm cubes offset (50,50,0) | Accuracy | P2 | Create two cubes; union. | Volume 1750000 mm³ | overlap 250000 mm³ |
| PRT-0258 | Subtract of two 100 mm cubes offset (50,50,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 750000 mm³ | overlap 250000 mm³ |
| PRT-0259 | Intersect of two 100 mm cubes offset (50,50,0) | Accuracy | P2 | Create two cubes; intersect. | Volume 250000 mm³ | overlap 250000 mm³ |
| PRT-0260 | Union of two 100 mm cubes offset (50,50,50) | Accuracy | P2 | Create two cubes; union. | Volume 1875000 mm³ | overlap 125000 mm³ |
| PRT-0261 | Subtract of two 100 mm cubes offset (50,50,50) | Accuracy | P2 | Create two cubes; subtract. | Volume 875000 mm³ | overlap 125000 mm³ |
| PRT-0262 | Intersect of two 100 mm cubes offset (50,50,50) | Accuracy | P2 | Create two cubes; intersect. | Volume 125000 mm³ | overlap 125000 mm³ |
| PRT-0263 | Union of two 100 mm cubes offset (99,0,0) | Accuracy | P2 | Create two cubes; union. | Volume 1990000 mm³ | overlap 10000 mm³ |
| PRT-0264 | Subtract of two 100 mm cubes offset (99,0,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 990000 mm³ | overlap 10000 mm³ |
| PRT-0265 | Intersect of two 100 mm cubes offset (99,0,0) | Accuracy | P2 | Create two cubes; intersect. | Volume 10000 mm³ | overlap 10000 mm³ |
| PRT-0266 | Union of two 100 mm cubes offset (99.999,0,0) | Accuracy | P2 | Create two cubes; union. | Volume 1999990 mm³ | overlap 10 mm³ |
| PRT-0267 | Subtract of two 100 mm cubes offset (99.999,0,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 999990 mm³ | overlap 10 mm³ |
| PRT-0268 | Intersect of two 100 mm cubes offset (99.999,0,0) | Accuracy | P2 | Create two cubes; intersect. | Volume 10 mm³ | overlap 10 mm³ |
| PRT-0269 | Union of two 100 mm cubes offset (100,0,0) | Accuracy | P2 | Create two cubes; union. | Volume 2000000 mm³ | overlap 0 mm³ |
| PRT-0270 | Subtract of two 100 mm cubes offset (100,0,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 1000000 mm³ | overlap 0 mm³ |
| PRT-0271 | Intersect of two 100 mm cubes offset (100,0,0) | Accuracy | P2 | Create two cubes; intersect. | Empty result reported as a warning, not a crash | overlap 0 mm³ |
| PRT-0272 | Union of two 100 mm cubes offset (100,100,0) | Accuracy | P2 | Create two cubes; union. | Volume 2000000 mm³ | overlap 0 mm³ |
| PRT-0273 | Subtract of two 100 mm cubes offset (100,100,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 1000000 mm³ | overlap 0 mm³ |
| PRT-0274 | Intersect of two 100 mm cubes offset (100,100,0) | Accuracy | P2 | Create two cubes; intersect. | Empty result reported as a warning, not a crash | overlap 0 mm³ |
| PRT-0275 | Union of two 100 mm cubes offset (150,0,0) | Accuracy | P2 | Create two cubes; union. | Volume 2000000 mm³; two lumps (disjoint) | overlap 0 mm³ |
| PRT-0276 | Subtract of two 100 mm cubes offset (150,0,0) | Accuracy | P2 | Create two cubes; subtract. | Volume 1000000 mm³ | overlap 0 mm³ |
| PRT-0277 | Intersect of two 100 mm cubes offset (150,0,0) | Accuracy | P2 | Create two cubes; intersect. | Empty result reported as a warning, not a crash | overlap 0 mm³ |
| PRT-0278 | Union of two 100 mm cubes offset (25,75,10) | Accuracy | P2 | Create two cubes; union. | Volume 1831250 mm³ | overlap 168750 mm³ |
| PRT-0279 | Subtract of two 100 mm cubes offset (25,75,10) | Accuracy | P2 | Create two cubes; subtract. | Volume 831250 mm³ | overlap 168750 mm³ |
| PRT-0280 | Intersect of two 100 mm cubes offset (25,75,10) | Accuracy | P2 | Create two cubes; intersect. | Volume 168750 mm³ | overlap 168750 mm³ |

## Patterns and mirror

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0281 | Rectangular pattern 1×1 of a Ø5 hole | Accuracy | P2 | Plate 300×300×5; pattern with 20 mm pitch. | 1 holes; volume drops by 1×π·2.5²·5 = 98.1748 mm³. |  |
| PRT-0282 | Rectangular pattern 2×1 of a Ø5 hole | Accuracy | P2 | Plate 300×300×5; pattern with 20 mm pitch. | 2 holes; volume drops by 2×π·2.5²·5 = 196.35 mm³. |  |
| PRT-0283 | Rectangular pattern 3×3 of a Ø5 hole | Accuracy | P2 | Plate 300×300×5; pattern with 20 mm pitch. | 9 holes; volume drops by 9×π·2.5²·5 = 883.573 mm³. |  |
| PRT-0284 | Rectangular pattern 5×2 of a Ø5 hole | Accuracy | P2 | Plate 300×300×5; pattern with 20 mm pitch. | 10 holes; volume drops by 10×π·2.5²·5 = 981.748 mm³. |  |
| PRT-0285 | Rectangular pattern 10×10 of a Ø5 hole | Accuracy | P2 | Plate 300×300×5; pattern with 20 mm pitch. | 100 holes; volume drops by 100×π·2.5²·5 = 9817.48 mm³. |  |
| PRT-0286 | Rectangular pattern 50×1 of a Ø5 hole | Accuracy | P2 | Plate 300×300×5; pattern with 20 mm pitch. | 50 holes; volume drops by 50×π·2.5²·5 = 4908.74 mm³. |  |
| PRT-0287 | Rectangular pattern 0×3 of a Ø5 hole | Negative | P2 | Plate 300×300×5; pattern with 20 mm pitch. | Rejected: instance count must be ≥ 1. |  |
| PRT-0288 | Circular pattern 2 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 2 instances; angular pitch 180°; no duplicate at 0/360. |  |
| PRT-0289 | Circular pattern 3 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 3 instances; angular pitch 120°; no duplicate at 0/360. |  |
| PRT-0290 | Circular pattern 6 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 6 instances; angular pitch 60°; no duplicate at 0/360. |  |
| PRT-0291 | Circular pattern 8 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 8 instances; angular pitch 45°; no duplicate at 0/360. |  |
| PRT-0292 | Circular pattern 12 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 12 instances; angular pitch 30°; no duplicate at 0/360. |  |
| PRT-0293 | Circular pattern 4 over 90° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 4 instances; angular pitch 30°; no duplicate at 0/360. |  |
| PRT-0294 | Circular pattern 5 over 180° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 5 instances; angular pitch 45°; no duplicate at 0/360. |  |
| PRT-0295 | Circular pattern 36 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 36 instances; angular pitch 10°; no duplicate at 0/360. |  |
| PRT-0296 | Circular pattern 1 over 360° | Functional | P2 | Boss Ø5 on a disc; pattern about Z. | 1 instances; angular pitch 360°; no duplicate at 0/360. |  |
| PRT-0297 | Pattern/mirror: mirror a pad about YZ | Functional | P2 | Apply: mirror a pad about YZ. | Expected instance count and positions; symmetric volume. |  |
| PRT-0298 | Pattern/mirror: mirror the whole body | Functional | P2 | Apply: mirror the whole body. | Expected instance count and positions; symmetric volume. |  |
| PRT-0299 | Pattern/mirror: mirror a pattern | Functional | P2 | Apply: mirror a pattern. | Expected instance count and positions; symmetric volume. |  |
| PRT-0300 | Pattern/mirror: pattern of a pattern | Functional | P2 | Apply: pattern of a pattern. | Expected instance count and positions; symmetric volume. |  |
| PRT-0301 | Pattern/mirror: pattern instance overlapping the edge (skip instance) | Functional | P2 | Apply: pattern instance overlapping the edge (skip instance). | Expected instance count and positions; symmetric volume. |  |
| PRT-0302 | Pattern/mirror: pattern driven by a parameter | Functional | P2 | Apply: pattern driven by a parameter. | Expected instance count and positions; symmetric volume. |  |

## Feature tree management

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0303 | Tree: reorder a fillet above the pad it uses (bracket) | Regression | P2 | On the bracket preset: reorder a fillet above the pad it uses. | Rejected: dependency would break. |  |
| PRT-0304 | Tree: reorder a fillet above the pad it uses (flange) | Regression | P2 | On the flange preset: reorder a fillet above the pad it uses. | Rejected: dependency would break. |  |
| PRT-0305 | Tree: reorder a fillet above the pad it uses (housing) | Regression | P2 | On the housing preset: reorder a fillet above the pad it uses. | Rejected: dependency would break. |  |
| PRT-0306 | Tree: reorder two independent pads (bracket) | Regression | P2 | On the bracket preset: reorder two independent pads. | Accepted; same final volume. |  |
| PRT-0307 | Tree: reorder two independent pads (flange) | Regression | P2 | On the flange preset: reorder two independent pads. | Accepted; same final volume. |  |
| PRT-0308 | Tree: reorder two independent pads (housing) | Regression | P2 | On the housing preset: reorder two independent pads. | Accepted; same final volume. |  |
| PRT-0309 | Tree: suppress a pocket (bracket) | Regression | P2 | On the bracket preset: suppress a pocket. | Pocket and its dependents greyed; volume restored. |  |
| PRT-0310 | Tree: suppress a pocket (flange) | Regression | P2 | On the flange preset: suppress a pocket. | Pocket and its dependents greyed; volume restored. |  |
| PRT-0311 | Tree: suppress a pocket (housing) | Regression | P2 | On the housing preset: suppress a pocket. | Pocket and its dependents greyed; volume restored. |  |
| PRT-0312 | Tree: delete a sketch used by a pad (bracket) | Regression | P2 | On the bracket preset: delete a sketch used by a pad. | Asks to delete dependents or cancel. |  |
| PRT-0313 | Tree: delete a sketch used by a pad (flange) | Regression | P2 | On the flange preset: delete a sketch used by a pad. | Asks to delete dependents or cancel. |  |
| PRT-0314 | Tree: delete a sketch used by a pad (housing) | Regression | P2 | On the housing preset: delete a sketch used by a pad. | Asks to delete dependents or cancel. |  |
| PRT-0315 | Tree: rename a feature (bracket) | Regression | P2 | On the bracket preset: rename a feature. | Name persists after save/reload; references kept. |  |
| PRT-0316 | Tree: rename a feature (flange) | Regression | P2 | On the flange preset: rename a feature. | Name persists after save/reload; references kept. |  |
| PRT-0317 | Tree: rename a feature (housing) | Regression | P2 | On the housing preset: rename a feature. | Name persists after save/reload; references kept. |  |
| PRT-0318 | Tree: edit an upstream sketch dimension (bracket) | Regression | P2 | On the bracket preset: edit an upstream sketch dimension. | Downstream features rebuild; failures flagged, not hidden. |  |
| PRT-0319 | Tree: edit an upstream sketch dimension (flange) | Regression | P2 | On the flange preset: edit an upstream sketch dimension. | Downstream features rebuild; failures flagged, not hidden. |  |
| PRT-0320 | Tree: edit an upstream sketch dimension (housing) | Regression | P2 | On the housing preset: edit an upstream sketch dimension. | Downstream features rebuild; failures flagged, not hidden. |  |
| PRT-0321 | Tree: insert a feature mid-tree (bracket) | Regression | P2 | On the bracket preset: insert a feature mid-tree. | Rebuild from that point only. |  |
| PRT-0322 | Tree: insert a feature mid-tree (flange) | Regression | P2 | On the flange preset: insert a feature mid-tree. | Rebuild from that point only. |  |
| PRT-0323 | Tree: insert a feature mid-tree (housing) | Regression | P2 | On the housing preset: insert a feature mid-tree. | Rebuild from that point only. |  |
| PRT-0324 | Tree: undo 20 times then redo 20 times (bracket) | Regression | P2 | On the bracket preset: undo 20 times then redo 20 times. | Exact same B-rep hash at the end. |  |
| PRT-0325 | Tree: undo 20 times then redo 20 times (flange) | Regression | P2 | On the flange preset: undo 20 times then redo 20 times. | Exact same B-rep hash at the end. |  |
| PRT-0326 | Tree: undo 20 times then redo 20 times (housing) | Regression | P2 | On the housing preset: undo 20 times then redo 20 times. | Exact same B-rep hash at the end. |  |
| PRT-0327 | Tree: rollback bar to feature 3 (bracket) | Regression | P2 | On the bracket preset: rollback bar to feature 3. | Model shows state after feature 3. |  |
| PRT-0328 | Tree: rollback bar to feature 3 (flange) | Regression | P2 | On the flange preset: rollback bar to feature 3. | Model shows state after feature 3. |  |
| PRT-0329 | Tree: rollback bar to feature 3 (housing) | Regression | P2 | On the housing preset: rollback bar to feature 3. | Model shows state after feature 3. |  |
| PRT-0330 | Tree: copy/paste a feature to another part (bracket) | Regression | P2 | On the bracket preset: copy/paste a feature to another part. | References re-mapped or flagged. |  |
| PRT-0331 | Tree: copy/paste a feature to another part (flange) | Regression | P2 | On the flange preset: copy/paste a feature to another part. | References re-mapped or flagged. |  |
| PRT-0332 | Tree: copy/paste a feature to another part (housing) | Regression | P2 | On the housing preset: copy/paste a feature to another part. | References re-mapped or flagged. |  |
| PRT-0333 | Tree: design table with 5 variants (bracket) | Regression | P2 | On the bracket preset: design table with 5 variants. | Each variant builds; CSV round-trips. |  |
| PRT-0334 | Tree: design table with 5 variants (flange) | Regression | P2 | On the flange preset: design table with 5 variants. | Each variant builds; CSV round-trips. |  |
| PRT-0335 | Tree: design table with 5 variants (housing) | Regression | P2 | On the housing preset: design table with 5 variants. | Each variant builds; CSV round-trips. |  |
| PRT-0336 | Tree: expression d2 = d1*2 drives a pad (bracket) | Regression | P2 | On the bracket preset: expression d2 = d1*2 drives a pad. | Changing d1 updates the pad. |  |
| PRT-0337 | Tree: expression d2 = d1*2 drives a pad (flange) | Regression | P2 | On the flange preset: expression d2 = d1*2 drives a pad. | Changing d1 updates the pad. |  |
| PRT-0338 | Tree: expression d2 = d1*2 drives a pad (housing) | Regression | P2 | On the housing preset: expression d2 = d1*2 drives a pad. | Changing d1 updates the pad. |  |
| PRT-0339 | Tree: circular expression d1 = d2, d2 = d1 (bracket) | Regression | P2 | On the bracket preset: circular expression d1 = d2, d2 = d1. | Rejected: cycle reported with both names. |  |
| PRT-0340 | Tree: circular expression d1 = d2, d2 = d1 (flange) | Regression | P2 | On the flange preset: circular expression d1 = d2, d2 = d1. | Rejected: cycle reported with both names. |  |
| PRT-0341 | Tree: circular expression d1 = d2, d2 = d1 (housing) | Regression | P2 | On the housing preset: circular expression d1 = d2, d2 = d1. | Rejected: cycle reported with both names. |  |
| PRT-0342 | Tree: save/reload a 200-feature part (bracket) | Regression | P2 | On the bracket preset: save/reload a 200-feature part. | Identical feature list and volume. |  |
| PRT-0343 | Tree: save/reload a 200-feature part (flange) | Regression | P2 | On the flange preset: save/reload a 200-feature part. | Identical feature list and volume. |  |
| PRT-0344 | Tree: save/reload a 200-feature part (housing) | Regression | P2 | On the housing preset: save/reload a 200-feature part. | Identical feature list and volume. |  |

## Loft / Sweep / Rib

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PRT-0345 | Loft 2 sections of circles | Functional | P2 | Create 2 circles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0346 | Loft 2 sections of rectangles | Functional | P2 | Create 2 rectangles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0347 | Loft 2 sections of mixed circle→square | Functional | P2 | Create 2 mixed circle→square 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0348 | Loft 2 sections of rotated rectangles (twist 45°) | Functional | P2 | Create 2 rotated rectangles (twist 45°) 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0349 | Loft 3 sections of circles | Functional | P2 | Create 3 circles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0350 | Loft 3 sections of rectangles | Functional | P2 | Create 3 rectangles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0351 | Loft 3 sections of mixed circle→square | Functional | P2 | Create 3 mixed circle→square 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0352 | Loft 3 sections of rotated rectangles (twist 45°) | Functional | P2 | Create 3 rotated rectangles (twist 45°) 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0353 | Loft 5 sections of circles | Functional | P2 | Create 5 circles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0354 | Loft 5 sections of rectangles | Functional | P2 | Create 5 rectangles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0355 | Loft 5 sections of mixed circle→square | Functional | P2 | Create 5 mixed circle→square 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0356 | Loft 5 sections of rotated rectangles (twist 45°) | Functional | P2 | Create 5 rotated rectangles (twist 45°) 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0357 | Loft 10 sections of circles | Functional | P2 | Create 10 circles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0358 | Loft 10 sections of rectangles | Functional | P2 | Create 10 rectangles 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0359 | Loft 10 sections of mixed circle→square | Functional | P2 | Create 10 mixed circle→square 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0360 | Loft 10 sections of rotated rectangles (twist 45°) | Functional | P2 | Create 10 rotated rectangles (twist 45°) 50 mm apart; loft (ruled and smooth). | Valid solid through every section (deviation < 1e-4 mm); smooth loft G1 between spans. |  |
| PRT-0361 | Sweep circle Ø10 along line | Functional | P2 | Sweep a Ø10 circle along a line. | Valid solid; volume ≈ π·25·path length (±0.5%). |  |
| PRT-0362 | Sweep circle Ø10 along arc | Functional | P2 | Sweep a Ø10 circle along a arc. | Valid solid; volume ≈ π·25·path length (±0.5%). |  |
| PRT-0363 | Sweep circle Ø10 along helix pitch 10 | Functional | P2 | Sweep a Ø10 circle along a helix pitch 10. | Valid solid; volume ≈ π·25·path length (±0.5%). |  |
| PRT-0364 | Sweep circle Ø10 along 3D spline | Functional | P2 | Sweep a Ø10 circle along a 3D spline. | Valid solid; volume ≈ π·25·path length (±0.5%). |  |
| PRT-0365 | Sweep circle Ø10 along path with a kink | Negative | P2 | Sweep a Ø10 circle along a path with a kink. | Rejected: tangent discontinuity |  |
| PRT-0366 | Sweep circle Ø10 along closed path | Functional | P2 | Sweep a Ø10 circle along a closed path. | Valid solid; volume ≈ π·25·path length (±0.5%). |  |
