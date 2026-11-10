"""Source evidence must carry real textbook passages, not citation labels.

Plan references are citation strings ending in a record id; resolved excerpts
replace them as the evidence the model grounds in. Unresolved references keep
the citation string (legacy behaviour) so nothing breaks when a record is
missing.
"""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_sources import (
    resolve_lesson_sources,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSource,
    LessonSources,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.expert_content.application.excerpt_resolver import reference_record_id
from app.shared.experiment_enums import Hypothesis
from app.shared.session_plan_view import SessionPlanView

_CITATION = "Chapter 2: Highest common factor and lowest common multiple (ch02-b029)"


def test_reference_record_id_parses_trailing_id() -> None:
    assert reference_record_id(_CITATION) == "ch02-b029"
    assert reference_record_id("A reference without an id") is None
    assert reference_record_id("") is None


def _plan(references: list[str]) -> SessionPlanView:
    # C2 builds step-level units, so the plan needs one core step.
    return SessionPlanView.model_validate(
        {
            "subject": "Mathematics",
            "grade": "JSS1",
            "topic": "LCM",
            "references": references,
            "steps": [
                {
                    "step_id": "s1",
                    "step_kind": "core",
                    "title": "Find the LCM",
                    "content": "List multiples of each number.",
                    "lesson_objective_id": "lop01",
                }
            ],
        }
    )


class _FakeExcerpts:
    """``ExcerptsPort`` stand-in — resolves the one reference that has a record."""

    async def excerpts_for(self, references: Sequence[str]) -> dict[str, str]:
        assert list(references) == [_CITATION, "Teacher handout"]
        return {"ch02-b029": "The resolved textbook passage."}


@pytest.mark.asyncio
async def test_lesson_sources_keep_citation_and_resolved_content() -> None:
    plan = _plan([_CITATION, "Teacher handout"])

    sources = await resolve_lesson_sources(_FakeExcerpts(), plan)

    assert sources.items == (
        LessonSource(
            citation=_CITATION,
            content="The resolved textbook passage.",
            record_id="ch02-b029",
        ),
        LessonSource(citation="Teacher handout", content="Teacher handout"),
    )


def test_resolved_excerpt_replaces_citation_and_keeps_it_as_title() -> None:
    builder = BaseReviewPackRequestBuilder()
    request = builder.build(
        session_plan=_plan([_CITATION]),
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=LessonSources(
            items=(
                LessonSource(
                    citation=_CITATION,
                    content="A multiple is a number that can be divided…",
                    record_id="ch02-b029",
                ),
            )
        ),
    )
    item = request.units[0].source_evidence[0]
    assert item.excerpt == "A multiple is a number that can be divided…"
    assert item.title == _CITATION
    assert item.source_ref == "REF-1"


def test_unresolved_reference_falls_back_to_citation_string() -> None:
    builder = BaseReviewPackRequestBuilder()
    request = builder.build(
        session_plan=_plan([_CITATION]),
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=LessonSources(items=(LessonSource(citation=_CITATION, content=_CITATION),)),
    )
    item = request.units[0].source_evidence[0]
    assert item.excerpt == _CITATION
    assert item.title is None
