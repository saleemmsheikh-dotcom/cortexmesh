RISK_LOW = "low"
RISK_MEDIUM = "medium"
RISK_HIGH = "high"
RISK_CRITICAL = "critical"


def classify_violation(issue):
    text = str(issue).lower()

    if "illegal version" in text:
        return RISK_MEDIUM

    if "strategy overflow" in text:
        return RISK_LOW

    if "recovery_failed" in text:
        return RISK_HIGH

    if "hash_mismatch" in text or "prev_hash_mismatch" in text:
        return RISK_CRITICAL

    return RISK_LOW
