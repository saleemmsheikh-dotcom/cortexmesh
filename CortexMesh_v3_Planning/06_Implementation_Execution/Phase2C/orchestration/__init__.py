"""Phase 2C orchestration reference components.

These modules are planning-stage reference implementations, not runtime
orchestrator integration.
"""

from .agent_planner import AgentDescriptor, AgentPlan, AgentPlanner, AgentRequirement
from .execution_plan import ExecutionDependency, ExecutionPlan, ExecutionPlanner, ExecutionStep
from .evidence import EvidenceBundle, EvidenceCollector, EvidenceRecord, EvidenceSource
from .consensus import (
    AgreementSignal,
    ConsensusAssessment,
    ConsensusEvaluator,
    ConsensusInput,
    ConsensusPolicy,
    DivergenceSignal,
)
from .synthesis import (
    EvidenceSynthesizer,
    SynthesisInput,
    SynthesisPolicy,
    SynthesisResult,
    SynthesisSection,
)
from .engine import OrchestrationContext, OrchestrationEngine, OrchestrationRequest, OrchestrationResult

__all__ = [
    "AgentDescriptor",
    "AgentPlan",
    "AgentPlanner",
    "AgentRequirement",
    "ExecutionDependency",
    "ExecutionPlan",
    "ExecutionPlanner",
    "ExecutionStep",
    "EvidenceBundle",
    "EvidenceCollector",
    "EvidenceRecord",
    "EvidenceSource",
    "AgreementSignal",
    "ConsensusAssessment",
    "ConsensusEvaluator",
    "ConsensusInput",
    "ConsensusPolicy",
    "DivergenceSignal",
    "EvidenceSynthesizer",
    "SynthesisInput",
    "SynthesisPolicy",
    "SynthesisResult",
    "SynthesisSection",
    "OrchestrationContext",
    "OrchestrationEngine",
    "OrchestrationRequest",
    "OrchestrationResult",
]
