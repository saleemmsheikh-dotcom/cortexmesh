POLICY = {
    "low": {
        "actions": ["log"]
    },
    "medium": {
        "actions": ["quarantine"]
    },
    "high": {
        "actions": ["rollback"]
    },
    "critical": {
        "actions": ["freeze", "rollback"]
    }
}


def policy_actions(risk):
    return POLICY.get(risk, POLICY["low"])["actions"]


def execute_policy(memory, issue, risk):
    executed = [
        execute_action(memory, issue, action)
        for action in policy_actions(risk)
    ]

    return executed


def execute_action(memory, issue, action):
    if action == "log":
        memory.setdefault("governance_actions", []).append({
            "action": "log",
            "issue": str(issue)
        })
        memory["governance_actions"] = memory["governance_actions"][-50:]
        return "log"

    if action == "quarantine":
        strategy_name = str(issue).split(":", 1)[0]

        from governance.enforcement import quarantine_strategy

        for family, data in memory.get("strategy_registry", {}).items():
            if strategy_name in data.get("strategies", {}):
                quarantine_strategy(memory, family, strategy_name)
                return "quarantine"

        return "quarantine_failed"

    if action == "rollback":
        from governance.snapshot import restore_latest_governance_snapshot

        if restore_latest_governance_snapshot(memory):
            return "rollback"

        return "rollback_failed"

    if action == "freeze":
        from governance.freeze import activate_freeze

        activate_freeze(memory)
        return "freeze"

    return "none"
