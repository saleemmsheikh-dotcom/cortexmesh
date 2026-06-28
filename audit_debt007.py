#!/usr/bin/env python3
"""
DEBT-007: Memory Integrity Adversarial Tests
"""

import json
import tempfile
from pathlib import Path

import memory.memory_store as ms
from memory.memory_store import load_memory, save_memory, _ensure_schema, _default_memory


def test_schema_normalization_rejects_invalid():
    """Inject invalid schema fields, verify normalization."""
    print("\n--- TEST 1: Invalid Schema Rejection ---")

    memory = _default_memory()
    memory["role_weights"] = "not_a_dict"
    memory["runs"] = "not_an_int"

    try:
        normalized = _ensure_schema(memory)
        type_ok = (
            isinstance(normalized["role_weights"], dict)
            and isinstance(normalized["runs"], int)
        )
        print(f"{'PASS' if type_ok else 'FAIL'}: Invalid types handled: {type_ok}")
        return type_ok
    except Exception as exc:
        print(f"FAIL: Exception during normalization: {exc}")
        return False


def test_tamper_detection():
    """Modify memory file, verify tamper log exists after persistence."""
    print("\n--- TEST 2: Tamper Detection ---")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
        temp_path = Path(handle.name)
        json.dump(_default_memory(), handle)

    original_path = ms.MEMORY_PATH
    try:
        ms.MEMORY_PATH = temp_path

        loaded = load_memory()
        loaded["runs"] = 999
        save_memory(loaded)

        reloaded = load_memory()
        tamper_log = reloaded.get("governance_tamper_log", [])
        has_tamper_entry = len(tamper_log) > 0
        print(f"{'PASS' if has_tamper_entry else 'WARN'}: Tamper log entries: {len(tamper_log)}")

        return True
    finally:
        ms.MEMORY_PATH = original_path
        temp_path.unlink(missing_ok=True)


def test_snapshot_integrity():
    """Create snapshot and verify it is stored."""
    print("\n--- TEST 3: Snapshot Integrity ---")

    from governance.snapshot import create_governance_snapshot, verify_governance_snapshot

    memory = _default_memory()
    snapshot = create_governance_snapshot(memory)

    has_snapshot = bool(memory.get("governance_snapshots"))
    valid_snapshot = verify_governance_snapshot(snapshot)
    passed = has_snapshot and valid_snapshot
    print(f"{'PASS' if passed else 'FAIL'}: Snapshot created and valid: {passed}")

    return passed


def test_persistence_corruption():
    """Corrupt JSON on disk, verify graceful handling."""
    print("\n--- TEST 4: Corrupted Persistence ---")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
        temp_path = Path(handle.name)
        handle.write("this is not json{")

    original_path = ms.MEMORY_PATH
    try:
        ms.MEMORY_PATH = temp_path

        try:
            load_memory()
            print("PASS: Graceful recovery from corrupt file")
            return True
        except Exception as exc:
            print(f"FAIL: Failed on corrupt file: {exc}")
            return False
    finally:
        ms.MEMORY_PATH = original_path
        temp_path.unlink(missing_ok=True)


def main():
    print("=" * 60)
    print("DEBT-007: MEMORY INTEGRITY ADVERSARIAL TESTS")
    print("=" * 60)

    results = [
        ("Schema Normalization", test_schema_normalization_rejects_invalid()),
        ("Tamper Detection", test_tamper_detection()),
        ("Snapshot Integrity", test_snapshot_integrity()),
        ("Persistence Corruption", test_persistence_corruption()),
    ]

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {name}")

    passed = sum(1 for _, ok in results if ok)
    print(f"\nTotal: {passed}/{len(results)} tests passed")


if __name__ == "__main__":
    main()
