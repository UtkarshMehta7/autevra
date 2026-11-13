# AIR — Aircraft

**CATIA-class equivalent:** Aerospace extensions (aircraft conceptual design, wing design, structures)  
**Autevra workspace:** Aircraft; Loads  
**Scope:** Air  
**Cases:** 303 (Have 267, Partial 6, Gap 30)

Atmosphere, aerodynamics, stability, performance and the turbofan presets.

[← Back to the index](../README.md)

## Features

- ISA atmosphere — 81 cases (Have)
- Induced drag and lifting line — 36 cases (Have)
- Performance — 144 cases (Have)
- Stability — 6 cases (Have)
- Aircraft features to add — 36 cases (Partial)

## ISA atmosphere

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| AIR-0001 | ISA at 0 m | Accuracy | P2 | Query the atmosphere model. | T = 288.15 K; p = 101325 Pa; ρ = 1.225 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0002 | ISA at 250 m | Accuracy | P2 | Query the atmosphere model. | T = 286.525 K; p = 98357.5 Pa; ρ = 1.1959 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0003 | ISA at 500 m | Accuracy | P2 | Query the atmosphere model. | T = 284.9 K; p = 95460.8 Pa; ρ = 1.1673 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0004 | ISA at 750 m | Accuracy | P2 | Query the atmosphere model. | T = 283.275 K; p = 92633.6 Pa; ρ = 1.1392 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0005 | ISA at 1000 m | Accuracy | P2 | Query the atmosphere model. | T = 281.65 K; p = 89874.6 Pa; ρ = 1.1116 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0006 | ISA at 1250 m | Accuracy | P2 | Query the atmosphere model. | T = 280.025 K; p = 87182.4 Pa; ρ = 1.0846 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0007 | ISA at 1500 m | Accuracy | P2 | Query the atmosphere model. | T = 278.4 K; p = 84556 Pa; ρ = 1.0581 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0008 | ISA at 1750 m | Accuracy | P2 | Query the atmosphere model. | T = 276.775 K; p = 81994 Pa; ρ = 1.032 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0009 | ISA at 2000 m | Accuracy | P2 | Query the atmosphere model. | T = 275.15 K; p = 79495.2 Pa; ρ = 1.0065 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0010 | ISA at 2250 m | Accuracy | P2 | Query the atmosphere model. | T = 273.525 K; p = 77058.5 Pa; ρ = 0.98143 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0011 | ISA at 2500 m | Accuracy | P2 | Query the atmosphere model. | T = 271.9 K; p = 74682.5 Pa; ρ = 0.95686 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0012 | ISA at 2750 m | Accuracy | P2 | Query the atmosphere model. | T = 270.275 K; p = 72366.3 Pa; ρ = 0.93276 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0013 | ISA at 3000 m | Accuracy | P2 | Query the atmosphere model. | T = 268.65 K; p = 70108.5 Pa; ρ = 0.90912 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0014 | ISA at 3250 m | Accuracy | P2 | Query the atmosphere model. | T = 267.025 K; p = 67908.2 Pa; ρ = 0.88595 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0015 | ISA at 3500 m | Accuracy | P2 | Query the atmosphere model. | T = 265.4 K; p = 65764.1 Pa; ρ = 0.86323 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0016 | ISA at 3750 m | Accuracy | P2 | Query the atmosphere model. | T = 263.775 K; p = 63675.1 Pa; ρ = 0.84096 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0017 | ISA at 4000 m | Accuracy | P2 | Query the atmosphere model. | T = 262.15 K; p = 61640.2 Pa; ρ = 0.81913 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0018 | ISA at 4250 m | Accuracy | P2 | Query the atmosphere model. | T = 260.525 K; p = 59658.3 Pa; ρ = 0.79774 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0019 | ISA at 4500 m | Accuracy | P2 | Query the atmosphere model. | T = 258.9 K; p = 57728.3 Pa; ρ = 0.77677 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0020 | ISA at 4750 m | Accuracy | P2 | Query the atmosphere model. | T = 257.275 K; p = 55849.2 Pa; ρ = 0.75624 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0021 | ISA at 5000 m | Accuracy | P2 | Query the atmosphere model. | T = 255.65 K; p = 54019.9 Pa; ρ = 0.73612 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0022 | ISA at 5250 m | Accuracy | P2 | Query the atmosphere model. | T = 254.025 K; p = 52239.4 Pa; ρ = 0.71641 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0023 | ISA at 5500 m | Accuracy | P2 | Query the atmosphere model. | T = 252.4 K; p = 50506.8 Pa; ρ = 0.69711 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0024 | ISA at 5750 m | Accuracy | P2 | Query the atmosphere model. | T = 250.775 K; p = 48821 Pa; ρ = 0.6782 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0025 | ISA at 6000 m | Accuracy | P2 | Query the atmosphere model. | T = 249.15 K; p = 47181 Pa; ρ = 0.6597 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0026 | ISA at 6250 m | Accuracy | P2 | Query the atmosphere model. | T = 247.525 K; p = 45586 Pa; ρ = 0.64158 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0027 | ISA at 6500 m | Accuracy | P2 | Query the atmosphere model. | T = 245.9 K; p = 44034.8 Pa; ρ = 0.62384 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0028 | ISA at 6750 m | Accuracy | P2 | Query the atmosphere model. | T = 244.275 K; p = 42526.7 Pa; ρ = 0.60649 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0029 | ISA at 7000 m | Accuracy | P2 | Query the atmosphere model. | T = 242.65 K; p = 41060.7 Pa; ρ = 0.5895 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0030 | ISA at 7250 m | Accuracy | P2 | Query the atmosphere model. | T = 241.025 K; p = 39635.9 Pa; ρ = 0.57288 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0031 | ISA at 7500 m | Accuracy | P2 | Query the atmosphere model. | T = 239.4 K; p = 38251.4 Pa; ρ = 0.55662 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0032 | ISA at 7750 m | Accuracy | P2 | Query the atmosphere model. | T = 237.775 K; p = 36906.3 Pa; ρ = 0.54072 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0033 | ISA at 8000 m | Accuracy | P2 | Query the atmosphere model. | T = 236.15 K; p = 35599.8 Pa; ρ = 0.52517 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0034 | ISA at 8250 m | Accuracy | P2 | Query the atmosphere model. | T = 234.525 K; p = 34331 Pa; ρ = 0.50996 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0035 | ISA at 8500 m | Accuracy | P2 | Query the atmosphere model. | T = 232.9 K; p = 33099 Pa; ρ = 0.49509 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0036 | ISA at 8750 m | Accuracy | P2 | Query the atmosphere model. | T = 231.275 K; p = 31903.1 Pa; ρ = 0.48055 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0037 | ISA at 9000 m | Accuracy | P2 | Query the atmosphere model. | T = 229.65 K; p = 30742.5 Pa; ρ = 0.46635 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0038 | ISA at 9250 m | Accuracy | P2 | Query the atmosphere model. | T = 228.025 K; p = 29616.2 Pa; ρ = 0.45247 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0039 | ISA at 9500 m | Accuracy | P2 | Query the atmosphere model. | T = 226.4 K; p = 28523.6 Pa; ρ = 0.4389 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0040 | ISA at 9750 m | Accuracy | P2 | Query the atmosphere model. | T = 224.775 K; p = 27463.9 Pa; ρ = 0.42565 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0041 | ISA at 10000 m | Accuracy | P2 | Query the atmosphere model. | T = 223.15 K; p = 26436.3 Pa; ρ = 0.41271 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0042 | ISA at 10250 m | Accuracy | P2 | Query the atmosphere model. | T = 221.525 K; p = 25440 Pa; ρ = 0.40007 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0043 | ISA at 10500 m | Accuracy | P2 | Query the atmosphere model. | T = 219.9 K; p = 24474.4 Pa; ρ = 0.38773 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0044 | ISA at 10750 m | Accuracy | P2 | Query the atmosphere model. | T = 218.275 K; p = 23538.6 Pa; ρ = 0.37568 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0045 | ISA at 11000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 22632.1 Pa; ρ = 0.36392 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0046 | ISA at 11250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 21757.2 Pa; ρ = 0.34985 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0047 | ISA at 11500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 20916.2 Pa; ρ = 0.33633 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0048 | ISA at 11750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 20107.7 Pa; ρ = 0.32333 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0049 | ISA at 12000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 19330.4 Pa; ρ = 0.31083 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0050 | ISA at 12250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 18583.2 Pa; ρ = 0.29881 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0051 | ISA at 12500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 17864.8 Pa; ρ = 0.28726 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0052 | ISA at 12750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 17174.3 Pa; ρ = 0.27616 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0053 | ISA at 13000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 16510.4 Pa; ρ = 0.26548 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0054 | ISA at 13250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 15872.2 Pa; ρ = 0.25522 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0055 | ISA at 13500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 15258.6 Pa; ρ = 0.24536 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0056 | ISA at 13750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 14668.8 Pa; ρ = 0.23587 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0057 | ISA at 14000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 14101.8 Pa; ρ = 0.22675 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0058 | ISA at 14250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 13556.7 Pa; ρ = 0.21799 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0059 | ISA at 14500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 13032.6 Pa; ρ = 0.20956 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0060 | ISA at 14750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 12528.9 Pa; ρ = 0.20146 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0061 | ISA at 15000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 12044.6 Pa; ρ = 0.19367 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0062 | ISA at 15250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 11579 Pa; ρ = 0.18619 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0063 | ISA at 15500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 11131.4 Pa; ρ = 0.17899 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0064 | ISA at 15750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 10701.1 Pa; ρ = 0.17207 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0065 | ISA at 16000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 10287.5 Pa; ρ = 0.16542 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0066 | ISA at 16250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 9889.79 Pa; ρ = 0.15903 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0067 | ISA at 16500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 9507.5 Pa; ρ = 0.15288 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0068 | ISA at 16750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 9139.98 Pa; ρ = 0.14697 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0069 | ISA at 17000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 8786.67 Pa; ρ = 0.14129 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0070 | ISA at 17250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 8447.02 Pa; ρ = 0.13583 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0071 | ISA at 17500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 8120.5 Pa; ρ = 0.13058 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0072 | ISA at 17750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 7806.6 Pa; ρ = 0.12553 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0073 | ISA at 18000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 7504.84 Pa; ρ = 0.12068 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0074 | ISA at 18250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 7214.74 Pa; ρ = 0.11601 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0075 | ISA at 18500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 6935.85 Pa; ρ = 0.11153 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0076 | ISA at 18750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 6667.74 Pa; ρ = 0.10722 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0077 | ISA at 19000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 6410 Pa; ρ = 0.10307 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0078 | ISA at 19250 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 6162.22 Pa; ρ = 0.099087 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0079 | ISA at 19500 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 5924.02 Pa; ρ = 0.095257 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0080 | ISA at 19750 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 5695.02 Pa; ρ = 0.091575 kg/m³ (±0.1%). | ICAO Doc 7488 |
| AIR-0081 | ISA at 20000 m | Accuracy | P2 | Query the atmosphere model. | T = 216.65 K; p = 5474.88 Pa; ρ = 0.088035 kg/m³ (±0.1%). | ICAO Doc 7488 |

