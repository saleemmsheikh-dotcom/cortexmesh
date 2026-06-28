import json
from collections import defaultdict
from pathlib import Path

from research.usefulness_discovery.external.scoring import WEIGHTS


ROOT = Path(__file__).resolve().parents[3]
EXTERNAL_ROOT = Path(__file__).resolve().parent
BENCHMARK_REPORT = ROOT / "reports" / "external_benchmark.json"
FAILURE_REPORT = ROOT / "reports" / "failure_analysis.json"
REVIEWS_DIR = EXTERNAL_ROOT / "blind_reviews"
SCORES_DIR = EXTERNAL_ROOT / "scores"

HYPOTHESES = {
    "decision_quality": (
        "CortexMesh outputs do not make and justify a sufficiently explicit decision."
    ),
    "risk_identification": (
        "CortexMesh outputs under-identify risks, failure modes, and safeguards."
    ),
    "traceability": (
        "CortexMesh outputs provide insufficient rationale, assumptions, and measurable evidence."
    ),
    "actionability": (
        "CortexMesh outputs are less actionable than the strongest baseline."
    ),
    "completeness": (
        "CortexMesh outputs omit important decision components covered by the strongest baseline."
    ),
}

RECOMMENDATIONS = {
    "decision_quality": (
        "Require the final Authority output to state one recommendation, rejected alternatives, "
        "trade-offs, and the decision rationale."
    ),
    "risk_identification": (
        "Add a mandatory final risk section covering failure modes, edge cases, safeguards, "
        "and validation checks."
    ),
    "traceability": (
        "Require final outputs to expose assumptions, evidence, metrics, and reasoning links "
        "from task constraints to recommendation."
    ),
    "actionability": (
        "Require final outputs to include ordered implementation steps, owners, validation, "
        "and measurable next actions."
    ),
    "completeness": (
        "Add a final synthesis pass that checks objectives, alternatives, risks, execution, "
        "and measurement before returning the answer."
    ),
}


def run_failure_analysis():
    if not BENCHMARK_REPORT.exists():
        return _inconclusive("Run external_benchmark before failure_analysis.")

    benchmark = json.loads(BENCHMARK_REPORT.read_text())
    completed = [
        item
        for item in benchmark.get("case_results", [])
        if "scores_by_source" in item
    ]

    if not completed:
        return _inconclusive("No completed external benchmark cases were found.")

    dimension_gaps = defaultdict(list)
    case_diagnostics = []

    for case in completed:
        diagnostic = _analyze_case(case)

        if diagnostic is None:
            continue

        case_diagnostics.append(diagnostic)

        for dimension, gap in diagnostic["weighted_dimension_gaps"].items():
            dimension_gaps[dimension].append(gap)

    if not case_diagnostics:
        return _inconclusive("Blind review artifacts are incomplete.")

    average_gaps = {
        dimension: sum(gaps) / len(gaps)
        for dimension, gaps in dimension_gaps.items()
    }
    primary = max(average_gaps, key=average_gaps.get)
    supporting = sum(
        item["weighted_dimension_gaps"][primary] > 0
        for item in case_diagnostics
    )
    support_rate = supporting / len(case_diagnostics)
    confidence = (
        "high"
        if support_rate >= 0.70
        else "medium"
        if support_rate >= 0.40
        else "low"
    )
    result = {
        "cases_analyzed": len(case_diagnostics),
        "primary_failure_hypothesis": HYPOTHESES[primary],
        "supporting_cases": supporting,
        "confidence": confidence,
        "recommended_action": RECOMMENDATIONS[primary],
    }
    detailed = {
        **result,
        "primary_dimension": primary,
        "support_rate": round(support_rate, 3),
        "average_weighted_dimension_gaps": {
            key: round(value, 3)
            for key, value in sorted(average_gaps.items())
        },
        "case_diagnostics": case_diagnostics,
    }
    FAILURE_REPORT.parent.mkdir(parents=True, exist_ok=True)
    FAILURE_REPORT.write_text(json.dumps(detailed, indent=2, sort_keys=True))
    return result


def _analyze_case(case):
    case_name = f"case_{case['id']:02d}.json"
    review_path = REVIEWS_DIR / case_name
    score_path = SCORES_DIR / case_name

    if not review_path.exists() or not score_path.exists():
        return None

    reviews = json.loads(review_path.read_text())["reviews"]
    score_map = json.loads(score_path.read_text())
    source_by_label = score_map["source_by_label"]
    cortex_label = _label_for_source(source_by_label, "cortexmesh")
    baseline_source = max(
        (
            source
            for source in score_map["scores_by_source"]
            if source != "cortexmesh"
        ),
        key=score_map["scores_by_source"].get,
    )
    baseline_label = _label_for_source(source_by_label, baseline_source)
    cortex_dimensions = reviews[cortex_label]["dimensions"]
    baseline_dimensions = reviews[baseline_label]["dimensions"]
    weighted_gaps = {
        dimension: round(
            (baseline_dimensions[dimension] - cortex_dimensions[dimension])
            * weight
            / 10,
            3,
        )
        for dimension, weight in WEIGHTS.items()
    }
    return {
        "id": case["id"],
        "domain": case["domain"],
        "best_baseline": baseline_source,
        "cortexmesh_total": score_map["scores_by_source"]["cortexmesh"],
        "baseline_total": score_map["scores_by_source"][baseline_source],
        "weighted_dimension_gaps": weighted_gaps,
    }


def _label_for_source(source_by_label, target):
    return next(
        label
        for label, source in source_by_label.items()
        if source == target
    )


def _inconclusive(action):
    return {
        "cases_analyzed": 0,
        "primary_failure_hypothesis": "Insufficient benchmark evidence.",
        "supporting_cases": 0,
        "confidence": "low",
        "recommended_action": action,
    }
