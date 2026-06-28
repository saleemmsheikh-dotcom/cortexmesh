import os
from datetime import datetime, timezone
from pathlib import Path

from testing import endurance, evolution, governance, knowledge, regression
from testing.common import restore_memory, snapshot_memory, timed_battery, write_json
from testing.report import build_summary


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def run_stability_review():
    quick = os.getenv("CORTEXMESH_STABILITY_QUICK") == "1"
    counts = {
        "endurance": 20 if quick else 500,
        "evolution": 5 if quick else 100,
        "knowledge": 12 if quick else 100,
    }
    baseline = snapshot_memory()
    batteries = {}

    try:
        batteries["endurance"] = _isolated(
            baseline,
            lambda: endurance.run(count=counts["endurance"]),
        )
        batteries["evolution"] = _isolated(
            baseline,
            lambda: evolution.run(per_type=counts["evolution"]),
        )
        batteries["knowledge"] = _isolated(
            baseline,
            lambda: knowledge.run(count=counts["knowledge"]),
        )
        batteries["governance"] = _isolated(baseline, governance.run)
        batteries["regression"] = _isolated(baseline, regression.run)
    finally:
        restore_memory(baseline)

    report = {
        "version": "V6.8",
        "quick_mode": quick,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "batteries": batteries,
    }
    summary = build_summary(report)
    report["summary"] = summary
    write_json(REPORTS / "v6_8_report.json", report)
    write_json(REPORTS / "v6_8_summary.json", summary)

    return report, summary


def _isolated(baseline, fn):
    restore_memory(baseline)

    try:
        return timed_battery(fn)
    finally:
        restore_memory(baseline)
