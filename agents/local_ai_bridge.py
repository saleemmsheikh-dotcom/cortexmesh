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
    provider_options: tuple[str, ...]
    base_url: str
    model: str
    timeout_seconds: float
    temperature: float
    max_tokens: int


def load_local_ai_solver_config() -> LocalAISolverConfig:
    """Load explicit Local AI solver configuration from environment."""

    return LocalAISolverConfig(
        enabled=os.getenv("CORTEX_LOCAL_AI_ENABLED", "").lower() in {"1", "true", "yes"},
        provider=os.getenv("CORTEX_LOCAL_AI_PROVIDER", "ollama").strip().lower(),
        provider_options=tuple(
            item.strip().lower()
            for item in os.getenv("CORTEX_LOCAL_AI_PROVIDER_OPTIONS", "ollama").split(",")
            if item.strip()
        ),
        base_url=os.getenv("CORTEX_LOCAL_AI_BASE_URL", ""),
        model=os.getenv("CORTEX_LOCAL_AI_MODEL", ""),
        timeout_seconds=float(os.getenv("CORTEX_LOCAL_AI_TIMEOUT", "60")),
        temperature=float(os.getenv("CORTEX_LOCAL_AI_TEMPERATURE", "0")),
        max_tokens=int(os.getenv("CORTEX_LOCAL_AI_MAX_TOKENS", "256")),
    )


def local_ai_enabled() -> bool:
    return load_local_ai_solver_config().enabled


def generate_local_solution(agent_name: str, role: str, base_agent: str, task: str):
    """Generate a solver response through the Local AI manager boundary."""

    config = load_local_ai_solver_config()
    if not config.enabled:
        return None

    _ensure_phase1b_import_path()
    from local_ai import LocalAIManager, LocalAIRequest

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
    manager = LocalAIManager(_manager_settings(config))
    result = manager.generate(request)
    provenance = {
        **dict(result.provenance),
        "objective_ref": request.objective_ref,
        "authoritative": False,
        "confidence_source": "static_local_solver_default",
        "integration_path": "agents.local_solver",
    }
    return {
        "solution": result.response.content,
        "provenance": provenance,
    }


def _manager_settings(config: LocalAISolverConfig):
    from local_ai import LocalAIManagerSettings

    return LocalAIManagerSettings(
        enabled=config.enabled,
        provider=config.provider,
        provider_options=config.provider_options,
        base_url=config.base_url,
        model=config.model,
        timeout_seconds=config.timeout_seconds,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        metadata={
            "integration_path": "agents.local_solver",
            "provider_selection": config.provider,
            "provider_options": list(config.provider_options),
        },
    )


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
