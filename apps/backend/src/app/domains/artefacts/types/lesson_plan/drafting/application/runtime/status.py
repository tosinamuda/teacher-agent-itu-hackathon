from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from time import perf_counter

from dspy.streaming import StatusMessageProvider
from dspy.utils.callback import BaseCallback


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def log_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def dspy_signature_name(instance: object) -> str:
    signature = getattr(instance, "signature", None)
    if signature is None:
        return instance.__class__.__name__
    return (
        getattr(signature, "__name__", None)
        or getattr(signature, "name", None)
        or instance.__class__.__name__
    )


class DspyStatusMessageProvider(StatusMessageProvider):
    def module_start_status_message(self, instance: object, inputs: dict[str, object]) -> str:
        class_name = instance.__class__.__name__
        signature_name = dspy_signature_name(instance)
        if class_name == "RLM":
            return f"DSPy status: RLM {signature_name} started"
        if class_name == "Predict":
            return f"DSPy status: Predict {signature_name} started"
        return f"DSPy status: Module {class_name} started"

    def module_end_status_message(self, outputs: object) -> str:
        return "DSPy status: module finished"

    def lm_start_status_message(self, instance: object, inputs: dict[str, object]) -> str:
        return "DSPy status: LM call started"

    def lm_end_status_message(self, outputs: object) -> str:
        return "DSPy status: LM call finished"

    def tool_start_status_message(self, instance: object, inputs: dict[str, object]) -> str:
        tool_name = getattr(instance, "name", instance.__class__.__name__)
        return f"DSPy status: tool {tool_name} started"

    def tool_end_status_message(self, outputs: object) -> str:
        return "DSPy status: tool finished"


