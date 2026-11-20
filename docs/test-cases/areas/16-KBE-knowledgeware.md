# KBE — Knowledgeware

**CATIA-class equivalent:** Knowledge Advisor / Knowledge Expert / Product Knowledge Template  
**Autevra workspace:** Design parameters; Part Design expressions; design tables  
**Scope:** Shared  
**Cases:** 164 (Have 120, Partial 0, Gap 44)

Parameters, formulas, rules, checks, design tables and templates.

[← Back to the index](../README.md)

## Features

- Formulas — 48 cases (Have)
- Rules, checks and reactions — 36 cases (Have)
- Templates and catalogues — 28 cases (Gap)
- Units — 52 cases (Have)

## Formulas

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| KBE-0001 | Evaluate 'a*2 + b' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 25. |  |
| KBE-0002 | Evaluate 'a*2 + b' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 6900. |  |
| KBE-0003 | Evaluate 'a*2 + b' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 1.25. |  |
| KBE-0004 | Evaluate 'a*2 + b' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 200. |  |
| KBE-0005 | Evaluate 'a*2 + b' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = -33. |  |
| KBE-0006 | Evaluate '(a + b) / 2' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 7.5. |  |
| KBE-0007 | Evaluate '(a + b) / 2' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 2100. |  |
| KBE-0008 | Evaluate '(a + b) / 2' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 0.375. |  |
| KBE-0009 | Evaluate '(a + b) / 2' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 50. |  |
| KBE-0010 | Evaluate '(a + b) / 2' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = -6.5. |  |
| KBE-0011 | Evaluate 'sqrt(a*a + b*b)' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 11.18034. |  |
| KBE-0012 | Evaluate 'sqrt(a*a + b*b)' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 3088.689. |  |
| KBE-0013 | Evaluate 'sqrt(a*a + b*b)' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 0.55901699. |  |
| KBE-0014 | Evaluate 'sqrt(a*a + b*b)' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 100. |  |
| KBE-0015 | Evaluate 'sqrt(a*a + b*b)' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 21.18962. |  |
| KBE-0016 | Evaluate 'a * sin(30)' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 5. |  |
| KBE-0017 | Evaluate 'a * sin(30)' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 1350. |  |
| KBE-0018 | Evaluate 'a * sin(30)' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 0.25. |  |
| KBE-0019 | Evaluate 'a * sin(30)' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 50. |  |
| KBE-0020 | Evaluate 'a * sin(30)' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = -10. |  |
| KBE-0021 | Evaluate 'max(a, b) - min(a, b)' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 5. |  |
| KBE-0022 | Evaluate 'max(a, b) - min(a, b)' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 1200. |  |
| KBE-0023 | Evaluate 'max(a, b) - min(a, b)' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 0.25. |  |
| KBE-0024 | Evaluate 'max(a, b) - min(a, b)' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 100. |  |
| KBE-0025 | Evaluate 'max(a, b) - min(a, b)' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 27. |  |
| KBE-0026 | Evaluate 'pi * a^2 / 4' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 78.539816. |  |
| KBE-0027 | Evaluate 'pi * a^2 / 4' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 5725552.6. |  |
| KBE-0028 | Evaluate 'pi * a^2 / 4' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 0.19634954. |  |
| KBE-0029 | Evaluate 'pi * a^2 / 4' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 7853.9816. |  |
| KBE-0030 | Evaluate 'pi * a^2 / 4' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 314.15927. |  |
| KBE-0031 | Evaluate 'a / b' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 2. |  |
| KBE-0032 | Evaluate 'a / b' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 1.8. |  |
| KBE-0033 | Evaluate 'a / b' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 2. |  |
| KBE-0034 | Evaluate 'a / b' with a=100, b=0 | Negative | P2 | Define a, b; create the formula; read the result. | Error: division by zero, reported on the formula. |  |
| KBE-0035 | Evaluate 'a / b' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = -2.8571429. |  |
| KBE-0036 | Evaluate 'round(a / 3, 2)' with a=10, b=5 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 3.33. |  |
| KBE-0037 | Evaluate 'round(a / 3, 2)' with a=2700, b=1500 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 900. |  |
| KBE-0038 | Evaluate 'round(a / 3, 2)' with a=0.5, b=0.25 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 0.17. |  |
| KBE-0039 | Evaluate 'round(a / 3, 2)' with a=100, b=0 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = 33.33. |  |
| KBE-0040 | Evaluate 'round(a / 3, 2)' with a=-20, b=7 | Accuracy | P2 | Define a, b; create the formula; read the result. | Result = -6.67. |  |
| KBE-0041 | Reject formula 'a +' | Negative | P1 | Enter the formula. | Rejected: syntax error at end; model unchanged. |  |
| KBE-0042 | Reject formula 'a + c' | Negative | P1 | Enter the formula. | Rejected: unknown parameter c; model unchanged. |  |
| KBE-0043 | Reject formula 'a = b; b = a' | Negative | P1 | Enter the formula. | Rejected: cycle a→b→a; model unchanged. |  |
| KBE-0044 | Reject formula 'length + angle' | Negative | P1 | Enter the formula. | Rejected: unit mismatch mm + deg; model unchanged. |  |
| KBE-0045 | Reject formula '__import__('os')' | Negative | P1 | Enter the formula. | Rejected: rejected: not an expression; model unchanged. |  |
| KBE-0046 | Reject formula 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | Negative | P1 | Enter the formula. | Rejected: unknown parameter; model unchanged. |  |
| KBE-0047 | Reject formula '1/0' | Negative | P1 | Enter the formula. | Rejected: division by zero; model unchanged. |  |
| KBE-0048 | Reject formula 'sqrt(-1)' | Negative | P1 | Enter the formula. | Rejected: domain error; model unchanged. |  |

