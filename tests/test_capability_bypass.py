import importlib.util
import tempfile
import unittest
from pathlib import Path

from core.contracts import CapabilityContext


class CapabilityBypassTests(unittest.TestCase):

    def test_capability_cannot_write_filesystem(self):
        """Capabilities must not be able to write arbitrary filesystem paths."""
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            capability_path = directory / "filesystem_probe.py"
            target_path = directory / "capability_write.txt"
            capability_path.write_text(
                "from pathlib import Path\n"
                "\n"
                "def run(context):\n"
                f"    Path({str(target_path)!r}).write_text('bypass')\n"
            )
            spec = importlib.util.spec_from_file_location(
                "filesystem_probe",
                capability_path,
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            result = CapabilityContext(
                {},
                "filesystem probe",
                trust_level="core",
            ).execute_capability(
                module.run
            )

            self.assertFalse(
                target_path.exists(),
                "Capability escaped its boundary and wrote to the filesystem.",
            )
            self.assertTrue(
                result["blocked"],
                "Capability sandbox did not report the blocked filesystem write.",
            )


if __name__ == "__main__":
    unittest.main()
