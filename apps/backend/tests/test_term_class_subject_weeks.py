import uuid
from datetime import date

import pytest
from sqlalchemy import text

from app.domains.school.models.core import AcademicYear, Term
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationService
from app.domains.teaching.models import SchemeOfWork


async def _offering(db, term: str, year: str) -> uuid.UUID:  # type: ignore[no-untyped-def]
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    offering_id = uuid.uuid4()
    db.add_all(
        [
            TermClassSubject(
                id=offering_id, course_id=uuid.uuid4(), class_id=uuid.uuid4(), term=term, year=year
            ),
            SchemeOfWork(
                id=uuid.uuid4(), term_class_subject_id=offering_id, week_number=1, title="Fractions"
            ),
            SchemeOfWork(
                id=uuid.uuid4(), term_class_subject_id=offering_id, week_number=3, title="Decimals"
            ),
        ]
    )
    await db.flush()
    return offering_id


@pytest.mark.asyncio
async def test_each_week_carries_its_date_from_the_term_it_belongs_to(db) -> None:  # type: ignore[no-untyped-def]
    year = AcademicYear(
        id=uuid.uuid4(), name="2099/2100", start_date=date(2099, 9, 1), end_date=date(2100, 7, 1)
    )
    db.add_all(
        [
            year,
            Term(
                id=uuid.uuid4(),
                name="1st Term",
                academic_year_id=year.id,
                start_date=date(2099, 9, 14),
                end_date=date(2099, 12, 11),
            ),
        ]
    )
    offering_id = await _offering(db, "1st Term", "2099/2100")

    response = await TeachingSequenceApplicationService().get_term_class_subject_by_id(
        db=db, term_class_subject_id=offering_id
    )

    assert [(w.week_number, w.starts_on) for w in response.weeks] == [
        (1, date(2099, 9, 14)),
        (3, date(2099, 9, 28)),
    ]
    assert response.current_week_number is None


@pytest.mark.asyncio
async def test_weeks_have_no_date_when_the_school_has_not_set_the_term(db) -> None:  # type: ignore[no-untyped-def]
    offering_id = await _offering(db, "3rd Term", "1999/2000")

    response = await TeachingSequenceApplicationService().get_term_class_subject_by_id(
        db=db, term_class_subject_id=offering_id
    )

    assert [w.starts_on for w in response.weeks] == [None, None]
    assert response.current_week_number is None
