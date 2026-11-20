# CMP — Composites Design

**CATIA-class equivalent:** Composites Design / Composites Engineering  
**Autevra workspace:** Loads → materials; /composites/laminate  
**Scope:** Shared  
**Cases:** 129 (Have 74, Partial 0, Gap 55)

Ply stacks, laminate theory and producibility.

[← Back to the index](../README.md)

## Features

- Stack properties — 64 cases (Have)
- Ply-level design — 40 cases (Gap)
- Failure criteria — 25 cases (Have)

## Stack properties

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CMP-0001 | Laminate [0]8, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 0, 0, 0, 0, 0, 0, 0]; Classical laminate theory |
| CMP-0002 | Laminate [0]8, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [0, 0, 0, 0, 0, 0, 0, 0]; Classical laminate theory |
| CMP-0003 | Laminate [0]8, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.48 kg/m² at 1550 kg/m³. | plies [0, 0, 0, 0, 0, 0, 0, 0]; Classical laminate theory |
| CMP-0004 | Laminate [0]8, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.1 kg/m² at 1550 kg/m³. | plies [0, 0, 0, 0, 0, 0, 0, 0]; Classical laminate theory |
| CMP-0005 | Laminate [0/90]s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.5 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.775 kg/m² at 1550 kg/m³. | plies [0, 90, 90, 0]; Classical laminate theory |
| CMP-0006 | Laminate [0/90]s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [0, 90, 90, 0]; Classical laminate theory |
| CMP-0007 | Laminate [0/90]s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.8 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.24 kg/m² at 1550 kg/m³. | plies [0, 90, 90, 0]; Classical laminate theory |
| CMP-0008 | Laminate [0/90]s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 90, 90, 0]; Classical laminate theory |
| CMP-0009 | Laminate [0/90]2s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 90, 0, 90, 90, 0, 90, 0]; Classical laminate theory |
| CMP-0010 | Laminate [0/90]2s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [0, 90, 0, 90, 90, 0, 90, 0]; Classical laminate theory |
| CMP-0011 | Laminate [0/90]2s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.48 kg/m² at 1550 kg/m³. | plies [0, 90, 0, 90, 90, 0, 90, 0]; Classical laminate theory |
| CMP-0012 | Laminate [0/90]2s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.1 kg/m² at 1550 kg/m³. | plies [0, 90, 0, 90, 90, 0, 90, 0]; Classical laminate theory |
| CMP-0013 | Laminate [0/45/-45/90]s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90, 90, -45, 45, 0]; Classical laminate theory |
| CMP-0014 | Laminate [0/45/-45/90]s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90, 90, -45, 45, 0]; Classical laminate theory |
| CMP-0015 | Laminate [0/45/-45/90]s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.48 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90, 90, -45, 45, 0]; Classical laminate theory |
| CMP-0016 | Laminate [0/45/-45/90]s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.1 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90, 90, -45, 45, 0]; Classical laminate theory |
| CMP-0017 | Laminate [45/-45]2s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [45, -45, 45, -45, -45, 45, -45, 45]; Classical laminate theory |
| CMP-0018 | Laminate [45/-45]2s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [45, -45, 45, -45, -45, 45, -45, 45]; Classical laminate theory |
| CMP-0019 | Laminate [45/-45]2s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.48 kg/m² at 1550 kg/m³. | plies [45, -45, 45, -45, -45, 45, -45, 45]; Classical laminate theory |
| CMP-0020 | Laminate [45/-45]2s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.1 kg/m² at 1550 kg/m³. | plies [45, -45, 45, -45, -45, 45, -45, 45]; Classical laminate theory |
| CMP-0021 | Laminate [0/45/90], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.375 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 0.5813 kg/m² at 1550 kg/m³. | plies [0, 45, 90]; Classical laminate theory |
| CMP-0022 | Laminate [0/45/90], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.45 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 0.6975 kg/m² at 1550 kg/m³. | plies [0, 45, 90]; Classical laminate theory |
| CMP-0023 | Laminate [0/45/90], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.6 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [0, 45, 90]; Classical laminate theory |
| CMP-0024 | Laminate [0/45/90], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.75 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 1.163 kg/m² at 1550 kg/m³. | plies [0, 45, 90]; Classical laminate theory |
| CMP-0025 | Laminate [0/45/-45/90], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.5 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.775 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90]; Classical laminate theory |
| CMP-0026 | Laminate [0/45/-45/90], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.6 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90]; Classical laminate theory |
| CMP-0027 | Laminate [0/45/-45/90], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.8 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.24 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90]; Classical laminate theory |
| CMP-0028 | Laminate [0/45/-45/90], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 1 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 45, -45, 90]; Classical laminate theory |
| CMP-0029 | Laminate [30/-30]s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.5 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.775 kg/m² at 1550 kg/m³. | plies [30, -30, -30, 30]; Classical laminate theory |
| CMP-0030 | Laminate [30/-30]s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [30, -30, -30, 30]; Classical laminate theory |
| CMP-0031 | Laminate [30/-30]s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.8 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.24 kg/m² at 1550 kg/m³. | plies [30, -30, -30, 30]; Classical laminate theory |
| CMP-0032 | Laminate [30/-30]s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [30, -30, -30, 30]; Classical laminate theory |
| CMP-0033 | Laminate [0/60/-60]s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 0.75 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.163 kg/m² at 1550 kg/m³. | plies [0, 60, -60, -60, 60, 0]; Classical laminate theory |
| CMP-0034 | Laminate [0/60/-60]s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 0.9 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.395 kg/m² at 1550 kg/m³. | plies [0, 60, -60, -60, 60, 0]; Classical laminate theory |
| CMP-0035 | Laminate [0/60/-60]s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [0, 60, -60, -60, 60, 0]; Classical laminate theory |
| CMP-0036 | Laminate [0/60/-60]s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 1.5 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.325 kg/m² at 1550 kg/m³. | plies [0, 60, -60, -60, 60, 0]; Classical laminate theory |
| CMP-0037 | Laminate [45/45/0], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.375 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 0.5813 kg/m² at 1550 kg/m³. | plies [45, 45, 0]; Classical laminate theory |
| CMP-0038 | Laminate [45/45/0], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.45 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 0.6975 kg/m² at 1550 kg/m³. | plies [45, 45, 0]; Classical laminate theory |
| CMP-0039 | Laminate [45/45/0], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.6 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [45, 45, 0]; Classical laminate theory |
| CMP-0040 | Laminate [45/45/0], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.75 mm; symmetric=False (B≈0 iff symmetric); balanced=False (A16=A26≈0 iff balanced); areal mass 1.163 kg/m² at 1550 kg/m³. | plies [45, 45, 0]; Classical laminate theory |
| CMP-0041 | Laminate [0/0/90/90], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.5 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.775 kg/m² at 1550 kg/m³. | plies [0, 0, 90, 90]; Classical laminate theory |
| CMP-0042 | Laminate [0/0/90/90], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.6 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [0, 0, 90, 90]; Classical laminate theory |
| CMP-0043 | Laminate [0/0/90/90], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 0.8 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.24 kg/m² at 1550 kg/m³. | plies [0, 0, 90, 90]; Classical laminate theory |
| CMP-0044 | Laminate [0/0/90/90], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 4 plies; thickness 1 mm; symmetric=False (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 0, 90, 90]; Classical laminate theory |
| CMP-0045 | Laminate [15/-15/0]s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 0.75 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.163 kg/m² at 1550 kg/m³. | plies [15, -15, 0, 0, -15, 15]; Classical laminate theory |
| CMP-0046 | Laminate [15/-15/0]s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 0.9 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.395 kg/m² at 1550 kg/m³. | plies [15, -15, 0, 0, -15, 15]; Classical laminate theory |
| CMP-0047 | Laminate [15/-15/0]s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [15, -15, 0, 0, -15, 15]; Classical laminate theory |
| CMP-0048 | Laminate [15/-15/0]s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 1.5 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.325 kg/m² at 1550 kg/m³. | plies [15, -15, 0, 0, -15, 15]; Classical laminate theory |
| CMP-0049 | Laminate [90/0/90], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.375 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.5813 kg/m² at 1550 kg/m³. | plies [90, 0, 90]; Classical laminate theory |
| CMP-0050 | Laminate [90/0/90], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.45 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.6975 kg/m² at 1550 kg/m³. | plies [90, 0, 90]; Classical laminate theory |
| CMP-0051 | Laminate [90/0/90], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 0.93 kg/m² at 1550 kg/m³. | plies [90, 0, 90]; Classical laminate theory |
| CMP-0052 | Laminate [90/0/90], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 3 plies; thickness 0.75 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.163 kg/m² at 1550 kg/m³. | plies [90, 0, 90]; Classical laminate theory |
| CMP-0053 | Laminate [45/0/-45/90]2s, ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 16 plies; thickness 2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.1 kg/m² at 1550 kg/m³. | plies [45, 0, -45, 90, 45, 0, -45, 90, 90, -45, 0, 45, 90, -45, 0, 45]; Classical laminate theory |
| CMP-0054 | Laminate [45/0/-45/90]2s, ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 16 plies; thickness 2.4 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.72 kg/m² at 1550 kg/m³. | plies [45, 0, -45, 90, 45, 0, -45, 90, 90, -45, 0, 45, 90, -45, 0, 45]; Classical laminate theory |
| CMP-0055 | Laminate [45/0/-45/90]2s, ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 16 plies; thickness 3.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 4.96 kg/m² at 1550 kg/m³. | plies [45, 0, -45, 90, 45, 0, -45, 90, 90, -45, 0, 45, 90, -45, 0, 45]; Classical laminate theory |
| CMP-0056 | Laminate [45/0/-45/90]2s, ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 16 plies; thickness 4 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 6.2 kg/m² at 1550 kg/m³. | plies [45, 0, -45, 90, 45, 0, -45, 90, 90, -45, 0, 45, 90, -45, 0, 45]; Classical laminate theory |
| CMP-0057 | Laminate [0/30/-30/90/90/-30/30/0], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.55 kg/m² at 1550 kg/m³. | plies [0, 30, -30, 90, 90, -30, 30, 0]; Classical laminate theory |
| CMP-0058 | Laminate [0/30/-30/90/90/-30/30/0], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [0, 30, -30, 90, 90, -30, 30, 0]; Classical laminate theory |
| CMP-0059 | Laminate [0/30/-30/90/90/-30/30/0], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 1.6 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.48 kg/m² at 1550 kg/m³. | plies [0, 30, -30, 90, 90, -30, 30, 0]; Classical laminate theory |
| CMP-0060 | Laminate [0/30/-30/90/90/-30/30/0], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 8 plies; thickness 2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 3.1 kg/m² at 1550 kg/m³. | plies [0, 30, -30, 90, 90, -30, 30, 0]; Classical laminate theory |
| CMP-0061 | Laminate [60/-60/0/0/-60/60], ply 0.125 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 0.75 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.163 kg/m² at 1550 kg/m³. | plies [60, -60, 0, 0, -60, 60]; Classical laminate theory |
| CMP-0062 | Laminate [60/-60/0/0/-60/60], ply 0.15 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 0.9 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.395 kg/m² at 1550 kg/m³. | plies [60, -60, 0, 0, -60, 60]; Classical laminate theory |
| CMP-0063 | Laminate [60/-60/0/0/-60/60], ply 0.2 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 1.2 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 1.86 kg/m² at 1550 kg/m³. | plies [60, -60, 0, 0, -60, 60]; Classical laminate theory |
| CMP-0064 | Laminate [60/-60/0/0/-60/60], ply 0.25 mm | Accuracy | P2 | POST /composites/laminate with T300/epoxy plies. | 6 plies; thickness 1.5 mm; symmetric=True (B≈0 iff symmetric); balanced=True (A16=A26≈0 iff balanced); areal mass 2.325 kg/m² at 1550 kg/m³. | plies [60, -60, 0, 0, -60, 60]; Classical laminate theory |

