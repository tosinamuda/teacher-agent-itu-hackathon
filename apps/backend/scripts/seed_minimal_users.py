"""Seed the minimal persona set onto a freshly-baselined database.

Creates exactly these logins (auth code == the name), with the same
role-driven side effects as admin onboarding (casbin grant; rater profile for
the rater; learner-profile binding for students):

    student-1, student-2, student-3   (bound to fresh JSS1 learner profiles)
    teacher-1                         (workspace assigned later under Setup)
    researcher                        (research_manager — global wildcard)
    rater-1                           (+ EvaluationRater row)
    admin

The JSS1 baseline (``seed_jss1_curriculum``) ships a 10-name sample roster;
this script REPLACES any login-less roster learners in the JSS1 class with the
three bound student profiles, so the class contains exactly the seeded
personas. Idempotent: existing logins are left untouched.

Usage:
    cd apps/backend
    uv run python scripts/seed_minimal_users.py
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from sqlalchemy import delete, select  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

import app.db.metadata  # noqa: F401, E402  (register ORM models)
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.domains.evaluation.infrastructure.models import EvaluationRater  # noqa: E402
from app.domains.evaluation.infrastructure.repository import EvaluationRepository  # noqa: E402
from app.domains.learners.models import LearnerProfile  # noqa: E402
from app.domains.school.models.structure import Class  # noqa: E402
from app.domains.users.application.service import (  # noqa: E402
    UserAlreadyExistsError,
    UserApplicationService,
)
from app.shared.auth import (  # noqa: E402
    ROLE_ADMIN,
    ROLE_RATER,
    ROLE_RESEARCH_MANAGER,
    ROLE_STUDENT,
    ROLE_TEACHER,
)
from app.shared.authz import grant_role_to_user  # noqa: E402
from app.shared.ids import PublicIdPrefix, new_public_id  # noqa: E402

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
logger = logging.getLogger("seed_minimal_users")

PERSONAS: list[tuple[str, str, str]] = [
    # (code, full name, role)
    ("student-1", "Student One", ROLE_STUDENT),
    ("student-2", "Student Two", ROLE_STUDENT),
    ("student-3", "Student Three", ROLE_STUDENT),
    ("teacher-1", "Teacher One", ROLE_TEACHER),
    ("researcher", "Researcher", ROLE_RESEARCH_MANAGER),
    ("rater-1", "Rater One", ROLE_RATER),
    ("admin", "Admin", ROLE_ADMIN),
]


async def _jss1_class(db: AsyncSession) -> Class:
    klass = (await db.execute(select(Class))).scalars().first()
    if klass is None:
        raise SystemExit("no class found — run scripts/seed_jss1_curriculum.py first")
    return klass


async def _replace_roster_with(
    db: AsyncSession, klass: Class, student_codes: list[str]
) -> dict[str, LearnerProfile]:
    """Drop login-less roster learners; ensure one profile per student persona."""
    await db.execute(
        delete(LearnerProfile).where(
            LearnerProfile.class_id == klass.id,
            LearnerProfile.user_id.is_(None),
            LearnerProfile.code.is_(None),
        )
    )
    profiles: dict[str, LearnerProfile] = {}
    for index, code in enumerate(student_codes, start=1):
        existing = (
            (await db.execute(select(LearnerProfile).where(LearnerProfile.code == code)))
            .scalars()
            .first()
        )
        if existing is not None:
            profiles[code] = existing
            continue
        profile = LearnerProfile(
            student_id=new_public_id(PublicIdPrefix.LEARNER),
            full_name=f"Student {('One', 'Two', 'Three')[index - 1]}",
            grade="JSS1",
            track="General",
            class_id=klass.id,
            language_level="simple",
            pace_preference="moderate",
            time_budget_minutes=40,
        )
        db.add(profile)
        profiles[code] = profile
    await db.flush()
    return profiles


async def main() -> None:
    service = UserApplicationService()
    async with AsyncSessionLocal() as db:
        klass = await _jss1_class(db)
        student_codes = [code for code, _, role in PERSONAS if role == ROLE_STUDENT]
        profiles = await _replace_roster_with(db, klass, student_codes)

        for code, full_name, role in PERSONAS:
            try:
                user = await service.create_user(
                    db=db,
                    code=code,
                    email=f"{code}@seed.local",
                    full_name=full_name,
                    role=role,
                )
            except UserAlreadyExistsError:
                # The baseline seed may have created the login (teacher-1) —
                # the casbin grant must still hold, so ensure it idempotently.
                existing = await service.repository.get_user_by_auth_id(db, f"code|{code}")
                if existing is not None:
                    await grant_role_to_user(user_id=existing.id, user_role=role)
                logger.info("%s: already exists — grant ensured", code)
                continue
            # Same invariant as admin onboarding: a user without their grant
            # authenticates but 403s on every authz check.
            await grant_role_to_user(user_id=user.id, user_role=role)
            if role == ROLE_RATER:
                await EvaluationRepository(db).stage_rater(
                    EvaluationRater(
                        rater_id=new_public_id(PublicIdPrefix.EVALUATION_RATER),
                        display_name=full_name,
                        user_id=user.id,
                    )
                )
            if role == ROLE_STUDENT:
                profile = profiles[code]
                profile.user_id = user.id
                profile.code = code
            logger.info("%s: created (%s)", code, role)

        await db.commit()
    logger.info("Minimal personas seeded.")


if __name__ == "__main__":
    asyncio.run(main())