## Rules, checks and reactions

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| KBE-0049 | check (warning): wall thickness ≥ 2 mm | Functional | P2 | Author check (warning) for 'wall thickness ≥ 2 mm'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0050 | check (warning): hole edge distance ≥ 1.5×Ø | Functional | P2 | Author check (warning) for 'hole edge distance ≥ 1.5×Ø'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0051 | check (warning): wheel inside arch | Functional | P2 | Author check (warning) for 'wheel inside arch'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0052 | check (warning): mass ≤ 1.2 kg | Functional | P2 | Author check (warning) for 'mass ≤ 1.2 kg'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0053 | check (warning): bend R ≥ t | Functional | P2 | Author check (warning) for 'bend R ≥ t'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0054 | check (warning): fillet on every sharp edge | Functional | P2 | Author check (warning) for 'fillet on every sharp edge'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0055 | check (error blocks save): wall thickness ≥ 2 mm | Functional | P2 | Author check (error blocks save) for 'wall thickness ≥ 2 mm'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0056 | check (error blocks save): hole edge distance ≥ 1.5×Ø | Functional | P2 | Author check (error blocks save) for 'hole edge distance ≥ 1.5×Ø'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0057 | check (error blocks save): wheel inside arch | Functional | P2 | Author check (error blocks save) for 'wheel inside arch'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0058 | check (error blocks save): mass ≤ 1.2 kg | Functional | P2 | Author check (error blocks save) for 'mass ≤ 1.2 kg'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0059 | check (error blocks save): bend R ≥ t | Functional | P2 | Author check (error blocks save) for 'bend R ≥ t'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0060 | check (error blocks save): fillet on every sharp edge | Functional | P2 | Author check (error blocks save) for 'fillet on every sharp edge'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0061 | rule (if/else sets a parameter): wall thickness ≥ 2 mm | Functional | P2 | Author rule (if/else sets a parameter) for 'wall thickness ≥ 2 mm'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0062 | rule (if/else sets a parameter): hole edge distance ≥ 1.5×Ø | Functional | P2 | Author rule (if/else sets a parameter) for 'hole edge distance ≥ 1.5×Ø'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0063 | rule (if/else sets a parameter): wheel inside arch | Functional | P2 | Author rule (if/else sets a parameter) for 'wheel inside arch'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0064 | rule (if/else sets a parameter): mass ≤ 1.2 kg | Functional | P2 | Author rule (if/else sets a parameter) for 'mass ≤ 1.2 kg'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0065 | rule (if/else sets a parameter): bend R ≥ t | Functional | P2 | Author rule (if/else sets a parameter) for 'bend R ≥ t'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0066 | rule (if/else sets a parameter): fillet on every sharp edge | Functional | P2 | Author rule (if/else sets a parameter) for 'fillet on every sharp edge'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0067 | reaction on parameter change: wall thickness ≥ 2 mm | Functional | P2 | Author reaction on parameter change for 'wall thickness ≥ 2 mm'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0068 | reaction on parameter change: hole edge distance ≥ 1.5×Ø | Functional | P2 | Author reaction on parameter change for 'hole edge distance ≥ 1.5×Ø'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0069 | reaction on parameter change: wheel inside arch | Functional | P2 | Author reaction on parameter change for 'wheel inside arch'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0070 | reaction on parameter change: mass ≤ 1.2 kg | Functional | P2 | Author reaction on parameter change for 'mass ≤ 1.2 kg'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0071 | reaction on parameter change: bend R ≥ t | Functional | P2 | Author reaction on parameter change for 'bend R ≥ t'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0072 | reaction on parameter change: fillet on every sharp edge | Functional | P2 | Author reaction on parameter change for 'fillet on every sharp edge'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0073 | reaction on feature update: wall thickness ≥ 2 mm | Functional | P2 | Author reaction on feature update for 'wall thickness ≥ 2 mm'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0074 | reaction on feature update: hole edge distance ≥ 1.5×Ø | Functional | P2 | Author reaction on feature update for 'hole edge distance ≥ 1.5×Ø'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0075 | reaction on feature update: wheel inside arch | Functional | P2 | Author reaction on feature update for 'wheel inside arch'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0076 | reaction on feature update: mass ≤ 1.2 kg | Functional | P2 | Author reaction on feature update for 'mass ≤ 1.2 kg'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0077 | reaction on feature update: bend R ≥ t | Functional | P2 | Author reaction on feature update for 'bend R ≥ t'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0078 | reaction on feature update: fillet on every sharp edge | Functional | P2 | Author reaction on feature update for 'fillet on every sharp edge'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0079 | rule set activation: wall thickness ≥ 2 mm | Functional | P2 | Author rule set activation for 'wall thickness ≥ 2 mm'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0080 | rule set activation: hole edge distance ≥ 1.5×Ø | Functional | P2 | Author rule set activation for 'hole edge distance ≥ 1.5×Ø'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0081 | rule set activation: wheel inside arch | Functional | P2 | Author rule set activation for 'wheel inside arch'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0082 | rule set activation: mass ≤ 1.2 kg | Functional | P2 | Author rule set activation for 'mass ≤ 1.2 kg'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0083 | rule set activation: bend R ≥ t | Functional | P2 | Author rule set activation for 'bend R ≥ t'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |
| KBE-0084 | rule set activation: fillet on every sharp edge | Functional | P2 | Author rule set activation for 'fillet on every sharp edge'; violate it; then fix it. | Status flips red → green; message names the rule and the parameters involved. |  |

