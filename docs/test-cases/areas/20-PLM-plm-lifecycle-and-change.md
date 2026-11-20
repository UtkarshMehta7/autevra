# PLM — PLM, lifecycle and change

**CATIA-class equivalent:** ENOVIA / 3DEXPERIENCE collaboration  
**Autevra workspace:** Reviews; Digital thread; Breakdown  
**Scope:** Shared  
**Cases:** 208 (Have 36, Partial 12, Gap 160)

Revisions, lifecycle, baselines, change requests, access control and audit.

[← Back to the index](../README.md)

## Features

- Lifecycle transitions — 12 cases (Partial)
- Access control — 112 cases (Gap)
- Revisions and baselines — 40 cases (Have)
- Engineering change — 24 cases (Have)
- Collaboration — 20 cases (Gap)

## Lifecycle transitions

Status in Autevra: **Partial**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLM-0001 | Promote In Work → In Review | Functional | P1 | Attempt the transition on a part. | Allowed; history records who/when/why. |  |
| PLM-0002 | Promote In Work → Released | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0003 | Promote In Work → Obsolete | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0004 | Promote In Review → In Work | Functional | P1 | Attempt the transition on a part. | Allowed; history records who/when/why. |  |
| PLM-0005 | Promote In Review → Released | Functional | P1 | Attempt the transition on a part. | Allowed; history records who/when/why. |  |
| PLM-0006 | Promote In Review → Obsolete | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0007 | Promote Released → In Work | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0008 | Promote Released → In Review | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0009 | Promote Released → Obsolete | Functional | P1 | Attempt the transition on a part. | Allowed; history records who/when/why. |  |
| PLM-0010 | Promote Obsolete → In Work | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0011 | Promote Obsolete → In Review | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |
| PLM-0012 | Promote Obsolete → Released | Negative | P1 | Attempt the transition on a part. | Refused: transition not in the lifecycle graph. |  |

