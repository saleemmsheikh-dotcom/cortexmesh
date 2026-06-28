def determine_failure_reason(score_data):
    if score_data.get("repetition_penalty", 0) > 1:
        return "repetition"

    if score_data.get("calibration", 1.0) < 0.95:
        return "calibration"

    if score_data["logic"] < 5:
        return "low_logic"

    if score_data["risk"] < 5:
        return "low_risk"

    if score_data["completeness"] < 5:
        return "low_completeness"

    return "task_mismatch"
