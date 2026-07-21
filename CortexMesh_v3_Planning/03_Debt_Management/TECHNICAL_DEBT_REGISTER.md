# CortexMesh Technical Debt Register

**Document role:** Authoritative consolidated governance register

**Version:** 1.0

**Status:** ACTIVE

**Established:** 2026-07-19

**Last reviewed:** 2026-07-19

**Repository baseline:** `main` at `d78516b`

**Supersedes:** No historical debt record

**Relationship to prior register:** Consolidates acknowledged liabilities while
preserving the identifiers, evidence, status, and priority of
`DEBT_REGISTER_v1.3.md`

## Executive Summary

This register is the permanent, consolidated governance record for acknowledged
CortexMesh technical debt. It brings the active Architecture Debt Register,
Foundation 1.1 deferred liabilities, research-integrity obligations, legal
completion work, and identified future-engineering questions into one review
surface.

The register does not authorize implementation, change an existing priority, or
close any item. Where a source does not assign a priority, authority, phase, or
date, the field is recorded as `NOT ASSIGNED` or `NOT DETERMINED`; no value is
inferred merely to complete the table.

The repository does not preserve `COMM-S13-DEEPSEEK-005` or the Independent
Enhancement Recommendations as standalone tracked artefacts at this baseline.
Their findings are therefore included only where corroborated by Session 13,
the War Room briefing, an existing debt record, or other repository evidence.
This limitation must be resolved by preserving those source communications or
recording an authoritative evidence disposition; it must not be concealed by
invented quotations or metadata.

All TD items remain open, monitored, investigated, deferred, paused, or
unassigned as stated below. No item is closed by publication of this register.

## Governance Purpose

The register exists to:

- prevent acknowledged liabilities from disappearing between phases;
- provide one discoverable record of ownership, authority, evidence, review,
  dependencies, compounding risk, and closure criteria;
- separate recognition of debt from authority to remediate it;
- preserve historical debt identifiers and source decisions;
- ensure deferral remains visible and reviewable; and
- provide the Board and Product Owner with evidence suitable for prioritisation
  without creating a compensating score or automatic rank.

This document is a governance record, not an implementation plan. Status and
priority changes require evidence and the approval applicable to the underlying
decision. GG-02 remains the governing authority for Board decisions,
architectural decisions, implementation authorization, roadmap authorization,
and ratification.

## Governance Rules

1. No TD item may be closed without evidence satisfying its verification
   criteria.
2. No TD item may be closed without the required approval or closure authority.
3. **Deferred does not mean ignored.**
4. Verification precedes closure.
5. Recording debt does not authorize investigation, design, implementation,
   runtime change, provider change, research execution, or modification of a
   LOCKED component.
6. Priorities may not be changed without evidence and an attributable decision.
7. Historical identifiers and source records remain valid. The `TD-###`
   identifier is the consolidated-register identity; aliases such as
   `DEBT-001` remain permanent traceability references.
8. A partial mitigation does not close an item unless the recorded verification
   criteria and closure approval are fully satisfied.
9. When evidence is missing, the register records the gap rather than presuming
   resolution.
10. Review may change metadata only through a traceable decision-log entry.

## Lifecycle

```text
IDENTIFIED
    -> TRIAGED
        -> MONITOR / INVESTIGATE / DEFER / PAUSE
            -> AUTHORISED REMEDIATION
                -> IMPLEMENTED
                    -> VERIFIED
                        -> APPROVED FOR CLOSURE
                            -> CLOSED
```

An item may return to investigation when new evidence invalidates an assumption
or satisfies a recorded escalation trigger. `MONITOR`, `DEFERRED`, and `PAUSED`
are active lifecycle states, not closure states. Implementation and verification
must remain distinct from approval.

## Decision Log

