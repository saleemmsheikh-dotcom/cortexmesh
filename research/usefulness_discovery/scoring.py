EXPECTED_FAMILY = {
    "research": "Researcher",
    "engineering": "Engineer",
    "systems": "Architect",
}

COMMERCIAL_THRESHOLDS = {
    "completion_rate": 0.95,
    "specialist_fit_rate": 0.60,
    "average_authority_score": 6.0,
    "domain_coverage_rate": 1.0,
}


def score_case(case, result):
    decision = result["final"]["authority"]["decision"]
    solution = decision["solution"]
    scores = decision["scores"]
    winner = solution["agent"]
    winner_family = winner.split("_v", 1)[0]
    authority_score = scores.get("authority_total", scores.get("total", 0))

    return {
        "id": case["id"],
        "domain": case["domain"],
        "task_type": case["task_type"],
        "winner": winner,
        "winner_family": winner_family,
        "expected_family": EXPECTED_FAMILY[case["task_type"]],
        "specialist_fit": winner_family == EXPECTED_FAMILY[case["task_type"]],
        "authority_score": round(float(authority_score), 3),
    }


def summarize_scores(case_scores, crashes, domains):
    completed = len(case_scores)
    requested = completed + len(crashes)
    specialist_wins = sum(item["specialist_fit"] for item in case_scores)
    authority_total = sum(item["authority_score"] for item in case_scores)
    covered_domains = {item["domain"] for item in case_scores}
    scores = {
        "completion_rate": _ratio(completed, requested),
        "specialist_fit_rate": _ratio(specialist_wins, completed),
        "average_authority_score": round(_ratio(authority_total, completed), 3),
        "domain_coverage_rate": _ratio(len(covered_domains), len(domains)),
    }
    scores["usefulness_score"] = round(
        (
            scores["completion_rate"] * 0.25
            + scores["specialist_fit_rate"] * 0.30
            + min(scores["average_authority_score"] / 10, 1.0) * 0.35
            + scores["domain_coverage_rate"] * 0.10
        ) * 10,
        3,
    )
    return scores


def commercial_hypothesis_supported(scores):
    return all(
        scores[metric] >= threshold
        for metric, threshold in COMMERCIAL_THRESHOLDS.items()
    )


def winner_distribution(case_scores):
    distribution = {}

    for item in case_scores:
        winner = item["winner"]
        distribution[winner] = distribution.get(winner, 0) + 1

    return dict(sorted(distribution.items()))


def _ratio(numerator, denominator):
    return round(numerator / denominator, 3) if denominator else 0.0