## Access control

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLM-0013 | Viewer tries 'edit' on a In Work item | Negative | P2 | Log in as Viewer; edit. | Refused: Viewer lacks 'edit'. |  |
| PLM-0014 | Viewer tries 'edit' on a In Review item | Negative | P2 | Log in as Viewer; edit. | Refused: Viewer lacks 'edit'. |  |
| PLM-0015 | Viewer tries 'edit' on a Released item | Negative | P2 | Log in as Viewer; edit. | Refused: Viewer lacks 'edit'. |  |
| PLM-0016 | Viewer tries 'edit' on a Obsolete item | Negative | P2 | Log in as Viewer; edit. | Refused: Viewer lacks 'edit'. |  |
| PLM-0017 | Viewer tries 'submit' on a In Work item | Negative | P2 | Log in as Viewer; submit. | Refused: Viewer lacks 'submit'. |  |
| PLM-0018 | Viewer tries 'submit' on a In Review item | Negative | P2 | Log in as Viewer; submit. | Refused: Viewer lacks 'submit'. |  |
| PLM-0019 | Viewer tries 'submit' on a Released item | Negative | P2 | Log in as Viewer; submit. | Refused: Viewer lacks 'submit'. |  |
| PLM-0020 | Viewer tries 'submit' on a Obsolete item | Negative | P2 | Log in as Viewer; submit. | Refused: Viewer lacks 'submit'. |  |
| PLM-0021 | Viewer tries 'approve' on a In Work item | Negative | P2 | Log in as Viewer; approve. | Refused: Viewer lacks 'approve'. |  |
| PLM-0022 | Viewer tries 'approve' on a In Review item | Negative | P2 | Log in as Viewer; approve. | Refused: Viewer lacks 'approve'. |  |
| PLM-0023 | Viewer tries 'approve' on a Released item | Negative | P2 | Log in as Viewer; approve. | Refused: Viewer lacks 'approve'. |  |
| PLM-0024 | Viewer tries 'approve' on a Obsolete item | Negative | P2 | Log in as Viewer; approve. | Refused: Viewer lacks 'approve'. |  |
| PLM-0025 | Viewer tries 'reject' on a In Work item | Negative | P2 | Log in as Viewer; reject. | Refused: Viewer lacks 'reject'. |  |
| PLM-0026 | Viewer tries 'reject' on a In Review item | Negative | P2 | Log in as Viewer; reject. | Refused: Viewer lacks 'reject'. |  |
| PLM-0027 | Viewer tries 'reject' on a Released item | Negative | P2 | Log in as Viewer; reject. | Refused: Viewer lacks 'reject'. |  |
| PLM-0028 | Viewer tries 'reject' on a Obsolete item | Negative | P2 | Log in as Viewer; reject. | Refused: Viewer lacks 'reject'. |  |
| PLM-0029 | Viewer tries 'revise' on a In Work item | Negative | P2 | Log in as Viewer; revise. | Refused: Viewer lacks 'revise'. |  |
| PLM-0030 | Viewer tries 'revise' on a In Review item | Negative | P2 | Log in as Viewer; revise. | Refused: Viewer lacks 'revise'. |  |
| PLM-0031 | Viewer tries 'revise' on a Released item | Negative | P2 | Log in as Viewer; revise. | Refused: Viewer lacks 'revise'. |  |
| PLM-0032 | Viewer tries 'revise' on a Obsolete item | Negative | P2 | Log in as Viewer; revise. | Refused: Viewer lacks 'revise'. |  |
| PLM-0033 | Viewer tries 'obsolete' on a In Work item | Negative | P2 | Log in as Viewer; obsolete. | Refused: Viewer lacks 'obsolete'. |  |
| PLM-0034 | Viewer tries 'obsolete' on a In Review item | Negative | P2 | Log in as Viewer; obsolete. | Refused: Viewer lacks 'obsolete'. |  |
| PLM-0035 | Viewer tries 'obsolete' on a Released item | Negative | P2 | Log in as Viewer; obsolete. | Refused: Viewer lacks 'obsolete'. |  |
| PLM-0036 | Viewer tries 'obsolete' on a Obsolete item | Negative | P2 | Log in as Viewer; obsolete. | Refused: Viewer lacks 'obsolete'. |  |
| PLM-0037 | Viewer tries 'delete' on a In Work item | Negative | P2 | Log in as Viewer; delete. | Refused: Viewer lacks 'delete'. |  |
| PLM-0038 | Viewer tries 'delete' on a In Review item | Negative | P2 | Log in as Viewer; delete. | Refused: Viewer lacks 'delete'. |  |
| PLM-0039 | Viewer tries 'delete' on a Released item | Negative | P2 | Log in as Viewer; delete. | Refused: Viewer lacks 'delete'. |  |
| PLM-0040 | Viewer tries 'delete' on a Obsolete item | Negative | P2 | Log in as Viewer; delete. | Refused: Viewer lacks 'delete'. |  |
| PLM-0041 | Designer tries 'edit' on a In Work item | Functional | P2 | Log in as Designer; edit. | Allowed and audited. |  |
| PLM-0042 | Designer tries 'edit' on a In Review item | Functional | P2 | Log in as Designer; edit. | Allowed and audited. |  |
| PLM-0043 | Designer tries 'edit' on a Released item | Negative | P2 | Log in as Designer; edit. | Refused: released data is frozen (revise instead). |  |
| PLM-0044 | Designer tries 'edit' on a Obsolete item | Negative | P2 | Log in as Designer; edit. | Refused: released data is frozen (revise instead). |  |
| PLM-0045 | Designer tries 'submit' on a In Work item | Functional | P2 | Log in as Designer; submit. | Allowed and audited. |  |
| PLM-0046 | Designer tries 'submit' on a In Review item | Functional | P2 | Log in as Designer; submit. | Allowed and audited. |  |
| PLM-0047 | Designer tries 'submit' on a Released item | Functional | P2 | Log in as Designer; submit. | Allowed and audited. |  |
| PLM-0048 | Designer tries 'submit' on a Obsolete item | Functional | P2 | Log in as Designer; submit. | Allowed and audited. |  |
| PLM-0049 | Designer tries 'approve' on a In Work item | Negative | P2 | Log in as Designer; approve. | Refused: Designer lacks 'approve'. |  |
| PLM-0050 | Designer tries 'approve' on a In Review item | Negative | P2 | Log in as Designer; approve. | Refused: Designer lacks 'approve'. |  |
| PLM-0051 | Designer tries 'approve' on a Released item | Negative | P2 | Log in as Designer; approve. | Refused: Designer lacks 'approve'. |  |
| PLM-0052 | Designer tries 'approve' on a Obsolete item | Negative | P2 | Log in as Designer; approve. | Refused: Designer lacks 'approve'. |  |
| PLM-0053 | Designer tries 'reject' on a In Work item | Negative | P2 | Log in as Designer; reject. | Refused: Designer lacks 'reject'. |  |
| PLM-0054 | Designer tries 'reject' on a In Review item | Negative | P2 | Log in as Designer; reject. | Refused: Designer lacks 'reject'. |  |
| PLM-0055 | Designer tries 'reject' on a Released item | Negative | P2 | Log in as Designer; reject. | Refused: Designer lacks 'reject'. |  |
| PLM-0056 | Designer tries 'reject' on a Obsolete item | Negative | P2 | Log in as Designer; reject. | Refused: Designer lacks 'reject'. |  |
| PLM-0057 | Designer tries 'revise' on a In Work item | Functional | P2 | Log in as Designer; revise. | Allowed and audited. |  |
| PLM-0058 | Designer tries 'revise' on a In Review item | Functional | P2 | Log in as Designer; revise. | Allowed and audited. |  |
| PLM-0059 | Designer tries 'revise' on a Released item | Functional | P2 | Log in as Designer; revise. | Allowed and audited. |  |
| PLM-0060 | Designer tries 'revise' on a Obsolete item | Functional | P2 | Log in as Designer; revise. | Allowed and audited. |  |
| PLM-0061 | Designer tries 'obsolete' on a In Work item | Negative | P2 | Log in as Designer; obsolete. | Refused: Designer lacks 'obsolete'. |  |
| PLM-0062 | Designer tries 'obsolete' on a In Review item | Negative | P2 | Log in as Designer; obsolete. | Refused: Designer lacks 'obsolete'. |  |
| PLM-0063 | Designer tries 'obsolete' on a Released item | Negative | P2 | Log in as Designer; obsolete. | Refused: Designer lacks 'obsolete'. |  |
| PLM-0064 | Designer tries 'obsolete' on a Obsolete item | Negative | P2 | Log in as Designer; obsolete. | Refused: Designer lacks 'obsolete'. |  |
| PLM-0065 | Designer tries 'delete' on a In Work item | Negative | P2 | Log in as Designer; delete. | Refused: Designer lacks 'delete'. |  |
| PLM-0066 | Designer tries 'delete' on a In Review item | Negative | P2 | Log in as Designer; delete. | Refused: Designer lacks 'delete'. |  |
| PLM-0067 | Designer tries 'delete' on a Released item | Negative | P2 | Log in as Designer; delete. | Refused: Designer lacks 'delete'. |  |
| PLM-0068 | Designer tries 'delete' on a Obsolete item | Negative | P2 | Log in as Designer; delete. | Refused: Designer lacks 'delete'. |  |
| PLM-0069 | Reviewer tries 'edit' on a In Work item | Negative | P2 | Log in as Reviewer; edit. | Refused: Reviewer lacks 'edit'. |  |
| PLM-0070 | Reviewer tries 'edit' on a In Review item | Negative | P2 | Log in as Reviewer; edit. | Refused: Reviewer lacks 'edit'. |  |
| PLM-0071 | Reviewer tries 'edit' on a Released item | Negative | P2 | Log in as Reviewer; edit. | Refused: Reviewer lacks 'edit'. |  |
| PLM-0072 | Reviewer tries 'edit' on a Obsolete item | Negative | P2 | Log in as Reviewer; edit. | Refused: Reviewer lacks 'edit'. |  |
| PLM-0073 | Reviewer tries 'submit' on a In Work item | Negative | P2 | Log in as Reviewer; submit. | Refused: Reviewer lacks 'submit'. |  |
| PLM-0074 | Reviewer tries 'submit' on a In Review item | Negative | P2 | Log in as Reviewer; submit. | Refused: Reviewer lacks 'submit'. |  |
| PLM-0075 | Reviewer tries 'submit' on a Released item | Negative | P2 | Log in as Reviewer; submit. | Refused: Reviewer lacks 'submit'. |  |
| PLM-0076 | Reviewer tries 'submit' on a Obsolete item | Negative | P2 | Log in as Reviewer; submit. | Refused: Reviewer lacks 'submit'. |  |
| PLM-0077 | Reviewer tries 'approve' on a In Work item | Functional | P2 | Log in as Reviewer; approve. | Allowed and audited. |  |
| PLM-0078 | Reviewer tries 'approve' on a In Review item | Functional | P2 | Log in as Reviewer; approve. | Allowed and audited. |  |
| PLM-0079 | Reviewer tries 'approve' on a Released item | Functional | P2 | Log in as Reviewer; approve. | Allowed and audited. |  |
| PLM-0080 | Reviewer tries 'approve' on a Obsolete item | Functional | P2 | Log in as Reviewer; approve. | Allowed and audited. |  |
| PLM-0081 | Reviewer tries 'reject' on a In Work item | Functional | P2 | Log in as Reviewer; reject. | Allowed and audited. |  |
| PLM-0082 | Reviewer tries 'reject' on a In Review item | Functional | P2 | Log in as Reviewer; reject. | Allowed and audited. |  |
| PLM-0083 | Reviewer tries 'reject' on a Released item | Functional | P2 | Log in as Reviewer; reject. | Allowed and audited. |  |
| PLM-0084 | Reviewer tries 'reject' on a Obsolete item | Functional | P2 | Log in as Reviewer; reject. | Allowed and audited. |  |
| PLM-0085 | Reviewer tries 'revise' on a In Work item | Negative | P2 | Log in as Reviewer; revise. | Refused: Reviewer lacks 'revise'. |  |
| PLM-0086 | Reviewer tries 'revise' on a In Review item | Negative | P2 | Log in as Reviewer; revise. | Refused: Reviewer lacks 'revise'. |  |
| PLM-0087 | Reviewer tries 'revise' on a Released item | Negative | P2 | Log in as Reviewer; revise. | Refused: Reviewer lacks 'revise'. |  |
| PLM-0088 | Reviewer tries 'revise' on a Obsolete item | Negative | P2 | Log in as Reviewer; revise. | Refused: Reviewer lacks 'revise'. |  |
| PLM-0089 | Reviewer tries 'obsolete' on a In Work item | Negative | P2 | Log in as Reviewer; obsolete. | Refused: Reviewer lacks 'obsolete'. |  |
| PLM-0090 | Reviewer tries 'obsolete' on a In Review item | Negative | P2 | Log in as Reviewer; obsolete. | Refused: Reviewer lacks 'obsolete'. |  |
| PLM-0091 | Reviewer tries 'obsolete' on a Released item | Negative | P2 | Log in as Reviewer; obsolete. | Refused: Reviewer lacks 'obsolete'. |  |
| PLM-0092 | Reviewer tries 'obsolete' on a Obsolete item | Negative | P2 | Log in as Reviewer; obsolete. | Refused: Reviewer lacks 'obsolete'. |  |
| PLM-0093 | Reviewer tries 'delete' on a In Work item | Negative | P2 | Log in as Reviewer; delete. | Refused: Reviewer lacks 'delete'. |  |
| PLM-0094 | Reviewer tries 'delete' on a In Review item | Negative | P2 | Log in as Reviewer; delete. | Refused: Reviewer lacks 'delete'. |  |
| PLM-0095 | Reviewer tries 'delete' on a Released item | Negative | P2 | Log in as Reviewer; delete. | Refused: Reviewer lacks 'delete'. |  |
| PLM-0096 | Reviewer tries 'delete' on a Obsolete item | Negative | P2 | Log in as Reviewer; delete. | Refused: Reviewer lacks 'delete'. |  |
| PLM-0097 | Admin tries 'edit' on a In Work item | Functional | P2 | Log in as Admin; edit. | Allowed and audited. |  |
| PLM-0098 | Admin tries 'edit' on a In Review item | Functional | P2 | Log in as Admin; edit. | Allowed and audited. |  |
| PLM-0099 | Admin tries 'edit' on a Released item | Negative | P2 | Log in as Admin; edit. | Refused: released data is frozen (revise instead). |  |
| PLM-0100 | Admin tries 'edit' on a Obsolete item | Negative | P2 | Log in as Admin; edit. | Refused: released data is frozen (revise instead). |  |
| PLM-0101 | Admin tries 'submit' on a In Work item | Functional | P2 | Log in as Admin; submit. | Allowed and audited. |  |
| PLM-0102 | Admin tries 'submit' on a In Review item | Functional | P2 | Log in as Admin; submit. | Allowed and audited. |  |
| PLM-0103 | Admin tries 'submit' on a Released item | Functional | P2 | Log in as Admin; submit. | Allowed and audited. |  |
| PLM-0104 | Admin tries 'submit' on a Obsolete item | Functional | P2 | Log in as Admin; submit. | Allowed and audited. |  |
| PLM-0105 | Admin tries 'approve' on a In Work item | Functional | P2 | Log in as Admin; approve. | Allowed and audited. |  |
| PLM-0106 | Admin tries 'approve' on a In Review item | Functional | P2 | Log in as Admin; approve. | Allowed and audited. |  |
| PLM-0107 | Admin tries 'approve' on a Released item | Functional | P2 | Log in as Admin; approve. | Allowed and audited. |  |
| PLM-0108 | Admin tries 'approve' on a Obsolete item | Functional | P2 | Log in as Admin; approve. | Allowed and audited. |  |
| PLM-0109 | Admin tries 'reject' on a In Work item | Functional | P2 | Log in as Admin; reject. | Allowed and audited. |  |
| PLM-0110 | Admin tries 'reject' on a In Review item | Functional | P2 | Log in as Admin; reject. | Allowed and audited. |  |
| PLM-0111 | Admin tries 'reject' on a Released item | Functional | P2 | Log in as Admin; reject. | Allowed and audited. |  |
| PLM-0112 | Admin tries 'reject' on a Obsolete item | Functional | P2 | Log in as Admin; reject. | Allowed and audited. |  |
| PLM-0113 | Admin tries 'revise' on a In Work item | Functional | P2 | Log in as Admin; revise. | Allowed and audited. |  |
| PLM-0114 | Admin tries 'revise' on a In Review item | Functional | P2 | Log in as Admin; revise. | Allowed and audited. |  |
| PLM-0115 | Admin tries 'revise' on a Released item | Functional | P2 | Log in as Admin; revise. | Allowed and audited. |  |
| PLM-0116 | Admin tries 'revise' on a Obsolete item | Functional | P2 | Log in as Admin; revise. | Allowed and audited. |  |
| PLM-0117 | Admin tries 'obsolete' on a In Work item | Functional | P2 | Log in as Admin; obsolete. | Allowed and audited. |  |
| PLM-0118 | Admin tries 'obsolete' on a In Review item | Functional | P2 | Log in as Admin; obsolete. | Allowed and audited. |  |
| PLM-0119 | Admin tries 'obsolete' on a Released item | Functional | P2 | Log in as Admin; obsolete. | Allowed and audited. |  |
| PLM-0120 | Admin tries 'obsolete' on a Obsolete item | Functional | P2 | Log in as Admin; obsolete. | Allowed and audited. |  |
| PLM-0121 | Admin tries 'delete' on a In Work item | Functional | P2 | Log in as Admin; delete. | Allowed and audited. |  |
| PLM-0122 | Admin tries 'delete' on a In Review item | Functional | P2 | Log in as Admin; delete. | Allowed and audited. |  |
| PLM-0123 | Admin tries 'delete' on a Released item | Functional | P2 | Log in as Admin; delete. | Allowed and audited. |  |
| PLM-0124 | Admin tries 'delete' on a Obsolete item | Functional | P2 | Log in as Admin; delete. | Allowed and audited. |  |

