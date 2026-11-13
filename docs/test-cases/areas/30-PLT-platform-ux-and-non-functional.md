# PLT — Platform, UX and non-functional

**CATIA-class equivalent:** V5/3DEXPERIENCE platform behaviour  
**Autevra workspace:** Studio shell; desktop app  
**Scope:** Shared  
**Cases:** 220 (Have 54, Partial 56, Gap 110)

Undo/redo, persistence, performance, security, accessibility and the desktop build.

[← Back to the index](../README.md)

## Features

- Undo/redo and persistence — 58 cases (Have)
- Performance budgets — 32 cases (Partial)
- Security — 24 cases (Partial)
- Accessibility and i18n — 40 cases (Gap)
- Desktop app (Tauri + Python sidecar) — 66 cases (Gap)

## Undo/redo and persistence

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLT-0001 | 1 edits then undo/redo all (Design) | Regression | P2 | Make 1 edits in Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0002 | 1 edits then undo/redo all (Part Design) | Regression | P2 | Make 1 edits in Part Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0003 | 1 edits then undo/redo all (Styling) | Regression | P2 | Make 1 edits in Styling; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0004 | 1 edits then undo/redo all (Vessel) | Regression | P2 | Make 1 edits in Vessel; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0005 | 1 edits then undo/redo all (Aircraft) | Regression | P2 | Make 1 edits in Aircraft; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0006 | 1 edits then undo/redo all (Engine) | Regression | P2 | Make 1 edits in Engine; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0007 | 5 edits then undo/redo all (Design) | Regression | P2 | Make 5 edits in Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0008 | 5 edits then undo/redo all (Part Design) | Regression | P2 | Make 5 edits in Part Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0009 | 5 edits then undo/redo all (Styling) | Regression | P2 | Make 5 edits in Styling; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0010 | 5 edits then undo/redo all (Vessel) | Regression | P2 | Make 5 edits in Vessel; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0011 | 5 edits then undo/redo all (Aircraft) | Regression | P2 | Make 5 edits in Aircraft; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0012 | 5 edits then undo/redo all (Engine) | Regression | P2 | Make 5 edits in Engine; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0013 | 20 edits then undo/redo all (Design) | Regression | P1 | Make 20 edits in Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0014 | 20 edits then undo/redo all (Part Design) | Regression | P1 | Make 20 edits in Part Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0015 | 20 edits then undo/redo all (Styling) | Regression | P1 | Make 20 edits in Styling; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0016 | 20 edits then undo/redo all (Vessel) | Regression | P1 | Make 20 edits in Vessel; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0017 | 20 edits then undo/redo all (Aircraft) | Regression | P1 | Make 20 edits in Aircraft; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0018 | 20 edits then undo/redo all (Engine) | Regression | P1 | Make 20 edits in Engine; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0019 | 100 edits then undo/redo all (Design) | Regression | P2 | Make 100 edits in Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0020 | 100 edits then undo/redo all (Part Design) | Regression | P2 | Make 100 edits in Part Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0021 | 100 edits then undo/redo all (Styling) | Regression | P2 | Make 100 edits in Styling; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0022 | 100 edits then undo/redo all (Vessel) | Regression | P2 | Make 100 edits in Vessel; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0023 | 100 edits then undo/redo all (Aircraft) | Regression | P2 | Make 100 edits in Aircraft; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0024 | 100 edits then undo/redo all (Engine) | Regression | P2 | Make 100 edits in Engine; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0025 | 500 edits then undo/redo all (Design) | Regression | P2 | Make 500 edits in Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0026 | 500 edits then undo/redo all (Part Design) | Regression | P2 | Make 500 edits in Part Design; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0027 | 500 edits then undo/redo all (Styling) | Regression | P2 | Make 500 edits in Styling; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0028 | 500 edits then undo/redo all (Vessel) | Regression | P2 | Make 500 edits in Vessel; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0029 | 500 edits then undo/redo all (Aircraft) | Regression | P2 | Make 500 edits in Aircraft; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0030 | 500 edits then undo/redo all (Engine) | Regression | P2 | Make 500 edits in Engine; undo all; redo all. | State after undo equals the initial state; after redo equals the final state (hash compare); replay() equals current. |  |
| PLT-0031 | save and reload (Design) | Functional | P2 | Save and reload. | No data loss; identical model after the operation. |  |
| PLT-0032 | save and reload (Part Design) | Functional | P2 | Save and reload. | No data loss; identical model after the operation. |  |
| PLT-0033 | save and reload (Vessel) | Functional | P2 | Save and reload. | No data loss; identical model after the operation. |  |
| PLT-0034 | save and reload (Aircraft) | Functional | P2 | Save and reload. | No data loss; identical model after the operation. |  |
| PLT-0035 | browser refresh mid-edit (Design) | Functional | P2 | Browser refresh mid-edit. | No data loss; identical model after the operation. |  |
| PLT-0036 | browser refresh mid-edit (Part Design) | Functional | P2 | Browser refresh mid-edit. | No data loss; identical model after the operation. |  |
| PLT-0037 | browser refresh mid-edit (Vessel) | Functional | P2 | Browser refresh mid-edit. | No data loss; identical model after the operation. |  |
| PLT-0038 | browser refresh mid-edit (Aircraft) | Functional | P2 | Browser refresh mid-edit. | No data loss; identical model after the operation. |  |
| PLT-0039 | server restart (Design) | Functional | P2 | Server restart. | No data loss; identical model after the operation. |  |
| PLT-0040 | server restart (Part Design) | Functional | P2 | Server restart. | No data loss; identical model after the operation. |  |
| PLT-0041 | server restart (Vessel) | Functional | P2 | Server restart. | No data loss; identical model after the operation. |  |
| PLT-0042 | server restart (Aircraft) | Functional | P2 | Server restart. | No data loss; identical model after the operation. |  |
| PLT-0043 | DB migration upgrade (Design) | Functional | P2 | Db migration upgrade. | No data loss; identical model after the operation. |  |
| PLT-0044 | DB migration upgrade (Part Design) | Functional | P2 | Db migration upgrade. | No data loss; identical model after the operation. |  |
| PLT-0045 | DB migration upgrade (Vessel) | Functional | P2 | Db migration upgrade. | No data loss; identical model after the operation. |  |
| PLT-0046 | DB migration upgrade (Aircraft) | Functional | P2 | Db migration upgrade. | No data loss; identical model after the operation. |  |
| PLT-0047 | two tabs same project (Design) | Functional | P2 | Two tabs same project. | No data loss; identical model after the operation. |  |
| PLT-0048 | two tabs same project (Part Design) | Functional | P2 | Two tabs same project. | No data loss; identical model after the operation. |  |
| PLT-0049 | two tabs same project (Vessel) | Functional | P2 | Two tabs same project. | No data loss; identical model after the operation. |  |
| PLT-0050 | two tabs same project (Aircraft) | Functional | P2 | Two tabs same project. | No data loss; identical model after the operation. |  |
| PLT-0051 | project export/import JSON (Design) | Functional | P2 | Project export/import json. | No data loss; identical model after the operation. |  |
| PLT-0052 | project export/import JSON (Part Design) | Functional | P2 | Project export/import json. | No data loss; identical model after the operation. |  |
| PLT-0053 | project export/import JSON (Vessel) | Functional | P2 | Project export/import json. | No data loss; identical model after the operation. |  |
| PLT-0054 | project export/import JSON (Aircraft) | Functional | P2 | Project export/import json. | No data loss; identical model after the operation. |  |
| PLT-0055 | delete and restore (trash) (Design) | Functional | P2 | Delete and restore (trash). | No data loss; identical model after the operation. |  |
| PLT-0056 | delete and restore (trash) (Part Design) | Functional | P2 | Delete and restore (trash). | No data loss; identical model after the operation. |  |
| PLT-0057 | delete and restore (trash) (Vessel) | Functional | P2 | Delete and restore (trash). | No data loss; identical model after the operation. |  |
| PLT-0058 | delete and restore (trash) (Aircraft) | Functional | P2 | Delete and restore (trash). | No data loss; identical model after the operation. |  |

