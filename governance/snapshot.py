import copy
import hashlib
import json
from datetime import datetime, timezone

GOVERNANCE_KEYS = [
    "strategy_registry",
    "governance_actions",
    "governance_violations",
    "governance_tamper_log"
]


def compute_snapshot_hash(snapshot):
    clean = {
        key: value
        for key, value in snapshot.items()
        if key != "hash"
    }
    payload = json.dumps(clean, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_governance_snapshot(snapshot):
    return snapshot.get("hash") == compute_snapshot_hash(snapshot)


def migrate_legacy_snapshots(memory):
    snapshots = memory.get("governance_snapshots", [])

    if not snapshots or any("hash" in snapshot for snapshot in snapshots):
        return False

    for snapshot in snapshots:
        snapshot["hash"] = compute_snapshot_hash(snapshot)

    return True


def create_governance_snapshot(memory):
    memory.setdefault("governance_snapshots", [])

    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "state": {
            key: copy.deepcopy(memory.get(key))
            for key in GOVERNANCE_KEYS
        }
    }
    snapshot["hash"] = compute_snapshot_hash(snapshot)

    memory["governance_snapshots"].append(snapshot)
    memory["governance_snapshots"] = memory["governance_snapshots"][-10:]

    return snapshot


def restore_latest_governance_snapshot(memory):
    snapshots = memory.get("governance_snapshots", [])

    if not snapshots:
        return False

    latest = next(
        (
            snapshot
            for snapshot in reversed(snapshots)
            if verify_governance_snapshot(snapshot)
        ),
        None,
    )

    if latest is None:
        memory.setdefault("governance_actions", []).append({
            "action": "rollback_failed",
            "reason": "no valid snapshot"
        })
        return False

    for key, value in latest["state"].items():
        memory[key] = copy.deepcopy(value)

    memory.setdefault("governance_actions", []).append({
        "action": "rollback",
        "source": latest["timestamp"]
    })
    return True
