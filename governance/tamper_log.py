import hashlib
import json
from datetime import datetime, timezone


MAX_TAMPER_LOG_ENTRIES = 500


def canonical_json(data):
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )


def compute_hash(record):
    clean = {
        key: value
        for key, value in record.items()
        if key != "hash"
    }
    payload = canonical_json(clean)

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


def get_last_hash(memory):
    log = memory.get("governance_tamper_log", [])

    if not log:
        return None

    return log[-1].get("hash")


def log_governance_event(memory, event):
    memory.setdefault("governance_tamper_log", [])

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prev_hash": get_last_hash(memory),
        **event
    }
    record["hash"] = compute_hash(record)

    log = memory["governance_tamper_log"]
    log.append(record)

    if len(log) > MAX_TAMPER_LOG_ENTRIES:
        removed_count = len(log) - MAX_TAMPER_LOG_ENTRIES
        removed = log[:removed_count]
        memory["governance_tamper_anchor"] = removed[-1].get("hash")
        log = log[removed_count:]

    memory["governance_tamper_log"] = log

    return record


def verify_tamper_log(memory):
    log = memory.get("governance_tamper_log", [])
    previous_hash = memory.get("governance_tamper_anchor")
    issues = []

    for index, record in enumerate(log):
        expected_prev = previous_hash

        if record.get("prev_hash") != expected_prev:
            issues.append({
                "index": index,
                "error": "prev_hash_mismatch"
            })

        expected_hash = compute_hash(record)

        if record.get("hash") != expected_hash:
            issues.append({
                "index": index,
                "error": "hash_mismatch"
            })

        previous_hash = record.get("hash")

    return issues


def migrate_legacy_tamper_log(memory):
    log = memory.get("governance_tamper_log", [])

    if not log or any("hash" in record for record in log):
        return False

    previous_hash = None

    for record in log:
        record["prev_hash"] = previous_hash
        record["hash"] = compute_hash(record)
        previous_hash = record["hash"]

    return True
