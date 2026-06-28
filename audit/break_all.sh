#!/bin/sh
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
MODE=${1:-safe}

if [ "$MODE" = "--live" ]; then
    if [ "${CORTEX_ALLOW_DESTRUCTIVE_AUDIT:-}" != "YES" ]; then
        echo "Refusing live destructive audit."
        echo "Set CORTEX_ALLOW_DESTRUCTIVE_AUDIT=YES and pass --live to proceed."
        exit 2
    fi

    TARGET_ROOT=$PROJECT_ROOT
    OUTSIDE_PATH=$(dirname "$PROJECT_ROOT")/outside_root.txt
    echo "WARNING: attacking real working-copy state at $TARGET_ROOT"
else
    TARGET_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/cortexmesh-break-all.XXXXXX")
    OUTSIDE_PATH=$(dirname "$TARGET_ROOT")/outside_root.txt
    mkdir -p "$TARGET_ROOT/memory"
    cp "$PROJECT_ROOT/memory/memory.json" "$TARGET_ROOT/memory/memory.json"

    cleanup() {
        rm -f "$OUTSIDE_PATH"
        rm -rf "$TARGET_ROOT"
    }

    trap cleanup EXIT INT TERM
    echo "Safe mode: attacking temporary state at $TARGET_ROOT"
fi

cd "$TARGET_ROOT"

PYTHONPATH="$PROJECT_ROOT${PYTHONPATH:+:$PYTHONPATH}" python3 - "$OUTSIDE_PATH" <<'PY'
import importlib
import json
import sys
from pathlib import Path

outside_path = Path(sys.argv[1])

# Attempt 1: Direct memory write
with open("memory/memory.json", "w") as file:
    json.dump({"hacked": True}, file)

# Attempt 2: Dynamic import capability
memory_store = importlib.import_module("memory.memory_store")

# Attempt 3: Filesystem escape
outside_path.write_text("bypassed")

print({
    "direct_memory_write": json.loads(Path("memory/memory.json").read_text()) == {"hacked": True},
    "dynamic_import": memory_store.__name__ == "memory.memory_store",
    "filesystem_escape": outside_path.exists(),
})
PY