| Date | Decision | Authority | Effect |
| --- | --- | --- | --- |
| 2026-06-20 | Current architecture debt states and severities recorded for DEBT-001, DEBT-007, DEBT-008, DEBT-010, and DEBT-011. | Existing Board records | Preserved in TD-001 through TD-005; no reclassification made here. |
| 2026-07-14 | Session 13 accepted Foundation 1.0 and RP-001 as baselines and deferred RP-002 pending evidence. | Session 13 non-decision review | Research liabilities remain bounded future work; no implementation authority created. |
| 2026-07-17 | Foundation 1.1-C disposition review retained explicit deferred repository questions. | Product Owner-accepted workstream record | Consolidated as TD-007 without executing deferred actions. |
| 2026-07-18 | Foundation 1.1-E closed; Foundation 1.1 remained open solely because F1.1-B was paused. | Product Owner acceptance | Legal completion remains visible as TD-006. |
| 2026-07-19 | War Room briefing identified incomplete consolidated debt coverage and summarized deferred liabilities. | Draft for Board review | Used as a corroborating source; draft status creates no priority, closure, or implementation decision. |
| 2026-07-19 | Consolidated Technical Debt Register v1.0 established. | Product Owner assignment; publication pending | TD-001 through TD-015 recorded; no item closed or reprioritized. |

## Register Table

`NOT ASSIGNED` means the evidence source did not assign a priority. It is not a
low priority.

| ID | Title | Status | Priority | Compounding Risk | Planned Phase | Next Review | Verification Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TD-001 | Orchestrator Randomness | MONITOR | Medium | Non-reproducible selection could obscure cause and effect if runtime use expands before benefit or harm is measured. | Evidence-led reassessment; phase not assigned | Next major programme milestone or monitoring trigger | Approved corpus demonstrates whether randomness causes material harm or benefit; deterministic controls and regression evidence are reviewed. |
| TD-002 | Memory Integrity Startup Resilience | INVESTIGATE | High | Corrupt or invalid memory state can prevent startup and make later recovery more costly as state formats evolve. | Model E planning; implementation not authorized | Next major programme milestone or implementation-authorization review | Corrupt JSON and invalid schema types are handled under an approved design, recovery is logged, tests pass, and protected identities remain intact. |
| TD-003 | Merkle Anchoring and External Integrity | INVESTIGATE / DEFERRED | Medium | Ledger growth without an anchoring strategy may increase later migration cost and weaken external tamper-evidence claims. | Design study deferred | Next major programme milestone | Approved design defines threat model, anchoring boundary, verification, failure handling, migration, and measurable benefit; implementation evidence passes required checks. |
| TD-004 | Docker Daemon and Capability Isolation Risk | MONITOR | High | Increased capability use could amplify daemon-compromise impact and normalize an unreviewed production isolation policy. | Path F selected; implementation not authorized | Reopening trigger or next major programme milestone | Approved isolation design is implemented and adversarially verified; daemon, capability-gateway, audit, rollback, and LOCKED boundaries pass review. |
| TD-005 | Timeout and Zombie Process Risk | INVESTIGATE | Medium | More external workloads can multiply leaked processes, resource exhaustion, and ambiguous termination outcomes. | Implementation plan drafted; implementation not authorized | Board implementation-plan review | Termination is bounded and verified; container state and audit trail are checked; kill failure, daemon hang, and zombie cases pass tests; required approval is recorded. |
| TD-006 | Final Proprietary Licence | PAUSED | NOT ASSIGNED | Commercial use, broader access, or distribution before reviewed terms could create legal ambiguity and inconsistent obligations. | Foundation 1.1-B | Every major programme milestone and before external access, commercial use, distribution, or contracting | Qualified legal review covers authorized access, evaluation, confidentiality, commercial licensing, warranties, liability, termination, and governing law; required acceptance is recorded. |
| TD-007 | Deferred Repository Hygiene Dispositions | DEFERRED | NOT ASSIGNED | Duplicate or ambiguous surfaces can increase navigation error, tooling ambiguity, repository growth, and provenance risk. | Future scoped hygiene assessment | Every major programme milestone or a recorded breakage trigger | Each D001-D012 item receives its own evidence-backed disposition and authorized manifest; P0 assets and hashes are preserved; structural and regression verification pass. |
| TD-008 | Communication Protocol Status Reconciliation | IDENTIFIED | NOT ASSIGNED | Conflicting document and decision-register statuses can cause contributors to rely on the wrong communication authority. | Governance reconciliation; phase not assigned | Next Board governance review | The operative version, ratification evidence, effective date, supersession, and document status agree across authoritative records without rewriting history. |
| TD-009 | Research Replication Terminology Consistency | MONITOR | NOT ASSIGNED | Inconsistent historical use of “independent reproduction” can compound into overstated research or publication claims. | Prospective research-maintenance review | Before the next research publication or programme | Current and future summaries consistently distinguish internal replication, repository-portable reproduction, and external reproduction; preserved history remains intact; claims trace to evidence. |
| TD-010 | Independently Administered Reproduction | DEFERRED | NOT ASSIGNED | Without genuinely independent administration, portability and internal replication evidence may be generalized beyond their demonstrated scope. | Future research programme | Before any claim of independent or external reproduction | A preregistered reproduction is administered independently, preserves immutable inputs and outputs, records environment and deviations, and is reviewed under the permanent validation methodology. |
| TD-011 | Comparative Evaluation of RP-001 H1 | DEFERRED | NOT ASSIGNED | Baseline findings may be mistaken for evidence of superiority if the comparative hypothesis remains untested. | RP-002 or later qualifying research | When a qualifying comparative hypothesis is proposed | Preregistered control and experimental conditions test H1 with independent metrics, declared inclusion rules, immutable evidence, and proportional conclusions. |
| TD-012 | Adversarial Replay Corpus Expansion | DEFERRED | NOT ASSIGNED | A stable benign corpus may conceal failure modes and encourage unsupported generality claims as orchestration evolves. | Future replay-corpus version / research authorization | Before broader robustness or generality claims | A new immutable, certified corpus version contains reviewed adversarial and malformed cases; comparator coverage, hashes, replay evidence, and non-regression gates pass. |
| TD-013 | Provider-Neutral Response Envelope Evolution | DEFERRED / NOT AUTHORIZED | NOT ASSIGNED | Provider-specific response handling could leak into coordination layers as optional integrations expand. | Future architecture assessment | Before adding a provider whose response cannot satisfy the current contract | Evidence demonstrates a contract gap; a provider-neutral design preserves provenance and capability semantics; adapter conformance and regression tests pass without provider authority leakage. |
| TD-014 | Capability-Aware Routing and Coverage Observability | DEFERRED / NOT AUTHORIZED | NOT ASSIGNED | Capability growth without explicit routing evidence and coverage visibility may create hidden provider coupling or untested execution paths. | Future engineering assessment | Before enabling adaptive or production capability routing | Separate approved designs define routing inputs and observational coverage; provider identity confers no authority; deterministic, protected-surface, regression, and coverage evidence pass. |
| TD-015 | Technical Debt Register Maintenance | DEFERRED | Low | Without periodic review, metadata and priorities may become stale and deferred liabilities may disappear from active planning. | Every major programme milestone | Every major programme milestone | Board review confirms each item’s evidence, status, priority, owner/authority, next review, and closure criteria; decision-log changes are traceable. |

