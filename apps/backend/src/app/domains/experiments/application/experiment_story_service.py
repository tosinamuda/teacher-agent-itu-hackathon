"""Reconstruct an experiment's pipeline as an ordered, log-traceable story.

The story is the dashboard's "what happened, in what order, with what
provenance?" view: lesson plan -> exit diagnostic -> learner band -> class
base pack -> personalised pack -> expert ratings. Each LLM-backed stage is
tagged with the matching generation-log correlation ids so the UI can show
how it was produced; non-LLM stages carry an explanatory note.

Distinct from CRUD/lifecycle (main service), execution (job queueing + H2
run), context assembly, packet export, results summary, and C4 governance —
this is a presentation concern over the generation log. Depends on its experiment
identity and context roles plus the generation log service (for generation-log events).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
    ExperimentContextReader,
)
from app.domains.experiments.domain.records import ExperimentAdministrationRecord
from app.shared.session_plan_view import SessionPlanView

_NOT_RECORDED = "Trace not recorded (generated before logging was enabled)."


class ExperimentStoryReader(Protocol):
    async def get_experiment(self, experiment_id: str) -> ExperimentAdministrationRecord | None: ...


@dataclass(frozen=True)
class _StageTrace:
    """Correlation ids + event count from the generation log for one story stage."""

    correlation_ids: list[str]
    event_count: int


class ExperimentStoryApplicationService:
    """Own the story-DTO assembly for one experiment (read-only, from the generation log)."""

    def __init__(
        self,
        experiments: ExperimentStoryReader,
        context: ExperimentContextReader,
    ) -> None:
        self.experiments = experiments
        self.context = context

    async def build_experiment_story(
        self,
        *,
        db: AsyncSession,
        experiment_id: str,
    ) -> dict[str, object]:
        """Assemble the 6-stage story for the dashboard, tagged with generation-log traces."""
        from app.domains.generation_log.application.service import GenerationLogService

        experiment = await self.experiments.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        context = await ExperimentContextApplicationService(self.context).get_experiment_context(
            experiment=experiment
        )
        if context.plan_version is None:
            raise ExperimentApplicationError(409, "experiment_plan_not_authored")

        session_plan = SessionPlanView.model_validate(context.plan_version.session_plan or {})
        curriculum = {
            "subject": session_plan.subject,
            "grade": session_plan.grade,
            "term": session_plan.term,
            "week": session_plan.week,
            "topic": session_plan.topic,
            "subtopic": session_plan.subtopic,
        }

        generation_log = GenerationLogService(db)
        events = await generation_log.list_for_experiment(
            experiment_id=experiment_id,
            plan_version_id=experiment.plan_version_id,
            session_id=getattr(context.lesson_plan, "session_id", None),
        )

        lp = self._trace_for(events, {"lesson_plan", "lesson_plan_revision"})
        dg = self._trace_for(events, {"diagnostic", "diagnostic_revision"})
        base = self._trace_for(events, {"study_pack_base"})
        cond = self._trace_for(events, {"experiment_condition"})

        stages = [
            self._stage("lesson_plan", "Lesson plan", llm=True, trace=lp),
            self._stage("diagnostic", "Exit diagnostic", llm=True, trace=dg),
            self._stage(
                "learner_state",
                "Learner band",
                llm=False,
                trace=_StageTrace([], 0),
                note="Diagnostic scoring places the learner in a band — no LLM call.",
            ),
            # The base pack falls back to the condition trace so older runs (before
            # the dedicated base-pack event kind) still show provenance.
            self._stage(
                "base",
                "Class base pack",
                llm=True,
                trace=base if base.event_count else cond,
            ),
            self._stage("personalised", "Personalised pack", llm=True, trace=cond),
            self._stage(
                "ratings",
                "Expert ratings",
                llm=False,
                trace=_StageTrace([], 0),
                note="Blinded expert evaluation — no LLM call.",
            ),
        ]

        return {
            "experiment_id": experiment.experiment_id,
            "plan_version_id": experiment.plan_version_id,
            "lesson_title": context.lesson_title,
            "curriculum": curriculum,
            "lesson_plan": context.plan_version.session_plan or None,
            "stages": stages,
        }

    @staticmethod
    def _trace_for(events: list, kinds: set[str]) -> _StageTrace:
        """Collect correlation ids + event count for the given generation-event kinds."""
        correlation_ids: list[str] = []
        count = 0
        for event in events:
            if event.kind not in kinds:
                continue
            count += 1
            if event.correlation_id and event.correlation_id not in correlation_ids:
                correlation_ids.append(event.correlation_id)
        return _StageTrace(correlation_ids=correlation_ids, event_count=count)

    @staticmethod
    def _stage(
        key: str,
        title: str,
        *,
        llm: bool,
        trace: _StageTrace,
        note: str | None = None,
    ) -> dict[str, object]:
        """Render one story stage as a DTO dict, defaulting note to ``_NOT_RECORDED``."""
        return {
            "key": key,
            "title": title,
            "llm": llm,
            "correlation_ids": trace.correlation_ids,
            "event_count": trace.event_count,
            "note": note if note is not None else (None if trace.event_count else _NOT_RECORDED),
        }
