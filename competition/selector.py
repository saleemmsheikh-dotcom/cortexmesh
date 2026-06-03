from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from competition.scorer import score

def select_best(solutions, ledger):
    if not solutions:
        raise ValueError("Cannot select a best solution from an empty list.")

    ranked = []

    for sol in solutions:
        ranked.append((score(sol), sol))

    ranked.sort(key=lambda x: x[0], reverse=True)

    return ranked[0][1]


if __name__ == "__main__":
    demo = [{"agent": "demo", "solution": "A practical solution with enough detail to score well."}]
    print(select_best(demo, None))
