import contextlib
import io
import json
import os
import random
from pathlib import Path

from engine.model_router import call_model
from engine.runner import run_task
from research.usefulness_discovery.external.external_report import (
    build_external_report,
    public_summary,
    save_external_report,
)
from research.usefulness_discovery.external.scoring import WEIGHTS, score_blind_outputs
from research.usefulness_discovery.runner import CASES
from testing.common import restore_memory, snapshot_memory


ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "cases"
OUTPUTS_DIR = ROOT / "outputs"
REVIEWS_DIR = ROOT / "blind_reviews"
SCORES_DIR = ROOT / "scores"

RISK_SECTION = """

FINAL RISK REVIEW

1. Failure modes:
- What could make this recommendation fail?

2. Edge cases:
- Where might this advice not apply?

3. Safeguards:
- What controls reduce downside risk?

4. Validation checks:
- What evidence should be checked before acting?
"""


def run_external_benchmark(seed=6910, patch=None):
    patch = patch or os.getenv("CORTEX_PATCH")

    if patch not in (None, "", "risk_section"):
        raise ValueError(f"Unknown controlled benchmark patch: {patch}")

    patch = patch or None
    baseline_memory = snapshot_memory()
    rng = random.Random(seed)
    results = []
    _prepare_directories()

    try:
        for index, source_case in enumerate(CASES):
            case = {"id": index + 1, **source_case}

            try:
                candidates = _generate_candidates(case, patch=patch)
                labels = ["Output_A", "Output_B", "Output_C"]
                rng.shuffle(labels)
                source_by_label = dict(zip(labels, candidates))
                blind_outputs = {
                    label: candidates[source]
                    for label, source in source_by_label.items()
                }
                blind_scores = score_blind_outputs(case["task"], blind_outputs)
                scores_by_source = {
                    source: blind_scores[label]["weighted_total"]
                    for label, source in source_by_label.items()
                }
                result = {
                    "id": case["id"],
                    "domain": case["domain"],
                    "task_type": case["task_type"],
                    "source_by_label": source_by_label,
                    "scores_by_source": scores_by_source,
                }
                _write_case_artifacts(
                    case,
                    blind_outputs,
                    blind_scores,
                    result,
                    patch=patch,
                )
                results.append(result)
            except Exception as exc:
                results.append({
                    "id": case["id"],
                    "domain": case["domain"],
                    "task_type": case["task_type"],
                    "error": repr(exc),
                })
    finally:
        restore_memory(baseline_memory)

    report = build_external_report(results)
    report["score_weights"] = WEIGHTS
    report["controlled_patch"] = patch
    save_external_report(report, patch=patch)
    return public_summary(report)


def _generate_candidates(case, patch=None):
    with contextlib.redirect_stdout(io.StringIO()):
        cortexmesh_result = run_task(case["task"])

    cortexmesh = cortexmesh_result["final"]["authority"]["decision"]["solution"]["solution"]

    if patch == "risk_section":
        cortexmesh += RISK_SECTION

    single_model = call_model(
        "You are a general business problem solver. Give one concise recommendation.",
        case["task"],
    )
    simple_framework = _simple_framework(case["task"])
    return {
        "cortexmesh": cortexmesh,
        "single_model": single_model,
        "simple_framework": simple_framework,
    }


def _simple_framework(task):
    return (
        f"Decision framework for: {task}\n"
        "1. Define the objective, constraints, owner, and measurable outcome.\n"
        "2. Compare three alternatives using impact, effort, cost, and evidence.\n"
        "3. Select the strongest option and record the rationale and assumptions.\n"
        "4. Identify risks, dependencies, failure modes, edge cases, and safeguards.\n"
        "5. Implement in phases, validate with metrics, monitor results, and iterate."
    )


def _prepare_directories():
    for path in (CASES_DIR, OUTPUTS_DIR, REVIEWS_DIR, SCORES_DIR):
        path.mkdir(parents=True, exist_ok=True)


def _write_case_artifacts(case, outputs, blind_scores, result, patch=None):
    name = f"case_{case['id']:02d}.json"
    arm = patch or "baseline"
    case_dir = CASES_DIR / arm
    output_dir = OUTPUTS_DIR / arm
    review_dir = REVIEWS_DIR / arm
    score_dir = SCORES_DIR / arm

    for path in (case_dir, output_dir, review_dir, score_dir):
        path.mkdir(parents=True, exist_ok=True)

    _write_json(case_dir / name, case)
    _write_json(output_dir / name, {
        "case_id": case["id"],
        "outputs": outputs,
    })
    _write_json(review_dir / name, {
        "case_id": case["id"],
        "blind_scoring": True,
        "weights": WEIGHTS,
        "reviews": blind_scores,
    })
    _write_json(score_dir / name, result)


def _write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True))
