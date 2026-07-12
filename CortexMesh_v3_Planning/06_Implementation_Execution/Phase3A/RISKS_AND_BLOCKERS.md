# Phase 3A Risks and Blockers

## Status

CLOSED - DEFERRED MAINTENANCE RISKS RETAINED

## Purpose

Track validation risks, blockers, constraints, and deferred decisions for Phase 3A.

## Active Risks

| ID | Risk | Impact | Mitigation | Status |
| --- | --- | --- | --- | --- |
| P3A-R001 | Replay cases may mirror implementation behavior instead of independent expectations. | Validation could confirm itself without testing correctness. | Review expected outcomes before execution and separate case authorship from expectation review where practical. | OPEN |
| P3A-R002 | A small or homogeneous corpus may overstate correctness and stability. | Important divergence, minority, failure, or domain cases may be absent. | Define a case taxonomy and coverage matrix before implementation. | OPEN |
| P3A-R003 | Aggregate metrics may hide failed minority cases. | Preservation regressions could pass an overall threshold. | Require case-level evidence and zero-tolerance preservation gates. | OPEN |
| P3A-R004 | Determinism may depend on an undocumented environment detail. | Replays may fail across clean environments. | Record interpreter, platform, policy, corpus, and component versions with artifact hashes. | OPEN |
| P3A-R005 | Consensus expectations may encode subjective semantics. | “Correctness” may be circular or domain-dependent. | Use explicit categorical policies, reviewed conflict pairs, rationales, and versioned expectations. | OPEN |
| P3A-R006 | Diagnostic quality may be reduced to a superficial presence check. | Diagnostics may be stable but unhelpful or unattributable. | Validate trigger, specificity, attribution, prohibited semantics, and actionability separately. | OPEN |
| P3A-R007 | Latency measurements may be noisy or optimized prematurely. | Effort may target measurement artifacts rather than real constraints. | Characterize variance and environment before setting a performance threshold. | OPEN |
| P3A-R008 | Validation success may be mistaken for runtime integration approval. | The isolated-path conclusion or governance boundary could be bypassed. | State that success permits only a new assessment; require separate authorization and Board review for LOCKED impact. | OPEN |
| P3A-R009 | Provider/model identity may leak into expectations or grouping. | Validation may introduce implicit provider ranking. | Prohibit identity-dependent cases, metrics, ordering, and conclusions; retain identity only as descriptive provenance where necessary. | OPEN |
| P3A-R010 | Validation tooling may import runtime or mutate persistent state. | Runtime behavior or accepted baselines could be altered. | Keep tooling isolated, read-only, no-network, and covered by changed-path and import checks. | OPEN |
| P3A-R011 | Published corpus content may be edited in place. | Historical replays would no longer be reproducible. | Use immutable version directories/manifests, content hashes, and new versions for all case changes. | OPEN |
| P3A-R012 | Compatibility exclusions may hide missing evidence or traceability. | A regression may be reported as compatible. | Require explicit field-level rules and prohibit exclusions for preservation, divergence, diagnostics, or trace links. | OPEN |
| P3A-R013 | Corpus versions may proliferate without a clear canonical release. | Validation may compare incompatible datasets. | Maintain explicit current-version metadata while retaining every historical manifest. | OPEN |
| P3A-R014 | Sanitized source scenarios may retain sensitive or identity-bearing data. | Corpus publication could leak data or introduce provider bias. | Prefer synthetic cases; require sanitization and sensitivity review for derived cases. | OPEN |
| P3A-R015 | Future runtime replay may be treated as authorized by the schema. | Live artifacts could cross the isolated boundary prematurely. | Mark future runtime replay reserved and disabled pending a separate design and authorization. | OPEN |
| P3A-R016 | A certification may be copied to changed corpus content. | An unreviewed dataset could appear certified. | Bind certification to exact version, schema, manifest hash, counts, and comparator coverage; require a new certification per release. | MITIGATED IN REFERENCE IMPLEMENTATION |
| P3A-R017 | Frozen top-level models may contain semantically mutable nested payloads in a future storage adapter. | Published content could change without an attribute assignment. | Require canonical serialization, content-hash revalidation, and immutable storage during dataset creation. | OPEN |
| P3A-R018 | Compatibility rules may be configured from unreviewed input. | Comparator could accept a material regression. | Keep compatibility rules corpus-declared, versioned, reviewed, and prohibited from excluding preservation fields. | OPEN |
| P3A-R019 | One person may perform author, expectation, integrity, and certification roles. | Review independence may be weaker than the process implies. | Record each review function and disclose role overlap; require independent review where practical or risk-sensitive. | OPEN |
| P3A-R020 | Certification checklist completion may become a paper exercise. | A structurally invalid corpus could be published. | Bind checklist claims to executable mixin tests, manifest hashes, regression evidence, and named review records. | MITIGATED IN AUTHORING KIT |
| P3A-R021 | Case templates may encourage mechanically complete but low-value fixtures. | Metadata completeness could mask weak scenario coverage. | Require scenario rationale, metric coverage, taxonomy review, and explicit exclusions before certification. | OPEN |
| P3A-R022 | Corpus v1.0 is synthetic and compact. | It may not represent the breadth or messiness of future real artifacts. | Treat v1.0 as canonical structural baseline, report exclusions, and add cases only through new certified versions. | OPEN |
| P3A-R023 | Compact characteristic expectations may be too coarse for deep semantic validation. | Baseline may pass while statement-level behavior differs. | Use M6 baseline findings to identify where v1.1 needs richer expected artifacts without editing v1.0. | OPEN |
| P3A-R024 | v1.0 lacks executable case-specific simulated claims and failure inputs. | Consensus, minority, divergence, and diagnostic expectations cannot all be reproduced. | Preserve v1.0; publish v1.1 with step-keyed payload/adaptation contracts and executable negative cases. | CONFIRMED |
| P3A-R025 | Planning expectations drift from sealed resolver/planner contracts. | Accuracy metrics remain below validation gates. | Independently review and correct expected capabilities, roles, and steps in a new corpus version. | CONFIRMED |
| P3A-R026 | Strong structural metrics may obscure weak semantic correctness. | Determinism/completeness could be mistaken for validation success. | Keep metrics separate and prohibit any overall score or integration recommendation. | MITIGATED IN REPORTING |
| P3A-R027 | v1.1 role-to-step payload resolution is an adapter contract. | A future adapter change could alter replay meaning. | Version the schema/adapter rules and bind results to corpus and component versions. | OPEN |
| P3A-R028 | Improved v1.1 metrics may be mistaken for engine improvement. | Corpus remediation could be misrepresented as code optimization. | Report deltas as corpus fidelity changes and explicitly confirm the engine is unchanged. | MITIGATED IN EVIDENCE |
| P3A-R029 | A metric aggregate may compensate for a protected regression. | Release could pass despite lost determinism, traceability, or minority evidence. | Prohibit overall scores and use independent non-compensating gates. | MITIGATED IN POLICY |
| P3A-R030 | Failed regression evidence may be overwritten by a later passing run. | Historical instability could disappear. | Keep result, metric, failure, and certification histories append-only. | MITIGATED IN POLICY |
| P3A-R031 | Cross-corpus comparison may attribute corpus changes to the engine. | Fidelity corrections could be misreported as engine improvement. | Require certified delta/migration and distinguish corpus from engine deltas explicitly. | MITIGATED IN POLICY |
| P3A-R032 | Latency noise may block releases or drive premature optimization. | Observational variance could distort engineering priorities. | Keep latency descriptive and require environment/variance context. | MITIGATED IN POLICY |
| P3A-R033 | Permanent maintenance ownership and cadence are not yet named. | Reviews or canonical-release stewardship may become inconsistent. | Assign named owners and cadence during/after adoption; retain defined review functions meanwhile. | OPEN - NON-BLOCKING |
| P3A-R034 | Permanent adoption may be interpreted as freezing all methodology evolution. | Useful phase-specific validation improvements could be discouraged. | Permit versioned extensions while requiring approved governance to supersede mandatory controls. | MITIGATED IN ADOPTION SCOPE |
| P3A-R035 | Future phases may weaken gates for convenience. | Certification could lose comparability and audit value. | Make mandatory criteria and non-compensating gates the permanent minimum unless superseded through approved governance. | MITIGATED IN ADOPTION STATEMENT |

