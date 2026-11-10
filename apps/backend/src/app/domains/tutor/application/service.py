from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.models.events import Event
from app.domains.tutor.infrastructure.repository import TutorRepository
from app.domains.tutor.schemas import TutorQueryResponse
from app.domains.tutor.services.tutor_answer_service import TutorAnswerService
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.review_pack_view import ReviewPackManifestView, ReviewPackStepView


@dataclass(frozen=True)
class TutorApplicationError(Exception):
    status_code: int
    detail: str


class TutorApplicationService:
    def __init__(
        self,
        repository: TutorRepository | None = None,
        tutor_service: TutorAnswerService | None = None,
    ) -> None:
        self.repository = repository or TutorRepository()
        self.tutor_service = tutor_service or TutorAnswerService()

    async def answer_question(
        self,
        *,
        db: AsyncSession,
        artefact_id: str,
        step_id: str,
        question: str,
    ) -> TutorQueryResponse:
        review_pack = await self.repository.get_review_pack(db, artefact_id)
        if review_pack is None:
            raise TutorApplicationError(404, "artefact_not_found")

        manifest = self._manifest(review_pack.manifest)
        step = self._find_step(manifest, step_id)
        if step is None:
            response = TutorQueryResponse(
                answer="I can only help with the current step in this pack.",
                citations=[],
                refusal=True,
                reason="step_not_found",
            )
        else:
            try:
                response = await self.tutor_service.answer_question(
                    review_pack=manifest,
                    step=step,
                    question=question,
                )
            except ValueError as exc:
                raise TutorApplicationError(502, str(exc)) from exc

        await self.repository.save_event(
            db,
            Event(
                event_id=new_public_id(PublicIdPrefix.EVENT),
                student_id=None,
                artefact_id=artefact_id,
                event_type="tutor_query",
                payload={"question": question, "response": response.model_dump()},
                event_timestamp=datetime.now(timezone.utc),
            ),
        )
        return response

    def _manifest(self, payload: object) -> ReviewPackManifestView:
        if not isinstance(payload, dict):
            raise TutorApplicationError(500, "pack_manifest_invalid")
        try:
            return ReviewPackManifestView.model_validate(payload)
        except Exception as exc:
            raise TutorApplicationError(500, "pack_manifest_invalid") from exc

    def _find_step(
        self,
        manifest: ReviewPackManifestView,
        step_id: str,
    ) -> ReviewPackStepView | None:
        for step in manifest.steps:
            if step.step_id == step_id:
                return step
        return None