## Revisions and baselines

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLM-0125 | create baseline on part | Functional | P2 | Create baseline for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0126 | create baseline on assembly | Functional | P2 | Create baseline for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0127 | create baseline on requirement | Functional | P2 | Create baseline for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0128 | create baseline on test run | Functional | P2 | Create baseline for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0129 | compare two baselines on part | Functional | P2 | Compare two baselines for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0130 | compare two baselines on assembly | Functional | P2 | Compare two baselines for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0131 | compare two baselines on requirement | Functional | P2 | Compare two baselines for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0132 | compare two baselines on test run | Functional | P2 | Compare two baselines for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0133 | revise A→B on part | Functional | P2 | Revise a→b for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0134 | revise A→B on assembly | Functional | P2 | Revise a→b for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0135 | revise A→B on requirement | Functional | P2 | Revise a→b for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0136 | revise A→B on test run | Functional | P2 | Revise a→b for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0137 | where-used on part | Functional | P2 | Where-used for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0138 | where-used on assembly | Functional | P2 | Where-used for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0139 | where-used on requirement | Functional | P2 | Where-used for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0140 | where-used on test run | Functional | P2 | Where-used for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0141 | rollback to baseline on part | Functional | P2 | Rollback to baseline for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0142 | rollback to baseline on assembly | Functional | P2 | Rollback to baseline for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0143 | rollback to baseline on requirement | Functional | P2 | Rollback to baseline for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0144 | rollback to baseline on test run | Functional | P2 | Rollback to baseline for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0145 | branch a design on part | Functional | P2 | Branch a design for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0146 | branch a design on assembly | Functional | P2 | Branch a design for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0147 | branch a design on requirement | Functional | P2 | Branch a design for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0148 | branch a design on test run | Functional | P2 | Branch a design for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0149 | merge branch on part | Functional | P2 | Merge branch for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0150 | merge branch on assembly | Functional | P2 | Merge branch for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0151 | merge branch on requirement | Functional | P2 | Merge branch for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0152 | merge branch on test run | Functional | P2 | Merge branch for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0153 | signed result (hash) on part | Functional | P2 | Signed result (hash) for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0154 | signed result (hash) on assembly | Functional | P2 | Signed result (hash) for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0155 | signed result (hash) on requirement | Functional | P2 | Signed result (hash) for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0156 | signed result (hash) on test run | Functional | P2 | Signed result (hash) for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0157 | stale evidence after change on part | Functional | P2 | Stale evidence after change for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0158 | stale evidence after change on assembly | Functional | P2 | Stale evidence after change for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0159 | stale evidence after change on requirement | Functional | P2 | Stale evidence after change for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0160 | stale evidence after change on test run | Functional | P2 | Stale evidence after change for a test run. | Correct, reproducible, and visible in the history. |  |
| PLM-0161 | audit trail export on part | Functional | P2 | Audit trail export for a part. | Correct, reproducible, and visible in the history. |  |
| PLM-0162 | audit trail export on assembly | Functional | P2 | Audit trail export for a assembly. | Correct, reproducible, and visible in the history. |  |
| PLM-0163 | audit trail export on requirement | Functional | P2 | Audit trail export for a requirement. | Correct, reproducible, and visible in the history. |  |
| PLM-0164 | audit trail export on test run | Functional | P2 | Audit trail export for a test run. | Correct, reproducible, and visible in the history. |  |

