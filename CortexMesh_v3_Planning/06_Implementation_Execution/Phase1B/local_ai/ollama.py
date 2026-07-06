"""Ollama Local AI provider adapter for Phase 1B."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Mapping

from .config import LocalAIConfig, LocalAIConfigError
from .provider import ConnectionCheck, LocalAIRequest, LocalAIResponse


class OllamaProvider:
    """Provider adapter that isolates Ollama-specific transport details."""

    provider_name = "ollama"

    def name(self) -> str:
        return self.provider_name

    def validate_config(self, config: LocalAIConfig) -> None:
        config.validate({self.provider_name})

    def check_connection(self, config: LocalAIConfig) -> ConnectionCheck:
        self.validate_config(config)
        endpoint = self._endpoint(config, "tags_path", "/api/tags")
        started = time.monotonic()
        try:
            payload = self._request_json(
                method="GET",
                url=endpoint,
                timeout=config.timeout_seconds,
            )
            latency_ms = self._elapsed_ms(started)
            models = payload.get("models", []) if isinstance(payload, dict) else []
            model_names = {
                item.get("name")
                for item in models
                if isinstance(item, dict) and isinstance(item.get("name"), str)
            }
            model_available = config.model in model_names if model_names else None
            return ConnectionCheck(
                provider=self.provider_name,
                model=config.model,
                endpoint_ref=endpoint,
                ok=True,
                status="connected",
                latency_ms=latency_ms,
                diagnostics={
                    "model_available": model_available,
                    "model_count": len(model_names),
                },
            )
        except Exception as exc:  # pragma: no cover - exercised by live provider checks
            return ConnectionCheck(
                provider=self.provider_name,
                model=config.model,
                endpoint_ref=endpoint,
                ok=False,
                status="failed",
                latency_ms=self._elapsed_ms(started),
                error=str(exc),
            )

    def generate(self, request: LocalAIRequest, config: LocalAIConfig) -> LocalAIResponse:
        self.validate_config(config)
        request.validate()
        endpoint = self._endpoint(config, "generate_path", "/api/generate")
        timeout = request.timeout_seconds or config.timeout_seconds
        body: dict[str, Any] = {
            "model": request.model or config.model,
            "prompt": request.prompt,
            "stream": False,
        }
        if request.system_prompt or config.system_prompt:
            body["system"] = request.system_prompt or config.system_prompt
        options: dict[str, Any] = {}
        temperature = request.temperature if request.temperature is not None else config.temperature
        if temperature is not None:
            options["temperature"] = temperature
        max_tokens = request.max_tokens if request.max_tokens is not None else config.max_tokens
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        if options:
            body["options"] = options

        started = time.monotonic()
        payload = self._request_json(
            method="POST",
            url=endpoint,
            timeout=timeout,
            body=body,
        )
        latency_ms = self._elapsed_ms(started)
        return self.normalize_response(payload, request, config, endpoint, latency_ms)

    def normalize_response(
        self,
        raw_response: Mapping[str, Any],
        request: LocalAIRequest,
        config: LocalAIConfig,
        endpoint_ref: str,
        latency_ms: int,
    ) -> LocalAIResponse:
        content = raw_response.get("response")
        if not isinstance(content, str):
            raise ValueError("invalid Ollama response: missing string response")
        done = raw_response.get("done")
        return LocalAIResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model=str(raw_response.get("model") or config.model),
            content=content,
            status="complete" if done is True else "partial",
            latency_ms=latency_ms,
            finish_reason="done" if done is True else None,
            diagnostics={
                "endpoint_ref": endpoint_ref,
                "provider_status": done,
            },
        )

    def _endpoint(self, config: LocalAIConfig, option_name: str, default_path: str) -> str:
        path = config.provider_options.get(option_name, default_path)
        if not isinstance(path, str) or not path.startswith("/"):
            raise LocalAIConfigError(f"{option_name} must be an absolute path")
        return f"{config.normalized_base_url}{path}"

    def _request_json(
        self,
        method: str,
        url: str,
        timeout: float,
        body: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            url=url,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"provider HTTP error {exc.code}: {details}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"provider connection error: {exc.reason}") from exc

    def _elapsed_ms(self, started: float) -> int:
        return int((time.monotonic() - started) * 1000)
