from agents.base import BaseAgent
from engine.model_router import call_model


class ReviewerAgent(BaseAgent):

    def __init__(self, role="logic"):
        super().__init__(f"{role}_critic", role)

    def _role_prompt(self):

        if self.role == "logic":
            return """
You are a Logic Critic.

Evaluate:
- internal consistency
- assumptions
- reasoning quality

Return only the most important weaknesses.
"""

        if self.role == "risk":
            return """
You are a Risk Critic.

Evaluate:
- failure modes
- operational risks
- edge cases

Return only the most important risks.
"""

        if self.role == "completeness":
            return """
You are a Completeness Critic.

Evaluate:
- missing elements
- blind spots
- omitted considerations

Return only the most important omissions.
"""

        return """
You are a reviewer.
Identify weaknesses.
"""

    def review(self, solution):
        raw = call_model(
            self._role_prompt(),
            solution["solution"]
        )

        # extract "action signal"
        return {
            "critic": self.role,
            "review": raw,
            "signal": f"refine:{self.role}"
        }
