import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORT_PATH = ROOT / "reports" / "external_benchmark.json"


def build_external_report(case_results):
    completed = [item for item in case_results if "scores_by_source" in item]
    wins = Counter()
    domain_advantages = defaultdict(list)

    for item in completed:
        source_scores = item["scores_by_source"]
        top_score = max(source_scores.values())
        winners = [
            source
            for source, score in source_scores.items()
            if score == top_score
        ]

        for winner in winners:
            wins[winner] += 1 / len(winners)

        baseline_best = max(
            score
            for source, score in source_scores.items()
            if source != "cortexmesh"
        )
        advantage = (
            (source_scores["cortexmesh"] - baseline_best) / baseline_best
            if baseline_best
            else 0.0
        )
        domain_advantages[item["domain"]].append(advantage)

    count = len(completed)
    win_rate = wins["cortexmesh"] / count if count else 0.0
    average_advantages = {
        domain: sum(values) / len(values)
        for domain, values in domain_advantages.items()
    }
    best_domain = (
        max(average_advantages, key=average_advantages.get)
        if average_advantages
        else None
    )
    best_advantage = average_advantages.get(best_domain, 0.0)

    if count < 20:
        status = "inconclusive"
    elif win_rate >= 0.70 or best_advantage >= 0.10:
        status = "supported"
    else:
        status = "not_supported"

    return {
        "cases_run": count,
        "blind_scoring": True,
        "cortexmesh_win_rate": round(win_rate, 3),
        "average_score_advantage": round(best_advantage, 3),
        "best_domain": best_domain,
        "commercial_hypothesis_status": status,
        "winner_distribution": {
            source: round(value, 3)
            for source, value in sorted(wins.items())
        },
        "domain_score_advantages": {
            domain: round(value, 3)
            for domain, value in sorted(average_advantages.items())
        },
        "case_results": case_results,
    }


def public_summary(report):
    return {
        "cases_run": report["cases_run"],
        "blind_scoring": report["blind_scoring"],
        "cortexmesh_win_rate": report["cortexmesh_win_rate"],
        "average_score_advantage": report["average_score_advantage"],
        "best_domain": report["best_domain"],
        "commercial_hypothesis_status": report["commercial_hypothesis_status"],
    }


def save_external_report(report, patch=None):
    path = (
        ROOT / "reports" / f"external_benchmark_{patch}.json"
        if patch
        else REPORT_PATH
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True))
