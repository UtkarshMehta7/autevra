# PIP — Piping and tubing

**CATIA-class equivalent:** Piping & Tubing Design / Fluid Systems  
**Autevra workspace:** Routing  
**Scope:** Shared  
**Cases:** 131 (Have 75, Partial 24, Gap 32)

Pipe routing, pressure drop, bend and spec checks.

[← Back to the index](../README.md)

## Features

- Pressure drop (water 20 °C) — 75 cases (Have)
- Fittings and bends — 24 cases (Partial)
- Routing rules — 32 cases (Gap)

## Pressure drop (water 20 °C)

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PIP-0001 | D=10 mm, v=0.1 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 996.01 (laminar); f = 0.06426; Δp = 32.064 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0002 | D=10 mm, v=0.1 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 996.01 (laminar); f = 0.06426; Δp = 160.32 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0003 | D=10 mm, v=0.1 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 996.01 (laminar); f = 0.06426; Δp = 641.28 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0004 | D=10 mm, v=0.2 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 1992 (laminar); f = 0.03213; Δp = 64.128 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0005 | D=10 mm, v=0.2 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 1992 (laminar); f = 0.03213; Δp = 320.64 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0006 | D=10 mm, v=0.2 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 1992 (laminar); f = 0.03213; Δp = 1282.6 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0007 | D=10 mm, v=0.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03808; Δp = 475.09 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0008 | D=10 mm, v=0.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03808; Δp = 2375.5 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0009 | D=10 mm, v=0.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03808; Δp = 9501.9 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0010 | D=10 mm, v=1.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 14940 (turbulent); f = 0.02814; Δp = 3159 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0011 | D=10 mm, v=1.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 14940 (turbulent); f = 0.02814; Δp = 15795 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0012 | D=10 mm, v=1.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 14940 (turbulent); f = 0.02814; Δp = 63180 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0013 | D=10 mm, v=3.0 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 29880 (turbulent); f = 0.02385; Δp = 10712 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0014 | D=10 mm, v=3.0 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 29880 (turbulent); f = 0.02385; Δp = 53562 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0015 | D=10 mm, v=3.0 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 29880 (turbulent); f = 0.02385; Δp = 214249 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0016 | D=15 mm, v=0.1 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 1494 (laminar); f = 0.04284; Δp = 14.251 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0017 | D=15 mm, v=0.1 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 1494 (laminar); f = 0.04284; Δp = 71.253 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0018 | D=15 mm, v=0.1 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 1494 (laminar); f = 0.04284; Δp = 285.01 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0019 | D=15 mm, v=0.2 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 2988 (turbulent); f = 0.04465; Δp = 59.417 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0020 | D=15 mm, v=0.2 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 2988 (turbulent); f = 0.04465; Δp = 297.08 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0021 | D=15 mm, v=0.2 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 2988 (turbulent); f = 0.04465; Δp = 1188.3 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0022 | D=15 mm, v=0.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 7470.1 (turbulent); f = 0.03377; Δp = 280.85 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0023 | D=15 mm, v=0.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 7470.1 (turbulent); f = 0.03377; Δp = 1404.3 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0024 | D=15 mm, v=0.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 7470.1 (turbulent); f = 0.03377; Δp = 5617 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0025 | D=15 mm, v=1.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 22410 (turbulent); f = 0.02536; Δp = 1897.9 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0026 | D=15 mm, v=1.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 22410 (turbulent); f = 0.02536; Δp = 9489.6 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0027 | D=15 mm, v=1.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 22410 (turbulent); f = 0.02536; Δp = 37958 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0028 | D=15 mm, v=3.0 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 44820 (turbulent); f = 0.02166; Δp = 6486 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0029 | D=15 mm, v=3.0 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 44820 (turbulent); f = 0.02166; Δp = 32430 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0030 | D=15 mm, v=3.0 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 44820 (turbulent); f = 0.02166; Δp = 129720 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0031 | D=25 mm, v=0.1 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 2490 (turbulent); f = 0.04741; Δp = 9.4635 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0032 | D=25 mm, v=0.1 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 2490 (turbulent); f = 0.04741; Δp = 47.318 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0033 | D=25 mm, v=0.1 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 2490 (turbulent); f = 0.04741; Δp = 189.27 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0034 | D=25 mm, v=0.2 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03797; Δp = 30.314 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0035 | D=25 mm, v=0.2 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03797; Δp = 151.57 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0036 | D=25 mm, v=0.2 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03797; Δp = 606.29 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0037 | D=25 mm, v=0.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 12450 (turbulent); f = 0.0293; Δp = 146.23 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0038 | D=25 mm, v=0.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 12450 (turbulent); f = 0.0293; Δp = 731.13 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0039 | D=25 mm, v=0.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 12450 (turbulent); f = 0.0293; Δp = 2924.5 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0040 | D=25 mm, v=1.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 37350 (turbulent); f = 0.0224; Δp = 1006.2 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0041 | D=25 mm, v=1.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 37350 (turbulent); f = 0.0224; Δp = 5030.9 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0042 | D=25 mm, v=1.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 37350 (turbulent); f = 0.0224; Δp = 20123 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0043 | D=25 mm, v=3.0 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 74701 (turbulent); f = 0.01931; Δp = 3468.7 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0044 | D=25 mm, v=3.0 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 74701 (turbulent); f = 0.01931; Δp = 17344 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0045 | D=25 mm, v=3.0 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 74701 (turbulent); f = 0.01931; Δp = 69374 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0046 | D=50 mm, v=0.1 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03793; Δp = 3.7855 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0047 | D=50 mm, v=0.1 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03793; Δp = 18.927 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0048 | D=50 mm, v=0.1 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 4980 (turbulent); f = 0.03793; Δp = 75.709 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0049 | D=50 mm, v=0.2 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 9960.1 (turbulent); f = 0.03106; Δp = 12.399 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0050 | D=50 mm, v=0.2 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 9960.1 (turbulent); f = 0.03106; Δp = 61.994 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0051 | D=50 mm, v=0.2 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 9960.1 (turbulent); f = 0.03106; Δp = 247.98 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0052 | D=50 mm, v=0.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 24900 (turbulent); f = 0.02453; Δp = 61.213 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0053 | D=50 mm, v=0.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 24900 (turbulent); f = 0.02453; Δp = 306.06 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0054 | D=50 mm, v=0.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 24900 (turbulent); f = 0.02453; Δp = 1224.3 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0055 | D=50 mm, v=1.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 74701 (turbulent); f = 0.01916; Δp = 430.19 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0056 | D=50 mm, v=1.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 74701 (turbulent); f = 0.01916; Δp = 2150.9 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0057 | D=50 mm, v=1.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 74701 (turbulent); f = 0.01916; Δp = 8603.8 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0058 | D=50 mm, v=3.0 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 149401 (turbulent); f = 0.01668; Δp = 1498.5 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0059 | D=50 mm, v=3.0 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 149401 (turbulent); f = 0.01668; Δp = 7492.6 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0060 | D=50 mm, v=3.0 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 149401 (turbulent); f = 0.01668; Δp = 29970 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0061 | D=100 mm, v=0.1 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 9960.1 (turbulent); f = 0.03103; Δp = 1.5485 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0062 | D=100 mm, v=0.1 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 9960.1 (turbulent); f = 0.03103; Δp = 7.7427 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0063 | D=100 mm, v=0.1 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 9960.1 (turbulent); f = 0.03103; Δp = 30.971 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0064 | D=100 mm, v=0.2 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 19920 (turbulent); f = 0.02588; Δp = 5.1652 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0065 | D=100 mm, v=0.2 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 19920 (turbulent); f = 0.02588; Δp = 25.826 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0066 | D=100 mm, v=0.2 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 19920 (turbulent); f = 0.02588; Δp = 103.3 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0067 | D=100 mm, v=0.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 49800 (turbulent); f = 0.02084; Δp = 25.999 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0068 | D=100 mm, v=0.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 49800 (turbulent); f = 0.02084; Δp = 130 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0069 | D=100 mm, v=0.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 49800 (turbulent); f = 0.02084; Δp = 519.99 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0070 | D=100 mm, v=1.5 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 149401 (turbulent); f = 0.01657; Δp = 186.04 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0071 | D=100 mm, v=1.5 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 149401 (turbulent); f = 0.01657; Δp = 930.18 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0072 | D=100 mm, v=1.5 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 149401 (turbulent); f = 0.01657; Δp = 3720.7 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0073 | D=100 mm, v=3.0 m/s, L=1 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 298802 (turbulent); f = 0.01456; Δp = 653.89 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0074 | D=100 mm, v=3.0 m/s, L=5 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 298802 (turbulent); f = 0.01456; Δp = 3269.5 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |
| PIP-0075 | D=100 mm, v=3.0 m/s, L=20 m | Accuracy | P2 | POST /routing/pipe for straight pipe. | Re = 298802 (turbulent); f = 0.01456; Δp = 13078 Pa (Darcy-Weisbach, Swamee-Jain). | ρ=998 kg/m³, μ=1.002e-3 Pa·s, ε=0.0015 mm; Swamee-Jain 1976 |

