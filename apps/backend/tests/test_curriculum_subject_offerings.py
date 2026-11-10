from app.domains.curriculum.domain import (
    load_subject_catalog,
    validate_student_subject_profile,
)


def test_subject_catalog_loads_trade_subjects_and_fields() -> None:
    catalog = load_subject_catalog()

    assert catalog.fields_of_study
    assert catalog.trade_subjects
    assert catalog.subject_slots.total_subjects >= 1


def test_validate_student_subject_profile_uses_curriculum_policy() -> None:
    assert (
        validate_student_subject_profile(
            field_of_study="Science",
            trade_subject="Computer hardware and GSM repairs",
            field_core_subjects=["Biology", "Chemistry", "Physics"],
        )
        == []
    )

    assert validate_student_subject_profile(
        field_of_study="Science",
        trade_subject="Invalid Trade Subject",
        field_core_subjects=["Biology", "Chemistry", "Physics"],
    ) == ["trade_subject_invalid"]
