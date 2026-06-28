import ast
import copy
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTING_DIR = str(Path(__file__).resolve().parent)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Prevent testing/evolution.py from shadowing the evolution package.
sys.path = [entry for entry in sys.path if entry != TESTING_DIR]

from agents.authority import AuthorityAgent
from core.contracts import CapabilityContext, validate_capability_source
from evolution.evolution_engine import run_evolution
from evolution.strategy_registry import active_strategy_specs, default_registry
from governance.enforcement import enforce_governance
from governance.freeze import record_governance_risk
from governance.snapshot import (
    create_governance_snapshot,
    restore_latest_governance_snapshot,
    verify_governance_snapshot,
)
from governance.tamper_log import log_governance_event, verify_tamper_log
from governance.validator import validate_governance
from ledger.ledger import Ledger
from memory.memory_store import load_memory


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "reports" / "v6_9_contracts.json"
SUMMARY_KEYS = (
    "memory_bypass",
    "authority_bypass",
    "governance_bypass",
    "evolution_bypass",
    "capability_import_bypass",
    "tamper_bypass",
    "snapshot_poisoning",
    "contract_status",
)
PROTECTED_KEYS = {
    "strategy_registry",
    "governance_frozen",
    "governance_risk_score",
    "governance_tamper_log",
    "task_trust",
    "knowledge_memory",
    "negative_knowledge",
    "failure_memory",
    "confidence_history",
    "agent_trust",
}
APPROVED_OWNERS = {
    "strategy_registry": ("evolution/", "governance/", "memory/memory_store.py", "testing/"),
    "governance_frozen": ("governance/", "memory/memory_store.py", "testing/"),
    "governance_risk_score": ("governance/", "memory/memory_store.py", "testing/"),
    "governance_tamper_log": ("governance/", "memory/memory_store.py", "testing/"),
    "task_trust": ("memory/task_trust.py", "memory/memory_store.py", "orchestrator.py", "testing/"),
    "knowledge_memory": ("memory/", "testing/"),
    "negative_knowledge": ("memory/", "testing/"),
    "failure_memory": ("memory/", "testing/"),
    "confidence_history": ("memory/", "testing/"),
    "agent_trust": ("memory/", "testing/"),
}


def run_contracts():
    static_violations = static_boundary_scan()
    capability_imports = capability_import_scan()
    capability = capability_sandbox_test()
    authority = authority_boundary_test()
    evolution = evolution_boundary_test()
    tamper = tamper_integrity_test()
    snapshot = snapshot_poisoning_test()
    governance = governance_boundary_test()
    governance_bypass = (
        bool(static_violations)
        or not all(capability.values())
        or not governance["passed"]
    )
    result = {
        "memory_bypass": bool(static_violations) or not all(capability.values()),
        "authority_bypass": not authority["passed"],
        "governance_bypass": governance_bypass,
        "evolution_bypass": not evolution["passed"],
        "capability_import_bypass": bool(capability_imports),
        "tamper_bypass": not tamper["passed"],
        "snapshot_poisoning": not snapshot["passed"],
        "details": {
            "static_boundary_violations": static_violations,
            "capability_import_violations": capability_imports,
            "capability_sandbox": capability,
            "governance": governance,
            "authority": authority,
            "evolution": evolution,
            "tamper": tamper,
            "snapshot": snapshot,
        },
    }
    result["contract_status"] = (
        "PASS"
        if not any(
            result[key]
            for key in (
                "memory_bypass",
                "authority_bypass",
                "governance_bypass",
                "evolution_bypass",
                "capability_import_bypass",
                "tamper_bypass",
                "snapshot_poisoning",
            )
        )
        else "FAIL"
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True))

    return {
        key: result[key]
        for key in SUMMARY_KEYS
    }