## Detailed Records

### TD-001 — Orchestrator Randomness

| Field | Value |
| --- | --- |
| Date Identified | Before or on 2026-06-20 |
| Source | `DEBT_REGISTER_v1.3.md`; `BOARD_CURRENT_STATE.md`; DEBT-001 evidence records |
| Status | MONITOR |
| Priority | Medium |
| Deferral Authority | Board reclassification after pilot evidence review |
| Planned Phase | Evidence-led reassessment; no phase assigned |
| Dependencies | Approved task corpus; monitoring trigger; deterministic comparator |
| Evidence Location | `03_Debt_Management/DEBT001/`; `00_Governance/BOARD_CURRENT_STATE.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Next major programme milestone or recorded monitoring trigger |
| Closure Authority | Board under GG-02 |
| Compounding Risk | Runtime expansion may make causal attribution and later determinisation more costly. |
| Verification Criteria | Approved evidence establishes material benefit or harm, compares deterministic controls, and passes regression and required governance review. |

Current evidence records randomness but establishes neither harm nor benefit.
This register preserves the Board’s Medium/MONITOR disposition.

### TD-002 — Memory Integrity Startup Resilience

| Field | Value |
| --- | --- |
| Date Identified | Before or on 2026-06-20 |
| Source | `DEBT_REGISTER_v1.3.md`; `DEBT007_DESIGN_STUDY_v2.0.md` |
| Status | INVESTIGATE |
| Priority | High |
| Deferral Authority | Board; Model E adopted as planning only |
| Planned Phase | Model E implementation assessment; not authorized |
| Dependencies | Memory schema, recovery behavior, audit logging, LOCKED review |
| Evidence Location | `03_Debt_Management/DEBT007/`; `00_Governance/BOARD_CURRENT_STATE.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Next major programme milestone or authorization request |
| Closure Authority | Board under GG-02 and Product Owner acceptance where applicable |
| Compounding Risk | State evolution can increase recovery complexity and blast radius. |
| Verification Criteria | Approved recovery design handles corrupt JSON and invalid types, logs recovery, preserves identity, and passes focused and regression tests. |

