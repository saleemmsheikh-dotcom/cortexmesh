import json
from pathlib import Path


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
            "Engineer": 1.0
        }
    }


def _ensure_schema(memory):
    defaults = _default_memory()

    for key, value in defaults.items():
        memory.setdefault(key, value)

    return memory


def load_memory():
    if not MEMORY_PATH.exists():
        memory = _default_memory()
        save_memory(memory)
        return memory

    with open(MEMORY_PATH, "r") as f:
        return _ensure_schema(json.load(f))


def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


def update_run(memory, result):
    memory["runs"] += 1

    # agent wins
    winner = result.get("agent")
    if winner:
        memory["agent_wins"][winner] = memory["agent_wins"].get(winner, 0) + 1

    # authority action (if exists)
    auth = result.get("authority_action")
    if auth:
        memory["authority_actions"][auth] = memory["authority_actions"].get(auth, 0) + 1

    # conflicts
    if result.get("conflict_detected"):
        memory["conflicts_detected"] += 1

    if result.get("conflict_resolved"):
        memory["conflicts_resolved"] += 1


def update_reputation(memory, final_decision):
    winner = final_decision.get("decision", {}).get("solution", {}).get("agent")

    if not winner:
        return

    if winner not in memory["agent_wins"]:
        memory["agent_wins"][winner] = 0

    memory["agent_wins"][winner] += 1


def apply_decay(agent_wins, decay=0.98):
    for k in list(agent_wins.keys()):
        agent_wins[k] *= decay

    return agent_wins


def system_entropy(memory):
    recent = memory.get("recent_structures", [])[-10:]
    agents = [x["agent"] for x in recent]
    
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
        "role_weights": memory["role_weights"]
    }
