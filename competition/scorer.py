from engine.structure_memory import structure_hash


LOGIC_EVIDENCE = {
    "has_systematic_structure": 2,
    "has_logical_gaps": -1,
}

RISK_EVIDENCE = {
    "has_failure_modes": 2,
    "is_over_abstract": -1,
}

COMPLETENESS_EVIDENCE = {
    "has_alternatives": 2,
    "is_single_path": -1,
}


def score(solution, critic_type):
    text = str(solution.get("solution", "")).lower()
    evidence = solution.get("evidence", {})
    base = 5

    if critic_type == "logic":
        if evidence.get("has_systematic_structure"):
            base += LOGIC_EVIDENCE["has_systematic_structure"]
        if evidence.get("has_logical_gaps"):
            base += LOGIC_EVIDENCE["has_logical_gaps"]

    if critic_type == "risk":
        if evidence.get("has_failure_modes"):
            base += RISK_EVIDENCE["has_failure_modes"]
        if evidence.get("is_over_abstract"):
            base += RISK_EVIDENCE["is_over_abstract"]

    if critic_type == "completeness":
        if evidence.get("has_alternatives"):
            base += COMPLETENESS_EVIDENCE["has_alternatives"]
        if evidence.get("is_single_path"):
            base += COMPLETENESS_EVIDENCE["is_single_path"]

    # Backward-compatible keyword hints when no structured evidence is present.
    if not evidence:
        if critic_type == "logic":
            if "system" in text or "structure" in text:
                base += 2
            if "step" in text:
                base -= 1
        if critic_type == "risk":
            if "fail" in text or "validate" in text:
                base += 2
            if "abstract" in text:
                base -= 1
        if critic_type == "completeness":
            if "compare" in text or "alternative" in text:
                base += 2
            if "single" in text:
                base -= 1

    return max(0, min(10, base))


def get_weights(ledger):
    memory = getattr(ledger, "persistent_memory", None)

    if not isinstance(memory, dict):
        memory = getattr(ledger, "memory", {})

    if not isinstance(memory, dict):
        memory = {}

    logic_w = 0.4
    risk_w = 0.3
    comp_w = 0.3

    critic_agreement = memory.get("critic_agreement", [])

    if len(critic_agreement) > 3:
        agreement = sum(critic_agreement[-3:]) / 3

        if agreement < 0.5:
            logic_w += 0.1
            comp_w -= 0.1

        if agreement > 0.8:
            risk_w += 0.1
            logic_w -= 0.1

    return logic_w, risk_w, comp_w


def apply_review_adjustments(scores, reviews):
    adjusted = dict(scores)

    for review in reviews:
        critic = review.get("critic")
        verdict = review.get("verdict")

        if critic not in adjusted or verdict not in {"negative", "positive"}:
            continue

        confidence = review.get("confidence", 1.0)
        delta = 2.0 * confidence

        if verdict == "negative":
            adjusted[critic] = max(0, adjusted[critic] - delta)
        else:
            adjusted[critic] = min(10, adjusted[critic] + delta)

    return adjusted


def compute_total_score(solution, reviews, ledger):
    logic_w, risk_w, comp_w = get_weights(ledger)

    scores = {
        "logic": score(solution, "logic"),
        "risk": score(solution, "risk"),
        "completeness": score(solution, "completeness"),
    }
    scores = apply_review_adjustments(scores, reviews)

    weighted_total = (
        scores["logic"] * logic_w
        + scores["risk"] * risk_w
        + scores["completeness"] * comp_w
    )

    return {
        **scores,
        "weighted_total": weighted_total,
        "total": weighted_total,
    }


def score_solution(solution, reviews, ledger):
    scores = compute_total_score(solution, reviews, ledger)

    return {
        "solution": solution,
        "scores": scores,
    }


def select_best(scored_solutions):
    if not scored_solutions:
        raise ValueError("Cannot select a best solution from an empty list.")

    ranked = sorted(
        scored_solutions,
        key=lambda item: item["scores"]["total"],
        reverse=True,
    )

    return ranked[0]
