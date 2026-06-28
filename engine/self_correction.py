def dominant_failure(memory, agent):
    failures = memory.get("failure_memory", {}).get(agent, {})

    if not failures:
        return None

    return max(failures, key=failures.get)


def correction_hint(memory, agent):
    reason = dominant_failure(memory, agent)

    if reason == "repetition":
        return "Avoid repeating the same structure. Add a different angle or method."

    if reason == "calibration":
        return "Reduce confidence unless the solution directly matches the task."

    if reason == "task_mismatch":
        return "Align more closely with the task type and expected specialist role."

    if reason == "low_logic":
        return "Strengthen reasoning structure and assumptions."

    if reason == "low_risk":
        return "Add risks, edge cases, failure modes, and safeguards."

    if reason == "low_completeness":
        return "Add missing coverage, alternatives, and edge cases."

    return None
