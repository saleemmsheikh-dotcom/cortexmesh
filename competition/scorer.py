from engine.structure_memory import repetition_penalty, structure_hash


def score(solution, critic_type):
    text = solution["solution"].lower()

    base = 5

    # LOGIC CRITIC (Architect lens)
    if critic_type == "logic":
        if "system" in text or "structure" in text:
            base += 2
        if "step" in text:
            base -= 1

    # RISK CRITIC (Engineer lens)
    if critic_type == "risk":
        if "fail" in text or "validate" in text:
            base += 2
        if "abstract" in text:
            base -= 1

    # COMPLETENESS CRITIC (Researcher lens)
    if critic_type == "completeness":
        if "compare" in text or "alternative" in text:
            base += 2
        if "single" in text:
            base -= 1

    return max(0, min(10, base))


def get_weights(ledger):
    memory = ledger.memory

    # default weights
    logic_w = 0.4
    risk_w = 0.3
    comp_w = 0.3

    # adaptive adjustment
    critic_agreement = getattr(memory, "critic_agreement", [])

    if len(critic_agreement) > 3:
        agreement = sum(critic_agreement[-3:]) / 3

        if agreement < 0.5:
            # critics disagree -> increase logic weight
            logic_w += 0.1
            comp_w -= 0.1

        if agreement > 0.8:
            # too aligned -> increase risk sensitivity
            risk_w += 0.1
            logic_w -= 0.1

    return logic_w, risk_w, comp_w


def score_solution(solution, reviews, ledger):

    logic_w, risk_w, comp_w = get_weights(ledger)
    memory = getattr(ledger, "persistent_memory", {})

    scores = {
        "logic": score(solution, "logic"),
        "risk": score(solution, "risk"),
        "completeness": score(solution, "completeness")
    }

    total = (
        scores["logic"] * logic_w +
        scores["risk"] * risk_w +
        scores["completeness"] * comp_w
    )

    penalty = repetition_penalty(
        solution["agent"],
        structure_hash(solution["solution"]),
        memory
    )
    total = max(0, total - penalty)

    return {
        "solution": solution,
        "scores": {
            "logic": scores["logic"],
            "risk": scores["risk"],
            "completeness": scores["completeness"],
            "repetition_penalty": penalty,
            "total": total
        }
    }


def select_best(scored_solutions):
    if not scored_solutions:
        raise ValueError("Cannot select a best solution from an empty list.")

    ranked = sorted(
        scored_solutions,
        key=lambda x: x["scores"]["total"],
        reverse=True
    )

    return ranked[0]