## Induced drag and lifting line

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| AIR-0082 | Induced drag AR=6, e=0.8, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.005968. |  |
| AIR-0083 | Induced drag AR=6, e=0.8, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.02387. |  |
| AIR-0084 | Induced drag AR=6, e=0.8, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.06631. |  |
| AIR-0085 | Induced drag AR=6, e=0.9, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.005305. |  |
| AIR-0086 | Induced drag AR=6, e=0.9, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.02122. |  |
| AIR-0087 | Induced drag AR=6, e=0.9, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.05895. |  |
| AIR-0088 | Induced drag AR=6, e=1.0, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.004775 (elliptic: lifting line matches within 1%). |  |
| AIR-0089 | Induced drag AR=6, e=1.0, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.0191 (elliptic: lifting line matches within 1%). |  |
| AIR-0090 | Induced drag AR=6, e=1.0, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.05305 (elliptic: lifting line matches within 1%). |  |
| AIR-0091 | Induced drag AR=8, e=0.8, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.004476. |  |
| AIR-0092 | Induced drag AR=8, e=0.8, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.0179. |  |
| AIR-0093 | Induced drag AR=8, e=0.8, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.04974. |  |
| AIR-0094 | Induced drag AR=8, e=0.9, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.003979. |  |
| AIR-0095 | Induced drag AR=8, e=0.9, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.01592. |  |
| AIR-0096 | Induced drag AR=8, e=0.9, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.04421. |  |
| AIR-0097 | Induced drag AR=8, e=1.0, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.003581 (elliptic: lifting line matches within 1%). |  |
| AIR-0098 | Induced drag AR=8, e=1.0, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.01432 (elliptic: lifting line matches within 1%). |  |
| AIR-0099 | Induced drag AR=8, e=1.0, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.03979 (elliptic: lifting line matches within 1%). |  |
| AIR-0100 | Induced drag AR=9.5, e=0.8, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.003769. |  |
| AIR-0101 | Induced drag AR=9.5, e=0.8, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.01508. |  |
| AIR-0102 | Induced drag AR=9.5, e=0.8, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.04188. |  |
| AIR-0103 | Induced drag AR=9.5, e=0.9, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.003351. |  |
| AIR-0104 | Induced drag AR=9.5, e=0.9, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.0134. |  |
| AIR-0105 | Induced drag AR=9.5, e=0.9, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.03723. |  |
| AIR-0106 | Induced drag AR=9.5, e=1.0, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.003016 (elliptic: lifting line matches within 1%). |  |
| AIR-0107 | Induced drag AR=9.5, e=1.0, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.01206 (elliptic: lifting line matches within 1%). |  |
| AIR-0108 | Induced drag AR=9.5, e=1.0, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.03351 (elliptic: lifting line matches within 1%). |  |
| AIR-0109 | Induced drag AR=12, e=0.8, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.002984. |  |
| AIR-0110 | Induced drag AR=12, e=0.8, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.01194. |  |
| AIR-0111 | Induced drag AR=12, e=0.8, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.03316. |  |
| AIR-0112 | Induced drag AR=12, e=0.9, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.002653. |  |
| AIR-0113 | Induced drag AR=12, e=0.9, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.01061. |  |
| AIR-0114 | Induced drag AR=12, e=0.9, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.02947. |  |
| AIR-0115 | Induced drag AR=12, e=1.0, CL=0.3 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.002387 (elliptic: lifting line matches within 1%). |  |
| AIR-0116 | Induced drag AR=12, e=1.0, CL=0.6 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.009549 (elliptic: lifting line matches within 1%). |  |
| AIR-0117 | Induced drag AR=12, e=1.0, CL=1.0 | Accuracy | P2 | POST /aero/analyse. | CDi = CL²/(π·AR·e) = 0.02653 (elliptic: lifting line matches within 1%). |  |

