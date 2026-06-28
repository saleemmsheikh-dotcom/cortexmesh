def log_confidence(memory, agent, confidence, won):
    if "confidence_history" not in memory:
        memory["confidence_history"] = {}

    if agent not in memory["confidence_history"]:
        memory["confidence_history"][agent] = []

    memory["confidence_history"][agent].append({
        "confidence": confidence,
        "won": won
    })

    memory["confidence_history"][agent] = memory["confidence_history"][agent][-50:]


def calibration_score(memory, agent):
    history = memory.get("confidence_history", {}).get(agent, [])

    if not history:
        return 1.0

    error = 0

    for h in history:
        expected = h["confidence"]
        actual = 1.0 if h["won"] else 0.0
        error += abs(expected - actual)

    avg_error = error / len(history)

    return max(0.8, min(1.2, 1.0 + (0.5 - avg_error)))