## Performance budgets

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLT-0059 | open studio on M1 8 GB | Performance | P2 | Time open studio. | ≤ 2 s (p95 of 5 runs). |  |
| PLT-0060 | open studio on M3 Pro | Performance | P2 | Time open studio. | ≤ 2 s (p95 of 5 runs). |  |
| PLT-0061 | open studio on Windows i5 16 GB | Performance | P2 | Time open studio. | ≤ 2 s (p95 of 5 runs). |  |
| PLT-0062 | open studio on CI runner | Performance | P2 | Time open studio. | ≤ 2 s (p95 of 5 runs). |  |
| PLT-0063 | create car project on M1 8 GB | Performance | P2 | Time create car project. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0064 | create car project on M3 Pro | Performance | P2 | Time create car project. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0065 | create car project on Windows i5 16 GB | Performance | P2 | Time create car project. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0066 | create car project on CI runner | Performance | P2 | Time create car project. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0067 | parameter edit → mesh update on M1 8 GB | Performance | P2 | Time parameter edit → mesh update. | ≤ 1 s (p95 of 5 runs). |  |
| PLT-0068 | parameter edit → mesh update on M3 Pro | Performance | P2 | Time parameter edit → mesh update. | ≤ 1 s (p95 of 5 runs). |  |
| PLT-0069 | parameter edit → mesh update on Windows i5 16 GB | Performance | P2 | Time parameter edit → mesh update. | ≤ 1 s (p95 of 5 runs). |  |
| PLT-0070 | parameter edit → mesh update on CI runner | Performance | P2 | Time parameter edit → mesh update. | ≤ 1 s (p95 of 5 runs). |  |
| PLT-0071 | part rebuild 50 features on M1 8 GB | Performance | P2 | Time part rebuild 50 features. | ≤ 3 s (p95 of 5 runs). |  |
| PLT-0072 | part rebuild 50 features on M3 Pro | Performance | P2 | Time part rebuild 50 features. | ≤ 3 s (p95 of 5 runs). |  |
| PLT-0073 | part rebuild 50 features on Windows i5 16 GB | Performance | P2 | Time part rebuild 50 features. | ≤ 3 s (p95 of 5 runs). |  |
| PLT-0074 | part rebuild 50 features on CI runner | Performance | P2 | Time part rebuild 50 features. | ≤ 3 s (p95 of 5 runs). |  |
| PLT-0075 | STEP export car on M1 8 GB | Performance | P2 | Time STEP export car. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0076 | STEP export car on M3 Pro | Performance | P2 | Time STEP export car. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0077 | STEP export car on Windows i5 16 GB | Performance | P2 | Time STEP export car. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0078 | STEP export car on CI runner | Performance | P2 | Time STEP export car. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0079 | FEA 100k DOF on M1 8 GB | Performance | P2 | Time FEA 100k DOF. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0080 | FEA 100k DOF on M3 Pro | Performance | P2 | Time FEA 100k DOF. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0081 | FEA 100k DOF on Windows i5 16 GB | Performance | P2 | Time FEA 100k DOF. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0082 | FEA 100k DOF on CI runner | Performance | P2 | Time FEA 100k DOF. | ≤ 10 s (p95 of 5 runs). |  |
| PLT-0083 | topology 120×40, 100 iters on M1 8 GB | Performance | P2 | Time topology 120×40, 100 iters. | ≤ 20 s (p95 of 5 runs). |  |
| PLT-0084 | topology 120×40, 100 iters on M3 Pro | Performance | P2 | Time topology 120×40, 100 iters. | ≤ 20 s (p95 of 5 runs). |  |
| PLT-0085 | topology 120×40, 100 iters on Windows i5 16 GB | Performance | P2 | Time topology 120×40, 100 iters. | ≤ 20 s (p95 of 5 runs). |  |
| PLT-0086 | topology 120×40, 100 iters on CI runner | Performance | P2 | Time topology 120×40, 100 iters. | ≤ 20 s (p95 of 5 runs). |  |
| PLT-0087 | 777 preset build on M1 8 GB | Performance | P2 | Time 777 preset build. | ≤ 40 s (p95 of 5 runs). |  |
| PLT-0088 | 777 preset build on M3 Pro | Performance | P2 | Time 777 preset build. | ≤ 40 s (p95 of 5 runs). |  |
| PLT-0089 | 777 preset build on Windows i5 16 GB | Performance | P2 | Time 777 preset build. | ≤ 40 s (p95 of 5 runs). |  |
| PLT-0090 | 777 preset build on CI runner | Performance | P2 | Time 777 preset build. | ≤ 40 s (p95 of 5 runs). |  |