## Ply-level design

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CMP-0065 | define rosette on flat panel | Functional | P2 | Run define rosette. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0066 | define rosette on hat stiffener | Functional | P2 | Run define rosette. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0067 | define rosette on spar C-section | Functional | P2 | Run define rosette. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0068 | define rosette on bonnet skin | Functional | P2 | Run define rosette. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0069 | ply by zone on flat panel | Functional | P2 | Run ply by zone. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0070 | ply by zone on hat stiffener | Functional | P2 | Run ply by zone. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0071 | ply by zone on spar C-section | Functional | P2 | Run ply by zone. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0072 | ply by zone on bonnet skin | Functional | P2 | Run ply by zone. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0073 | ply drop-off 10:1 on flat panel | Functional | P2 | Run ply drop-off 10:1. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0074 | ply drop-off 10:1 on hat stiffener | Functional | P2 | Run ply drop-off 10:1. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0075 | ply drop-off 10:1 on spar C-section | Functional | P2 | Run ply drop-off 10:1. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0076 | ply drop-off 10:1 on bonnet skin | Functional | P2 | Run ply drop-off 10:1. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0077 | core sample at a point on flat panel | Functional | P2 | Run core sample at a point. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0078 | core sample at a point on hat stiffener | Functional | P2 | Run core sample at a point. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0079 | core sample at a point on spar C-section | Functional | P2 | Run core sample at a point. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0080 | core sample at a point on bonnet skin | Functional | P2 | Run core sample at a point. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0081 | flatten ply on flat panel | Functional | P2 | Run flatten ply. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0082 | flatten ply on hat stiffener | Functional | P2 | Run flatten ply. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0083 | flatten ply on spar C-section | Functional | P2 | Run flatten ply. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0084 | flatten ply on bonnet skin | Functional | P2 | Run flatten ply. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0085 | producibility (draping) on a dome on flat panel | Functional | P2 | Run producibility (draping) on a dome. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0086 | producibility (draping) on a dome on hat stiffener | Functional | P2 | Run producibility (draping) on a dome. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0087 | producibility (draping) on a dome on spar C-section | Functional | P2 | Run producibility (draping) on a dome. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0088 | producibility (draping) on a dome on bonnet skin | Functional | P2 | Run producibility (draping) on a dome. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0089 | ply book export on flat panel | Functional | P2 | Run ply book export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0090 | ply book export on hat stiffener | Functional | P2 | Run ply book export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0091 | ply book export on spar C-section | Functional | P2 | Run ply book export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0092 | ply book export on bonnet skin | Functional | P2 | Run ply book export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0093 | laser projection export on flat panel | Functional | P2 | Run laser projection export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0094 | laser projection export on hat stiffener | Functional | P2 | Run laser projection export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0095 | laser projection export on spar C-section | Functional | P2 | Run laser projection export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0096 | laser projection export on bonnet skin | Functional | P2 | Run laser projection export. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0097 | solid from plies on flat panel | Functional | P2 | Run solid from plies. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0098 | solid from plies on hat stiffener | Functional | P2 | Run solid from plies. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0099 | solid from plies on spar C-section | Functional | P2 | Run solid from plies. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0100 | solid from plies on bonnet skin | Functional | P2 | Run solid from plies. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0101 | ply interference with insert on flat panel | Functional | P2 | Run ply interference with insert. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0102 | ply interference with insert on hat stiffener | Functional | P2 | Run ply interference with insert. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0103 | ply interference with insert on spar C-section | Functional | P2 | Run ply interference with insert. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |
| CMP-0104 | ply interference with insert on bonnet skin | Functional | P2 | Run ply interference with insert. | Correct per-ply geometry/orientation; shear-angle warnings > 30°. |  |

## Failure criteria

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| CMP-0105 | max stress under Nx=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0106 | max stress under Ny=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0107 | max stress under Nxy=50 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0108 | max stress under Mx=10 N | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0109 | max stress under combined | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0110 | max strain under Nx=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0111 | max strain under Ny=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0112 | max strain under Nxy=50 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0113 | max strain under Mx=10 N | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0114 | max strain under combined | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0115 | Tsai-Hill under Nx=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0116 | Tsai-Hill under Ny=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0117 | Tsai-Hill under Nxy=50 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0118 | Tsai-Hill under Mx=10 N | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0119 | Tsai-Hill under combined | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0120 | Tsai-Wu under Nx=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0121 | Tsai-Wu under Ny=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0122 | Tsai-Wu under Nxy=50 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0123 | Tsai-Wu under Mx=10 N | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0124 | Tsai-Wu under combined | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0125 | Hashin under Nx=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0126 | Hashin under Ny=100 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0127 | Hashin under Nxy=50 N/mm | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0128 | Hashin under Mx=10 N | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
| CMP-0129 | Hashin under combined | Functional | P2 | Analyse a [0/45/-45/90]s laminate. | First-ply-failure index per ply; matches a hand CLT calc within 1%. |  |
