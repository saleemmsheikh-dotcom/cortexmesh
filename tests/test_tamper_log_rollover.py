import unittest

from governance.tamper_log import log_governance_event, verify_tamper_log


class TamperLogRolloverTests(unittest.TestCase):

    def test_tamper_log_maintains_hash_chain_past_500(self):
        """Rolling retention must preserve a verifiable tamper-log chain."""
        memory = {"governance_tamper_log": []}

        for index in range(502):
            log_governance_event(memory, {
                "type": "rollover_probe",
                "index": index,
            })

        self.assertEqual(
            verify_tamper_log(memory),
            [],
            "Tamper-log retention broke the hash chain after rollover.",
        )


if __name__ == "__main__":
    unittest.main()
