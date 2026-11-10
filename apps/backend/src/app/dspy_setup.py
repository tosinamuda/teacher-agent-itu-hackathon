"""The API process's model client and the callbacks every model call passes through."""

from __future__ import annotations

import logging

import dspy

from app.config import CONFIG
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    DspyStatusLogger,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.status import (
    DspyStatusMessageProvider,
)
from app.domains.generation_log.application import GenerationLogRecorder
from app.infra.dspy_lm import build_dspy_lm

_STATUS_LOGGER = "app.domains.artefacts.types.lesson_plan.drafting.application.runtime.status"


def configure_dspy() -> None:
    """Point dspy at the generator model, logging progress and recording every call.

    Idempotent: each callback is installed once.
    """
    callbacks = list(getattr(dspy.settings, "callbacks", []) or [])
    if CONFIG.lesson_plan.dspy_status_logging and not _has(callbacks, DspyStatusLogger):
        callbacks.append(
            DspyStatusLogger(
                logger=logging.getLogger(_STATUS_LOGGER), provider=DspyStatusMessageProvider()
            )
        )
    if CONFIG.log_model_calls and not _has(callbacks, GenerationLogRecorder):
        callbacks.append(GenerationLogRecorder())
    dspy.configure(lm=build_dspy_lm(), callbacks=callbacks)
    if CONFIG.lesson_plan.rlm_verbose:
        logging.getLogger("dspy.predict.rlm").setLevel(logging.INFO)


def _has(callbacks: list[object], kind: type) -> bool:
    return any(isinstance(callback, kind) for callback in callbacks)
