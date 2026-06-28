import unittest

from core.contracts import SecurityBoundaryViolation, execute_capability


class ExternalCapabilityBoundaryTests(unittest.TestCase):

    def test_external_capability_cannot_run_in_process(self):
        with self.assertRaises(SecurityBoundaryViolation):
            execute_capability(
                "untrusted.module",
                bypass_runner=True,
            )


if __name__ == "__main__":
    unittest.main()