## Security

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLT-0091 | path traversal in import filename (web) | Security | P1 | Attempt: path traversal in import filename. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0092 | path traversal in import filename (desktop) | Security | P1 | Attempt: path traversal in import filename. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0093 | zip bomb STEP (web) | Security | P1 | Attempt: zip bomb STEP. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0094 | zip bomb STEP (desktop) | Security | P1 | Attempt: zip bomb STEP. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0095 | XXE in ReqIF (web) | Security | P1 | Attempt: XXE in ReqIF. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0096 | XXE in ReqIF (desktop) | Security | P1 | Attempt: XXE in ReqIF. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0097 | SQL injection in project name (web) | Security | P1 | Attempt: SQL injection in project name. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0098 | SQL injection in project name (desktop) | Security | P1 | Attempt: SQL injection in project name. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0099 | XSS in part name rendered in tree (web) | Security | P1 | Attempt: XSS in part name rendered in tree. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0100 | XSS in part name rendered in tree (desktop) | Security | P1 | Attempt: XSS in part name rendered in tree. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0101 | SSRF via URL import (web) | Security | P1 | Attempt: SSRF via URL import. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0102 | SSRF via URL import (desktop) | Security | P1 | Attempt: SSRF via URL import. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0103 | oversized JSON nesting (web) | Security | P1 | Attempt: oversized JSON nesting. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0104 | oversized JSON nesting (desktop) | Security | P1 | Attempt: oversized JSON nesting. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0105 | formula code injection (web) | Security | P1 | Attempt: formula code injection. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0106 | formula code injection (desktop) | Security | P1 | Attempt: formula code injection. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0107 | CSRF on state-changing routes (web) | Security | P1 | Attempt: CSRF on state-changing routes. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0108 | CSRF on state-changing routes (desktop) | Security | P1 | Attempt: CSRF on state-changing routes. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0109 | CORS from unknown origin (web) | Security | P1 | Attempt: CORS from unknown origin. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0110 | CORS from unknown origin (desktop) | Security | P1 | Attempt: CORS from unknown origin. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0111 | secrets in logs (web) | Security | P1 | Attempt: secrets in logs. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0112 | secrets in logs (desktop) | Security | P1 | Attempt: secrets in logs. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0113 | dependency CVE scan (web) | Security | P1 | Attempt: dependency CVE scan. | Blocked; logged without sensitive data; no crash. |  |
| PLT-0114 | dependency CVE scan (desktop) | Security | P1 | Attempt: dependency CVE scan. | Blocked; logged without sensitive data; no crash. |  |

