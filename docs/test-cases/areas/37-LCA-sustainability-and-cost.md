# LCA — Sustainability and cost

**CATIA-class equivalent:** Sustainable design / cost estimation add-ons  
**Autevra workspace:** Production (cost, CO2); /lca  
**Scope:** Shared  
**Cases:** 104 (Have 80, Partial 0, Gap 24)

Material CO2e, cost roll-ups and design-for-recycling checks.

[← Back to the index](../README.md)

## Features

- Material CO2e and cost — 80 cases (Have)
- Design for recycling — 24 cases (Gap)

## Material CO2e and cost

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| LCA-0001 | 0.25 kg of steel | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 0.5 kg (2.0 kg/kg); material cost = 0.275 € (1.1 €/kg), using the library values in force. |  |
| LCA-0002 | 1 kg of steel | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 2 kg (2.0 kg/kg); material cost = 1.1 € (1.1 €/kg), using the library values in force. |  |
| LCA-0003 | 5 kg of steel | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 10 kg (2.0 kg/kg); material cost = 5.5 € (1.1 €/kg), using the library values in force. |  |
| LCA-0004 | 20 kg of steel | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 40 kg (2.0 kg/kg); material cost = 22 € (1.1 €/kg), using the library values in force. |  |
| LCA-0005 | 120 kg of steel | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 240 kg (2.0 kg/kg); material cost = 132 € (1.1 €/kg), using the library values in force. |  |
| LCA-0006 | 0.25 kg of aluminium (primary) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 3 kg (12.0 kg/kg); material cost = 0.8 € (3.2 €/kg), using the library values in force. |  |
| LCA-0007 | 1 kg of aluminium (primary) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 12 kg (12.0 kg/kg); material cost = 3.2 € (3.2 €/kg), using the library values in force. |  |
| LCA-0008 | 5 kg of aluminium (primary) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 60 kg (12.0 kg/kg); material cost = 16 € (3.2 €/kg), using the library values in force. |  |
| LCA-0009 | 20 kg of aluminium (primary) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 240 kg (12.0 kg/kg); material cost = 64 € (3.2 €/kg), using the library values in force. |  |
| LCA-0010 | 120 kg of aluminium (primary) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 1440 kg (12.0 kg/kg); material cost = 384 € (3.2 €/kg), using the library values in force. |  |
| LCA-0011 | 0.25 kg of aluminium (recycled) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 0.375 kg (1.5 kg/kg); material cost = 0.65 € (2.6 €/kg), using the library values in force. |  |
| LCA-0012 | 1 kg of aluminium (recycled) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 1.5 kg (1.5 kg/kg); material cost = 2.6 € (2.6 €/kg), using the library values in force. |  |
| LCA-0013 | 5 kg of aluminium (recycled) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 7.5 kg (1.5 kg/kg); material cost = 13 € (2.6 €/kg), using the library values in force. |  |
| LCA-0014 | 20 kg of aluminium (recycled) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 30 kg (1.5 kg/kg); material cost = 52 € (2.6 €/kg), using the library values in force. |  |
| LCA-0015 | 120 kg of aluminium (recycled) | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 180 kg (1.5 kg/kg); material cost = 312 € (2.6 €/kg), using the library values in force. |  |
| LCA-0016 | 0.25 kg of CFRP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 6.25 kg (25.0 kg/kg); material cost = 7.5 € (30.0 €/kg), using the library values in force. |  |
| LCA-0017 | 1 kg of CFRP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 25 kg (25.0 kg/kg); material cost = 30 € (30.0 €/kg), using the library values in force. |  |
| LCA-0018 | 5 kg of CFRP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 125 kg (25.0 kg/kg); material cost = 150 € (30.0 €/kg), using the library values in force. |  |
| LCA-0019 | 20 kg of CFRP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 500 kg (25.0 kg/kg); material cost = 600 € (30.0 €/kg), using the library values in force. |  |
| LCA-0020 | 120 kg of CFRP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 3000 kg (25.0 kg/kg); material cost = 3600 € (30.0 €/kg), using the library values in force. |  |
| LCA-0021 | 0.25 kg of PP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 0.5 kg (2.0 kg/kg); material cost = 0.4 € (1.6 €/kg), using the library values in force. |  |
| LCA-0022 | 1 kg of PP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 2 kg (2.0 kg/kg); material cost = 1.6 € (1.6 €/kg), using the library values in force. |  |
| LCA-0023 | 5 kg of PP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 10 kg (2.0 kg/kg); material cost = 8 € (1.6 €/kg), using the library values in force. |  |
| LCA-0024 | 20 kg of PP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 40 kg (2.0 kg/kg); material cost = 32 € (1.6 €/kg), using the library values in force. |  |
| LCA-0025 | 120 kg of PP | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 240 kg (2.0 kg/kg); material cost = 192 € (1.6 €/kg), using the library values in force. |  |
| LCA-0026 | 0.25 kg of ABS | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 0.875 kg (3.5 kg/kg); material cost = 0.65 € (2.6 €/kg), using the library values in force. |  |
| LCA-0027 | 1 kg of ABS | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 3.5 kg (3.5 kg/kg); material cost = 2.6 € (2.6 €/kg), using the library values in force. |  |
| LCA-0028 | 5 kg of ABS | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 17.5 kg (3.5 kg/kg); material cost = 13 € (2.6 €/kg), using the library values in force. |  |
| LCA-0029 | 20 kg of ABS | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 70 kg (3.5 kg/kg); material cost = 52 € (2.6 €/kg), using the library values in force. |  |
| LCA-0030 | 120 kg of ABS | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 420 kg (3.5 kg/kg); material cost = 312 € (2.6 €/kg), using the library values in force. |  |
| LCA-0031 | 0.25 kg of glass | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 0.3 kg (1.2 kg/kg); material cost = 0.25 € (1.0 €/kg), using the library values in force. |  |
| LCA-0032 | 1 kg of glass | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 1.2 kg (1.2 kg/kg); material cost = 1 € (1.0 €/kg), using the library values in force. |  |
| LCA-0033 | 5 kg of glass | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 6 kg (1.2 kg/kg); material cost = 5 € (1.0 €/kg), using the library values in force. |  |
| LCA-0034 | 20 kg of glass | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 24 kg (1.2 kg/kg); material cost = 20 € (1.0 €/kg), using the library values in force. |  |
| LCA-0035 | 120 kg of glass | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 144 kg (1.2 kg/kg); material cost = 120 € (1.0 €/kg), using the library values in force. |  |
| LCA-0036 | 0.25 kg of copper | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 1 kg (4.0 kg/kg); material cost = 2.375 € (9.5 €/kg), using the library values in force. |  |
| LCA-0037 | 1 kg of copper | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 4 kg (4.0 kg/kg); material cost = 9.5 € (9.5 €/kg), using the library values in force. |  |
| LCA-0038 | 5 kg of copper | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 20 kg (4.0 kg/kg); material cost = 47.5 € (9.5 €/kg), using the library values in force. |  |
| LCA-0039 | 20 kg of copper | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 80 kg (4.0 kg/kg); material cost = 190 € (9.5 €/kg), using the library values in force. |  |
| LCA-0040 | 120 kg of copper | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 480 kg (4.0 kg/kg); material cost = 1140 € (9.5 €/kg), using the library values in force. |  |
| LCA-0041 | 0.25 kg of magnesium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 6 kg (24.0 kg/kg); material cost = 1.125 € (4.5 €/kg), using the library values in force. |  |
| LCA-0042 | 1 kg of magnesium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 24 kg (24.0 kg/kg); material cost = 4.5 € (4.5 €/kg), using the library values in force. |  |
| LCA-0043 | 5 kg of magnesium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 120 kg (24.0 kg/kg); material cost = 22.5 € (4.5 €/kg), using the library values in force. |  |
| LCA-0044 | 20 kg of magnesium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 480 kg (24.0 kg/kg); material cost = 90 € (4.5 €/kg), using the library values in force. |  |
| LCA-0045 | 120 kg of magnesium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 2880 kg (24.0 kg/kg); material cost = 540 € (4.5 €/kg), using the library values in force. |  |
| LCA-0046 | 0.25 kg of titanium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 8.75 kg (35.0 kg/kg); material cost = 6.25 € (25.0 €/kg), using the library values in force. |  |
| LCA-0047 | 1 kg of titanium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 35 kg (35.0 kg/kg); material cost = 25 € (25.0 €/kg), using the library values in force. |  |
| LCA-0048 | 5 kg of titanium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 175 kg (35.0 kg/kg); material cost = 125 € (25.0 €/kg), using the library values in force. |  |
| LCA-0049 | 20 kg of titanium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 700 kg (35.0 kg/kg); material cost = 500 € (25.0 €/kg), using the library values in force. |  |
| LCA-0050 | 120 kg of titanium | Accuracy | P2 | Assign the material; read the LCA and cost roll-up. | CO2e = m × factor = 4200 kg (35.0 kg/kg); material cost = 3000 € (25.0 €/kg), using the library values in force. |  |
| LCA-0051 | steel part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 2.105 kg. |  |
| LCA-0052 | steel part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 2.5 kg. |  |
| LCA-0053 | steel part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 4 kg. |  |
| LCA-0054 | aluminium (primary) part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 12.63 kg. |  |
| LCA-0055 | aluminium (primary) part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 15 kg. |  |
| LCA-0056 | aluminium (primary) part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 24 kg. |  |
| LCA-0057 | aluminium (recycled) part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 1.579 kg. |  |
| LCA-0058 | aluminium (recycled) part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 1.875 kg. |  |
| LCA-0059 | aluminium (recycled) part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 3 kg. |  |
| LCA-0060 | CFRP part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 26.32 kg. |  |
| LCA-0061 | CFRP part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 31.25 kg. |  |
| LCA-0062 | CFRP part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 50 kg. |  |
| LCA-0063 | PP part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 2.105 kg. |  |
| LCA-0064 | PP part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 2.5 kg. |  |
| LCA-0065 | PP part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 4 kg. |  |
| LCA-0066 | ABS part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 3.684 kg. |  |
| LCA-0067 | ABS part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 4.375 kg. |  |
| LCA-0068 | ABS part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 7 kg. |  |
| LCA-0069 | glass part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 1.263 kg. |  |
| LCA-0070 | glass part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 1.5 kg. |  |
| LCA-0071 | glass part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 2.4 kg. |  |
| LCA-0072 | copper part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 4.211 kg. |  |
| LCA-0073 | copper part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 5 kg. |  |
| LCA-0074 | copper part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 8 kg. |  |
| LCA-0075 | magnesium part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 25.26 kg. |  |
| LCA-0076 | magnesium part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 30 kg. |  |
| LCA-0077 | magnesium part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 48 kg. |  |
| LCA-0078 | titanium part 1 kg with 5% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.053 kg; CO2e = 36.84 kg. |  |
| LCA-0079 | titanium part 1 kg with 20% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 1.25 kg; CO2e = 43.75 kg. |  |
| LCA-0080 | titanium part 1 kg with 50% process scrap | Accuracy | P2 | Include buy-to-fly/scrap in the LCA. | Material input = 1/(1−s) = 2 kg; CO2e = 70 kg. |  |

