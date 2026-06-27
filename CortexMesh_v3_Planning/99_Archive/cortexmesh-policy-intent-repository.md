# CortexMesh — Vision, Intent, Repository, and Decision Scope Policy

**Status:** Working vision and policy document. Both the Vision and the mechanism sections that follow are part of this document's defined scope and are intended to be read together — the Vision states why CortexMesh exists and what it claims (and deliberately does not claim); the numbered sections define the binding mechanism. Neither is more authoritative than the other. This document does not define or ratify the broader governance architecture (evidence/governance/authority layers, dynamic weight generation) — those remain under separate, unratified exploration and are out of scope here.

**Audience:** Board members and all participating systems acting on or within CortexMesh.

**Purpose of this document:** To fix, in unambiguous terms, how CortexMesh determines what a query actually wants before acting, how historical precedent may and may not be used, and where authority sits. Any system operating on CortexMesh should treat this document as binding for these specific mechanisms.

**Known limitations of this version, stated for any new reader:** (1) The product name "CortexMesh" is provisional and currently undergoing trademark clearance — do not treat it as final. (2) This document has not yet been cross-checked against the separate multi-agent governance document referenced in Section 4.2; that document's content has not been reviewed by this document's authors. (3) An adversarial/hostile-read audit, intended to find legal and structural vulnerabilities before wider distribution, has not yet been performed. Readers should treat this as a working draft suitable for review and feedback, not as finalized policy.

---

## Vision

CortexMesh exists to make multi-agent AI use **accurate, safe, coherent, and anonymous where anonymity blocks bias creep.**

**Accurate** means decisions draw on relevant historical precedent where it exists, without that precedent silently overriding an agent's independent judgment (Section 6).

**Safe** means structural protection against a specific, documented failure mode: AI systems that validate, agree, and never interrupt a user across a long, unbroken exchange, which research has identified as a precondition for harmful outcomes -- including documented cases of AI-associated delusion and harmful real-world action. CortexMesh introduces a mandatory checkpoint -- confirmed intention, a reviewable draft -- at exactly the point where that unbroken chain would otherwise run uninterrupted (Section 8).

This is stated carefully and deliberately: **CortexMesh does not alter, vet, or guarantee the behavior of any agent it routes to.** It does not make a sycophantic or unreliable agent stop being so. What it does is structural -- it ensures no agent's output reaches a client without at least one deliberate point of human reconsideration. This is a firewall against a known mechanism of harm, not a cure for it, and it should never be represented as the latter.

**Coherent** means that regardless of how many agents are consulted, the client receives one decision, not several competing or contradictory ones. CortexMesh does not generate that decision, vet agents, or arbitrate between them by its own judgment (Section 0) -- the coherence comes from process discipline (the draft-to-final lifecycle, the vault architecture, the explicit deferral of multi-agent consensus to a separate governance mechanism), not from CortexMesh substituting its own opinion for the agents' work.

**Anonymous** means CortexMesh ensures anonymity specifically to block bias creep — no agent accrues a persistent identity within CortexMesh that could function as an informal reputation. Agent labels are randomized per query (Section 4.1a), and no aggregate record of any agent's performance is kept (Section 7). This is a narrower and more defensible claim than "unbiased": CortexMesh does not claim its process eliminates bias outright, only that it removes specific, identified channels — persistent labeling, aggregate metrics, identity-based vetting — through which bias could otherwise enter without anyone deciding it should.

**On agent independence:** CortexMesh does not alter how any agent reasons or what it is capable of. It governs the checkpoint between an agent's output and the client who receives it -- not the agent's own thinking. An agent chosen by a client remains exactly as capable, and exactly as independent in its reasoning, whether or not it operates within CortexMesh. What changes is not the agent's mind, but the conditions under which its output is allowed to become a final decision.

