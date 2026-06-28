PASS_THRESHOLDS = {
    "crashes": 0,
    "illegal_v3_strategies": 0,
    "quarantine_bypasses": 0,
    "tamper_bypasses": 0,
    "freeze_lockups": 0,
    "unbounded_memory_growth": False,
    "specialist_win_rate_minimum": 0.60,
    "bad_lessons_remaining": 0,
    "regression_pass_rate": 1.0,
    "rollback_success_rate": 1.0,
    "memory_recovery_success_rate": 1.0,
    "audit_integrity_failures": 0,
}


def build_summary(report):
    batteries = report["batteries"]
    crashes = sum(len(item.get("crashes", [])) for item in batteries.values())
    endurance = batteries["endurance"]
    evolution = batteries["evolution"]
    knowledge = batteries["knowledge"]
    governance = batteries["governance"]
    regression = batteries["regression"]
    specialist_min = min(
        list(endurance["specialist_win_rates"].values())
        + list(evolution["specialist_win_rates"].values())
        + list(regression["specialist_win_rates"].values())
    )
    metrics = {
        "crashes": crashes,
        "illegal_v3_strategies": max(
            endurance["illegal_v3_strategies"],
            evolution["illegal_v3_strategies"],
        ),
        "quarantine_bypasses": governance["quarantine_bypasses"],
        "tamper_bypasses": governance["tamper_bypasses"],
        "freeze_lockups": governance["freeze_lockups"],
        "unbounded_memory_growth": (
            endurance["memory_bytes_growth"]
            > max(250000, endurance["memory_bytes_start"] * 2)
        ),
        "specialist_win_rate_minimum": specialist_min,
        "bad_lessons_remaining": knowledge["bad_lessons_remaining"],
        "regression_pass_rate": regression["regression_pass_rate"],
        "rollback_success_rate": governance["rollback_success_rate"],
        "memory_recovery_success_rate": governance["memory_recovery_success_rate"],
        "audit_integrity_failures": governance["audit_integrity_failures"],
    }
    failures = []

    for key, expected in PASS_THRESHOLDS.items():
        actual = metrics[key]

        if key == "specialist_win_rate_minimum":
            passed = actual >= expected
        else:
            passed = actual == expected

        if not passed:
            failures.append({
                "metric": key,
                "expected": expected,
                "actual": actual,
            })

    return {
        "status": "PASS" if not failures else "FAIL",
        "metrics": metrics,
        "thresholds": PASS_THRESHOLDS,
        "failures": failures,
    }


def print_summary(summary):
    print("\n===== CORTEXMESH V6.8 STABILITY REVIEW =====\n")
    print("Status:", summary["status"])
    print("\nMetrics:")

    for key, value in summary["metrics"].items():
        print(f"{key}: {value}")

    print("\nFailures:")

    if summary["failures"]:
        for failure in summary["failures"]:
            print(failure)
    else:
        print("(none)")
