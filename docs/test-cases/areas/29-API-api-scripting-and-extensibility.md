# API — API, scripting and extensibility

**CATIA-class equivalent:** CAA / VBA / EKL automation  
**Autevra workspace:** REST API; plugins  
**Scope:** Shared  
**Cases:** 503 (Have 479, Partial 0, Gap 24)

Every REST route checked for success and failure paths; plugins and scripting.

[← Back to the index](../README.md)

## Features

- REST contract — 473 cases (Have)
- Scripting and plugins — 30 cases (Have)

## REST contract

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| API-0001 | GET /api/health: valid request | Functional | P1 | Send GET /api/health with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0002 | GET /api/health: out-of-range values | Negative | P2 | Send GET /api/health with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0003 | GET /api/health: concurrent identical requests ×20 | Negative | P2 | Send GET /api/health with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0004 | GET /api/health: unicode/emoji in names | Functional | P2 | Send GET /api/health with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0005 | GET /api/health: request while another rebuild is running | Negative | P2 | Send GET /api/health with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0006 | GET /projects: valid request | Functional | P1 | Send GET /projects with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0007 | GET /projects: out-of-range values | Negative | P2 | Send GET /projects with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0008 | GET /projects: concurrent identical requests ×20 | Negative | P2 | Send GET /projects with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0009 | GET /projects: unicode/emoji in names | Functional | P2 | Send GET /projects with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0010 | GET /projects: request while another rebuild is running | Negative | P2 | Send GET /projects with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0011 | POST /projects: valid request | Functional | P1 | Send POST /projects with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0012 | POST /projects: malformed JSON body | Negative | P1 | Send POST /projects with a malformed JSON body. | 422 with field-level errors. |  |
| API-0013 | POST /projects: wrong field types | Negative | P2 | Send POST /projects with a wrong field types. | 422 naming the field. |  |
| API-0014 | POST /projects: out-of-range values | Negative | P2 | Send POST /projects with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0015 | POST /projects: oversized payload (50 MB) | Negative | P2 | Send POST /projects with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0016 | POST /projects: concurrent identical requests ×20 | Negative | P2 | Send POST /projects with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0017 | POST /projects: unicode/emoji in names | Functional | P2 | Send POST /projects with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0018 | POST /projects: missing required field | Negative | P2 | Send POST /projects with a missing required field. | 422 naming the missing field. |  |
| API-0019 | POST /projects: request while another rebuild is running | Negative | P2 | Send POST /projects with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0020 | GET /projects/{project_id}: valid request | Functional | P1 | Send GET /projects/{project_id} with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0021 | GET /projects/{project_id}: unknown project/part id | Negative | P2 | Send GET /projects/{project_id} with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0022 | GET /projects/{project_id}: out-of-range values | Negative | P2 | Send GET /projects/{project_id} with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0023 | GET /projects/{project_id}: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id} with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0024 | GET /projects/{project_id}: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id} with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0025 | GET /projects/{project_id}: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id} with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0026 | PATCH /projects/{project_id}: valid request | Functional | P1 | Send PATCH /projects/{project_id} with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0027 | PATCH /projects/{project_id}: unknown project/part id | Negative | P2 | Send PATCH /projects/{project_id} with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0028 | PATCH /projects/{project_id}: malformed JSON body | Negative | P1 | Send PATCH /projects/{project_id} with a malformed JSON body. | 422 with field-level errors. |  |
| API-0029 | PATCH /projects/{project_id}: wrong field types | Negative | P2 | Send PATCH /projects/{project_id} with a wrong field types. | 422 naming the field. |  |
| API-0030 | PATCH /projects/{project_id}: out-of-range values | Negative | P2 | Send PATCH /projects/{project_id} with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0031 | PATCH /projects/{project_id}: oversized payload (50 MB) | Negative | P2 | Send PATCH /projects/{project_id} with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0032 | PATCH /projects/{project_id}: concurrent identical requests ×20 | Negative | P2 | Send PATCH /projects/{project_id} with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0033 | PATCH /projects/{project_id}: unicode/emoji in names | Functional | P2 | Send PATCH /projects/{project_id} with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0034 | PATCH /projects/{project_id}: missing required field | Negative | P2 | Send PATCH /projects/{project_id} with a missing required field. | 422 naming the missing field. |  |
| API-0035 | PATCH /projects/{project_id}: request while another rebuild is running | Negative | P2 | Send PATCH /projects/{project_id} with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0036 | DELETE /projects/{project_id}: valid request | Functional | P1 | Send DELETE /projects/{project_id} with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0037 | DELETE /projects/{project_id}: unknown project/part id | Negative | P2 | Send DELETE /projects/{project_id} with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0038 | DELETE /projects/{project_id}: out-of-range values | Negative | P2 | Send DELETE /projects/{project_id} with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0039 | DELETE /projects/{project_id}: concurrent identical requests ×20 | Negative | P2 | Send DELETE /projects/{project_id} with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0040 | DELETE /projects/{project_id}: unicode/emoji in names | Functional | P2 | Send DELETE /projects/{project_id} with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0041 | DELETE /projects/{project_id}: request while another rebuild is running | Negative | P2 | Send DELETE /projects/{project_id} with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0042 | GET /projects/{project_id}/model: valid request | Functional | P1 | Send GET /projects/{project_id}/model with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0043 | GET /projects/{project_id}/model: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/model with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0044 | GET /projects/{project_id}/model: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/model with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0045 | GET /projects/{project_id}/model: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/model with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0046 | GET /projects/{project_id}/model: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/model with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0047 | GET /projects/{project_id}/model: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/model with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0048 | POST /projects/{project_id}/preview: valid request | Functional | P1 | Send POST /projects/{project_id}/preview with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0049 | POST /projects/{project_id}/preview: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/preview with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0050 | POST /projects/{project_id}/preview: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/preview with a malformed JSON body. | 422 with field-level errors. |  |
| API-0051 | POST /projects/{project_id}/preview: wrong field types | Negative | P2 | Send POST /projects/{project_id}/preview with a wrong field types. | 422 naming the field. |  |
| API-0052 | POST /projects/{project_id}/preview: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/preview with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0053 | POST /projects/{project_id}/preview: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/preview with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0054 | POST /projects/{project_id}/preview: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/preview with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0055 | POST /projects/{project_id}/preview: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/preview with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0056 | POST /projects/{project_id}/preview: missing required field | Negative | P2 | Send POST /projects/{project_id}/preview with a missing required field. | 422 naming the missing field. |  |
| API-0057 | POST /projects/{project_id}/preview: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/preview with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0058 | POST /projects/{project_id}/undo: valid request | Functional | P1 | Send POST /projects/{project_id}/undo with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0059 | POST /projects/{project_id}/undo: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/undo with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0060 | POST /projects/{project_id}/undo: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/undo with a malformed JSON body. | 422 with field-level errors. |  |
| API-0061 | POST /projects/{project_id}/undo: wrong field types | Negative | P2 | Send POST /projects/{project_id}/undo with a wrong field types. | 422 naming the field. |  |
| API-0062 | POST /projects/{project_id}/undo: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/undo with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0063 | POST /projects/{project_id}/undo: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/undo with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0064 | POST /projects/{project_id}/undo: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/undo with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0065 | POST /projects/{project_id}/undo: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/undo with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0066 | POST /projects/{project_id}/undo: missing required field | Negative | P2 | Send POST /projects/{project_id}/undo with a missing required field. | 422 naming the missing field. |  |
| API-0067 | POST /projects/{project_id}/undo: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/undo with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0068 | POST /projects/{project_id}/redo: valid request | Functional | P1 | Send POST /projects/{project_id}/redo with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0069 | POST /projects/{project_id}/redo: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/redo with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0070 | POST /projects/{project_id}/redo: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/redo with a malformed JSON body. | 422 with field-level errors. |  |
| API-0071 | POST /projects/{project_id}/redo: wrong field types | Negative | P2 | Send POST /projects/{project_id}/redo with a wrong field types. | 422 naming the field. |  |
| API-0072 | POST /projects/{project_id}/redo: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/redo with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0073 | POST /projects/{project_id}/redo: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/redo with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0074 | POST /projects/{project_id}/redo: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/redo with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0075 | POST /projects/{project_id}/redo: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/redo with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0076 | POST /projects/{project_id}/redo: missing required field | Negative | P2 | Send POST /projects/{project_id}/redo with a missing required field. | 422 naming the missing field. |  |
| API-0077 | POST /projects/{project_id}/redo: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/redo with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0078 | GET /projects/{project_id}/history: valid request | Functional | P1 | Send GET /projects/{project_id}/history with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0079 | GET /projects/{project_id}/history: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/history with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0080 | GET /projects/{project_id}/history: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/history with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0081 | GET /projects/{project_id}/history: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/history with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0082 | GET /projects/{project_id}/history: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/history with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0083 | GET /projects/{project_id}/history: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/history with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0084 | GET /projects/{project_id}/export.step: valid request | Functional | P1 | Send GET /projects/{project_id}/export.step with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0085 | GET /projects/{project_id}/export.step: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/export.step with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0086 | GET /projects/{project_id}/export.step: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/export.step with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0087 | GET /projects/{project_id}/export.step: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/export.step with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0088 | GET /projects/{project_id}/export.step: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/export.step with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0089 | GET /projects/{project_id}/export.step: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/export.step with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0090 | GET /projects/{project_id}/export.glb: valid request | Functional | P1 | Send GET /projects/{project_id}/export.glb with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0091 | GET /projects/{project_id}/export.glb: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/export.glb with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0092 | GET /projects/{project_id}/export.glb: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/export.glb with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0093 | GET /projects/{project_id}/export.glb: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/export.glb with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0094 | GET /projects/{project_id}/export.glb: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/export.glb with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0095 | GET /projects/{project_id}/export.glb: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/export.glb with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0096 | POST /projects/{project_id}/import-step: valid request | Functional | P1 | Send POST /projects/{project_id}/import-step with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0097 | POST /projects/{project_id}/import-step: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/import-step with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0098 | POST /projects/{project_id}/import-step: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/import-step with a malformed JSON body. | 422 with field-level errors. |  |
| API-0099 | POST /projects/{project_id}/import-step: wrong field types | Negative | P2 | Send POST /projects/{project_id}/import-step with a wrong field types. | 422 naming the field. |  |
| API-0100 | POST /projects/{project_id}/import-step: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/import-step with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0101 | POST /projects/{project_id}/import-step: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/import-step with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0102 | POST /projects/{project_id}/import-step: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/import-step with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0103 | POST /projects/{project_id}/import-step: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/import-step with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0104 | POST /projects/{project_id}/import-step: missing required field | Negative | P2 | Send POST /projects/{project_id}/import-step with a missing required field. | 422 naming the missing field. |  |
| API-0105 | POST /projects/{project_id}/import-step: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/import-step with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0106 | GET /projects/{project_id}/parts: valid request | Functional | P1 | Send GET /projects/{project_id}/parts with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0107 | GET /projects/{project_id}/parts: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/parts with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0108 | GET /projects/{project_id}/parts: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/parts with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0109 | GET /projects/{project_id}/parts: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/parts with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0110 | GET /projects/{project_id}/parts: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/parts with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0111 | GET /projects/{project_id}/parts: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/parts with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0112 | POST /projects/{project_id}/parts: valid request | Functional | P1 | Send POST /projects/{project_id}/parts with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0113 | POST /projects/{project_id}/parts: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/parts with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0114 | POST /projects/{project_id}/parts: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/parts with a malformed JSON body. | 422 with field-level errors. |  |
| API-0115 | POST /projects/{project_id}/parts: wrong field types | Negative | P2 | Send POST /projects/{project_id}/parts with a wrong field types. | 422 naming the field. |  |
| API-0116 | POST /projects/{project_id}/parts: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/parts with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0117 | POST /projects/{project_id}/parts: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/parts with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0118 | POST /projects/{project_id}/parts: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/parts with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0119 | POST /projects/{project_id}/parts: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/parts with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0120 | POST /projects/{project_id}/parts: missing required field | Negative | P2 | Send POST /projects/{project_id}/parts with a missing required field. | 422 naming the missing field. |  |
| API-0121 | POST /projects/{project_id}/parts: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/parts with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0122 | PUT /projects/{project_id}/parts/{part_id}: valid request | Functional | P1 | Send PUT /projects/{project_id}/parts/{part_id} with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0123 | PUT /projects/{project_id}/parts/{part_id}: unknown project/part id | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0124 | PUT /projects/{project_id}/parts/{part_id}: malformed JSON body | Negative | P1 | Send PUT /projects/{project_id}/parts/{part_id} with a malformed JSON body. | 422 with field-level errors. |  |
| API-0125 | PUT /projects/{project_id}/parts/{part_id}: wrong field types | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a wrong field types. | 422 naming the field. |  |
| API-0126 | PUT /projects/{project_id}/parts/{part_id}: out-of-range values | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0127 | PUT /projects/{project_id}/parts/{part_id}: oversized payload (50 MB) | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0128 | PUT /projects/{project_id}/parts/{part_id}: concurrent identical requests ×20 | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0129 | PUT /projects/{project_id}/parts/{part_id}: unicode/emoji in names | Functional | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0130 | PUT /projects/{project_id}/parts/{part_id}: missing required field | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a missing required field. | 422 naming the missing field. |  |
| API-0131 | PUT /projects/{project_id}/parts/{part_id}: request while another rebuild is running | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id} with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0132 | DELETE /projects/{project_id}/parts/{part_id}: valid request | Functional | P1 | Send DELETE /projects/{project_id}/parts/{part_id} with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0133 | DELETE /projects/{project_id}/parts/{part_id}: unknown project/part id | Negative | P2 | Send DELETE /projects/{project_id}/parts/{part_id} with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0134 | DELETE /projects/{project_id}/parts/{part_id}: out-of-range values | Negative | P2 | Send DELETE /projects/{project_id}/parts/{part_id} with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0135 | DELETE /projects/{project_id}/parts/{part_id}: concurrent identical requests ×20 | Negative | P2 | Send DELETE /projects/{project_id}/parts/{part_id} with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0136 | DELETE /projects/{project_id}/parts/{part_id}: unicode/emoji in names | Functional | P2 | Send DELETE /projects/{project_id}/parts/{part_id} with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0137 | DELETE /projects/{project_id}/parts/{part_id}: request while another rebuild is running | Negative | P2 | Send DELETE /projects/{project_id}/parts/{part_id} with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0138 | POST /projects/{project_id}/parts/{part_id}/undo: valid request | Functional | P1 | Send POST /projects/{project_id}/parts/{part_id}/undo with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0139 | POST /projects/{project_id}/parts/{part_id}/undo: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0140 | POST /projects/{project_id}/parts/{part_id}/undo: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/parts/{part_id}/undo with a malformed JSON body. | 422 with field-level errors. |  |
| API-0141 | POST /projects/{project_id}/parts/{part_id}/undo: wrong field types | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a wrong field types. | 422 naming the field. |  |
| API-0142 | POST /projects/{project_id}/parts/{part_id}/undo: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0143 | POST /projects/{project_id}/parts/{part_id}/undo: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0144 | POST /projects/{project_id}/parts/{part_id}/undo: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0145 | POST /projects/{project_id}/parts/{part_id}/undo: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0146 | POST /projects/{project_id}/parts/{part_id}/undo: missing required field | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a missing required field. | 422 naming the missing field. |  |
| API-0147 | POST /projects/{project_id}/parts/{part_id}/undo: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/undo with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0148 | POST /projects/{project_id}/parts/{part_id}/reorder: valid request | Functional | P1 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0149 | POST /projects/{project_id}/parts/{part_id}/reorder: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0150 | POST /projects/{project_id}/parts/{part_id}/reorder: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a malformed JSON body. | 422 with field-level errors. |  |
| API-0151 | POST /projects/{project_id}/parts/{part_id}/reorder: wrong field types | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a wrong field types. | 422 naming the field. |  |
| API-0152 | POST /projects/{project_id}/parts/{part_id}/reorder: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0153 | POST /projects/{project_id}/parts/{part_id}/reorder: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0154 | POST /projects/{project_id}/parts/{part_id}/reorder: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0155 | POST /projects/{project_id}/parts/{part_id}/reorder: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0156 | POST /projects/{project_id}/parts/{part_id}/reorder: missing required field | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a missing required field. | 422 naming the missing field. |  |
| API-0157 | POST /projects/{project_id}/parts/{part_id}/reorder: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/reorder with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0158 | GET /projects/{project_id}/parts/{part_id}/drawing.svg: valid request | Functional | P1 | Send GET /projects/{project_id}/parts/{part_id}/drawing.svg with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0159 | GET /projects/{project_id}/parts/{part_id}/drawing.svg: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/drawing.svg with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0160 | GET /projects/{project_id}/parts/{part_id}/drawing.svg: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/drawing.svg with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0161 | GET /projects/{project_id}/parts/{part_id}/drawing.svg: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/drawing.svg with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0162 | GET /projects/{project_id}/parts/{part_id}/drawing.svg: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/parts/{part_id}/drawing.svg with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0163 | GET /projects/{project_id}/parts/{part_id}/drawing.svg: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/drawing.svg with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0164 | GET /projects/{project_id}/parts/{part_id}/draft: valid request | Functional | P1 | Send GET /projects/{project_id}/parts/{part_id}/draft with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0165 | GET /projects/{project_id}/parts/{part_id}/draft: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/draft with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0166 | GET /projects/{project_id}/parts/{part_id}/draft: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/draft with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0167 | GET /projects/{project_id}/parts/{part_id}/draft: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/draft with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0168 | GET /projects/{project_id}/parts/{part_id}/draft: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/parts/{part_id}/draft with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0169 | GET /projects/{project_id}/parts/{part_id}/draft: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/parts/{part_id}/draft with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0170 | PUT /projects/{project_id}/parts/{part_id}/design-table: valid request | Functional | P1 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0171 | PUT /projects/{project_id}/parts/{part_id}/design-table: unknown project/part id | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0172 | PUT /projects/{project_id}/parts/{part_id}/design-table: malformed JSON body | Negative | P1 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a malformed JSON body. | 422 with field-level errors. |  |
| API-0173 | PUT /projects/{project_id}/parts/{part_id}/design-table: wrong field types | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a wrong field types. | 422 naming the field. |  |
| API-0174 | PUT /projects/{project_id}/parts/{part_id}/design-table: out-of-range values | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0175 | PUT /projects/{project_id}/parts/{part_id}/design-table: oversized payload (50 MB) | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0176 | PUT /projects/{project_id}/parts/{part_id}/design-table: concurrent identical requests ×20 | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0177 | PUT /projects/{project_id}/parts/{part_id}/design-table: unicode/emoji in names | Functional | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0178 | PUT /projects/{project_id}/parts/{part_id}/design-table: missing required field | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a missing required field. | 422 naming the missing field. |  |
| API-0179 | PUT /projects/{project_id}/parts/{part_id}/design-table: request while another rebuild is running | Negative | P2 | Send PUT /projects/{project_id}/parts/{part_id}/design-table with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0180 | POST /projects/{project_id}/parts/{part_id}/structures: valid request | Functional | P1 | Send POST /projects/{project_id}/parts/{part_id}/structures with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0181 | POST /projects/{project_id}/parts/{part_id}/structures: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0182 | POST /projects/{project_id}/parts/{part_id}/structures: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/parts/{part_id}/structures with a malformed JSON body. | 422 with field-level errors. |  |
| API-0183 | POST /projects/{project_id}/parts/{part_id}/structures: wrong field types | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a wrong field types. | 422 naming the field. |  |
| API-0184 | POST /projects/{project_id}/parts/{part_id}/structures: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0185 | POST /projects/{project_id}/parts/{part_id}/structures: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0186 | POST /projects/{project_id}/parts/{part_id}/structures: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0187 | POST /projects/{project_id}/parts/{part_id}/structures: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0188 | POST /projects/{project_id}/parts/{part_id}/structures: missing required field | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a missing required field. | 422 naming the missing field. |  |
| API-0189 | POST /projects/{project_id}/parts/{part_id}/structures: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/parts/{part_id}/structures with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0190 | GET /projects/{project_id}/requirements: valid request | Functional | P1 | Send GET /projects/{project_id}/requirements with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0191 | GET /projects/{project_id}/requirements: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/requirements with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0192 | GET /projects/{project_id}/requirements: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/requirements with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0193 | GET /projects/{project_id}/requirements: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/requirements with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0194 | GET /projects/{project_id}/requirements: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/requirements with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0195 | GET /projects/{project_id}/requirements: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/requirements with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0196 | GET /projects/{project_id}/requirements.reqif: valid request | Functional | P1 | Send GET /projects/{project_id}/requirements.reqif with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0197 | GET /projects/{project_id}/requirements.reqif: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/requirements.reqif with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0198 | GET /projects/{project_id}/requirements.reqif: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/requirements.reqif with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0199 | GET /projects/{project_id}/requirements.reqif: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/requirements.reqif with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0200 | GET /projects/{project_id}/requirements.reqif: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/requirements.reqif with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0201 | GET /projects/{project_id}/requirements.reqif: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/requirements.reqif with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0202 | POST /projects/{project_id}/changes: valid request | Functional | P1 | Send POST /projects/{project_id}/changes with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0203 | POST /projects/{project_id}/changes: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/changes with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0204 | POST /projects/{project_id}/changes: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/changes with a malformed JSON body. | 422 with field-level errors. |  |
| API-0205 | POST /projects/{project_id}/changes: wrong field types | Negative | P2 | Send POST /projects/{project_id}/changes with a wrong field types. | 422 naming the field. |  |
| API-0206 | POST /projects/{project_id}/changes: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/changes with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0207 | POST /projects/{project_id}/changes: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/changes with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0208 | POST /projects/{project_id}/changes: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/changes with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0209 | POST /projects/{project_id}/changes: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/changes with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0210 | POST /projects/{project_id}/changes: missing required field | Negative | P2 | Send POST /projects/{project_id}/changes with a missing required field. | 422 naming the missing field. |  |
| API-0211 | POST /projects/{project_id}/changes: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/changes with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0212 | POST /projects/{project_id}/baselines: valid request | Functional | P1 | Send POST /projects/{project_id}/baselines with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0213 | POST /projects/{project_id}/baselines: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/baselines with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0214 | POST /projects/{project_id}/baselines: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/baselines with a malformed JSON body. | 422 with field-level errors. |  |
| API-0215 | POST /projects/{project_id}/baselines: wrong field types | Negative | P2 | Send POST /projects/{project_id}/baselines with a wrong field types. | 422 naming the field. |  |
| API-0216 | POST /projects/{project_id}/baselines: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/baselines with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0217 | POST /projects/{project_id}/baselines: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/baselines with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0218 | POST /projects/{project_id}/baselines: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/baselines with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0219 | POST /projects/{project_id}/baselines: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/baselines with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0220 | POST /projects/{project_id}/baselines: missing required field | Negative | P2 | Send POST /projects/{project_id}/baselines with a missing required field. | 422 naming the missing field. |  |
| API-0221 | POST /projects/{project_id}/baselines: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/baselines with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0222 | GET /projects/{project_id}/clearance: valid request | Functional | P1 | Send GET /projects/{project_id}/clearance with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0223 | GET /projects/{project_id}/clearance: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/clearance with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0224 | GET /projects/{project_id}/clearance: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/clearance with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0225 | GET /projects/{project_id}/clearance: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/clearance with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0226 | GET /projects/{project_id}/clearance: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/clearance with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0227 | GET /projects/{project_id}/clearance: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/clearance with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0228 | GET /projects/{project_id}/pfmea: valid request | Functional | P1 | Send GET /projects/{project_id}/pfmea with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0229 | GET /projects/{project_id}/pfmea: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/pfmea with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0230 | GET /projects/{project_id}/pfmea: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/pfmea with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0231 | GET /projects/{project_id}/pfmea: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/pfmea with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0232 | GET /projects/{project_id}/pfmea: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/pfmea with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0233 | GET /projects/{project_id}/pfmea: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/pfmea with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0234 | GET /projects/{project_id}/lca: valid request | Functional | P1 | Send GET /projects/{project_id}/lca with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0235 | GET /projects/{project_id}/lca: unknown project/part id | Negative | P2 | Send GET /projects/{project_id}/lca with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0236 | GET /projects/{project_id}/lca: out-of-range values | Negative | P2 | Send GET /projects/{project_id}/lca with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0237 | GET /projects/{project_id}/lca: concurrent identical requests ×20 | Negative | P2 | Send GET /projects/{project_id}/lca with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0238 | GET /projects/{project_id}/lca: unicode/emoji in names | Functional | P2 | Send GET /projects/{project_id}/lca with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0239 | GET /projects/{project_id}/lca: request while another rebuild is running | Negative | P2 | Send GET /projects/{project_id}/lca with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0240 | POST /projects/{project_id}/optimize: valid request | Functional | P1 | Send POST /projects/{project_id}/optimize with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0241 | POST /projects/{project_id}/optimize: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/optimize with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0242 | POST /projects/{project_id}/optimize: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/optimize with a malformed JSON body. | 422 with field-level errors. |  |
| API-0243 | POST /projects/{project_id}/optimize: wrong field types | Negative | P2 | Send POST /projects/{project_id}/optimize with a wrong field types. | 422 naming the field. |  |
| API-0244 | POST /projects/{project_id}/optimize: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/optimize with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0245 | POST /projects/{project_id}/optimize: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/optimize with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0246 | POST /projects/{project_id}/optimize: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/optimize with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0247 | POST /projects/{project_id}/optimize: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/optimize with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0248 | POST /projects/{project_id}/optimize: missing required field | Negative | P2 | Send POST /projects/{project_id}/optimize with a missing required field. | 422 naming the missing field. |  |
| API-0249 | POST /projects/{project_id}/optimize: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/optimize with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0250 | POST /projects/{project_id}/routes: valid request | Functional | P1 | Send POST /projects/{project_id}/routes with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0251 | POST /projects/{project_id}/routes: unknown project/part id | Negative | P2 | Send POST /projects/{project_id}/routes with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0252 | POST /projects/{project_id}/routes: malformed JSON body | Negative | P1 | Send POST /projects/{project_id}/routes with a malformed JSON body. | 422 with field-level errors. |  |
| API-0253 | POST /projects/{project_id}/routes: wrong field types | Negative | P2 | Send POST /projects/{project_id}/routes with a wrong field types. | 422 naming the field. |  |
| API-0254 | POST /projects/{project_id}/routes: out-of-range values | Negative | P2 | Send POST /projects/{project_id}/routes with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0255 | POST /projects/{project_id}/routes: oversized payload (50 MB) | Negative | P2 | Send POST /projects/{project_id}/routes with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0256 | POST /projects/{project_id}/routes: concurrent identical requests ×20 | Negative | P2 | Send POST /projects/{project_id}/routes with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0257 | POST /projects/{project_id}/routes: unicode/emoji in names | Functional | P2 | Send POST /projects/{project_id}/routes with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0258 | POST /projects/{project_id}/routes: missing required field | Negative | P2 | Send POST /projects/{project_id}/routes with a missing required field. | 422 naming the missing field. |  |
| API-0259 | POST /projects/{project_id}/routes: request while another rebuild is running | Negative | P2 | Send POST /projects/{project_id}/routes with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0260 | PUT /projects/{project_id}/vessel/spec: valid request | Functional | P1 | Send PUT /projects/{project_id}/vessel/spec with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0261 | PUT /projects/{project_id}/vessel/spec: unknown project/part id | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0262 | PUT /projects/{project_id}/vessel/spec: malformed JSON body | Negative | P1 | Send PUT /projects/{project_id}/vessel/spec with a malformed JSON body. | 422 with field-level errors. |  |
| API-0263 | PUT /projects/{project_id}/vessel/spec: wrong field types | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a wrong field types. | 422 naming the field. |  |
| API-0264 | PUT /projects/{project_id}/vessel/spec: out-of-range values | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0265 | PUT /projects/{project_id}/vessel/spec: oversized payload (50 MB) | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0266 | PUT /projects/{project_id}/vessel/spec: concurrent identical requests ×20 | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0267 | PUT /projects/{project_id}/vessel/spec: unicode/emoji in names | Functional | P2 | Send PUT /projects/{project_id}/vessel/spec with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0268 | PUT /projects/{project_id}/vessel/spec: missing required field | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a missing required field. | 422 naming the missing field. |  |
| API-0269 | PUT /projects/{project_id}/vessel/spec: request while another rebuild is running | Negative | P2 | Send PUT /projects/{project_id}/vessel/spec with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0270 | PUT /projects/{project_id}/aircraft/spec: valid request | Functional | P1 | Send PUT /projects/{project_id}/aircraft/spec with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0271 | PUT /projects/{project_id}/aircraft/spec: unknown project/part id | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0272 | PUT /projects/{project_id}/aircraft/spec: malformed JSON body | Negative | P1 | Send PUT /projects/{project_id}/aircraft/spec with a malformed JSON body. | 422 with field-level errors. |  |
| API-0273 | PUT /projects/{project_id}/aircraft/spec: wrong field types | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a wrong field types. | 422 naming the field. |  |
| API-0274 | PUT /projects/{project_id}/aircraft/spec: out-of-range values | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0275 | PUT /projects/{project_id}/aircraft/spec: oversized payload (50 MB) | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0276 | PUT /projects/{project_id}/aircraft/spec: concurrent identical requests ×20 | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0277 | PUT /projects/{project_id}/aircraft/spec: unicode/emoji in names | Functional | P2 | Send PUT /projects/{project_id}/aircraft/spec with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0278 | PUT /projects/{project_id}/aircraft/spec: missing required field | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a missing required field. | 422 naming the missing field. |  |
| API-0279 | PUT /projects/{project_id}/aircraft/spec: request while another rebuild is running | Negative | P2 | Send PUT /projects/{project_id}/aircraft/spec with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0280 | PUT /projects/{project_id}/engine/spec: valid request | Functional | P1 | Send PUT /projects/{project_id}/engine/spec with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0281 | PUT /projects/{project_id}/engine/spec: unknown project/part id | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0282 | PUT /projects/{project_id}/engine/spec: malformed JSON body | Negative | P1 | Send PUT /projects/{project_id}/engine/spec with a malformed JSON body. | 422 with field-level errors. |  |
| API-0283 | PUT /projects/{project_id}/engine/spec: wrong field types | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a wrong field types. | 422 naming the field. |  |
| API-0284 | PUT /projects/{project_id}/engine/spec: out-of-range values | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0285 | PUT /projects/{project_id}/engine/spec: oversized payload (50 MB) | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0286 | PUT /projects/{project_id}/engine/spec: concurrent identical requests ×20 | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0287 | PUT /projects/{project_id}/engine/spec: unicode/emoji in names | Functional | P2 | Send PUT /projects/{project_id}/engine/spec with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0288 | PUT /projects/{project_id}/engine/spec: missing required field | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a missing required field. | 422 naming the missing field. |  |
| API-0289 | PUT /projects/{project_id}/engine/spec: request while another rebuild is running | Negative | P2 | Send PUT /projects/{project_id}/engine/spec with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0290 | POST /sketch/solve: valid request | Functional | P1 | Send POST /sketch/solve with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0291 | POST /sketch/solve: malformed JSON body | Negative | P1 | Send POST /sketch/solve with a malformed JSON body. | 422 with field-level errors. |  |
| API-0292 | POST /sketch/solve: wrong field types | Negative | P2 | Send POST /sketch/solve with a wrong field types. | 422 naming the field. |  |
| API-0293 | POST /sketch/solve: out-of-range values | Negative | P2 | Send POST /sketch/solve with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0294 | POST /sketch/solve: oversized payload (50 MB) | Negative | P2 | Send POST /sketch/solve with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0295 | POST /sketch/solve: concurrent identical requests ×20 | Negative | P2 | Send POST /sketch/solve with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0296 | POST /sketch/solve: unicode/emoji in names | Functional | P2 | Send POST /sketch/solve with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0297 | POST /sketch/solve: missing required field | Negative | P2 | Send POST /sketch/solve with a missing required field. | 422 naming the missing field. |  |
| API-0298 | POST /sketch/solve: request while another rebuild is running | Negative | P2 | Send POST /sketch/solve with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0299 | POST /structures/run: valid request | Functional | P1 | Send POST /structures/run with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0300 | POST /structures/run: malformed JSON body | Negative | P1 | Send POST /structures/run with a malformed JSON body. | 422 with field-level errors. |  |
| API-0301 | POST /structures/run: wrong field types | Negative | P2 | Send POST /structures/run with a wrong field types. | 422 naming the field. |  |
| API-0302 | POST /structures/run: out-of-range values | Negative | P2 | Send POST /structures/run with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0303 | POST /structures/run: oversized payload (50 MB) | Negative | P2 | Send POST /structures/run with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0304 | POST /structures/run: concurrent identical requests ×20 | Negative | P2 | Send POST /structures/run with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0305 | POST /structures/run: unicode/emoji in names | Functional | P2 | Send POST /structures/run with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0306 | POST /structures/run: missing required field | Negative | P2 | Send POST /structures/run with a missing required field. | 422 naming the missing field. |  |
| API-0307 | POST /structures/run: request while another rebuild is running | Negative | P2 | Send POST /structures/run with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0308 | POST /structures/topology: valid request | Functional | P1 | Send POST /structures/topology with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0309 | POST /structures/topology: malformed JSON body | Negative | P1 | Send POST /structures/topology with a malformed JSON body. | 422 with field-level errors. |  |
| API-0310 | POST /structures/topology: wrong field types | Negative | P2 | Send POST /structures/topology with a wrong field types. | 422 naming the field. |  |
| API-0311 | POST /structures/topology: out-of-range values | Negative | P2 | Send POST /structures/topology with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0312 | POST /structures/topology: oversized payload (50 MB) | Negative | P2 | Send POST /structures/topology with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0313 | POST /structures/topology: concurrent identical requests ×20 | Negative | P2 | Send POST /structures/topology with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0314 | POST /structures/topology: unicode/emoji in names | Functional | P2 | Send POST /structures/topology with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0315 | POST /structures/topology: missing required field | Negative | P2 | Send POST /structures/topology with a missing required field. | 422 naming the missing field. |  |
| API-0316 | POST /structures/topology: request while another rebuild is running | Negative | P2 | Send POST /structures/topology with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0317 | POST /structures/mesh: valid request | Functional | P1 | Send POST /structures/mesh with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0318 | POST /structures/mesh: malformed JSON body | Negative | P1 | Send POST /structures/mesh with a malformed JSON body. | 422 with field-level errors. |  |
| API-0319 | POST /structures/mesh: wrong field types | Negative | P2 | Send POST /structures/mesh with a wrong field types. | 422 naming the field. |  |
| API-0320 | POST /structures/mesh: out-of-range values | Negative | P2 | Send POST /structures/mesh with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0321 | POST /structures/mesh: oversized payload (50 MB) | Negative | P2 | Send POST /structures/mesh with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0322 | POST /structures/mesh: concurrent identical requests ×20 | Negative | P2 | Send POST /structures/mesh with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0323 | POST /structures/mesh: unicode/emoji in names | Functional | P2 | Send POST /structures/mesh with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0324 | POST /structures/mesh: missing required field | Negative | P2 | Send POST /structures/mesh with a missing required field. | 422 naming the missing field. |  |
| API-0325 | POST /structures/mesh: request while another rebuild is running | Negative | P2 | Send POST /structures/mesh with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0326 | POST /aero/analyse: valid request | Functional | P1 | Send POST /aero/analyse with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0327 | POST /aero/analyse: malformed JSON body | Negative | P1 | Send POST /aero/analyse with a malformed JSON body. | 422 with field-level errors. |  |
| API-0328 | POST /aero/analyse: wrong field types | Negative | P2 | Send POST /aero/analyse with a wrong field types. | 422 naming the field. |  |
| API-0329 | POST /aero/analyse: out-of-range values | Negative | P2 | Send POST /aero/analyse with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0330 | POST /aero/analyse: oversized payload (50 MB) | Negative | P2 | Send POST /aero/analyse with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0331 | POST /aero/analyse: concurrent identical requests ×20 | Negative | P2 | Send POST /aero/analyse with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0332 | POST /aero/analyse: unicode/emoji in names | Functional | P2 | Send POST /aero/analyse with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0333 | POST /aero/analyse: missing required field | Negative | P2 | Send POST /aero/analyse with a missing required field. | 422 naming the missing field. |  |
| API-0334 | POST /aero/analyse: request while another rebuild is running | Negative | P2 | Send POST /aero/analyse with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0335 | POST /marine/analyse: valid request | Functional | P1 | Send POST /marine/analyse with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0336 | POST /marine/analyse: malformed JSON body | Negative | P1 | Send POST /marine/analyse with a malformed JSON body. | 422 with field-level errors. |  |
| API-0337 | POST /marine/analyse: wrong field types | Negative | P2 | Send POST /marine/analyse with a wrong field types. | 422 naming the field. |  |
| API-0338 | POST /marine/analyse: out-of-range values | Negative | P2 | Send POST /marine/analyse with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0339 | POST /marine/analyse: oversized payload (50 MB) | Negative | P2 | Send POST /marine/analyse with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0340 | POST /marine/analyse: concurrent identical requests ×20 | Negative | P2 | Send POST /marine/analyse with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0341 | POST /marine/analyse: unicode/emoji in names | Functional | P2 | Send POST /marine/analyse with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0342 | POST /marine/analyse: missing required field | Negative | P2 | Send POST /marine/analyse with a missing required field. | 422 naming the missing field. |  |
| API-0343 | POST /marine/analyse: request while another rebuild is running | Negative | P2 | Send POST /marine/analyse with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0344 | POST /engines/analyse: valid request | Functional | P1 | Send POST /engines/analyse with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0345 | POST /engines/analyse: malformed JSON body | Negative | P1 | Send POST /engines/analyse with a malformed JSON body. | 422 with field-level errors. |  |
| API-0346 | POST /engines/analyse: wrong field types | Negative | P2 | Send POST /engines/analyse with a wrong field types. | 422 naming the field. |  |
| API-0347 | POST /engines/analyse: out-of-range values | Negative | P2 | Send POST /engines/analyse with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0348 | POST /engines/analyse: oversized payload (50 MB) | Negative | P2 | Send POST /engines/analyse with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0349 | POST /engines/analyse: concurrent identical requests ×20 | Negative | P2 | Send POST /engines/analyse with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0350 | POST /engines/analyse: unicode/emoji in names | Functional | P2 | Send POST /engines/analyse with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0351 | POST /engines/analyse: missing required field | Negative | P2 | Send POST /engines/analyse with a missing required field. | 422 naming the missing field. |  |
| API-0352 | POST /engines/analyse: request while another rebuild is running | Negative | P2 | Send POST /engines/analyse with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0353 | POST /composites/laminate: valid request | Functional | P1 | Send POST /composites/laminate with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0354 | POST /composites/laminate: malformed JSON body | Negative | P1 | Send POST /composites/laminate with a malformed JSON body. | 422 with field-level errors. |  |
| API-0355 | POST /composites/laminate: wrong field types | Negative | P2 | Send POST /composites/laminate with a wrong field types. | 422 naming the field. |  |
| API-0356 | POST /composites/laminate: out-of-range values | Negative | P2 | Send POST /composites/laminate with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0357 | POST /composites/laminate: oversized payload (50 MB) | Negative | P2 | Send POST /composites/laminate with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0358 | POST /composites/laminate: concurrent identical requests ×20 | Negative | P2 | Send POST /composites/laminate with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0359 | POST /composites/laminate: unicode/emoji in names | Functional | P2 | Send POST /composites/laminate with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0360 | POST /composites/laminate: missing required field | Negative | P2 | Send POST /composites/laminate with a missing required field. | 422 naming the missing field. |  |
| API-0361 | POST /composites/laminate: request while another rebuild is running | Negative | P2 | Send POST /composites/laminate with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0362 | POST /quality/stackup: valid request | Functional | P1 | Send POST /quality/stackup with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0363 | POST /quality/stackup: malformed JSON body | Negative | P1 | Send POST /quality/stackup with a malformed JSON body. | 422 with field-level errors. |  |
| API-0364 | POST /quality/stackup: wrong field types | Negative | P2 | Send POST /quality/stackup with a wrong field types. | 422 naming the field. |  |
| API-0365 | POST /quality/stackup: out-of-range values | Negative | P2 | Send POST /quality/stackup with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0366 | POST /quality/stackup: oversized payload (50 MB) | Negative | P2 | Send POST /quality/stackup with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0367 | POST /quality/stackup: concurrent identical requests ×20 | Negative | P2 | Send POST /quality/stackup with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0368 | POST /quality/stackup: unicode/emoji in names | Functional | P2 | Send POST /quality/stackup with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0369 | POST /quality/stackup: missing required field | Negative | P2 | Send POST /quality/stackup with a missing required field. | 422 naming the missing field. |  |
| API-0370 | POST /quality/stackup: request while another rebuild is running | Negative | P2 | Send POST /quality/stackup with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0371 | POST /routing/harness: valid request | Functional | P1 | Send POST /routing/harness with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0372 | POST /routing/harness: malformed JSON body | Negative | P1 | Send POST /routing/harness with a malformed JSON body. | 422 with field-level errors. |  |
| API-0373 | POST /routing/harness: wrong field types | Negative | P2 | Send POST /routing/harness with a wrong field types. | 422 naming the field. |  |
| API-0374 | POST /routing/harness: out-of-range values | Negative | P2 | Send POST /routing/harness with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0375 | POST /routing/harness: oversized payload (50 MB) | Negative | P2 | Send POST /routing/harness with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0376 | POST /routing/harness: concurrent identical requests ×20 | Negative | P2 | Send POST /routing/harness with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0377 | POST /routing/harness: unicode/emoji in names | Functional | P2 | Send POST /routing/harness with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0378 | POST /routing/harness: missing required field | Negative | P2 | Send POST /routing/harness with a missing required field. | 422 naming the missing field. |  |
| API-0379 | POST /routing/harness: request while another rebuild is running | Negative | P2 | Send POST /routing/harness with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0380 | POST /routing/pipe: valid request | Functional | P1 | Send POST /routing/pipe with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0381 | POST /routing/pipe: malformed JSON body | Negative | P1 | Send POST /routing/pipe with a malformed JSON body. | 422 with field-level errors. |  |
| API-0382 | POST /routing/pipe: wrong field types | Negative | P2 | Send POST /routing/pipe with a wrong field types. | 422 naming the field. |  |
| API-0383 | POST /routing/pipe: out-of-range values | Negative | P2 | Send POST /routing/pipe with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0384 | POST /routing/pipe: oversized payload (50 MB) | Negative | P2 | Send POST /routing/pipe with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0385 | POST /routing/pipe: concurrent identical requests ×20 | Negative | P2 | Send POST /routing/pipe with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0386 | POST /routing/pipe: unicode/emoji in names | Functional | P2 | Send POST /routing/pipe with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0387 | POST /routing/pipe: missing required field | Negative | P2 | Send POST /routing/pipe with a missing required field. | 422 naming the missing field. |  |
| API-0388 | POST /routing/pipe: request while another rebuild is running | Negative | P2 | Send POST /routing/pipe with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0389 | POST /continuity: valid request | Functional | P1 | Send POST /continuity with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0390 | POST /continuity: malformed JSON body | Negative | P1 | Send POST /continuity with a malformed JSON body. | 422 with field-level errors. |  |
| API-0391 | POST /continuity: wrong field types | Negative | P2 | Send POST /continuity with a wrong field types. | 422 naming the field. |  |
| API-0392 | POST /continuity: out-of-range values | Negative | P2 | Send POST /continuity with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0393 | POST /continuity: oversized payload (50 MB) | Negative | P2 | Send POST /continuity with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0394 | POST /continuity: concurrent identical requests ×20 | Negative | P2 | Send POST /continuity with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0395 | POST /continuity: unicode/emoji in names | Functional | P2 | Send POST /continuity with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0396 | POST /continuity: missing required field | Negative | P2 | Send POST /continuity with a missing required field. | 422 naming the missing field. |  |
| API-0397 | POST /continuity: request while another rebuild is running | Negative | P2 | Send POST /continuity with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0398 | POST /join: valid request | Functional | P1 | Send POST /join with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0399 | POST /join: malformed JSON body | Negative | P1 | Send POST /join with a malformed JSON body. | 422 with field-level errors. |  |
| API-0400 | POST /join: wrong field types | Negative | P2 | Send POST /join with a wrong field types. | 422 naming the field. |  |
| API-0401 | POST /join: out-of-range values | Negative | P2 | Send POST /join with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0402 | POST /join: oversized payload (50 MB) | Negative | P2 | Send POST /join with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0403 | POST /join: concurrent identical requests ×20 | Negative | P2 | Send POST /join with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0404 | POST /join: unicode/emoji in names | Functional | P2 | Send POST /join with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0405 | POST /join: missing required field | Negative | P2 | Send POST /join with a missing required field. | 422 naming the missing field. |  |
| API-0406 | POST /join: request while another rebuild is running | Negative | P2 | Send POST /join with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0407 | POST /insert-knot: valid request | Functional | P1 | Send POST /insert-knot with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0408 | POST /insert-knot: malformed JSON body | Negative | P1 | Send POST /insert-knot with a malformed JSON body. | 422 with field-level errors. |  |
| API-0409 | POST /insert-knot: wrong field types | Negative | P2 | Send POST /insert-knot with a wrong field types. | 422 naming the field. |  |
| API-0410 | POST /insert-knot: out-of-range values | Negative | P2 | Send POST /insert-knot with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0411 | POST /insert-knot: oversized payload (50 MB) | Negative | P2 | Send POST /insert-knot with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0412 | POST /insert-knot: concurrent identical requests ×20 | Negative | P2 | Send POST /insert-knot with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0413 | POST /insert-knot: unicode/emoji in names | Functional | P2 | Send POST /insert-knot with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0414 | POST /insert-knot: missing required field | Negative | P2 | Send POST /insert-knot with a missing required field. | 422 naming the missing field. |  |
| API-0415 | POST /insert-knot: request while another rebuild is running | Negative | P2 | Send POST /insert-knot with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0416 | POST /mechanisms/fourbar: valid request | Functional | P1 | Send POST /mechanisms/fourbar with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0417 | POST /mechanisms/fourbar: malformed JSON body | Negative | P1 | Send POST /mechanisms/fourbar with a malformed JSON body. | 422 with field-level errors. |  |
| API-0418 | POST /mechanisms/fourbar: wrong field types | Negative | P2 | Send POST /mechanisms/fourbar with a wrong field types. | 422 naming the field. |  |
| API-0419 | POST /mechanisms/fourbar: out-of-range values | Negative | P2 | Send POST /mechanisms/fourbar with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0420 | POST /mechanisms/fourbar: oversized payload (50 MB) | Negative | P2 | Send POST /mechanisms/fourbar with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0421 | POST /mechanisms/fourbar: concurrent identical requests ×20 | Negative | P2 | Send POST /mechanisms/fourbar with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0422 | POST /mechanisms/fourbar: unicode/emoji in names | Functional | P2 | Send POST /mechanisms/fourbar with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0423 | POST /mechanisms/fourbar: missing required field | Negative | P2 | Send POST /mechanisms/fourbar with a missing required field. | 422 naming the missing field. |  |
| API-0424 | POST /mechanisms/fourbar: request while another rebuild is running | Negative | P2 | Send POST /mechanisms/fourbar with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0425 | POST /mechanisms/slider-crank: valid request | Functional | P1 | Send POST /mechanisms/slider-crank with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0426 | POST /mechanisms/slider-crank: malformed JSON body | Negative | P1 | Send POST /mechanisms/slider-crank with a malformed JSON body. | 422 with field-level errors. |  |
| API-0427 | POST /mechanisms/slider-crank: wrong field types | Negative | P2 | Send POST /mechanisms/slider-crank with a wrong field types. | 422 naming the field. |  |
| API-0428 | POST /mechanisms/slider-crank: out-of-range values | Negative | P2 | Send POST /mechanisms/slider-crank with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0429 | POST /mechanisms/slider-crank: oversized payload (50 MB) | Negative | P2 | Send POST /mechanisms/slider-crank with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0430 | POST /mechanisms/slider-crank: concurrent identical requests ×20 | Negative | P2 | Send POST /mechanisms/slider-crank with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0431 | POST /mechanisms/slider-crank: unicode/emoji in names | Functional | P2 | Send POST /mechanisms/slider-crank with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0432 | POST /mechanisms/slider-crank: missing required field | Negative | P2 | Send POST /mechanisms/slider-crank with a missing required field. | 422 naming the missing field. |  |
| API-0433 | POST /mechanisms/slider-crank: request while another rebuild is running | Negative | P2 | Send POST /mechanisms/slider-crank with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0434 | GET /inventory: valid request | Functional | P1 | Send GET /inventory with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0435 | GET /inventory: out-of-range values | Negative | P2 | Send GET /inventory with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0436 | GET /inventory: concurrent identical requests ×20 | Negative | P2 | Send GET /inventory with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0437 | GET /inventory: unicode/emoji in names | Functional | P2 | Send GET /inventory with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0438 | GET /inventory: request while another rebuild is running | Negative | P2 | Send GET /inventory with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0439 | GET /materials: valid request | Functional | P1 | Send GET /materials with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0440 | GET /materials: out-of-range values | Negative | P2 | Send GET /materials with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0441 | GET /materials: concurrent identical requests ×20 | Negative | P2 | Send GET /materials with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0442 | GET /materials: unicode/emoji in names | Functional | P2 | Send GET /materials with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0443 | GET /materials: request while another rebuild is running | Negative | P2 | Send GET /materials with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0444 | GET /templates: valid request | Functional | P1 | Send GET /templates with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0445 | GET /templates: out-of-range values | Negative | P2 | Send GET /templates with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0446 | GET /templates: concurrent identical requests ×20 | Negative | P2 | Send GET /templates with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0447 | GET /templates: unicode/emoji in names | Functional | P2 | Send GET /templates with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0448 | GET /templates: request while another rebuild is running | Negative | P2 | Send GET /templates with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0449 | GET /parameters: valid request | Functional | P1 | Send GET /parameters with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0450 | GET /parameters: out-of-range values | Negative | P2 | Send GET /parameters with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0451 | GET /parameters: concurrent identical requests ×20 | Negative | P2 | Send GET /parameters with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0452 | GET /parameters: unicode/emoji in names | Functional | P2 | Send GET /parameters with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0453 | GET /parameters: request while another rebuild is running | Negative | P2 | Send GET /parameters with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0454 | GET /plugins: valid request | Functional | P1 | Send GET /plugins with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0455 | GET /plugins: out-of-range values | Negative | P2 | Send GET /plugins with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0456 | GET /plugins: concurrent identical requests ×20 | Negative | P2 | Send GET /plugins with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0457 | GET /plugins: unicode/emoji in names | Functional | P2 | Send GET /plugins with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0458 | GET /plugins: request while another rebuild is running | Negative | P2 | Send GET /plugins with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0459 | POST /feature-templates: valid request | Functional | P1 | Send POST /feature-templates with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0460 | POST /feature-templates: malformed JSON body | Negative | P1 | Send POST /feature-templates with a malformed JSON body. | 422 with field-level errors. |  |
| API-0461 | POST /feature-templates: wrong field types | Negative | P2 | Send POST /feature-templates with a wrong field types. | 422 naming the field. |  |
| API-0462 | POST /feature-templates: out-of-range values | Negative | P2 | Send POST /feature-templates with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0463 | POST /feature-templates: oversized payload (50 MB) | Negative | P2 | Send POST /feature-templates with a oversized payload (50 MB). | 413 or 422; server stays responsive. |  |
| API-0464 | POST /feature-templates: concurrent identical requests ×20 | Negative | P2 | Send POST /feature-templates with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0465 | POST /feature-templates: unicode/emoji in names | Functional | P2 | Send POST /feature-templates with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0466 | POST /feature-templates: missing required field | Negative | P2 | Send POST /feature-templates with a missing required field. | 422 naming the missing field. |  |
| API-0467 | POST /feature-templates: request while another rebuild is running | Negative | P2 | Send POST /feature-templates with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |
| API-0468 | DELETE /feature-templates/{template_id}: valid request | Functional | P1 | Send DELETE /feature-templates/{template_id} with a valid request. | 2xx with a body matching the OpenAPI schema. |  |
| API-0469 | DELETE /feature-templates/{template_id}: unknown project/part id | Negative | P2 | Send DELETE /feature-templates/{template_id} with a unknown project/part id. | 404 with a JSON error, no stack trace. |  |
| API-0470 | DELETE /feature-templates/{template_id}: out-of-range values | Negative | P2 | Send DELETE /feature-templates/{template_id} with a out-of-range values. | 422 or a 4xx rule violation listing the rule. |  |
| API-0471 | DELETE /feature-templates/{template_id}: concurrent identical requests ×20 | Negative | P2 | Send DELETE /feature-templates/{template_id} with a concurrent identical requests ×20. | No 5xx; consistent final state. |  |
| API-0472 | DELETE /feature-templates/{template_id}: unicode/emoji in names | Functional | P2 | Send DELETE /feature-templates/{template_id} with a unicode/emoji in names. | Stored and returned intact. |  |
| API-0473 | DELETE /feature-templates/{template_id}: request while another rebuild is running | Negative | P2 | Send DELETE /feature-templates/{template_id} with a request while another rebuild is running. | Queued or 409; never a corrupted model. |  |

