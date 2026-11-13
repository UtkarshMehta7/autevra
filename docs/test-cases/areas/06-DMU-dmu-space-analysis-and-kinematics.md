# DMU — DMU Space Analysis and Kinematics

**CATIA-class equivalent:** DMU Space Analysis / DMU Kinematics / Fitting  
**Autevra workspace:** Assembly; Production (mechanisms)  
**Scope:** Shared  
**Cases:** 134 (Have 21, Partial 51, Gap 62)

Clash, clearance, sectioning, measurement and mechanisms.

[← Back to the index](../README.md)

## Features

- Clash and clearance — 31 cases (Partial)
- Sectioning and measurement — 43 cases (Gap)
- Mechanisms — 60 cases (Partial)

## Clash and clearance

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| DMU-0001 | Pair at distance -5 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clash (penetration 5 mm) listed with both parts and depth. | d=-5, c=0 |
| DMU-0002 | Pair at distance -5 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clash (penetration 5 mm) listed with both parts and depth. | d=-5, c=1 |
| DMU-0003 | Pair at distance -5 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clash (penetration 5 mm) listed with both parts and depth. | d=-5, c=3 |
| DMU-0004 | Pair at distance -0.01 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clash (penetration 0.01 mm) listed with both parts and depth. | d=-0.01, c=0 |
| DMU-0005 | Pair at distance -0.01 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clash (penetration 0.01 mm) listed with both parts and depth. | d=-0.01, c=1 |
| DMU-0006 | Pair at distance -0.01 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clash (penetration 0.01 mm) listed with both parts and depth. | d=-0.01, c=3 |
| DMU-0007 | Pair at distance 0 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Contact (distance 0) listed separately from clash. | d=0, c=0 |
| DMU-0008 | Pair at distance 0 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Contact (distance 0) listed separately from clash. | d=0, c=1 |
| DMU-0009 | Pair at distance 0 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Contact (distance 0) listed separately from clash. | d=0, c=3 |
| DMU-0010 | Pair at distance 0.01 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=0.01, c=0 |
| DMU-0011 | Pair at distance 0.01 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clearance violation: 0.01 < 1 mm. | d=0.01, c=1 |
| DMU-0012 | Pair at distance 0.01 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clearance violation: 0.01 < 3 mm. | d=0.01, c=3 |
| DMU-0013 | Pair at distance 0.99 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=0.99, c=0 |
| DMU-0014 | Pair at distance 0.99 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clearance violation: 0.99 < 1 mm. | d=0.99, c=1 |
| DMU-0015 | Pair at distance 0.99 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clearance violation: 0.99 < 3 mm. | d=0.99, c=3 |
| DMU-0016 | Pair at distance 1.0 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=1.0, c=0 |
| DMU-0017 | Pair at distance 1.0 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=1.0, c=1 |
| DMU-0018 | Pair at distance 1.0 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clearance violation: 1.0 < 3 mm. | d=1.0, c=3 |
| DMU-0019 | Pair at distance 1.01 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=1.01, c=0 |
| DMU-0020 | Pair at distance 1.01 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=1.01, c=1 |
| DMU-0021 | Pair at distance 1.01 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | Clearance violation: 1.01 < 3 mm. | d=1.01, c=3 |
| DMU-0022 | Pair at distance 5 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=5, c=0 |
| DMU-0023 | Pair at distance 5 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=5, c=1 |
| DMU-0024 | Pair at distance 5 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=5, c=3 |
| DMU-0025 | Pair at distance 50 mm, required clearance 0 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=50, c=0 |
| DMU-0026 | Pair at distance 50 mm, required clearance 1 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=50, c=1 |
| DMU-0027 | Pair at distance 50 mm, required clearance 3 mm | Boundary | P1 | Place two blocks at the given distance; run clash with clearance. | No issue. | d=50, c=3 |
| DMU-0028 | All-pairs clash on 10 parts | Performance | P2 | Run all-pairs clash. | Broad phase prunes pairs; finishes < 2 s; results stable across runs. |  |
| DMU-0029 | All-pairs clash on 100 parts | Performance | P2 | Run all-pairs clash. | Broad phase prunes pairs; finishes < 2 s; results stable across runs. |  |
| DMU-0030 | All-pairs clash on 1000 parts | Performance | P2 | Run all-pairs clash. | Broad phase prunes pairs; finishes < 4 s; results stable across runs. |  |
| DMU-0031 | All-pairs clash on 5000 parts | Performance | P2 | Run all-pairs clash. | Broad phase prunes pairs; finishes < 20 s; results stable across runs. |  |

