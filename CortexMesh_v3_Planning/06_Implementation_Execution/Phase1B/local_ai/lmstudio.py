"""LM Studio Local AI provider adapter for Phase 1B."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Mapping

from .config import LocalAIConfig, LocalAIConfigError
from .provider import ConnectionCheck, LocalAIRequest, LocalAIResponse


class LMStudioProvider:
    """Provider adapter for LM Studio's OpenAI-compatible local API."""

    provider_name = "lmstudio"

    def name(self) -> str:
        return self.provider_name

    def validate_config(self, config: LocalAIConfig) -> None:
        config.validate({self.provider_name})

    def check_connection(self, config: LocalAIConfig) -> ConnectionCheck:
        self.validate_config(config)
        endpoint = self._endpoint(config, "models_path", "/v1/models")
        started = time.monotonic()
        try:
            payload = self._request_json(
                method="GET",
                url=endpoint,
                timeout=config.timeout_seconds,
            )
            latency_ms = self._elapsed_ms(started)
            model_names = self._model_names(payload)
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
        endpoint = self._endpoint(config, "chat_completions_path", "/v1/chat/completions")
        timeout = request.timeout_seconds or config.timeout_seconds
        body: dict[str, Any] = {
            "model": request.model or config.model,
            "messages": self._messages(request, config),
        }
        temperature = request.temperature if request.temperature is not None else config.temperature
        if temperature is not None:
            body["temperature"] = temperature
        max_tokens = request.max_tokens if request.max_tokens is not None else config.max_tokens
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

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
        choices = raw_response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("invalid LM Studio response: missing choices")
        first_choice = choices[0]
        if not isinstance(first_choice, Mapping):
            raise ValueError("invalid LM Studio response: malformed choice")
        message = first_choice.get("message")
        if not isinstance(message, Mapping):
            raise ValueError("invalid LM Studio response: missing message")
        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("invalid LM Studio response: missing string content")

        finish_reason = first_choice.get("finish_reason")
        usage = raw_response.get("usage")
        return LocalAIResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model=str(raw_response.get("model") or config.model),
            content=content,
            status="complete" if finish_reason else "partial",
            latency_ms=latency_ms,
            usage=usage if isinstance(usage, Mapping) else {},
            finish_reason=str(finish_reason) if finish_reason is not None else None,
            diagnostics={
                "endpoint_ref": endpoint_ref,
                "choice_count": len(choices),
            },
        )

    def _messages(
        self,
        request: LocalAIRequest,
        config: LocalAIConfig,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        system_prompt = request.system_prompt or config.system_prompt
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        return messages

    def _model_names(self, payload: Mapping[str, Any]) -> set[str]:
        data = payload.get("data", [])
        return {
            item.get("id")
            for item in data
            if isinstance(item, Mapping) and isinstance(item.get("id"), str)
        }

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
