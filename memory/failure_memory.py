def initialize_failure_memory(memory):
    if "failure_memory" not in memory:
        memory["failure_memory"] = {}

    for agent in ["Architect", "Researcher", "Engineer"]:
        memory["failure_memory"].setdefault(agent, {
            "repetition": 0,
            "calibration": 0,
            "task_mismatch": 0,
            "low_logic": 0,
            "low_risk": 0,
            "low_completeness": 0
        })


def record_failure(memory, agent, reason):
    initialize_failure_memory(memory)
    memory["failure_memory"].setdefault(agent, {
        "repetition": 0,
        "calibration": 0,
        "task_mismatch": 0,
        "low_logic": 0,
        "low_risk": 0,
        "low_completeness": 0
    })

    if reason in memory["failure_memory"][agent]:
        memory["failure_memory"][agent][reason] += 1
