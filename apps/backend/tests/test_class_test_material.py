"""The class test is a registered kind, and its generator is told what the registry says."""

from __future__ import annotations

import asyncio

import dspy

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.assessments.application.diagnostic_generator import (
    DiagnosticMCQItem,
    GenerateDiagnosticItemsSignature,
)
from app.domains.assessments.application.diagnostic_service import (
    ClassTestLesson,
    DiagnosticGenerationService,
)
from app.shared.session_plan_view import LessonPlanObjectiveView


class _RecordingGenerator:
    def __init__(self) -> None:
        self.briefs: list[ArtefactSpec] = []

    async def generate(self, *, brief: ArtefactSpec, **_: object) -> list[DiagnosticMCQItem]:
        self.briefs.append(brief)
        return [
            DiagnosticMCQItem(
                stem="2 + 3 × 4 = ?",
                options={"A": "20", "B": "14", "C": "24", "D": "9"},
                correct_option="B",
                distractor_misconceptions={"A": "add_before_multiply", "C": "x", "D": "y"},
                difficulty="easy",
            )
        ]


CLASS_TEST = seed_specification(ArtefactType.DIAGNOSTIC.value)


def test_the_class_test_is_seeded_class_level_and_never_adapted() -> None:
    assert CLASS_TEST.levels == frozenset({ArtefactScope.CLASS_LEVEL})
    assert CLASS_TEST.adaptable == ()


def test_every_objective_is_generated_against_the_registered_brief() -> None:
    generator = _RecordingGenerator()
    service = DiagnosticGenerationService(generator=generator)  # type: ignore[arg-type]
    objectives = [
        LessonPlanObjectiveView(lesson_objective_id=f"LO-{n}", objective_text=f"objective {n}")
        for n in (1, 2)
    ]

    payloads = asyncio.run(
        service._build_item_payloads(
            specification=CLASS_TEST,
            objectives=objectives,
            subtopic_id="sub-1",
            plan_version_id="LPV-1",
            lesson=ClassTestLesson(
                taught="", subject="Mathematics", grade="JSS1", topic="Order of operations"
            ),
            item_count=1,
        )
    )

    assert len(payloads) == 2
    assert generator.briefs == [CLASS_TEST.brief("a junior secondary student aged about 11-13")] * 2


def test_the_rendered_prompt_carries_every_registered_requirement() -> None:
    predictor = dspy.ChainOfThought(GenerateDiagnosticItemsSignature)
    messages = dspy.ChatAdapter().format(
        predictor.predict.signature,
        demos=[],
        inputs={
            "artefact_spec": CLASS_TEST.brief("a junior secondary student aged about 11-13"),
            "objective_text": "Use the order of operations",
            "subject": "Mathematics",
            "grade": "JSS1",
            "topic": "Order of operations",
            "item_count": 2,
        },
    )
    user = messages[-1]["content"]

    assert CLASS_TEST.material in user
    for requirement in CLASS_TEST.requirements:
        assert requirement.replace('"', '\\"') in user
