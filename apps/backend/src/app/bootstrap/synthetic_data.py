from __future__ import annotations

import logging
import random
from datetime import date
from typing import TypedDict

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.learners.models import LearnerProfile
from app.domains.school.models import (
    AcademicYear,
    Class,
    Course,
    GradeLevel,
    School,
    Subject,
    TermClassSubject,
)
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace
from app.domains.users.models import User
from app.shared.ids import PublicIdPrefix, new_public_id

logger = logging.getLogger(__name__)

DEMO_SCHOOL_CODE = "DEMO"
DEMO_SCHOOL_NAME = "Plan-to-Tutor Demo School"

TEACHER_SEEDS = [
    {
        "code": "uncle-tosin",
        "name": "Uncle Tosin",
        "subject": "Mathematics",
        "role": "research_manager",
    },
    {"code": "aunty-blessing", "name": "Aunty Blessing", "subject": "English Language"},
    {"code": "dr-chika", "name": "Dr. Chika", "subject": "Physics"},
    {
        "code": "synthetic-teacher-1",
        "auth_id": "auth0|synthetic-teacher-1",
        "name": "Mr. Synthetic",
        "subject": "Mathematics",
    },
    # Platform admin — manages schools/workspaces/learners/users; teaches nothing,
    # so it gets no workspace (no "subject"). Audit-separated from the researcher.
    {"code": "admin", "name": "Platform Admin", "role": "admin"},
]

# Roles that teach a class and therefore get a demo workspace seeded.
_WORKSPACE_SEED_ROLES = frozenset({"teacher", "research_manager"})

APP_SUBJECTS = [
    {"name": "Mathematics", "code": "MATH", "category": "Science", "is_compulsory": True},
    {"name": "English Language", "code": "ENG", "category": "Arts", "is_compulsory": True},
    {"name": "Physics", "code": "PHY", "category": "Science", "is_compulsory": False},
    {"name": "Chemistry", "code": "CHEM", "category": "Science", "is_compulsory": False},
    {"name": "Biology", "code": "BIO", "category": "Science", "is_compulsory": False},
]

GRADE_LEVELS = ["JSS1", "SS1", "SS2", "SS3"]


class GradeSeedConfig(TypedDict):
    grade: str
    is_primary: bool
    seed_weeks: bool
    terms: list[str]