## Scripting and plugins

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| API-0474 | plugin entry point registers a part builder (local) | Functional | P2 | Exercise: plugin entry point registers a part builder. | Works as documented; errors are actionable. |  |
| API-0475 | plugin entry point registers a part builder (Docker) | Functional | P2 | Exercise: plugin entry point registers a part builder. | Works as documented; errors are actionable. |  |
| API-0476 | plugin entry point registers a part builder (desktop sidecar) | Functional | P2 | Exercise: plugin entry point registers a part builder. | Works as documented; errors are actionable. |  |
| API-0477 | plugin with a bad manifest (local) | Functional | P2 | Exercise: plugin with a bad manifest. | Works as documented; errors are actionable. |  |
| API-0478 | plugin with a bad manifest (Docker) | Functional | P2 | Exercise: plugin with a bad manifest. | Works as documented; errors are actionable. |  |
| API-0479 | plugin with a bad manifest (desktop sidecar) | Functional | P2 | Exercise: plugin with a bad manifest. | Works as documented; errors are actionable. |  |
| API-0480 | macro recording of UI actions (local) | Functional | P2 | Exercise: macro recording of UI actions. | Works as documented; errors are actionable. |  |
| API-0481 | macro recording of UI actions (Docker) | Functional | P2 | Exercise: macro recording of UI actions. | Works as documented; errors are actionable. |  |
| API-0482 | macro recording of UI actions (desktop sidecar) | Functional | P2 | Exercise: macro recording of UI actions. | Works as documented; errors are actionable. |  |
| API-0483 | Python script runs a parameter sweep (local) | Functional | P2 | Exercise: Python script runs a parameter sweep. | Works as documented; errors are actionable. |  |
| API-0484 | Python script runs a parameter sweep (Docker) | Functional | P2 | Exercise: Python script runs a parameter sweep. | Works as documented; errors are actionable. |  |
| API-0485 | Python script runs a parameter sweep (desktop sidecar) | Functional | P2 | Exercise: Python script runs a parameter sweep. | Works as documented; errors are actionable. |  |
| API-0486 | headless batch rebuild (local) | Functional | P2 | Exercise: headless batch rebuild. | Works as documented; errors are actionable. |  |
| API-0487 | headless batch rebuild (Docker) | Functional | P2 | Exercise: headless batch rebuild. | Works as documented; errors are actionable. |  |
| API-0488 | headless batch rebuild (desktop sidecar) | Functional | P2 | Exercise: headless batch rebuild. | Works as documented; errors are actionable. |  |
| API-0489 | journal replay (local) | Functional | P2 | Exercise: journal replay. | Works as documented; errors are actionable. |  |
| API-0490 | journal replay (Docker) | Functional | P2 | Exercise: journal replay. | Works as documented; errors are actionable. |  |
| API-0491 | journal replay (desktop sidecar) | Functional | P2 | Exercise: journal replay. | Works as documented; errors are actionable. |  |
| API-0492 | API token auth (local) | Functional | P2 | Exercise: API token auth. | Works as documented; errors are actionable. |  |
| API-0493 | API token auth (Docker) | Functional | P2 | Exercise: API token auth. | Works as documented; errors are actionable. |  |
| API-0494 | API token auth (desktop sidecar) | Functional | P2 | Exercise: API token auth. | Works as documented; errors are actionable. |  |
| API-0495 | rate limiting (local) | Functional | P2 | Exercise: rate limiting. | Works as documented; errors are actionable. |  |
| API-0496 | rate limiting (Docker) | Functional | P2 | Exercise: rate limiting. | Works as documented; errors are actionable. |  |
| API-0497 | rate limiting (desktop sidecar) | Functional | P2 | Exercise: rate limiting. | Works as documented; errors are actionable. |  |
| API-0498 | OpenAPI client generation (TS) (local) | Functional | P2 | Exercise: OpenAPI client generation (TS). | Works as documented; errors are actionable. |  |
| API-0499 | OpenAPI client generation (TS) (Docker) | Functional | P2 | Exercise: OpenAPI client generation (TS). | Works as documented; errors are actionable. |  |
| API-0500 | OpenAPI client generation (TS) (desktop sidecar) | Functional | P2 | Exercise: OpenAPI client generation (TS). | Works as documented; errors are actionable. |  |
| API-0501 | webhook on change approval (local) | Functional | P2 | Exercise: webhook on change approval. | Works as documented; errors are actionable. |  |
| API-0502 | webhook on change approval (Docker) | Functional | P2 | Exercise: webhook on change approval. | Works as documented; errors are actionable. |  |
| API-0503 | webhook on change approval (desktop sidecar) | Functional | P2 | Exercise: webhook on change approval. | Works as documented; errors are actionable. |  |
