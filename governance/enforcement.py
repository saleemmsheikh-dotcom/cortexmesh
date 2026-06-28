from governance.validator import validate_governance
from governance.freeze import record_governance_risk
from governance.tamper_log import log_governance_event, verify_tamper_log
from governance.constitution import CONSTITUTION


def record_governance_action(memory, action):
    memory.setdefault("governance_actions", [])

    if action not in memory["governance_actions"]:
        memory["governance_actions"].append(action)
        memory["governance_actions"] = memory["governance_actions"][-50:]
        return True

    return False


def quarantine_strategy(memory, family, strategy_name):
    registry = memory.get("strategy_registry", {})
    family_data = registry.get(family, {})
    strategies = family_data.get("strategies", {})

    if strategy_name in strategies:
        was_quarantined = strategies[strategy_name].get("status") == "quarantined"
        strategies[strategy_name]["status"] = "quarantined"

        action = {
            "action": "quarantine",
            "strategy": strategy_name
        }
        record_governance_action(memory, action)

        if not was_quarantined:
            log_governance_event(memory, {
                "type": "quarantine",
                "strategy": strategy_name
            })


def recover_active_strategy(memory, family):
    registry = memory.get("strategy_registry", {})
    family_data = registry.get(family, {})
    strategies = family_data.get("strategies", {})
    active = family_data.get("active")

    if active:
        active_strategy = strategies.get(active)

        if active_strategy and active_strategy.get("status") != "quarantined":
            return False

    fallback = None

    # Prefer highest legal active/promoted non-quarantined strategy.
    for name, strategy in strategies.items():
        if strategy.get("status") == "quarantined":
            continue

        if strategy.get("version", 1) > 2:
            continue

        if fallback is None:
            fallback = name
            continue

        if strategy.get("version", 1) > strategies[fallback].get("version", 1):
            fallback = name

    if fallback is None:
        family_data["active"] = None
        action_recorded = record_governance_action(memory, {
            "action": "recovery_failed",
            "family": family,
            "reason": "no legal fallback"
        })

        if action_recorded:
            record_governance_risk(memory, f"{family}: recovery_failed")

        log_governance_event(memory, {
            "type": "recovery_failed",
            "family": family
        })

        return True

    family_data["active"] = fallback
    record_governance_action(memory, {
        "action": "recover_active_strategy",
        "family": family,
        "fallback": fallback
    })
    log_governance_event(memory, {
        "type": "recovery",
        "family": family,
        "fallback": fallback
    })

    return True


def enforce_governance(memory):
    violations = validate_governance(memory)

    tamper_issues = verify_tamper_log(memory)
    if tamper_issues:
        for issue in tamper_issues:
            record_governance_risk(memory, f"tamper_{issue['error']}")

        from governance.freeze import activate_freeze
        from governance.policy import POLICY
        from governance.snapshot import restore_latest_governance_snapshot

        policy_action = POLICY.get("critical", {}).get("actions", ["freeze"])
        if "freeze" in policy_action or "freeze" in str(policy_action):
            activate_freeze(memory)

        restore_latest_governance_snapshot(memory)

        violations.extend([
            f"tamper_log:{issue['error']}"
            for issue in tamper_issues
        ])

    previous_violations = set(memory.get("governance_violations", []))

    for issue in violations:
        if "strategy overflow" in issue:
            family = issue.split(":")[0]
            _enforce_overflow_limit(memory, family)

    for issue in violations:
        if issue not in previous_violations:
            record_governance_risk(memory, issue)

    for issue in violations:
        if "strategy overflow" in issue:
            continue

        if "illegal version" not in issue:
            continue

        strategy = issue.split(":")[0]

        for family, data in memory.get("strategy_registry", {}).items():
            if strategy in data.get("strategies", {}):
                quarantine_strategy(memory, family, strategy)

    for family in memory.get("strategy_registry", {}):
        recover_active_strategy(memory, family)

    memory["governance_violations"] = violations

    return violations


def _enforce_overflow_limit(memory, family):
    max_strategies = CONSTITUTION["hard_limits"]["max_active_strategies_per_agent"]
    registry = memory.get("strategy_registry", {})
    family_data = registry.get(family, {})
    strategies = family_data.get("strategies", {})
    active = family_data.get("active")

    while _participating_count(strategies) > max_strategies:
        candidate = _overflow_quarantine_candidate(strategies, active)

        if candidate is None:
            break

        quarantine_strategy(memory, family, candidate)
        record_governance_action(memory, {
            "action": "overflow_quarantine",
            "strategy": candidate,
            "family": family
        })


def _participating_count(strategies):
    return sum(
        strategy.get("status") != "quarantined"
        for strategy in strategies.values()
    )


def _overflow_quarantine_candidate(strategies, active):
    candidates = [
        (name, strategy)
        for name, strategy in strategies.items()
        if name != active and strategy.get("status") != "quarantined"
    ]

    if not candidates:
        return None

    return sorted(
        candidates,
        key=lambda item: (
            item[1].get("version", 1),
            item[0]
        )
    )[0][0]
