# EXP-001 Execution Authorization

## Authorization Record

| Field | Value |
| --- | --- |
| Research program | RP-001 |
| Experiment | EXP-001 |
| Decision | AUTHORIZED FOR EXECUTION |
| Authorized by | Product Owner |
| Authorization date | 2026-07-13 |
| Data collected before authorization | None |
| Protocol source | Commit `e7ddcb1` |
| Protocol SHA-256 | `51d649de94b12eacb22c99b8efc343af42b6f250a5fe41b35337882a80194ff2` |

## Authorization Gates

| Gate | Verification | Result |
| --- | --- | --- |
| 1. Protocol hash recorded | SHA-256 calculated from `EXP-001_PROTOCOL.md` at review commit `e7ddcb1` | PASS |
| 2. Replay certification verified | Corpus v1.1.0 status `CERTIFIED`; schema 1.1; 24 cases; 12 scenarios; all manifest file hashes and derived content hash verified | PASS |
| 3. Reference engine verified | Annotated tag `phase2c-complete` dereferences to commit `a72d11fe57f9026ab307efeaf962b97095527039` | PASS |

Verified Replay Corpus v1.1 content hash:

```text
20e4b446097db5b3dcaa6fbf214218038c9c297d2e60bbbc57b9d24bc1e59788
```

## Authorization Statement

**EXP-001 AUTHORIZED FOR EXECUTION**

## State Transition

| Before | After |
| --- | --- |
| PROTOCOL APPROVED - EXECUTION NOT AUTHORIZED | AUTHORIZED FOR EXECUTION - DATA COLLECTION NOT STARTED |

This is an administrative research-methodology state transition. It records no data, observation, result, anomaly, or conclusion.

## Scientific Integrity Rule

Execution authorization is a governance event within the research methodology, not a data event. It changes experiment state but shall not alter the experiment design, hypotheses, metrics, comparators, or expected outcomes.

The authorized scientific design remains exactly the reviewed design identified by the protocol hash. Any material change requires a preserved deviation or a new preregistration/protocol and renewed authorization before affected collection.

## Scope of Authorization

Authorization permits only the isolated 24-case, ten-repetition characterization specified in EXP-001 Protocol v1.0.

It does not authorize:

- runtime integration;
- Local AI, provider, network, or live-agent invocation;
- adaptive orchestration or provider selection;
- engine, corpus, validation framework, governance, or LOCKED modification;
- authority, scoring, confidence, ranking, voting, or governance semantics;
- any experiment other than RP-001/EXP-001.