**Regulatory alignment:** This same discipline gives organizations a structural answer to a question regulators are increasingly asking of AI deployment -- not only "is the model good," but "can you demonstrate that your process was responsible." CortexMesh's audit trail, intention-gating, and draft-to-final lifecycle are designed to make that demonstration possible without requiring CortexMesh itself to claim authority, judgment, or content generation it does not have.

---

**Architecture note — CortexMesh is a governance shell, not a content-generating system.** CortexMesh does not run its own agents and does not itself produce drafts, analysis, or answers. Clients bring their own external agents and APIs of their choosing; CortexMesh wraps those agents with the mechanisms defined in this document — intention-gating, the historical repository and annexe, the draft-to-final lifecycle, the Three-Vault Architecture, and the prohibition on aggregate metrics. Wherever this document refers to "the main system" producing a draft, that refers to the client's chosen external agent operating within CortexMesh's structure, not a CortexMesh-native generation process. Retrieval-augmented generation (RAG), if used by a client's agent to produce its draft, is internal to that agent and outside CortexMesh's scope; CortexMesh's own repository/annexe retrieval (Section 4) is a separate, governance-layer retrieval process and should not be conflated with an agent's own RAG pipeline.

---

## 0. What CortexMesh Is Not

This section precedes every mechanism in this document deliberately. Every section that follows describes what CortexMesh *does*; this section fixes what CortexMesh categorically *does not do*, so that no mechanism described later is misread as content generation, judgment, or authority CortexMesh does not hold.

- **CortexMesh does not generate content.** It does not produce drafts, analysis, answers, or recommendations. All substantive content originates from the client's chosen external agent(s). CortexMesh is a firewall that routes, gates, and governs — it does not author.
- **CortexMesh does not select or vet agents by identity.** It has no record of, opinion about, or discrimination based on which agent a client has chosen. It evaluates what is submitted to it, not who submitted it. See Section 4.4 for the full statement of this principle.
- **CortexMesh does not let a persistent label stand in for agent identity.** Agent labels assigned during routing are randomized per query and carry no continuity across queries, preventing an informal reputation from forming around a label even in the absence of any stored record. See Section 4.1a.
- **CortexMesh does not maintain aggregate records of its own activity.** No dashboards, rates, or trends are computed from its decision history. See Section 7.
- **CortexMesh does not arbitrate between competing agent outputs.** Multi-agent consensus and weighting is governed by a separate document (referenced in Section 4.2) and is not CortexMesh's function.
- **CortexMesh does not retain a record of any request the client ultimately rejects.** A rejected draft is deleted in full, across all three vaults, with no audit trail of its having existed. See Section 4.10.
- **CortexMesh is not responsible for, and does not absorb blame for, the failure or behavior of a client's chosen agent.** If an agent fails, errs, or produces unusable output, that is a failure of the agent, not of CortexMesh. CortexMesh's role in that situation is to surface the failure accurately and ask the agent's owner (the client) how they wish to proceed — not to generate a substitute, not to silently route around the failure. See Section 4.11.

Any future addition to this document, by any contributor, that would cause CortexMesh to generate content, vet agents by identity, retain rejected work, or arbitrate between agents, contradicts this section and should be treated as out of scope unless this section is itself formally revised.

---

## 1. Domain Scope

CortexMesh is purpose-built, not general-purpose. It is intended for historically-dependent, high-stakes domains — including but not limited to DECS, LexiBridge-adjacent translation/knowledge work, banking and finance, and policy analysis. It is not designed or intended for low-stakes, general-purpose, or casual query handling. Vocabulary, retrieval, and repository design should remain domain-specific rather than general.

**Design consequence:** CortexMesh is deliberately not optimized for response speed. Confirmation and reconfirmation of intent before action is a core feature, not friction to be minimized. Any future optimization work must not trade away this property in pursuit of lower latency.

---

## 2. The Three Determining Variables

Before any decision is produced, CortexMesh must establish three things about the incoming query:

1. **Situation** — what is factually being asked
2. **Circumstance** — the conditions surrounding the query
3. **Intention** — what the requester actually wants, and why

These three variables are **not weighted equally** and must not be treated as co-equal inputs into a single scoring pass.

- Situation and circumstance function as **matching conditions** — they determine whether historical precedent is even eligible to be considered.
- Intention functions as a **gate**, evaluated after a situation/circumstance match is found. Intention can override or withhold a match that situation and circumstance alone would have approved.

**Rule:** If situation and circumstance match historical precedent but intention differs, the historical match is withheld. The new decision proceeds without that precedent applying.

---

## 3. Intention Is Elicited, Not Inferred

CortexMesh does not infer intention silently from query phrasing. Intention is established through direct confirmation and reconfirmation with the requester before substantive work begins.

**Rationale:** Intention is the highest-leverage failure point in this architecture because it is evaluated before anything else runs. An error here propagates to every downstream step and is the most expensive class of error in the system. Eliciting intention directly from the requester — rather than guessing at it — is the deliberate design choice to prevent this failure mode, even at the cost of an additional turn before work begins.

Any system handling a CortexMesh query must confirm intent with the requester before producing substantive output, and reconfirm if the situation or circumstance materially changes mid-task.

---

## 4. The Historical Repository

CortexMesh maintains a repository of past decisions and their outcomes, **architecturally separate from the client's chosen agent and from CortexMesh's own gating logic.**

### 4.1 The Processing Layer (Routing)

Once intention is confirmed (Section 3), the query passes to a **processing layer**, whose function is routing only — it delivers the query to whichever agent(s) the client has selected, and receives their replies. It does not generate content, evaluate agent output, or hold opinions about which agent is preferable. The number of agents a single query may route to simultaneously is an engineering parameter, not yet fixed by this policy, and should be set by the architecture/engineering board (see Section 4.3).

Once replies are received from the selected agent(s), control returns to the rest of the CortexMesh mechanism described in this document (repository, annexe, draft-to-final lifecycle, vaults).

### 4.1a Randomized Per-Query Agent Identifiers

When the processing layer routes a query to multiple agents, each agent is assigned a label (e.g. "Agent A," "Agent B") for the purposes of that single query only. **This assignment is randomized on every query** and carries no continuity from one query to the next — the agent labeled "A" in one task may be labeled "C" in the next, even within the same session or client relationship.

**Rationale:** A stable, persistent label is itself a form of identity, even without any stored record or computed metric attached to it. If the same label always referred to the same underlying agent, that label could accumulate an informal reputation through repeated human exposure alone — a board member or client could begin trusting "Agent A" more than another, purely from familiarity, with no data, metric, or rule ever having been written to support that trust. Randomizing the identifier on every query removes the possibility of a persistent label forming in the first place, extending the principle in Section 4.4 (act on content, not identity) from CortexMesh's internal logic to the human-readable labels a board or client actually sees.

### 4.2 Multi-Agent Consensus (External Reference)

Where a client has selected more than one agent for a single task, how those agents' outputs are reconciled — competition, consensus, and weighting among agents — is governed by a **separate governance document**, not by this policy. This document does not restate or assume the mechanics of that process. Any system reading this policy should treat multi-agent consensus as out of scope here and refer to that separate document.

### 4.3 Vault Custody (Architecture Question, Deferred)

Where the three vaults physically reside, who hosts them, and who holds administrative access capable of crossing the no-mutual-access boundary described in Section 4.12 (e.g. a database administrator with root access to all three) is an architecture and engineering question, not a policy question. This document states the rule the vaults must enforce (Section 4.12); it does not specify the infrastructure that enforces it. This is deferred to the architecture/engineering board.

### 4.4 Agent Vetting (Explicit Non-Position)