## Fittings and bends

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PIP-0076 | 90° long-radius elbow at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.3×998×1²/2 = 149.7 Pa. |  |
| PIP-0077 | 90° long-radius elbow at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.3×998×2²/2 = 598.8 Pa. |  |
| PIP-0078 | 90° long-radius elbow at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.3×998×3²/2 = 1347.3 Pa. |  |
| PIP-0079 | 90° standard elbow at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.75×998×1²/2 = 374.25 Pa. |  |
| PIP-0080 | 90° standard elbow at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.75×998×2²/2 = 1497 Pa. |  |
| PIP-0081 | 90° standard elbow at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.75×998×3²/2 = 3368.2 Pa. |  |
| PIP-0082 | 45° elbow at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.35×998×1²/2 = 174.65 Pa. |  |
| PIP-0083 | 45° elbow at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.35×998×2²/2 = 698.6 Pa. |  |
| PIP-0084 | 45° elbow at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.35×998×3²/2 = 1571.8 Pa. |  |
| PIP-0085 | tee (run) at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.4×998×1²/2 = 199.6 Pa. |  |
| PIP-0086 | tee (run) at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.4×998×2²/2 = 798.4 Pa. |  |
| PIP-0087 | tee (run) at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.4×998×3²/2 = 1796.4 Pa. |  |
| PIP-0088 | tee (branch) at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 1.5×998×1²/2 = 748.5 Pa. |  |
| PIP-0089 | tee (branch) at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 1.5×998×2²/2 = 2994 Pa. |  |
| PIP-0090 | tee (branch) at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 1.5×998×3²/2 = 6736.5 Pa. |  |
| PIP-0091 | gate valve open at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.2×998×1²/2 = 99.8 Pa. |  |
| PIP-0092 | gate valve open at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.2×998×2²/2 = 399.2 Pa. |  |
| PIP-0093 | gate valve open at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.2×998×3²/2 = 898.2 Pa. |  |
| PIP-0094 | globe valve open at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 6.0×998×1²/2 = 2994 Pa. |  |
| PIP-0095 | globe valve open at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 6.0×998×2²/2 = 11976 Pa. |  |
| PIP-0096 | globe valve open at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 6.0×998×3²/2 = 26946 Pa. |  |
| PIP-0097 | sudden contraction at 1 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.5×998×1²/2 = 249.5 Pa. |  |
| PIP-0098 | sudden contraction at 2 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.5×998×2²/2 = 998 Pa. |  |
| PIP-0099 | sudden contraction at 3 m/s | Accuracy | P2 | Add the fitting to the route. | Minor loss Δp = K·ρv²/2 = 0.5×998×3²/2 = 2245.5 Pa. |  |

