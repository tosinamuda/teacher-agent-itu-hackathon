"""Project lesson objectives or steps into condition-specific generation units."""

from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.session_plan_view import (
    LessonPlanObjectiveView,
    SessionPlanStepView,
    SessionPlanView,
)

from .evidence import SourceEvidenceProjector
from .schemas import (
    ObjectiveLearnerState,
    SectionGenerationUnit,
    SourceEvidenceItem,
    StepActivityView,
)
from .source_content import (
    instructional_events,
    question_as_asked,
    work_the_step_sets,
)
from .sources import LessonSources

CORE_STEP_KIND = "core"


class SectionGenerationUnitProjector:
    """Map a lesson plan into objective or step units declared by the policy."""

    def __init__(
        self,
        evidence: SourceEvidenceProjector,
        expert_sources: ExpertSources = ExpertSources.LESSON_NOTE,
    ) -> None:
        self._evidence = evidence
        self._expert_sources = expert_sources

    def project(
        self,
        *,
        plan: SessionPlanView,
        policy: ReviewPackGenerationPolicy,
        learner_states: dict[str, ObjectiveLearnerState],
        sources: LessonSources,
    ) -> list[SectionGenerationUnit]:
        plan_evidence = self._evidence.for_plan(sources, policy)
        if policy.context.generation_unit == "objective":
            return [
                self._objective_unit(objective, plan_evidence, learner_states)
                for objective in plan.lesson_plan_objectives
            ]
        objective_text = {
            objective.lesson_objective_id: objective.objective_text
            for objective in plan.lesson_plan_objectives
        }
        assessment_points = self._assessment_points(plan, policy.context.include_assessment_figures)
        return [
            self._step_unit(
                step=step,
                policy=policy,
                objective_text=objective_text,
                evidence=self._expert_evidence(self._lesson_note(step, policy), plan_evidence),
                learner_states=learner_states,
                assessment_points=assessment_points,
                position=position,
            )
            for position, step in enumerate(self._core_steps(plan), start=1)
        ]

    def _lesson_note(
        self, step: SessionPlanStepView, policy: ReviewPackGenerationPolicy
    ) -> list[SourceEvidenceItem]:
        """The step's lesson note, where it has one: its plan's own blocks are not a note."""
        if not (step.note or "").strip():
            return []
        return self._evidence.for_step(step, policy)

    def _expert_evidence(
        self, note: list[SourceEvidenceItem], references: list[SourceEvidenceItem]
    ) -> list[SourceEvidenceItem]:
        """A step's evidence from the expert sources this generation reads."""
        if self._expert_sources is ExpertSources.TEXTBOOK:
            return references
        if self._expert_sources is ExpertSources.BOTH:
            return [*note, *references]
        return note or references

    @staticmethod
    def _core_steps(plan: SessionPlanView) -> list[SessionPlanStepView]:
        return [step for step in plan.steps if step.step_kind == CORE_STEP_KIND]

    @staticmethod
    def _objective_unit(
        objective: LessonPlanObjectiveView,
        evidence: list[SourceEvidenceItem],
        learner_states: dict[str, ObjectiveLearnerState],
    ) -> SectionGenerationUnit:
        return SectionGenerationUnit(
            unit_id=f"objective:{objective.lesson_objective_id}",
            lesson_objective_id=objective.lesson_objective_id,
            objective_text=objective.objective_text or "",
            source_evidence=evidence,
            objective_learner_state=learner_states.get(objective.lesson_objective_id),
        )

    def _step_unit(
        self,
        *,
        step: SessionPlanStepView,
        policy: ReviewPackGenerationPolicy,
        objective_text: dict[str, str | None],
        evidence: list[SourceEvidenceItem],
        learner_states: dict[str, ObjectiveLearnerState],
        assessment_points: dict[str, list[str]],
        position: int,
    ) -> SectionGenerationUnit:
        context = policy.context
        objective_id = step.lesson_objective_id or ""
        return SectionGenerationUnit(
            unit_id=f"step:{step.step_id}",
            lesson_objective_id=objective_id,
            objective_text=objective_text.get(objective_id) or "",
            source_step_id=step.step_id,
            step_title=step.title if context.include_step_title else None,
            step_content=step.content if context.include_step_content else None,
            instructional_type=(
                step.instructional_type if context.include_lesson_step_structure else None
            ),
            current_step=position if context.include_lesson_sequence else None,
            instructional_events=(
                list(instructional_events(step.activities))
                if context.include_instructional_events
                else []
            ),
            student_tasks=(self._student_tasks(step) if context.include_student_tasks else []),
            activities=(
                [StepActivityView.model_validate(item) for item in step.activities]
                if context.include_teacher_student_activities
                else []
            ),
            assessment_points=(
                assessment_points.get(objective_id, []) if context.include_assessment_points else []
            ),
            source_evidence=evidence,
            source_figures=self._evidence.figures_for_step(step, policy, objective_id),
            objective_learner_state=learner_states.get(objective_id),
        )

    @staticmethod
    def _student_tasks(step: SessionPlanStepView) -> list[str]:
        """The work this step sets, however she wrote it down.

        Her practice blocks carry question text. A construction has none — "construct
        angle 90 degrees" IS the whole of what she set — so reading only question-shaped
        blocks lost the field on five of the cohort's seventeen steps, every one of them
        on the two lessons that are mostly construction. See ``work_the_step_sets`` for
        why the activity column can be read without carrying her narration with it.

        A fallback rather than an addition. On every step of the cohort that has both,
        the activity is a label for the questions beside it — "solve some questions
        independently" against four listed questions — so appending it would send a
        contentless second task and say nothing the block has not.
        """
        written = [
            question_as_asked(question)
            for block in step.blocks
            if isinstance(block, dict) and block.get("type") == "practice"
            if (question := str(block.get("question") or "").strip())
        ]
        return written or work_the_step_sets(step.activities)

    @staticmethod
    def _assessment_points(
        plan: SessionPlanView, keep_drawings: bool = False
    ) -> dict[str, list[str]]:
        points: dict[str, list[str]] = {}
        for step in plan.steps:
            if step.step_kind != "evaluation":
                continue
            for block in step.blocks:
                if not isinstance(block, dict):
                    continue
                question = str(block.get("question") or "").strip()
                objective_id = str(block.get("lesson_objective_id") or "").strip()
                if not question or not objective_id:
                    continue
                points.setdefault(objective_id, []).append(
                    question_as_asked(question, keep_drawing=keep_drawings)
                )
        return points
