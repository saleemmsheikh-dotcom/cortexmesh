from datetime import datetime, timezone


FREEZE_THRESHOLD = 3
CLEAN_RUNS_TO_RELEASE = 5
RISK_FREEZE_THRESHOLD = 10
RISK_POINTS = {
    "low": 1,
    "medium": 2,
    "high": 4,
    "critical": 8,
}


def record_governance_risk(memory, issue):
    from governance.policy import execute_policy, policy_actions
    from governance.risk import classify_violation

    risk = classify_violation(issue)
    points = RISK_POINTS[risk]
    memory["governance_risk_score"] = (
        memory.get("governance_risk_score", 0)
        + points
    )
    event = {
        "issue": str(issue),
        "risk": risk,
        "points": points,
        "policy_actions": policy_actions(risk)
    }
    event["actions_executed"] = execute_policy(memory, issue, risk)
    memory.setdefault("governance_risk_history", []).append(event)
    memory["governance_risk_history"] = memory["governance_risk_history"][-100:]
    memory["governance_incidents"] = memory.get("governance_incidents", 0) + 1
    memory["governance_clean_runs"] = 0

    if memory["governance_risk_score"] >= RISK_FREEZE_THRESHOLD:
        activate_freeze(memory)

    return event


def activate_freeze(memory):
    if memory.get("governance_frozen"):
        return

    memory["governance_frozen"] = True
    memory.setdefault("governance_actions", []).append({
        "action": "freeze",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


def clear_governance_incidents(memory):
    memory["governance_incidents"] = 0


def release_freeze(memory):
    if not memory.get("governance_frozen"):
        return

    memory["governance_frozen"] = False
    memory.setdefault("governance_actions", []).append({
        "action": "unfreeze",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


def update_governance_stability(memory, violations):
    if violations:
        memory["governance_clean_runs"] = 0
        return

    memory["governance_clean_runs"] = memory.get("governance_clean_runs", 0) + 1
    memory["governance_risk_score"] = memory.get("governance_risk_score", 0) * 0.8

    if (
        memory.get("governance_frozen")
        and memory["governance_clean_runs"] >= CLEAN_RUNS_TO_RELEASE
    ):
        release_freeze(memory)
        clear_governance_incidents(memory)
