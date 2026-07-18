from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ENVIRONMENT = ROOT / "ENVIRONMENT.md"
REQUIREMENTS = ROOT / "requirements.txt"
OPENAI_REQUIREMENTS = ROOT / "requirements-openai.txt"
CONSTRAINTS = ROOT / "constraints" / "cpython314-ubuntu.txt"
GATES = ROOT / ".github" / "workflows" / "quality-gates.yml"
OBSERVATIONS = ROOT / ".github" / "workflows" / "quality-observations.yml"
PLANNING = (
    ROOT
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Foundation_1_1"
)


class DocumentationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README.read_text(encoding="utf-8")
        cls.environment = ENVIRONMENT.read_text(encoding="utf-8")

    def test_readme_links_authoritative_environment_guide(self):
        self.assertIn("[ENVIRONMENT.md](ENVIRONMENT.md)", self.readme)
        self.assertIn("# CortexMesh Environment Contract", self.environment)

    def test_verified_profile_is_exact(self):
        for content in (self.readme, self.environment):
            self.assertIn("CPython 3.14", content)
            self.assertIn("Ubuntu CI", content)

    def test_generic_python_compatibility_claim_is_absent(self):
        prohibited = (
            "badge/python-3-",
            "compatible with Python 3",
            "supports Python 3",
            "all Python 3",
        )
        combined = self.readme + self.environment
        for phrase in prohibited:
            self.assertNotIn(phrase, combined)

    def test_observed_and_uncertified_environments_are_distinguished(self):
        self.assertIn("OBSERVED", self.environment)
        self.assertIn("NOT CERTIFIED", self.environment)
        self.assertIn("may be attempted", self.environment)

    def test_repository_root_is_supported_context(self):
        self.assertIn("run every", self.environment)
        self.assertIn("from its root", self.environment)
        self.assertIn("repository root", self.readme)

    def test_verification_precedes_optional_execution(self):
        verification = self.environment.index("## Verification-first fresh clone")
        stateful = self.environment.index("## Stateful CLI contract")
        openai = self.environment.index("## Optional OpenAI profile")
        local_ai = self.environment.index("## Optional Local AI profile")
        docker = self.environment.index("## Docker external-capability limitation")
        self.assertLess(verification, stateful)
        self.assertLess(verification, openai)
        self.assertLess(verification, local_ai)
        self.assertLess(verification, docker)

    def test_canonical_unittest_command_is_exact(self):
        command = "PYTHONDONTWRITEBYTECODE=1 python -m unittest discover tests"
        self.assertIn(command, self.readme)
        self.assertIn(command, self.environment)

    def test_pytest_is_optional_parity(self):
        self.assertIn("Pytest is optional", self.environment)
        self.assertIn("authoritative regression", self.environment)

    def test_state_warning_precedes_cli(self):
        warning = self.readme.index("Stateful CLI warning")
        command = self.readme.index('python3 main.py "Design')
        self.assertLess(warning, command)

    def test_memory_and_backup_mutation_are_disclosed(self):
        for path in ("memory/memory.json", "memory/memory.json.bak"):
            self.assertIn(path, self.readme)
            self.assertIn(path, self.environment)

    def test_destructive_or_relocated_state_guidance_is_absent(self):
        prohibited = (
            "git reset --hard",
            "rm memory/memory.json",
            "delete memory/memory.json",
            "move memory/memory.json",
            "stateless CLI",
        )
        combined = self.readme + self.environment
        for phrase in prohibited:
            self.assertNotIn(phrase, combined)

    def test_local_ai_variables_are_complete(self):
        variables = (
            "CORTEX_LOCAL_AI_ENABLED",
            "CORTEX_LOCAL_AI_PROVIDER",
            "CORTEX_LOCAL_AI_PROVIDER_OPTIONS",
            "CORTEX_LOCAL_AI_BASE_URL",
            "CORTEX_LOCAL_AI_MODEL",
            "CORTEX_LOCAL_AI_TIMEOUT",
            "CORTEX_LOCAL_AI_TEMPERATURE",
            "CORTEX_LOCAL_AI_MAX_TOKENS",
        )
        for variable in variables:
            self.assertIn(variable, self.environment)

    def test_docker_is_separate_and_unprovisioned(self):
        self.assertIn("Docker is not required for the SAFE Local AI bridge", self.environment)
        self.assertIn("does not provide", self.environment)
        self.assertIn("cortexmesh-capability", self.environment)
        self.assertIn("fresh-clone capability-execution guarantee", self.environment)

    def test_no_secret_values_or_packaging_claims(self):
        combined = self.readme + self.environment
        secret_patterns = (
            r"sk-[A-Za-z0-9]{12,}",
            r"OPENAI_API_KEY\s*=\s*\S+",
            r"OPENAI_ADMIN_KEY\s*=\s*\S+",
        )
        for pattern in secret_patterns:
            self.assertIsNone(re.search(pattern, combined))
        self.assertNotIn("pip install cortexmesh", combined.lower())
        self.assertNotIn("pip install -e .", combined.lower())


@unittest.skipUnless(
    OPENAI_REQUIREMENTS.exists() and CONSTRAINTS.exists(),
    "W2 dependency profiles not yet present",
)
class DependencyContractTests(unittest.TestCase):
    pass


@unittest.skipUnless(CONSTRAINTS.exists(), "W3 CI constraints not yet present")
class WorkflowContractTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
