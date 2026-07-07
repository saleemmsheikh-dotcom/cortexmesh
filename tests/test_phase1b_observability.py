import sys
import unittest
from pathlib import Path


PHASE1B_PATH = (
    Path(__file__).resolve().parents[1]
    / "CortexMesh_v3_Planning"
    / "06_Implementation_Execution"
    / "Phase1B"
)
if str(PHASE1B_PATH) not in sys.path:
    sys.path.insert(0, str(PHASE1B_PATH))

from local_ai import (  # noqa: E402
    EVENT_CAPABILITY_DISCOVERY,
    EVENT_HEALTH_CHECK,
    EVENT_PROVIDER_LIFECYCLE,
    EVENT_REQUEST_TIMING,
    EVENT_RESPONSE_TIMING,
    LocalAIEvent,
    LocalAIRequest,
    LocalAIResponse,
    LocalAITelemetryBuffer,
    capability_discovery_event,
    health_check_event,
    new_trace_id,
    provider_lifecycle_event,
    request_timing_event,
    response_timing_event,
)
from local_ai.provider import ConnectionCheck  # noqa: E402


FORBIDDEN_KEYS = {"authority", "confidence", "rank", "score", "vote_weight"}


class TestPhase1BObservability(unittest.TestCase):
    def test_local_ai_event_is_informational_only(self):
        event = LocalAIEvent(
            event_type="test",
            trace_id="trace-1",
            correlation_id="corr-1",
            provider="ollama",
            diagnostics={
                "detail": "kept",
                "score": 10,
                "authority": "forbidden",
            },
        )

        exported = event.as_dict()

        self.assertTrue(exported["informational_only"])
        self.assertFalse(exported["ranking_used"])
        self.assertEqual(exported["diagnostics"], {"detail": "kept"})
        for key in FORBIDDEN_KEYS:
            self.assertNotIn(key, exported)
            self.assertNotIn(key, exported["diagnostics"])

    def test_trace_ids_are_unique_and_prefixed(self):
        first = new_trace_id("phase1b")
        second = new_trace_id("phase1b")

        self.assertTrue(first.startswith("phase1b-"))
        self.assertTrue(second.startswith("phase1b-"))
        self.assertNotEqual(first, second)

    def test_provider_lifecycle_event(self):
        event = provider_lifecycle_event(
            provider="ollama",
            status="initialized",
            trace_id="trace-1",
            correlation_id="corr-1",
        )

        exported = event.as_dict()

        self.assertEqual(exported["event_type"], EVENT_PROVIDER_LIFECYCLE)
        self.assertEqual(exported["provider"], "ollama")
        self.assertEqual(exported["status"], "initialized")

    def test_capability_discovery_event_sorts_capabilities(self):
        event = capability_discovery_event(
            capabilities=["health_check", "text_generation", "health_check"],
            trace_id="trace-1",
            correlation_id="corr-1",
            provider="ollama",
        )

        exported = event.as_dict()

        self.assertEqual(exported["event_type"], EVENT_CAPABILITY_DISCOVERY)
        self.assertEqual(exported["diagnostics"]["capabilities"], ["health_check", "text_generation"])
        self.assertFalse(exported["ranking_used"])

    def test_health_check_event_exports_structured_diagnostics(self):
        check = ConnectionCheck(
            provider="ollama",
            model="model",
            endpoint_ref="http://localhost:11434/api/tags",
            ok=True,
            status="connected",
            latency_ms=5,
            diagnostics={"model_count": 1, "confidence": 0.9},
        )

        event = health_check_event(check, trace_id="trace-1", correlation_id="corr-1")
        exported = event.as_dict()

        self.assertEqual(exported["event_type"], EVENT_HEALTH_CHECK)
        self.assertEqual(exported["provider"], "ollama")
        self.assertEqual(exported["model"], "model")
        self.assertEqual(exported["latency_ms"], 5)
        self.assertTrue(exported["diagnostics"]["ok"])
        self.assertEqual(exported["diagnostics"]["endpoint_ref"], "http://localhost:11434/api/tags")
        self.assertNotIn("confidence", exported["diagnostics"])

    def test_request_and_response_timing_events(self):
        request = LocalAIRequest(
            prompt="hello",
            model="model",
            request_id="REQ-1",
            objective_ref="OBJ-1",
            metadata={"purpose": "test", "vote_weight": 9},
        )
        response = LocalAIResponse(
            request_id="REQ-1",
            provider="ollama",
            model="model",
            content="world",
            status="complete",
            latency_ms=12,
            finish_reason="done",
            diagnostics={"endpoint_ref": "test://generate", "rank": 1},
        )

        request_event = request_timing_event(
            request,
            provider="ollama",
            trace_id="trace-1",
            correlation_id="corr-1",
        )
        response_event = response_timing_event(
            response,
            trace_id="trace-1",
            correlation_id="corr-1",
        )

        request_export = request_event.as_dict()
        response_export = response_event.as_dict()

        self.assertEqual(request_export["event_type"], EVENT_REQUEST_TIMING)
        self.assertEqual(request_export["request_id"], "REQ-1")
        self.assertEqual(request_export["status"], "started")
        self.assertEqual(request_export["diagnostics"], {"purpose": "test"})
        self.assertEqual(response_export["event_type"], EVENT_RESPONSE_TIMING)
        self.assertEqual(response_export["status"], "complete")
        self.assertEqual(response_export["latency_ms"], 12)
        self.assertEqual(response_export["diagnostics"]["finish_reason"], "done")
        self.assertNotIn("rank", response_export["diagnostics"])

    def test_telemetry_buffer_exports_diagnostics(self):
        buffer = LocalAITelemetryBuffer()
        buffer.record(
            provider_lifecycle_event(
                provider="ollama",
                status="initialized",
                trace_id="trace-1",
                correlation_id="corr-1",
            )
        )
        buffer.extend(
            [
                capability_discovery_event(
                    ["text_generation"],
                    trace_id="trace-1",
                    correlation_id="corr-1",
                )
            ]
        )

        exported = buffer.export_diagnostics()

        self.assertEqual(exported["event_count"], 2)
        self.assertTrue(exported["telemetry_is_informational_only"])
        self.assertFalse(exported["ranking_used"])
        self.assertEqual(len(buffer.events()), 2)
        for key in FORBIDDEN_KEYS:
            self.assertNotIn(key, exported)


if __name__ == "__main__":
    unittest.main()
