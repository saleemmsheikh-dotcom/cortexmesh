FAILURE_TRAITS = {
    "repetition": "anti_repetition",
    "low_logic": "stronger_reasoning",
    "low_risk": "risk_expansion",
    "low_completeness": "coverage_expansion",
    "calibration": "confidence_reduction",
    "task_mismatch": "task_alignment"
}


def trait_for_failure(failure):
    return FAILURE_TRAITS.get(failure)
