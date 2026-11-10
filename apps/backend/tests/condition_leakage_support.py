"""Canary plans + fake LLMs shared by the two condition-leakage suites.

``test_condition_leakage_downstream`` asks whether condition-forbidden context
can reach a rater; ``test_condition_run_isolation`` asks whether one condition
run can rewrite another's record. Both need the same two things.

**Canaries.** Every plan-derived string carries a unique token tagged with the
CLASS of lesson-plan context it belongs to (``CYSTEP0007Z`` is step context,
``CYEVID0011Z`` is textbook evidence, ...). A leak is then found by scanning the
final JSON for token classes, not by knowing in advance which field to inspect —
so a new field added anywhere downstream is covered without editing the test.

**Fake LLM.** ``EchoModel`` regurgitates its ENTIRE input into the section it
returns and invents a textbook figure on top. Real models do regurgitate context,
so this is the strongest probe available: whatever a condition's request carries
shows up verbatim in that condition's pack, and whatever the request withholds
cannot appear no matter how badly the model misbehaves.
"""

from __future__ import annotations

import itertools
import json
import os
import random
import re
from dataclasses import dataclass
from typing import Protocol

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSource,
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionCritic,
    SectionGenerator,
    SectionPersonaliser,
    SectionRepairer,
    SectionReviser,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    CheckResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ValidationCheck,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    normalise_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    SectionCollaborators,
)
from app.shared.session_plan_view import SessionPlanView

# Context classes a canary token can belong to.
OBJECTIVE = "OBJ"  # lesson objective text — every condition may use it
GLOBAL = "GLOBAL"  # subject/grade/topic/term/theme — every condition may use it
STEP = "STEP"  # lesson-plan step context — C1 and up
EVIDENCE = "EVID"  # textbook citation + resolved passage — C2 and up
FIGURE = "FIG"  # grounded figure url/caption/record id — C2 and up
OUTLINE = "OUTLINE"  # the plan's step titles in order — conditions carrying the outline
DESIGN = "DESIGN"  # entry behaviour + lesson materials — the plan-design conditions
PLAN_ONLY = "PLAN"  # plan fields no condition's request carries — never allowed
ROGUE = "ROGUE"  # invented by the model — never allowed

ROGUE_FIGURE_URL = "https://hallucinated.example/CYROGUE9001Z.png"

_TOKEN = re.compile(r"CY([A-Z]+)\d{4}Z")


def classes_in(payload: object) -> set[str]:
    """Every canary CLASS present anywhere in ``payload``, however deeply nested."""
    text = json.dumps(payload, sort_keys=True, default=str)
    return {match.group(1) for match in _TOKEN.finditer(text)}


@dataclass(frozen=True)
class CanaryPlan:
    """A lesson plan whose every field and resolved source is traceable."""

    view: SessionPlanView
    sources: LessonSources = LessonSources()
    figure_urls: tuple[str, ...] = ()


class _Tokens:
    """Hands out one unique token per plan field, tagged with its context class."""

    def __init__(self) -> None:
        self._counter = itertools.count(1)

    def __call__(self, context_class: str) -> str:
        return f"CY{context_class}{next(self._counter):04d}Z"