## Blockers

| ID | Blocker | Impact | Disposition |
| --- | --- | --- | --- |
| None | No active blockers at Phase 3A closeout. | None | N/A |

## Deferred Items

| ID | Item | Target | Rationale |
| --- | --- | --- | --- |
| P3A-D001 | Runtime integration | Future evidence-driven assessment | Phase 2C concluded the isolated path is sufficient; Phase 3A creates validation evidence only. |
| P3A-D002 | Adaptive orchestration | Future separately authorized phase | Determinism and reproducibility must be demonstrated first. |
| P3A-D003 | Performance optimization | After reproducible latency baseline | Optimization without characterized measurements is premature. |
| P3A-D004 | Live runtime comparator | Future read-only measurement design | The live runtime cannot enter the validation boundary without separate scope and safeguards. |
| P3A-D005 | LOCKED component changes | Future Board authorization if justified | Phase 3A authorizes none. |
| P3A-D006 | Future runtime replay implementation | Future separately authorized design | M2 defines only a reserved comparator contract; no live runtime access is authorized. |
| P3A-D007 | Replay corpus 1.0 certification | M5 first dataset | Certification requires actual reviewed cases, scenarios, hashes, coverage, and approval evidence. |
| P3A-D008 | First certified replay dataset | M5 | Authoring and certification controls are complete; actual case content and release approval remain separate work. |
| P3A-D009 | Runtime replay | Future separately authorized work | Corpus v1.0 explicitly does not certify runtime replay. |
| P3A-D010 | Replay Corpus v1.1 | Replay regression program | Required to encode executable semantic and negative cases while preserving immutable v1.0. |
| P3A-D011 | Replay regression automation | Next milestone | v1.1 is executable and certified; repeated comparisons should become a stable program. |
| P3A-D012 | Automated longitudinal runner | Future isolated validation milestone | M8 defines policy and history first; automation must preserve these gates and boundaries. |
| P3A-D013 | Named methodology owner and review cadence | Post-adoption maintenance record | Review functions are defined; permanent operational assignment is non-blocking closeout follow-up. |

## Governance Constraints

- GG-02 remains ratified and authoritative.
- Metrics and pass states create no governance authority.
- No runtime, Local AI, scoring, confidence, ranking, voting, authority, or provider-selection change.
- No LOCKED modification without prior explicit authorization.

## Acceptance Gate

Runtime integration shall not be considered until measurable improvements are demonstrated against the defined validation metrics. Inconclusive or failed evidence retains the isolated path.

## Current Recommendation

Product Owner acceptance was recorded on 2026-07-12. Remaining maintenance risks are non-blocking and remain governed by the permanently adopted methodology.

**PHASE 3A READY FOR CLOSEOUT**
