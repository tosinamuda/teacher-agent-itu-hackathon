"""Write and revise a lesson note with DSPy."""

from __future__ import annotations

import dspy
from dspy.utils.exceptions import AdapterParseError

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.lesson_note.application.draft import NoteLesson, NoteStepInput
from app.domains.artefacts.lesson_note.application.errors import UnreadableReplyError
from app.domains.artefacts.lesson_note.domain.note import NoteSection, NoteStepDraft


class WriteNoteStep(dspy.Signature):
    """Write the part of the lesson note artefact_spec describes, for ONE lesson step.

    Follow every requirement in artefact_spec exactly. Draw only on the lesson and the
    step you are given.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(desc="The brief to follow exactly.")
    lesson: NoteLesson = dspy.InputField(desc="The lesson this step belongs to.")
    step: NoteStepInput = dspy.InputField(desc="The plan step to write the note for.")
    part: NoteStepDraft = dspy.OutputField(desc="This step's part of the note.")


class ReviseLessonNote(dspy.Signature):
    """Apply the teacher's instruction to the lesson note.

    Change only what the instruction asks for, in the section it points to if it points to
    one. Keep every other section word for word, and keep following every requirement in
    artefact_spec. Return every section, with its step_id, in the same order.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(desc="The brief the note follows.")
    current_sections: list[NoteSection] = dspy.InputField(desc="The note as it stands.")
    highlighted_section: str = dspy.InputField(desc="The section the teacher pointed to, if any.")
    instruction: str = dspy.InputField(desc="What the teacher wants changed.")
    revised_sections: list[NoteSection] = dspy.OutputField(
        desc="Every section as markdown, revised where the instruction asks, in the same order."
    )
    change_summary: str = dspy.OutputField(desc="One sentence saying what changed.")


class DSPyNoteStepWriter:
    """One chain-of-thought call per step."""

    def __init__(self, *, lm: dspy.BaseLM) -> None:
        self._lm = lm
        self._write = dspy.ChainOfThought(WriteNoteStep)

    async def write(
        self, *, brief: ArtefactSpec, lesson: NoteLesson, step: NoteStepInput, draw: int = 0
    ) -> NoteStepDraft:
        config = {"rollout_id": draw} if draw else {}
        with dspy.settings.context(lm=self._lm):
            result = await self._write.acall(
                artefact_spec=brief, lesson=lesson, step=step, config=config
            )
        part: NoteStepDraft = result.part
        return part


#: A reply that cannot be read is asked for once more, as a new draw, before the revision fails.
REVISION_REPLY_ATTEMPTS = 2


class DSPyLessonNoteReviser:
    """One chain-of-thought call over the whole note."""

    def __init__(self, *, lm: dspy.BaseLM) -> None:
        self._lm = lm
        self._revise = dspy.ChainOfThought(ReviseLessonNote)

    async def revise(
        self,
        *,
        brief: ArtefactSpec,
        current_sections: list[NoteSection],
        highlighted_section: str,
        instruction: str,
    ) -> tuple[list[NoteSection], str]:
        unreadable: AdapterParseError | None = None
        for attempt in range(REVISION_REPLY_ATTEMPTS):
            config = {"rollout_id": attempt} if attempt else {}
            try:
                with dspy.settings.context(lm=self._lm):
                    result = await self._revise.acall(
                        artefact_spec=brief,
                        current_sections=current_sections,
                        highlighted_section=highlighted_section,
                        instruction=instruction,
                        config=config,
                    )
            except AdapterParseError as error:
                unreadable = error
                continue
            return list(result.revised_sections), str(result.change_summary)
        raise UnreadableReplyError(
            f"the reply was not readable after {REVISION_REPLY_ATTEMPTS} attempts"
        ) from unreadable
