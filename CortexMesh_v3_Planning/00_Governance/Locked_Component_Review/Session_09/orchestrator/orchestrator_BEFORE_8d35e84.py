import random

from agents.solver import SolverAgent
from agents.local_solver import LocalSolverAgent
from agents.reviewer import ReviewerAgent
from agents.authority import AuthorityAgent

from competition.conflict import detect_conflict
from competition.scorer import score_solution

from ledger.ledger import Ledger
from cost.budget import Budget
from memory.memory_store import load_memory

from engine.diversity_guard import detect_similarity
from engine.mode_manager import get_mode
from engine.rebalancer import compute_rebalance
from engine.structure_memory import structure_hash
from engine.task_classifier import classify_task


SOLVER_ROLES = (
    ("Architect", "architect"),
    ("Researcher", "researcher"),
    ("Engineer", "engineer"),
)

CRITIC_ROLES = ("logic", "risk", "completeness")
MIN_PROB = 0.15


def build_solvers(mode):
    agent_class = LocalSolverAgent if mode == "dev" else SolverAgent
    return [agent_class(name, role) for name, role in SOLVER_ROLES]


def build_critics():
    return [ReviewerAgent(role) for role in CRITIC_ROLES]


def diversity_boost(agents, memory):
    total = sum(memory["agent_wins"].values()) or 1

    boosted = []

    for a in agents:
        wins = memory["agent_wins"].get(a.name, 0)
        ratio = wins / total

        # underrepresented agents get boost
        boost = 1.5 if ratio < 0.2 else 1.0

        boosted.append((a, boost))

    return boosted


def add_noise(weights, epsilon=0.08):
    noisy = []

    for w in weights:
        noisy.append(w + random.uniform(0, epsilon))

    return noisy


def weighted_choice(agents, memory):
    weighted = diversity_boost(agents, memory)

    agents, weights = zip(*weighted)
    weights = add_noise(weights)

    floored_weights = []

    for weight in weights:
        if weight < MIN_PROB:
            weight = MIN_PROB

        floored_weights.append(weight)

    return random.choices(agents, weights=floored_weights, k=len(agents))


def weighted_agents(base_agents, weights):
    return sorted(
        base_agents,
        key=lambda a: weights.get(a.name, 1.0) * random.random(),
        reverse=True
    )


def update_role_weights(memory, final_agent):
    weights = memory.get("role_weights", {})

    for role in weights:
        if role == final_agent:
            weights[role] *= 1.05  # reward winner slightly
        else:
            weights[role] *= 0.98  # decay others slightly

    # normalise
    total = sum(weights.values())
    for role in weights:
        weights[role] /= total


def enforce_rotation(agents, memory):
    usage = memory.get("agent_usage", {})

    for a in agents:
        if usage.get(a.name, 0) > 5:
            usage[a.name] *= 0.7  # soft cooldown

    return agents


def record_solution_structure(memory, solution):
    h = structure_hash(solution["solution"])

    memory.setdefault("recent_structures", [])
    memory["recent_structures"].append({
        "agent": solution["agent"],
        "hash": h
    })

    # keep last 20 only
    memory["recent_structures"] = memory["recent_structures"][-20:]

    memory.setdefault("agent_usage", {})
    memory["agent_usage"][solution["agent"]] = memory["agent_usage"].get(solution["agent"], 0) + 1


def spend_budget(budget):
    if budget.exceeded():
        return False

    budget.tick()
    return True


def reviews_for(critiques, index):
    if index < len(critiques):
        return critiques[index]["reviews"]

    return []


def orchestrate(task, memory=None):
    task = str(task).strip()
    if not task:
        raise ValueError("Task cannot be empty.")

    memory = memory or load_memory()
    task_type = classify_task(task)

    ledger = Ledger()
    ledger.persistent_memory = memory
    budget = Budget(limit=12)
    ledger.add("PERSISTED_MEMORY", memory)
    ledger.add("TASK_TYPE", task_type)

    mode = get_mode(budget)
    ledger.add("mode", mode)

    solvers = build_solvers(mode)
    solvers = enforce_rotation(solvers, memory)
    solvers = weighted_agents(solvers, memory["role_weights"])
    solvers = weighted_choice(solvers, memory)
    critics = build_critics()

    solutions = []

    for s in solvers:
        weight_adjust = ledger.rebalance.get(s.role, 0)

        base_prob = 0.7 + weight_adjust

        if random.random() > base_prob:
            continue

        if not spend_budget(budget):
            break

        sol = s.act(task, ledger)
        solutions.append(sol)
        ledger.add("solution", sol)
        record_solution_structure(memory, sol)

    if not solutions and solvers:
        fallback_solver = solvers[0]
        sol = fallback_solver.act(task, ledger)
        solutions.append(sol)
        ledger.add("solution", sol)
        record_solution_structure(memory, sol)
        ledger.add("ACTIVATION_FALLBACK", fallback_solver.role)

    conflict_mode = detect_conflict(solutions)
    ledger.add("CONFLICT_MODE", conflict_mode)

    if detect_similarity(solutions):
        ledger.add("DIVERSITY_WARNING", "All solutions identical - forcing variation")

    critiques = []

    for solution in solutions:
        reviews = []

        for critic in critics:
            if not spend_budget(budget):
                ledger.add("budget", "Review budget exhausted")
                break

            critique = critic.review(solution)
            reviews.append(critique)

            ledger.add("critique", critique)

        critiques.append({
            "solution": solution,
            "reviews": reviews
        })

    refinement_required = False

    for c_group in critiques:
        for r in c_group["reviews"]:
            if "missing" in r["review"].lower() or "unclear" in r["review"].lower():
                refinement_required = True

    if refinement_required:
        ledger.add("REFINEMENT_TRIGGERED", True)

        refined_solutions = []

        for solver in solvers:
            refined_task = task + "\n\nCRITIC FEEDBACK:\n" + str(critiques)
            refined_solution = solver.act(refined_task, ledger)
            refined_solutions.append(refined_solution)
            ledger.add("refined_solution", refined_solution)
            record_solution_structure(memory, refined_solution)

        solutions = refined_solutions

    scored = []

    for i, solution in enumerate(solutions):
        reviews = reviews_for(critiques, i)
        scored_solution = score_solution(solution, reviews, ledger)
        scored.append(scored_solution)

    ledger.add("scored", scored)

    authority = AuthorityAgent()
    final_decision = authority.decide(scored, ledger, task_type=task_type)

    ledger.add("AUTHORITY", final_decision)

    winner = final_decision["decision"]["solution"]["agent"] \
        if isinstance(final_decision["decision"], dict) else final_decision["decision"]["agent"]

    ledger.meta.log_win(winner)
    update_role_weights(memory, winner)

    rebalance = compute_rebalance(ledger.meta)
    ledger.rebalance = rebalance

    if final_decision["action"] == "CONFLICT_RESOLUTION":
        ledger.add("CONFLICT_DETAILS", final_decision["alternatives"])

        # optional: expose disagreement instead of hiding it
        best = {
            "primary": final_decision["decision"]["solution"],
            "alternatives": [
                a["solution"] for a in final_decision["alternatives"]
            ]
        }
    else:
        best = final_decision["decision"]["solution"]

    ledger.add("FINAL_SCORED", final_decision["decision"])
    ledger.add("FINAL", best)

    meta_report = ledger.meta.report()

    return {
        "final": best,
        "critiques": critiques,
        "authority": final_decision,
        "meta": meta_report,
        "mode": mode,
        "scored": scored,
        "conflict_mode": conflict_mode,
        "conflict_resolved": final_decision["action"] == "CONFLICT_RESOLUTION",
    }