The historical register reports load failure, no fallback, and no recovery
logging. Model E remains a design artefact only.

### TD-003 — Merkle Anchoring and External Integrity

| Field | Value |
| --- | --- |
| Date Identified | Before or on 2026-06-20 |
| Source | `DEBT_REGISTER_v1.3.md`; `PROGRAM_ROADMAP.md` |
| Status | INVESTIGATE / DEFERRED |
| Priority | Medium |
| Deferral Authority | Board roadmap record |
| Planned Phase | Design study deferred |
| Dependencies | Ledger threat model, hash-chain migration, external trust boundary |
| Evidence Location | `03_Debt_Management/DEBT_REGISTER_v1.3.md`; `05_Program_Management/PROGRAM_ROADMAP.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Next major programme milestone |
| Closure Authority | Board under GG-02 |
| Compounding Risk | Larger ledgers increase migration and external-verification cost. |
| Verification Criteria | Approved threat model and architecture precede implementation; anchoring, failure, migration, and audit tests pass. |

No implementation authority is recorded.

### TD-004 — Docker Daemon and Capability Isolation Risk

| Field | Value |
| --- | --- |
| Date Identified | Before or on 2026-06-20 |
| Source | `DEBT_REGISTER_v1.3.md`; Board history; DEBT-010 studies |
| Status | MONITOR |
| Priority | High |
| Deferral Authority | Board selected Path F; implementation not authorized |
| Planned Phase | Future authorized isolation hardening |
| Dependencies | Docker daemon, capability gateway policy, external runner, threat model |
| Evidence Location | `03_Debt_Management/DEBT010/`; `00_Governance/BOARD_HISTORY_SUMMARY.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Reopening trigger or next major programme milestone |
| Closure Authority | Board under GG-02; explicit LOCKED approval if affected |
| Compounding Risk | Capability expansion can magnify daemon and isolation exposure. |
| Verification Criteria | Approved defense-in-depth controls pass adversarial isolation, audit, rollback, and protected-boundary checks. |

Path F is a selected direction, not completed remediation.

### TD-005 — Timeout and Zombie Process Risk

| Field | Value |
| --- | --- |
| Date Identified | Before or on 2026-06-20 |
| Source | `DEBT_REGISTER_v1.3.md`; DEBT-011 design and implementation plan |
| Status | INVESTIGATE |
| Priority | Medium |
| Deferral Authority | Board authorized planning only |
| Planned Phase | Board review of implementation plan |
| Dependencies | External runner, Docker state, termination audit trail |
| Evidence Location | `03_Debt_Management/DEBT011/`; `99_Archive/DEBT011/` |
| Last Reviewed | 2026-07-19 |
| Next Review | Implementation-plan review |
| Closure Authority | Board under GG-02; explicit LOCKED approval if affected |
| Compounding Risk | Workload volume can multiply leaked processes and resource exhaustion. |
| Verification Criteria | Kill-failure, hang, timeout, zombie, and container-state tests pass under an approved termination and audit design. |

Implementation remains unauthorized.

### TD-006 — Final Proprietary Licence

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-17 |
| Source | F1.1-B licensing correction; Foundation 1.1 status; War Room briefing |
| Status | PAUSED |
| Priority | NOT ASSIGNED |
| Deferral Authority | Product Owner; formal legal review required |
| Planned Phase | Foundation 1.1-B |
| Dependencies | Qualified legal counsel; commercial and access requirements |
| Evidence Location | `06_Implementation_Execution/Foundation_1_1/F1.1-B_LICENSING_CORRECTION.md`; `LICENSE` |
| Last Reviewed | 2026-07-19 |
| Next Review | Every major programme milestone and before distribution or commercial use |
| Closure Authority | Product Owner plus qualified legal acceptance; Board if governance authority changes |
| Compounding Risk | Unreviewed terms may create ambiguity as access or commercial activity grows. |
| Verification Criteria | Reviewed proprietary terms cover the required legal subjects and are accepted and published through an authorized process. |