## Engineering change

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLM-0165 | raise ECR from a parameter edit | Functional | P2 | Raise ecr. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0166 | raise ECR from a part replacement | Functional | P2 | Raise ecr. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0167 | raise ECR from a requirement change | Functional | P2 | Raise ecr. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0168 | impact analysis before approval from a parameter edit | Functional | P2 | Impact analysis before approval. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0169 | impact analysis before approval from a part replacement | Functional | P2 | Impact analysis before approval. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0170 | impact analysis before approval from a requirement change | Functional | P2 | Impact analysis before approval. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0171 | approve from a parameter edit | Functional | P2 | Approve. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0172 | approve from a part replacement | Functional | P2 | Approve. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0173 | approve from a requirement change | Functional | P2 | Approve. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0174 | reject from a parameter edit | Functional | P2 | Reject. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0175 | reject from a part replacement | Functional | P2 | Reject. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0176 | reject from a requirement change | Functional | P2 | Reject. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0177 | implement (ECO) from a parameter edit | Functional | P2 | Implement (eco). | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0178 | implement (ECO) from a part replacement | Functional | P2 | Implement (eco). | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0179 | implement (ECO) from a requirement change | Functional | P2 | Implement (eco). | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0180 | notify affected owners from a parameter edit | Functional | P2 | Notify affected owners. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0181 | notify affected owners from a part replacement | Functional | P2 | Notify affected owners. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0182 | notify affected owners from a requirement change | Functional | P2 | Notify affected owners. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0183 | change with no impact from a parameter edit | Functional | P2 | Change with no impact. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0184 | change with no impact from a part replacement | Functional | P2 | Change with no impact. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0185 | change with no impact from a requirement change | Functional | P2 | Change with no impact. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0186 | change touching 50 parts from a parameter edit | Functional | P2 | Change touching 50 parts. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0187 | change touching 50 parts from a part replacement | Functional | P2 | Change touching 50 parts. | Impact lists parts, requirements and tests; decision recorded. |  |
| PLM-0188 | change touching 50 parts from a requirement change | Functional | P2 | Change touching 50 parts. | Impact lists parts, requirements and tests; decision recorded. |  |