## Templates and catalogues

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| KBE-0085 | power copy (sketch + pad + holes): create | Functional | P2 | Create the power copy (sketch + pad + holes). | Instances correct and traceable to the template. |  |
| KBE-0086 | power copy (sketch + pad + holes): instantiate | Functional | P2 | Instantiate the power copy (sketch + pad + holes). | Instances correct and traceable to the template. |  |
| KBE-0087 | power copy (sketch + pad + holes): edit source then update instances | Functional | P2 | Edit source then update instances the power copy (sketch + pad + holes). | Instances correct and traceable to the template. |  |
| KBE-0088 | power copy (sketch + pad + holes): missing input | Negative | P2 | Missing input the power copy (sketch + pad + holes). | Rejected with the missing input named. |  |
| KBE-0089 | user feature (rib with lightening holes): create | Functional | P2 | Create the user feature (rib with lightening holes). | Instances correct and traceable to the template. |  |
| KBE-0090 | user feature (rib with lightening holes): instantiate | Functional | P2 | Instantiate the user feature (rib with lightening holes). | Instances correct and traceable to the template. |  |
| KBE-0091 | user feature (rib with lightening holes): edit source then update instances | Functional | P2 | Edit source then update instances the user feature (rib with lightening holes). | Instances correct and traceable to the template. |  |
| KBE-0092 | user feature (rib with lightening holes): missing input | Negative | P2 | Missing input the user feature (rib with lightening holes). | Rejected with the missing input named. |  |
| KBE-0093 | document template (bracket family): create | Functional | P2 | Create the document template (bracket family). | Instances correct and traceable to the template. |  |
| KBE-0094 | document template (bracket family): instantiate | Functional | P2 | Instantiate the document template (bracket family). | Instances correct and traceable to the template. |  |
| KBE-0095 | document template (bracket family): edit source then update instances | Functional | P2 | Edit source then update instances the document template (bracket family). | Instances correct and traceable to the template. |  |
| KBE-0096 | document template (bracket family): missing input | Negative | P2 | Missing input the document template (bracket family). | Rejected with the missing input named. |  |
| KBE-0097 | catalogue of standard parts: create | Functional | P2 | Create the catalogue of standard parts. | Instances correct and traceable to the template. |  |
| KBE-0098 | catalogue of standard parts: instantiate | Functional | P2 | Instantiate the catalogue of standard parts. | Instances correct and traceable to the template. |  |
| KBE-0099 | catalogue of standard parts: edit source then update instances | Functional | P2 | Edit source then update instances the catalogue of standard parts. | Instances correct and traceable to the template. |  |
| KBE-0100 | catalogue of standard parts: missing input | Negative | P2 | Missing input the catalogue of standard parts. | Rejected with the missing input named. |  |
| KBE-0101 | feature template API: create | Functional | P2 | Create the feature template API. | Instances correct and traceable to the template. |  |
| KBE-0102 | feature template API: instantiate | Functional | P2 | Instantiate the feature template API. | Instances correct and traceable to the template. |  |
| KBE-0103 | feature template API: edit source then update instances | Functional | P2 | Edit source then update instances the feature template API. | Instances correct and traceable to the template. |  |
| KBE-0104 | feature template API: missing input | Negative | P2 | Missing input the feature template API. | Rejected with the missing input named. |  |
| KBE-0105 | template with 10 inputs: create | Functional | P2 | Create the template with 10 inputs. | Instances correct and traceable to the template. |  |
| KBE-0106 | template with 10 inputs: instantiate | Functional | P2 | Instantiate the template with 10 inputs. | Instances correct and traceable to the template. |  |
| KBE-0107 | template with 10 inputs: edit source then update instances | Functional | P2 | Edit source then update instances the template with 10 inputs. | Instances correct and traceable to the template. |  |
| KBE-0108 | template with 10 inputs: missing input | Negative | P2 | Missing input the template with 10 inputs. | Rejected with the missing input named. |  |
| KBE-0109 | template instantiated 100×: create | Functional | P2 | Create the template instantiated 100×. | Instances correct and traceable to the template. |  |
| KBE-0110 | template instantiated 100×: instantiate | Functional | P2 | Instantiate the template instantiated 100×. | Instances correct and traceable to the template. |  |
| KBE-0111 | template instantiated 100×: edit source then update instances | Functional | P2 | Edit source then update instances the template instantiated 100×. | Instances correct and traceable to the template. |  |
| KBE-0112 | template instantiated 100×: missing input | Negative | P2 | Missing input the template instantiated 100×. | Rejected with the missing input named. |  |

