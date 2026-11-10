"""Regression: GET /learners?class_id=<uuid> is MySQL-safe.

``LearnerProfile.class_id`` is a UUID column (CHAR(32) on MySQL). The list filter
received ``class_id`` straight from the query string as a ``str`` and bound it to
that column, which on MySQL raised ``'str' object has no attribute 'hex'`` (the
same class as the synthetic-student bug; Postgres' driver had coerced it). The
create/update paths coerced via ``_optional_uuid`` but this list path was missed.
These pin the fix against the MySQL test DB.
"""

from __future__ import annotations

import uuid

import pytest

from app.domains.learners.application import (
    LearnerApplicationError,
    LearnerApplicationService,
)

pytestmark = pytest.mark.asyncio


async def test_list_learners_accepts_str_class_id(db) -> None:
    # str class_id (as the query param delivers it) must bind to the UUID column
    # without the MySQL '.hex' crash; no learner matches → empty result.
    rows, total = await LearnerApplicationService().list_learners(
        db=db,
        grade=None,
        track=None,
        class_id=str(uuid.uuid4()),
        field_of_study=None,
        page=1,
        page_size=10,
    )
    assert total == 0
    assert rows == []


async def test_list_learners_rejects_malformed_class_id(db) -> None:
    # A malformed class_id is a clean 422, not an unhandled 500.
    with pytest.raises(LearnerApplicationError) as info:
        await LearnerApplicationService().list_learners(
            db=db,
            grade=None,
            track=None,
            class_id="not-a-uuid",
            field_of_study=None,
            page=1,
            page_size=10,
        )
    assert info.value.status_code == 422
