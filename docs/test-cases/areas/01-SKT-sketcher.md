# SKT — Sketcher

**CATIA-class equivalent:** Sketcher  
**Autevra workspace:** Part Design → Sketcher; /sketch/solve  
**Scope:** Shared  
**Cases:** 319 (Have 0, Partial 244, Gap 75)

2D profiles with geometric and dimensional constraints, DOF reporting and profile validation.

[← Back to the index](../README.md)

## Features

- Sketch entities — 24 cases (Partial)
- Geometric and dimensional constraints — 126 cases (Partial)
- Dimension values — 36 cases (Partial)
- Conflict and DOF status — 10 cases (Partial)
- Sketch operations — 75 cases (Gap)
- Profile validation — 48 cases (Partial)

## Sketch entities

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SKT-0001 | Create a point | Functional | P1 | Open a sketch on XY; create a point by clicking points; finish. | Entity appears, is selectable and reports 2 free DOF in the status bar. |  |
| SKT-0002 | Delete a point that carries constraints | Functional | P2 | Create a point, constrain it to another entity, delete the point. | Entity and every constraint that references it are removed; solver re-runs; no orphan constraints. |  |
| SKT-0003 | Drag an unconstrained point | Usability | P2 | Create a point; drag a handle 25 mm in X. | Entity follows the cursor live; no other entity moves. |  |
| SKT-0004 | Convert point to construction | Functional | P2 | Create a point; toggle construction mode. | Rendered dashed; excluded from profile loops used by Pad/Pocket; still usable by constraints. |  |
| SKT-0005 | Create a line | Functional | P1 | Open a sketch on XY; create a line by clicking points; finish. | Entity appears, is selectable and reports 4 free DOF in the status bar. |  |
| SKT-0006 | Delete a line that carries constraints | Functional | P2 | Create a line, constrain it to another entity, delete the line. | Entity and every constraint that references it are removed; solver re-runs; no orphan constraints. |  |
| SKT-0007 | Drag an unconstrained line | Usability | P2 | Create a line; drag a handle 25 mm in X. | Entity follows the cursor live; no other entity moves. |  |
| SKT-0008 | Convert line to construction | Functional | P2 | Create a line; toggle construction mode. | Rendered dashed; excluded from profile loops used by Pad/Pocket; still usable by constraints. |  |
| SKT-0009 | Create a circle | Functional | P1 | Open a sketch on XY; create a circle by clicking points; finish. | Entity appears, is selectable and reports 3 free DOF in the status bar. |  |
| SKT-0010 | Delete a circle that carries constraints | Functional | P2 | Create a circle, constrain it to another entity, delete the circle. | Entity and every constraint that references it are removed; solver re-runs; no orphan constraints. |  |
| SKT-0011 | Drag an unconstrained circle | Usability | P2 | Create a circle; drag a handle 25 mm in X. | Entity follows the cursor live; no other entity moves. |  |
| SKT-0012 | Convert circle to construction | Functional | P2 | Create a circle; toggle construction mode. | Rendered dashed; excluded from profile loops used by Pad/Pocket; still usable by constraints. |  |
| SKT-0013 | Create a arc | Functional | P1 | Open a sketch on XY; create a arc by clicking points; finish. | Entity appears, is selectable and reports 5 free DOF in the status bar. |  |
| SKT-0014 | Delete a arc that carries constraints | Functional | P2 | Create a arc, constrain it to another entity, delete the arc. | Entity and every constraint that references it are removed; solver re-runs; no orphan constraints. |  |
| SKT-0015 | Drag an unconstrained arc | Usability | P2 | Create a arc; drag a handle 25 mm in X. | Entity follows the cursor live; no other entity moves. |  |
| SKT-0016 | Convert arc to construction | Functional | P2 | Create a arc; toggle construction mode. | Rendered dashed; excluded from profile loops used by Pad/Pocket; still usable by constraints. |  |
| SKT-0017 | Create a ellipse | Functional | P1 | Open a sketch on XY; create a ellipse by clicking points; finish. | Entity appears, is selectable and reports 5 free DOF in the status bar. |  |
| SKT-0018 | Delete a ellipse that carries constraints | Functional | P2 | Create a ellipse, constrain it to another entity, delete the ellipse. | Entity and every constraint that references it are removed; solver re-runs; no orphan constraints. |  |
| SKT-0019 | Drag an unconstrained ellipse | Usability | P2 | Create a ellipse; drag a handle 25 mm in X. | Entity follows the cursor live; no other entity moves. |  |
| SKT-0020 | Convert ellipse to construction | Functional | P2 | Create a ellipse; toggle construction mode. | Rendered dashed; excluded from profile loops used by Pad/Pocket; still usable by constraints. |  |
| SKT-0021 | Create a spline (4 poles) | Functional | P1 | Open a sketch on XY; create a spline (4 poles) by clicking points; finish. | Entity appears, is selectable and reports 8 free DOF in the status bar. |  |
| SKT-0022 | Delete a spline (4 poles) that carries constraints | Functional | P2 | Create a spline (4 poles), constrain it to another entity, delete the spline (4 poles). | Entity and every constraint that references it are removed; solver re-runs; no orphan constraints. |  |
| SKT-0023 | Drag an unconstrained spline (4 poles) | Usability | P2 | Create a spline (4 poles); drag a handle 25 mm in X. | Entity follows the cursor live; no other entity moves. |  |
| SKT-0024 | Convert spline (4 poles) to construction | Functional | P2 | Create a spline (4 poles); toggle construction mode. | Rendered dashed; excluded from profile loops used by Pad/Pocket; still usable by constraints. |  |