## Units

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| KBE-0113 | Convert 0 mm → in | Accuracy | P2 | convert(value, from, to). | 0 in. |  |
| KBE-0114 | Convert 1 mm → in | Accuracy | P2 | convert(value, from, to). | 0.03937008 in. |  |
| KBE-0115 | Convert 12.5 mm → in | Accuracy | P2 | convert(value, from, to). | 0.492126 in. |  |
| KBE-0116 | Convert 1000 mm → in | Accuracy | P2 | convert(value, from, to). | 39.37008 in. |  |
| KBE-0117 | Convert 0 in → mm | Accuracy | P2 | convert(value, from, to). | 0 mm. |  |
| KBE-0118 | Convert 1 in → mm | Accuracy | P2 | convert(value, from, to). | 25.4 mm. |  |
| KBE-0119 | Convert 12.5 in → mm | Accuracy | P2 | convert(value, from, to). | 317.5 mm. |  |
| KBE-0120 | Convert 1000 in → mm | Accuracy | P2 | convert(value, from, to). | 25400 mm. |  |
| KBE-0121 | Convert 0 m → mm | Accuracy | P2 | convert(value, from, to). | 0 mm. |  |
| KBE-0122 | Convert 1 m → mm | Accuracy | P2 | convert(value, from, to). | 1000 mm. |  |
| KBE-0123 | Convert 12.5 m → mm | Accuracy | P2 | convert(value, from, to). | 12500 mm. |  |
| KBE-0124 | Convert 1000 m → mm | Accuracy | P2 | convert(value, from, to). | 1000000 mm. |  |
| KBE-0125 | Convert 0 cm → mm | Accuracy | P2 | convert(value, from, to). | 0 mm. |  |
| KBE-0126 | Convert 1 cm → mm | Accuracy | P2 | convert(value, from, to). | 10 mm. |  |
| KBE-0127 | Convert 12.5 cm → mm | Accuracy | P2 | convert(value, from, to). | 125 mm. |  |
| KBE-0128 | Convert 1000 cm → mm | Accuracy | P2 | convert(value, from, to). | 10000 mm. |  |
| KBE-0129 | Convert 0 deg → rad | Accuracy | P2 | convert(value, from, to). | 0 rad. |  |
| KBE-0130 | Convert 1 deg → rad | Accuracy | P2 | convert(value, from, to). | 0.01745329 rad. |  |
| KBE-0131 | Convert 12.5 deg → rad | Accuracy | P2 | convert(value, from, to). | 0.2181662 rad. |  |
| KBE-0132 | Convert 1000 deg → rad | Accuracy | P2 | convert(value, from, to). | 17.45329 rad. |  |
| KBE-0133 | Convert 0 rad → deg | Accuracy | P2 | convert(value, from, to). | 0 deg. |  |
| KBE-0134 | Convert 1 rad → deg | Accuracy | P2 | convert(value, from, to). | 57.29578 deg. |  |
| KBE-0135 | Convert 12.5 rad → deg | Accuracy | P2 | convert(value, from, to). | 716.1972 deg. |  |
| KBE-0136 | Convert 1000 rad → deg | Accuracy | P2 | convert(value, from, to). | 57295.78 deg. |  |
| KBE-0137 | Convert 0 N → kN | Accuracy | P2 | convert(value, from, to). | 0 kN. |  |
| KBE-0138 | Convert 1 N → kN | Accuracy | P2 | convert(value, from, to). | 0.001 kN. |  |
| KBE-0139 | Convert 12.5 N → kN | Accuracy | P2 | convert(value, from, to). | 0.0125 kN. |  |
| KBE-0140 | Convert 1000 N → kN | Accuracy | P2 | convert(value, from, to). | 1 kN. |  |
| KBE-0141 | Convert 0 MPa → psi | Accuracy | P2 | convert(value, from, to). | 0 psi. |  |
| KBE-0142 | Convert 1 MPa → psi | Accuracy | P2 | convert(value, from, to). | 145.0377 psi. |  |
| KBE-0143 | Convert 12.5 MPa → psi | Accuracy | P2 | convert(value, from, to). | 1812.971 psi. |  |
| KBE-0144 | Convert 1000 MPa → psi | Accuracy | P2 | convert(value, from, to). | 145037.7 psi. |  |
| KBE-0145 | Convert 0 kg → lb | Accuracy | P2 | convert(value, from, to). | 0 lb. |  |
| KBE-0146 | Convert 1 kg → lb | Accuracy | P2 | convert(value, from, to). | 2.204623 lb. |  |
| KBE-0147 | Convert 12.5 kg → lb | Accuracy | P2 | convert(value, from, to). | 27.55779 lb. |  |
| KBE-0148 | Convert 1000 kg → lb | Accuracy | P2 | convert(value, from, to). | 2204.623 lb. |  |
| KBE-0149 | Convert 0 N/mm → lbf/in | Accuracy | P2 | convert(value, from, to). | 0 lbf/in. |  |
| KBE-0150 | Convert 1 N/mm → lbf/in | Accuracy | P2 | convert(value, from, to). | 5.710147 lbf/in. |  |
| KBE-0151 | Convert 12.5 N/mm → lbf/in | Accuracy | P2 | convert(value, from, to). | 71.37684 lbf/in. |  |
| KBE-0152 | Convert 1000 N/mm → lbf/in | Accuracy | P2 | convert(value, from, to). | 5710.147 lbf/in. |  |
| KBE-0153 | Convert 0 km/h → m/s | Accuracy | P2 | convert(value, from, to). | 0 m/s. |  |
| KBE-0154 | Convert 1 km/h → m/s | Accuracy | P2 | convert(value, from, to). | 0.2777778 m/s. |  |
| KBE-0155 | Convert 12.5 km/h → m/s | Accuracy | P2 | convert(value, from, to). | 3.472222 m/s. |  |
| KBE-0156 | Convert 1000 km/h → m/s | Accuracy | P2 | convert(value, from, to). | 277.7778 m/s. |  |
| KBE-0157 | Convert 0 kW → hp | Accuracy | P2 | convert(value, from, to). | 0 hp. |  |
| KBE-0158 | Convert 1 kW → hp | Accuracy | P2 | convert(value, from, to). | 1.341022 hp. |  |
| KBE-0159 | Convert 12.5 kW → hp | Accuracy | P2 | convert(value, from, to). | 16.76277 hp. |  |
| KBE-0160 | Convert 1000 kW → hp | Accuracy | P2 | convert(value, from, to). | 1341.022 hp. |  |
| KBE-0161 | Refuse mm → deg | Negative | P2 | convert across dimensions. | Raises a unit-dimension error. |  |
| KBE-0162 | Refuse kg → mm | Negative | P2 | convert across dimensions. | Raises a unit-dimension error. |  |
| KBE-0163 | Refuse % → N | Negative | P2 | convert across dimensions. | Raises a unit-dimension error. |  |
| KBE-0164 | Refuse Pa → s | Negative | P2 | convert across dimensions. | Raises a unit-dimension error. |  |
