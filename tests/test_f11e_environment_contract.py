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
    EXPECTED_DEFAULT = ("pytest>=7.0.0", "coverage>=7.0.0")
    EXPECTED_OPENAI = ("-r requirements.txt", "openai>=1.0.0")
    EXPECTED_CONSTRAINTS = (
        "annotated-types==0.7.0",
        "anyio==4.14.2",
        "certifi==2026.6.17",
        "coverage==7.15.2",
        "distro==1.9.0",
        "h11==0.16.0",
        "httpcore==1.0.9",
        "httpx==0.28.1",
        "idna==3.18",
        "iniconfig==2.3.0",
        "jiter==0.16.0",
        "openai==2.46.0",
        "packaging==26.2",
        "pluggy==1.6.0",
        "pydantic==2.13.4",
        "pydantic-core==2.46.4",
        "pygments==2.20.0",
        "pytest==9.1.1",
        "sniffio==1.3.1",
        "tqdm==4.68.4",
        "typing-extensions==4.16.0",
        "typing-inspection==0.4.2",
    )

    @staticmethod
    def declarations(path: Path) -> tuple[str, ...]:
        return tuple(
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )

    def test_default_declarations_are_exact(self):
        self.assertEqual(self.declarations(REQUIREMENTS), self.EXPECTED_DEFAULT)

    def test_openai_declarations_are_exact(self):
        self.assertEqual(self.declarations(OPENAI_REQUIREMENTS), self.EXPECTED_OPENAI)

    def test_constraints_are_exact(self):
        self.assertEqual(self.declarations(CONSTRAINTS), self.EXPECTED_CONSTRAINTS)

    def test_constraints_are_sorted_and_unique(self):
        declarations = self.declarations(CONSTRAINTS)
        names = tuple(line.split("==", 1)[0].lower() for line in declarations)
        self.assertEqual(names, tuple(sorted(set(names))))

    def test_constraints_provenance_is_present(self):
        content = CONSTRAINTS.read_text(encoding="utf-8")
        for value in (
            "CPython 3.14.6",
            "pip 26.1.2",
            "ubuntu-latest",
            "29565319116",
            "dace93dc68c1f8b793456da6f19a66bda4e2a87d",
        ):
            self.assertIn(value, content)

    def test_constraints_reject_prohibited_sources(self):
        declarations = self.declarations(CONSTRAINTS)
        prohibited = ("-e ", "--editable", "://", "--index", " @ ", "file:")
        for declaration in declarations:
            for marker in prohibited:
                self.assertNotIn(marker, declaration)
        self.assertTrue(all("==" in line for line in declarations))

    def test_default_profile_does_not_declare_openai(self):
        self.assertNotIn("openai", REQUIREMENTS.read_text(encoding="utf-8").lower())

    def test_external_services_are_not_pip_dependencies(self):
        combined = (
            REQUIREMENTS.read_text(encoding="utf-8")
            + OPENAI_REQUIREMENTS.read_text(encoding="utf-8")
        ).lower()
        for service in ("ollama", "lmstudio", "docker"):
            self.assertNotIn(service, combined)


@unittest.skipUnless(CONSTRAINTS.exists(), "W3 CI constraints not yet present")
class WorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gates = GATES.read_text(encoding="utf-8")
        cls.observations = OBSERVATIONS.read_text(encoding="utf-8")
        cls.combined = cls.gates + cls.observations

    def test_default_installs_use_constraints(self):
        unconstrained = "python -m pip install -r requirements.txt"
        constrained = (
            "python -m pip install \\\n"
            "            -c constraints/cpython314-ubuntu.txt \\\n"
            "            -r requirements.txt"
        )
        self.assertNotIn(unconstrained, self.combined)
        self.assertEqual(self.combined.count(constrained), 3)

    def test_cache_inputs_cover_all_dependency_profiles(self):
        for path in (
            "requirements.txt",
            "requirements-openai.txt",
            "constraints/cpython314-ubuntu.txt",
        ):
            self.assertGreaterEqual(self.combined.count(path), 3)

    def test_workflows_record_all_dependency_input_hashes(self):
        for path in (
            "requirements.txt",
            "requirements-openai.txt",
            "constraints/cpython314-ubuntu.txt",
        ):
            self.assertGreaterEqual(
                self.combined.count(f"shasum -a 256 {path}"),
                3,
            )

    def test_python_and_action_pins_remain_exact(self):
        self.assertEqual(self.combined.count('python-version: "3.14"'), 4)
        self.assertEqual(
            self.combined.count(
                "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5"
            ),
            6,
        )
        self.assertEqual(
            self.combined.count(
                "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1"
            ),
            4,
        )
        self.assertEqual(
            self.combined.count(
                "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"
            ),
            2,
        )
        self.assertIn("python -m pip install pip-audit==2.10.1", self.observations)

    def test_workflow_jobs_and_permissions_remain_exact(self):
        for job in (
            "  scope:",
            "  whitespace:",
            "  compile:",
            "  regression:",
        ):
            self.assertIn(job, self.gates)
        for job in ("  coverage:", "  dependency-audit:"):
            self.assertIn(job, self.observations)
        self.assertEqual(self.combined.count("permissions:\n  contents: read"), 2)

    def test_canonical_regression_and_observations_remain(self):
        self.assertIn(
            "run: PYTHONDONTWRITEBYTECODE=1 python -m unittest discover tests",
            self.gates,
        )
        self.assertIn("python tools/audit/audit_coverage.py", self.observations)
        self.assertIn("--requirement requirements.txt", self.observations)
        self.assertIn("Policy: descriptive", self.observations)

    def test_no_openai_install_or_provider_execution_in_ci(self):
        self.assertNotIn("-r requirements-openai.txt", self.combined)
        self.assertNotIn("OPENAI_API_KEY", self.combined)
        self.assertNotIn("import openai", self.combined)


if __name__ == "__main__":
    unittest.main()