## Geometric and dimensional constraints

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SKT-0025 | Apply 'coincident' to point + point | Functional | P1 | Create point and point in general position; apply coincident; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 2. | Entities: ('point', 'point'); Grübler-style DOF count for planar sketches |
| SKT-0026 | Drag after 'coincident' on point + point | Regression | P2 | With coincident applied, drag the first entity 10 mm. | coincident stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0027 | Delete a 'coincident' constraint | Regression | P2 | Apply coincident, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0028 | Redundant 'coincident' | Negative | P2 | Apply coincident twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0029 | Apply 'point-on-curve' to point + line | Functional | P1 | Create point and line in general position; apply point-on-curve; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 6 → 5. | Entities: ('point', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0030 | Drag after 'point-on-curve' on point + line | Regression | P2 | With point-on-curve applied, drag the first entity 10 mm. | point-on-curve stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0031 | Apply 'point-on-curve' to point + circle | Functional | P1 | Create point and circle in general position; apply point-on-curve; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 5 → 4. | Entities: ('point', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0032 | Drag after 'point-on-curve' on point + circle | Regression | P2 | With point-on-curve applied, drag the first entity 10 mm. | point-on-curve stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0033 | Apply 'point-on-curve' to point + arc | Functional | P1 | Create point and arc in general position; apply point-on-curve; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 7 → 6. | Entities: ('point', 'arc'); Grübler-style DOF count for planar sketches |
| SKT-0034 | Drag after 'point-on-curve' on point + arc | Regression | P2 | With point-on-curve applied, drag the first entity 10 mm. | point-on-curve stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0035 | Apply 'point-on-curve' to point + ellipse | Functional | P1 | Create point and ellipse in general position; apply point-on-curve; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 7 → 6. | Entities: ('point', 'ellipse'); Grübler-style DOF count for planar sketches |
| SKT-0036 | Drag after 'point-on-curve' on point + ellipse | Regression | P2 | With point-on-curve applied, drag the first entity 10 mm. | point-on-curve stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0037 | Apply 'point-on-curve' to point + spline (4 poles) | Functional | P1 | Create point and spline (4 poles) in general position; apply point-on-curve; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 10 → 9. | Entities: ('point', 'spline (4 poles)'); Grübler-style DOF count for planar sketches |
| SKT-0038 | Drag after 'point-on-curve' on point + spline (4 poles) | Regression | P2 | With point-on-curve applied, drag the first entity 10 mm. | point-on-curve stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0039 | Delete a 'point-on-curve' constraint | Regression | P2 | Apply point-on-curve, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0040 | Redundant 'point-on-curve' | Negative | P2 | Apply point-on-curve twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0041 | Apply 'horizontal' to line | Functional | P1 | Create line in general position; apply horizontal; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 3. | Entities: ('line',); Grübler-style DOF count for planar sketches |
| SKT-0042 | Drag after 'horizontal' on line | Regression | P2 | With horizontal applied, drag the first entity 10 mm. | horizontal stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0043 | Apply 'horizontal' to point + point | Functional | P1 | Create point and point in general position; apply horizontal; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 3. | Entities: ('point', 'point'); Grübler-style DOF count for planar sketches |
| SKT-0044 | Drag after 'horizontal' on point + point | Regression | P2 | With horizontal applied, drag the first entity 10 mm. | horizontal stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0045 | Delete a 'horizontal' constraint | Regression | P2 | Apply horizontal, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0046 | Redundant 'horizontal' | Negative | P2 | Apply horizontal twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0047 | Apply 'vertical' to line | Functional | P1 | Create line in general position; apply vertical; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 3. | Entities: ('line',); Grübler-style DOF count for planar sketches |
| SKT-0048 | Drag after 'vertical' on line | Regression | P2 | With vertical applied, drag the first entity 10 mm. | vertical stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0049 | Apply 'vertical' to point + point | Functional | P1 | Create point and point in general position; apply vertical; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 3. | Entities: ('point', 'point'); Grübler-style DOF count for planar sketches |
| SKT-0050 | Drag after 'vertical' on point + point | Regression | P2 | With vertical applied, drag the first entity 10 mm. | vertical stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0051 | Delete a 'vertical' constraint | Regression | P2 | Apply vertical, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0052 | Redundant 'vertical' | Negative | P2 | Apply vertical twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0053 | Apply 'parallel' to line + line | Functional | P1 | Create line and line in general position; apply parallel; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('line', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0054 | Drag after 'parallel' on line + line | Regression | P2 | With parallel applied, drag the first entity 10 mm. | parallel stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0055 | Delete a 'parallel' constraint | Regression | P2 | Apply parallel, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0056 | Redundant 'parallel' | Negative | P2 | Apply parallel twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0057 | Apply 'perpendicular' to line + line | Functional | P1 | Create line and line in general position; apply perpendicular; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('line', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0058 | Drag after 'perpendicular' on line + line | Regression | P2 | With perpendicular applied, drag the first entity 10 mm. | perpendicular stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0059 | Delete a 'perpendicular' constraint | Regression | P2 | Apply perpendicular, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0060 | Redundant 'perpendicular' | Negative | P2 | Apply perpendicular twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0061 | Apply 'tangent' to line + circle | Functional | P1 | Create line and circle in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 7 → 6. | Entities: ('line', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0062 | Drag after 'tangent' on line + circle | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0063 | Apply 'tangent' to line + arc | Functional | P1 | Create line and arc in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 9 → 8. | Entities: ('line', 'arc'); Grübler-style DOF count for planar sketches |
| SKT-0064 | Drag after 'tangent' on line + arc | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0065 | Apply 'tangent' to arc + arc | Functional | P1 | Create arc and arc in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 10 → 9. | Entities: ('arc', 'arc'); Grübler-style DOF count for planar sketches |
| SKT-0066 | Drag after 'tangent' on arc + arc | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0067 | Apply 'tangent' to arc + circle | Functional | P1 | Create arc and circle in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('arc', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0068 | Drag after 'tangent' on arc + circle | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0069 | Apply 'tangent' to circle + circle | Functional | P1 | Create circle and circle in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 6 → 5. | Entities: ('circle', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0070 | Drag after 'tangent' on circle + circle | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0071 | Apply 'tangent' to line + spline (4 poles) | Functional | P1 | Create line and spline (4 poles) in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 12 → 11. | Entities: ('line', 'spline (4 poles)'); Grübler-style DOF count for planar sketches |
| SKT-0072 | Drag after 'tangent' on line + spline (4 poles) | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0073 | Apply 'tangent' to arc + spline (4 poles) | Functional | P1 | Create arc and spline (4 poles) in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 13 → 12. | Entities: ('arc', 'spline (4 poles)'); Grübler-style DOF count for planar sketches |
| SKT-0074 | Drag after 'tangent' on arc + spline (4 poles) | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0075 | Apply 'tangent' to line + ellipse | Functional | P1 | Create line and ellipse in general position; apply tangent; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 9 → 8. | Entities: ('line', 'ellipse'); Grübler-style DOF count for planar sketches |
| SKT-0076 | Drag after 'tangent' on line + ellipse | Regression | P2 | With tangent applied, drag the first entity 10 mm. | tangent stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0077 | Delete a 'tangent' constraint | Regression | P2 | Apply tangent, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0078 | Redundant 'tangent' | Negative | P2 | Apply tangent twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0079 | Apply 'concentric' to circle + circle | Functional | P1 | Create circle and circle in general position; apply concentric; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 6 → 4. | Entities: ('circle', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0080 | Drag after 'concentric' on circle + circle | Regression | P2 | With concentric applied, drag the first entity 10 mm. | concentric stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0081 | Apply 'concentric' to arc + circle | Functional | P1 | Create arc and circle in general position; apply concentric; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 6. | Entities: ('arc', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0082 | Drag after 'concentric' on arc + circle | Regression | P2 | With concentric applied, drag the first entity 10 mm. | concentric stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0083 | Apply 'concentric' to arc + arc | Functional | P1 | Create arc and arc in general position; apply concentric; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 10 → 8. | Entities: ('arc', 'arc'); Grübler-style DOF count for planar sketches |
| SKT-0084 | Drag after 'concentric' on arc + arc | Regression | P2 | With concentric applied, drag the first entity 10 mm. | concentric stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0085 | Apply 'concentric' to ellipse + circle | Functional | P1 | Create ellipse and circle in general position; apply concentric; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 6. | Entities: ('ellipse', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0086 | Drag after 'concentric' on ellipse + circle | Regression | P2 | With concentric applied, drag the first entity 10 mm. | concentric stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0087 | Delete a 'concentric' constraint | Regression | P2 | Apply concentric, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0088 | Redundant 'concentric' | Negative | P2 | Apply concentric twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0089 | Apply 'equal length/radius' to line + line | Functional | P1 | Create line and line in general position; apply equal length/radius; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('line', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0090 | Drag after 'equal length/radius' on line + line | Regression | P2 | With equal length/radius applied, drag the first entity 10 mm. | equal length/radius stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0091 | Apply 'equal length/radius' to circle + circle | Functional | P1 | Create circle and circle in general position; apply equal length/radius; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 6 → 5. | Entities: ('circle', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0092 | Drag after 'equal length/radius' on circle + circle | Regression | P2 | With equal length/radius applied, drag the first entity 10 mm. | equal length/radius stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0093 | Apply 'equal length/radius' to arc + arc | Functional | P1 | Create arc and arc in general position; apply equal length/radius; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 10 → 9. | Entities: ('arc', 'arc'); Grübler-style DOF count for planar sketches |
| SKT-0094 | Drag after 'equal length/radius' on arc + arc | Regression | P2 | With equal length/radius applied, drag the first entity 10 mm. | equal length/radius stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0095 | Apply 'equal length/radius' to arc + circle | Functional | P1 | Create arc and circle in general position; apply equal length/radius; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('arc', 'circle'); Grübler-style DOF count for planar sketches |
| SKT-0096 | Drag after 'equal length/radius' on arc + circle | Regression | P2 | With equal length/radius applied, drag the first entity 10 mm. | equal length/radius stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0097 | Delete a 'equal length/radius' constraint | Regression | P2 | Apply equal length/radius, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0098 | Redundant 'equal length/radius' | Negative | P2 | Apply equal length/radius twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0099 | Apply 'symmetric about line' to point + point | Functional | P1 | Create point and point in general position; apply symmetric about line; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 2. | Entities: ('point', 'point'); Grübler-style DOF count for planar sketches |
| SKT-0100 | Drag after 'symmetric about line' on point + point | Regression | P2 | With symmetric about line applied, drag the first entity 10 mm. | symmetric about line stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0101 | Delete a 'symmetric about line' constraint | Regression | P2 | Apply symmetric about line, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0102 | Redundant 'symmetric about line' | Negative | P2 | Apply symmetric about line twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0103 | Apply 'midpoint' to point + line | Functional | P1 | Create point and line in general position; apply midpoint; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 6 → 4. | Entities: ('point', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0104 | Drag after 'midpoint' on point + line | Regression | P2 | With midpoint applied, drag the first entity 10 mm. | midpoint stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0105 | Delete a 'midpoint' constraint | Regression | P2 | Apply midpoint, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0106 | Redundant 'midpoint' | Negative | P2 | Apply midpoint twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0107 | Apply 'distance' to point + point | Functional | P1 | Create point and point in general position; apply distance; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 3. | Entities: ('point', 'point'); Grübler-style DOF count for planar sketches |
| SKT-0108 | Drag after 'distance' on point + point | Regression | P2 | With distance applied, drag the first entity 10 mm. | distance stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0109 | Apply 'distance' to point + line | Functional | P1 | Create point and line in general position; apply distance; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 6 → 5. | Entities: ('point', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0110 | Drag after 'distance' on point + line | Regression | P2 | With distance applied, drag the first entity 10 mm. | distance stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0111 | Apply 'distance' to line + line | Functional | P1 | Create line and line in general position; apply distance; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('line', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0112 | Drag after 'distance' on line + line | Regression | P2 | With distance applied, drag the first entity 10 mm. | distance stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0113 | Delete a 'distance' constraint | Regression | P2 | Apply distance, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0114 | Redundant 'distance' | Negative | P2 | Apply distance twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0115 | Apply 'angle' to line + line | Functional | P1 | Create line and line in general position; apply angle; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 8 → 7. | Entities: ('line', 'line'); Grübler-style DOF count for planar sketches |
| SKT-0116 | Drag after 'angle' on line + line | Regression | P2 | With angle applied, drag the first entity 10 mm. | angle stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0117 | Delete a 'angle' constraint | Regression | P2 | Apply angle, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0118 | Redundant 'angle' | Negative | P2 | Apply angle twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0119 | Apply 'radius' to circle | Functional | P1 | Create circle in general position; apply radius; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 3 → 2. | Entities: ('circle',); Grübler-style DOF count for planar sketches |
| SKT-0120 | Drag after 'radius' on circle | Regression | P2 | With radius applied, drag the first entity 10 mm. | radius stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0121 | Apply 'radius' to arc | Functional | P1 | Create arc in general position; apply radius; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 5 → 4. | Entities: ('arc',); Grübler-style DOF count for planar sketches |
| SKT-0122 | Drag after 'radius' on arc | Regression | P2 | With radius applied, drag the first entity 10 mm. | radius stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0123 | Delete a 'radius' constraint | Regression | P2 | Apply radius, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0124 | Redundant 'radius' | Negative | P2 | Apply radius twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0125 | Apply 'diameter' to circle | Functional | P1 | Create circle in general position; apply diameter; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 3 → 2. | Entities: ('circle',); Grübler-style DOF count for planar sketches |
| SKT-0126 | Drag after 'diameter' on circle | Regression | P2 | With diameter applied, drag the first entity 10 mm. | diameter stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0127 | Apply 'diameter' to arc | Functional | P1 | Create arc in general position; apply diameter; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 5 → 4. | Entities: ('arc',); Grübler-style DOF count for planar sketches |
| SKT-0128 | Drag after 'diameter' on arc | Regression | P2 | With diameter applied, drag the first entity 10 mm. | diameter stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0129 | Delete a 'diameter' constraint | Regression | P2 | Apply diameter, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0130 | Redundant 'diameter' | Negative | P2 | Apply diameter twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0131 | Apply 'fix' to point | Functional | P1 | Create point in general position; apply fix; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 2 → 0. | Entities: ('point',); Grübler-style DOF count for planar sketches |
| SKT-0132 | Drag after 'fix' on point | Regression | P2 | With fix applied, drag the first entity 10 mm. | fix stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0133 | Apply 'fix' to line | Functional | P1 | Create line in general position; apply fix; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 4 → 0. | Entities: ('line',); Grübler-style DOF count for planar sketches |
| SKT-0134 | Drag after 'fix' on line | Regression | P2 | With fix applied, drag the first entity 10 mm. | fix stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0135 | Apply 'fix' to circle | Functional | P1 | Create circle in general position; apply fix; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 3 → 0. | Entities: ('circle',); Grübler-style DOF count for planar sketches |
| SKT-0136 | Drag after 'fix' on circle | Regression | P2 | With fix applied, drag the first entity 10 mm. | fix stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0137 | Apply 'fix' to arc | Functional | P1 | Create arc in general position; apply fix; run solver. | Solver converges; constraint residual < 1e-9 mm; DOF 5 → 0. | Entities: ('arc',); Grübler-style DOF count for planar sketches |
| SKT-0138 | Drag after 'fix' on arc | Regression | P2 | With fix applied, drag the first entity 10 mm. | fix stays satisfied during the drag (residual < 1e-6 mm per frame). |  |
| SKT-0139 | Delete a 'fix' constraint | Regression | P2 | Apply fix, then delete it. | DOF count returns to its previous value; geometry does not jump. |  |
| SKT-0140 | Redundant 'fix' | Negative | P2 | Apply fix twice to the same entities. | Second constraint is flagged redundant (over-constrained, consistent); sketch still solves. |  |
| SKT-0141 | Reject 'parallel' on point + circle | Negative | P2 | Select ('point', 'circle'); attempt parallel. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0142 | Reject 'perpendicular' on circle + circle | Negative | P2 | Select ('circle', 'circle'); attempt perpendicular. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0143 | Reject 'radius' on line | Negative | P2 | Select ('line',); attempt radius. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0144 | Reject 'concentric' on line + line | Negative | P2 | Select ('line', 'line'); attempt concentric. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0145 | Reject 'angle' on point + point | Negative | P2 | Select ('point', 'point'); attempt angle. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0146 | Reject 'tangent' on point + point | Negative | P2 | Select ('point', 'point'); attempt tangent. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0147 | Reject 'midpoint' on circle + circle | Negative | P2 | Select ('circle', 'circle'); attempt midpoint. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0148 | Reject 'diameter' on point | Negative | P2 | Select ('point',); attempt diameter. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0149 | Reject 'horizontal' on circle | Negative | P2 | Select ('circle',); attempt horizontal. | Command is disabled or rejected with a message naming the incompatible entity types. |  |
| SKT-0150 | Reject 'equal length/radius' on point + point | Negative | P2 | Select ('point', 'point'); attempt equal length/radius. | Command is disabled or rejected with a message naming the incompatible entity types. |  |

## Dimension values

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SKT-0151 | Set distance = 0 mm | Boundary | P2 | Dimension an entity with distance; type 0. | Value accepted; geometry updates; dimension shows 0 mm. | distance=0 mm |
| SKT-0152 | Set distance = -5 mm | Boundary | P3 | Dimension an entity with distance; type -5. | Value rejected with a range message; previous value kept. | distance=-5 mm |
| SKT-0153 | Set distance = 1.000e-06 mm | Boundary | P2 | Dimension an entity with distance; type 1e-06. | Value accepted; geometry updates; dimension shows 1.000e-06 mm. | distance=1e-06 mm |
| SKT-0154 | Set distance = 0.001 mm | Boundary | P2 | Dimension an entity with distance; type 0.001. | Value accepted; geometry updates; dimension shows 0.001 mm. | distance=0.001 mm |
| SKT-0155 | Set distance = 1 mm | Boundary | P2 | Dimension an entity with distance; type 1. | Value accepted; geometry updates; dimension shows 1 mm. | distance=1 mm |
| SKT-0156 | Set distance = 25.4 mm | Boundary | P2 | Dimension an entity with distance; type 25.4. | Value accepted; geometry updates; dimension shows 25.4 mm. | distance=25.4 mm |
| SKT-0157 | Set distance = 1000 mm | Boundary | P2 | Dimension an entity with distance; type 1000. | Value accepted; geometry updates; dimension shows 1000 mm. | distance=1000 mm |
| SKT-0158 | Set distance = 99999 mm | Boundary | P2 | Dimension an entity with distance; type 99999. | Value accepted; geometry updates; dimension shows 99999 mm. | distance=99999 mm |
| SKT-0159 | Set distance = 10000000 mm | Boundary | P3 | Dimension an entity with distance; type 10000000.0. | Value rejected with a range message; previous value kept. | distance=10000000.0 mm |
| SKT-0160 | Set radius = 0 mm | Boundary | P3 | Dimension an entity with radius; type 0. | Value rejected with a range message; previous value kept. | radius=0 mm |
| SKT-0161 | Set radius = -5 mm | Boundary | P3 | Dimension an entity with radius; type -5. | Value rejected with a range message; previous value kept. | radius=-5 mm |
| SKT-0162 | Set radius = 1.000e-06 mm | Boundary | P2 | Dimension an entity with radius; type 1e-06. | Value accepted; geometry updates; dimension shows 1.000e-06 mm. | radius=1e-06 mm |
| SKT-0163 | Set radius = 0.001 mm | Boundary | P2 | Dimension an entity with radius; type 0.001. | Value accepted; geometry updates; dimension shows 0.001 mm. | radius=0.001 mm |
| SKT-0164 | Set radius = 1 mm | Boundary | P2 | Dimension an entity with radius; type 1. | Value accepted; geometry updates; dimension shows 1 mm. | radius=1 mm |
| SKT-0165 | Set radius = 25.4 mm | Boundary | P2 | Dimension an entity with radius; type 25.4. | Value accepted; geometry updates; dimension shows 25.4 mm. | radius=25.4 mm |
| SKT-0166 | Set radius = 1000 mm | Boundary | P2 | Dimension an entity with radius; type 1000. | Value accepted; geometry updates; dimension shows 1000 mm. | radius=1000 mm |
| SKT-0167 | Set radius = 99999 mm | Boundary | P2 | Dimension an entity with radius; type 99999. | Value accepted; geometry updates; dimension shows 99999 mm. | radius=99999 mm |
| SKT-0168 | Set radius = 10000000 mm | Boundary | P3 | Dimension an entity with radius; type 10000000.0. | Value rejected with a range message; previous value kept. | radius=10000000.0 mm |
| SKT-0169 | Set diameter = 0 mm | Boundary | P3 | Dimension an entity with diameter; type 0. | Value rejected with a range message; previous value kept. | diameter=0 mm |
| SKT-0170 | Set diameter = -5 mm | Boundary | P3 | Dimension an entity with diameter; type -5. | Value rejected with a range message; previous value kept. | diameter=-5 mm |
| SKT-0171 | Set diameter = 1.000e-06 mm | Boundary | P2 | Dimension an entity with diameter; type 1e-06. | Value accepted; geometry updates; dimension shows 1.000e-06 mm. | diameter=1e-06 mm |
| SKT-0172 | Set diameter = 0.001 mm | Boundary | P2 | Dimension an entity with diameter; type 0.001. | Value accepted; geometry updates; dimension shows 0.001 mm. | diameter=0.001 mm |
| SKT-0173 | Set diameter = 1 mm | Boundary | P2 | Dimension an entity with diameter; type 1. | Value accepted; geometry updates; dimension shows 1 mm. | diameter=1 mm |
| SKT-0174 | Set diameter = 25.4 mm | Boundary | P2 | Dimension an entity with diameter; type 25.4. | Value accepted; geometry updates; dimension shows 25.4 mm. | diameter=25.4 mm |
| SKT-0175 | Set diameter = 1000 mm | Boundary | P2 | Dimension an entity with diameter; type 1000. | Value accepted; geometry updates; dimension shows 1000 mm. | diameter=1000 mm |
| SKT-0176 | Set diameter = 99999 mm | Boundary | P2 | Dimension an entity with diameter; type 99999. | Value accepted; geometry updates; dimension shows 99999 mm. | diameter=99999 mm |
| SKT-0177 | Set diameter = 10000000 mm | Boundary | P3 | Dimension an entity with diameter; type 10000000.0. | Value rejected with a range message; previous value kept. | diameter=10000000.0 mm |
| SKT-0178 | Set angle = 0 deg | Boundary | P3 | Dimension an entity with angle; type 0. | Value rejected with a range message; previous value kept. | angle=0 deg |
| SKT-0179 | Set angle = -5 deg | Boundary | P3 | Dimension an entity with angle; type -5. | Value rejected with a range message; previous value kept. | angle=-5 deg |
| SKT-0180 | Set angle = 1.000e-06 deg | Boundary | P2 | Dimension an entity with angle; type 1e-06. | Value accepted; geometry updates; dimension shows 1.000e-06 deg. | angle=1e-06 deg |
| SKT-0181 | Set angle = 0.001 deg | Boundary | P2 | Dimension an entity with angle; type 0.001. | Value accepted; geometry updates; dimension shows 0.001 deg. | angle=0.001 deg |
| SKT-0182 | Set angle = 1 deg | Boundary | P2 | Dimension an entity with angle; type 1. | Value accepted; geometry updates; dimension shows 1 deg. | angle=1 deg |
| SKT-0183 | Set angle = 25.4 deg | Boundary | P2 | Dimension an entity with angle; type 25.4. | Value accepted; geometry updates; dimension shows 25.4 deg. | angle=25.4 deg |
| SKT-0184 | Set angle = 1000 deg | Boundary | P3 | Dimension an entity with angle; type 1000. | Value rejected with a range message; previous value kept. | angle=1000 deg |
| SKT-0185 | Set angle = 99999 deg | Boundary | P3 | Dimension an entity with angle; type 99999. | Value rejected with a range message; previous value kept. | angle=99999 deg |
| SKT-0186 | Set angle = 10000000 deg | Boundary | P3 | Dimension an entity with angle; type 10000000.0. | Value rejected with a range message; previous value kept. | angle=10000000.0 deg |

## Conflict and DOF status

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SKT-0187 | DOF status: rectangle with 2 horizontal, 2 vertical, width, height, one fixed corner | Functional | P1 | Draw rectangle with 2 horizontal, 2 vertical, width, height, one fixed corner; read the DOF indicator. | Fully constrained (0 DOF), shown green |  |
| SKT-0188 | DOF status: rectangle without the fixed corner | Functional | P1 | Draw rectangle without the fixed corner; read the DOF indicator. | Under-constrained with 2 DOF (translation), shown white/blue |  |
| SKT-0189 | DOF status: rectangle with width 50 and an extra diagonal 60 (consistent: √(50²+33.17²)) | Functional | P1 | Draw rectangle with width 50 and an extra diagonal 60 (consistent: √(50²+33.17²)); read the DOF indicator. | Redundant but consistent; solver warns |  |
| SKT-0190 | DOF status: rectangle 50×30 with a diagonal of 40 (impossible, < 50) | Functional | P1 | Draw rectangle 50×30 with a diagonal of 40 (impossible, < 50); read the DOF indicator. | Over-constrained conflict; conflicting constraints highlighted; last valid state kept |  |
| SKT-0191 | DOF status: triangle 3-4-5 with a right angle | Functional | P1 | Draw triangle 3-4-5 with a right angle; read the DOF indicator. | Consistent; 0 internal DOF |  |
| SKT-0192 | DOF status: circle tangent to three mutually tangent circles | Functional | P1 | Draw circle tangent to three mutually tangent circles; read the DOF indicator. | Solver picks the branch nearest the sketched position |  |
| SKT-0193 | DOF status: two concentric circles with equal radius | Functional | P1 | Draw two concentric circles with equal radius; read the DOF indicator. | Accepted; solver reports coincident geometry warning |  |
| SKT-0194 | DOF status: chain of 50 lines with coincident ends and all lengths fixed | Functional | P1 | Draw chain of 50 lines with coincident ends and all lengths fixed; read the DOF indicator. | Solves < 200 ms; 3 rigid-body DOF + 49 angle DOF reported |  |
| SKT-0195 | DOF status: 200-entity sketch, all constrained | Functional | P1 | Draw 200-entity sketch, all constrained; read the DOF indicator. | Solves < 1 s; status 0 DOF |  |
| SKT-0196 | DOF status: arc with radius 10 and chord 25 | Functional | P1 | Draw arc with radius 10 and chord 25; read the DOF indicator. | Conflict (chord > 2r); highlighted |  |

## Sketch operations

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SKT-0197 | trim on line | Functional | P2 | Create a line; apply trim. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0198 | trim on arc | Functional | P2 | Create a arc; apply trim. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0199 | trim on circle | Functional | P2 | Create a circle; apply trim. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0200 | trim on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply trim. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0201 | trim on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply trim. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0202 | extend on line | Functional | P2 | Create a line; apply extend. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0203 | extend on arc | Functional | P2 | Create a arc; apply extend. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0204 | extend on circle | Negative | P2 | Create a circle; apply extend. | Operation not offered for this entity (message). |  |
| SKT-0205 | extend on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply extend. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0206 | extend on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply extend. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0207 | offset 5 mm on line | Functional | P2 | Create a line; apply offset 5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0208 | offset 5 mm on arc | Functional | P2 | Create a arc; apply offset 5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0209 | offset 5 mm on circle | Functional | P2 | Create a circle; apply offset 5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0210 | offset 5 mm on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply offset 5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0211 | offset 5 mm on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply offset 5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0212 | offset -5 mm on line | Functional | P2 | Create a line; apply offset -5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0213 | offset -5 mm on arc | Functional | P2 | Create a arc; apply offset -5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0214 | offset -5 mm on circle | Functional | P2 | Create a circle; apply offset -5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0215 | offset -5 mm on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply offset -5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0216 | offset -5 mm on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply offset -5 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0217 | mirror about axis on line | Functional | P2 | Create a line; apply mirror about axis. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0218 | mirror about axis on arc | Functional | P2 | Create a arc; apply mirror about axis. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0219 | mirror about axis on circle | Functional | P2 | Create a circle; apply mirror about axis. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0220 | mirror about axis on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply mirror about axis. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0221 | mirror about axis on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply mirror about axis. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0222 | corner fillet r=3 on line | Functional | P2 | Create a line; apply corner fillet r=3. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0223 | corner fillet r=3 on arc | Functional | P2 | Create a arc; apply corner fillet r=3. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0224 | corner fillet r=3 on circle | Negative | P2 | Create a circle; apply corner fillet r=3. | Operation not offered for this entity (message). |  |
| SKT-0225 | corner fillet r=3 on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply corner fillet r=3. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0226 | corner fillet r=3 on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply corner fillet r=3. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0227 | chamfer 2 mm on line | Functional | P2 | Create a line; apply chamfer 2 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0228 | chamfer 2 mm on arc | Negative | P2 | Create a arc; apply chamfer 2 mm. | Operation not offered for this entity (message). |  |
| SKT-0229 | chamfer 2 mm on circle | Negative | P2 | Create a circle; apply chamfer 2 mm. | Operation not offered for this entity (message). |  |
| SKT-0230 | chamfer 2 mm on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply chamfer 2 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0231 | chamfer 2 mm on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply chamfer 2 mm. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0232 | split at point on line | Functional | P2 | Create a line; apply split at point. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0233 | split at point on arc | Functional | P2 | Create a arc; apply split at point. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0234 | split at point on circle | Functional | P2 | Create a circle; apply split at point. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0235 | split at point on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply split at point. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0236 | split at point on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply split at point. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0237 | project 3D edge on line | Functional | P2 | Create a line; apply project 3D edge. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0238 | project 3D edge on arc | Functional | P2 | Create a arc; apply project 3D edge. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0239 | project 3D edge on circle | Functional | P2 | Create a circle; apply project 3D edge. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0240 | project 3D edge on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply project 3D edge. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0241 | project 3D edge on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply project 3D edge. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0242 | intersect with 3D face on line | Functional | P2 | Create a line; apply intersect with 3D face. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0243 | intersect with 3D face on arc | Functional | P2 | Create a arc; apply intersect with 3D face. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0244 | intersect with 3D face on circle | Functional | P2 | Create a circle; apply intersect with 3D face. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0245 | intersect with 3D face on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply intersect with 3D face. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0246 | intersect with 3D face on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply intersect with 3D face. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0247 | convert to spline on line | Functional | P2 | Create a line; apply convert to spline. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0248 | convert to spline on arc | Functional | P2 | Create a arc; apply convert to spline. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0249 | convert to spline on circle | Functional | P2 | Create a circle; apply convert to spline. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0250 | convert to spline on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply convert to spline. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0251 | convert to spline on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply convert to spline. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0252 | rotate 30° on line | Functional | P2 | Create a line; apply rotate 30°. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0253 | rotate 30° on arc | Functional | P2 | Create a arc; apply rotate 30°. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0254 | rotate 30° on circle | Functional | P2 | Create a circle; apply rotate 30°. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0255 | rotate 30° on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply rotate 30°. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0256 | rotate 30° on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply rotate 30°. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0257 | scale ×2 on line | Functional | P2 | Create a line; apply scale ×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0258 | scale ×2 on arc | Functional | P2 | Create a arc; apply scale ×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0259 | scale ×2 on circle | Functional | P2 | Create a circle; apply scale ×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0260 | scale ×2 on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply scale ×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0261 | scale ×2 on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply scale ×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0262 | translate 10,5 on line | Functional | P2 | Create a line; apply translate 10,5. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0263 | translate 10,5 on arc | Functional | P2 | Create a arc; apply translate 10,5. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0264 | translate 10,5 on circle | Functional | P2 | Create a circle; apply translate 10,5. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0265 | translate 10,5 on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply translate 10,5. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0266 | translate 10,5 on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply translate 10,5. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0267 | rectangular pattern 3×2 on line | Functional | P2 | Create a line; apply rectangular pattern 3×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0268 | rectangular pattern 3×2 on arc | Functional | P2 | Create a arc; apply rectangular pattern 3×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0269 | rectangular pattern 3×2 on circle | Functional | P2 | Create a circle; apply rectangular pattern 3×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0270 | rectangular pattern 3×2 on spline (4 poles) | Functional | P2 | Create a spline (4 poles); apply rectangular pattern 3×2. | Result geometry correct; dependent constraints updated or reported broken. |  |
| SKT-0271 | rectangular pattern 3×2 on polyline (5 segments) | Functional | P2 | Create a polyline (5 segments); apply rectangular pattern 3×2. | Result geometry correct; dependent constraints updated or reported broken. |  |

## Profile validation

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| SKT-0272 | Pad from closed rectangle | Functional | P1 | Sketch a closed rectangle; use it for Pad. | Accepted (1 outer loop). |  |
| SKT-0273 | Pocket from closed rectangle | Functional | P1 | Sketch a closed rectangle; use it for Pocket. | Accepted (1 outer loop). |  |
| SKT-0274 | Shaft from closed rectangle | Functional | P1 | Sketch a closed rectangle; use it for Shaft. | Accepted (1 outer loop). |  |
| SKT-0275 | Rib section from closed rectangle | Functional | P1 | Sketch a closed rectangle; use it for Rib section. | Accepted (1 outer loop). |  |
| SKT-0276 | Pad from open polyline | Negative | P1 | Sketch a open polyline; use it for Pad. | Rejected before build: open profile; offending elements highlighted. |  |
| SKT-0277 | Pocket from open polyline | Negative | P1 | Sketch a open polyline; use it for Pocket. | Rejected before build: open profile; offending elements highlighted. |  |
| SKT-0278 | Shaft from open polyline | Negative | P1 | Sketch a open polyline; use it for Shaft. | Rejected before build: open profile; offending elements highlighted. |  |
| SKT-0279 | Rib section from open polyline | Negative | P1 | Sketch a open polyline; use it for Rib section. | Rejected before build: open profile; offending elements highlighted. |  |
| SKT-0280 | Pad from figure-eight (self-intersecting) | Negative | P1 | Sketch a figure-eight (self-intersecting); use it for Pad. | Rejected before build: self-intersection at one point; offending elements highlighted. |  |
| SKT-0281 | Pocket from figure-eight (self-intersecting) | Negative | P1 | Sketch a figure-eight (self-intersecting); use it for Pocket. | Rejected before build: self-intersection at one point; offending elements highlighted. |  |
| SKT-0282 | Shaft from figure-eight (self-intersecting) | Negative | P1 | Sketch a figure-eight (self-intersecting); use it for Shaft. | Rejected before build: self-intersection at one point; offending elements highlighted. |  |
| SKT-0283 | Rib section from figure-eight (self-intersecting) | Negative | P1 | Sketch a figure-eight (self-intersecting); use it for Rib section. | Rejected before build: self-intersection at one point; offending elements highlighted. |  |
| SKT-0284 | Pad from rectangle with a circular island | Functional | P1 | Sketch a rectangle with a circular island; use it for Pad. | Accepted (outer + 1 inner loop → pocketed face). |  |
| SKT-0285 | Pocket from rectangle with a circular island | Functional | P1 | Sketch a rectangle with a circular island; use it for Pocket. | Accepted (outer + 1 inner loop → pocketed face). |  |
| SKT-0286 | Shaft from rectangle with a circular island | Functional | P1 | Sketch a rectangle with a circular island; use it for Shaft. | Accepted (outer + 1 inner loop → pocketed face). |  |
| SKT-0287 | Rib section from rectangle with a circular island | Functional | P1 | Sketch a rectangle with a circular island; use it for Rib section. | Accepted (outer + 1 inner loop → pocketed face). |  |
| SKT-0288 | Pad from two disjoint rectangles | Functional | P1 | Sketch a two disjoint rectangles; use it for Pad. | Accepted (2 outer loops → multi-body pad or single body per option). |  |
| SKT-0289 | Pocket from two disjoint rectangles | Functional | P1 | Sketch a two disjoint rectangles; use it for Pocket. | Accepted (2 outer loops → multi-body pad or single body per option). |  |
| SKT-0290 | Shaft from two disjoint rectangles | Functional | P1 | Sketch a two disjoint rectangles; use it for Shaft. | Accepted (2 outer loops → multi-body pad or single body per option). |  |
| SKT-0291 | Rib section from two disjoint rectangles | Functional | P1 | Sketch a two disjoint rectangles; use it for Rib section. | Accepted (2 outer loops → multi-body pad or single body per option). |  |
| SKT-0292 | Pad from nested 3 levels (ring in ring in ring) | Functional | P1 | Sketch a nested 3 levels (ring in ring in ring); use it for Pad. | Accepted (alternating material regions). |  |
| SKT-0293 | Pocket from nested 3 levels (ring in ring in ring) | Functional | P1 | Sketch a nested 3 levels (ring in ring in ring); use it for Pocket. | Accepted (alternating material regions). |  |
| SKT-0294 | Shaft from nested 3 levels (ring in ring in ring) | Functional | P1 | Sketch a nested 3 levels (ring in ring in ring); use it for Shaft. | Accepted (alternating material regions). |  |
| SKT-0295 | Rib section from nested 3 levels (ring in ring in ring) | Functional | P1 | Sketch a nested 3 levels (ring in ring in ring); use it for Rib section. | Accepted (alternating material regions). |  |
| SKT-0296 | Pad from two rectangles sharing an edge | Negative | P1 | Sketch a two rectangles sharing an edge; use it for Pad. | Rejected before build: non-manifold shared edge; offending elements highlighted. |  |
| SKT-0297 | Pocket from two rectangles sharing an edge | Negative | P1 | Sketch a two rectangles sharing an edge; use it for Pocket. | Rejected before build: non-manifold shared edge; offending elements highlighted. |  |
| SKT-0298 | Shaft from two rectangles sharing an edge | Negative | P1 | Sketch a two rectangles sharing an edge; use it for Shaft. | Rejected before build: non-manifold shared edge; offending elements highlighted. |  |
| SKT-0299 | Rib section from two rectangles sharing an edge | Negative | P1 | Sketch a two rectangles sharing an edge; use it for Rib section. | Rejected before build: non-manifold shared edge; offending elements highlighted. |  |
| SKT-0300 | Pad from circle tangent to a line inside a rectangle | Negative | P1 | Sketch a circle tangent to a line inside a rectangle; use it for Pad. | Rejected before build: touching islands; offending elements highlighted. |  |
| SKT-0301 | Pocket from circle tangent to a line inside a rectangle | Negative | P1 | Sketch a circle tangent to a line inside a rectangle; use it for Pocket. | Rejected before build: touching islands; offending elements highlighted. |  |
| SKT-0302 | Shaft from circle tangent to a line inside a rectangle | Negative | P1 | Sketch a circle tangent to a line inside a rectangle; use it for Shaft. | Rejected before build: touching islands; offending elements highlighted. |  |
| SKT-0303 | Rib section from circle tangent to a line inside a rectangle | Negative | P1 | Sketch a circle tangent to a line inside a rectangle; use it for Rib section. | Rejected before build: touching islands; offending elements highlighted. |  |
| SKT-0304 | Pad from loop with a 1e-4 mm gap | Negative | P1 | Sketch a loop with a 1e-4 mm gap; use it for Pad. | Rejected before build: gap above 1e-6 tolerance; offending elements highlighted. |  |
| SKT-0305 | Pocket from loop with a 1e-4 mm gap | Negative | P1 | Sketch a loop with a 1e-4 mm gap; use it for Pocket. | Rejected before build: gap above 1e-6 tolerance; offending elements highlighted. |  |
| SKT-0306 | Shaft from loop with a 1e-4 mm gap | Negative | P1 | Sketch a loop with a 1e-4 mm gap; use it for Shaft. | Rejected before build: gap above 1e-6 tolerance; offending elements highlighted. |  |
| SKT-0307 | Rib section from loop with a 1e-4 mm gap | Negative | P1 | Sketch a loop with a 1e-4 mm gap; use it for Rib section. | Rejected before build: gap above 1e-6 tolerance; offending elements highlighted. |  |
| SKT-0308 | Pad from loop with a 1e-8 mm gap | Functional | P1 | Sketch a loop with a 1e-8 mm gap; use it for Pad. | Accepted (gap healed under tolerance). |  |
| SKT-0309 | Pocket from loop with a 1e-8 mm gap | Functional | P1 | Sketch a loop with a 1e-8 mm gap; use it for Pocket. | Accepted (gap healed under tolerance). |  |
| SKT-0310 | Shaft from loop with a 1e-8 mm gap | Functional | P1 | Sketch a loop with a 1e-8 mm gap; use it for Shaft. | Accepted (gap healed under tolerance). |  |
| SKT-0311 | Rib section from loop with a 1e-8 mm gap | Functional | P1 | Sketch a loop with a 1e-8 mm gap; use it for Rib section. | Accepted (gap healed under tolerance). |  |
| SKT-0312 | Pad from rectangle with a dangling line | Negative | P1 | Sketch a rectangle with a dangling line; use it for Pad. | Rejected before build: dangling element; offending elements highlighted. |  |
| SKT-0313 | Pocket from rectangle with a dangling line | Negative | P1 | Sketch a rectangle with a dangling line; use it for Pocket. | Rejected before build: dangling element; offending elements highlighted. |  |
| SKT-0314 | Shaft from rectangle with a dangling line | Negative | P1 | Sketch a rectangle with a dangling line; use it for Shaft. | Rejected before build: dangling element; offending elements highlighted. |  |
| SKT-0315 | Rib section from rectangle with a dangling line | Negative | P1 | Sketch a rectangle with a dangling line; use it for Rib section. | Rejected before build: dangling element; offending elements highlighted. |  |
| SKT-0316 | Pad from spline closed on itself | Functional | P1 | Sketch a spline closed on itself; use it for Pad. | Accepted (single closed loop). |  |
| SKT-0317 | Pocket from spline closed on itself | Functional | P1 | Sketch a spline closed on itself; use it for Pocket. | Accepted (single closed loop). |  |
| SKT-0318 | Shaft from spline closed on itself | Functional | P1 | Sketch a spline closed on itself; use it for Shaft. | Accepted (single closed loop). |  |
| SKT-0319 | Rib section from spline closed on itself | Functional | P1 | Sketch a spline closed on itself; use it for Rib section. | Accepted (single closed loop). |  |
