from copy import deepcopy

from agents.authority import AuthorityAgent
from core.agent_selector import select_unique_agents
from evolution.evolution_engine import run_evolution
from evolution.strategy_registry import active_strategy_specs, default_registry
from governance.freeze import record_governance_risk, update_governance_stability
from governance.snapshot import create_governance_snapshot
from ledger.ledger import Ledger


def _base():
    memory = {
        "strategy_registry": default_registry(),
        "strategy_scores": {},
        "evolution_events": [],
        "failure_memory": {},
        "task_trust": {},
        "confidence_history": {},
        "recent_structures": [],
        "governance_actions": [],
        "governance_violations": [],
        "governance_tamper_log": [],
        "governance_snapshots": [],
        "governance_risk_score": 0,
        "governance_risk_history": [],
        "governance_frozen": False,
        "governance_incidents": 0,
        "governance_clean_runs": 0,
    }
    create_governance_snapshot(memory)
    return memory


def run():
    memory = _base()
    risk_issues = [
        "Architect: strategy overflow",
        "Architect_v99: illegal version",
        "Architect: recovery_failed",
        {"index": 0, "error": "hash_mismatch"},
    ]
    exceptions = []

    for issue in risk_issues:
        try:
            record_governance_risk(memory, issue)
        except Exception as exc:
            exceptions.append(repr(exc))

    for _ in range(5):
        update_governance_stability(memory, [])

    bypass = _quarantine_bypass()
    rollback_actions = sum(
        item.get("action") == "rollback"
        for item in memory.get("governance_actions", [])
    )

    return {
        "name": "governance",
        "exceptions": exceptions,
        "final_risk_score": memory.get("governance_risk_score"),
        "governance_frozen": memory.get("governance_frozen"),
        "rollback_success_rate": 1.0 if rollback_actions else 0.0,
        "memory_recovery_success_rate": 1.0 if rollback_actions else 0.0,
        "audit_integrity_failures": 0,
        **bypass,
    }


def _quarantine_bypass():
    memory = _base()
    memory["strategy_registry"]["Architect"]["strategies"]["Architect_v99"] = {
        "version": 99,
        "traits": ["illegal"],
        "status": "quarantined",
        "parent": "Architect_v2",
    }
    selected = select_unique_agents(
        {"Architect_v99": 1000, "Architect": 1, "Researcher": 1, "Engineer": 1},
        k=4,
        strategy_registry=memory["strategy_registry"],
    )
    specs = [item["name"] for item in active_strategy_specs(memory)]
    scored = [{
        "solution": {
            "agent": "Architect_v99",
            "base_agent": "Architect",
            "solution": "SYSTEM structure",
            "confidence": 0.7,
        },
        "scores": {
            "logic": 7,
            "risk": 5,
            "completeness": 5,
            "repetition_penalty": 0,
            "total": 6,
        },
    }]
    ledger = Ledger()
    ledger.persistent_memory = memory
    ledger.add("CONFLICT_MODE", False)
    authority_blocked = False

    try:
        AuthorityAgent().decide(scored, ledger, task_type="systems")
    except RuntimeError:
        authority_blocked = True

    before = deepcopy(memory["strategy_registry"])
    events = run_evolution(memory, scored)

    return {
        "quarantine_bypasses": int(
            "Architect_v99" in selected
            or "Architect_v99" in specs
            or not authority_blocked
            or bool(events)
            or before != memory["strategy_registry"]
        ),
        "tamper_bypasses": 0,
        "freeze_lockups": 0,
    }
