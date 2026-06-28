import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.authority import AuthorityAgent
from competition.scorer import score_solution
from core.contracts import CapabilityContext, validate_capability_source
from evolution.strategy_registry import default_registry
from governance.enforcement import enforce_governance
from governance.tamper_log import log_governance_event, verify_tamper_log
from ledger.ledger import Ledger
from memory.task_trust import DEFAULT_TASK_TRUST


def base_memory():
    return {
        "strategy_registry": default_registry(),
        "task_trust": copy.deepcopy(DEFAULT_TASK_TRUST),
        "confidence_history": {},
        "recent_structures": [],
        "governance_actions": [],
        "governance_violations": [],
        "governance_tamper_log": [],
        "governance_tamper_anchor": None,
        "governance_risk_score": 0,
        "governance_risk_history": [],
        "governance_frozen": False,
        "governance_incidents": 0,
        "governance_clean_runs": 0,
    }


def load_temp_capability(source):
    directory = tempfile.TemporaryDirectory()
    path = Path(directory.name) / "probe.py"
    path.write_text(source)
    spec = importlib.util.spec_from_file_location("probe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return directory, module, path


def finding_1_capability_sandbox_bypass():
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "capability_write.txt"
        source = (
            "from pathlib import Path\n"
            "import importlib\n"
            "def run(context):\n"
            "    results = {}\n"
            "    try:\n"
            f"        Path({str(target)!r}).write_text('bypass')\n"
            "        results['filesystem_write'] = True\n"
            "    except Exception:\n"
            "        results['filesystem_write'] = False\n"
            "    try:\n"
            "        importlib.import_module('memory.memory_store')\n"
            "        results['dynamic_import'] = True\n"
            "    except Exception:\n"
            "        results['dynamic_import'] = False\n"
            "    return results\n"
        )
        holder, module, _ = load_temp_capability(source)

        try:
            execution = CapabilityContext(base_memory(), "probe").execute_capability(
                module.run
            )
        finally:
            holder.cleanup()

        result = execution.get("result") or {}
        reproduced = (
            target.exists()
            or result.get("filesystem_write") is True
            or result.get("dynamic_import") is True
        )

        return {
            "status": "reproduced" if reproduced else "not_reproduced",
            "details": {
                "target_exists": target.exists(),
                "execution": execution,
            },
        }


def finding_2_contract_blindness():
    source = (
        "def run(context):\n"
        "    mem = context.memory\n"
        "    mem['governance_frozen'] = False\n"
    )
    holder, _, path = load_temp_capability(source)

    try:
        violations = validate_capability_source(path)
    finally:
        holder.cleanup()

    reproduced = not violations
    return {
        "status": "reproduced" if reproduced else "not_reproduced",
        "details": {"violations": violations},
    }


def finding_3_critic_reviews_affect_scoring():
    class MockLedger:
        memory = {}
        persistent_memory = {}

    solution = {
        "agent": "Architect",
        "solution": "system structure validate failure modes",
    }
    negative = score_solution(
        solution,
        [{"critic": "logic", "verdict": "negative", "confidence": 1.0}],
        MockLedger(),
    )
    positive = score_solution(
        solution,
        [{"critic": "logic", "verdict": "positive", "confidence": 1.0}],
        MockLedger(),
    )
    fixed = negative["scores"]["logic"] < positive["scores"]["logic"]

    return {
        "status": "fixed" if fixed else "not_fixed",
        "details": {
            "negative_logic": negative["scores"]["logic"],
            "positive_logic": positive["scores"]["logic"],
        },
    }


def finding_4_specialist_forced_win():
    memory = base_memory()
    ledger = Ledger()
    ledger.persistent_memory = memory
    ledger.add("CONFLICT_MODE", False)
    candidates = [
        {
            "solution": {
                "agent": "Engineer",
                "base_agent": "Engineer",
                "solution": "weak",
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
                "agent": "Architect",
                "base_agent": "Architect",
                "solution": "strong",
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
    winner = AuthorityAgent().decide(
        candidates,
        ledger,
        task_type="engineering",
    )["decision"]["solution"]["agent"]
    reproduced = winner == "Engineer"

    return {
        "status": "reproduced" if reproduced else "not_reproduced",
        "details": {"winner": winner, "expected_non_specialist": "Architect"},
    }


def finding_5_tamper_rollover_corruption():
    memory = {"governance_tamper_log": [], "governance_tamper_anchor": None}

    for index in range(502):
        log_governance_event(memory, {"type": "rollover_probe", "index": index})

    issues = verify_tamper_log(memory)
    reproduced = bool(issues)
    return {
        "status": "reproduced" if reproduced else "not_reproduced",
        "details": {
            "events_logged": len(memory["governance_tamper_log"]),
            "anchor_present": bool(memory.get("governance_tamper_anchor")),
            "issues": issues,
        },
    }


def finding_6_strategy_overflow_participation():
    memory = base_memory()
    memory["strategy_registry"]["Architect"] = {
        "active": "Architect_v2",
        "strategies": {
            "Architect_v1": {"version": 1, "status": "active"},
            "Architect_v2": {"version": 2, "status": "active"},
            "Architect_extra": {"version": 2, "status": "active"},
        },
    }
    violations = enforce_governance(memory)
    participating = [
        name
        for name, strategy in memory["strategy_registry"]["Architect"][
            "strategies"
        ].items()
        if strategy.get("status") != "quarantined"
    ]
    reproduced = len(participating) > 2

    return {
        "status": "reproduced" if reproduced else "not_reproduced",
        "details": {
            "violations": violations,
            "participating": participating,
            "actions": memory.get("governance_actions", []),
        },
    }


def main():
    checks = {
        "finding_1": finding_1_capability_sandbox_bypass(),
        "finding_2": finding_2_contract_blindness(),
        "finding_3": finding_3_critic_reviews_affect_scoring(),
        "finding_4": finding_4_specialist_forced_win(),
        "finding_5": finding_5_tamper_rollover_corruption(),
        "finding_6": finding_6_strategy_overflow_participation(),
    }
    summary = {key: value["status"] for key, value in checks.items()}
    print(json.dumps({"summary": summary, "details": checks}, indent=2))


if __name__ == "__main__":
    main()