The interim proprietary correction is effective. It is containment, not final
legal completion.

### TD-007 — Deferred Repository Hygiene Dispositions

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-17 |
| Source | F1.1-C inventory, disposition, and cleanup manifest |
| Status | DEFERRED |
| Priority | NOT ASSIGNED |
| Deferral Authority | Product Owner-accepted F1.1-C disposition |
| Planned Phase | Separate evidence-preserving workstreams |
| Dependencies | D001-D012 evidence, lineage, hashes, P0 protection |
| Evidence Location | `06_Implementation_Execution/Foundation_1_1/F1.1-C_REPOSITORY_DISPOSITION.md`; `F1.1-C_CLEANUP_MANIFEST.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Every major programme milestone or breakage trigger |
| Closure Authority | Product Owner; Board where a P0, governance, architecture, research, validation, or LOCKED surface is involved |
| Compounding Risk | Duplication and ambiguity increase contributor error and tool friction over time. |
| Verification Criteria | All D001-D012 items have evidence-backed dispositions, authorized manifests, exact provenance checks, and successful structural and regression verification. |

Completed C001-C019 actions do not close D001-D012.

### TD-008 — Communication Protocol Status Reconciliation

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-19 |
| Source | War Room briefing evidence reconciliation |
| Status | IDENTIFIED |
| Priority | NOT ASSIGNED |
| Deferral Authority | NOT DETERMINED |
| Planned Phase | Governance record reconciliation |
| Dependencies | Board Decisions Register, Session 11 evidence, protocol v1.0/v1.1 |
| Evidence Location | `00_Governance/Communications/WAR_ROOM_EXECUTIVE_BRIEFING_001.md`; protocol and decision records |
| Last Reviewed | 2026-07-19 |
| Next Review | Next Board governance review |
| Closure Authority | Board under GG-02 |
| Compounding Risk | Conflicting authority labels can propagate incorrect procedural assumptions. |
| Verification Criteria | Protocol status, ratification, effective date, supersession, and Board register are mutually consistent and historically accurate. |

The Board register and Session 11 narrative conflict with protocol documents
that remain marked `PROPOSED`.

### TD-009 — Research Replication Terminology Consistency

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-14 |
| Source | Session 13 summary; Research Logbook; War Room briefing |
| Status | MONITOR |
| Priority | NOT ASSIGNED |
| Deferral Authority | Session 13 prospective recommendation |
| Planned Phase | Research publication and record maintenance |
| Dependencies | Research glossary, publication review, preserved historical records |
| Evidence Location | `00_Governance/Board_Sessions/Session_13/SESSION_13_SUMMARY.md`; `07_Research/RESEARCH_LOGBOOK.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Before next research publication or programme |
| Closure Authority | Research-methodology review and Product Owner acceptance; Board if certification authority changes |
| Compounding Risk | Repetition of ambiguous terms can become an overstated scientific claim. |
| Verification Criteria | Prospective records consistently use the defined replication categories, while historical records remain unchanged and claims remain evidence-bounded. |

Current summary records identify R1 as Internal Replication. Preserved historical
wording remains part of the audit trail.

### TD-010 — Independently Administered Reproduction

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-14 |
| Source | Session 13 recommendations; War Room briefing |
| Status | DEFERRED |
| Priority | NOT ASSIGNED |
| Deferral Authority | Session 13; RP-002 deferred pending evidence |
| Planned Phase | Future qualifying research |
| Dependencies | Independent administrator, preregistration, immutable baseline and corpus |
| Evidence Location | `00_Governance/Board_Sessions/Session_13/SESSION_13_SUMMARY.md`; `07_Research/REPRODUCIBILITY_STATUS.md` |
| Last Reviewed | 2026-07-19 |
| Next Review | Before independent/external reproduction claims |
| Closure Authority | Research certification process and required Product Owner/Board acceptance |
| Compounding Risk | Internal evidence may be generalized as independent confirmation. |
| Verification Criteria | Independent administration, environment capture, immutable evidence, protocol adherence, deviations, and review are all recorded. |

EXP-001-R2 establishes repository-portable Ubuntu reproduction, not universal
or independently administered reproduction.

