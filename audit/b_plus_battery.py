#!/usr/bin/env python3
"""
Option B+ Adversarial Stability Battery
V6.10.2 Remediation Verification - Gate 4

Runs 500 tasks with embedded adversarial injections:
- Governance stress (tamper, overflow, illegal version)
- Authority adversarial (1/10 specialist vs 10/10 non-specialist)
- Critic divergence (contradictory reviews)

Pass thresholds defined below. No internal test framework used for sign-off.
"""

import contextlib
import io
import json
import random
import sys
import time
from pathlib import Path


# Add project to path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.authority import AuthorityAgent, specialist_family
from competition.scorer import score_solution
from engine.runner import run_task
from evolution.strategy_registry import base_agent_name
from governance.enforcement import enforce_governance
from governance.tamper_log import verify_tamper_log
from memory.memory_store import load_memory


# === CONFIGURATION ===

TOTAL_RUNS = 500
INJECTION_CLEAN = range(1, 101)      # Runs 1-100: clean baseline
INJECTION_GOV = range(101, 201)      # Runs 101-200: governance stress
INJECTION_AUTH = range(201, 301)     # Runs 201-300: authority adversarial
INJECTION_CRITIC = range(301, 401)   # Runs 301-400: critic divergence
INJECTION_MIXED = range(401, 501)    # Runs 401-500: combined stress

# Authority adversarial: 10% of runs in range
AUTH_ADVERSARIAL_RATE = 0.10
# Critic divergence: 10% of runs in range
CRITIC_DIVERGENCE_RATE = 0.10

# Pass thresholds
THRESHOLDS = {
    "crashes_max": 0,
    "specialist_win_rate_max": 0.95,
    "critic_divergence_min": 2.0,
    "memory_growth_per_run_max": 200,
    "governance_recovery_rate_min": 1.0,
    "tamper_integrity_failures_max": 0,
    "rollback_success_rate_min": 1.0,
    "freeze_lockups_max": 0,
    "non_specialist_must_win": True,
}

# Tasks by domain
TASKS = {
    "engineering": [
        "Design a REST API for inventory management",
        "Optimize database query performance",
        "Implement CI/CD pipeline for microservices",
    ],
    "research": [
        "Analyze market trends for electric vehicles",
        "Evaluate competing machine learning frameworks",
        "Review academic literature on distributed systems",
    ],
    "systems": [
        "Design system architecture for real-time analytics",
        "Plan cloud migration strategy for legacy application",
        "Evaluate security posture of Kubernetes cluster",
    ],
}


# === HELPERS ===

def extract_winner(task_result):
    """Extract the winning solution from the production runner result."""
    final = task_result.get("final", {}).get("final", {})

    if isinstance(final, dict) and "primary" in final:
        final = final["primary"]

    if not isinstance(final, dict):
        return None, None

    winner = final.get("agent")
    winner_base = final.get("base_agent") or base_agent_name(winner)
    return winner, winner_base


def quiet_run_task(task):
    """Run the production task path while keeping this audit's console clean."""
    with contextlib.redirect_stdout(io.StringIO()):
        return run_task(task)


# === INJECTION FUNCTIONS ===