## Sectioning and measurement

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| DMU-0032 | Section X: capped | Functional | P2 | Create a X section; capped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0033 | Section X: uncapped | Functional | P2 | Create a X section; uncapped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0034 | Section X: moving | Functional | P2 | Create a X section; moving. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0035 | Section X: 2D result view | Functional | P2 | Create a X section; 2D result view. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0036 | Section X: export section as DXF | Functional | P2 | Create a X section; export section as DXF. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0037 | Section Y: capped | Functional | P2 | Create a Y section; capped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0038 | Section Y: uncapped | Functional | P2 | Create a Y section; uncapped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0039 | Section Y: moving | Functional | P2 | Create a Y section; moving. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0040 | Section Y: 2D result view | Functional | P2 | Create a Y section; 2D result view. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0041 | Section Y: export section as DXF | Functional | P2 | Create a Y section; export section as DXF. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0042 | Section Z: capped | Functional | P2 | Create a Z section; capped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0043 | Section Z: uncapped | Functional | P2 | Create a Z section; uncapped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0044 | Section Z: moving | Functional | P2 | Create a Z section; moving. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0045 | Section Z: 2D result view | Functional | P2 | Create a Z section; 2D result view. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0046 | Section Z: export section as DXF | Functional | P2 | Create a Z section; export section as DXF. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0047 | Section arbitrary 30°/45°: capped | Functional | P2 | Create a arbitrary 30°/45° section; capped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0048 | Section arbitrary 30°/45°: uncapped | Functional | P2 | Create a arbitrary 30°/45° section; uncapped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0049 | Section arbitrary 30°/45°: moving | Functional | P2 | Create a arbitrary 30°/45° section; moving. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0050 | Section arbitrary 30°/45°: 2D result view | Functional | P2 | Create a arbitrary 30°/45° section; 2D result view. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0051 | Section arbitrary 30°/45°: export section as DXF | Functional | P2 | Create a arbitrary 30°/45° section; export section as DXF. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0052 | Section box section: capped | Functional | P2 | Create a box section section; capped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0053 | Section box section: uncapped | Functional | P2 | Create a box section section; uncapped. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0054 | Section box section: moving | Functional | P2 | Create a box section section; moving. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0055 | Section box section: 2D result view | Functional | P2 | Create a box section section; 2D result view. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0056 | Section box section: export section as DXF | Functional | P2 | Create a box section section; export section as DXF. | Cut is exact; capping faces closed per part; colours per part. |  |
| DMU-0057 | Measure point-point on part | Functional | P2 | Measure point-point. | Euclidean distance ±1e-6. |  |
| DMU-0058 | Measure point-point on assembly | Functional | P2 | Measure point-point. | Euclidean distance ±1e-6. |  |
| DMU-0059 | Measure point-point on imported STEP | Functional | P2 | Measure point-point. | Euclidean distance ±1e-6. |  |
| DMU-0060 | Measure edge length on part | Functional | P2 | Measure edge length. | Exact length. |  |
| DMU-0061 | Measure edge length on assembly | Functional | P2 | Measure edge length. | Exact length. |  |
| DMU-0062 | Measure edge length on imported STEP | Functional | P2 | Measure edge length. | Exact length. |  |
| DMU-0063 | Measure minimum distance between bodies on part | Functional | P2 | Measure minimum distance between bodies. | Matches OCCT BRepExtrema. |  |
| DMU-0064 | Measure minimum distance between bodies on assembly | Functional | P2 | Measure minimum distance between bodies. | Matches OCCT BRepExtrema. |  |
| DMU-0065 | Measure minimum distance between bodies on imported STEP | Functional | P2 | Measure minimum distance between bodies. | Matches OCCT BRepExtrema. |  |
| DMU-0066 | Measure angle between faces on part | Functional | P2 | Measure angle between faces. | Dihedral angle ±1e-6°. |  |
| DMU-0067 | Measure angle between faces on assembly | Functional | P2 | Measure angle between faces. | Dihedral angle ±1e-6°. |  |
| DMU-0068 | Measure angle between faces on imported STEP | Functional | P2 | Measure angle between faces. | Dihedral angle ±1e-6°. |  |
| DMU-0069 | Measure radius of arc on part | Functional | P2 | Measure radius of arc. | Exact radius. |  |
| DMU-0070 | Measure radius of arc on assembly | Functional | P2 | Measure radius of arc. | Exact radius. |  |
| DMU-0071 | Measure radius of arc on imported STEP | Functional | P2 | Measure radius of arc. | Exact radius. |  |
| DMU-0072 | Measure inertia of selection on part | Functional | P2 | Measure inertia of selection. | Mass, CG and inertia tensor reported. |  |
| DMU-0073 | Measure inertia of selection on assembly | Functional | P2 | Measure inertia of selection. | Mass, CG and inertia tensor reported. |  |
| DMU-0074 | Measure inertia of selection on imported STEP | Functional | P2 | Measure inertia of selection. | Mass, CG and inertia tensor reported. |  |

