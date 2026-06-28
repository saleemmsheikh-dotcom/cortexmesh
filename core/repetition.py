def repetition_penalty(agent_name, memory):
    recent = [
        x["agent"]
        for x in memory.get("recent_structures", [])
    ]

    count = recent.count(agent_name)

    return count * 0.20
