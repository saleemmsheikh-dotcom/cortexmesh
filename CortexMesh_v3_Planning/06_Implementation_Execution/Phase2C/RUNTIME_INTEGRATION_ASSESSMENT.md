# Phase 2C M11 - Runtime Integration Assessment

## 1. Purpose

Assess whether the Phase 2C reference orchestration engine should remain an isolated planning/evidence subsystem or be integrated into the live CortexMesh runtime.

This is a documentation-only assessment. It authorizes no implementation, runtime change, Local AI change, adaptive behavior, or LOCKED component modification.

## 2. Assessment Basis

The assessment reviewed:

- the M2-M10 Phase 2C reference pipeline;
- `orchestrator.py`;
- `competition/scorer.py`;
- `agents/authority.py`;
- `core/contracts.py`;
- `core/external_runner.py`;
- `governance/snapshot.py`;
- `engine/runner.py`;
- `agents/local_solver.py`;
- `agents/local_ai_bridge.py`;
- the LOCK registry and current Phase 2C constraints.

The six named candidate core components are explicitly LOCKED. The agent and runner glue is not listed as LOCKED, but it feeds directly into the LOCKED runtime orchestrator and its scoring, authority, confidence, memory, evolution, and governance behaviors.

## 3. Current Isolated Reference-Engine Value

The M10 engine already provides measurable engineering value without runtime integration:

- deterministic composition of capability resolution, agent planning, execution planning, evidence collection, consensus assessment, and synthesis;
- dependency injection for isolated testing;
- explicit simulated-output boundaries rather than hidden agent calls;
- full preservation of intermediate artifacts and diagnostics;
- rejection of provider selection, authority, scoring, confidence, ranking, voting, and governance semantics;
- reproducible exact, compatible, partial, divergent, and insufficient-evidence behavior;
- 200 passing repository tests at M10 completion;
- an executable reference contract for future adapters, fixtures, design review, and regression analysis.

This value does not depend on the live runtime. The isolated subsystem is useful for offline evidence analysis, architecture validation, deterministic scenario testing, and defining future integration contracts.

## 4. Live Runtime Characteristics

The live runtime has materially different semantics from the reference engine:

- `orchestrator.py` uses randomness for solver selection and activation;
- agents are invoked directly through `solver.act` and critics through `review`;
- solutions carry confidence values;
- `competition/scorer.py` calculates critic and weighted scores and selects a best candidate;
- `agents/authority.py` applies trust, calibration, repetition penalties, diversity bonuses, specialist boosts, and an authority total before selecting a decision;
- runtime memory records wins, failures, confidence, trust, negative knowledge, evolution, entropy, and role weights;
- governance enforcement and snapshot creation occur inside the orchestration lifecycle;
- `engine/runner.py` persists runtime memory based on the authority outcome;
- dev-mode `agents/local_solver.py` may invoke Local AI through `agents/local_ai_bridge.py`.

The Phase 2C reference engine intentionally prohibits or omits these behaviors. It consumes simulated evidence and returns advisory synthesis; it does not produce a runtime winner or authority decision.

## 5. Candidate Integration Points

### 5.1 `orchestrator.py` - LOCKED

Potential integration points include before solver selection, after solution generation, after critique, before scoring, or after authority selection.

Each location is unsafe without redesign:

- before solver selection, the reference engine has no execution outputs and cannot complete its pipeline;
- after solution generation, live solution schemas must be adapted into evidence claims, assumptions, limitations, diagnostics, and trace identifiers;
- before scoring, advisory evidence alignment could accidentally influence score or confidence semantics;
- after authority selection, synthesis would be post hoc and could conflict with the already selected winner;
- replacing the central pipeline would remove or alter existing budget, critic, scoring, authority, memory, evolution, and governance behavior.

Any direct insertion changes the LOCKED orchestrator and requires prior Board authorization.

### 5.2 `competition/scorer.py` - LOCKED

The scorer produces numeric critic and weighted totals and selects a highest-scored result. Phase 2C consensus and synthesis explicitly create no score, rank, winner, or confidence adjustment.

Using alignment categories as scoring inputs would violate the Phase 2C contract. Replacing scoring with synthesis would change core runtime selection semantics. No safe direct integration is identified.

### 5.3 `agents/authority.py` - LOCKED