## Mechanisms

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| DMU-0075 | Four-bar g=4, crank=2, coupler=5, rocker=4 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 7, p+q = 8 → Grashof crank-rocker. | Grashof criterion |
| DMU-0076 | Four-bar g=2, crank=4, coupler=5, rocker=4 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 7, p+q = 8 → Grashof double crank (drag link). | Grashof criterion |
| DMU-0077 | Four-bar g=5, crank=2, coupler=3, rocker=4 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 7, p+q = 7 → change-point mechanism (flags singular positions). | Grashof criterion |
| DMU-0078 | Four-bar g=3, crank=4, coupler=5, rocker=6 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 9, p+q = 9 → change-point mechanism (flags singular positions). | Grashof criterion |
| DMU-0079 | Four-bar g=2, crank=7, coupler=9, rocker=3 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 11, p+q = 10 → non-Grashof triple rocker. | Grashof criterion |
| DMU-0080 | Four-bar g=4, crank=4, coupler=4, rocker=4 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 8, p+q = 8 → change-point mechanism (flags singular positions). | Grashof criterion |
| DMU-0081 | Four-bar g=1, crank=3, coupler=3, rocker=3 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 4, p+q = 6 → Grashof double crank (drag link). | Grashof criterion |
| DMU-0082 | Four-bar g=6, crank=2, coupler=7, rocker=3 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 9, p+q = 9 → change-point mechanism (flags singular positions). | Grashof criterion |
| DMU-0083 | Four-bar g=3, crank=3, coupler=8, rocker=4 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 11, p+q = 7 → non-Grashof triple rocker. | Grashof criterion |
| DMU-0084 | Four-bar g=10, crank=2, coupler=7, rocker=6 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 12, p+q = 13 → Grashof crank-rocker. | Grashof criterion |
| DMU-0085 | Four-bar g=5, crank=5, coupler=1, rocker=2 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 6, p+q = 7 → Grashof double rocker. | Grashof criterion |
| DMU-0086 | Four-bar g=8, crank=3, coupler=5, rocker=6 | Accuracy | P2 | POST /mechanisms/fourbar with the link lengths. | s+l = 11, p+q = 11 → change-point mechanism (flags singular positions). | Grashof criterion |
| DMU-0087 | Slider-crank r=20, l=60 | Accuracy | P2 | POST /mechanisms/slider-crank. | Stroke = 2r = 40; TDC at r+l = 80; BDC at l−r = 40. |  |
| DMU-0088 | Slider-crank r=25, l=100 | Accuracy | P2 | POST /mechanisms/slider-crank. | Stroke = 2r = 50; TDC at r+l = 125; BDC at l−r = 75. |  |
| DMU-0089 | Slider-crank r=40, l=140 | Accuracy | P2 | POST /mechanisms/slider-crank. | Stroke = 2r = 80; TDC at r+l = 180; BDC at l−r = 100. |  |
| DMU-0090 | Slider-crank r=50, l=50 | Negative | P2 | POST /mechanisms/slider-crank. | Rejected: connecting rod must be longer than the crank. |  |
| DMU-0091 | Slider-crank r=60, l=40 | Negative | P2 | POST /mechanisms/slider-crank. | Rejected: connecting rod must be longer than the crank. |  |
| DMU-0092 | Slider-crank r=45, l=160 | Accuracy | P2 | POST /mechanisms/slider-crank. | Stroke = 2r = 90; TDC at r+l = 205; BDC at l−r = 115. |  |
| DMU-0093 | revolute joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0094 | revolute joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0095 | revolute joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0096 | prismatic joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0097 | prismatic joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0098 | prismatic joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0099 | cylindrical joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 2 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0100 | cylindrical joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 2 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0101 | cylindrical joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 2 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0102 | spherical joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 3 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0103 | spherical joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 3 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0104 | spherical joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 3 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0105 | planar joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 3 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0106 | planar joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 3 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0107 | planar joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 3 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0108 | screw (pitch 2) joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0109 | screw (pitch 2) joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0110 | screw (pitch 2) joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0111 | universal joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 2 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0112 | universal joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 2 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0113 | universal joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 2 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0114 | rack-pinion joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0115 | rack-pinion joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0116 | rack-pinion joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0117 | gear pair 1:3 joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0118 | gear pair 1:3 joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0119 | gear pair 1:3 joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0120 | cam-follower joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0121 | cam-follower joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0122 | cam-follower joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 1 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0123 | rigid joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 0 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0124 | rigid joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 0 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0125 | rigid joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 0 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0126 | point-curve joint in a 2-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 4 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0127 | point-curve joint in a 3-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 4 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0128 | point-curve joint in a 4-body mechanism | Functional | P2 | Build the mechanism; compute mobility. | Joint allows 4 DOF; Grübler/Kutzbach mobility reported; simulate 360 steps without drift > 1e-6. |  |
| DMU-0129 | Mechanism analysis: swept volume | Functional | P2 | Run swept volume on the wiper four-bar. | Result produced and exportable. |  |
| DMU-0130 | Mechanism analysis: trace of a point | Functional | P2 | Run trace of a point on the wiper four-bar. | Result produced and exportable. |  |
| DMU-0131 | Mechanism analysis: clash during motion | Functional | P2 | Run clash during motion on the wiper four-bar. | Result produced and exportable. |  |
| DMU-0132 | Mechanism analysis: velocity/acceleration plot | Functional | P2 | Run velocity/acceleration plot on the wiper four-bar. | Result produced and exportable. |  |
| DMU-0133 | Mechanism analysis: law-driven command (sin) | Functional | P2 | Run law-driven command (sin) on the wiper four-bar. | Result produced and exportable. |  |
| DMU-0134 | Mechanism analysis: export motion as glTF animation | Functional | P2 | Run export motion as glTF animation on the wiper four-bar. | Result produced and exportable. |  |