def build_canary_plan(rng: random.Random) -> CanaryPlan:
    """A randomly shaped but fully canaried session plan.

    Always carries at least one objective, one core step, one reference and one
    grounded figure, so a condition that is SUPPOSED to surface a context class
    can be asserted positively rather than passing vacuously.
    """
    token = _Tokens()
    objectives = [
        {"lesson_objective_id": f"lop{index:02d}", "objective_text": f"Master {token(OBJECTIVE)}"}
        for index in range(1, rng.randint(1, 3) + 1)
    ]
    steps: list[dict[str, object]] = []
    figure_urls: list[str] = []
    for objective_index, objective in enumerate(objectives):
        for repeat in range(rng.randint(1, 2)):
            with_figure = not figure_urls or rng.random() < 0.5
            url = f"https://figures.example/{token(FIGURE)}.png" if with_figure else None
            if url:
                figure_urls.append(url)
            steps.append(
                _canary_step(
                    step_id=f"s{objective_index}{repeat}",
                    objective_id=str(objective["lesson_objective_id"]),
                    token=token,
                    figure_url=url,
                    rng=rng,
                )
            )
    steps.append(
        # Never a generation unit (only "core" steps are), so its canaries must
        # not appear in ANY condition's pack.
        {
            "step_id": "s-exit",
            "step_kind": "evaluation",
            "title": f"Exit {token(OUTLINE)}",
            "content": f"Quiz {token(PLAN_ONLY)}",
        }
    )
    references: list[str] = []
    sources: list[LessonSource] = []
    for index in range(1, rng.randint(1, 3) + 1):
        record_id = f"ch01-b{index:03d}"
        citation = f"Chapter {token(EVIDENCE)} ({record_id})"
        references.append(citation)
        sources.append(
            LessonSource(
                citation=citation,
                content=f"Passage {token(EVIDENCE)}",
                record_id=record_id,
            )
        )
    view = SessionPlanView.model_validate(
        {
            "subject": f"Maths {token(GLOBAL)}",
            "grade": f"JSS {token(GLOBAL)}",
            "topic": f"Topic {token(GLOBAL)}",
            "subtopic": f"Subtopic {token(GLOBAL)}",
            "term": f"Term {token(GLOBAL)}",
            "theme": f"Theme {token(GLOBAL)}",
            "week": rng.randint(1, 12),
            "track": f"Track {token(PLAN_ONLY)}",
            "title": f"Lesson {token(PLAN_ONLY)}",
            "misconceptions": [f"Believes {token(PLAN_ONLY)}"],
            "entry_behaviour": [f"Knows {token(DESIGN)}"],
            "instructional_materials": [f"Ruler {token(DESIGN)}"],
            "curriculum_objectives": [{"objective_text": f"Curriculum {token(PLAN_ONLY)}"}],
            "lesson_plan_objectives": objectives,
            "steps": steps,
            "references": references,
        }
    )
    return CanaryPlan(
        view=view,
        sources=LessonSources(items=tuple(sources)),
        figure_urls=tuple(figure_urls),
    )


def _canary_step(
    *,
    step_id: str,
    objective_id: str,
    token: _Tokens,
    figure_url: str | None,
    rng: random.Random,
) -> dict[str, object]:
    blocks: list[dict[str, object]] = [
        {"id": f"{step_id}-b0", "type": "explanation", "content": f"Explain {token(STEP)}"}
    ]
    if figure_url:
        blocks.append(
            {
                "id": f"{step_id}-fig",
                "type": "visual",
                "variant": "image",
                "url": figure_url,
                "caption": f"Figure {token(FIGURE)}",
                "source_record_id": f"rec-{token(FIGURE)}",
            }
        )
    return {
        "step_id": step_id,
        "step_kind": "core",
        "lesson_objective_id": objective_id,
        # Withheld from every condition now: the title paraphrases the objective,
        # content duplicates the activities, and instructional_type is a lossy
        # parse of the note. What C1 receives is the Gagne-coded activities and
        # the tasks they set — so the STEP canary rides those.
        "title": f"Step {token(PLAN_ONLY)}",
        "content": f"Teach {token(PLAN_ONLY)}",
        "instructional_type": f"type-{token(PLAN_ONLY)}",
        "kc_type": f"kc-{token(PLAN_ONLY)}",
        "estimated_minutes": rng.randint(5, 20),
        "activities": [
            {"who": "teacher", "what": f"Demonstrate {token(STEP)}"},
            {"who": "student", "what": f"Practise {token(STEP)}"},
        ],
        # The teacher's note for this step — the source scoped retrieval cites.
        "note": f"Worked example: {token(EVIDENCE)}",
        "blocks": [
            *blocks,
            {
                "id": f"{step_id}-task",
                "type": "practice",
                "question": f"Find {token(STEP)}",
                "answer": f"Answer {token(PLAN_ONLY)}",
            },
        ],
    }


