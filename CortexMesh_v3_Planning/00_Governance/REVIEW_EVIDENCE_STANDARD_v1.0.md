# REVIEW_EVIDENCE_STANDARD_v1.0

Status: PROPOSED

## Purpose

Define how CortexMesh governance reviews distinguish repository findings from evidence limitations.

This standard reduces the risk that absence of evidence in a reviewer packet is treated as evidence of repository absence.

## Core Principle

A reviewer packet may be incomplete even when the repository is consistent.

Governance findings must distinguish:

1. Defects observed in the repository.
2. Limits in the evidence supplied to reviewers.
3. Inferences requiring repository validation.

## Review Packet Completeness

Every reviewer packet should declare its repository snapshot classification.

Permitted classifications:

| Classification | Meaning |
|---|---|
| FULL | Packet contains a complete repository snapshot or complete path map sufficient for repository-level validation. |
| PARTIAL | Packet contains selected repository artifacts and may omit relevant supporting files. |
| TOPIC LIMITED | Packet is scoped to a specific decision, debt, policy, or workstream and is not suitable for broad repository-conformance conclusions. |

## Evidence Limitation Classification

Review outputs may record an Evidence Limitation when reviewers cannot verify a claim because the packet lacks needed artifacts.

Evidence Limitations are not repository findings.

Recommended format:

```text
Evidence Limitation ID:
Classification: EVIDENCE LIMITATION
Observed:
Impact:
Disposition:
Required Follow-up:
```

## Example Evidence Limitation

```text
Evidence Limitation ID: EL-001
Classification: EVIDENCE LIMITATION
Observed: Reviewer packet did not include all referenced governance documents.
Impact: Reviewer could not verify repository conformance from the supplied packet alone.
Disposition: No repository finding recorded.
Required Follow-up: Validate against directory map or repository snapshot.
```

## Repository Finding Requirement

A repository finding requires repository-level evidence.

Acceptable repository-level evidence includes:

- directory map
- direct repository inspection
- committed file paths
- scoped grep/search output
- git status or git tree output
- named artifact excerpts

## Classification Pattern

When packet evidence is incomplete, use this pattern:

```text
OBSERVED
The review packet did not contain sufficient evidence to verify repository structure.

INFERRED
Repository inconsistencies may exist.

VERIFICATION
Repository snapshot or directory map demonstrates whether referenced files exist.

CONCLUSION
If files exist, close as Evidence Packet Incomplete, not Repository Incorrect.
```

## Disposition Values

| Disposition | Meaning |
|---|---|
| OPEN | Evidence limitation remains unresolved. |
| VALIDATED | Repository evidence resolved the limitation. |
| SUPERSEDED | Later packet or artifact replaced the limitation. |
| CLOSED | No further action required. |

## Reviewer Instruction

Reviewers shall not convert packet omissions into repository findings without repository-level validation.

Packet omissions may justify requests for additional evidence, directory maps, or repository snapshots.

## Governance Status

This standard is proposed governance guidance.

It does not amend policy.

It does not authorize implementation.

It does not modify LOCKED components.
