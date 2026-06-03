import os

from config.mode import ModeConfig


def check_api_available():
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        return False

    if key == "sk-your-real-key":
        return False

    return True


def get_mode(budget):

    api_ok = check_api_available()
    budget_ok = not budget.exceeded()

    return ModeConfig.get_mode(
        api_available=api_ok,
        budget_ok=budget_ok
    )