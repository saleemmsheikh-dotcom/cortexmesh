import contextlib
import io
import random

from engine.runner import run_task
from research.usefulness_discovery.report import build_report, public_summary, save_report
from research.usefulness_discovery.scoring import (
    commercial_hypothesis_supported,
    score_case,
    summarize_scores,
    winner_distribution,
)
from testing.common import restore_memory, snapshot_memory


CASES = [
    {"domain": "cloud_finops", "task_type": "research", "task": "Compare approaches to reducing cloud infrastructure costs"},
    {"domain": "cloud_finops", "task_type": "engineering", "task": "Implement a practical cloud cost optimisation script"},
    {"domain": "cloud_finops", "task_type": "systems", "task": "Design a resilient cloud cost optimisation architecture"},
    {"domain": "software_delivery", "task_type": "research", "task": "Analyze methods for reducing software delivery risk"},
    {"domain": "software_delivery", "task_type": "engineering", "task": "Build an automated deployment validation utility"},
    {"domain": "software_delivery", "task_type": "systems", "task": "Design a reliable continuous delivery system architecture"},
    {"domain": "data_platform", "task_type": "research", "task": "Compare alternatives for improving database performance"},
    {"domain": "data_platform", "task_type": "engineering", "task": "Implement a reliable database backup utility"},
    {"domain": "data_platform", "task_type": "systems", "task": "Design a stable data ingestion architecture"},
    {"domain": "cybersecurity", "task_type": "research", "task": "Research approaches for reducing identity security risk"},
    {"domain": "cybersecurity", "task_type": "engineering", "task": "Implement a practical access audit tool"},
    {"domain": "cybersecurity", "task_type": "systems", "task": "Design a resilient identity and access management system"},
    {"domain": "operations", "task_type": "research", "task": "Compare methods for improving incident response"},
    {"domain": "operations", "task_type": "engineering", "task": "Build an execution plan for automated service health checks"},
    {"domain": "operations", "task_type": "systems", "task": "Design a stable distributed job processing system"},
    {"domain": "customer_support", "task_type": "research", "task": "Analyze approaches for reducing customer support resolution time"},
    {"domain": "customer_support", "task_type": "engineering", "task": "Implement a practical support ticket prioritisation workflow"},
    {"domain": "customer_support", "task_type": "systems", "task": "Design a scalable customer support routing system"},
    {"domain": "commercial_strategy", "task_type": "research", "task": "Compare go-to-market approaches for a workflow automation product"},
    {"domain": "commercial_strategy", "task_type": "systems", "task": "Design a repeatable partner-led sales operating system"},
]


def run_discovery(seed=6900):
    baseline = snapshot_memory()
    case_scores = []
    crashes = []
    random.seed(seed)

    try:
        for index, source_case in enumerate(CASES):
            case = {"id": index + 1, **source_case}

            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    result = run_task(case["task"])

                case_scores.append(score_case(case, result))
            except Exception as exc:
                crashes.append({
                    "id": case["id"],
                    "domain": case["domain"],
                    "error": repr(exc),
                })
    finally:
        restore_memory(baseline)

    domains = sorted({case["domain"] for case in CASES})
    scores = summarize_scores(case_scores, crashes, domains)
    supported = commercial_hypothesis_supported(scores)
    report = build_report(
        CASES,
        case_scores,
        crashes,
        scores,
        winner_distribution(case_scores),
        supported,
    )
    save_report(report)
    return public_summary(report)
