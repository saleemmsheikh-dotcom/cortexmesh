import json
import os
import tempfile
from pathlib import Path

from evolution.strategy_registry import default_registry, ensure_strategy_registry
from governance.tamper_log import log_governance_event


MEMORY_PATH = Path(__file__).parent / "memory.json"


def _default_memory():
    return {
        "runs": 0,
        "agent_wins": {},
        "agent_usage": {},
        "authority_actions": {},
        "conflicts_detected": 0,
        "conflicts_resolved": 0,
        "recent_structures": [],
        "role_weights": {
            "Architect": 1.0,
            "Researcher": 1.0,
            "Engineer": 1.0,
        },
        "strategy_registry": default_registry(),
        "strategy_scores": {},
        "task_trust": {},
        "agent_trust": {},
        "confidence_history": {},
        "knowledge_memory": {},
        "negative_knowledge": {},
        "knowledge_conflicts": [],
        "failure_memory": {},
        "evolution_events": [],
        "entropy_target": 0.5,
        "entropy_drift": 0.1,
        "governance_frozen": False,
        "governance_violations": [],
        "governance_actions": [],
        "governance_snapshots": [],
        "governance_tamper_log": [],
        "governance_tamper_anchor": None,
        "governance_incidents": 0,
        "governance_clean_runs": 0,
        "governance_risk_score": 0.0,
        "governance_risk_history": [],
    }


def _normalize_types(memory):
    runs = memory.get("runs", 0)

    if not isinstance(runs, int):
        try:
            memory["runs"] = int(runs or 0)
        except (TypeError, ValueError):
            memory["runs"] = 0

    if not isinstance(memory.get("role_weights"), dict):
        memory["role_weights"] = _default_memory()["role_weights"].copy()

    if not isinstance(memory.get("agent_wins"), dict):
        memory["agent_wins"] = {}

    if not isinstance(memory.get("agent_usage"), dict):
        memory["agent_usage"] = {}

    if not isinstance(memory.get("governance_actions"), list):
        memory["governance_actions"] = []

    return memory


def _ensure_schema(memory):
    defaults = _default_memory()

    for key, value in defaults.items():
        memory.setdefault(key, value if not isinstance(value, dict) else value.copy())

    memory = _normalize_types(memory)
    ensure_strategy_registry(memory)

    return memory


def _recover_from_backup():
    backup_path = MEMORY_PATH.with_suffix(".json.bak")

    if backup_path.exists():
        try:
            with open(backup_path, "r", encoding="utf-8") as handle:
                return _ensure_schema(json.load(handle))
        except (json.JSONDecodeError, OSError):
            pass

    return _default_memory()


def load_memory():
    if not MEMORY_PATH.exists():
        memory = _default_memory()
        save_memory(memory)
        return memory

    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as handle:
            return _ensure_schema(json.load(handle))
    except json.JSONDecodeError:
        recovered = _recover_from_backup()
        save_memory(recovered)
        return recovered


def save_memory(memory):
    memory = _ensure_schema(memory)
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    previous = None

    if MEMORY_PATH.exists():
        try:
            with open(MEMORY_PATH, "r", encoding="utf-8") as handle:
                previous = json.load(handle)
        except (json.JSONDecodeError, OSError):
            previous = None

    fd, temp_name = tempfile.mkstemp(
        suffix=".json",
        dir=str(MEMORY_PATH.parent),
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(memory, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())

        if previous is not None:
            previous_canonical = json.dumps(previous, sort_keys=True)
            current_canonical = json.dumps(memory, sort_keys=True)

            if previous_canonical != current_canonical:
                log_governance_event(memory, {
                    "type": "memory_persist",
                    "detail": "memory.json updated",
                })

        backup_path = MEMORY_PATH.with_suffix(".json.bak")
        if MEMORY_PATH.exists():
            MEMORY_PATH.replace(backup_path)

        Path(temp_name).replace(MEMORY_PATH)
    except OSError:
        Path(temp_name).unlink(missing_ok=True)
        raise


def update_run(memory, result):
    memory["runs"] += 1

    winner = result.get("agent")
    if winner:
        memory["agent_wins"][winner] = memory["agent_wins"].get(winner, 0) + 1

    auth = result.get("authority_action")
    if auth:
        memory["authority_actions"][auth] = memory["authority_actions"].get(auth, 0) + 1

    if result.get("conflict_detected"):
        memory["conflicts_detected"] += 1

    if result.get("conflict_resolved"):
        memory["conflicts_resolved"] += 1


def update_reputation(memory, final_decision):
    winner = final_decision.get("decision", {}).get("solution", {}).get("agent")

    if not winner:
        return

    memory["agent_wins"][winner] = memory["agent_wins"].get(winner, 0) + 1


def apply_decay(agent_wins, decay=0.98):
    for key in list(agent_wins.keys()):
        agent_wins[key] *= decay

    return agent_wins


def system_entropy(memory):
    recent = memory.get("recent_structures", [])[-10:]
    agents = [entry["agent"] for entry in recent]

    unique = len(set(agents))
    return unique / max(len(agents), 1)


def build_report(memory):
    return {
        "runs": memory["runs"],
        "agent_wins": memory["agent_wins"],
        "agent_usage": memory["agent_usage"],
        "authority_actions": memory["authority_actions"],
        "conflicts_detected": memory["conflicts_detected"],
        "conflicts_resolved": memory["conflicts_resolved"],
        "recent_structures": memory["recent_structures"],
        "role_weights": memory["role_weights"],
    }
