"""The brief a review-pack section is written to, read from the pack's specification."""

from app.domains.artefacts.core.domain.specification import ArtefactSpec, ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification
from app.shared.readers import reader_for

from .schemas import LessonContextForGeneration

_CURRICULA = {"JSS": "the Nigerian UBE junior secondary (NERDC) mathematics curriculum"}


def learner_setting(context: LessonContextForGeneration) -> str:
    """Name the curriculum a section is written for."""
    grade = (context.grade_level or "").strip().upper()
    curriculum = next((text for prefix, text in _CURRICULA.items() if grade.startswith(prefix)), "")
    return f"{grade or 'unstated grade'}, {curriculum}" if curriculum else grade


def revision_pack_spec(
    grade_level: str, specification: ContentSpecification | None = None
) -> ArtefactSpec:
    """The take-home revision-pack brief for one grade band.

    ``specification`` is the stored revision the app read from the database. Without one
    the seed revision is used — the brief the evaluated study sent, word for word.
    """
    pack = specification or seed_specification(ArtefactType.POST_CLASS_REVIEW_PACK.value)
    if pack.kind != ArtefactType.POST_CLASS_REVIEW_PACK.value:
        raise ValueError(f"not_a_revision_pack_specification:{pack.kind}")
    return pack.brief(reader_for(grade_level))