The authority agent combines score, trust, calibration, diversity, specialist preference, and repetition penalties to choose an accepted candidate or conflict resolution. `ConsensusAssessment` is advisory and must never become authority, vote weight, or a winning-position mechanism.

Passing consensus or synthesis into authority requires a separately governed semantic contract. Current evidence does not justify this change.

### 5.4 `core/contracts.py` - LOCKED

This module enforces capability isolation and prohibits protected imports and memory mutation. A live Phase 2C adapter could require new envelope or validation contracts, particularly if used through the capability gateway.

Changing these protections would affect a security boundary. No M10 evidence demonstrates a need to modify it.

### 5.5 `core/external_runner.py` - LOCKED

The external runner executes untrusted capabilities in Docker with resource and network isolation. The Phase 2C reference pipeline is an in-process deterministic subsystem, not an untrusted capability payload.

Using the external runner would require serialization contracts, image lifecycle, timeout behavior, failure mapping, and reproducibility evidence. It would also modify a LOCKED security component. No benefit sufficient to justify this path has been measured.

### 5.6 `governance/snapshot.py` - LOCKED

Snapshots preserve governed runtime state and rollback that state. Phase 2C results are descriptive and advisory, with no governance state mutation.

Adding Phase 2C results to governance snapshots risks implying governance status and expanding snapshot contracts. The reference artifacts can be retained independently without modifying this component.

### 5.7 Existing Non-LOCKED Agent and Runtime Glue

`agents/local_solver.py`, `agents/local_ai_bridge.py`, and `engine/runner.py` are candidate adapter surfaces, but they do not provide a complete safe integration path:

- `local_solver.py` returns the legacy solution schema and feeds directly into the LOCKED orchestrator;
- `local_ai_bridge.py` performs actual provider/model configuration and Local AI invocation, which the reference engine explicitly excludes;
- `engine/runner.py` calls the LOCKED `orchestrate` function and persists authority-derived memory state.

A separate offline harness or export adapter could be created in a new non-LOCKED module, but connecting it to live task execution would still change behavior at or around the LOCKED orchestrator. The current reference engine already supports offline callers without such changes.

## 6. Potential Benefits of Live Integration

Potential benefits are plausible but unmeasured:

- structured evidence and traceability for live agent outputs;
- visible minority evidence and unresolved divergence;
- deterministic synthesis alongside legacy final output;
- clearer diagnosis of missing execution outputs;
- a future provider-neutral planning description.

No benchmark currently shows improved task quality, safety, latency, cost, failure recovery, or auditability in the live runtime. The potential benefits therefore do not outweigh the known semantic and governance risks.

## 7. Risks and Failure Modes

| Risk | Failure mode | Consequence |
| --- | --- | --- |
| Dual decision systems | Advisory synthesis conflicts with authority-selected winner. | Users cannot tell which result governs runtime behavior. |
| Consensus-to-score leakage | Alignment category becomes a score or confidence proxy. | Violates Phase 2C boundaries and changes LOCKED scoring semantics. |
| Identity leakage | Live provider/model provenance influences selection or prominence. | Breaks provider neutrality. |
| Schema mismatch | Legacy solution text lacks explicit claims, assumptions, limitations, or trace data. | Evidence is incomplete or fabricated by an adapter. |
| Non-deterministic inputs | Random selection and invocation produce different evidence sets. | Reference determinism no longer characterizes end-to-end runs. |
| Partial failure | Some live agents, critics, or providers fail before evidence collection. | Synthesis may misrepresent availability unless failure contracts are designed. |
| Memory side effects | New outputs affect wins, confidence, trust, evolution, or governance state. | Rollback becomes complex and may require LOCKED changes. |
| Latency and budget expansion | Planning, evaluation, and synthesis add work to the live loop. | Existing budget and timeout assumptions may fail. |
| Governance ambiguity | Structured advisory output is mistaken for authority or Board approval. | GG-02 process could be blurred. |
| Rollback incompleteness | Adapter removal does not restore changed memory or snapshots. | Runtime state remains contaminated after rollback. |

## 8. SAFE Non-LOCKED Alternatives

The following alternatives preserve current value without live integration:

