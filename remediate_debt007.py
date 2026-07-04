#!/usr/bin/env python3
"""
DEBT-007 Remediation: Memory Integrity Adversarial Tests
Charter Reference: P0 Audit Charter v1.1 DEBT-007
"""

import json
import tempfile
from pathlib import Path

from memory.memory_store import (
    _default_memory,
    _ensure_schema,
    load_memory,
    save_memory,
)


def test_schema_normalization_rejects_invalid_types():
    """Inject invalid types, verify _ensure_schema handles or rejects."""
    print("\n--- TEST 1: Schema Normalization with Invalid Types ---")

    memory = _default_memory()
    memory["role_weights"] = "not_a_dict"
    memory["runs"] = "not_an_int"
    memory["agent_wins"] = 12345

    try:
        normalized = _ensure_schema(memory)
        checks = {
            "role_weights_is_dict": isinstance(normalized.get("role_weights"), dict),
            "runs_is_int": isinstance(normalized.get("runs"), int),
            "agent_wins_is_dict": isinstance(normalized.get("agent_wins"), dict),
        }
        print(f"Type correction results: {checks}")
        return checks
    except Exception as exc:
        print(f"EXCEPTION during normalization: {type(exc).__name__}: {exc}")
        return {"exception": str(exc)}


def test_tamper_detection():
    """Verify tamper log chain records and verifies events."""
    print("\n--- TEST 2: Tamper Log Detection ---")

    memory = _default_memory()

    from governance.tamper_log import log_governance_event, verify_tamper_log

    log_governance_event(memory, {"type": "test_event", "data": "original"})

    initial_log_len = len(memory.get("governance_tamper_log", []))
    print(f"Initial log entries: {initial_log_len}")

    memory["runs"] = 99999
    log_governance_event(memory, {"type": "tamper_simulation", "changed": "runs"})

    final_log_len = len(memory.get("governance_tamper_log", []))
    print(f"Final log entries: {final_log_len}")

    violations = verify_tamper_log(memory)
    print(f"Tamper violations detected: {len(violations)}")
    return {
        "initial_entries": initial_log_len,
        "final_entries": final_log_len,
        "violations": len(violations),
        "violations_detail": violations,
    }


def test_snapshot_integrity():
    """Create snapshot, verify it is valid and contains governance state."""
    print("\n--- TEST 3: Snapshot Integrity ---")

    from governance.snapshot import create_governance_snapshot, verify_governance_snapshot

    memory = _default_memory()
    memory["runs"] = 42
    memory["role_weights"] = {
        "Architect": 2.0,
        "Researcher": 1.0,
        "Engineer": 1.0,
    }

    snapshot = create_governance_snapshot(memory)

    has_snapshot = bool(memory.get("governance_snapshots"))
    snapshot_count = len(memory.get("governance_snapshots", []))
    valid_snapshot = verify_governance_snapshot(snapshot)

    print(f"Snapshot created: {has_snapshot}")
    print(f"Snapshot count: {snapshot_count}")
    print(f"Snapshot valid: {valid_snapshot}")

    if memory["governance_snapshots"]:
        last_snapshot = memory["governance_snapshots"][-1]
        state = last_snapshot.get("state", {})
        print(f"Snapshot keys: {list(last_snapshot.keys())}")
        return {
            "created": has_snapshot,
            "count": snapshot_count,
            "valid": valid_snapshot,
            "has_strategy_registry": "strategy_registry" in state,
            "has_governance_actions": "governance_actions" in state,
            "has_governance_violations": "governance_violations" in state,
            "has_governance_tamper_log": "governance_tamper_log" in state,
        }
    return {"created": False, "count": 0, "valid": False}


def test_persistence_corruption_recovery():
    """Corrupt JSON file, verify load_memory handles gracefully."""
    print("\n--- TEST 4: Corrupted Persistence Recovery ---")

    import memory.memory_store as ms

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
        temp_path = Path(handle.name)
        handle.write('{"runs": 0, "role_weights": {"Architect": 1.0, ')

    original_path = ms.MEMORY_PATH
    try:
        ms.MEMORY_PATH = temp_path

        try:
            loaded = load_memory()
            print("Graceful recovery: returned memory")
            print(f"Keys present: {list(loaded.keys())[:5]}...")
            return {"recovered": True, "is_default_schema": "role_weights" in loaded}
        except json.JSONDecodeError as exc:
            print(f"JSONDecodeError on corrupt file: {exc}")
            return {"recovered": False, "error": "JSONDecodeError"}
        except Exception as exc:
            print(f"Unexpected exception: {type(exc).__name__}: {exc}")
            return {"recovered": False, "error": type(exc).__name__}
    finally:
        ms.MEMORY_PATH = original_path
        temp_path.unlink(missing_ok=True)


def test_schema_migration():
    """Test legacy migration paths."""
    print("\n--- TEST 5: Legacy Migration ---")

    legacy = {
        "runs": 10,
        "agent_wins": {},
    }

    migrated = _ensure_schema(legacy)

    required_fields = [
        "strategy_registry",
        "entropy_target",
        "entropy_drift",
        "governance_tamper_log",
        "governance_snapshots",
    ]

    results = {field: field in migrated for field in required_fields}
    print(f"Migration results: {results}")
    return results


def result_is_warning(result):
    if "exception" in result:
        return True
    return any(value is False for value in result.values() if isinstance(value, bool))


def main():
    print("=" * 60)
    print("DEBT-007: MEMORY INTEGRITY ADVERSARIAL TESTS")
    print("=" * 60)

    results = {
        "schema_normalization": test_schema_normalization_rejects_invalid_types(),
        "tamper_detection": test_tamper_detection(),
        "snapshot_integrity": test_snapshot_integrity(),
        "persistence_recovery": test_persistence_corruption_recovery(),
        "schema_migration": test_schema_migration(),
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for name, result in results.items():
        status = "WARN" if result_is_warning(result) else "OK"
        print(f"{status} {name}: {result}")

    with open("debt007_results.json", "w") as handle:
        json.dump(results, handle, indent=2)

    print("\nResults saved to debt007_results.json")
    return results


if __name__ == "__main__":
    main()
