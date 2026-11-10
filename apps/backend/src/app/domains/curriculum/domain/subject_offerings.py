from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class SubjectSlotRules(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_subjects: int = Field(..., ge=1)
    compulsory_subjects: int = Field(..., ge=1)
    field_core_subjects: int = Field(..., ge=1)
    trade_subjects: int = Field(..., ge=0)
    notes: list[str] = Field(default_factory=list)


class SubjectCatalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    curriculum: str | None = None
    subject_slots: SubjectSlotRules
    core_compulsory_subjects: list[str] = Field(default_factory=list)
    fields_of_study: dict[str, list[str]] = Field(default_factory=dict)
    trade_subjects: list[str] = Field(default_factory=list)


_FALLBACK_CATALOG = SubjectCatalog(
    curriculum="Senior Secondary Curriculum Offering",
    subject_slots=SubjectSlotRules(
        total_subjects=9,
        compulsory_subjects=5,
        field_core_subjects=3,
        trade_subjects=1,
        notes=[
            "Compulsory list includes the 'One Trade Subject' slot.",
            "Trade subject is selected from trade_subjects and fills that slot.",
        ],
    ),
    core_compulsory_subjects=[
        "English Language",
        "General Mathematics",
        "Citizenship and Heritage Studies",
        "Digital Technologies",
        "One Trade Subject",
    ],
    fields_of_study={
        "Science": [
            "Biology",
            "Chemistry",
            "Physics",
            "Agriculture",
            "Further Mathematics",
            "Physical Education",
            "Health Education",
            "Foods & Nutrition",
            "Geography",
            "Technical Drawing",
        ],
        "Humanities": [
            "Nigerian History",
            "Government",
            "Christian Religious Studies",
            "Islamic Studies",
            "One Nigerian language",
            "French",
            "Arabic",
            "Visual Arts",
            "Music",
            "Literature in English",
            "Home Management",
            "Catering craft",
        ],
        "Business": [
            "Accounting",
            "Commerce",
            "Marketing",
            "Economics",
        ],
    },
    trade_subjects=[
        "Solar Photovoltaic installation and maintenance",
        "Fashion design and garment making",
        "Livestock farming",
        "Beauty and cosmetology",
        "Computer hardware and GSM repairs",
        "Horticulture and crop production",
    ],
)


def _find_catalog_path() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "docs" / "data" / "ss-subjects.json"
        if candidate.exists():
            return candidate
    return None


def load_subject_catalog() -> SubjectCatalog:
    path = _find_catalog_path()
    if path is None:
        return _FALLBACK_CATALOG
    try:
        return SubjectCatalog.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValidationError):
        return _FALLBACK_CATALOG


def validate_student_subject_profile(
    *,
    field_of_study: str | None,
    trade_subject: str | None,
    field_core_subjects: list[str] | None,
) -> list[str]:
    catalog = load_subject_catalog()
    errors: list[str] = []

    if field_of_study is None and trade_subject is None and field_core_subjects is None:
        return errors

    if field_of_study is None:
        errors.append("field_of_study_required")
        return errors

    if field_of_study not in catalog.fields_of_study:
        errors.append("field_of_study_invalid")
        return errors

    if trade_subject is None:
        errors.append("trade_subject_required")
    elif trade_subject not in set(catalog.trade_subjects):
        errors.append("trade_subject_invalid")

    if field_core_subjects is None:
        errors.append("field_core_subjects_required")
        return errors

    normalized_subjects = [subject.strip() for subject in field_core_subjects]
    if len(normalized_subjects) != 3:
        errors.append("field_core_subjects_must_be_three")
    if len(set(normalized_subjects)) != len(normalized_subjects):
        errors.append("field_core_subjects_duplicate")

    allowed_subjects = set(catalog.fields_of_study[field_of_study])
    if any(subject not in allowed_subjects for subject in normalized_subjects):
        errors.append("field_core_subjects_invalid")
    return errors