def static_boundary_scan():
    violations = []

    for path in ROOT.rglob("*.py"):
        relative = path.relative_to(ROOT).as_posix()

        try:
            tree = ast.parse(path.read_text(), filename=str(path))
        except SyntaxError as exc:
            violations.append({"file": relative, "error": str(exc)})
            continue

        for node in ast.walk(tree):
            targets = []

            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = (
                    node.targets
                    if isinstance(node, ast.Assign)
                    else [node.target]
                )

            for target in targets:
                key = _protected_subscript_key(target)

                if key and not _approved(relative, key):
                    violations.append({
                        "file": relative,
                        "line": node.lineno,
                        "key": key,
                    })

            if isinstance(node, ast.Delete):
                for target in node.targets:
                    key = _protected_subscript_key(target)

                    if key and not _approved(relative, key):
                        violations.append({
                            "file": relative,
                            "line": node.lineno,
                            "key": key,
                            "operation": "delete",
                        })

            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                key = _protected_subscript_key(node.func.value)

                if (
                    key
                    and node.func.attr in {
                        "append",
                        "clear",
                        "extend",
                        "insert",
                        "pop",
                        "remove",
                        "setdefault",
                        "update",
                        "__setitem__",
                    }
                    and not _approved(relative, key)
                ):
                    violations.append({
                        "file": relative,
                        "line": node.lineno,
                        "key": key,
                        "operation": node.func.attr,
                    })

    return violations


def capability_import_scan():
    violations = []

    for path in (ROOT / "capabilities").glob("*.py"):
        for issue in validate_capability_source(path):
            violations.append({
                "file": path.relative_to(ROOT).as_posix(),
                "issue": issue,
            })

    return violations


def capability_sandbox_test():
    memory = _base_memory()
    module = importlib.import_module("capabilities.malicious_probe")
    context = CapabilityContext(memory, "probe")
    execution = context.execute_capability(module.run)
    result = execution["result"]
    result["runtime_blocked"] = execution["blocked"]
    return result


def authority_boundary_test():
    cases = {}

    for name, candidate, setup in (
        ("unknown", _candidate("FakeAgent"), None),
        ("missing_agent", _candidate(None), None),
        ("quarantined", _candidate("Architect_v99"), "quarantined"),
        ("illegal_version", _candidate("Architect_v99"), "illegal"),
    ):
        memory = _base_memory()

        if setup:
            memory["strategy_registry"]["Architect"]["strategies"]["Architect_v99"] = {
                "version": 99 if setup == "illegal" else 2,
                "traits": ["illegal"],
                "status": "quarantined" if setup == "quarantined" else "active",
                "parent": "Architect_v2",
            }

        ledger = Ledger()
        ledger.persistent_memory = memory
        ledger.add("CONFLICT_MODE", False)

        try:
            AuthorityAgent().decide([candidate], ledger, task_type="systems")
            cases[name] = False
        except RuntimeError:
            cases[name] = True

    proposal = CapabilityContext(_base_memory(), "task").submit_proposal({
        "agent": "FakeAgent",
        "solution": "final",
    })
    cases["direct_final"] = proposal.get("final") is False

    return {"passed": all(cases.values()), "cases": cases}


def governance_boundary_test():
    memory = _base_memory()
    memory["governance_frozen"] = True
    memory["governance_risk_score"] = 12
    log_governance_event(memory, {"type": "freeze"})
    before = copy.deepcopy(memory)
    probe = capability_sandbox_test()

    return {
        "passed": (
            all(probe.values())
            and memory == before
        ),
        "probe": probe,
    }


def evolution_boundary_test():
    memory = _base_memory()
    memory["strategy_registry"]["Engineer"]["strategies"]["Engineer_v3"] = {
        "version": 3,
        "traits": ["illegal"],
        "status": "active",
        "parent": "Engineer_v2",
    }
    memory["strategy_registry"]["Engineer"]["active"] = "Engineer_v3"
    violations = enforce_governance(memory)
    v3 = memory["strategy_registry"]["Engineer"]["strategies"]["Engineer_v3"]
    specs = [spec["name"] for spec in active_strategy_specs(memory)]
    before = copy.deepcopy(memory["strategy_registry"])
    events = run_evolution(memory, [])
    memory["governance_frozen"] = True
    frozen_before = copy.deepcopy(memory["strategy_registry"])
    frozen_events = run_evolution(memory, [_candidate("Engineer")])

    return {
        "passed": (
            v3["status"] == "quarantined"
            and memory["strategy_registry"]["Engineer"]["active"] != "Engineer_v3"
            and "Engineer_v3" not in specs
            and not events
            and before == memory["strategy_registry"]
            and not frozen_events
            and frozen_before == memory["strategy_registry"]
        ),
        "violations": violations,
        "v3_status": v3["status"],
        "active": memory["strategy_registry"]["Engineer"]["active"],
        "active_specs": specs,
        "frozen_events": frozen_events,
    }