## Collaboration

Status in Autevra: **Gap**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| PLM-0189 | two users edit different parts (2 users) | Functional | P2 | Simulate 2 users: two users edit different parts. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0190 | two users edit different parts (10 users) | Functional | P2 | Simulate 10 users: two users edit different parts. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0191 | two users edit the same part (lock) (2 users) | Functional | P2 | Simulate 2 users: two users edit the same part (lock). | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0192 | two users edit the same part (lock) (10 users) | Functional | P2 | Simulate 10 users: two users edit the same part (lock). | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0193 | check-in/check-out (2 users) | Functional | P2 | Simulate 2 users: check-in/check-out. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0194 | check-in/check-out (10 users) | Functional | P2 | Simulate 10 users: check-in/check-out. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0195 | comment on a 3D view (2 users) | Functional | P2 | Simulate 2 users: comment on a 3D view. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0196 | comment on a 3D view (10 users) | Functional | P2 | Simulate 10 users: comment on a 3D view. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0197 | @mention notification (2 users) | Functional | P2 | Simulate 2 users: @mention notification. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0198 | @mention notification (10 users) | Functional | P2 | Simulate 10 users: @mention notification. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0199 | offline edit then sync (2 users) | Functional | P2 | Simulate 2 users: offline edit then sync. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0200 | offline edit then sync (10 users) | Functional | P2 | Simulate 10 users: offline edit then sync. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0201 | conflict resolution (2 users) | Functional | P2 | Simulate 2 users: conflict resolution. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0202 | conflict resolution (10 users) | Functional | P2 | Simulate 10 users: conflict resolution. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0203 | share read-only link (2 users) | Functional | P2 | Simulate 2 users: share read-only link. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0204 | share read-only link (10 users) | Functional | P2 | Simulate 10 users: share read-only link. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0205 | project permissions per user (2 users) | Functional | P2 | Simulate 2 users: project permissions per user. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0206 | project permissions per user (10 users) | Functional | P2 | Simulate 10 users: project permissions per user. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0207 | SSO login (2 users) | Functional | P2 | Simulate 2 users: SSO login. | No lost updates; conflicts surfaced; audit complete. |  |
| PLM-0208 | SSO login (10 users) | Functional | P2 | Simulate 10 users: SSO login. | No lost updates; conflicts surfaced; audit complete. |  |
