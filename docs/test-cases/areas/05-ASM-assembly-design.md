# ASM — Assembly Design

**CATIA-class equivalent:** Assembly Design / Product Structure  
**Autevra workspace:** Assembly; Inventory; Breakdown  
**Scope:** Shared  
**Cases:** 216 (Have 82, Partial 134, Gap 0)

Product structure, constraints, instances, replacement and assembly-level operations.

[← Back to the index](../README.md)

## Features

- Assembly constraints — 80 cases (Partial)
- Product structure — 54 cases (Partial)
- Interfaces and mates (Autevra model) — 50 cases (Have)
- Bill of materials — 32 cases (Have)

## Assembly constraints

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ASM-0001 | coincidence (axis-axis) on bolt + hole | Functional | P1 | Insert bolt + hole; apply coincidence (axis-axis); update. | Constraint satisfied (<1e-6 mm/1e-6°); 4 DOF removed; remaining DOF shown. |  |
| ASM-0002 | coincidence (axis-axis) on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply coincidence (axis-axis); update. | Constraint satisfied (<1e-6 mm/1e-6°); 4 DOF removed; remaining DOF shown. |  |
| ASM-0003 | coincidence (axis-axis) on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply coincidence (axis-axis); update. | Constraint satisfied (<1e-6 mm/1e-6°); 4 DOF removed; remaining DOF shown. |  |
| ASM-0004 | coincidence (axis-axis) on wheel + hub | Functional | P1 | Insert wheel + hub; apply coincidence (axis-axis); update. | Constraint satisfied (<1e-6 mm/1e-6°); 4 DOF removed; remaining DOF shown. |  |
| ASM-0005 | coincidence (axis-axis) on panel + panel | Functional | P1 | Insert panel + panel; apply coincidence (axis-axis); update. | Constraint satisfied (<1e-6 mm/1e-6°); 4 DOF removed; remaining DOF shown. |  |
| ASM-0006 | coincidence (plane-plane) on bolt + hole | Functional | P1 | Insert bolt + hole; apply coincidence (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0007 | coincidence (plane-plane) on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply coincidence (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0008 | coincidence (plane-plane) on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply coincidence (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0009 | coincidence (plane-plane) on wheel + hub | Functional | P1 | Insert wheel + hub; apply coincidence (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0010 | coincidence (plane-plane) on panel + panel | Functional | P1 | Insert panel + panel; apply coincidence (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0011 | contact (face-face) on bolt + hole | Functional | P1 | Insert bolt + hole; apply contact (face-face); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0012 | contact (face-face) on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply contact (face-face); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0013 | contact (face-face) on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply contact (face-face); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0014 | contact (face-face) on wheel + hub | Functional | P1 | Insert wheel + hub; apply contact (face-face); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0015 | contact (face-face) on panel + panel | Functional | P1 | Insert panel + panel; apply contact (face-face); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0016 | offset 10 mm (plane-plane) on bolt + hole | Functional | P1 | Insert bolt + hole; apply offset 10 mm (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0017 | offset 10 mm (plane-plane) on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply offset 10 mm (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0018 | offset 10 mm (plane-plane) on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply offset 10 mm (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0019 | offset 10 mm (plane-plane) on wheel + hub | Functional | P1 | Insert wheel + hub; apply offset 10 mm (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0020 | offset 10 mm (plane-plane) on panel + panel | Functional | P1 | Insert panel + panel; apply offset 10 mm (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0021 | angle 30° (plane-plane) on bolt + hole | Functional | P1 | Insert bolt + hole; apply angle 30° (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0022 | angle 30° (plane-plane) on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply angle 30° (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0023 | angle 30° (plane-plane) on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply angle 30° (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0024 | angle 30° (plane-plane) on wheel + hub | Functional | P1 | Insert wheel + hub; apply angle 30° (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0025 | angle 30° (plane-plane) on panel + panel | Functional | P1 | Insert panel + panel; apply angle 30° (plane-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0026 | parallel on bolt + hole | Functional | P1 | Insert bolt + hole; apply parallel; update. | Constraint satisfied (<1e-6 mm/1e-6°); 2 DOF removed; remaining DOF shown. |  |
| ASM-0027 | parallel on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply parallel; update. | Constraint satisfied (<1e-6 mm/1e-6°); 2 DOF removed; remaining DOF shown. |  |
| ASM-0028 | parallel on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply parallel; update. | Constraint satisfied (<1e-6 mm/1e-6°); 2 DOF removed; remaining DOF shown. |  |
| ASM-0029 | parallel on wheel + hub | Functional | P1 | Insert wheel + hub; apply parallel; update. | Constraint satisfied (<1e-6 mm/1e-6°); 2 DOF removed; remaining DOF shown. |  |
| ASM-0030 | parallel on panel + panel | Functional | P1 | Insert panel + panel; apply parallel; update. | Constraint satisfied (<1e-6 mm/1e-6°); 2 DOF removed; remaining DOF shown. |  |
| ASM-0031 | perpendicular on bolt + hole | Functional | P1 | Insert bolt + hole; apply perpendicular; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0032 | perpendicular on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply perpendicular; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0033 | perpendicular on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply perpendicular; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0034 | perpendicular on wheel + hub | Functional | P1 | Insert wheel + hub; apply perpendicular; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0035 | perpendicular on panel + panel | Functional | P1 | Insert panel + panel; apply perpendicular; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0036 | fix on bolt + hole | Functional | P1 | Insert bolt + hole; apply fix; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0037 | fix on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply fix; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0038 | fix on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply fix; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0039 | fix on wheel + hub | Functional | P1 | Insert wheel + hub; apply fix; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0040 | fix on panel + panel | Functional | P1 | Insert panel + panel; apply fix; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0041 | fix together on bolt + hole | Functional | P1 | Insert bolt + hole; apply fix together; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0042 | fix together on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply fix together; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0043 | fix together on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply fix together; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0044 | fix together on wheel + hub | Functional | P1 | Insert wheel + hub; apply fix together; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0045 | fix together on panel + panel | Functional | P1 | Insert panel + panel; apply fix together; update. | Constraint satisfied (<1e-6 mm/1e-6°); 6 DOF removed; remaining DOF shown. |  |
| ASM-0046 | tangent (cyl-plane) on bolt + hole | Functional | P1 | Insert bolt + hole; apply tangent (cyl-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0047 | tangent (cyl-plane) on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply tangent (cyl-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0048 | tangent (cyl-plane) on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply tangent (cyl-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0049 | tangent (cyl-plane) on wheel + hub | Functional | P1 | Insert wheel + hub; apply tangent (cyl-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0050 | tangent (cyl-plane) on panel + panel | Functional | P1 | Insert panel + panel; apply tangent (cyl-plane); update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0051 | point on plane on bolt + hole | Functional | P1 | Insert bolt + hole; apply point on plane; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0052 | point on plane on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply point on plane; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0053 | point on plane on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply point on plane; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0054 | point on plane on wheel + hub | Functional | P1 | Insert wheel + hub; apply point on plane; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0055 | point on plane on panel + panel | Functional | P1 | Insert panel + panel; apply point on plane; update. | Constraint satisfied (<1e-6 mm/1e-6°); 1 DOF removed; remaining DOF shown. |  |
| ASM-0056 | point-point on bolt + hole | Functional | P1 | Insert bolt + hole; apply point-point; update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0057 | point-point on shaft + bearing | Functional | P1 | Insert shaft + bearing; apply point-point; update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0058 | point-point on bracket + frame rail | Functional | P1 | Insert bracket + frame rail; apply point-point; update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0059 | point-point on wheel + hub | Functional | P1 | Insert wheel + hub; apply point-point; update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0060 | point-point on panel + panel | Functional | P1 | Insert panel + panel; apply point-point; update. | Constraint satisfied (<1e-6 mm/1e-6°); 3 DOF removed; remaining DOF shown. |  |
| ASM-0061 | Constraint management: circular constraint loop (variant 1) | Regression | P2 | Set up: circular constraint loop. | Detected and reported. |  |
| ASM-0062 | Constraint management: circular constraint loop (variant 2) | Regression | P2 | Set up: circular constraint loop. | Detected and reported. |  |
| ASM-0063 | Constraint management: circular constraint loop (variant 3) | Regression | P2 | Set up: circular constraint loop. | Detected and reported. |  |
| ASM-0064 | Constraint management: circular constraint loop (variant 4) | Regression | P2 | Set up: circular constraint loop. | Detected and reported. |  |
| ASM-0065 | Constraint management: conflicting offset 10 vs contact (variant 1) | Regression | P2 | Set up: conflicting offset 10 vs contact. | Conflict highlighted; last good position kept. |  |
| ASM-0066 | Constraint management: conflicting offset 10 vs contact (variant 2) | Regression | P2 | Set up: conflicting offset 10 vs contact. | Conflict highlighted; last good position kept. |  |
| ASM-0067 | Constraint management: conflicting offset 10 vs contact (variant 3) | Regression | P2 | Set up: conflicting offset 10 vs contact. | Conflict highlighted; last good position kept. |  |
| ASM-0068 | Constraint management: conflicting offset 10 vs contact (variant 4) | Regression | P2 | Set up: conflicting offset 10 vs contact. | Conflict highlighted; last good position kept. |  |
| ASM-0069 | Constraint management: constraint to a deleted face (variant 1) | Regression | P2 | Set up: constraint to a deleted face. | Broken reference flagged; re-route offered. |  |
| ASM-0070 | Constraint management: constraint to a deleted face (variant 2) | Regression | P2 | Set up: constraint to a deleted face. | Broken reference flagged; re-route offered. |  |
| ASM-0071 | Constraint management: constraint to a deleted face (variant 3) | Regression | P2 | Set up: constraint to a deleted face. | Broken reference flagged; re-route offered. |  |
| ASM-0072 | Constraint management: constraint to a deleted face (variant 4) | Regression | P2 | Set up: constraint to a deleted face. | Broken reference flagged; re-route offered. |  |
| ASM-0073 | Constraint management: update 500 constraints (variant 1) | Regression | P2 | Set up: update 500 constraints. | < 2 s. |  |
| ASM-0074 | Constraint management: update 500 constraints (variant 2) | Regression | P2 | Set up: update 500 constraints. | < 2 s. |  |
| ASM-0075 | Constraint management: update 500 constraints (variant 3) | Regression | P2 | Set up: update 500 constraints. | < 2 s. |  |
| ASM-0076 | Constraint management: update 500 constraints (variant 4) | Regression | P2 | Set up: update 500 constraints. | < 2 s. |  |
| ASM-0077 | Constraint management: flexible sub-assembly (variant 1) | Regression | P2 | Set up: flexible sub-assembly. | Child moves inside parent. |  |
| ASM-0078 | Constraint management: flexible sub-assembly (variant 2) | Regression | P2 | Set up: flexible sub-assembly. | Child moves inside parent. |  |
| ASM-0079 | Constraint management: flexible sub-assembly (variant 3) | Regression | P2 | Set up: flexible sub-assembly. | Child moves inside parent. |  |
| ASM-0080 | Constraint management: flexible sub-assembly (variant 4) | Regression | P2 | Set up: flexible sub-assembly. | Child moves inside parent. |  |

## Product structure

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ASM-0081 | insert existing part (5 parts) | Functional | P2 | In an assembly of 5 parts: insert existing part. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0082 | insert existing part (50 parts) | Functional | P2 | In an assembly of 50 parts: insert existing part. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0083 | insert existing part (500 parts) | Performance | P2 | In an assembly of 500 parts: insert existing part. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0084 | insert new part (5 parts) | Functional | P2 | In an assembly of 5 parts: insert new part. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0085 | insert new part (50 parts) | Functional | P2 | In an assembly of 50 parts: insert new part. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0086 | insert new part (500 parts) | Performance | P2 | In an assembly of 500 parts: insert new part. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0087 | insert sub-assembly (5 parts) | Functional | P2 | In an assembly of 5 parts: insert sub-assembly. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0088 | insert sub-assembly (50 parts) | Functional | P2 | In an assembly of 50 parts: insert sub-assembly. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0089 | insert sub-assembly (500 parts) | Performance | P2 | In an assembly of 500 parts: insert sub-assembly. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0090 | multi-instantiate ×8 (5 parts) | Functional | P2 | In an assembly of 5 parts: multi-instantiate ×8. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0091 | multi-instantiate ×8 (50 parts) | Functional | P2 | In an assembly of 50 parts: multi-instantiate ×8. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0092 | multi-instantiate ×8 (500 parts) | Performance | P2 | In an assembly of 500 parts: multi-instantiate ×8. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0093 | reuse pattern from part (5 parts) | Functional | P2 | In an assembly of 5 parts: reuse pattern from part. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0094 | reuse pattern from part (50 parts) | Functional | P2 | In an assembly of 50 parts: reuse pattern from part. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0095 | reuse pattern from part (500 parts) | Performance | P2 | In an assembly of 500 parts: reuse pattern from part. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0096 | replace component (same interfaces) (5 parts) | Functional | P2 | In an assembly of 5 parts: replace component (same interfaces). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0097 | replace component (same interfaces) (50 parts) | Functional | P2 | In an assembly of 50 parts: replace component (same interfaces). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0098 | replace component (same interfaces) (500 parts) | Performance | P2 | In an assembly of 500 parts: replace component (same interfaces). | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0099 | replace component (different interfaces) (5 parts) | Functional | P2 | In an assembly of 5 parts: replace component (different interfaces). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0100 | replace component (different interfaces) (50 parts) | Functional | P2 | In an assembly of 50 parts: replace component (different interfaces). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0101 | replace component (different interfaces) (500 parts) | Performance | P2 | In an assembly of 500 parts: replace component (different interfaces). | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0102 | graph tree reordering (5 parts) | Functional | P2 | In an assembly of 5 parts: graph tree reordering. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0103 | graph tree reordering (50 parts) | Functional | P2 | In an assembly of 50 parts: graph tree reordering. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0104 | graph tree reordering (500 parts) | Performance | P2 | In an assembly of 500 parts: graph tree reordering. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0105 | generate numbering (5 parts) | Functional | P2 | In an assembly of 5 parts: generate numbering. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0106 | generate numbering (50 parts) | Functional | P2 | In an assembly of 50 parts: generate numbering. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0107 | generate numbering (500 parts) | Performance | P2 | In an assembly of 500 parts: generate numbering. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0108 | load/unload component (5 parts) | Functional | P2 | In an assembly of 5 parts: load/unload component. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0109 | load/unload component (50 parts) | Functional | P2 | In an assembly of 50 parts: load/unload component. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0110 | load/unload component (500 parts) | Performance | P2 | In an assembly of 500 parts: load/unload component. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0111 | hide/show (5 parts) | Functional | P2 | In an assembly of 5 parts: hide/show. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0112 | hide/show (50 parts) | Functional | P2 | In an assembly of 50 parts: hide/show. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0113 | hide/show (500 parts) | Performance | P2 | In an assembly of 500 parts: hide/show. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0114 | isolate (5 parts) | Functional | P2 | In an assembly of 5 parts: isolate. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0115 | isolate (50 parts) | Functional | P2 | In an assembly of 50 parts: isolate. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0116 | isolate (500 parts) | Performance | P2 | In an assembly of 500 parts: isolate. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0117 | cut/paste between assemblies (5 parts) | Functional | P2 | In an assembly of 5 parts: cut/paste between assemblies. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0118 | cut/paste between assemblies (50 parts) | Functional | P2 | In an assembly of 50 parts: cut/paste between assemblies. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0119 | cut/paste between assemblies (500 parts) | Performance | P2 | In an assembly of 500 parts: cut/paste between assemblies. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0120 | symmetry (mirror a sub-assembly) (5 parts) | Functional | P2 | In an assembly of 5 parts: symmetry (mirror a sub-assembly). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0121 | symmetry (mirror a sub-assembly) (50 parts) | Functional | P2 | In an assembly of 50 parts: symmetry (mirror a sub-assembly). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0122 | symmetry (mirror a sub-assembly) (500 parts) | Performance | P2 | In an assembly of 500 parts: symmetry (mirror a sub-assembly). | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0123 | manipulate with compass (5 parts) | Functional | P2 | In an assembly of 5 parts: manipulate with compass. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0124 | manipulate with compass (50 parts) | Functional | P2 | In an assembly of 50 parts: manipulate with compass. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0125 | manipulate with compass (500 parts) | Performance | P2 | In an assembly of 500 parts: manipulate with compass. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0126 | snap to axis (5 parts) | Functional | P2 | In an assembly of 5 parts: snap to axis. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0127 | snap to axis (50 parts) | Functional | P2 | In an assembly of 50 parts: snap to axis. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0128 | snap to axis (500 parts) | Performance | P2 | In an assembly of 500 parts: snap to axis. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0129 | explode (scenes) (5 parts) | Functional | P2 | In an assembly of 5 parts: explode (scenes). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0130 | explode (scenes) (50 parts) | Functional | P2 | In an assembly of 50 parts: explode (scenes). | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0131 | explode (scenes) (500 parts) | Performance | P2 | In an assembly of 500 parts: explode (scenes). | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |
| ASM-0132 | save as new revision (5 parts) | Functional | P2 | In an assembly of 5 parts: save as new revision. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0133 | save as new revision (50 parts) | Functional | P2 | In an assembly of 50 parts: save as new revision. | Result correct; tree and 3D in sync; undo restores the prior state. |  |
| ASM-0134 | save as new revision (500 parts) | Performance | P2 | In an assembly of 500 parts: save as new revision. | Result correct; tree and 3D in sync; undo restores the prior state. Completes < 3 s. |  |

## Interfaces and mates (Autevra model)

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ASM-0135 | Impact of wheelbase on body | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether body rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0136 | Impact of front track on body | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether body rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0137 | Impact of ground clearance on body | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether body rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0138 | Impact of tyre width on body | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether body rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0139 | Impact of rim diameter on body | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether body rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0140 | Impact of wheelbase on frame | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether frame rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0141 | Impact of front track on frame | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether frame rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0142 | Impact of ground clearance on frame | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether frame rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0143 | Impact of tyre width on frame | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether frame rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0144 | Impact of rim diameter on frame | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether frame rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0145 | Impact of wheelbase on front axle | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether front axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0146 | Impact of front track on front axle | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether front axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0147 | Impact of ground clearance on front axle | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether front axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0148 | Impact of tyre width on front axle | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether front axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0149 | Impact of rim diameter on front axle | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether front axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0150 | Impact of wheelbase on rear axle | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether rear axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0151 | Impact of front track on rear axle | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether rear axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0152 | Impact of ground clearance on rear axle | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether rear axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0153 | Impact of tyre width on rear axle | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether rear axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0154 | Impact of rim diameter on rear axle | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether rear axle rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0155 | Impact of wheelbase on wheel FL | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether wheel FL rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0156 | Impact of front track on wheel FL | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether wheel FL rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0157 | Impact of ground clearance on wheel FL | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether wheel FL rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0158 | Impact of tyre width on wheel FL | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether wheel FL rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0159 | Impact of rim diameter on wheel FL | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether wheel FL rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0160 | Impact of wheelbase on wheel RR | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether wheel RR rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0161 | Impact of front track on wheel RR | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether wheel RR rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0162 | Impact of ground clearance on wheel RR | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether wheel RR rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0163 | Impact of tyre width on wheel RR | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether wheel RR rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0164 | Impact of rim diameter on wheel RR | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether wheel RR rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0165 | Impact of wheelbase on damper | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether damper rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0166 | Impact of front track on damper | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether damper rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0167 | Impact of ground clearance on damper | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether damper rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0168 | Impact of tyre width on damper | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether damper rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0169 | Impact of rim diameter on damper | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether damper rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0170 | Impact of wheelbase on engine | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether engine rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0171 | Impact of front track on engine | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether engine rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0172 | Impact of ground clearance on engine | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether engine rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0173 | Impact of tyre width on engine | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether engine rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0174 | Impact of rim diameter on engine | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether engine rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0175 | Impact of wheelbase on battery pack | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether battery pack rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0176 | Impact of front track on battery pack | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether battery pack rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0177 | Impact of ground clearance on battery pack | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether battery pack rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0178 | Impact of tyre width on battery pack | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether battery pack rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0179 | Impact of rim diameter on battery pack | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether battery pack rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0180 | Impact of wheelbase on seat row 2 | Functional | P2 | Preview a +50 mm (or +1 size) change of wheelbase. | Impact report says whether seat row 2 rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0181 | Impact of front track on seat row 2 | Functional | P2 | Preview a +50 mm (or +1 size) change of front track. | Impact report says whether seat row 2 rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0182 | Impact of ground clearance on seat row 2 | Functional | P2 | Preview a +50 mm (or +1 size) change of ground clearance. | Impact report says whether seat row 2 rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0183 | Impact of tyre width on seat row 2 | Functional | P2 | Preview a +50 mm (or +1 size) change of tyre width. | Impact report says whether seat row 2 rebuilds, moves or is unaffected, per declared dependencies. |  |
| ASM-0184 | Impact of rim diameter on seat row 2 | Functional | P2 | Preview a +50 mm (or +1 size) change of rim diameter. | Impact report says whether seat row 2 rebuilds, moves or is unaffected, per declared dependencies. |  |

## Bill of materials

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| ASM-0185 | BOM flat: part number | Functional | P2 | Generate the flat BOM. | 'part number' column correct; CSV export matches. |  |
| ASM-0186 | BOM indented: part number | Functional | P2 | Generate the indented BOM. | 'part number' column correct; CSV export matches. |  |
| ASM-0187 | BOM after multi-instancing: part number | Functional | P2 | Generate the after multi-instancing BOM. | 'part number' column correct; CSV export matches. |  |
| ASM-0188 | BOM after replace: part number | Functional | P2 | Generate the after replace BOM. | 'part number' column correct; CSV export matches. |  |
| ASM-0189 | BOM flat: quantity | Functional | P2 | Generate the flat BOM. | 'quantity' column correct; CSV export matches. |  |
| ASM-0190 | BOM indented: quantity | Functional | P2 | Generate the indented BOM. | 'quantity' column correct; CSV export matches. |  |
| ASM-0191 | BOM after multi-instancing: quantity | Functional | P2 | Generate the after multi-instancing BOM. | 'quantity' column correct; CSV export matches. |  |
| ASM-0192 | BOM after replace: quantity | Functional | P2 | Generate the after replace BOM. | 'quantity' column correct; CSV export matches. |  |
| ASM-0193 | BOM flat: mass | Functional | P2 | Generate the flat BOM. | 'mass' column correct; CSV export matches. |  |
| ASM-0194 | BOM indented: mass | Functional | P2 | Generate the indented BOM. | 'mass' column correct; CSV export matches. |  |
| ASM-0195 | BOM after multi-instancing: mass | Functional | P2 | Generate the after multi-instancing BOM. | 'mass' column correct; CSV export matches. |  |
| ASM-0196 | BOM after replace: mass | Functional | P2 | Generate the after replace BOM. | 'mass' column correct; CSV export matches. |  |
| ASM-0197 | BOM flat: material | Functional | P2 | Generate the flat BOM. | 'material' column correct; CSV export matches. |  |
| ASM-0198 | BOM indented: material | Functional | P2 | Generate the indented BOM. | 'material' column correct; CSV export matches. |  |
| ASM-0199 | BOM after multi-instancing: material | Functional | P2 | Generate the after multi-instancing BOM. | 'material' column correct; CSV export matches. |  |
| ASM-0200 | BOM after replace: material | Functional | P2 | Generate the after replace BOM. | 'material' column correct; CSV export matches. |  |
| ASM-0201 | BOM flat: volume | Functional | P2 | Generate the flat BOM. | 'volume' column correct; CSV export matches. |  |
| ASM-0202 | BOM indented: volume | Functional | P2 | Generate the indented BOM. | 'volume' column correct; CSV export matches. |  |
| ASM-0203 | BOM after multi-instancing: volume | Functional | P2 | Generate the after multi-instancing BOM. | 'volume' column correct; CSV export matches. |  |
| ASM-0204 | BOM after replace: volume | Functional | P2 | Generate the after replace BOM. | 'volume' column correct; CSV export matches. |  |
| ASM-0205 | BOM flat: size | Functional | P2 | Generate the flat BOM. | 'size' column correct; CSV export matches. |  |
| ASM-0206 | BOM indented: size | Functional | P2 | Generate the indented BOM. | 'size' column correct; CSV export matches. |  |
| ASM-0207 | BOM after multi-instancing: size | Functional | P2 | Generate the after multi-instancing BOM. | 'size' column correct; CSV export matches. |  |
| ASM-0208 | BOM after replace: size | Functional | P2 | Generate the after replace BOM. | 'size' column correct; CSV export matches. |  |
| ASM-0209 | BOM flat: revision | Functional | P2 | Generate the flat BOM. | 'revision' column correct; CSV export matches. |  |
| ASM-0210 | BOM indented: revision | Functional | P2 | Generate the indented BOM. | 'revision' column correct; CSV export matches. |  |
| ASM-0211 | BOM after multi-instancing: revision | Functional | P2 | Generate the after multi-instancing BOM. | 'revision' column correct; CSV export matches. |  |
| ASM-0212 | BOM after replace: revision | Functional | P2 | Generate the after replace BOM. | 'revision' column correct; CSV export matches. |  |
| ASM-0213 | BOM flat: maker/buyer | Functional | P2 | Generate the flat BOM. | 'maker/buyer' column correct; CSV export matches. |  |
| ASM-0214 | BOM indented: maker/buyer | Functional | P2 | Generate the indented BOM. | 'maker/buyer' column correct; CSV export matches. |  |
| ASM-0215 | BOM after multi-instancing: maker/buyer | Functional | P2 | Generate the after multi-instancing BOM. | 'maker/buyer' column correct; CSV export matches. |  |
| ASM-0216 | BOM after replace: maker/buyer | Functional | P2 | Generate the after replace BOM. | 'maker/buyer' column correct; CSV export matches. |  |
