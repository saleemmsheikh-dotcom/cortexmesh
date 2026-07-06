"""SAFE Local AI bridge for non-LOCKED local solver integration."""

from __future__ import annotations

import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path


PHASE1B_PATH = (
    Path(__file__).resolve().parents[1]
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase1B"
)


@dataclass(frozen=True)
class LocalAISolverConfig:
    enabled: bool
    provider: str
    base_url: str
    model: str
    timeout_seconds: float
    temperature: float
    max_tokens: int


def load_local_ai_solver_config() -> LocalAISolverConfig:
    """Load explicit Local AI solver configuration from environment."""

    return LocalAISolverConfig(
        enabled=os.getenv("CORTEX_LOCAL_AI_ENABLED", "").lower() in {"1", "true", "yes"},
        provider=os.getenv("CORTEX_LOCAL_AI_PROVIDER", "ollama"),
        base_url=os.getenv("CORTEX_LOCAL_AI_BASE_URL", "http://localhost:11434"),
        model=os.getenv("CORTEX_LOCAL_AI_MODEL", "qwen2.5-coder:7b"),
        timeout_seconds=float(os.getenv("CORTEX_LOCAL_AI_TIMEOUT", "60")),
        temperature=float(os.getenv("CORTEX_LOCAL_AI_TEMPERATURE", "0")),
        max_tokens=int(os.getenv("CORTEX_LOCAL_AI_MAX_TOKENS", "256")),
    )


def local_ai_enabled() -> bool:
    return load_local_ai_solver_config().enabled


def generate_local_solution(agent_name: str, role: str, base_agent: str, task: str):
    """Generate a solver response through the Phase 1B provider abstraction."""

    config = load_local_ai_solver_config()
    if not config.enabled:
        return None

    _ensure_phase1b_import_path()
    from local_ai import LocalAIConfig, LocalAIRequest, OllamaProvider

    if config.provider != "ollama":
        raise ValueError(f"unsupported Local AI provider for Phase 1B solver: {config.provider}")

    provider = OllamaProvider()
    local_config = LocalAIConfig(
        provider=config.provider,
        base_url=config.base_url,
        model=config.model,
        timeout_seconds=config.timeout_seconds,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        metadata={"integration_path": "agents.local_solver"},
    )
    request_id = _request_id(agent_name, role, task)
    request = LocalAIRequest(
        prompt=_task_prompt(role, task),
        model=config.model,
        request_id=request_id,
        objective_ref="PHASE1B-SAFE-LOCAL-SOLVER",
        system_prompt=_system_prompt(agent_name, role, base_agent),
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        timeout_seconds=config.timeout_seconds,
        metadata={"agent": agent_name, "role": role, "base_agent": base_agent},
    )
    response = provider.generate(request, local_config)
    return {
        "solution": response.content,
        "provenance": {
            "provider": response.provider,
            "model": response.model,
            "request_id": response.request_id,
            "objective_ref": request.objective_ref,
            "endpoint_ref": response.diagnostics.get("endpoint_ref"),
            "status": response.status,
            "latency_ms": response.latency_ms,
            "finish_reason": response.finish_reason,
            "authoritative": False,
            "confidence_source": "static_local_solver_default",
            "integration_path": "agents.local_solver",
        },
    }


def _ensure_phase1b_import_path() -> None:
    phase1b = str(PHASE1B_PATH)
    if phase1b not in sys.path:
        sys.path.insert(0, phase1b)


def _request_id(agent_name: str, role: str, task: str) -> str:
    digest = hashlib.sha256(
        f"{agent_name}\n{role}\n{task}".encode("utf-8")
    ).hexdigest()[:12]
    return f"PHASE1B-LSOL-{digest}"


def _system_prompt(agent_name: str, role: str, base_agent: str) -> str:
    return (
        f"You are {agent_name}, a CortexMesh local solver.\n"
        f"Role: {role}.\n"
        f"Base agent: {base_agent}.\n"
        "Return a concise solution candidate only. "
        "Do not claim authority, confidence, ranking, voting weight, or governance status."
    )


def _task_prompt(role: str, task: str) -> str:
    return (
        f"Produce a {role} solution candidate for this task.\n\n"
        f"Task:\n{str(task).strip()}"
    )