class SyntheticDataSeeder:
    """Seeds optional demo-only data without touching the canonical JSS1 baseline."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def seed(self) -> list[User]:
        await self._seed_metadata()

        seeded_teachers: list[User] = []
        for teacher_seed in TEACHER_SEEDS:
            auth_id = teacher_seed.get("auth_id", f"code|{teacher_seed['code']}")
            email = f"{teacher_seed['code']}@school.com"
            teacher = await self._get_teacher_by_auth_id(auth_id)

            role = teacher_seed.get("role", "teacher")
            if teacher is None:
                logger.info("Seeding teacher %s", teacher_seed["name"])
                teacher = User(
                    auth_id=auth_id,
                    email=email,
                    full_name=teacher_seed["name"],
                    role=role,
                )
                self.db.add(teacher)
                await self.db.commit()
                await self.db.refresh(teacher)
            elif teacher.role != role:
                teacher.role = role
                await self.db.commit()
                await self.db.refresh(teacher)
            else:
                logger.info("Teacher %s already exists", teacher_seed["name"])

            # Only teaching roles get a demo workspace; admin teaches nothing.
            if role in _WORKSPACE_SEED_ROLES and teacher_seed.get("subject"):
                await self._seed_workspaces(teacher=teacher, subject_name=teacher_seed["subject"])
            seeded_teachers.append(teacher)

        return seeded_teachers

    async def _seed_metadata(self) -> None:
        result = await self.db.execute(select(AcademicYear))
        if result.scalars().first() is None:
            self.db.add(
                AcademicYear(
                    name="2024/2025",
                    start_date=date(2024, 9, 1),
                    end_date=date(2025, 7, 31),
                    is_current=True,
                )
            )

        max_sequence_result = await self.db.execute(
            select(func.coalesce(func.max(GradeLevel.sequence), 0))
        )
        next_sequence = int(max_sequence_result.scalar() or 0) + 1

        for grade_name in GRADE_LEVELS:
            grade_result = await self.db.execute(
                select(GradeLevel).where(GradeLevel.name == grade_name)
            )
            if grade_result.scalars().first() is None:
                self.db.add(GradeLevel(name=grade_name, sequence=next_sequence))
                next_sequence += 1

        for subject_seed in APP_SUBJECTS:
            subject_result = await self.db.execute(
                select(Subject).where(Subject.code == subject_seed["code"])
            )
            if subject_result.scalars().first() is None:
                self.db.add(Subject(**subject_seed, is_trade=False))

        await self.db.commit()

    async def _get_teacher_by_auth_id(self, auth_id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.auth_id == auth_id))
        return result.scalars().first()

    async def _seed_workspaces(self, *, teacher: User, subject_name: str) -> None:
        logger.info("Seeding workspaces for %s", teacher.full_name)

        subject = await self._find_subject(subject_name)
        if subject is None:
            logger.error("Subject %s not found for demo seed", subject_name)
            return
        school = await self._get_or_create_school()

        grade_configs: list[GradeSeedConfig] = [
            {
                "grade": "JSS1",
                "is_primary": False,
                "seed_weeks": False,
                "terms": ["First Term", "Second Term", "Third Term"],
            },
            {
                "grade": "SS1",
                "is_primary": True,
                "seed_weeks": True,
                "terms": ["First Term"],
            },
            {
                "grade": "SS2",
                "is_primary": False,
                "seed_weeks": True,
                "terms": ["First Term"],
            },
        ]

        for config in grade_configs:
            grade = await self._get_grade_level(config["grade"])
            if grade is None:
                continue

            course = await self._get_or_create_course(subject=subject, grade=grade)
            klass = await self._get_or_create_class(
                name=f"DEMO-{config['grade']}",
                grade=grade,
                school=school,
            )

            for term_name in config["terms"]:
                subject_offering = await self._get_or_create_subject_offering(
                    course=course,
                    classroom=klass,
                    term_name=term_name,
                    seed_weeks=config["seed_weeks"],
                )
                await self._get_or_create_workspace(
                    teacher=teacher,
                    subject_offering=subject_offering,
                    is_primary=config["is_primary"] and term_name == "First Term",
                )

            await self._seed_learners(klass=klass, count=5, name_suffix=config["grade"])

    async def _find_subject(self, subject_name: str) -> Subject | None:
        exact_match = await self.db.execute(select(Subject).where(Subject.name == subject_name))
        subject = exact_match.scalars().first()
        if subject is not None:
            return subject

        fuzzy_match = await self.db.execute(
            select(Subject).where(Subject.name.ilike(f"%{subject_name}%"))
        )
        return fuzzy_match.scalars().first()

    async def _get_grade_level(self, grade_name: str) -> GradeLevel | None:
        result = await self.db.execute(select(GradeLevel).where(GradeLevel.name == grade_name))
        return result.scalars().first()

    async def _get_or_create_course(self, *, subject: Subject, grade: GradeLevel) -> Course:
        result = await self.db.execute(
            select(Course).where(
                Course.subject_id == subject.id,
                Course.grade_level_id == grade.id,
            )
        )
        course = result.scalars().first()
        if course is not None:
            return course

        course = Course(
            name=f"{grade.name} {subject.name}",
            subject_id=subject.id,
            grade_level_id=grade.id,
        )
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def _get_or_create_school(self) -> School:
        result = await self.db.execute(select(School).where(School.code == DEMO_SCHOOL_CODE))
        school = result.scalars().first()
        if school is not None:
            return school

        school = School(name=DEMO_SCHOOL_NAME, code=DEMO_SCHOOL_CODE)
        self.db.add(school)
        await self.db.commit()
        await self.db.refresh(school)
        return school

    async def _get_or_create_class(
        self,
        *,
        name: str,
        grade: GradeLevel,
        school: School,
    ) -> Class:
        result = await self.db.execute(
            select(Class).where(
                Class.name == name,
                Class.grade_level_id == grade.id,
                Class.school_id == school.id,
            )
        )
        klass = result.scalars().first()
        if klass is not None:
            return klass

        klass = Class(name=name, grade_level_id=grade.id, school_id=school.id)
        self.db.add(klass)
        await self.db.commit()
        await self.db.refresh(klass)
        return klass

    async def _get_or_create_workspace(
        self,
        *,
        teacher: User,
        subject_offering: TermClassSubject,
        is_primary: bool,
    ) -> TeacherWorkspace:
        result = await self.db.execute(
            select(TeacherWorkspace).where(
                TeacherWorkspace.teacher_id == teacher.id,
                TeacherWorkspace.term_class_subject_id == subject_offering.id,
            )
        )
        workspace = result.scalars().first()
        if workspace is not None:
            return workspace

        workspace = TeacherWorkspace(
            teacher_id=teacher.id,
            term_class_subject_id=subject_offering.id,
            is_primary=is_primary,
            settings=None,
        )
        self.db.add(workspace)
        await self.db.commit()
        await self.db.refresh(workspace)
        return workspace

    async def _seed_learners(self, *, klass: Class, count: int, name_suffix: str) -> None:
        grade_name = "SS1"
        if klass.grade_level_id:
            grade = await self.db.get(GradeLevel, klass.grade_level_id)
            if grade is not None:
                grade_name = grade.name

        for index in range(count):
            full_name = f"Learner {name_suffix}-{index + 1}"
            existing = await self.db.execute(
                select(LearnerProfile).where(LearnerProfile.full_name == full_name)
            )
            if existing.scalars().first() is not None:
                continue

            learner = LearnerProfile(
                student_id=new_public_id(PublicIdPrefix.LEARNER),
                full_name=full_name,
                grade=grade_name,
                track="General",
                class_id=klass.id,
                field_of_study="Science" if random.choice([True, False]) else "Arts",
                language_level="standard",
                pace_preference="moderate",
                time_budget_minutes=45,
            )
            self.db.add(learner)

        await self.db.commit()

    async def _get_or_create_subject_offering(
        self,
        *,
        course: Course,
        classroom: Class,
        term_name: str,
        seed_weeks: bool,
    ) -> TermClassSubject:
        result = await self.db.execute(
            select(TermClassSubject).where(
                TermClassSubject.course_id == course.id,
                TermClassSubject.class_id == classroom.id,
                TermClassSubject.term == term_name,
            )
        )
        subject_offering = result.scalars().first()
        if subject_offering is None:
            subject_offering = TermClassSubject(
                course_id=course.id,
                class_id=classroom.id,
                term=term_name,
                year="2024/2025",
            )
            self.db.add(subject_offering)
            await self.db.commit()
            await self.db.refresh(subject_offering)

        if seed_weeks:
            await self._seed_scheme_of_work(subject_offering=subject_offering)
        return subject_offering

    async def _seed_scheme_of_work(self, *, subject_offering: TermClassSubject) -> None:
        existing_week = await self.db.execute(
            select(SchemeOfWork).where(SchemeOfWork.term_class_subject_id == subject_offering.id)
        )
        if existing_week.scalars().first() is not None:
            return

        for week_number in range(1, 3):
            week = SchemeOfWork(
                term_class_subject_id=subject_offering.id,
                week_number=week_number,
                title=f"Week {week_number}",
                objectives=None,
            )
            self.db.add(week)
            await self.db.flush()

            for period_number in range(1, 3):
                self.db.add(
                    LessonPeriod(
                        scheme_of_work_id=week.id,
                        period_number=period_number,
                        title=f"Period {period_number}",
                        subtopic_id=None,
                    )
                )

        await self.db.commit()