class EchoModel:
    """Generator + personaliser stand-in that echoes its whole context back.

    Mirrors the real DSPy modules exactly: it echoes the fields the matching
    signature declares (never more), routes the result through the production
    ``normalise_section``, and — like a misbehaving model — authors a ``visual``
    block of its own and mislabels the section's ids.

    ``bad_refs_first_call`` cites a ref that is not in the evidence, which fails
    C3's deterministic validation and drives the real repair pass.
    """

    def __init__(self, *, marker: str = "", bad_refs_first_call: bool = False) -> None:
        self.marker = marker
        self.bad_refs_first_call = bad_refs_first_call
        self.generated: list[str] = []
        self.repaired: list[str] = []
        self.personalised: list[str] = []

    async def generate_pack(self, *, request: ReviewPackRequest) -> list[ReviewPackSection]:
        return [await self.generate_section(request=request, unit=unit) for unit in request.units]

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        first = unit.unit_id not in self.generated
        self.generated.append(unit.unit_id)
        echoed = {
            "policy": request.policy.model_dump(mode="json"),
            "lesson_context": request.lesson_context.model_dump(mode="json"),
            "unit_context": unit.model_dump(mode="json"),
            "source_evidence": [item.model_dump(mode="json") for item in unit.source_evidence],
        }
        refs = [] if (first and self.bad_refs_first_call) else _refs(unit)
        return normalise_section(self._section(echoed, refs), unit)

    async def repair_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        failed_section: ReviewPackSection,
        issues: list[str],
    ) -> ReviewPackSection:
        self.repaired.append(unit.unit_id)
        echoed = {
            "policy": request.policy.model_dump(mode="json"),
            "lesson_context": request.lesson_context.model_dump(mode="json"),
            "unit_context": unit.model_dump(mode="json"),
            "source_evidence": [item.model_dump(mode="json") for item in unit.source_evidence],
            "failed_section": failed_section.model_dump(mode="json"),
            "validation_issues": issues,
        }
        return normalise_section(self._section(echoed, _refs(unit)), unit)

    async def personalise_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        self.personalised.append(unit.unit_id)
        signals = request.session_signals
        echoed = {
            "personalisation_policy": request.policy.model_dump(mode="json"),
            "lesson_context": request.lesson_context.model_dump(mode="json"),
            "base_section": base_section.model_dump(mode="json"),
            "learner_state": learner_state.model_dump(mode="json"),
            "session_signals": signals.model_dump(mode="json") if signals else None,
            "source_evidence": [item.model_dump(mode="json") for item in unit.source_evidence],
        }
        return normalise_section(self._section(echoed, _refs(unit)), unit)

    def _section(self, echoed: dict[str, object], refs: list[str]) -> ReviewPackSection:
        return ReviewPackSection(
            # Deliberately wrong ids: normalise_section must overwrite them.
            section_id="model-authored-section",
            title=f"Model section {self.marker}".strip(),
            lesson_objective_id="model-authored-objective",
            blocks=[
                ReviewPackBlock(
                    block_id="",
                    block_type="explanation",
                    text=f"{self.marker} {json.dumps(echoed, sort_keys=True)}".strip(),
                    lesson_objective_id="model-authored-objective",
                    source_refs=refs,
                ),
                ReviewPackBlock(
                    block_id="",
                    block_type="visual",
                    lesson_objective_id="model-authored-objective",
                    variant="image",
                    url=ROGUE_FIGURE_URL,
                    caption="Figure copied from the textbook",
                    source_record_id="rec-hallucinated",
                ),
            ],
        )


def _refs(unit: SectionGenerationUnit) -> list[str]:
    return [item.source_ref for item in unit.source_evidence]


class SilentCritic:
    """A critic that finds nothing, so the prose checks never reach an LM.

    These suites ask what CONTEXT reaches a pack, not whether its prose is any
    good. The real critic reads every section with an LM; left at its default
    the whole family would need network access to answer a question about
    payloads.
    """

    async def review(
        self,
        *,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        checks: tuple[ValidationCheck, ...],
    ) -> list[CheckResult]:
        return [CheckResult(check=check, passed=True) for check in checks]


class GenerationModelDouble(
    SectionGenerator,
    SectionRepairer,
    SectionPersonaliser,
    Protocol,
):
    """The three generation roles implemented by deterministic test models."""


def stand_in_collaborators(
    model: GenerationModelDouble,
    *,
    critic: SectionCritic | None = None,
    reviser: SectionReviser | None = None,
) -> SectionCollaborators:
    """Every model-backed seam answered by one deterministic stand-in."""
    return SectionCollaborators(
        generator=model,
        repairer=model,
        personaliser=model,
        critic=critic or SilentCritic(),
        reviser=reviser,
    )


def fuzz_seeds(*default: int) -> list[int]:
    """The seeds a canary-fuzz test runs over.

    A handful by default — enough to catch a reintroduced leak on every commit.
    ``LEAKAGE_SEEDS=n`` turns the same test into a campaign over n distinct
    plans, so widening the search costs an env var rather than an edit.
    """
    wanted = int(os.environ.get("LEAKAGE_SEEDS", "0"))
    if wanted <= len(default):
        return list(default)
    return list(range(1, wanted + 1))