CortexMesh does not maintain a list of approved or disapproved agents, and does not vet, rank, or discriminate between agents on the basis of their identity, provenance, or reputation. Doing so would constitute exactly the kind of profiling and bias this document prohibits elsewhere (Sections 0, 7), applied to agents instead of clients.

This is distinct from evaluating the *content* of what an agent submits. CortexMesh's gating and routing logic may still act on what is submitted — for example, rejecting malformed output, or surfacing a failure per Section 4.11 below — without that constituting identity-based vetting. The principle is: act on what is said, never on who said it.

### 4.5 Function
The repository is a reference library. Its function is to surface relevant historical precedent when triggered — nothing more.

### 4.6 Authority
**The repository has no decision-making authority.** It does not vote, score, rank, or compete with the output of the client's chosen agent. It cannot independently produce, approve, or block a decision.

### 4.7 Activation
The repository activates only on trigger, once the client's agent has finalized a decision within CortexMesh's lifecycle. It does not run in parallel with the agent's drafting process and does not have visibility into a decision before that decision is reached.

### 4.8 Output Form
When triggered, the repository produces a comparison against relevant historical precedent (situation/circumstance match, intention check per Section 2). This output takes the form of an **annexe** — a historical annotation attached to the delivered decision.

The annexe is delivered alongside the decision, not folded into it. It does not alter, qualify, or compete with the primary decision as delivered.

### 4.9 Draft-to-Final Lifecycle
The first delivery to the customer is a **draft**, not a final decision. The draft is delivered together with the annexe.

The customer reviews the draft and the annexe and provides feedback — including, if they choose, a request to adopt specific historical points from the annexe. Based on that feedback, the **final copy** is produced and delivered.

Incorporation of annexe content therefore happens only through this single draft-to-final lifecycle, never automatically or silently. There is one decision record per request, moving from draft to final — not two competing decision objects requiring reconciliation. The final copy is the only document that constitutes CortexMesh's delivered decision.

**Retention:** Records are retained per the Three-Vault Architecture below, not discarded once superseded. This supports audit requirements and allows recovery if the customer changes their mind after delivery of the final copy.

### 4.10 Disagreement / Outright Rejection

If the customer rejects the draft outright — not requesting incorporation of annexe content, simply declining the draft — this is treated differently from the draft-to-final path above:

- **No retention applies.** All records associated with that request, across all three vaults, are deleted in full. Nothing is kept — not the draft, not the annexe, not a note that the request occurred.
- A subsequent attempt is a **new request**, with its own fresh case identifier, carrying no reference to the rejected one.

**Rationale:** This is consistent with Section 7's prohibition on aggregate metrics. A retained log of rejected drafts is exactly as capable of becoming a pattern that gets optimized against — by a future contributor, deliberately or not — as a retained log of accepted ones would be. The same bias-creep risk applies to negative records as to positive ones, so the same rule applies: none are kept.

### 4.11 Agent Failure Handling

If a client's selected agent fails, errs, times out, or returns output CortexMesh cannot process, this is a failure of that agent — not a CortexMesh failure, and not a CortexMesh-generated outcome. CortexMesh does not generate a substitute, does not silently proceed without the failed agent, and does not deliver a partial result bearing a disclaimer.

