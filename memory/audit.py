from governance.validator import validate_governance
from governance.tamper_log import verify_tamper_log


def build_audit_report(memory):
    report = {}

    report["runs"] = memory.get("runs", 0)
    report["role_weights"] = memory.get("role_weights", {})
    report["task_trust"] = memory.get("task_trust", {})
    report["agent_trust"] = memory.get("agent_trust", {})
    report["strategy_registry"] = memory.get("strategy_registry", {})
    report["failure_memory"] = memory.get("failure_memory", {})
    report["knowledge_memory"] = memory.get("knowledge_memory", {})
    report["negative_knowledge"] = memory.get("negative_knowledge", {})
    report["knowledge_conflicts"] = memory.get("knowledge_conflicts", [])
    report["governance_violations"] = validate_governance(memory)
    report["governance_actions"] = memory.get("governance_actions", [])
    report["governance_tamper_log"] = memory.get("governance_tamper_log", [])
    report["tamper_log_integrity"] = verify_tamper_log(memory)
    report["governance_snapshots"] = memory.get("governance_snapshots", [])
    report["governance_frozen"] = memory.get("governance_frozen", False)
    report["governance_incidents"] = memory.get("governance_incidents", 0)
    report["governance_clean_runs"] = memory.get("governance_clean_runs", 0)
    report["governance_risk_score"] = memory.get("governance_risk_score", 0)
    report["governance_risk_history"] = memory.get("governance_risk_history", [])
    report["archive_counts"] = {}

    archive = memory.get("memory_archive", {})

    for category, tasks in archive.items():
        count = 0

        for items in tasks.values():
            count += len(items)

        report["archive_counts"][category] = count

    report["evolution_events"] = memory.get("evolution_events", [])[-20:]

    return report


def print_audit_report(memory):
    report = build_audit_report(memory)

    print("\n===== CORTEXMESH AUDIT =====\n")

    print("Runs:")
    print(report["runs"])

    print("\nRole Weights:")
    print(report["role_weights"])

    print("\nTask Trust:")
    print(report["task_trust"])

    print("\nAgent Trust:")
    print(report["agent_trust"])

    print("\nStrategy Registry:")
    print(report["strategy_registry"])

    print("\nKnowledge Counts:")

    for task, lessons in report["knowledge_memory"].items():
        print(task, len(lessons))

    print("\nActive Knowledge:")
    print(report["knowledge_memory"])

    print("\nNegative Knowledge Counts:")

    for task, lessons in report["negative_knowledge"].items():
        print(task, len(lessons))

    print("\nNegative Knowledge:")
    print(report["negative_knowledge"])

    print("\nKnowledge Conflicts:")
    print(report["knowledge_conflicts"])

    print("\nFailure Memory:")
    print(report["failure_memory"])

    print("\nArchive Counts:")
    print(report["archive_counts"])

    print("\nGovernance Violations:")

    if report["governance_violations"]:
        for item in report["governance_violations"]:
            print(item)
    else:
        print("(none)")

    print("\nGovernance Actions:")

    if report["governance_actions"]:
        for action in report["governance_actions"][-20:]:
            print(action)
    else:
        print("(none)")

    print("\nGovernance Snapshots:")
    print(len(report["governance_snapshots"]))

    print("\nGovernance Freeze:")
    print(report["governance_frozen"])
    print("Incidents:", report["governance_incidents"])
    print("Clean Runs:", report["governance_clean_runs"])
    print("Governance Risk Score:", report["governance_risk_score"])

    print("Recent Risk Events:")

    if report["governance_risk_history"]:
        for event in report["governance_risk_history"][-10:]:
            print(event)
    else:
        print("(none)")

    print("\nRecent Rollback Actions:")
    rollback_actions = [
        action
        for action in report["governance_actions"]
        if action.get("action") == "rollback"
    ][-20:]

    if rollback_actions:
        for action in rollback_actions:
            print(action)
    else:
        print("(none)")

    print("\nTamper Log:")

    if report["governance_tamper_log"]:
        for event in report["governance_tamper_log"][-20:]:
            print(event)
    else:
        print("(none)")

    print("\nTamper Log Integrity:")

    if not report["tamper_log_integrity"]:
        print("(valid)")
    else:
        for issue in report["tamper_log_integrity"]:
            print(issue)

    print("\nRecent Evolution:")

    for event in report["evolution_events"]:
        print(event)
