"""A lesson's published transcripts as the app keeps them, one row each."""

from __future__ import annotations

from app.domains.experiments.infrastructure.study_transcript_models import StudyTranscript
from experiments.study_import.lessons import learner_id
from experiments.study_import.transcripts import PublishedTranscript, pages_of


def transcript_rows(
    transcripts: list[PublishedTranscript], plan_version_id: str
) -> list[StudyTranscript]:
    return [
        StudyTranscript(
            plan_version_id=plan_version_id,
            kind=transcript.kind,
            student_id=learner_id(transcript.pseudonym) if transcript.pseudonym else None,
            pages=pages_of(transcript.header),
            header=transcript.header,
            body=transcript.body,
            source_path=transcript.path,
            sha256=transcript.sha256,
        )
        for transcript in transcripts
    ]
