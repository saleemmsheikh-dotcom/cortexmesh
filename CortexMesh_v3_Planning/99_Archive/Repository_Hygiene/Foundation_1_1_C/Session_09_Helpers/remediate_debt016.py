#!/usr/bin/env python3
"""
DEBT-016 Remediation: Orchestrator Coverage Expansion
Charter Reference: P0 Audit Charter v1.1 DEBT-016
Target: >=80% coverage of anchored functions
"""

import subprocess
import sys


def run_coverage():
    """Run coverage with orchestrator focus."""
    cmd = [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--source=orchestrator",
        "-m",
        "unittest",
        "discover",
        "tests",
        "-v",
    ]

    print("Running tests with coverage...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    print("\n" + "=" * 60)
    print("ORCHESTRATOR COVERAGE DETAIL")
    print("=" * 60)

    report_cmd = [
        sys.executable,
        "-m",
        "coverage",
        "report",
        "-m",
        "--include=orchestrator.py",
    ]
    report = subprocess.run(report_cmd, capture_output=True, text=True)
    print(report.stdout)
    if report.stderr:
        print("STDERR:", report.stderr)

    html_cmd = [
        sys.executable,
        "-m",
        "coverage",
        "html",
        "--include=orchestrator.py",
    ]
    html = subprocess.run(html_cmd, capture_output=True, text=True)
    if html.stdout:
        print(html.stdout)
    if html.stderr:
        print("STDERR:", html.stderr)
    print("\nHTML report generated: htmlcov/index.html")

    lines = report.stdout.strip().split("\n")
    for line in lines:
        if "orchestrator.py" in line:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    coverage = float(parts[3].rstrip("%"))
                    print(f"\nCurrent orchestrator coverage: {coverage}%")
                    print("Target: 80%")
                    print(f"Gap: {max(0, 80 - coverage)}%")
                    return coverage
                except ValueError:
                    pass

    return None


def identify_uncovered_lines():
    """List anchored functions whose line coverage requires review."""
    anchored = [
        "orchestrate",
        "build_selection_weights",
        "weighted_agents",
        "add_noise",
        "solver.act loop",
        "critic.review loop",
        "authority.resolve",
        "memory update section",
    ]

    print("\n" + "=" * 60)
    print("ANCHORED FUNCTIONS COVERAGE STATUS")
    print("=" * 60)

    for func in anchored:
        print(f"PENDING REVIEW: {func}: coverage status requires htmlcov/index.html review")

    return anchored


def main():
    print("=" * 60)
    print("DEBT-016: ORCHESTRATOR COVERAGE EXPANSION")
    print("=" * 60)

    coverage = run_coverage()
    anchored = identify_uncovered_lines()

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Review htmlcov/index.html for uncovered lines")
    print("2. Identify which anchored functions have gaps")
    print("3. Write tests targeting uncovered branches:")
    print("   - random activation skip, line 262")
    print("   - refinement loop, lines 324-329")
    print("   - entropy_correction path")
    print("   - fallback solver activation")
    print("4. Re-run coverage until >=80% achieved")

    return {"coverage": coverage, "anchored": anchored}


if __name__ == "__main__":
    main()