## Performance

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| AIR-0118 | Stall: m=1100 kg, S=12 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 31.28 m/s = 60.8 kt. |  |
| AIR-0119 | Stall: m=1100 kg, S=12 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 33.66 m/s = 65.42 kt. |  |
| AIR-0120 | Stall: m=1100 kg, S=12 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 36.31 m/s = 70.58 kt. |  |
| AIR-0121 | Stall: m=1100 kg, S=12 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 39.28 m/s = 76.36 kt. |  |
| AIR-0122 | Stall: m=1100 kg, S=12 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 26.44 m/s = 51.39 kt. |  |
| AIR-0123 | Stall: m=1100 kg, S=12 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 28.45 m/s = 55.29 kt. |  |
| AIR-0124 | Stall: m=1100 kg, S=12 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 30.69 m/s = 59.65 kt. |  |
| AIR-0125 | Stall: m=1100 kg, S=12 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 33.2 m/s = 64.53 kt. |  |
| AIR-0126 | Stall: m=1100 kg, S=16 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 27.09 m/s = 52.66 kt. |  |
| AIR-0127 | Stall: m=1100 kg, S=16 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 29.15 m/s = 56.66 kt. |  |
| AIR-0128 | Stall: m=1100 kg, S=16 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 31.45 m/s = 61.12 kt. |  |
| AIR-0129 | Stall: m=1100 kg, S=16 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 34.02 m/s = 66.13 kt. |  |
| AIR-0130 | Stall: m=1100 kg, S=16 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 22.89 m/s = 44.5 kt. |  |
| AIR-0131 | Stall: m=1100 kg, S=16 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 24.63 m/s = 47.89 kt. |  |
| AIR-0132 | Stall: m=1100 kg, S=16 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 26.58 m/s = 51.66 kt. |  |
| AIR-0133 | Stall: m=1100 kg, S=16 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 28.75 m/s = 55.89 kt. |  |
| AIR-0134 | Stall: m=1100 kg, S=25 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 21.67 m/s = 42.13 kt. |  |
| AIR-0135 | Stall: m=1100 kg, S=25 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 23.32 m/s = 45.33 kt. |  |
| AIR-0136 | Stall: m=1100 kg, S=25 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 25.16 m/s = 48.9 kt. |  |
| AIR-0137 | Stall: m=1100 kg, S=25 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 27.22 m/s = 52.9 kt. |  |
| AIR-0138 | Stall: m=1100 kg, S=25 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 18.32 m/s = 35.6 kt. |  |
| AIR-0139 | Stall: m=1100 kg, S=25 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 19.71 m/s = 38.31 kt. |  |
| AIR-0140 | Stall: m=1100 kg, S=25 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 21.26 m/s = 41.33 kt. |  |
| AIR-0141 | Stall: m=1100 kg, S=25 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 23 m/s = 44.71 kt. |  |
| AIR-0142 | Stall: m=2500 kg, S=12 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 47.16 m/s = 91.66 kt. |  |
| AIR-0143 | Stall: m=2500 kg, S=12 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 50.74 m/s = 98.63 kt. |  |
| AIR-0144 | Stall: m=2500 kg, S=12 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 54.74 m/s = 106.4 kt. |  |
| AIR-0145 | Stall: m=2500 kg, S=12 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 59.22 m/s = 115.1 kt. |  |
| AIR-0146 | Stall: m=2500 kg, S=12 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 39.85 m/s = 77.47 kt. |  |
| AIR-0147 | Stall: m=2500 kg, S=12 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 42.88 m/s = 83.36 kt. |  |
| AIR-0148 | Stall: m=2500 kg, S=12 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 46.26 m/s = 89.93 kt. |  |
| AIR-0149 | Stall: m=2500 kg, S=12 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 50.05 m/s = 97.29 kt. |  |
| AIR-0150 | Stall: m=2500 kg, S=16 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 40.84 m/s = 79.38 kt. |  |
| AIR-0151 | Stall: m=2500 kg, S=16 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 43.94 m/s = 85.42 kt. |  |
| AIR-0152 | Stall: m=2500 kg, S=16 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 47.41 m/s = 92.15 kt. |  |
| AIR-0153 | Stall: m=2500 kg, S=16 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 51.29 m/s = 99.69 kt. |  |
| AIR-0154 | Stall: m=2500 kg, S=16 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 34.51 m/s = 67.09 kt. |  |
| AIR-0155 | Stall: m=2500 kg, S=16 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 37.14 m/s = 72.19 kt. |  |
| AIR-0156 | Stall: m=2500 kg, S=16 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 40.06 m/s = 77.88 kt. |  |
| AIR-0157 | Stall: m=2500 kg, S=16 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 43.34 m/s = 84.25 kt. |  |
| AIR-0158 | Stall: m=2500 kg, S=25 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 32.67 m/s = 63.51 kt. |  |
| AIR-0159 | Stall: m=2500 kg, S=25 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 35.15 m/s = 68.33 kt. |  |
| AIR-0160 | Stall: m=2500 kg, S=25 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 37.92 m/s = 73.72 kt. |  |
| AIR-0161 | Stall: m=2500 kg, S=25 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 41.03 m/s = 79.75 kt. |  |
| AIR-0162 | Stall: m=2500 kg, S=25 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 27.61 m/s = 53.67 kt. |  |
| AIR-0163 | Stall: m=2500 kg, S=25 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 29.71 m/s = 57.75 kt. |  |
| AIR-0164 | Stall: m=2500 kg, S=25 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 32.05 m/s = 62.3 kt. |  |
| AIR-0165 | Stall: m=2500 kg, S=25 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 34.68 m/s = 67.4 kt. |  |
| AIR-0166 | Stall: m=5700 kg, S=12 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 71.2 m/s = 138.4 kt. |  |
| AIR-0167 | Stall: m=5700 kg, S=12 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 76.62 m/s = 148.9 kt. |  |
| AIR-0168 | Stall: m=5700 kg, S=12 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 82.65 m/s = 160.7 kt. |  |
| AIR-0169 | Stall: m=5700 kg, S=12 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 89.42 m/s = 173.8 kt. |  |
| AIR-0170 | Stall: m=5700 kg, S=12 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 60.18 m/s = 117 kt. |  |
| AIR-0171 | Stall: m=5700 kg, S=12 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 64.75 m/s = 125.9 kt. |  |
| AIR-0172 | Stall: m=5700 kg, S=12 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 69.86 m/s = 135.8 kt. |  |
| AIR-0173 | Stall: m=5700 kg, S=12 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 75.57 m/s = 146.9 kt. |  |
| AIR-0174 | Stall: m=5700 kg, S=16 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 61.67 m/s = 119.9 kt. |  |
| AIR-0175 | Stall: m=5700 kg, S=16 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 66.35 m/s = 129 kt. |  |
| AIR-0176 | Stall: m=5700 kg, S=16 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 71.58 m/s = 139.1 kt. |  |
| AIR-0177 | Stall: m=5700 kg, S=16 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 77.44 m/s = 150.5 kt. |  |
| AIR-0178 | Stall: m=5700 kg, S=16 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 52.12 m/s = 101.3 kt. |  |
| AIR-0179 | Stall: m=5700 kg, S=16 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 56.08 m/s = 109 kt. |  |
| AIR-0180 | Stall: m=5700 kg, S=16 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 60.5 m/s = 117.6 kt. |  |
| AIR-0181 | Stall: m=5700 kg, S=16 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 65.45 m/s = 127.2 kt. |  |
| AIR-0182 | Stall: m=5700 kg, S=25 m², CLmax=1.5, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 49.33 m/s = 95.89 kt. |  |
| AIR-0183 | Stall: m=5700 kg, S=25 m², CLmax=1.5, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 53.08 m/s = 103.2 kt. |  |
| AIR-0184 | Stall: m=5700 kg, S=25 m², CLmax=1.5, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 57.26 m/s = 111.3 kt. |  |
| AIR-0185 | Stall: m=5700 kg, S=25 m², CLmax=1.5, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 61.95 m/s = 120.4 kt. |  |
| AIR-0186 | Stall: m=5700 kg, S=25 m², CLmax=2.1, h=0 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 41.69 m/s = 81.05 kt. |  |
| AIR-0187 | Stall: m=5700 kg, S=25 m², CLmax=2.1, h=1500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 44.86 m/s = 87.2 kt. |  |
| AIR-0188 | Stall: m=5700 kg, S=25 m², CLmax=2.1, h=3000 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 48.4 m/s = 94.08 kt. |  |
| AIR-0189 | Stall: m=5700 kg, S=25 m², CLmax=2.1, h=4500 m | Accuracy | P2 | Read stall speed. | Vs = √(2mg/ρSCLmax) = 52.36 m/s = 101.8 kt. |  |
| AIR-0190 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=10, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 311 km. | Breguet range (propeller) |
| AIR-0191 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=10, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 728.1 km. | Breguet range (propeller) |
| AIR-0192 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=10, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1098 km. | Breguet range (propeller) |
| AIR-0193 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=14, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 435.4 km. | Breguet range (propeller) |
| AIR-0194 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=14, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1019 km. | Breguet range (propeller) |
| AIR-0195 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=14, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1537 km. | Breguet range (propeller) |
| AIR-0196 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=18, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 559.8 km. | Breguet range (propeller) |
| AIR-0197 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=18, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1311 km. | Breguet range (propeller) |
| AIR-0198 | Prop Breguet η=0.8, c=2.5e-07 kg/J, L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1976 km. | Breguet range (propeller) |
| AIR-0199 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=10, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 222.1 km. | Breguet range (propeller) |
| AIR-0200 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=10, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 520.1 km. | Breguet range (propeller) |
| AIR-0201 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=10, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 784.2 km. | Breguet range (propeller) |
| AIR-0202 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=14, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 311 km. | Breguet range (propeller) |
| AIR-0203 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=14, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 728.1 km. | Breguet range (propeller) |
| AIR-0204 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=14, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1098 km. | Breguet range (propeller) |
| AIR-0205 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=18, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 399.9 km. | Breguet range (propeller) |
| AIR-0206 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=18, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 936.2 km. | Breguet range (propeller) |
| AIR-0207 | Prop Breguet η=0.8, c=3.5e-07 kg/J, L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1412 km. | Breguet range (propeller) |
| AIR-0208 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=10, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 330.4 km. | Breguet range (propeller) |
| AIR-0209 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=10, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 773.6 km. | Breguet range (propeller) |
| AIR-0210 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=10, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1167 km. | Breguet range (propeller) |
| AIR-0211 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=14, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 462.6 km. | Breguet range (propeller) |
| AIR-0212 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=14, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1083 km. | Breguet range (propeller) |
| AIR-0213 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=14, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1633 km. | Breguet range (propeller) |
| AIR-0214 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=18, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 594.8 km. | Breguet range (propeller) |
| AIR-0215 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=18, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1393 km. | Breguet range (propeller) |
| AIR-0216 | Prop Breguet η=0.85, c=2.5e-07 kg/J, L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 2100 km. | Breguet range (propeller) |
| AIR-0217 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=10, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 236 km. | Breguet range (propeller) |
| AIR-0218 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=10, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 552.6 km. | Breguet range (propeller) |
| AIR-0219 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=10, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 833.3 km. | Breguet range (propeller) |
| AIR-0220 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=14, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 330.4 km. | Breguet range (propeller) |
| AIR-0221 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=14, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 773.6 km. | Breguet range (propeller) |
| AIR-0222 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=14, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1167 km. | Breguet range (propeller) |
| AIR-0223 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=18, W0/W1=1.1 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 424.9 km. | Breguet range (propeller) |
| AIR-0224 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=18, W0/W1=1.25 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 994.7 km. | Breguet range (propeller) |
| AIR-0225 | Prop Breguet η=0.85, c=3.5e-07 kg/J, L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute range. | R = η/(c·g)·(L/D)·ln(W0/W1) = 1500 km. | Breguet range (propeller) |
| AIR-0226 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=16, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 4561 km. | Breguet range (jet) |
| AIR-0227 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=16, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 8418 km. | Breguet range (jet) |
| AIR-0228 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=16, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 11758 km. | Breguet range (jet) |
| AIR-0229 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=18, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 5131 km. | Breguet range (jet) |
| AIR-0230 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 9470 km. | Breguet range (jet) |
| AIR-0231 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=18, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 13228 km. | Breguet range (jet) |
| AIR-0232 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=20, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 5701 km. | Breguet range (jet) |
| AIR-0233 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=20, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 10522 km. | Breguet range (jet) |
| AIR-0234 | Jet Breguet V=230 m/s, TSFC=1.5e-05 kg/(N·s), L/D=20, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 14698 km. | Breguet range (jet) |
| AIR-0235 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=16, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 4025 km. | Breguet range (jet) |
| AIR-0236 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=16, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 7427 km. | Breguet range (jet) |
| AIR-0237 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=16, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 10375 km. | Breguet range (jet) |
| AIR-0238 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=18, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 4528 km. | Breguet range (jet) |
| AIR-0239 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 8356 km. | Breguet range (jet) |
| AIR-0240 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=18, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 11672 km. | Breguet range (jet) |
| AIR-0241 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=20, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 5031 km. | Breguet range (jet) |
| AIR-0242 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=20, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 9284 km. | Breguet range (jet) |
| AIR-0243 | Jet Breguet V=230 m/s, TSFC=1.7e-05 kg/(N·s), L/D=20, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 12968 km. | Breguet range (jet) |
| AIR-0244 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=16, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 4958 km. | Breguet range (jet) |
| AIR-0245 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=16, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 9149 km. | Breguet range (jet) |
| AIR-0246 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=16, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 12781 km. | Breguet range (jet) |
| AIR-0247 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=18, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 5577 km. | Breguet range (jet) |
| AIR-0248 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 10293 km. | Breguet range (jet) |
| AIR-0249 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=18, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 14378 km. | Breguet range (jet) |
| AIR-0250 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=20, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 6197 km. | Breguet range (jet) |
| AIR-0251 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=20, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 11437 km. | Breguet range (jet) |
| AIR-0252 | Jet Breguet V=250 m/s, TSFC=1.5e-05 kg/(N·s), L/D=20, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 15976 km. | Breguet range (jet) |
| AIR-0253 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=16, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 4374 km. | Breguet range (jet) |
| AIR-0254 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=16, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 8073 km. | Breguet range (jet) |
| AIR-0255 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=16, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 11277 km. | Breguet range (jet) |
| AIR-0256 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=18, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 4921 km. | Breguet range (jet) |
| AIR-0257 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=18, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 9082 km. | Breguet range (jet) |
| AIR-0258 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=18, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 12687 km. | Breguet range (jet) |
| AIR-0259 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=20, W0/W1=1.2 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 5468 km. | Breguet range (jet) |
| AIR-0260 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=20, W0/W1=1.4 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 10091 km. | Breguet range (jet) |
| AIR-0261 | Jet Breguet V=250 m/s, TSFC=1.7e-05 kg/(N·s), L/D=20, W0/W1=1.6 | Accuracy | P2 | Compute cruise range. | R = V/(c·g)·(L/D)·ln(W0/W1) = 14096 km. | Breguet range (jet) |

