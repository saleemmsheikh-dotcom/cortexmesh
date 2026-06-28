import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "reports" / "usefulness_discovery.json"


def build_report(cases, case_scores, crashes, scores, winner_distribution, supported):
    return {
        "cases_run": len(cases),
        "domains": sorted({case["domain"] for case in cases}),
        "scores": scores,
        "winner_distribution": winner_distribution,
        "commercial_hypothesis_supported": supported,
        "crashes": crashes,
        "case_results": case_scores,
    }


def public_summary(report):
    return {
        "cases_run": report["cases_run"],
        "domains": report["domains"],
        "scores": report["scores"],
        "winner_distribution": report["winner_distribution"],
        "commercial_hypothesis_supported": report["commercial_hypothesis_supported"],
    }


def save_report(report):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True))