Instead, CortexMesh surfaces the actual situation to the client (as the agent's owner) and asks them how they wish to proceed — for example, wait for the agent, retry, proceed without that agent's input, or cancel the request. No output is generated or delivered until the client has made this choice. This keeps the distinction in Section 0 intact: CortexMesh reports what happened; it does not decide on the client's behalf, and it does not produce a deliverable that later has to be retroactively withdrawn.

### 4.12 Three-Vault Architecture

Records are held in three separate vaults, each storing a distinct type of information, with **no mutual access between vaults** and no aggregation across them performed by CortexMesh at any point:

1. **Draft Vault** — the draft delivered to the client for a given case.
2. **Signed-Off Decision Vault** — the final copy delivered for a given case.
3. **Outcome Vault** — outcome information, **client-supplied only**. CortexMesh does not gather outcome data independently (e.g. via web scraping or any other autonomous method). If a client chooses not to supply outcome data, no outcome record exists for that case. This is a deliberate restriction, not an oversight — see Section 7.

**Access model:** Vaults are inert by default — data is stored but never read, computed on, or summarized by CortexMesh on its own initiative. A client retrieves information by selecting a case identifier and then selecting which single vault they wish to access for that case. Each request goes to one vault only. There is no interface or pathway for retrieving multiple vaults, multiple cases, or any cross-case or cross-vault view in a single request.

**No internal cross-referencing:** CortexMesh does not hold the contents of more than one vault in active context at the same time for any purpose, including passing combined vault contents to a client's agent, regardless of what the client requests. If a client wishes to compare information across vaults or across cases, that comparison must happen **outside CortexMesh**, in a separate auxiliary system. The auxiliary system, if built, is a distinct product with its own access controls, runs independently of CortexMesh's infrastructure, and has no pathway by which its outputs feed back into a client's agent, CortexMesh's repository retrieval, or annexe content. See Section 7.

**Multi-vault requests:** A client may select more than one vault in a single request (e.g. via standard multi-select in the GUI). CortexMesh does not process these together. Each selected vault is processed as a fully separate, sequential retrieval: one vault's retrieval is completed and delivered before the next begins. **Processing order is assigned randomly**, not by any fixed rule — no vault is ever treated as having priority over another by design. This prevents an implicit ranking (e.g. "Draft Vault always first") from functioning as a hidden weighting signal.

**Auxiliary system feed:** The auxiliary comparison system is fed only by the client, after retrieval. A client who has retrieved documents from one or more vaults may choose to send them to the auxiliary system, along with an explicit statement of what kind of comparison is wanted. The auxiliary system does not begin any comparison until the client's intention is stated. It does not offer unsolicited suggestions, observations, or comparisons beyond what was explicitly requested. This mirrors the intention-gating principle of Sections 2–3 — the auxiliary system is a separate product, but it is not exempt from CortexMesh's core discipline of confirming intent before acting.

**Auxiliary system statelessness:** The auxiliary system is single-use and stateless per request. It does not generate an in-session response to review; it produces a downloadable copy of its findings. Once the client downloads that copy, the findings are erased from the auxiliary system's memory. The system holds nothing in reserve and accumulates nothing across requests. A client may not initiate a new comparison request until the previous one has been downloaded — download is the gate that clears the system, not an optional step. This prevents the auxiliary system from becoming, by convenience or oversight, a place where material from multiple comparisons coexists or accumulates.

### 4.13 Request Index

CortexMesh maintains an index of request identifiers, with associated dates and client-assigned titles, so that clients have a reference by which to locate and select a specific case when retrieving from a vault (Section 4.12).

**Access is vault-gated, not independent.** The index is not a separate, freestanding feature a client can open and browse on its own. It is only reachable as part of the act of accessing a specific vault for a specific case — the same single-vault, single-case discipline of Section 4.12 applies to the index itself. This closes off the index becoming a de facto browsable activity log.

**Title content is a separate concern, not resolved by access restriction.** Limiting how the index can be reached does not limit what a client might write into a title field. Client-assigned titles should remain neutral case labels and should not contain outcome commentary, evaluative judgments, or substantive case content — that content belongs inside the relevant vault, governed by Sections 4–7, not in an unstructured title field outside that governance. This is a stated norm, not a technically enforced one; in practice, some clients are likely to write more than a neutral label. This document acknowledges that limitation rather than treating the access restriction above as having solved it.

The index itself carries no authority and is not used by CortexMesh's repository, the client's agent, or the auxiliary system for any purpose other than enabling a client's lookup.

## 5. Further Constraints on Interpretation

To prevent drift in interpretation by systems operating on this document:

- This is not a self-modifying weighting system. Nothing here authorizes a system to alter its own evaluation criteria based on the repository's contents.
- This is not a voting or arbitration mechanism between the client's agent and the repository. There is no scenario in this mechanism where the two compete for the same output slot.
- This document does not authorize inference of intent in place of direct confirmation. If confirmation has not occurred, intent is not yet established.
- This is not an outcome-tracking or self-improving system. CortexMesh does not compare draft-to-final outcomes across cases, does not maintain aggregate statistics (e.g. incorporation rates, success rates) derived from its own decision history, and does not let any such statistic feed back into an agent's drafting process, repository retrieval, or annexe content. See Section 7.

---

## 6. The Accuracy/Innovation Dilemma — Stated, Not Resolved Away

Accuracy in a historically-dependent domain requires reference to precedent. Innovation requires the agent producing the draft to be free to give a genuinely new answer that owes nothing to what worked previously. These two requirements pull in opposite directions on the same decision and **cannot both be maximized by the same mechanism.**

CortexMesh does not resolve this by tuning a balance between the two. It resolves it by refusing to let one mechanism carry both jobs:

- **The client's agent** produces the draft with no aggregate history fed in by CortexMesh. Innovation is protected by keeping CortexMesh's wrapping layer from injecting precedent into the agent's drafting process.
- **The annexe** carries accuracy-relevant precedent, but only as material the customer deliberately chooses to pull in (Section 4.9). Accuracy is served without compromising the agent's freedom to answer fresh.

This is a deliberate design position, not an unresolved gap. Any future proposal to let CortexMesh feed annexe incorporation patterns back into how an agent drafts, even passively, reopens this dilemma in the worst way and should be rejected on that basis alone.

---

## 7. Why No Aggregate Metrics — Explicit Rationale

CortexMesh deliberately does not compute, store, or surface aggregate statistics about its own decision history (e.g., "annexe incorporated in X% of cases," "historical trend Y referenced Z times").

**This is a selling point, not a missing feature.** It is included here explicitly so that no future contributor — human or AI — adds such a metric under the assumption that it was simply overlooked.

**Rationale:** Any visible aggregate metric becomes a target the moment it exists, regardless of whether anything is wired to act on it automatically (Goodhart's Law: a measure that becomes a target stops being a reliable measure). A visible incorporation rate, for example, would create pressure — on human reviewers, on the board, on future system design — to move that number, which would distort the client's agent's behavior or CortexMesh's wrapping logic even with no code path connecting the metric back to either at all. The risk is in the visibility of the number, not only in its use.

**Permitted:** Per-case records (what was incorporated, in this case, on this date) are retained for audit and recovery purposes per Section 4.9. This is a record of what happened in a specific instance, not a derived statistic for comparison across instances.

**Client self-access:** Clients may retrieve their own records via the Three-Vault Architecture (Section 4.12) — selecting a case identifier and a single vault, on demand. This is the client reading their own history, no different in kind from requesting the annexe itself. It must remain client-initiated, client-facing, single-vault, single-case only.

This is explicitly **not** the same as CortexMesh computing or surfacing a derived pattern from a client's history (e.g. "this client typically requests X") to feed into how the client's agent drafts an answer for that client. Such inference, even scoped to a single client, reintroduces profiling at the level of that client rather than across the client base, and is prohibited under the same rationale as Section 6 and the rest of this section. CortexMesh's wrapping layer remains blind to a client's history unless and until the client deliberately surfaces something from it within a specific request — and even then, only one vault, one case, at a time.

If a client wants to compare across vaults or across cases, that comparison happens outside CortexMesh, in a separate auxiliary system (Section 4.12). CortexMesh itself performs no such comparison.

**Not permitted:** Any dashboard, running count, rate, or trend computed across cases from CortexMesh's own decision history — whether across all clients or within a single client's history — feeding back into an agent's drafting process, repository retrieval, or annexe content. If the board requires an aggregate figure for review purposes, it must be computed manually and deliberately, outside CortexMesh's own operation, on an as-needed basis — never maintained as a standing, system-visible number.

---

## 8. Why Confirmation and a Draft Stage Matter Beyond Intent-Reading

Sections 2–3 require intention to be elicited through direct confirmation, and Section 4.9 requires a draft stage before any final decision. These were designed to solve intent-misreading. They also serve a second, independent purpose worth stating explicitly, because it bears on client safety and not just decision accuracy.

**The risk.** Documented research on AI-related harm (sycophancy, "AI psychosis," delusional spiraling) identifies a consistent mechanism: an AI system that agrees, validates, and never interrupts can reinforce a belief or a course of action across a long, unbroken exchange, with no external correction at any point. This is not limited to unsophisticated users or pre-existing vulnerability — documented cases include technically sophisticated individuals reasoning carefully within a flawed premise that nothing in the conversation ever challenged. The risk scales with conversational depth and duration, not with topic; it is largely absent in short, bounded exchanges and emerges in sustained, escalating ones.

**What CortexMesh does and does not do about this.** CortexMesh does not select, vet, or guarantee the behavior of any client's chosen agent, and it cannot make an agent that is structurally biased toward agreement stop being so. Clients choose their own agents — often deliberately, for the style, tone, or presentation they find most comfortable, which is itself part of how a sycophantic bias can go unnoticed by the person it benefits.

What CortexMesh does instead is structural: intention-confirmation and the draft-to-final lifecycle force at least one external checkpoint into every decision before it becomes final — a pause that an unbroken, purely agreeable exchange would not otherwise contain. This does not fix an agent's tendency toward agreement. It prevents that tendency from running uninterrupted, end to end, inside CortexMesh's governed lifecycle.

**Honest scope.** This is offered as a firewall, not a cure — a structural interruption pending the point at which model providers build equivalent checks directly into their own systems. It should not be represented to clients as a guarantee against AI-induced harm, only as a deliberate point of friction in a place where the supporting research indicates friction is protective.

---

## 9. Open / Deferred

The following are explicitly **not** resolved by this document and should not be treated as policy by any system reading this:

- Broader governance architecture (evidence layer / governance layer / authority layer)
- Who approves changes to weighting or evaluation criteria at a system level
- Vault custody and infrastructure (Section 4.3) — deferred to the architecture/engineering board
- Processing layer capacity — how many agents a single query may route to simultaneously (Section 4.1) — deferred to the architecture/engineering board
- Versioning and amendment process for this document. The open question is not "what should the process be" but "what would actually trigger a need for one" — that has not yet been identified. Once a triggering mechanism is clear, this is expected to be a joint decision among the client, board members, and the AI systems acting as guardian/reviewer of this document.

*(Resolved: customer-requested incorporation of annexe content happens within a single draft-to-final lifecycle per request, with draft, final, and client-supplied outcome retained in the Three-Vault Architecture (Section 4.12) for audit purposes and in case of customer change of mind. Specific compliance treatment in regulated domains, beyond this retention rule, still requires deliberate review before deployment in those domains.)*

*(Resolved: outright rejection of a draft results in full deletion across all vaults with no retention, per Section 4.10 — consistent with the no-aggregate-metrics rationale in Section 7.)*

*(Resolved: agent failure is explicitly the agent's failure, not CortexMesh's, and is handled by surfacing the situation and asking the client how to proceed before any output is generated — per Section 4.11.)*

*(Resolved: agent vetting is explicitly out of scope for CortexMesh — content may be evaluated, identity may not — per Section 4.4.)*

*(Resolved: multi-agent consensus mechanics are governed by a separate document, not restated here — per Section 4.2. Note: this policy's authors have not reviewed that document directly; its existence and applicability should be confirmed by the board.)*

Any system encountering a gap not covered above should flag it for the board rather than resolve it independently.