## Routing rules

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PIP-0100 | min bend radius 3×D — coolant loop | Functional | P2 | Apply min bend radius 3×D to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0101 | min bend radius 3×D — brake line | Functional | P2 | Apply min bend radius 3×D to the brake line. | Violations listed with location; data exports. |  |
| PIP-0102 | min bend radius 3×D — fuel line | Functional | P2 | Apply min bend radius 3×D to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0103 | min bend radius 3×D — hydraulic 200 bar | Functional | P2 | Apply min bend radius 3×D to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0104 | spec-driven fittings — coolant loop | Functional | P2 | Apply spec-driven fittings to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0105 | spec-driven fittings — brake line | Functional | P2 | Apply spec-driven fittings to the brake line. | Violations listed with location; data exports. |  |
| PIP-0106 | spec-driven fittings — fuel line | Functional | P2 | Apply spec-driven fittings to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0107 | spec-driven fittings — hydraulic 200 bar | Functional | P2 | Apply spec-driven fittings to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0108 | slope ≥ 1% for drains — coolant loop | Functional | P2 | Apply slope ≥ 1% for drains to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0109 | slope ≥ 1% for drains — brake line | Functional | P2 | Apply slope ≥ 1% for drains to the brake line. | Violations listed with location; data exports. |  |
| PIP-0110 | slope ≥ 1% for drains — fuel line | Functional | P2 | Apply slope ≥ 1% for drains to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0111 | slope ≥ 1% for drains — hydraulic 200 bar | Functional | P2 | Apply slope ≥ 1% for drains to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0112 | clearance to hot parts — coolant loop | Functional | P2 | Apply clearance to hot parts to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0113 | clearance to hot parts — brake line | Functional | P2 | Apply clearance to hot parts to the brake line. | Violations listed with location; data exports. |  |
| PIP-0114 | clearance to hot parts — fuel line | Functional | P2 | Apply clearance to hot parts to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0115 | clearance to hot parts — hydraulic 200 bar | Functional | P2 | Apply clearance to hot parts to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0116 | support spacing — coolant loop | Functional | P2 | Apply support spacing to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0117 | support spacing — brake line | Functional | P2 | Apply support spacing to the brake line. | Violations listed with location; data exports. |  |
| PIP-0118 | support spacing — fuel line | Functional | P2 | Apply support spacing to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0119 | support spacing — hydraulic 200 bar | Functional | P2 | Apply support spacing to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0120 | isometric drawing — coolant loop | Functional | P2 | Apply isometric drawing to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0121 | isometric drawing — brake line | Functional | P2 | Apply isometric drawing to the brake line. | Violations listed with location; data exports. |  |
| PIP-0122 | isometric drawing — fuel line | Functional | P2 | Apply isometric drawing to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0123 | isometric drawing — hydraulic 200 bar | Functional | P2 | Apply isometric drawing to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0124 | cut list — coolant loop | Functional | P2 | Apply cut list to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0125 | cut list — brake line | Functional | P2 | Apply cut list to the brake line. | Violations listed with location; data exports. |  |
| PIP-0126 | cut list — fuel line | Functional | P2 | Apply cut list to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0127 | cut list — hydraulic 200 bar | Functional | P2 | Apply cut list to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
| PIP-0128 | tube bending data (LRA/YBC) — coolant loop | Functional | P2 | Apply tube bending data (LRA/YBC) to the coolant loop. | Violations listed with location; data exports. |  |
| PIP-0129 | tube bending data (LRA/YBC) — brake line | Functional | P2 | Apply tube bending data (LRA/YBC) to the brake line. | Violations listed with location; data exports. |  |
| PIP-0130 | tube bending data (LRA/YBC) — fuel line | Functional | P2 | Apply tube bending data (LRA/YBC) to the fuel line. | Violations listed with location; data exports. |  |
| PIP-0131 | tube bending data (LRA/YBC) — hydraulic 200 bar | Functional | P2 | Apply tube bending data (LRA/YBC) to the hydraulic 200 bar. | Violations listed with location; data exports. |  |
