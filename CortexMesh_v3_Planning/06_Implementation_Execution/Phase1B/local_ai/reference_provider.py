"""Deterministic example LocalAIProvider for Phase 2A certification.

This provider performs no network or runtime integration. It exists only as a
copyable implementation example for provider developers.
"""

from __future__ import annotations

import time
from typing import Any, Mapping

from .config import LocalAIConfig
from .provider import ConnectionCheck, LocalAIRequest, LocalAIResponse


class ReferenceProvider:
    """Deterministic, non-production Local AI provider example."""

    provider_name = "reference"
    reference_model = "reference-model"

    def name(self) -> str:
        return self.provider_name

    def validate_config(self, config: LocalAIConfig) -> None:
        config.validate({self.provider_name})

    def check_connection(self, config: LocalAIConfig) -> ConnectionCheck:
        self.validate_config(config)
        endpoint = self._endpoint(config, "/models")
        started = time.monotonic()
        try:
            payload = self._request_json(
                method="GET",
                url=endpoint,
                timeout=config.timeout_seconds,
            )
            models = self._model_names(payload)
            return ConnectionCheck(
                provider=self.provider_name,
                model=config.model,
                endpoint_ref=endpoint,
                ok=True,
                status="connected",
                latency_ms=self._elapsed_ms(started),
                diagnostics={
                    "model_available": config.model in models,
                    "model_count": len(models),
                    "reference_only": True,
                },
            )
        except Exception as exc:
            return ConnectionCheck(
                provider=self.provider_name,
                model=config.model,
                endpoint_ref=endpoint,
                ok=False,
                status="failed",
                latency_ms=self._elapsed_ms(started),
                diagnostics={"reference_only": True},
                error=str(exc),
            )

    def generate(self, request: LocalAIRequest, config: LocalAIConfig) -> LocalAIResponse:
        self.validate_config(config)
        request.validate()
        endpoint = self._endpoint(config, "/generate")
        started = time.monotonic()
        payload = self._request_json(
            method="POST",
            url=endpoint,
            timeout=request.timeout_seconds or config.timeout_seconds,
            body={"model": request.model, "prompt": request.prompt},
        )
        return self.normalize_response(
            payload,
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
            raise ValueError("invalid reference response: missing string content")

        return LocalAIResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model=str(raw_response.get("model") or config.model),
            content=content,
            status="complete",
            latency_ms=latency_ms,
            finish_reason=str(raw_response.get("finish_reason") or "complete"),
            diagnostics={
                "endpoint_ref": endpoint_ref,
                "reference_only": True,
            },
        )

    def _request_json(
        self,
        method: str,
        url: str,
        timeout: float,
        body: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        """Return deterministic example data without external I/O."""

        del timeout
        if method == "GET" and url.endswith("/models"):
            return {
                "models": [
                    {"name": self.reference_model},
                    {"name": "reference-model-secondary"},
                ]
            }
        if method == "POST" and url.endswith("/generate") and body is not None:
            return {
                "model": body.get("model") or self.reference_model,
                "content": f"Reference response: {body.get('prompt', '')}",
                "finish_reason": "complete",
            }
        raise ValueError("unsupported reference provider request")

    def _model_names(self, payload: Mapping[str, Any]) -> set[str]:
        models = payload.get("models", [])
        return {
            item.get("name")
            for item in models
            if isinstance(item, Mapping) and isinstance(item.get("name"), str)
        }

    def _endpoint(self, config: LocalAIConfig, path: str) -> str:
        return f"{config.normalized_base_url}{path}"

    def _elapsed_ms(self, started: float) -> int:
        return int((time.monotonic() - started) * 1000)