## Accessibility and i18n

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLT-0115 | keyboard-only navigation of panels — Design | Usability | P2 | Check keyboard-only navigation of panels. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0116 | keyboard-only navigation of panels — Part Design | Usability | P2 | Check keyboard-only navigation of panels. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0117 | keyboard-only navigation of panels — Structures | Usability | P2 | Check keyboard-only navigation of panels. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0118 | keyboard-only navigation of panels — Reviews | Usability | P2 | Check keyboard-only navigation of panels. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0119 | screen reader labels on toolbar — Design | Usability | P2 | Check screen reader labels on toolbar. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0120 | screen reader labels on toolbar — Part Design | Usability | P2 | Check screen reader labels on toolbar. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0121 | screen reader labels on toolbar — Structures | Usability | P2 | Check screen reader labels on toolbar. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0122 | screen reader labels on toolbar — Reviews | Usability | P2 | Check screen reader labels on toolbar. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0123 | contrast ≥ 4.5:1 (light/dark) — Design | Usability | P2 | Check contrast ≥ 4.5:1 (light/dark). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0124 | contrast ≥ 4.5:1 (light/dark) — Part Design | Usability | P2 | Check contrast ≥ 4.5:1 (light/dark). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0125 | contrast ≥ 4.5:1 (light/dark) — Structures | Usability | P2 | Check contrast ≥ 4.5:1 (light/dark). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0126 | contrast ≥ 4.5:1 (light/dark) — Reviews | Usability | P2 | Check contrast ≥ 4.5:1 (light/dark). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0127 | focus visible — Design | Usability | P2 | Check focus visible. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0128 | focus visible — Part Design | Usability | P2 | Check focus visible. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0129 | focus visible — Structures | Usability | P2 | Check focus visible. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0130 | focus visible — Reviews | Usability | P2 | Check focus visible. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0131 | reduced motion — Design | Usability | P2 | Check reduced motion. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0132 | reduced motion — Part Design | Usability | P2 | Check reduced motion. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0133 | reduced motion — Structures | Usability | P2 | Check reduced motion. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0134 | reduced motion — Reviews | Usability | P2 | Check reduced motion. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0135 | decimal comma locale (de-DE) — Design | Usability | P2 | Check decimal comma locale (de-DE). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0136 | decimal comma locale (de-DE) — Part Design | Usability | P2 | Check decimal comma locale (de-DE). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0137 | decimal comma locale (de-DE) — Structures | Usability | P2 | Check decimal comma locale (de-DE). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0138 | decimal comma locale (de-DE) — Reviews | Usability | P2 | Check decimal comma locale (de-DE). | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0139 | inch display preference — Design | Usability | P2 | Check inch display preference. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0140 | inch display preference — Part Design | Usability | P2 | Check inch display preference. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0141 | inch display preference — Structures | Usability | P2 | Check inch display preference. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0142 | inch display preference — Reviews | Usability | P2 | Check inch display preference. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0143 | RTL layout — Design | Usability | P2 | Check RTL layout. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0144 | RTL layout — Part Design | Usability | P2 | Check RTL layout. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0145 | RTL layout — Structures | Usability | P2 | Check RTL layout. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0146 | RTL layout — Reviews | Usability | P2 | Check RTL layout. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0147 | UI zoom 200% — Design | Usability | P2 | Check UI zoom 200%. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0148 | UI zoom 200% — Part Design | Usability | P2 | Check UI zoom 200%. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0149 | UI zoom 200% — Structures | Usability | P2 | Check UI zoom 200%. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0150 | UI zoom 200% — Reviews | Usability | P2 | Check UI zoom 200%. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0151 | colour-blind safe analysis maps — Design | Usability | P2 | Check colour-blind safe analysis maps. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0152 | colour-blind safe analysis maps — Part Design | Usability | P2 | Check colour-blind safe analysis maps. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0153 | colour-blind safe analysis maps — Structures | Usability | P2 | Check colour-blind safe analysis maps. | Meets WCAG 2.2 AA (or the stated rule). |  |
| PLT-0154 | colour-blind safe analysis maps — Reviews | Usability | P2 | Check colour-blind safe analysis maps. | Meets WCAG 2.2 AA (or the stated rule). |  |