### TD-011 — Comparative Evaluation of RP-001 H1

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-14 |
| Source | Session 13 findings; RP-001 preregistration history; War Room briefing |
| Status | DEFERRED |
| Priority | NOT ASSIGNED |
| Deferral Authority | Session 13; RP-002 deferred |
| Planned Phase | RP-002 or later qualifying research |
| Dependencies | Qualifying hypothesis, comparator, preregistration, certified corpus |
| Evidence Location | `07_Research/RP-001/RP-001_PREREGISTRATION.md`; Session 13 summary |
| Last Reviewed | 2026-07-19 |
| Next Review | When a comparative research question qualifies |
| Closure Authority | Research certification process and required Product Owner/Board acceptance |
| Compounding Risk | Baseline characterization can be misrepresented as comparative superiority. |
| Verification Criteria | A preregistered comparative study tests H1 with independent metrics, controls, immutable evidence, and proportional findings. |

EXP-001 was deliberately reduced to baseline characterization before data
collection. It did not test comparative superiority.

### TD-012 — Adversarial Replay Corpus Expansion

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-14 |
| Source | Session 13 near-term recommendations; War Room briefing |
| Status | DEFERRED |
| Priority | NOT ASSIGNED |
| Deferral Authority | Session 13; future research authorization required |
| Planned Phase | Future certified replay-corpus version |
| Dependencies | Corpus architecture, authoring kit, certification, threat scenarios |
| Evidence Location | `06_Implementation_Execution/Phase3A/`; Session 13 summary |
| Last Reviewed | 2026-07-19 |
| Next Review | Before broader robustness claims |
| Closure Authority | Permanent validation certification process and applicable Product Owner/Board approval |
| Compounding Risk | Validation confidence may outrun scenario diversity. |
| Verification Criteria | An immutable certified version adds reviewed adversarial and malformed cases and passes comparator, hash, replay, and non-regression gates. |

The current corpus remains the valid baseline within its certified scope.

### TD-013 — Provider-Neutral Response Envelope Evolution

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-19 |
| Source | War Room deferred future-engineering summary; Phase 1B provider-neutral architecture |
| Status | DEFERRED / NOT AUTHORIZED |
| Priority | NOT ASSIGNED |
| Deferral Authority | No implementation authorization; future design required |
| Planned Phase | Future evidence-led architecture assessment |
| Dependencies | LocalAI contracts, provider adapters, provenance, capability semantics |
| Evidence Location | `06_Implementation_Execution/Phase1B/LOCAL_AI_MANAGER_ARCHITECTURE.md`; War Room briefing |
| Last Reviewed | 2026-07-19 |
| Next Review | Before an incompatible provider response is introduced |
| Closure Authority | Board under GG-02 and Product Owner acceptance; LOCKED approval if applicable |
| Compounding Risk | Provider-specific parsing can leak into neutral coordination layers. |
| Verification Criteria | A demonstrated contract gap and approved neutral envelope precede adapter conformance, provenance, compatibility, and regression verification. |

This is a future design question, not evidence that the current provider
contract is defective.

### TD-014 — Capability-Aware Routing and Coverage Observability

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-19 |
| Source | War Room deferred future-engineering summary; architecture audit and CI evidence |
| Status | DEFERRED / NOT AUTHORIZED |
| Priority | NOT ASSIGNED |
| Deferral Authority | No implementation authorization; separate architecture review required |
| Planned Phase | Future engineering assessment |
| Dependencies | Capability registry, provider neutrality, routing policy, coverage evidence |
| Evidence Location | `05_Program_Management/AUDIT_REPORT_2026-06-28.md`; War Room briefing; CI records |
| Last Reviewed | 2026-07-19 |
| Next Review | Before adaptive or production capability routing |
| Closure Authority | Board under GG-02 and Product Owner acceptance |
| Compounding Risk | Hidden coupling and untested paths may grow with capabilities. |
| Verification Criteria | Approved independent designs preserve determinism and neutrality; routing and coverage evidence pass required regression and protected-surface gates. |

Coverage is observational unless a separately approved release gate says
otherwise. Provider identity must not become routing authority.

### TD-015 — Technical Debt Register Maintenance