def tamper_integrity_test():
    memory = _base_memory()
    create_governance_snapshot(memory)
    log_governance_event(memory, {"type": "quarantine", "strategy": "Architect_v99"})
    log_governance_event(memory, {"type": "recovery", "family": "Architect"})
    variants = {}

    for name, mutate in (
        ("edit", lambda log: log[0].update({"strategy": "Architect_v98"})),
        ("delete", lambda log: log.pop(0)),
        ("reorder", lambda log: log.reverse()),
        ("timestamp", lambda log: log[0].update({"timestamp": "changed"})),
        ("action_type", lambda log: log[0].update({"type": "changed"})),
    ):
        attacked = copy.deepcopy(memory)
        mutate(attacked["governance_tamper_log"])
        issues = verify_tamper_log(attacked)

        for issue in issues:
            record_governance_risk(attacked, issue)

        variants[name] = {
            "detected": bool(issues),
            "frozen": attacked.get("governance_frozen", False),
            "rollback": any(
                action.get("action") == "rollback"
                for action in attacked.get("governance_actions", [])
            ),
        }

    return {
        "passed": all(
            item["detected"] and item["frozen"] and item["rollback"]
            for item in variants.values()
        ),
        "variants": variants,
    }


def snapshot_poisoning_test():
    memory = _base_memory()
    clean_snapshot = create_governance_snapshot(memory)
    memory["strategy_registry"]["Architect"]["active"] = "Architect"
    poisoned_snapshot = create_governance_snapshot(memory)
    memory["governance_snapshots"][-1]["state"]["strategy_registry"]["Architect"]["active"] = "Architect_v99"
    memory["strategy_registry"]["Architect"]["active"] = "Architect_v99"
    valid = verify_governance_snapshot(memory["governance_snapshots"][-1])
    restored = restore_latest_governance_snapshot(memory)
    restored_active = memory["strategy_registry"]["Architect"]["active"]

    return {
        "passed": (
            not valid
            and restored
            and restored_active == "Architect"
            and clean_snapshot.get("hash") is not None
            and poisoned_snapshot.get("hash") is not None
        ),
        "valid_after_poisoning": valid,
        "restored": restored,
        "restored_active": restored_active,
        "actions": memory.get("governance_actions", []),
    }


def _candidate(agent):
    return {
        "solution": {
            "agent": agent,
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
    }


def _base_memory():
    memory = copy.deepcopy(load_memory())
    memory["strategy_registry"] = default_registry()
    memory["strategy_scores"] = {}
    memory["evolution_events"] = []
    memory["failure_memory"] = {}
    memory["governance_actions"] = []
    memory["governance_violations"] = []
    memory["governance_tamper_log"] = []
    memory["governance_snapshots"] = []
    memory["governance_risk_score"] = 0
    memory["governance_risk_history"] = []
    memory["governance_frozen"] = False
    memory["governance_incidents"] = 0
    memory["governance_clean_runs"] = 0
    return memory


def _protected_subscript_key(node):
    while isinstance(node, ast.Subscript):
        key = _literal_slice(node.slice)

        if key in PROTECTED_KEYS:
            root = node.value

            while isinstance(root, ast.Subscript):
                root = root.value

            if isinstance(root, ast.Name) and root.id == "memory":
                return key

        node = node.value

    return None


def _literal_slice(node):
    if isinstance(node, ast.Constant):
        return node.value

    return None


def _approved(relative, key):
    return any(
        relative == prefix or relative.startswith(prefix)
        for prefix in APPROVED_OWNERS[key]
    )