## Desktop app (Tauri + Python sidecar)

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLT-0155 | install/notarised/signed — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: install/notarised/signed. | Works as on the web build; logs in the user data folder. |  |
| PLT-0156 | first launch offline — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: first launch offline. | Works as on the web build; logs in the user data folder. |  |
| PLT-0157 | sidecar start < 5 s — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: sidecar start < 5 s. | Works as on the web build; logs in the user data folder. |  |
| PLT-0158 | sidecar crash → restart — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: sidecar crash → restart. | Works as on the web build; logs in the user data folder. |  |
| PLT-0159 | open .autevra by double-click — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: open .autevra by double-click. | Works as on the web build; logs in the user data folder. |  |
| PLT-0160 | drag-drop STEP onto window — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: drag-drop STEP onto window. | Works as on the web build; logs in the user data folder. |  |
| PLT-0161 | path with spaces/unicode — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: path with spaces/unicode. | Works as on the web build; logs in the user data folder. |  |
| PLT-0162 | HiDPI and multi-monitor — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: HiDPI and multi-monitor. | Works as on the web build; logs in the user data folder. |  |
| PLT-0163 | auto-update — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: auto-update. | Works as on the web build; logs in the user data folder. |  |
| PLT-0164 | uninstall leaves no sidecar — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: uninstall leaves no sidecar. | Works as on the web build; logs in the user data folder. |  |
| PLT-0165 | file save dialog — macOS 14 arm64 | Functional | P2 | On macOS 14 arm64: file save dialog. | Works as on the web build; logs in the user data folder. |  |
| PLT-0166 | install/notarised/signed — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: install/notarised/signed. | Works as on the web build; logs in the user data folder. |  |
| PLT-0167 | first launch offline — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: first launch offline. | Works as on the web build; logs in the user data folder. |  |
| PLT-0168 | sidecar start < 5 s — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: sidecar start < 5 s. | Works as on the web build; logs in the user data folder. |  |
| PLT-0169 | sidecar crash → restart — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: sidecar crash → restart. | Works as on the web build; logs in the user data folder. |  |
| PLT-0170 | open .autevra by double-click — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: open .autevra by double-click. | Works as on the web build; logs in the user data folder. |  |
| PLT-0171 | drag-drop STEP onto window — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: drag-drop STEP onto window. | Works as on the web build; logs in the user data folder. |  |
| PLT-0172 | path with spaces/unicode — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: path with spaces/unicode. | Works as on the web build; logs in the user data folder. |  |
| PLT-0173 | HiDPI and multi-monitor — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: HiDPI and multi-monitor. | Works as on the web build; logs in the user data folder. |  |
| PLT-0174 | auto-update — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: auto-update. | Works as on the web build; logs in the user data folder. |  |
| PLT-0175 | uninstall leaves no sidecar — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: uninstall leaves no sidecar. | Works as on the web build; logs in the user data folder. |  |
| PLT-0176 | file save dialog — macOS 15 arm64 | Functional | P2 | On macOS 15 arm64: file save dialog. | Works as on the web build; logs in the user data folder. |  |
| PLT-0177 | install/notarised/signed — macOS x86_64 | Functional | P2 | On macOS x86_64: install/notarised/signed. | Works as on the web build; logs in the user data folder. |  |
| PLT-0178 | first launch offline — macOS x86_64 | Functional | P2 | On macOS x86_64: first launch offline. | Works as on the web build; logs in the user data folder. |  |
| PLT-0179 | sidecar start < 5 s — macOS x86_64 | Functional | P2 | On macOS x86_64: sidecar start < 5 s. | Works as on the web build; logs in the user data folder. |  |
| PLT-0180 | sidecar crash → restart — macOS x86_64 | Functional | P2 | On macOS x86_64: sidecar crash → restart. | Works as on the web build; logs in the user data folder. |  |
| PLT-0181 | open .autevra by double-click — macOS x86_64 | Functional | P2 | On macOS x86_64: open .autevra by double-click. | Works as on the web build; logs in the user data folder. |  |
| PLT-0182 | drag-drop STEP onto window — macOS x86_64 | Functional | P2 | On macOS x86_64: drag-drop STEP onto window. | Works as on the web build; logs in the user data folder. |  |
| PLT-0183 | path with spaces/unicode — macOS x86_64 | Functional | P2 | On macOS x86_64: path with spaces/unicode. | Works as on the web build; logs in the user data folder. |  |
| PLT-0184 | HiDPI and multi-monitor — macOS x86_64 | Functional | P2 | On macOS x86_64: HiDPI and multi-monitor. | Works as on the web build; logs in the user data folder. |  |
| PLT-0185 | auto-update — macOS x86_64 | Functional | P2 | On macOS x86_64: auto-update. | Works as on the web build; logs in the user data folder. |  |
| PLT-0186 | uninstall leaves no sidecar — macOS x86_64 | Functional | P2 | On macOS x86_64: uninstall leaves no sidecar. | Works as on the web build; logs in the user data folder. |  |
| PLT-0187 | file save dialog — macOS x86_64 | Functional | P2 | On macOS x86_64: file save dialog. | Works as on the web build; logs in the user data folder. |  |
| PLT-0188 | install/notarised/signed — Windows 10 x64 | Functional | P2 | On Windows 10 x64: install/notarised/signed. | Works as on the web build; logs in the user data folder. |  |
| PLT-0189 | first launch offline — Windows 10 x64 | Functional | P2 | On Windows 10 x64: first launch offline. | Works as on the web build; logs in the user data folder. |  |
| PLT-0190 | sidecar start < 5 s — Windows 10 x64 | Functional | P2 | On Windows 10 x64: sidecar start < 5 s. | Works as on the web build; logs in the user data folder. |  |
| PLT-0191 | sidecar crash → restart — Windows 10 x64 | Functional | P2 | On Windows 10 x64: sidecar crash → restart. | Works as on the web build; logs in the user data folder. |  |
| PLT-0192 | open .autevra by double-click — Windows 10 x64 | Functional | P2 | On Windows 10 x64: open .autevra by double-click. | Works as on the web build; logs in the user data folder. |  |
| PLT-0193 | drag-drop STEP onto window — Windows 10 x64 | Functional | P2 | On Windows 10 x64: drag-drop STEP onto window. | Works as on the web build; logs in the user data folder. |  |
| PLT-0194 | path with spaces/unicode — Windows 10 x64 | Functional | P2 | On Windows 10 x64: path with spaces/unicode. | Works as on the web build; logs in the user data folder. |  |
| PLT-0195 | HiDPI and multi-monitor — Windows 10 x64 | Functional | P2 | On Windows 10 x64: HiDPI and multi-monitor. | Works as on the web build; logs in the user data folder. |  |
| PLT-0196 | auto-update — Windows 10 x64 | Functional | P2 | On Windows 10 x64: auto-update. | Works as on the web build; logs in the user data folder. |  |
| PLT-0197 | uninstall leaves no sidecar — Windows 10 x64 | Functional | P2 | On Windows 10 x64: uninstall leaves no sidecar. | Works as on the web build; logs in the user data folder. |  |
| PLT-0198 | file save dialog — Windows 10 x64 | Functional | P2 | On Windows 10 x64: file save dialog. | Works as on the web build; logs in the user data folder. |  |
| PLT-0199 | install/notarised/signed — Windows 11 x64 | Functional | P2 | On Windows 11 x64: install/notarised/signed. | Works as on the web build; logs in the user data folder. |  |
| PLT-0200 | first launch offline — Windows 11 x64 | Functional | P2 | On Windows 11 x64: first launch offline. | Works as on the web build; logs in the user data folder. |  |
| PLT-0201 | sidecar start < 5 s — Windows 11 x64 | Functional | P2 | On Windows 11 x64: sidecar start < 5 s. | Works as on the web build; logs in the user data folder. |  |
| PLT-0202 | sidecar crash → restart — Windows 11 x64 | Functional | P2 | On Windows 11 x64: sidecar crash → restart. | Works as on the web build; logs in the user data folder. |  |
| PLT-0203 | open .autevra by double-click — Windows 11 x64 | Functional | P2 | On Windows 11 x64: open .autevra by double-click. | Works as on the web build; logs in the user data folder. |  |
| PLT-0204 | drag-drop STEP onto window — Windows 11 x64 | Functional | P2 | On Windows 11 x64: drag-drop STEP onto window. | Works as on the web build; logs in the user data folder. |  |
| PLT-0205 | path with spaces/unicode — Windows 11 x64 | Functional | P2 | On Windows 11 x64: path with spaces/unicode. | Works as on the web build; logs in the user data folder. |  |
| PLT-0206 | HiDPI and multi-monitor — Windows 11 x64 | Functional | P2 | On Windows 11 x64: HiDPI and multi-monitor. | Works as on the web build; logs in the user data folder. |  |
| PLT-0207 | auto-update — Windows 11 x64 | Functional | P2 | On Windows 11 x64: auto-update. | Works as on the web build; logs in the user data folder. |  |
| PLT-0208 | uninstall leaves no sidecar — Windows 11 x64 | Functional | P2 | On Windows 11 x64: uninstall leaves no sidecar. | Works as on the web build; logs in the user data folder. |  |
| PLT-0209 | file save dialog — Windows 11 x64 | Functional | P2 | On Windows 11 x64: file save dialog. | Works as on the web build; logs in the user data folder. |  |
| PLT-0210 | install/notarised/signed — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: install/notarised/signed. | Works as on the web build; logs in the user data folder. |  |
| PLT-0211 | first launch offline — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: first launch offline. | Works as on the web build; logs in the user data folder. |  |
| PLT-0212 | sidecar start < 5 s — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: sidecar start < 5 s. | Works as on the web build; logs in the user data folder. |  |
| PLT-0213 | sidecar crash → restart — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: sidecar crash → restart. | Works as on the web build; logs in the user data folder. |  |
| PLT-0214 | open .autevra by double-click — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: open .autevra by double-click. | Works as on the web build; logs in the user data folder. |  |
| PLT-0215 | drag-drop STEP onto window — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: drag-drop STEP onto window. | Works as on the web build; logs in the user data folder. |  |
| PLT-0216 | path with spaces/unicode — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: path with spaces/unicode. | Works as on the web build; logs in the user data folder. |  |
| PLT-0217 | HiDPI and multi-monitor — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: HiDPI and multi-monitor. | Works as on the web build; logs in the user data folder. |  |
| PLT-0218 | auto-update — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: auto-update. | Works as on the web build; logs in the user data folder. |  |
| PLT-0219 | uninstall leaves no sidecar — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: uninstall leaves no sidecar. | Works as on the web build; logs in the user data folder. |  |
| PLT-0220 | file save dialog — Windows 11 ARM | Functional | P2 | On Windows 11 ARM: file save dialog. | Works as on the web build; logs in the user data folder. |  |