| Field | Value |
| --- | --- |
| Date Identified | 2026-07-19 |
| Source | Product Owner assignment for consolidated register |
| Purpose | Establish periodic Board review so priorities remain current |
| Status | DEFERRED |
| Priority | Low |
| Review Cadence | Every major programme milestone |
| Deferral Authority | Product Owner assignment; Board review not yet scheduled |
| Planned Phase | Every major programme milestone |
| Dependencies | Current programme roadmap, evidence locations, decision records |
| Evidence Location | This register and its decision log |
| Last Reviewed | 2026-07-19 |
| Next Review | Every major programme milestone |
| Closure Authority | Board under GG-02 |
| Compounding Risk | Stale priorities, lost deferrals, and obsolete verification criteria can undermine lifecycle traceability. |
| Verification Criteria | A Board review records evidence, status, priority, review dates, dependencies, closure criteria, and attributable decisions for every active item. |

TD-015 remains deferred. Its Low priority does not reduce the review obligation.

## Source and Evidence Reconciliation

The following repository evidence was inspected for this version:

- `CortexMesh_v3_Planning/03_Debt_Management/DEBT_REGISTER_v1.3.md`;
- `CortexMesh_v3_Planning/00_Governance/BOARD_CURRENT_STATE.md`;
- `CortexMesh_v3_Planning/00_Governance/BOARD_HISTORY_SUMMARY.md`;
- `CortexMesh_v3_Planning/00_Governance/GOVERNANCE_BASELINE_v1.0.md`;
- `CortexMesh_v3_Planning/00_Governance/GG-02_Board_Voting_and_Ratification_Rules_v1.0.md`;
- `CortexMesh_v3_Planning/00_Governance/Board_Sessions/Session_13/EVIDENCE_INDEX.md`;
- `CortexMesh_v3_Planning/00_Governance/Board_Sessions/Session_13/SESSION_13_SUMMARY.md`;
- `CortexMesh_v3_Planning/00_Governance/Communications/WAR_ROOM_EXECUTIVE_BRIEFING_001.md`;
- `CortexMesh_v3_Planning/05_Program_Management/PROGRAM_ROADMAP.md`;
- `CortexMesh_v3_Planning/05_Program_Management/AUDIT_REPORT_2026-06-28.md`;
- `CortexMesh_v3_Planning/06_Implementation_Execution/Foundation_1_1/F1.1-C_REPOSITORY_DISPOSITION.md`;
- `CortexMesh_v3_Planning/06_Implementation_Execution/Foundation_1_1/F1.1-C_CLEANUP_MANIFEST.md`;
- `CortexMesh_v3_Planning/06_Implementation_Execution/Foundation_1_1/FOUNDATION_1_1_STATUS.md`;
- `CortexMesh_v3_Planning/06_Implementation_Execution/Phase1B/LOCAL_AI_MANAGER_ARCHITECTURE.md`;
- `CortexMesh_v3_Planning/06_Implementation_Execution/Phase3A/`;
- `CortexMesh_v3_Planning/07_Research/RESEARCH_LOGBOOK.md`;
- `CortexMesh_v3_Planning/07_Research/RESEARCH_OBSERVATIONS.md`; and
- `CortexMesh_v3_Planning/07_Research/REPRODUCIBILITY_STATUS.md`.

Repository searches found no tracked standalone file matching
`COMM-S13-DEEPSEEK-005` and no tracked standalone file titled Independent
Enhancement Recommendations. This register therefore does not attribute any
uncorroborated wording, severity, priority, authority, or closure criterion to
those missing inputs. If they are later preserved, the next review must compare
them against TD-001 through TD-015 and record any evidence-backed correction in
the Decision Log.

## Review and Closure Control

At each major programme milestone, TD-015 requires the Board to review this
register. Review must identify:

1. new evidence since the prior review;
2. status or priority changes proposed, with authority;
3. dependencies added or removed;
4. items whose escalation triggers have fired;
5. verification completed but not yet approved;
6. missing, moved, or superseded evidence locations; and
7. the next review point for every item.

Silence, elapsed time, completed adjacent work, or a superseded roadmap does
not close debt. Closure requires evidence, verification, and the recorded
approval specified by each detailed record.

## Repository Housekeeping Register

| Field | Value |
| --- | --- |
| ID | RH-001 |
| Title | Governance Source Preservation |
| Priority | Low |
| Category | Repository Housekeeping |
| Status | OPEN |
| Blocking | No |
| Description | Verify that governance artefacts referenced by Board decisions exist as permanent tracked repository records or have authoritative archival references. |
| Created By | BD-12-002 |
| Review | Future repository maintenance |
