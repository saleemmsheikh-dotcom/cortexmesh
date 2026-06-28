from testing.common import run_tasks, specialist_rates


def _prompts():
    return (
        ["research"] * 10
        + ["engineering"] * 10
        + ["systems"] * 10
    )


def run(seed=6804):
    results, crashes = run_tasks(_prompts(), seed=seed)
    passed = sum(
        item["winner_family"] == {
            "research": "Researcher",
            "engineering": "Engineer",
            "systems": "Architect",
        }[item["task_type"]]
        for item in results
    )
    total = len(_prompts())

    return {
        "name": "regression",
        "runs_requested": total,
        "runs_completed": len(results),
        "crashes": crashes,
        "specialist_win_rates": specialist_rates(results),
        "regression_pass_rate": passed / total if total else 0,
        "results": results,
    }
