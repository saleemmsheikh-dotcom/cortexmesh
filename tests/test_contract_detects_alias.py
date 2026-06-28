import tempfile
import unittest
from pathlib import Path

from core.contracts import validate_capability_source


class ContractAliasTests(unittest.TestCase):

    def test_contract_detects_writes_to_memory_alias(self):
        """Protected-memory writes through aliases must be rejected."""
        with tempfile.TemporaryDirectory() as directory:
            capability_path = Path(directory) / "alias_probe.py"
            capability_path.write_text(
                "def run(context):\n"
                "    mem = context.memory\n"
                "    mem['governance_frozen'] = False\n"
            )

            violations = validate_capability_source(capability_path)

            self.assertTrue(
                violations,
                "Contract scan failed to detect a protected write through an alias.",
            )


if __name__ == "__main__":
    unittest.main()