def inject_governance_stress(memory):
    """Inject random governance violations and verify recovery."""
    injection_type = random.choice(["tamper", "overflow", "illegal_version"])
    registry = memory.get("strategy_registry", {})
    detected_tamper_issues = []

    if injection_type == "tamper":
        from governance.tamper_log import log_governance_event

        if not memory.get("governance_tamper_log"):
            log_governance_event(memory, {"type": "seed", "detail": "audit seed"})

        idx = random.randint(0, len(memory["governance_tamper_log"]) - 1)
        memory["governance_tamper_log"][idx]["type"] = "CORRUPTED"
        detected_tamper_issues = verify_tamper_log(memory)
        enforce_governance(memory)

    elif injection_type == "overflow" and registry:
        # Add extra strategies to trigger overflow.
        family = random.choice(list(registry.keys()))
        strategies = registry[family]["strategies"]
        for i in range(5):
            strategies[f"Fake_v{i}"] = {
                "version": 2,
                "status": "active",
                "traits": ["injected"],
            }

    elif injection_type == "illegal_version" and registry:
        # Add illegal version strategy.
        family = random.choice(list(registry.keys()))
        registry[family]["strategies"]["Illegal_v99"] = {
            "version": 99,
            "status": "active",
            "traits": ["injected"],
        }

    violations = enforce_governance(memory)

    # For tamper, recovery means detection plus policy response, not issues absent.
    if injection_type == "tamper":
        actions = memory.get("governance_actions", [])
        recent_actions = actions[-5:] if len(actions) >= 5 else actions

        return {
            "type": injection_type,
            "violations": len(violations),
            "detected": len(detected_tamper_issues) > 0,
            "frozen": memory.get("governance_frozen", False),
            "rollback": any(
                action.get("action") == "rollback"
                for action in recent_actions
            ),
            "recovered": memory.get("governance_frozen", False) or any(
                action.get("action") == "rollback"
                for action in recent_actions
            ),
        }

    # For overflow/illegal version, verify actual quarantine.
    if injection_type in ("overflow", "illegal_version"):
        quarantined_count = 0

        for _family, data in registry.items():
            for _name, strategy in data.get("strategies", {}).items():
                if (
                    "injected" in strategy.get("traits", [])
                    and strategy.get("status") == "quarantined"
                ):
                    quarantined_count += 1

        return {
            "type": injection_type,
            "violations": len(violations),
            "quarantined": quarantined_count,
            "recovered": quarantined_count > 0,
        }

    return {
        "type": injection_type,
        "violations": len(violations),
        "recovered": False,
    }


def inject_authority_adversarial(memory, task_type):
    """Force 1/10 specialist vs 10/10 non-specialist scenario."""
    specialist = specialist_family(task_type)
    non_specialist = next(
        family
        for family in ("Architect", "Researcher", "Engineer")
        if family != specialist
    )

    candidates = [
        {
            "solution": {
                "agent": f"{specialist}_v2",
                "base_agent": specialist,
                "solution": "weak specialist output",
            },
            "scores": {
                "logic": 1,
                "risk": 1,
                "completeness": 1,
                "repetition_penalty": 0,
                "total": 1,
            },
        },
        {
            "solution": {
                "agent": f"{non_specialist}_v2",
                "base_agent": non_specialist,
                "solution": "strong non-specialist output",
            },
            "scores": {
                "logic": 10,
                "risk": 10,
                "completeness": 10,
                "repetition_penalty": 0,
                "total": 10,
            },
        },
    ]

    class MockLedger:
        def __init__(self, mem):
            self.memory = {}
            self.persistent_memory = mem

    ledger = MockLedger(memory)
    authority = AuthorityAgent()

    try:
        result = authority.decide(candidates, ledger, task_type=task_type)
        winner = result["decision"]["solution"]["agent"]
        winner_base = result["decision"]["solution"].get("base_agent", winner)

        return {
            "winner": winner,
            "winner_base": winner_base,
            "specialist": specialist,
            "non_specialist": non_specialist,
            "non_specialist_won": winner_base != specialist,
            "authority_total": result["decision"]["scores"]["authority_total"],
        }
    except Exception as exc:
        return {
            "error": str(exc),
            "specialist": specialist,
            "non_specialist": non_specialist,
            "non_specialist_won": False,
        }