1. Keep M2-M10 as an isolated reference and test subsystem.
2. Use deterministic fixtures or externally supplied historical/simulated outputs for offline evaluation.
3. Build a separate documentation-only schema mapping between legacy solution fields and Phase 2C evidence fields before any adapter code.
4. Export live-run artifacts manually or through an independently reviewed read-only tool, then process copies offline; do not write results back into runtime memory or governance state.
5. Use the reference engine for scenario comparison, regression fixtures, architecture demonstrations, and integration contract testing.
6. Add no Local AI, provider, agent, scorer, authority, or orchestrator dependency to the reference subsystem.

These alternatives retain evidence alignment and synthesis benefits while avoiding changes to runtime decisions.

## 9. Evidence Required Before Reconsideration

Before any integration design or Board proposal, the following evidence is required:

- a concrete user/runtime problem that the isolated path cannot address;
- a versioned mapping from live solution and critique schemas to evidence claims, assumptions, limitations, diagnostics, provenance, and traceability;
- deterministic replay fixtures from representative live runs;
- comparative benchmarks for quality, auditability, latency, cost, and failure recovery;
- evidence that consensus categories cannot affect score, confidence, rank, authority, provider selection, or vote weight;
- defined behavior for missing, malformed, timed-out, or contradictory live outputs;
- a data-flow and mutation inventory covering ledger, memory, trust, confidence, evolution, governance enforcement, and snapshots;
- a security review for any capability or external-runner boundary;
- an explicit compatibility contract for existing CLI and `engine.runner` output;
- a canary and feature-disable design with zero-write shadow operation;
- test coverage proving identical legacy outcomes when the feature is disabled;
- a complete LOCKED component impact list and Board authorization before implementation if any listed component changes.

This evidence does not currently exist in the Phase 2C record.

## 10. Rollback Strategy for Any Future Trial

No trial is recommended now. If reconsidered after the evidence above exists, rollback must be designed before implementation:

1. Run initially in read-only shadow mode with no influence on selection, scoring, authority, confidence, memory, evolution, or governance.
2. Gate the adapter behind a default-off explicit feature setting.
3. Preserve the pre-integration runtime response schema and execution path unchanged.
4. Write Phase 2C artifacts to an isolated ephemeral or append-only store, not governed runtime memory.
5. Record correlation identifiers linking shadow artifacts to live runs without provider/model decision use.
6. Define abort thresholds for exceptions, latency, schema mismatch, missing evidence, or output drift.
7. Roll back by disabling and removing the adapter, then verify legacy regression behavior and confirm no Phase 2C state remains in memory or governance snapshots.
8. If LOCKED files are involved, include file-level restoration, verification evidence, and Board-reviewed rollback authorization.

## 11. Governance Implications

- Direct integration with `orchestrator.py` changes a LOCKED component.
- Changes to scoring, authority, contracts, external execution, or governance snapshots implicate additional LOCKED components.
- GG-02 does not permit machine consensus or synthesis to create governance authority.
- Any LOCKED implementation requires explicit unanimous Board authorization before work begins.
- No Board proposal is justified without measurable benefits and the missing evidence listed in Section 9.
- A future non-LOCKED adapter design would still require proof that it does not alter the behavior or contracts of LOCKED callers and callees.

## 12. Adaptive Orchestration

Adaptive orchestration should remain deferred. The live runtime already adapts selection weights, trust, confidence, entropy, and evolution. Adding Phase 2C adaptation without a clear separation contract could create a second feedback system and violate the prohibition on scoring, confidence, ranking, provider preference, and authority effects.

No adaptive behavior should be designed for implementation until runtime observation contracts, measurable objectives, feedback boundaries, failure isolation, and governance implications are separately assessed.

## 13. Engineering Conclusion

The isolated reference engine is sufficient for the demonstrated Phase 2C value. Live integration has plausible benefits but no measured improvement, no validated live-evidence adapter, no shadow-mode contract, and no proof that legacy scoring, authority, confidence, memory, and governance semantics remain unaffected.

Direct integration would touch the LOCKED orchestrator and may implicate the LOCKED scorer, authority, contracts, external runner, and snapshot components. The non-LOCKED glue does not avoid those downstream boundaries.

## 14. Outcome

A. SAFE ISOLATED PATH SUFFICIENT

No runtime integration or Board proposal recommended.