## Stability

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| AIR-0262 | Static margin NP=0.3 c̄, CG=0.2 c̄ | Accuracy | P2 | Read stability. | SM = 10% c̄ → stable. |  |
| AIR-0263 | Static margin NP=0.3 c̄, CG=0.25 c̄ | Accuracy | P2 | Read stability. | SM = 5% c̄ → low (< 5%, warn). |  |
| AIR-0264 | Static margin NP=0.3 c̄, CG=0.3 c̄ | Accuracy | P2 | Read stability. | SM = 0% c̄ → unstable (flag). |  |
| AIR-0265 | Static margin NP=0.3 c̄, CG=0.35 c̄ | Accuracy | P2 | Read stability. | SM = -5% c̄ → unstable (flag). |  |
| AIR-0266 | Static margin NP=0.45 c̄, CG=0.28 c̄ | Accuracy | P2 | Read stability. | SM = 17% c̄ → stable. |  |
| AIR-0267 | Static margin NP=0.25 c̄, CG=0.1 c̄ | Accuracy | P2 | Read stability. | SM = 15% c̄ → stable. |  |

## Aircraft features to add

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| AIR-0268 | V-n diagram (CS-23/CS-25) — trainer | Functional | P2 | Run V-n diagram (CS-23/CS-25). | Result with method, inputs and credibility label. |  |
| AIR-0269 | V-n diagram (CS-23/CS-25) — regional turboprop | Functional | P2 | Run V-n diagram (CS-23/CS-25). | Result with method, inputs and credibility label. |  |
| AIR-0270 | V-n diagram (CS-23/CS-25) — 777-300ER preset | Functional | P2 | Run V-n diagram (CS-23/CS-25). | Result with method, inputs and credibility label. |  |
| AIR-0271 | gust loads (Pratt) — trainer | Functional | P2 | Run gust loads (Pratt). | Result with method, inputs and credibility label. |  |
| AIR-0272 | gust loads (Pratt) — regional turboprop | Functional | P2 | Run gust loads (Pratt). | Result with method, inputs and credibility label. |  |
| AIR-0273 | gust loads (Pratt) — 777-300ER preset | Functional | P2 | Run gust loads (Pratt). | Result with method, inputs and credibility label. |  |
| AIR-0274 | wing box sizing — trainer | Functional | P2 | Run wing box sizing. | Result with method, inputs and credibility label. |  |
| AIR-0275 | wing box sizing — regional turboprop | Functional | P2 | Run wing box sizing. | Result with method, inputs and credibility label. |  |
| AIR-0276 | wing box sizing — 777-300ER preset | Functional | P2 | Run wing box sizing. | Result with method, inputs and credibility label. |  |
| AIR-0277 | fuel tank volumes — trainer | Functional | P2 | Run fuel tank volumes. | Result with method, inputs and credibility label. |  |
| AIR-0278 | fuel tank volumes — regional turboprop | Functional | P2 | Run fuel tank volumes. | Result with method, inputs and credibility label. |  |
| AIR-0279 | fuel tank volumes — 777-300ER preset | Functional | P2 | Run fuel tank volumes. | Result with method, inputs and credibility label. |  |
| AIR-0280 | landing gear retraction kinematics — trainer | Functional | P2 | Run landing gear retraction kinematics. | Result with method, inputs and credibility label. |  |
| AIR-0281 | landing gear retraction kinematics — regional turboprop | Functional | P2 | Run landing gear retraction kinematics. | Result with method, inputs and credibility label. |  |
| AIR-0282 | landing gear retraction kinematics — 777-300ER preset | Functional | P2 | Run landing gear retraction kinematics. | Result with method, inputs and credibility label. |  |
| AIR-0283 | control surface hinge moments — trainer | Functional | P2 | Run control surface hinge moments. | Result with method, inputs and credibility label. |  |
| AIR-0284 | control surface hinge moments — regional turboprop | Functional | P2 | Run control surface hinge moments. | Result with method, inputs and credibility label. |  |
| AIR-0285 | control surface hinge moments — 777-300ER preset | Functional | P2 | Run control surface hinge moments. | Result with method, inputs and credibility label. |  |
| AIR-0286 | trim drag — trainer | Functional | P2 | Run trim drag. | Result with method, inputs and credibility label. |  |
| AIR-0287 | trim drag — regional turboprop | Functional | P2 | Run trim drag. | Result with method, inputs and credibility label. |  |
| AIR-0288 | trim drag — 777-300ER preset | Functional | P2 | Run trim drag. | Result with method, inputs and credibility label. |  |
| AIR-0289 | engine-out (Vmc) — trainer | Functional | P2 | Run engine-out (Vmc). | Result with method, inputs and credibility label. |  |
| AIR-0290 | engine-out (Vmc) — regional turboprop | Functional | P2 | Run engine-out (Vmc). | Result with method, inputs and credibility label. |  |
| AIR-0291 | engine-out (Vmc) — 777-300ER preset | Functional | P2 | Run engine-out (Vmc). | Result with method, inputs and credibility label. |  |
| AIR-0292 | takeoff field length — trainer | Functional | P2 | Run takeoff field length. | Result with method, inputs and credibility label. |  |
| AIR-0293 | takeoff field length — regional turboprop | Functional | P2 | Run takeoff field length. | Result with method, inputs and credibility label. |  |
| AIR-0294 | takeoff field length — 777-300ER preset | Functional | P2 | Run takeoff field length. | Result with method, inputs and credibility label. |  |
| AIR-0295 | noise footprint — trainer | Functional | P2 | Run noise footprint. | Result with method, inputs and credibility label. |  |
| AIR-0296 | noise footprint — regional turboprop | Functional | P2 | Run noise footprint. | Result with method, inputs and credibility label. |  |
| AIR-0297 | noise footprint — 777-300ER preset | Functional | P2 | Run noise footprint. | Result with method, inputs and credibility label. |  |
| AIR-0298 | flutter estimate — trainer | Functional | P2 | Run flutter estimate. | Result with method, inputs and credibility label. |  |
| AIR-0299 | flutter estimate — regional turboprop | Functional | P2 | Run flutter estimate. | Result with method, inputs and credibility label. |  |
| AIR-0300 | flutter estimate — 777-300ER preset | Functional | P2 | Run flutter estimate. | Result with method, inputs and credibility label. |  |
| AIR-0301 | composite wing skin — trainer | Functional | P2 | Run composite wing skin. | Result with method, inputs and credibility label. |  |
| AIR-0302 | composite wing skin — regional turboprop | Functional | P2 | Run composite wing skin. | Result with method, inputs and credibility label. |  |
| AIR-0303 | composite wing skin — 777-300ER preset | Functional | P2 | Run composite wing skin. | Result with method, inputs and credibility label. |  |
