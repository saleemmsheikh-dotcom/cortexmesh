#!/usr/bin/env python3
"""
DEBT-006: Verify authority consumes scorer output without recomputation.
"""

import ast
from pathlib import Path


SCORER = Path("competition/scorer.py")
AUTHORITY = Path("agents/authority.py")


def find_recomputation(filepath):
    """Check if authority recalculates weighted totals."""
    if not filepath.exists():
        print(f"WARN: {filepath} not found; skipping authority check")
        return []

    tree = ast.parse(filepath.read_text(), filename=str(filepath))

    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "compute_total_score":
                issues.append({
                    "line": node.lineno,
                    "issue": "Authority calls compute_total_score; potential recomputation",
                })
            if isinstance(func, ast.Attribute) and func.attr == "compute_total_score":
                issues.append({
                    "line": node.lineno,
                    "issue": "Authority calls compute_total_score; potential recomputation",
                })

    return issues


def verify_scorer_exports():
    """Verify scorer exports canonical functions."""
    content = SCORER.read_text()
    required = ["compute_total_score", "score_solution", "score"]
    return {name: f"def {name}(" in content for name in required}


def authority_consumes_weighted_total():
    content = AUTHORITY.read_text()
    return 'scores.get("weighted_total"' in content or "scores.get('weighted_total'" in content


def main():
    print("=" * 60)
    print("DEBT-006: SCORING PIPELINE VERIFICATION")
    print("=" * 60)

    print("\n--- 1. SCORER EXPORTS ---")
    exports = verify_scorer_exports()
    for name, found in exports.items():
        print(f"{'PASS' if found else 'FAIL'}: {name}()")

    print("\n--- 2. AUTHORITY RECOMPUTATION CHECK ---")
    issues = find_recomputation(AUTHORITY)
    if issues:
        for issue in issues:
            print(f"WARN: Line {issue['line']}: {issue['issue']}")
    else:
        print("PASS: No compute_total_score calls found in authority")

    print("\n--- 3. PIPELINE FLOW ---")
    scorer_content = SCORER.read_text()
    pipeline_ok = "compute_total_score" in scorer_content and "score_solution" in scorer_content
    print(f"{'PASS' if pipeline_ok else 'FAIL'}: score_solution -> compute_total_score chain exists")

    print("\n--- 4. ADR-004 VERIFICATION ---")
    consumes = authority_consumes_weighted_total()
    print(f"{'PASS' if consumes else 'FAIL'}: authority.decide() consumes scores['weighted_total']")

    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
