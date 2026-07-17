#!/usr/bin/env python3
"""
DEBT-005 Execution Path Audit
DEBT-001 Determinism Validation
"""

import ast
from pathlib import Path


ORCHESTRATOR = Path("orchestrator.py")
EXTERNAL_RUNNER = Path("core/external_runner.py")


def find_random_usage(filepath):
    """Find all random.* calls in a Python file."""
    source = filepath.read_text()
    tree = ast.parse(source, filename=str(filepath))
    lines = source.splitlines(keepends=True)

    random_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "random"
            ):
                random_calls.append({
                    "line": node.lineno,
                    "call": f"random.{func.attr}(...)",
                    "context": get_context(lines, node.lineno),
                })
    return random_calls


def get_context(lines, lineno, context_lines=2):
    """Get surrounding lines for context."""
    start = max(0, lineno - context_lines - 1)
    end = min(len(lines), lineno + context_lines)
    return "".join(lines[start:end])


def audit_trust_enforcement():
    """Verify ExternalRunner isolation flags."""
    content = EXTERNAL_RUNNER.read_text()

    required_flags = [
        "--network=none",
        "--read-only",
        "--memory=256m",
        "--cpus=0.5",
    ]

    results = []
    for flag in required_flags:
        results.append({
            "flag": flag,
            "present": flag in content,
            "critical": True,
        })

    dangerous = ["--privileged", "-v /var/run/docker.sock"]
    for flag in dangerous:
        results.append({
            "flag": flag,
            "present": flag in content,
            "critical": False,
        })

    return results


def main():
    print("=" * 60)
    print("DEBT-005 / DEBT-001: EXECUTION PATH & DETERMINISM AUDIT")
    print("=" * 60)

    print("\n--- 1. RANDOM USAGE IN ORCHESTRATOR ---")
    random_calls = find_random_usage(ORCHESTRATOR)
    print(f"Found {len(random_calls)} random.* calls:\n")

    for call in random_calls:
        print(f"Line {call['line']}: {call['call']}")
        print(f"Context:\n{call['context']}")
        print("-" * 40)

    if random_calls:
        print(f"\nWARNING: DETERMINISM VIOLATION: {len(random_calls)} random calls in core path")

    print("\n--- 2. EXTERNAL RUNNER ISOLATION FLAGS ---")
    flags = audit_trust_enforcement()
    for flag in flags:
        passed = flag["present"] == flag["critical"]
        status = "PASS" if passed else "FAIL"
        expected = "required" if flag["critical"] else "forbidden"
        print(f"{status}: {flag['flag']} ({expected})")

    print("\n--- 3. EXECUTION PATH SUMMARY ---")
    content = ORCHESTRATOR.read_text()

    key_functions = [
        "build_solvers",
        "build_critics",
        "diversity_boost",
        "add_noise",
        "weighted_agents",
        "update_role_weights",
        "entropy_correction",
        "build_selection_weights",
        "enforce_rotation",
        "spend_budget",
        "orchestrate",
    ]

    for func in key_functions:
        if f"def {func}(" in content:
            print(f"PASS: {func}() defined")
        else:
            print(f"FAIL: {func}() NOT FOUND")

    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
