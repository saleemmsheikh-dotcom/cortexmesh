#!/usr/bin/env python3
"""
DEBT-016: Orchestrator Coverage
DEBT-006: Scoring Pipeline Coverage
"""

import subprocess
import sys


def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result


def run_coverage():
    """Generate coverage report for orchestrator and scorer."""
    cmd = [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--source=orchestrator,competition.scorer,memory.memory_store,core.external_runner",
        "-m",
        "unittest",
        "discover",
        "tests",
    ]

    print("Running tests with coverage...")
    run_command(cmd)

    print("\n" + "=" * 60)
    print("COVERAGE REPORT")
    print("=" * 60)
    run_command([sys.executable, "-m", "coverage", "report", "-m"])

    print("\n" + "=" * 60)
    print("ORCHESTRATOR DETAIL")
    print("=" * 60)
    run_command([
        sys.executable,
        "-m",
        "coverage",
        "report",
        "-m",
        "--include=orchestrator.py",
    ])

    print("\n" + "=" * 60)
    print("SCORER DETAIL")
    print("=" * 60)
    run_command([
        sys.executable,
        "-m",
        "coverage",
        "report",
        "-m",
        "--include=competition/scorer.py",
    ])


if __name__ == "__main__":
    run_coverage()
