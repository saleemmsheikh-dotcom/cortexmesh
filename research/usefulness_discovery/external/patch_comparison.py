import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = ROOT / "reports" / "external_benchmark.json"
PATCHED_PATH = ROOT / "reports" / "external_benchmark_risk_section.json"
COMPARISON_PATH = ROOT / "reports" / "risk_section_patch_comparison.json"

MEANINGFUL_GAP_REDUCTION = 0.05


def compare_risk_section_patch():
    if not BASELINE_PATH.exists() or not PATCHED_PATH.exists():
        return {
            "baseline": None,
            "patched": None,
            "effect": None,
            "patch_status": "inconclusive",
        }

    baseline_report = json.loads(BASELINE_PATH.read_text())
    patched_report = json.loads(PATCHED_PATH.read_text())
    baseline = _metrics(baseline_report)
    patched = _metrics(patched_report)
    win_delta = patched["cortexmesh_win_rate"] - baseline["cortexmesh_win_rate"]
    advantage_delta = (
        patched["average_score_advantage"]
        - baseline["average_score_advantage"]
    )

    if win_delta > 0 or advantage_delta >= MEANINGFUL_GAP_REDUCTION:
        status = "supported"
    elif win_delta < 0 or advantage_delta < 0:
        status = "not_supported"
    else:
        status = "inconclusive"

    result = {
        "baseline": baseline,
        "patched": patched,
        "effect": {
            "win_rate_delta": round(win_delta, 3),
            "score_advantage_delta": round(advantage_delta, 3),
        },
        "patch_status": status,
    }
    COMPARISON_PATH.parent.mkdir(parents=True, exist_ok=True)
    COMPARISON_PATH.write_text(json.dumps(result, indent=2, sort_keys=True))
    return result


def _metrics(report):
    return {
        "cortexmesh_win_rate": report["cortexmesh_win_rate"],
        "average_score_advantage": report["average_score_advantage"],
    }