class DspyStatusLogger(BaseCallback):
    def __init__(
        self,
        *,
        logger: logging.Logger,
        provider: StatusMessageProvider | None = None,
    ) -> None:
        self.logger = logger
        self.provider = provider or DspyStatusMessageProvider()
        self._module_calls: dict[str, tuple[str, float]] = {}
        self._lm_calls: dict[str, tuple[str, float]] = {}
        self._completed_lm_calls = 0
        self._adapter_format_calls: dict[str, tuple[str, float]] = {}
        self._adapter_parse_calls: dict[str, tuple[str, float, bool]] = {}
        self._tool_calls: dict[str, tuple[str, float]] = {}

    def _safe_keys(self, payload: object) -> str:
        if isinstance(payload, dict):
            return ",".join(sorted(str(key) for key in payload.keys())[:8])
        return "-"

    def _info(self, message: str, *args: object) -> None:
        self.logger.info("%s " + message, log_timestamp(), *args)

    def _warning(self, message: str, *args: object) -> None:
        self.logger.warning("%s " + message, log_timestamp(), *args)

    def on_module_start(self, call_id: str, instance: object, inputs: dict[str, object]) -> None:
        label = f"{instance.__class__.__name__}[{dspy_signature_name(instance)}]"
        self._module_calls[call_id] = (label, perf_counter())
        if message := self.provider.module_start_status_message(instance, inputs):
            self._info("%s label=%s input_keys=%s", message, label, self._safe_keys(inputs))

    def on_module_end(
        self,
        call_id: str,
        outputs: object | None,
        exception: Exception | None = None,
    ) -> None:
        label, started_at = self._module_calls.pop(call_id, ("Module", perf_counter()))
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        if exception is not None:
            self._warning(
                "DSPy status: %s failed elapsed_ms=%s error=%s",
                label,
                elapsed_ms,
                exception,
            )
            return
        if message := self.provider.module_end_status_message(outputs):
            self._info("%s label=%s elapsed_ms=%s", message, label, elapsed_ms)

    def on_lm_start(self, call_id: str, instance: object, inputs: dict[str, object]) -> None:
        label = str(getattr(instance, "model", None) or instance.__class__.__name__)
        self._lm_calls[call_id] = (label, perf_counter())
        if message := self.provider.lm_start_status_message(instance, inputs):
            self._info("%s model=%s input_keys=%s", message, label, self._safe_keys(inputs))

    def on_lm_end(
        self,
        call_id: str,
        outputs: dict[str, object] | None,
        exception: Exception | None = None,
    ) -> None:
        label, started_at = self._lm_calls.pop(call_id, ("LM", perf_counter()))
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        if exception is not None:
            self._warning(
                "DSPy status: LM %s failed elapsed_ms=%s error=%s",
                label,
                elapsed_ms,
                exception,
            )
            return
        if message := self.provider.lm_end_status_message(outputs):
            self._info(
                "%s model=%s elapsed_ms=%s output_keys=%s",
                message,
                label,
                elapsed_ms,
                self._safe_keys(outputs),
            )
        self._completed_lm_calls += 1

    def lm_call_count(self) -> int:
        return self._completed_lm_calls

    def on_adapter_format_start(
        self, call_id: str, instance: object, inputs: dict[str, object]
    ) -> None:
        label = instance.__class__.__name__
        self._adapter_format_calls[call_id] = (label, perf_counter())
        self._info(
            "DSPy status: adapter format started adapter=%s input_keys=%s",
            label,
            self._safe_keys(inputs),
        )

    def on_adapter_format_end(
        self,
        call_id: str,
        outputs: dict[str, object] | None,
        exception: Exception | None = None,
    ) -> None:
        label, started_at = self._adapter_format_calls.pop(call_id, ("Adapter", perf_counter()))
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        if exception is not None:
            self._warning(
                "DSPy status: adapter format failed adapter=%s elapsed_ms=%s error=%s",
                label,
                elapsed_ms,
                exception,
            )
            return
        self._info(
            "DSPy status: adapter format finished adapter=%s elapsed_ms=%s output_keys=%s",
            label,
            elapsed_ms,
            self._safe_keys(outputs),
        )

    def on_adapter_parse_start(
        self, call_id: str, instance: object, inputs: dict[str, object]
    ) -> None:
        label = instance.__class__.__name__
        fallback_enabled = bool(getattr(instance, "use_json_adapter_fallback", False))
        self._adapter_parse_calls[call_id] = (label, perf_counter(), fallback_enabled)
        self._info(
            "DSPy status: adapter parse started adapter=%s input_keys=%s",
            label,
            self._safe_keys(inputs),
        )

    def on_adapter_parse_end(
        self,
        call_id: str,
        outputs: dict[str, object] | None,
        exception: Exception | None = None,
    ) -> None:
        label, started_at, fallback_enabled = self._adapter_parse_calls.pop(
            call_id,
            ("Adapter", perf_counter(), False),
        )
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        if exception is not None:
            if label == "ChatAdapter" and fallback_enabled:
                self._info(
                    "DSPy status: adapter parse fallback adapter=%s "
                    "elapsed_ms=%s error=%s fallback=JSONAdapter",
                    label,
                    elapsed_ms,
                    exception,
                )
                return
            self._warning(
                "DSPy status: adapter parse failed adapter=%s elapsed_ms=%s error=%s",
                label,
                elapsed_ms,
                exception,
            )
            return
        self._info(
            "DSPy status: adapter parse finished adapter=%s elapsed_ms=%s output_keys=%s",
            label,
            elapsed_ms,
            self._safe_keys(outputs),
        )

    def on_tool_start(self, call_id: str, instance: object, inputs: dict[str, object]) -> None:
        label = getattr(instance, "name", instance.__class__.__name__)
        self._tool_calls[call_id] = (label, perf_counter())
        if message := self.provider.tool_start_status_message(instance, inputs):
            self._info("%s label=%s input_keys=%s", message, label, self._safe_keys(inputs))

    def on_tool_end(
        self,
        call_id: str,
        outputs: dict[str, object] | None,
        exception: Exception | None = None,
    ) -> None:
        label, started_at = self._tool_calls.pop(call_id, ("Tool", perf_counter()))
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        if exception is not None:
            self._warning(
                "DSPy status: tool failed label=%s elapsed_ms=%s error=%s",
                label,
                elapsed_ms,
                exception,
            )
            return
        if message := self.provider.tool_end_status_message(outputs):
            self._info(
                "%s label=%s elapsed_ms=%s output_keys=%s",
                message,
                label,
                elapsed_ms,
                self._safe_keys(outputs),
            )
