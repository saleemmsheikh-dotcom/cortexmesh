WEIGHTS = {
    "decision_quality": 30,
    "risk_identification": 25,
    "traceability": 20,
    "actionability": 15,
    "completeness": 10,
}

SIGNALS = {
    "decision_quality": (
        "recommend",
        "select",
        "priorit",
        "trade-off",
        "objective",
        "constraint",
        "alternative",
        "compare",
    ),
    "risk_identification": (
        "risk",
        "failure",
        "edge case",
        "safeguard",
        "validate",
        "monitor",
        "dependency",
        "constraint",
    ),
    "traceability": (
        "because",
        "evidence",
        "assumption",
        "measure",
        "metric",
        "rationale",
        "feedback",
        "trade-off",
    ),
    "actionability": (
        "step",
        "implement",
        "build",
        "phase",
        "execute",
        "owner",
        "validate",
        "iterate",
    ),
    "completeness": (
        "objective",
        "alternative",
        "risk",
        "step",
        "measure",
        "monitor",
        "constraint",
        "outcome",
    ),
}


def score_blind_outputs(task, outputs):
    return {
        label: score_blind_output(task, text)
        for label, text in outputs.items()
    }


def score_blind_output(task, text):
    normalized = str(text).lower()
    task_terms = {
        word.strip(".,:;!?()[]")
        for word in str(task).lower().split()
        if len(word.strip(".,:;!?()[]")) >= 5
    }
    task_overlap = sum(term in normalized for term in task_terms)
    dimensions = {}

    for dimension, signals in SIGNALS.items():
        matched = sum(signal in normalized for signal in signals)
        score = 3.0 + min(5.0, matched * 0.9) + min(2.0, task_overlap * 0.35)
        dimensions[dimension] = round(min(10.0, score), 2)

    total = sum(
        dimensions[dimension] * weight / 10
        for dimension, weight in WEIGHTS.items()
    )
    return {
        "dimensions": dimensions,
        "weighted_total": round(total, 2),
    }
