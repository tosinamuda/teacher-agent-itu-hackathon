"""Targeted repair: only failing sections, only their issues, no plan leak.

The original repair loop regenerated EVERY section whenever anything failed
(wasted calls, risk of breaking fine sections), fed each repair all sections'
issues, and — for P1 — passed units carrying raw lesson-plan step content,
smuggling the lesson plan back into the personalisation path.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.decisions import (
    implicated_objectives,
    issues_for_section,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    CheckResult,
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    unit_for_personalisation_repair,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)


def _section(objective_id: str, text: str = "x", refs: list[str] | None = None):
    return ReviewPackSection(
        section_id=f"objective:{objective_id}",
        title="t",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text=text,
                lesson_objective_id=objective_id,
                source_refs=refs or [],
            )
        ],
    )


def test_implicated_objectives_points_at_failing_sections_only() -> None:
    validation = ValidationResult(
        passed=False,
        checks=[
            CheckResult(check="objective_preservation", passed=True),
            CheckResult(
                check="scope_compliance",
                passed=False,
                details={"out_of_scope": ["lop02"]},
            ),
        ],
    )
    sections = [_section("lop01"), _section("lop02")]
    assert implicated_objectives(validation, sections) == {"lop02"}


def test_invalid_refs_implicate_the_citing_section() -> None:
    validation = ValidationResult(
        passed=False,
        checks=[
            CheckResult(
                check="source_refs_valid",
                passed=False,
                details={"invalid_refs": ["REF-9"], "allowed_count": 3},
            )
        ],
    )
    sections = [_section("lop01", refs=["REF-9"]), _section("lop02", refs=["REF-1"])]
    assert implicated_objectives(validation, sections) == {"lop01"}


def test_unattributable_failure_falls_back_to_repair_all() -> None:
    validation = ValidationResult(
        passed=False,
        checks=[
            # A dropped objective can't be fixed by editing existing sections;
            # with nothing attributable the caller repairs everything (None).
            CheckResult(
                check="objective_preservation", passed=False, details={"dropped": ["lop03"]}
            )
        ],
    )
    assert implicated_objectives(validation, [_section("lop01")]) is None


def test_p1_repair_unit_strips_lesson_plan_steps() -> None:
    unit = SectionGenerationUnit(
        unit_id="step:s1",
        lesson_objective_id="lop01",
        objective_text="Find the LCM",
        source_step_id="s1",
        step_title="Teach LCM",
        step_content="Raw lesson plan step content",
        instructional_type="core",
        estimated_minutes=10,
        activities=[
            {"who": "teacher", "what": "explain"},
            {"who": "student", "what": "listen"},
        ],
    )
    stripped = unit_for_personalisation_repair(unit, _section("lop01"))
    assert stripped.step_content is None
    assert stripped.step_title is None
    assert stripped.activities == []
    assert stripped.objective_text == "Find the LCM"  # the objective survives


def test_issues_filtered_per_section() -> None:
    issues = [
        "generated content is attributed to the textbook/source — lop02: 'mirrors the textbook'",
        "refs not in provided evidence: ['REF-9']",  # unattributed -> everyone sees it
    ]
    assert issues_for_section("lop01", ["lop01", "lop02"], issues) == [issues[1]]
    assert issues_for_section("lop02", ["lop01", "lop02"], issues) == issues
