from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from orchestrator import orchestrate
from memory.memory_store import (
    load_memory,
    save_memory,
    update_run,
    update_reputation,
    apply_decay,
    build_report,
)

def run_task(task):
    task = str(task).strip()
    if not task:
        raise ValueError("Task cannot be empty.")

    memory = load_memory()

    result = orchestrate(task, memory=memory)

    # attach memory signals (minimal instrumentation)
    memory_event = {
        "agent": result.get("final", {}).get("agent"),
        "authority_action": result.get("authority", {}).get("action") if "authority" in result else None,
        "conflict_detected": result.get("conflict_mode", False),
        "conflict_resolved": result.get("conflict_resolved", False)
    }

    update_run(memory, memory_event)
    update_reputation(memory, result.get("authority", {}))
    memory["agent_wins"] = apply_decay(memory["agent_wins"])
    save_memory(memory)

    report = build_report(memory)

    return {
        "final": result,
        "memory": report
    }


if __name__ == "__main__":
    print(run_task("Design a simple optimisation strategy for resource allocation"))
