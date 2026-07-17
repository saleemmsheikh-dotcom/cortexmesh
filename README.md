# CortexMesh

## Governed Multi-Agent AI Orchestration Platform

[![Regression: 226/226 passing](https://img.shields.io/badge/regression-226%2F226%20passing-brightgreen)](CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/reproduction/EXP-001-R2/REPRODUCTION_REPORT.md)
![Python 3](https://img.shields.io/badge/python-3-blue)
![License not yet selected](https://img.shields.io/badge/license-not%20yet%20selected-lightgrey)

**CortexMesh is an engineering and research platform for governed AI orchestration. It prioritizes deterministic behaviour, reproducible evidence, and architectural discipline over rapid feature expansion.**

CortexMesh coordinates AI-system components within explicit governance, evidence, and validation boundaries. The repository combines provider-neutral Local AI support, a deterministic reference orchestration pipeline, replay-based validation, and a preregistered research methodology. Its published results are deliberately bounded: CortexMesh is currently a governed engineering and research platform, not a production-certified AI framework.

## Current Status

| Status | Value |
| --- | --- |
| Foundation | 1.0 established |
| Research | RP-001 baseline and reproductions complete |
| Validation | Permanently adopted methodology |
| Orchestration | Isolated deterministic reference engine |
| Commercial | Research platform; no readiness claim |

## Repository Purpose

CortexMesh exists to study and engineer multi-agent orchestration while preserving governance authority, deterministic controls, provenance, minority evidence, unresolved divergence, and reproducibility. It provides a structured environment for architecture, implementation evidence, replay validation, and controlled research.

CortexMesh is not presented as:

- a production-certified deployment framework;
- an autonomous governance authority;
- evidence that multi-agent orchestration is universally superior;
- a commercial-readiness certification;
- an adaptive or continuously learning orchestration system.

## Key Features

- **Deterministic orchestration:** capability resolution, agent-role planning, execution planning, evidence collection, consensus assessment, and synthesis are reproducible for equivalent inputs.
- **Descriptive evidence preservation:** provenance, trace identifiers, assumptions, limitations, diagnostics, minority evidence, and unresolved divergence remain visible.
- **Consensus without voting:** consensus evaluates evidence alignment without score, rank, confidence adjustment, authority, majority rule, or vote weight.
- **Replay-first validation:** versioned certified replay corpora support deterministic regression and reproducibility assessment.
- **Independent release gates:** a strong metric cannot compensate for regression in another protected metric.
- **Provider neutrality:** provider and model identity are descriptive provenance, not authority or preference signals.
- **Local AI support:** provider-neutral management and adapters support controlled local-provider integration.
- **Governance boundaries:** GG-02 and LOCKED-component protections separate engineering evidence from governance authority.
- **Immutable certification:** published baselines and evidence remain preserved; corrections require explicit new versions or append-only records.

## Repository Structure

```text
cortexmesh/
├── agents/                         Live agent implementations
├── core/                           Contracts and execution boundaries
├── engine/                         Runtime engine components
├── governance/                     Runtime governance support
├── tests/                          Regression and validation tests
└── CortexMesh_v3_Planning/
    ├── 00_Governance/              Governance records and Board sessions
    ├── 04_Architecture/            Architecture records
    ├── 06_Implementation_Execution/ Sealed phase evidence and reference work
    ├── 07_Research/                Research programs and reproducibility evidence
    ├── 99_Archive/                 Preserved historical material
    └── FOUNDATION_BASELINE_v1.0.md Foundation 1.0 landmark
```

The planning tree is the canonical source for architectural, governance, validation, and research records. See the [CortexMesh directory map](CortexMesh_v3_Planning/CORTEXMESH_DIRECTORY_MAP.md) for the detailed index.

## Architecture

CortexMesh separates authority and responsibility across five principal layers:

| Layer | Established role |
| --- | --- |
| Governance | Controls Board decisions, protected boundaries, ratification, and applicable implementation authority |
| Validation | Provides immutable replay corpora, independent gates, certification, regression, and reproducibility records |
| Orchestration | Provides an isolated deterministic pipeline for planning, evidence, non-voting consensus, and synthesis |
| Local AI | Provides provider-neutral management, configuration, discovery, diagnostics, and controlled integration |
| Provider | Defines shared contracts and repeatable provider-extension requirements |

The [Foundation 1.0 baseline](CortexMesh_v3_Planning/FOUNDATION_BASELINE_v1.0.md) is the architectural landmark for these layers. The Phase 2C reference engine remains isolated from live runtime integration, and research or validation output does not create governance authority.

## Foundation Timeline

```text
Foundation 1.0
    Phase 1B — Local AI Platform
        ↓
    Phase 2A — Provider Platform Consolidation
        ↓
    Phase 2C — Reference Orchestration Engine
        ↓
    Phase 3A — Validation and Certification Framework
        ↓
    RP-001 — Baseline Characterization and Reproduction
        ↓
    Session 13 — Independent Critical Review
```

Published phase tags preserve the completed baselines: `phase1b-complete`, `phase2a-complete`, `phase2c-complete`, and `phase3a-complete`.

## Validation and Reproducibility

Phase 3A established the permanent validation and certification methodology. It uses immutable, versioned replay corpora and independent release gates rather than a compensating aggregate score.

The sealed Phase 2C reference engine was characterized using certified Replay Corpus v1.1. EXP-001 completed 240 executions, EXP-001-R1 internally replicated the results, and EXP-001-R2 reproduced the registered behaviour on Ubuntu using repository-relative isolated outputs. The Ubuntu reproduction recorded 240/240 canonical matches with both prior collections; the four published statement-presentation differences remained visible. These results demonstrate reproducibility under the recorded conditions, not universal correctness, optimality, learning, production readiness, or external generality.

Start with the [reproducibility status](CortexMesh_v3_Planning/07_Research/REPRODUCIBILITY_STATUS.md) and the [EXP-001-R2 report](CortexMesh_v3_Planning/07_Research/RP-001/EXP-001/reproduction/EXP-001-R2/REPRODUCTION_REPORT.md).

## Current Research

- **RP-001:** the research baseline, EXP-001 characterization, internal replication, and Ubuntu reproduction are complete and preserved.
- **RP-002:** deferred pending a hypothesis that cannot be answered using the current evidence base.

Research findings are advisory evidence. They do not authorize runtime integration, provider selection, adaptive behaviour, governance changes, or modification of LOCKED components.

## Getting Started

Clone the repository and enter the project:

```bash
git clone https://github.com/saleemmsheikh-dotcom/cortexmesh.git
cd cortexmesh
```

Create an isolated environment and install the declared development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Run the complete regression suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests
```

Then read the [Foundation 1.0 baseline](CortexMesh_v3_Planning/FOUNDATION_BASELINE_v1.0.md) before proposing architectural, runtime, provider, governance, or research changes.

The repository also contains a CLI entry point:

```bash
python3 main.py "Design a simple optimisation strategy for resource allocation"
```

CLI execution may require locally configured runtime or provider dependencies. It is separate from the isolated Phase 2C reference-engine evidence.

## Documentation

- **Foundation:** [Foundation Baseline v1.0](CortexMesh_v3_Planning/FOUNDATION_BASELINE_v1.0.md)
- **Governance:** [Governance records](CortexMesh_v3_Planning/00_Governance/)
- **Architecture:** [Architecture records](CortexMesh_v3_Planning/04_Architecture/)
- **Implementation:** [Implementation execution and sealed phases](CortexMesh_v3_Planning/06_Implementation_Execution/)
- **Research:** [Research program](CortexMesh_v3_Planning/07_Research/README.md)
- **Reproducibility:** [Current reproducibility status](CortexMesh_v3_Planning/07_Research/REPRODUCIBILITY_STATUS.md)

## Current Limitations

- CortexMesh is not production-certified.
- No commercial-readiness, security-certification, reliability, scalability, or service-level claim is made.
- The Phase 2C reference orchestration engine is an isolated planning and evidence subsystem, not live runtime integration.
- RP-001 characterizes a sealed engine against a certified replay corpus; it does not prove that the engine is optimal or that its findings generalize to every environment or task.
- Local AI and provider capabilities require environment-specific configuration and validation.
- Governance is authoritative within the CortexMesh project under its ratified rules; it is advisory outside CortexMesh.
- LOCKED components remain protected and require applicable evidence and governance authorization before modification.

## License

No public license has been selected. Until an explicit license file is published, all rights remain reserved and no permission to use, copy, modify, or distribute the repository should be inferred.
