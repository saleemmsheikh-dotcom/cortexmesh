import argparse

from engine.runner import run_task


DEFAULT_TASK = "Design a simple optimisation strategy for resource allocation"


def parse_args():
    parser = argparse.ArgumentParser(description="Run a CortexMesh task.")
    parser.add_argument("task", nargs="*", help="Task to send to the solver agents.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    task = " ".join(args.task).strip() or DEFAULT_TASK

    try:
        result = run_task(task)
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print("\n===== FINAL RESULT =====\n")
    print(result["final"])

    print("\n===== MEMORY STATE =====\n")
    print(result["memory"])