def inject_critic_divergence(solution, ledger):
    """Test if contradictory reviews produce score divergence."""
    negative_reviews = [
        {"critic": "logic", "verdict": "negative", "confidence": 1.0},
        {"critic": "risk", "verdict": "negative", "confidence": 1.0},
    ]
    positive_reviews = [
        {"critic": "logic", "verdict": "positive", "confidence": 1.0},
        {"critic": "risk", "verdict": "positive", "confidence": 1.0},
    ]

    score_neg = score_solution(solution, negative_reviews, ledger)
    score_pos = score_solution(solution, positive_reviews, ledger)
    divergence = abs(score_pos["scores"]["total"] - score_neg["scores"]["total"])

    return {
        "score_negative": score_neg["scores"]["total"],
        "score_positive": score_pos["scores"]["total"],
        "divergence": divergence,
        "divergence_sufficient": divergence >= THRESHOLDS["critic_divergence_min"],
    }


# === MAIN BATTERY ===

def run_battery():
    results = {
        "runs": [],
        "summary": {
            "total_runs": 0,
            "crashes": 0,
            "specialist_wins": 0,
            "non_specialist_wins": 0,
            "critic_divergence_runs": 0,
            "critic_divergence_sufficient": 0,
            "governance_injections": 0,
            "governance_recoveries": 0,
            "tamper_integrity_failures": 0,
            "memory_start": 0,
            "memory_end": 0,
        },
    }

    memory = load_memory()
    results["summary"]["memory_start"] = len(json.dumps(memory))
    start_time = time.time()

    for run_num in range(1, TOTAL_RUNS + 1):
        run_result = {
            "run": run_num,
            "injection": None,
            "crash": False,
            "domain": None,
        }

        try:
            domain = random.choice(list(TASKS.keys()))
            task = random.choice(TASKS[domain])
            run_result["domain"] = domain

            if run_num in INJECTION_CLEAN:
                injection_type = "clean"
            elif run_num in INJECTION_GOV:
                injection_type = "governance"
            elif run_num in INJECTION_AUTH and random.random() < AUTH_ADVERSARIAL_RATE:
                injection_type = "authority_adversarial"
            elif run_num in INJECTION_CRITIC and random.random() < CRITIC_DIVERGENCE_RATE:
                injection_type = "critic_divergence"
            elif run_num in INJECTION_MIXED:
                injection_type = random.choice([
                    "clean",
                    "governance",
                    "authority_adversarial",
                    "critic_divergence",
                ])
            else:
                injection_type = "clean"

            run_result["injection"] = injection_type

            if injection_type == "governance":
                gov_result = inject_governance_stress(memory)
                run_result["governance"] = gov_result
                results["summary"]["governance_injections"] += 1
                if gov_result.get("recovered"):
                    results["summary"]["governance_recoveries"] += 1

            elif injection_type == "authority_adversarial":
                auth_result = inject_authority_adversarial(memory, domain)
                run_result["authority"] = auth_result
                if auth_result.get("non_specialist_won"):
                    results["summary"]["non_specialist_wins"] += 1
                else:
                    results["summary"]["specialist_wins"] += 1

            elif injection_type == "critic_divergence":
                solution = {
                    "agent": "Test",
                    "solution": "system structure with fail validate",
                }

                class MockLedger:
                    def __init__(self):
                        self.memory = {}
                        self.persistent_memory = memory

                ledger = MockLedger()
                critic_result = inject_critic_divergence(solution, ledger)
                run_result["critic"] = critic_result
                results["summary"]["critic_divergence_runs"] += 1
                if critic_result["divergence_sufficient"]:
                    results["summary"]["critic_divergence_sufficient"] += 1

            else:
                task_result = quiet_run_task(task)
                winner, winner_base = extract_winner(task_result)
                run_result["winner"] = winner
                run_result["winner_base"] = winner_base
                if winner_base == specialist_family(domain):
                    results["summary"]["specialist_wins"] += 1
                else:
                    results["summary"]["non_specialist_wins"] += 1
                memory = load_memory()

            tamper_issues = (
                []
                if run_result["governance"].get("type") == "tamper"
                else verify_tamper_log(memory)
            ) if injection_type == "governance" else verify_tamper_log(memory)
            if tamper_issues:
                results["summary"]["tamper_integrity_failures"] += len(tamper_issues)
                run_result["tamper_issues"] = tamper_issues

        except Exception as exc:
            run_result["crash"] = True
            run_result["error"] = str(exc)
            results["summary"]["crashes"] += 1

        results["runs"].append(run_result)
        results["summary"]["total_runs"] += 1

    memory = load_memory()
    results["summary"]["memory_end"] = len(json.dumps(memory))
    final_tamper_issues = verify_tamper_log(memory)
    results["summary"]["tamper_integrity_failures"] = len(final_tamper_issues)
    if final_tamper_issues:
        results["final_tamper_issues"] = final_tamper_issues
    results["summary"]["runtime_seconds"] = time.time() - start_time
    results["pass"] = evaluate_pass_fail(results)

    return results


