"""Template for a CortexMesh LocalAIProvider adapter.

Copy this file when starting a new provider adapter. The template is not
imported by runtime code.
"""

from __future__ import annotations

import time
from typing import Any, Mapping

from local_ai import LocalAIConfig
from local_ai.provider import ConnectionCheck, LocalAIRequest, LocalAIResponse


class ExampleProvider:
    """Example LocalAIProvider skeleton."""

    provider_name = "example"

    def name(self) -> str:
        return self.provider_name

    def validate_config(self, config: LocalAIConfig) -> None:
        config.validate({self.provider_name})

    def check_connection(self, config: LocalAIConfig) -> ConnectionCheck:
        self.validate_config(config)
        started = time.monotonic()

        try:
            payload = self._health_request(config)
            model_available = self._model_available(payload, config.model)
            return ConnectionCheck(
                provider=self.provider_name,
                model=config.model,
                endpoint_ref=self._endpoint(config, "/health"),
                ok=True,
                status="connected",
                latency_ms=self._elapsed_ms(started),
                diagnostics={
                    "model_available": model_available,
                    "model_count": self._model_count(payload),
                },
            )
        except Exception as exc:
            return ConnectionCheck(
                provider=self.provider_name,
                model=config.model,
                endpoint_ref=self._endpoint(config, "/health"),
                ok=False,
                status="failed",
                latency_ms=self._elapsed_ms(started),
                error=str(exc),
            )

    def generate(self, request: LocalAIRequest, config: LocalAIConfig) -> LocalAIResponse:
        self.validate_config(config)
        request.validate()
        endpoint = self._endpoint(config, "/generate")
        started = time.monotonic()
        raw_response = self._generate_request(request, config, endpoint)
        return self.normalize_response(
            raw_response,
            request,
            config,
            endpoint,
            self._elapsed_ms(started),
        )

    def normalize_response(
        self,
        raw_response: Mapping[str, Any],
        request: LocalAIRequest,
        config: LocalAIConfig,
        endpoint_ref: str,
        latency_ms: int,
    ) -> LocalAIResponse:
        content = raw_response.get("content")
        if not isinstance(content, str):
            raise ValueError("invalid provider response: missing string content")

        return LocalAIResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model=str(raw_response.get("model") or config.model),
            content=content,
            status="complete",
            latency_ms=latency_ms,
            usage={},
            finish_reason=str(raw_response.get("finish_reason") or "complete"),
            diagnostics={"endpoint_ref": endpoint_ref},
        )

    def _health_request(self, config: LocalAIConfig) -> Mapping[str, Any]:
        raise NotImplementedError

    def _generate_request(
        self,
        request: LocalAIRequest,
        config: LocalAIConfig,
        endpoint: str,
    ) -> Mapping[str, Any]:
        raise NotImplementedError

    def _endpoint(self, config: LocalAIConfig, path: str) -> str:
        return f"{config.normalized_base_url}{path}"

    def _model_available(self, payload: Mapping[str, Any], model: str) -> bool | None:
        return None

    def _model_count(self, payload: Mapping[str, Any]) -> int:
        return 0

    def _elapsed_ms(self, started: float) -> int:
        return int((time.monotonic() - started) * 1000)