## Design for recycling

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| LCA-0081 | mixed-material joints — car | Functional | P2 | Run mixed-material joints. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0082 | mixed-material joints — aircraft | Functional | P2 | Run mixed-material joints. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0083 | mixed-material joints — vessel | Functional | P2 | Run mixed-material joints. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0084 | mixed-material joints — engine | Functional | P2 | Run mixed-material joints. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0085 | label plastics (ISO 11469) — car | Functional | P2 | Run label plastics (ISO 11469). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0086 | label plastics (ISO 11469) — aircraft | Functional | P2 | Run label plastics (ISO 11469). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0087 | label plastics (ISO 11469) — vessel | Functional | P2 | Run label plastics (ISO 11469). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0088 | label plastics (ISO 11469) — engine | Functional | P2 | Run label plastics (ISO 11469). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0089 | hazardous substances (REACH list) — car | Functional | P2 | Run hazardous substances (REACH list). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0090 | hazardous substances (REACH list) — aircraft | Functional | P2 | Run hazardous substances (REACH list). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0091 | hazardous substances (REACH list) — vessel | Functional | P2 | Run hazardous substances (REACH list). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0092 | hazardous substances (REACH list) — engine | Functional | P2 | Run hazardous substances (REACH list). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0093 | recyclability rate (ISO 22628) — car | Functional | P2 | Run recyclability rate (ISO 22628). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0094 | recyclability rate (ISO 22628) — aircraft | Functional | P2 | Run recyclability rate (ISO 22628). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0095 | recyclability rate (ISO 22628) — vessel | Functional | P2 | Run recyclability rate (ISO 22628). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0096 | recyclability rate (ISO 22628) — engine | Functional | P2 | Run recyclability rate (ISO 22628). | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0097 | disassembly time — car | Functional | P2 | Run disassembly time. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0098 | disassembly time — aircraft | Functional | P2 | Run disassembly time. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0099 | disassembly time — vessel | Functional | P2 | Run disassembly time. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0100 | disassembly time — engine | Functional | P2 | Run disassembly time. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0101 | recycled content target — car | Functional | P2 | Run recycled content target. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0102 | recycled content target — aircraft | Functional | P2 | Run recycled content target. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0103 | recycled content target — vessel | Functional | P2 | Run recycled content target. | Rate/flags per part with the rule cited; totals per product. |  |
| LCA-0104 | recycled content target — engine | Functional | P2 | Run recycled content target. | Rate/flags per part with the rule cited; totals per product. |  |