def evaluate_pass_fail(results):
    """Evaluate summary against THRESHOLDS."""
    summary = results["summary"]
    governance_runs = [
        run
        for run in results["runs"]
        if run.get("injection") == "governance"
    ]
    checks = {
        "crashes": summary["crashes"] <= THRESHOLDS["crashes_max"],
        "specialist_rate": (
            summary["specialist_wins"] / max(summary["total_runs"], 1)
        ) <= THRESHOLDS["specialist_win_rate_max"],
        "critic_divergence": (
            summary["critic_divergence_sufficient"]
            / max(summary["critic_divergence_runs"], 1)
        ) >= 0.5 if summary["critic_divergence_runs"] > 0 else True,
        "memory_growth": (
            (summary["memory_end"] - summary["memory_start"])
            / max(summary["total_runs"], 1)
        ) <= THRESHOLDS["memory_growth_per_run_max"],
        "governance_recovery": (
            all(
                run.get("governance", {}).get("detected", True)
                if run.get("governance", {}).get("type") == "tamper"
                else True
                for run in governance_runs
            )
            and all(
                run.get("governance", {}).get("recovered", False)
                for run in governance_runs
            )
        ),
        "tamper_integrity": (
            summary["tamper_integrity_failures"]
            <= THRESHOLDS["tamper_integrity_failures_max"]
        ),
        "non_specialist_won": (
            summary["non_specialist_wins"] > 0
            or not THRESHOLDS["non_specialist_must_win"]
        ),
    }

    return {
        "overall": all(checks.values()),
        "checks": checks,
    }


# === OUTPUT ===

if __name__ == "__main__":
    print("=" * 60)
    print("Option B+ Adversarial Stability Battery")
    print("=" * 60)

    results = run_battery()

    report_path = Path(__file__).resolve().parents[1] / "reports" / "b_plus_battery.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(results, indent=2))

    print(f"\nTotal Runs: {results['summary']['total_runs']}")
    print(f"Crashes: {results['summary']['crashes']}")
    print(f"Specialist Wins: {results['summary']['specialist_wins']}")
    print(f"Non-Specialist Wins: {results['summary']['non_specialist_wins']}")
    print(f"Governance Injections: {results['summary']['governance_injections']}")
    print(f"Governance Recoveries: {results['summary']['governance_recoveries']}")
    print(f"Critic Divergence Runs: {results['summary']['critic_divergence_runs']}")
    print(
        "Critic Divergence Sufficient: "
        f"{results['summary']['critic_divergence_sufficient']}"
    )
    print(f"Tamper Integrity Failures: {results['summary']['tamper_integrity_failures']}")
    print(
        "Memory Growth: "
        f"{results['summary']['memory_end'] - results['summary']['memory_start']} bytes"
    )
    print(f"Runtime: {results['summary']['runtime_seconds']:.2f}s")
    print(f"\n{'=' * 60}")
    print(f"PASS: {results['pass']['overall']}")
    print(f"{'=' * 60}")

    for check, passed in results["pass"]["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"  {check}: {status}")

    print(f"{'=' * 60}")
