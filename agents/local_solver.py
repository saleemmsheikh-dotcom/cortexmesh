from agents.base import BaseAgent


class LocalSolverAgent(BaseAgent):

    def __init__(self, name, role="general"):
        super().__init__(name, role)

    def act(self, task, ledger):
        if self.role == "architect":
            return {
                "agent": self.name,
                "solution": (
                    "SYSTEMS VIEW\n"
                    "- Model system components\n"
                    "- Define constraints\n"
                    "- Identify dependencies\n"
                    "- Design for stability\n"
                    "- Optimise interactions"
                )
            }

        if self.role == "researcher":
            return {
                "agent": self.name,
                "solution": (
                    "RESEARCH VIEW\n"
                    "- Compare known approaches\n"
                    "- Identify alternatives\n"
                    "- Evaluate evidence\n"
                    "- Review trade-offs\n"
                    "- Select best precedent"
                )
            }

        if self.role == "engineer":
            return {
                "agent": self.name,
                "solution": (
                    "ENGINEERING VIEW\n"
                    "- Break into steps\n"
                    "- Define implementation path\n"
                    "- Reduce complexity\n"
                    "- Validate feasibility\n"
                    "- Iterate solution"
                )
            }

        return {
            "agent": self.name,
            "solution": (
                "GENERAL VIEW\n"
                "- Define objectives\n"
                "- Allocate resources\n"
                "- Measure outcomes"
            )
        }
